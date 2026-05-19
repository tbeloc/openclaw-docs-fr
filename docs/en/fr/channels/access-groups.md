---
summary: "Listes d'expéditeurs réutilisables pour les canaux de messages"
read_when:
  - Configuring the same allowlist across multiple message channels
  - Sharing DM and group sender access rules
  - Reviewing message-channel access control
title: "Groupes d'accès"
---

Les groupes d'accès sont des listes d'expéditeurs nommées que vous définissez une fois et référencez à partir des listes blanches de canaux avec `accessGroup:<name>`.

Utilisez-les quand les mêmes personnes doivent être autorisées sur plusieurs canaux de messages, ou quand un ensemble de confiance doit s'appliquer à la fois aux DM et à l'autorisation d'expéditeur de groupe.

Les groupes d'accès n'accordent pas l'accès par eux-mêmes. Un groupe n'a d'importance que lorsqu'un champ de liste blanche le référence.

## Groupes d'expéditeurs de messages statiques

Les groupes d'expéditeurs statiques utilisent `type: "message.senders"`.

```json5
{
  accessGroups: {
    operators: {
      type: "message.senders",
      members: {
        "*": ["global-owner-id"],
        discord: ["discord:123456789012345678"],
        telegram: ["987654321"],
        whatsapp: ["+15551234567"],
      },
    },
  },
}
```

Les listes de membres sont indexées par l'identifiant du canal de message :

| Clé        | Signification                                                                 |
| ---------- | ----------------------------------------------------------------------- |
| `"*"`      | Entrées partagées vérifiées pour chaque canal de message qui référence le groupe. |
| `discord`  | Entrées vérifiées uniquement pour la correspondance de la liste blanche Discord.                    |
| `telegram` | Entrées vérifiées uniquement pour la correspondance de la liste blanche Telegram.                   |
| `whatsapp` | Entrées vérifiées uniquement pour la correspondance de la liste blanche WhatsApp.                   |

Les entrées sont mises en correspondance avec les règles normales `allowFrom` du canal de destination. OpenClaw ne traduit pas les identifiants d'expéditeur entre les canaux. Si Alice a un identifiant Telegram et un identifiant Discord, listez les deux identifiants sous les clés appropriées.

## Référencer les groupes à partir des listes blanches

Référencez un groupe avec `accessGroup:<name>` n'importe où le chemin du canal de message supporte les listes blanches d'expéditeurs.

Exemple de liste blanche DM :

```json5
{
  accessGroups: {
    operators: {
      type: "message.senders",
      members: {
        discord: ["discord:123456789012345678"],
        telegram: ["987654321"],
      },
    },
  },
  channels: {
    discord: {
      dmPolicy: "allowlist",
      allowFrom: ["accessGroup:operators"],
    },
    telegram: {
      dmPolicy: "allowlist",
      allowFrom: ["accessGroup:operators"],
    },
  },
}
```

Exemple de liste blanche d'expéditeur de groupe :

```json5
{
  accessGroups: {
    oncall: {
      type: "message.senders",
      members: {
        whatsapp: ["+15551234567"],
        googlechat: ["users/1234567890"],
      },
    },
  },
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["accessGroup:oncall"],
    },
    googlechat: {
      spaces: {
        "spaces/AAA": {
          users: ["accessGroup:oncall"],
        },
      },
    },
  },
}
```

Vous pouvez mélanger les groupes et les entrées directes :

```json5
{
  channels: {
    discord: {
      dmPolicy: "allowlist",
      allowFrom: ["accessGroup:operators", "discord:123456789012345678"],
    },
  },
}
```

## Chemins de canaux de messages supportés

Les groupes d'accès sont disponibles dans les chemins d'autorisation de canaux de messages partagés, notamment :

- Les listes blanches d'expéditeurs DM telles que `channels.<channel>.allowFrom`
- Les listes blanches d'expéditeurs de groupe telles que `channels.<channel>.groupAllowFrom`
- Les listes blanches d'expéditeurs par salle spécifiques au canal qui utilisent les mêmes règles de correspondance d'expéditeur
- Les chemins d'autorisation de commande qui réutilisent les listes blanches d'expéditeurs de canaux de messages

Le support des canaux dépend du fait que ce canal soit connecté via les assistants d'autorisation d'expéditeur OpenClaw partagés. Le support groupé actuel inclut Discord, Feishu, Google Chat, iMessage, LINE, Mattermost, Microsoft Teams, Nextcloud Talk, Nostr, QQBot, Signal, WhatsApp, Zalo et Zalo Personal. Les groupes statiques `message.senders` sont conçus pour être indépendants des canaux, donc les nouveaux canaux de messages devraient les supporter en utilisant les assistants du SDK de plugin partagé au lieu de l'expansion de liste blanche personnalisée.

## Diagnostics des plugins

Les auteurs de plugins peuvent inspecter l'état structuré du groupe d'accès sans l'étendre en une liste blanche plate :

```typescript
import { resolveAccessGroupAllowFromState } from "openclaw/plugin-sdk/security-runtime";

const state = await resolveAccessGroupAllowFromState({
  accessGroups: cfg.accessGroups,
  allowFrom: channelConfig.allowFrom,
  channel: "my-channel",
  accountId: "default",
  senderId,
  isSenderAllowed,
});
```

Le résultat rapporte les groupes référencés, mis en correspondance, manquants, non supportés et échoués. Utilisez ceci quand vous avez besoin de diagnostics ou de tests de conformité. Utilisez `expandAllowFromWithAccessGroups(...)` uniquement pour les chemins de compatibilité qui s'attendent toujours à un tableau `allowFrom` plat.

## Audiences de canaux Discord

Discord supporte également un type de groupe d'accès dynamique :

```json5
{
  accessGroups: {
    maintainers: {
      type: "discord.channelAudience",
      guildId: "1456350064065904867",
      channelId: "1456744319972282449",
      membership: "canViewChannel",
    },
  },
  channels: {
    discord: {
      dmPolicy: "allowlist",
      allowFrom: ["accessGroup:maintainers"],
    },
  },
}
```

`discord.channelAudience` signifie « autoriser les expéditeurs DM Discord qui peuvent actuellement voir ce canal de guilde ». OpenClaw résout l'expéditeur via Discord au moment de l'autorisation et applique les règles de permission Discord `ViewChannel`.

Utilisez ceci quand un canal Discord est déjà la source de vérité pour une équipe, comme `#maintainers` ou `#on-call`.

Exigences et comportement en cas d'échec :

- Le bot a besoin d'accès à la guilde et au canal.
- Le bot a besoin de l'**intention des membres du serveur** du portail des développeurs Discord.
- Le groupe d'accès échoue fermé quand Discord retourne `Missing Access`, l'expéditeur ne peut pas être résolu en tant que membre de la guilde, ou le canal appartient à une autre guilde.

Plus d'exemples spécifiques à Discord : [Contrôle d'accès Discord](/fr/channels/discord#access-control-and-routing)

## Notes de sécurité

- Les groupes d'accès sont des alias de liste blanche, pas des rôles. Ils ne créent pas de propriétaires, n'approuvent pas les demandes d'appairage ou n'accordent pas les permissions d'outils par eux-mêmes.
- `dmPolicy: "open"` nécessite toujours `"*"` dans la liste blanche DM effective. Référencer un groupe d'accès n'est pas la même chose que l'accès public.
- Les noms de groupes manquants échouent fermés. Si `allowFrom` contient `accessGroup:operators` et que `accessGroups.operators` est absent, cette entrée n'autorise personne.
- Gardez les identifiants de canaux stables. Préférez les identifiants numériques/utilisateur aux noms d'affichage quand le canal supporte les deux.

## Dépannage

Si un expéditeur devrait correspondre mais est bloqué :

1. Confirmez que le champ de liste blanche contient la référence exacte `accessGroup:<name>`.
2. Confirmez que `accessGroups.<name>.type` est correct.
3. Confirmez que l'identifiant de l'expéditeur est listé sous la clé de canal correspondante, ou sous `"*"`.
4. Confirmez que l'entrée utilise la syntaxe de liste blanche normale de ce canal.
5. Pour les audiences de canaux Discord, confirmez que le bot peut voir le canal de guilde et que l'intention des membres du serveur est activée.

Exécutez `openclaw doctor` après avoir modifié la configuration du contrôle d'accès. Il détecte de nombreuses combinaisons invalides de liste blanche et de politique avant l'exécution.
