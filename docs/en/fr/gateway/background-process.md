---
summary: "Exécution en arrière-plan et gestion des processus"
read_when:
  - Adding or modifying background exec behavior
  - Debugging long-running exec tasks
title: "Outil Background Exec et Process"
---

# Background Exec + Outil Process

OpenClaw exécute les commandes shell via l'outil `exec` et conserve les tâches longues en mémoire. L'outil `process` gère ces sessions en arrière-plan.

## Outil exec

Paramètres clés :

- `command` (requis)
- `yieldMs` (par défaut 10000) : passer en arrière-plan après ce délai
- `background` (booléen) : passer en arrière-plan immédiatement
- `timeout` (secondes, par défaut 1800) : terminer le processus après ce délai
- `elevated` (booléen) : exécuter sur l'hôte si le mode élevé est activé/autorisé
- Besoin d'un vrai TTY ? Définissez `pty: true`.
- `workdir`, `env`

Comportement :

- Les exécutions au premier plan retournent la sortie directement.
- Lorsqu'elles sont mises en arrière-plan (explicitement ou par délai), l'outil retourne `status: "running"` + `sessionId` et une courte fin.
- La sortie est conservée en mémoire jusqu'à ce que la session soit interrogée ou effacée.
- Si l'outil `process` est désactivé, `exec` s'exécute de manière synchrone et ignore `yieldMs`/`background`.
- Les commandes exec générées reçoivent `OPENCLAW_SHELL=exec` pour les règles de shell/profil conscientes du contexte.

## Pontage des processus enfants

Lors du lancement de processus enfants longue durée en dehors des outils exec/process (par exemple, les respawns CLI ou les assistants de passerelle), attachez l'assistant de pontage de processus enfants pour que les signaux de terminaison soient transmis et que les écouteurs soient détachés à la sortie/erreur. Cela évite les processus orphelins sur systemd et maintient un comportement d'arrêt cohérent sur toutes les plateformes.

Remplacements d'environnement :

- `PI_BASH_YIELD_MS` : rendement par défaut (ms)
- `PI_BASH_MAX_OUTPUT_CHARS` : plafond de sortie en mémoire (caractères)
- `OPENCLAW_BASH_PENDING_MAX_OUTPUT_CHARS` : plafond stdout/stderr en attente par flux (caractères)
- `PI_BASH_JOB_TTL_MS` : TTL pour les sessions terminées (ms, limité à 1m–3h)

Configuration (préférée) :

- `tools.exec.backgroundMs` (par défaut 10000)
- `tools.exec.timeoutSec` (par défaut 1800)
- `tools.exec.cleanupMs` (par défaut 1800000)
- `tools.exec.notifyOnExit` (par défaut true) : mettre en file d'attente un événement système + demander un battement de cœur lorsqu'une exécution en arrière-plan se termine.
- `tools.exec.notifyOnExitEmptySuccess` (par défaut false) : lorsque true, mettre également en file d'attente les événements d'achèvement pour les exécutions en arrière-plan réussies qui n'ont produit aucune sortie.

## Outil process

Actions :

- `list` : sessions en cours d'exécution + terminées
- `poll` : vider la nouvelle sortie pour une session (rapporte également le statut de sortie)
- `log` : lire la sortie agrégée (supporte `offset` + `limit`)
- `write` : envoyer stdin (`data`, `eof` optionnel)
- `kill` : terminer une session en arrière-plan
- `clear` : supprimer une session terminée de la mémoire
- `remove` : terminer si en cours d'exécution, sinon effacer si terminée

Notes :

- Seules les sessions mises en arrière-plan sont listées/persistées en mémoire.
- Les sessions sont perdues au redémarrage du processus (pas de persistance disque).
- Les journaux de session ne sont enregistrés dans l'historique de chat que si vous exécutez `process poll/log` et que le résultat de l'outil est enregistré.
- `process` est limité par agent ; il ne voit que les sessions démarrées par cet agent.
- `process list` inclut un `name` dérivé (verbe de commande + cible) pour des analyses rapides.
- `process log` utilise `offset`/`limit` basés sur les lignes.
- Lorsque `offset` et `limit` sont tous deux omis, il retourne les 200 dernières lignes et inclut un indice de pagination.
- Lorsque `offset` est fourni et `limit` est omis, il retourne de `offset` à la fin (non limité à 200).

## Exemples

Exécuter une tâche longue et interroger plus tard :

```json
{ "tool": "exec", "command": "sleep 5 && echo done", "yieldMs": 1000 }
```

```json
{ "tool": "process", "action": "poll", "sessionId": "<id>" }
```

Démarrer immédiatement en arrière-plan :

```json
{ "tool": "exec", "command": "npm run build", "background": true }
```

Envoyer stdin :

```json
{ "tool": "process", "action": "write", "sessionId": "<id>", "data": "y\n" }
```
