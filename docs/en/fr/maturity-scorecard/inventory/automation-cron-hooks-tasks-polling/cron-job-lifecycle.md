---
title: "Automation: cron, hooks, tasks, polling - Cron Jobs Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automation: cron, hooks, tasks, polling - Cron Jobs Maturity Note

## Résumé

La création et la gestion des planifications des tâches cron sont documentées et implémentées dans les points d'entrée CLI, Gateway RPC et agent-tool. Le planificateur supporte les tâches ponctuelles, par intervalle et par expression cron avec contrôles de fuseau horaire et d'échelonnement, ainsi que des fichiers d'état de tâche et d'exécution durables. Le risque principal n'est pas l'absence de fonctionnalités de base ; il s'agit du comportement des cas limites d'état de planification, où les archives montrent des rapports récurrents autour de `nextRunAtMs` non résolu ou obsolète, de suppression de tâches manuelles et du comportement du planificateur lors d'une longue disponibilité.

## Portée de la catégorie

Inclus dans cette catégorie :

- Créer/modifier/supprimer des tâches : Couvre Créer/modifier/supprimer des tâches dans la création de tâches cron, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches cron associé.
- Types de planification : Couvre Types de planification dans la création de tâches cron, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches cron associé.
- Fuseau horaire et échelonnement : Couvre Fuseau horaire et échelonnement dans la création de tâches cron, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches cron associé.
- RPC Cron : Couvre RPC Cron dans la création de tâches cron, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches cron associé.
- Outil cron agent : Couvre Outil cron agent dans la création de tâches cron, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches cron associé.
- Exécutions cron manuelles : Couvre Exécutions cron manuelles dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Exécution cron isolée : Couvre Exécution cron isolée dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Précontrôle modèle/fournisseur : Couvre Précontrôle modèle/fournisseur dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Historique des exécutions : Couvre Historique des exécutions dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Diagnostics de délai d'attente et de refus : Couvre Diagnostics de délai d'attente et de refus dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Livraison d'annonce de chat : Couvre Livraison d'annonce de chat dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et d'alertes d'échec associé.
- Livraison webhook : Couvre Livraison webhook dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et d'alertes d'échec associé.
- Destinations d'échec : Couvre Destinations d'échec dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et d'alertes d'échec associé.
- Alertes d'exécution ignorée : Couvre Alertes d'exécution ignorée dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et d'alertes d'échec associé.
- Aperçus de livraison : Couvre Aperçus de livraison dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et d'alertes d'échec associé.

## Fonctionnalités

- Créer/modifier/supprimer des tâches : Couvre Créer/modifier/supprimer des tâches dans la création de tâches cron, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches cron associé.
- Types de planification : Couvre Types de planification dans la création de tâches cron, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches cron associé.
- Fuseau horaire et échelonnement : Couvre Fuseau horaire et échelonnement dans la création de tâches cron, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches cron associé.
- RPC Cron : Couvre RPC Cron dans la création de tâches cron, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches cron associé.
- Outil cron agent : Couvre Outil cron agent dans la création de tâches cron, l'énumération, l'inspection, la modification et le comportement du cycle de vie des tâches cron associé.
- Exécutions cron manuelles : Couvre Exécutions cron manuelles dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Exécution cron isolée : Couvre Exécution cron isolée dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Précontrôle modèle/fournisseur : Couvre Précontrôle modèle/fournisseur dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Historique des exécutions : Couvre Historique des exécutions dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Diagnostics de délai d'attente et de refus : Couvre Diagnostics de délai d'attente et de refus dans la distribution du planificateur, l'armement du minuteur, les exécutions manuelles/dues, l'exécution isolée de l'agent et le comportement des exécutions cron et diagnostics associé.
- Livraison d'annonce de chat : Couvre Livraison d'annonce de chat dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et d'alertes d'échec associé.
- Livraison webhook : Couvre Livraison webhook dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et d'alertes d'échec associé.
- Destinations d'échec : Couvre Destinations d'échec dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et d'alertes d'échec associé.
- Alertes d'exécution ignorée : Couvre Alertes d'exécution ignorée dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et d'alertes d'échec associé.
- Aperçus de livraison : Couvre Aperçus de livraison dans les modes de livraison de sortie cron, la résolution de cible de canal, les tentatives de livraison directe, la mise en miroir de transcription et le comportement de livraison cron et d'alertes d'échec associé.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (85%)`
- Signaux positifs : Les chemins CLI, Gateway RPC et agent-tool partagent la normalisation via `src/cron/normalize.ts` et `src/gateway/server-methods/cron.ts` ; une couverture unitaire ciblée existe pour l'analyse de planification, les options de planification, la migration de magasin, la réparation de `nextRunAtMs`, l'échelonnement en haut de l'heure, la pagination de liste et les exécutions manuelles.
- Signaux négatifs : La couverture est la plus forte au niveau unitaire et au niveau de service ciblé ; les preuves trouvées montrent moins de preuves de bout en bout que les flux créer/modifier/exécuter survivent à une longue disponibilité de la passerelle, aux magasins édités manuellement et à la parité UI/CLI/agent-tool dans un scénario.
- Lacunes d'intégration : Aucun scénario en direct/e2e unique n'a été trouvé qui démarre une vraie Gateway, crée les trois types de planification via différentes surfaces utilisateur, redémarre la Gateway et prouve que les mêmes tâches persistées calculent toujours la prochaine exécution correcte.

## Score de qualité

- Score : `Beta (78%)`
- Rapports Gitcrawl : Les threads ouverts incluent PR #52109 pour les lacunes de refeu de planification `every` haute fréquence, issue #81691 pour la réparation de créneau futur à la seconde exacte, PR #75970 pour les tâches persistées malformées, issue #83538 pour la perte de données `deleteAfterRun` d'exécution manuelle et issue #73166 pour l'arrêt du planificateur lors d'une longue disponibilité.
- Rapports Discrawl : L'archive Discord montre une confusion des opérateurs autour des lignes cron de session principale qui semblaient activées mais avaient `lastError: "disabled"`, plus une discussion d'examen sur les boucles de refeu de prochaine exécution non résolues et les erreurs de planification laissant les minuteurs inactifs.
- Bonnes qualités : La source a une limite de service claire, la validation du schéma avant la mutation de service, une division fichier de tâche/état, la validation d'horodatage, le suivi de l'identité de planification et des docs explicites pour le fuseau horaire, le comportement OU jour du mois/jour de la semaine, l'échelonnement et la gestion des fichiers d'état.
- Mauvaises qualités : Le dossier de bogues vécu montre que la réparation d'état de planification reste subtile et la sémantique d'exécution manuelle/suppression peut surprendre les opérateurs. La qualité est limitée par ces cas limites opérationnels, pas par l'inventaire de tests.
- Exclu de la qualité : L'inventaire de tests et la profondeur de preuve d'exécution ; ils sont des entrées de couverture uniquement.

## Score de complétude

- Score : `Stable (85%)`
- Instructions de surface : évaluées par rapport à `references/completeness/automation-cron-hooks-tasks-polling.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Créer/modifier/supprimer des tâches, Types de planification, Fuseau horaire et échelonnement, RPC Cron, Outil cron agent, Exécutions cron manuelles, Exécution cron isolée, Précontrôle modèle/fournisseur, Historique des exécutions, Diagnostics de délai d'attente et de refus, Livraison d'annonce de chat, Livraison webhook, Destinations d'échec, Alertes d'exécution ignorée, Aperçus de livraison.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du dossier de lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Un scénario unique face à l'opérateur devrait couvrir la création de tâches `at`, `every` et `cron` via les chemins CLI/Gateway/agent-tool, la modification des métadonnées de non-planification, la préservation/réparation d'état, le redémarrage de la Gateway et l'exécution manuelle d'une tâche due et non-due.
- La sémantique d'exécution manuelle a besoin d'une meilleure visibilité pour l'opérateur autour de `deleteAfterRun` et des vérifications de non-opération dues.
- La réparation d'état de planification devrait rester un foyer de régression car plusieurs entrées d'archive se regroupent autour de la corruption de `nextRunAtMs`, des valeurs zéro, des planifications non résolues et de l'identité de créneau à la seconde exacte.

## Preuves

### Docs

- `docs/automation/cron-jobs.md` documente la persistance des tâches à `~/.openclaw/cron/jobs.json`, l'état d'exécution dans `jobs-state.json`, les types de planification, le fuseau horaire, l'échelonnement, l'exécution manuelle, l'historique d'exécution et les commandes de gestion.
- `docs/cli/cron.md` fournit la référence CLI pour `openclaw cron add`, `list`, `get`, `show`, `edit`, `run`, `runs` et `remove`.
- `docs/gateway/protocol.md` énumère les RPC d'automatisation incluant `cron.get`, `cron.list`, `cron.status`, `cron.add`, `cron.update`, `cron.remove`, `cron.run` et `cron.runs`.

### Source

- `src/gateway/server-methods/cron.ts` implémente les méthodes Gateway validées pour `cron.list`, `cron.add`, `cron.update`, `cron.remove`, `cron.run` et `cron.runs`.
- `src/cli/cron-cli/register.cron-add.ts`, `src/cli/cron-cli/register.cron-edit.ts`, `src/cli/cron-cli/schedule-options.ts` et `src/cli/cron-cli/shared.ts` implémentent l'analyse des drapeaux CLI, la construction de planification et l'affichage.
- `src/agents/tools/cron-tool.ts` expose l'outil cron de l'agent, récupère les paramètres plats dans les objets de tâche, gère l'introspection d'auto-portée et appelle les méthodes cron de la Gateway.
- `src/cron/normalize.ts`, `src/cron/schedule.ts`, `src/cron/stagger.ts`, `src/cron/service/jobs.ts`, `src/cron/service/ops.ts` et `src/cron/service/store.ts` normalisent, calculent, persistent et mutent les tâches.

### Tests d'intégration

- `test/gateway.multi.e2e.test.ts` offre une couverture e2e gateway large mais pas spécifique à tous les chemins de gestion de planification cron.
- `src/gateway/tools-invoke-http.cron-regression.test.ts` exerce cron via l'invocation d'outil Gateway.
- `src/cron/cron-protocol-conformance.test.ts` et `src/cron/cron-protocol-schema.test.ts` exercent la forme et la compatibilité du protocole.

### Tests unitaires

- `src/cron/schedule.test.ts`, `src/cron/parse.test.ts`, `src/cron/normalize.test.ts`, `src/cron/stagger.test.ts` et `src/cron/validate-timestamp.ts` couvrent l'analyse et la normalisation de la planification.
- `src/cron/service.jobs.test.ts`, `src/cron/service.jobs.top-of-hour-stagger.test.ts`, `src/cron/service.issue-regressions.test.ts`, `src/cron/service.store-load-invalid-main-job.test.ts` et `src/cron/service/ops.test.ts` couvrent la création de tâches, la mutation, la réparation et le comportement du magasin.
- `src/cli/cron-cli/register.cron-simple.test.ts`, `src/cli/cron-cli/register.cron-edit.test.ts`, `src/cli/cron-cli/shared.test.ts` et `src/agents/tools/cron-tool.schema.test.ts` couvrent les surfaces CLI et outil-agent.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "cron add schedule nextRunAtMs" --json --limit 5`

Résultats :

- PR #52109, `fix(cron): apply MIN_REFIRE_GAP_MS to every-schedule jobs`, signale un risque de refire de planification `every` haute fréquence.
- Issue #81691, `Cron future-slot repair misclassifies exact second cron slots`, signale un problème de réparation d'état de créneau exact-seconde.
- PR #75970, `fix(cron): ignore malformed persisted jobs`, pointe vers la gestion des tâches persistées malformées.
- Issue #83538, `cron: deleteAfterRun fires on manual run even when no run executes`, signale un risque de perte de données lors d'exécution manuelle.
- Issue #73166, `Cron scheduler silently stops firing after ~2.5 days of gateway uptime`, signale une défaillance de planification après une longue durée de fonctionnement.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "cron add schedule nextRunAtMs"`

Résultats :

- Discussion PR #66083 : les résultats `computeJobNextRunAtMs` non résolus causaient précédemment des boucles de refire ; le correctif actuel ajoute un comportement de réveil de maintenance pour les tâches activées sans exécution suivante.
- Discussion PR #63507 : `nextRunAtMs=0` sur les modifications sans planification requérait une réparation.
- Thread utilisateur `Triggering main to do something in a cron.` inclut une tâche cron de session main concrète qui n'a pas été exécutée et a montré `lastError: "disabled"`.
- Commentaire d'examen sur PR #52619 avertit que les erreurs de calcul de planification pourraient laisser une tâche activée sans minuteur armé.
