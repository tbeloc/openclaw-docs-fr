---
summary: "Référence CLI pour `openclaw memory` (status/index/search)"
read_when:
  - Vous voulez indexer ou rechercher dans la mémoire sémantique
  - Vous déboguez la disponibilité ou l'indexation de la mémoire
title: "memory"
---

# `openclaw memory`

Gérez l'indexation et la recherche de mémoire sémantique.
Fourni par le plugin de mémoire actif (par défaut : `memory-core` ; définissez `plugins.slots.memory = "none"` pour désactiver).

Connexes :

- Concept de mémoire : [Memory](/fr/concepts/memory)
- Plugins : [Plugins](/fr/tools/plugin)

## Exemples

```bash
openclaw memory status
openclaw memory status --deep
openclaw memory index --force
openclaw memory search "meeting notes"
openclaw memory search --query "deployment" --max-results 20
openclaw memory status --json
openclaw memory status --deep --index
openclaw memory status --deep --index --verbose
openclaw memory status --agent main
openclaw memory index --agent main --verbose
```

## Options

`memory status` et `memory index` :

- `--agent <id>` : limiter à un seul agent. Sans cela, ces commandes s'exécutent pour chaque agent configuré ; si aucune liste d'agents n'est configurée, elles reviennent à l'agent par défaut.
- `--verbose` : émettre des journaux détaillés lors des sondes et de l'indexation.

`memory status` :

- `--deep` : sonder la disponibilité des vecteurs + embeddings.
- `--index` : exécuter une réindexation si le magasin est marqué comme modifié (implique `--deep`).
- `--json` : imprimer la sortie JSON.

`memory index` :

- `--force` : forcer une réindexation complète.

`memory search` :

- Entrée de requête : passer soit `[query]` en position, soit `--query <text>`.
- Si les deux sont fournis, `--query` a la priorité.
- Si aucun n'est fourni, la commande se termine avec une erreur.
- `--agent <id>` : limiter à un seul agent (par défaut : l'agent par défaut).
- `--max-results <n>` : limiter le nombre de résultats retournés.
- `--min-score <n>` : filtrer les correspondances avec un faible score.
- `--json` : imprimer les résultats JSON.

Remarques :

- `memory index --verbose` imprime les détails par phase (fournisseur, modèle, sources, activité par lot).
- `memory status` inclut tous les chemins supplémentaires configurés via `memorySearch.extraPaths`.
- Si les champs de clé API de mémoire active effectivement actifs sont configurés en tant que SecretRefs, la commande résout ces valeurs à partir de l'instantané de passerelle actif. Si la passerelle n'est pas disponible, la commande échoue rapidement.
- Remarque sur le décalage de version de passerelle : ce chemin de commande nécessite une passerelle qui supporte `secrets.resolve` ; les anciennes passerelles retournent une erreur de méthode inconnue.
