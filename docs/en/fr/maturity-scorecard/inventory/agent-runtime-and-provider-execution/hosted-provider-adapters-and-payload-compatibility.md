---
title: "Agent Runtime - Hosted Provider Execution Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Agent Runtime - Hosted Provider Execution Maturity Note

## Résumé

La couverture de l'adaptateur de fournisseur hébergé est solide pour les routes OpenAI/Codex, Anthropic, Google et compatibles avec OpenAI. La documentation explique la configuration spécifique au fournisseur, les contrôles de réflexion, les distinctions OAuth/clé API, les alternatives d'exécution CLI et les attentes en matière de capacités. La source inclut la conversion de message/outil/réflexion spécifique au fournisseur, la gestion des délais d'expiration, le comportement websocket/SSE, l'affinité du cache de prompt et la normalisation des appels d'outils. La qualité est Beta car la sémantique de la charge utile du fournisseur hébergé change encore rapidement, en particulier pour le routage OAuth de Codex, le JSON de streaming d'Anthropic, les identifiants d'appel d'outil de Google et le comportement des outils compatibles avec OpenAI.

## Portée de la catégorie

Cette catégorie couvre l'exécution du fournisseur hébergé visible par l'opérateur : exécution de tours
contre des fournisseurs hébergés, utilisation d'options de modèle spécifiques au fournisseur, exercice
de l'utilisation d'outils hébergés, application de contrôles de raisonnement ou de cache et réception de réponses
en streaming ou finales malgré les différences de charge utile du fournisseur.

## Fonctionnalités

- Tours de fournisseur hébergé : Exécution de tours d'agent contre des fournisseurs hébergés tels que OpenAI, Anthropic et Google.
- Options de modèle spécifiques au fournisseur : Paramètres de modèle spécifiques au fournisseur et paramètres de demande d'exécution exposés aux utilisateurs ou opérateurs.
- Utilisation d'outils hébergés : Comportement de l'utilisation d'outils lorsque l'exécution active est un fournisseur hébergé.
- Contrôles de raisonnement et de cache : Contrôles spécifiques au fournisseur liés au raisonnement, à la réflexion et au cache lors de l'exécution hébergée.
- Streaming et réponses hébergés : Comportement de streaming et de réponse visible par l'opérateur tandis que les adaptateurs hébergés normalisent les différences de charge utile.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`

La couverture est bonne pour les fournisseurs majeurs, mais les variantes de fournisseur hébergé compatibles avec OpenAI et à évolution rapide s'appuient toujours sur des tests, des documents et des preuves d'archive dispersés plutôt que sur un tableau de compatibilité uniforme.

## Score de qualité

- Score : `Beta (70%)`

Les adaptateurs incluent de nombreuses protections de compatibilité, mais la dérive de la charge utile du fournisseur et les particularités du streaming/appel d'outil restent visibles dans les problèmes archivés et les rapports Discord.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/agent-runtime-and-provider-execution.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les tours de fournisseur hébergé, les options de modèle spécifiques au fournisseur, l'utilisation d'outils hébergés, les contrôles de raisonnement et de cache, le streaming et les réponses hébergés.
- Signaux négatifs : la note archivée a précédé le scoring de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La sémantique de l'appel d'outil et de la réflexion spécifique au fournisseur a toujours besoin de preuves en direct récurrentes.
- Les fournisseurs hébergés compatibles avec OpenAI et les alias de route ont moins de preuves systématiques que les routes de première partie.
- Certaines défaillances d'adaptateur apparaissent comme des erreurs de secours générique ou de clé manquante, ce qui rend le diagnostic de l'opérateur plus difficile.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/providers/openai.md` documente les distinctions de route OpenAI/Codex, les cartes de nommage, les tableaux de capacités, les notes d'application serveur GPT-5.5/Codex, la configuration OAuth de Codex et les routes d'agent par défaut.
- `/Users/kevinlin/code/openclaw/docs/providers/anthropic.md` documente la clé API Anthropic par rapport à Claude CLI, les références canoniques, les références héritées, les paramètres par défaut de réflexion et la mise en cache des prompts.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md` documente les capacités du plugin Google, OAuth CLI Gemini, les références de modèle, les capacités et les contrôles de réflexion/raisonnement.
- `/Users/kevinlin/code/openclaw/docs/concepts/models.md` documente la séparation référence de modèle/exécution et la sélection de secours que les adaptateurs de fournisseur consomment.

### Source

- `/Users/kevinlin/code/openclaw/src/llm/providers/openai-codex-responses.ts` implémente la configuration du transport Codex Responses, la gestion de l'identifiant de compte, la construction du corps/en-tête, les signaux de délai d'expiration, le chemin websocket, la classification des erreurs réessayables et l'affinité du cache de prompt.
- `/Users/kevinlin/code/openclaw/src/llm/providers/anthropic.ts` implémente la configuration du flux Anthropic, la construction des paramètres de demande, la gestion des événements, la gestion du message système OAuth, les modes de réflexion, la normalisation de l'identifiant d'outil, les transformations de message, le streaming d'outil à grain fin bêta et la conversion d'outil.
- `/Users/kevinlin/code/openclaw/src/llm/providers/google-shared.ts` implémente la sémantique de la partie réflexion Google, la rétention de la signature de pensée, les exigences d'identifiant d'appel d'outil, la conversion texte/réflexion/appel d'outil assistant et la conversion de résultat d'outil.
- `/Users/kevinlin/code/openclaw/src/agents/transport-stream-shared.ts` fournit l'assainissement du flux de transport inter-fournisseur, la coercition d'argument d'appel d'outil, la fusion de métadonnées, la finalisation et la gestion du flux d'erreur.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.test.ts` couvre les remplacements d'exécution de session OpenAI, la télémétrie du serveur d'application Codex, le formatage des erreurs externes, les conseils de sortie d'outil personnalisé manquant et les conseils de réinitialisation de non-concordance d'outil Bedrock.
- `/Users/kevinlin/code/openclaw/src/commands/models.list.e2e.test.ts` couvre les lignes du catalogue de fournisseurs, le comportement auth/local/provider et la réactivité du catalogue.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/llm/providers/openai-codex-responses.test.ts` couvre le décodage de l'identifiant de compte, les délais d'expiration du transport, le comportement websocket/SSE, le comportement du délai d'expiration et l'affinité du cache de prompt.
- `/Users/kevinlin/code/openclaw/src/llm/providers/anthropic.test.ts` couvre l'authentification du fournisseur Anthropic et la relecture de réflexion signée.
- `/Users/kevinlin/code/openclaw/src/llm/providers/google-shared.test.ts` couvre la projection du texte, de la réflexion, des appels d'outil, des identifiants de réponse et de l'utilisation.
- `/Users/kevinlin/code/openclaw/src/agents/transport-stream-shared.test.ts` couvre l'assainissement, le texte de charge utile d'outil non vide, les en-têtes, les flux de succès et le nettoyage des défaillances.

### Requêtes Gitcrawl

- `gitcrawl --json search issues -R openclaw/openclaw "openai-codex Anthropic Google provider tool call"` a retourné #80667 sur les sessions pures `claude-cli` manquant `trajectory.jsonl` et #78196 sur le comportement du chargeur de plugin d'extension.
- `gitcrawl --json search issues -R openclaw/openclaw "tool call streaming truncated tool_call provider"` a retourné #60593 sur les erreurs d'analyse JSON de streaming Anthropic récurrentes, #70033 sur les appels d'outil émettant des arguments `{}` vides pour le contenu volumineux et #87711 sur la livraison d'assistant vide.
- `gitcrawl --json search prs -R openclaw/openclaw "provider error descriptors fallback rate limit"` a retourné la PR #86642 ajoutant des descripteurs d'erreur de fournisseur structurés.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "tool call streaming"` a retourné des discussions sur les rappels de progression natifs, l'enveloppe de streaming/appel d'outil du fournisseur, les blocs d'appel d'outil visibles, le comportement du chien de garde inactif du serveur d'application, la visibilité de l'outil Claude CLI/WebChat et les modes de progression Telegram.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "openai-codex provider routing"` a retourné des rapports sur le routage OAuth/Codex OpenAI, la dérive du chemin Codex Responses OpenAI direct, l'état de route persistant obsolète et les anciens épingles de configuration/exécution.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "model fallback decision"` a retourné des discussions sur le délai d'expiration du fournisseur hébergé et le secours, y compris les délais d'expiration d'OpenRouter et les défaillances du porteur manquant.
