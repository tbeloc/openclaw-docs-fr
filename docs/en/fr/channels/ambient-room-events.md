---
summary: "Permettre aux salons de groupe pris en charge de fournir un contexte silencieux sauf si l'agent envoie avec l'outil de message"
read_when:
  - Configuring always-on group or channel rooms
  - You want the agent to watch room chatter without posting final text automatically
  - Debugging typing and token usage with no visible room message
title: "Événements de salon ambiant"
sidebarTitle: "Événements de salon ambiant"
---

Les événements de salon ambiant permettent à OpenClaw de traiter les discussions de groupe ou de canal non mentionnées comme un contexte silencieux. L'agent peut mettre à jour la mémoire et l'état de la session, mais le salon reste silencieux sauf si l'agent appelle explicitement l'outil `message`.

Pour les chats de groupe toujours actifs, c'est le mode recommandé : combinez `messages.groupChat.unmentionedInbound: "room_event"` avec `messages.groupChat.visibleReplies: "message_tool"`. Utilisez-le quand l'agent doit écouter, décider quand une réponse est utile, et éviter l'ancien modèle d'invite de répondre `NO_REPLY`.

Pris en charge aujourd'hui : canaux de guilde Discord, canaux Slack et canaux privés, DM multi-personnes Slack, et groupes ou supergroups Telegram. Les autres canaux de groupe conservent leur comportement de groupe existant sauf si leur page de canal indique qu'ils prennent en charge les événements de salon ambiant.

## Configuration recommandée

Définissez le comportement global du chat de groupe :

```json5
{
  messages: {
    groupChat: {
      unmentionedInbound: "room_event",
      visibleReplies: "message_tool",
      historyLimit: 50,
    },
  },
}
```

Ensuite, configurez le salon lui-même comme toujours actif en désactivant la restriction de mention pour ce salon. Le canal doit toujours être autorisé par sa `groupPolicy` normale, la liste d'autorisation du salon et la liste d'autorisation de l'expéditeur.

Après avoir enregistré la configuration, la Gateway recharge à chaud les paramètres `messages`. Redémarrez uniquement quand la surveillance de fichiers ou le rechargement de configuration est désactivé.

## Ce qui change

Avec `messages.groupChat.unmentionedInbound: "room_event"` :

- les messages de groupe ou de canal non mentionnés autorisés deviennent des événements de salon silencieux
- les messages mentionnés restent des demandes utilisateur
- les commandes texte et les commandes natives restent des demandes utilisateur
- les demandes d'abandon ou d'arrêt restent des demandes utilisateur
- les messages directs restent des demandes utilisateur

Les événements de salon utilisent une livraison visible stricte. Le texte final de l'assistant est privé. L'agent doit appeler `message(action=send)` pour publier dans le salon.

## Exemple Discord

```json5
{
  messages: {
    groupChat: {
      unmentionedInbound: "room_event",
      visibleReplies: "message_tool",
      historyLimit: 50,
    },
  },
  channels: {
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        "<DISCORD_SERVER_ID>": {
          requireMention: false,
          users: ["<YOUR_DISCORD_USER_ID>"],
        },
      },
    },
  },
}
```

Utilisez la configuration Discord par canal quand un seul canal doit être ambiant :

```json5
{
  channels: {
    discord: {
      guilds: {
        "<DISCORD_SERVER_ID>": {
          channels: {
            "<DISCORD_CHANNEL_ID_OR_NAME>": {
              allow: true,
              requireMention: false,
            },
          },
        },
      },
    },
  },
}
```

## Exemple Slack

Les listes d'autorisation de canaux Slack sont basées sur les ID. Utilisez les ID de canal tels que `C12345678`, pas `#channel-name`.

```json5
{
  messages: {
    groupChat: {
      unmentionedInbound: "room_event",
      visibleReplies: "message_tool",
      historyLimit: 50,
    },
  },
  channels: {
    slack: {
      groupPolicy: "allowlist",
      channels: {
        "<SLACK_CHANNEL_ID>": {
          allow: true,
          requireMention: false,
        },
      },
    },
  },
}
```

## Exemple Telegram

Pour les groupes Telegram, le bot doit pouvoir voir les messages de groupe normaux. Si `requireMention: false`, désactivez le mode de confidentialité BotFather ou utilisez une autre configuration Telegram qui livre le trafic de groupe complet au bot.

```json5
{
  messages: {
    groupChat: {
      unmentionedInbound: "room_event",
      visibleReplies: "message_tool",
      historyLimit: 50,
    },
  },
  channels: {
    telegram: {
      groups: {
        "<TELEGRAM_GROUP_CHAT_ID>": {
          groupPolicy: "open",
          requireMention: false,
        },
      },
    },
  },
}
```

Les ID de groupe Telegram sont généralement des nombres négatifs tels que `-1001234567890`. Lisez `chat.id` à partir de `openclaw logs --follow`, transférez un message de groupe à un bot d'aide d'ID, ou inspectez `getUpdates` de l'API Bot.

## Politique spécifique à l'agent

Utilisez un remplacement d'agent quand plusieurs agents partagent le même salon mais un seul doit traiter les discussions non mentionnées comme un contexte ambiant :

```json5
{
  messages: {
    groupChat: {
      visibleReplies: "message_tool",
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          unmentionedInbound: "room_event",
          mentionPatterns: ["@openclaw", "openclaw"],
        },
      },
    ],
  },
}
```

La valeur `agents.list[].groupChat.unmentionedInbound` spécifique à l'agent remplace `messages.groupChat.unmentionedInbound` pour cet agent.

## Modes de réponse visible

`messages.groupChat.visibleReplies` est par défaut `"automatic"` pour les demandes utilisateur normales de groupe/canal. Conservez cette valeur par défaut quand vous voulez que le texte final de l'assistant soit publié visiblement sans nécessiter un appel explicite à l'outil de message.

Pour les salons toujours actifs ambiants, `messages.groupChat.visibleReplies: "message_tool"` est toujours recommandé, en particulier avec les modèles de dernière génération fiables pour les outils tels que GPT 5.5. Cela permet à l'agent de décider quand parler en appelant l'outil de message. Si le modèle retourne du texte final sans appeler l'outil, OpenClaw garde ce texte final privé et enregistre les métadonnées de livraison supprimées.

Les événements de salon restent stricts même quand d'autres demandes de groupe utilisent des réponses automatiques. Les événements de salon ambiant non mentionnés nécessitent toujours `message(action=send)` pour une sortie visible.

## Historique

`messages.groupChat.historyLimit` contrôle la valeur par défaut globale de l'historique de groupe. Les canaux peuvent la remplacer avec `channels.<channel>.historyLimit`, et certains canaux prennent également en charge les limites d'historique par compte.

Définissez `historyLimit: 0` pour désactiver le contexte d'historique de groupe.

Les canaux d'événement de salon pris en charge conservent les messages de salon ambiant récents comme contexte. Discord conserve l'historique des événements de salon jusqu'à ce qu'un envoi Discord visible réussisse, de sorte que le contexte silencieux n'est pas perdu avant la livraison de l'outil de message.

## Dépannage

Si le salon affiche la saisie ou l'utilisation de jetons mais aucun message visible :

1. Confirmez que le salon est autorisé par la liste d'autorisation du canal et la liste d'autorisation de l'expéditeur.
2. Confirmez que `requireMention: false` est défini au niveau du salon que vous attendez.
3. Vérifiez si `messages.groupChat.unmentionedInbound` ou le remplacement de l'agent est `"room_event"`.
4. Inspectez les journaux pour les métadonnées de charge utile finale supprimées ou `didSendViaMessagingTool: false`.
5. Pour les demandes de groupe normales, conservez ou restaurez `messages.groupChat.visibleReplies: "automatic"` si vous voulez que les réponses finales soient publiées automatiquement. Pour les salons ambiants utilisant `message_tool`, utilisez un modèle/runtime qui appelle les outils de manière fiable.

Si les salons ambiants Telegram ne se déclenchent pas du tout, vérifiez le mode de confidentialité BotFather et vérifiez que la Gateway reçoit les messages de groupe normaux.

Si les salons ambiants Slack ne se déclenchent pas, vérifiez que la clé de canal est l'ID de canal Slack et que l'application a la portée requise `channels:history` ou `groups:history` pour ce type de salon.

## Connexes

- [Groups](/fr/channels/groups)
- [Discord](/fr/channels/discord)
- [Slack](/fr/channels/slack)
- [Telegram](/fr/channels/telegram)
- [Channel troubleshooting](/fr/channels/troubleshooting)
- [Channel configuration reference](/fr/gateway/config-channels)
