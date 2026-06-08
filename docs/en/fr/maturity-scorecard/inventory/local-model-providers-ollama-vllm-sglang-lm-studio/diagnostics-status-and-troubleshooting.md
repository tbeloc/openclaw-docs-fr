---
title: "Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Note de maturité des diagnostics et dépannage"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Note de maturité des diagnostics et dépannage

## Résumé

Les diagnostics des modèles locaux sont utiles mais restent dispersés dans la documentation des fournisseurs, le dépannage des passerelles, les vérifications du médecin mémoire, les sondes curl directes et l'extraction des erreurs d'exécution. Le code dispose d'erreurs HTTP structurées des fournisseurs et d'une classification des modèles non trouvés, et la documentation couvre les signatures communes des backends locaux. La principale faiblesse est l'absence d'une surface d'état consolidée unique qui explique le fournisseur configuré, le point de terminaison accessible, le modèle sélectionné, le fournisseur d'intégration mémoire et la disponibilité des tours d'agent ensemble.

## Portée de la catégorie

Cette catégorie couvre les commandes de diagnostic visibles par l'utilisateur, la normalisation des erreurs HTTP des fournisseurs, la classification des modèles non trouvés, les sondes directes des backends locaux, les vérifications de disponibilité de la recherche mémoire, les pages de dépannage spécifiques aux fournisseurs et les preuves d'archive pour les défaillances de LM Studio, Ollama, vLLM, SGLang et des fournisseurs génériques compatibles OpenAI locaux.

## Fonctionnalités

- État du fournisseur local : Couvre l'état du fournisseur local dans les commandes de diagnostic visibles par l'utilisateur, la normalisation des erreurs HTTP des fournisseurs, la classification des modèles non trouvés, les sondes directes des backends locaux et le comportement de diagnostic et dépannage associé.
- Sondes de disponibilité du backend : Couvre les sondes de disponibilité du backend dans les commandes de diagnostic visibles par l'utilisateur, la normalisation des erreurs HTTP des fournisseurs, la classification des modèles non trouvés, les sondes directes des backends locaux et le comportement de diagnostic et dépannage associé.
- Erreurs de disponibilité des modèles : Couvre les erreurs de disponibilité des modèles dans les commandes de diagnostic visibles par l'utilisateur, la normalisation des erreurs HTTP des fournisseurs, la classification des modèles non trouvés, les sondes directes des backends locaux et le comportement de diagnostic et dépannage associé.
- Diagnostics de disponibilité mémoire : Couvre les diagnostics de disponibilité mémoire dans les commandes de diagnostic visibles par l'utilisateur, la normalisation des erreurs HTTP des fournisseurs, la classification des modèles non trouvés, les sondes directes des backends locaux et le comportement de diagnostic et dépannage associé.
- Documentation de dépannage des fournisseurs : Couvre la documentation de dépannage des fournisseurs dans les commandes de diagnostic visibles par l'utilisateur, la normalisation des erreurs HTTP des fournisseurs, la classification des modèles non trouvés, les sondes directes des backends locaux et le comportement de diagnostic et dépannage associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs :
  - `/Users/kevinlin/code/openclaw/docs/gateway/troubleshooting.md:236`
    jusqu'à la ligne 278 documentent les sondes directes des backends locaux et les signatures/corrections communes.
  - `/Users/kevinlin/code/openclaw/docs/gateway/local-models.md:324` jusqu'à
    la ligne 350 documentent le dépannage des modèles locaux et les vérifications de sécurité.
  - `/Users/kevinlin/code/openclaw/src/agents/provider-http-errors.ts:141`
    jusqu'à la ligne 240 extraient les détails des erreurs des fournisseurs pour les défaillances visibles par l'utilisateur.
  - `/Users/kevinlin/code/openclaw/src/agents/live-model-errors.ts:1` jusqu'à
    la ligne 45 classifient les erreurs de modèle non trouvé.
  - `/Users/kevinlin/code/openclaw/docs/gateway/doctor.md:512` jusqu'à la ligne
    523 documentent les vérifications de disponibilité de la recherche mémoire, y compris les défaillances des fournisseurs.
- Signaux négatifs :
  - Les diagnostics sont solides en tant que pièces individuelles mais divisés par les couches de fournisseur, mémoire, passerelle et transport.
  - Les preuves d'archive incluent des questions répétées sur les délais d'expiration des backends locaux, l'URL de base Docker et la disponibilité des modèles, ce qui indique que le chemin de diagnostic actuel nécessite toujours une interprétation du support.
- Lacunes d'intégration :
  - Ajouter un `openclaw doctor local-models` ou équivalent qui rapporte le fournisseur configuré, l'URL de base, la liste des modèles, le modèle sélectionné, la disponibilité des intégrations et une sonde de chat minimale en une seule sortie.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl :
  - La requête `LM Studio timeout local provider` a retourné le problème #87616 et la PR #81777, montrant la pression UX des délais d'expiration et des fournisseurs locaux.
  - La requête `Ollama cron local unreachable` a retourné le problème #79329, la PR #82887, le problème #86044 et la PR #62682, montrant une pression récurrente sur les points de terminaison locaux et la disponibilité d'exécution.
- Rapports Discrawl :
  - La requête `LM Studio timeout local provider` a retourné des résumés de tendances d'aide, des corrections de délai d'expiration LM Studio et des défaillances répétées de chargement de modèles locaux/garde-fous de ressources.
  - La requête `Ollama cron local unreachable` a retourné des conseils de support vérifiant `ollama list`, l'URL de base Docker, le statut `/gateway/models` et les entrées d'exécution cron.
- Bonnes qualités :
  - La documentation fournit des sondes directes concrètes au lieu de conseils génériques, et l'extraction des erreurs d'exécution préserve les corps de réponse des fournisseurs et les détails de statut.
  - Les vérifications du médecin mémoire aident à détecter une incompatibilité courante des modèles locaux : le fournisseur de chat fonctionne tandis que les intégrations mémoire sont manquantes ou inaccessibles.
- Mauvaises qualités :
  - Les utilisateurs doivent toujours corréler plusieurs surfaces de diagnostic manuellement avant de savoir si le problème est la disponibilité du point de terminaison, la sélection du modèle, le comportement de l'analyseur du fournisseur, les intégrations mémoire ou la pression des ressources.
  - Les pages de dépannage spécifiques aux fournisseurs sont inégales en profondeur.
- Exclus de la qualité :
  - La couverture des tests et la profondeur des tests de diagnostic n'ont pas été utilisées comme entrées de qualité.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/local-model-providers-ollama-vllm-sglang-lm-studio.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'état du fournisseur local, les sondes de disponibilité du backend, les erreurs de disponibilité des modèles, les diagnostics de disponibilité mémoire, la documentation de dépannage des fournisseurs.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Il n'y a pas de commande d'état unique dans l'ensemble de preuves qui prouve le chat local, l'intégration locale, la liste des modèles du fournisseur et un tour d'agent minimal ensemble.
- Les preuves d'archive suggèrent que les délais d'expiration et la disponibilité des points de terminaison locaux restent assez courants pour mériter un diagnostic guidé plus direct.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/gateway/troubleshooting.md:236`
  documente les sondes directes des backends locaux.
- `/Users/kevinlin/code/openclaw/docs/gateway/troubleshooting.md:253`
  documente les signatures et corrections communes des backends locaux.
- `/Users/kevinlin/code/openclaw/docs/gateway/local-models.md:324`
  documente le dépannage et la sécurité des modèles locaux.
- `/Users/kevinlin/code/openclaw/docs/providers/ollama.md:207` documente
  les vérifications de fumée d'exécution et d'image Ollama.
- `/Users/kevinlin/code/openclaw/docs/providers/lmstudio.md:180` documente
  le dépannage du chargement JIT et du préchargement de LM Studio.
- `/Users/kevinlin/code/openclaw/docs/gateway/doctor.md:512` documente les
  vérifications de disponibilité de la recherche mémoire.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/provider-http-errors.ts:141`
  extrait les métadonnées des erreurs du fournisseur.
- `/Users/kevinlin/code/openclaw/src/agents/provider-http-errors.ts:177`
  définit les détails de `ProviderHttpError`.
- `/Users/kevinlin/code/openclaw/src/agents/live-model-errors.ts:1`
  classifie les réponses de modèle non trouvé.
- `/Users/kevinlin/code/openclaw/extensions/ollama/src/discovery-shared.ts:225`
  retourne les résultats de découverte Ollama utilisés par les chemins de configuration/statut.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/commands/model-picker.test.ts:1068`
  exerce le comportement du flux de configuration pour vLLM.
- `/Users/kevinlin/code/openclaw/src/commands/model-picker.test.ts:1141`
  exerce le comportement de contribution du sélecteur de modèles du fournisseur.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/commands/doctor-memory-search.test.ts:611`
  couvre les vérifications de disponibilité de la recherche mémoire compatible OpenAI.
- `/Users/kevinlin/code/openclaw/src/commands/doctor-memory-search.test.ts:693`
  couvre le comportement de sonde ignorée.
- `/Users/kevinlin/code/openclaw/src/commands/doctor-memory-search.test.ts:709`
  couvre les diagnostics d'URL de base manquante.
- `/Users/kevinlin/code/openclaw/src/commands/doctor-memory-search.test.ts:727`
  couvre les diagnostics de modèle manquant.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "LM Studio timeout local provider" --json --limit 5`

Résultats :

- A retourné le problème #87616 et la PR #81777, incluant le délai d'expiration du fournisseur local et la pression des diagnostics.

Requête : `gitcrawl search openclaw/openclaw --query "Ollama cron local unreachable" --json --limit 5`

Résultats :

- A retourné le problème #79329, la PR #82887, le problème #86044 et la PR #62682, qui montrent des questions répétées de disponibilité locale et d'état d'exécution.

### Requêtes Discrawl

Requête : `discrawl search --mode hybrid --limit 5 "LM Studio timeout local provider"`

Résultats :

- A retourné des résumés de tendances d'aide et des discussions sur le chargement de modèles locaux/garde-fous de ressources impliquant LM Studio.

Requête : `discrawl search --mode hybrid --limit 5 "Ollama cron local unreachable"`

Résultats :

- A retourné des conseils de support vérifiant `ollama list`, l'URL de base Docker, `/gateway/models` et les entrées d'exécution cron.
