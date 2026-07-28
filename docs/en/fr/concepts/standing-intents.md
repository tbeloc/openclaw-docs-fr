---
summary: "Mémoriser les actions futures conditionnées par des événements sans dépendre d'un long contexte conversationnel"
title: "Intentions permanentes"
read_when:
  - You want the agent to act when a future event appears
  - You are choosing between a scheduled task and an event trigger
  - You want to inspect or cancel a standing intent
---

Une intention permanente est une instruction conditionnée par un événement, par exemple « quand le candidat à la version est mentionné, rappelle-moi de vérifier la propriété du retour en arrière ». OpenClaw la stocke dans la base de données SQLite de l'agent propriétaire et la vérifie avant les réponses interactives éligibles.

Les intentions permanentes sont une mémoire prospective. Elles se souviennent de ce qu'il faut faire quand un déclencheur apparaît ; elles ne planifient pas de travail pour une heure d'horloge.

## Choisir le bon niveau d'intention

| Intention   | Utilisation                                      | Exemple                                              |
| ----------- | ---------------------------------------- | ---------------------------------------------------- |
| Basée sur l'heure  | [Tâches planifiées](/fr/automation/cron-jobs) | « Rappelle-moi vendredi à 9 h »                           |
| Basée sur un événement | Intention permanente                          | « Quand Alice mentionne le lancement, demande des informations sur le retour en arrière » |
| Aspiration  | Markdown avec une date d'examen              | « Améliorer la liste de contrôle de version ce trimestre »         |

Mettez les aspirations dans `MEMORY.md`, une note de projet ou un autre fichier Markdown maintenu avec une date d'examen explicite. Ce ne sont ni des tâches d'horloge ni des déclencheurs d'événements.

## Créer une intention basée sur un événement

Les intentions permanentes sont une mémoire dirigée par le propriétaire. Seuls les propriétaires de commandes reconnus par
`commands.ownerAllowFrom` peuvent voir ou utiliser l'outil `intent` pour créer, lister ou
annuler les intentions ; les autres expéditeurs ne reçoivent pas cet outil.

Demandez à l'agent de créer l'intention et de nommer l'événement clairement :

```text
When someone mentions the launch checklist, remind me to confirm the rollback owner.
```

L'agent utilise l'outil `intent` avec une description et des mots-clés de déclenchement. Il peut également limiter l'intention à un identifiant de canal de conversation ou un identifiant d'expéditeur, définir une expiration, réduire ou augmenter le budget de déclenchement, ou modifier le délai d'attente.

Les valeurs par défaut sont intentionnellement conservatrices :

- délai d'attente : 24 heures
- déclenchements maximum : 3
- expiration : 90 jours

Pour une heure d'horloge, l'agent doit utiliser le chemin de tâche planifiée existant au lieu de créer une intention permanente.

## Fonctionnement de la correspondance

À un tour d'utilisateur éligible, OpenClaw effectue un préfiltre de mots-clés FTS déterministe sur les intentions armées. Un candidat ne se déclenche que lorsque chaque terme d'au moins une entrée de déclencheur configurée apparaît dans le tour. OpenClaw revérifie également la portée du canal, la portée de l'expéditeur, l'expiration, le délai d'attente et le budget de déclenchement par rapport aux lignes SQLite faisant autorité dans une seule transaction synchrone. La correspondance analyse au maximum 256 candidats FTS délimités par portée par tour, de sorte qu'un ensemble de déclencheurs bruyants ne peut pas bloquer le chemin de réponse.

Aucun appel de modèle ne se produit dans le chemin de correspondance. En cas de correspondance, la réponse principale reçoit un bloc de contexte caché limité :

```text
Standing intent (created 2026-07-27): Confirm the rollback owner.
```

Le moteur de correspondance incrémente `fire_count`, enregistre `last_fired_at` et fait passer l'intention par son cycle de vie explicite. Une intention déclenchée devient armée à nouveau seulement après son délai d'attente. Elle devient `done` quand son budget de déclenchement est épuisé et `expired` quand son expiration arrive. La maintenance de l'expiration et du délai d'attente s'ajoute également aux crochets de réponse de battement de cœur et de cron existants ; OpenClaw n'ajoute pas un autre sous-système de minuterie.

TriggerBench constate que le rappel prospectif diminue à mesure que le contexte augmente et peut dériver vers une heuristique de rappel constant ([arXiv:2606.23459](https://arxiv.org/abs/2606.23459)). La correspondance structurelle et les budgets de déclenchement maintiennent le rappel indépendant du contexte conversationnel tout en limitant les fausses alarmes.

## Lister et annuler

Demandez à l'agent de lister les intentions permanentes quand vous voulez inspecter leur statut, portée, expiration ou nombre de déclenchements.

L'annulation est toujours explicite. Demandez à l'agent d'annuler une intention spécifique ; la ligne stockée passe à `cancelled` et ne peut plus se déclencher. OpenClaw ne déduit jamais l'annulation d'une conversation ordinaire. ProEvent rapporte que les systèmes proactifs réagissent souvent de manière excessive et ont du mal avec l'annulation d'événements ([arXiv:2607.17701](https://arxiv.org/abs/2607.17701)), donc l'annulation est un état durable plutôt qu'un jugement de modèle.

## États du cycle de vie

| État       | Signification                          |
| ----------- | -------------------------------- |
| `pending`   | Stocké mais pas encore armé         |
| `armed`     | Éligible pour la correspondance            |
| `fired`     | Correspondance trouvée et en attente du délai d'attente |
| `done`      | Budget de déclenchement épuisé            |
| `cancelled` | Explicitement annulé             |
| `expired`   | Expiration atteinte                   |

Les intentions permanentes vivent dans `agents/<agentId>/agent/openclaw-agent.sqlite`. Elles n'ajoutent aucune clé de configuration et ne créent aucun fichier annexe.

## Connexes

- [Aperçu de la mémoire](/fr/concepts/memory)
- [Modèle utilisateur](/fr/concepts/user-model)
- [Tâches planifiées](/fr/automation/cron-jobs)
