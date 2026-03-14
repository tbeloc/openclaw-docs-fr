---
read_when: Vous voulez plusieurs agents isolés (espaces de travail + auth) dans un processus gateway unique.
status: active
summary: Routage multi-agents : agents isolés, comptes de canal et liaisons
title: Routage multi-agents
x-i18n:
  generated_at: "2026-02-03T07:47:38Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 1848266c632cd6c96ff99ea9eb9c17bbfe6d35fa1f90450853083e7c548d5324
  source_path: concepts/multi-agent.md
  workflow: 15
---

# Routage multi-agents

Objectif : plusieurs agents *isolés* (espaces de travail indépendants + `agentDir` + sessions), plus plusieurs comptes de canal (par exemple deux WhatsApp) dans un Gateway en cours d'exécution. Les messages entrants sont routés vers les agents via des liaisons.

## Qu'est-ce qu'un « agent » ?

Un **agent** est un cerveau complètement isolé avec son propre :

- **Espace de travail** (fichiers, AGENTS.md/SOUL.md/USER.md, notes locales, règles de personnalité).
- **Répertoire d'état** (`agentDir`) pour les fichiers de configuration d'authentification, le registre des modèles et la configuration par agent.
- **Stockage de session** (historique de chat + état de routage) situé sous `~/.openclaw/agents/<agentId>/sessions`.

Les fichiers de configuration d'authentification sont **isolés par agent**. Chaque agent lit depuis sa propre localisation :

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

Les identifiants de l'agent principal **ne sont pas** partagés automatiquement. Ne réutilisez jamais `agentDir` entre agents (cela provoque des conflits d'authentification/session). Si vous souhaitez partager des identifiants, copiez `auth-profiles.json` vers le `agentDir` d'un autre agent.

Les Skills sont isolés par agent via le dossier `skills/` de chaque espace de travail ; les Skills partagés peuvent être récupérés depuis `~/.openclaw/skills`. Voir [Skills : par agent vs partagés](/tools/skills#per-agent-vs-shared-skills).

Le Gateway peut héberger **un agent** (par défaut) ou **plusieurs agents** en parallèle.

**Remarque sur l'espace de travail :** L'espace de travail de chaque agent est le **cwd par défaut**, pas un bac à sable strict. Les chemins relatifs sont résolus dans l'espace de travail, mais les chemins absolus peuvent accéder à d'autres emplacements sur l'hôte, sauf si l'isolation du bac à sable est activée. Voir [Isolation du bac à sable](/gateway/sandboxing).

## Chemins (mappage rapide)

- Configuration : `~/.openclaw/openclaw.json` (ou `OPENCLAW_CONFIG_PATH`)
- Répertoire d'état : `~/.openclaw` (ou `OPENCLAW_STATE_DIR`)
- Espace de travail : `~/.openclaw/workspace` (ou `~/.openclaw/workspace-<agentId>`)
- Répertoire agent : `~/.openclaw/agents/<agentId>/agent` (ou `agents.list[].agentDir`)
- Sessions : `~/.openclaw/agents/<agentId>/sessions`

### Mode agent unique (par défaut)

Si vous ne faites rien, OpenClaw exécute un agent unique :

- `agentId` par défaut est **`main`**.
- La clé de session est `agent:main:<mainKey>`.
- L'espace de travail par défaut est `~/.openclaw/workspace` (ou `~/.openclaw/workspace-<profile>` quand `OPENCLAW_PROFILE` est défini).
- L'état par défaut est `~/.openclaw/agents/main/agent`.

## Assistant agents

Utilisez l'assistant agents pour ajouter un nouvel agent isolé :

```bash
openclaw agents add work
```

Puis ajoutez des `bindings` (ou laissez l'assistant terminer) pour router les messages entrants.

Vérifiez :

```bash
openclaw agents list --bindings
```

## Plusieurs agents = plusieurs personnes, plusieurs personnalités

Avec **plusieurs agents**, chaque `agentId` devient une **personnalité complètement isolée** :

- **Numéros de téléphone/comptes différents** (par `accountId` de canal).
- **Personnalités différentes** (fichiers d'espace de travail par agent comme `AGENTS.md` et `SOUL.md`).
- **Authentification + sessions indépendantes** (pas de communication croisée sauf si explicitement activée).

Cela permet à **plusieurs personnes** de partager un serveur Gateway tout en gardant leurs « cerveaux » IA et données isolés.

## Un numéro WhatsApp, plusieurs personnes (division des messages privés)

Vous pouvez router **différents messages privés WhatsApp** vers différents agents tout en maintenant **un compte WhatsApp**. Utilisez `peer.kind: "dm"` pour correspondre à l'E.164 de l'expéditeur (par exemple `+15551234567`). Les réponses proviennent toujours du même numéro WhatsApp (pas d'identité d'expéditeur par agent).

Détail important : les chats directs s'effondrent dans la **clé de session principale** de l'agent, donc une véritable isolation nécessite **un agent par personne**.

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
    { agentId: "alex", match: { channel: "whatsapp", peer: { kind: "dm", id: "+15551230001" } } },
    { agentId: "mia", match: { channel: "whatsapp", peer: { kind: "dm", id: "+15551230002" } } },
  ],
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551230001", "+15551230002"],
    },
  },
}
```

Remarques :

- Le contrôle d'accès aux messages privés est **global par compte WhatsApp** (liste d'appairage/autorisation), pas par agent.
- Pour les groupes partagés, liez le groupe à un agent ou utilisez [groupes de diffusion](/channels/broadcast-groups).

## Règles de routage (comment les messages choisissent un agent)

Les liaisons sont **déterministes**, **le plus spécifique en premier** :

1. Correspondance `peer` (id exact de message privé/groupe/canal)
2. `guildId` (Discord)
3. `teamId` (Slack)
4. Correspondance `accountId` du canal
5. Correspondance au niveau du canal (`accountId: "*"`)
6. Retour à l'agent par défaut (`agents.list[].default`, sinon première entrée de la liste, par défaut : `main`)

## Plusieurs comptes/numéros de téléphone

Les canaux supportant **plusieurs comptes** (comme WhatsApp) utilisent `accountId` pour identifier chaque connexion. Chaque `accountId` peut être routé vers différents agents, donc un serveur peut héberger plusieurs numéros de téléphone sans mélanger les sessions.

## Concepts

- `agentId` : un « cerveau » (espace de travail, authentification par agent, stockage de session par agent).
- `accountId` : une instance de compte de canal (par exemple compte WhatsApp `"personal"` vs `"biz"`).
- `binding` : route les messages entrants vers `agentId` via `(channel, accountId, peer)` et optionnellement guild/team id.
- Les chats directs s'effondrent dans `agent:<agentId>:<mainKey>` (« principal » par agent ; `session.mainKey`).

## Exemple : deux WhatsApp → deux agents

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

  // Routage déterministe : la première correspondance gagne (le plus spécifique en premier).
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },

    // Surcharges optionnelles par pair (exemple : envoyer un groupe spécifique à l'agent work).
    {
      agentId: "work",
      match: {
        channel: "whatsapp",
        accountId: "personal",
        peer: { kind: "group", id: "1203630...@g.us" },
      },
    },
  ],

  // Désactivé par défaut : les messages agent-à-agent doivent être explicitement activés + mis en liste blanche.
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
          // Surcharge optionnelle. Par défaut : ~/.openclaw/credentials/whatsapp/personal
          // authDir: "~/.openclaw/credentials/whatsapp/personal",
        },
        biz: {
          // Surcharge optionnelle. Par défaut : ~/.openclaw/credentials/whatsapp/biz
          // authDir: "~/.openclaw/credentials/whatsapp/biz",
        },
      },
    },
  },
}
```

## Exemple : chat quotidien WhatsApp + travail approfondi Telegram

Divisez par canal : routez WhatsApp vers un agent quotidien rapide, Telegram vers un agent Opus.

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
        model: "anthropic/claude-opus-4-5",
      },
    ],
  },
  bindings: [
    { agentId: "chat", match: { channel: "whatsapp" } },
    { agentId: "opus", match: { channel: "telegram" } },
  ],
}
```

Remarques :

- Si vous avez plusieurs comptes pour un canal, ajoutez `accountId` dans la liaison (par exemple `{ channel: "whatsapp", accountId: "personal" }`).
- Pour router un message privé/groupe unique vers Opus tout en gardant le reste sur chat, ajoutez une liaison `match.peer` pour ce pair ; la correspondance de pair a toujours priorité sur les règles au niveau du canal.

## Exemple : même canal, un pair vers Opus

Gardez WhatsApp sur l'agent rapide, mais routez un message privé vers Opus :

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
        model: "anthropic/claude-opus-4-5",
      },
    ],
  },
  bindings: [
    { agentId: "opus", match: { channel: "whatsapp", peer: { kind: "dm", id: "+15551234567" } } },
    { agentId: "chat", match: { channel: "whatsapp" } },
  ],
}
```

Les liaisons de pair gagnent toujours, donc placez-les au-dessus des règles au niveau du canal.

## Lier un agent familial à un groupe WhatsApp

Liez un agent familial dédié à un groupe WhatsApp unique, avec des restrictions de mention et une politique d'outils plus stricte :

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

Remarques :

- Les listes d'autorisation/refus d'outils sont des **outils**, pas des Skills. Si un skill doit exécuter un binaire, assurez-vous que `exec` est autorisé et que le binaire existe dans le bac à sable.
- Pour des restrictions plus strictes, définissez `agents.list[].groupChat.mentionPatterns` et maintenez la liste blanche des groupes activée pour le canal.

## Configuration du bac à sable et des outils par agent

À partir de v2026.1.6, chaque agent peut avoir son propre bac à sable et ses propres restrictions d'outils :

```js
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: {
          mode: "off",  // Agent personnel sans bac à sable
        },
        // Pas de restriction d'outils - tous les outils disponibles
      },
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",     // Toujours en bac à sable
          scope: "agent",  // Un conteneur par agent
          docker: {
            // Configuration optionnelle unique après création du conteneur
            setupCommand: "apt-get update && apt-get install -y git curl",
          },
        },
        tools: {
          allow: ["read"],                    // Seulement l'outil read
          deny: ["exec", "write", "edit", "apply_patch
