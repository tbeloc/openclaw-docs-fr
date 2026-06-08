---
title: "Chemin du fournisseur OpenAI / Codex - Note de maturité de compatibilité des réponses et des outils"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur OpenAI / Codex - Note de maturité de compatibilité des réponses et des outils

## Résumé

Le transport Codex Responses dispose de preuves solides en matière de source et de test. Il prend en charge les URL du backend ChatGPT, les en-têtes account-id, WebSocket en premier avec repli SSE, les délais d'expiration des requêtes, l'affinité du cache de prompt, les tentatives, le niveau de service, les champs reasoning/text, la conversion des messages Responses, la conversion des outils et la normalisation des flux. La qualité reste Beta car la sémantique des charges utiles OpenAI/Codex change fréquemment et les preuves archivées incluent des problèmes antérieurs de relecture des appels d'outils et d'état de transport.

## Portée de la catégorie

Inclus dans cette catégorie :

- Transport Codex Responses : Couvre le transport Codex Responses sur le chemin de requête/streaming du fournisseur de bas niveau pour `openai-codex-responses` et le code de conversion OpenAI Responses partagé utilisé par les routes de compatibilité OpenAI directe et Codex-auth.
- Compatibilité des charges utiles : Couvre la compatibilité des charges utiles sur le chemin de requête/streaming du fournisseur de bas niveau pour `openai-codex-responses` et le code de conversion OpenAI Responses partagé utilisé par les routes de compatibilité OpenAI directe et Codex-auth.
- Contexte des outils : Couvre le contexte des outils sur les outils côté fournisseur, l'injection de contexte, les entrées médias, la propriété des outils native par rapport au client, la compatibilité OpenAI Responses et la façon dont les modèles OpenAI/Codex reçoivent le contexte d'exécution OpenClaw.
- Compatibilité des capacités : Couvre la compatibilité des capacités sur les outils côté fournisseur, l'injection de contexte, les entrées médias, la propriété des outils native par rapport au client, la compatibilité OpenAI Responses et la façon dont les modèles OpenAI/Codex reçoivent le contexte d'exécution OpenClaw.

## Fonctionnalités

- Transport Codex Responses : Couvre le transport Codex Responses sur le chemin de requête/streaming du fournisseur de bas niveau pour `openai-codex-responses` et le code de conversion OpenAI Responses partagé utilisé par les routes de compatibilité OpenAI directe et Codex-auth.
- Compatibilité des charges utiles : Couvre la compatibilité des charges utiles sur le chemin de requête/streaming du fournisseur de bas niveau pour `openai-codex-responses` et le code de conversion OpenAI Responses partagé utilisé par les routes de compatibilité OpenAI directe et Codex-auth.
- Contexte des outils : Couvre le contexte des outils sur les outils côté fournisseur, l'injection de contexte, les entrées médias, la propriété des outils native par rapport au client, la compatibilité OpenAI Responses et la façon dont les modèles OpenAI/Codex reçoivent le contexte d'exécution OpenClaw.
- Compatibilité des capacités : Couvre la compatibilité des capacités sur les outils côté fournisseur, l'injection de contexte, les entrées médias, la propriété des outils native par rapport au client, la compatibilité OpenAI Responses et la façon dont les modèles OpenAI/Codex reçoivent le contexte d'exécution OpenClaw.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (80%)`
- Signaux positifs : Les tests unitaires ciblés couvrent l'extraction de compte JWT, les délais d'expiration du transport, les choix WebSocket/SSE, les en-têtes de tentative, l'affinité du cache de prompt, la conversion stricte des outils et la relecture du reasoning.
- Signaux négatifs : La preuve d'intégration est toujours répartie entre les tests de modèle/runtime/gateway plutôt que dans une seule voie de compatibilité Codex Responses.
- Lacunes d'intégration : Plus de preuves en direct sont nécessaires pour le repli WebSocket, le cache de prompt, le niveau de service et la relecture des appels d'outils par rapport au comportement actuel du backend ChatGPT.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : La requête pour transport/prompt-cache n'a retourné aucune ligne directe, mais la requête de relecture du reasoning a retourné #76413 sur la relecture de session Telegram `openai-codex` après un appel d'outil.
- Rapports Discrawl : La requête pour transport/prompt-cache n'a retourné aucune ligne correspondante ; la discussion sur les outils natifs du fournisseur montre une confusion continue entre les outils côté serveur OpenAI Responses et les outils côté client OpenClaw.
- Bonnes qualités : Le code dispose de gardes explicites pour timeout, retry, account-header, prompt-cache, strict-tool et stream-processing.
- Mauvaises qualités : Le comportement du transport dépend d'un backend en amont qui évolue rapidement et la sémantique des éléments tool/reasoning est suffisamment fragile pour nécessiter des tests de régression ciblés.
- Exclu de la qualité : La couverture des tests unitaires et d'intégration n'a pas été utilisée comme entrée de qualité.

## Score de complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openai-codex-provider-path.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le transport Codex Responses, la compatibilité des charges utiles, le contexte des outils et la compatibilité des capacités.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connus utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Il n'existe pas de matrice de compatibilité publique unique pour les champs de charge utile OpenAI/Codex acceptés par chaque route.
- La dégradation WebSocket et le repli SSE nécessitent une preuve de voie de publication après les modifications en amont.
- La relecture des outils et du reasoning reste à haut risque car l'appairage d'éléments invalides peut fuir entre les tours.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/openai.md` documente les choix de transport, le mode rapide, le niveau de service, la compaction côté serveur et le comportement des points de terminaison natifs/compatibles.
- `/Users/kevinlin/code/openclaw/docs/gateway/openresponses-http-api.md` documente les champs de requête compatibles OpenResponses, les fichiers/images, les outils et le comportement de session.
- `/Users/kevinlin/code/openclaw/docs/gateway/openai-http-api.md` documente le comportement des outils et du streaming Chat Completions compatible OpenAI.

### Source

- `/Users/kevinlin/code/openclaw/src/llm/providers/openai-codex-responses.ts` implémente la gestion des URL du backend Codex, les en-têtes account-id, le transport WebSocket/SSE, les tentatives, les délais d'expiration des requêtes, l'affinité du cache de prompt, les champs niveau de service/text/reasoning et la gestion des flux.
- `/Users/kevinlin/code/openclaw/src/llm/providers/openai-responses-shared.ts` convertit les messages OpenClaw, les images, les appels d'outils, les résultats d'outils, les éléments de reasoning et les événements de réponse en flux vers/depuis les formes OpenAI Responses.
- `/Users/kevinlin/code/openclaw/src/llm/providers/openai-responses-tools.ts` convertit les outils OpenClaw en outils de fonction Responses.
- `/Users/kevinlin/code/openclaw/src/agents/provider-transport-stream.ts` achemine `openai-codex-responses` via le transport OpenAI Responses OpenClaw lorsqu'un comportement conscient du transport est requis.
- `/Users/kevinlin/code/openclaw/src/agents/openai-responses-payload-policy.ts` supprime ou préserve les champs niveau de service, cache de prompt, store et compaction selon la classe de point de terminaison.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/openresponses-http.test.ts` exerce l'analyse des requêtes OpenResponses, l'authentification/routage, le comportement de session, SSE et la gestion des fichiers/images.
- `/Users/kevinlin/code/openclaw/src/gateway/openai-http.test.ts` exerce la validation des requêtes Chat Completions compatible OpenAI, le routage, SSE, les images et les outils clients.
- `/Users/kevinlin/code/openclaw/scripts/e2e/openai-chat-tools-docker.sh` exécute un E2E Docker OpenAI Chat Completions tools.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/llm/providers/openai-codex-responses.test.ts` couvre l'extraction d'account-id, le comportement WebSocket explicite, la gestion des délais d'expiration, l'analyse de Retry-After et l'affinité du cache de prompt.
- `/Users/kevinlin/code/openclaw/src/llm/providers/openai-responses-shared.test.ts` couvre la conversion stricte des outils et la normalisation du schéma.
- `/Users/kevinlin/code/openclaw/src/agents/openai-responses.reasoning-replay.test.ts` couvre la relecture du reasoning autour des appels d'outils et des messages d'assistant.
- `/Users/kevinlin/code/openclaw/src/agents/openai-strict-tool-setting.ts` et les tests adjacents couvrent les décisions strict-tool pour les routes OpenAI natives et Codex.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "openai-codex responses websocket sse tool call prompt_cache service_tier"`

Résultats :

- N'a retourné aucune ligne correspondante. Ceci a été traité comme neutre après des vérifications de fraîcheur réussies.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OpenAI Responses reasoning replay function_call tool result"`

Résultats :

- A retourné #76413 sur une session Telegram `openai-codex` relisant une réponse d'assistant antérieure après un appel d'outil.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "openai-codex responses websocket sse tool call prompt cache service tier"`

Résultats :

- N'a retourné aucune ligne correspondante. Ceci a été traité comme neutre après des vérifications de fraîcheur réussies.

Requête : `discrawl search --limit 10 "strict tools OpenAI Responses schema tool_choice"`

Résultats :

- N'a retourné aucune ligne correspondante. Ceci a été traité comme neutre après des vérifications de fraîcheur réussies.
