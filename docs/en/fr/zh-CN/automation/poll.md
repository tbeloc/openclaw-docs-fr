---
read_when:
  - 添加或修改投票支持
  - 调试从 CLI 或 Gateway 网关发送的投票
summary: 通过 Gateway 网关 + CLI 发送投票
title: 投票
x-i18n:
  generated_at: "2026-02-03T07:43:12Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 760339865d27ec40def7996cac1d294d58ab580748ad6b32cc34d285d0314eaf
  source_path: automation/poll.md
  workflow: 15
---

# Sondage

## Canaux pris en charge

- WhatsApp (canal Web)
- Discord
- MS Teams (Cartes adaptatives)

## CLI

```bash
# WhatsApp
openclaw message poll --target +15555550123 \
  --poll-question "Lunch today?" --poll-option "Yes" --poll-option "No" --poll-option "Maybe"
openclaw message poll --target 123456789@g.us \
  --poll-question "Meeting time?" --poll-option "10am" --poll-option "2pm" --poll-option "4pm" --poll-multi

# Discord
openclaw message poll --channel discord --target channel:123456789 \
  --poll-question "Snack?" --poll-option "Pizza" --poll-option "Sushi"
openclaw message poll --channel discord --target channel:123456789 \
  --poll-question "Plan?" --poll-option "A" --poll-option "B" --poll-duration-hours 48

# MS Teams
openclaw message poll --channel msteams --target conversation:19:abc@thread.tacv2 \
  --poll-question "Lunch?" --poll-option "Pizza" --poll-option "Sushi"
```

Options :

- `--channel` : `whatsapp` (par défaut), `discord` ou `msteams`
- `--poll-multi` : permet de sélectionner plusieurs options
- `--poll-duration-hours` : Discord uniquement (par défaut 24 si omis)

## RPC Gateway

Méthode : `poll`

Paramètres :

- `to` (chaîne, obligatoire)
- `question` (chaîne, obligatoire)
- `options` (tableau de chaînes, obligatoire)
- `maxSelections` (nombre, optionnel)
- `durationHours` (nombre, optionnel)
- `channel` (chaîne, optionnel, par défaut : `whatsapp`)
- `idempotencyKey` (chaîne, obligatoire)

## Différences entre les canaux

- WhatsApp : 2-12 options, `maxSelections` doit être dans la plage du nombre d'options, `durationHours` est ignoré.
- Discord : 2-10 options, `durationHours` limité à 1-768 heures (par défaut 24). `maxSelections > 1` active le multi-sélection ; Discord ne supporte pas la limitation stricte du nombre de sélections.
- MS Teams : Sondage par carte adaptative (géré par OpenClaw). Pas d'API de sondage natif ; `durationHours` est ignoré.

## Outil d'agent (Message)

Utilisez l'opération `poll` de l'outil `message` (`to`, `pollQuestion`, `pollOption`, optionnellement `pollMulti`, `pollDurationHours`, `channel`).

Remarque : Discord n'a pas de mode « exactement N sélections » ; `pollMulti` est mappé au multi-sélection.
Les sondages Teams sont rendus sous forme de cartes adaptatives et nécessitent que Gateway reste en ligne
pour enregistrer les sondages dans `~/.openclaw/msteams-polls.json`.
