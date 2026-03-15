---
summary: "Configuration de webhook Synology Chat et configuration OpenClaw"
read_when:
  - Configuration de Synology Chat avec OpenClaw
  - Débogage du routage des webhooks Synology Chat
title: "Synology Chat"
---

# Synology Chat (plugin)

Statut : supporté via plugin en tant que canal de message direct utilisant les webhooks Synology Chat.
Le plugin accepte les messages entrants des webhooks sortants de Synology Chat et envoie les réponses
via un webhook entrant de Synology Chat.

## Plugin requis

Synology Chat est basé sur les plugins et ne fait pas partie de l'installation du canal principal par défaut.

Installez à partir d'une copie locale :

```bash
openclaw plugins install ./extensions/synology-chat
```

Détails : [Plugins](/tools/plugin)

## Configuration rapide

1. Installez et activez le plugin Synology Chat.
2. Dans les intégrations Synology Chat :
   - Créez un webhook entrant et copiez son URL.
   - Créez un webhook sortant avec votre jeton secret.
3. Pointez l'URL du webhook sortant vers votre passerelle OpenClaw :
   - `https://gateway-host/webhook/synology` par défaut.
   - Ou votre `channels.synology-chat.webhookPath` personnalisé.
4. Configurez `channels.synology-chat` dans OpenClaw.
5. Redémarrez la passerelle et envoyez un DM au bot Synology Chat.

Configuration minimale :

```json5
{
  channels: {
    "synology-chat": {
      enabled: true,
      token: "synology-outgoing-token",
      incomingUrl: "https://nas.example.com/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=...",
      webhookPath: "/webhook/synology",
      dmPolicy: "allowlist",
      allowedUserIds: ["123456"],
      rateLimitPerMinute: 30,
      allowInsecureSsl: false,
    },
  },
}
```

## Variables d'environnement

Pour le compte par défaut, vous pouvez utiliser des variables d'environnement :

- `SYNOLOGY_CHAT_TOKEN`
- `SYNOLOGY_CHAT_INCOMING_URL`
- `SYNOLOGY_NAS_HOST`
- `SYNOLOGY_ALLOWED_USER_IDS` (séparés par des virgules)
- `SYNOLOGY_RATE_LIMIT`
- `OPENCLAW_BOT_NAME`

Les valeurs de configuration remplacent les variables d'environnement.

## Politique DM et contrôle d'accès

- `dmPolicy: "allowlist"` est la valeur par défaut recommandée.
- `allowedUserIds` accepte une liste (ou une chaîne séparée par des virgules) d'ID d'utilisateurs Synology.
- En mode `allowlist`, une liste `allowedUserIds` vide est traitée comme une mauvaise configuration et la route du webhook ne démarrera pas (utilisez `dmPolicy: "open"` pour autoriser tous).
- `dmPolicy: "open"` autorise tout expéditeur.
- `dmPolicy: "disabled"` bloque les DM.
- Les approbations d'appairage fonctionnent avec :
  - `openclaw pairing list synology-chat`
  - `openclaw pairing approve synology-chat <CODE>`

## Livraison sortante

Utilisez les ID d'utilisateurs Synology Chat numériques comme cibles.

Exemples :

```bash
openclaw message send --channel synology-chat --target 123456 --text "Hello from OpenClaw"
openclaw message send --channel synology-chat --target synology-chat:123456 --text "Hello again"
```

Les envois de médias sont supportés par la livraison de fichiers basée sur les URL.

## Multi-compte

Plusieurs comptes Synology Chat sont supportés sous `channels.synology-chat.accounts`.
Chaque compte peut remplacer le jeton, l'URL entrante, le chemin du webhook, la politique DM et les limites.

```json5
{
  channels: {
    "synology-chat": {
      enabled: true,
      accounts: {
        default: {
          token: "token-a",
          incomingUrl: "https://nas-a.example.com/...token=...",
        },
        alerts: {
          token: "token-b",
          incomingUrl: "https://nas-b.example.com/...token=...",
          webhookPath: "/webhook/synology-alerts",
          dmPolicy: "allowlist",
          allowedUserIds: ["987654"],
        },
      },
    },
  },
}
```

## Notes de sécurité

- Gardez `token` secret et faites-le tourner s'il est divulgué.
- Gardez `allowInsecureSsl: false` sauf si vous faites explicitement confiance à un certificat auto-signé NAS local.
- Les demandes de webhook entrant sont vérifiées par jeton et limitées en débit par expéditeur.
- Préférez `dmPolicy: "allowlist"` pour la production.
