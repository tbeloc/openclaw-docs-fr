---
summary: "Référence CLI pour `openclaw flows` (list, inspect, cancel)"
read_when:
  - You want to inspect or cancel a flow
  - You want to see how background tasks roll up into a higher-level job
title: "flows"
---

# `openclaw flows`

Inspectez et gérez les tâches [ClawFlow](/fr/automation/clawflow).

```bash
openclaw flows list
openclaw flows show <lookup>
openclaw flows cancel <lookup>
```

## Commandes

### `flows list`

Listez les flux suivis et leurs comptages de tâches.

```bash
openclaw flows list
openclaw flows list --status blocked
openclaw flows list --json
```

### `flows show`

Affichez un flux par ID de flux ou clé de session du propriétaire.

```bash
openclaw flows show <lookup>
openclaw flows show <lookup> --json
```

La sortie inclut le statut du flux, l'étape actuelle, la cible d'attente, le résumé bloqué le cas échéant, les clés de sortie stockées et les tâches liées.

### `flows cancel`

Annulez un flux et toutes les tâches enfants actives.

```bash
openclaw flows cancel <lookup>
```

## Connexes

- [ClawFlow](/fr/automation/clawflow) — orchestration au niveau des tâches au-dessus des tâches
- [Tâches en arrière-plan](/fr/automation/tasks) — registre de travail détaché
- [Référence CLI](/fr/cli/index) — arborescence complète des commandes
