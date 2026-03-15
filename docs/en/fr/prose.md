---
summary: "OpenProse: workflows .prose, commandes slash et état dans OpenClaw"
read_when:
  - You want to run or write .prose workflows
  - You want to enable the OpenProse plugin
  - You need to understand state storage
title: "OpenProse"
---

# OpenProse

OpenProse est un format de workflow portable et orienté markdown pour orchestrer des sessions IA. Dans OpenClaw, il est fourni en tant que plugin qui installe un pack de compétences OpenProse plus une commande slash `/prose`. Les programmes vivent dans des fichiers `.prose` et peuvent générer plusieurs sous-agents avec un contrôle de flux explicite.

Site officiel : [https://www.prose.md](https://www.prose.md)

## Ce qu'il peut faire

- Recherche multi-agents + synthèse avec parallélisme explicite.
- Workflows reproductibles et sûrs pour approbation (révision de code, triage d'incidents, pipelines de contenu).
- Programmes `.prose` réutilisables que vous pouvez exécuter sur les runtimes d'agents supportés.

## Installation et activation

Les plugins fournis sont désactivés par défaut. Activez OpenProse :

```bash
openclaw plugins enable open-prose
```

Redémarrez la Gateway après activation du plugin.

Développement/checkout local : `openclaw plugins install ./extensions/open-prose`

Documentation associée : [Plugins](/tools/plugin), [Manifeste de plugin](/plugins/manifest), [Compétences](/tools/skills).

## Commande slash

OpenProse enregistre `/prose` comme commande de compétence invocable par l'utilisateur. Elle achemine vers les instructions de la VM OpenProse et utilise les outils OpenClaw en arrière-plan.

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

## Exemple : un fichier `.prose` simple

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

OpenProse conserve l'état sous `.prose/` dans votre espace de travail :

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

## Modes d'état

OpenProse supporte plusieurs backends d'état :

- **filesystem** (par défaut) : `.prose/runs/...`
- **in-context** : transitoire, pour les petits programmes
- **sqlite** (expérimental) : nécessite le binaire `sqlite3`
- **postgres** (expérimental) : nécessite `psql` et une chaîne de connexion

Notes :

- sqlite/postgres sont optionnels et expérimentaux.
- Les identifiants postgres s'écoulent dans les journaux des sous-agents ; utilisez une base de données dédiée avec les privilèges minimaux.

## Programmes distants

`/prose run <handle/slug>` se résout en `https://p.prose.md/<handle>/<slug>`.
Les URL directes sont récupérées telles quelles. Cela utilise l'outil `web_fetch` (ou `exec` pour POST).

## Mappage du runtime OpenClaw

Les programmes OpenProse se mappent aux primitives OpenClaw :

| Concept OpenProse         | Outil OpenClaw   |
| ------------------------- | ---------------- |
| Spawn session / Task tool | `sessions_spawn` |
| Lecture/écriture de fichier | `read` / `write` |
| Web fetch                 | `web_fetch`      |

Si votre liste d'autorisation d'outils bloque ces outils, les programmes OpenProse échoueront. Voir [Configuration des compétences](/tools/skills-config).

## Sécurité et approbations

Traitez les fichiers `.prose` comme du code. Examinez-les avant d'exécuter. Utilisez les listes d'autorisation d'outils OpenClaw et les portes d'approbation pour contrôler les effets secondaires.

Pour les workflows déterministes et contrôlés par approbation, comparez avec [Lobster](/tools/lobster).
