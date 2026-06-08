---
title: Gateway Runtime - HTTP APIs Maturity Note
version: 3
last_refreshed: 2026-05-29
last_refreshed_by: codex
feature_family: HTTP APIs
feature_slug: http-apis
---

# HTTP APIs

## Résumé

OpenClaw expose des routes HTTP API de première classe sur le port Gateway, notamment les routes compatibles OpenAI `/v1/models`, `/v1/chat/completions`, `/v1/responses`, et `/v1/embeddings`, `/tools/invoke`, un RPC HTTP admin optionnel, et l'ingress des hooks. La couverture reste forte car les preuves archivées incluent des tests réels de flux serveur Gateway pour les routes principales compatibles OpenAI, l'invocation d'outils et les hooks. La qualité reste Beta car les rapports d'archive incluent toujours des cas limites de compatibilité, une confusion sur l'authentification des hooks, des lacunes dans l'activation du RPC admin et des problèmes de disponibilité des outils.

Scores :

- Couverture : `88` - `Stable`
- Qualité : `74` - `Beta`
- Complétude : `72` - `Beta`

## Fonctionnalités

- APIs compatibles OpenAI : APIs HTTP compatibles OpenAI (`/v1/models`, `/v1/chat/completions`, `/v1/responses`, `/v1/embeddings`).
- API d'invocation d'outils : Chemin HTTP d'invocation d'outils.
- Accès à l'API Admin : Route de plugin RPC HTTP admin optionnelle.
- Ingress des hooks : Hébergement de hooks et routes d'ingress HTTP.

## Couverture

Score : `88`

Signaux positifs :

- La documentation Gateway liste `/v1/*`, `/tools/invoke`, le RPC HTTP admin et les routes de hooks comme surfaces HTTP Gateway.
- La source distribue `/v1/models`, `/v1/embeddings`, `/v1/chat/completions`, `/v1/responses` et `/tools/invoke` depuis le serveur HTTP Gateway.
- Les tests d'intégration couvrent les modèles, les complétions de chat, les réponses, les embeddings, `/tools/invoke` et les routes de hooks via des requêtes HTTP Gateway réelles.

Signaux négatifs :

- Le RPC HTTP admin a des tests d'enregistrement et de gestionnaire, mais nécessite toujours un flux Gateway avec plugin activé pour `POST /api/v1/admin/rpc`.
- L'enregistrement des problèmes archivés inclut des cas limites ouverts autour du mappage des médias `/v1/*`, de l'exposition du raisonnement, de la réutilisation de session, de l'actualisation dynamique du catalogue de modèles et de l'authentification des hooks.

## Qualité

Score : `74`

Bonnes qualités :

- Les points de terminaison compatibles OpenAI et `/tools/invoke` partagent la sémantique d'authentification Gateway.
- Les routes de hooks sont documentées et ont des tests Gateway dédiés.
- Le RPC HTTP admin est désactivé par défaut et protégé par plugin.

Mauvaises qualités :

- Les attentes des opérateurs autour des tokens de hooks par rapport à l'authentification Gateway restent confuses.
- La compatibilité avec les clients de style OpenAI a toujours des cas limites actifs.
- La maturité du RPC HTTP admin dépend de la preuve du scénario avec plugin activé.

## Complétude

Score : `72`

Signaux positifs :

- La catégorie couvre les familles de points de terminaison HTTP durables que les clients externes et l'automatisation peuvent appeler directement.

Branches de capacité manquantes :

- Preuve complète du flux Gateway du RPC admin.
- Scénario de coexistence couvrant les routes compatibles OpenAI, `/tools/invoke`, les hooks et les routes HTTP admin/plugin sur un processus Gateway.

## Preuves

- Docs : `docs/gateway/index.md`, `docs/gateway/openai-http-api.md`, `docs/gateway/openresponses-http-api.md`, `docs/gateway/tools-invoke-http-api.md`, `docs/automation/hooks.md`, `docs/web/index.md`.
- Source : `src/gateway/server-http.ts`, `src/gateway/models-http.ts`, `src/gateway/openai-http.ts`, `src/gateway/openresponses-http.ts`, `src/gateway/embeddings-http.ts`, `src/gateway/tools-invoke-http.ts`, `extensions/admin-http-rpc/index.ts`.
- Tests : `src/gateway/models-http.test.ts`, `src/gateway/openai-http.test.ts`, `src/gateway/openresponses-http.test.ts`, `src/gateway/embeddings-http.test.ts`, `src/gateway/gateway.test.ts`, `src/gateway/server.hooks.test.ts`, `extensions/admin-http-rpc/index.test.ts`, `extensions/admin-http-rpc/src/handler.test.ts`.
- Requêtes d'archive : Problèmes Gateway compatibles OpenAI, `/v1/responses`, `/tools/invoke`, HTTP hooks Gateway et problèmes RPC HTTP admin de l'exécution du score archivé.
