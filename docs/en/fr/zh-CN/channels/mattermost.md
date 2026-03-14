---
read_when:
  - 设置 Mattermost
  - 调试 Mattermost 路由
summary: Mattermost 机器人设置和 OpenClaw 配置
title: Mattermost
x-i18n:
  generated_at: "2026-02-03T07:43:43Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 57fabe5eb0efbcb885f4178b317b2fa99a41daf609e3a471de2b44db9def4ad7
  source_path: channels/mattermost.md
  workflow: 15
---

# Mattermost (Plugin)

Statut : Support via plugin (bot token + événements WebSocket). Supporte les canaux, les groupes et les messages privés.
Mattermost est une plateforme de messagerie d'équipe auto-hébergée ; pour les détails du produit et les téléchargements, visitez le site officiel
[mattermost.com](https://mattermost.com).

## Plugin requis

Mattermost est fourni en tant que plugin et n'est pas inclus dans l'installation principale.

Installation via CLI (registre npm) :

```bash
openclaw plugins install @openclaw/mattermost
```

Extraction locale (lors de l'exécution à partir du dépôt git) :

```bash
openclaw plugins install ./extensions/mattermost
```

Si vous sélectionnez Mattermost lors de la configuration/initialisation et qu'une extraction git est détectée, OpenClaw fournira automatiquement le chemin d'installation local.

Détails : [Plugins](/tools/plugin)

## Configuration rapide

1. Installez le plugin Mattermost.
2. Créez un compte bot Mattermost et copiez le **bot token**.
3. Copiez l'**URL de base** de Mattermost (par exemple `https://chat.example.com`).
4. Configurez OpenClaw et démarrez la passerelle Gateway.

Configuration minimale :

```json5
{
  channels: {
    mattermost: {
      enabled: true,
      botToken: "mm-token",
      baseUrl: "https://chat.example.com",
      dmPolicy: "pairing",
    },
  },
}
```

## Variables d'environnement (compte par défaut)

Si vous préférez utiliser des variables d'environnement, définissez-les sur l'hôte de la passerelle Gateway :

- `MATTERMOST_BOT_TOKEN=...`
- `MATTERMOST_URL=https://chat.example.com`

Les variables d'environnement s'appliquent uniquement au compte **par défaut** (`default`). Les autres comptes doivent utiliser les valeurs de configuration.

## Mode de chat

Mattermost répond automatiquement aux messages privés. Le comportement des canaux est contrôlé par `chatmode` :

- `oncall` (par défaut) : Répond uniquement lorsqu'il est @mentionné dans le canal.
- `onmessage` : Répond à chaque message du canal.
- `onchar` : Répond lorsque le message commence par un préfixe de déclenchement.

Exemple de configuration :

```json5
{
  channels: {
    mattermost: {
      chatmode: "onchar",
      oncharPrefixes: [">", "!"],
    },
  },
}
```

Remarques :

- `onchar` répond toujours aux @mentions explicites.
- `channels.mattermost.requireMention` reste valide pour les anciennes configurations, mais `chatmode` est recommandé.

## Contrôle d'accès (messages privés)

- Par défaut : `channels.mattermost.dmPolicy = "pairing"` (les expéditeurs inconnus reçoivent un code d'appairage).
- Approuver via :
  - `openclaw pairing list mattermost`
  - `openclaw pairing approve mattermost <CODE>`
- Messages privés ouverts : `channels.mattermost.dmPolicy="open"` plus `channels.mattermost.allowFrom=["*"]`.

## Canaux (groupes)

- Par défaut : `channels.mattermost.groupPolicy = "allowlist"` (restrictions de mention).
- Utilisez `channels.mattermost.groupAllowFrom` pour ajouter des expéditeurs à la liste blanche (ID utilisateur ou `@username`).
- Canaux ouverts : `channels.mattermost.groupPolicy="open"` (restrictions de mention).

## Cibles de livraison sortante

Utilisez ces formats de cible dans `openclaw message send` ou cron/webhooks :

- `channel:<id>` pour les canaux
- `user:<id>` pour les messages privés
- `@username` pour les messages privés (résolu via l'API Mattermost)

Les ID nus sont traités comme des canaux.

## Comptes multiples

Mattermost supporte la configuration de plusieurs comptes sous `channels.mattermost.accounts` :

```json5
{
  channels: {
    mattermost: {
      accounts: {
        default: { name: "Primary", botToken: "mm-token", baseUrl: "https://chat.example.com" },
        alerts: { name: "Alerts", botToken: "mm-token-2", baseUrl: "https://alerts.example.com" },
      },
    },
  },
}
```

## Dépannage

- Pas de réponse dans le canal : Assurez-vous que le bot est dans le canal et mentionnez-le (oncall), utilisez un préfixe de déclenchement (onchar), ou définissez `chatmode: "onmessage"`.
- Erreurs d'authentification : Vérifiez le bot token, l'URL de base et que le compte est activé.
- Problèmes de comptes multiples : Les variables d'environnement s'appliquent uniquement au compte `default`.
