---
summary: "Routage multi-agent : agents isolés, comptes de canal et liaisons"
title: Routage Multi-Agent
read_when: "Vous voulez plusieurs agents isolés (espaces de travail + auth) dans un processus Gateway."
status: active
---

# Routage Multi-Agent

Objectif : plusieurs agents _isolés_ (espace de travail séparé + `agentDir` + sessions), plus plusieurs comptes de canal (par exemple deux WhatsApps) dans une Gateway en cours d'exécution. Le trafic entrant est acheminé vers un agent via des liaisons.

## Qu'est-ce qu'« un agent » ?

Un **agent** est un cerveau entièrement délimité avec ses propres :

- **Espace de travail** (fichiers, AGENTS.md/SOUL.md/USER.md, notes locales, règles de persona).
- **Répertoire d'état** (`agentDir`) pour les profils d'authentification, le registre de modèles et la configuration par agent.
- **Magasin de sessions** (historique de chat + état de routage) sous `~/.openclaw/agents/<agentId>/sessions`.

Les profils d'authentification sont **par agent**. Chaque agent lit à partir de :

```text
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

Les identifiants principaux de l'agent ne sont **pas** partagés automatiquement. Ne réutilisez jamais `agentDir`
entre les agents (cela provoque des collisions d'authentification/session). Si vous souhaitez partager des identifiants,
copiez `auth-profiles.json` dans le `agentDir` de l'autre agent.

Les compétences sont par agent via le dossier `skills/` de chaque espace de travail, avec des compétences partagées
disponibles à partir de `~/.openclaw/skills`. Voir [Compétences : par agent vs partagées](/tools/skills#per-agent-vs-shared-skills).

La Gateway peut héberger **un agent** (par défaut) ou **plusieurs agents** côte à côte.

**Note sur l'espace de travail :** l'espace de travail de chaque agent est le **répertoire de travail par défaut**, pas un bac à sable strict. Les chemins relatifs se résolvent à l'intérieur de l'espace de travail, mais les chemins absolus peuvent atteindre d'autres emplacements d'hôte sauf si le bac à sable est activé. Voir
[Bac à sable](/gateway/sandboxing).

## Chemins (carte rapide)

- Config : `~/.openclaw/openclaw.json` (ou `OPENCLAW_CONFIG_PATH`)
- Répertoire d'état : `~/.openclaw` (ou `OPENCLAW_STATE_DIR`)
- Espace de travail : `~/.openclaw/workspace` (ou `~/.openclaw/workspace-<agentId>`)
- Répertoire agent : `~/.openclaw/agents/<agentId>/agent` (ou `agents.list[].agentDir`)
- Sessions : `~/.openclaw/agents/<agentId>/sessions`

### Mode agent unique (par défaut)

Si vous ne faites rien, OpenClaw exécute un seul agent :

- `agentId` par défaut à **`main`**.
- Les sessions sont indexées comme `agent:main:<mainKey>`.
- L'espace de travail par défaut est `~/.openclaw/workspace` (ou `~/.openclaw/workspace-<profile>` quand `OPENCLAW_PROFILE` est défini).
- L'état par défaut est `~/.openclaw/agents/main/agent`.

## Assistant agent

Utilisez l'assistant agent pour ajouter un nouvel agent isolé :

```bash
openclaw agents add work
```

Ensuite, ajoutez des `bindings` (ou laissez l'assistant le faire) pour acheminer les messages entrants.

Vérifiez avec :

```bash
openclaw agents list --bindings
```

## Démarrage rapide

<Steps>
  <Step title="Créer chaque espace de travail agent">

Utilisez l'assistant ou créez les espaces de travail manuellement :

```bash
openclaw agents add coding
openclaw agents add social
```

Chaque agent obtient son propre espace de travail avec `SOUL.md`, `AGENTS.md` et optionnellement `USER.md`, plus un `agentDir` dédié et un magasin de sessions sous `~/.openclaw/agents/<agentId>`.

  </Step>

  <Step title="Créer des comptes de canal">

Créez un compte par agent sur vos canaux préférés :

- Discord : un bot par agent, activez Message Content Intent, copiez chaque token.
- Telegram : un bot par agent via BotFather, copiez chaque token.
- WhatsApp : liez chaque numéro de téléphone par compte.

```bash
openclaw channels login --channel whatsapp --account work
```

Voir les guides de canal : [Discord](/channels/discord), [Telegram](/channels/telegram), [WhatsApp](/channels/whatsapp).

  </Step>

  <Step title="Ajouter des agents, des comptes et des liaisons">

Ajoutez des agents sous `agents.list`, des comptes de canal sous `channels.<channel>.accounts`, et connectez-les avec des `bindings` (exemples ci-dessous).

  </Step>

  <Step title="Redémarrer et vérifier">

```bash
openclaw gateway restart
openclaw agents list --bindings
openclaw channels status --probe
```

  </Step>
</Steps>

## Plusieurs agents = plusieurs personnes, plusieurs personnalités

Avec **plusieurs agents**, chaque `agentId` devient une **persona entièrement isolée** :

- **Différents numéros de téléphone/comptes** (par `accountId` de canal).
- **Différentes personnalités** (fichiers d'espace de travail par agent comme `AGENTS.md` et `SOUL.md`).
- **Auth + sessions séparées** (pas de communication croisée sauf si explicitement activée).

Cela permet à **plusieurs personnes** de partager un serveur Gateway tout en gardant leurs « cerveaux » IA et données isolés.

## Un numéro WhatsApp, plusieurs personnes (division DM)

Vous pouvez acheminer **différents DM WhatsApp** vers différents agents tout en restant sur **un seul compte WhatsApp**. Faites correspondre l'expéditeur E.164 (comme `+15551234567`) avec `peer.kind: "direct"`. Les réponses proviennent toujours du même numéro WhatsApp (pas d'identité d'expéditeur par agent).

Détail important : les chats directs s'effondrent à la **clé de session principale** de l'agent, donc l'isolation véritable nécessite **un agent par personne**.

Exemple :

```json5
{
  agents: {
    list: [
      { id: "alex", workspace: "~/.openclaw/workspace-alex" },
      { id: "mia", workspace: "~/.openclaw/workspace-mia" },
    ],
  },
  bindings: [
    {
      agentId: "alex",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230001" } },
    },
    {
      agentId: "mia",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230002" } },
    },
  ],
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551230001", "+15551230002"],
    },
  },
}
```

Notes :

- Le contrôle d'accès DM est **global par compte WhatsApp** (appairage/liste blanche), pas par agent.
- Pour les groupes partagés, liez le groupe à un agent ou utilisez [Groupes de diffusion](/channels/broadcast-groups).

## Règles de routage (comment les messages choisissent un agent)

Les liaisons sont **déterministes** et **la plus spécifique gagne** :

1. Correspondance `peer` (ID DM/groupe/canal exact)
2. Correspondance `parentPeer` (héritage de thread)
3. `guildId + roles` (routage par rôle Discord)
4. `guildId` (Discord)
5. `teamId` (Slack)
6. Correspondance `accountId` pour un canal
7. Correspondance au niveau du canal (`accountId: "*"`)
8. Retour à l'agent par défaut (`agents.list[].default`, sinon première entrée de liste, par défaut : `main`)

Si plusieurs liaisons correspondent au même niveau, la première dans l'ordre de configuration gagne.
Si une liaison définit plusieurs champs de correspondance (par exemple `peer` + `guildId`), tous les champs spécifiés sont requis (sémantique `AND`).

Détail important sur la portée du compte :

- Une liaison qui omet `accountId` correspond uniquement au compte par défaut.
- Utilisez `accountId: "*"` pour un repli à l'échelle du canal sur tous les comptes.
- Si vous ajoutez ultérieurement la même liaison pour le même agent avec un ID de compte explicite, OpenClaw met à niveau la liaison existante au niveau du canal vers une portée de compte au lieu de la dupliquer.

## Plusieurs comptes / numéros de téléphone

Les canaux qui supportent **plusieurs comptes** (par exemple WhatsApp) utilisent `accountId` pour identifier
chaque connexion. Chaque `accountId` peut être acheminé vers un agent différent, donc un serveur peut héberger
plusieurs numéros de téléphone sans mélanger les sessions.

Si vous voulez un compte par défaut à l'échelle du canal quand `accountId` est omis, définissez
`channels.<channel>.defaultAccount` (optionnel). Quand non défini, OpenClaw revient à
`default` s'il est présent, sinon le premier ID de compte configuré (trié).

Les canaux courants supportant ce modèle incluent :

- `whatsapp`, `telegram`, `discord`, `slack`, `signal`, `imessage`
- `irc`, `line`, `googlechat`, `mattermost`, `matrix`, `nextcloud-talk`
- `bluebubbles`, `zalo`, `zalouser`, `nostr`, `feishu`

## Concepts

- `agentId` : un « cerveau » (espace de travail, auth par agent, magasin de sessions par agent).
- `accountId` : une instance de compte de canal (par exemple compte WhatsApp `"personal"` vs `"biz"`).
- `binding` : achemine les messages entrants vers un `agentId` par `(channel, accountId, peer)` et optionnellement les IDs de guild/équipe.
- Les chats directs s'effondrent à `agent:<agentId>:<mainKey>` (« main » par agent ; `session.mainKey`).

## Exemples de plateforme

### Bots Discord par agent

Chaque compte bot Discord correspond à un `accountId` unique. Liez chaque compte à un agent et maintenez des listes blanches par bot.

```json5
{
  agents: {
    list: [
      { id: "main", workspace: "~/.openclaw/workspace-main" },
      { id: "coding", workspace: "~/.openclaw/workspace-coding" },
    ],
  },
  bindings: [
    { agentId: "main", match: { channel: "discord", accountId: "default" } },
    { agentId: "coding", match: { channel: "discord", accountId: "coding" } },
  ],
  channels: {
    discord: {
      groupPolicy: "allowlist",
      accounts: {
        default: {
          token: "DISCORD_BOT_TOKEN_MAIN",
          guilds: {
            "123456789012345678": {
              channels: {
                "222222222222222222": { allow: true, requireMention: false },
              },
            },
          },
        },
        coding: {
          token: "DISCORD_BOT_TOKEN_CODING",
          guilds: {
            "123456789012345678": {
              channels: {
                "333333333333333333": { allow: true, requireMention: false },
              },
            },
          },
        },
      },
    },
  },
}
```

Notes :

- Invitez chaque bot à la guild et activez Message Content Intent.
- Les tokens se trouvent dans `channels.discord.accounts.<id>.token` (le compte par défaut peut utiliser `DISCORD_BOT_TOKEN`).

### Bots Telegram par agent

```json5
{
  agents: {
    list: [
      { id: "main", workspace: "~/.openclaw/workspace-main" },
      { id: "alerts", workspace: "~/.openclaw/workspace-alerts" },
    ],
  },
  bindings: [
    { agentId: "main", match: { channel: "telegram", accountId: "default" } },
    { agentId: "alerts", match: { channel: "telegram", accountId: "alerts" } },
  ],
  channels: {
    telegram: {
      accounts: {
        default: {
          botToken: "123456:ABC...",
          dmPolicy: "pairing",
        },
        alerts: {
          botToken: "987654:XYZ...",
          dmPolicy: "allowlist",
          allowFrom: ["tg:123456789"],
        },
      },
    },
  },
}
```

Notes :

- Créez un bot par agent avec BotFather et copiez chaque token.
- Les tokens se trouvent dans `channels.telegram.accounts.<id>.botToken` (le compte par défaut peut utiliser `TELEGRAM_BOT_TOKEN`).

### Numéros WhatsApp par agent

Liez chaque compte avant de démarrer la gateway :

```bash
openclaw channels login --channel whatsapp --account personal
openclaw channels login --channel whatsapp --account biz
```

`~/.openclaw/openclaw.json` (JSON5) :

```js
{
  agents: {
    list: [
      {
        id: "home",
        default: true,
        name: "Home",
        workspace: "~/.openclaw/workspace-home",
        agentDir: "~/.openclaw/agents/home/agent",
      },
      {
        id: "work",
        name: "Work",
        workspace: "~/.openclaw/workspace-work",
        agentDir: "~/.openclaw/agents/work/agent",
      },
    ],
  },

  // Routage déterministe : la première correspondance gagne (la plus spécifique en premier).
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },

    // Remplacement optionnel par pair (exemple : envoyer un groupe spécifique à l'agent work).
    {
      agentId: "work",
      match: {
        channel: "whatsapp",
        accountId: "personal",
        peer: { kind: "group", id: "1203630...@g.us" },
      },
    },
  ],

  // Désactivé par défaut : la messagerie agent-à-agent doit être explicitement activée + autorisée.
  tools: {
    agentToAgent: {
      enabled: false,
      allow: ["home", "work"],
    },
  },

  channels: {
    whatsapp: {
      accounts: {
        personal: {
          // Remplacement optionnel. Par défaut : ~/.openclaw/credentials/whatsapp/personal
          // authDir: "~/.openclaw/credentials/whatsapp/personal",
        },
        biz: {
          // Remplacement optionnel. Par défaut : ~/.openclaw/credentials/whatsapp/biz
          // authDir: "~/.openclaw/credentials/whatsapp/biz",
        },
      },
    },
  },
}
```

## Exemple : chat WhatsApp quotidien + travail approfondi Telegram

Divisez par canal : acheminez WhatsApp vers un agent rapide quotidien et Telegram vers un agent Opus.

```json5
{
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "opus",
        name: "Deep Work",
        workspace: "~/.openclaw/workspace-opus",
        model: "anthropic/claude-opus-4-6",
      },
    ],
  },
  bindings: [
    { agentId: "chat", match: { channel: "whatsapp" } },
    { agentId: "opus", match: { channel: "telegram" } },
  ],
}
```

Notes :

- Si vous avez plusieurs comptes pour un canal, ajoutez `accountId` à la liaison (par exemple `{ channel: "whatsapp", accountId: "personal" }`).
- Pour acheminer un seul DM/groupe vers Opus tout en gardant le reste sur chat, ajoutez une liaison `match.peer` pour ce pair ; les correspondances de pair gagnent toujours sur les règles à l'échelle du canal.

## Exemple : même canal, un pair vers Opus

Gardez WhatsApp sur l'agent rapide, mais acheminez un DM vers Opus :

```json5
{
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "opus",
        name: "Deep Work",
        workspace: "~/.openclaw/workspace-opus",
        model: "anthropic/claude-opus-4-6",
      },
    ],
  },
  bindings: [
    {
      agentId: "opus",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551234567" } },
    },
    { agentId: "chat", match: { channel: "whatsapp" } },
  ],
}
```

Les liaisons de pair gagnent toujours, gardez-les donc au-dessus de la règle à l'échelle du canal.

## Agent familial lié à un groupe WhatsApp

Liez un agent familial dédié à un seul groupe WhatsApp, avec contrôle de mention
et une politique d'outils plus stricte :

```json5
{
  agents: {
    list: [
      {
        id: "family",
        name: "Family",
        workspace: "~/.openclaw/workspace-family",
        identity: { name: "Family Bot" },
        groupChat: {
          mentionPatterns: ["@family", "@familybot", "@Family Bot"],
        },
        sandbox: {
          mode: "all",
          scope: "agent",
        },
        tools: {
          allow: [
            "exec",
            "read",
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
          ],
          deny: ["write", "edit", "apply_patch", "browser", "canvas", "nodes", "cron"],
        },
      },
    ],
  },
  bindings: [
    {
      agentId: "family",
      match: {
        channel: "whatsapp",
        peer: { kind: "group", id: "120363999999999999@g.us" },
      },
    },
  ],
}
```

Notes :

- Les listes d'autorisation/refus d'outils sont des **outils**, pas des compétences. Si une compétence doit exécuter un binaire, assurez-vous que `exec` est autorisé et que le binaire existe dans le bac à sable.
- Pour un contrôle plus strict, définissez `agents.list[].groupChat.mentionPatterns` et gardez les listes d'autorisation de groupe activées pour le canal.

## Configuration du bac à sable et des outils par agent

À partir de v2026.1.6, chaque agent peut avoir ses propres restrictions de bac à sable et d'outils :

```js
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: {
          mode: "off",  // No sandbox for personal agent
        },
        // No tool restrictions - all tools available
      },
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",     // Always sandboxed
          scope: "agent",  // One container per agent
          docker: {
            // Optional one-time setup after container creation
            setupCommand: "apt-get update && apt-get install -y git curl",
          },
        },
        tools: {
          allow: ["read"],                    // Only read tool
          deny: ["exec", "write", "edit", "apply_patch"],    // Deny others
        },
      },
    ],
  },
}
```

Note : `setupCommand` se trouve sous `sandbox.docker` et s'exécute une fois à la création du conteneur.
Les remplacements `sandbox.docker.*` par agent sont ignorés lorsque la portée résolue est `"shared"`.

**Avantages :**

- **Isolation de sécurité** : Restreignez les outils pour les agents non fiables
- **Contrôle des ressources** : Bac à sable pour des agents spécifiques tout en gardant d'autres sur l'hôte
- **Politiques flexibles** : Permissions différentes par agent

Note : `tools.elevated` est **global** et basé sur l'expéditeur ; il n'est pas configurable par agent.
Si vous avez besoin de limites par agent, utilisez `agents.list[].tools` pour refuser `exec`.
Pour le ciblage de groupe, utilisez `agents.list[].groupChat.mentionPatterns` pour que les @mentions se mappent correctement à l'agent prévu.

Voir [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools) pour des exemples détaillés.
