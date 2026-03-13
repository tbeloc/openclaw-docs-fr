---
read_when:
  - Vous avez besoin de plusieurs agents isolés (espace de travail + routage + authentification)
summary: "Référence CLI pour `openclaw agents` (lister/ajouter/supprimer/définir l'identité)"
title: agents
x-i18n:
  generated_at: "2026-02-01T19:58:38Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 30556d81636a9ad8972573cc6b498e620fd266e1dfb16eef3f61096ea62f9896
  source_path: cli/agents.md
  workflow: 14
---

# `openclaw agents`

Gérez les agents isolés (espace de travail + authentification + routage).

Contenu connexe :

- Routage multi-agents : [Routage multi-agents](/concepts/multi-agent)
- Espace de travail des agents : [Espace de travail des agents](/concepts/agent-workspace)

## Exemples

```bash
openclaw agents list
openclaw agents add work --workspace ~/.openclaw/workspace-work
openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity
openclaw agents set-identity --agent main --avatar avatars/openclaw.png
openclaw agents delete work
```

## Fichiers d'identité

Chaque espace de travail d'agent peut contenir un fichier `IDENTITY.md` à la racine de l'espace de travail :

- Chemin d'exemple : `~/.openclaw/workspace/IDENTITY.md`
- `set-identity --from-identity` lit depuis la racine de l'espace de travail (ou depuis un `--identity-file` explicitement spécifié)

Les chemins d'avatar sont résolus relativement à la racine de l'espace de travail.

## Définir l'identité

`set-identity` écrit les champs dans `agents.list[].identity` :

- `name`
- `theme`
- `emoji`
- `avatar` (chemin relatif à l'espace de travail, URL http(s) ou URI de données)

Charger depuis `IDENTITY.md` :

```bash
openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity
```

Remplacer explicitement les champs :

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
