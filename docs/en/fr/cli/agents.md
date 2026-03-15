---
summary: "Référence CLI pour `openclaw agents` (list/add/delete/bindings/bind/unbind/set identity)"
read_when:
  - You want multiple isolated agents (workspaces + routing + auth)
title: "agents"
---

# `openclaw agents`

Gérer les agents isolés (workspaces + auth + routing).

Connexes :

- Routage multi-agent : [Multi-Agent Routing](/concepts/multi-agent)
- Workspace d'agent : [Agent workspace](/concepts/agent-workspace)

## Exemples

```bash
openclaw agents list
openclaw agents add work --workspace ~/.openclaw/workspace-work
openclaw agents bindings
openclaw agents bind --agent work --bind telegram:ops
openclaw agents unbind --agent work --bind telegram:ops
openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity
openclaw agents set-identity --agent main --avatar avatars/openclaw.png
openclaw agents delete work
```

## Liaisons de routage

Utilisez les liaisons de routage pour épingler le trafic des canaux entrants à un agent spécifique.

Lister les liaisons :

```bash
openclaw agents bindings
openclaw agents bindings --agent work
openclaw agents bindings --json
```

Ajouter des liaisons :

```bash
openclaw agents bind --agent work --bind telegram:ops --bind discord:guild-a
```

Si vous omettez `accountId` (`--bind <channel>`), OpenClaw le résout à partir des paramètres par défaut du canal et des hooks de configuration du plugin si disponibles.

### Comportement de la portée de liaison

- Une liaison sans `accountId` correspond uniquement au compte par défaut du canal.
- `accountId: "*"` est le fallback à l'échelle du canal (tous les comptes) et est moins spécifique qu'une liaison de compte explicite.
- Si le même agent a déjà une liaison de canal correspondante sans `accountId`, et que vous la liez ultérieurement avec un `accountId` explicite ou résolu, OpenClaw met à niveau cette liaison existante sur place au lieu d'ajouter un doublon.

Exemple :

```bash
# liaison initiale au niveau du canal uniquement
openclaw agents bind --agent work --bind telegram

# mise à niveau ultérieure vers une liaison au niveau du compte
openclaw agents bind --agent work --bind telegram:ops
```

Après la mise à niveau, le routage pour cette liaison est limité à `telegram:ops`. Si vous souhaitez également le routage du compte par défaut, ajoutez-le explicitement (par exemple `--bind telegram:default`).

Supprimer les liaisons :

```bash
openclaw agents unbind --agent work --bind telegram:ops
openclaw agents unbind --agent work --all
```

## Fichiers d'identité

Chaque workspace d'agent peut inclure un `IDENTITY.md` à la racine du workspace :

- Chemin d'exemple : `~/.openclaw/workspace/IDENTITY.md`
- `set-identity --from-identity` lit à partir de la racine du workspace (ou d'un `--identity-file` explicite)

Les chemins d'avatar sont résolus par rapport à la racine du workspace.

## Définir l'identité

`set-identity` écrit les champs dans `agents.list[].identity` :

- `name`
- `theme`
- `emoji`
- `avatar` (chemin relatif au workspace, URL http(s), ou data URI)

Charger à partir de `IDENTITY.md` :

```bash
openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity
```

Remplacer les champs explicitement :

```bash
openclaw agents set-identity --agent main --name "OpenClaw" --emoji "🦞" --avatar avatars/openclaw.png
```

Exemple de configuration :

```json5
{
  agents: {
    list: [
      {
        id: "main",
        identity: {
          name: "OpenClaw",
          theme: "space lobster",
          emoji: "🦞",
          avatar: "avatars/openclaw.png",
        },
      },
    ],
  },
}
```
