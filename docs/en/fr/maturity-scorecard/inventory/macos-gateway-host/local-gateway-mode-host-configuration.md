---
title: "Hôte macOS Gateway - Note de Maturité de l'Intégration Local Gateway"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Hôte macOS Gateway - Note de Maturité de l'Intégration Local Gateway

## Résumé

Le mode Local Gateway est le mode hôte macOS le mieux supporté. La documentation et le code source couvrent `gateway.mode=local`, la liaison par défaut en loopback, les garde-fous d'authentification non-loopback, la précédence port/config, la santé/statut, la résolution des points de terminaison d'application locale, et la découverte Bonjour. La principale faiblesse n'est pas le modèle d'exécution local lui-même, mais la dérive de l'opérateur due à la propriété mixte, la configuration obsolète, et les installations en split-brain.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Mode de connexion local/distant de l'application : Coordination du mode de connexion local/distant de l'application
- Installation/redémarrage/désinstallation du LaunchAgent Gateway géré par l'application : Installation/redémarrage/désinstallation du LaunchAgent Gateway géré par l'application via la CLI
- Détection d'installation CLI : Détection d'installation CLI et invite d'installation d'application
- Compatibilité d'attachement au Gateway local existant : Vérifications de compatibilité d'attachement au Gateway local existant
- Point de terminaison Gateway : Résolution du point de terminaison Gateway, des identifiants et du canal de contrôle
- Configuration gateway.mode=local : Configuration gateway.mode=local et définition par défaut lors de l'installation du service
- Liaison en loopback : Liaison en loopback, remplacements explicites d'hôte/liaison, exigences d'authentification, et précédence des ports
- Résolution des points de terminaison d'application locale : Résolution des points de terminaison d'application locale, canal de contrôle local, et comportement d'attachement au Gateway existant
- Découverte Bonjour : Découverte Bonjour et surfaces de statut/sonde/santé locales

## Fonctionnalités

- Mode de connexion local/distant de l'application : Coordination du mode de connexion local/distant de l'application
- Installation/redémarrage/désinstallation du LaunchAgent Gateway géré par l'application : Installation/redémarrage/désinstallation du LaunchAgent Gateway géré par l'application via la CLI
- Détection d'installation CLI : Détection d'installation CLI et invite d'installation d'application
- Compatibilité d'attachement au Gateway local existant : Vérifications de compatibilité d'attachement au Gateway local existant
- Point de terminaison Gateway : Résolution du point de terminaison Gateway, des identifiants et du canal de contrôle
- Configuration gateway.mode=local : Configuration gateway.mode=local et définition par défaut lors de l'installation du service
- Liaison en loopback : Liaison en loopback, remplacements explicites d'hôte/liaison, exigences d'authentification, et précédence des ports
- Résolution des points de terminaison d'application locale : Résolution des points de terminaison d'application locale, canal de contrôle local, et comportement d'attachement au Gateway existant
- Découverte Bonjour : Découverte Bonjour et surfaces de statut/sonde/santé locales

## Fraîcheur des Archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (84%)`
- Signaux positifs : la documentation, la source d'installation du service, la source d'exécution du Gateway, la source du point de terminaison de l'application, la documentation de statut/sonde, et les tests d'exécution multi-Gateway couvrent le mode local de la configuration à l'exécution.
- Signaux négatifs : la preuve du mode local est répartie entre les surfaces CLI, Gateway, application et Bonjour plutôt que dans un scénario macOS complet et emballé.
- Lacunes d'intégration : aucune voie visible unique ne prouve le mode local de l'application, l'installation du LaunchAgent, la publicité Bonjour, l'interface de contrôle, et `gateway status --deep` ensemble après une installation propre.

## Score de Qualité

- Score : `Stable (83%)`
- Rapports Gitcrawl : `gateway.mode local macOS gateway start blocked token port` a retourné le problème ouvert #78493 pour la propriété mixte sudo et la réparation de la configuration après l'échec EACCES/read ; aucune rupture de transport en mode local direct n'a dominé l'ensemble des résultats.
- Rapports Discrawl : `gateway mode local macOS` a retourné des fils de support où la dérive de la configuration/routage a affecté le comportement du Gateway, y compris les problèmes de routage de groupe/session et les rapports fermés autour du redémarrage du gateway local/décalage de jeton.
- Bonnes qualités : la CLI définit par défaut `gateway.mode` à local lors de l'installation, l'exécution du Gateway rejette les combinaisons de liaison/authentification non sûres, la résolution des points de terminaison locaux a une précédence explicite de jeton/mot de passe, et la documentation met l'accent sur le loopback et les vérifications de santé locales.
- Mauvaises qualités : le mode local est sensible à la propriété, au chemin de configuration, au jeton, et à la dérive d'installation-root mixte ; les utilisateurs peuvent toujours se retrouver avec un Gateway installé localement dont la configuration d'exécution n'est pas celle que l'application ou la CLI attend.
- Exclu de la qualité : Les preuves de couverture uniquement ont été considérées uniquement dans le score de Couverture, pas dans ce score de Qualité.

## Score d'Exhaustivité

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-gateway-host.md`.
- Signaux positifs : la documentation archivée, la source, les tests, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour le mode de connexion local/distant de l'application, l'installation/redémarrage/désinstallation du LaunchAgent Gateway géré par l'application, la détection d'installation CLI, la compatibilité d'attachement au Gateway local existant, le point de terminaison Gateway, la configuration gateway.mode=local, la liaison en loopback, la résolution des points de terminaison d'application locale, la découverte Bonjour.
- Signaux négatifs : la note archivée a précédé la notation d'Exhaustivité de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- La propriété mixte et la réparation de la configuration peuvent faire que le mode local semble cassé même lorsque le modèle d'hôte local principal est sain.
- La précédence du point de terminaison local, du jeton et du chemin de configuration devrait être plus facile à inspecter à partir d'une seule commande spécifique à macOS.
- Le démarrage automatique Bonjour et le statut local sont documentés séparément du chemin de configuration du mode local de l'application.

## Preuves

### Documentation

- `docs/gateway/index.md:25` : documente les commandes de démarrage local et de santé.
- `docs/gateway/index.md:71` : documente le modèle d'exécution, le comportement de liaison en loopback par défaut, et l'authentification requise.
- `docs/gateway/index.md:111` : documente la précédence port/liaison et l'actualisation des métadonnées du superviseur.
- `docs/cli/gateway.md:25` : documente `gateway run`, la garde `gateway.mode=local`, et les exigences d'authentification non-loopback.
- `docs/cli/gateway.md:267` : documente `gateway status`, le statut profond, la dérive du chemin de configuration, et les exigences RPC.
- `docs/cli/gateway.md:323` : documente les avertissements `gateway probe` et la détection de plusieurs Gateway.
- `docs/gateway/bonjour.md:9` : documente la découverte LAN Bonjour comme une fonctionnalité de commodité macOS.
- `docs/platforms/macos.md:24` : documente le comportement d'attachement ou d'activation du mode local.

### Source

- `src/cli/daemon-cli/install.ts:80` : écrit `gateway.mode=local` lorsqu'il est manquant lors de l'installation.
- `src/cli/gateway-cli/run.ts:472` : lit la configuration, résout le port, applique la garde de configuration future, et démarre le Gateway.
- `src/cli/gateway-cli/run.ts:575` : applique la gestion du mode de liaison.
- `src/cli/gateway-cli/run.ts:645` : analyse les options de jeton/authentification/Tailscale avant de servir.
- `src/config/paths.ts:56` : résout le répertoire d'état avec le remplacement `OPENCLAW_STATE_DIR` et la valeur par défaut `~/.openclaw`.
- `src/config/paths.ts:151` : résout le chemin de configuration avec le remplacement env.
- `src/config/paths.ts:331` : résout le port Gateway à partir de env/config/défaut.
- `apps/macos/Sources/OpenClaw/GatewayEndpointStore.swift:11` : centralise la résolution du point de terminaison effectif local/distant.
- `apps/macos/Sources/OpenClaw/GatewayEndpointStore.swift:81` : résout la précédence du jeton/mot de passe local à partir de l'application, env, configuration, et launchd.
- `apps/macos/Sources/OpenClaw/GatewayProcessManager.swift:192` : s'attache à un Gateway local existant lorsqu'il est compatible.

### Tests d'intégration

- `test/gateway.multi.e2e.test.ts:27` : lance plusieurs instances de Gateway, crochets HTTP, et appairage de nœuds WebSocket.
- `scripts/e2e/parallels/macos-smoke.ts:827` : effectue l'intégration locale avec `--install-daemon` sur un invité macOS.
- `scripts/e2e/parallels/macos-smoke.ts:923` : vérifie `gateway status --deep --require-rpc` sur l'invité macOS.
- `scripts/e2e/parallels/macos-smoke.ts:980` : charge le tableau de bord via le Gateway local.

### Tests unitaires

- `src/daemon/service-env.test.ts:640` : affirme TMPDIR durable et PATH canonique pour les LaunchAgents macOS.
- `src/daemon/service-env.test.ts:725` : vérifie les règles de persistance proxy/env pour les services gérés.
- `src/commands/doctor-platform-notes.launchctl-env-overrides.test.ts:19` : avertit des remplacements de jeton launchctl qui peuvent affecter l'authentification du Gateway local.
- `apps/macos/Tests/OpenClawIPCTests/CommandResolverTests.swift:210` : assure que le remplacement local ignore les valeurs par défaut distantes pour les commandes daemon.
- `apps/macos/Tests/OpenClawIPCTests/GatewayLaunchAgentManagerTests.swift:29` : analyse le port/liaison/jeton/mot de passe du LaunchAgent Gateway local à partir de l'instantané plist.

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search issues "gateway.mode local macOS gateway start blocked token port" -R openclaw/openclaw --state open --json number,title,url,state --limit 5
```

Résultats :

- Problème ouvert #78493 : `sudo openclaw update can create mixed ownership, then doctor overwrites config after EACCES/read failure`.

### Requêtes Discrawl

Requête :

```bash
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "gateway mode local macOS"
```

Résultats :

- A retourné des fils de support où la dérive de la configuration du Gateway a affecté le comportement d'exécution, y compris la divergence de routage de groupe/DM Discord.
- A retourné des commentaires de miroir GitHub fermant les rapports plus anciens de redémarrage du gateway local macOS/décalage de jeton comme remplacés ou implémentés.
