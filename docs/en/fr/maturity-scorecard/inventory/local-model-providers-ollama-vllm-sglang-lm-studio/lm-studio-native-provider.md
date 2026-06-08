---
title: "Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Note de maturité du fournisseur natif LM Studio"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Note de maturité du fournisseur natif LM Studio

## Résumé

Le fournisseur LM Studio est un plugin fournisseur fourni et activé par défaut avec
une configuration interactive et non-interactive, une découverte de modèles, une authentification locale synthétique,
un préchargement de modèles, une compatibilité d'utilisation en streaming, et un adaptateur d'intégration mémoire.
Sa documentation et son code source sont matériellement plus solides qu'une entrée proxy générique, mais
les preuves archivées montrent toujours une inadéquation des points de terminaison, une pression sur les ressources et une confusion des délais d'expiration
dans l'utilisation réelle.

## Portée de la catégorie

Cette catégorie couvre le plugin fournisseur LM Studio, la documentation `/providers/lmstudio`,
la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI,
et les intégrations mémoire LM Studio.

## Fonctionnalités

- Configuration LM Studio : Couvre la configuration LM Studio sur le plugin fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI, et les intégrations mémoire LM Studio.
- Découverte de modèles et authentification : Couvre la découverte de modèles et l'authentification sur le plugin fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI, et les intégrations mémoire LM Studio.
- Préchargement de modèles et chargement JIT : Couvre le préchargement de modèles et le chargement JIT sur le plugin fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI, et les intégrations mémoire LM Studio.
- Compatibilité du streaming : Couvre la compatibilité du streaming sur le plugin fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI, et les intégrations mémoire LM Studio.
- Intégrations mémoire LM Studio : Couvre les intégrations mémoire LM Studio sur le plugin fournisseur LM Studio, la documentation `/providers/lmstudio`, la découverte de modèles à partir des API LM Studio, le comportement d'authentification pour les instances locales et authentifiées, le comportement de préchargement/JIT, le streaming compatible OpenAI, et les intégrations mémoire LM Studio.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs :
  - `/Users/kevinlin/code/openclaw/extensions/lmstudio/openclaw.plugin.json:2`
    déclare l'ID du fournisseur `lmstudio`, le statut activé par défaut, le support d'utilisation en streaming,
    les variables d'environnement de configuration, le marqueur d'authentification non-secret, et le contrat d'intégration mémoire.
  - `/Users/kevinlin/code/openclaw/extensions/lmstudio/index.ts:55`
    enregistre le fournisseur ; la ligne 56 enregistre le fournisseur d'intégration mémoire ;
    les lignes 69-89 câblent la configuration et la découverte.
  - `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/models.fetch.ts:74`
    récupère `/api/v1/models`, et la ligne 183 démarre le contrôle préalable de chargement de modèle natif.
  - `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/stream.ts:176`
    enveloppe le flux de base avec la compatibilité d'appel d'outil en texte brut local et le comportement de préchargement.
- Signaux négatifs :
  - L'audit a trouvé des tests solides au niveau des composants mais aucun fichier de test LM Studio en direct dédié équivalent au test Ollama en direct.
  - Le comportement à l'exécution dépend de l'état externe de LM Studio : modèle chargé ou chargeable, mode d'authentification, paramètres JIT/TTL, et mémoire système.
- Lacunes d'intégration :
  - Ajouter un scénario LM Studio en direct ou soutenu par des fixtures couvrant la configuration, la découverte du catalogue,
    le repli de préchargement, un tour d'agent, et l'utilisation d'intégration mémoire.

## Score de qualité

- Score : `Beta (78%)`
- Rapports Gitcrawl :
  - La requête `LM Studio local provider` a retourné le problème #80495 pour l'expansion des variables d'environnement et l'inadéquation des points de terminaison API, la PR #77053 pour le TTL d'inactivité opt-in via l'API de chargement natif, le problème #87616 pour les délais d'expiration rapides des requêtes LLM, et la PR #75198 pour les alias qualifiés par fournisseur.
  - La requête `LM Studio timeout local provider` a retourné le problème #87616 pour le comportement du délai d'expiration de LM Studio.
- Rapports Discrawl :
  - La requête `LM Studio local provider` a retourné une discussion de mainteneur selon laquelle les appels de modèles locaux à LM Studio/Ollama/vLLM/llama-server ont été refusés par la garde SSRF jusqu'à ce qu'une confiance d'origine exacte étroite soit ajoutée.
  - La requête `LM Studio timeout local provider` a retourné des preuves communautaires répétées autour de la confusion des délais d'expiration/pression des ressources de LM Studio, y compris les défaillances des garde-fous de chargement de modèles.
- Bonnes qualités :
  - Le plugin normalise les URL LM Studio copiées par l'utilisateur, supporte l'authentification locale synthétique, précharge les modèles le cas échéant, et dégénère les défaillances de préchargement sans bloquer le flux sous-jacent.
  - La documentation distingue maintenant les serveurs locaux non authentifiés, les serveurs avec authentification activée, les hôtes LAN/tailnet, le chargement JIT, et la récupération d'utilisation en streaming.
- Mauvaises qualités :
  - L'état externe de LM Studio reste à variance élevée ; les modèles non chargés, la mémoire insuffisante, et l'inadéquation des points de terminaison/authentification produisent une confusion utilisateur.
  - Le fournisseur natif est toujours une intégration d'exécution locale plutôt qu'un service entièrement contrôlé, donc la clarté de l'opérateur compte plus que d'habitude.
- Exclus de la qualité :
  - La couverture des tests, la profondeur d'intégration, et l'absence de tests n'ont pas été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/local-model-providers-ollama-vllm-sglang-lm-studio.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration LM Studio, la découverte de modèles et l'authentification, le préchargement de modèles et le chargement JIT, la compatibilité du streaming, les intégrations mémoire LM Studio.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La vérification en direct pour LM Studio devrait couvrir à la fois les serveurs locaux authentifiés et non authentifiés.
- La documentation de l'opérateur pourrait mieux connecter les défaillances de préchargement/JIT de LM Studio à des conseils d'action sur la mémoire et la taille du modèle.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/providers/lmstudio.md:11` démarre le démarrage rapide LM Studio ; les lignes 33-41 documentent l'authentification optionnelle.
- `/Users/kevinlin/code/openclaw/docs/providers/lmstudio.md:61` documente l'intégration non-interactive ; les lignes 84-94 expliquent les ID de modèles et les écritures de profil.
- `/Users/kevinlin/code/openclaw/docs/providers/lmstudio.md:101` documente la compatibilité d'utilisation en streaming.
- `/Users/kevinlin/code/openclaw/docs/providers/lmstudio.md:180` documente le chargement JIT et la désactivation du préchargement OpenClaw.
- `/Users/kevinlin/code/openclaw/docs/providers/lmstudio.md:199` documente les hôtes LM Studio LAN/tailnet et la confiance d'origine exacte.

### Source

- `/Users/kevinlin/code/openclaw/extensions/lmstudio/openclaw.plugin.json:25`
  déclare `lmstudio-local` comme marqueur d'authentification non-secret.
- `/Users/kevinlin/code/openclaw/extensions/lmstudio/index.ts:92` synthétise
  l'authentification locale si nécessaire.
- `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/models.ts:293`
  résout les URL de base du serveur LM Studio et normalise `/v1`/`/api/v1`.
- `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/models.fetch.ts:183`
  assure qu'un modèle est chargé avant l'inférence.
- `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/embedding-provider.ts:67`
  crée le fournisseur d'intégration mémoire LM Studio et précharge le modèle d'intégration.

### Tests d'intégration

- Aucun fichier de test LM Studio en direct dédié n'a été trouvé dans cet audit.
- `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/stream.test.ts:179`
  exerce le préchargement avant l'inférence par rapport à un exécution simulée.
- `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/setup.test.ts:1454`
  couvre les chemins de configuration du fournisseur découvert.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/lmstudio/index.test.ts:36` vérifie
  la canonicalisation des URL.
- `/Users/kevinlin/code/openclaw/extensions/lmstudio/index.test.ts:54`
  vérifie l'authentification synthétique d'espace réservé pour les modèles locaux configurés.
- `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/models.test.ts:256`
  vérifie la découverte de modèles LM Studio et le mappage des métadonnées.
- `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/stream.test.ts:498`
  vérifie que la compatibilité d'utilisation en streaming est forcée avant le flux sous-jacent.
- `/Users/kevinlin/code/openclaw/extensions/lmstudio/src/setup.test.ts:800`
  vérifie l'acceptation de clé API vide pour LM Studio local non authentifié.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "LM Studio local provider" --json --limit 5`

Résultats :

- A retourné le problème #80495 sur l'inadéquation des points de terminaison/authentification du fournisseur LM Studio, la PR #77053 pour le TTL d'inactivité de l'API de chargement natif, le problème #87616 sur le comportement du délai d'expiration local rapide, et la PR #75198 autour des alias qualifiés par fournisseur.

Requête : `gitcrawl search openclaw/openclaw --query "LM Studio timeout local provider" --json --limit 5`

Résultats :

- A retourné le problème #87616, signalant un délai d'expiration rapide lors du routage vers LM Studio local, plus une PR client d'application serveur isolée par session touchant les attentes du fournisseur LM Studio.

### Requêtes Discrawl

Requête : `discrawl search --mode hybrid --limit 5 "LM Studio local provider"`

Résultats :

- A retourné une discussion de mainteneur pour la PR de brouillon #80751 sur la garde SSRF bloquant les appels de modèles localhost à LM Studio, Ollama, vLLM, ou llama-server et le besoin de confiance du fournisseur local d'origine exacte.

Requête : `discrawl search --mode hybrid --limit 5 "LM Studio timeout local provider"`

Résultats :

- A retourné des rapports communautaires et de mainteneur selon lesquels la douleur locale/auto-hébergée se regroupe autour de la fiabilité des appels d'outils, des délais d'expiration, des points de terminaison LAN privés, et des défaillances des garde-fous de ressources de chargement de modèles LM Studio.
