---
title: "Chemin du fournisseur OpenRouter - Note de maturité du streaming et de la relecture des appels d'outils"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur OpenRouter - Note de maturité du streaming et de la relecture des appels d'outils

## Résumé

La normalisation du streaming/relecture d'OpenRouter a une couverture ciblée forte pour `reasoning_details`, l'extraction de texte visible, les chunks d'appels d'outils répétés, les identifiants d'outils Mistral strict9, la relecture du raisonnement DeepSeek, le suivi du modèle de réponse et la normalisation du cache/utilisation. La couverture est Stable car les tests source et de régression couvrent directement les chemins historiquement fragiles.

La qualité est Beta car l'archive montre plusieurs régressions récentes et des fils de discussion autour des tours vides, de la portée strict9 et des champs de raisonnement spécifiques au fournisseur, bien que la branche main actuelle semble inclure les corrections correspondantes.

## Portée de la catégorie

Cette catégorie couvre l'analyse des réponses en streaming, l'extraction de la sortie visible depuis `reasoning_details` d'OpenRouter, la préservation des deltas d'appels d'outils, la politique de relecture Mistral strict9, les champs de relecture du raisonnement DeepSeek, l'assainissement de la signature de pensée Gemini, la capture du modèle de réponse et la normalisation des tokens de cache/utilisation.

## Fonctionnalités

- Analyse du contenu en streaming : Couvre l'analyse du contenu en streaming dans l'analyse des réponses en streaming, l'extraction de la sortie visible depuis `reasoning_details` d'OpenRouter, la préservation des deltas d'appels d'outils, la politique de relecture Mistral strict9 et le comportement de streaming et de relecture des appels d'outils associés.
- Sortie visible de reasoning_details : Couvre la sortie visible de reasoning_details dans l'analyse des réponses en streaming, l'extraction de la sortie visible depuis `reasoning_details` d'OpenRouter, la préservation des deltas d'appels d'outils, la politique de relecture Mistral strict9 et le comportement de streaming et de relecture des appels d'outils associés.
- Préservation des deltas d'appels d'outils : Couvre la préservation des deltas d'appels d'outils dans l'analyse des réponses en streaming, l'extraction de la sortie visible depuis `reasoning_details` d'OpenRouter, la préservation des deltas d'appels d'outils, la politique de relecture Mistral strict9 et le comportement de streaming et de relecture des appels d'outils associés.
- Politique de relecture spécifique à la famille : Couvre la politique de relecture spécifique à la famille dans l'analyse des réponses en streaming, l'extraction de la sortie visible depuis `reasoning_details` d'OpenRouter, la préservation des deltas d'appels d'outils, la politique de relecture Mistral strict9 et le comportement de streaming et de relecture des appels d'outils associés.
- Normalisation du modèle de réponse et de l'utilisation : Couvre la normalisation du modèle de réponse et de l'utilisation dans l'analyse des réponses en streaming, l'extraction de la sortie visible depuis `reasoning_details` d'OpenRouter, la préservation des deltas d'appels d'outils, la politique de relecture Mistral strict9 et le comportement de streaming et de relecture des appels d'outils associés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : Les tests de régression couvrent les détails du raisonnement OpenRouter/Qwen3, les appels d'outils dans le même chunk, les chunks de raisonnement répétés, le texte de réponse visible, les exclusions de texte de raisonnement ambigu, la normalisation des champs de relecture et la politique Mistral strict9.
- Signaux négatifs : Les tests toujours actifs simulent les charges utiles du fournisseur ; la preuve en direct est contrôlée et ne peut pas couvrir la matrice complète des fournisseurs en amont d'OpenRouter.
- Lacunes d'intégration : Ajouter une matrice en direct périodique pour les appels d'outils Mistral d'OpenRouter, le streaming de reasoning-details Qwen/GLM, le texte de raisonnement visible MiniMax et la relecture DeepSeek V4.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl : Les recherches d'archive ont trouvé #58012 et les PR associées pour la régression de l'identifiant d'appel d'outil strict9, plus les fermetures de problèmes de réponse vide liées aux corrections `reasoning_details` d'OpenRouter.
- Rapports Discrawl : La recherche Discord a trouvé des rapports d'avril 2026 concernant les tours complétés vides d'OpenRouter, `payloads=0`, les URL de base obsolètes et la sortie visible dans les champs `reasoning_details` sur les versions plus anciennes.
- Bonnes qualités : La source actuelle contient des politiques de relecture explicitement délimitées par fournisseur, des vérifications de route vérifiées, la gestion du texte de réponse visible et l'assainissement de la relecture pour les champs de raisonnement d'OpenRouter.
- Mauvaises qualités : Le nombre de corrections récentes montre que cette surface est fragile et couplée aux formes de réponse changeantes des fournisseurs en amont.
- Exclu de la qualité : L'étendue des tests de régression et l'existence de tests contrôlés en direct sont des entrées de couverture uniquement.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openrouter-provider-path.md`.
- Signaux positifs : Les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'analyse du contenu en streaming, la sortie visible de reasoning_details, la préservation des deltas d'appels d'outils, la politique de relecture spécifique à la famille et la normalisation du modèle de réponse et de l'utilisation.
- Signaux négatifs : La note archivée a précédé le scoring de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les tests actuels sont larges mais simulent toujours les formes de charge utile connues plutôt que les formes futures inconnues en amont d'OpenRouter.
- `openrouter/auto` peut router vers des fournisseurs avec une sémantique de réponse qu'OpenClaw n'a pas explicitement vue auparavant.
- La transparence de l'utilisation/coût et du modèle de réponse restent des problèmes adjacents lorsqu'OpenRouter route via un backend différent de celui demandé.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/openrouter.md` documente la relecture du raisonnement DeepSeek V4, l'élimination du prefill Anthropic, le comportement de la route soutenue par Gemini et la gestion compatible OpenAI de style proxy.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md` documente le marqueur de cache OpenRouter et la gestion de la signature de pensée Gemini.

### Source

- `/Users/kevinlin/code/openclaw/extensions/openrouter/index.ts` construit la politique de relecture OpenRouter, y compris la gestion Mistral strict9.
- `/Users/kevinlin/code/openclaw/extensions/openrouter/stream.ts` corrige les charges utiles OpenRouter Anthropic, DeepSeek V4 et de routage.
- `/Users/kevinlin/code/openclaw/src/agents/openai-transport-stream.ts` analyse `reasoning_details` d'OpenRouter, assainit les champs de raisonnement de relecture, préserve le raisonnement OpenRouter lorsqu'il est valide et mappe l'utilisation.
- `/Users/kevinlin/code/openclaw/src/llm/providers/openai-completions.ts` suit le modèle de réponse, analyse les détails du raisonnement et mappe l'utilisation du cache-read/cache-write d'OpenRouter.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/openrouter/openrouter.live.test.ts` contrôle en direct les observations de complétion et de cache d'OpenRouter.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner.e2e.test.ts` couvre la résolution explicite du modèle OpenRouter via des exécutions intégrées.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/openrouter/index.test.ts` couvre la politique Mistral strict9, le raisonnement DeepSeek V4, l'élimination du prefill Anthropic et les exclusions de route personnalisée.
- `/Users/kevinlin/code/openclaw/src/agents/openai-transport-stream.test.ts` couvre `reasoning_details` d'OpenRouter, la préservation des appels d'outils, l'extraction du texte visible, l'assainissement de la relecture et l'ordre du texte de réponse.
- `/Users/kevinlin/code/openclaw/src/llm/providers/stream-wrappers/proxy.test.ts` couvre le comportement du wrapper de flux OpenRouter et les correctifs contrôlés par route.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "OpenRouter Mistral strict9 tool_call invalid_function_call DeepSeek reasoning"`

Résultats :

- Aucun résultat direct pour la phrase exacte.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "reasoning_details OpenRouter payloads zero content null"`

Résultats :

- Aucun résultat direct pour la phrase exacte.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "OpenRouter"`

Résultats :

- Retourné #62100 sur les références de modèle slash natif OpenRouter, #63062 sur les corrections de charge utile de contrôle de cache, #79370 sur la rétention de cache Anthropic OpenRouter et #87562 sur la réconciliation des coûts en streaming.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "OpenRouter strict9"`

Résultats :

- Trouvé #58012 et la discussion PR associée pour la régression de l'identifiant d'appel d'outil Mistral-via-OpenRouter strict9, y compris les commentaires d'examen sur la portée de strict9 uniquement aux routes OpenRouter de la famille Mistral.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "OpenRouter reasoning_details"`

Résultats :

- Trouvé les rapports d'avril 2026 et les commentaires de fermeture pour les réponses OpenRouter vides, `payloads=0`, Qwen3 `reasoning_details` et les corrections `response.output_text` / `response.text` visibles.
