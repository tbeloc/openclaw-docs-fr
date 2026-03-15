---
summary: "Règles de routage par canal (WhatsApp, Telegram, Discord, Slack) et contexte partagé"
read_when:
  - Changing channel routing or inbox behavior
title: "Channel Routing"
---

# Canaux et routage

OpenClaw achemine les réponses **vers le canal d'où provient le message**. Le
modèle ne choisit pas de canal ; le routage est déterministe et contrôlé par la
configuration de l'hôte.

## Termes clés

- **Canal** : `whatsapp`, `telegram`, `discord`, `slack`, `signal`, `imessage`, `webchat`.
- **AccountId** : instance de compte par canal (si supportée).
- Compte par défaut optionnel du canal : `channels.<channel>.defaultAccount` choisit
quel compte est utilisé quand un chemin sortant ne spécifie pas `accountId`.
  - Dans les configurations multi-comptes, définissez un défaut explicite (`defaultAccount` ou `accounts.default`) quand deux comptes ou plus sont configurés. Sans cela, le routage de secours peut choisir le premier ID de compte normalisé.
- **AgentId** : un espace de travail isolé + magasin de sessions ("cerveau").
- **SessionKey** : la clé de bucket utilisée pour stocker le contexte et contrôler la concurrence.

## Formes de clés de session (exemples)

Les messages directs se réduisent à la session **principale** de l'agent :

- `agent:<agentId>:<mainKey>` (par défaut : `agent:main:main`)

Les groupes et canaux restent isolés par canal :

- Groupes : `agent:<agentId>:<channel>:group:<id>`
- Canaux/salons : `agent:<agentId>:<channel>:channel:<id>`

Fils de discussion :

- Les fils Slack/Discord ajoutent `:thread:<threadId>` à la clé de base.
- Les sujets de forum Telegram intègrent `:topic:<topicId>` dans la clé de groupe.

Exemples :

- `agent:main:telegram:group:-1001234567890:topic:42`
- `agent:main:discord:channel:123456:thread:987654`

## Épinglage de route DM principal

Quand `session.dmScope` est `main`, les messages directs peuvent partager une session principale.
Pour empêcher que `lastRoute` de la session soit écrasé par des DM de non-propriétaires,
OpenClaw déduit un propriétaire épinglé de `allowFrom` quand tous ces éléments sont vrais :

- `allowFrom` a exactement une entrée non-joker.
- L'entrée peut être normalisée en un ID d'expéditeur concret pour ce canal.
- L'expéditeur du DM entrant ne correspond pas à ce propriétaire épinglé.

Dans ce cas de non-correspondance, OpenClaw enregistre toujours les métadonnées de session entrantes, mais
il ignore la mise à jour de `lastRoute` de la session principale.

## Règles de routage (comment un agent est choisi)

Le routage choisit **un agent** pour chaque message entrant :

1. **Correspondance exacte de pair** (`bindings` avec `peer.kind` + `peer.id`).
2. **Correspondance de pair parent** (héritage de fil).
3. **Correspondance de guilde + rôles** (Discord) via `guildId` + `roles`.
4. **Correspondance de guilde** (Discord) via `guildId`.
5. **Correspondance d'équipe** (Slack) via `teamId`.
6. **Correspondance de compte** (`accountId` sur le canal).
7. **Correspondance de canal** (tout compte sur ce canal, `accountId: "*"`).
8. **Agent par défaut** (`agents.list[].default`, sinon première entrée de liste, secours vers `main`).

Quand une liaison inclut plusieurs champs de correspondance (`peer`, `guildId`, `teamId`, `roles`), **tous les champs fournis doivent correspondre** pour que cette liaison s'applique.

L'agent correspondant détermine quel espace de travail et magasin de sessions sont utilisés.

## Groupes de diffusion (exécuter plusieurs agents)

Les groupes de diffusion vous permettent d'exécuter **plusieurs agents** pour le même pair **quand OpenClaw répondrait normalement** (par exemple : dans les groupes WhatsApp, après un filtrage de mention/activation).

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

Voir : [Broadcast Groups](/channels/broadcast-groups).

## Aperçu de la configuration

- `agents.list` : définitions d'agents nommés (espace de travail, modèle, etc.).
- `bindings` : mappe les canaux/comptes/pairs entrants aux agents.

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

Les magasins de sessions se trouvent sous le répertoire d'état (par défaut `~/.openclaw`) :

- `~/.openclaw/agents/<agentId>/sessions/sessions.json`
- Les transcriptions JSONL se trouvent à côté du magasin

Vous pouvez remplacer le chemin du magasin via `session.store` et le modèle `{agentId}`.

La découverte de session de la passerelle et de l'ACP analyse également les magasins d'agents sauvegardés sur disque sous la
racine `agents/` par défaut et sous les racines `session.store` modélisées. Les magasins découverts
doivent rester à l'intérieur de cette racine d'agent résolue et utiliser un fichier
`sessions.json` régulier. Les liens symboliques et les chemins hors racine sont ignorés.

## Comportement de WebChat

WebChat s'attache à l'**agent sélectionné** et utilise par défaut la session principale de l'agent.
De ce fait, WebChat vous permet de voir le contexte multi-canal pour cet
agent en un seul endroit.

## Contexte de réponse

Les réponses entrantes incluent :

- `ReplyToId`, `ReplyToBody`, et `ReplyToSender` quand disponibles.
- Le contexte cité est ajouté à `Body` sous forme de bloc `[Replying to ...]`.

C'est cohérent sur tous les canaux.
