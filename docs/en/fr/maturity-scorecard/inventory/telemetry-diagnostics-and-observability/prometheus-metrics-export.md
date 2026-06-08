---
title: "Observabilité - Note de Maturité de l'Export de Métriques Prometheus"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Observabilité - Note de Maturité de l'Export de Métriques Prometheus

## Résumé

L'exportateur Prometheus est un plugin de métriques basé sur le pull, ciblé, avec une route de passerelle protégée, des étiquettes de faible cardinalité, un plafond de séries strict, et une couverture large des métriques run/model/tool/message/Talk/queue/session/memory/exporter. Il est plus jeune que les surfaces de journalisation locale et doctor, mais sa conception en matière de confidentialité et de cardinalité est solide.

## Portée de la Catégorie

- Installation et activation du plugin `diagnostics-prometheus`.
- `GET /api/diagnostics/prometheus` authentifié par passerelle.
- Exposition de texte Prometheus, compteurs, jauges, histogrammes, politique d'étiquettes, plafond de séries, et métrique de débordement.
- Abonnement aux événements de diagnostic de confiance et rendu des métriques run, model, tool, message, Talk, queue, session, liveness, payload, memory, et exporter.

## Fonctionnalités

- Installation du plugin diagnostics-prometheus : installation et activation du plugin diagnostics-prometheus
- GET /api/diagnostics/prometheus authentifié par passerelle : comportement, statut et vérification visible par l'opérateur de GET /api/diagnostics/prometheus.
- Exposition de texte Prometheus : exposition de texte Prometheus, compteurs, jauges, histogrammes, politique d'étiquettes, plafond de séries, et métrique de débordement
- Abonnement aux événements de diagnostic de confiance : abonnement aux événements de diagnostic de confiance et rendu des métriques run, model, tool, message, Talk, queue, session, liveness, payload, memory, et exporter

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (78%)`
- Signaux positifs : L'exportateur dispose de tests unitaires, de documentation, de référence de plugin, d'identifiants de scénario QA-lab, et de preuves d'archive Discord de planification de smoke source-checkout.
- Signaux négatifs : La preuve directe de scrape Prometheus réel est moins visible que la preuve de smoke OTEL.
- Lacunes d'intégration : La route de scrape protégée devrait faire partie d'un smoke Prometheus docker récurrent avec assertions d'authentification et de cardinalité.

## Score de Qualité

- Score : `Stable (80%)`
- Rapports Gitcrawl : La requête de fonctionnalité exacte n'a retourné aucun résultat gitcrawl, donc le silence de l'archive est neutre après les vérifications de fraîcheur.
- Rapports Discrawl : L'archive identifie positivement le point de terminaison protégé, le plafond de 2048 séries, la politique de faible cardinalité, et le travail de confidentialité/cardinalité, avec des notes de version pointant vers `feat(diagnostics-prometheus): add protected metrics exporter`.
- Bonnes qualités : La route utilise l'authentification de passerelle, supprime les diagnostics émis par les plugins non fiables, limite les étiquettes, masque les valeurs, supprime les identifiants de forme session, et signale les séries supprimées.
- Mauvaises qualités : Le runbook public suppose toujours que l'opérateur sait comment fournir l'authentification de passerelle à Prometheus et comment agir sur le débordement de cardinalité.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, live et runtime-flow ne sont comptabilisées que sous Couverture, pas sous Qualité.

## Score de Complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telemetry-diagnostics-and-observability.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'installation du plugin diagnostics-prometheus, GET /api/diagnostics/prometheus authentifié par passerelle, exposition de texte Prometheus, abonnement aux événements de diagnostic de confiance.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Aucun tableau de bord d'exemple ou pack d'alerte archivé n'existe pour les recettes PromQL documentées.
- La configuration d'authentification Prometheus réelle pourrait bénéficier de plus d'exemples testés au-delà de l'extrait de documentation.

## Preuves

### Documentation

- `docs/gateway/prometheus.md` documente la route protégée, le flux d'installation/activation, la configuration de scrape, les métriques exportées, la politique d'étiquettes, le plafond de séries, les recettes PromQL, et le choix entre Prometheus et OTEL.
- `docs/plugins/reference/diagnostics-prometheus.md` documente la page de référence du plugin.

### Source

- `extensions/diagnostics-prometheus/index.ts` enregistre le service et la route `/api/diagnostics/prometheus` authentifiée par passerelle.
- `extensions/diagnostics-prometheus/src/service.ts` implémente le magasin de métriques, le rendu de texte, les étiquettes de faible cardinalité, le plafond de 2048 séries, le filtrage des événements de confiance, le mappage événement-à-métrique, et les événements de diagnostic de l'exportateur.

### Tests d'intégration

- `extensions/qa-lab/src/scenario-packs.ts` définit `docker-prometheus-smoke` dans le pack de scénario smoke diagnostics source-checkout.
- `extensions/qa-lab/src/coverage-report.test.ts` affirme que la couverture smoke d'observabilité inclut `telemetry.prometheus`.

### Tests unitaires

- `extensions/diagnostics-prometheus/src/service.test.ts` couvre les métriques run de confiance, les suppressions d'événements non fiables, la limitation des étiquettes, les métriques messaging/session/Talk/recovery, les plafonds de séries, et le rendu de texte de scrape.
- `src/wizard/setup.official-plugins.test.ts` inclut les choix de configuration de plugin officiel pour `diagnostics-prometheus`.

### Requêtes Gitcrawl

Requête :

`gitcrawl search --json openclaw/openclaw --query "diagnostics prometheus metrics exporter" --limit 5`

Résultats :

- 0 résultat retourné pour la requête de fonctionnalité exacte.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "diagnostics prometheus metrics exporter"`

Résultats :

- 5 résultats. Les résultats résument `GET /api/diagnostics/prometheus`, authentification de passerelle, plafond de 2048 séries, étiquettes de faible cardinalité, métriques run/model/tool/message/Talk/queue/session/memory/exporter, notes de version freshbits pour `feat(diagnostics-prometheus): add protected metrics exporter`, et fermeture du support des métriques/observabilité tel qu'implémenté.
