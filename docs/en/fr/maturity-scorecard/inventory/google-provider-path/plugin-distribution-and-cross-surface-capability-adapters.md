---
title: "Chemin du fournisseur Google - Note de maturité Media, Search et Realtime"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur Google - Note de maturité Media, Search et Realtime

## Résumé

Le plugin Google est largement distribué et enregistre plus que le chemin du modèle texte : génération d'images, compréhension des médias, intégration de mémoire, génération de musique, voix en temps réel, parole/TTS, génération vidéo et recherche web. La couverture est Stable car la documentation, le manifeste, l'enregistrement du fournisseur, les tests en direct et de nombreux tests unitaires d'adaptateur couvrent la surface. La qualité est Stable à la limite partagée car le code de l'adaptateur est explicite et appartient au fournisseur, mais la surface est fragmentée sur de nombreuses capacités et les recherches d'archives n'ont pas produit un seul fil de qualité d'adaptateur consolidé.

## Portée de la catégorie

Inclus dans cette catégorie :

- Distribution du plugin groupé : Couvre la distribution du plugin groupé dans le package `@openclaw/google-plugin` groupé, la distribution du manifeste du plugin, les métadonnées d'activation automatique, l'enregistrement de la capacité-fournisseur et le comportement des adaptateurs de plugin google associés.
- Métadonnées d'activation automatique du fournisseur : Couvre les métadonnées d'activation automatique du fournisseur dans le package `@openclaw/google-plugin` groupé, la distribution du manifeste du plugin, les métadonnées d'activation automatique, l'enregistrement de la capacité-fournisseur et le comportement des adaptateurs de plugin google associés.
- Adaptateurs d'image et de médias : Couvre les adaptateurs d'image et de médias dans le package `@openclaw/google-plugin` groupé, la distribution du manifeste du plugin, les métadonnées d'activation automatique, l'enregistrement de la capacité-fournisseur et le comportement des adaptateurs de plugin google associés.
- Adaptateurs de parole et temps réel : Couvre les adaptateurs de parole et temps réel dans le package `@openclaw/google-plugin` groupé, la distribution du manifeste du plugin, les métadonnées d'activation automatique, l'enregistrement de la capacité-fournisseur et le comportement des adaptateurs de plugin google associés.
- Outils de recherche et de génération : Couvre les outils de recherche et de génération dans le package `@openclaw/google-plugin` groupé, la distribution du manifeste du plugin, les métadonnées d'activation automatique, l'enregistrement de la capacité-fournisseur et le comportement des adaptateurs de plugin google associés.
- Sessions de voix en temps réel : Couvre les sessions de voix en temps réel dans le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket du navigateur contraint, la mise en file d'attente audio et le comportement gemini live talk associé.
- Jetons de navigateur contraint : Couvre les jetons de navigateur contraint dans le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket du navigateur contraint, la mise en file d'attente audio et le comportement gemini live talk associé.
- Événements audio et transcription : Couvre les événements audio et transcription dans le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket du navigateur contraint, la mise en file d'attente audio et le comportement gemini live talk associé.
- Appels d'outils en direct : Couvre les appels d'outils en direct dans le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket du navigateur contraint, la mise en file d'attente audio et le comportement gemini live talk associé.
- Reconnexions de session : Couvre les reconnexions de session dans le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket du navigateur contraint, la mise en file d'attente audio et le comportement gemini live talk associé.

## Fonctionnalités

- Distribution du plugin groupé : Couvre la distribution du plugin groupé dans le package `@openclaw/google-plugin` groupé, la distribution du manifeste du plugin, les métadonnées d'activation automatique, l'enregistrement de la capacité-fournisseur et le comportement des adaptateurs de plugin google associés.
- Métadonnées d'activation automatique du fournisseur : Couvre les métadonnées d'activation automatique du fournisseur dans le package `@openclaw/google-plugin` groupé, la distribution du manifeste du plugin, les métadonnées d'activation automatique, l'enregistrement de la capacité-fournisseur et le comportement des adaptateurs de plugin google associés.
- Adaptateurs d'image et de médias : Couvre les adaptateurs d'image et de médias dans le package `@openclaw/google-plugin` groupé, la distribution du manifeste du plugin, les métadonnées d'activation automatique, l'enregistrement de la capacité-fournisseur et le comportement des adaptateurs de plugin google associés.
- Adaptateurs de parole et temps réel : Couvre les adaptateurs de parole et temps réel dans le package `@openclaw/google-plugin` groupé, la distribution du manifeste du plugin, les métadonnées d'activation automatique, l'enregistrement de la capacité-fournisseur et le comportement des adaptateurs de plugin google associés.
- Outils de recherche et de génération : Couvre les outils de recherche et de génération dans le package `@openclaw/google-plugin` groupé, la distribution du manifeste du plugin, les métadonnées d'activation automatique, l'enregistrement de la capacité-fournisseur et le comportement des adaptateurs de plugin google associés.
- Sessions de voix en temps réel : Couvre les sessions de voix en temps réel dans le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket du navigateur contraint, la mise en file d'attente audio et le comportement gemini live talk associé.
- Jetons de navigateur contraint : Couvre les jetons de navigateur contraint dans le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket du navigateur contraint, la mise en file d'attente audio et le comportement gemini live talk associé.
- Événements audio et transcription : Couvre les événements audio et transcription dans le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket du navigateur contraint, la mise en file d'attente audio et le comportement gemini live talk associé.
- Appels d'outils en direct : Couvre les appels d'outils en direct dans le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket du navigateur contraint, la mise en file d'attente audio et le comportement gemini live talk associé.
- Reconnexions de session : Couvre les reconnexions de session dans le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket du navigateur contraint, la mise en file d'attente audio et le comportement gemini live talk associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (83%)`
- Signaux positifs : Le package du plugin, le manifeste, la référence de documentation, l'enregistrement de la capacité, les tests Google en direct et les tests unitaires spécifiques à l'adaptateur couvrent un large ensemble de surfaces Google.
- Signaux négatifs : La preuve de capacité est fragmentée sur de nombreux adaptateurs plutôt que sur une seule matrice de version.
- Lacunes d'intégration : Les preuves d'archive et de test sont plus fortes par adaptateur que pour le plugin groupé en tant que produit multi-surface.

## Score de qualité

- Score : `Stable (80%)`
- Rapports Gitcrawl : Les recherches exactes de problèmes et de PR pour `google plugin provider image generation web search speech` n'ont retourné aucun résultat direct.
- Rapports Discrawl : `@openclaw/google-plugin capability adapters` n'a retourné aucun résultat ; `Google Gemini web search image generation provider` a retourné un fil de support custom-provider/openrouter adjacent mais aucun défaut d'adaptateur Google groupé direct.
- Bonnes qualités : Le plugin utilise un manifeste, l'enregistrement lazy appartenant au fournisseur, des contrats de capacité explicites, la gestion des identifiants de secours et les fichiers source locaux à l'adaptateur au lieu d'une implémentation Google monolithique.
- Mauvaises qualités : La surface du produit est répartie sur de nombreux adaptateurs de capacité, de sorte que la validation de version et le débogage des opérateurs peuvent devenir fragmentés.
- Exclus de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel ; ceux-ci sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Stable (83%)`
- Instructions de surface : évaluées par rapport à `references/completeness/google-provider-path.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la distribution du plugin groupé, les métadonnées d'activation automatique du fournisseur, les adaptateurs d'image et de médias, les adaptateurs de parole et temps réel, les outils de recherche et de génération, les sessions de voix en temps réel, les jetons de navigateur contraint, les événements audio et transcription, les appels d'outils en direct, les reconnexions de session.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucune matrice d'adaptateur Google unique n'a été trouvée qui prouve toutes les capacités groupées ensemble.
- La documentation de l'adaptateur Google est divisée entre la page du fournisseur et la référence du plugin.
- Les identifiants spécifiques à la capacité et les valeurs par défaut du modèle peuvent dériver indépendamment du chemin du fournisseur de texte direct.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/reference/google.md:8` documente
  le résumé du plugin Google et le package.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/google.md:19` liste
  les ID de fournisseur et les contrats de capacité pour le plugin Google.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:131` liste les capacités
  Google supportées, incluant le chat, l'image, la musique, la TTS, la voix en temps réel, la compréhension des médias, la recherche web, la réflexion et Gemma.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:194` documente la
  génération d'images.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:222` documente la
  génération de vidéos.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:250` documente la
  génération de musique.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:280` documente la TTS.

## Source

- `/Users/kevinlin/code/openclaw/extensions/google/package.json:2` déclare le
  package `@openclaw/google-plugin`.
- `/Users/kevinlin/code/openclaw/extensions/google/package.json:14` déclare le
  point d'entrée de l'extension OpenClaw.
- `/Users/kevinlin/code/openclaw/extensions/google/openclaw.plugin.json:1`
  déclare l'ID du plugin `google`, l'activation par défaut, les fournisseurs, l'entrée du catalogue et les métadonnées d'activation automatique.
- `/Users/kevinlin/code/openclaw/extensions/google/index.ts:38` définit les
  importations lazy pour les fournisseurs d'image, de médias, de musique, en temps réel, de parole, de vidéo et de recherche web.
- `/Users/kevinlin/code/openclaw/extensions/google/index.ts:337` enregistre les
  capacités du plugin Google auprès du registre de plugins.
- `/Users/kevinlin/code/openclaw/extensions/google/src/gemini-web-search-provider.ts:129`
  définit les variables d'environnement de recherche web Google.
- `/Users/kevinlin/code/openclaw/extensions/google/embedding-provider.ts`
  implémente le support d'intégration de mémoire Google.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/google/google.live.test.ts:58`
  teste en direct les chemins TTS/transcription audio/recherche web Google lorsque les tests en direct sont activés.
- `/Users/kevinlin/code/openclaw/extensions/google/google.live.test.ts:152`
  teste en direct le repli de configuration du fournisseur de modèle de recherche web.
- `/Users/kevinlin/code/openclaw/test/image-generation.infer-cli.live.test.ts:24`
  exécute la génération d'images Google en direct via une référence de modèle Google.
- `/Users/kevinlin/code/openclaw/scripts/dev/realtime-talk-live-smoke.ts:340`
  teste la configuration du websocket du navigateur Google Live.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/google/image-generation-provider.test.ts:126`
  couvre le comportement des requêtes de génération d'images Google.
- `/Users/kevinlin/code/openclaw/extensions/google/media-understanding-provider.video.test.ts`
  couvre le comportement vidéo de la compréhension des médias Google.
- `/Users/kevinlin/code/openclaw/extensions/google/speech-provider.test.ts`
  couvre le comportement de la parole/TTS Google.
- `/Users/kevinlin/code/openclaw/extensions/google/music-generation-provider.test.ts:53`
  couvre le comportement du fournisseur de génération de musique Google.
- `/Users/kevinlin/code/openclaw/extensions/google/video-generation-provider.test.ts`
  couvre le comportement du fournisseur de génération de vidéo Google.
- `/Users/kevinlin/code/openclaw/extensions/google/web-search-provider.test.ts:88`
  couvre les diagnostics de recherche web Google et le repli des identifiants.
- `/Users/kevinlin/code/openclaw/extensions/google/embedding-provider.test.ts:126`
  couvre la normalisation du modèle d'intégration Gemini.

## Requêtes Gitcrawl

Requête : `gitcrawl search issues "google plugin provider image generation web search speech" -R openclaw/openclaw --state all`

Résultats :

- Aucun résultat direct de problème retourné.

Requête : `gitcrawl search prs "google plugin provider image generation web search speech" -R openclaw/openclaw --state all`

Résultats :

- Aucun résultat direct de demande de tirage retourné.

## Requêtes Discrawl

Requête : `discrawl search --limit 5 "@openclaw/google-plugin capability adapters"`

Résultats :

- Aucun résultat retourné.

Requête : `discrawl search --limit 5 "Google Gemini web search image generation provider"`

Résultats :

- Un fil de support personnalisé custom-provider/openrouter adjacent a été retourné, mais aucun défaut d'adaptateur Google groupé direct.
