---
title: "Rêver (expérimental)"
summary: "Consolidation de la mémoire en arrière-plan avec trois phases coopératives : légère, profonde et REM"
read_when:
  - You want memory promotion to run automatically
  - You want to understand the three dreaming phases
  - You want to tune consolidation without polluting MEMORY.md
---

# Rêver (expérimental)

Rêver est le système de consolidation de la mémoire en arrière-plan dans `memory-core`. Il
revisit ce qui s'est passé pendant les conversations et décide ce qui vaut la peine d'être conservé en tant que
contexte durable.

Rêver utilise trois **phases** coopératives, et non des modes concurrents. Chaque phase a
un rôle distinct, écrit dans une cible distincte et s'exécute selon son propre calendrier.

## Les trois phases

### Légère

Le rêve léger trie le désordre récent. Il analyse les traces de mémoire récentes, les déduplique
par similarité de Jaccard, regroupe les entrées connexes et prépare les mémoires candidates dans
la note de mémoire quotidienne (`memory/YYYY-MM-DD.md`).

Le rêve léger **n'écrit rien** dans `MEMORY.md`. Il organise et
prépare seulement. Pensez : « qu'est-ce qui pourrait être important plus tard ? »

### Profonde

Le rêve profond décide ce qui devient une mémoire durable. Il exécute la logique de promotion réelle : notation pondérée
sur six signaux, portes de seuil, nombre de rappels,
diversité des requêtes uniques, décroissance de récence et filtrage d'âge maximal.

Le rêve profond est la **seule** phase autorisée à écrire des faits durables dans `MEMORY.md`.
Il gère également la récupération quand la mémoire est faible (la santé tombe en dessous d'un
seuil configuré). Pensez : « qu'est-ce qui est assez vrai pour être conservé ? »

### REM

Le rêve REM cherche des motifs et de la réflexion. Il examine le matériel récent,
identifie les thèmes récurrents par regroupement de balises de concepts et écrit
des notes d'ordre supérieur et des réflexions dans la note quotidienne.

Le rêve REM écrit dans la note quotidienne (`memory/YYYY-MM-DD.md`), **pas** dans `MEMORY.md`.
Son résultat est interprétatif, pas canonique. Pensez : « quel motif remarqué-je ? »

## Limites strictes

| Phase | Rôle      | Écrit dans                 | N'écrit PAS dans |
| ----- | --------- | -------------------------- | ---------------- |
| Légère | Organiser | Note quotidienne (YYYY-MM-DD.md) | MEMORY.md        |
| Profonde | Préserver | MEMORY.md                  | --               |
| REM   | Interpréter | Note quotidienne (YYYY-MM-DD.md) | MEMORY.md        |

## Démarrage rapide

Activez les trois phases (recommandé) :

```json
{
  "plugins": {
    "entries": {
      "memory-core": {
        "config": {
          "dreaming": {
            "enabled": true
          }
        }
      }
    }
  }
}
```

Activez uniquement la promotion profonde :

```json
{
  "plugins": {
    "entries": {
      "memory-core": {
        "config": {
          "dreaming": {
            "enabled": true,
            "phases": {
              "light": { "enabled": false },
              "deep": { "enabled": true },
              "rem": { "enabled": false }
            }
          }
        }
      }
    }
  }
}
```

## Configuration

Tous les paramètres de rêve se trouvent sous `plugins.entries.memory-core.config.dreaming`
dans `openclaw.json`. Voir [Référence de configuration de la mémoire](/fr/reference/memory-config#dreaming-experimental)
pour la liste complète des clés.

### Paramètres globaux

| Clé              | Type      | Par défaut | Description                                      |
| ---------------- | --------- | ---------- | ------------------------------------------------ |
| `enabled`        | `boolean` | `true`     | Interrupteur maître pour toutes les phases       |
| `timezone`       | `string`  | non défini | Fuseau horaire pour l'évaluation du calendrier et les notes quotidiennes |
| `verboseLogging` | `boolean` | `false`    | Émettre des journaux détaillés par exécution de rêve |
| `storage.mode`   | `string`  | `"inline"` | `inline`, `separate`, ou `both`                  |

### Configuration de la phase légère

| Clé                | Type       | Par défaut                      | Description                       |
| ------------------ | ---------- | ------------------------------- | --------------------------------- |
| `enabled`          | `boolean`  | `true`                          | Activer la phase légère           |
| `cron`             | `string`   | `0 */6 * * *`                   | Calendrier (par défaut : toutes les 6 heures) |
| `lookbackDays`     | `number`   | `2`                             | Combien de jours de traces à analyser |
| `limit`            | `number`   | `100`                           | Max de candidats à préparer par exécution |
| `dedupeSimilarity` | `number`   | `0.9`                           | Seuil de Jaccard pour la déduplication |
| `sources`          | `string[]` | `["daily","sessions","recall"]` | Sources de données à analyser     |

### Configuration de la phase profonde

| Clé                   | Type       | Par défaut                                      | Description                          |
| --------------------- | ---------- | ----------------------------------------------- | ------------------------------------ |
| `enabled`             | `boolean`  | `true`                                          | Activer la phase profonde            |
| `cron`                | `string`   | `0 3 * * *`                                     | Calendrier (par défaut : quotidien à 3 h du matin) |
| `limit`               | `number`   | `10`                                            | Max de candidats à promouvoir par cycle |
| `minScore`            | `number`   | `0.8`                                           | Score pondéré minimum pour la promotion |
| `minRecallCount`      | `number`   | `3`                                             | Seuil de nombre de rappels minimum |
| `minUniqueQueries`    | `number`   | `3`                                             | Nombre minimum de requêtes distinctes |
| `recencyHalfLifeDays` | `number`   | `14`                                            | Jours pour que le score de récence soit divisé par deux |
| `maxAgeDays`          | `number`   | `30`                                            | Âge maximal de la note quotidienne pour la promotion |
| `sources`             | `string[]` | `["daily","memory","sessions","logs","recall"]` | Sources de données                   |

### Configuration de la récupération profonde

La récupération s'active quand la santé de la mémoire à long terme tombe en dessous d'un seuil.

| Clé                               | Type      | Par défaut | Description                                |
| --------------------------------- | --------- | ---------- | ------------------------------------------ |
| `recovery.enabled`                | `boolean` | `true`     | Activer la récupération automatique        |
| `recovery.triggerBelowHealth`     | `number`  | `0.35`     | Seuil de score de santé pour déclencher la récupération |
| `recovery.lookbackDays`           | `number`  | `30`       | Combien de jours en arrière pour chercher le matériel de récupération |
| `recovery.maxRecoveredCandidates` | `number`  | `20`       | Max de candidats à récupérer par exécution |
| `recovery.minRecoveryConfidence`  | `number`  | `0.9`      | Confiance minimale pour les candidats de récupération |
| `recovery.autoWriteMinConfidence` | `number`  | `0.97`     | Seuil d'écriture automatique (ignorer l'examen manuel) |

### Configuration de la phase REM

| Clé                  | Type       | Par défaut                      | Description                             |
| -------------------- | ---------- | ------------------------------- | --------------------------------------- |
| `enabled`            | `boolean`  | `true`                          | Activer la phase REM                    |
| `cron`               | `string`   | `0 5 * * 0`                     | Calendrier (par défaut : hebdomadaire, dimanche 5 h du matin) |
| `lookbackDays`       | `number`   | `7`                             | Combien de jours de matériel à analyser |
| `limit`              | `number`   | `10`                            | Max de motifs ou thèmes à écrire        |
| `minPatternStrength` | `number`   | `0.75`                          | Force minimale de co-occurrence de balises |
| `sources`            | `string[]` | `["memory","daily","deep"]`     | Sources de données pour la réflexion    |

### Remplacements d'exécution

Chaque phase accepte un bloc `execution` pour remplacer les valeurs par défaut globales :

| Clé               | Type     | Par défaut   | Description                    |
| ----------------- | -------- | ------------ | ------------------------------ |
| `speed`           | `string` | `"balanced"` | `fast`, `balanced`, ou `slow`  |
| `thinking`        | `string` | `"medium"`   | `low`, `medium`, ou `high`     |
| `budget`          | `string` | `"medium"`   | `cheap`, `medium`, `expensive` |
| `model`           | `string` | non défini   | Remplacer le modèle pour cette phase |
| `maxOutputTokens` | `number` | non défini   | Limiter les jetons de sortie   |
| `temperature`     | `number` | non défini   | Température d'échantillonnage (0-2) |
| `timeoutMs`       | `number` | non défini   | Délai d'expiration de la phase en millisecondes |

## Signaux de promotion (phase profonde)

Le rêve profond combine six signaux pondérés. La promotion nécessite que toutes les portes de seuil configurées
passent simultanément.

| Signal              | Poids | Description                                        |
| ------------------- | ----- | -------------------------------------------------- |
| Fréquence           | 0.24  | Combien de fois la même entrée a été rappelée     |
| Pertinence          | 0.30  | Scores de rappel moyens lors de la récupération   |
| Diversité des requêtes | 0.15 | Nombre d'intentions de requête distinctes qui l'ont surfacée |
| Récence             | 0.15  | Décroissance temporelle (`recencyHalfLifeDays`, par défaut 14) |
| Consolidation       | 0.10  | Récompenser les rappels répétés sur plusieurs jours |
| Richesse conceptuelle | 0.06 | Récompenser les entrées avec des balises de concepts dérivées plus riches |

## Commandes de chat

```
/dreaming status                 # Afficher la configuration des phases et le calendrier
/dreaming on                     # Activer toutes les phases
/dreaming off                    # Désactiver toutes les phases
/dreaming enable light|deep|rem  # Activer une phase spécifique
/dreaming disable light|deep|rem # Désactiver une phase spécifique
/dreaming help                   # Afficher le guide d'utilisation
```

## Commandes CLI

Prévisualisez et appliquez les promotions profondes depuis la ligne de commande :

```bash
# Prévisualiser les candidats à la promotion
openclaw memory promote

# Appliquer les promotions à MEMORY.md
openclaw memory promote --apply

# Limiter le nombre de prévisualisations
openclaw memory promote --limit 5

# Inclure les entrées déjà promues
openclaw memory promote --include-promoted

# Vérifier l'état du rêve
openclaw memory status --deep
```

Voir [memory CLI](/fr/cli/memory) pour la référence complète des drapeaux.

## Comment ça marche

### Pipeline de la phase légère

1. Lire les entrées de rappel à court terme depuis `memory/.dreams/short-term-recall.json`.
2. Filtrer les entrées dans les `lookbackDays` du moment actuel.
3. Dédupliquer par similarité de Jaccard (seuil configurable).
4. Trier par score de rappel moyen, prendre jusqu'à `limit` entrées.
5. Écrire les candidats préparés dans la note quotidienne sous un bloc `## Light Sleep`.

### Pipeline de la phase profonde

1. Lire et classer les candidats de rappel à court terme en utilisant des signaux pondérés.
2. Appliquer les portes de seuil : `minScore`, `minRecallCount`, `minUniqueQueries`.
3. Filtrer par `maxAgeDays` et appliquer la décroissance de récence.
4. Distribuer sur les espaces de travail de mémoire configurés.
5. Relire la note quotidienne en direct avant d'écrire (ignorer les extraits obsolètes ou supprimés).
6. Ajouter les entrées qualifiantes à `MEMORY.md` avec les horodatages promus.
7. Marquer les entrées promues pour les exclure des cycles futurs.
8. Si la santé est en dessous de `recovery.triggerBelowHealth`, exécuter la passe de récupération.

### Pipeline de la phase REM

1. Lire les traces de mémoire récentes dans les `lookbackDays`.
2. Regrouper les balises de concepts par co-occurrence.
3. Filtrer les motifs par `minPatternStrength`.
4. Écrire les thèmes et réflexions dans la note quotidienne sous un bloc `## REM Sleep`.

## Planification

Chaque phase gère automatiquement son propre travail cron. Lorsque la rêverie est activée,
`memory-core` réconcilie les travaux cron gérés au démarrage de la passerelle. Vous n'avez pas besoin
de créer manuellement des entrées cron.

| Phase | Planification par défaut | Description         |
| ----- | ------------------------ | ------------------- |
| Light | `0 */6 * * *`            | Toutes les 6 heures |
| Deep  | `0 3 * * *`              | Quotidiennement à 3 h |
| REM   | `0 5 * * 0`              | Hebdomadaire, dimanche 5 h |

Remplacez n'importe quelle planification avec la clé `cron` de la phase. Tous les horaires respectent le paramètre global
`timezone`.

## Interface utilisateur Dreams

Lorsque la rêverie est activée, la barre latérale de la passerelle affiche un onglet **Dreams** avec
les statistiques de mémoire (nombre à court terme, nombre à long terme, nombre promu) et l'heure
du prochain cycle planifié. Les compteurs quotidiens respectent `dreaming.timezone` lorsqu'il est défini et
sinon reviennent au fuseau horaire utilisateur configuré.

Les exécutions manuelles de `openclaw memory promote` utilisent les mêmes seuils de phase profonde
par défaut, de sorte que la promotion planifiée et à la demande restent alignées sauf si vous transmettez des remplacements CLI.

## Connexes

- [Memory](/fr/concepts/memory)
- [Memory Search](/fr/concepts/memory-search)
- [Référence de configuration Memory](/fr/reference/memory-config)
- [memory CLI](/fr/cli/memory)
