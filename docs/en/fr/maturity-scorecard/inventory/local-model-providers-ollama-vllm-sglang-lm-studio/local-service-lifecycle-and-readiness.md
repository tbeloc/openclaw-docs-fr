---
title: "Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Cycle de vie du service local et note de maturité de disponibilité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Cycle de vie du service local et note de maturité de disponibilité

## Résumé

OpenClaw dispose d'une couche de cycle de vie de service local réelle pour les processus de modèles locaux soutenus par des fournisseurs : la configuration du fournisseur peut déclarer un `localService`, le transport de requête acquiert le service avant d'envoyer du trafic, et le code de service gère les sondes de santé, la sérialisation du démarrage, l'arrêt inactif et le redémarrage des processus défaillants. La couverture est la plus forte pour le gestionnaire de cycle de vie lui-même et plus faible pour les services en direct spécifiques aux fournisseurs tels que Ollama, vLLM, SGLang ou LM Studio exercés de bout en bout à partir d'une installation d'opérateur vierge.

## Portée de la catégorie

Cette catégorie couvre le contrat de configuration `localService`, le démarrage du processus, les sondes de disponibilité, le comportement de location/libération lors des requêtes du fournisseur, l'arrêt inactif, les vérifications de santé et la transmission des métadonnées du modèle du fournisseur sélectionné à l'orchestration du service local au niveau du transport.

## Fonctionnalités

- Configuration localService : Couvre la configuration localService dans le contrat de configuration `localService`, le démarrage du processus, les sondes de disponibilité, le comportement de location/libération lors des requêtes du fournisseur et le comportement de cycle de vie et de disponibilité du service local associé.
- Démarrage du processus et disponibilité : Couvre le démarrage du processus et la disponibilité dans le contrat de configuration `localService`, le démarrage du processus, les sondes de disponibilité, le comportement de location/libération lors des requêtes du fournisseur et le comportement de cycle de vie et de disponibilité du service local associé.
- Locations de requêtes et arrêt inactif : Couvre les locations de requêtes et l'arrêt inactif dans le contrat de configuration `localService`, le démarrage du processus, les sondes de disponibilité, le comportement de location/libération lors des requêtes du fournisseur et le comportement de cycle de vie et de disponibilité du service local associé.
- Vérifications de santé et redémarrage : Couvre les vérifications de santé et le redémarrage dans le contrat de configuration `localService`, le démarrage du processus, les sondes de disponibilité, le comportement de location/libération lors des requêtes du fournisseur et le comportement de cycle de vie et de disponibilité du service local associé.
- Recettes de fournisseur : Couvre les recettes de fournisseur dans le contrat de configuration `localService`, le démarrage du processus, les sondes de disponibilité, le comportement de location/libération lors des requêtes du fournisseur et le comportement de cycle de vie et de disponibilité du service local associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs :
  - `/Users/kevinlin/code/openclaw/docs/gateway/local-model-services.md:10`
    documente `localService` comme gestionnaire de processus fournisseur optionnel, et
    les lignes 18-27 expliquent le comportement de démarrage à froid, de location, de vérification de santé et d'arrêt inactif.
  - `/Users/kevinlin/code/openclaw/docs/gateway/local-model-services.md:32`
    jusqu'à la ligne 67 donne un exemple de configuration de fournisseur fonctionnant, et les lignes 69-82
    définissent les champs pris en charge.
  - `/Users/kevinlin/code/openclaw/src/agents/provider-local-service.ts:57`
    jusqu'à la ligne 132 implémentent le registre de service et le modèle de location ; les lignes
    199-280 implémentent le démarrage, l'attente de disponibilité et la gestion des défaillances.
  - `/Users/kevinlin/code/openclaw/src/agents/provider-transport-fetch.ts:522`
    jusqu'à la ligne 657 attachent l'acquisition et la libération du service local au
    chemin de récupération du fournisseur gardé.
- Signaux négatifs :
  - La couche de cycle de vie est générique et bien testée, mais les preuves d'archive et de source
    n'ont pas montré une exécution en direct récente qui démarre un vrai service Ollama, vLLM,
    SGLang ou LM Studio et prouve ensuite une requête d'agent.
  - La documentation est orientée vers les auteurs de configuration avancée ; les pages spécifiques aux fournisseurs
    ne routent pas systématiquement les utilisateurs de la configuration du fournisseur local vers
    l'automatisation `localService`.
- Lacunes d'intégration :
  - Ajouter un test de fumée d'intégration utilisant un petit fixture HTTP local qui démarre
    via `localService`, sert les points de terminaison `/v1/models` et de complétion de chat,
    et prouve un tour de passerelle plus l'arrêt inactif.

## Score de qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl :
  - La requête `localService local model server` n'a retourné aucun résultat direct, ce qui
    suggère que peu de problèmes publics nomment directement l'abstraction du cycle de vie.
- Rapports Discrawl :
  - La requête `localService local model server` n'a retourné aucun résultat direct.
- Bonnes qualités :
  - L'implémentation valide la forme de la commande, prend en charge les en-têtes de santé,
    sérialise les démarrages à froid, libère les locations après la fin de la requête et
    redémarre les services qui deviennent défaillants.
  - Le routage des requêtes maintient l'abstraction du service proche du transport du fournisseur
    plutôt que d'exiger que chaque appelant gère la disponibilité du processus.
- Mauvaises qualités :
  - Les commentaires des opérateurs sont toujours indirects : les utilisateurs diagnostiquent généralement le serveur du fournisseur,
    la configuration et la route de passerelle séparément au lieu de voir un état de disponibilité unifié.
  - L'abstraction est documentée comme une machinerie de configuration, pas comme une
    expérience de configuration de modèle local guidée de première classe.
- Exclus de la qualité :
  - La couverture des tests, la profondeur d'intégration et l'absence de tests de service de fournisseur en direct
    n'ont pas été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/local-model-providers-ollama-vllm-sglang-lm-studio.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration localService, le démarrage du processus et la disponibilité, les locations de requêtes et l'arrêt inactif, les vérifications de santé et le redémarrage, les recettes de fournisseur.
- Signaux négatifs : la note archivée a précédé la notation de complétude du processus-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucune recette de service local spécifique au fournisseur n'a été trouvée pour Ollama, LM Studio,
  vLLM ou SGLang qui inclut une commande exécutable, une URL de santé et une sélection de modèle dans un seul chemin.
- Aucun signal d'archive ne montre les utilisateurs parlant de `localService` par nom, ce qui peut
  signifier soit que l'abstraction est bien cachée, soit pas assez découvrable pour
  déboguer quand le démarrage du processus local échoue.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/gateway/local-model-services.md:10`
  introduit les services locaux gérés par le fournisseur.
- `/Users/kevinlin/code/openclaw/docs/gateway/local-model-services.md:32`
  fournit un exemple de configuration `localService` complet.
- `/Users/kevinlin/code/openclaw/docs/gateway/local-model-services.md:183`
  énumère les notes opérationnelles pour la journalisation, les vérifications de santé et le délai d'inactivité.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-agents.md:461` inclut
  `localService` dans les champs de configuration du modèle du fournisseur.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/provider-local-service.ts:57`
  implémente l'acquisition du service local et le suivi d'état.
- `/Users/kevinlin/code/openclaw/src/agents/provider-local-service.ts:141`
  valide les commandes de service et les chemins de commande absolus.
- `/Users/kevinlin/code/openclaw/src/agents/provider-local-service.ts:199`
  sonde l'URL de santé du service.
- `/Users/kevinlin/code/openclaw/src/agents/provider-transport-fetch.ts:522`
  câble l'acquisition du service local dans les requêtes du fournisseur.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/model.ts:695`
  attache les métadonnées du service local à la configuration du modèle résolu.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/provider-transport-stream.test.ts:115`
  vérifie que les API non prises en charge échouent fermées quand un service local est attaché.
- `/Users/kevinlin/code/openclaw/src/agents/provider-transport-stream.test.ts:179`
  vérifie que les modèles de service local routent via le transport de complétion simple.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/provider-local-service.test.ts:75`
  couvre le démarrage et l'arrêt inactif.
- `/Users/kevinlin/code/openclaw/src/agents/provider-local-service.test.ts:107`
  couvre les en-têtes de santé.
- `/Users/kevinlin/code/openclaw/src/agents/provider-local-service.test.ts:148`
  couvre les démarrages à froid sérialisés.
- `/Users/kevinlin/code/openclaw/src/agents/provider-local-service.test.ts:193`
  couvre la gestion distincte de l'environnement.
- `/Users/kevinlin/code/openclaw/src/agents/provider-local-service.test.ts:257`
  couvre le redémarrage après un état défaillant.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "localService local model server" --json --limit 5`

Résultats :

- Aucun résultat direct retourné.

### Requêtes Discrawl

Requête : `discrawl search --mode hybrid --limit 5 "localService local model server"`

Résultats :

- Aucun résultat direct retourné.
