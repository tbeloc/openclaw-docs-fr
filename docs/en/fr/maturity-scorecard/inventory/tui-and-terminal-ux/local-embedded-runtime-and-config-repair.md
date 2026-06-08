---
title: "TUI - Local Embedded Runtime and Config Repair Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# TUI - Local Embedded Runtime and Config Repair Maturity Note

## Résumé

Le mode intégré local est l'ajout TUI le plus important côté utilisateur : il permet
à `openclaw chat` et `openclaw tui --local` de s'exécuter sans Gateway, de charger l'historique des sessions locales, d'envoyer des tours via le runtime de l'agent intégré, d'exécuter `/auth`, et de supporter une boucle de réparation de configuration documentée. La couverture inclut un test de fumée PTY en mode local avec un endpoint de modèle simulé. La qualité reste bêta car le mode local a toujours des lacunes documentées dans la surface des commandes et une confusion local-provider/operator dans l'archive.

## Portée de la catégorie

Cette catégorie couvre le cycle de vie du backend intégré, le chargement du catalogue de modèles locaux, la projection d'événements `chat.send` locaux, les exécutions locales en file d'attente, l'historique des sessions locales, `/auth` local, la documentation de réparation de configuration locale, et les scénarios de récupération sans Gateway.

## Fonctionnalités

- Chat local intégré : Couvre le chat local intégré sur l'ensemble du cycle de vie du backend intégré, du chargement du catalogue de modèles locaux, de la projection d'événements `chat.send` locaux, des exécutions locales en file d'attente, de l'historique des sessions locales, de `/auth` local, de la documentation de réparation de configuration locale, et des scénarios de récupération sans Gateway.
- Flux d'authentification local : Couvre le flux d'authentification local sur l'ensemble du cycle de vie du backend intégré, du chargement du catalogue de modèles locaux, de la projection d'événements `chat.send` locaux, des exécutions locales en file d'attente, de l'historique des sessions locales, de `/auth` local, de la documentation de réparation de configuration locale, et des scénarios de récupération sans Gateway.
- Boucle de réparation de configuration : Couvre la boucle de réparation de configuration sur l'ensemble du cycle de vie du backend intégré, du chargement du catalogue de modèles locaux, de la projection d'événements `chat.send` locaux, des exécutions locales en file d'attente, de l'historique des sessions locales, de `/auth` local, de la documentation de réparation de configuration locale, et des scénarios de récupération sans Gateway.
- Récupération sans Gateway : Couvre la récupération sans Gateway sur l'ensemble du cycle de vie du backend intégré, du chargement du catalogue de modèles locaux, de la projection d'événements `chat.send` locaux, des exécutions locales en file d'attente, de l'historique des sessions locales, de `/auth` local, de la documentation de réparation de configuration locale, et des scénarios de récupération sans Gateway.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (80%)`
- Signaux positifs : le mode intégré local a de la documentation, l'enregistrement des commandes, les tests du backend intégré, et un e2e PTY qui envoie un vrai tour en mode local à un endpoint de modèle simulé.
- Signaux négatifs : l'e2e PTY ne couvre pas `/auth`, la réparation de configuration du shell local, plusieurs vrais fournisseurs locaux, ou la récupération hatch en cas de Gateway défaillant.
- Lacunes d'intégration : ajouter un scénario de réparation de configuration locale qui exécute `/auth`, `!openclaw config validate`, et une réponse de modèle via le même harnais PTY.

## Score de qualité

- Score : `Bêta (74%)`
- Rapports Gitcrawl : `gitcrawl search issues "tui commands" -R openclaw/openclaw --state all --json number,title,url,state --limit 10` a retourné `#71592` pour la publicité du mode local `/status` et `/compact` tout en basculant vers le texte du modèle. `gitcrawl search issues "TUI local shell" ...` a retourné `#86632` pour une session Ollama/Qwen intégrée locale échouant une demande de données en direct gérée par un autre chemin de shell d'agent de codage.
- Rapports Discrawl : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "local embedded tui auth config repair"` a retourné une discussion de PR `#66767` et PR `#69995`, plus le travail de polissage de suivi restant pour la récupération setup/hatch.
- Bonnes qualités : le mode intégré supprime la pollution de la console runtime, projette les événements de l'agent dans les événements de chat TUI, met en file d'attente les envois locaux de même session, résout l'historique local à partir des magasins de session, et a un chemin `/auth` local.
- Mauvaises qualités : la capacité de commande locale n'est pas encore entièrement alignée avec les commandes slash documentées, et la discussion d'archive montre que les expériences de modèle/fournisseur local peuvent toujours échouer de manière confuse.
- Exclu de la qualité : profondeur des tests unitaires, d'intégration, e2e, en direct et de flux runtime.

## Score de complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/tui-and-terminal-ux.md`.
- Signaux positifs : la documentation archivée, la source, les tests, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour le chat local intégré, le flux d'authentification local, la boucle de réparation de configuration, la récupération sans Gateway.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La sémantique des commandes locales uniquement doit être mieux alignée avec la documentation et le texte d'aide.
- La réparation de configuration est documentée, mais la boucle de réparation complète a une preuve exécutable plus mince que le simple chat local.

## Preuves

### Documentation

- `docs/web/tui.md:35` documente le mode local avec `openclaw chat` et `openclaw tui --local`.
- `docs/web/tui.md:144` documente un flux de réparation de configuration TUI local.
- `docs/cli/tui.md:60` documente la même boucle de réparation de configuration dans la référence CLI.
- `docs/cli/tui.md:44` documente `/auth` local uniquement.

### Source

- `src/tui/embedded-backend.ts:253` implémente `EmbeddedTuiBackend`.
- `src/tui/embedded-backend.ts:270` démarre le mode intégré, réchauffe le contexte, supprime les journaux runtime, et s'abonne aux événements de l'agent.
- `src/tui/embedded-backend.ts:325` envoie les tours de chat locaux, supporte les commandes d'arrêt, et met en file d'attente les exécutions de même session.
- `src/tui/embedded-backend.ts:382` charge l'historique des sessions locales et limite les octets d'historique d'affichage.
- `src/tui/tui-command-handlers.ts:308` implémente `/auth` local et le rejette en dehors du mode local.

### Tests d'intégration

- `src/tui/tui-pty-local.e2e.test.ts:249` pilote `tui --local` via un endpoint de modèle simulé et attend la sortie du terminal.
- `src/tui/tui-pty-harness.e2e.test.ts:397` vérifie que les réponses de source UI interne message-tool-only sont visibles dans la boucle du terminal.

### Tests unitaires

- `src/tui/embedded-backend.test.ts:748` couvre l'arrêt des exécutions locales pendant que la maintenance post-tour est en attente.
- `src/tui/embedded-backend.test.ts:861` couvre les envois de même session en file d'attente derrière les exécutions locales du terminal.
- `src/tui/tui-command-handlers.test.ts:643` exécute `/auth` via le flux d'authentification local et actualise les informations de session.
- `src/tui/tui-event-handlers.test.ts:1026` affiche des indices `/auth` concis pour les échecs d'authentification locaux.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues "tui commands" -R openclaw/openclaw --state all --json number,title,url,state --limit 10`

Résultats :

- A retourné `#71592`, `#78347`, et d'autres lacunes de surface de commande ; `#71592` affecte directement le comportement des commandes en mode local.

Requête :

`gitcrawl search issues "TUI local shell" -R openclaw/openclaw --state all --json number,title,url,state --limit 8`

Résultats :

- A retourné `#86632` concernant l'échec de données en direct Ollama/Qwen intégré local et d'autres problèmes de mode terminal TUI.

### Requêtes Discrawl

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "local embedded tui auth config repair"`

Résultats :

- A retourné une discussion des mainteneurs selon laquelle le TUI local sans Gateway et la documentation de réparation de configuration ont été intégrés, avec le travail de suivi setup/hatch toujours visible.
