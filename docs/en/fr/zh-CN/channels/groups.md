---
read_when:
  - Modification du comportement des groupes ou des restrictions de mention
summary: Comportement des groupes multiplateforme (WhatsApp/Telegram/Discord/Slack/Signal/iMessage/Microsoft Teams)
title: Groupes
x-i18n:
  generated_at: "2026-02-03T07:47:08Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b727a053edf51f6e7b5c0c324c2fc9c9789a9796c37f622418bd555e8b5a0ec4
  source_path: channels/groups.md
  workflow: 15
---

# Groupes

OpenClaw gère uniformément les chats de groupe sur toutes les plateformes : WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Microsoft Teams.

## Démarrage rapide (2 minutes)

OpenClaw « s'exécute » sur votre propre compte de messagerie. Il n'y a pas d'utilisateur bot WhatsApp séparé. Si **vous** êtes dans un groupe, OpenClaw peut voir le groupe et y répondre.

Comportement par défaut :

- Les groupes sont restreints (`groupPolicy: "allowlist"`).
- Les réponses nécessitent une mention @ sauf si vous désactivez explicitement la restriction de mention.

Explication : Les expéditeurs de la liste d'autorisation peuvent déclencher OpenClaw via une mention.

> En résumé
>
> - **L'accès aux messages privés** est contrôlé par `*.allowFrom`.
> - **L'accès aux groupes** est contrôlé par `*.groupPolicy` + liste d'autorisation (`*.groups`, `*.groupAllowFrom`).
> - **Le déclenchement des réponses** est contrôlé par les restrictions de mention (`requireMention`, `/activation`).

Flux rapide (ce qui se passe avec un message de groupe) :

```
groupPolicy? disabled -> Abandonner
groupPolicy? allowlist -> Groupe autorisé? Non -> Abandonner
requireMention? Oui -> Mentionné? Non -> Stocker uniquement comme contexte
Sinon -> Répondre
```

![Flux des messages de groupe](/images/groups-flow.svg)

Si vous voulez...
| Objectif | Configurer quoi |
|----------|-----------------|
| Autoriser tous les groupes mais répondre uniquement si @ mentionné | `groups: { "*": { requireMention: true } }` |
| Désactiver toutes les réponses de groupe | `groupPolicy: "disabled"` |
| Seulement des groupes spécifiques | `groups: { "<group-id>": { ... } }`(pas de clé `"*"`) |
| Seulement vous pouvez déclencher dans les groupes | `groupPolicy: "allowlist"`, `groupAllowFrom: ["+1555..."]` |

## Clés de session

- Les sessions de groupe utilisent la clé de session `agent:<agentId>:<channel>:group:<id>` (les salons/canaux utilisent `agent:<agentId>:<channel>:channel:<id>`).
- Les sujets des forums Telegram ajoutent `:topic:<threadId>` après l'ID du groupe, donc chaque sujet a sa propre session.
- Les messages privés utilisent la session principale (ou les sessions respectives lors de la configuration par expéditeur).
- Les sessions de groupe ignorent les battements de cœur.

## Modèle : Messages privés personnels + Groupes publics (agent unique)

Oui — cela fonctionne bien si votre trafic « personnel » est des **messages privés** et votre trafic « public » est des **groupes**.

Raison : En mode agent unique, les messages privés tombent généralement dans la clé de session **principale** (`agent:main:main`), tandis que les groupes utilisent toujours des clés de session **non-principales** (`agent:main:<channel>:group:<id>`). Si vous activez l'isolation sandbox avec `mode: "non-main"`, ces sessions de groupe s'exécutent dans Docker tandis que votre session de message privé principal reste sur l'hôte.

Cela vous donne un « cerveau » d'agent (espace de travail partagé + mémoire), mais deux postures d'exécution :

- **Messages privés** : Outils complets (hôte)
- **Groupes** : Sandbox + outils restreints (Docker)

> Si vous avez besoin d'espaces de travail/rôles vraiment indépendants (« personnel » et « public » ne doivent jamais se mélanger), utilisez un deuxième agent + liaison. Voir [Routage multi-agent](/concepts/multi-agent).

Exemple (messages privés sur l'hôte, groupes isolés en sandbox + outils de messagerie uniquement) :

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // groupes/canaux sont non-principaux -> isolés en sandbox
        scope: "session", // isolation la plus forte (un conteneur par groupe/canal)
        workspaceAccess: "none",
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        // Si allow est non vide, tous les autres outils sont bloqués (deny a toujours priorité).
        allow: ["group:messaging", "group:sessions"],
        deny: ["group:runtime", "group:fs", "group:ui", "nodes", "cron", "gateway"],
      },
    },
  },
}
```

Vous voulez « les groupes ne peuvent voir que le dossier X » au lieu de « pas d'accès à l'hôte » ? Gardez `workspaceAccess: "none"` et montez uniquement les chemins autorisés dans le sandbox :

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "none",
        docker: {
          binds: [
            // hostPath:containerPath:mode
            "~/FriendsShared:/data:ro",
          ],
        },
      },
    },
  },
}
```

Connexes :

- Clés de configuration et valeurs par défaut : [Configuration de la passerelle](/gateway/configuration#agentsdefaultssandbox)
- Déboguer pourquoi les outils sont bloqués : [Sandbox vs Politique des outils vs Élévation](/gateway/sandbox-vs-tool-policy-vs-elevated)
- Détails des montages de liaison : [Isolation sandbox](/gateway/sandboxing#custom-bind-mounts)

## Étiquettes d'affichage

- Les étiquettes UI utilisent `displayName` quand disponible, au format `<channel>:<token>`.
- `#room` est réservé aux salons/canaux ; les chats de groupe utilisent `g-<slug>` (minuscules, espaces -> `-`, conservent `#@+._-`).

## Politique de groupe

Contrôle comment chaque canal traite les messages de groupe/salon :

```json5
{
  channels: {
    whatsapp: {
      groupPolicy: "disabled", // "open" | "disabled" | "allowlist"
      groupAllowFrom: ["+15551234567"],
    },
    telegram: {
      groupPolicy: "disabled",
      groupAllowFrom: ["123456789", "@username"],
    },
    signal: {
      groupPolicy: "disabled",
      groupAllowFrom: ["+15551234567"],
    },
    imessage: {
      groupPolicy: "disabled",
      groupAllowFrom: ["chat_id:123"],
    },
    msteams: {
      groupPolicy: "disabled",
      groupAllowFrom: ["user@org.com"],
    },
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        GUILD_ID: { channels: { help: { allow: true } } },
      },
    },
    slack: {
      groupPolicy: "allowlist",
      channels: { "#general": { allow: true } },
    },
    matrix: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["@owner:example.org"],
      groups: {
        "!roomId:example.org": { allow: true },
        "#alias:example.org": { allow: true },
      },
    },
  },
}
```

| Politique     | Comportement                                                |
| ------------- | ----------------------------------------------------------- |
| `"open"`      | Les groupes contournent la liste d'autorisation ; les restrictions de mention s'appliquent toujours. |
| `"disabled"`  | Bloque complètement tous les messages de groupe.            |
| `"allowlist"` | Autorise uniquement les groupes/salons correspondant à la liste d'autorisation configurée. |

Remarques :

- `groupPolicy` est séparé des restrictions de mention (nécessite @ mention).
- WhatsApp/Telegram/Signal/iMessage/Microsoft Teams : utilisez `groupAllowFrom` (secours : `allowFrom` explicite).
- Discord : la liste d'autorisation utilise `channels.discord.guilds.<id>.channels`.
- Slack : la liste d'autorisation utilise `channels.slack.channels`.
- Matrix : la liste d'autorisation utilise `channels.matrix.groups` (ID de salon, alias ou nom). Utilisez `channels.matrix.groupAllowFrom` pour restreindre les expéditeurs ; supporte aussi une liste d'autorisation `users` par salon.
- Les messages privés de groupe sont contrôlés séparément (`channels.discord.dm.*`, `channels.slack.dm.*`).
- La liste d'autorisation Telegram peut correspondre à l'ID utilisateur (`"123456789"`, `"telegram:123456789"`, `"tg:123456789"`) ou au nom d'utilisateur (`"@alice"` ou `"alice"`); les préfixes ne sont pas sensibles à la casse.
- Par défaut `groupPolicy: "allowlist"` ; si votre liste d'autorisation de groupe est vide, les messages de groupe seront bloqués.

Modèle mental rapide (ordre d'évaluation des messages de groupe) :

1. `groupPolicy` (open/disabled/allowlist)
2. Liste d'autorisation de groupe (`*.groups`, `*.groupAllowFrom`, listes d'autorisation spécifiques au canal)
3. Restrictions de mention (`requireMention`, `/activation`)

## Restrictions de mention (par défaut)

Les messages de groupe nécessitent une mention, sauf s'ils sont remplacés par groupe. Les valeurs par défaut se trouvent sous `*.groups."*"` dans chaque sous-système.

Répondre aux messages du bot est considéré comme une mention implicite (quand les métadonnées de réponse du canal sont supportées). Cela s'applique à Telegram, WhatsApp, Slack, Discord et Microsoft Teams.

```json5
{
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true },
        "123@g.us": { requireMention: false },
      },
    },
    telegram: {
      groups: {
        "*": { requireMention: true },
        "123456789": { requireMention: false },
      },
    },
    imessage: {
      groups: {
        "*": { requireMention: true },
        "123": { requireMention: false },
      },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          mentionPatterns: ["@openclaw", "openclaw", "\\+15555550123"],
          historyLimit: 50,
        },
      },
    ],
  },
}
```

Remarques :

- `mentionPatterns` sont des expressions régulières insensibles à la casse.
- Les plateformes avec mentions explicites passent toujours ; les modèles sont un secours.
- Remplacement par agent : `agents.list[].groupChat.mentionPatterns` (utile quand plusieurs agents partagent un groupe).
- Les restrictions de mention ne sont appliquées que si la détection de mention est viable (mentions natives ou `mentionPatterns` configurés).
- La valeur par défaut Discord se trouve sous `channels.discord.guilds."*"` (peut être remplacée par serveur/canal).
- Le contexte de l'historique de groupe est enveloppé uniformément entre les canaux et est **en attente uniquement** (messages ignorés en raison des restrictions de mention) ; utilisez `messages.groupChat.historyLimit` comme valeur par défaut globale, `channels.<channel>.historyLimit` (ou `channels.<channel>.accounts.*.historyLimit`) pour les remplacements. Définissez `0` pour désactiver.

## Restrictions d'outils de groupe/canal (optionnel)

Certaines configurations de canal supportent la limitation des outils disponibles **dans des groupes/salons/canaux spécifiques**.

- `tools` : autoriser/refuser les outils pour l'ensemble du groupe.
- `toolsBySender` : remplacements par expéditeur dans le groupe (les clés sont l'ID expéditeur/nom d'utilisateur/email/numéro de téléphone, selon le canal). Utilisez `"*"` comme caractère générique.

Ordre de résolution (le plus spécifique en premier) :

1. Correspondance `toolsBySender` du groupe/canal
2. `tools` du groupe/canal
3. Correspondance `toolsBySender` par défaut (`"*"`)
4. `tools` par défaut (`"*"`)

Exemple (Telegram) :

```json5
{
  channels: {
    telegram: {
      groups: {
        "*": { tools: { deny: ["exec"] } },
        "-1001234567890": {
          tools: { deny: ["exec", "read", "write"] },
          toolsBySender: {
            "123456789": { alsoAllow: ["exec"] },
          },
        },
      },
    },
  },
}
```

Remarques :

- Les restrictions d'outils de groupe/canal s'appliquent en plus de la politique d'outils globale/agent (deny a toujours priorité).
- Certains canaux utilisent des structures d'imbrication différentes pour les salons/canaux (par exemple, Discord `guilds.*.channels.*`, Slack `channels.*`, MS Teams `teams.*.channels.*`).

## Liste d'autorisation de groupe

Quand `channels.whatsapp.groups`, `channels.telegram.groups` ou `channels.imessage.groups` sont configurés, les clés agissent comme une liste d'autorisation de groupe. Utilisez `"*"` pour autoriser tous les groupes tout en définissant le comportement de mention par défaut.

Intentions courantes (copier/coller) :

1. Désactiver toutes les réponses de groupe

```json5
{
  channels: { whatsapp: { groupPolicy: "disabled" } },
}
```

2. Autoriser uniquement des groupes spécifiques (WhatsApp)

```json5
{
  channels: {
    whatsapp: {
      groups: {
        "123@g.us": { requireMention: true },
        "456@g.us": { requireMention: false },
      },
    },
  },
}
```

3. Autoriser tous les groupes mais nécessiter une mention (explicite)

```json5
{
  channels: {
    whatsapp: {
      groups: { "*": { requireMention: true } },
    },
