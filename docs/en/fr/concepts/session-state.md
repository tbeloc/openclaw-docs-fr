---
summary: "Journal durable des signaux d'état de session : versions d'état, observateurs, avis d'état obsolète et réconciliation"
read_when:
  - Vous voulez que les agents remarquent quand des humains ou d'autres agents modifient une session à leur insu
  - Vous déboguez des avis de changement d'état, des curseurs de surveillance ou des modifications de session_status changesSince
  - Vous voulez comprendre comment les agents parents restent synchronisés avec les sessions enfants
title: "Sensibilisation à l'état de la session"
sidebarTitle: "Sensibilisation à l'état de la session"
---

Quand plusieurs sessions travaillent sur le même problème — un gestionnaire déléguant à des enfants, un humain accédant directement à une session de travail, deux agents se coordonnant via [`sessions_send`](/fr/concepts/session-tool) — chaque session construit des hypothèses sur les autres. Ces hypothèses deviennent obsolètes dès qu'un autre acteur intervient. La sensibilisation à l'état de la session est le mécanisme qui détecte l'intervention, en informe la session affectée une seule fois, et lui donne un moyen peu coûteux de se rattraper avant d'agir.

Trois éléments travaillent ensemble :

1. Un **journal de signaux durable** enregistre les changements d'état sélectionnés par session.
2. Les **observateurs** maintiennent des curseurs par cible et reçoivent un avis d'état obsolète coalescé.
3. La **réconciliation** extrait le delta exact via `session_status` avec `changesSince`.

## Le journal de signaux

OpenClaw ajoute un événement typé à la base de données d'état partagée (`session_state_events`) quand une session observée change matériellement. Les événements portent des métadonnées et un résumé d'une ligne — jamais le contenu des messages.

| Type                   | Enregistré quand                                                    | Notifie les observateurs |
| ---------------------- | ------------------------------------------------------------------- | ------------------------ |
| `human_direct_message` | Un humain envoie un tour directement à une session observée          | Oui                      |
| `goal_changed`         | L'état d'objectif de la session est créé, mis à jour ou effacé      | Oui                      |
| `child_spawned`        | Une session enfant de sous-agent ou ACP est créée                   | Non (initialise curseur) |
| `run_completed`        | Une exécution enfant se termine avec succès                         | Non (journal uniquement) |
| `run_failed`           | Une exécution enfant échoue, expire ou est annulée                  | Non (journal uniquement) |
| `compacted`            | L'historique de la session est compacté                             | Non (journal uniquement) |

Chaque événement nomme son acteur (`human`, `agent` ou `system`). Les exécutions enfants annulées et expirées sont enregistrées comme des échecs avec le résultat précis (`cancelled`, `timeout` ou `error`) préservé dans la charge utile de l'événement.

La **version d'état** d'une session est simplement le plus haut numéro de séquence dans son journal, suivi dans une tête durable par session qui survit à l'élagage. Les lignes `sessions_list` incluent `stateVersion` quand une session a enregistré des changements ; `session_status` le rapporte toujours.

Les types journal uniquement existent pour l'historique de réconciliation, pas pour la notification : la livraison ordinaire de fin d'exécution enfant reste la responsabilité des [annonces de sous-agents](/fr/tools/subagents), et le journal de signaux ne la duplique jamais.

## Observateurs

Un observateur est une session qui maintient un curseur (`session_watch_cursors`) sur une cible. Les curseurs proviennent de deux endroits :

- **Implicite (arêtes de génération).** Quand une session génère un sous-agent ou un enfant ACP, le curseur du parent est initialisé automatiquement à la version de génération de l'enfant. Les parents ne s'abonnent jamais manuellement.
- **Explicite (`sessions_send watch: true`).** N'importe quel coordinateur peut observer une cible non générée : passez `watch: true` sur `sessions_send`, et après que l'envoi se soit distribué avec succès, l'expéditeur est enregistré comme observateur de la session qui a réellement reçu le message. L'enregistrement commence à la version d'état actuelle de la cible — l'historique antérieur ne produit jamais d'avis. Le résultat de l'outil rapporte `watched: true|false` quand le paramètre a été défini.

L'identité de l'observateur doit être une clé de session qualifiée par agent. Sous `session.scope="global"` la clé `global` partagée est ambiguë entre les agents, donc ces sessions obtiennent le journal durable et `changesSince` mais pas d'avis proactifs.

Les observations se nettoient elles-mêmes : les lignes de curseur expirent avec la rétention du journal de signaux, sont supprimées quand la session observatrice se réinitialise, et sont supprimées avec l'une ou l'autre session. Il n'y a pas de verbe unwatch en v1.

## Avis : un seul, pas plusieurs

Quand un événement éligible à la notification arrive et que le curseur d'un observateur est en retard, l'observateur reçoit un avis système sur son prochain tour :

```
Session "agent:main:subagent:child" changed (other actor). Reconcile before acting: session_status sessionKey "agent:main:subagent:child" changesSince 12.
```

Les observateurs de session principale sont également réveillés immédiatement via un battement de cœur ; les observateurs de sous-agent imbriqués reçoivent l'avis sur leur prochain tour.

Le protocole est délibérément anti-spam :

- **Un avis en attente par paire observateur/cible.** Le texte de l'avis est stable en octets en attente et la file d'attente d'événements système le déduplique, donc vingt changements rapides à la même cible produisent toujours une seule ligne dans l'invite de l'observateur.
- **Marque d'eau gelée.** Le curseur gèle sa position notifiée quand un avis est mis en file d'attente. Les événements matériels supplémentaires avancent uniquement la marque d'eau matérielle ; ils ne re-notifient pas.
- **Accusé de réception à l'épuisement, réouverture uniquement pour le travail entrelacé.** Quand le tour de l'observateur consomme l'avis, le curseur avance. Si plus d'événements matériels sont arrivés entre la mise en file d'attente et l'épuisement, exactement un avis frais est ouvert pour le reste.
- **Auto-suppression.** Un observateur ne reçoit jamais de notification sur les événements qu'il a causés lui-même.
- **Récupération au redémarrage.** Les avis en attente vivent dans une file d'attente en mémoire ; un balayage au démarrage les re-matérialise à partir de curseurs durables après un redémarrage de passerelle.

## Réconciliation

L'avis dit à l'observateur exactement quoi faire. `session_status` avec `changesSince: <version>` retourne les événements typés après cette version (jusqu'à 200), sans avancer aucun curseur :

```json
{
  "stateVersion": 19,
  "stateChanges": {
    "events": [
      {
        "sequence": 14,
        "kind": "human_direct_message",
        "actorType": "human",
        "summary": "human message via telegram"
      },
      { "sequence": 19, "kind": "goal_changed", "actorType": "human", "summary": "goal updated" }
    ],
    "historyGap": false
  }
}
```

`historyGap: true` signifie que la version demandée est antérieure à l'historique conservé — actualisez l'état de session entier (`sessions_history`, `session_status`) au lieu de traiter la réponse comme un delta exact. Le signal d'écart est exact : il provient d'une marque d'eau élagée par session, pas déduit de l'arithmétique de séquence.

## Stockage et limites

L'historique vit dans la base de données d'état partagée, limité à 30 jours et 50 000 lignes ; les têtes par session restent monotones après élagage. L'enregistrement est au mieux — un ajout échoué est enregistré et ne fait jamais échouer le tour d'origine — donc `stateVersion` est une tête de journal de signaux, pas une version de capture de données de changement transactionnelle.

Limites actuelles :

- La livraison d'avis suppose qu'un processus de passerelle possède la base de données d'état partagée. Plusieurs passerelles partagent le journal durable et `changesSince`, mais v1 ne pousse pas les avis entre les processus.
- Les événements de compaction couvrent les propriétaires de compaction du runtime intégré ; la compaction native-harness uniquement n'est pas entièrement enregistrée.
- Le détail de la charge utile de résultat annulé est actuellement produit par les exécutions enfants ACP ; les annulations de sous-agent natif apparaissent comme des échecs génériques.

## Connexes

- [Outils de session](/fr/concepts/session-tool) — `sessions_send`, `session_status`, `sessions_list`
- [Sous-agents](/fr/tools/subagents) — arêtes de génération et annonces de fin
- [Battement de cœur](/fr/gateway/heartbeat) — comment les avis en file d'attente réveillent les sessions principales
- [Gestion de session](/fr/concepts/session) — clés de session, portées, cycle de vie
