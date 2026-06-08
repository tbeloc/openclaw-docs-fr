---
title: "Chemin du fournisseur OpenRouter - Note de maturité de la génération de médias et de la parole"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur OpenRouter - Note de maturité de la génération de médias et de la parole

## Résumé

Le support des médias OpenRouter est large : la génération d'images, la génération de vidéos, la génération de musique, la synthèse vocale, la transcription vocale/compréhension des médias et les métadonnées du contrat du fournisseur sont tous enregistrés dans le plugin fourni et documentés. La couverture est Beta car les tests du fournisseur exercent la mise en forme des requêtes, l'interrogation, les en-têtes, l'authentification, les catalogues de modèles et l'enregistrement à l'exécution, mais la preuve en direct est inégale et le comportement des outils varie selon le modèle.

La qualité est Alpha car l'archive contient des rapports actifs/récents selon lesquels la génération de vidéos OpenRouter a échoué silencieusement, la musique n'avait pas été livrée dans une fenêtre de rapport, et les examens du transport de la parole/du fournisseur ont trouvé des problèmes de garde-fou et de SecretRef.

## Portée de la catégorie

Inclus dans cette catégorie :

- route image_generate OpenRouter : Couvre la route image_generate OpenRouter sur les comportements d'image, vidéo, musique, TTS et comportements d'image, vidéo, musique et parole connexes OpenRouter.
- travaux asynchrones video_generate/interrogation/téléchargement : Couvre les travaux asynchrones video_generate/interrogation/téléchargement sur les comportements d'image, vidéo, musique, TTS et comportements d'image, vidéo, musique et parole connexes OpenRouter.
- route audio music_generate : Couvre la route audio music_generate sur les comportements d'image, vidéo, musique, TTS et comportements d'image, vidéo, musique et parole connexes OpenRouter.
- Synthèse vocale : Couvre la synthèse vocale sur les comportements d'image, vidéo, musique, TTS et comportements d'image, vidéo, musique et parole connexes OpenRouter.
- Transcription parole-texte : Couvre la transcription parole-texte sur les comportements d'image, vidéo, musique, TTS et comportements d'image, vidéo, musique et parole connexes OpenRouter.
- Compréhension des médias entrants : Couvre la compréhension des médias entrants sur les comportements d'image, vidéo, musique, TTS et comportements d'image, vidéo, musique et parole connexes OpenRouter.
- Livraison d'artefacts générés : Couvre la livraison d'artefacts générés sur les comportements d'image, vidéo, musique, TTS et comportements d'image, vidéo, musique et parole connexes OpenRouter.

## Fonctionnalités

- route image_generate OpenRouter : Couvre la route image_generate OpenRouter sur les comportements d'image, vidéo, musique, TTS et comportements d'image, vidéo, musique et parole connexes OpenRouter.
- travaux asynchrones video_generate/interrogation/téléchargement : Couvre les travaux asynchrones video_generate/interrogation/téléchargement sur les comportements d'image, vidéo, musique, TTS et comportements d'image, vidéo, musique et parole connexes OpenRouter.
- route audio music_generate : Couvre la route audio music_generate sur les comportements d'image, vidéo, musique, TTS et comportements d'image, vidéo, musique et parole connexes OpenRouter.
- Synthèse vocale : Couvre la synthèse vocale sur les comportements d'image, vidéo, musique, TTS et comportements d'image, vidéo, musique et parole connexes OpenRouter.
- Transcription parole-texte : Couvre la transcription parole-texte sur les comportements d'image, vidéo, musique, TTS et comportements d'image, vidéo, musique et parole connexes OpenRouter.
- Compréhension des médias entrants : Couvre la compréhension des médias entrants sur les comportements d'image, vidéo, musique, TTS et comportements d'image, vidéo, musique et parole connexes OpenRouter.
- Livraison d'artefacts générés : Couvre la livraison d'artefacts générés sur les comportements d'image, vidéo, musique, TTS et comportements d'image, vidéo, musique et parole connexes OpenRouter.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (72%)`
- Signaux positifs : Les tests du fournisseur de médias OpenRouter couvrent la génération d'images, la découverte de modèles vidéo, les travaux vidéo et les téléchargements, la génération de musique, la parole, la STT/compréhension des médias, les en-têtes, l'authentification et l'enregistrement des plugins.
- Signaux négatifs : C'est une surface large avec un comportement spécifique au modèle et moins de fumées en direct/version que l'inférence de texte ; les chemins vidéo/musique sont plus récents et plus dépendants en amont.
- Lacunes d'intégration : Ajouter des fumées de médias en direct pour un modèle d'image, un modèle vidéo, un modèle musique, un modèle TTS et un modèle STT, plus une vérification de livraison passerelle/canal pour chaque type d'artefact généré.

## Score de qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl : La requête OpenRouter large a retourné #79535, « La génération de vidéos OpenRouter échoue silencieusement ; la génération de musique n'a jamais été livrée », et #83030 demandant le support de la famille de modèles ReCraft d'image via OpenRouter.
- Rapports Discrawl : La recherche Discord a trouvé des commentaires d'examen PR pour les ajouts de fournisseur d'image/vidéo/musique OpenRouter, y compris les problèmes de garde-fou de transport de parole et de SecretRef.
- Bonnes qualités : Le manifeste du plugin déclare les contrats de médias OpenRouter et les métadonnées du fournisseur ; la documentation couvre la configuration d'image, vidéo, musique, TTS et STT dans une page de fournisseur.
- Mauvaises qualités : Les points de terminaison des médias diffèrent considérablement de l'inférence de texte, avec interrogation vidéo asynchrone, charges utiles d'image/audio de complétions de chat, points de terminaison de parole et support de paramètres spécifiques au modèle.
- Exclu de la qualité : L'étendue des tests du fournisseur et les tests de contrat du fournisseur de médias sont des entrées de couverture uniquement.

## Score de complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openrouter-provider-path.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la route image_generate OpenRouter, les travaux asynchrones video_generate/interrogation/téléchargement, la route audio music_generate, la transcription parole-texte, la compréhension des médias entrants, la livraison d'artefacts générés.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'étendue des fonctionnalités de médias dépasse la preuve en direct stable sur tous les modes de médias.
- La génération de vidéos est asynchrone et dépend de la sémantique du statut/contenu du travail OpenRouter.
- Le comportement du transport/authentification de la parole et de la compréhension des médias a des exigences de politique réseau plus sensibles à la sécurité que les simples complétions de chat.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/openrouter.md` documente la génération d'images OpenRouter, la génération de vidéos, la génération de musique, la synthèse vocale et la transcription vocale/compréhension des médias.
- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md` documente la sélection de modèles d'images OpenRouter, la clé API, le support des images d'entrée, les délais d'expiration, l'édition et les conseils d'images Gemini.
- `/Users/kevinlin/code/openclaw/docs/tools/music-generation.md` documente la génération de musique Lyria OpenRouter et le support d'édition.
- `/Users/kevinlin/code/openclaw/docs/tools/media-overview.md` répertorie la couverture des capacités de médias OpenRouter.

### Source

- `/Users/kevinlin/code/openclaw/extensions/openrouter/index.ts` enregistre la compréhension des médias OpenRouter, la génération d'images, la génération de musique, la génération de vidéos, le catalogue de modèles vidéo et les fournisseurs de parole.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/image-generation-provider.ts` implémente la génération d'images de complétions de chat OpenRouter.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/video-generation-provider.ts` et `/Users/kevinlin/code/openclaw/extensions/openrouter/video-http.ts` implémentent le comportement de soumission de travaux vidéo OpenRouter, d'interrogation et de téléchargement.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/music-generation-provider.ts` implémente la génération audio de complétions de chat OpenRouter.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/speech-provider.ts` et `/Users/kevinlin/code/openclaw/extensions/openrouter/media-understanding-provider.ts` implémentent les chemins de parole et de STT/compréhension des médias.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/video-generation/runtime.test.ts` couvre l'utilisation à l'exécution des fournisseurs de génération de vidéos OpenRouter.
- `/Users/kevinlin/code/openclaw/src/media-understanding/runner.vision-skip.test.ts` couvre le comportement du coureur de compréhension des médias OpenRouter.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/openrouter.live.test.ts` contrôle en direct le côté texte/catalogue du fournisseur ; la couverture en direct des médias est moins visible.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/openrouter/image-generation-provider.test.ts` couvre la mise en forme des requêtes d'images OpenRouter, les en-têtes, l'authentification et le comportement du modèle.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/video-generation-provider.test.ts` couvre la découverte de modèles vidéo, les URL de base personnalisées, la soumission de travaux, l'interrogation, le téléchargement, l'URL de rappel et les en-têtes d'authentification.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/music-generation-provider.test.ts` couvre la mise en forme des requêtes de musique et la gestion de la sortie audio.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/speech-provider.test.ts` couvre la configuration de la parole, la normalisation de l'URL de base, l'authentification, les en-têtes et l'URL de requête.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/media-understanding-provider.test.ts` couvre les métadonnées du fournisseur STT/compréhension des médias, l'authentification, les en-têtes, les charges utiles et la sélection d'URL.
- `/Users/kevinlin/code/openclaw/src/media-generation/provider-capabilities.contract.test.ts` couvre les déclarations de capacité du fournisseur y compris OpenRouter.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OpenRouter image video music speech provider openrouter"`

Résultats :

- N'a retourné aucun résultat direct pour la phrase exacte.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OpenRouter"`

Résultats :

- A retourné #79535 sur l'échec silencieux de la génération de vidéos OpenRouter et la non-livraison de la génération de musique dans ce rapport, plus #83030 pour le support de la famille de modèles ReCraft d'image OpenRouter.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "openrouter add image video music generation providers"`

Résultats :

- N'a retourné aucun résultat direct pour la phrase exacte, tandis que l'archive Discord référence la PR #64513 pour l'ajout du fournisseur de médias.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "OpenRouter image generation music video speech"`

Résultats :

- A trouvé des commentaires d'examen PR d'avril 2026 pour `openrouter: add image, video, and music generation providers`, y compris les conclusions pour normaliser les clés API de parole comme entrée secrète, utiliser le transport gardé pour la diffusion en continu de parole et corriger un échec de simulation de test de parole.
