---
read_when:
  - 更改渠道路由或收件箱行为
summary: 每个渠道（WhatsApp、Telegram、Discord、Slack）的路由规则及共享上下文
title: 渠道路由
x-i18n:
  generated_at: "2026-02-01T20:22:21Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 1a322b5187e32c82fc1e8aac02437e2eeb7ba84e7b3a1db89feeab1dcf7dbbab
  source_path: channels/channel-routing.md
  workflow: 14
---

# Canaux et routage

OpenClaw achemine les réponses **vers le canal source du message**. Le modèle ne choisit pas le canal ; le routage est déterministe et contrôlé par la configuration de l'hôte.

## Termes clés

- **Canal** : `whatsapp`, `telegram`, `discord`, `slack`, `signal`, `imessage`, `webchat`.
- **AccountId** : Instance de compte pour chaque canal (le cas échéant).
- **AgentId** : Espace de travail isolé + stockage de session (« cerveau »).
- **SessionKey** : Clé de compartiment pour stocker le contexte et contrôler la concurrence.

## Formats de clé de session (exemples)

Les messages privés sont regroupés dans la session **principale** de l'agent :

- `agent:<agentId>:<mainKey>` (par défaut : `agent:main:main`)

Les groupes et canaux sont isolés par canal :

- Groupes : `agent:<agentId>:<channel>:group:<id>`
- Canaux/salons : `agent:<agentId>:<channel>:channel:<id>`

Fils de discussion :

- Les fils Slack/Discord sont ajoutés après la clé de base avec `:thread:<threadId>`.
- Les sujets de forum Telegram sont intégrés dans la clé de groupe avec `:topic:<topicId>`.

Exemples :

- `agent:main:telegram:group:-1001234567890:topic:42`
- `agent:main:discord:channel:123456:thread:987654`

## Règles de routage (comment sélectionner un agent)

Le routage sélectionne **un agent** pour chaque message entrant :

1. **Correspondance exacte du pair** (`peer.kind` + `peer.id` dans `bindings`).
2. **Correspondance Guild** (Discord) via `guildId`.
3. **Correspondance Team** (Slack) via `teamId`.
4. **Correspondance de compte** (`accountId` sur le canal).
5. **Correspondance de canal** (tout compte sur ce canal).
6. **Agent par défaut** (`agents.list[].default`, sinon le premier élément de la liste, par défaut `main`).

L'agent correspondant détermine quel espace de travail et quel stockage de session utiliser.

## Groupes de diffusion (exécuter plusieurs agents)

Les groupes de diffusion vous permettent d'exécuter **plusieurs agents** pour le même pair, **déclenchés lors d'une réponse normale d'OpenClaw** (par exemple : dans un groupe WhatsApp, après une mention/activation de porte).

Configuration :

```json5
{
  broadcast: {
    strategy: "parallel",
    "120363403215116621@g.us": ["alfred", "baerbel"],
    "+15555550123": ["support", "logger"],
  },
}
```

Voir : [Groupes de diffusion](/channels/broadcast-groups).

## Aperçu de la configuration

- `agents.list` : Définitions d'agents nommés (espace de travail, modèle, etc.).
- `bindings` : Mappe les canaux/comptes/pairs entrants aux agents.

Exemple :

```json5
{
  agents: {
    list: [{ id: "support", name: "Support", workspace: "~/.openclaw/workspace-support" }],
  },
  bindings: [
    { match: { channel: "slack", teamId: "T123" }, agentId: "support" },
    { match: { channel: "telegram", peer: { kind: "group", id: "-100123" } }, agentId: "support" },
  ],
}
```

## Stockage de session

Le stockage de session se trouve dans le répertoire d'état (par défaut `~/.openclaw`) :

- `~/.openclaw/agents/<agentId>/sessions/sessions.json`
- Les fichiers journaux JSONL se trouvent dans le même répertoire que le stockage

Vous pouvez remplacer le chemin de stockage via `session.store` et le modèle `{agentId}`.

## Comportement de WebChat

WebChat se connecte à **l'agent sélectionné** et utilise par défaut la session principale de cet agent. Ainsi, WebChat vous permet de voir le contexte multi-canal de cet agent en un seul endroit.

## Contexte de réponse

Les réponses entrantes contiennent :

- `ReplyToId`, `ReplyToBody` et `ReplyToSender` (le cas échéant).
- Le contexte référencé est ajouté au `Body` sous la forme d'un bloc `[Replying to ...]`.

Ceci reste cohérent sur tous les canaux.
