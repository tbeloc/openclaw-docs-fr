---
summary: "Configuration du plugin de canal QQ Bot, configuration et utilisation"
read_when:
  - You want to connect OpenClaw to QQ
  - You need QQ Bot credential setup
  - You want QQ Bot group or private chat support
title: QQ Bot
---

# QQ Bot (plugin)

QQ Bot se connecte à OpenClaw via l'API officielle QQ Bot (passerelle WebSocket). Le
plugin supporte les chats privés C2C, les messages @group, et les messages de canaux de guilde avec
des médias enrichis (images, voix, vidéo, fichiers).

Statut : supporté via plugin. Les messages directs, les chats de groupe, les canaux de guilde et
les médias sont supportés. Les réactions et les fils de discussion ne sont pas supportés.

## Plugin requis

Installez le plugin QQ Bot :

```bash
openclaw plugins install @openclaw/qqbot
```

Checkout local (lors de l'exécution à partir d'un dépôt git) :

```bash
openclaw plugins install ./extensions/qqbot
```

## Configuration

1. Allez sur la [plateforme ouverte QQ](https://q.qq.com/) et scannez le code QR avec votre
   téléphone QQ pour vous inscrire / vous connecter.
2. Cliquez sur **Créer un Bot** pour créer un nouveau bot QQ.
3. Trouvez **AppID** et **AppSecret** sur la page des paramètres du bot et copiez-les.

> AppSecret n'est pas stocké en texte brut — si vous quittez la page sans l'enregistrer,
> vous devrez en régénérer un nouveau.

4. Ajoutez le canal :

```bash
openclaw channels add --channel qqbot --token "AppID:AppSecret"
```

5. Redémarrez la passerelle.

## Configurer

Configuration minimale :

```json5
{
  channels: {
    qqbot: {
      enabled: true,
      appId: "YOUR_APP_ID",
      clientSecret: "YOUR_APP_SECRET",
    },
  },
}
```

### Configuration multi-comptes

Exécutez plusieurs bots QQ sous une seule instance OpenClaw :

```json5
{
  channels: {
    qqbot: {
      enabled: true,
      appId: "111111111",
      clientSecret: "secret-of-bot-1",
      accounts: {
        bot2: {
          enabled: true,
          appId: "222222222",
          clientSecret: "secret-of-bot-2",
        },
      },
    },
  },
}
```

Chaque compte lance sa propre connexion WebSocket et maintient un cache de jetons indépendant
(isolé par `appId`).

Ajoutez un deuxième bot via CLI :

```bash
openclaw channels add --channel qqbot --account bot2 --token "222222222:secret-of-bot-2"
```

### Voix (STT / TTS)

Le support STT et TTS utilise une configuration à deux niveaux avec repli prioritaire :

| Paramètre | Spécifique au plugin | Repli du framework        |
| --------- | -------------------- | ------------------------- |
| STT       | `channels.qqbot.stt` | `tools.media.audio.models[0]` |
| TTS       | `channels.qqbot.tts` | `messages.tts`            |

```json5
{
  channels: {
    qqbot: {
      stt: {
        provider: "your-provider",
        model: "your-stt-model",
      },
      tts: {
        provider: "your-provider",
        model: "your-tts-model",
        voice: "your-voice",
      },
    },
  },
}
```

Définissez `enabled: false` sur l'un ou l'autre pour désactiver.

## Formats de cible

| Format                     | Description        |
| -------------------------- | ------------------ |
| `qqbot:c2c:OPENID`         | Chat privé (C2C)   |
| `qqbot:group:GROUP_OPENID` | Chat de groupe     |
| `qqbot:channel:CHANNEL_ID` | Canal de guilde    |

> Chaque bot a son propre ensemble d'OpenID utilisateur. Un OpenID reçu par Bot A **ne peut pas**
> être utilisé pour envoyer des messages via Bot B.

## Commandes slash

Commandes intégrées interceptées avant la file d'attente IA :

| Commande       | Description                          |
| -------------- | ------------------------------------ |
| `/bot-ping`    | Test de latence                      |
| `/bot-version` | Afficher la version du framework OpenClaw |
| `/bot-help`    | Lister toutes les commandes          |
| `/bot-upgrade` | Afficher le lien du guide de mise à niveau QQBot |
| `/bot-logs`    | Exporter les journaux récents de la passerelle en tant que fichier |

Ajoutez `?` à n'importe quelle commande pour obtenir de l'aide sur l'utilisation (par exemple `/bot-upgrade ?`).

## Dépannage

- **Le bot répond "parti sur Mars" :** identifiants non configurés ou passerelle non démarrée.
- **Pas de messages entrants :** vérifiez que `appId` et `clientSecret` sont corrects, et que le
  bot est activé sur la plateforme ouverte QQ.
- **Les messages proactifs n'arrivent pas :** QQ peut intercepter les messages initiés par le bot si
  l'utilisateur n'a pas interagi récemment.
- **La voix n'est pas transcrite :** assurez-vous que STT est configuré et que le fournisseur est accessible.
