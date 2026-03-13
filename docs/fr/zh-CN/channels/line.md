---
read_when:
  - 你想将 OpenClaw 连接到 LINE
  - 你需要配置 LINE webhook + 凭证
  - 你想了解 LINE 特有的消息选项
summary: LINE Messaging API 插件的配置、设置和使用方法
title: LINE
x-i18n:
  generated_at: "2026-02-03T07:43:38Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 8fbac126786f95b9454f3cc61906c2798393a8d7914e787d3755c020c7ab2da6
  source_path: channels/line.md
  workflow: 15
---

# LINE (Plugin)

LINE se connecte à OpenClaw via l'API LINE Messaging. Le plugin fonctionne comme un récepteur webhook sur la passerelle Gateway, en s'authentifiant avec votre jeton d'accès au canal + secret du canal.

Statut : Pris en charge via plugin. Supporte les messages privés, les conversations de groupe, les médias, les emplacements, les messages Flex, les messages de modèle et les réponses rapides. Les réactions emoji et les réponses de sujet ne sont pas prises en charge.

## Installation du plugin requise

Installez le plugin LINE :

```bash
openclaw plugins install @openclaw/line
```

Extraction locale (lors de l'exécution à partir du référentiel git) :

```bash
openclaw plugins install ./extensions/line
```

## Étapes de configuration

1. Créez un compte LINE Developers et ouvrez la console :
   https://developers.line.biz/console/
2. Créez (ou sélectionnez) un Provider et ajoutez un canal **Messaging API**.
3. Copiez le **Jeton d'accès au canal** et le **Secret du canal** à partir des paramètres du canal.
4. Activez **Utiliser webhook** dans les paramètres de l'API Messaging.
5. Définissez l'URL du webhook sur votre point de terminaison Gateway (doit utiliser HTTPS) :

```
https://gateway-host/line/webhook
```

La passerelle Gateway répondra à la vérification du webhook LINE (GET) et aux événements entrants (POST). Si vous avez besoin d'un chemin personnalisé, définissez `channels.line.webhookPath` ou `channels.line.accounts.<id>.webhookPath` et mettez à jour l'URL en conséquence.

## Configuration

Configuration minimale :

```json5
{
  channels: {
    line: {
      enabled: true,
      channelAccessToken: "LINE_CHANNEL_ACCESS_TOKEN",
      channelSecret: "LINE_CHANNEL_SECRET",
      dmPolicy: "pairing",
    },
  },
}
```

Variables d'environnement (compte par défaut uniquement) :

- `LINE_CHANNEL_ACCESS_TOKEN`
- `LINE_CHANNEL_SECRET`

Fichiers de jeton/secret :

```json5
{
  channels: {
    line: {
      tokenFile: "/path/to/line-token.txt",
      secretFile: "/path/to/line-secret.txt",
    },
  },
}
```

Configuration multi-comptes :

```json5
{
  channels: {
    line: {
      accounts: {
        marketing: {
          channelAccessToken: "...",
          channelSecret: "...",
          webhookPath: "/line/marketing",
        },
      },
    },
  },
}
```

## Contrôle d'accès

Les messages privés utilisent par défaut le mode d'appairage. Les expéditeurs inconnus reçoivent un code d'appairage et leurs messages sont ignorés jusqu'à approbation.

```bash
openclaw pairing list line
openclaw pairing approve line <CODE>
```

Liste d'autorisation et politiques :

- `channels.line.dmPolicy` : `pairing | allowlist | open | disabled`
- `channels.line.allowFrom` : Liste d'autorisation des ID utilisateur LINE pour les messages privés
- `channels.line.groupPolicy` : `allowlist | open | disabled`
- `channels.line.groupAllowFrom` : Liste d'autorisation des ID utilisateur LINE pour les groupes
- Remplacement par groupe : `channels.line.groups.<groupId>.allowFrom`

Les ID LINE sont sensibles à la casse. Les formats d'ID valides sont les suivants :

- Utilisateur : `U` + 32 caractères hexadécimaux
- Groupe : `C` + 32 caractères hexadécimaux
- Salle : `R` + 32 caractères hexadécimaux

## Comportement des messages

- Le texte est divisé en chunks de 5000 caractères.
- La mise en forme Markdown est supprimée ; les blocs de code et les tableaux sont convertis en cartes Flex si possible.
- Les réponses en streaming sont mises en buffer ; LINE reçoit des chunks complets avec une animation de chargement lors du traitement par l'agent.
- Le téléchargement de médias est limité par `channels.line.mediaMaxMb` (par défaut 10).

## Données de canal (messages enrichis)

Utilisez `channelData.line` pour envoyer des réponses rapides, des emplacements, des cartes Flex ou des messages de modèle.

```json5
{
  text: "Here you go",
  channelData: {
    line: {
      quickReplies: ["Status", "Help"],
      location: {
        title: "Office",
        address: "123 Main St",
        latitude: 35.681236,
        longitude: 139.767125,
      },
      flexMessage: {
        altText: "Status card",
        contents: {
          /* Flex payload */
        },
      },
      templateMessage: {
        type: "confirm",
        text: "Proceed?",
        confirmLabel: "Yes",
        confirmData: "yes",
        cancelLabel: "No",
        cancelData: "no",
      },
    },
  },
}
```

Le plugin LINE fournit également la commande `/card` pour les présets de messages Flex :

```
/card info "Welcome" "Thanks for joining!"
```

## Dépannage

- **Échec de la vérification du webhook :** Assurez-vous que l'URL du webhook utilise HTTPS et que `channelSecret` correspond à celui de la console LINE.
- **Pas d'événements entrants :** Confirmez que le chemin du webhook correspond à `channels.line.webhookPath` et que la passerelle Gateway est accessible depuis LINE.
- **Erreurs de téléchargement de médias :** Si les médias dépassent la limite par défaut, augmentez `channels.line.mediaMaxMb`.
