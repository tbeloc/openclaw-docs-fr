---
summary: "Référence CLI pour `openclaw approvals` (approvals d'exécution pour les hôtes de passerelle ou de nœud)"
read_when:
  - You want to edit exec approvals from the CLI
  - You need to manage allowlists on gateway or node hosts
title: "approvals"
---

# `openclaw approvals`

Gérez les approvals d'exécution pour l'**hôte local**, l'**hôte de passerelle**, ou un **hôte de nœud**.
Par défaut, les commandes ciblent le fichier d'approvals local sur le disque. Utilisez `--gateway` pour cibler la passerelle, ou `--node` pour cibler un nœud spécifique.

Connexes :

- Approvals d'exécution : [Exec approvals](/fr/tools/exec-approvals)
- Nœuds : [Nodes](/fr/nodes)

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

## Assistants de liste d'autorisation

```bash
openclaw approvals allowlist add "~/Projects/**/bin/rg"
openclaw approvals allowlist add --agent main --node <id|name|ip> "/usr/bin/uptime"
openclaw approvals allowlist add --agent "*" "/usr/bin/uname"

openclaw approvals allowlist remove "~/Projects/**/bin/rg"
```

## Notes

- `--node` utilise le même résolveur que `openclaw nodes` (id, nom, ip, ou préfixe d'id).
- `--agent` est par défaut `"*"`, qui s'applique à tous les agents.
- L'hôte de nœud doit annoncer `system.execApprovals.get/set` (application macOS ou hôte de nœud sans interface).
- Les fichiers d'approvals sont stockés par hôte à `~/.openclaw/exec-approvals.json`.
