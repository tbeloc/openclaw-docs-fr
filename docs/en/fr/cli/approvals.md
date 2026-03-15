---
summary: "Référence CLI pour `openclaw approvals` (approvals d'exécution pour les hôtes gateway ou node)"
read_when:
  - You want to edit exec approvals from the CLI
  - You need to manage allowlists on gateway or node hosts
title: "approvals"
---

# `openclaw approvals`

Gérez les approvals d'exécution pour l'**hôte local**, l'**hôte gateway**, ou un **hôte node**.
Par défaut, les commandes ciblent le fichier d'approvals local sur le disque. Utilisez `--gateway` pour cibler la gateway, ou `--node` pour cibler un node spécifique.

Liens connexes :

- Exec approvals: [Exec approvals](/tools/exec-approvals)
- Nodes: [Nodes](/nodes)

## Commandes courantes

```bash
openclaw approvals get
openclaw approvals get --node <id|name|ip>
openclaw approvals get --gateway
```

## Remplacer les approvals à partir d'un fichier

```bash
openclaw approvals set --file ./exec-approvals.json
openclaw approvals set --node <id|name|ip> --file ./exec-approvals.json
openclaw approvals set --gateway --file ./exec-approvals.json
```

## Assistants d'allowlist

```bash
openclaw approvals allowlist add "~/Projects/**/bin/rg"
openclaw approvals allowlist add --agent main --node <id|name|ip> "/usr/bin/uptime"
openclaw approvals allowlist add --agent "*" "/usr/bin/uname"

openclaw approvals allowlist remove "~/Projects/**/bin/rg"
```

## Notes

- `--node` utilise le même résolveur que `openclaw nodes` (id, name, ip, ou préfixe d'id).
- `--agent` par défaut à `"*"`, qui s'applique à tous les agents.
- L'hôte node doit annoncer `system.execApprovals.get/set` (app macOS ou headless node host).
- Les fichiers d'approvals sont stockés par hôte à `~/.openclaw/exec-approvals.json`.
