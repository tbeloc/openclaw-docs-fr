---
read_when:
  - Ajouter ou modifier les opérations CLI de message
  - Modifier le comportement des canaux sortants
summary: "Référence CLI pour `openclaw message` (envoi + opérations de canal)"
title: message
x-i18n:
  generated_at: "2026-02-01T20:21:30Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 35159baf1ef7136252e3ab1e5e03881ebc4196dd43425e2319a39306ced7f48c
  source_path: cli/message.md
  workflow: 14
---

# `openclaw message`

Commande sortante unique pour envoyer des messages et effectuer des opérations de canal
(Discord/Google Chat/Slack/Mattermost (plugin)/Telegram/WhatsApp/Signal/iMessage/MS Teams).

## Utilisation

```
openclaw message <subcommand> [flags]
```

Sélection du canal :

- Si plusieurs canaux sont configurés, vous devez spécifier `--channel`.
- Si un seul canal est configuré, celui-ci est le canal par défaut.
- Valeurs possibles : `whatsapp|telegram|discord|googlechat|slack|mattermost|signal|imessage|msteams` (Mattermost nécessite un plugin)

Format de la cible (`--target`) :

- WhatsApp : E.164 ou JID de groupe
- Telegram : ID de chat ou `@username`
- Discord : `channel:<id>` ou `user:<id>` (ou mention `<@id>` ; les ID numériques purs sont traités comme des canaux)
- Google Chat : `spaces/<spaceId>` ou `users/<userId>`
- Slack : `channel:<id>` ou `user:<id>` (accepte les ID de canal purs)
- Mattermost (plugin) : `channel:<id>`, `user:<id>` ou `@username` (les ID purs sont traités comme des canaux)
- Signal : `+E.164`, `group:<id>`, `signal:+E.164`, `signal:group:<id>` ou `username:<name>`/`u:<name>`
- iMessage : handle, `chat_id:<id>`, `chat_guid:<guid>` ou `chat_identifier:<id>`
- MS Teams : ID de conversation (`19:...@thread.tacv2`) ou `conversation:<id>` ou `user:<aad-object-id>`

Recherche par nom :

- Pour les fournisseurs supportés (Discord/Slack, etc.), les noms de canaux comme `Help` ou `#help` sont résolus via le cache du répertoire.
- En cas d'absence du cache, OpenClaw tentera une recherche de répertoire en temps réel si le fournisseur le supporte.

## Drapeaux généraux

- `--channel <name>`
- `--account <id>`
- `--target <dest>` (canal ou utilisateur de destination pour send/poll/read, etc.)
- `--targets <name>` (répétable ; diffusion uniquement)
- `--json`
- `--dry-run`
- `--verbose`

## Opérations

### Cœur

- `send`
  - Canaux : WhatsApp/Telegram/Discord/Google Chat/Slack/Mattermost (plugin)/Signal/iMessage/MS Teams
  - Requis : `--target`, et `--message` ou `--media`
  - Optionnel : `--media`, `--reply-to`, `--thread-id`, `--gif-playback`
  - Telegram uniquement : `--buttons` (nécessite `channels.telegram.capabilities.inlineButtons` pour activer)
  - Telegram uniquement : `--thread-id` (ID du sujet du forum)
  - Slack uniquement : `--thread-id` (timestamp du fil ; `--reply-to` utilise le même champ)
  - WhatsApp uniquement : `--gif-playback`

- `poll`
  - Canaux : WhatsApp/Discord/MS Teams
  - Requis : `--target`, `--poll-question`, `--poll-option` (répétable)
  - Optionnel : `--poll-multi`
  - Discord uniquement : `--poll-duration-hours`, `--message`

- `react`
  - Canaux : Discord/Google Chat/Slack/Telegram/WhatsApp/Signal
  - Requis : `--message-id`, `--target`
  - Optionnel : `--emoji`, `--remove`, `--participant`, `--from-me`, `--target-author`, `--target-author-uuid`
  - Remarque : `--remove` nécessite `--emoji` (omettre `--emoji` efface votre propre réaction emoji si supporté ; voir /tools/reactions)
  - WhatsApp uniquement : `--participant`, `--from-me`
  - Réactions emoji de groupe Signal : nécessite `--target-author` ou `--target-author-uuid`

- `reactions`
  - Canaux : Discord/Google Chat/Slack
  - Requis : `--message-id`, `--target`
  - Optionnel : `--limit`

- `read`
  - Canaux : Discord/Slack
  - Requis : `--target`
  - Optionnel : `--limit`, `--before`, `--after`
  - Discord uniquement : `--around`

- `edit`
  - Canaux : Discord/Slack
  - Requis : `--message-id`, `--message`, `--target`

- `delete`
  - Canaux : Discord/Slack/Telegram
  - Requis : `--message-id`, `--target`

- `pin` / `unpin`
  - Canaux : Discord/Slack
  - Requis : `--message-id`, `--target`

- `pins` (liste)
  - Canaux : Discord/Slack
  - Requis : `--target`

- `permissions`
  - Canaux : Discord
  - Requis : `--target`

- `search`
  - Canaux : Discord
  - Requis : `--guild-id`, `--query`
  - Optionnel : `--channel-id`, `--channel-ids` (répétable), `--author-id`, `--author-ids` (répétable), `--limit`

### Fils

- `thread create`
  - Canaux : Discord
  - Requis : `--thread-name`, `--target` (ID du canal)
  - Optionnel : `--message-id`, `--auto-archive-min`

- `thread list`
  - Canaux : Discord
  - Requis : `--guild-id`
  - Optionnel : `--channel-id`, `--include-archived`, `--before`, `--limit`

- `thread reply`
  - Canaux : Discord
  - Requis : `--target` (ID du fil), `--message`
  - Optionnel : `--media`, `--reply-to`

### Emoji

- `emoji list`
  - Discord : `--guild-id`
  - Slack : aucun drapeau supplémentaire

- `emoji upload`
  - Canaux : Discord
  - Requis : `--guild-id`, `--emoji-name`, `--media`
  - Optionnel : `--role-ids` (répétable)

### Autocollants

- `sticker send`
  - Canaux : Discord
  - Requis : `--target`, `--sticker-id` (répétable)
  - Optionnel : `--message`

- `sticker upload`
  - Canaux : Discord
  - Requis : `--guild-id`, `--sticker-name`, `--sticker-desc`, `--sticker-tags`, `--media`

### Rôles / Canaux / Membres / Voix

- `role info` (Discord) : `--guild-id`
- `role add` / `role remove` (Discord) : `--guild-id`, `--user-id`, `--role-id`
- `channel info` (Discord) : `--target`
- `channel list` (Discord) : `--guild-id`
- `member info` (Discord/Slack) : `--user-id` (Discord nécessite aussi `--guild-id`)
- `voice status` (Discord) : `--guild-id`, `--user-id`

### Événements

- `event list` (Discord) : `--guild-id`
- `event create` (Discord) : `--guild-id`, `--event-name`, `--start-time`
  - Optionnel : `--end-time`, `--desc`, `--channel-id`, `--location`, `--event-type`

### Administration (Discord)

- `timeout` : `--guild-id`, `--user-id` (optionnel `--duration-min` ou `--until` ; omettre les deux efface le timeout)
- `kick` : `--guild-id`, `--user-id` (+ `--reason`)
- `ban` : `--guild-id`, `--user-id` (+ `--delete-days`, `--reason`)
  - `timeout` supporte aussi `--reason`

### Diffusion

- `broadcast`
  - Canaux : tout canal configuré ; utilisez `--channel all` pour tous les fournisseurs
  - Requis : `--targets` (répétable)
  - Optionnel : `--message`, `--media`, `--dry-run`

## Exemples

Envoyer une réponse Discord :

```
openclaw message send --channel discord \
  --target channel:123 --message "hi" --reply-to 456
```

Créer un sondage Discord :

```
openclaw message poll --channel discord \
  --target channel:123 \
  --poll-question "Snack?" \
  --poll-option Pizza --poll-option Sushi \
  --poll-multi --poll-duration-hours 48
```

Envoyer un message proactif Teams :

```
openclaw message send --channel msteams \
  --target conversation:19:abc@thread.tacv2 --message "hi"
```

Créer un sondage Teams :

```
openclaw message poll --channel msteams \
  --target conversation:19:abc@thread.tacv2 \
  --poll-question "Lunch?" \
  --poll-option Pizza --poll-option Sushi
```

Ajouter une réaction emoji dans Slack :

```
openclaw message react --channel slack \
  --target C123 --message-id 456 --emoji "✅"
```

Ajouter une réaction emoji dans un groupe Signal :

```
openclaw message react --channel signal \
  --target signal:group:abc123 --message-id 1737630212345 \
  --emoji "✅" --target-author-uuid 123e4567-e89b-12d3-a456-426614174000
```

Envoyer des boutons inline Telegram :

```
openclaw message send --channel telegram --target @mychat --message "Choose:" \
  --buttons '[ [{"text":"Yes","callback_data":"cmd:yes"}], [{"text":"No","callback_data":"cmd:no"}] ]'
```
