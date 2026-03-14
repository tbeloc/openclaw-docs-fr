---
read_when:
  - 开发 Tlon/Urbit 渠道功能
summary: Tlon/Urbit 支持状态、功能和配置
title: Tlon
x-i18n:
  generated_at: "2026-02-03T07:44:17Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 19d7ffe23e82239fd2a2e35913e0d52c809b2c2b939dd39184e6c27a539ed97d
  source_path: channels/tlon.md
  workflow: 15
---

# Tlon (Plugin)

Tlon est un outil de messagerie instantanée décentralisé construit sur Urbit. OpenClaw se connecte à votre ship Urbit et peut répondre aux messages privés et aux messages de groupe. Les réponses de groupe nécessitent par défaut une mention @, et peuvent être davantage restreintes via une liste d'autorisation.

Statut : Support via plugin. Les messages privés, les mentions de groupe, les réponses de sujet et le repli sur texte brut pour les médias (URL ajoutée à la légende) sont pris en charge. Les réactions emoji, les sondages et les téléchargements de médias natifs ne sont pas pris en charge.

## Plugin requis

Tlon est fourni en tant que plugin et n'est pas inclus dans l'installation principale.

Installation via CLI (référentiel npm) :

```bash
openclaw plugins install @openclaw/tlon
```

Extraction locale (lors de l'exécution à partir du référentiel git) :

```bash
openclaw plugins install ./extensions/tlon
```

Détails : [Plugins](/tools/plugin)

## Configuration

1. Installez le plugin Tlon.
2. Obtenez l'URL de votre ship et le code de connexion.
3. Configurez `channels.tlon`.
4. Redémarrez la passerelle Gateway.
5. Envoyez un message privé au bot ou mentionnez-le dans un canal de groupe.

Configuration minimale (compte unique) :

```json5
{
  channels: {
    tlon: {
      enabled: true,
      ship: "~sampel-palnet",
      url: "https://your-ship-host",
      code: "lidlut-tabwed-pillex-ridrup",
    },
  },
}
```

## Canaux de groupe

La découverte automatique est activée par défaut. Vous pouvez également épingler manuellement des canaux :

```json5
{
  channels: {
    tlon: {
      groupChannels: ["chat/~host-ship/general", "chat/~host-ship/support"],
    },
  },
}
```

Désactiver la découverte automatique :

```json5
{
  channels: {
    tlon: {
      autoDiscoverChannels: false,
    },
  },
}
```

## Contrôle d'accès

Liste d'autorisation des messages privés (vide = autoriser tous) :

```json5
{
  channels: {
    tlon: {
      dmAllowlist: ["~zod", "~nec"],
    },
  },
}
```

Autorisation de groupe (restreinte par défaut) :

```json5
{
  channels: {
    tlon: {
      defaultAuthorizedShips: ["~zod"],
      authorization: {
        channelRules: {
          "chat/~host-ship/general": {
            mode: "restricted",
            allowedShips: ["~zod", "~nec"],
          },
          "chat/~host-ship/announcements": {
            mode: "open",
          },
        },
      },
    },
  },
}
```

## Cibles de livraison (CLI/cron)

À utiliser avec `openclaw message send` ou la livraison cron :

- Message privé : `~sampel-palnet` ou `dm/~sampel-palnet`
- Groupe : `chat/~host-ship/channel` ou `group:~host-ship/channel`

## Remarques

- Les réponses de groupe nécessitent une mention (par exemple `~your-bot-ship`) pour répondre.
- Réponses de sujet : Si le message entrant se trouve dans un sujet, OpenClaw répond dans le sujet.
- Médias : `sendMedia` revient à texte + URL (pas de téléchargement natif).
