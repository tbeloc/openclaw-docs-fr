---
title: "Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Note de maturité des mémoires locales et des intégrations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Note de maturité des mémoires locales et des intégrations

## Résumé

OpenClaw peut utiliser des fournisseurs locaux pour les intégrations de mémoire et la sélection du modèle de vidage de mémoire, avec Ollama et LM Studio exposant les contrats de fournisseur d'intégration et le cœur de mémoire se dégradant vers une recherche lexicale de secours lorsque les intégrations ne sont pas disponibles. La couverture est crédible pour l'enregistrement des fournisseurs et le comportement de secours, mais le parcours utilisateur global reste fragile car la sélection du fournisseur de chat, la sélection du modèle d'intégration de mémoire, les dimensions vectorielles et le comportement de reconstruction peuvent diverger.

## Portée des catégories

Inclus dans cette catégorie :

- Sélection du fournisseur d'intégration : Couvre la sélection du fournisseur d'intégration sur les fournisseurs d'intégration locaux pour Ollama et LM Studio, le comportement d'intégration de l'hôte de mémoire, la disponibilité de la recherche de mémoire, les remplacements locaux du modèle `memoryFlush`, et les comportements associés des intégrations et de la mémoire locales.
- Disponibilité de la recherche de mémoire : Couvre la disponibilité de la recherche de mémoire sur les fournisseurs d'intégration locaux pour Ollama et LM Studio, le comportement d'intégration de l'hôte de mémoire, la disponibilité de la recherche de mémoire, les remplacements locaux du modèle `memoryFlush`, et les comportements associés des intégrations et de la mémoire locales.
- Remplacement du modèle memoryFlush : Couvre le remplacement du modèle memoryFlush sur les fournisseurs d'intégration locaux pour Ollama et LM Studio, le comportement d'intégration de l'hôte de mémoire, la disponibilité de la recherche de mémoire, les remplacements locaux du modèle `memoryFlush`, et les comportements associés des intégrations et de la mémoire locales.
- Recherche lexicale de secours : Couvre la recherche lexicale de secours sur les fournisseurs d'intégration locaux pour Ollama et LM Studio, le comportement d'intégration de l'hôte de mémoire, la disponibilité de la recherche de mémoire, les remplacements locaux du modèle `memoryFlush`, et les comportements associés des intégrations et de la mémoire locales.
- Orientation en cas de non-concordance des fournisseurs : Couvre l'orientation en cas de non-concordance des fournisseurs sur les fournisseurs d'intégration locaux pour Ollama et LM Studio, le comportement d'intégration de l'hôte de mémoire, la disponibilité de la recherche de mémoire, les remplacements locaux du modèle `memoryFlush`, et les comportements associés des intégrations et de la mémoire locales.

## Fonctionnalités

- Sélection du fournisseur d'intégration : Couvre la sélection du fournisseur d'intégration sur les fournisseurs d'intégration locaux pour Ollama et LM Studio, le comportement d'intégration de l'hôte de mémoire, la disponibilité de la recherche de mémoire, les remplacements locaux du modèle `memoryFlush`, et les comportements associés des intégrations et de la mémoire locales.
- Disponibilité de la recherche de mémoire : Couvre la disponibilité de la recherche de mémoire sur les fournisseurs d'intégration locaux pour Ollama et LM Studio, le comportement d'intégration de l'hôte de mémoire, la disponibilité de la recherche de mémoire, les remplacements locaux du modèle `memoryFlush`, et les comportements associés des intégrations et de la mémoire locales.
- Remplacement du modèle memoryFlush : Couvre le remplacement du modèle memoryFlush sur les fournisseurs d'intégration locaux pour Ollama et LM Studio, le comportement d'intégration de l'hôte de mémoire, la disponibilité de la recherche de mémoire, les remplacements locaux du modèle `memoryFlush`, et les comportements associés des intégrations et de la mémoire locales.
- Recherche lexicale de secours : Couvre la recherche lexicale de secours sur les fournisseurs d'intégration locaux pour Ollama et LM Studio, le comportement d'intégration de l'hôte de mémoire, la disponibilité de la recherche de mémoire, les remplacements locaux du modèle `memoryFlush`, et les comportements associés des intégrations et de la mémoire locales.
- Orientation en cas de non-concordance des fournisseurs : Couvre l'orientation en cas de non-concordance des fournisseurs sur les fournisseurs d'intégration locaux pour Ollama et LM Studio, le comportement d'intégration de l'hôte de mémoire, la disponibilité de la recherche de mémoire, les remplacements locaux du modèle `memoryFlush`, et les comportements associés des intégrations et de la mémoire locales.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs :
  - `/Users/kevinlin/code/openclaw/docs/concepts/memory.md:141` jusqu'à la ligne
    154 documentent les fournisseurs de recherche de mémoire, y compris les options locales, Ollama et
    compatibles avec OpenAI.
  - `/Users/kevinlin/code/openclaw/docs/concepts/memory.md:171` jusqu'à la ligne
    174 documentent le support local d'intégration Ollama avec LanceDB.
  - `/Users/kevinlin/code/openclaw/docs/concepts/memory.md:192` jusqu'à la ligne
    210 documentent les remplacements locaux du modèle `memoryFlush`.
  - `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/embedding-provider.ts:67`
    jusqu'à la ligne 145 implémentent les intégrations LM Studio et le comportement de préchauffage.
  - `/Users/kevinlin/code/openclaw/extensions/memory-core/src/memory/manager.ts:346`
    jusqu'à la ligne 359 gèrent la dégradation des fournisseurs locaux après l'échec du worker.
- Signaux négatifs :
  - vLLM et SGLang sont couverts par la mécanique des fournisseurs compatibles avec OpenAI,
    mais les preuves du fournisseur d'intégration local de première classe sont beaucoup plus fortes pour
    Ollama et LM Studio.
  - Les changements de dimension, la non-concordance des fournisseurs et le comportement de secours/reconstruction sont
    difficiles à comprendre à partir d'une seule page orientée utilisateur.
- Lacunes d'intégration :
  - Ajouter un test qui configure le chat local plus les intégrations locales, indexe un
    petit ensemble de mémoire, vérifie les dimensions vectorielles, redémarre avec un fournisseur d'intégration indisponible, et vérifie les messages de secours lexical.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl :
  - La requête `local embeddings Ollama mixed OpenAI vector` a retourné le problème #83333,
    montrant la pression des utilisateurs autour des intégrations locales et de la configuration mixte des fournisseurs/vecteurs.
  - La requête `Ollama LM Studio memory embeddings local provider` a retourné le problème
    #81961, qui demandait également un tableau de bord pour gérer les fournisseurs locaux.
- Rapports Discrawl :
  - La requête `local embeddings Ollama mixed OpenAI vector` a retourné des conseils sur
    les intégrations OpenAI hébergées, les modèles locaux QMD et la non-concordance des dimensions.
  - La requête `Ollama LM Studio memory embeddings local provider` a retourné des threads d'assistance sur le chat local par rapport aux intégrations de mémoire et la non-concordance des fournisseurs locaux.
- Bonnes qualités :
  - Le cœur de mémoire se dégrade plutôt que d'échouer complètement dans plusieurs chemins d'intégration indisponible, et la documentation reconnaît directement les fournisseurs d'intégration locaux.
  - Ollama et LM Studio exposent les contrats de fournisseur pour l'intégration de mémoire au lieu de traiter les intégrations comme un service externe non lié.
- Mauvaises qualités :
  - Le fournisseur de chat local et le fournisseur d'intégration de mémoire local sont toujours des concepts utilisateur distincts, ce qui rend les défaillances de fournisseur mixte et de non-concordance de dimension faciles à créer.
  - Les preuves d'archive montrent que les utilisateurs ont besoin d'aide pour distinguer « modèle local pour le chat » de « modèle local pour les intégrations de mémoire ».
- Exclus de la qualité :
  - La couverture des tests du fournisseur d'intégration et la profondeur des tests de l'hôte de mémoire n'ont pas été utilisées comme entrées de qualité.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/local-model-providers-ollama-vllm-sglang-lm-studio.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la sélection du fournisseur d'intégration, la disponibilité de la recherche de mémoire, le remplacement du modèle memoryFlush, la recherche lexicale de secours, l'orientation en cas de non-concordance des fournisseurs.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucun flux de configuration de modèle local unique n'a été trouvé qui configure le chat, les intégrations,
  le vidage de mémoire, les attentes de dimension vectorielle et le comportement de secours ensemble.
- L'orientation des intégrations locales vLLM et SGLang est moins directe que l'orientation Ollama et LM
  Studio.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/concepts/memory.md:141` documente les options de fournisseur de recherche de mémoire.
- `/Users/kevinlin/code/openclaw/docs/concepts/memory.md:171` documente le support local d'intégration Ollama avec LanceDB.
- `/Users/kevinlin/code/openclaw/docs/concepts/memory.md:192` documente les remplacements locaux du modèle `memoryFlush`.
- `/Users/kevinlin/code/openclaw/docs/gateway/doctor.md:512` documente les vérifications de disponibilité de la recherche de mémoire.

### Source

- `/Users/kevinlin/code/openclaw/extensions/lmstudio/openclaw.plugin.json:51`
  déclare la capacité d'intégration de mémoire LM Studio.
- `/Users/kevinlin/code/openclaw/extensions/ollama/openclaw.plugin.json:45`
  déclare les contrats de mémoire et de recherche web Ollama.
- `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/embedding-provider.ts:67`
  implémente les intégrations LM Studio.
- `/Users/kevinlin/code/openclaw/extensions/ollama/index.ts:132` enregistre
  le support d'intégration de mémoire Ollama.
- `/Users/kevinlin/code/openclaw/extensions/ollama/index.ts:247` câble le
  fournisseur d'intégration Ollama.
- `/Users/kevinlin/code/openclaw/extensions/memory-core/src/memory/manager.ts:346`
  marque les fournisseurs locaux dégradés après l'échec du worker.
- `/Users/kevinlin/code/openclaw/extensions/memory-core/src/memory/manager.ts:1009`
  gère le secours d'intégration indisponible.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/packages/memory-host-sdk/src/host/embeddings.test.ts:339`
  couvre le comportement d'intégration du processus worker.
- `/Users/kevinlin/code/openclaw/extensions/memory-core/src/memory/manager-sync-ops.ts:1398`
  abandonne lorsqu'un fournisseur d'intégration configuré est indisponible.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/packages/memory-host-sdk/src/host/embeddings.test.ts:72`
  couvre la gestion du modèle par défaut du fournisseur d'intégration local.
- `/Users/kevinlin/code/openclaw/packages/memory-host-sdk/src/host/embeddings.test.ts:156`
  couvre le comportement du lot séquentiel.
- `/Users/kevinlin/code/openclaw/packages/memory-host-sdk/src/host/embeddings.test.ts:189`
  couvre le chemin du modèle et le comportement du cache.
- `/Users/kevinlin/code/openclaw/extensions/ollama/src/embedding-provider.test.ts:104`
  couvre les appels à `/api/embed` et le routage d'origine local.
- `/Users/kevinlin/code/openclaw/extensions/ollama/src/embedding-provider.test.ts:149`
  couvre la gestion de l'origine cloud.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "local embeddings Ollama mixed OpenAI vector" --json --limit 5`

Résultats :

- A retourné le problème #83333, pertinent pour la configuration mixte d'intégration locale et vectorielle.

Requête : `gitcrawl search openclaw/openclaw --query "Ollama LM Studio memory embeddings local provider" --json --limit 5`

Résultats :

- A retourné le problème #81961, qui demande une surface de gestion des fournisseurs de modèles
  incluant les fournisseurs locaux.

### Requêtes Discrawl

Requête : `discrawl search --mode hybrid --limit 5 "local embeddings Ollama mixed OpenAI vector"`

Résultats :

- A retourné des conseils d'assistance sur les intégrations OpenAI hébergées, les modèles locaux QMD,
  et la non-concordance des dimensions.

Requête : `discrawl search --mode hybrid --limit 5 "Ollama LM Studio memory embeddings local provider"`

Résultats :

- A retourné des threads d'assistance sur le chat local par rapport aux intégrations de mémoire et la non-concordance des fournisseurs locaux.
