---
read_when:
  - Lors de l'ajout ou de la modification du comportement d'exec en arrière-plan
  - Lors du débogage de tâches exec longues
summary: Exécution d'exec en arrière-plan et gestion des processus
title: Outils Exec et Process en arrière-plan
x-i18n:
  generated_at: "2026-02-03T10:05:51Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: e11a7d74a75000d6882f703693c2c49a2ecd3e730b6ec2b475ac402abde9e465
  source_path: gateway/background-process.md
  workflow: 15
---

# Outils Exec + Process en arrière-plan

OpenClaw exécute les commandes shell via l'outil `exec` et conserve les tâches longues en mémoire. L'outil `process` gère ces sessions en arrière-plan.

## Outil exec

Paramètres clés :

- `command` (obligatoire)
- `yieldMs` (par défaut 10000) : passe automatiquement en arrière-plan après ce délai
- `background` (booléen) : passe immédiatement en arrière-plan
- `timeout` (secondes, par défaut 1800) : termine le processus après ce délai d'expiration
- `elevated` (booléen) : s'exécute sur l'hôte si l'élévation de privilèges est activée/autorisée
- Besoin d'un vrai TTY ? Définissez `pty: true`.
- `workdir`, `env`

Comportement :

- L'exécution au premier plan retourne directement la sortie.
- Lors du passage en arrière-plan (explicite ou par délai d'expiration), l'outil retourne `status: "running"` + `sessionId` et une courte sortie de fin.
- La sortie est conservée en mémoire jusqu'à ce que la session soit interrogée ou effacée.
- Si l'outil `process` est désactivé, `exec` s'exécute de manière synchrone et ignore `yieldMs`/`background`.

## Pont de sous-processus

Lors de la génération de sous-processus longues en dehors des outils exec/process (par exemple, régénération CLI ou programmes auxiliaires Gateway), attachez le pont de sous-processus pour que les signaux de terminaison soient transférés et que les écouteurs soient détachés à la sortie/erreur. Cela évite les processus orphelins sur systemd et maintient un comportement d'arrêt cohérent entre les plateformes.

Remplacements de variables d'environnement :

- `PI_BASH_YIELD_MS` : délai de rendement par défaut (millisecondes)
- `PI_BASH_MAX_OUTPUT_CHARS` : limite de sortie en mémoire (caractères)
- `OPENCLAW_BASH_PENDING_MAX_OUTPUT_CHARS` : limite stdout/stderr en attente par flux (caractères)
- `PI_BASH_JOB_TTL_MS` : TTL des sessions terminées (millisecondes, limité entre 1 minute et 3 heures)

Configuration (recommandée) :

- `tools.exec.backgroundMs` (par défaut 10000)
- `tools.exec.timeoutSec` (par défaut 1800)
- `tools.exec.cleanupMs` (par défaut 1800000)
- `tools.exec.notifyOnExit` (par défaut true) : met en file d'attente un événement système et demande un battement de cœur lorsqu'un exec en arrière-plan se termine.

## Outil process

Opérations :

- `list` : sessions en cours d'exécution et terminées
- `poll` : obtient la nouvelle sortie d'une session (rapporte également l'état de sortie)
- `log` : lit la sortie agrégée (supporte `offset` + `limit`)
- `write` : envoie stdin (`data`, `eof` optionnel)
- `kill` : termine une session en arrière-plan
- `clear` : supprime une session terminée de la mémoire
- `remove` : termine si en cours d'exécution, sinon efface la session terminée

Remarques :

- Seules les sessions en arrière-plan sont listées/conservées en mémoire.
- Les sessions sont perdues au redémarrage du processus (pas de persistance disque).
- Les journaux de session ne sont sauvegardés dans l'historique de chat que si vous exécutez `process poll/log` et que le résultat de l'outil est enregistré.
- `process` est isolé par agent ; il ne peut voir que les sessions lancées par cet agent.
- `process list` inclut le `name` dérivé (verbe de commande + cible) pour une navigation rapide.
- `process log` utilise `offset`/`limit` basé sur les lignes (omettez `offset` pour obtenir les N dernières lignes).

## Exemples

Exécuter une tâche longue et l'interroger plus tard :

```json
{ "tool": "exec", "command": "sleep 5 && echo done", "yieldMs": 1000 }
```

```json
{ "tool": "process", "action": "poll", "sessionId": "<id>" }
```

Lancer immédiatement en arrière-plan :

```json
{ "tool": "exec", "command": "npm run build", "background": true }
```

Envoyer stdin :

```json
{ "tool": "process", "action": "write", "sessionId": "<id>", "data": "y\n" }
```
