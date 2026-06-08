---
title: "Automation: cron, hooks, tasks, polling - Task Flow Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automation: cron, hooks, tasks, polling - Task Flow Maturity Note

## Résumé

Task Flow fournit une orchestration durable au-dessus des tâches de fond individuelles. La source inclut un registre, l'accès propriétaire, l'audit, la maintenance, les API de runtime de plugin, et l'intégration Lobster. Le composant est prometteur mais moins mature que le simple registre de tâches : la documentation explique les concepts, mais les archives montrent que les utilisateurs se demandent toujours comment les flux sont réellement déclenchés et quand choisir TaskFlow, les tâches de fond, cron, ou une file d'attente durable externe.

## Portée de la catégorie

Cette catégorie couvre les modes de flux gérés et en miroir, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire, l'audit/maintenance des flux, les commandes CLI `openclaw tasks flow`, les API de runtime de plugin `managedFlows`, l'intégration de workflow Lobster, l'annulation, et la relation avec cron/tâches de fond.

## Fonctionnalités

- Flux gérés : Couvre les flux gérés dans les modes de flux gérés et en miroir, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire, et le comportement associé du flux de tâches.
- Flux en miroir : Couvre les flux en miroir dans les modes de flux gérés et en miroir, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire, et le comportement associé du flux de tâches.
- openclaw tasks flow : Couvre openclaw tasks flow dans les modes de flux gérés et en miroir, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire, et le comportement associé du flux de tâches.
- Audit et maintenance des flux : Couvre l'audit et la maintenance des flux dans les modes de flux gérés et en miroir, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire, et le comportement associé du flux de tâches.
- Plugin managedFlows : Couvre Plugin managedFlows dans les modes de flux gérés et en miroir, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire, et le comportement associé du flux de tâches.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (73%)`
- Signaux positifs : Le registre, le magasin SQLite, l'accès propriétaire, l'audit, la maintenance, l'API de runtime de plugin, et l'intégration de flux Lobster ont des tests ciblés.
- Signaux négatifs : La couverture est plus mince pour l'exécution réelle de workflows multi-étapes à travers le redémarrage de Gateway, la mise en miroir de tâches externes, l'inspection CLI utilisateur, et les chemins d'approbation/reprise dans un scénario.
- Lacunes d'intégration : Ajouter un flux e2e travaillé : cron déclenche une session persistante, le plugin crée un flux géré avec des tâches enfants, une étape attend l'approbation, Gateway redémarre, et `openclaw tasks flow show` prouve la continuité de l'état et de la révision.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : La PR #68687 achemine le travail d'agent durable via TaskFlow ; le problème #78019 signale `inconsistent_timestamps` ; la PR #60183 améliore la fraîcheur de l'audit TaskFlow ; la PR #61242 améliore l'UX des tâches enfants gérées ; le problème #79038 signale les préoccupations d'autorité de la route-session du webhook `run_task`.
- Rapports Discrawl : Les mainteneurs rapportent que les utilisateurs demandent comment TaskFlow est déclenché ou construit, et recommandent d'ajouter un "hello world" concret avec déclenchement, état, reprise, défaillance, et piste d'audit.
- Bonnes qualités : L'architecture sépare l'orchestration de l'exécution des tâches individuelles, suit les révisions, a l'intention d'annulation, et expose l'accès limité au propriétaire et la maintenance.
- Mauvaises qualités : Le workflow opérationnel est encore sous-documenté, et les rapports d'archives montrent à la fois des lacunes UX et des bugs de cohérence dans l'audit/timestamps/autorité des flux.
- Exclu de la qualité : L'inventaire des tests et la profondeur de la preuve de runtime ; ils sont des entrées de couverture uniquement.

## Score de complétude

- Score : `Beta (73%)`
- Instructions de surface : évaluées par rapport à `references/completeness/automation-cron-hooks-tasks-polling.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour les flux gérés, les flux en miroir, openclaw tasks flow, l'audit et la maintenance des flux, Plugin managedFlows.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Publier un tutoriel TaskFlow concret avec déclenchement, transitions d'état, reprise, défaillance, audit, et relation avec les tâches de fond.
- Renforcer les exemples de redémarrage/reprise pour les flux gérés et les tâches externes en miroir.
- Garder les limites d'autorité explicites pour les tâches créées par webhook et les arbres de session de route.

## Preuves

### Docs

- `docs/automation/taskflow.md` documente Task Flow comme une couche d'orchestration, les modes gérés et en miroir, l'état durable, le suivi des révisions, l'annulation, et les commandes CLI.
- `docs/automation/tasks.md` explique comment les tâches se rapportent à Task Flow et lie `openclaw tasks flow list|show|cancel`.
- `docs/plugins/sdk-runtime.md` référence `api.runtime.tasks.managedFlows` et dit que Task Flow n'est pas lui-même un planificateur.

### Source

- `src/tasks/task-flow-registry.ts`, `src/tasks/task-flow-registry.store.ts`, `src/tasks/task-flow-registry.store.sqlite.ts`, `src/tasks/task-flow-registry.audit.ts`, `src/tasks/task-flow-registry.maintenance.ts`, et `src/tasks/task-flow-registry.types.ts` implémentent le registre de flux.
- `src/tasks/task-flow-owner-access.ts` applique l'accès aux flux limité au propriétaire.
- `src/plugins/runtime/runtime-taskflow.ts` expose les API de runtime de plugin pour les flux gérés.
- `extensions/lobster/src/lobster-taskflow.ts` lie l'exécution de workflow Lobster à Task Flow.
- `src/commands/tasks.ts` implémente les opérations CLI `openclaw tasks flow`.

### Tests d'intégration

- `extensions/lobster/src/lobster-taskflow.test.ts` exerce une intégration de plugin réelle avec l'API Task Flow.
- `src/plugins/runtime/runtime-taskflow.test.ts` exerce le comportement Task Flow du runtime de plugin.
- Aucun e2e complet de redémarrage/reprise de Gateway pour Task Flow n'a été trouvé.

### Tests unitaires

- `src/tasks/task-flow-registry.test.ts`, `src/tasks/task-flow-registry.store.test.ts`, `src/tasks/task-flow-registry.audit.test.ts`, `src/tasks/task-flow-registry.maintenance.test.ts`, et `src/tasks/task-flow-owner-access.test.ts` couvrent le comportement principal de Task Flow.
- `src/tasks/task-registry.maintenance.ts` et `src/commands/tasks.ts` incluent également les chemins de maintenance des flux.
- `src/plugins/runtime/runtime-taskflow.test.ts` couvre la forme et le comportement de l'API de plugin.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "task flow registry managed mirrored tasks flow" --json --limit 5`

Résultats :

- Aucun résultat pour la requête exacte.

Requête de secours :

`gitcrawl search openclaw/openclaw --query "TaskFlow" --json --limit 5`

Résultats :

- La PR #68687 achemine le travail d'agent durable via TaskFlow.
- Le problème #78019 signale `TaskFlow inconsistent_timestamps`.
- La PR #60183 améliore la fraîcheur de l'audit TaskFlow.
- La PR #61242 améliore l'UX des tâches enfants gérées.
- Le problème #79038 signale les problèmes d'autorité du webhook `run_task` autour des arbres de session de route.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "TaskFlow"`

Résultats :

- La discussion mainteneur/utilisateur dit que les utilisateurs demandent comment TaskFlow est réellement déclenché ou construit, et recommandent un hello-world TaskFlow concret avec déclenchement, état, reprise, défaillance, et piste d'audit.
- Le même rapport encadre TaskFlow comme la visibilité du flux durable au-dessus des tâches de fond, avec Postgres/Redis externe toujours préféré pour un registre de travail durable difficile dans les déploiements complexes multi-agents.
