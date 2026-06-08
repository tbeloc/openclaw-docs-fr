---
title: "Automation: cron, hooks, tasks, polling - Automation Hooks Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automation: cron, hooks, tasks, polling - Automation Hooks Maturity Note

## Résumé

Les hooks internes sont une surface d'automatisation d'opérateur utilisable avec documentation, gestion CLI, découverte basée sur les métadonnées, hooks groupés, packs de hooks, précédence workspace/managed et événements de cycle de vie. Les principaux problèmes de maturité sont la clarté de la portée et la surcharge opérationnelle : les utilisateurs demandent toujours des hooks pré-outil de style plugin dans le système de hooks internes, et les rapports d'archive montrent que le comportement bootstrap-extra-files et la surcharge des hooks restent des sources de confusion.

## Portée de la catégorie

Inclus dans cette catégorie :

- Authoring HOOK.md : Couvre l'authoring HOOK.md sur les métadonnées `HOOK.md`, le chargement des handlers, la découverte des hooks bundled/managed/workspace/plugin, la politique d'éligibilité et le comportement des hooks internes associés.
- Découverte des hooks : Couvre la découverte des hooks sur les métadonnées `HOOK.md`, le chargement des handlers, la découverte des hooks bundled/managed/workspace/plugin, la politique d'éligibilité et le comportement des hooks internes associés.
- Gestion CLI des hooks : Couvre la gestion CLI des hooks sur les métadonnées `HOOK.md`, le chargement des handlers, la découverte des hooks bundled/managed/workspace/plugin, la politique d'éligibilité et le comportement des hooks internes associés.
- Packs de hooks : Couvre les packs de hooks sur les métadonnées `HOOK.md`, le chargement des handlers, la découverte des hooks bundled/managed/workspace/plugin, la politique d'éligibilité et le comportement des hooks internes associés.
- Dispatch des événements de cycle de vie : Couvre le dispatch des événements de cycle de vie sur les métadonnées `HOOK.md`, le chargement des handlers, la découverte des hooks bundled/managed/workspace/plugin, la politique d'éligibilité et le comportement des hooks internes associés.
- Enregistrement api.on : Couvre l'enregistrement api.on sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks plugin associés.
- Hooks de politique d'appel d'outil : Couvre les hooks de politique d'appel d'outil sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks plugin associés.
- Hooks de message : Couvre les hooks de message sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks plugin associés.
- Hooks de session/cycle de vie : Couvre les hooks de session/cycle de vie sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks plugin associés.
- Demandes d'approbation de plugin : Couvre les demandes d'approbation de plugin sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks plugin associés.
- cron_changed : Couvre cron_changed sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks plugin associés.

## Fonctionnalités

- Authoring HOOK.md : Couvre l'authoring HOOK.md sur les métadonnées `HOOK.md`, le chargement des handlers, la découverte des hooks bundled/managed/workspace/plugin, la politique d'éligibilité et le comportement des hooks internes associés.
- Découverte des hooks : Couvre la découverte des hooks sur les métadonnées `HOOK.md`, le chargement des handlers, la découverte des hooks bundled/managed/workspace/plugin, la politique d'éligibilité et le comportement des hooks internes associés.
- Gestion CLI des hooks : Couvre la gestion CLI des hooks sur les métadonnées `HOOK.md`, le chargement des handlers, la découverte des hooks bundled/managed/workspace/plugin, la politique d'éligibilité et le comportement des hooks internes associés.
- Packs de hooks : Couvre les packs de hooks sur les métadonnées `HOOK.md`, le chargement des handlers, la découverte des hooks bundled/managed/workspace/plugin, la politique d'éligibilité et le comportement des hooks internes associés.
- Dispatch des événements de cycle de vie : Couvre le dispatch des événements de cycle de vie sur les métadonnées `HOOK.md`, le chargement des handlers, la découverte des hooks bundled/managed/workspace/plugin, la politique d'éligibilité et le comportement des hooks internes associés.
- Enregistrement api.on : Couvre l'enregistrement api.on sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks plugin associés.
- Hooks de politique d'appel d'outil : Couvre les hooks de politique d'appel d'outil sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks plugin associés.
- Hooks de message : Couvre les hooks de message sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks plugin associés.
- Hooks de session/cycle de vie : Couvre les hooks de session/cycle de vie sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks plugin associés.
- Demandes d'approbation de plugin : Couvre les demandes d'approbation de plugin sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks plugin associés.
- cron_changed : Couvre cron_changed sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks plugin associés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : La source et les tests couvrent l'analyse du frontmatter, le chargement du workspace, les URL d'importation, le chargement des modules, l'éligibilité de la configuration, l'installation/mise à jour des hooks, le comportement fire-and-forget, les handlers de hooks groupés, les mappers de messages et la liste des hooks gérés par plugin.
- Signaux négatifs : La couverture est large au niveau du module mais limitée pour l'ordre réel du cycle de vie de Gateway sur le démarrage, l'arrêt, le flux de messages, la compaction et les événements de commande sous plusieurs répertoires de hooks configurés.
- Lacunes d'intégration : Un scénario Gateway unique devrait charger les hooks bundled, managed, workspace et plugin-managed, vérifier la précédence, exercer un événement replyable et un événement de cycle de vie non-replyable, et prouver que le statut CLI reflète l'éligibilité d'exécution.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : Le problème #84744 signale que `bootstrap-extra-files.paths` est silencieusement supprimé par la liste blanche de basename bootstrap reconnue ; la PR #74735 ajoute des fichiers supplémentaires à portée de session ; le problème #43454 demande des hooks de cycle de vie Gateway plus larges ; le problème #53600 souligne la surcharge des hooks sur les configurations VPS contraintes.
- Rapports Discrawl : Les journaux Discord montrent le chargement des hooks groupés au démarrage réel de la gateway, la confusion des utilisateurs autour des lectures répétées de `BOOT.md`, et un problème ouvert pour un hook interne `before_tool` bien que cela appartienne aux hooks plugin aujourd'hui.
- Bonnes qualités : La découverte a une précédence claire, les hooks workspace ne peuvent pas remplacer les hooks managed avec le même nom, les vérifications de limite de chemin du handler existent, les hooks mutables obtiennent des URL d'importation invalidées par cache, et les hooks groupés sont documentés.
- Mauvaises qualités : Les hooks internes et les hooks plugin typés restent faciles à confondre. Certains comportements de hooks filtrent silencieusement l'intention de l'utilisateur, et la surcharge des hooks peut être importante sur les petits hôtes.
- Exclus de la qualité : L'inventaire des tests et la profondeur de la preuve d'exécution ; ils sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/automation-cron-hooks-tasks-polling.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour l'authoring HOOK.md, la découverte des hooks, la gestion CLI des hooks, les packs de hooks, le dispatch des événements de cycle de vie, l'enregistrement api.on, les hooks de politique d'appel d'outil, les hooks de message, les hooks de session/cycle de vie, les demandes d'approbation de plugin, cron_changed.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La documentation et la sortie CLI devraient distinguer plus agressivement les hooks internes des hooks plugin typés.
- `bootstrap-extra-files` devrait signaler clairement les chemins filtrés au lieu de rendre le comportement de la liste blanche silencieux.
- La sortie de démarrage/statut devrait rendre le coût par hook et la portée des événements chargés plus visibles pour les déploiements contraints.

## Preuve

### Docs

- `docs/automation/hooks.md` documente l'objectif des hooks internes, les types d'événements, la structure `HOOK.md`, la précédence de découverte, les hooks groupés, la configuration, la référence CLI et les meilleures pratiques.
- `docs/cli/hooks.md` documente les opérations CLI pour la gestion des hooks.
- `docs/plugins/hooks.md` distingue les hooks de plugin typés des hooks internes.

### Source

- `src/hooks/frontmatter.ts`, `src/hooks/workspace.ts`, `src/hooks/loader.ts`, `src/hooks/config.ts`, `src/hooks/policy.ts`, `src/hooks/internal-hooks.ts`, `src/hooks/install.ts`, et `src/hooks/update.ts` implémentent le système de hooks internes principal.
- `src/hooks/bundled/session-memory/`, `src/hooks/bundled/bootstrap-extra-files/`, `src/hooks/bundled/command-logger/`, `src/hooks/bundled/compaction-notifier/`, et `src/hooks/bundled/boot-md/` implémentent les hooks groupés.
- `src/cli/hooks-cli.ts`, `src/gateway/session-patch-hooks.ts`, `src/agents/bootstrap-hooks.ts`, et `src/auto-reply/reply/message-preprocess-hooks.ts` connectent les hooks aux événements CLI et runtime.

### Tests d'intégration

- `src/hooks/bundled/boot-md/handler.gateway-startup.integration.test.ts` exerce boot-md au démarrage de la passerelle.
- `src/gateway/server.sessions.reset-hooks.test.ts` et `src/gateway/server.sessions.permissions-hooks.test.ts` exercent l'intégration des hooks de session.
- `src/auto-reply/reply/get-reply.message-hooks.test.ts` et `src/auto-reply/reply/message-preprocess-hooks.test.ts` exercent l'intégration des hooks de flux de messages.

### Tests unitaires

- `src/hooks/frontmatter.test.ts`, `src/hooks/workspace.test.ts`, `src/hooks/loader.test.ts`, `src/hooks/module-loader.test.ts`, `src/hooks/configured.ts`, `src/hooks/policy.test.ts`, `src/hooks/fire-and-forget.test.ts`, et `src/hooks/internal-hooks.test.ts` couvrent le comportement principal.
- `src/hooks/bundled/session-memory/handler.test.ts`, `src/hooks/bundled/bootstrap-extra-files/handler.test.ts`, et `src/hooks/bundled/boot-md/handler.test.ts` couvrent les hooks groupés.
- `src/cli/hooks-cli.test.ts`, `src/hooks/hooks-install.test.ts`, et `src/hooks/update.test.ts` couvrent le comportement CLI/installation/mise à jour.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "internal hooks HOOK.md session-memory bootstrap-extra-files" --json --limit 5`

Résultats :

- Le problème #84744 signale que les chemins configurés par l'utilisateur `bootstrap-extra-files` sont silencieusement supprimés par la liste blanche.
- La PR #74735 ajoute des fichiers supplémentaires à portée de session.
- Le problème #43454 demande des hooks de cycle de vie de passerelle plus larges.
- Le problème #53600 mentionne la surcharge des hooks par tour sur les configurations VPS contraintes.

Requête de secours :

`gitcrawl search openclaw/openclaw --query "session-memory hook bootstrap-extra-files" --json --limit 5`

Résultats :

- Le même cluster plus le problème #22438 sur le chargement en cascade des fichiers d'amorçage, renforçant la pression sur la taille du contexte d'amorçage.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "internal hooks HOOK.md session-memory bootstrap-extra-files"`

Résultats :

- Aucun message Discord correspondant retourné pour cette requête exacte.

Requête de secours :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "session-memory hook bootstrap-extra-files"`

Résultats :

- Les journaux réels de la passerelle montrent les hooks groupés chargés au démarrage : `boot-md`, `bootstrap-extra-files`, `command-logger`, et `session-memory`.
- Un fil de discussion utilisateur demande pourquoi les agents relisent répétitivement `BOOT.md` et affiche `openclaw hooks list` avec les hooks groupés et un hook memory-core géré par plugin.
- La discussion du problème #60065 demande une capacité de hook pré-outil dans la surface des hooks internes, montrant une confusion entre les hooks internes et les hooks de plugin.
