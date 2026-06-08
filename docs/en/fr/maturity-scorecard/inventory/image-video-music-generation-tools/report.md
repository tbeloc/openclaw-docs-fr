---
title: "Rapport de maturité des outils de génération d'images/vidéos/musique"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité des outils de génération d'images/vidéos/musique

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (77%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (77%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées `image-video-music-generation-tools` de `/Users/kevinlin/tmp/maturity/image-video-music-generation-tools` dans le contrat d'inventaire process-version-3 actuel.

Les scores de Couverture et Qualité de la catégorie proviennent des lignes de score archivées soutenues par des preuves. La Complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                            | LTS | Couverture     | Qualité       | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                   |
| ----------------------------------------------------------------------------------- | --- | -------------- | ------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Routage et découverte des médias](configuration-model-refs-and-provider-discovery.md)   | ❌  | `Stable (82%)` | `Beta (74%)`  | `Stable (82%)` | config du modèle de média par défaut, références de modèle par appel et secours, découverte d'outils soutenue par l'authentification, inspection du fournisseur action=list                                                                                                                                                                                  |
| [Cycle de vie et livraison des tâches](session-backed-tool-invocation-and-task-lifecycle.md) | ❌  | `Beta (78%)`   | `Alpha (65%)` | `Beta (78%)`   | création de tâche en arrière-plan, statut/liste/affichage/annulation de tâche, gardes contre les doublons, maintien de la progression, réveil à la fin/échec, secours en ligne sans session, persistance des médias locaux, inférence MIME/nom de fichier, secours URL hébergée, remise message-outil, secours idempotent pour médias manquants, preuve de pièce jointe de canal |
| [Génération d'images](image-generation-and-editing-runtime.md)                         | ❌  | `Beta (78%)`   | `Alpha (66%)` | `Beta (78%)`   | texte vers image, édition d'image de référence, indices de sortie, action=status, métadonnées de tentative du fournisseur, OAuth OpenAI/Codex, clé API OpenAI, authentification OpenRouter/xAI/fal/LiteLLM/DeepInfra/Google/MiniMax/ComfyUI, diagnostics d'erreur du fournisseur                                                            |
| [Génération vidéo](video-generation-modes-and-request-normalization.md)             | ❌  | `Beta (76%)`   | `Alpha (62%)` | `Beta (76%)`   | texte vers vidéo, image vers vidéo, vidéo vers vidéo, validation du rôle de référence, références audio, providerOptions typés, tâches soutenues par file d'attente, gestion du sondage/délai d'expiration, téléchargement URL hébergée, explications de saut du fournisseur, métadonnées d'actif retournées                                                          |
| [Génération musicale](music-generation-tools-and-providers.md)                         | ❌  | `Beta (72%)`   | `Alpha (61%)` | `Beta (72%)`   | entrée d'invite et de paroles, mode instrumental, contrôles de durée/format, couloirs d'édition de référence d'image, sorties audio générées, secours du fournisseur                                                                                                                                                                |

## Rubrique de notation

- Couverture :
  notation de label de maturité pour l'intégration, e2e, en direct, ou les preuves de flux
  serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de label de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de Couverture
  uniquement ; elles ne relèvent ni n'abaissent la Qualité.
- Complétude :
  notation de label de maturité pour la complétude avec laquelle la catégorie fournit l'ensemble de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante
  définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez le
  label de maturité supérieur.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Routage des médias et découverte

Ancres de recherche : config du modèle média par défaut, références de modèles par appel et solutions de secours, découverte d'outils soutenue par l'authentification, inspection du fournisseur action=list.

Note de catégorie : [Routage des médias et découverte](configuration-model-refs-and-provider-discovery.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (74%)`
- Complétude : `Stable (82%)`
- LTS : ❌

Fonctionnalités :

- config du modèle média par défaut : Couvre la config du modèle média par défaut sur `imageGenerationModel`, `videoGenerationModel`, `musicGenerationModel`, références fournisseur/modèle, et le comportement associé du routage des modèles et de la découverte d'outils.
- références de modèles par appel et solutions de secours : Couvre les références de modèles par appel et les solutions de secours sur `imageGenerationModel`, `videoGenerationModel`, `musicGenerationModel`, références fournisseur/modèle, et le comportement associé du routage des modèles et de la découverte d'outils.
- découverte d'outils soutenue par l'authentification : Couvre la découverte d'outils soutenue par l'authentification sur `imageGenerationModel`, `videoGenerationModel`, `musicGenerationModel`, références fournisseur/modèle, et le comportement associé du routage des modèles et de la découverte d'outils.
- inspection du fournisseur action=list : Couvre l'inspection du fournisseur action=list sur `imageGenerationModel`, `videoGenerationModel`, `musicGenerationModel`, références fournisseur/modèle, et le comportement associé du routage des modèles et de la découverte d'outils.

Documentation principale :

- `docs/gateway/config-agents.md`
- `docs/tools/image-generation.md`
- `docs/tools/video-generation.md`
- `docs/tools/music-generation.md`

### 2. Cycle de vie des tâches et livraison

Ancres de recherche : création de tâches en arrière-plan, statut/liste/affichage/annulation des tâches, garde contre les doublons, maintien de la progression, réveil à la fin/échec, solution de secours en ligne sans session, persistance des médias locaux, inférence MIME/nom de fichier, solution de secours URL hébergée, remise message-outil, solution de secours idempotente pour médias manquants, preuve de pièce jointe de canal.

Note de catégorie : [Cycle de vie des tâches et livraison](session-backed-tool-invocation-and-task-lifecycle.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Alpha (65%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- création de tâches en arrière-plan : Couvre la création de tâches en arrière-plan sur l'exposition des outils `image_generate`, `video_generate` et `music_generate`, la planification des tâches en arrière-plan, et le comportement associé du cycle de vie des tâches asynchrones.
- statut/liste/affichage/annulation des tâches : Couvre le statut/liste/affichage/annulation des tâches sur l'exposition des outils `image_generate`, `video_generate` et `music_generate`, la planification des tâches en arrière-plan, et le comportement associé du cycle de vie des tâches asynchrones.
- garde contre les doublons : Couvre la garde contre les doublons sur l'exposition des outils `image_generate`, `video_generate` et `music_generate`, la planification des tâches en arrière-plan, et le comportement associé du cycle de vie des tâches asynchrones.
- maintien de la progression : Couvre le maintien de la progression sur l'exposition des outils `image_generate`, `video_generate` et `music_generate`, la planification des tâches en arrière-plan, et le comportement associé du cycle de vie des tâches asynchrones.
- réveil à la fin/échec : Couvre le réveil à la fin/échec sur l'exposition des outils `image_generate`, `video_generate` et `music_generate`, la planification des tâches en arrière-plan, et le comportement associé du cycle de vie des tâches asynchrones.
- solution de secours en ligne sans session : Couvre la solution de secours en ligne sans session sur l'exposition des outils `image_generate`, `video_generate` et `music_generate`, la planification des tâches en arrière-plan, et le comportement associé du cycle de vie des tâches asynchrones.
- persistance des médias locaux : Couvre la persistance des médias locaux sur les objets artefacts image/audio/vidéo générés, l'inférence MIME et du nom de fichier, les chemins des médias locaux, les URL des médias hébergés, et le comportement associé de la livraison des médias générés.
- inférence MIME/nom de fichier : Couvre l'inférence MIME/nom de fichier sur les objets artefacts image/audio/vidéo générés, l'inférence MIME et du nom de fichier, les chemins des médias locaux, les URL des médias hébergés, et le comportement associé de la livraison des médias générés.
- solution de secours URL hébergée : Couvre la solution de secours URL hébergée sur les objets artefacts image/audio/vidéo générés, l'inférence MIME et du nom de fichier, les chemins des médias locaux, les URL des médias hébergés, et le comportement associé de la livraison des médias générés.
- remise message-outil : Couvre la remise message-outil sur les objets artefacts image/audio/vidéo générés, l'inférence MIME et du nom de fichier, les chemins des médias locaux, les URL des médias hébergés, et le comportement associé de la livraison des médias générés.
- solution de secours idempotente pour médias manquants : Couvre la solution de secours idempotente pour médias manquants sur les objets artefacts image/audio/vidéo générés, l'inférence MIME et du nom de fichier, les chemins des médias locaux, les URL des médias hébergés, et le comportement associé de la livraison des médias générés.
- preuve de pièce jointe de canal : Couvre la preuve de pièce jointe de canal sur les objets artefacts image/audio/vidéo générés, l'inférence MIME et du nom de fichier, les chemins des médias locaux, les URL des médias hébergés, et le comportement associé de la livraison des médias générés.

Documentation principale :

- `docs/tools/media-overview.md`
- `docs/tools/image-generation.md`
- `docs/tools/video-generation.md`
- `docs/tools/music-generation.md`

### 3. Génération d'images

Ancres de recherche : texte vers image, édition d'image de référence, indices de sortie, action=status, métadonnées de tentative du fournisseur, OAuth OpenAI/Codex, OpenAI avec clé API, authentification OpenRouter/xAI/fal/LiteLLM/DeepInfra/Google/MiniMax/ComfyUI, diagnostics d'erreur du fournisseur.

Note de catégorie : [Génération d'images](image-generation-and-editing-runtime.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- texte vers image : Couvre le texte vers image sur le comportement d'exécution de la génération et de l'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des requêtes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images, et le comportement associé de la génération et de l'édition d'images.
- édition d'image de référence : Couvre l'édition d'image de référence sur le comportement d'exécution de la génération et de l'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des requêtes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images, et le comportement associé de la génération et de l'édition d'images.
- indices de sortie : Couvre les indices de sortie sur le comportement d'exécution de la génération et de l'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des requêtes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images, et le comportement associé de la génération et de l'édition d'images.
- action=status : Couvre action=status sur le comportement d'exécution de la génération et de l'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des requêtes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images, et le comportement associé de la génération et de l'édition d'images.
- métadonnées de tentative du fournisseur : Couvre les métadonnées de tentative du fournisseur sur le comportement d'exécution de la génération et de l'édition d'images après qu'un candidat fournisseur a été sélectionné : normalisation des requêtes, gestion des délais d'expiration, entrées d'images de référence, analyse des réponses d'images, et le comportement associé de la génération et de l'édition d'images.
- OAuth OpenAI/Codex : Couvre OAuth OpenAI/Codex sur les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OAuth OpenAI/Codex, OpenRouter, xAI, et le comportement associé des fournisseurs d'images et d'authentification.
- OpenAI avec clé API : Couvre OpenAI avec clé API sur les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OAuth OpenAI/Codex, OpenRouter, xAI, et le comportement associé des fournisseurs d'images et d'authentification.
- authentification OpenRouter/xAI/fal/LiteLLM/DeepInfra/Google/MiniMax/ComfyUI : Couvre l'authentification OpenRouter/xAI/fal/LiteLLM/DeepInfra/Google/MiniMax/ComfyUI sur les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OAuth OpenAI/Codex, OpenRouter, xAI, et le comportement associé des fournisseurs d'images et d'authentification.
- diagnostics d'erreur du fournisseur : Couvre les diagnostics d'erreur du fournisseur sur les enregistrements de fournisseurs et les chemins d'authentification pour la génération et l'édition d'images, y compris OAuth OpenAI/Codex, OpenRouter, xAI, et le comportement associé des fournisseurs d'images et d'authentification.

Documentation principale :

- `docs/tools/image-generation.md`
- `docs/cli/infer.md`
- `docs/tools/media-overview.md`

### 4. Génération de vidéos

Ancres de recherche : texte vers vidéo, image vers vidéo, vidéo vers vidéo, validation du rôle de référence, références audio, providerOptions typés, tâches soutenues par file d'attente, gestion de l'interrogation/délai d'expiration, téléchargement d'URL hébergée, explications de saut du fournisseur, métadonnées d'actifs retournées.

Note de catégorie : [Génération de vidéos](video-generation-modes-and-request-normalization.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Alpha (62%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- texte vers vidéo : Couvre le texte vers vidéo sur la normalisation des requêtes de génération de vidéos avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et le comportement associé des modes de génération de vidéos.
- image vers vidéo : Couvre l'image vers vidéo sur la normalisation des requêtes de génération de vidéos avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et le comportement associé des modes de génération de vidéos.
- vidéo vers vidéo : Couvre la vidéo vers vidéo sur la normalisation des requêtes de génération de vidéos avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et le comportement associé des modes de génération de vidéos.
- validation du rôle de référence : Couvre la validation du rôle de référence sur la normalisation des requêtes de génération de vidéos avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et le comportement associé des modes de génération de vidéos.
- références audio : Couvre les références audio sur la normalisation des requêtes de génération de vidéos avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et le comportement associé des modes de génération de vidéos.
- providerOptions typés : Couvre les providerOptions typés sur la normalisation des requêtes de génération de vidéos avant l'exécution du fournisseur : modes `generate`, `imageToVideo` et `videoToVideo`, typage des médias de référence et rôles, et le comportement associé des modes de génération de vidéos.
- tâches soutenues par file d'attente : Couvre les tâches soutenues par file d'attente sur l'intégration du fournisseur et l'interrogation asynchrone pour la génération de vidéos après la normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et le comportement associé des fournisseurs de vidéos et d'interrogation.
- gestion de l'interrogation/délai d'expiration : Couvre la gestion de l'interrogation/délai d'expiration sur l'intégration du fournisseur et l'interrogation asynchrone pour la génération de vidéos après la normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et le comportement associé des fournisseurs de vidéos et d'interrogation.
- téléchargement d'URL hébergée : Couvre le téléchargement d'URL hébergée sur l'intégration du fournisseur et l'interrogation asynchrone pour la génération de vidéos après la normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et le comportement associé des fournisseurs de vidéos et d'interrogation.
- explications de saut du fournisseur : Couvre les explications de saut du fournisseur sur l'intégration du fournisseur et l'interrogation asynchrone pour la génération de vidéos après la normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et le comportement associé des fournisseurs de vidéos et d'interrogation.
- métadonnées d'actifs retournées : Couvre les métadonnées d'actifs retournées sur l'intégration du fournisseur et l'interrogation asynchrone pour la génération de vidéos après la normalisation des requêtes : OpenAI Sora, OpenRouter, fal, Runway, et le comportement associé des fournisseurs de vidéos et d'interrogation.

Documentation principale :

- `docs/tools/video-generation.md`
- `docs/providers/runway.md`
- `docs/providers/pixverse.md`
- `docs/providers/fal.md`
- `docs/providers/openrouter.md`

### 5. Génération de musique

Ancres de recherche : entrée d'invite et de paroles, mode instrumental, contrôles de durée/format, pistes d'édition de référence d'image, sorties audio générées, solution de secours du fournisseur.

Note de catégorie : [Génération de musique](music-generation-tools-and-providers.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (61%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- entrée d'invite et de paroles : Couvre l'entrée d'invite et de paroles sur `music_generate`, entrées d'invite et de paroles, mode instrumental, durée, et le comportement associé de la génération de musique.
- mode instrumental : Couvre le mode instrumental sur `music_generate`, entrées d'invite et de paroles, mode instrumental, durée, et le comportement associé de la génération de musique.
- contrôles de durée/format : Couvre les contrôles de durée/format sur `music_generate`, entrées d'invite et de paroles, mode instrumental, durée, et le comportement associé de la génération de musique.
- pistes d'édition de référence d'image : Couvre les pistes d'édition de référence d'image sur `music_generate`, entrées d'invite et de paroles, mode instrumental, durée, et le comportement associé de la génération de musique.
- sorties audio générées : Couvre les sorties audio générées sur `music_generate`, entrées d'invite et de paroles, mode instrumental, durée, et le comportement associé de la génération de musique.
- solution de secours du fournisseur : Couvre la solution de secours du fournisseur sur `music_generate`, entrées d'invite et de paroles, mode instrumental, durée, et le comportement associé de la génération de musique.

Documentation principale :

- `docs/tools/music-generation.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/image-video-music-generation-tools/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/image-video-music-generation-tools`.
