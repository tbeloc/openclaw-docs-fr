---
title: "Automation: cron, hooks, tasks, polling - Plugin Hooks Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automation: cron, hooks, tasks, polling - Plugin Hooks Maturity Note

## Résumé

Les hooks de plugin typés sont l'une des surfaces d'automatisation les plus capables : ils couvrent la résolution de modèles, la construction de prompts, la politique d'outils, la dispatch de messages, les sessions, la compaction, les sous-agents, le cycle de vie, l'installation et l'observation des changements cron. La couverture est large, mais la qualité est limitée par une couverture inégale des chemins et des rapports en direct où les événements de hook attendus ne se déclenchent pas sur des chemins d'exécution spécifiques.

## Portée de la catégorie

Cette catégorie couvre les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, les hooks de session et de cycle de vie, les hooks de sous-agents, `cron_changed`, les demandes d'approbation de plugin, les politiques d'outils de confiance, les contextes de hook et le câblage SDK/runtime.

## Fonctionnalités

- Enregistrement api.on : Couvre l'enregistrement api.on sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks de plugin associés.
- Hooks de politique d'appel d'outil : Couvre les hooks de politique d'appel d'outil sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks de plugin associés.
- Hooks de message : Couvre les hooks de message sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks de plugin associés.
- Hooks de session/cycle de vie : Couvre les hooks de session/cycle de vie sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks de plugin associés.
- Demandes d'approbation de plugin : Couvre les demandes d'approbation de plugin sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks de plugin associés.
- cron_changed : Couvre cron_changed sur les hooks typés `api.on(...)`, le comportement de priorité/timeout, les hooks de décision tels que `before_tool_call`, les hooks de message et de dispatch, et le comportement des hooks de plugin associés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (80%)`
- Signaux positifs : Il existe une couverture ciblée pour les hooks avant/après les outils, les hooks avant-agent, les hooks de réponse/finalisation, les portes de cycle de vie, la sécurité, la corrélation, les chemins de passerelle/session/sous-agent/dispatch-réponse câblés, et les contrats host-hook.
- Signaux négatifs : Les preuves d'archive et la forme source indiquent que tous les chemins d'exécution d'outils ne passent pas systématiquement par les deux wrappers de hook pré et post, en particulier l'invocation directe d'outils de passerelle et la boucle MCP.
- Lacunes d'intégration : Une suite de conformité de hook inter-runtime devrait prouver le même cycle de vie de hook pour les outils OpenClaw intégrés, les hooks Codex natifs, la `tools.invoke` directe de passerelle, la boucle MCP et les exécutions déclenchées par canal.

## Score de qualité

- Score : `Beta (75%)`
- Rapports Gitcrawl : La PR #62701 ajoute du contexte à `before_tool_call` ; le problème #76201 signale que `before_tool_call` du plugin ne se déclenche pas pour l'exécution native sur le harnais Anthropic ; le problème #86777 demande de documenter la gestion du mode rapport du serveur d'application Codex pour `requireApproval` du plugin ; le problème #23451 maintient une porte de confirmation d'outil intégrée ouverte même si les approbations de plugin existent.
- Rapports Discrawl : La discussion du mainteneur dit que `before_tool_call` et `after_tool_call` existent, et que le relais natif Codex mappe `PreToolUse`/`PostToolUse`, mais la `tools.invoke` directe de passerelle et la boucle MCP semblent exécuter `before_tool_call` sans exécuter systématiquement `after_tool_call`.
- Bonnes qualités : Le catalogue de hooks est explicite, la sémantique de décision est typée, les priorités et les timeouts sont configurables, la configuration du plugin est injectée par gestionnaire, et les demandes d'approbation ont un contrat de résolution documenté.
- Mauvaises qualités : La couverture runtime est suffisamment inégale pour que les auteurs de plugins ne puissent pas supposer que chaque chemin d'exécution déclenche la même séquence de hook. C'est un problème de qualité car les plugins de politique et d'observabilité dépendent de limites de hook uniformes.
- Exclu de la qualité : L'inventaire des tests et la profondeur de preuve runtime ; ils sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/automation-cron-hooks-tasks-polling.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'enregistrement api.on, les hooks de politique d'appel d'outil, les hooks de message, les hooks de session/cycle de vie, les demandes d'approbation de plugin, cron_changed.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Centraliser l'exécution des outils via un wrapper de cycle de vie afin que les hooks pré/post et les diagnostics ne puissent pas dériver par chemin d'exécution.
- Documenter le comportement natif de Codex et du mode rapport pour les approbations de plugin.
- Rendre la couverture du chemin de hook visible dans la documentation SDK afin que les auteurs de plugins sachent quels hooks sont garantis pour chaque runtime.

## Preuves

### Docs

- `docs/plugins/hooks.md` documente le catalogue de hooks, le comportement de priorité et de timeout, la sémantique des résultats de décision, les contextes, `cron_changed` et la politique d'appel d'outil.
- `docs/plugins/plugin-permission-requests.md` documente les approbations de plugin et comment `before_tool_call.requireApproval` interagit avec `/approve`.
- `docs/plugins/sdk-subpaths.md` liste `plugin-sdk/hook-runtime` et les sous-chemins runtime associés.

### Source

- `src/plugins/hooks.ts`, `src/plugins/host-hooks.ts`, `src/plugins/host-hook-runtime.ts`, `src/plugins/hook-runner-global.ts`, `src/plugins/hook-decision-types.ts` et `src/plugins/hook-agent-context.ts` implémentent l'enregistrement et l'exécution des hooks typés.
- `src/gateway/server-methods/plugin-host-hooks.ts` câble les hooks de plugin dans les méthodes de passerelle.
- `src/plugin-sdk/hook-runtime.ts` expose les aides de hook via le SDK.
- `extensions/codex/src/app-server/native-hook-relay.ts` mappe les hooks natifs Codex dans le comportement des hooks OpenClaw.

### Tests d'intégration

- `src/plugins/wired-hooks-after-tool-call.e2e.test.ts`, `src/plugins/wired-hooks-gateway.test.ts`, `src/plugins/wired-hooks-session.test.ts`, `src/plugins/wired-hooks-subagent.test.ts` et `src/plugins/wired-hooks-reply-dispatch.test.ts` exercent le câblage intégré des hooks.
- `src/plugins/contracts/host-hooks.contract.test.ts` couvre le comportement du contrat host-hook.
- `extensions/codex/src/app-server/run-attempt.hooks.test.ts` et `extensions/codex/src/app-server/native-hook-relay.test.ts` couvrent les chemins de relais de hook du serveur d'application Codex.

### Tests unitaires

- `src/plugins/hooks.before-tool-call.test.ts`, `src/plugins/hooks.before-agent-start.test.ts`, `src/plugins/hooks.before-agent-reply.test.ts`, `src/plugins/hooks.before-agent-finalize.test.ts`, `src/plugins/hooks.before-install.test.ts`, `src/plugins/hooks.security.test.ts` et `src/plugins/hook-runner-global.test.ts` couvrent la sémantique des hooks.
- `src/plugins/hook-decision-types.test.ts`, `src/plugins/hook-agent-context.test.ts` et `src/plugins/host-hook-cleanup-timeout.test.ts` couvrent les décisions, le contexte et le nettoyage.
- `src/agents/agent-tools.before-tool-call.integration.e2e.test.ts` exerce le comportement avant-outil du côté des outils d'agent.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "plugin hooks before_tool_call cron_changed before_agent_finalize" --json --limit 5`

Résultats :

- Aucun résultat pour la requête exacte.

Requête de secours :

`gitcrawl search openclaw/openclaw --query "before_tool_call hook" --json --limit 5`

Résultats :

- La PR #62701 ajoute precedingText et messageId optionnels au contexte `before_tool_call`.
- Le problème #76201 signale que `before_tool_call` ne se déclenche pas pour l'exécution native sur un harnais spécifique.
- Le problème #79168 référence l'analyse d'injection de prompt basée sur le contenu sur la sortie d'outil.
- Le problème #48509 demande un hook `before_persistence_write` d'état durable.
- Le problème #86777 demande de documenter `requireApproval` du plugin en mode rapport du serveur d'application Codex.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "before_tool_call hook"`

Résultats :

- La discussion du mainteneur dit que les hooks pré/post d'outil existent et que le relais natif Codex les mappe, mais la couverture post-hook est inégale sur les chemins directs `tools.invoke` de passerelle et la boucle MCP.
- Les commentaires de problème GitHub restent ouverts #23451, #13364 et #13225, clarifiant que `before_tool_call` du plugin existe mais ne satisfait pas tous les cas d'utilisation de hook interne ou de délégation de modèle demandés.
