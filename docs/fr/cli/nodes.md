---
summary: "Référence CLI pour `openclaw nodes` (list/status/approve/invoke, camera/canvas/screen)"
read_when:
  - Vous gérez des nœuds appairés (caméras, écran, canvas)
  - Vous devez approuver des demandes ou invoquer des commandes de nœud
title: "nodes"
---

# `openclaw nodes`

Gérez les nœuds appairés (appareils) et invoquez les capacités des nœuds.

Connexes :

- Aperçu des nœuds : [Nodes](/nodes)
- Caméra : [Camera nodes](/nodes/camera)
- Images : [Image nodes](/nodes/images)

Options communes :

- `--url`, `--token`, `--timeout`, `--json`

## Commandes communes

```bash
openclaw nodes list
openclaw nodes list --connected
openclaw nodes list --last-connected 24h
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes status
openclaw nodes status --connected
openclaw nodes status --last-connected 24h
```

`nodes list` affiche les tableaux en attente/appairés. Les lignes appairées incluent l'âge de connexion le plus récent (Last Connect).
Utilisez `--connected` pour afficher uniquement les nœuds actuellement connectés. Utilisez `--last-connected <duration>` pour
filtrer les nœuds qui se sont connectés dans une durée (par exemple `24h`, `7d`).

## Invoke / run

```bash
openclaw nodes invoke --node <id|name|ip> --command <command> --params <json>
openclaw nodes run --node <id|name|ip> <command...>
openclaw nodes run --raw "git status"
openclaw nodes run --agent main --node <id|name|ip> --raw "git status"
```

Drapeaux Invoke :

- `--params <json>` : chaîne d'objet JSON (par défaut `{}`).
- `--invoke-timeout <ms>` : délai d'expiration d'invocation du nœud (par défaut `15000`).
- `--idempotency-key <key>` : clé d'idempotence optionnelle.

### Valeurs par défaut de style Exec

`nodes run` reflète le comportement exec du modèle (valeurs par défaut + approbations) :

- Lit `tools.exec.*` (plus les remplacements `agents.list[].tools.exec.*`).
- Utilise les approbations exec (`exec.approval.request`) avant d'invoquer `system.run`.
- `--node` peut être omis quand `tools.exec.node` est défini.
- Nécessite un nœud qui annonce `system.run` (application compagnon macOS ou hôte de nœud sans interface).

Drapeaux :

- `--cwd <path>` : répertoire de travail.
- `--env <key=val>` : remplacement d'env (répétable). Remarque : les hôtes de nœud ignorent les remplacements `PATH` (et `tools.exec.pathPrepend` n'est pas appliqué aux hôtes de nœud).
- `--command-timeout <ms>` : délai d'expiration de la commande.
- `--invoke-timeout <ms>` : délai d'expiration d'invocation du nœud (par défaut `30000`).
- `--needs-screen-recording` : nécessite la permission d'enregistrement d'écran.
- `--raw <command>` : exécute une chaîne shell (`/bin/sh -lc` ou `cmd.exe /c`).
  En mode liste blanche sur les hôtes de nœud Windows, les exécutions du wrapper shell `cmd.exe /c` nécessitent une approbation
  (l'entrée de liste blanche seule ne permet pas automatiquement la forme du wrapper).
- `--agent <id>` : approbations/listes blanches limitées à l'agent (par défaut à l'agent configuré).
- `--ask <off|on-miss|always>`, `--security <deny|allowlist|full>` : remplacements.
