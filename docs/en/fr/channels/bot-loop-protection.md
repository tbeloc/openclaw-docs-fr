---
summary: "Valeurs par défaut de la protection contre les boucles bot-à-bot et remplacements de canal"
read_when:
  - Configuring bot-authored channel messages
  - Tuning bot-to-bot loop protection
title: "Protection contre les boucles bot"
sidebarTitle: "Protection contre les boucles bot"
---

# Protection contre les boucles bot

OpenClaw peut accepter les messages écrits par d'autres bots sur les canaux qui supportent `allowBots`.
Lorsque ce chemin est activé, la protection contre les boucles par paires empêche deux identités de bot de
se répondre l'une l'autre indéfiniment.

La protection est appliquée par le noyau de canal-tour principal. Chaque canal supporté
mappe son événement entrant dans des faits génériques : compte ou portée, identifiant de conversation,
identifiant du bot émetteur et identifiant du bot récepteur. Le noyau suit ensuite la paire de participants dans les deux
directions, applique un budget à fenêtre glissante et supprime la paire pendant un
refroidissement après que le budget soit dépassé.

## Valeurs par défaut

La protection contre les boucles par paires est active lorsqu'un canal permet aux messages rédigés par des bots d'atteindre
la distribution. Les valeurs par défaut intégrées sont :

- `maxEventsPerWindow: 20` - une paire de bots peut échanger 20 événements dans la fenêtre
- `windowSeconds: 60` - longueur de la fenêtre glissante
- `cooldownSeconds: 60` - durée de suppression après que la paire dépasse le budget

La protection n'affecte pas les messages normaux rédigés par des humains, les déploiements à bot unique,
le filtrage des auto-messages ou les réponses de bot ponctuelles qui restent sous le budget.

## Configurer les valeurs par défaut partagées

Définissez `channels.defaults.botLoopProtection` une fois pour donner à chaque canal supporté
la même ligne de base. Les remplacements de canal et de compte peuvent toujours affiner les
surfaces individuelles.

```json5
{
  channels: {
    defaults: {
      botLoopProtection: {
        maxEventsPerWindow: 20,
        windowSeconds: 60,
        cooldownSeconds: 60,
      },
    },
  },
}
```

Définissez `enabled: false` uniquement lorsque votre politique de canal autorise intentionnellement
les conversations bot-à-bot sans suppression automatique.

## Remplacer par canal ou compte

Les canaux supportés superposent leur propre configuration à la valeur par défaut partagée. L'ordre de priorité est :

- `channels.<channel>.<room-or-space>.botLoopProtection`, lorsque le canal supporte les remplacements par conversation
- `channels.<channel>.accounts.<account>.botLoopProtection`, lorsque le canal supporte les comptes
- `channels.<channel>.botLoopProtection`, lorsque le canal supporte les valeurs par défaut au niveau supérieur
- `channels.defaults.botLoopProtection`
- valeurs par défaut intégrées

```json5
{
  channels: {
    defaults: {
      botLoopProtection: {
        maxEventsPerWindow: 20,
      },
    },
    discord: {
      botLoopProtection: {
        maxEventsPerWindow: 8,
      },
      accounts: {
        molty: {
          allowBots: "mentions",
          botLoopProtection: {
            maxEventsPerWindow: 5,
            cooldownSeconds: 90,
          },
        },
      },
    },
    slack: {
      allowBots: "mentions",
      botLoopProtection: {
        maxEventsPerWindow: 8,
      },
    },
    matrix: {
      allowBots: "mentions",
      groups: {
        "!roomid:example.org": {
          botLoopProtection: {
            maxEventsPerWindow: 5,
          },
        },
      },
    },
    googlechat: {
      allowBots: true,
      groups: {
        "spaces/AAAA": {
          botLoopProtection: {
            maxEventsPerWindow: 5,
          },
        },
      },
    },
  },
}
```

## Support des canaux

- Discord : faits natifs `author.bot`, indexés par compte Discord, canal et paire de bots.
- Slack : faits natifs `bot_id` pour les messages rédigés par des bots acceptés, indexés par compte Slack, canal et paire de bots.
- Matrix : comptes de bots Matrix configurés, indexés par compte Matrix, salle et paire de bots configurée.
- Google Chat : faits natifs `sender.type=BOT` pour les messages rédigés par des bots acceptés, indexés par compte, espace et paire de bots.

Les canaux qui n'exposent pas une identité de bot entrant fiable continuent d'utiliser leurs
filtres normaux d'auto-message et de politique d'accès. Ils ne doivent pas opter pour cette
protection jusqu'à ce qu'ils puissent identifier les deux participants dans la paire de bots.

Voir [SDK runtime](/fr/plugins/sdk-runtime#reusable-runtime-utilities) pour les détails de
l'implémentation du plugin.
