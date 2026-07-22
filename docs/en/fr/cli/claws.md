---
summary: "Valider, prévisualiser et ajouter des packages d'agent Claw expérimentaux"
read_when:
  - You want to validate a grouped Claw manifest
  - You want to preview or add one agent from a Claw
title: "Claws"
---

# `openclaw claws`

Un Claw est une configuration versionnée pour un nouvel agent OpenClaw. Il peut décrire la configuration de l'agent, les fichiers d'espace de travail, les compétences, les plugins, les serveurs MCP et les tâches cron dont cet agent a besoin. Un Claw ne remplace ni ne modifie un agent existant.

Les Claws sont expérimentaux. Leur schéma, la sortie des commandes et leur cycle de vie peuvent changer. Activez la surface de commande explicitement :

```bash
export OPENCLAW_EXPERIMENTAL_CLAWS=1
```

L'interface de ligne de commande actuelle lit un répertoire de package local ou un manifeste JSON groupé. La publication, la recherche et l'installation de Claws complets via ClawHub constituent une piste de registre distincte et ne font pas encore partie de cette surface de commande.

## Créer un manifeste groupé

Commencez par un manifeste JSON version 1 :

```json
{
  "schemaVersion": 1,
  "agent": {
    "id": "incident-triage",
    "name": "Incident triage",
    "tools": { "deny": ["exec"] }
  },
  "workspace": { "bootstrapFiles": {} },
  "packages": [],
  "mcpServers": {},
  "cronJobs": []
}
```

Les chemins des packages et de l'espace de travail doivent rester à l'intérieur de la racine du package. Les manifestes sont limités à 1 Mio, les métadonnées du package à 256 Kio, et les sources d'espace de travail appliquent des limites distinctes par fichier et agrégées. Les sources d'espace de travail rejettent également les parents avec liens symboliques.

Les fichiers d'espace de travail sont déclarés par chemin et lus à partir des sidecars de package. Les fichiers d'amorçage tels que `SOUL.md` utilisent des entrées nommées ; les fichiers supplémentaires utilisent des sources relatives au package et des cibles relatives à l'espace de travail :

```json
{
  "workspace": {
    "bootstrapFiles": {
      "SOUL.md": { "source": "workspace/SOUL.md" }
    },
    "files": [
      {
        "source": "workspace/reference/policy.md",
        "path": "reference/policy.md"
      }
    ]
  }
}
```

## Inspecter et prévisualiser

Validez la source sans planifier les modifications locales :

```bash
openclaw claws inspect ./incident-triage.claw.json
```

Prévisualisez toutes les actions de cycle de vie proposées :

```bash
openclaw claws add ./incident-triage.claw.json --dry-run --json
```

Le plan rapporte l'agent et l'espace de travail dérivés, chaque action proposée, les prérequis, les bloqueurs, les escalades de capacité distinctes et un digest `planIntegrity`. Les enregistrements de capacité montrent l'effet exact du package, MCP, travail planifié, sandbox, outil ou heartbeat. Examinez le plan avant de créer l'agent :

```bash
openclaw claws add ./incident-triage.claw.json \
  --yes \
  --plan-integrity <SHA256_FROM_DRY_RUN>
```

`--yes` seul est insuffisant. OpenClaw reconstruit le plan et rejette le consentement lorsque la source, la destination ou la configuration en direct a changé après la prévisualisation. Utilisez `--agent-id` ou `--workspace` lors de la prévisualisation et de l'application lorsque les valeurs par défaut du package entrent en collision avec l'état local.

L'ajout d'un Claw crée la nouvelle configuration d'agent et d'espace de travail, écrit les fichiers d'espace de travail déclarés et enregistre l'installation et la provenance par fichier. Les fichiers existants ne sont pas remplacés, et les tentatives échouent de manière fermée lorsque le contenu possédé a dérivé. Les étapes Claw ultérieures ajoutent d'autres ressources déclarées.

## Référence des commandes

| Commande                 | Objectif                                                    |
| ----------------------- | ----------------------------------------------------------- |
| `claws inspect <source>` | Valider un répertoire de package ou un manifeste JSON.      |
| `claws add <source>`     | Prévisualiser ou créer un nouvel agent et espace de travail. |

Utilisez `--json` pour une sortie expérimentale lisible par machine.

## Voir aussi

- [Agents](/fr/cli/agents)
- [Skills](/fr/tools/skills)
- [Plugins](/fr/tools/plugin)
