---
summary: "Référence CLI pour `openclaw directory` (self, peers, groups)"
read_when:
  - Vous voulez rechercher les identifiants de contacts/groupes/self pour un canal
  - Vous développez un adaptateur de répertoire de canal
title: "directory"
---

# `openclaw directory`

Recherches de répertoire pour les canaux qui les supportent (contacts/pairs, groupes et "moi").

## Drapeaux courants

- `--channel <name>`: identifiant/alias du canal (requis quand plusieurs canaux sont configurés; automatique quand un seul canal est configuré)
- `--account <id>`: identifiant du compte (par défaut: défaut du canal)
- `--json`: sortie JSON

## Notes

- `directory` est destiné à vous aider à trouver les identifiants que vous pouvez coller dans d'autres commandes (en particulier `openclaw message send --target ...`).
- Pour de nombreux canaux, les résultats sont basés sur la configuration (listes blanches / groupes configurés) plutôt que sur un répertoire de fournisseur en direct.
- La sortie par défaut est `id` (et parfois `name`) séparés par une tabulation; utilisez `--json` pour les scripts.

## Utilisation des résultats avec `message send`

```bash
openclaw directory peers list --channel slack --query "U0"
openclaw message send --channel slack --target user:U012ABCDEF --message "hello"
```

## Formats d'identifiant (par canal)

- WhatsApp: `+15551234567` (DM), `1234567890-1234567890@g.us` (groupe)
- Telegram: `@username` ou identifiant de chat numérique; les groupes sont des identifiants numériques
- Slack: `user:U…` et `channel:C…`
- Discord: `user:<id>` et `channel:<id>`
- Matrix (plugin): `user:@user:server`, `room:!roomId:server`, ou `#alias:server`
- Microsoft Teams (plugin): `user:<id>` et `conversation:<id>`
- Zalo (plugin): identifiant utilisateur (API Bot)
- Zalo Personal / `zalouser` (plugin): identifiant de fil (DM/groupe) de `zca` (`me`, `friend list`, `group list`)

## Self ("moi")

```bash
openclaw directory self --channel zalouser
```

## Pairs (contacts/utilisateurs)

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
