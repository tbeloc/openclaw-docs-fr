---
title: "Agent Runtime - Tool Execution Controls Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Agent Runtime - Tool Execution Controls Maturity Note

## Résumé

La politique d'exécution des outils est le composant le plus robuste de cette surface. La documentation distingue l'isolation, la politique des outils et les approbations élevées ; la source centralise l'enregistrement des outils, les racines d'espace de travail/sandbox, la politique héritée/sous-agent, la configuration d'exécution, la normalisation du schéma et les hooks avant l'appel d'outil ; les tests couvrent les portes d'approbation, les hooks de politique, les restrictions d'outils des sous-agents et le comportement de progression. La qualité est Beta car les preuves d'archive montrent toujours des cas limites autour du transfert d'approbation d'exécution, des règles de refus par agent, des attentes du backend sandbox et des hypothèses de limite plugin/service.

## Portée de la catégorie

Cette catégorie couvre le contrôle visible par l'opérateur sur les outils pendant les tours d'agent :
règles de disponibilité des outils, comportement d'exécution en sandbox, flux d'approbation, exécution
élevée, contrôles de sécurité des outils et accès aux outils délégués pour les sous-agents.

## Fonctionnalités

- Règles de disponibilité des outils : Quels outils sont disponibles pendant un tour après la résolution de la politique et la suppression basée sur le fournisseur.
- Comportement d'exécution en sandbox : Comportement d'exécution, racines de sandbox et contraintes d'espace de travail visibles pour les opérateurs.
- Flux d'approbation : Portes d'approbation de l'opérateur pour l'exécution des outils.
- Exécution élevée : Règles d'exécution d'hôte élevées et contrôles connexes.
- Contrôles de sécurité des outils : Hooks avant l'appel d'outil et garde-fous connexes qui façonnent le comportement des outils visible par l'opérateur.
- Accès aux outils délégués : Politique d'outils héritée ou restreinte pour les sous-agents et l'exécution déléguée.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (86%)`

La couverture est forte dans la documentation, la source, les tests e2e, les tests unitaires et les preuves d'archive pour le comportement de politique et d'approbation.

## Score de qualité

- Score : `Beta (74%)`

La conception est mature, mais la sémantique de la politique reste subtile pour les utilisateurs et les opérateurs lorsque les backends CLI, les sous-agents, les services de plugin et l'exécution élevée se chevauchent.

## Score de complétude

- Score : `Stable (86%)`
- Instructions de surface : évaluées par rapport à `references/completeness/agent-runtime-and-provider-execution.md`.
- Signaux positifs : les preuves de documentation archivée, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les règles de disponibilité des outils, le comportement d'exécution en sandbox, le flux d'approbation, l'exécution élevée, les contrôles de sécurité des outils, l'accès aux outils délégués.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La documentation de l'opérateur explique les couches de politique, mais les rapports de terrain montrent toujours une confusion sur ce que l'isolation en sandbox contraint et ne contraint pas.
- Le transfert d'approbation du backend CLI n'est pas aussi établi que le chemin d'exécution intégré principal.
- Le comportement de la politique par agent et héritée nécessite une preuve de régression continue à mesure que les sous-agents se développent.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/gateway/sandbox-vs-tool-policy-vs-elevated.md` distingue l'isolation, la politique des outils et l'exécution élevée ; documente les couches/règles de politique des outils, les groupes d'outils, les portes d'autorisation du serveur MCP en sandbox, les portes d'exécution uniquement élevées et les correctifs de prison sandbox.
- `/Users/kevinlin/code/openclaw/docs/concepts/agent-loop.md` documente les hooks de plugin incluant `before_tool_call`, la gestion des appels d'outils et les flux d'événements d'exécution.
- `/Users/kevinlin/code/openclaw/docs/tools/subagents.md` documente la politique d'outils des sous-agents, la restriction d'outils, la résolution d'authentification, le comportement d'annonce, le routage de livraison, la concurrence, la vivacité et la récupération.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/agent-tools.ts` implémente la politique d'outils du fournisseur de modèle, la suppression d'outils du modèle local, la fusion de la configuration d'exécution, la configuration de la politique d'outils, la politique de groupe/expéditeur/sandbox/sous-agent/héritée, les racines d'espace de travail/sandbox, les restrictions `apply_patch`, la configuration de l'outil d'exécution, le pipeline de politique d'outils, la normalisation du schéma et l'enveloppe du hook `before_tool_call`.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.ts` transfère les événements de plan, approbation, sortie de commande et patch via la livraison d'exécution.
- `/Users/kevinlin/code/openclaw/src/agents/cli-runner.ts` persiste les transcriptions de tour utilisateur CLI approuvées et exécute les hooks CLI autour de l'exécution du backend.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-gateway-approval.e2e.test.ts` couvre les approbations d'exécution hébergées par la passerelle sur des connexions séparées.
- `/Users/kevinlin/code/openclaw/src/agents/agent-tools.before-tool-call.integration.e2e.test.ts` couvre le comportement normal de `before_tool_call`, la modification de paramètres, le blocage, la déduplication et le contexte.
- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.subagents.sessions-spawn.lifecycle.test.ts` couvre le cycle de vie des sous-agents, le nettoyage, la gestion des délais d'expiration, le routage des comptes, le comportement d'annonce et le comportement de session adjacent à la politique.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/agent-tools.message-provider-policy.test.ts` couvre le comportement de la politique de message/outil basée sur le fournisseur.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.test.ts` couvre le transfert d'approbation, de sortie de commande, d'événement de patch, les détails de progression des outils et la livraison de résultat d'outil en flux.
- `/Users/kevinlin/code/openclaw/src/agents/transport-stream-shared.test.ts` couvre le comportement de transport sécurisé pour les charges utiles d'outils.

### Requêtes Gitcrawl

- `gitcrawl --json search issues -R openclaw/openclaw "exec approvals tool policy sandbox agent tool"` a retourné #44253 sur `tools.selfDeny` par agent, #69512 sur le transfert des listes blanches `exec-approvals.json` aux sessions du backend `claude-cli`, #78965 sur le backend sandbox utilisateur local, #48532 sur la sécurité par intention, #67440 sur TOTP optionnel pour les approbations d'exécution, #48503 sur l'enrichissement des événements `before_tool_call` avec la classification d'action/provenance d'entrée et #82548 sur les événements d'observabilité de sécurité/qualité.
- `gitcrawl --json search issues -R openclaw/openclaw "claude-cli codex cli harness subagent sessions_spawn"` a retourné #73097 sur le harnais PI ignorant la configuration `cliBackends` et séparant l'exécution des sous-agents du chemin de chat.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "exec approvals tool policy"` a retourné les notes de test de la version de mai 2026 couvrant l'authentification/profil, la politique de sandbox et les approbations d'exécution ; les discussions de la politique de récupération de fichiers de nœud ; les explications que refuser `exec` au niveau de la politique d'outil d'agent ne met pas en sandbox les plugins/services ; les commentaires que les contrôles sandbox/tool-policy/exec-approval sont utiles mais ne résolvent pas les défauts ; et les commentaires de fermeture de problème pour les contrôles connexes.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "sessions_spawn claude-cli"` a retourné les discussions Claude CLI et ACP runtime qui affectent les permissions d'outils, les limites de sandbox et l'UX des sous-agents.
