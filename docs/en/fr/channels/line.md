---
summary: "Configuration et utilisation du plugin LINE Messaging API, setup"
read_when:
  - You want to connect OpenClaw to LINE
  - You need LINE webhook + credential setup
  - You want LINE-specific message options
title: LINE
---

# LINE (plugin)

LINE se connecte à OpenClaw via l'API LINE Messaging. Le plugin fonctionne comme un récepteur webhook sur la passerelle et utilise votre jeton d'accès au canal + secret du canal pour l'authentification.

Statut : supporté via plugin. Les messages directs, les chats de groupe, les médias, les localisations, les messages Flex, les messages de modèle et les réponses rapides sont supportés. Les réactions et les fils de discussion ne sont pas supportés.

## Plugin requis

Installez le plugin LINE :

```bash
openclaw plugins install @openclaw/line
```

Checkout local (lors de l'exécution à partir d'un dépôt git) :

```bash
openclaw plugins install ./extensions/line
```

## Configuration

1. Créez un compte LINE Developers et ouvrez la Console :
   [https://developers.line.biz/console/](https://developers.line.biz/console/)
2. Créez (ou sélectionnez) un Provider et ajoutez un canal **Messaging API**.
3. Copiez le **jeton d'accès au canal** et le **secret du canal** à partir des paramètres du canal.
4. Activez **Use webhook** dans les paramètres de l'API Messaging.
5. Définissez l'URL du webhook sur votre point de terminaison de passerelle (HTTPS requis) :

```
https://gateway-host/line/webhook
```

La passerelle répond à la vérification du webhook de LINE (GET) et aux événements entrants (POST).
Si vous avez besoin d'un chemin personnalisé, définissez `channels.line.webhookPath` ou
`channels.line.accounts.<id>.webhookPath` et mettez à jour l'URL en conséquence.

Note de sécurité :

- La vérification de signature LINE dépend du corps (HMAC sur le corps brut), donc OpenClaw applique des limites strictes de pré-authentification du corps et un délai d'expiration avant la vérification.

## Configurer

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

`tokenFile` et `secretFile` doivent pointer vers des fichiers réguliers. Les liens symboliques sont rejetés.

Comptes multiples :

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

Les messages directs utilisent par défaut l'appairage. Les expéditeurs inconnus reçoivent un code d'appairage et leurs messages sont ignorés jusqu'à approbation.

```bash
openclaw pairing list line
openclaw pairing approve line <CODE>
```

Listes blanches et politiques :

- `channels.line.dmPolicy`: `pairing | allowlist | open | disabled`
- `channels.line.allowFrom`: IDs utilisateur LINE autorisés pour les messages directs
- `channels.line.groupPolicy`: `allowlist | open | disabled`
- `channels.line.groupAllowFrom`: IDs utilisateur LINE autorisés pour les groupes
- Remplacements par groupe : `channels.line.groups.<groupId>.allowFrom`
- Note d'exécution : si `channels.line` est complètement absent, l'exécution revient à `groupPolicy="allowlist"` pour les vérifications de groupe (même si `channels.defaults.groupPolicy` est défini).

Les IDs LINE sont sensibles à la casse. Les IDs valides ressemblent à :

- Utilisateur : `U` + 32 caractères hexadécimaux
- Groupe : `C` + 32 caractères hexadécimaux
- Salle : `R` + 32 caractères hexadécimaux

## Comportement des messages

- Le texte est divisé en chunks de 5000 caractères.
- La mise en forme Markdown est supprimée ; les blocs de code et les tableaux sont convertis en cartes Flex si possible.
- Les réponses en streaming sont mises en buffer ; LINE reçoit des chunks complets avec une animation de chargement pendant que l'agent travaille.
- Les téléchargements de médias sont limités par `channels.line.mediaMaxMb` (par défaut 10).

## Données de canal (messages enrichis)

Utilisez `channelData.line` pour envoyer des réponses rapides, des localisations, des cartes Flex ou des messages de modèle.

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

Le plugin LINE inclut également une commande `/card` pour les présets de messages Flex :

```
/card info "Welcome" "Thanks for joining!"
```

## Dépannage

- **La vérification du webhook échoue :** assurez-vous que l'URL du webhook est HTTPS et que le `channelSecret` correspond à la console LINE.
- **Aucun événement entrant :** confirmez que le chemin du webhook correspond à `channels.line.webhookPath` et que la passerelle est accessible depuis LINE.
- **Erreurs de téléchargement de médias :** augmentez `channels.line.mediaMaxMb` si les médias dépassent la limite par défaut.
