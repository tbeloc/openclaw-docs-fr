---
read_when:
  - Concevoir une mémoire d'espace de travail au-delà du journal Markdown quotidien (~/.openclaw/workspace)
  - Décider : CLI autonome vs intégration profonde OpenClaw
  - Ajouter la mémorisation hors ligne + réflexion (retain/recall/reflect)
summary: Notes de recherche : système de mémoire hors ligne pour l'espace de travail Clawd (Markdown comme source de données + index dérivés)
title: Recherche sur la mémoire d'espace de travail
x-i18n:
  generated_at: "2026-02-03T10:06:14Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 1753c8ee6284999fab4a94ff5fae7421c85233699c9d3088453d0c2133ac0feb
  source_path: experiments/research/memory.md
  workflow: 15
---

# Mémoire d'espace de travail v2 (hors ligne) : Notes de recherche

Objectif : Un espace de travail de style Clawd (`agents.defaults.workspace`, par défaut `~/.openclaw/workspace`), où la "mémoire" est stockée sous la forme d'un fichier Markdown par jour (`memory/YYYY-MM-DD.md`) plus un petit ensemble de fichiers stables (par exemple `memory.md`, `SOUL.md`).

Ce document propose une architecture de mémoire **hors ligne en priorité**, en gardant Markdown comme source de données canonique et révisable, mais en ajoutant une **mémorisation structurée** (recherche, résumés d'entités, mises à jour de confiance) via des index dérivés.

## Pourquoi changer ?

La configuration actuelle (un fichier par jour) est excellente pour :

- Journalisation "append-only"
- Édition manuelle
- Persistance soutenue par git + auditabilité
- Capture à faible friction ("écrivez simplement")

Mais elle est faible pour :

- Récupération à haut rappel ("Quelle décision avons-nous prise sur X ?", "Quand avons-nous essayé Y la dernière fois ?")
- Réponses centrées sur l'entité ("Parlez-moi d'Alice / The Castle / warelay") sans relire plusieurs fichiers
- Stabilité des opinions/préférences (et preuves de changement)
- Contraintes temporelles ("Qu'était vrai pendant novembre 2025 ?") et résolution de conflits

## Objectifs de conception

- **Hors ligne** : Fonctionne sans réseau ; peut s'exécuter sur un ordinateur portable/Castle ; pas de dépendance cloud.
- **Interprétable** : Les éléments récupérés doivent être attribuables (fichier + emplacement) et séparés du raisonnement.
- **Faible cérémonie** : Les journaux quotidiens restent Markdown, pas de travail de schéma lourd.
- **Incrémental** : v1 est utile avec juste FTS ; sémantique/vecteurs et graphes sont des mises à niveau optionnelles.
- **Convivial pour les agents** : Rendre "mémoriser dans le budget de tokens" simple (retourner de petits paquets de faits).

## Modèle de l'étoile polaire (Hindsight × Letta)

Besoin de fusionner deux parties :

1. **Boucle de contrôle de style Letta/MemGPT**

- Maintenir un petit "noyau" toujours en contexte (rôle + faits clés de l'utilisateur)
- Tout le reste est hors contexte, récupéré via des outils
- Les écritures de mémoire sont des appels d'outils explicites (append/replace/insert), réinjectés après persistance au prochain tour

2. **Base de mémoire de style Hindsight**

- Séparer observé, cru et résumé
- Supporter retain/recall/reflect
- Les opinions avec confiance peuvent évoluer avec les preuves
- Récupération consciente des entités + requêtes temporelles (même sans graphe de connaissances complet)

## Architecture proposée (source de données Markdown + index dérivés)

### Stockage canonique (git-friendly)

Garder `~/.openclaw/workspace` comme mémoire canonique lisible par l'homme.

Disposition d'espace de travail recommandée :

```
~/.openclaw/workspace/
  memory.md                    # Petit : faits persistants + préférences (comme noyau)
  memory/
    YYYY-MM-DD.md              # Journal quotidien (append ; narratif)
  bank/                        # Pages de mémoire "typées" (stables, révisables)
    world.md                   # Faits objectifs sur le monde
    experience.md              # Ce que l'agent a fait (première personne)
    opinions.md                # Préférences/jugements subjectifs + confiance + pointeurs de preuves
    entities/
      Peter.md
      The-Castle.md
      warelay.md
      ...
```

Notes :

- **Les journaux quotidiens restent des journaux quotidiens**. Pas besoin de les convertir en JSON.
- Les fichiers `bank/` sont **curés**, générés par des tâches de réflexion, toujours modifiables manuellement.
- `memory.md` reste "petit + comme noyau" : ce que vous voulez que Clawd voie à chaque session.

### Stockage dérivé (mémorisation machine)

Ajouter des index dérivés sous l'espace de travail (pas nécessairement suivi par git) :

```
~/.openclaw/workspace/.memory/index.sqlite
```

Support backend :

- Schéma SQLite pour faits + liens d'entités + métadonnées d'opinions
- **FTS5** SQLite pour mémorisation lexicale (rapide, petit, hors ligne)
- Table d'embeddings optionnelle pour mémorisation sémantique (toujours hors ligne)

L'index est toujours **reconstructible à partir de Markdown**.

## Retain / Recall / Reflect (boucle opérationnelle)

### Retain : Normaliser le journal quotidien en "faits"

L'insight clé important ici de Hindsight : stocker des **faits narratifs, autonomes**, pas de minuscules fragments.

Règles pratiques pour `memory/YYYY-MM-DD.md` :

- À la fin de la journée (ou pendant), ajouter une section `## Retain` avec 2-5 points clés :
  - Narratif (conserver le contexte entre les tours)
  - Autonome (a du sens même isolé)
  - Marquer le type + mentions d'entités

Exemple :

```
## Retain
- W @Peter: Currently in Marrakech (Nov 27–Dec 1, 2025) for Andy's birthday.
- B @warelay: I fixed the Baileys WS crash by wrapping connection.update handlers in try/catch (see memory/2025-11-27.md).
- O(c=0.95) @Peter: Prefers concise replies (<1500 chars) on WhatsApp; long content goes into files.
```

Analyse minimale :

- Préfixes de type : `W` (monde), `B` (expérience/biographie), `O` (opinion), `S` (observation/résumé ; généralement généré)
- Entités : `@Peter`, `@warelay`, etc. (slug mappé à `bank/entities/*.md`)
- Confiance d'opinion : `O(c=0.0..1.0)` optionnel

Si vous ne voulez pas que l'auteur considère ces éléments : une tâche de réflexion peut déduire ces points du reste du journal, mais avoir une section `## Retain` explicite est le "levier de qualité" le plus simple.

### Recall : Requêtes sur l'index dérivé

Recall devrait supporter :

- **Lexical** : "Trouver des termes/noms/commandes exacts" (FTS5)
- **Entité** : "Parlez-moi de X" (page d'entité + faits liés aux entités)
- **Temporel** : "Qu'est-ce qui s'est passé autour du 27 novembre"/"Depuis la semaine dernière"
- **Opinion** : "Quelles sont les préférences de Peter ?" (avec confiance + preuves)

Le format de retour devrait être convivial pour les agents et citer les sources :

- `kind` (`world|experience|opinion|observation`)
- `timestamp` (date source, ou plage de temps extraite si présente)
- `entities` (`["Peter","warelay"]`)
- `content` (fait narratif)
- `source` (`memory/2025-11-27.md#L12`, etc.)

### Reflect : Générer des pages stables + mettre à jour les croyances

Reflect est une tâche programmée (quotidienne ou heartbeat `ultrathink`) qui :

- Met à jour `bank/entities/*.md` (résumés d'entités) basé sur les faits récents
- Met à jour les confiances `bank/opinions.md` basées sur le renforcement/contradiction
- Peut proposer des éditions à `memory.md` (faits persistants "comme noyau")

Évolution d'opinion (simple, interprétable) :

- Chaque opinion a :
  - Énoncé
  - Confiance `c ∈ [0,1]`
  - last_updated
  - Liens de preuves (faits de soutien + contradiction)
- Quand un nouveau fait arrive :
  - Trouver les opinions candidates par chevauchement d'entité + similarité (d'abord FTS, puis embedding)
  - Mettre à jour la confiance par petits incréments ; les grands sauts nécessitent une contradiction forte + preuves répétées

## Intégration CLI : Autonome vs Intégration profonde

Recommandation : **Intégration profonde dans OpenClaw**, mais garder une bibliothèque centrale séparable.

### Pourquoi intégrer dans OpenClaw ?

- OpenClaw connaît déjà :
  - Chemin d'espace de travail (`agents.defaults.workspace`)
  - Modèle de session + heartbeat
  - Journalisation + modes de dépannage
- Vous voulez que les agents appellent eux-mêmes les outils :
  - `openclaw memory recall "…" --k 25 --since 30d`
  - `openclaw memory reflect --since 7d`

### Pourquoi rester séparé ?

- Garder la logique de mémoire testable sans Gateway/runtime
- Réutilisable à partir d'autres contextes (scripts locaux, futures applications de bureau, etc.)

Morphologie :
Les outils de mémoire sont censés être une petite couche CLI + bibliothèque, mais c'est exploratoire.

## "S-Collide" / SuCo : Quand l'utiliser (Recherche)

Si "S-Collide" fait référence à **SuCo (Subspace Collision)** : c'est une méthode de récupération ANN qui réalise un bon compromis rappel/latence via des collisions apprises/structurées dans les sous-espaces (papier : arXiv 2411.14754, 2024).

Pour une perspective pragmatique sur `~/.openclaw/workspace` :

- **Ne pas commencer** par SuCo.
- Commencer par SQLite FTS + (optionnellement) embeddings simples ; vous obtiendrez immédiatement la plupart des gains UX.
- Considérer les solutions au niveau SuCo/HNSW/ScaNN uniquement si :
  - Le corpus est volumineux (dizaines de milliers/centaines de milliers de chunks)
  - La recherche d'embeddings par force brute devient trop lente
  - La qualité du rappel est clairement goulot d'étranglement par la recherche lexicale

Alternatives conviviales hors ligne (complexité croissante) :

- SQLite FTS5 + filtrage de métadonnées (zéro ML)
- Embeddings + recherche par force brute (fonctionne étonnamment bien si le nombre de chunks est bas)
- Index HNSW (courant, robuste ; nécessite des liaisons de bibliothèque)
- SuCo (niveau recherche ; attrayant s'il existe une implémentation fiable embarquée)

Questions ouvertes :

- Pour la "mémoire d'assistant personnel" sur votre machine (ordinateur portable + bureau), quel est le **meilleur** modèle d'embedding hors ligne ?
  - Si vous avez déjà Ollama : utilisez les embeddings du modèle local ; sinon, incluez un petit modèle d'embedding dans la chaîne d'outils.

## Pilote minimum viable

Si vous voulez une version minimale mais toujours utile :

- Ajouter des pages d'entités `bank/` et une section `## Retain` dans les journaux quotidiens.
- Utiliser SQLite FTS pour la mémorisation avec citations (chemin + numéro de ligne).
- Ajouter des embeddings uniquement si la qualité du rappel ou l'échelle l'exigent.

## Références

- Concepts Letta / MemGPT : "bloc de mémoire centrale" + "mémoire d'archive" + mémoire auto-éditée pilotée par outils.
- Rapport technique Hindsight : "retain / recall / reflect", mémoire à quatre réseaux, extraction de faits narratifs, évolution de confiance d'opinion.
- SuCo : arXiv 2411.14754 (2024) : "Subspace Collision" pour la récupération des plus proches voisins approximatifs.
