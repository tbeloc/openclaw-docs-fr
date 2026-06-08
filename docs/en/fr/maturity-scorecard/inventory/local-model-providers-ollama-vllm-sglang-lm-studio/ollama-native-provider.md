---
title: "Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Note de Maturité des Plugins de Fournisseurs Natifs"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Note de Maturité des Plugins de Fournisseurs Natifs

## Résumé

Ollama est le fournisseur local le plus profondément intégré dans cette surface : le plugin utilise la sémantique native de l'API Ollama, dispose de la découverte, de la configuration, du streaming, de la recherche web, de la vision, de l'intégration, de la politique, de la couverture des risques WSL2 et des tests en direct, et la documentation met en garde contre le chemin `/v1` compatible OpenAI pour l'appel d'outils. La qualité est réduite par le volume de problèmes opérationnels vécus autour des points de terminaison locaux inaccessibles, du comportement cron/fallback, des refroidissements cloud, de la confusion entre le mode natif/local et des transitions d'intégration de mémoire.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Configuration d'Ollama et extraction de modèles : Couvre la configuration d'Ollama et l'extraction de modèles sur la découverte native de chat/modèle Ollama, la configuration cloud+local/local uniquement, les marqueurs d'authentification locaux, l'extraction de modèles et le comportement du fournisseur natif ollama associé.
- Découverte de modèles : Couvre la découverte de modèles sur la découverte native de chat/modèle Ollama, la configuration cloud+local/local uniquement, les marqueurs d'authentification locaux, l'extraction de modèles et le comportement du fournisseur natif ollama associé.
- Streaming et vision : Couvre le streaming et la vision sur la découverte native de chat/modèle Ollama, la configuration cloud+local/local uniquement, les marqueurs d'authentification locaux, l'extraction de modèles et le comportement du fournisseur natif ollama associé.
- Intégrations Ollama : Couvre les intégrations Ollama sur la découverte native de chat/modèle Ollama, la configuration cloud+local/local uniquement, les marqueurs d'authentification locaux, l'extraction de modèles et le comportement du fournisseur natif ollama associé.
- Support de la recherche web : Couvre le support de la recherche web sur la découverte native de chat/modèle Ollama, la configuration cloud+local/local uniquement, les marqueurs d'authentification locaux, l'extraction de modèles et le comportement du fournisseur natif ollama associé.
- Configuration de LM Studio : Couvre la configuration de LM Studio sur le plugin du fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI et les intégrations de mémoire LM Studio.
- Découverte de modèles et authentification : Couvre la découverte de modèles et l'authentification sur le plugin du fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI et les intégrations de mémoire LM Studio.
- Préchargement de modèles et chargement JIT : Couvre le préchargement de modèles et le chargement JIT sur le plugin du fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI et les intégrations de mémoire LM Studio.
- Compatibilité du streaming : Couvre la compatibilité du streaming sur le plugin du fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI et les intégrations de mémoire LM Studio.
- Intégrations LM Studio : Couvre les intégrations LM Studio sur le plugin du fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI et les intégrations de mémoire LM Studio.

## Fonctionnalités

- Configuration d'Ollama et extraction de modèles : Couvre la configuration d'Ollama et l'extraction de modèles sur la découverte native de chat/modèle Ollama, la configuration cloud+local/local uniquement, les marqueurs d'authentification locaux, l'extraction de modèles et le comportement du fournisseur natif ollama associé.
- Découverte de modèles : Couvre la découverte de modèles sur la découverte native de chat/modèle Ollama, la configuration cloud+local/local uniquement, les marqueurs d'authentification locaux, l'extraction de modèles et le comportement du fournisseur natif ollama associé.
- Streaming et vision : Couvre le streaming et la vision sur la découverte native de chat/modèle Ollama, la configuration cloud+local/local uniquement, les marqueurs d'authentification locaux, l'extraction de modèles et le comportement du fournisseur natif ollama associé.
- Intégrations Ollama : Couvre les intégrations Ollama sur la découverte native de chat/modèle Ollama, la configuration cloud+local/local uniquement, les marqueurs d'authentification locaux, l'extraction de modèles et le comportement du fournisseur natif ollama associé.
- Support de la recherche web : Couvre le support de la recherche web sur la découverte native de chat/modèle Ollama, la configuration cloud+local/local uniquement, les marqueurs d'authentification locaux, l'extraction de modèles et le comportement du fournisseur natif ollama associé.
- Configuration de LM Studio : Couvre la configuration de LM Studio sur le plugin du fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI et les intégrations de mémoire LM Studio.
- Découverte de modèles et authentification : Couvre la découverte de modèles et l'authentification sur le plugin du fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI et les intégrations de mémoire LM Studio.
- Préchargement de modèles et chargement JIT : Couvre le préchargement de modèles et le chargement JIT sur le plugin du fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI et les intégrations de mémoire LM Studio.
- Compatibilité du streaming : Couvre la compatibilité du streaming sur le plugin du fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI et les intégrations de mémoire LM Studio.
- Intégrations LM Studio : Couvre les intégrations LM Studio sur le plugin du fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI et les intégrations de mémoire LM Studio.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (86%)`
- Signaux positifs :
  - `/Users/kevinlin/code/openclaw/extensions/ollama/openclaw.plugin.json:2`
    déclare le fournisseur `ollama`, le plugin activé par défaut, l'entrée du
    catalogue de modèles, le marqueur d'authentification local, la variable
    d'environnement de configuration et les contrats d'intégration de mémoire et
    de recherche web.
  - `/Users/kevinlin/code/openclaw/extensions/ollama/index.ts:128` enregistre
    le fournisseur ; les lignes 132-143 enregistrent l'intégration de mémoire,
    la compréhension des médias, la recherche web et les vérifications de
    boucle de crash WSL2.
  - `/Users/kevinlin/code/openclaw/docs/providers/ollama.md:180` documente
    la découverte implicite de modèles ; les lignes 255-280 documentent les
    commandes de test en direct pour Ollama local et cloud.
  - `/Users/kevinlin/code/openclaw/extensions/ollama/ollama.live.test.ts:161`
    teste en direct `infer model run` ; les lignes 196-254 testent en direct le
    streaming natif ; et les lignes 271-329 testent en direct les intégrations
    et la recherche web.
- Signaux négatifs :
  - Certains comportements sont intentionnellement divisés entre la configuration
    Ollama native et Ollama compatible OpenAI, augmentant les pièges des
    opérateurs.
  - La couverture en direct dépend d'un runtime Ollama externe et de portes
    d'environnement, elle n'est donc pas toujours exercée dans l'IC ordinaire.
- Lacunes d'intégration :
  - Ajouter une preuve en direct routinière ou programmée pour le chemin texte
    local natif, la sélection exacte du modèle, le mode cloud+local et la
    sémantique de fallback.

## Score de Qualité

- Score : `Beta (78%)`
- Rapports Gitcrawl :
  - La requête `Ollama local provider` a retourné le problème #79329 concernant
    le saut de cron preflight lors d'une exécution lorsque le primaire local
    était inaccessible, le problème #74986 concernant `infer model run --local`
    qui se bloque et le problème #81214 autour du runtime du sous-agent
    utilisant Ollama local/distant.
  - La requête `Ollama cron local unreachable` a retourné le problème #79329 et
    la PR #82887, qui a corrigé le comportement du preflight de fallback cron.
- Rapports Discrawl :
  - La requête `Ollama local provider` a retourné une confirmation communautaire
    de test avec un vrai fournisseur Ollama local.
  - La requête `Ollama cron local unreachable` a retourné des conseils de
    support autour de `ollama list`, de l'incompatibilité Docker/Podman
    `127.0.0.1`, du statut de la passerelle, du statut du modèle et de
    l'inspection de la dernière exécution cron.
- Bonnes qualités :
  - Les conseils d'API native évitent directement l'échec courant de l'appel
    d'outil brut `/v1`.
  - Le fournisseur gère les marqueurs d'authentification local/LAN, le mode
    cloud, la découverte, les métadonnées du modèle, la vision, les
    intégrations, la recherche web et le risque spécifique à WSL2.
- Mauvaises qualités :
  - Un démon local arrêté, une incompatibilité d'hôte Docker, un mauvais ID de
    modèle ou une incompatibilité de mode cloud/local peuvent toujours créer
    des états d'échec confus.
  - Les preuves d'archive incluent plusieurs bugs récents ou fils de support
    autour de l'accessibilité locale, du comportement de fallback cron, des
    blocages et des refroidissements.
- Exclu de la qualité :
  - La couverture des tests, la profondeur d'intégration et l'absence de tests
    n'ont pas été utilisés comme entrées de qualité.

## Score de Complétude

- Score : `Stable (86%)`
- Instructions de surface : évaluées par rapport à `references/completeness/local-model-providers-ollama-vllm-sglang-lm-studio.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl
  couvrent la portée de la taxonomie pour la configuration d'Ollama et
  l'extraction de modèles, la découverte de modèles, le streaming et la vision,
  les intégrations Ollama, le support de la recherche web, la configuration de
  LM Studio, la découverte de modèles et l'authentification, le préchargement
  de modèles et le chargement JIT, la compatibilité du streaming et les
  intégrations LM Studio.
- Signaux négatifs : la note archivée a précédé la notation de complétude de
  la version 3 du processus, ce score est donc initialisé à partir de la même
  largeur de preuve et du registre des lacunes connues utilisés pour le score
  de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves`
  ci-dessous pour les branches manquantes enregistrées et les mises en garde
  visibles par l'opérateur.

## Lacunes Connues

- Les workflows cron et en arrière-plan devraient continuer à obtenir des
  messages d'opérateur plus clairs lorsqu'un primaire Ollama local est arrêté
  mais que des fallbacks existent.
- La documentation pourrait mieux exposer un arbre de décision de diagnostic
  pour les erreurs Ollama native par rapport à Ollama compatible OpenAI.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/ollama.md:10` décrit l'intégration native de l'API pour les serveurs cloud et locaux/auto-hébergés.
- `/Users/kevinlin/code/openclaw/docs/providers/ollama.md:12` avertit les utilisateurs distants de ne pas utiliser l'URL compatible OpenAI `/v1` car elle casse l'appel d'outils.
- `/Users/kevinlin/code/openclaw/docs/providers/ollama.md:180` documente la découverte implicite du fournisseur et les métadonnées `/api/tags`/`/api/show`.
- `/Users/kevinlin/code/openclaw/docs/providers/ollama.md:248` documente le comportement de préflight cron isolé pour les points de terminaison Ollama locaux inaccessibles.
- `/Users/kevinlin/code/openclaw/docs/providers/ollama.md:294` documente la vision Ollama et le support de la description d'images.

### Source

- `/Users/kevinlin/code/openclaw/extensions/ollama/index.ts:132` enregistre le fournisseur d'intégration mémoire ; la ligne 133 enregistre la compréhension des médias ; la ligne 142 enregistre la recherche web.
- `/Users/kevinlin/code/openclaw/extensions/ollama/src/discovery-shared.ts:117` classifie les URL de base Ollama locales.
- `/Users/kevinlin/code/openclaw/extensions/ollama/provider-discovery.ts:39` exécute la découverte du fournisseur via le chemin du catalogue de plugins.
- `/Users/kevinlin/code/openclaw/extensions/ollama/runtime-api.ts:3` exporte les API natives de flux, de compatibilité et d'enveloppe num-ctx.
- `/Users/kevinlin/code/openclaw/extensions/ollama/src/embedding-provider.ts` possède le comportement du client d'intégration mémoire Ollama.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/ollama/ollama.live.test.ts:161` teste en direct la CLI locale `infer model run`.
- `/Users/kevinlin/code/openclaw/extensions/ollama/ollama.live.test.ts:196` teste en direct le chat natif avec un préfixe de fournisseur personnalisé.
- `/Users/kevinlin/code/openclaw/extensions/ollama/ollama.live.test.ts:271` teste en direct les intégrations via le point de terminaison Ollama actuel.
- `/Users/kevinlin/code/openclaw/extensions/ollama/ollama.live.test.ts:301` teste en direct les points de terminaison de secours de recherche web Ollama.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/ollama/provider-discovery.test.ts:136` vérifie l'injection implicite native du fournisseur `api: "ollama"`.
- `/Users/kevinlin/code/openclaw/extensions/ollama/provider-discovery.test.ts:178` vérifie la découverte de la fenêtre de contexte à partir de `/api/show`.
- `/Users/kevinlin/code/openclaw/extensions/ollama/src/setup.test.ts:450` vérifie les fenêtres de contexte `/api/show` lors de la configuration.
- `/Users/kevinlin/code/openclaw/extensions/ollama/src/stream-runtime.test.ts:76` couvre la construction native de la requête de chat Ollama.
- `/Users/kevinlin/code/openclaw/extensions/ollama/src/embedding-provider.test.ts:104` vérifie les appels d'intégration `/api/embed` et la normalisation des vecteurs.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "Ollama local provider" --json --limit 5`

Résultats :

- A retourné le problème #79329 sur la réachabilité du fournisseur local cron, la PR #85373 sur le runtime du modèle résolu via l'authentification, le problème #74986 sur `infer model run --local` qui se bloque, la PR #87558 sur le streaming dense du fournisseur local, et le problème #81214 sur l'utilisation de Ollama par les sous-agents/runtime.

Requête : `gitcrawl search openclaw/openclaw --query "Ollama cron local unreachable" --json --limit 5`

Résultats :

- A retourné le problème #79329 et la PR #82887, le correctif pour le préflight des modèles de secours avant le comportement de saut cron.

### Requêtes Discrawl

Requête : `discrawl search --mode hybrid --limit 5 "Ollama local provider"`

Résultats :

- A retourné des messages récents de la communauté mentionnant des tests réels du fournisseur Ollama local.

Requête : `discrawl search --mode hybrid --limit 5 "Ollama cron local unreachable"`

Résultats :

- A retourné des conseils de support qui distinguent l'ID de modèle incorrect, l'env/config manquant, l'incompatibilité de l'URL de base Docker et l'hôte Ollama inaccessible.
