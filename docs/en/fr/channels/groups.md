---
summary: "Comportement des chats de groupe sur plusieurs surfaces (WhatsApp/Telegram/Discord/Slack/Signal/iMessage/Microsoft Teams/Zalo)"
read_when:
  - Changing group chat behavior or mention gating
title: "Groupes"
---

# Groupes

OpenClaw traite les chats de groupe de manière cohérente sur plusieurs surfaces : WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Microsoft Teams, Zalo.

## Introduction pour débutants (2 minutes)

OpenClaw « vit » sur vos propres comptes de messagerie. Il n'y a pas d'utilisateur bot WhatsApp séparé.
Si **vous** êtes dans un groupe, OpenClaw peut voir ce groupe et y répondre.

Comportement par défaut :

- Les groupes sont restreints (`groupPolicy: "allowlist"`).
- Les réponses nécessitent une mention sauf si vous désactivez explicitement la mention gating.

Traduction : les expéditeurs autorisés peuvent déclencher OpenClaw en le mentionnant.

> TL;DR
>
> - **L'accès aux DM** est contrôlé par `*.allowFrom`.
> - **L'accès aux groupes** est contrôlé par `*.groupPolicy` + listes blanches (`*.groups`, `*.groupAllowFrom`).
> - **Le déclenchement des réponses** est contrôlé par mention gating (`requireMention`, `/activation`).

Flux rapide (ce qui se passe avec un message de groupe) :

```
groupPolicy? disabled -> drop
groupPolicy? allowlist -> group allowed? no -> drop
requireMention? yes -> mentioned? no -> store for context only
otherwise -> reply
```

![Flux des messages de groupe](/images/groups-flow.svg)

Si vous voulez...

| Objectif                                         | Ce qu'il faut définir                                       |
| ------------------------------------------------ | ----------------------------------------------------------- |
| Autoriser tous les groupes mais répondre uniquement sur @mentions | `groups: { "*": { requireMention: true } }`                |
| Désactiver toutes les réponses de groupe                    | `groupPolicy: "disabled"`                                  |
| Seulement des groupes spécifiques                         | `groups: { "<group-id>": { ... } }` (pas de clé `"*"`)     |
| Seul vous pouvez déclencher dans les groupes               | `groupPolicy: "allowlist"`, `groupAllowFrom: ["+1555..."]` |

## Clés de session

- Les sessions de groupe utilisent les clés de session `agent:<agentId>:<channel>:group:<id>` (les salons/canaux utilisent `agent:<agentId>:<channel>:channel:<id>`).
- Les sujets du forum Telegram ajoutent `:topic:<threadId>` à l'ID du groupe pour que chaque sujet ait sa propre session.
- Les chats directs utilisent la session principale (ou par expéditeur si configuré).
- Les battements de cœur sont ignorés pour les sessions de groupe.

## Modèle : DM personnels + groupes publics (agent unique)

Oui — cela fonctionne bien si votre trafic « personnel » est des **DM** et votre trafic « public » est des **groupes**.

Pourquoi : en mode agent unique, les DM atterrissent généralement dans la clé de session **principale** (`agent:main:main`), tandis que les groupes utilisent toujours des clés de session **non-principales** (`agent:main:<channel>:group:<id>`). Si vous activez le sandboxing avec `mode: "non-main"`, ces sessions de groupe s'exécutent dans Docker tandis que votre session DM principale reste sur l'hôte.

Cela vous donne un « cerveau » d'agent (espace de travail partagé + mémoire), mais deux postures d'exécution :

- **DM** : outils complets (hôte)
- **Groupes** : sandbox + outils restreints (Docker)

> Si vous avez besoin d'espaces de travail/personas vraiment séparés (« personnel » et « public » ne doivent jamais se mélanger), utilisez un deuxième agent + liaisons. Voir [Routage Multi-Agent](/concepts/multi-agent).

Exemple (DM sur l'hôte, groupes sandboxés + outils de messagerie uniquement) :

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // groups/channels are non-main -> sandboxed
        scope: "session", // strongest isolation (one container per group/channel)
        workspaceAccess: "none",
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        // If allow is non-empty, everything else is blocked (deny still wins).
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
            "/home/user/FriendsShared:/data:ro",
          ],
        },
      },
    },
  },
}
```

Connexes :

- Clés de configuration et valeurs par défaut : [Configuration de la passerelle](/gateway/configuration#agentsdefaultssandbox)
- Débogage de la raison pour laquelle un outil est bloqué : [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated)
- Détails des montages de liaison : [Sandboxing](/gateway/sandboxing#custom-bind-mounts)

## Étiquettes d'affichage

- Les étiquettes de l'interface utilisateur utilisent `displayName` quand disponible, formatées comme `<channel>:<token>`.
- `#room` est réservé aux salons/canaux ; les chats de groupe utilisent `g-<slug>` (minuscules, espaces -> `-`, conservent `#@+._-`).

## Politique de groupe

Contrôlez comment les messages de groupe/salon sont traités par canal :

```json5
{
  channels: {
    whatsapp: {
      groupPolicy: "disabled", // "open" | "disabled" | "allowlist"
      groupAllowFrom: ["+15551234567"],
    },
    telegram: {
      groupPolicy: "disabled",
      groupAllowFrom: ["123456789"], // numeric Telegram user id (wizard can resolve @username)
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

| Politique     | Comportement                                                 |
| ------------- | ------------------------------------------------------------ |
| `"open"`      | Les groupes contournent les listes blanches ; mention-gating s'applique toujours. |
| `"disabled"`  | Bloquer complètement tous les messages de groupe.            |
| `"allowlist"` | Autoriser uniquement les groupes/salons qui correspondent à la liste blanche configurée. |

Notes :

- `groupPolicy` est séparé de mention-gating (qui nécessite des @mentions).
- WhatsApp/Telegram/Signal/iMessage/Microsoft Teams/Zalo : utilisez `groupAllowFrom` (secours : `allowFrom` explicite).
- Les approbations d'appairage DM (`*-allowFrom` entrées de magasin) s'appliquent uniquement à l'accès DM ; l'autorisation de l'expéditeur du groupe reste explicite aux listes blanches du groupe.
- Discord : la liste blanche utilise `channels.discord.guilds.<id>.channels`.
- Slack : la liste blanche utilise `channels.slack.channels`.
- Matrix : la liste blanche utilise `channels.matrix.groups` (IDs de salle, alias ou noms). Utilisez `channels.matrix.groupAllowFrom` pour restreindre les expéditeurs ; les listes blanches `users` par salle sont également supportées.
- Les DM de groupe sont contrôlés séparément (`channels.discord.dm.*`, `channels.slack.dm.*`).
- La liste blanche Telegram peut correspondre à des IDs utilisateur (`"123456789"`, `"telegram:123456789"`, `"tg:123456789"`) ou des noms d'utilisateur (`"@alice"` ou `"alice"`); les préfixes sont insensibles à la casse.
- La valeur par défaut est `groupPolicy: "allowlist"` ; si votre liste blanche de groupe est vide, les messages de groupe sont bloqués.
- Sécurité à l'exécution : quand un bloc de fournisseur est complètement absent (`channels.<provider>` absent), la politique de groupe revient à un mode fermé (généralement `allowlist`) au lieu d'hériter de `channels.defaults.groupPolicy`.

Modèle mental rapide (ordre d'évaluation pour les messages de groupe) :

1. `groupPolicy` (open/disabled/allowlist)
2. listes blanches de groupe (`*.groups`, `*.groupAllowFrom`, liste blanche spécifique au canal)
3. mention gating (`requireMention`, `/activation`)

## Mention gating (par défaut)

Les messages de groupe nécessitent une mention sauf s'ils sont remplacés par groupe. Les valeurs par défaut vivent par sous-système sous `*.groups."*"`.

Répondre à un message de bot compte comme une mention implicite (quand le canal supporte les métadonnées de réponse). Cela s'applique à Telegram, WhatsApp, Slack, Discord et Microsoft Teams.

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

Notes :

- `mentionPatterns` sont des regex insensibles à la casse.
- Les surfaces qui fournissent des mentions explicites passent toujours ; les modèles sont un secours.
- Remplacement par agent : `agents.list[].groupChat.mentionPatterns` (utile quand plusieurs agents partagent un groupe).
- Mention gating n'est appliqué que quand la détection de mention est possible (mentions natives ou `mentionPatterns` sont configurés).
- Les valeurs par défaut Discord vivent dans `channels.discord.guilds."*"` (remplaçable par guilde/canal).
- Le contexte d'historique de groupe est enveloppé uniformément sur les canaux et est **pending-only** (messages ignorés en raison de mention gating) ; utilisez `messages.groupChat.historyLimit` pour la valeur par défaut globale et `channels.<channel>.historyLimit` (ou `channels.<channel>.accounts.*.historyLimit`) pour les remplacements. Définissez `0` pour désactiver.

## Restrictions d'outils de groupe/canal (optionnel)

Certaines configurations de canal supportent la restriction des outils disponibles **à l'intérieur d'un groupe/salon/canal spécifique**.

- `tools` : autoriser/refuser les outils pour tout le groupe.
- `toolsBySender` : remplacements par expéditeur dans le groupe.
  Utilisez des préfixes de clé explicites :
  `id:<senderId>`, `e164:<phone>`, `username:<handle>`, `name:<displayName>`, et le joker `"*"`.
  Les clés non préfixées héritées sont toujours acceptées et correspondent à `id:` uniquement.

Ordre de résolution (le plus spécifique gagne) :

1. correspondance `toolsBySender` de groupe/canal
2. `tools` de groupe/canal
3. correspondance `toolsBySender` par défaut (`"*"`)
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
            "id:123456789": { alsoAllow: ["exec"] },
          },
        },
      },
    },
  },
}
```

Notes :

- Les restrictions d'outils de groupe/canal sont appliquées en plus de la politique d'outils globale/agent (deny gagne toujours).
- Certains canaux utilisent un imbrication différente pour les salons/canaux (par ex. Discord `guilds.*.channels.*`, Slack `channels.*`, MS Teams `teams.*.channels.*`).

## Listes blanches de groupe

Quand `channels.whatsapp.groups`, `channels.telegram.groups`, ou `channels.imessage.groups` est configuré, les clés agissent comme une liste blanche de groupe. Utilisez `"*"` pour autoriser tous les groupes tout en définissant le comportement de mention par défaut.

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
  },
}
```

4. Seul le propriétaire peut déclencher dans les groupes (WhatsApp)

```json5
{
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
      groups: { "*": { requireMention: true } },
    },
  },
}
```

## Activation (propriétaire uniquement)

Les propriétaires de groupe peuvent basculer l'activation par groupe :

- `/activation mention`
- `/activation always`

Le propriétaire est déterminé par `channels.whatsapp.allowFrom` (ou le E.164 auto du bot quand non défini). Envoyez la commande comme un message autonome. Les autres surfaces ignorent actuellement `/activation`.

## Champs de contexte

Les ensembles de charges utiles entrantes de groupe définissent :

- `ChatType=group`
- `GroupSubject` (si connu)
- `GroupMembers` (si connu)
- `WasMentioned` (résultat du filtrage des mentions)
- Les sujets de forum Telegram incluent également `MessageThreadId` et `IsForum`.

L'invite système de l'agent inclut une introduction de groupe au premier tour d'une nouvelle session de groupe. Elle rappelle au modèle de répondre comme un humain, d'éviter les tableaux Markdown et d'éviter de taper des séquences littérales `\n`.

## Spécificités d'iMessage

- Préférez `chat_id:<id>` lors du routage ou de la mise en liste blanche.
- Lister les chats : `imsg chats --limit 20`.
- Les réponses de groupe reviennent toujours au même `chat_id`.

## Spécificités de WhatsApp

Voir [Messages de groupe](/channels/group-messages) pour le comportement spécifique à WhatsApp (injection d'historique, détails de gestion des mentions).
