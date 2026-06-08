---
title: "TUI - Note de Maturité des Modes d'Exécution"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# TUI - Note de Maturité des Modes d'Exécution

## Résumé

Le TUI est une commande CLI de première classe avec le mode Gateway, le mode embarqué local et les alias `chat` / `terminal`. La documentation et l'enregistrement des commandes sont clairs, et il existe des preuves unitaires et PTY ciblées pour le comportement de lancement local. Le principal risque produit reste le polissage du contexte de lancement : les relancés hatch/setup, la sélection de port Gateway obsolète et le démarrage lent du mode terminal ont des signaux d'archive actifs.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Lancement TUI Gateway : Couvre le lancement TUI Gateway sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation des options local-vs-Gateway, relancement depuis les chemins setup/hatch, drapeaux de message initial et de délai d'attente, et documentation de lancement.
- Lancement chat local : Couvre le lancement chat local sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation des options local-vs-Gateway, relancement depuis les chemins setup/hatch, drapeaux de message initial et de délai d'attente, et documentation de lancement.
- Lancement alias Terminal : Couvre le lancement alias Terminal sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation des options local-vs-Gateway, relancement depuis les chemins setup/hatch, drapeaux de message initial et de délai d'attente, et documentation de lancement.
- Lancement message initial : Couvre le lancement message initial sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation des options local-vs-Gateway, relancement depuis les chemins setup/hatch, drapeaux de message initial et de délai d'attente, et documentation de lancement.
- Validation des options de lancement : Couvre la validation des options de lancement sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation des options local-vs-Gateway, relancement depuis les chemins setup/hatch, drapeaux de message initial et de délai d'attente, et documentation de lancement.
- Connexion Gateway : Couvre la connexion Gateway sur la résolution de connexion Gateway, l'authentification token/password/SecretRef pour TUI, les exigences d'authentification `--url`, l'enregistrement du mode client/capacité, et le comportement de transport, d'authentification et d'historique de gateway associé.
- Authentification Gateway : Couvre l'authentification Gateway sur la résolution de connexion Gateway, l'authentification token/password/SecretRef pour TUI, les exigences d'authentification `--url`, l'enregistrement du mode client/capacité, et le comportement de transport, d'authentification et d'historique de gateway associé.
- Chargement de l'historique à l'attachement : Couvre le chargement de l'historique à l'attachement sur la résolution de connexion Gateway, l'authentification token/password/SecretRef pour TUI, les exigences d'authentification `--url`, l'enregistrement du mode client/capacité, et le comportement de transport, d'authentification et d'historique de gateway associé.
- Visibilité de la reconnexion : Couvre la visibilité de la reconnexion sur la résolution de connexion Gateway, l'authentification token/password/SecretRef pour TUI, les exigences d'authentification `--url`, l'enregistrement du mode client/capacité, et le comportement de transport, d'authentification et d'historique de gateway associé.
- RPC de commande Gateway : Couvre les RPC de commande Gateway sur la résolution de connexion Gateway, l'authentification token/password/SecretRef pour TUI, les exigences d'authentification `--url`, l'enregistrement du mode client/capacité, et le comportement de transport, d'authentification et d'historique de gateway associé.
- Chat local embarqué : Couvre le chat local embarqué sur le cycle de vie du backend embarqué, le chargement du catalogue de modèles local, la projection d'événement `chat.send` local, les exécutions locales en file d'attente, l'historique de session local, `/auth` local, la documentation de réparation de configuration locale, et les scénarios de récupération sans Gateway.
- Flux d'authentification local : Couvre le flux d'authentification local sur le cycle de vie du backend embarqué, le chargement du catalogue de modèles local, la projection d'événement `chat.send` local, les exécutions locales en file d'attente, l'historique de session local, `/auth` local, la documentation de réparation de configuration locale, et les scénarios de récupération sans Gateway.
- Boucle de réparation de configuration : Couvre la boucle de réparation de configuration sur le cycle de vie du backend embarqué, le chargement du catalogue de modèles local, la projection d'événement `chat.send` local, les exécutions locales en file d'attente, l'historique de session local, `/auth` local, la documentation de réparation de configuration locale, et les scénarios de récupération sans Gateway.
- Récupération sans Gateway : Couvre la récupération sans Gateway sur le cycle de vie du backend embarqué, le chargement du catalogue de modèles local, la projection d'événement `chat.send` local, les exécutions locales en file d'attente, l'historique de session local, `/auth` local, la documentation de réparation de configuration locale, et les scénarios de récupération sans Gateway.

## Fonctionnalités

- Lancement TUI Gateway : Couvre le lancement TUI Gateway sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation des options local-vs-Gateway, relancement depuis les chemins setup/hatch, drapeaux de message initial et de délai d'attente, et documentation de lancement.
- Lancement chat local : Couvre le lancement chat local sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation des options local-vs-Gateway, relancement depuis les chemins setup/hatch, drapeaux de message initial et de délai d'attente, et documentation de lancement.
- Lancement alias Terminal : Couvre le lancement alias Terminal sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation des options local-vs-Gateway, relancement depuis les chemins setup/hatch, drapeaux de message initial et de délai d'attente, et documentation de lancement.
- Lancement message initial : Couvre le lancement message initial sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation des options local-vs-Gateway, relancement depuis les chemins setup/hatch, drapeaux de message initial et de délai d'attente, et documentation de lancement.
- Validation des options de lancement : Couvre la validation des options de lancement sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation des options local-vs-Gateway, relancement depuis les chemins setup/hatch, drapeaux de message initial et de délai d'attente, et documentation de lancement.
- Connexion Gateway : Couvre la connexion Gateway sur la résolution de connexion Gateway, l'authentification token/password/SecretRef pour TUI, les exigences d'authentification `--url`, l'enregistrement du mode client/capacité, et le comportement de transport, d'authentification et d'historique de gateway associé.
- Authentification Gateway : Couvre l'authentification Gateway sur la résolution de connexion Gateway, l'authentification token/password/SecretRef pour TUI, les exigences d'authentification `--url`, l'enregistrement du mode client/capacité, et le comportement de transport, d'authentification et d'historique de gateway associé.
- Chargement de l'historique à l'attachement : Couvre le chargement de l'historique à l'attachement sur la résolution de connexion Gateway, l'authentification token/password/SecretRef pour TUI, les exigences d'authentification `--url`, l'enregistrement du mode client/capacité, et le comportement de transport, d'authentification et d'historique de gateway associé.
- Visibilité de la reconnexion : Couvre la visibilité de la reconnexion sur la résolution de connexion Gateway, l'authentification token/password/SecretRef pour TUI, les exigences d'authentification `--url`, l'enregistrement du mode client/capacité, et le comportement de transport, d'authentification et d'historique de gateway associé.
- RPC de commande Gateway : Couvre les RPC de commande Gateway sur la résolution de connexion Gateway, l'authentification token/password/SecretRef pour TUI, les exigences d'authentification `--url`, l'enregistrement du mode client/capacité, et le comportement de transport, d'authentification et d'historique de gateway associé.
- Chat local embarqué : Couvre le chat local embarqué sur le cycle de vie du backend embarqué, le chargement du catalogue de modèles local, la projection d'événement `chat.send` local, les exécutions locales en file d'attente, l'historique de session local, `/auth` local, la documentation de réparation de configuration locale, et les scénarios de récupération sans Gateway.
- Flux d'authentification local : Couvre le flux d'authentification local sur le cycle de vie du backend embarqué, le chargement du catalogue de modèles local, la projection d'événement `chat.send` local, les exécutions locales en file d'attente, l'historique de session local, `/auth` local, la documentation de réparation de configuration locale, et les scénarios de récupération sans Gateway.
- Boucle de réparation de configuration : Couvre la boucle de réparation de configuration sur le cycle de vie du backend embarqué, le chargement du catalogue de modèles local, la projection d'événement `chat.send` local, les exécutions locales en file d'attente, l'historique de session local, `/auth` local, la documentation de réparation de configuration locale, et les scénarios de récupération sans Gateway.
- Récupération sans Gateway : Couvre la récupération sans Gateway sur le cycle de vie du backend embarqué, le chargement du catalogue de modèles local, la projection d'événement `chat.send` local, les exécutions locales en file d'attente, l'historique de session local, `/auth` local, la documentation de réparation de configuration locale, et les scénarios de récupération sans Gateway.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (82%)`
- Signaux positifs : La documentation CLI, l'enregistrement des commandes, les tests d'aide de lancement et les tests PTY du mode local couvrent les principaux points d'entrée utilisateur et la sémantique des alias.
- Signaux négatifs : La couverture du lancement en mode Gateway est principalement au niveau unitaire et au niveau de l'adaptateur de transport plutôt qu'un scénario de terminal Gateway réel récurrent.
- Lacunes d'intégration : ajouter une fiche de score de lancement réel récurrent qui démarre `openclaw tui` contre une Gateway gérée, contre `--url`, et via relancement setup/hatch.

## Score de Qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : `gitcrawl search issues "tui terminal local chat" -R openclaw/openclaw --state all --json number,title,url,state --limit 10` a retourné des rapports ouverts adjacents au lancement TUI incluant `#42461` pour la sélection de port Gateway obsolète, `#74385` pour le mode terminal Hatch lent, et `#74614` / `#78360` pour les problèmes de cycle de vie de chat visibles après le lancement.
- Rapports Discrawl : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "tui terminal local chat"` a retourné une discussion de mainteneur/version que le mode TUI embarqué local a atterri dans la PR `#66767`, la documentation a atterri dans la PR `#69995`, et les correctifs setup/hatch de suivi sont restés ouverts.
- Bonnes qualités : les alias de commande sont explicites, le mode local s'exclut mutuellement avec les identifiants distants, les valeurs de délai d'attente et de limite d'historique invalides sont gérées au lancement, et le code de relancement préserve le mode et le stdio enfant.
- Mauvaises qualités : les rapports d'archive actifs montrent que le contexte de lancement fuit toujours les hypothèses Gateway obsolètes et les performances du mode terminal Hatch/setup peuvent être surprenantes.
- Exclu de la qualité : profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution.

## Score de Complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/tui-and-terminal-ux.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le lancement TUI Gateway, le lancement chat local, le lancement alias Terminal, le lancement message initial, la validation des options de lancement, la connexion Gateway, l'authentification Gateway, le chargement de l'historique à l'attachement, la visibilité de la reconnexion, les RPC de commande Gateway, le chat local embarqué, le flux d'authentification local, la boucle de réparation de configuration, la récupération sans Gateway.
- Signaux négatifs : la note archivée a précédé le score de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Le lancement en mode Gateway manque de la même preuve au niveau PTY que le mode local.
- Le relancement setup/hatch a toujours besoin d'un contrat d'opérateur net pour savoir quand il devrait rester local par rapport à l'attachement à une Gateway.

## Preuve

### Docs

- `docs/cli/tui.md:20` documente `--local`, `--url`, les drapeaux d'authentification, `--message`, `--timeout-ms`, et `--history-limit`.
- `docs/cli/tui.md:35` documente `openclaw chat` et `openclaw terminal` comme alias du mode local.
- `docs/web/tui.md:35` documente le mode local sans passerelle et le comportement des alias.
- `docs/cli/index.md:32` liste `tui`, `chat`, et `terminal` sous la famille de commandes runtime et sandbox.

### Source

- `src/cli/tui-cli.ts:10` enregistre `tui` ; `src/cli/tui-cli.ts:11` et `src/cli/tui-cli.ts:12` enregistrent les alias `terminal` et `chat`.
- `src/cli/tui-cli.ts:34` détecte les alias et implique le mode local ; `src/cli/tui-cli.ts:37` rejette le mode local avec les remplacements d'URL/token/mot de passe.
- `src/tui/tui-launch.ts:36` construit les arguments du processus enfant et préserve `--local`, `--url`, l'authentification, la session, la réflexion, le message, le délai d'attente, la limite d'historique, et les drapeaux de livraison.
- `src/tui/tui.ts:479` initialise `runTui()` avec le mode local/passerelle, la configuration, l'agent, la session, et l'état de l'interface utilisateur.

### Tests d'intégration

- `src/tui/tui-pty-harness.e2e.test.ts:368` pilote la boucle réelle du terminal TUI via une entrée typée avec un faux backend.
- `src/tui/tui-pty-local.e2e.test.ts:249` lance `scripts/run-node.mjs tui --local` et pilote un backend local contre un point de terminaison de modèle simulé.
- `test/vitest/vitest.tui-pty.config.ts:5` définit les fichiers e2e PTY TUI ciblables et sérialise la voie.

### Tests unitaires

- `src/tui/tui-launch.test.ts:98` vérifie que le mode local est transmis au TUI relancé.
- `src/tui/tui-launch.test.ts:111` vérifie la propagation du message initial et du délai d'attente.
- `src/tui/tui.test.ts:404` couvre le drainage du terminal avant l'arrêt.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues "tui terminal local chat" -R openclaw/openclaw --state all --json number,title,url,state --limit 10`

Résultats :

- A retourné 6 rapports ouverts. Les éléments pertinents de lancement/point d'entrée incluaient `#42461` sélection de port passerelle obsolète et `#74385` mode terminal Hatch lent.

### Requêtes Discrawl

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "tui terminal local chat"`

Résultats :

- A retourné une discussion de mainteneur et de PR confirmant que le mode TUI intégré local et les alias ont été déployés, avec un suivi du polissage setup/hatch toujours actif.
