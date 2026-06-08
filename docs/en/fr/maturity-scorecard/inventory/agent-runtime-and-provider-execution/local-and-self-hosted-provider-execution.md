---
title: "Agent Runtime - Local and Self-hosted Providers Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Agent Runtime - Local and Self-hosted Providers Maturity Note

## Résumé

L'exécution des fournisseurs locaux et auto-hébergés est documentée et implémentée, avec notamment des conseils détaillés sur Ollama pour l'API native `/api/chat`, l'API compatible OpenAI `/v1`, les marqueurs locaux, le format du profil d'authentification, les drapeaux de support des outils, les profils allégés, les fenêtres de contexte, les délais d'expiration et les commandes de vérification en direct. La couverture est Beta car elle est concentrée dans la documentation Ollama/modèles locaux et le comportement des commandes. La qualité est Alpha car les preuves d'archive montrent que les modèles locaux ont toujours du mal avec l'appel d'outils, les délais d'expiration au démarrage à froid, le JSON brut/texte d'outils et le blocage de la boucle d'événements.

## Portée de la catégorie

Cette catégorie couvre les chemins d'exécution locaux et auto-hébergés visibles aux utilisateurs/opérateurs : Ollama, serveurs locaux compatibles OpenAI, configuration des profils de modèles locaux, drapeaux de capacité des outils, délais d'expiration, fenêtres de contexte, vérifications de fumée des images/modèles locaux et gestion des défaillances des fournisseurs locaux.

## Fonctionnalités

- Profils de fournisseurs locaux : Configuration des profils de modèles locaux pour Ollama et serveurs locaux compatibles OpenAI.
- Drapeaux de capacité des outils : Drapeaux de capacité des fournisseurs locaux et comportement pour l'utilisation des outils.
- Délais d'expiration et fenêtres de contexte : Configuration des délais d'expiration et des fenêtres de contexte des fournisseurs locaux.
- Vérifications de fumée locales : Vérifications de fumée des images et modèles locaux visibles aux opérateurs.
- Gestion des défaillances locales : Gestion des défaillances visibles aux opérateurs pour les fournisseurs locaux et auto-hébergés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (70%)`

La couverture est utile et visible aux opérateurs, mais elle est inégale entre les backends locaux et moins uniformément testée que les fournisseurs hébergés.

## Score de qualité

- Score : `Alpha (60%)`

L'exécution locale est fonctionnelle mais toujours fragile en pratique : la qualité de l'appel d'outils des modèles, les démarrages à froid, les limites de contexte, le blocage du serveur local et les particularités du mode compatible OpenAI restent des problèmes récurrents.

## Score de complétude

- Score : `Beta (70%)`
- Instructions de surface : évaluées par rapport à `references/completeness/agent-runtime-and-provider-execution.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les profils de fournisseurs locaux, les drapeaux de capacité des outils, les délais d'expiration et fenêtres de contexte, les vérifications de fumée locales, la gestion des défaillances locales.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles aux opérateurs.

## Lacunes connues

- Les preuves des fournisseurs locaux sont fortement centrées sur Ollama ; les autres runtimes locaux/auto-hébergés ont besoin du même niveau de preuve de scénario.
- Le comportement de l'appel d'outils dépend fortement de la capacité du modèle et du mode du fournisseur.
- Des conseils sur les délais d'expiration existent, mais les valeurs par défaut des opérateurs produisent toujours des rapports pour les LLM locaux lents.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/ollama.md` documente l'API native `/api/chat`, les avertissements `/v1`, le comportement brut des outils JSON, les règles d'authentification locales, les ID de fournisseurs, `models list`, le comportement exact des défaillances `/model ollama`, la vérification préalable des points de terminaison, la commande de test en direct, les URL de base personnalisées, `compat.supportsTools: false`, `localModelLean`, `timeoutSeconds`, les avertissements de fiabilité des outils/streaming/pensée du mode compatible OpenAI, les fenêtres de contexte, le support du streaming/appel d'outils/pensée, la gestion des sorties brouillées et les délais d'expiration des modèles locaux au démarrage à froid.
- `/Users/kevinlin/code/openclaw/docs/concepts/models.md` documente les références locales/GGUF, les listes blanches de modèles et les références de modèles indépendantes du runtime.
- `/Users/kevinlin/code/openclaw/docs/cli/agent.md` documente `--local`, les options de délai d'expiration et le comportement de secours intégré pour les exécutions d'agents locaux.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/agent-tools.ts` applique la politique des outils du fournisseur de modèles et supprime les outils tels que la recherche web pour les profils allégés locaux.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/model-selection.ts` résout les listes blanches de modèles, les références locales, les paramètres de pensée/raisonnement et les limites de jetons de contexte utilisées par les fournisseurs locaux.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.ts` gère les indices de fenêtre de contexte, le comportement de secours du runtime local/intégré, la copie du délai d'expiration du fournisseur et les interactions de secours/nouvelle tentative du modèle local.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/commands/models.list.e2e.test.ts` couvre le comportement local/fournisseur dans la sortie du catalogue/statut des modèles.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.test.ts` couvre les planchers de jetons de réserve conscients du contexte, le texte de récupération de débordement, les interactions de secours local/runtime, la copie de capacité du modèle et les diagnostics de délai d'expiration/secours pertinents pour les fournisseurs locaux.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/agent-tools.message-provider-policy.test.ts` couvre le comportement de la politique des outils basée sur le fournisseur.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.test.ts` inclut une couverture de style unitaire pour les fenêtres de contexte, l'état de secours du fournisseur et la copie de délai d'expiration/défaillance.

### Requêtes Gitcrawl

- `gitcrawl --json search issues -R openclaw/openclaw "Ollama vLLM SGLang LM Studio tool calling"` n'a retourné aucune correspondance pour l'ensemble exact des backends.
- `gitcrawl --json search issues -R openclaw/openclaw "local model provider context timeout Ollama"` a retourné #87642 sur l'exposition du délai d'expiration `waitForRun` pour les LLM locaux lents, #86599 sur les appels du fournisseur de modèles locaux bloquant la boucle d'événements de la passerelle sur Windows, #74204 sur le délai d'expiration de l'intégration de mémoire pour GGUF local, #81214 sur la régression du sous-agent et #65502 sur le secours de modèle résilient avec nouvelle tentative et mode sûr.
- `gitcrawl --json search prs -R openclaw/openclaw "Ollama native tool calling streaming"` n'a retourné aucune RP correspondante.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "Ollama tool calling OpenClaw"` a retourné des conseils selon lesquels certains modèles locaux sont mauvais pour l'appel d'outils, des questions des utilisateurs sur les limitations des modèles locaux et l'utilisation des outils, des conseils des mainteneurs selon lesquels les outils bruts imprimés en tant que texte indiquent des problèmes de compatibilité des modèles/appel d'outils et des commentaires fermant les problèmes autour du support des backends locaux et de la mauvaise configuration Ollama `/v1`.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "models list provider routing fallback"` a retourné des conseils d'utilisateur à utilisateur sur le fournisseur Ollama par rapport à la pression de session/outils et la gestion des fournisseurs locaux/personnalisés.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "usage limit fallback openai-codex"` incluait des discussions d'opérateurs adjacentes sur la configuration de secours, utiles comme contraste mais pas comme preuves principales des fournisseurs locaux.
