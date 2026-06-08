---
title: "Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Note de maturité de compatibilité du runtime compatible OpenAI"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Note de maturité de compatibilité du runtime compatible OpenAI

## Résumé

OpenClaw dispose d'une machinerie de compatibilité mature pour les différences de requête et de flux des fournisseurs locaux : la documentation explique les backends strictement compatibles avec OpenAI, le code du fournisseur encapsule le comportement de LM Studio, Ollama, vLLM et SGLang, et les tests couvrent le texte brut des appels d'outils, les drapeaux de réflexion, les clés de message strictes et les contrôles de contexte. Le risque restant est opérationnel : les serveurs locaux diffèrent toujours par le modèle, le modèle, l'analyseur et les drapeaux d'exécution, de sorte que les utilisateurs peuvent atteindre une sortie d'appel d'outil brute ou des défaillances spécifiques au fournisseur même lorsque le chemin de code est couvert.

## Portée de la catégorie

Inclus dans cette catégorie :

- Configuration du fournisseur groupé : couvre la configuration du fournisseur groupé sur les plugins de fournisseur `vllm` et `sglang` groupés, la documentation, le comportement par défaut de l'env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs openai-compatible vllm et sglang associés.
- Point de terminaison de découverte de modèle : couvre le point de terminaison de découverte de modèle sur les plugins de fournisseur `vllm` et `sglang` groupés, la documentation, le comportement par défaut de l'env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs openai-compatible vllm et sglang associés.
- Configuration non interactive : couvre la configuration non interactive sur les plugins de fournisseur `vllm` et `sglang` groupés, la documentation, le comportement par défaut de l'env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs openai-compatible vllm et sglang associés.
- Contrôles de réflexion vLLM : couvre les contrôles de réflexion vLLM sur les plugins de fournisseur `vllm` et `sglang` groupés, la documentation, le comportement par défaut de l'env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs openai-compatible vllm et sglang associés.
- Sémantique de chat et d'outils compatible OpenAI : couvre la sémantique de chat et d'outils compatible OpenAI sur les plugins de fournisseur `vllm` et `sglang` groupés, la documentation, le comportement par défaut de l'env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs openai-compatible vllm et sglang associés.
- Guidance de compatibilité SGLang : couvre la guidance de compatibilité SGLang sur les plugins de fournisseur `vllm` et `sglang` groupés, la documentation, le comportement par défaut de l'env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs openai-compatible vllm et sglang associés.
- Compatibilité du flux de requête : couvre la compatibilité du flux de requête sur la mise en forme des requêtes de style chat et Responses, la normalisation du flux, la compatibilité des appels d'outils, les contrôles de raisonnement du modèle local et le comportement associé de compatibilité du flux de requête et d'appel d'outils.
- Appel d'outils : couvre l'appel d'outils sur la mise en forme des requêtes de style chat et Responses, la normalisation du flux, la compatibilité des appels d'outils, les contrôles de raisonnement du modèle local et le comportement associé de compatibilité du flux de requête et d'appel d'outils.

## Fonctionnalités

- Configuration du fournisseur groupé : couvre la configuration du fournisseur groupé sur les plugins de fournisseur `vllm` et `sglang` groupés, la documentation, le comportement par défaut de l'env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs openai-compatible vllm et sglang associés.
- Point de terminaison de découverte de modèle : couvre le point de terminaison de découverte de modèle sur les plugins de fournisseur `vllm` et `sglang` groupés, la documentation, le comportement par défaut de l'env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs openai-compatible vllm et sglang associés.
- Configuration non interactive : couvre la configuration non interactive sur les plugins de fournisseur `vllm` et `sglang` groupés, la documentation, le comportement par défaut de l'env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs openai-compatible vllm et sglang associés.
- Contrôles de réflexion vLLM : couvre les contrôles de réflexion vLLM sur les plugins de fournisseur `vllm` et `sglang` groupés, la documentation, le comportement par défaut de l'env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs openai-compatible vllm et sglang associés.
- Sémantique de chat et d'outils compatible OpenAI : couvre la sémantique de chat et d'outils compatible OpenAI sur les plugins de fournisseur `vllm` et `sglang` groupés, la documentation, le comportement par défaut de l'env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs openai-compatible vllm et sglang associés.
- Guidance de compatibilité SGLang : couvre la guidance de compatibilité SGLang sur les plugins de fournisseur `vllm` et `sglang` groupés, la documentation, le comportement par défaut de l'env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs openai-compatible vllm et sglang associés.
- Compatibilité du flux de requête : couvre la compatibilité du flux de requête sur la mise en forme des requêtes de style chat et Responses, la normalisation du flux, la compatibilité des appels d'outils, les contrôles de raisonnement du modèle local et le comportement associé de compatibilité du flux de requête et d'appel d'outils.
- Appel d'outils : couvre l'appel d'outils sur la mise en forme des requêtes de style chat et Responses, la normalisation du flux, la compatibilité des appels d'outils, les contrôles de raisonnement du modèle local et le comportement associé de compatibilité du flux de requête et d'appel d'outils.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs :
  - `/Users/kevinlin/code/openclaw/docs/gateway/local-models.md:218` jusqu'à
    la ligne 260 documentent le comportement strict du backend, `requiresStringContent` et
    la compatibilité des appels d'outils.
  - `/Users/kevinlin/code/openclaw/docs/gateway/local-models.md:268` jusqu'à
    la ligne 300 documentent les contrôles de reasoning-effort et de réflexion pour les backends locaux.
  - `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/stream.ts:176`
    jusqu'à la ligne 264 gère la compatibilité d'utilisation du préchargement et du flux.
  - `/Users/kevinlin/code/openclaw/extensions/vllm/stream.ts:13` jusqu'à la ligne
    140 encapsule le comportement du flux vLLM, y compris les aides à la compatibilité.
  - `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/replay-history.ts:828`
    empêche les fournisseurs strictement compatibles avec OpenAI de recevoir des métadonnées d'assistant non supportées.
- Signaux négatifs :
  - Le succès des appels d'outils dépend toujours de la configuration du parser et du chat-template du backend qu'OpenClaw peut documenter et adapter mais ne peut pas entièrement appliquer sur tous les serveurs de modèles locaux.
  - SGLang partage le chemin compatible OpenAI mais a moins de preuves de flux spécifiques au fournisseur que LM Studio, Ollama et vLLM.
- Lacunes d'intégration :
  - Ajouter une matrice de fixture de serveur local pour JSON brut, texte entre crochets, texte d'outil Harmony, relecture de message strictement compatible OpenAI et contrôles de réflexion sur les familles de fournisseurs locaux nommées.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl :
  - La requête `vLLM tool calls raw text` a retourné le problème #87687 et la PR #79702,
    montrant une pression réelle autour de la sortie des appels d'outils vLLM et du comportement du parser/template spécifique au fournisseur.
  - La requête `local model tool calls raw JSON` a retourné le problème #85883 et les discussions d'échec d'appel d'outils associées.
- Rapports Discrawl :
  - La requête `vLLM tool calls raw text` a retourné des threads d'assistance où les modèles locaux émettaient du XML `<tool_call>` brut ou du texte et les utilisateurs avaient besoin de guidance sur le parser ou le template vLLM.
  - La requête `OpenAI-compatible local backend tool calls requiresStringContent` a retourné une guidance d'assistance recommandant `compat.requiresStringContent` pour les serveurs locaux strictement compatibles avec OpenAI.
- Bonnes qualités :
  - Les contrôles de compatibilité sont explicites et documentés au lieu d'être cachés dans le code du fournisseur : `requiresStringContent`, clés strictes, drapeaux de réflexion et champs de corps spécifiques au backend peuvent être raisonnés par les opérateurs.
  - Les adaptateurs de flux isolent les particularités spécifiques au fournisseur afin que le code d'agent de niveau supérieur puisse utiliser des événements normalisés.
- Mauvaises qualités :
  - Les preuves d'archive montrent que les utilisateurs rencontrent toujours une sortie d'appel d'outil brute et ont besoin de correctifs spécifiques au modèle/serveur en dehors d'OpenClaw.
  - La surface de compatibilité est puissante mais fragmentée sur la documentation des fournisseurs, la documentation de la passerelle et les champs de configuration du fournisseur.
- Exclus de la qualité :
  - La couverture des tests et le nombre de tests de compatibilité de flux n'ont pas été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/local-model-providers-ollama-vllm-sglang-lm-studio.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration du fournisseur groupé, le point de terminaison de découverte de modèle, la configuration non interactive, les contrôles de réflexion vLLM, la sémantique de chat et d'outils compatible OpenAI, la guidance de compatibilité SGLang, la compatibilité du flux de requête, l'appel d'outils.
- Signaux négatifs : la note archivée a précédé le scoring de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucun tableau de dépannage unique ne mappe les symptômes d'appel d'outil brut au paramètre exact du fournisseur pour LM Studio, le mode compatible OpenAI d'Ollama, vLLM et SGLang.
- Les preuves spécifiques à SGLang pour les appels d'outils sont plus minces que les preuves partagée compatible OpenAI et vLLM.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/gateway/local-models.md:218` documente
  les directives strictes de compatibilité backend et tool-call.
- `/Users/kevinlin/code/openclaw/docs/gateway/local-models.md:268` documente
  les contrôles locaux de reasoning-effort.
- `/Users/kevinlin/code/openclaw/docs/gateway/local-models.md:302` documente
  les ajustements backend plus petits et plus stricts.
- `/Users/kevinlin/code/openclaw/docs/providers/vllm.md:230` documente la
  configuration des tool-call Qwen pour vLLM.
- `/Users/kevinlin/code/openclaw/docs/providers/lmstudio.md:101` documente
  l'utilisation du streaming LM Studio et la compatibilité thinking.

### Source

- `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/stream.ts:176`
  gère les champs de préchargement et d'utilisation du streaming LM Studio.
- `/Users/kevinlin/code/openclaw/extensions/vllm/stream.ts:13` implémente le
  wrapper de flux de compatibilité vLLM.
- `/Users/kevinlin/code/openclaw/extensions/vllm/thinking-policy.ts:54`
  décide quand thinking est activé pour les modèles vLLM.
- `/Users/kevinlin/code/openclaw/extensions/ollama/runtime-api.ts:3` exporte
  les helpers de streaming et de compatibilité du runtime Ollama.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/replay-history.ts:828`
  supprime les métadonnées d'assistant non supportées pour les fournisseurs stricts.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/stream.test.ts:541`
  couvre le texte tool-call du modèle local entre crochets.
- `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/stream.test.ts:596`
  couvre le texte tool-call du modèle local Harmony.
- `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/stream.test.ts:639`
  couvre le comportement pass-through pour le texte tool non enregistré.
- `/Users/kevinlin/code/openclaw/extensions/vllm/stream.test.ts:46` jusqu'à
  la ligne 118 couvrent la compatibilité du flux vLLM.
- `/Users/kevinlin/code/openclaw/extensions/vllm/stream.test.ts:198` jusqu'à
  la ligne 233 couvrent la gestion de la sortie tool-call vLLM.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/ollama/src/stream-runtime.test.ts:119`
  couvre le wrapper de flux de compatibilité Ollama configuré.
- `/Users/kevinlin/code/openclaw/extensions/ollama/src/stream-runtime.test.ts:158`
  couvre la gestion du fallback `num_ctx`.
- `/Users/kevinlin/code/openclaw/extensions/ollama/src/stream-runtime.test.ts:193`
  couvre le comportement `thinking=false`.
- `/Users/kevinlin/code/openclaw/extensions/ollama/src/stream-runtime.test.ts:402`
  couvre le comportement avec thinking activé.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "vLLM tool calls raw text" --json --limit 5`

Résultats :

- A retourné le problème #87687 et la PR #79702, tous deux pertinents pour le
  comportement du tool-call vLLM et du parser/template.

Requête : `gitcrawl search openclaw/openclaw --query "local model tool calls raw JSON" --json --limit 5`

Résultats :

- A retourné le problème #85883 et les discussions connexes sur les échecs de
  tool-call du modèle local.

### Requêtes Discrawl

Requête : `discrawl search --mode hybrid --limit 5 "vLLM tool calls raw text"`

Résultats :

- A retourné des threads de support décrivant le XML ou le texte brut
  `<tool_call>` des modèles locaux basés sur vLLM et le besoin de directives
  parser/template.

Requête : `discrawl search --mode hybrid --limit 5 "OpenAI-compatible local backend tool calls requiresStringContent"`

Résultats :

- A retourné des directives de support recommandant `compat.requiresStringContent`
  pour les fournisseurs locaux stricts compatibles avec OpenAI.
