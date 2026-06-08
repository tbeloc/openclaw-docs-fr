---
title: "Agent Runtime - Agent Turn Execution Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Agent Runtime - Agent Turn Execution Maturity Note

## Résumé

Les tours d'agent ont un cycle de vie d'exécution de première classe : la documentation explique les démarrages passerelle/intégrés, la mise en file d'attente, les verrous de session, les flux d'événements, les délais d'expiration et l'arrêt anticipé ; la source centralise l'exécution des tours dans `runAgentTurnWithFallback` ; les tests exercent l'orchestration de secours, les abandons, les backstops du cycle de vie, la livraison d'événements et la télémétrie d'exécution. La qualité est Beta car les preuves d'archive montrent toujours des réponses vides/échouées récentes et des cas limites de délai d'expiration autour des tours intégrés de longue durée ou redémarrés.

## Portée de la catégorie

Cette catégorie couvre l'exécution des tours visible par l'utilisateur/l'opérateur : démarrage d'un tour d'agent, choix entre l'exécution de la passerelle et du runtime intégré, établissement des identifiants de session/exécution, application des verrous de file d'attente, pontage des événements, respect des abandons, chronométrage du travail du fournisseur/modèle et émission des résultats terminaux.

## Fonctionnalités

- Démarrage du tour et choix du runtime : Démarrage d'un tour d'agent et choix entre l'exécution de la passerelle et du runtime intégré.
- Coordination de session et d'exécution : Établissement des identifiants de session et d'exécution, verrous de file d'attente et coordination d'exécution connexe.
- Abandon et résultats terminaux : Respect des abandons, chronométrage du travail du fournisseur/modèle et émission des résultats terminaux.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`

La couverture est large sur les concepts, la documentation CLI, la source et les tests. L'écart de couverture restant est la preuve directe du scénario pour chaque chemin de redémarrage/délai d'expiration du runtime par version du fournisseur.

## Score de qualité

- Score : `Beta (74%)`

Le cycle de vie a des garde-fous et des diagnostics solides, mais les rapports opérationnels récents montrent toujours des réponses vides terminales, des cas de récupération de redémarrage et des exécutions locales/intégrées sensibles aux délais d'expiration qui nécessitent un comportement de récupération d'opérateur plus clair.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/agent-runtime-and-provider-execution.md`.
- Signaux positifs : les preuves de documentation archivée, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le démarrage du tour et le choix du runtime, la coordination de session et d'exécution, l'abandon et les résultats terminaux.
- Signaux négatifs : la note archivée a précédé le scoring de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Certains modes de défaillance du runtime sont documentés par le biais de tests et de problèmes archivés plutôt que par un seul guide de dépannage destiné à l'opérateur.
- Les tours de runtime locaux ou externes de longue durée semblent toujours sensibles à la configuration du délai d'expiration.
- Les recherches d'archive ont trouvé peu de couverture directe de problèmes GitHub pour les termes étroits `agent.wait` et de secours intégré, donc les preuves Discord portent plus du fardeau du signal de terrain.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/concepts/agent-loop.md` documente la forme RPC de l'agent, `agentCommand`, `runEmbeddedAgent`, le pont d'événement, `agent.wait`, le comportement de verrouillage/session de mise en file d'attente, le comportement de charge utile de streaming/outil/final, les flux d'événements, les délais d'expiration et les raisons d'arrêt anticipé.
- `/Users/kevinlin/code/openclaw/docs/cli/agent.md` documente l'exécution d'un tour d'agent via Gateway, les options de modèle/réflexion/local/livraison/délai d'expiration, le comportement de préchargement local, les identifiants de session/exécution de secours de délai d'expiration de passerelle et `chat.abort` SIGTERM/SIGINT.
- `/Users/kevinlin/code/openclaw/docs/concepts/agent-runtimes.md` explique les runtimes par rapport aux fournisseurs/modèle/canal, les harnais intégrés, les backends CLI, les surfaces Codex, la propriété du runtime, la sélection du runtime et les runtimes explicites fermés en cas d'échec.

### Source

- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.ts` importe `runEmbeddedAgent`, `runWithModelFallback`, la résolution du fournisseur de runtime et la planification des résultats ; il implémente le chronométrage des tours, la résolution de la fenêtre de contexte, `runAgentTurnWithFallback`, la configuration de l'authentification/profil des candidats de secours, les commutateurs de modèle en direct, les diagnostics d'exécution, les médias de réponse et les avis de compaction.
- `/Users/kevinlin/code/openclaw/src/agents/cli-runner.ts` finalise les tours du moteur de contexte CLI, persiste les transcriptions CLI approuvées et exécute les tours d'agent CLI via le même chemin de hook.
- `/Users/kevinlin/code/openclaw/packages/agent-core/src/agent-loop.test.ts` ancre la gestion des défaillances EventStream dans le package de boucle d'agent de niveau inférieur.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.test.ts` couvre `runAgentTurnWithFallback`, la propagation du signal d'abandon, les revérifications de secours en file d'attente, la disponibilité de l'authentification de secours, les aperçus d'événements de l'assistant CLI, les backstops terminaux du cycle de vie, la copie de redémarrage de la passerelle, le formatage des erreurs externes, les plafonds de redémarrage/nouvelle tentative de commutateur de modèle en direct et l'état du profil d'authentification lors des nouvelles tentatives.
- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.subagents.sessions-spawn.lifecycle.test.ts` couvre le nettoyage du cycle de vie de la session générée, suffisamment de temps de demande de passerelle, le nettoyage MCP, la suppression via `agent.wait`, la gestion du délai d'expiration, le routage des comptes et le comportement d'annonce.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/packages/agent-core/src/agent-loop.test.ts` couvre les chemins d'erreur EventStream.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.test.ts` inclut une couverture unitaire ciblée pour l'orchestration de secours, la classification des résultats terminaux, la gestion des résultats vides et les diagnostics au niveau des tours.

### Requêtes Gitcrawl

- `gitcrawl --json search issues -R openclaw/openclaw "agent loop gateway_timeout chat.abort embedded fallback"` n'a retourné aucun problème correspondant, ce qui suggère que la requête de cycle de vie exacte n'est pas l'endroit où les rapports de terrain sont regroupés.
- `gitcrawl --json search issues -R openclaw/openclaw "runAgentTurnWithFallback agent runner timeout"` n'a retourné aucun problème correspondant.
- `gitcrawl --json search issues -R openclaw/openclaw "local model provider context timeout Ollama"` a retourné des problèmes incluant #87642 sur l'exposition du délai d'expiration `waitForRun` pour les LLM locaux lents, #86599 sur les appels du fournisseur local bloquant la boucle d'événement de la passerelle sur Windows et #74204 sur le délai d'expiration d'intégration de mémoire pour GGUF local.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "runEmbeddedAgent agent.wait"` n'a retourné aucune correspondance.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "agent.wait gateway_timeout embedded fallback"` n'a retourné aucune correspondance.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "model fallback decision"` a retourné des discussions récentes autour des délais d'expiration openai-codex, des décisions de secours, des décisions de secours sans clé API, des décisions de délai d'expiration OpenRouter, des journaux de porteur manquants et des erreurs de secours répétées dans les boucles de réparation de session.
