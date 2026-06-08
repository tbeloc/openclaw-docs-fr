---
title: "Compréhension des médias et génération de médias - Note de maturité de la génération de médias"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Compréhension des médias et génération de médias - Note de maturité de la génération de médias

## Résumé

La génération d'images a une surface utilisateur d'apparence mature : documentation publique, nombreux fournisseurs, livraison de session asynchrone, actions de statut/liste, édition d'images de référence, normalisation des capacités des fournisseurs et enregistrement des fournisseurs SDK. La qualité est limitée par la variance d'authentification des fournisseurs, les problèmes de routage OAuth Codex, le couplage de la livraison d'achèvement et la dérive des capacités du modèle/fournisseur.

## Portée de la catégorie

Inclus dans cette catégorie :

- Invocation de l'outil de génération d'images : Couvre l'invocation de l'outil de génération d'images sur `image_generate`, la sélection de modèle, l'enregistrement des fournisseurs, l'énumération des capacités des fournisseurs et le comportement de routage associé de l'outil de génération d'images et des fournisseurs.
- Sélection du fournisseur et du modèle : Couvre la sélection du fournisseur et du modèle sur `image_generate`, la sélection de modèle, l'enregistrement des fournisseurs, l'énumération des capacités des fournisseurs et le comportement de routage associé de l'outil de génération d'images et des fournisseurs.
- Édition d'images de référence : Couvre l'édition d'images de référence sur `image_generate`, la sélection de modèle, l'enregistrement des fournisseurs, l'énumération des capacités des fournisseurs et le comportement de routage associé de l'outil de génération d'images et des fournisseurs.
- Cycle de vie des tâches d'images générées : Couvre le cycle de vie des tâches d'images générées sur `image_generate`, la sélection de modèle, l'enregistrement des fournisseurs, l'énumération des capacités des fournisseurs et le comportement de routage associé de l'outil de génération d'images et des fournisseurs.
- Persistance et livraison des images générées : Couvre la persistance et la livraison des images générées sur `image_generate`, la sélection de modèle, l'enregistrement des fournisseurs, l'énumération des capacités des fournisseurs et le comportement de routage associé de l'outil de génération d'images et des fournisseurs.
- Invocation de l'outil de génération de musique : Couvre l'invocation de l'outil de génération de musique sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées d'images de référence le cas échéant et le comportement de routage associé de l'outil de génération de musique et des fournisseurs.
- Sélection du fournisseur et du modèle : Couvre la sélection du fournisseur et du modèle sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées d'images de référence le cas échéant et le comportement de routage associé de l'outil de génération de musique et des fournisseurs.
- Contrôles de paroles, instrumental, durée et format : Couvre les contrôles de paroles, instrumental, durée et format sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées d'images de référence le cas échéant et le comportement de routage associé de l'outil de génération de musique et des fournisseurs.
- Entrées de référence le cas échéant : Couvre les entrées de référence le cas échéant sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées d'images de référence le cas échéant et le comportement de routage associé de l'outil de génération de musique et des fournisseurs.
- Cycle de vie des tâches musicales et statut des doublons : Couvre le cycle de vie des tâches musicales et le statut des doublons sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées d'images de référence le cas échéant et le comportement de routage associé de l'outil de génération de musique et des fournisseurs.
- Persistance et livraison de l'audio généré : Couvre la persistance et la livraison de l'audio généré sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées d'images de référence le cas échéant et le comportement de routage associé de l'outil de génération de musique et des fournisseurs.
- Invocation de l'outil de génération vidéo : Couvre l'invocation de l'outil de génération vidéo sur `video_generate`, la résolution de mode, les capacités des fournisseurs, les entrées d'images/vidéos/audio de référence et le comportement de routage associé de l'outil de génération vidéo et des fournisseurs.
- Sélection du mode et des capacités du fournisseur : Couvre la sélection du mode et des capacités du fournisseur sur `video_generate`, la résolution de mode, les capacités des fournisseurs, les entrées d'images/vidéos/audio de référence et le comportement de routage associé de l'outil de génération vidéo et des fournisseurs.
- Entrées d'images, vidéos et audio de référence : Couvre les entrées d'images, vidéos et audio de référence sur `video_generate`, la résolution de mode, les capacités des fournisseurs, les entrées d'images/vidéos/audio de référence et le comportement de routage associé de l'outil de génération vidéo et des fournisseurs.
- Validation des options du fournisseur : Couvre la validation des options du fournisseur sur `video_generate`, la résolution de mode, les capacités des fournisseurs, les entrées d'images/vidéos/audio de référence et le comportement de routage associé de l'outil de génération vidéo et des fournisseurs.
- Cycle de vie des tâches vidéo et statut : Couvre le cycle de vie des tâches vidéo et le statut sur `video_generate`, la résolution de mode, les capacités des fournisseurs, les entrées d'images/vidéos/audio de référence et le comportement de routage associé de l'outil de génération vidéo et des fournisseurs.
- Persistance et livraison des vidéos générées : Couvre la persistance et la livraison des vidéos générées sur `video_generate`, la résolution de mode, les capacités des fournisseurs, les entrées d'images/vidéos/audio de référence et le comportement de routage associé de l'outil de génération vidéo et des fournisseurs.

## Fonctionnalités

- Invocation de l'outil de génération d'images : Couvre l'invocation de l'outil de génération d'images sur `image_generate`, la sélection de modèle, l'enregistrement des fournisseurs, l'énumération des capacités des fournisseurs et le comportement de routage associé de l'outil de génération d'images et des fournisseurs.
- Sélection du fournisseur et du modèle : Couvre la sélection du fournisseur et du modèle sur `image_generate`, la sélection de modèle, l'enregistrement des fournisseurs, l'énumération des capacités des fournisseurs et le comportement de routage associé de l'outil de génération d'images et des fournisseurs.
- Édition d'images de référence : Couvre l'édition d'images de référence sur `image_generate`, la sélection de modèle, l'enregistrement des fournisseurs, l'énumération des capacités des fournisseurs et le comportement de routage associé de l'outil de génération d'images et des fournisseurs.
- Cycle de vie des tâches d'images générées : Couvre le cycle de vie des tâches d'images générées sur `image_generate`, la sélection de modèle, l'enregistrement des fournisseurs, l'énumération des capacités des fournisseurs et le comportement de routage associé de l'outil de génération d'images et des fournisseurs.
- Persistance et livraison des images générées : Couvre la persistance et la livraison des images générées sur `image_generate`, la sélection de modèle, l'enregistrement des fournisseurs, l'énumération des capacités des fournisseurs et le comportement de routage associé de l'outil de génération d'images et des fournisseurs.
- Invocation de l'outil de génération de musique : Couvre l'invocation de l'outil de génération de musique sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées d'images de référence le cas échéant et le comportement de routage associé de l'outil de génération de musique et des fournisseurs.
- Sélection du fournisseur et du modèle : Couvre la sélection du fournisseur et du modèle sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées d'images de référence le cas échéant et le comportement de routage associé de l'outil de génération de musique et des fournisseurs.
- Contrôles de paroles, instrumental, durée et format : Couvre les contrôles de paroles, instrumental, durée et format sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées d'images de référence le cas échéant et le comportement de routage associé de l'outil de génération de musique et des fournisseurs.
- Entrées de référence le cas échéant : Couvre les entrées de référence le cas échéant sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées d'images de référence le cas échéant et le comportement de routage associé de l'outil de génération de musique et des fournisseurs.
- Cycle de vie des tâches musicales et statut des doublons : Couvre le cycle de vie des tâches musicales et le statut des doublons sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées d'images de référence le cas échéant et le comportement de routage associé de l'outil de génération de musique et des fournisseurs.
- Persistance et livraison de l'audio généré : Couvre la persistance et la livraison de l'audio généré sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées d'images de référence le cas échéant et le comportement de routage associé de l'outil de génération de musique et des fournisseurs.
- Invocation de l'outil de génération vidéo : Couvre l'invocation de l'outil de génération vidéo sur `video_generate`, la résolution de mode, les capacités des fournisseurs, les entrées d'images/vidéos/audio de référence et le comportement de routage associé de l'outil de génération vidéo et des fournisseurs.
- Sélection du mode et des capacités du fournisseur : Couvre la sélection du mode et des capacités du fournisseur sur `video_generate`, la résolution de mode, les capacités des fournisseurs, les entrées d'images/vidéos/audio de référence et le comportement de routage associé de l'outil de génération vidéo et des fournisseurs.
- Entrées d'images, vidéos et audio de référence : Couvre les entrées d'images, vidéos et audio de référence sur `video_generate`, la résolution de mode, les capacités des fournisseurs, les entrées d'images/vidéos/audio de référence et le comportement de routage associé de l'outil de génération vidéo et des fournisseurs.
- Validation des options du fournisseur : Couvre la validation des options du fournisseur sur `video_generate`, la résolution de mode, les capacités des fournisseurs, les entrées d'images/vidéos/audio de référence et le comportement de routage associé de l'outil de génération vidéo et des fournisseurs.
- Cycle de vie des tâches vidéo et statut : Couvre le cycle de vie des tâches vidéo et le statut sur `video_generate`, la résolution de mode, les capacités des fournisseurs, les entrées d'images/vidéos/audio de référence et le comportement de routage associé de l'outil de génération vidéo et des fournisseurs.
- Persistance et livraison des vidéos générées : Couvre la persistance et la livraison des vidéos générées sur `video_generate`, la résolution de mode, les capacités des fournisseurs, les entrées d'images/vidéos/audio de référence et le comportement de routage associé de l'outil de génération vidéo et des fournisseurs.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs : La documentation couvre la configuration, les fournisseurs, la matrice de capacités, les paramètres, les secours, les délais d'expiration, l'édition d'images, les actions de statut/liste et les notes spécifiques aux fournisseurs. La source dispose de l'outil, du runtime, du registre des fournisseurs, du fournisseur compatible OpenAI, du cycle de vie des tâches en arrière-plan et des exportations SDK.
- Signaux négatifs : Le comportement en direct spécifique au fournisseur varie et la matrice des fournisseurs change rapidement ; pas tous les chemins des fournisseurs ont une preuve de scénario récurrent visible.
- Lacunes d'intégration : La preuve de livraison visible asynchrone est partagée avec le composant de livraison de médias et a des frictions d'archive connues.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : #76690 et #85797 montrent des incompatibilités de disponibilité OAuth/génération d'images Codex ; #86034/#86279 montrent que le succès des médias générés est confondu avec l'échec de la livraison ; #79360 demande d'exposer les ID d'images Responses pour les éditions itératives ; #86493/#86605 montrent des lacunes d'enregistrement des fournisseurs ; #84627 montre des problèmes de configuration SSRF/réseau privé xAI.
- Rapports Discrawl : Les rapports d'archive du responsable montrent le comportement de génération d'images OAuth Codex, l'ajustement des valeurs par défaut des délais d'expiration (#75337) et les préoccupations concernant la facturation accidentelle des API par rapport à OAuth. Les résultats plus larges de discrawl sur la génération de médias montrent des bogues de remise après le succès du fournisseur.
- Bonnes qualités : L'outil valide les limites de capacité difficiles, signale les remplacements ignorés, dispose d'actions de liste/statut, déduplique les tâches actives et bloque les URL distantes dans les contextes en bac à sable.
- Mauvaises qualités : La sélection de la source d'authentification du fournisseur et l'enregistrement du fournisseur restent faciles à mal configurer, et le résultat utilisateur de bout en bout dépend toujours de la livraison de messages asynchrones après que la génération réussisse.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/media-understanding-and-media-generation.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent l'étendue de la taxonomie pour l'invocation de l'outil de génération d'images, la sélection du fournisseur et du modèle, l'édition d'images de référence, le cycle de vie des tâches d'images générées, la persistance et la livraison des images générées, l'invocation de l'outil de génération musicale, la sélection du fournisseur et du modèle, les paroles, les contrôles instrumentaux, de durée et de format, les entrées de référence où supportées, le cycle de vie des tâches musicales et le statut des doublons, la persistance et la livraison de l'audio généré, l'invocation de l'outil de génération vidéo, la sélection du mode et des capacités du fournisseur, les entrées d'images, vidéos et audio de référence, la validation des options du fournisseur, le cycle de vie des tâches vidéo et le statut, la persistance et la livraison des vidéos générées.
- Signaux négatifs : la note archivée a précédé le score de complétude process-version-3, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les éditions d'images itératives manquent d'exposition de l'ID de génération retourné par le fournisseur dans le chemin d'outil public.
- Le routage OAuth/clé API reste une source de confusion et de bogues.
- Les capacités du fournisseur et les délais d'expiration par défaut nécessitent une maintenance continue à mesure que les API hébergées changent.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/image-generation.md` documente `image_generate`, le comportement des tâches asynchrones, la configuration du fournisseur, les capacités du fournisseur, l'édition d'images de référence, le comportement des délais d'expiration, la normalisation et les exemples.
- `/Users/kevinlin/code/openclaw/docs/tools/media-overview.md` énumère la génération d'images et les capacités du fournisseur.
- `/Users/kevinlin/code/openclaw/docs/tools/skills.md` et `/Users/kevinlin/code/openclaw/docs/tools/skills-config.md` conseillent d'utiliser le chemin `image_generate` principal pour la génération d'images de stock.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/tools/image-generate-tool.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/image-generate-tool.actions.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/image-generate-background.ts`
- `/Users/kevinlin/code/openclaw/src/image-generation/runtime.ts`
- `/Users/kevinlin/code/openclaw/src/image-generation/provider-registry.ts`
- `/Users/kevinlin/code/openclaw/src/image-generation/openai-compatible-image-provider.ts`
- `/Users/kevinlin/code/openclaw/src/image-generation/image-assets.ts`
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/image-generation.ts`
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/image-generation-core.ts`

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.image-generation.test.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/image-tool.providers.live.test.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/image-tool.ollama.live.test.ts`
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-subscribe.tools.media.test.ts`

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/tools/image-generate-tool.test.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/image-generate-tool.actions.ts` a le support statut/liste couvert par les tests d'outils à proximité.
- `/Users/kevinlin/code/openclaw/src/image-generation/runtime.test.ts`
- `/Users/kevinlin/code/openclaw/src/image-generation/provider-registry.test.ts`
- `/Users/kevinlin/code/openclaw/src/image-generation/openai-compatible-image-provider.test.ts`
- `/Users/kevinlin/code/openclaw/src/image-generation/image-assets.test.ts`
- `/Users/kevinlin/code/openclaw/src/test-utils/generation-live-test-helpers.ts`

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search openclaw/openclaw --query "image generation Codex OAuth" --json
```

Résultats :

- A retourné #76690 pour `openai/gpt-image-2` via Codex OAuth outil-non-trouvé, #85797 pour la génération d'images de capacité nécessitant une clé API malgré le chemin OAuth fonctionnel, #72087 pour la rupture de génération d'images Codex OAuth dist/entry Linux, #79360 pour les IDs de génération de réponses, et #87051 pour la propagation du profil OAuth affectant le travail de génération d'images.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "image generation" --json
```

Résultats :

- A retourné les métadonnées du fournisseur (#85466), la séparation des défaillances de génération/livraison (#86034/#86279), les problèmes de fournisseur xAI et StepFun (#83857/#86493/#86605), et les demandes de capacité du fournisseur OpenRouter/hébergé.

### Requêtes Discrawl

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "image generation Codex OAuth" --limit 5
```

Résultats :

- A retourné l'archive du responsable avec #77388 fusionné par Peter pour le routage d'édition GPT Image 2/NB2 fal, #80687 pour les délais d'expiration de génération de médias, et la discussion orientée utilisateur de Codex OAuth par rapport à la facturation API pour la génération d'images.
- A retourné la note du responsable du 2026-05-01 selon laquelle les défaillances de génération d'images observées avec `openai/gpt-image-2` via Codex OAuth utilisaient des délais d'expiration de 120s/180s et les défauts hébergés non-OpenAI devaient être augmentés.
