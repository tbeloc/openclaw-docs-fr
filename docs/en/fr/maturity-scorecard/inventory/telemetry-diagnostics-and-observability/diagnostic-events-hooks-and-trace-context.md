---
title: "Observabilité - Note de Maturité de l'Export de Télémétrie"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Observabilité - Note de Maturité de l'Export de Télémétrie

## Résumé

Le bus d'événements de diagnostic est le contrat de télémétrie interne derrière la stabilité, OTEL, Prometheus, les hooks, le chronométrage des appels de modèle et la corrélation des journaux de fichiers. Il est large et soigneusement gardé, mais le catalogue d'événements évolue toujours à mesure que de nouvelles demandes d'observabilité en matière de sécurité de l'IA, de qualité et de plugins apparaissent.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Types d'événements de diagnostic : Types d'événements de diagnostic et limites d'abonnement de confiance/interne/public
- Dispatch asynchrone : Dispatch asynchrone, résumés de saturation de file d'attente, copies d'événements immuables, gestion des données privées et activation des diagnostics
- Création de contexte de trace W3C : Création de contexte de trace W3C, portées de requête actives, spans enfants et formatage de traceparent de confiance
- Exports de diagnostic du runtime du SDK de plugin : Exports de diagnostic du runtime du SDK de plugin et champs de trace du contexte de hook
- Événements de diagnostic d'appel de modèle : Événements de diagnostic d'appel de modèle, outil, exec, webhook, message, Talk, session, harness et exporter.
- Installation du plugin diagnostics-otel : Installation du plugin diagnostics-otel, activation, configuration, remplacements d'env, échantillonnage, intervalle de flush et mode SDK préchargé
- Traces OTLP/HTTP : Traces, métriques et journaux OTLP/HTTP
- Contexte de trace de confiance : Contexte de trace de confiance, propagation de traceparent W3C aux appels de modèle, corrélation des journaux de fichiers, contrôles de capture de contenu et attributs masqués/limités
- Télémétrie du modèle et du runtime : Signaux de santé du modèle, outil, message, session, file d'attente, Talk, exec, webhook, assemblage de contexte, harness et exporter
- Installation du plugin diagnostics-prometheus : Installation du plugin diagnostics-prometheus et activation
- GET /api/diagnostics/prometheus authentifié par passerelle : Comportement, statut et vérification visible par l'opérateur de GET /api/diagnostics/prometheus authentifié par passerelle.
- Exposition de texte Prometheus : Exposition de texte Prometheus, compteurs, jauges, histogrammes, politique d'étiquette, limite de série et métrique de débordement
- Abonnement aux événements de diagnostic de confiance : Abonnement aux événements de diagnostic de confiance et rendu des métriques d'exécution, modèle, outil, message, Talk, file d'attente, session, vivacité, charge utile, mémoire et exporter

## Fonctionnalités

- Types d'événements de diagnostic : Types d'événements de diagnostic et limites d'abonnement de confiance/interne/public
- Dispatch asynchrone : Dispatch asynchrone, résumés de saturation de file d'attente, copies d'événements immuables, gestion des données privées et activation des diagnostics
- Création de contexte de trace W3C : Création de contexte de trace W3C, portées de requête actives, spans enfants et formatage de traceparent de confiance
- Exports de diagnostic du runtime du SDK de plugin : Exports de diagnostic du runtime du SDK de plugin et champs de trace du contexte de hook
- Événements de diagnostic d'appel de modèle : Événements de diagnostic d'appel de modèle, outil, exec, webhook, message, Talk, session, harness et exporter.
- Installation du plugin diagnostics-otel : Installation du plugin diagnostics-otel, activation, configuration, remplacements d'env, échantillonnage, intervalle de flush et mode SDK préchargé
- Traces OTLP/HTTP : Traces, métriques et journaux OTLP/HTTP
- Contexte de trace de confiance : Contexte de trace de confiance, propagation de traceparent W3C aux appels de modèle, corrélation des journaux de fichiers, contrôles de capture de contenu et attributs masqués/limités
- Télémétrie du modèle et du runtime : Signaux de santé du modèle, outil, message, session, file d'attente, Talk, exec, webhook, assemblage de contexte, harness et exporter
- Installation du plugin diagnostics-prometheus : Installation du plugin diagnostics-prometheus et activation
- GET /api/diagnostics/prometheus authentifié par passerelle : Comportement, statut et vérification visible par l'opérateur de GET /api/diagnostics/prometheus authentifié par passerelle.
- Exposition de texte Prometheus : Exposition de texte Prometheus, compteurs, jauges, histogrammes, politique d'étiquette, limite de série et métrique de débordement
- Abonnement aux événements de diagnostic de confiance : Abonnement aux événements de diagnostic de confiance et rendu des métriques d'exécution, modèle, outil, message, Talk, file d'attente, session, vivacité, charge utile, mémoire et exporter

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (82%)`
- Signaux positifs : Le bus d'événements, le contexte de trace, les exports du SDK de plugin, les événements d'appel de modèle, la propagation de trace de hook et les consommateurs d'exporter ont des tests ciblés.
- Signaux négatifs : La couverture est répartie sur de nombreux producteurs et consommateurs, donc chaque nouvelle famille d'événements nécessite des vérifications explicites de fumée et de masquage.
- Lacunes d'intégration : Les traces de hook de plugin tiers et la propagation de trace de fournisseur de bout en bout nécessitent plus de preuves de scénario reproductible.

## Score de Qualité

- Score : `Beta (78%)`
- Rapports Gitcrawl : Le problème #82548 demande plus d'événements d'observabilité en matière de sécurité de l'IA et de qualité, ce qui implique que l'inventaire des événements n'est pas encore final.
- Rapports Discrawl : Les résumés d'archive appellent le bus d'événements de diagnostic la source de vérité et mentionnent des corrections de suivi pour les métriques Talk, la limitation des étiquettes de message, les diagnostics de manifeste et les diagnostics de statut inaccessible.
- Bonnes qualités : Le bus isole les défaillances d'écouteur, garde la récursion, gèle les contextes de trace, sépare les métadonnées de confiance/privée et supprime les événements à haut volume de manière asynchrone avec des résumés limités.
- Mauvaises qualités : La croissance de la taxonomie des événements peut créer une ambiguïté pour l'opérateur à moins que la documentation, les exportateurs et les contrôles de confidentialité restent alignés.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution ne sont comptées que sous Couverture, pas Qualité.

## Score de Complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telemetry-diagnostics-and-observability.md`.
- Signaux positifs : Les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les types d'événements de diagnostic, le dispatch asynchrone, la création de contexte de trace W3C, les exports de diagnostic du runtime du SDK de plugin, les événements de diagnostic d'appel de modèle, l'installation du plugin diagnostics-otel, les traces OTLP/HTTP, le contexte de trace de confiance, la télémétrie du modèle et du runtime, l'installation du plugin diagnostics-prometheus, GET /api/diagnostics/prometheus authentifié par passerelle, l'exposition de texte Prometheus, l'abonnement aux événements de diagnostic de confiance.
- Signaux négatifs : La note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Les conseils publics pour les auteurs de plugins n'énumèrent pas encore chaque famille d'événements de diagnostic et limite de confidentialité en un seul endroit.
- Les demandes de signaux de sécurité de l'IA et de qualité doivent être réconciliées avec le modèle d'événements de diagnostics existant.

## Preuves

### Docs

- `docs/plugins/hooks.md` documente les champs de contexte de hook incluant `ctx.trace`, `ctx.traceId`, `ctx.spanId` et `ctx.parentSpanId`.
- `docs/gateway/opentelemetry.md` explique les événements de diagnostic comme des enregistrements en processus structurés et décrit le `traceparent` de fournisseur de confiance.
- `docs/logging.md` documente la corrélation de trace via les journaux de fichiers et les événements de diagnostic.
- `docs/plugins/sdk-subpaths.md` énumère `plugin-sdk/diagnostic-runtime` et `plugin-sdk/logging-core`.

### Source

- `src/infra/diagnostic-events.ts` définit les types d'événements, le dispatch, les métadonnées de confiance, les données privées, le comportement de la file d'attente asynchrone, l'activation des diagnostics et les abonnés.
- `src/infra/diagnostic-trace-context.ts` implémente l'analyse du contexte de trace W3C, le formatage, les portées asynchrones actives et les contextes enfants.
- `src/plugin-sdk/diagnostic-runtime.ts` exporte les aides de diagnostic aux plugins.
- `src/gateway/server-http.ts` et `src/gateway/server/ws-connection/message-handler.ts` créent des portées de trace de requête pour les flux HTTP et WS.
- `src/agents/embedded-agent-runner/run/attempt.model-diagnostic-events.ts` émet des événements de diagnostic d'appel de modèle de confiance et `traceparent` de fournisseur.

### Tests d'intégration

- `src/agents/agent-tools.before-tool-call.e2e.test.ts` et `src/agents/agent-tools.before-tool-call.integration.e2e.test.ts` capturent les événements de diagnostic autour des hooks d'outil.
- `src/gateway/server-http.request-trace.test.ts` exerce les portées de trace de requête via la gestion HTTP de la passerelle.
- `scripts/qa-otel-smoke.ts` valide les traces exportées et les vérifications de fuite à partir des événements de diagnostic.

### Tests unitaires

- `src/infra/diagnostic-events.test.ts` couvre le séquençage des événements, l'isolation des écouteurs, la confiance/provenance, les copies immuables, les files d'attente asynchrones, les résumés de suppression, les données privées, les diagnostics désactivés et les gardes de récursion.
- `src/infra/diagnostic-trace-context.test.ts` couvre l'analyse/formatage de traceparent, les entrées malformées, les contextes enfants, le gel et la propagation de portée asynchrone.
- `src/agents/embedded-agent-runner/run/attempt.model-diagnostic-events.test.ts` couvre l'émission d'événements d'appel de modèle et la propagation de traceparent de confiance.

### Requêtes Gitcrawl

Requête :

`gitcrawl search --json openclaw/openclaw --query "diagnostic events trace context plugin hooks telemetry" --limit 5`

Résultats :

- 1 résultat. Le problème #82548 référence le contexte de trace manquant pour l'observabilité dans les hooks de plugin et les diagnostics de qualité de réponse dans le cadre des événements d'observabilité de sécurité de l'IA et de qualité demandés.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "diagnostic events trace context plugin hooks telemetry"`

Résultats :

- 1 résultat. L'archive résume le bus d'événements de diagnostic comme la source de vérité pour les appels de modèle, l'exécution d'outil, les processus exec, le flux de message, la livraison sortante, les hooks, la mémoire, le cycle de vie du harness, les files d'attente, les sessions et la récupération, avec le contexte de trace porté via les hooks et les appels de fournisseur.
