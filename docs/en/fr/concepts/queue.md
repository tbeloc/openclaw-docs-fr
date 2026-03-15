---
summary: "Conception de file d'attente de commandes qui sérialise les exécutions de réponse automatique entrantes"
read_when:
  - Changing auto-reply execution or concurrency
title: "Command Queue"
---

# Command Queue (2026-01-16)

Nous sérialisons les exécutions de réponse automatique entrantes (tous les canaux) via une petite file d'attente en mémoire pour éviter que plusieurs exécutions d'agent ne se heurtent, tout en permettant un parallélisme sûr entre les sessions.

## Pourquoi

- Les exécutions de réponse automatique peuvent être coûteuses (appels LLM) et peuvent entrer en collision lorsque plusieurs messages entrants arrivent rapprochés.
- La sérialisation évite de concourir pour les ressources partagées (fichiers de session, journaux, stdin CLI) et réduit le risque de limites de débit en amont.

## Comment ça marche

- Une file d'attente FIFO consciente des voies vide chaque voie avec un plafond de concurrence configurable (par défaut 1 pour les voies non configurées ; main par défaut à 4, subagent à 8).
- `runEmbeddedPiAgent` met en file d'attente par **clé de session** (voie `session:<key>`) pour garantir une seule exécution active par session.
- Chaque exécution de session est ensuite mise en file d'attente dans une **voie globale** (`main` par défaut) afin que le parallélisme global soit limité par `agents.defaults.maxConcurrent`.
- Lorsque la journalisation détaillée est activée, les exécutions en file d'attente émettent un court avis si elles ont attendu plus de ~2s avant de commencer.
- Les indicateurs de saisie se déclenchent toujours immédiatement à la mise en file d'attente (lorsqu'ils sont pris en charge par le canal) afin que l'expérience utilisateur reste inchangée pendant que nous attendons notre tour.

## Modes de file d'attente (par canal)

Les messages entrants peuvent diriger l'exécution actuelle, attendre un tour de suivi, ou faire les deux :

- `steer`: injecter immédiatement dans l'exécution actuelle (annule les appels d'outils en attente après la prochaine limite d'outil). Si ce n'est pas en streaming, revient à followup.
- `followup`: mettre en file d'attente pour le prochain tour d'agent après la fin de l'exécution actuelle.
- `collect`: fusionner tous les messages en file d'attente en un **seul** tour de suivi (par défaut). Si les messages ciblent différents canaux/threads, ils se vident individuellement pour préserver le routage.
- `steer-backlog` (alias `steer+backlog`): diriger maintenant **et** préserver le message pour un tour de suivi.
- `interrupt` (hérité): abandonner l'exécution active pour cette session, puis exécuter le message le plus récent.
- `queue` (alias hérité): identique à `steer`.

Steer-backlog signifie que vous pouvez obtenir une réponse de suivi après l'exécution dirigée, donc
les surfaces de streaming peuvent ressembler à des doublons. Préférez `collect`/`steer` si vous voulez
une réponse par message entrant.
Envoyez `/queue collect` comme commande autonome (par session) ou définissez `messages.queue.byChannel.discord: "collect"`.

Valeurs par défaut (lorsqu'elles ne sont pas définies dans la configuration) :

- Toutes les surfaces → `collect`

Configurez globalement ou par canal via `messages.queue` :

```json5
{
  messages: {
    queue: {
      mode: "collect",
      debounceMs: 1000,
      cap: 20,
      drop: "summarize",
      byChannel: { discord: "collect" },
    },
  },
}
```

## Options de file d'attente

Les options s'appliquent à `followup`, `collect` et `steer-backlog` (et à `steer` lorsqu'il revient à followup) :

- `debounceMs`: attendre le silence avant de commencer un tour de suivi (empêche "continue, continue").
- `cap`: nombre maximum de messages en file d'attente par session.
- `drop`: politique de débordement (`old`, `new`, `summarize`).

Summarize conserve une courte liste à puces des messages supprimés et l'injecte comme une invite de suivi synthétique.
Valeurs par défaut : `debounceMs: 1000`, `cap: 20`, `drop: summarize`.

## Remplacements par session

- Envoyez `/queue <mode>` comme commande autonome pour stocker le mode de la session actuelle.
- Les options peuvent être combinées : `/queue collect debounce:2s cap:25 drop:summarize`
- `/queue default` ou `/queue reset` efface le remplacement de session.

## Portée et garanties

- S'applique aux exécutions d'agent de réponse automatique sur tous les canaux entrants qui utilisent le pipeline de réponse de passerelle (WhatsApp web, Telegram, Slack, Discord, Signal, iMessage, webchat, etc.).
- La voie par défaut (`main`) est au niveau du processus pour les entrées + battements de cœur principaux ; définissez `agents.defaults.maxConcurrent` pour permettre plusieurs sessions en parallèle.
- Des voies supplémentaires peuvent exister (par exemple `cron`, `subagent`) afin que les tâches de fond puissent s'exécuter en parallèle sans bloquer les réponses entrantes.
- Les voies par session garantissent qu'une seule exécution d'agent touche une session donnée à la fois.
- Aucune dépendance externe ou thread de travail en arrière-plan ; pur TypeScript + promesses.

## Dépannage

- Si les commandes semblent bloquées, activez les journaux détaillés et recherchez les lignes "queued for …ms" pour confirmer que la file d'attente se vide.
- Si vous avez besoin de la profondeur de la file d'attente, activez les journaux détaillés et observez les lignes de synchronisation de la file d'attente.
