---
title: "Automatisation : cron, hooks, tâches, polling - Note de Maturité des Tâches de Fond et des Flux"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automatisation : cron, hooks, tâches, polling - Note de Maturité des Tâches de Fond et des Flux

## Résumé

Le registre des tâches de fond est bien spécifié et implémenté : il suit les tâches ACP détachées, les sous-agents, cron, CLI et médias ; persiste l'état SQLite ; réconcilie le support d'exécution ; expose les méthodes CLI et Gateway ; gère les notifications terminales ; et inclut l'audit/maintenance. La qualité est limitée par les cas limites de redémarrage/tâches perdues et la confusion des opérateurs sur la différence entre les enregistrements de tâches et l'exécution durable.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Liste/affichage/annulation de tâches : Couvre la liste/affichage/annulation de tâches dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre des tâches de fond associé.
- Notifications de tâches : Couvre les notifications de tâches dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre des tâches de fond associé.
- Audit et maintenance des tâches : Couvre l'audit et la maintenance des tâches dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre des tâches de fond associé.
- Tableau des tâches de chat : Couvre le tableau des tâches de chat dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre des tâches de fond associé.
- Statut de pression des tâches : Couvre le statut de pression des tâches dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre des tâches de fond associé.
- Flux gérés : Couvre les flux gérés dans les modes flux gérés et mirrorés, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire et le comportement du flux de tâches associé.
- Flux mirrorés : Couvre les flux mirrorés dans les modes flux gérés et mirrorés, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire et le comportement du flux de tâches associé.
- Flux de tâches openclaw : Couvre le flux de tâches openclaw dans les modes flux gérés et mirrorés, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire et le comportement du flux de tâches associé.
- Audit et maintenance des flux : Couvre l'audit et la maintenance des flux dans les modes flux gérés et mirrorés, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire et le comportement du flux de tâches associé.
- Plugin managedFlows : Couvre le plugin managedFlows dans les modes flux gérés et mirrorés, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire et le comportement du flux de tâches associé.

## Fonctionnalités

- Liste/affichage/annulation de tâches : Couvre la liste/affichage/annulation de tâches dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre des tâches de fond associé.
- Notifications de tâches : Couvre les notifications de tâches dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre des tâches de fond associé.
- Audit et maintenance des tâches : Couvre l'audit et la maintenance des tâches dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre des tâches de fond associé.
- Tableau des tâches de chat : Couvre le tableau des tâches de chat dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre des tâches de fond associé.
- Statut de pression des tâches : Couvre le statut de pression des tâches dans la création de tâches, les transitions d'état, les types d'exécution, l'accès propriétaire/session et le comportement du registre des tâches de fond associé.
- Flux gérés : Couvre les flux gérés dans les modes flux gérés et mirrorés, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire et le comportement du flux de tâches associé.
- Flux mirrorés : Couvre les flux mirrorés dans les modes flux gérés et mirrorés, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire et le comportement du flux de tâches associé.
- Flux de tâches openclaw : Couvre le flux de tâches openclaw dans les modes flux gérés et mirrorés, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire et le comportement du flux de tâches associé.
- Audit et maintenance des flux : Couvre l'audit et la maintenance des flux dans les modes flux gérés et mirrorés, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire et le comportement du flux de tâches associé.
- Plugin managedFlows : Couvre le plugin managedFlows dans les modes flux gérés et mirrorés, la persistance du registre de flux, le suivi des révisions, l'accès limité au propriétaire et le comportement du flux de tâches associé.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (84%)`
- Signaux positifs : Le registre, le magasin, la maintenance, l'audit, la réconciliation, l'accès propriétaire, la livraison, la politique d'exécuteur, le formatage du statut, les méthodes Gateway et les commandes CLI ont tous des tests ciblés.
- Signaux négatifs : La couverture est plus faible pour les scénarios de redémarrage complet où la Gateway est arrêtée pendant les tâches actives, puis réconcilie l'état de support mixte ACP/sous-agent/cron/CLI dans un processus réel.
- Lacunes d'intégration : Un harnais de redémarrage-arrêt devrait créer une tâche par exécution, forcer l'arrêt de la Gateway avant le drainage, redémarrer et prouver les résultats d'audit/maintenance, les notifications de livraison et la rétention du nettoyage.

## Score de Qualité

- Score : `Beta (77%)`
- Rapports Gitcrawl : La PR #59719 suit la vivacité de l'exécution de fond avec les tâches CLI ; le problème #42767 a été fermé après que les tâches actives obsolètes aient obtenu la réconciliation d'état perdu ; le problème #66909 a demandé si les tâches reprennent après le redémarrage de la Gateway ; le problème #42246 demande le regroupement/l'agrégation des notifications sortantes pour les tâches de fond.
- Rapports Discrawl : Les rapports des responsables mentionnent la PR #78575 pour les entrées d'audit de tâches obsolètes après les redémarrages forcés/expirés, et les discussions des utilisateurs conseillent de traiter les tâches/transcriptions OpenClaw comme une piste d'audit d'opérateur plutôt que comme la seule file d'attente de travail durable.
- Bonnes qualités : La documentation indique clairement que les tâches sont des enregistrements, pas des planificateurs ; le registre persiste vers SQLite ; la réconciliation est consciente du runtime ; les lignes terminales sont conservées pendant sept jours ; et la sortie du statut de la tâche assainit le texte du runtime interne.
- Mauvaises qualités : L'enregistrement vécu montre que le comportement de tâche `perdue`, la sémantique de redémarrage et le volume de notification restent difficiles à raisonner pour les utilisateurs.
- Exclu de la qualité : L'inventaire des tests et la profondeur de la preuve d'exécution ; ils sont uniquement des entrées de couverture.

## Score de Complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/automation-cron-hooks-tasks-polling.md`.
- Signaux positifs : les documents archivés, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la liste/affichage/annulation de tâches, les notifications de tâches, l'audit et la maintenance des tâches, le tableau des tâches de chat, le statut de pression des tâches, les flux gérés, les flux mirrorés, le flux de tâches openclaw, l'audit et la maintenance des flux, le plugin managedFlows.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Le comportement de redémarrage doit être résumé dans le statut CLI et la documentation avec un tableau explicite : ce qui peut reprendre, ce qui devient perdu et ce que TaskFlow ajoute.
- L'agrégation ou le regroupement des notifications reste un besoin visible par l'utilisateur pour les déploiements de tâches de fond occupés.
- La maintenance doit rester fortement observable car `perdu` est un signal de récupération normal, pas seulement une erreur.

## Preuves

### Docs

- `docs/automation/tasks.md` explique les sources de tâches, le cycle de vie, les statuts, la livraison, les politiques de notification, l'audit, la maintenance, le chat `/tasks`, l'intégration du statut et le stockage, ainsi que la relation avec cron/heartbeat/Task Flow.
- `docs/automation/index.md` positionne les tâches comme le registre de travail détaché plutôt que comme un planificateur.
- `docs/cli/tasks.md` documente les commandes CLI pour lister, afficher, annuler, notifier, auditer, maintenir et inspecter les flux.

### Source

- `src/tasks/task-registry.ts`, `src/tasks/task-registry.store.ts`, `src/tasks/task-registry.store.sqlite.ts`, `src/tasks/task-registry.reconcile.ts`, `src/tasks/task-registry.audit.ts`, `src/tasks/task-registry.maintenance.ts` et `src/tasks/task-registry.types.ts` implémentent la persistance des tâches, la réconciliation, l'audit et la maintenance.
- `src/tasks/task-executor.ts`, `src/tasks/task-executor-policy.ts`, `src/tasks/task-registry-delivery-runtime.ts` et `src/tasks/task-status.ts` implémentent l'annulation, les notifications, la livraison et le formatage du statut.
- `src/gateway/server-methods/tasks.ts` et `src/commands/tasks.ts` exposent les opérations de tâches Gateway et CLI.

### Tests d'intégration

- `src/gateway/server-methods/tasks.test.ts` couvre les méthodes Gateway pour les tâches.
- `test/scripts/openclaw-test-state.test.ts` exerce un état de test OpenClaw plus large qui inclut la gestion de l'état d'exécution.
- Aucun e2e de redémarrage-arrêt de processus complet sur tous les types d'exécution de tâches n'a été trouvé.

### Tests unitaires

- `src/tasks/task-registry.test.ts`, `src/tasks/task-registry.store.test.ts`, `src/tasks/task-registry.audit.test.ts`, `src/tasks/task-registry.maintenance.issue-60299.test.ts` et `src/tasks/task-registry.process-state.test.ts` couvrent le comportement du registre.
- `src/tasks/task-executor.test.ts`, `src/tasks/task-executor-policy.test.ts`, `src/tasks/detached-task-runtime.test.ts` et `src/tasks/task-status.test.ts` couvrent le comportement de l'exécuteur, de la notification, du runtime et du statut.
- `src/commands/tasks.test.ts`, `src/commands/tasks-json.test.ts` et `src/commands/tasks-audit-system.ts` couvrent le formatage CLI et le comportement d'audit système.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "tasks ledger stale lost maintenance cron subagent" --json --limit 5`

Résultats :

- Aucun résultat pour la requête exacte.

Requête de secours :

`gitcrawl search openclaw/openclaw --query "background tasks lost" --json --limit 5`

Résultats :

- La PR #59719 corrige la vivacité de l'exécution de fond via les tâches CLI.
- Le problème #42767 discute des tâches longues bloquées en cours d'exécution ; le main actuel réconcilie les tâches actives orphelines vers `perdu`.
- Le problème #66909 demande si les tâches reprennent automatiquement après le redémarrage de la Gateway.
- Le problème #42246 demande le regroupement/l'agrégation configurable pour les notifications de tâches de fond sortantes.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "background tasks lost"`

Résultats :

- Les responsables ont demandé l'examen de la PR #78575, décrite comme corrigeant les entrées d'audit de tâches obsolètes en marquant les tâches de fond en cours d'exécution comme perdues lorsque le redémarrage forcé/expiré de la Gateway procède avant la fin du drainage.
- Les discussions des responsables/utilisateurs expliquent que les tâches de fond peuvent devenir `perdues` et recommandent de traiter les tâches/transcriptions OpenClaw comme une piste d'audit d'opérateur, avec Postgres/Redis pour un registre de travail externe durable si nécessaire.
- Le problème #66909 a été fermé après que la documentation ait clarifié que les tâches persistent les enregistrements de suivi mais pas l'état d'exécution.
