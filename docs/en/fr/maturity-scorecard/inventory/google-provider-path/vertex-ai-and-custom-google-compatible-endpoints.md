---
title: "Chemin du fournisseur Google - Note de maturité Vertex AI et points de terminaison personnalisés"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur Google - Note de maturité Vertex AI et points de terminaison personnalisés

## Résumé

Le support de Vertex AI et des points de terminaison personnalisés compatibles avec Google est implémenté, mais c'est la partie la plus faible du chemin du fournisseur Google. Le code source gère l'enregistrement `google-vertex`, l'authentification ADC/compte de service, la construction d'URL Vertex, les en-têtes de porteur et la politique d'URL de base personnalisée. La couverture est Alpha car la preuve en direct est principalement un comportement Google natif adjacent plutôt que des appels réels ADC/compte de service Vertex. La qualité est Alpha car les preuves d'archive montrent un routage Vertex actif, une configuration ADC, des erreurs 404 et des défaillances Gemini compatibles OpenAI.

## Portée de la catégorie

Cette catégorie couvre `google-vertex`, l'authentification ADC/compte de service Vertex, la construction de points de terminaison projet/localisation, la gestion des URL de base personnalisées compatibles avec Google, et les limites des points de terminaison Gemini/OpenAI-compatibles. Elle exclut l'authentification OAuth CLI Gemini et le comportement direct des clés API Google, sauf lorsque la logique de transport partagée est réutilisée par Vertex.

## Fonctionnalités

- Sélection du fournisseur Vertex : Couvre la sélection du fournisseur Vertex sur `google-vertex`, l'authentification ADC/compte de service Vertex, la construction de points de terminaison projet/localisation, la gestion des URL de base personnalisées compatibles avec Google, et le comportement associé de vertex ai et des points de terminaison personnalisés.
- Authentification ADC/compte de service : Couvre l'authentification ADC/compte de service sur `google-vertex`, l'authentification ADC/compte de service Vertex, la construction de points de terminaison projet/localisation, la gestion des URL de base personnalisées compatibles avec Google, et le comportement associé de vertex ai et des points de terminaison personnalisés.
- Points de terminaison projet/localisation : Couvre les points de terminaison projet/localisation sur `google-vertex`, l'authentification ADC/compte de service Vertex, la construction de points de terminaison projet/localisation, la gestion des URL de base personnalisées compatibles avec Google, et le comportement associé de vertex ai et des points de terminaison personnalisés.
- Politique d'URL de base personnalisée : Couvre la politique d'URL de base personnalisée sur `google-vertex`, l'authentification ADC/compte de service Vertex, la construction de points de terminaison projet/localisation, la gestion des URL de base personnalisées compatibles avec Google, et le comportement associé de vertex ai et des points de terminaison personnalisés.
- Limites de compatibilité : Couvre les limites de compatibilité sur `google-vertex`, l'authentification ADC/compte de service Vertex, la construction de points de terminaison projet/localisation, la gestion des URL de base personnalisées compatibles avec Google, et le comportement associé de vertex ai et des points de terminaison personnalisés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (68%)`
- Signaux positifs : Une couverture de flux unitaire/runtime existe pour la détection ADC, l'authentification de porteur, la construction de requête SSE Vertex, le repli ADC Windows et la normalisation baseUrl personnalisée ; les tests de fournisseur en direct plus larges incluent l'analyse des références de modèles Google.
- Signaux négatifs : Aucune preuve en direct/e2e dédiée n'a été trouvée pour les appels réels ADC/compte de service `google-vertex` contre Vertex AI.
- Lacunes d'intégration : Les points de terminaison personnalisés compatibles avec Google ont des preuves de configuration et d'unité, mais pas de matrice de compatibilité en direct uniforme.

## Score de qualité

- Score : `Alpha (62%)`
- Rapports Gitcrawl : #58775 rapporte la fusion de `google-vertex` dans le chemin de transport Google ; #84804 rapporte que Vertex retourne 404 via `openclaw agent` tandis que curl direct fonctionne ; #84384 rapporte un délai d'expiration du streaming compatible OpenAI Vertex autour des jetons de réflexion.
- Rapports Discrawl : Les recherches `google-vertex Vertex AI` et `Vertex AI ADC google-vertex` ont trouvé des défaillances de configuration autour de `No API key found for provider "google-vertex"`, des régressions de marqueur ADC et des clarifications répétées selon lesquelles Vertex utilise l'authentification ADC/compte de service plutôt que les clés API Gemini.
- Bonnes qualités : La source sépare la construction d'URL Vertex, la résolution du chemin ADC, la mise en cache des jetons, la normalisation des URL de base et la génération d'en-têtes de requête.
- Mauvaises qualités : Le chemin du produit a toujours une confusion de routage et d'authentification active, et le support des points de terminaison personnalisés dépend d'une classification soigneuse des limites.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux runtime réel ; ceux-ci sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Alpha (68%)`
- Instructions de surface : évaluées par rapport à `references/completeness/google-provider-path.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la sélection du fournisseur Vertex, l'authentification ADC/compte de service, les points de terminaison projet/localisation, la politique d'URL de base personnalisée, les limites de compatibilité.
- Signaux négatifs : la note archivée a précédé le scoring de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La dispatch réelle ADC/compte de service Vertex a besoin d'une preuve en direct dédiée.
- La documentation Vertex est clairsemée par rapport aux docs Google direct et Gemini CLI.
- Les exemples de localisation, projet et point de terminaison personnalisé par modèle sont minces.
- Les preuves d'archive montrent que les utilisateurs confondent toujours l'authentification par clé API `google` avec l'authentification ADC/compte de service `google-vertex`.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/reference/google.md:10` dit que le plugin Google inclut les fournisseurs de modèles Google, Gemini CLI et Google Vertex.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md:217` identifie `google-vertex` et dit que Vertex utilise gcloud ADC.
- `/Users/kevinlin/code/openclaw/docs/tools/gemini-search.md:101` documente les remplacements d'URL de base de recherche web Gemini pour les points de terminaison personnalisés compatibles avec Gemini.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md:686` documente la mise en forme du proxy compatible OpenAI et les règles de confiance d'origine exacte.

### Source

- `/Users/kevinlin/code/openclaw/extensions/google/provider-registration.ts:60` achemine les modèles `google-vertex` vers `createGoogleVertexTransportStreamFn`.
- `/Users/kevinlin/code/openclaw/extensions/google/provider-contract-api.ts:31` déclare le fournisseur `google-vertex` et les variables d'environnement requises.
- `/Users/kevinlin/code/openclaw/extensions/google/transport-stream.ts:332` résout le projet/localisation Vertex et l'origine de la requête.
- `/Users/kevinlin/code/openclaw/extensions/google/transport-stream.ts:384` construit l'URL Vertex `streamGenerateContent?alt=sse`.
- `/Users/kevinlin/code/openclaw/extensions/google/transport-stream.ts:764` construit les en-têtes d'authentification Vertex à partir du marqueur ADC ou de la clé API.
- `/Users/kevinlin/code/openclaw/extensions/google/vertex-adc.ts:118` supporte ADC `authorized_user`, `external_account` et `service_account`.
- `/Users/kevinlin/code/openclaw/extensions/google/provider-policy.ts:40` normalise les URL de base Google et supprime `/openai` uniquement pour les chemins Gemini natifs.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/google/google.live.test.ts:121` teste en direct l'exécution du fournisseur de recherche web Gemini natif.
- `/Users/kevinlin/code/openclaw/src/agents/google-gemini-switch.live.test.ts:12` teste en direct les exécutions de modèles Google natifs avec l'historique des appels d'outils.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-models.profiles.live.test.ts:2019` inclut une couverture d'analyseur de références de modèles en direct pour `google`, `google-gemini-cli` et `google-vertex`.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/google/transport-stream.test.ts:718` couvre la détection de source ADC.
- `/Users/kevinlin/code/openclaw/extensions/google/transport-stream.test.ts:758` couvre les en-têtes de porteur Google Auth et le flux de requête SSE Vertex.
- `/Users/kevinlin/code/openclaw/extensions/google/transport-stream.test.ts:871` couvre le repli ADC APPDATA Windows.
- `/Users/kevinlin/code/openclaw/extensions/google/api.test.ts:109` préserve le `baseUrl` Vertex compatible OpenAI.
- `/Users/kevinlin/code/openclaw/src/llm/env-api-keys.test.ts:52` détecte ADC Vertex et évite les défauts de cache.

### Requêtes Gitcrawl

Requête : `gitcrawl search issues "Google Vertex ADC google-vertex" -R openclaw/openclaw --state all`

Résultats :

- #58775 `google-vertex provider merged into google transport path`.
- #84804 `google-vertex provider returns 404 from Google when models are accessed via openclaw agent`.
- #84384 `Gemini 2.5 Flash via vertex-ai streaming times out`.

Requête : `gitcrawl search issues "OpenAI-compatible Gemini" -R openclaw/openclaw --state all`

Résultats :

- Retourné #84384 sur le délai d'expiration du streaming compatible OpenAI Vertex AI et la gestion des jetons de réflexion.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "google-vertex Vertex AI"`

Résultats :

- Trouvé des défaillances de configuration avec `No API key found for provider "google-vertex"` et des commentaires d'archive autour des régressions de sentinelle ADC.

Requête : `discrawl search --limit 10 "Vertex AI ADC google-vertex"`

Résultats :

- Trouvé des rapports de régression de marqueur ADC/authentification répétés et des conseils selon lesquels `google-vertex/*` utilise l'authentification ADC/compte de service plutôt que les clés API Gemini.

Requête : `discrawl search --limit 10 "Gemini compatible endpoint baseUrl"`

Résultats :

- Trouvé des défaillances de schéma/limite de point de terminaison Gemini compatible OpenAI, des rapports de jetons zéro et des correctifs et demandes liés à baseUrl.
