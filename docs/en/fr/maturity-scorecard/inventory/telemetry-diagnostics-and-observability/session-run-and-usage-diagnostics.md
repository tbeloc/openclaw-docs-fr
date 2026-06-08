---
title: "Observabilité - Note de Maturité des Diagnostics de Session"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Observabilité - Note de Maturité des Diagnostics de Session

## Résumé

Les diagnostics de session, d'exécution et d'utilisation rendent observable le travail d'agent long ou bloqué par le biais d'événements d'état de session, de profondeur de file d'attente, de suivi du travail actif, d'événements de récupération, d'utilisation de jetons/coûts, de chronométrage des appels de modèle et de journaux d'utilisation. Le modèle source est solide, mais l'histoire "ce qui s'est passé avec mon tour" orientée vers l'opérateur est fragmentée entre les journaux, la stabilité, OTEL/Prometheus, les commandes de session et les diagnostics de chat.

## Portée de la Catégorie

Inclus dans cette catégorie :

- session.state : événements diagnostiques session.state, session.stuck, session.long_running, session.stalled, session.recovery.\*, et session.turn.created
- Snapshots d'activité de session diagnostique : Snapshots d'activité de session diagnostique pour les exécutions intégrées, les appels de modèle et les appels d'outil
- Utilisation du modèle : Utilisation du modèle, jetons/coûts, octets/chronométrage des appels de modèle, tentatives d'exécution et journaux d'utilisation
- Export des signaux de session vers la stabilité : Export des signaux de session vers la stabilité, OpenTelemetry et Prometheus

## Fonctionnalités

- session.state : événements diagnostiques session.state, session.stuck, session.long_running, session.stalled, session.recovery.\*, et session.turn.created
- Snapshots d'activité de session diagnostique : Snapshots d'activité de session diagnostique pour les exécutions intégrées, les appels de modèle et les appels d'outil
- Utilisation du modèle : Utilisation du modèle, jetons/coûts, octets/chronométrage des appels de modèle, tentatives d'exécution et journaux d'utilisation
- Export des signaux de session vers la stabilité : Export des signaux de session vers la stabilité, OpenTelemetry et Prometheus

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (82%)`
- Signaux positifs : L'état de session, la récupération de session bloquée, l'activité d'exécution, les mappages d'exportateur et la télémétrie des appels de modèle ont des tests approfondis de style unitaire et intégration.
- Signaux négatifs : Un scénario complet d'utilisateur réel allant d'un tour bloqué au diagnostic de l'opérateur est moins visible que les tests d'événements et d'exportateurs isolés.
- Lacunes d'intégration : La preuve de version devrait inclure une session en file d'attente complète, une exécution intégrée bloquée, une récupération et un chemin de diagnostic de l'opérateur.

## Score de Qualité

- Score : `Beta (78%)`
- Rapports Gitcrawl : La requête exacte n'a retourné aucun résultat direct, donc le silence de l'archive est neutre après les vérifications de fraîcheur.
- Rapports Discrawl : La requête exacte n'a retourné aucun résultat direct ; les résultats d'archive OTEL plus larges citent toujours les métriques de session et de récupération comme des signaux récemment ajoutés.
- Bonnes qualités : L'implémentation distingue le travail long, bloqué et coincé ; suit les types de travail actif ; émet des événements de récupération demandée/complétée ; et évite les identifiants de session bruts dans les exportateurs.
- Mauvaises qualités : L'expérience de l'opérateur est fragmentée car les diagnostics de session apparaissent sur plusieurs surfaces au lieu d'une seule chronologie de diagnostic.
- Exclus de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution sont comptées uniquement sous Couverture, pas Qualité.

## Score de Complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telemetry-diagnostics-and-observability.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour session.state, Snapshots d'activité de session diagnostique, Utilisation du modèle, Export des signaux de session vers la stabilité.
- Signaux négatifs : la note archivée a précédé le score de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Il n'existe pas de runbook public unique qui guide de "mon tour est bloqué" à travers l'état de session, le travail actif, la stabilité, les journaux et les événements de récupération.
- Les seuils de diagnostic de session sont documentés principalement par le biais de documents de diagnostics/export adjacents plutôt que par une page d'opérateur dédiée.

## Preuves

### Docs

- `docs/gateway/opentelemetry.md` documente les métriques de session, file d'attente, session bloquée, récupération, exécution et utilisation.
- `docs/gateway/prometheus.md` documente les métriques Prometheus d'état de session, profondeur de file d'attente, bloqué, récupération, vivacité et tour créé.
- `docs/gateway/diagnostics.md` documente les comptes de session vivacité, actif/en attente/en file d'attente, les spans de phase et les marqueurs de progression stale terminal.
- `docs/gateway/protocol.md` documente `sessions.usage.logs`.

### Source

- `src/logging/diagnostic.ts`, `src/logging/diagnostic-session-state.ts`, `src/logging/diagnostic-run-activity.ts` et `src/logging/diagnostic-session-recovery-coordinator.ts` implémentent l'état de session, le suivi du travail actif, la classification bloquée et les événements de récupération.
- `src/logging/diagnostic-stability.ts` projette les événements de session dans les snapshots de stabilité.
- `extensions/diagnostics-otel/src/service.ts` et `extensions/diagnostics-prometheus/src/service.ts` exportent la télémétrie de session, récupération et utilisation.
- `src/agents/embedded-agent-runner/run/attempt.model-diagnostic-events.ts` enregistre les octets d'appel de modèle, le chronométrage, l'utilisation et le contexte de trace.

### Tests d'intégration

- `src/logging/diagnostic-stuck-session-recovery.integration.test.ts` exerce les flux de récupération de session bloquée.
- `src/agents/agent-tools.before-tool-call.e2e.test.ts` et `src/agents/agent-tools.before-tool-call.integration.e2e.test.ts` exercent les événements diagnostiques pendant les chemins d'appel d'outil réels.
- `scripts/qa-otel-smoke.ts` valide les signaux de session/file d'attente/utilisation exportés dans les charges OTLP.

### Tests unitaires

- `src/logging/diagnostic.test.ts` couvre l'état de session, la profondeur de file d'attente, la progression, la classification bloquée, les seuils et le comportement des événements de récupération.
- `src/logging/diagnostic-run-activity.ts` est couvert par les tests de diagnostic et d'exécuteur d'agent.
- `extensions/diagnostics-otel/src/service.test.ts` et `extensions/diagnostics-prometheus/src/service.test.ts` couvrent le comportement des métriques/export de session bloquée, tour créé et récupération.

### Requêtes Gitcrawl

Requête :

`gitcrawl search --json openclaw/openclaw --query "session usage logs diagnostic run activity embedded agent telemetry" --limit 5`

Résultats :

- 0 résultats retournés pour la requête de fonctionnalité exacte.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "session usage logs diagnostic run activity embedded agent telemetry"`

Résultats :

- 0 résultats retournés pour la requête de fonctionnalité exacte.
