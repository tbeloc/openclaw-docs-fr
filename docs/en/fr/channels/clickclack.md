---
summary: "Configuration du canal de jeton bot ClickClack et syntaxe des cibles"
read_when:
  - Connecting OpenClaw to a ClickClack workspace
  - Testing ClickClack bot identities
title: "ClickClack"
---

ClickClack connecte OpenClaw à un espace de travail ClickClack auto-hébergé via des jetons bot ClickClack de première classe.

Utilisez ceci lorsque vous souhaitez qu'un agent OpenClaw apparaisse comme un utilisateur bot ClickClack. ClickClack prend en charge les bots de service indépendants et les bots appartenant à des utilisateurs ; les bots appartenant à des utilisateurs conservent un `owner_user_id` et ne reçoivent que les portées de jeton que vous accordez.

## Configuration rapide

Créez un jeton bot dans ClickClack :

```bash
clickclack admin bot create \
  --workspace <workspace_id_or_slug> \
  --name "OpenClaw" \
  --handle openclaw \
  --scopes bot:write \
  --plain
```

Pour un bot appartenant à un utilisateur, ajoutez `--owner <user_id>`.

Configurez OpenClaw :

```json5
{
  plugins: {
    entries: {
      clickclack: {
        llm: {
          allowAgentIdOverride: true,
        },
      },
    },
  },
  channels: {
    clickclack: {
      enabled: true,
      baseUrl: "https://app.clickclack.chat",
      token: { source: "env", provider: "default", id: "CLICKCLACK_BOT_TOKEN" },
      workspace: "default",
      defaultTo: "channel:general",
      agentId: "clickclack-bot",
      replyMode: "model",
    },
  },
}
```

Ensuite, exécutez :

```bash
export CLICKCLACK_BOT_TOKEN="ccb_..."
openclaw gateway
```

## Plusieurs bots

Chaque compte ouvre sa propre connexion en temps réel ClickClack et utilise son propre jeton bot.

```json5
{
  plugins: {
    entries: {
      clickclack: {
        llm: {
          allowAgentIdOverride: true,
        },
      },
    },
  },
  channels: {
    clickclack: {
      enabled: true,
      baseUrl: "https://app.clickclack.chat",
      defaultAccount: "service",
      accounts: {
        service: {
          token: { source: "env", provider: "default", id: "CLICKCLACK_SERVICE_BOT_TOKEN" },
          workspace: "default",
          defaultTo: "channel:general",
          agentId: "service-bot",
          replyMode: "model",
        },
        peter: {
          token: { source: "env", provider: "default", id: "CLICKCLACK_PETER_BOT_TOKEN" },
          workspace: "default",
          defaultTo: "dm:usr_...",
          agentId: "peter-bot",
          replyMode: "model",
        },
      },
    },
  },
}
```

`replyMode: "model"` utilise `api.runtime.llm.complete` directement pour les réponses courtes du bot.
Lorsqu'un compte définit `agentId`, OpenClaw nécessite le bit de confiance explicite
`plugins.entries.clickclack.llm.allowAgentIdOverride` afin que le plugin
puisse exécuter des complétions pour cet agent bot. Gardez-le désactivé si vous utilisez uniquement l'itinéraire d'agent par défaut.

## Cibles

- `channel:<name-or-id>` envoie à un canal de l'espace de travail. Les cibles nues sont par défaut `channel:`.
- `dm:<user_id>` crée ou réutilise une conversation directe avec cet utilisateur.
- `thread:<message_id>` répond dans un fil existant.

Exemples :

```bash
openclaw message send --channel clickclack --target channel:general --message "hello"
openclaw message send --channel clickclack --target dm:usr_123 --message "hello"
openclaw message send --channel clickclack --target thread:msg_123 --message "following up"
```

## Permissions

Les portées de jeton ClickClack sont appliquées par l'API ClickClack.

- `bot:read` : lire les données de l'espace de travail/canal/message/fil/DM/temps réel/profil.
- `bot:write` : `bot:read` plus les messages de canal, les réponses de fil, les DM et les téléchargements.
- `bot:admin` : `bot:write` plus la création de canal.

OpenClaw n'a besoin que de `bot:write` pour le chat d'agent normal.

## Dépannage

- `ClickClack is not configured` : définissez `channels.clickclack.token` ou `CLICKCLACK_BOT_TOKEN`.
- `workspace not found` : définissez `workspace` sur l'ID ou le slug de l'espace de travail renvoyé par ClickClack.
- Pas de réponses entrantes : confirmez que le jeton a accès à la lecture en temps réel et que le bot ne répond pas à ses propres messages.
- Les envois de canal échouent : vérifiez que le bot est membre de l'espace de travail et dispose de `bot:write`.
