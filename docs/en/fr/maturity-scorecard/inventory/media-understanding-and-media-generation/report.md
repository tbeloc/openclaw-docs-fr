---
title: "Rapport de maturité de la compréhension et de la génération de médias"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité de la compréhension et de la génération de médias

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont arrondis au nombre entier le plus proche.

- Couverture : `Beta (78%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (78%)`
- Fonctionnalités LTS : `0/6`

## Résumé

Ce rapport promeut les preuves de maturité archivées `media-understanding-and-media-generation` de `/Users/kevinlin/tmp/maturity/media-understanding-and-media-generation` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de Couverture et Qualité des catégories proviennent des lignes de score soutenues par les preuves archivées. La Complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                         | LTS | Couverture     | Qualité       | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| -------------------------------------------------------------------------------- | --- | -------------- | ------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Ingestion et accès aux médias](media-file-intake-storage-and-secure-access.md)        | ❌  | `Beta (74%)`   | `Beta (76%)`  | `Beta (74%)`   | Références de médias locales et distantes, détection MIME et de type, Limites de taille et lectures bornées, Récupération distante sécurisée, Politique de racine locale, Magasin de médias entrants, Dispatch d'extraction PDF/document, Classification des assistants QR et médias                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [Gestion des médias de canal](channel-attachment-staging-and-reply-media-delivery.md) | ❌  | `Stable (84%)` | `Alpha (68%)` | `Stable (84%)` | Staging des pièces jointes entrantes, Réécritures de médias en sandbox, Modélisation des médias de réponse, Livraison des pièces jointes des outils de message, Suppression de la livraison en double                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [Configuration des médias](media-understanding-orchestration-and-configuration.md)    | ❌  | `Stable (82%)` | `Beta (77%)`  | `Stable (82%)` | Configuration des capacités médias                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| [Livraison de synthèse vocale](tts-and-outbound-voice-audio-delivery.md)              | ❌  | `Stable (84%)` | `Beta (70%)`  | `Stable (84%)` | Synthèse vocale, Livraison d'audio vocal sortant                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| [Compréhension des médias](image-understanding-and-vision-routing.md)                 | ❌  | `Beta (72%)`   | `Alpha (62%)` | `Beta (72%)`   | Sélection des pièces jointes audio, Fournisseur STT par lot et secours CLI, Préflight de mention de note vocale, Insertion et écho de transcription, Gestion du proxy audio et des limites, Résumé d'image entrant, Contournement du modèle de vision actif, Déchargement de médias du modèle texte uniquement, Secours du fournisseur de vision, Routage des entrées image et PDF, Compréhension vidéo, Analyse vidéo directe                                                                                                                                                                                                  |
| [Génération de médias](image-generation-tool-and-provider-routing.md)                | ❌  | `Beta (74%)`   | `Alpha (64%)` | `Beta (74%)`   | Invocation de l'outil de génération d'images, Sélection du fournisseur et du modèle, Édition d'images de référence, Cycle de vie des tâches d'images générées, Persistance et livraison des images générées, Invocation de l'outil de génération musicale, Sélection du fournisseur et du modèle, Contrôles des paroles, instrumentaux, durée et format, Entrées de référence où supportées, Cycle de vie des tâches musicales et statut de duplication, Persistance et livraison de l'audio généré, Invocation de l'outil de génération vidéo, Sélection du mode et des capacités du fournisseur, Entrées d'images, vidéos et audio de référence, Validation des options du fournisseur, Cycle de vie et statut des tâches vidéo, Persistance et livraison des vidéos générées |

## Rubrique de notation

- Couverture :
  notation de label de maturité pour l'intégration, e2e, live, ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de label de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, live et du flux runtime réel sont des entrées de Couverture uniquement ; elles ne
  augmentent ni ne diminuent la Qualité.
- Complétude :
  notation de label de maturité pour la façon dont la catégorie livre l'ensemble complet des
  capacités spécifiques à la surface prévues. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez le
  label de maturité supérieur.
- Lacunes majeures de qualité/complétude :
  texte de preuves uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Ingestion et accès aux médias

Ancres de recherche : Références de médias locaux et distants, Détection MIME et de type, Limites de taille et lectures délimitées, Récupération distante sécurisée, Politique de racine locale, Magasin de médias entrants, Dispatch d'extraction PDF/document, Classification des codes QR et des assistants médias.

Note de catégorie : [Ingestion et accès aux médias](media-file-intake-storage-and-secure-access.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Beta (76%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Références de médias locaux et distants : Couvre les références de médias locaux et distants dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S), et le comportement associé d'ingestion, de stockage et d'accès sécurisé des fichiers médias.
- Détection MIME et de type : Couvre la détection MIME et de type dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S), et le comportement associé d'ingestion, de stockage et d'accès sécurisé des fichiers médias.
- Limites de taille et lectures délimitées : Couvre les limites de taille et les lectures délimitées dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S), et le comportement associé d'ingestion, de stockage et d'accès sécurisé des fichiers médias.
- Récupération distante sécurisée : Couvre la récupération distante sécurisée dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S), et le comportement associé d'ingestion, de stockage et d'accès sécurisé des fichiers médias.
- Politique de racine locale : Couvre la politique de racine locale dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S), et le comportement associé d'ingestion, de stockage et d'accès sécurisé des fichiers médias.
- Magasin de médias entrants : Couvre le magasin de médias entrants dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S), et le comportement associé d'ingestion, de stockage et d'accès sécurisé des fichiers médias.
- Dispatch d'extraction PDF/document : Couvre le dispatch d'extraction PDF/document dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S), et le comportement associé d'ingestion, de stockage et d'accès sécurisé des fichiers médias.
- Classification des codes QR et des assistants médias : Couvre la classification des codes QR et des assistants médias dans Inclus : Références de médias locaux et distants, y compris les chemins simples, `file://`, HTTP(S), et le comportement associé d'ingestion, de stockage et d'accès sécurisé des fichiers médias.

Documentation principale :

- `docs/tools/media-overview.md`
- `docs/nodes/media-understanding.md`
- `docs/gateway/security/secure-file-operations.md`
- `docs/tools/pdf.md`
- `docs/tools/image-generation.md`
- `docs/cli/qr.md`
- `docs/channels/line.md`
- `docs/channels/whatsapp.md`

### 2. Gestion des médias de canal

Ancres de recherche : Staging des pièces jointes entrantes, Réécritures de médias en sandbox, Modèles de médias de réponse, Livraison des pièces jointes outil-message, Suppression de la livraison en double, Compréhension des médias (audio), Fallback fournisseur + CLI, Détection des mentions dans les groupes.

Note de catégorie : [Gestion des médias de canal](channel-attachment-staging-and-reply-media-delivery.md)

Décisions de score :

- Couverture : `Stable (84%)`
- Qualité : `Alpha (68%)`
- Complétude : `Stable (84%)`
- LTS : ❌

Fonctionnalités :

- Staging des pièces jointes entrantes : Couvre le staging des pièces jointes entrantes dans le staging des pièces jointes entrantes, les réécritures en sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias, et le comportement associé du staging des pièces jointes de canal et de la livraison des médias de réponse.
- Réécritures de médias en sandbox : Couvre les réécritures de médias en sandbox dans le staging des pièces jointes entrantes, les réécritures en sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias, et le comportement associé du staging des pièces jointes de canal et de la livraison des médias de réponse.
- Modèles de médias de réponse : Couvre les modèles de médias de réponse dans le staging des pièces jointes entrantes, les réécritures en sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias, et le comportement associé du staging des pièces jointes de canal et de la livraison des médias de réponse.
- Livraison des pièces jointes outil-message : Couvre la livraison des pièces jointes outil-message dans le staging des pièces jointes entrantes, les réécritures en sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias, et le comportement associé du staging des pièces jointes de canal et de la livraison des médias de réponse.
- Suppression de la livraison en double : Couvre la suppression de la livraison en double dans le staging des pièces jointes entrantes, les réécritures en sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias, et le comportement associé du staging des pièces jointes de canal et de la livraison des médias de réponse.

Documentation principale :

- `docs/nodes/images.md`
- `docs/tools/media-overview.md`
- `docs/channels/discord.md`

### 3. Configuration des médias

Ancres de recherche : Orchestration et configuration de la compréhension et de la génération des médias, orchestration et configuration de la compréhension et de la génération des médias.

Note de catégorie : [Configuration des médias](media-understanding-orchestration-and-configuration.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (77%)`
- Complétude : `Stable (82%)`
- LTS : ❌

Fonctionnalités :

- Configuration des capacités médias : Configuration tools.media image/audio/vidéo, entrées de modèles médias partagées et par capacité, résolution des entrées fournisseur/CLI, sélection de capacité soutenue par authentification, ordre de fallback, règles de portée, concurrence, comportement de saut de modèle actif, routage d'image déchargée, disponibilité de l'usine d'outils de génération d'images, statut/liste/garde en double de tâche de génération d'images, et livraison de médias générés dans le pipeline de réponse

Documentation principale :

- `docs/tools/media-overview.md`
- `docs/tools/image-generation.md`
- `docs/plugins/manifest.md`
- `docs/plugins/codex-harness.md`

### 4. Livraison de synthèse vocale

Ancres de recherche : TTS, Livraison audio vocale sortante, Synthèse vocale et livraison audio vocale sortante, synthèse vocale et livraison audio vocale sortante.

Note de catégorie : [Livraison de synthèse vocale](tts-and-outbound-voice-audio-delivery.md)

Décisions de score :

- Couverture : `Stable (84%)`
- Qualité : `Beta (70%)`
- Complétude : `Stable (84%)`
- LTS : ❌

Fonctionnalités :

- TTS : Couvre TTS dans l'agent/outil `tts` et les méthodes Gateway, `messages.tts`, registre des fournisseurs, directives, et le comportement associé de synthèse vocale et de livraison audio vocale sortante.
- Livraison audio vocale sortante : Couvre la livraison audio vocale sortante dans l'agent/outil `tts` et les méthodes Gateway, `messages.tts`, registre des fournisseurs, directives, et le comportement associé de synthèse vocale et de livraison audio vocale sortante.

Documentation principale :

- `docs/tools/tts.md`
- `docs/tools/media-overview.md`
- `docs/channels/discord.md`

### 5. Compréhension des médias

Ancres de recherche : Sélection des pièces jointes audio, Fallback fournisseur STT par lot et CLI, Préflight de mention de note vocale, Insertion et écho de transcription, Gestion du proxy audio et des limites, Compréhension des médias (audio), Fallback fournisseur + CLI, Détection des mentions dans les groupes, Résumé d'image entrant, Contournement du modèle de vision actif, Déchargement de médias de modèle texte uniquement, Fallback du fournisseur de vision, Routage d'entrée image et PDF, Compréhension vidéo, Analyse vidéo directe, Compréhension vidéo et analyse vidéo directe, compréhension vidéo et analyse vidéo directe.

Note de catégorie : [Compréhension des médias](image-understanding-and-vision-routing.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (62%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Sélection des pièces jointes audio : Couvre la sélection des pièces jointes audio dans la compréhension des médias audio/STT par lot, les fallbacks CLI locaux, la transcription du fournisseur, le préflight de note vocale avant les portes de mention, et le comportement associé de transcription audio et de compréhension des notes vocales.
- Fallback fournisseur STT par lot et CLI : Couvre le fallback fournisseur STT par lot et CLI dans la compréhension des médias audio/STT par lot, les fallbacks CLI locaux, la transcription du fournisseur, le préflight de note vocale avant les portes de mention, et le comportement associé de transcription audio et de compréhension des notes vocales.
- Préflight de mention de note vocale : Couvre le préflight de mention de note vocale dans la compréhension des médias audio/STT par lot, les fallbacks CLI locaux, la transcription du fournisseur, le préflight de note vocale avant les portes de mention, et le comportement associé de transcription audio et de compréhension des notes vocales.
- Insertion et écho de transcription : Couvre l'insertion et l'écho de transcription dans la compréhension des médias audio/STT par lot, les fallbacks CLI locaux, la transcription du fournisseur, le préflight de note vocale avant les portes de mention, et le comportement associé de transcription audio et de compréhension des notes vocales.
- Gestion du proxy audio et des limites : Couvre la gestion du proxy audio et des limites dans la compréhension des médias audio/STT par lot, les fallbacks CLI locaux, la transcription du fournisseur, le préflight de note vocale avant les portes de mention, et le comportement associé de transcription audio et de compréhension des notes vocales.
- Résumé d'image entrant : Couvre le résumé d'image entrant dans le résumé d'image avant le routage de réponse, le comportement de saut de vision de modèle actif, le déchargement de modèle texte uniquement via `MediaPaths`/`media://inbound`, la résolution de fallback de modèle image, et le comportement associé de compréhension d'image et de routage de vision.
- Contournement du modèle de vision actif : Couvre le contournement du modèle de vision actif dans le résumé d'image avant le routage de réponse, le comportement de saut de vision de modèle actif, le déchargement de modèle texte uniquement via `MediaPaths`/`media://inbound`, la résolution de fallback de modèle image, et le comportement associé de compréhension d'image et de routage de vision.
- Déchargement de médias de modèle texte uniquement : Couvre le déchargement de médias de modèle texte uniquement dans le résumé d'image avant le routage de réponse, le comportement de saut de vision de modèle actif, le déchargement de modèle texte uniquement via `MediaPaths`/`media://inbound`, la résolution de fallback de modèle image, et le comportement associé de compréhension d'image et de routage de vision.
- Fallback du fournisseur de vision : Couvre le fallback du fournisseur de vision dans le résumé d'image avant le routage de réponse, le comportement de saut de vision de modèle actif, le déchargement de modèle texte uniquement via `MediaPaths`/`media://inbound`, la résolution de fallback de modèle image, et le comportement associé de compréhension d'image et de routage de vision.
- Routage d'entrée image et PDF : Couvre le routage d'entrée image et PDF dans le résumé d'image avant le routage de réponse, le comportement de saut de vision de modèle actif, le déchargement de modèle texte uniquement via `MediaPaths`/`media://inbound`, la résolution de fallback de modèle image, et le comportement associé de compréhension d'image et de routage de vision.
- Compréhension vidéo : Couvre la compréhension vidéo dans le résumé vidéo avant le routage de réponse, les entrées de médias vidéo fournisseur/CLI, les contrôles de taille et de délai d'expiration, le support du proxy, la construction de requête vidéo, et les chemins d'analyse vidéo directe. Elle ne note pas la génération vidéo.
- Analyse vidéo directe : Couvre l'analyse vidéo directe dans le résumé vidéo avant le routage de réponse, les entrées de médias vidéo fournisseur/CLI, les contrôles de taille et de délai d'expiration, le support du proxy, la construction de requête vidéo, et les chemins d'analyse vidéo directe. Elle ne note pas la génération vidéo.

Documentation principale :

- `docs/nodes/audio.md`
- `docs/nodes/media-understanding.md`
- `docs/tools/media-overview.md`
- `docs/channels/whatsapp.md`
- `docs/nodes/images.md`
- `docs/cli/infer.md`
- `docs/tools/pdf.md`

### 6. Génération de médias

Ancres de recherche : Invocation de l'outil de génération d'images, Sélection du fournisseur et du modèle, Édition d'image de référence, Cycle de vie de la tâche d'image générée, Persistance et livraison d'image générée, Compréhension des médias (audio), Fallback fournisseur + CLI, Détection des mentions dans les groupes, Invocation de l'outil de génération de musique, Contrôles de paroles, instrumental, durée et format, Entrées de référence où supportées, Cycle de vie de la tâche de musique et statut en double, Persistance et livraison audio générée, Invocation de l'outil de génération vidéo, Sélection du mode et de la capacité du fournisseur, Entrées d'image, vidéo et audio de référence, Validation des options du fournisseur, Cycle de vie et statut de la tâche vidéo, Persistance et livraison vidéo générée.

Note de catégorie : [Génération de médias](image-generation-tool-and-provider-routing.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Alpha (64%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Invocation de l'outil de génération d'images : Couvre l'invocation de l'outil de génération d'images dans `image_generate`, sélection du modèle, enregistrement du fournisseur, liste des capacités du fournisseur, et le comportement associé de l'outil de génération d'images et du routage du fournisseur.
- Sélection du fournisseur et du modèle : Couvre la sélection du fournisseur et du modèle dans `image_generate`, sélection du modèle, enregistrement du fournisseur, liste des capacités du fournisseur, et le comportement associé de l'outil de génération d'images et du routage du fournisseur.
- Édition d'image de référence : Couvre l'édition d'image de référence dans `image_generate`, sélection du modèle, enregistrement du fournisseur, liste des capacités du fournisseur, et le comportement associé de l'outil de génération d'images et du routage du fournisseur.
- Cycle de vie de la tâche d'image générée : Couvre le cycle de vie de la tâche d'image générée dans `image_generate`, sélection du modèle, enregistrement du fournisseur, liste des capacités du fournisseur, et le comportement associé de l'outil de génération d'images et du routage du fournisseur.
- Persistance et livraison d'image générée : Couvre la persistance et la livraison d'image générée dans `image_generate`, sélection du modèle, enregistrement du fournisseur, liste des capacités du fournisseur, et le comportement associé de l'outil de génération d'images et du routage du fournisseur.
- Invocation de l'outil de génération de musique : Couvre l'invocation de l'outil de génération de musique dans `music_generate`, configuration fournisseur/modèle, contrôles de paroles/instrumental/durée/format, entrées d'image de référence où supportées, et le comportement associé de l'outil de génération de musique et du routage du fournisseur.
- Sélection du fournisseur et du modèle : Couvre la sélection du fournisseur et du modèle dans `music_generate`, configuration fournisseur/modèle, contrôles de paroles/instrumental/durée/format, entrées d'image de référence où supportées, et le comportement associé de l'outil de génération de musique et du routage du fournisseur.
- Contrôles de paroles, instrumental, durée et format : Couvre les contrôles de paroles, instrumental, durée et format dans `music_generate`, configuration fournisseur/modèle, contrôles de paroles/instrumental/durée/format, entrées d'image de référence où supportées, et le comportement associé de l'outil de génération de musique et du routage du fournisseur.
- Entrées de référence où supportées : Couvre les entrées de référence où supportées dans `music_generate`, configuration fournisseur/modèle, contrôles de paroles/instrumental/durée/format, entrées d'image de référence où supportées, et le comportement associé de l'outil de génération de musique et du routage du fournisseur.
- Cycle de vie de la tâche de musique et statut en double : Couvre le cycle de vie de la tâche de musique et le statut en double dans `music_generate`, configuration fournisseur/modèle, contrôles de paroles/instrumental/durée/format, entrées d'image de référence où supportées, et le comportement associé de l'outil de génération de musique et du routage du fournisseur.
- Persistance et livraison audio générée : Couvre la persistance et la livraison audio générée dans `music_generate`, configuration fournisseur/modèle, contrôles de paroles/instrumental/durée/format, entrées d'image de référence où supportées, et le comportement associé de l'outil de génération de musique et du routage du fournisseur.
- Invocation de l'outil de génération vidéo : Couvre l'invocation de l'outil de génération vidéo dans `video_generate`, résolution du mode, capacités du fournisseur, entrées d'image/vidéo/audio de référence, et le comportement associé de l'outil de génération vidéo et du routage du fournisseur.
- Sélection du mode et de la capacité du fournisseur : Couvre la sélection du mode et de la capacité du fournisseur dans `video_generate`, résolution du mode, capacités du fournisseur, entrées d'image/vidéo/audio de référence, et le comportement associé de l'outil de génération vidéo et du routage du fournisseur.
- Entrées d'image, vidéo et audio de référence : Couvre les entrées d'image, vidéo et audio de référence dans `video_generate`, résolution du mode, capacités du fournisseur, entrées d'image/vidéo/audio de référence, et le comportement associé de l'outil de génération vidéo et du routage du fournisseur.
- Validation des options du fournisseur : Couvre la validation des options du fournisseur dans `video_generate`, résolution du mode, capacités du fournisseur, entrées d'image/vidéo/audio de référence, et le comportement associé de l'outil de génération vidéo et du routage du fournisseur.
- Cycle de vie et statut de la tâche vidéo : Couvre le cycle de vie et le statut de la tâche vidéo dans `video_generate`, résolution du mode, capacités du fournisseur, entrées d'image/vidéo/audio de référence, et le comportement associé de l'outil de génération vidéo et du routage du fournisseur.
- Persistance et livraison vidéo générée : Couvre la persistance et la livraison vidéo générée dans `video_generate`, résolution du mode, capacités du fournisseur, entrées d'image/vidéo/audio de référence, et le comportement associé de l'outil de génération vidéo et du routage du fournisseur.

Documentation principale :

- `docs/tools/image-generation.md`
- `docs/tools/media-overview.md`
- `docs/tools/skills.md`
- `docs/tools/music-generation.md`
- `docs/tools/video-generation.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/media-understanding-and-media-generation/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/media-understanding-and-media-generation`.
