---
title: "Observabilité - Note de Maturité de l'Export OpenTelemetry"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Observabilité - Note de Maturité de l'Export OpenTelemetry

## Résumé

L'exportateur OpenTelemetry est un plugin de diagnostics de première classe qui transforme les événements de diagnostics OpenClaw de confiance en traces, métriques et logs OTLP/HTTP. Il dispose d'une documentation solide, d'une configuration, de contrôles de confidentialité, de propagation du contexte de trace, d'un support des métriques GenAI et d'un harnais de test QA. Il évolue encore rapidement et dispose d'une demande ouverte pour des événements d'observabilité supplémentaires en matière de sécurité IA et de qualité.

## Portée de la Catégorie

- Installation du plugin `diagnostics-otel`, activation, configuration, remplacements d'env, échantillonnage, intervalle de vidage et mode SDK préchargé.
- Traces, métriques et logs OTLP/HTTP.
- Contexte de trace de confiance, propagation W3C `traceparent` vers les appels de modèle, corrélation des logs de fichier, contrôles de capture de contenu et attributs redactés/limités.
- Signaux de modèle, outil, message, session, file d'attente, Talk, exec, webhook, assemblage de contexte, harnais et santé de l'exportateur.

## Fonctionnalités

- Installation du plugin diagnostics-otel : installation du plugin diagnostics-otel, activation, configuration, remplacements d'env, échantillonnage, intervalle de vidage et mode SDK préchargé
- Traces OTLP/HTTP : traces, métriques et logs OTLP/HTTP
- Contexte de trace de confiance : contexte de trace de confiance, propagation W3C traceparent vers les appels de modèle, corrélation des logs de fichier, contrôles de capture de contenu et attributs redactés/limités
- Télémétrie du modèle et du runtime : signaux de modèle, outil, message, session, file d'attente, Talk, exec, webhook, assemblage de contexte, harnais et santé de l'exportateur

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (83%)`
- Signaux positifs : L'exportateur dispose de tests unitaires, d'un harnais de test QA OTLP dédié, de tests de fixture et de documentation pour le comportement exact des métriques/spans/logs.
- Signaux négatifs : Les permutations de collecteur/backend sont larges et la preuve de version est plus forte pour le récepteur OTLP local et les chemins SDK simulés que pour chaque backend réel.
- Lacunes d'intégration : Le test récurrent devrait inclure un vrai collecteur plus des tableaux de bord/alertes représentatifs pour les traces, métriques et logs.

## Score de Qualité

- Score : `Beta (78%)`
- Rapports Gitcrawl : Le problème #82548 demande des événements d'observabilité supplémentaires en matière de sécurité IA et de qualité, montrant que l'inventaire des événements de télémétrie attendus évolue toujours.
- Rapports Discrawl : Les résumés d'archives Discord décrivent le pipeline OTEL comme récemment déployé et réparti sur plusieurs commits, avec des correctifs de suivi jusqu'à début mai.
- Bonnes qualités : Le plugin supprime les identifiants de haute cardinalité, redacte les attributs, contrôle la capture de contenu, gère les protocoles non supportés, signale la santé de l'exportateur et empêche la propagation de traceparent non fiable.
- Mauvaises qualités : Le catalogue d'événements est toujours en expansion et les opérateurs ont besoin d'une orientation plus claire sur « quoi inspecter en premier » pour les vrais backends OTEL.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux runtime ne sont comptées que sous Couverture, pas sous Qualité.

## Score de Complétude

- Score : `Stable (83%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telemetry-diagnostics-and-observability.md`.
- Signaux positifs : les archives de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'installation du plugin diagnostics-otel, les traces OTLP/HTTP, le contexte de trace de confiance, la télémétrie du modèle et du runtime.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Aucun pack de tableau de bord public ou ligne de base d'alerte n'est documenté aux côtés de l'exportateur.
- Les demandes d'événements de sécurité IA et de qualité indiquent que le catalogue de signaux n'est pas encore stabilisé.

## Preuves

### Documentation

- `docs/gateway/opentelemetry.md` documente l'export OTLP/HTTP, les signaux, les variables de configuration/env, la confidentialité/capture de contenu, l'échantillonnage, les métriques, les traces, les logs et la corrélation de trace.
- `docs/plugins/reference/diagnostics-otel.md` documente la page de référence du plugin.
- `docs/logging.md` documente les champs de corrélation de trace et les champs de taille/timing d'appel de modèle qui alimentent OTEL.

### Source

- `extensions/diagnostics-otel/index.ts` enregistre le service du plugin.
- `extensions/diagnostics-otel/src/service.ts` configure le SDK OpenTelemetry/exportateurs, les points de terminaison de signaux, l'échantillonnage, le mode SDK préchargé, la capture de contenu, le mappage métrique/span/log, les attributs de faible cardinalité et les événements de diagnostics de l'exportateur.
- `src/infra/diagnostic-events.ts` et `src/infra/diagnostic-trace-context.ts` définissent les événements de diagnostics et le contexte de trace.
- `src/agents/embedded-agent-runner/run/attempt.model-diagnostic-events.ts` émet les événements d'appel de modèle et le `traceparent` du fournisseur de confiance.

### Tests d'intégration

- `scripts/qa-otel-smoke.ts` exécute un récepteur OTLP local ou un vrai Collecteur OpenTelemetry et valide les traces, métriques, logs, limites de charge utile et vérifications de fuite de contenu.
- `test/scripts/qa-otel-smoke.test.ts` teste le harnais de test.
- `extensions/qa-lab/src/scenario-packs.ts` définit `otel-trace-smoke` comme faisant partie des scénarios de test de diagnostics de source-checkout.

### Tests unitaires

- `extensions/diagnostics-otel/src/service.test.ts` couvre le démarrage du service, les points de terminaison, le comportement du SDK préchargé, les erreurs d'exportateur, le mappage métrique/span/log, les signaux de récupération de session, la redaction et les contrôles de contenu.
- `src/infra/diagnostic-events.test.ts` et `src/infra/diagnostic-trace-context.test.ts` couvrent la distribution de diagnostics, la confiance, les files d'attente asynchrones et le contexte de trace W3C.
- `src/agents/embedded-agent-runner/run/attempt.model-diagnostic-events.test.ts` couvre la propagation de traceparent d'appel de modèle de confiance et les événements de diagnostics.

### Requêtes Gitcrawl

Requête :

`gitcrawl search --json openclaw/openclaw --query "diagnostics otel opentelemetry trace context metrics spans" --limit 5`

Résultats :

- 1 résultat. Le problème #82548 demande des événements d'observabilité de sécurité IA et de qualité et référence les logs JSONL existants, la corrélation de trace, les événements de diagnostics, l'export OpenTelemetry, les métriques de token/coût, le timing d'appel de modèle, les spans d'exécution d'outil et les signaux de file d'attente.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "diagnostics otel opentelemetry trace context metrics spans"`

Résultats :

- 3 résultats. L'archive résume un pipeline diagnostics-vers-OTEL/Prometheus qui a été déployé autour du 24-26 avril, incluant le contexte de trace via des hooks, la propagation de traceparent de confiance, les métriques/spans GenAI, les contrôles de capture de contenu optionnels, les diagnostics de santé de l'exportateur et les correctifs de suivi.
