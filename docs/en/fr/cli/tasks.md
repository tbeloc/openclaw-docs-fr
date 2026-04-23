---
summary: "Référence CLI pour `openclaw tasks` (ledger de tâches de fond et état de Task Flow)"
read_when:
  - You want to inspect, audit, or cancel background task records
  - You are documenting Task Flow commands under `openclaw tasks flow`
title: "`openclaw tasks`"
---

# `openclaw tasks`

Inspectez les tâches de fond durables et l'état de Task Flow. Sans sous-commande,
`openclaw tasks` est équivalent à `openclaw tasks list`.

Voir [Background Tasks](/fr/automation/tasks) pour le cycle de vie et le modèle de livraison.

## Utilisation

```bash
openclaw tasks
openclaw tasks list
openclaw tasks list --runtime acp
openclaw tasks list --status running
openclaw tasks show <lookup>
openclaw tasks notify <lookup> state_changes
openclaw tasks cancel <lookup>
openclaw tasks audit
openclaw tasks maintenance
openclaw tasks maintenance --apply
openclaw tasks flow list
openclaw tasks flow show <lookup>
openclaw tasks flow cancel <lookup>
```

## Options racine

- `--json`: sortie JSON.
- `--runtime <name>`: filtrer par type : `subagent`, `acp`, `cron`, ou `cli`.
- `--status <name>`: filtrer par statut : `queued`, `running`, `succeeded`, `failed`, `timed_out`, `cancelled`, ou `lost`.

## Sous-commandes

### `list`

```bash
openclaw tasks list [--runtime <name>] [--status <name>] [--json]
```

Liste les tâches de fond suivies, les plus récentes en premier.

### `show`

```bash
openclaw tasks show <lookup> [--json]
```

Affiche une tâche par ID de tâche, ID d'exécution ou clé de session.

### `notify`

```bash
openclaw tasks notify <lookup> <done_only|state_changes|silent>
```

Modifie la politique de notification pour une tâche en cours d'exécution.

### `cancel`

```bash
openclaw tasks cancel <lookup>
```

Annule une tâche de fond en cours d'exécution.

### `audit`

```bash
openclaw tasks audit [--severity <warn|error>] [--code <name>] [--limit <n>] [--json]
```

Expose les enregistrements de tâches et Task Flow obsolètes, perdus, en échec de livraison ou autrement incohérents.

### `maintenance`

```bash
openclaw tasks maintenance [--apply] [--json]
```

Prévisualise ou applique la réconciliation des tâches et Task Flow, l'horodatage du nettoyage et l'élagage.

### `flow`

```bash
openclaw tasks flow list [--status <name>] [--json]
openclaw tasks flow show <lookup> [--json]
openclaw tasks flow cancel <lookup>
```

Inspectez ou annulez l'état durable de Task Flow sous le ledger de tâches.
