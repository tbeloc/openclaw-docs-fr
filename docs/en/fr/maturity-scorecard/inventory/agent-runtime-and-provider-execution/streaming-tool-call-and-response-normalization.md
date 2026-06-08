---
title: "Agent Runtime - Tool Calls and Response Handling Maturity Note"
version: 3
last_refreshed: 2026-05-31
last_refreshed_by: codex
---

# Agent Runtime - Tool Calls and Response Handling Maturity Note

## Résumé

La gestion des appels d'outils et la normalisation des réponses sont bien couvertes dans la documentation et les tests : OpenClaw normalise les arguments d'appels d'outils malformés, les différences de charge utile spécifiques aux fournisseurs, la comptabilité d'utilisation et les flux d'échec terminal entre les adaptateurs et le code de transport partagé. La couverture est Stable. La qualité est Alpha car les preuves d'archive récentes montrent toujours des arguments d'outils vides, du JSON d'outils brut ou des blocs d'appels d'outils visibles, et une livraison d'assistant vide terminal qui fuit toujours des états surprenants aux utilisateurs.

## Portée de la catégorie

Cette catégorie couvre le comportement d'appels d'outils et de gestion des réponses visible par l'opérateur :
gestion fiable de la charge utile d'appels d'outils entre les fournisseurs, rapports d'utilisation et de réponse,
et récupération lorsque la sortie du fournisseur est malformée, vide ou
incomplète.

## Fonctionnalités

- Gestion des appels d'outils : Comportement fiable des appels d'outils entre les fournisseurs, y compris les différences de charge utile malformées ou spécifiques aux fournisseurs.
- Rapports d'utilisation et de réponse : IDs de réponse et comptabilité d'utilisation normalisés dans le comportement d'exécution visible par l'opérateur.
- Récupération d'échec : Finalisation et nettoyage du flux d'échec lorsque la sortie du fournisseur est malformée ou incomplète.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (80%)`

La couverture est forte entre les adaptateurs de fournisseurs, le code de transport partagé et les tests ciblés pour la coercition de charge utile d'outils, les IDs de réponse et l'utilisation, la sortie de fournisseur malformée et la finalisation d'échec.

## Score de qualité

- Score : `Alpha (66%)`

La normalisation est robuste dans la source, mais les rapports de terrain montrent que la sortie d'appels d'outils de fournisseur et les réponses malformées fuient toujours des états surprenants aux utilisateurs.

## Score de complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/agent-runtime-and-provider-execution.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la gestion des appels d'outils, les rapports d'utilisation et de réponse, la récupération d'échec.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les arguments d'appels d'outils vides ou malformés émergent toujours dans les cas limites spécifiques aux fournisseurs.
- Le JSON d'outils brut ou les blocs d'appels d'outils visibles apparaissent toujours dans certains modes locaux ou de compatibilité.
- Les réponses vides terminal et réservées aux outils ont toujours besoin d'une explication plus cohérente face à l'opérateur.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/concepts/agent-loop.md` documente les flux d'événements d'outils, le comportement de charge utile final et le comportement de délai d'attente autour de la boucle d'agent.
- `/Users/kevinlin/code/openclaw/docs/providers/ollama.md` documente l'appel d'outils natif, les avertissements de fiabilité du mode compatible OpenAI, le JSON d'outils brut en tant que texte, la gestion de la sortie brouillée et les avertissements de compatibilité d'appel d'outils.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/transport-stream-shared.ts` coerce les arguments d'appels d'outils de transport, fusionne les en-têtes et métadonnées, finalise les flux d'échec et normalise les détails d'erreur de transport.
- `/Users/kevinlin/code/openclaw/src/llm/providers/anthropic.ts` normalise les IDs d'outils diffusés et les arguments d'outils JSON partiels pour les réponses Anthropic.
- `/Users/kevinlin/code/openclaw/src/llm/providers/google-shared.ts` normalise les IDs d'appels d'outils, les arguments d'outils, les IDs de réponse et la comptabilité d'utilisation pour les fournisseurs de la famille Google.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.ts` formate les résultats vides terminal/réservés aux outils et relie les résultats d'outils normalisés dans les réponses visibles par l'opérateur.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.test.ts` couvre les résultats d'outils réservés aux médias, le repli de résultat terminal réservé au plan, la classification de résultat vide terminal, le dépouille des jetons `NO_REPLY` collés en tête, la livraison de résultats d'outils diffusés et la gestion des résultats réservés aux outils.
- `/Users/kevinlin/code/openclaw/src/agents/agent-tools.before-tool-call.integration.e2e.test.ts` couvre la modification de paramètres d'outils pilotée par hook, le blocage, la déduplication et le contexte autour de l'exécution d'appels d'outils.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/transport-stream-shared.test.ts` couvre la désinfection de substitut, le texte de charge utile d'outils non vide, la propagation d'en-têtes, la finalisation de flux réussie et le nettoyage d'échec.
- `/Users/kevinlin/code/openclaw/src/llm/providers/google-shared.test.ts` couvre la projection d'appels d'outils, les IDs de réponse et l'utilisation.
- `/Users/kevinlin/code/openclaw/src/llm/providers/anthropic.test.ts` couvre la relecture de réflexion signée et le comportement du fournisseur qui affecte la normalisation de charge utile d'outils.

### Requêtes Gitcrawl

- `gitcrawl --json search issues -R openclaw/openclaw "tool call streaming truncated tool_call provider"` a retourné #60593 sur les erreurs d'analyse JSON Anthropic streaming récurrentes, #70033 sur les appels d'outils émettant des arguments `{}` vides pour le contenu volumineux et #87711 sur la livraison d'assistant vide.
- `gitcrawl --json search issues -R openclaw/openclaw "openai-codex Anthropic Google provider tool call"` a retourné des problèmes adjacents aux adaptateurs pour les artefacts de session `claude-cli` et le chargement de plugin d'extension.
- `gitcrawl --json search prs -R openclaw/openclaw "provider error descriptors fallback rate limit"` a retourné #86642, qui améliore les descripteurs d'erreur de fournisseur structurés alimentant les erreurs d'exécution normalisées.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "tool call streaming"` a retourné des discussions de mai 2026 sur l'encapsulation streaming/appel d'outils du fournisseur, les blocs d'appels d'outils visibles, la visibilité des outils Claude CLI/WebChat et les mises à jour terminal manquantes.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "Ollama tool calling OpenClaw"` a retourné des rapports et des conseils sur les outils bruts imprimés en tant que texte et la compatibilité du modèle/appel d'outils.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "model fallback decision"` a retourné des journaux de repli où la sortie de fournisseur manquante ou vide a contribué aux chemins d'échec visibles par l'opérateur.
