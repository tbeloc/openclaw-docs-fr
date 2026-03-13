---
read_when:
  - Vous souhaitez modifier les approbations d'exécution via CLI
  - Vous devez gérer la liste d'autorisation sur la passerelle Gateway ou l'hôte du nœud
summary: Référence CLI : `openclaw approvals`（approbations d'exécution pour la passerelle Gateway ou l'hôte du nœud）
title: approvals
x-i18n:
  generated_at: "2026-02-03T10:04:09Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 4329cdaaec2c5f5d619415b6431196512d4834dc1ccd7363576f03dd9b845130
  source_path: cli/approvals.md
  workflow: 15
---

# `openclaw approvals`

Gérez les approbations d'exécution pour l'**hôte local**, l'**hôte Gateway** ou l'**hôte du nœud**.
Par défaut, la commande cible le fichier d'approbation local sur le disque. Utilisez `--gateway` pour cibler la passerelle Gateway, et `--node` pour un nœud spécifique.

Contenu connexe :

- Approbations d'exécution : [Approbations d'exécution](/tools/exec-approvals)
- Nœuds : [Nœuds](/nodes)

## Commandes courantes

```bash
openclaw approvals get
openclaw approvals get --node <id|name|ip>
openclaw approvals get --gateway
```

## Remplacer les approbations à partir d'un fichier

```bash
openclaw approvals set --file ./exec-approvals.json
openclaw approvals set --node <id|name|ip> --file ./exec-approvals.json
openclaw approvals set --gateway --file ./exec-approvals.json
```

## Commandes auxiliaires de la liste d'autorisation

```bash
openclaw approvals allowlist add "~/Projects/**/bin/rg"
openclaw approvals allowlist add --agent main --node <id|name|ip> "/usr/bin/uptime"
openclaw approvals allowlist add --agent "*" "/usr/bin/uname"

openclaw approvals allowlist remove "~/Projects/**/bin/rg"
```

## Remarques

- `--node` utilise le même analyseur que `openclaw nodes`（id, name, ip ou préfixe d'id）.
- `--agent` est défini par défaut sur `"*"`, ce qui signifie qu'il s'applique à tous les agents.
- L'hôte du nœud doit exposer `system.execApprovals.get/set`（application macOS ou hôte de nœud sans interface）.
- Les fichiers d'approbation sont stockés par hôte dans `~/.openclaw/exec-approvals.json`.
