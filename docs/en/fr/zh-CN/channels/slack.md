# Slack

## Mode Socket（par défaut）

### Configuration rapide（débutants）

1. Créez une application Slack et activez **Socket Mode**.
2. Créez un **App Token**（`xapp-...`）et un **Bot Token**（`xoxb-...`）.
3. Configurez les tokens pour OpenClaw et démarrez la Gateway.

Configuration minimale :

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
    },
  },
}
```

### Configuration

1. Créez une application Slack sur https://api.slack.com/apps（à partir de zéro）.
2. **Socket Mode** → Activez-le. Allez ensuite à **Basic Information** → **App-Level Tokens** → **Generate Token and Scopes**, ajoutez la portée `connections:write`. Copiez le **App Token**（`xapp-...`）.
3. **OAuth & Permissions** → Ajoutez les portées de token bot（utilisez le manifest ci-dessous）. Cliquez sur **Install to Workspace**. Copiez le **Bot User OAuth Token**（`xoxb-...`）.
4. Optionnel : **OAuth & Permissions** → Ajoutez les **User Token Scopes**（voir la liste en lecture seule ci-dessous）. Réinstallez l'application et copiez le **User OAuth Token**（`xoxp-...`）.
5. **Event Subscriptions** → Activez les événements et abonnez-vous à :
   - `message.*`（y compris édition/suppression/diffusion de thread）
   - `app_mention`
   - `reaction_added`, `reaction_removed`
   - `member_joined_channel`, `member_left_channel`
   - `channel_rename`
   - `pin_added`, `pin_removed`
6. Invitez le bot à rejoindre les canaux que vous souhaitez qu'il lise.
7. Slash Commands → Si vous utilisez `channels.slack.slashCommand`, créez `/openclaw`. Si vous activez les commandes natives, ajoutez une commande slash pour chaque commande intégrée（nom identique à `/help`）. Sauf si vous définissez `channels.slack.commands.native: true`, Slack désactive par défaut les commandes natives（le `commands.native` global est `"auto"`, reste désactivé pour Slack）.
8. App Home → Activez l'onglet **Messages** pour que les utilisateurs puissent envoyer des messages privés au bot.

Utilisez le manifest ci-dessous pour maintenir les portées et événements synchronisés.

Support multi-comptes : utilisez `channels.slack.accounts` pour configurer les tokens de chaque compte et un `name` optionnel. Voir [`gateway/configuration`](/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) pour les modes partagés.

### Configuration OpenClaw（minimale）

Définissez les tokens via des variables d'environnement（recommandé）:

- `SLACK_APP_TOKEN=xapp-...`
- `SLACK_BOT_TOKEN=xoxb-...`

Ou via la configuration :

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
    },
  },
}
```

### Token utilisateur（optionnel）

OpenClaw peut utiliser un token utilisateur Slack（`xoxp-...`）pour les opérations de lecture（historique, épingles, réactions, emojis, infos membres）. Par défaut, il reste en lecture seule : quand un token utilisateur est présent, les lectures utilisent de préférence le token utilisateur, tandis que les écritures utilisent toujours le token bot, sauf si vous acceptez explicitement. Même si `userTokenReadOnly: false` est défini, les écritures utilisent de préférence le token bot quand il est disponible.

Le token utilisateur est configuré dans le fichier de configuration（pas de support des variables d'environnement）. Pour les comptes multiples, définissez `channels.slack.accounts.<id>.userToken`.

Exemple avec bot + app + token utilisateur :

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
      userToken: "xoxp-...",
    },
  },
}
```

Exemple avec userTokenReadOnly explicitement défini（autoriser les écritures du token utilisateur）:

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
      userToken: "xoxp-...",
      userTokenReadOnly: false,
    },
  },
}
```

#### Utilisation des tokens

- Les opérations de lecture（historique, liste de réactions, liste d'épingles, liste d'emojis, infos membres, recherche）utilisent de préférence le token utilisateur quand il est configuré, sinon le token bot.
- Les opérations d'écriture（envoi/édition/suppression de messages, ajout/suppression de réactions, épinglage/dépinglage, téléchargement de fichiers）utilisent par défaut le token bot. Si `userTokenReadOnly: false` et qu'aucun token bot n'est disponible, OpenClaw revient au token utilisateur.

### Contexte historique

- `channels.slack.historyLimit`（ou `channels.slack.accounts.*.historyLimit`）contrôle le nombre de messages récents du canal/groupe à inclure dans le prompt.
- Revient à `messages.groupChat.historyLimit`. Définissez à `0` pour désactiver（par défaut 50）.

## Mode HTTP（Events API）

Utilisez le mode webhook HTTP quand votre Gateway est accessible par Slack via HTTPS（cas typique d'un serveur déployé）.
Le mode HTTP utilise Events API + Interactivity + Slash Commands, partageant une URL de requête.

### Configuration

1. Créez une application Slack et **désactivez Socket Mode**（optionnel si vous utilisez uniquement HTTP）.
2. **Basic Information** → Copiez le **Signing Secret**.
3. **OAuth & Permissions** → Installez l'application et copiez le **Bot User OAuth Token**（`xoxb-...`）.
4. **Event Subscriptions** → Activez les événements et définissez l'**URL de requête** sur le chemin webhook de votre Gateway（par défaut `/slack/events`）.
5. **Interactivity & Shortcuts** → Activez et définissez la même **URL de requête**.
6. **Slash Commands** → Définissez la même **URL de requête** pour vos commandes.

Exemple d'URL de requête :
`https://gateway-host/slack/events`

### Configuration OpenClaw（minimale）

```json5
{
  channels: {
    slack: {
      enabled: true,
      mode: "http",
      botToken: "xoxb-...",
      signingSecret: "your-signing-secret",
      webhookPath: "/slack/events",
    },
  },
}
```

Mode HTTP multi-comptes : définissez `channels.slack.accounts.<id>.mode = "http"` et fournissez un `webhookPath` unique pour chaque compte, afin que chaque application Slack puisse pointer vers sa propre URL.

### Manifest（optionnel）

Utilisez ce manifest d'application Slack pour créer rapidement une application（ajustez le nom/les commandes si nécessaire）. Si vous prévoyez de configurer un token utilisateur, incluez les portées de permissions utilisateur.

```json
{
  "display_information": {
    "name": "OpenClaw",
    "description": "Slack connector for OpenClaw"
  },
  "features": {
    "bot_user": {
      "display_name": "OpenClaw",
      "always_online": false
    },
    "app_home": {
      "messages_tab_enabled": true,
      "messages_tab_read_only_enabled": false
    },
    "slash_commands": [
      {
        "command": "/openclaw",
        "description": "Send a message to OpenClaw",
        "should_escape": false
      }
    ]
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "chat:write",
        "channels:history",
        "channels:read",
        "groups:history",
        "groups:read",
        "groups:write",
        "im:history",
        "im:read",
        "im:write",
        "mpim:history",
        "mpim:read",
        "mpim:write",
        "users:read",
        "app_mentions:read",
        "reactions:read",
        "reactions:write",
        "pins:read",
        "pins:write",
        "emoji:read",
        "commands",
        "files:read",
        "files:write"
      ],
      "user": [
        "channels:history",
        "channels:read",
        "groups:history",
        "groups:read",
        "im:history",
        "im:read",
        "mpim:history",
        "mpim:read",
        "users:read",
        "reactions:read",
        "pins:read",
        "emoji:read",
        "search:read"
      ]
    }
  },
  "settings": {
    "socket_mode_enabled": true,
    "event_subscriptions": {
      "bot_events": [
        "app_mention",
        "message.channels",
        "message.groups",
        "message.im",
        "message.mpim",
        "reaction_added",
        "reaction_removed",
        "member_joined_channel",
        "member_left_channel",
        "channel_rename",
        "pin_added",
        "pin_removed"
      ]
    }
  }
}
```

Si vous activez les commandes natives, ajoutez une entrée `slash_commands` pour chaque commande que vous souhaitez exposer（correspondant à la liste `/help`）. Utilisez `channels.slack.commands.native` pour remplacer.

## Portées de permissions（actuelles vs optionnelles）

L'API Conversations de Slack est différenciée par type : vous n'avez besoin que des portées pour les types de conversation que vous touchez réellement（channels, groups, im, mpim）. Voir https://docs.slack.dev/apis/web-api/using-the-conversations-api/ pour un aperçu.

### Portées de permissions du token bot（requises）

- `chat:write`（envoyer/mettre à jour/supprimer des messages via `chat.postMessage`）
  https://docs.slack.dev/reference/methods/chat.postMessage
- `im:write`（ouvrir les messages directs via `conversations.open` pour les messages privés des utilisateurs）
  https://docs.slack.dev/reference/methods/conversations.open
- `channels:history`, `groups:history`, `im:history`, `mpim:history`
  https://docs.slack.dev/reference/methods/conversations.history
- `channels:read`, `groups:read`, `im:read`, `mpim:read`
  https://docs.slack.dev/reference/methods/conversations.info
- `users:read`（requête utilisateur）
  https://docs.slack.dev/reference/methods/users.info
- `reactions:read`, `reactions:write`（`reactions.get` / `reactions.add`）
  https://docs.slack.dev/reference/methods/reactions.get
  https://docs.slack.dev/reference/methods/reactions.add
- `pins:read`, `pins:write`（`pins.list` / `pins.add` / `pins.remove`）
  https://docs.slack.dev/reference/scopes/pins.read
  https://docs.slack.dev/reference/scopes/pins.write
- `emoji:read`（`emoji.list`）
  https://docs.slack.dev/reference/scopes/emoji.read
- `files:write`（télécharger via `files.uploadV2`）
  https://docs.slack.dev/messaging/working-with-files/#upload

### Portées de permissions du token utilisateur（optionnelles, lecture seule par défaut）

Si vous avez configuré `channels.slack.userToken`, ajoutez celles-ci sous **User Token Scopes**.

- `channels:history`, `groups:history`, `im:history`, `mpim:history`
- `channels:read`, `groups:read`, `im:read`, `mpim:read`
- `users:read`
- `reactions:read`
- `pins:read`
- `emoji:read`
- `search:read`

### Actuellement non requises（mais peuvent être nécessaires à l'avenir）

- `mpim:write`（uniquement si nous ajoutons l'ouverture de groupe privé/démarrage de message privé via `conversations.open`）
- `groups:write`（uniquement si nous ajoutons la gestion des canaux privés : créer/renommer/inviter/archiver）
- `chat:write.public`（uniquement si nous voulons publier sur des canaux auxquels le bot n'a pas accès）
  https://docs.slack.dev/reference/scopes/chat.write.public
- `users:read.email`（uniquement si nous avons besoin du champ email de `users.info`）
  https://docs.slack.dev/changelog/2017-04-narrowing-email-access
- `files:read`（uniquement si nous commençons à lister/lire les métadonnées de fichiers）

## Configuration

Slack utilise uniquement Socket Mode（pas de serveur webhook HTTP）. Fournissez deux tokens :

```json
{
  "slack": {
    "enabled": true,
    "botToken": "xoxb-...",
    "appToken": "xapp-...",
    "groupPolicy": "allowlist",
    "dm": {
      "enabled": true,
      "policy": "pairing",
      "allowFrom": ["U123", "U456", "*"],
      "groupEnabled": false,
      "groupChannels": ["G123"],
      "replyToMode": "all"
    },
    "channels": {
      "C123": { "allow": true, "requireMention": true },
      "#general": {
        "allow": true,
        "requireMention": true,
        "users": ["U123"],
        "skills": ["search", "docs"],
        "systemPrompt": "Keep answers short."
      }
    },
    "reactionNotifications": "own",
    "reactionAllowlist": ["U123"],
    "replyToMode": "off",
    "actions": {
      "reactions": true,
      "messages": true,
      "pins": true,
      "memberInfo": true,
      "emojiList": true
    },
    "slashCommand": {
      "enabled": true,
      "name": "openclaw",
      "sessionPrefix": "slack:slash",
      "ephemeral": true
    },
    "textChunkLimit": 4000,
    "mediaMaxMb": 20
  }
}
```

Les tokens peuvent également être fournis via des variables d'environnement :

- `SLACK_BOT_TOKEN`
- `SLACK_APP_TOKEN`

Confirmez les réactions emoji via `messages
