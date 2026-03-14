---
read_when:
  - Vous souhaitez indexer ou rechercher la mémoire sémantique
  - Vous déboguez des problèmes de disponibilité ou d'indexation de la mémoire
summary: "Référence CLI pour `openclaw memory`（status/index/search）"
title: memory
x-i18n:
  generated_at: "2026-02-01T20:21:11Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 95a9e94306f95be2218a909be59be5bbaa5d31322b71b23564c71a89c3a3941a
  source_path: cli/memory.md
  workflow: 14
---

# `openclaw memory`

Gérez l'indexation et la recherche de la mémoire sémantique.
Fourni par le plugin de mémoire actif (par défaut : `memory-core` ; définissez `plugins.slots.memory = "none"` pour désactiver).

Contenu connexe :

- Concepts de mémoire : [Mémoire](/concepts/memory)
- Plugins : [Plugins](/tools/plugin)

## Exemples

```bash
openclaw memory status
openclaw memory status --deep
openclaw memory status --deep --index
openclaw memory status --deep --index --verbose
openclaw memory index
openclaw memory index --verbose
openclaw memory search "release checklist"
openclaw memory status --agent main
openclaw memory index --agent main --verbose
```

## Options

Options générales :

- `--agent <id>` : Limiter à un seul agent (par défaut : tous les agents configurés).
- `--verbose` : Afficher les journaux détaillés pendant le sondage et l'indexation.

Remarques :

- `memory status --deep` sonde la disponibilité du magasin vectoriel et du modèle d'intégration.
- `memory status --deep --index` réexécute l'indexation lorsque le magasin contient des modifications non synchronisées.
- `memory index --verbose` affiche les détails de chaque étape (fournisseur, modèle, sources de données, activité de traitement par lots).
- `memory status` inclut tous les chemins supplémentaires configurés via `memorySearch.extraPaths`.
