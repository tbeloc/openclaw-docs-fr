---
title: "Rapport de maturité du chemin du fournisseur Google"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité du chemin du fournisseur Google

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (73%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (73%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées de `google-provider-path` depuis `/Users/kevinlin/tmp/maturity/google-provider-path` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                                                    | LTS | Couverture     | Qualité        | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------------- | --- | -------------- | -------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Configuration du fournisseur et identifiants](provider-auth-credentials-and-operator-setup.md)           | ❌  | `Beta (72%)`   | `Alpha (60%)`  | `Beta (72%)`   | Intégration des clés API, Métadonnées de choix d'authentification, Configuration OAuth de Gemini CLI, Configuration ADC Vertex, Identifiants daemon et de secours, Sélection du runtime CLI, Connexion et actualisation OAuth, Références de modèles Google canoniques, Normalisation de l'utilisation CLI, Diagnostics OAuth                           |
| [Routage des modèles et points de terminaison](model-catalog-provider-routing-and-config-normalization.md)   | ❌  | `Alpha (68%)`  | `Alpha (62%)`  | `Alpha (68%)`  | Lignes et alias du catalogue, Résolution dynamique des modèles, Routage du fournisseur, Normalisation de la configuration native Google, Disponibilité du sélecteur de modèles, Sélection du fournisseur Vertex, Authentification ADC/compte de service, Points de terminaison de projet/localisation, Politique d'URL de base personnalisée, Limites de compatibilité |
| [Runtime Gemini direct](direct-gemini-api-transport-streaming-and-multimodal-payloads.md)   | ❌  | `Stable (82%)` | `Stable (80%)` | `Stable (82%)` | Chat Gemini direct, Entrées multimodales, Streaming des appels d'outils, Utilisation et raisons d'arrêt, Relecture de signature de pensée, Mappage du niveau de pensée, Relecture de signature de pensée, Ordre des tours d'outils, Récupération de tour incomplet, Récupération de tour de planification uniquement                              |
| [Médias, recherche et temps réel](plugin-distribution-and-cross-surface-capability-adapters.md) | ❌  | `Beta (76%)`   | `Alpha (65%)`  | `Beta (76%)`   | Distribution de plugins groupés, Métadonnées d'activation automatique du fournisseur, Adaptateurs d'image et de médias, Adaptateurs de parole et temps réel, Outils de recherche et de génération, Sessions de voix en temps réel, Jetons de navigateur contraints, Événements audio et transcription, Appels d'outils en direct, Reconnexions de session |
| [Mise en cache des invites](prompt-cache-cache-retention-and-usage-accounting.md)                      | ❌  | `Alpha (68%)`  | `Beta (74%)`   | `Alpha (68%)`  | Configuration de la rétention du cache, cachedContents gérés, Handles cachedContent manuels, Comptabilité de l'utilisation du cache, Diagnostics du cache et preuve en direct                                                                                                                                 |

## Barème de notation

- Couverture :
  notation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les
  preuves de flux de serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, en direct et de flux de runtime réel sont des
  entrées de couverture uniquement ; elles ne relèvent ni n'abaissent la qualité.
- Complétude :
  notation de l'étiquette de maturité pour la complétude avec laquelle la catégorie fournit l'ensemble de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration du fournisseur et identifiants

Ancres de recherche : Intégration des clés API, Métadonnées de choix d'authentification, Configuration OAuth de Gemini CLI, Configuration ADC Vertex, Identifiants de daemon et de secours, Sélection du runtime CLI, Connexion et actualisation OAuth, Références canoniques des modèles Google, Normalisation de l'utilisation CLI, Diagnostics OAuth.

Note de catégorie : [Configuration du fournisseur et identifiants](provider-auth-credentials-and-operator-setup.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (60%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Intégration des clés API : Couvre l'intégration des clés API sur l'authentification directe `GEMINI_API_KEY` et `GOOGLE_API_KEY`, les métadonnées du fournisseur de configuration, les choix d'authentification de configuration, les champs de configuration du fournisseur, et le comportement d'authentification et de configuration du fournisseur associé.
- Métadonnées de choix d'authentification : Couvre les métadonnées de choix d'authentification sur l'authentification directe `GEMINI_API_KEY` et `GOOGLE_API_KEY`, les métadonnées du fournisseur de configuration, les choix d'authentification de configuration, les champs de configuration du fournisseur, et le comportement d'authentification et de configuration du fournisseur associé.
- Configuration OAuth de Gemini CLI : Couvre la configuration OAuth de Gemini CLI sur l'authentification directe `GEMINI_API_KEY` et `GOOGLE_API_KEY`, les métadonnées du fournisseur de configuration, les choix d'authentification de configuration, les champs de configuration du fournisseur, et le comportement d'authentification et de configuration du fournisseur associé.
- Configuration ADC Vertex : Couvre la configuration ADC Vertex sur l'authentification directe `GEMINI_API_KEY` et `GOOGLE_API_KEY`, les métadonnées du fournisseur de configuration, les choix d'authentification de configuration, les champs de configuration du fournisseur, et le comportement d'authentification et de configuration du fournisseur associé.
- Identifiants de daemon et de secours : Couvre les identifiants de daemon et de secours sur l'authentification directe `GEMINI_API_KEY` et `GOOGLE_API_KEY`, les métadonnées du fournisseur de configuration, les choix d'authentification de configuration, les champs de configuration du fournisseur, et le comportement d'authentification et de configuration du fournisseur associé.
- Sélection du runtime CLI : Couvre la sélection du runtime CLI sur le fournisseur `google-gemini-cli`, les références canoniques des modèles `google/*` utilisant `agentRuntime.id: "google-gemini-cli"`, les références héritées `google-gemini-cli/*`, l'invocation de commande Gemini CLI, et le comportement OAuth de gemini cli associé.
- Connexion et actualisation OAuth : Couvre la connexion et l'actualisation OAuth sur le fournisseur `google-gemini-cli`, les références canoniques des modèles `google/*` utilisant `agentRuntime.id: "google-gemini-cli"`, les références héritées `google-gemini-cli/*`, l'invocation de commande Gemini CLI, et le comportement OAuth de gemini cli associé.
- Références canoniques des modèles Google : Couvre les références canoniques des modèles Google sur le fournisseur `google-gemini-cli`, les références canoniques des modèles `google/*` utilisant `agentRuntime.id: "google-gemini-cli"`, les références héritées `google-gemini-cli/*`, l'invocation de commande Gemini CLI, et le comportement OAuth de gemini cli associé.
- Normalisation de l'utilisation CLI : Couvre la normalisation de l'utilisation CLI sur le fournisseur `google-gemini-cli`, les références canoniques des modèles `google/*` utilisant `agentRuntime.id: "google-gemini-cli"`, les références héritées `google-gemini-cli/*`, l'invocation de commande Gemini CLI, et le comportement OAuth de gemini cli associé.
- Diagnostics OAuth : Couvre les diagnostics OAuth sur le fournisseur `google-gemini-cli`, les références canoniques des modèles `google/*` utilisant `agentRuntime.id: "google-gemini-cli"`, les références héritées `google-gemini-cli/*`, l'invocation de commande Gemini CLI, et le comportement OAuth de gemini cli associé.

Documentation principale :

- `docs/providers/google.md`
- `docs/concepts/model-providers.md`

### 2. Routage des modèles et points de terminaison

Ancres de recherche : Lignes de catalogue et alias, Résolution dynamique des modèles, Routage du fournisseur, Normalisation de la configuration native Google, Disponibilité du sélecteur de modèles, Sélection du fournisseur Vertex, Authentification ADC/compte de service, Points de terminaison de projet/localisation, Politique d'URL de base personnalisée, Limites de compatibilité.

Note de catégorie : [Routage des modèles et points de terminaison](model-catalog-provider-routing-and-config-normalization.md)

Décisions de score :

- Couverture : `Alpha (68%)`
- Qualité : `Alpha (62%)`
- Complétude : `Alpha (68%)`
- LTS : ❌

Fonctionnalités :

- Lignes de catalogue et alias : Couvre les lignes de catalogue et alias sur les lignes du catalogue de modèles, la normalisation des ID de modèles, la résolution dynamique des modèles, les hooks du fournisseur, et le comportement du catalogue de modèles et du routage associé.
- Résolution dynamique des modèles : Couvre la résolution dynamique des modèles sur les lignes du catalogue de modèles, la normalisation des ID de modèles, la résolution dynamique des modèles, les hooks du fournisseur, et le comportement du catalogue de modèles et du routage associé.
- Routage du fournisseur : Couvre le routage du fournisseur sur les lignes du catalogue de modèles, la normalisation des ID de modèles, la résolution dynamique des modèles, les hooks du fournisseur, et le comportement du catalogue de modèles et du routage associé.
- Normalisation de la configuration native Google : Couvre la normalisation de la configuration native Google sur les lignes du catalogue de modèles, la normalisation des ID de modèles, la résolution dynamique des modèles, les hooks du fournisseur, et le comportement du catalogue de modèles et du routage associé.
- Disponibilité du sélecteur de modèles : Couvre la disponibilité du sélecteur de modèles sur les lignes du catalogue de modèles, la normalisation des ID de modèles, la résolution dynamique des modèles, les hooks du fournisseur, et le comportement du catalogue de modèles et du routage associé.
- Sélection du fournisseur Vertex : Couvre la sélection du fournisseur Vertex sur `google-vertex`, l'authentification ADC/compte de service Vertex, la construction du point de terminaison de projet/localisation, la gestion de l'URL de base compatible Google personnalisée, et le comportement de vertex ai et des points de terminaison personnalisés associé.
- Authentification ADC/compte de service : Couvre l'authentification ADC/compte de service sur `google-vertex`, l'authentification ADC/compte de service Vertex, la construction du point de terminaison de projet/localisation, la gestion de l'URL de base compatible Google personnalisée, et le comportement de vertex ai et des points de terminaison personnalisés associé.
- Points de terminaison de projet/localisation : Couvre les points de terminaison de projet/localisation sur `google-vertex`, l'authentification ADC/compte de service Vertex, la construction du point de terminaison de projet/localisation, la gestion de l'URL de base compatible Google personnalisée, et le comportement de vertex ai et des points de terminaison personnalisés associé.
- Politique d'URL de base personnalisée : Couvre la politique d'URL de base personnalisée sur `google-vertex`, l'authentification ADC/compte de service Vertex, la construction du point de terminaison de projet/localisation, la gestion de l'URL de base compatible Google personnalisée, et le comportement de vertex ai et des points de terminaison personnalisés associé.
- Limites de compatibilité : Couvre les limites de compatibilité sur `google-vertex`, l'authentification ADC/compte de service Vertex, la construction du point de terminaison de projet/localisation, la gestion de l'URL de base compatible Google personnalisée, et le comportement de vertex ai et des points de terminaison personnalisés associé.

Documentation principale :

- `docs/providers/google.md`
- `docs/concepts/model-providers.md`
- `docs/plugins/reference/google.md`
- `docs/tools/gemini-search.md`

### 3. Runtime Gemini direct

Ancres de recherche : Chat Gemini direct, Entrées multimodales, Streaming des appels d'outils, Utilisation et raisons d'arrêt, Relecture de signature de pensée, Mappage du niveau de réflexion, Ordre des tours d'outils, Récupération de tour incomplet, Récupération de tour de planification uniquement.

Note de catégorie : [Runtime Gemini direct](direct-gemini-api-transport-streaming-and-multimodal-payloads.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Stable (80%)`
- Complétude : `Stable (82%)`
- LTS : ❌

Fonctionnalités :

- Chat Gemini direct : Couvre le chat Gemini direct sur le transport Gemini `google-generative-ai` direct et la conversion de message/flux Google partagée : construction d'URL de requête, configuration de requête, conversion de charge utile texte/image/audio/vidéo/outil, gestion de réponse de fonction, et comportement d'API gemini direct associé.
- Entrées multimodales : Couvre les entrées multimodales sur le transport Gemini `google-generative-ai` direct et la conversion de message/flux Google partagée : construction d'URL de requête, configuration de requête, conversion de charge utile texte/image/audio/vidéo/outil, gestion de réponse de fonction, et comportement d'API gemini direct associé.
- Streaming des appels d'outils : Couvre le streaming des appels d'outils sur le transport Gemini `google-generative-ai` direct et la conversion de message/flux Google partagée : construction d'URL de requête, configuration de requête, conversion de charge utile texte/image/audio/vidéo/outil, gestion de réponse de fonction, et comportement d'API gemini direct associé.
- Utilisation et raisons d'arrêt : Couvre l'utilisation et les raisons d'arrêt sur le transport Gemini `google-generative-ai` direct et la conversion de message/flux Google partagée : construction d'URL de requête, configuration de requête, conversion de charge utile texte/image/audio/vidéo/outil, gestion de réponse de fonction, et comportement d'API gemini direct associé.
- Relecture de signature de pensée : Couvre la relecture de signature de pensée sur le transport Gemini `google-generative-ai` direct et la conversion de message/flux Google partagée : construction d'URL de requête, configuration de requête, conversion de charge utile texte/image/audio/vidéo/outil, gestion de réponse de fonction, et comportement d'API gemini direct associé.
- Mappage du niveau de réflexion : Couvre le mappage du niveau de réflexion sur le mappage du niveau de réflexion Gemini, la forme de requête de réflexion adaptative, la capture/relecture/assainissement de `thoughtSignature`, la politique de relecture Google, et le comportement de réflexion et de récupération de tour associé.
- Relecture de signature de pensée : Couvre la relecture de signature de pensée sur le mappage du niveau de réflexion Gemini, la forme de requête de réflexion adaptative, la capture/relecture/assainissement de `thoughtSignature`, la politique de relecture Google, et le comportement de réflexion et de récupération de tour associé.
- Ordre des tours d'outils : Couvre l'ordre des tours d'outils sur le mappage du niveau de réflexion Gemini, la forme de requête de réflexion adaptative, la capture/relecture/assainissement de `thoughtSignature`, la politique de relecture Google, et le comportement de réflexion et de récupération de tour associé.
- Récupération de tour incomplet : Couvre la récupération de tour incomplet sur le mappage du niveau de réflexion Gemini, la forme de requête de réflexion adaptative, la capture/relecture/assainissement de `thoughtSignature`, la politique de relecture Google, et le comportement de réflexion et de récupération de tour associé.
- Récupération de tour de planification uniquement : Couvre la récupération de tour de planification uniquement sur le mappage du niveau de réflexion Gemini, la forme de requête de réflexion adaptative, la capture/relecture/assainissement de `thoughtSignature`, la politique de relecture Google, et le comportement de réflexion et de récupération de tour associé.

Documentation principale :

- `docs/providers/google.md`
- `docs/concepts/model-providers.md`
- `docs/help/faq-models.md`
- `docs/help/testing-live.md`

### 4. Médias, recherche et temps réel

Ancres de recherche : Distribution de plugin groupé, Métadonnées d'activation automatique du fournisseur, Adaptateurs d'image et de médias, Adaptateurs de parole et temps réel, Outils de recherche et de génération, Sessions vocales en temps réel, Jetons de navigateur contraints, Événements audio et transcription, Appels d'outils en direct, Reconnexions de session.

Note de catégorie : [Médias, recherche et temps réel](plugin-distribution-and-cross-surface-capability-adapters.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Alpha (65%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Distribution de plugin groupé : Couvre la distribution de plugin groupé sur le paquet `@openclaw/google-plugin` groupé, la distribution du manifeste de plugin, les métadonnées d'activation automatique, l'enregistrement du fournisseur de capacité, et le comportement des adaptateurs de plugin google associé.
- Métadonnées d'activation automatique du fournisseur : Couvre les métadonnées d'activation automatique du fournisseur sur le paquet `@openclaw/google-plugin` groupé, la distribution du manifeste de plugin, les métadonnées d'activation automatique, l'enregistrement du fournisseur de capacité, et le comportement des adaptateurs de plugin google associé.
- Adaptateurs d'image et de médias : Couvre les adaptateurs d'image et de médias sur le paquet `@openclaw/google-plugin` groupé, la distribution du manifeste de plugin, les métadonnées d'activation automatique, l'enregistrement du fournisseur de capacité, et le comportement des adaptateurs de plugin google associé.
- Adaptateurs de parole et temps réel : Couvre les adaptateurs de parole et temps réel sur le paquet `@openclaw/google-plugin` groupé, la distribution du manifeste de plugin, les métadonnées d'activation automatique, l'enregistrement du fournisseur de capacité, et le comportement des adaptateurs de plugin google associé.
- Outils de recherche et de génération : Couvre les outils de recherche et de génération sur le paquet `@openclaw/google-plugin` groupé, la distribution du manifeste de plugin, les métadonnées d'activation automatique, l'enregistrement du fournisseur de capacité, et le comportement des adaptateurs de plugin google associé.
- Sessions vocales en temps réel : Couvre les sessions vocales en temps réel sur le comportement du fournisseur de voix temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket de navigateur contraints, la mise en file d'attente audio, et le comportement de gemini live talk associé.
- Jetons de navigateur contraints : Couvre les jetons de navigateur contraints sur le comportement du fournisseur de voix temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket de navigateur contraints, la mise en file d'attente audio, et le comportement de gemini live talk associé.
- Événements audio et transcription : Couvre les événements audio et transcription sur le comportement du fournisseur de voix temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket de navigateur contraints, la mise en file d'attente audio, et le comportement de gemini live talk associé.
- Appels d'outils en direct : Couvre les appels d'outils en direct sur le comportement du fournisseur de voix temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket de navigateur contraints, la mise en file d'attente audio, et le comportement de gemini live talk associé.
- Reconnexions de session : Couvre les reconnexions de session sur le comportement du fournisseur de voix temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket de navigateur contraints, la mise en file d'attente audio, et le comportement de gemini live talk associé.

Documentation principale :

- `docs/plugins/reference/google.md`
- `docs/providers/google.md`

### 5. Mise en cache des invites

Ancres de recherche : Configuration de rétention du cache, cachedContents gérés, Poignées cachedContent manuelles, Comptabilité d'utilisation du cache, Diagnostics du cache et preuve en direct.

Note de catégorie : [Mise en cache des invites](prompt-cache-cache-retention-and-usage-accounting.md)

Décisions de score :

- Couverture : `Alpha (68%)`
- Qualité : `Beta (74%)`
- Complétude : `Alpha (68%)`
- LTS : ❌

Fonctionnalités :

- Configuration de rétention du cache : Couvre la configuration de rétention du cache sur l'admissibilité du cache d'invites Gemini `google-generative-ai` direct, `cacheRetention`, la création/réutilisation/actualisation de `cachedContents` gérés, la configuration manuelle de `cachedContent`, et le comportement de mise en cache des invites associé.
- cachedContents gérés : Couvre les cachedContents gérés sur l'admissibilité du cache d'invites Gemini `google-generative-ai` direct, `cacheRetention`, la création/réutilisation/actualisation de `cachedContents` gérés, la configuration manuelle de `cachedContent`, et le comportement de mise en cache des invites associé.
- Poignées cachedContent manuelles : Couvre les poignées cachedContent manuelles sur l'admissibilité du cache d'invites Gemini `google-generative-ai` direct, `cacheRetention`, la création/réutilisation/actualisation de `cachedContents` gérés, la configuration manuelle de `cachedContent`, et le comportement de mise en cache des invites associé.
- Comptabilité d'utilisation du cache : Couvre la comptabilité d'utilisation du cache sur l'admissibilité du cache d'invites Gemini `google-generative-ai` direct, `cacheRetention`, la création/réutilisation/actualisation de `cachedContents` gérés, la configuration manuelle de `cachedContent`, et le comportement de mise en cache des invites associé.
- Diagnostics du cache et preuve en direct : Couvre les diagnostics du cache et la preuve en direct sur l'admissibilité du cache d'invites Gemini `google-generative-ai` direct, `cacheRetention`, la création/réutilisation/actualisation de `cachedContents` gérés, la configuration manuelle de `cachedContent`, et le comportement de mise en cache des invites associé.

Documentation principale :

- `docs/reference/prompt-caching.md`
- `docs/providers/google.md`
- `docs/concepts/model-providers.md`
- `docs/reference/token-use.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/google-provider-path/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/google-provider-path`.
