---
read_when:
  - Vous avez besoin de tâches planifiées et de fonctionnalités de réveil
  - Vous déboguez l'exécution de cron et les journaux
summary: "Référence CLI pour `openclaw cron` (planification et exécution de tâches en arrière-plan)"
title: cron
x-i18n:
  generated_at: "2026-02-03T07:44:47Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: bc9317c824f3b6339df657cc269961d9b5f121da65ec2b23a07d454e6d611135
  source_path: cli/cron.md
  workflow: 15
---

# `openclaw cron`

Gérez les tâches cron du planificateur Gateway.

Contenu connexe :

- Tâches Cron : [Tâches Cron](/automation/cron-jobs)

Conseil : Exécutez `openclaw cron --help` pour voir l'ensemble complet des commandes.

Remarque : Les tâches `cron add` isolées utilisent par défaut `--announce` pour la livraison du résumé. Utilisez `--no-deliver` pour exécuter uniquement en interne.
`--deliver` est conservé comme alias obsolète pour `--announce`.

Remarque : Les tâches ponctuelles (`--at`) sont supprimées par défaut après une exécution réussie. Utilisez `--keep-after-run` pour les conserver.

## Modifications courantes

Mettez à jour les paramètres de livraison sans modifier le message :

```bash
openclaw cron edit <job-id> --announce --channel telegram --to "123456789"
```

Désactivez la livraison pour une tâche isolée :

```bash
openclaw cron edit <job-id> --no-deliver
```
