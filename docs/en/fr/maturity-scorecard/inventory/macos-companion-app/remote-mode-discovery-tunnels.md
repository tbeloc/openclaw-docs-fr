---
title: "Application compagne macOS - Note de maturité des connexions distantes"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne macOS - Note de maturité des connexions distantes

## Résumé

Le mode distant est largement implémenté : l'application peut configurer l'accès SSH ou direct ws/wss Gateway, maintenir un tunnel de contrôle en boucle locale, démarrer le service d'hôte de nœud local, gérer l'épinglage TLS et réutiliser le même chemin WebChat/santé. La couverture est Beta car les flux de tunnel, découverte, épinglage et santé ont une implémentation concrète avec preuve d'aide, mais aucun scénario d'application Gateway distante de bout en bout n'a été trouvé. La qualité est Alpha en raison des preuves d'archive autour de la récupération de jeton obsolète, de la confusion tunnel SSH/découverte et de la dérive de capacité du nœud macOS distant.

## Portée de la catégorie

Inclus dans cette catégorie :

- Sélection du mode de connexion distante : sélection et configuration du mode de connexion distante
- Tunnel SSH : tunnel SSH et transport Gateway ws/wss direct
- Découverte Gateway : découverte Gateway, réparation d'épinglage TLS et démarrage du service de nœud distant

## Fonctionnalités

- Sélection du mode de connexion distante : sélection et configuration du mode de connexion distante
- Tunnel SSH : tunnel SSH et transport Gateway ws/wss direct
- Découverte Gateway : découverte Gateway, réparation d'épinglage TLS et démarrage du service de nœud distant

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (72%)`
- Signaux positifs : la documentation couvre le tunnel SSH, ws/wss direct, CLI de configuration, réutilisation WebChat, permissions et dépannage. La source a des branches de coordinateur de mode explicites, réutilisation/redémarrage/backoff de tunnel, configuration de commande distante, magasin de points de terminaison, politique d'épinglage TLS et démarrage du service de nœud.
- Signaux négatifs : les tests unitaires se concentrent sur la logique d'aide de tunnel et les décisions TLS. Ils ne prouvent pas un vrai hôte distant avec SSH, Tailscale, rotation d'authentification Gateway, WebChat, réveil vocal et capacités de nœud Mac.
- Lacunes d'intégration : manque un scénario d'application distante de bout en bout avec configuration de tunnel SSH, `wss://*.ts.net` direct, réparation d'épinglage obsolète, rotation de jeton, démarrage du service d'hôte de nœud, tour WebChat et invocation de capacité macOS.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : les résultats incluent le problème #26250 sur la vérification de sécurité du transport SSH avant l'établissement du tunnel, le problème #47342 sur le transport SSH de l'hôte de nœud et l'authentification du proxy inverse, le problème #69135 sur la détection Gateway dupliquée accessible avec tunnel SSH plus URL distante, et la PR #82739 montrant la récupération du tunnel du canal de contrôle dans le contexte d'icône dupliquée.
- Rapports Discrawl : la discussion du responsable du 2026-05-01 appelle la récupération de jeton partagé obsolète pour les clients Swift distants pertinente pour la version ; le miroir GitHub Discord montre également le problème d'éligibilité de compétence macOS distant #71877 et le problème de chemin du navigateur SSH distant #67336.
- Bonnes qualités : la documentation distante est explicite sur le choix du transport, la sécurité du tunnel en boucle locale, les vérifications strictes de clé d'hôte, la réparation d'empreinte TLS pour la boucle locale de confiance/Tailscale Serve, et le dépannage quand le tableau de bord fonctionne mais les capacités Mac sont hors ligne.
- Mauvaises qualités : le contrôle distant dépend de SSH, PATH, authentification, réutilisation de tunnel, épinglage TLS, état du service de nœud et permissions macOS. Les preuves d'archive montrent que ces limites peuvent bloquer les clients appairés ou les compétences distantes.
- Exclu de la qualité : la couverture des tests unitaires, intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-companion-app.md`.
- Signaux positifs : les preuves d'archive, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la sélection du mode de connexion distante, le tunnel SSH, la découverte Gateway.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Besoin de preuve de fumée de version pour la rotation d'authentification d'hôte distant et la récupération TLS/empreinte de confiance.
- Besoin d'une distinction d'opérateur plus claire entre la connexion de contrôle saine, WebChat sain et la connexion de nœud/capacité Mac saine.
- Besoin d'un scénario de sonde de compétence/bin de nœud macOS distant qui prouve `system.which` et la propriété du navigateur/canevas.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/platforms/mac/remote.md` documente les modes local/distant/direct, le comportement du tunnel SSH, les prérequis de l'hôte distant, CLI de configuration, WebChat, permissions, sécurité et dépannage.
- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md` documente le mode distant, la plomberie du tunnel, CLI de débogage et la préférence pour Tailscale MagicDNS.
- `/Users/kevinlin/code/openclaw/docs/gateway/remote.md` fournit des conseils Gateway d'hôte distant adjacents.

### Source

- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/ConnectionModeCoordinator.swift` arrête la Gateway locale, démarre le service de nœud, assure le tunnel de contrôle distant et configure le canal de contrôle en mode distant.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/RemoteTunnelManager.swift` crée/réutilise/redémarre les tunnels SSH avec vérifications d'écouteur et backoff de redémarrage.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/RemotePortTunnel.swift` construit le processus de transfert SSH.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/NodeMode/MacNodeModeCoordinator.swift` gère les épingles TLS distantes et la réparation d'épingle Tailscale Serve obsolète.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClawMacCLI/ConfigureRemoteCommand.swift` écrit la configuration distante.

### Tests d'intégration

- Aucun scénario d'intégration d'application d'hôte distant complet n'a été trouvé.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/GatewayConnectionControlTests.swift` utilise des sessions WebSocket factices pour le comportement de connexion Gateway, pas un hôte distant.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/RemotePortTunnelTests.swift` couvre la détection sans port et l'analyse de remplacement de port distant.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/ConfigureRemoteCommandTests.swift` couvre la configuration CLI distante.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/MacNodeModeCoordinatorTests.swift` couvre les paramètres TLS distants et les décisions de réparation automatique d'épingle obsolète.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/GatewayDiscoveryModelTests.swift`, `WideAreaGatewayDiscoveryTests.swift` et `TailscaleServeGatewayDiscoveryTests.swift` couvrent les aides de découverte.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "macOS remote gateway ssh tunnel" --json`

Résultats :

- Problème #26250 `SSH transport security check rejects connection before tunnel is established`.
- Problème #47342 `Node host: no SSH transport support + challenge auth fails behind reverse proxy`.
- Problème #69135 ``gateway probe`: false positive "multiple reachable gateways" when SSH tunnel + remote.url hit the same gateway`.
- PR #82739 incluse preuve de journal de récupération de tunnel du canal de contrôle SSH.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "macOS remote gateway"`

Résultats :

- Thread du responsable du 2026-05-01 : récupération de jeton partagé obsolète Swift distant et boucle de nouvelle tentative/annulation ont été appelées pertinentes pour la version.
- Miroir GitHub du 2026-04-26 : le problème #67336 note la réécriture du chemin du navigateur distant sur SSH vers l'URL d'hôte découverte.
- Miroir GitHub du 2026-04-26 : le problème #71877 note l'éligibilité de compétence macOS distant ignorant les réponses de carte d'objet `system.which`.
