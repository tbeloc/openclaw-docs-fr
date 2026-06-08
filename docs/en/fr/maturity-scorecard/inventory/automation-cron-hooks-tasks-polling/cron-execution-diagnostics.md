---
title: "Automatisation : cron, hooks, tâches, polling - Note de Maturité des Exécutions Cron et des Diagnostics"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automatisation : cron, hooks, tâches, polling - Note de Maturité des Exécutions Cron et des Diagnostics

## Résumé

L'exécution cron dispose d'une implémentation de service mature et d'agent isolé : elle enregistre l'historique des exécutions, mappe les résultats des exécutions, supporte les exécutions manuelles et uniquement dues, applique la sélection de modèle, vérifie l'accessibilité du fournisseur local, enregistre les diagnostics et crée des entrées de registre de tâches. La couverture est large mais surtout ciblée et simulée. La qualité est limitée par les rapports en direct concernant la sémantique de préflight/fallback du modèle et les tâches déterministes longue durée.

## Portée de la Catégorie

Cette catégorie couvre la distribution du planificateur, l'armement des minuteurs, les exécutions manuelles/dues, l'exécution d'agent isolé, l'identité de session, la sélection de modèle, la politique de fallback, le préflight du fournisseur, les délais d'exécution, les diagnostics d'exécution, l'historique des exécutions et la création de registre de tâches. Elle exclut la livraison/les alertes, qui sont évaluées séparément.

## Fonctionnalités

- Exécutions cron manuelles : Couvre les exécutions cron manuelles dans la distribution du planificateur, l'armement des minuteurs, les exécutions manuelles/dues, l'exécution d'agent isolé et le comportement associé des exécutions cron et des diagnostics.
- Exécution cron isolée : Couvre l'exécution cron isolée dans la distribution du planificateur, l'armement des minuteurs, les exécutions manuelles/dues, l'exécution d'agent isolé et le comportement associé des exécutions cron et des diagnostics.
- Préflight modèle/fournisseur : Couvre le préflight modèle/fournisseur dans la distribution du planificateur, l'armement des minuteurs, les exécutions manuelles/dues, l'exécution d'agent isolé et le comportement associé des exécutions cron et des diagnostics.
- Historique des exécutions : Couvre l'historique des exécutions dans la distribution du planificateur, l'armement des minuteurs, les exécutions manuelles/dues, l'exécution d'agent isolé et le comportement associé des exécutions cron et des diagnostics.
- Diagnostics de délai d'attente et de refus : Couvre les diagnostics de délai d'attente et de refus dans la distribution du planificateur, l'armement des minuteurs, les exécutions manuelles/dues, l'exécution d'agent isolé et le comportement associé des exécutions cron et des diagnostics.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (83%)`
- Signaux positifs : Les suites `src/cron/service.*.test.ts` et `src/cron/isolated-agent/*.test.ts` couvrent la distribution, le réarmement des minuteurs, la récupération au redémarrage, les remplacements de modèle, la politique de fallback, le préflight du modèle local, les diagnostics d'exécution, la politique de délai d'attente, la propagation du statut d'erreur méta, l'isolation des clés de session et la création de registre de tâches.
- Signaux négatifs : Le composant dispose de moins de preuves en direct/e2e pour les blocages réels du fournisseur, les redémarrages réels de Gateway pendant les exécutions isolées actives et la supervision des processus déterministes longue durée via le chemin d'outil intégré.
- Lacunes d'intégration : Un scénario en direct devrait prouver une exécution isolée due via une Gateway réelle, un saut de préflight de modèle, un délai d'attente, un `cron.run --wait` manuel et une récupération durable de `cron.runs` après redémarrage.

## Score de Qualité

- Score : `Beta (73%)`
- Rapports Gitcrawl : Le problème #79329 signale que le préflight du modèle cron saute une exécution entière quand un primaire local est inaccessible au lieu d'essayer les fallbacks cloud configurés.
- Rapports Discrawl : Un fil de discussion mainteneur/utilisateur du 17 mai décrit un travail cron déterministe longue durée où la propriété du shell native Codex peut se terminer avant qu'OpenClaw ne reçoive la sortie de la commande ; le modèle recommandé est les outils OpenClaw intégrés avec `exec` plus `process` polling et un `timeoutSeconds` adéquat.
- Bonnes qualités : Les chemins d'exécution séparent les événements système de session principale des tâches `agentTurn` isolées/actuelles/personnalisées, appliquent les listes blanches de modèle avant le démarrage du runner, persistent les journaux d'exécution et les diagnostics et classifient les états ignorés/erreur/délai d'attente au lieu de traiter chaque réponse d'assistant comme un succès.
- Mauvaises qualités : Le préflight du fournisseur et la propriété des processus longue durée restent sensibles à l'opérateur. Le runtime dispose de nombreuses protections, mais le modèle opérationnel nécessite toujours que les utilisateurs choisissent le bon chemin d'exécution d'agent/outil pour le travail shell déterministe.
- Exclu de la qualité : L'inventaire des tests et la profondeur de la preuve runtime ; ils sont uniquement des entrées de couverture.

## Score de Complétude

- Score : `Stable (83%)`
- Instructions de surface : évaluées par rapport à `references/completeness/automation-cron-hooks-tasks-polling.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les exécutions cron manuelles, l'exécution cron isolée, le préflight modèle/fournisseur, l'historique des exécutions et les diagnostics de délai d'attente et de refus.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Le préflight du modèle devrait s'aligner avec les attentes de fallback ou rendre le comportement de saut primaire strict incontestable pour les opérateurs.
- Le travail déterministe longue durée a besoin d'un modèle de première classe plus clair ou de docs plus fortes qui distinguent l'orchestration d'agent-turn de l'exécution déterministe.
- Une preuve de reprise au redémarrage pour les exécutions cron isolées actives réduirait l'incertitude autour du comportement de délai d'attente et de réconciliation de tâches.

## Preuves

### Docs

- `docs/automation/cron-jobs.md` documente les styles d'exécution, le comportement de session isolée, la précédence modèle/thinking/fallback, le préflight du fournisseur local, la gestion des délais d'attente, l'historique des exécutions et le `cron run --wait` manuel.
- `.mem/main/ref/cron-run-diagnostics.md` et `.mem/main/pkg/claw/flow/cron-run-diagnostics.md` décrivent les attentes de diagnostic et le contexte de réparation récent pour les défaillances d'exécution cron.
- `docs/automation/tasks.md` indique que chaque exécution cron crée une tâche en arrière-plan et explique la réconciliation d'état perdu spécifique à cron.

### Source

- `src/cron/service/timer.ts`, `src/cron/service/ops.ts`, `src/cron/service/timeout-policy.ts` et `src/cron/service/task-ledger.ts` possèdent la distribution, les exécutions manuelles, la politique de délai d'attente et la création de tâches.
- `src/cron/run-log.ts`, `src/cron/run-diagnostics.ts` et `src/cron/retry-hint.ts` implémentent l'historique d'exécution durable et les résumés de diagnostic.
- `src/cron/isolated-agent/run.ts`, `src/cron/isolated-agent/model-selection.ts`, `src/cron/isolated-agent/model-preflight.runtime.ts`, `src/cron/isolated-agent/run-fallback-policy.ts` et `src/cron/isolated-agent/session-key.ts` implémentent l'exécution d'agent isolé, le choix de modèle, le préflight, les fallbacks et l'identité de session.

### Tests d'intégration

- `src/cron/cron-protocol-conformance.test.ts` couvre le comportement cron au niveau du protocole.
- `src/cron/isolated-agent/model-preflight.runtime.test.ts` exerce le comportement de préflight du fournisseur runtime plutôt que seulement les fonctions pures.
- `src/cron/isolated-agent/run.runtime-plugins.test.ts` exerce l'intégration du plugin runtime pendant les exécutions cron.

### Tests unitaires

- `src/cron/service.restart-catchup.test.ts`, `src/cron/service.rearm-timer-when-running.test.ts`, `src/cron/service.prevents-duplicate-timers.test.ts`, `src/cron/service.every-jobs-fire.test.ts` et `src/cron/service/timeout-policy.test.ts` couvrent la mécanique d'exécution du planificateur.
- `src/cron/isolated-agent/run.cron-model-override.test.ts`, `src/cron/isolated-agent/run.payload-fallbacks.test.ts`, `src/cron/isolated-agent/run.meta-error-status.test.ts`, `src/cron/isolated-agent/run.interim-retry.test.ts`, `src/cron/isolated-agent/run.live-session-model-switch.test.ts` et `src/cron/isolated-agent/run.tools-allow.test.ts` couvrent le comportement d'exécution isolée.
- `src/cron/run-log.test.ts`, `src/cron/run-log.error-reason.test.ts` et `src/cron/run-diagnostics.test.ts` couvrent l'historique des exécutions et les diagnostics.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "cron timeout diagnostics model preflight run history" --json --limit 5`

Résultats :

- Le problème #79329, `Cron model preflight skips entire run when local primary is unreachable, ignoring configured cloud fallbacks [AI]`, est le seul résultat et abaisse directement la qualité pour la sémantique du préflight de modèle.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "cron timeout diagnostics model preflight run history"`

Résultats :

- Aucun message Discord correspondant retourné pour cette requête exacte.

Requête de secours :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "poll loop"`

Résultats :

- La discussion mainteneur/utilisateur du 17 mai recommande l'exécution OpenClaw intégrée avec `exec` plus `process` pour le travail cron déterministe longue durée et avertit que la propriété du shell native Codex peut se terminer avant que le résultat final ne soit observé.
