---
title: "Rêver (expérimental)"
summary: "Promotion en arrière-plan de la mémoire à court terme vers la mémoire à long terme"
read_when:
  - You want memory promotion to run automatically
  - You want to understand dreaming modes and thresholds
  - You want to tune consolidation without polluting MEMORY.md
---

# Rêver (expérimental)

Rêver est le passage de consolidation de mémoire en arrière-plan dans `memory-core`.

On l'appelle « rêver » parce que le système revisite ce qui s'est passé pendant la journée
et décide ce qui vaut la peine de conserver comme contexte durable.

Rêver est **expérimental**, **optionnel**, et **désactivé par défaut**.

## Ce que fait rêver

1. Suit les événements de rappel à court terme à partir des résultats de `memory_search` dans
   `memory/YYYY-MM-DD.md`.
2. Évalue les candidats de rappel avec des signaux pondérés.
3. Promeut uniquement les candidats qualifiés dans `MEMORY.md`.

Cela maintient la mémoire à long terme concentrée sur le contexte durable et répété au lieu de
détails ponctuels.

## Signaux de promotion

Rêver combine quatre signaux :

- **Fréquence** : à quelle fréquence le même candidat a été rappelé.
- **Pertinence** : à quel point les scores de rappel étaient forts lors de sa récupération.
- **Diversité des requêtes** : combien d'intentions de requête distinctes l'ont surfacé.
- **Récence** : pondération temporelle sur les rappels récents.

La promotion nécessite que toutes les portes de seuil configurées passent, pas seulement un signal.

### Poids des signaux

| Signal    | Poids | Description                                      |
| --------- | ----- | ------------------------------------------------ |
| Fréquence | 0.35  | À quelle fréquence la même entrée a été rappelée |
| Pertinence | 0.35  | Scores de rappel moyens lors de la récupération  |
| Diversité | 0.15  | Nombre d'intentions de requête distinctes qui l'ont surfacé |
| Récence   | 0.15  | Décroissance temporelle (demi-vie de 14 jours)   |

## Comment ça marche

1. **Suivi du rappel** -- Chaque résultat de `memory_search` est enregistré dans
   `memory/.dreams/short-term-recall.json` avec le nombre de rappels, les scores et le hash de requête.
2. **Notation planifiée** -- Selon le calendrier configuré, les candidats sont classés
   en utilisant des signaux pondérés. Toutes les portes de seuil doivent passer simultanément.
3. **Promotion** -- Les entrées qualifiantes sont ajoutées à `MEMORY.md` avec un
   timestamp de promotion.
4. **Nettoyage** -- Les entrées déjà promues sont filtrées des cycles futurs. Un
   verrou de fichier empêche les exécutions concurrentes.

## Modes

`dreaming.mode` contrôle le calendrier et les seuils par défaut :

| Mode   | Calendrier     | minScore | minRecallCount | minUniqueQueries |
| ------ | -------------- | -------- | -------------- | ---------------- |
| `off`  | Désactivé      | --       | --             | --               |
| `core` | Quotidien 3 AM | 0.75     | 3              | 2                |
| `rem`  | Toutes les 6h  | 0.85     | 4              | 3                |
| `deep` | Toutes les 12h | 0.80     | 3              | 3                |

## Modèle de planification

Lorsque rêver est activé, `memory-core` gère le calendrier récurrent
automatiquement. Vous n'avez pas besoin de créer manuellement une tâche cron pour cette fonctionnalité.

Vous pouvez toujours affiner le comportement avec des remplacements explicites tels que :

- `dreaming.frequency` (expression cron)
- `dreaming.timezone`
- `dreaming.limit`
- `dreaming.minScore`
- `dreaming.minRecallCount`
- `dreaming.minUniqueQueries`

## Configurer

```json
{
  "plugins": {
    "entries": {
      "memory-core": {
        "config": {
          "dreaming": {
            "mode": "core"
          }
        }
      }
    }
  }
}
```

## Commandes de chat

Changez les modes et vérifiez l'état depuis le chat :

```
/dreaming core          # Basculer vers le mode core (nuit)
/dreaming rem           # Basculer vers le mode rem (toutes les 6h)
/dreaming deep          # Basculer vers le mode deep (toutes les 12h)
/dreaming off           # Désactiver rêver
/dreaming status        # Afficher la configuration et le calendrier actuels
/dreaming help          # Afficher le guide des modes
```

## Commandes CLI

Prévisualisez et appliquez les promotions depuis la ligne de commande :

```bash
# Prévisualiser les candidats de promotion
openclaw memory promote

# Appliquer les promotions à MEMORY.md
openclaw memory promote --apply

# Limiter le nombre de prévisualisations
openclaw memory promote --limit 5

# Inclure les entrées déjà promues
openclaw memory promote --include-promoted

# Vérifier l'état de rêver
openclaw memory status --deep
```

Voir [memory CLI](/fr/cli/memory) pour la référence complète des drapeaux.

## Interface Dreams

Lorsque rêver est activé, la barre latérale Gateway affiche un onglet **Dreams** avec
les statistiques de mémoire (nombre à court terme, nombre à long terme, nombre promu) et l'heure
du prochain cycle planifié.

## Lectures complémentaires

- [Memory](/fr/concepts/memory)
- [Memory Search](/fr/concepts/memory-search)
- [memory CLI](/fr/cli/memory)
- [Memory configuration reference](/fr/reference/memory-config)
