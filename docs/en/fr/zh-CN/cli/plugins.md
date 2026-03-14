---
read_when:
  - Vous souhaitez installer ou gérer des plugins Gateway en processus
  - Vous souhaitez déboguer les problèmes de chargement de plugins
summary: "Référence CLI pour `openclaw plugins` (lister, installer, activer/désactiver, diagnostiquer)"
title: plugins
x-i18n:
  generated_at: "2026-02-03T07:45:08Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: c6bf76b1e766b912ec30a0101d455151c88f1a778bffa121cdd1d0b4fbe73e1c
  source_path: cli/plugins.md
  workflow: 15
---

# `openclaw plugins`

Gérez les plugins/extensions Gateway (chargement en processus).

Contenu connexe :

- Système de plugins : [Plugins](/tools/plugin)
- Manifeste de plugins + schéma : [Manifeste de plugins](/plugins/manifest)
- Durcissement de la sécurité : [Sécurité](/gateway/security)

## Commandes

```bash
openclaw plugins list
openclaw plugins info <id>
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins doctor
openclaw plugins update <id>
openclaw plugins update --all
```

Les plugins intégrés sont distribués avec OpenClaw, mais désactivés par défaut. Utilisez `plugins enable` pour les activer.

Tous les plugins doivent fournir un fichier `openclaw.plugin.json` contenant un JSON Schema en ligne (`configSchema`, même s'il est vide). Un manifeste manquant ou invalide ou un schéma invalide empêchera le chargement du plugin et entraînera l'échec de la validation de la configuration.

### Installation

```bash
openclaw plugins install <path-or-spec>
```

Conseil de sécurité : Traitez l'installation de plugins comme l'exécution de code. Privilégiez les versions fixes.

Formats d'archive supportés : `.zip`, `.tgz`, `.tar.gz`, `.tar`.

Utilisez `--link` pour éviter de copier les répertoires locaux (ajoutés à `plugins.load.paths`) :

```bash
openclaw plugins install -l ./my-plugin
```

### Mise à jour

```bash
openclaw plugins update <id>
openclaw plugins update --all
openclaw plugins update <id> --dry-run
```

Les mises à jour s'appliquent uniquement aux plugins installés à partir de npm (suivis dans `plugins.installs`).
