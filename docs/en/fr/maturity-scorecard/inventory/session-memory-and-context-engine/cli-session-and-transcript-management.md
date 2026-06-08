---
title: "Session, memory, and context engine - CLI Session and Transcript Management Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Session, memory, and context engine - CLI Session and Transcript Management Maturity Note

## Résumé

L'interface CLI de l'opérateur expose des chemins pratiques d'inspection de session et de transcription :
`openclaw sessions`, nettoyage, export de trajectoire, audit/maintenance des tâches, et
`openclaw transcripts` list/show/path. Elle est soutenue par des RPC Gateway si
possible et revient à des chemins hors ligne explicites. La couverture est solide pour l'enregistrement des commandes et les RPC de session Gateway, mais le comportement de la CLI de transcription est plus mince que la gestion des sessions et les preuves d'archive montrent que les attentes de nettoyage/restauration dépassent toujours l'UX de l'opérateur.

## Portée de la catégorie

Cette catégorie couvre `openclaw sessions`, `openclaw transcripts`, nettoyage,
comportement show/list/path, actions d'historique de session TUI, et commandes de gestion de session soutenues par Gateway.

## Fonctionnalités

- CLI Session : Couvre CLI Session dans `openclaw sessions`, `openclaw transcripts`, nettoyage, comportement show/list/path, actions d'historique de session TUI, et commandes de gestion de session soutenues par Gateway.
- Transcript Management : Couvre Transcript Management dans `openclaw sessions`, `openclaw transcripts`, nettoyage, comportement show/list/path, actions d'historique de session TUI, et commandes de gestion de session soutenues par Gateway.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : L'enregistrement CLI couvre les flux sessions list/cleanup/export/audit/show/notify/cancel, les tests RPC de session Gateway exercent list, resolve, patch, cleanup, compact, delete, et reset, et les tests TUI couvrent l'actualisation de l'historique et la sélection de session.
- Signaux négatifs : les commandes CLI de transcription sont plus simples et moins largement exercées ; les flux de restauration et d'archive ne sont pas prouvés de bout en bout à partir de la documentation CLI à l'état Gateway.
- Lacunes d'intégration : ajouter un scénario CLI qui exécute `sessions cleanup --dry-run`, `sessions cleanup --enforce`, `transcripts list`, `transcripts show`, et une lecture Gateway `chat.history` contre le même fixture.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : la recherche d'archive session/transcript a trouvé des rapports ouverts pour le nettoyage des transcriptions orphelines/non indexées et le support de restauration.
- Rapports Discrawl : les discussions d'archive Discord montrent des opérateurs posant des questions sur la réinitialisation automatique des archives et les préoccupations d'examen concernant le nettoyage de la rétention d'archive de compaction.
- Bonnes qualités : la documentation CLI et l'aide des commandes sont explicites, JSON lisible par machine est disponible, et le nettoyage sans dry-run délègue à Gateway quand il est accessible.
- Mauvaises qualités : les conseils de réparation CLI peuvent toujours être dangereux quand ils archivez l'historique valide comme orphelin ou manquent une route de restauration.
- Exclu de la qualité : profondeur des tests unitaires, intégration, e2e, live, et runtime-flow.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/session-memory-and-context-engine.md`.
- Signaux positifs : les docs archivées, source, test, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour CLI Session, Transcript Management.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'inspection de transcription existe, mais les flux de travail de restauration/branche/archive visibles par l'utilisateur restent dispersés.
- Les conseils de nettoyage ont besoin de garde-fous plus forts quand `sessions.json` et les transcriptions JSONL ne sont pas d'accord.

## Preuves

### Docs

- `docs/concepts/session.md:142` liste `openclaw status`, `openclaw sessions --json`, `/status`, et `/context list`.
- `docs/reference/session-management-compaction.md:114` documente `openclaw sessions cleanup --dry-run` et `--enforce`.
- `docs/cli/sessions.md` et `docs/cli/transcripts.md` sont les points d'entrée spécifiques à la CLI pour l'utilisation par l'opérateur.

### Source

- `src/cli/program/register.status-health-sessions.ts:175` enregistre la commande `sessions` ; `src/cli/program/register.status-health-sessions.ts:210` enregistre le nettoyage.
- `src/cli/program/register.transcripts.ts:290` enregistre `transcripts` ; `src/cli/program/register.transcripts.ts:221` liste les sessions de transcription stockées ; `src/cli/program/register.transcripts.ts:249` affiche une transcription.
- `src/tui/tui-session-actions.ts:236` liste les sessions ; `src/tui/tui-session-actions.ts:299` charge l'historique ; `src/tui/tui-session-actions.ts:397` abandonne les exécutions actives.

### Tests d'intégration

- `src/gateway/server.sessions.store-rpc.test.ts:35` valide les RPC de session list/patch/cleanup/reset/compact/delete soutenues par Gateway.
- `src/gateway/server.sessions.compaction.test.ts:277` valide le `sessions.compact` manuel sur RPC Gateway.
- `src/tui/gateway-chat.test.ts:572` vérifie que TUI réessaye `chat.history` lors du démarrage de Gateway.

### Tests unitaires

- `src/tui/tui-session-actions.test.ts:60` vérifie les actualisations de session en file d'attente ; `src/tui/tui-session-actions.test.ts:549` se souvient des sessions sélectionnées après le chargement de l'historique.
- `src/tui/tui-last-session.test.ts:26` persiste l'état de la dernière session et évite les sessions de type heartbeat.
- `src/cli/program/register.transcripts.test.ts` couvre l'enregistrement des commandes de transcription et le comportement d'analyse.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues "openclaw sessions transcripts chat.history" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats :

- A retourné 13 rapports ouverts touchant la restauration de transcription de session, le nettoyage, la visibilité de l'historique, et la persistance de session.

Requête :

`gitcrawl search issues "sessions cleanup session maintenance transcript archive" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats :

- A retourné les `#77941 Add native sessions cleanup support for orphan/unindexed transcript archive/prune` et `#60745 Feature: ephemeral sessions` ouverts.

### Requêtes Discrawl

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "sessions cleanup session maintenance transcript archive"`

Résultats :

- A retourné une discussion Discord expliquant la réinitialisation des archives inactives, la rétention de réinitialisation, et les commentaires d'examen PR concernant le nettoyage de la rétention d'archive de compaction en modes warn/enforce.
