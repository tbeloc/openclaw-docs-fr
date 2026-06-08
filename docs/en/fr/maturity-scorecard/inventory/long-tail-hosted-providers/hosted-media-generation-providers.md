---
title: "Long-tail hosted providers - Hosted Media Providers Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Long-tail hosted providers - Hosted Media Providers Maturity Note

## Résumé

Les fournisseurs de génération de médias hébergés sont en Beta pour la couverture et en Alpha pour la qualité.
La source dispose de contrats partagés solides et de balayages en direct pour les fournisseurs d'images, de vidéos et de musique,
mais la latence de file d'attente spécifique au fournisseur, l'interrogation des opérations,
les exigences de médias distants et la variance d'accès aux modèles maintiennent l'implémentation
en dessous de la qualité Beta.

## Portée de la catégorie

Inclus dans cette catégorie :

- Fournisseurs de génération d'images : Couvre les fournisseurs de génération d'images sur les chemins de fournisseurs de génération d'images, de vidéos et de musique hébergés, y compris DeepInfra et les comportements des fournisseurs de génération de médias hébergés connexes.
- Fournisseurs de génération de vidéos : Couvre les fournisseurs de génération de vidéos sur les chemins de fournisseurs de génération d'images, de vidéos et de musique hébergés, y compris DeepInfra et les comportements des fournisseurs de génération de médias hébergés connexes.
- Fournisseurs de génération de musique : Couvre les fournisseurs de génération de musique sur les chemins de fournisseurs de génération d'images, de vidéos et de musique hébergés, y compris DeepInfra et les comportements des fournisseurs de génération de médias hébergés connexes.
- Couverture du mode média : Couvre la couverture du mode média sur les chemins de fournisseurs de génération d'images, de vidéos et de musique hébergés, y compris DeepInfra et les comportements des fournisseurs de génération de médias hébergés connexes.
- Fournisseurs de synthèse vocale : Couvre les fournisseurs de synthèse vocale sur les chemins de synthèse vocale, de reconnaissance vocale, de transcription en temps réel, d'audio téléphonique et les comportements des fournisseurs de parole, de transcription et d'audio hébergés connexes.
- Fournisseurs de reconnaissance vocale : Couvre les fournisseurs de reconnaissance vocale sur les chemins de synthèse vocale, de reconnaissance vocale, de transcription en temps réel, d'audio téléphonique et les comportements des fournisseurs de parole, de transcription et d'audio hébergés connexes.
- Fournisseurs de transcription en temps réel : Couvre les fournisseurs de transcription en temps réel sur les chemins de synthèse vocale, de reconnaissance vocale, de transcription en temps réel, d'audio téléphonique et les comportements des fournisseurs de parole, de transcription et d'audio hébergés connexes.
- Diagnostics de format audio : Couvre les diagnostics de format audio sur les chemins de synthèse vocale, de reconnaissance vocale, de transcription en temps réel, d'audio téléphonique et les comportements des fournisseurs de parole, de transcription et d'audio hébergés connexes.

## Fonctionnalités

- Fournisseurs de génération d'images : Couvre les fournisseurs de génération d'images sur les chemins de fournisseurs de génération d'images, de vidéos et de musique hébergés, y compris DeepInfra et les comportements des fournisseurs de génération de médias hébergés connexes.
- Fournisseurs de génération de vidéos : Couvre les fournisseurs de génération de vidéos sur les chemins de fournisseurs de génération d'images, de vidéos et de musique hébergés, y compris DeepInfra et les comportements des fournisseurs de génération de médias hébergés connexes.
- Fournisseurs de génération de musique : Couvre les fournisseurs de génération de musique sur les chemins de fournisseurs de génération d'images, de vidéos et de musique hébergés, y compris DeepInfra et les comportements des fournisseurs de génération de médias hébergés connexes.
- Couverture du mode média : Couvre la couverture du mode média sur les chemins de fournisseurs de génération d'images, de vidéos et de musique hébergés, y compris DeepInfra et les comportements des fournisseurs de génération de médias hébergés connexes.
- Fournisseurs de synthèse vocale : Couvre les fournisseurs de synthèse vocale sur les chemins de synthèse vocale, de reconnaissance vocale, de transcription en temps réel, d'audio téléphonique et les comportements des fournisseurs de parole, de transcription et d'audio hébergés connexes.
- Fournisseurs de reconnaissance vocale : Couvre les fournisseurs de reconnaissance vocale sur les chemins de synthèse vocale, de reconnaissance vocale, de transcription en temps réel, d'audio téléphonique et les comportements des fournisseurs de parole, de transcription et d'audio hébergés connexes.
- Fournisseurs de transcription en temps réel : Couvre les fournisseurs de transcription en temps réel sur les chemins de synthèse vocale, de reconnaissance vocale, de transcription en temps réel, d'audio téléphonique et les comportements des fournisseurs de parole, de transcription et d'audio hébergés connexes.
- Diagnostics de format audio : Couvre les diagnostics de format audio sur les chemins de synthèse vocale, de reconnaissance vocale, de transcription en temps réel, d'audio téléphonique et les comportements des fournisseurs de parole, de transcription et d'audio hébergés connexes.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (70%)`
- Signaux positifs :
  - Les docs de manifeste définissent les contrats des fournisseurs de génération d'images, de vidéos et de musique et les métadonnées de génération statiques.
  - Les docs de test en direct décrivent les suites en direct d'images, de musique et de vidéo ainsi qu'un harnais média combiné.
  - Les cas en direct de génération de vidéos couvrent Alibaba, BytePlus, DeepInfra, fal, MiniMax, OpenRouter, PixVerse, Qwen, Runway, Together, Vydra et xAI.
  - Les cas en direct de génération de musique couvrent fal, Google, MiniMax et OpenRouter.
  - Les docs en direct de génération d'images listent DeepInfra, fal, Google, MiniMax, OpenAI, OpenRouter, Vydra et xAI.
  - Des tests unitaires existent pour les fournisseurs de génération spécifiques au fournisseur.
- Signaux négatifs :
  - Les docs en direct partagés ignorent explicitement ou réduisent les fournisseurs/modes pour les exécutions sûres pour la version.
  - Certains fournisseurs nécessitent des URL distantes ou un accès spécifique au compte pour les chemins image-vers-vidéo ou vidéo-vers-vidéo.
  - Les recherches d'archives pour la phrase exacte media-provider ont retourné peu de preuves directes GitHub ou Discord.

## Score de qualité

- Score : `Alpha (64%)`
- Bonnes qualités :
  - Les métadonnées du fournisseur de génération gardent les signaux d'authentification bon marché et de disponibilité en dehors du code d'exécution uniquement.
  - Les chemins de fournisseur partagés exposent les filtres de fournisseur, les cartes de modèles env, les contrôles de délai d'expiration des opérations et les options de clé de profil.
  - Le comportement d'exécution de la génération de vidéos est structuré autour des limites d'opération par fournisseur plutôt qu'une exécution agrégée unique non bornée.
  - Les docs du harnais média sont explicites sur les fournisseurs ignorés, la couverture Vydra spécifique au fournisseur et les contraintes de mode connues.
- Mauvaises qualités :
  - Les fournisseurs de génération de médias ont une sémantique d'opération coûteuse, lente, soutenue par une file d'attente et spécifique au fournisseur.
  - Les exigences d'URL de médias distants et les portes d'accès aux modèles maintiennent la couverture du mode incohérente.
  - Le chemin de fumée sûr pour la version échange la largeur et la profondeur du mode pour l'exécution pratique.
- Exclus de la qualité :
  - Les preuves unitaires, d'intégration et en direct ont été utilisées uniquement pour le score de couverture.

## Score de complétude

- Score : `Beta (70%)`
- Instructions de surface : évaluées par rapport à `references/completeness/long-tail-hosted-providers.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les fournisseurs de génération d'images, les fournisseurs de génération de vidéos, les fournisseurs de génération de musique, la couverture du mode média, les fournisseurs de synthèse vocale, les fournisseurs de reconnaissance vocale, les fournisseurs de transcription en temps réel, les diagnostics de format audio.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter des tableaux de couverture des fournisseurs/modes générés pour les images, la musique et la vidéo.
- Ajouter des présets de fumée stables qui distinguent les chemins sûrs pour la version des balayages de mode exhaustifs.
- Ajouter un suivi soutenu par archive pour les défaillances du mode fournisseur, les délais d'expiration de la file d'attente et les limites d'accès spécifiques au compte.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:196` : les métadonnées du fournisseur de génération décrivent les signaux d'authentification statiques avant le chargement du runtime.
- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:204` : le comportement de génération réel reste dans le runtime du plugin.
- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:630` : les contrats statiques incluent les listes de fournisseurs de génération d'images, vidéos et musique.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:466` : le nom des docs en direct de génération d'images `test/image-generation.runtime.live.test.ts`.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:478` : les fournisseurs de génération d'images actuellement fournis incluent DeepInfra, fal, Google, MiniMax, OpenAI, OpenRouter, Vydra et xAI.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:512` : le nom des docs en direct de génération de musique `extensions/music-generation-providers.live.test.ts`.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:536` : le nom des docs en direct de génération vidéo `extensions/video-generation-providers.live.test.ts`.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:541` : la portée vidéo en direct exerce le chemin du fournisseur vidéo partagé fourni.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:552` : les docs listent les fournisseurs image-vers-vidéo déclarés mais ignorés et la couverture Vydra spécifique au fournisseur.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:571` : le harnais média en direct exécute les suites d'images, de musique et de vidéo via un seul point d'entrée.

## Source

- `/Users/kevinlin/code/openclaw/extensions/fal/openclaw.plugin.json:2` : fal est fourni en tant que plugin de fournisseur de génération.
- `/Users/kevinlin/code/openclaw/extensions/runway/openclaw.plugin.json:2` : Runway est fourni en tant que plugin de fournisseur vidéo.
- `/Users/kevinlin/code/openclaw/extensions/pixverse/openclaw.plugin.json:2` : PixVerse est fourni en tant que plugin de fournisseur vidéo.
- `/Users/kevinlin/code/openclaw/extensions/vydra/openclaw.plugin.json:2` : Vydra est fourni en tant que plugin de fournisseur de génération.
- `/Users/kevinlin/code/openclaw/extensions/comfy/openclaw.plugin.json:2` : Comfy est fourni avec les métadonnées du fournisseur de génération.
- `/Users/kevinlin/code/openclaw/extensions/deepinfra/openclaw.plugin.json:2` : DeepInfra est fourni avec les métadonnées du fournisseur d'images/vidéos hébergées.
- `/Users/kevinlin/code/openclaw/extensions/xai/openclaw.plugin.json:2` : xAI est fourni avec les métadonnées de génération d'images/vidéos hébergées.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/video-generation-providers.live.test.ts:45` : la suite vidéo en direct partagée importe les plugins Alibaba, BytePlus, DeepInfra, fal, Google, MiniMax, OpenAI, OpenRouter, PixVerse, Qwen, Runway, Together, Vydra et xAI.
- `/Users/kevinlin/code/openclaw/extensions/video-generation-providers.live.test.ts:61` : la suite vidéo en direct se verrouille sur l'env live-test et les filtres de fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/video-generation-providers.live.test.ts:97` : les cas vidéo en direct énumèrent les fournisseurs vidéo hébergés.
- `/Users/kevinlin/code/openclaw/extensions/video-generation-providers.live.test.ts:594` : la suite vidéo en direct exécute un cas par fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/music-generation-providers.live.test.ts:33` : la suite musique en direct importe les plugins fal, Google, MiniMax et OpenRouter.
- `/Users/kevinlin/code/openclaw/extensions/music-generation-providers.live.test.ts:53` : les cas musique en direct énumèrent fal, Google, MiniMax et OpenRouter.
- `/Users/kevinlin/code/openclaw/extensions/music-generation-providers.live.test.ts:170` : la suite musique en direct couvre la génération plus les chemins d'édition déclarés avec l'authentification shell/profile.
- `/Users/kevinlin/code/openclaw/extensions/vydra/vydra.live.test.ts:42` : le test en direct Vydra couvre la génération d'images.
- `/Users/kevinlin/code/openclaw/extensions/vydra/vydra.live.test.ts:77` : le test en direct Vydra couvre la génération vidéo.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/fal/image-generation-provider.test.ts` : couverture unitaire pour la génération d'images fal.
- `/Users/kevinlin/code/openclaw/extensions/runway/video-generation-provider.test.ts` : couverture unitaire pour la génération vidéo Runway.
- `/Users/kevinlin/code/openclaw/extensions/pixverse/video-generation-provider.test.ts` : couverture unitaire pour la génération vidéo PixVerse.
- `/Users/kevinlin/code/openclaw/extensions/vydra/image-generation-provider.test.ts` : couverture unitaire pour la génération d'images Vydra.
- `/Users/kevinlin/code/openclaw/extensions/vydra/video-generation-provider.test.ts` : couverture unitaire pour la génération vidéo Vydra.
- `/Users/kevinlin/code/openclaw/extensions/deepinfra/video-generation-provider.test.ts` : couverture unitaire pour la génération vidéo DeepInfra.
- `/Users/kevinlin/code/openclaw/extensions/qwen/video-generation-provider.test.ts` : couverture unitaire pour la génération vidéo Qwen.
- `/Users/kevinlin/code/openclaw/extensions/together/video-generation-provider.test.ts` : couverture unitaire pour la génération vidéo Together.
- `/Users/kevinlin/code/openclaw/extensions/minimax/music-generation-provider.test.ts` : couverture unitaire pour la génération de musique MiniMax.

## Requêtes Gitcrawl

- `gitcrawl --json search issues -R openclaw/openclaw "fal Runway Pixverse Vydra image video generation provider"` a retourné `[]`.
- `gitcrawl --json search prs -R openclaw/openclaw "fal Runway Pixverse Vydra image video generation provider"` a retourné `[]`.
- La requête d'aide `StepFun image_generation provider catalog` a trouvé #86493, le fournisseur de texte du plan StepFun n'enregistre pas le fournisseur de génération d'images.
- La requête d'aide `OpenRouter video generation music provider registry` a trouvé #79535, lacunes du registre vidéo/musique OpenRouter.

## Requêtes Discrawl

- `env DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search "fal Runway Pixverse Vydra video generation provider" --limit 5` a retourné `null`.
- La requête d'aide `StepFun provider registry image_generation provider catalog` n'a retourné aucun résultat Discord direct.
- Ce faible taux de résultats d'archive est traité comme neutre, non comme preuve de qualité.
