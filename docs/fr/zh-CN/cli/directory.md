---
read_when:
  - 你想查找某个渠道的联系人/群组/自身 ID
  - 你正在开发渠道目录适配器
summary: "`openclaw directory` 的 CLI 参考（self、peers、groups）"
title: directory
x-i18n:
  generated_at: "2026-02-01T19:58:58Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 7c878d9013aeaa22c8a21563fac30b465a86be85d8c917c5d4591b5c3d4b2025
  source_path: cli/directory.md
  workflow: 14
---

# `openclaw directory`

Recherchez les fonctionnalités de répertoire sur les canaux pris en charge (contacts/pairs, groupes et « moi »).

## Paramètres généraux

- `--channel <name>` : ID/alias du canal (obligatoire si plusieurs canaux sont configurés ; sélectionné automatiquement si un seul canal est configuré)
- `--account <id>` : ID du compte (par défaut : compte par défaut du canal)
- `--json` : Sortie au format JSON

## Description

- `directory` vous aide à trouver les ID à coller dans d'autres commandes (en particulier `openclaw message send --target ...`).
- Pour de nombreux canaux, les résultats proviennent de la configuration (liste d'autorisation/groupes configurés) plutôt que du répertoire du fournisseur en temps réel.
- La sortie par défaut est `id` séparé par des tabulations (parfois avec `name`) ; utilisez `--json` dans les scripts.

## Utiliser les résultats avec `message send`

```bash
openclaw directory peers list --channel slack --query "U0"
openclaw message send --channel slack --target user:U012ABCDEF --message "hello"
```

## Formats d'ID (par canal)

- WhatsApp : `+15551234567` (chat privé), `1234567890-1234567890@g.us` (groupe)
- Telegram : `@username` ou ID de chat numérique ; les groupes sont des ID numériques
- Slack : `user:U…` et `channel:C…`
- Discord : `user:<id>` et `channel:<id>`
- Matrix (plugin) : `user:@user:server`, `room:!roomId:server` ou `#alias:server`
- Microsoft Teams (plugin) : `user:<id>` et `conversation:<id>`
- Zalo (plugin) : ID utilisateur (Bot API)
- Zalo Personal / `zalouser` (plugin) : ID de session de `zca` (chat privé/groupe) (`me`, `friend list`, `group list`)

## Self (« moi »)

```bash
openclaw directory self --channel zalouser
```

## Peers (contacts/utilisateurs)

```bash
openclaw directory peers list --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory peers list --channel zalouser --limit 50
```

## Groupes

```bash
openclaw directory groups list --channel zalouser
openclaw directory groups list --channel zalouser --query "work"
openclaw directory groups members --channel zalouser --group-id <id>
```
