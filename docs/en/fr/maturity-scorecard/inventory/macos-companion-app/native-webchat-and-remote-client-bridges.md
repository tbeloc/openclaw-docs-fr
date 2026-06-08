---
title: "Application compagne macOS - Note de maturité WebChat distant"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne macOS - Note de maturité WebChat distant

## Résumé

Le pont WebChat natif macOS partage le contrat Gateway WebSocket avec WebChat navigateur tout en ajoutant des fenêtres/panneaux SwiftUI, la sélection de session, les contrôles de modèle/réflexion, la santé, les événements et la gestion des tunnels SSH distants. La couverture est Bêta car les tests Swift couvrent de nombreuses pièces du pont, mais la preuve de fumée de version sur le sommeil, le mode distant, la reconnexion et la récupération du tunnel SSH est plus mince. La qualité est Bêta car le pont réutilise bien le protocole Gateway, tandis que les preuves d'archive montrent que la réinitialisation de session, la reconnexion et les distinctions de type de client restent des problèmes actifs.

## Portée de la catégorie

Inclus dans cette catégorie :

- Transport WebChat macOS : Couvre le transport WebChat macOS sur WebChat natif macOS, la réutilisation de connexion Gateway, le mappage de transport de chat natif, la présentation de fenêtre/panneau et le comportement des ponts de client WebChat distant associés.
- Plan de données du tunnel SSH : Couvre le plan de données du tunnel SSH sur WebChat natif macOS, la réutilisation de connexion Gateway, le mappage de transport de chat natif, la présentation de fenêtre/panneau et le comportement des ponts de client WebChat distant associés.
- Mode distant ws/wss direct : Couvre le mode distant ws/wss direct sur WebChat natif macOS, la réutilisation de connexion Gateway, le mappage de transport de chat natif, la présentation de fenêtre/panneau et le comportement des ponts de client WebChat distant associés.
- Continuité de session : Couvre la continuité de session sur WebChat natif macOS, la réutilisation de connexion Gateway, le mappage de transport de chat natif, la présentation de fenêtre/panneau et le comportement des ponts de client WebChat distant associés.
- Dépannage distant : Couvre le dépannage distant sur WebChat natif macOS, la réutilisation de connexion Gateway, le mappage de transport de chat natif, la présentation de fenêtre/panneau et le comportement des ponts de client WebChat distant associés.

## Fonctionnalités

- Transport WebChat macOS : Couvre le transport WebChat macOS sur WebChat natif macOS, la réutilisation de connexion Gateway, le mappage de transport de chat natif, la présentation de fenêtre/panneau et le comportement des ponts de client WebChat distant associés.
- Plan de données du tunnel SSH : Couvre le plan de données du tunnel SSH sur WebChat natif macOS, la réutilisation de connexion Gateway, le mappage de transport de chat natif, la présentation de fenêtre/panneau et le comportement des ponts de client WebChat distant associés.
- Mode distant ws/wss direct : Couvre le mode distant ws/wss direct sur WebChat natif macOS, la réutilisation de connexion Gateway, le mappage de transport de chat natif, la présentation de fenêtre/panneau et le comportement des ponts de client WebChat distant associés.
- Continuité de session : Couvre la continuité de session sur WebChat natif macOS, la réutilisation de connexion Gateway, le mappage de transport de chat natif, la présentation de fenêtre/panneau et le comportement des ponts de client WebChat distant associés.
- Dépannage distant : Couvre le dépannage distant sur WebChat natif macOS, la réutilisation de connexion Gateway, le mappage de transport de chat natif, la présentation de fenêtre/panneau et le comportement des ponts de client WebChat distant associés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (74%)`
- Signaux positifs : Les tests IPC macOS couvrent la fumée SwiftUI WebChat, le comportement du gestionnaire, la clé de session principale, la connexion/demande/configuration du canal Gateway, le contrôle de connexion Gateway, le magasin de points de terminaison, la découverte, le tunnel de port distant et les invites d'authentification distante.
- Signaux négatifs : Il y a moins de preuve répétée pour le sommeil/réveil réel de l'application, la déconnexion réseau, la perte du tunnel SSH distant, le repli distant direct/tailnet et la continuité de session longue durée que pour les tests locaux du navigateur.
- Lacunes d'intégration : Ajouter une fumée de version native pour WebChat local, WebChat distant sur SSH, tailnet direct distant, reconnexion sommeil/réveil, redémarrage du tunnel et continuité de session après redémarrage de la passerelle.

## Score de qualité

- Score : `Bêta (76%)`
- Rapports Gitcrawl : Les requêtes `mac WebChat` et `remote WebChat` ont retourné #39597 pour distinguer les types de client Mac app vs navigateur, #87700 pour la réinitialisation de session après déconnexion réseau/sommeil, #38091 pour la reconnexion WebSocket UI causant la terminaison de session, #78674 pour l'identité client nulle via le tunnel Cloudflare, et les PR #74733 et #87474 pour l'ordre des messages et l'état faux occupé.
- Rapports Discrawl : La requête macOS distant exacte n'a retourné aucune ligne, mais le trafic d'archive WebChat et Control UI mentionne à plusieurs reprises la reconnexion, la session obsolète, l'accès distant/hébergé et les corrections de routage visibles.
- Bonnes qualités : L'application native réutilise un seul acteur Gateway WebSocket, mappe les événements Gateway dans les événements de transport d'interface utilisateur de chat partagés, enregistre les sessions actives et gère la réutilisation/redémarrage du tunnel SSH avec des vérifications d'écouteur.
- Mauvaises qualités : Le mode distant natif ajoute l'OS, le réseau, le tunnel et l'état de sommeil qui ne sont pas visibles dans les tests navigateur uniquement ; les problèmes de continuité de session apparaissent toujours dans l'historique d'archive.
- Exclu de la qualité : La preuve unitaire, d'intégration, e2e, en direct et de flux d'exécution réel affectent uniquement la couverture.

## Score de complétude

- Score : `Bêta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-companion-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le transport WebChat macOS, le plan de données du tunnel SSH, le mode distant ws/wss direct, la continuité de session, le dépannage distant.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les types de client WebChat Mac app et navigateur ne sont pas entièrement distincts dans la sémantique du produit.
- La récupération après sommeil/déconnexion réseau reste un risque connu pour la continuité de session.
- Le comportement du tunnel distant et du repli tailnet nécessite plus de preuve régulière dans le cadre de la qualification de version.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/mac/webchat.md` documente WebChat macOS, l'utilisation directe de Gateway WebSocket, le mode local/distant, le lancement/débogage, les RPC, les événements, le comportement de session et la limite de sécurité.
- `/Users/kevinlin/code/openclaw/docs/gateway/remote.md` documente l'accès distant WebChat, les tunnels SSH, le mode direct LAN/Tailnet, le mode distant macOS et les règles de sécurité.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/remote.md` documente la configuration distante macOS et note qu'il n'y a pas de serveur HTTP WebChat séparé.

### Source

- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/WebChatSwiftUI.swift` mappe les événements Gateway chat/history/models/sessions/abort au transport d'interface utilisateur de chat natif partagé.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/WebChatManager.swift` gère le cycle de vie de la fenêtre/panneau et les clés de session actives.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/GatewayConnection.swift` possède la connexion WebSocket Gateway partagée et le comportement de demande/nouvelle tentative.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/RemoteTunnelManager.swift` gère la création du tunnel SSH, la réutilisation, les vérifications d'écouteur et le backoff de redémarrage.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/GatewayEndpointStore.swift` et `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/RemoteGatewayProbe.swift` supportent la sélection de point de terminaison et le sondage distant.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/WebChatSwiftUISmokeTests.swift`, `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/WebChatManagerTests.swift` et `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/WebChatMainSessionKeyTests.swift` couvrent le comportement natif de l'interface utilisateur WebChat et de session.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/GatewayChannelConnectTests.swift`, `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/GatewayChannelRequestTests.swift` et `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/GatewayConnectionControlTests.swift` couvrent la communication Gateway.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/RemotePortTunnelTests.swift`, `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/ConfigureRemoteCommandTests.swift` et `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/OnboardingRemoteAuthPromptTests.swift` couvrent le support du mode distant.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/MacGatewayChatTransportMappingTests.swift` couvre le mappage du transport de chat natif.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/GatewayEndpointStoreTests.swift`, `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/GatewayEnvironmentTests.swift` et `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/GatewayDiscoveryModelTests.swift` couvrent la logique de point de terminaison et de découverte de support.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "mac WebChat"`

Résultats :

- Retourné ouvert #39597, `Feature: Distinguish webchat client types (Mac app vs browser)`.
- Retourné ouvert #87700, `Control UI webchat session silently resets after network disconnect / sleep`.
- Retourné ouvert #54874, saisie lente dans l'entrée WebChat, plus les problèmes de routage/session #67735, #77012 et #86262.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "remote WebChat"`

Résultats :

- Retourné ouvert #38091 pour la reconnexion WebSocket UI causant la terminaison de session.
- Retourné ouvert #78674 pour l'identité client nulle via le tunnel Cloudflare.
- Retourné ouvert #87387 et #87700 pour l'état faux en cours et le comportement de reconnexion/réinitialisation de session.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "mac WebChat"`

Résultats :

- Retourné ouvert PR #74733, `fix(ui): stabilize WebChat message ordering`.
- Retourné ouvert PR #86335, `feat(webchat): allow safe app-protocol links`.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "macOS WebChat remote mode Gateway WebSocket SSH tunnel"`

Résultats :

- Retourné aucune ligne.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 20 "WebChat"`

Résultats :

- Trouvé le trafic de mainteneur et de version sur la préservation d'envoi de reconnexion, le routage WebChat obsolète et les corrections de chat/session.
