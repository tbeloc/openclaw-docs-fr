---
read_when:
  - 你想运行或编写 .prose 工作流
  - 你想启用 OpenProse 插件
  - 你需要了解状态存储
summary: OpenProse：OpenClaw 中的 .prose 工作流、斜杠命令和状态
title: OpenProse
x-i18n:
  generated_at: "2026-02-03T07:53:38Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: cf7301e927b9a46347b498e264aeaa10dd76e85ff2de04775be57435718339f5
  source_path: prose.md
  workflow: 15
---

# OpenProse

OpenProse est un format de flux de travail portable et centré sur Markdown pour orchestrer des sessions d'IA. Dans OpenClaw, il est distribué en tant que plugin, installant un package OpenProse Skills ainsi qu'une commande slash `/prose`. Les programmes sont stockés dans des fichiers `.prose` et peuvent générer plusieurs sous-agents avec un contrôle de flux explicite.

Site officiel : https://www.prose.md

## Ce qu'il peut faire

- Recherche multi-agents + synthèse avec parallélisme explicite.
- Flux de travail d'approbation reproductibles et sécurisés (révision de code, classification d'événements, pipeline de contenu).
- Programmes `.prose` réutilisables exécutables entre les runtimes d'agents supportés.

## Installation + activation

Les plugins fournis sont désactivés par défaut. Activez OpenProse :

```bash
openclaw plugins enable open-prose
```

Redémarrez la passerelle après activation du plugin.

Développement/extraction locale : `openclaw plugins install ./extensions/open-prose`

Documentation connexe : [Plugins](/tools/plugin), [Manifeste de plugin](/plugins/manifest), [Skills](/tools/skills).

## Commandes slash

OpenProse enregistre `/prose` comme commande Skills invocable par l'utilisateur. Elle route vers les instructions de la VM OpenProse et utilise les outils OpenClaw en arrière-plan.

Commandes courantes :

```
/prose help
/prose run <file.prose>
/prose run <handle/slug>
/prose run <https://example.com/file.prose>
/prose compile <file.prose>
/prose examples
/prose update
```

## Exemple : un simple fichier `.prose`

```prose
# Research + synthesis with two agents running in parallel.

input topic: "What should we research?"

agent researcher:
  model: sonnet
  prompt: "You research thoroughly and cite sources."

agent writer:
  model: opus
  prompt: "You write a concise summary."

parallel:
  findings = session: researcher
    prompt: "Research {topic}."
  draft = session: writer
    prompt: "Summarize {topic}."

session "Merge the findings + draft into a final answer."
context: { findings, draft }
```

## Emplacements des fichiers

OpenProse sauvegarde l'état sous `.prose/` dans l'espace de travail :

```
.prose/
├── .env
├── runs/
│   └── {YYYYMMDD}-{HHMMSS}-{random}/
│       ├── program.prose
│       ├── state.md
│       ├── bindings/
│       └── agents/
└── agents/
```

Les agents persistants au niveau utilisateur se trouvent à :

```
~/.prose/agents/
```

## Schéma d'état

OpenProse supporte plusieurs backends d'état :

- **filesystem** (par défaut) : `.prose/runs/...`
- **in-context** : transitoire, pour les petits programmes
- **sqlite** (expérimental) : nécessite le binaire `sqlite3`
- **postgres** (expérimental) : nécessite `psql` et une chaîne de connexion

Remarques :

- sqlite/postgres sont opt-in et en phase expérimentale.
- Les identifiants postgres s'écoulent dans les journaux des sous-agents ; utilisez une base de données dédiée avec des privilèges minimaux.

## Programmes distants

`/prose run <handle/slug>` se résout en `https://p.prose.md/<handle>/<slug>`.
Les URL directes sont récupérées telles quelles. Cela utilise l'outil `web_fetch` (ou `exec` pour POST).

## Mappage du runtime OpenClaw

Les programmes OpenProse mappent aux primitives OpenClaw :

| Concept OpenProse    | Outil OpenClaw   |
| -------------------- | ---------------- |
| Générer session / Task | `sessions_spawn` |
| Lecture/écriture de fichiers | `read` / `write` |
| Récupération web     | `web_fetch`      |

Si votre liste blanche d'outils bloque ces outils, les programmes OpenProse échoueront. Voir [Configuration Skills](/tools/skills-config).

## Sécurité + approbation

Traitez les fichiers `.prose` comme du code. Examinez-les avant exécution. Utilisez la liste blanche d'outils OpenClaw et le contrôle d'approbation pour contrôler les effets secondaires.

Pour les flux de travail déterministes et contrôlés par approbation, comparez avec [Lobster](/tools/lobster).
