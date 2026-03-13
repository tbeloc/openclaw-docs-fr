---
read_when:
  - 你正在管理已配对的节点（摄像头、屏幕、画布）
  - 你需要批准请求或调用节点命令
summary: "`openclaw nodes` 的 CLI 参考（列表/状态/批准/调用，摄像头/画布/屏幕）"
title: nodes
x-i18n:
  generated_at: "2026-02-03T10:04:26Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 23da6efdd659a82dbbc4afd18eb4ab1020a2892f69c28d610f912c8a799f734c
  source_path: cli/nodes.md
  workflow: 15
---

# `openclaw nodes`

Gérez les nœuds appairés (appareils) et invoquez les fonctionnalités des nœuds.

Contenu connexe :

- Aperçu des nœuds : [Nœuds](/nodes)
- Caméra : [Nœud caméra](/nodes/camera)
- Images : [Nœud images](/nodes/images)

Options générales :

- `--url`, `--token`, `--timeout`, `--json`

## Commandes courantes

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

`nodes list` affiche un tableau des nœuds en attente/appairés. Les lignes appairées contiennent la dernière durée de connexion (Last Connect).
Utilisez `--connected` pour afficher uniquement les nœuds actuellement connectés. Utilisez `--last-connected <duration>`
pour filtrer les nœuds connectés au cours de la période spécifiée (par exemple `24h`, `7d`).

## Invocation / Exécution

```bash
openclaw nodes invoke --node <id|name|ip> --command <command> --params <json>
openclaw nodes run --node <id|name|ip> <command...>
openclaw nodes run --raw "git status"
openclaw nodes run --agent main --node <id|name|ip> --raw "git status"
```

Drapeaux d'invocation :

- `--params <json>` : Chaîne d'objet JSON (par défaut `{}`).
- `--invoke-timeout <ms>` : Délai d'expiration de l'invocation du nœud (par défaut `15000`).
- `--idempotency-key <key>` : Clé d'idempotence optionnelle.

### Valeurs par défaut du style Exec

`nodes run` est conforme au comportement exec du modèle (valeurs par défaut + approbation) :

- Lisez `tools.exec.*` (et les remplacements `agents.list[].tools.exec.*`).
- Utilisez l'approbation exec avant d'invoquer `system.run` (`exec.approval.request`).
- Omettez `--node` lorsque `tools.exec.node` est défini.
- Nécessite un nœud prenant en charge `system.run` (application compagnon macOS ou hôte de nœud sans interface).

Drapeaux :

- `--cwd <path>` : Répertoire de travail.
- `--env <key=val>` : Remplacements de variables d'environnement (répétable).
- `--command-timeout <ms>` : Délai d'expiration de la commande.
- `--invoke-timeout <ms>` : Délai d'expiration de l'invocation du nœud (par défaut `30000`).
- `--needs-screen-recording` : Exige les permissions d'enregistrement d'écran.
- `--raw <command>` : Exécutez une chaîne shell (`/bin/sh -lc` ou `cmd.exe /c`).
- `--agent <id>` : Approbation ou liste blanche au niveau de l'agent (par défaut l'agent configuré).
- `--ask <off|on-miss|always>`, `--security <deny|allowlist|full>` : Options de remplacement.
