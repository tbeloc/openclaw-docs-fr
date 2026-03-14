---
summary: "Référence CLI pour `openclaw cron` (planifier et exécuter des tâches de fond)"
read_when:
  - Vous voulez des tâches planifiées et des réveils
  - Vous déboguez l'exécution de cron et les journaux
title: "cron"
---

# `openclaw cron`

Gérer les tâches cron pour le planificateur Gateway.

Connexes :

- Tâches cron : [Tâches cron](/automation/cron-jobs)

Conseil : exécutez `openclaw cron --help` pour la surface de commande complète.

Remarque : les tâches `cron add` isolées utilisent par défaut la livraison `--announce`. Utilisez `--no-deliver` pour garder la sortie interne. `--deliver` reste un alias déprécié pour `--announce`.

Remarque : les tâches ponctuelles (`--at`) se suppriment après succès par défaut. Utilisez `--keep-after-run` pour les conserver.

Remarque : les tâches récurrentes utilisent désormais une réessai exponentiel après des erreurs consécutives (30s → 1m → 5m → 15m → 60m), puis reviennent au calendrier normal après la prochaine exécution réussie.

Remarque : `openclaw cron run` revient dès que l'exécution manuelle est mise en file d'attente. Les réponses réussies incluent `{ ok: true, enqueued: true, runId }`; utilisez `openclaw cron runs --id <job-id>` pour suivre le résultat final.

Remarque : la rétention/élagage est contrôlé dans la configuration :

- `cron.sessionRetention` (par défaut `24h`) élague les sessions d'exécution isolées terminées.
- `cron.runLog.maxBytes` + `cron.runLog.keepLines` élaguent `~/.openclaw/cron/runs/<jobId>.jsonl`.

Note de mise à niveau : si vous avez des tâches cron plus anciennes antérieures au format de livraison/stockage actuel, exécutez `openclaw doctor --fix`. Doctor normalise désormais les champs cron hérités (`jobId`, `schedule.cron`, champs de livraison de haut niveau, alias de livraison `provider` de charge utile) et migre les tâches de secours webhook simples `notify: true` vers une livraison webhook explicite lorsque `cron.webhook` est configuré.

## Modifications courantes

Mettre à jour les paramètres de livraison sans modifier le message :

```bash
openclaw cron edit <job-id> --announce --channel telegram --to "123456789"
```

Désactiver la livraison pour une tâche isolée :

```bash
openclaw cron edit <job-id> --no-deliver
```

Activer le contexte de bootstrap léger pour une tâche isolée :

```bash
openclaw cron edit <job-id> --light-context
```

Annoncer sur un canal spécifique :

```bash
openclaw cron edit <job-id> --announce --channel slack --to "channel:C1234567890"
```

Créer une tâche isolée avec contexte de bootstrap léger :

```bash
openclaw cron add \
  --name "Lightweight morning brief" \
  --cron "0 7 * * *" \
  --session isolated \
  --message "Summarize overnight updates." \
  --light-context \
  --no-deliver
```

`--light-context` s'applique uniquement aux tâches de tour d'agent isolées. Pour les exécutions cron, le mode léger garde le contexte de bootstrap vide au lieu d'injecter l'ensemble complet de bootstrap de l'espace de travail.
