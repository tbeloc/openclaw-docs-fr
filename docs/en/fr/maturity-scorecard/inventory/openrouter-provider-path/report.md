---
title: "Rapport de maturité du chemin du fournisseur OpenRouter"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité du chemin du fournisseur OpenRouter

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (75%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (75%)`
- Fonctionnalités LTS : `0/4`

## Résumé

Ce rapport promeut les preuves de maturité archivées de `openrouter-provider-path` depuis `/Users/kevinlin/tmp/maturity/openrouter-provider-path` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de catégorie Couverture et Qualité proviennent des lignes de score archivées soutenues par des preuves. La Complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                                              | LTS | Couverture   | Qualité       | Complétude   | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------- | --- | ------------ | ------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Configuration du fournisseur et authentification](operator-setup-and-provider-registration.md)                | ❌  | `Beta (78%)` | `Alpha (64%)` | `Beta (78%)` | Configuration au premier lancement, Sélection du modèle par défaut, Enregistrement du plugin fournisseur, Exemples de références de modèle, OPENROUTER_API_KEY, Profils d'authentification et ordre d'authentification, Statut/sonde et suppression, Résolution SecretRef/clé API de l'entrée fournisseur, Héritage env de la passerelle, Lignes de catalogue statique, Découverte dynamique /models, openrouter/auto et références imbriquées, Analyse/sonde de modèle gratuit, Cache du sélecteur/liste de modèles                                                                   |
| [Runtime de chat et normalisation](chat-completions-transport-routing-and-reasoning.md) | ❌  | `Beta (76%)` | `Beta (70%)`  | `Beta (76%)` | Route de complétions de chat, Paramètres de routage du fournisseur, Remplacements de route par modèle, Politique de charge utile de raisonnement, Variantes Anthropic/Gemini/DeepSeek, Analyse du contenu en flux, Sortie visible de reasoning_details, Préservation du delta d'appel d'outil, Politique de relecture spécifique à la famille, Normalisation du modèle de réponse et de l'utilisation, En-têtes d'attribution, En-têtes/TTL/effacement du cache de réponse, Marqueurs de contrôle de cache Anthropic, Mappage d'utilisation du cache, Exclusions de proxy personnalisées |
| [Récupération et diagnostics du fournisseur](failover-errors-overflow-and-diagnostics.md)      | ❌  | `Beta (74%)` | `Alpha (65%)` | `Beta (74%)` | Classification des délais d'expiration/tentatives, Classification de l'authentification/facturation/limite de clé, Débordement de contexte, Avis de secours de modèle, Avertissements de récupération/tarification gardés                                                                                                                                                                                                                                                                                                                   |
| [Génération de médias et parole](media-generation-speech-and-media-understanding.md)     | ❌  | `Beta (72%)` | `Alpha (66%)` | `Beta (72%)` | Route OpenRouter image_generate, Tâches asynchrones video_generate/interrogation/téléchargement, Route audio music_generate, Synthèse vocale, Transcription parole-texte, Compréhension des médias entrants, Livraison d'artefacts générés                                                                                                                                                                                                                                                                                                                                 |

## Barème de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de Couverture
  uniquement ; ils ne relèvent ni n'abaissent la Qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie livre l'ensemble complet de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante
  définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité
  supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration du fournisseur et authentification

Ancres de recherche : Configuration au premier lancement, Sélection du modèle par défaut, Enregistrement du plugin du fournisseur, Exemples de références de modèles, OPENROUTER_API_KEY, Profils d'authentification et ordre d'authentification, Statut/sonde et suppression, Résolution SecretRef/clé API de l'entrée du fournisseur, Héritage env de la passerelle, Lignes de catalogue statique, Découverte dynamique /models, openrouter/auto et références imbriquées, Analyse/sonde de modèle gratuit, Cache du sélecteur/liste de modèles.

Note de catégorie : [Configuration du fournisseur et authentification](operator-setup-and-provider-registration.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Alpha (64%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- Configuration au premier lancement : Couvre la configuration au premier lancement dans la configuration accessible à l'utilisateur et l'enregistrement du fournisseur : la documentation `/providers/openrouter`, le manifeste du plugin, le hook d'enregistrement du fournisseur, l'enregistrement du modèle par défaut, et le comportement connexe de configuration de l'opérateur et de sélection de modèle.
- Sélection du modèle par défaut : Couvre la sélection du modèle par défaut dans la configuration accessible à l'utilisateur et l'enregistrement du fournisseur : la documentation `/providers/openrouter`, le manifeste du plugin, le hook d'enregistrement du fournisseur, l'enregistrement du modèle par défaut, et le comportement connexe de configuration de l'opérateur et de sélection de modèle.
- Enregistrement du plugin du fournisseur : Couvre l'enregistrement du plugin du fournisseur dans la configuration accessible à l'utilisateur et l'enregistrement du fournisseur : la documentation `/providers/openrouter`, le manifeste du plugin, le hook d'enregistrement du fournisseur, l'enregistrement du modèle par défaut, et le comportement connexe de configuration de l'opérateur et de sélection de modèle.
- Exemples de références de modèles : Couvre les exemples de références de modèles dans la configuration accessible à l'utilisateur et l'enregistrement du fournisseur : la documentation `/providers/openrouter`, le manifeste du plugin, le hook d'enregistrement du fournisseur, l'enregistrement du modèle par défaut, et le comportement connexe de configuration de l'opérateur et de sélection de modèle.
- OPENROUTER_API_KEY : Couvre OPENROUTER_API_KEY dans la découverte `OPENROUTER_API_KEY`, le stockage du choix d'authentification/intégration, `auth-profiles.json`, la visibilité du statut/sonde, et le comportement connexe des identifiants et profils d'authentification.
- Profils d'authentification et ordre d'authentification : Couvre les profils d'authentification et l'ordre d'authentification dans la découverte `OPENROUTER_API_KEY`, le stockage du choix d'authentification/intégration, `auth-profiles.json`, la visibilité du statut/sonde, et le comportement connexe des identifiants et profils d'authentification.
- Statut/sonde et suppression : Couvre le statut/sonde et la suppression dans la découverte `OPENROUTER_API_KEY`, le stockage du choix d'authentification/intégration, `auth-profiles.json`, la visibilité du statut/sonde, et le comportement connexe des identifiants et profils d'authentification.
- Résolution SecretRef/clé API de l'entrée du fournisseur : Couvre la résolution SecretRef/clé API de l'entrée du fournisseur dans la découverte `OPENROUTER_API_KEY`, le stockage du choix d'authentification/intégration, `auth-profiles.json`, la visibilité du statut/sonde, et le comportement connexe des identifiants et profils d'authentification.
- Héritage env de la passerelle : Couvre l'héritage env de la passerelle dans la découverte `OPENROUTER_API_KEY`, le stockage du choix d'authentification/intégration, `auth-profiles.json`, la visibilité du statut/sonde, et le comportement connexe des identifiants et profils d'authentification.
- Lignes de catalogue statique : Couvre les lignes de catalogue statique dans les lignes de catalogue statique, la découverte dynamique des capacités de modèle, la normalisation des identifiants de modèle, les références `openrouter/<provider>/<model>`, et le comportement connexe du catalogue de modèles et de la découverte dynamique.
- Découverte dynamique /models : Couvre la découverte dynamique /models dans les lignes de catalogue statique, la découverte dynamique des capacités de modèle, la normalisation des identifiants de modèle, les références `openrouter/<provider>/<model>`, et le comportement connexe du catalogue de modèles et de la découverte dynamique.
- openrouter/auto et références imbriquées : Couvre openrouter/auto et les références imbriquées dans les lignes de catalogue statique, la découverte dynamique des capacités de modèle, la normalisation des identifiants de modèle, les références `openrouter/<provider>/<model>`, et le comportement connexe du catalogue de modèles et de la découverte dynamique.
- Analyse/sonde de modèle gratuit : Couvre l'analyse/sonde de modèle gratuit dans les lignes de catalogue statique, la découverte dynamique des capacités de modèle, la normalisation des identifiants de modèle, les références `openrouter/<provider>/<model>`, et le comportement connexe du catalogue de modèles et de la découverte dynamique.
- Cache du sélecteur/liste de modèles : Couvre le cache du sélecteur/liste de modèles dans les lignes de catalogue statique, la découverte dynamique des capacités de modèle, la normalisation des identifiants de modèle, les références `openrouter/<provider>/<model>`, et le comportement connexe du catalogue de modèles et de la découverte dynamique.

Documentation principale :

- `docs/providers/openrouter.md`
- `docs/concepts/model-providers.md`
- `docs/cli/configure.md`
- `docs/gateway/authentication.md`
- `docs/help/environment.md`
- `docs/cli/models.md`
- `docs/concepts/models.md`

### 2. Runtime de chat et normalisation

Ancres de recherche : Route de complétions de chat, Paramètres de routage du fournisseur, Remplacements de route par modèle, Politique de charge utile de raisonnement, Variantes Anthropic/Gemini/DeepSeek, Analyse du contenu en flux, Sortie visible reasoning_details, Préservation du delta d'appel d'outil, Politique de relecture spécifique à la famille, Normalisation du modèle de réponse et de l'utilisation, En-têtes d'attribution, En-têtes/TTL/effacement du cache de réponse, Marqueurs de contrôle de cache Anthropic, Mappage d'utilisation du cache, Exclusions de proxy personnalisées.

Note de catégorie : [Runtime de chat et normalisation](chat-completions-transport-routing-and-reasoning.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Route de complétions de chat : Couvre la route de complétions de chat dans le transport de complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de route par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement connexe du routage de chat et du raisonnement.
- Paramètres de routage du fournisseur : Couvre les paramètres de routage du fournisseur dans le transport de complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de route par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement connexe du routage de chat et du raisonnement.
- Remplacements de route par modèle : Couvre les remplacements de route par modèle dans le transport de complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de route par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement connexe du routage de chat et du raisonnement.
- Politique de charge utile de raisonnement : Couvre la politique de charge utile de raisonnement dans le transport de complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de route par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement connexe du routage de chat et du raisonnement.
- Variantes Anthropic/Gemini/DeepSeek : Couvre les variantes Anthropic/Gemini/DeepSeek dans le transport de complétions de chat OpenRouter, le routage `models.providers.openrouter.params.provider`, les remplacements de route par modèle, les charges utiles de raisonnement proxy OpenRouter, et le comportement connexe du routage de chat et du raisonnement.
- Analyse du contenu en flux : Couvre l'analyse du contenu en flux dans l'analyse des réponses en flux, l'extraction de la sortie visible de `reasoning_details` OpenRouter, la préservation du delta d'appel d'outil, la politique de relecture Mistral strict9, et le comportement connexe du flux et de la relecture d'appel d'outil.
- Sortie visible reasoning_details : Couvre la sortie visible reasoning_details dans l'analyse des réponses en flux, l'extraction de la sortie visible de `reasoning_details` OpenRouter, la préservation du delta d'appel d'outil, la politique de relecture Mistral strict9, et le comportement connexe du flux et de la relecture d'appel d'outil.
- Préservation du delta d'appel d'outil : Couvre la préservation du delta d'appel d'outil dans l'analyse des réponses en flux, l'extraction de la sortie visible de `reasoning_details` OpenRouter, la préservation du delta d'appel d'outil, la politique de relecture Mistral strict9, et le comportement connexe du flux et de la relecture d'appel d'outil.
- Politique de relecture spécifique à la famille : Couvre la politique de relecture spécifique à la famille dans l'analyse des réponses en flux, l'extraction de la sortie visible de `reasoning_details` OpenRouter, la préservation du delta d'appel d'outil, la politique de relecture Mistral strict9, et le comportement connexe du flux et de la relecture d'appel d'outil.
- Normalisation du modèle de réponse et de l'utilisation : Couvre la normalisation du modèle de réponse et de l'utilisation dans l'analyse des réponses en flux, l'extraction de la sortie visible de `reasoning_details` OpenRouter, la préservation du delta d'appel d'outil, la politique de relecture Mistral strict9, et le comportement connexe du flux et de la relecture d'appel d'outil.
- En-têtes d'attribution : Couvre les en-têtes d'attribution dans l'attribution d'application OpenRouter, les en-têtes du cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache d'invite, le mappage d'utilisation cache-read/cache-write, le gating de route vérifiée, et les exclusions de proxy personnalisées.
- En-têtes/TTL/effacement du cache de réponse : Couvre les en-têtes/TTL/effacement du cache de réponse dans l'attribution d'application OpenRouter, les en-têtes du cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache d'invite, le mappage d'utilisation cache-read/cache-write, le gating de route vérifiée, et les exclusions de proxy personnalisées.
- Marqueurs de contrôle de cache Anthropic : Couvre les marqueurs de contrôle de cache Anthropic dans l'attribution d'application OpenRouter, les en-têtes du cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache d'invite, le mappage d'utilisation cache-read/cache-write, le gating de route vérifiée, et les exclusions de proxy personnalisées.
- Mappage d'utilisation du cache : Couvre le mappage d'utilisation du cache dans l'attribution d'application OpenRouter, les en-têtes du cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache d'invite, le mappage d'utilisation cache-read/cache-write, le gating de route vérifiée, et les exclusions de proxy personnalisées.
- Exclusions de proxy personnalisées : Couvre les exclusions de proxy personnalisées dans l'attribution d'application OpenRouter, les en-têtes du cache de réponse, le comportement TTL et d'effacement, les marqueurs de contrôle de cache Anthropic, la rétention du cache d'invite, le mappage d'utilisation cache-read/cache-write, le gating de route vérifiée, et les exclusions de proxy personnalisées.

Documentation principale :

- `docs/providers/openrouter.md`
- `docs/concepts/model-providers.md`
- `docs/reference/prompt-caching.md`

### 3. Récupération et diagnostics du fournisseur

Ancres de recherche : Classification délai d'attente/nouvelle tentative, Classification authentification/facturation/limite de clé, Débordement de contexte, Avis de secours de modèle, Avertissements de récupération/tarification gardés.

Note de catégorie : [Récupération et diagnostics du fournisseur](failover-errors-overflow-and-diagnostics.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Alpha (65%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Classification délai d'attente/nouvelle tentative : Couvre la classification délai d'attente/nouvelle tentative dans la classification délai d'attente/nouvelle tentative OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification authentification/facturation/limite de clé, l'analyse du débordement de contexte, et le comportement connexe du basculement et des diagnostics.
- Classification authentification/facturation/limite de clé : Couvre la classification authentification/facturation/limite de clé dans la classification délai d'attente/nouvelle tentative OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification authentification/facturation/limite de clé, l'analyse du débordement de contexte, et le comportement connexe du basculement et des diagnostics.
- Débordement de contexte : Couvre le débordement de contexte dans la classification délai d'attente/nouvelle tentative OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification authentification/facturation/limite de clé, l'analyse du débordement de contexte, et le comportement connexe du basculement et des diagnostics.
- Avis de secours de modèle : Couvre les avis de secours de modèle dans la classification délai d'attente/nouvelle tentative OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification authentification/facturation/limite de clé, l'analyse du débordement de contexte, et le comportement connexe du basculement et des diagnostics.
- Avertissements de récupération/tarification gardés : Couvre les avertissements de récupération/tarification gardés dans la classification délai d'attente/nouvelle tentative OpenRouter, les erreurs génériques spécifiques au fournisseur, la classification authentification/facturation/limite de clé, l'analyse du débordement de contexte, et le comportement connexe du basculement et des diagnostics.

Documentation principale :

- `docs/concepts/model-failover.md`
- `docs/providers/openrouter.md`
- `docs/cli/models.md`

### 4. Génération de médias et parole

Ancres de recherche : Route image_generate OpenRouter, Tâches asynchrones video_generate/interrogation/téléchargement, Route audio music_generate, Synthèse vocale, Transcription parole-texte, Compréhension des médias entrants, Livraison d'artefacts générés.

Note de catégorie : [Génération de médias et parole](media-generation-speech-and-media-understanding.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Route image_generate OpenRouter : Couvre la route image_generate OpenRouter dans l'image, la vidéo, la musique, la synthèse vocale OpenRouter, et le comportement connexe de l'image, la vidéo, la musique, et la parole.
- Tâches asynchrones video_generate/interrogation/téléchargement : Couvre les tâches asynchrones video_generate/interrogation/téléchargement dans l'image, la vidéo, la musique, la synthèse vocale OpenRouter, et le comportement connexe de l'image, la vidéo, la musique, et la parole.
- Route audio music_generate : Couvre la route audio music_generate dans l'image, la vidéo, la musique, la synthèse vocale OpenRouter, et le comportement connexe de l'image, la vidéo, la musique, et la parole.
- Synthèse vocale : Couvre la synthèse vocale dans l'image, la vidéo, la musique, la synthèse vocale OpenRouter, et le comportement connexe de l'image, la vidéo, la musique, et la parole.
- Transcription parole-texte : Couvre la transcription parole-texte dans l'image, la vidéo, la musique, la synthèse vocale OpenRouter, et le comportement connexe de l'image, la vidéo, la musique, et la parole.
- Compréhension des médias entrants : Couvre la compréhension des médias entrants dans l'image, la vidéo, la musique, la synthèse vocale OpenRouter, et le comportement connexe de l'image, la vidéo, la musique, et la parole.
- Livraison d'artefacts générés : Couvre la livraison d'artefacts générés dans l'image, la vidéo, la musique, la synthèse vocale OpenRouter, et le comportement connexe de l'image, la vidéo, la musique, et la parole.

Documentation principale :

- `docs/providers/openrouter.md`
- `docs/tools/image-generation.md`
- `docs/tools/music-generation.md`
- `docs/tools/media-overview.md`
- `docs/tools/video-generation.md`
- `docs/tools/tts.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/openrouter-provider-path/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/openrouter-provider-path`.
