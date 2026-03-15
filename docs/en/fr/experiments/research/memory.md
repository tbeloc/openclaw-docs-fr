---
summary: "Notes de recherche : système de mémoire hors ligne pour les espaces de travail Clawd (source de vérité Markdown + index dérivé)"
read_when:
  - Concevoir la mémoire de l'espace de travail (~/.openclaw/workspace) au-delà des journaux Markdown quotidiens
  - Décider : CLI autonome vs intégration profonde d'OpenClaw
  - Ajouter la récupération hors ligne + réflexion (retain/recall/reflect)
title: "Recherche sur la mémoire de l'espace de travail"
---

# Mémoire de l'espace de travail v2 (hors ligne) : notes de recherche

Objectif : espace de travail de style Clawd (`agents.defaults.workspace`, par défaut `~/.openclaw/workspace`) où la « mémoire » est stockée sous forme d'un fichier Markdown par jour (`memory/YYYY-MM-DD.md`) plus un petit ensemble de fichiers stables (par exemple `memory.md`, `SOUL.md`).

Ce document propose une **architecture de mémoire hors ligne d'abord** qui garde Markdown comme source de vérité canonique et vérifiable, mais ajoute une **récupération structurée** (recherche, résumés d'entités, mises à jour de confiance) via un index dérivé.

## Pourquoi changer ?

La configuration actuelle (un fichier par jour) est excellente pour :

- journalisation « append-only »
- édition humaine
- durabilité et auditabilité sauvegardées par git
- capture sans friction (« écrivez-le simplement »)

Elle est faible pour :

- récupération à haut rappel (« qu'avons-nous décidé à propos de X ? », « la dernière fois que nous avons essayé Y ? »)
- réponses centrées sur les entités (« parlez-moi d'Alice / Le Château / warelay ») sans relire plusieurs fichiers
- stabilité des opinions/préférences (et preuves quand elles changent)
- contraintes temporelles (« qu'était-il vrai en novembre 2025 ? ») et résolution des conflits

## Objectifs de conception

- **Hors ligne** : fonctionne sans réseau ; peut s'exécuter sur un ordinateur portable/Château ; aucune dépendance cloud.
- **Explicable** : les éléments récupérés doivent être attribuables (fichier + localisation) et séparables de l'inférence.
- **Peu de cérémonie** : la journalisation quotidienne reste Markdown, pas de travail de schéma lourd.
- **Incrémental** : v1 est utile avec FTS uniquement ; sémantique/vecteur et graphes sont des améliorations optionnelles.
- **Convivial pour les agents** : rend facile la « récupération dans les budgets de jetons » (retourner de petits paquets de faits).

## Modèle de l'étoile du nord (Hindsight × Letta)

Deux éléments à fusionner :

1. **Boucle de contrôle de style Letta/MemGPT**

- garder un petit « noyau » toujours en contexte (persona + faits clés de l'utilisateur)
- tout le reste est hors contexte et récupéré via des outils
- les écritures de mémoire sont des appels d'outils explicites (append/replace/insert), persistés, puis réinjectés au tour suivant

2. **Substrat de mémoire de style Hindsight**

- séparer ce qui est observé vs ce qui est cru vs ce qui est résumé
- supporter retain/recall/reflect
- opinions portant la confiance qui peuvent évoluer avec les preuves
- récupération consciente des entités + requêtes temporelles (même sans graphes de connaissances complets)

## Architecture proposée (source de vérité Markdown + index dérivé)

### Magasin canonique (convivial pour git)

Gardez `~/.openclaw/workspace` comme mémoire canonique lisible par l'homme.

Disposition d'espace de travail suggérée :

```
~/.openclaw/workspace/
  memory.md                    # petit : faits durables + préférences (noyau-ish)
  memory/
    YYYY-MM-DD.md              # journal quotidien (append ; narratif)
  bank/                        # pages de mémoire « typées » (stables, vérifiables)
    world.md                   # faits objectifs sur le monde
    experience.md              # ce que l'agent a fait (première personne)
    opinions.md                # prefs/jugements subjectifs + confiance + pointeurs de preuves
    entities/
      Peter.md
      The-Castle.md
      warelay.md
      ...
```

Notes :

- **Le journal quotidien reste un journal quotidien**. Pas besoin de le transformer en JSON.
- Les fichiers `bank/` sont **curés**, produits par des travaux de réflexion, et peuvent toujours être édités à la main.
- `memory.md` reste « petit + noyau-ish » : les choses que vous voulez que Clawd voie à chaque session.

### Magasin dérivé (rappel machine)

Ajoutez un index dérivé sous l'espace de travail (pas nécessairement suivi par git) :

```
~/.openclaw/workspace/.memory/index.sqlite
```

Soutenez-le avec :

- schéma SQLite pour les faits + liens d'entités + métadonnées d'opinion
- **FTS5** SQLite pour la récupération lexicale (rapide, minuscule, hors ligne)
- table d'embeddings optionnelle pour la récupération sémantique (toujours hors ligne)

L'index est toujours **reconstructible à partir de Markdown**.

## Retain / Recall / Reflect (boucle opérationnelle)

### Retain : normaliser les journaux quotidiens en « faits »

L'insight clé de Hindsight qui compte ici : stocker des **faits narratifs, autonomes**, pas de minuscules extraits.

Règle pratique pour `memory/YYYY-MM-DD.md` :

- à la fin de la journée (ou pendant), ajoutez une section `## Retain` avec 2–5 puces qui sont :
  - narratives (contexte inter-tours préservé)
  - autonomes (le sens seul a du sens plus tard)
  - étiquetées avec type + mentions d'entités

Exemple :

```
## Retain
- W @Peter: Actuellement à Marrakech (27 nov–1 déc 2025) pour l'anniversaire d'Andy.
- B @warelay: J'ai corrigé le crash Baileys WS en enveloppant les gestionnaires connection.update dans try/catch (voir memory/2025-11-27.md).
- O(c=0.95) @Peter: Préfère les réponses concises (<1500 caractères) sur WhatsApp ; le contenu long va dans les fichiers.
```

Analyse minimale :

- Préfixe de type : `W` (monde), `B` (expérience/biographique), `O` (opinion), `S` (observation/résumé ; généralement généré)
- Entités : `@Peter`, `@warelay`, etc (les slugs mappent à `bank/entities/*.md`)
- Confiance d'opinion : `O(c=0.0..1.0)` optionnel

Si vous ne voulez pas que les auteurs y pensent : le travail de réflexion peut déduire ces puces du reste du journal, mais avoir une section `## Retain` explicite est le plus facile « levier de qualité ».

### Recall : requêtes sur l'index dérivé

Recall devrait supporter :

- **lexical** : « trouver des termes/noms/commandes exacts » (FTS5)
- **entité** : « parlez-moi de X » (pages d'entités + faits liés aux entités)
- **temporel** : « qu'est-il arrivé autour du 27 nov » / « depuis la semaine dernière »
- **opinion** : « que préfère Peter ? » (avec confiance + preuves)

Le format de retour devrait être convivial pour les agents et citer les sources :

- `kind` (`world|experience|opinion|observation`)
- `timestamp` (jour source, ou plage de temps extraite si présente)
- `entities` (`["Peter","warelay"]`)
- `content` (le fait narratif)
- `source` (`memory/2025-11-27.md#L12` etc)

### Reflect : produire des pages stables + mettre à jour les croyances

La réflexion est un travail programmé (quotidien ou heartbeat `ultrathink`) qui :

- met à jour `bank/entities/*.md` à partir des faits récents (résumés d'entités)
- met à jour la confiance `bank/opinions.md` basée sur le renforcement/la contradiction
- propose optionnellement des modifications à `memory.md` (« faits durables noyau-ish »)

Évolution d'opinion (simple, explicable) :

- chaque opinion a :
  - déclaration
  - confiance `c ∈ [0,1]`
  - last_updated
  - liens de preuves (IDs de faits supportants + contredisant)
- quand de nouveaux faits arrivent :
  - trouver les opinions candidates par chevauchement d'entités + similarité (FTS d'abord, embeddings plus tard)
  - mettre à jour la confiance par de petits deltas ; les grands sauts nécessitent une forte contradiction + preuves répétées

## Intégration CLI : autonome vs intégration profonde

Recommandation : **intégration profonde dans OpenClaw**, mais gardez une bibliothèque séparable.

### Pourquoi intégrer dans OpenClaw ?

- OpenClaw connaît déjà :
  - le chemin de l'espace de travail (`agents.defaults.workspace`)
  - le modèle de session + heartbeats
  - les modèles de journalisation + dépannage
- Vous voulez que l'agent lui-même appelle les outils :
  - `openclaw memory recall "…" --k 25 --since 30d`
  - `openclaw memory reflect --since 7d`

### Pourquoi toujours diviser une bibliothèque ?

- garder la logique de mémoire testable sans passerelle/runtime
- réutiliser à partir d'autres contextes (scripts locaux, future application de bureau, etc.)

Forme :
L'outillage de mémoire est destiné à être une petite couche CLI + bibliothèque, mais c'est exploratoire uniquement.

## « S-Collide » / SuCo : quand l'utiliser (recherche)

Si « S-Collide » fait référence à **SuCo (Subspace Collision)** : c'est une approche de récupération ANN qui cible des compromis fort rappel/latence en utilisant des collisions apprises/structurées dans les sous-espaces (article : arXiv 2411.14754, 2024).

Approche pragmatique pour `~/.openclaw/workspace` :

- **ne pas commencer** avec SuCo.
- commencer avec SQLite FTS + (optionnel) embeddings simples ; vous obtiendrez la plupart des gains UX immédiatement.
- considérer les solutions de classe SuCo/HNSW/ScaNN uniquement une fois :
  - le corpus est grand (dizaines/centaines de milliers de chunks)
  - la recherche d'embeddings par force brute devient trop lente
  - la qualité du rappel est significativement goulot d'étranglement par la recherche lexicale

Alternatives conviviales hors ligne (complexité croissante) :

- SQLite FTS5 + filtres de métadonnées (zéro ML)
- Embeddings + force brute (fonctionne étonnamment loin si le nombre de chunks est faible)
- Index HNSW (courant, robuste ; nécessite une liaison de bibliothèque)
- SuCo (grade recherche ; attrayant s'il y a une implémentation solide que vous pouvez intégrer)

Question ouverte :

- quel est le **meilleur** modèle d'embedding hors ligne pour la « mémoire d'assistant personnel » sur vos machines (ordinateur portable + bureau) ?
  - si vous avez déjà Ollama : intégrer avec un modèle local ; sinon expédier un petit modèle d'embedding dans la chaîne d'outils.

## Pilote utile le plus petit

Si vous voulez une version minimale, toujours utile :

- Ajoutez des pages d'entités `bank/` et une section `## Retain` dans les journaux quotidiens.
- Utilisez SQLite FTS pour la récupération avec citations (chemin + numéros de ligne).
- Ajoutez des embeddings uniquement si la qualité du rappel ou l'échelle l'exige.

## Références

- Concepts Letta / MemGPT : « blocs de mémoire centrale » + « mémoire d'archivage » + mémoire auto-éditable pilotée par outils.
- Rapport technique Hindsight : « retain / recall / reflect », mémoire à quatre réseaux, extraction de faits narratifs, évolution de la confiance d'opinion.
- SuCo : arXiv 2411.14754 (2024) : « Subspace Collision » récupération de voisin le plus proche approximatif.
