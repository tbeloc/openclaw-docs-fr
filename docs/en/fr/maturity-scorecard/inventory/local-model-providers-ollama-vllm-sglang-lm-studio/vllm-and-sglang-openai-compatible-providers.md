---
title: "Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Note de maturité des fournisseurs compatibles OpenAI vLLM et SGLang"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Note de maturité des fournisseurs compatibles OpenAI vLLM et SGLang

## Résumé

vLLM et SGLang sont des plugins de fournisseur groupés de première classe, mais ils partagent intentionnellement le chemin de configuration/découverte OpenAI-compatible auto-hébergé. Cela leur donne une véritable histoire d'intégration et de découverte de modèles tout en laissant une grande partie du comportement d'exécution le plus difficile aux modèles de chat spécifiques au backend, aux analyseurs d'appels d'outils et à la configuration des opérateurs. vLLM dispose d'un support supplémentaire de politique de réflexion ; SGLang est plus fin et plus générique.

## Portée de la catégorie

Cette catégorie couvre les plugins de fournisseur groupés `vllm` et `sglang`, la documentation, le comportement par défaut env/URL de base, la découverte `/v1/models`, la configuration non-interactive, les contrôles de réflexion vLLM, la sémantique des requêtes de style proxy et les bords de compatibilité connus avec OpenAI Chat-Completions.

## Fonctionnalités

- Configuration du fournisseur groupé : Couvre la configuration du fournisseur groupé sur les plugins de fournisseur groupés `vllm` et `sglang`, la documentation, le comportement par défaut env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs vllm et sglang compatibles openai-compatible.
- Point de terminaison de découverte de modèles : Couvre le point de terminaison de découverte de modèles sur les plugins de fournisseur groupés `vllm` et `sglang`, la documentation, le comportement par défaut env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs vllm et sglang compatibles openai-compatible.
- Configuration non-interactive : Couvre la configuration non-interactive sur les plugins de fournisseur groupés `vllm` et `sglang`, la documentation, le comportement par défaut env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs vllm et sglang compatibles openai-compatible.
- Contrôles de réflexion vLLM : Couvre les contrôles de réflexion vLLM sur les plugins de fournisseur groupés `vllm` et `sglang`, la documentation, le comportement par défaut env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs vllm et sglang compatibles openai-compatible.
- Sémantique de chat et d'outils compatible OpenAI : Couvre la sémantique de chat et d'outils compatible OpenAI sur les plugins de fournisseur groupés `vllm` et `sglang`, la documentation, le comportement par défaut env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs vllm et sglang compatibles openai-compatible.
- Conseils de compatibilité SGLang : Couvre les conseils de compatibilité SGLang sur les plugins de fournisseur groupés `vllm` et `sglang`, la documentation, le comportement par défaut env/URL de base, la découverte `/v1/models` et le comportement des fournisseurs vllm et sglang compatibles openai-compatible.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs :
  - `/Users/kevinlin/code/openclaw/extensions/vllm/openclaw.plugin.json:2`
    et `/Users/kevinlin/code/openclaw/extensions/sglang/openclaw.plugin.json:2`
    définissent les fournisseurs groupés activés par défaut avec support
    d'utilisation en streaming compatible OpenAI.
  - `/Users/kevinlin/code/openclaw/extensions/vllm/index.ts:26` et
    `/Users/kevinlin/code/openclaw/extensions/sglang/index.ts:25` enregistrent
    la configuration du fournisseur, la découverte, les choix d'authentification
    et les métadonnées du sélecteur de modèles.
  - `/Users/kevinlin/code/openclaw/src/plugins/provider-self-hosted-setup.ts:138`
    découvre les catalogues OpenAI-compatible `/models` en utilisant une
    récupération protégée.
  - `/Users/kevinlin/code/openclaw/extensions/vllm/stream.ts:123` encapsule
    les charges utiles de flux vLLM pour les contrôles de réflexion
    Qwen/Nemotron.
- Signaux négatifs :
  - L'audit n'a pas trouvé de tests en direct vLLM ou SGLang analogues au test
    en direct Ollama.
  - SGLang a actuellement une surface d'implémentation beaucoup plus fine que
    vLLM : découverte/configuration et comportement de politique de relecture
    sans wrappers de transport spécifiques au fournisseur.
- Lacunes d'intégration :
  - Ajouter des tests de serveur faux locaux ou en direct avec opt-in pour
    `/v1/models`, `/v1/chat/completions`, utilisation en streaming et un chemin
    de modèle capable d'appels d'outils pour vLLM et SGLang.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl :
  - La requête `vLLM tool calls raw text` a retourné le problème ouvert #87687
    pour l'analyseur de flux OpenAI-compatible vLLM supprimant `tool_calls`
    quand `reasoning_content` diffuse en premier, plus une PR de requête
    d'intégration connexe.
  - La requête `SGLang OpenAI-compatible local` a retourné le problème #81961
    et la PR #68019 mais peu de preuves de défaut spécifiques à SGLang.
- Rapports Discrawl :
  - La requête `vLLM tool calls raw text` a retourné le problème #49508 et les
    discussions d'assistance décrivant la sortie XML/texte brute vLLM/Qwen
    `<tool_call>` et les exigences d'analyseur d'outils.
  - La requête `SGLang OpenAI-compatible local` a retourné des messages
    confirmant le support de découverte/configuration locale pour vLLM/SGLang
    et des conseils communautaires selon lesquels ces fournisseurs sont
    supportés en général, mais peuvent ne pas être le meilleur choix pour les
    appareils contraints et peuvent ajouter des problèmes de compatibilité.
- Bonnes qualités :
  - Les fournisseurs utilisent un chemin de configuration partagé et explicite
    avec les valeurs par défaut `openai-completions` correctes, les variables
    env spécifiques au fournisseur, l'opt-in de découverte dynamique et les
    drapeaux d'utilisation en streaming.
  - vLLM dispose de wrappers de réflexion Qwen et Nemotron ciblés, évitant une
    approche générique unique.
- Mauvaises qualités :
  - La fiabilité des appels d'outils vLLM dépend fortement des drapeaux de
    démarrage du modèle/analyseur en amont, et les preuves d'archive montrent
    que le texte brut des appels d'outils atteint toujours les utilisateurs.
  - SGLang est documenté et découvrable, mais la couverture source est
    principalement une plomberie OpenAI-compatible générique avec une
    résilience spécifique au fournisseur limitée.
- Exclus de la qualité :
  - La couverture des tests, la profondeur d'intégration et l'absence de tests
    n'ont pas été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/local-model-providers-ollama-vllm-sglang-lm-studio.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl
  couvrent la portée de la taxonomie pour la configuration du fournisseur
  groupé, le point de terminaison de découverte de modèles, la configuration
  non-interactive, les contrôles de réflexion vLLM, la sémantique de chat et
  d'outils compatible OpenAI, les conseils de compatibilité SGLang.
- Signaux négatifs : la note archivée a précédé la notation de complétude de
  la version 3 du processus, donc ce score est initialisé à partir de la même
  largeur de preuves et du registre des lacunes connues utilisés pour le score
  de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves`
  ci-dessous pour les branches manquantes enregistrées et les avertissements
  visibles par l'opérateur.

## Lacunes connues

- vLLM a besoin d'une preuve d'opérateur plus claire autour du démarrage de
  l'analyseur d'appels d'outils et du streaming de contenu de réflexion.
- SGLang a besoin soit de plus de gestion d'exécution spécifique au fournisseur,
  soit de documentation explicite expliquant qu'il s'agit actuellement d'un
  chemin de fournisseur OpenAI-compatible fin.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/vllm.md:9` indique qu'OpenClaw
  se connecte à vLLM avec `openai-completions`.
- `/Users/kevinlin/code/openclaw/docs/providers/vllm.md:64` documente la
  découverte implicite de modèles à partir de `GET /v1/models`.
- `/Users/kevinlin/code/openclaw/docs/providers/vllm.md:130` documente le
  comportement de style proxy ; les lignes 146-207 documentent les contrôles de
  réflexion Qwen/Nemotron.
- `/Users/kevinlin/code/openclaw/docs/providers/vllm.md:230` documente les
  exigences d'analyseur/modèle d'outils Qwen et `tool_choice: "required"`.
- `/Users/kevinlin/code/openclaw/docs/providers/sglang.md:9` indique que
  SGLang utilise la famille de fournisseur `openai-completions` compatible
  OpenAI avec découverte.

### Source

- `/Users/kevinlin/code/openclaw/extensions/vllm/defaults.ts:1` déclare l'URL
  de base vLLM par défaut et la variable env.
- `/Users/kevinlin/code/openclaw/extensions/sglang/defaults.ts:1` déclare l'URL
  de base SGLang par défaut et la variable env.
- `/Users/kevinlin/code/openclaw/extensions/vllm/models.ts:12` découvre les
  modèles vLLM à partir d'un point de terminaison `/models` auto-hébergé.
- `/Users/kevinlin/code/openclaw/extensions/sglang/models.ts:12` découvre les
  modèles SGLang à partir d'un point de terminaison `/models` auto-hébergé.
- `/Users/kevinlin/code/openclaw/extensions/vllm/thinking-policy.ts:54`
  expose les profils de réflexion binaires pour les modèles vLLM configurés.
- `/Users/kevinlin/code/openclaw/extensions/sglang/index.ts:91` signale les
  conseils d'authentification/configuration manquants pour SGLang.

### Tests d'intégration

- Aucun test en direct vLLM ou SGLang n'a été trouvé dans cet audit.
- `/Users/kevinlin/code/openclaw/src/plugins/provider-self-hosted-setup.test.ts:88`
  teste le chemin de découverte de modèles OpenAI-compatible partagé avec une
  réponse de serveur `/v1/models` local simulée.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/plugins/provider-self-hosted-setup.test.ts:399`
  vérifie la configuration vLLM et SGLang non-interactive plus les écritures de
  profil d'authentification.
- `/Users/kevinlin/code/openclaw/extensions/vllm/provider-discovery.contract.test.ts:12`
  vérifie l'enregistrement du fournisseur vLLM et l'exposition du hook de
  profil de réflexion.
- `/Users/kevinlin/code/openclaw/extensions/vllm/stream.test.ts:46` vérifie
  les charges utiles de réflexion du modèle de chat Qwen.
- `/Users/kevinlin/code/openclaw/extensions/vllm/stream.test.ts:156` vérifie
  l'injection de charge utile de réflexion désactivée Nemotron.
- `/Users/kevinlin/code/openclaw/extensions/sglang/index.test.ts:5` vérifie le
  comportement de politique de relecture SGLang.
- `/Users/kevinlin/code/openclaw/extensions/sglang/provider-discovery.contract.test.ts`
  vérifie le comportement du contrat de découverte du fournisseur SGLang.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "vLLM tool calls raw text" --json --limit 5`

Résultats :

- A retourné le problème ouvert #87687, "vllm openai-completions streaming
  parser drops tool_calls when reasoning_content streams first for gpt-oss-120b
  at large systemPrompt".

Requête : `gitcrawl search openclaw/openclaw --query "SGLang OpenAI-compatible local" --json --limit 5`

Résultats :

- A retourné le problème #81961 autour de l'UX du tableau de bord du
  fournisseur de modèles et la PR #68019 avec des exemples de modèles
  SGLang/vLLM dans le travail de mémoire-core, mais aucun défaut d'exécution
  SGLang concret dans les cinq premiers résultats.

### Requêtes Discrawl

Requête : `discrawl search --mode hybrid --limit 5 "vLLM tool calls raw text"`

Résultats :

- A retourné le problème #49508 et la discussion d'assistance expliquant la
  sortie XML/texte brute vLLM/Qwen `<tool_call>` et la nécessité d'une
  configuration d'analyseur d'appels d'outils et de modèle de chat en amont.

Requête : `discrawl search --mode hybrid --limit 5 "SGLang OpenAI-compatible local"`

Résultats :

- A retourné des messages confirmant le support de découverte/configuration
  locale pour vLLM/SGLang et des conseils communautaires selon lesquels ces
  fournisseurs sont supportés en général mais peuvent ajouter des problèmes de
  compatibilité sur le matériel contraint.
