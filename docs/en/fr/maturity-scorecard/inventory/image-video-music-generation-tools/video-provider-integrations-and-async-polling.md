---
title: "Outils de génération d'images/vidéos/musique - Note de maturité des fournisseurs vidéo et interrogation"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de génération d'images/vidéos/musique - Note de maturité des fournisseurs vidéo et interrogation

## Résumé

L'étendue des fournisseurs vidéo est élevée. La surface du fournisseur fourni couvre OpenAI
Sora, l'API vidéos OpenRouter, les travaux de file d'attente fal, les tâches Runway, PixVerse, Together,
xAI, Qwen, Google, MiniMax et des enregistrements de fournisseurs supplémentaires. Le contrat
commun prend en charge la soumission de file d'attente, l'interrogation, la gestion des URL hébergées, les téléchargements et
les déclarations de capacité du fournisseur.

La couverture est Beta car la documentation et les tests couvrent la liste des fournisseurs principaux et la
suite en direct, mais la sémantique asynchrone spécifique au fournisseur varie considérablement. La qualité est Alpha
car les résultats d'archive incluent les défaillances vidéo OpenRouter, la configuration acceptée qui
échoue à l'exécution, l'instabilité de la livraison asynchrone et les combinaisons fournisseur/requête qui
ignorent tous les candidats.

## Portée de la catégorie

Cette catégorie couvre l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo
après la normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway,
PixVerse, Together, xAI, Qwen, Google, MiniMax, BytePlus, Alibaba, DeepInfra,
Vydra, travaux de file d'attente, interrogation de tâches, URL de médias hébergés, téléchargements et
métadonnées d'actifs vidéo retournées.

## Fonctionnalités

- travaux soutenus par file d'attente : Couvre les travaux soutenus par file d'attente dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway et fournisseurs vidéo connexes et comportement d'interrogation.
- gestion de l'interrogation/délai d'expiration : Couvre la gestion de l'interrogation/délai d'expiration dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway et fournisseurs vidéo connexes et comportement d'interrogation.
- Téléchargement d'URL hébergée : Couvre le téléchargement d'URL hébergée dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway et fournisseurs vidéo connexes et comportement d'interrogation.
- explications de saut de fournisseur : Couvre les explications de saut de fournisseur dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway et fournisseurs vidéo connexes et comportement d'interrogation.
- métadonnées d'actif retournées : Couvre les métadonnées d'actif retournées dans l'intégration du fournisseur et l'interrogation asynchrone pour la génération vidéo après normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway et fournisseurs vidéo connexes et comportement d'interrogation.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : La documentation des fournisseurs répertorie de nombreux fournisseurs vidéo, la source enregistre plusieurs plugins, les tests de contrat de capacité suivent les manifestes des fournisseurs et les wrappers de fournisseur en direct exercent les modes déclarés.
- Signaux négatifs : L'interrogation asynchrone, l'expiration des URL hébergées, la dérive de schéma spécifique au fournisseur et le comportement spécifique au mode varient considérablement et ne sont pas également prouvés entre les fournisseurs.
- Lacunes d'intégration : Ajouter des voies de fumée de fournisseur pour une API directe représentative, une API de file d'attente, un téléchargement d'URL hébergée et un travail d'API vidéos OpenRouter, avec vérification de livraison d'artefact.

## Score de qualité

- Score : `Alpha (62%)`
- Rapports Gitcrawl : Les recherches vidéo ont retourné #79535 sur la génération vidéo OpenRouter échouant silencieusement, #45655 sur les modèles de sortie image/vidéo configurés échouant à l'exécution et #86279/#86034 sur le succès des médias générés étant obscurci par l'échec de livraison.
- Rapports Discrawl : La recherche Discord a trouvé une requête vidéo où les fournisseurs sur fal, Google, MiniMax, OpenAI, Runway, xAI, OpenRouter, BytePlus, Qwen, Alibaba, DeepInfra et Vydra ont été ignorés en raison des entrées audio de référence non prises en charge.
- Bonnes qualités : Les déclarations de fournisseur et la logique de saut à l'exécution rendent explicites les capacités hétérogènes des fournisseurs.
- Mauvaises qualités : L'étendue du fournisseur crée de nombreux bords fragiles : la sémantique de file d'attente, la latence longue, les défaillances de téléchargement d'URL hébergée et les incompatibilités de capacité peuvent tous empêcher une vidéo visible par l'utilisateur réussie.
- Exclu de la qualité : L'étendue des tests unitaires, d'intégration, en direct et d'assurance qualité a été traitée comme des entrées de couverture uniquement ; les tests n'ont pas augmenté ou diminué ce score de qualité.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/image-video-music-generation-tools.md`.
- Signaux positifs : les documents archivés, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour les travaux soutenus par file d'attente, la gestion de l'interrogation/délai d'expiration, le téléchargement d'URL hébergée, les explications de saut de fournisseur, les métadonnées d'actif retournées.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La latence vidéo inter-fournisseur et la sémantique d'interrogation ne sont pas uniformes suffisamment pour des preuves solides.
- Le comportement des URL hébergées et du téléchargement d'artefacts reste dépendant du fournisseur.
- Les vidéos OpenRouter et les configurations de modèle acceptées mais défaillantes plus anciennes sont toujours visibles dans les preuves d'archive actuelles.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/video-generation.md:11` documente la génération à partir de texte, d'images ou de vidéos et la sélection automatique du fournisseur.
- `/Users/kevinlin/code/openclaw/docs/tools/video-generation.md:108` répertorie les fournisseurs vidéo pris en charge.
- `/Users/kevinlin/code/openclaw/docs/tools/video-generation.md:380` documente les notes du fournisseur pour fal, OpenAI, OpenRouter, Runway, xAI et autres.
- `/Users/kevinlin/code/openclaw/docs/providers/runway.md` documente le fournisseur Runway.
- `/Users/kevinlin/code/openclaw/docs/providers/pixverse.md` documente le fournisseur PixVerse.
- `/Users/kevinlin/code/openclaw/docs/providers/fal.md` documente la prise en charge de la génération de médias fal.
- `/Users/kevinlin/code/openclaw/docs/providers/openrouter.md` documente la prise en charge de la génération de médias OpenRouter.

### Source

- `/Users/kevinlin/code/openclaw/extensions/openai/index.ts:47` enregistre la génération vidéo OpenAI.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/index.ts:194` enregistre la génération vidéo OpenRouter et les fournisseurs de catalogue vidéo.
- `/Users/kevinlin/code/openclaw/extensions/fal/index.ts:13` enregistre la génération vidéo fal.
- `/Users/kevinlin/code/openclaw/extensions/xai/index.ts:234` enregistre la génération vidéo xAI.
- `/Users/kevinlin/code/openclaw/extensions/runway/index.ts:4` enregistre la génération vidéo Runway.
- `/Users/kevinlin/code/openclaw/extensions/pixverse/index.ts:6` enregistre la génération vidéo PixVerse.
- `/Users/kevinlin/code/openclaw/extensions/together/index.ts:39` enregistre la génération vidéo Together.
- `/Users/kevinlin/code/openclaw/src/video-generation/runtime.ts:282` invoque les fournisseurs et valide les résultats vidéo retournés.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/video-generation-providers.live.test.ts:594` teste en direct les fournisseurs vidéo sélectionnés et les modes déclarés.
- `/Users/kevinlin/code/openclaw/scripts/test-live-media.ts:31` inclut les définitions de suite en direct du fournisseur vidéo.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/media-generation/provider-capabilities.contract.test.ts:4` répertorie les fournisseurs vidéo fournis attendus.
- `/Users/kevinlin/code/openclaw/src/media-generation/provider-capabilities.contract.test.ts:54` vérifie les manifestes des fournisseurs vidéo fournis.
- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.video-generation.test.ts:1` exerce la prise en charge de l'enregistrement d'outil vidéo partagé.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "video generation provider OpenRouter Runway fal xAI Sora" --json`

Résultats :

- N'a retourné aucun résultat direct pour la phrase exacte.

Requête : `gitcrawl search openclaw/openclaw --query "video generation" --json`

Résultats :

- A retourné #79535 sur la génération vidéo OpenRouter échouant silencieusement, #45655 sur les modèles de sortie image/vidéo acceptés dans la configuration mais échouant à l'exécution, #86279 sur le succès de la génération de médias par rapport à l'échec de livraison et #77700 sur la migration de résolution d'exécution préparée pour les fournisseurs image/musique/vidéo.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "video generation OpenRouter Runway fal xAI Sora"`

Résultats :

- A trouvé un rapport de saut de fournisseur couvrant fal, Google, MiniMax, OpenAI, Runway, xAI, OpenRouter, BytePlus, Qwen, Alibaba, DeepInfra et Vydra lorsque les entrées audio de référence n'étaient pas prises en charge.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "video_generate"`

Résultats :

- A trouvé une discussion du responsable sur la découverte d'outil différée et le comportement d'aperçu de l'outil multimédia.
