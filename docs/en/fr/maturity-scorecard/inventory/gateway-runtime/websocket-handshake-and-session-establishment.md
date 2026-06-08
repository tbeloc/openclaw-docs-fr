---
title: Gateway Runtime WebSocket Feature Matrix - WebSocket Connection
version: 3
last_refreshed: 2026-05-29
last_refreshed_by: codex
feature_family: WebSocket connection setup
feature_slug: websocket-handshake-and-session-establishment
---

# Connexion WebSocket

## Résumé

OpenClaw dispose d'une poignée de main WebSocket Gateway bien définie : le serveur envoie
`connect.challenge`, les clients doivent envoyer une première requête `connect`,
les plages de protocole sont négociées, `hello-ok` porte les champs de découverte,
snapshot, authentification et politique requis, et les défaillances de démarrage-sidecar réessayables
sont représentées comme `UNAVAILABLE`. Le chemin de connexion principal dispose d'une
preuve WS Gateway/serveur réelle, donc la couverture est `Yes`.

Les lacunes principales ne concernent pas le contrat de poignée de main de base. Les lacunes de couverture subsistent autour
du démarrage-sidecar retry et de l'actualisation `pluginSurfaceUrls` dans les flux Gateway/nœud complets. Les lacunes de qualité sont opérationnelles et des lacunes d'attentes : observabilité de la phase de poignée de main, rapports d'appairage d'appareils ouverts sur les plates-formes moins courantes, et
l'absence d'un SDK client Gateway WS public réutilisable.

## Fonctionnalités

- Transport WebSocket : Transport WebSocket avec trames texte JSON.
- Défi de connexion : `connect.challenge` obligatoire avant la connexion.
- Requête de connexion : Requête `connect` obligatoire en première trame.
- Négociation de version de protocole : Négociation de plage de protocole (`minProtocol`/`maxProtocol`).
- Snapshot hello-ok : Structure de charge utile `hello-ok` requise : identité du serveur, authentification négociée, découverte de fonctionnalités, snapshot et limites de politique.
- Démarrage retry : Comportement `UNAVAILABLE` de démarrage-sidecar réessayable pendant le démarrage de Gateway.
- Limites de session : Annonce de politique post-poignée de main (`maxPayload`, `maxBufferedBytes`, `tickIntervalMs`).
- URL de surface de plugin : Émission et actualisation optionnelles de `pluginSurfaceUrls`.

## Fraîcheur de l'archive

- `gitcrawl doctor --json`: `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, `repository_count=2`.
- `discrawl status --json`: `generated_at=2026-05-30T00:04:12Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Couverture

Score : 84

Étiquette : Yes

Signaux positifs :

- La documentation définit le transport WS, les trames texte JSON, la première requête `connect` obligatoire, le plafond de 64 KiB avant connexion, et les limites de politique post-poignée de main dans
  `docs/gateway/protocol.md:15`.
- La documentation définit `connect.challenge`, les paramètres `connect`, `hello-ok`, le démarrage
  `UNAVAILABLE`, et les `pluginSurfaceUrls` optionnels dans
  `docs/gateway/protocol.md:27`.
- La documentation d'architecture décrit les clients du plan de contrôle et des nœuds utilisant le même
  serveur WS et documente l'invariant de poignée de main obligatoire dans
  `docs/concepts/architecture.md:10` et `docs/concepts/architecture.md:76`.
- Le schéma de protocole requiert les champs `ConnectParamsSchema`, les champs serveur/fonctionnalités/snapshot/authentification/politique de `HelloOkSchema`, les `pluginSurfaceUrls` optionnels, et
  les limites de politique dans `src/gateway/protocol/schema/frames.ts:20` et
  `src/gateway/protocol/schema/frames.ts:73`.
- Le serveur envoie le nonce `connect.challenge` immédiatement après l'ouverture du socket
  dans `src/gateway/server/ws-connection.ts:313`.
- Le serveur rejette les premières trames non-`connect` ou les paramètres de connexion invalides dans
  `src/gateway/server/ws-connection/message-handler.ts:523`.
- Le serveur retourne le démarrage-sidecar `UNAVAILABLE` réessayable et ferme avec le
  code de fermeture de démarrage dans `src/gateway/server/ws-connection/message-handler.ts:598`.
- Le serveur négocie les plages de protocole et rejette les incompatibilités dans
  `src/gateway/server/ws-connection/message-handler.ts:614`.
- Le serveur valide la liaison de nonce d'appareil par rapport au nonce de défi dans
  `src/gateway/server/ws-connection/message-handler.ts:913`.
- Le serveur construit `pluginSurfaceUrls`, enregistre le client, augmente la charge utile maximale du socket post-authentification, et envoie `hello-ok` avec méthodes/événements/snapshot/authentification et
  politique dans `src/gateway/server/ws-connection/message-handler.ts:1598`,
  `src/gateway/server/ws-connection/message-handler.ts:1651`, et
  `src/gateway/server/ws-connection/message-handler.ts:1790`.
- Le client attend `connect.challenge`, inclut l'authentification d'appareil liée au nonce dans
  `connect`, stocke les jetons d'appareil, adopte `hello-ok.policy.tickIntervalMs`, et
  réessaye le démarrage-sidecar `UNAVAILABLE` en utilisant le délai de nouvelle tentative annoncé dans
  `src/gateway/client.ts:552`, `src/gateway/client.ts:664`,
  `src/gateway/client.ts:997`, et `src/gateway/client.ts:600`.
- Des preuves de flux Gateway/serveur réel existent : `src/gateway/gateway.test.ts:156`
  démarre une Gateway, connecte un client Gateway, et envoie une requête d'agent sur
  WS ; `src/gateway/test-helpers.e2e.ts:242` montre que l'assistant démarre
  `startGatewayServer` et connecte un `GatewayClient` sur
  `ws://127.0.0.1:<port>`.
- Des preuves d'assistant WS réel existent pour le flux de défi/nonce dans
  `src/gateway/test-helpers.e2e.ts:125` et
  `src/gateway/test-helpers.server.ts:956`.
- Les tests WS du serveur couvrent `connect.challenge`, `hello-ok`, incompatibilité de protocole,
  compatibilité de sonde, requête première non-`connect`, nonce-required, nonce-mismatch,
  et paramètres de connexion invalides dans `src/gateway/server.auth.default-token.suite.ts:124`,
  `src/gateway/server.auth.default-token.suite.ts:404`,
  `src/gateway/server.auth.default-token.suite.ts:418`,
  `src/gateway/server.auth.default-token.suite.ts:439`,
  `src/gateway/server.auth.default-token.suite.ts:470`,
  `src/gateway/server.auth.default-token.suite.ts:481`, et
  `src/gateway/server.auth.default-token.suite.ts:524`.
- L'application de limite de charge utile préauth est testée avec des diagnostics dans
  `src/gateway/server.preauth-hardening.test.ts:195`.
- Le démarrage-sidecar `UNAVAILABLE` est couvert au niveau du gestionnaire/test-client dans
  `src/gateway/server/ws-connection.startup.test.ts:31` et
  `src/gateway/client.test.ts:600`.

Signaux négatifs :

- Le comportement de démarrage-sidecar retry dispose de bons tests de source et de gestionnaire/client, mais je
  n'ai pas trouvé d'intégration de démarrage Gateway complète qui maintient les sidecars réels
  en attente et prouve qu'un client en direct réessaye jusqu'à `hello-ok`.
- L'émission de `pluginSurfaceUrls` est enfilée à travers le chemin de connexion WS, mais
  le chemin d'actualisation est principalement testé au niveau unitaire/gestionnaire dans
  `src/gateway/server-methods/nodes.invoke-wake.test.ts:432` et
  `src/gateway/plugin-node-capability.test.ts:141`, pas une intégration complète de poignée de main-plus-actualisation de nœud.
- La forme de charge utile requise de `hello-ok` est soutenue par un schéma et partiellement affirmée dans
  les tests d'intégration, mais il n'y a pas de test de contrat de haut niveau unique affirmant
  l'objet `hello-ok` documenté entier.

Lacunes d'intégration :

- Ajouter une intégration complète de démarrage-sidecar en attente qui démarre une Gateway réelle dans
  l'état en attente, observe `UNAVAILABLE` réessayable, puis complète le démarrage et
  confirme que le client atteint `hello-ok`.
- Ajouter une intégration WS de nœud complète qui prouve que `pluginSurfaceUrls` sont émis sur
  `hello-ok`, expirent/s'actualisent via `node.pluginSurface.refresh`, et restent
  limités à la session du nœud.
- Ajouter une affirmation de contrat `hello-ok` complète dans un flux de serveur réel afin que le schéma,
  la documentation, et la dérive de charge utile d'exécution soient détectés avant les régressions du client.

## Qualité

Score : 76

Label : Moyen

Rapports Gitcrawl :

- `gitcrawl search issues "gateway websocket handshake timeout" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné 20 lignes plafonnées, toutes fermées. Les rapports pertinents incluent #73631
  « WebSocket handshake-timeout on reconnect causes Control UI to stay
  disconnected for minutes », #56254 « CLI handshake timeout when plugins take
  > 3s to load », #54616 « Feature request: configurable WebSocket handshake
  > timeout », #61554 « WebSocket handshake timeout when executing `openclaw cron
list` », #52453 « Gateway WebSocket rejects all inbound client connections with
  > handshake timeout », #48297 « Gateway sends connect.challenge but CLI never
  > replies with signed nonce », et #64911 « Gateway logs ready before websocket
  > control plane is usable ».
- `gitcrawl search issues "connect.challenge" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné 20 lignes plafonnées. La plupart étaient des régressions de handshake/nonce fermées, incluant
  #50504, #9222, #9225, #49726, #22553, #46560, #52837, #49118, #46218,
  #48297, #49291, #15922, #68944, #50603, et #46885.
- `gitcrawl search issues "hello-ok" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné 20 lignes plafonnées. Les lignes pertinentes incluent #6411 demandant l'identité de l'agent
  dans `hello-ok`, #46560 pour l'identité du dispositif manquante/signature de défi dans la dispatch WS A2A, #64911 pour
  le comportement de démarrage ready-before-usable, et #41652 pour
  les erreurs de non-concordance device-id.
- `gitcrawl search issues "startup-sidecars" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné 20 lignes plafonnées. Les lignes ouvertes incluent #85366, #78954, et #84771 ; les lignes fermées
  incluent #75051, #73276, #74325, #73555, #73645, #73411, #73353, et
  #82398. Celles-ci indiquent que le timing des startup-sidecar reste un point de pression actif pour
  l'établissement de session.
- `gitcrawl search issues "websocket handshake timeout" -R openclaw/openclaw --state open --json number,title,state,url`
  a retourné 9 lignes : #79603 handshake phase logging, #79601 client identity labels,
  #61095 env leakage causing CLI failures, #73602 channel flapping on WSL2,
  #80344 heartbeat timeout/event-loop starvation, #53399 browser control server
  hang, #83366 event-loop starvation, #49599 custom HTTP headers on CLI WS
  connections, et #76562 RPC latency/unstable polling.
- `gitcrawl search issues "connect.challenge" -R openclaw/openclaw --state open --json number,title,state,url`
  a retourné 7 lignes : #47342 reverse-proxy challenge auth, #53599 browser relay
  regression, #86778 Trim OS/TerraMaster device-proof close 1002, #49178
  reusable Gateway WS client SDK, #47826 REST endpoints, #87058 Android node
  connect-nonce retry race, et #65355 remote probe timeout cap.
- `gitcrawl threads openclaw/openclaw --numbers 86778 --json` montre un rapport utilisateur ouvert où les connexions TCP/WS et la réception de défi fonctionnent, mais la réponse de preuve de dispositif signée se ferme avec le code WS 1002 sur Trim OS/TerraMaster NAS.
- `gitcrawl threads openclaw/openclaw --numbers 78954 --json` montre une demande ouverte pour une limite de démarrage `core-ready` explicite avant que les sidecars de canal/plugin puissent bloquer l'attachement Gateway/TUI.
- `gitcrawl threads openclaw/openclaw --numbers 79603 --json` montre une demande ouverte pour la journalisation du handshake gateway/ws par phase car les défaillances actuelles ne montrent pas si l'acceptation TCP, la mise à niveau WS, la validation d'authentification, l'attachement de session, ou l'enregistrement d'abonnement s'est arrêté.
- `gitcrawl threads openclaw/openclaw --numbers 49178 --json` montre une demande de fonctionnalité ouverte pour un paquet `@openclaw/gateway-client` réutilisable couvrant le handshake challenge-response, l'authentification, la reconnexion, la requête/réponse, et les événements.
- `gitcrawl search issues "pluginSurfaceUrls node.pluginSurface.refresh" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné `[]`.
- `gitcrawl search issues "node.pluginSurface.refresh" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné `[]`.

Rapports Discrawl :

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "connect.challenge"`
  a retourné 10 lignes. La note de mainteneur la plus pertinente sur
  `2026-05-01T08:33:14Z` dans `maintainers` a listé le timing challenge/nonce,
  `connect.challenge` retardé, nonce périmé, défi dupliqué,
  response-before-challenge, rotation de jeton gateway pendant que les sockets sont actifs, rotation d'empreinte TLS, et les courses d'authentification au démarrage comme scénarios de durcissement. Les autres lignes étaient des commentaires de miroir GitHub fermant les rapports de handshake corrigés de l'ère 2026.3.13.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "hello-ok"` a retourné
  10 lignes. Les lignes pertinentes ont mentionné `hello-ok.server.version`,
  `hello-ok.auth`, le comportement de retry du nœud Windows se réinitialisant uniquement après
  `hello-ok`, et les PR de suivi de schéma pour exiger l'authentification `hello-ok`.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "websocket handshake timeout"`
  a retourné 10 lignes. Il incluait une question de support VPS utilisateur qui soupçonnait le handshake WS mais montrait des réponses `gateway/ws` réussies, plus plusieurs commentaires de miroir GitHub fermant les rapports de handshake-timeout corrigés.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "startup-sidecars"`
  a retourné 10 lignes. Les lignes pertinentes ont mentionné les correctifs startup-sidecar actuels,
  les commits, la PR #69164 pour réessayer `chat.history` TUI pendant le démarrage, et un
  contrat de commande de démarrage sidecar.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "preauth handshake timeout"`
  a retourné 10 lignes, tous les commentaires de miroir GitHub pour les rapports de timeout preauth 3s corrigés et les demandes de configurabilité de timeout.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Gateway websocket handlers unavailable"`
  a retourné 3 lignes, incluant une discussion d'examen sur le non-blocage de l'attachement WS sur le démarrage sidecar et l'assurance que le chemin no-listener 503 ne consomme pas le budget preauth.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "pluginSurfaceUrls"`
  n'a retourné aucune ligne.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "node.pluginSurface.refresh"`
  n'a retourné aucune ligne.

Bonnes qualités :

- Le contrat de handshake est explicite dans la documentation, le schéma, l'implémentation du serveur,
  et le comportement du client.
- Le serveur enregistre les causes de fermeture et l'état du handshake autour des défaillances dans
  `src/gateway/server/ws-connection.ts:370`.
- La configuration du timeout est centralisée via
  `src/gateway/handshake-timeouts.ts:1`, et la résolution du timeout client/serveur
  partagent le même modèle.
- Les limites de charge utile sont appliquées avant et après l'authentification, avec des événements de diagnostic pour les trames surdimensionnées et les tampons sortants lents.
- Les résultats d'archive actuels montrent de nombreux anciens rapports de timeout de handshake et de nonce manquant fermés comme implémentés, avec des atténuations expédiées telles que les timeouts preauth/connect-challenge plus longs et la gestion des défis côté client.

Mauvaises qualités :

- L'archive a toujours des rapports ouverts adjacents à l'établissement de session :
  #86778 pour une fermeture device-proof 1002, #79603 pour la journalisation de phase de handshake manquante, #49178 pour aucun SDK client WS réutilisable, et #78954/#85366/#84771 pour la pression startup-sidecar/event-loop.
- Certaines classes de défaillance ne sont observables que comme résultats finaux de fermeture/erreur ; l'ouverture #79603 indique que les opérateurs ne peuvent toujours pas localiser de manière fiable la phase arrêtée.
- L'implémentation s'étend sur plusieurs fichiers et a des clients Node/navigateur/natifs séparés, donc la pression de dérive persiste jusqu'à ce qu'un contrat client partagé existe.

## Lacunes connues

Lacunes de couverture :

- Preuve complète de retry pending-to-ready du startup-sidecar Gateway.
- Émission complète de `pluginSurfaceUrls` du nœud plus preuve de rafraîchissement.
- Preuve de forme `hello-ok` complète et unique qui protège les attentes du serveur, du schéma, de la documentation, et du client ensemble.

Lacunes opérationnelles et d'attentes :

- SDK client WebSocket Gateway réutilisable public pour les consommateurs tiers, navigateur, mobile,
  et CLI.
- Journaux/traces de phase de handshake plus forts qui identifient la dernière phase complétée en cas de défaillance.
- Une commande de preuve/guide de charge utile de preuve documentée face aux opérateurs pour les cas comme le rapport Trim OS/TerraMaster ouvert.

Demandes utilisateur-mainteneur :

- #49178 demande un SDK client WebSocket Gateway réutilisable avec handshake, authentification,
  reconnexion, requête/réponse, et gestion des événements.
- #79603 demande la journalisation de phase de handshake pour les défaillances gateway/ws.
- #79601 demande les étiquettes d'identité du client sur les connexions WebSocket Gateway.
- #49599 demande les en-têtes HTTP personnalisés sur les connexions WebSocket CLI.
- #78954 demande un core-ready explicite avant les sidecars de canal/plugin.
- #86778 demande le comportement de preuve d'appairage Gateway documenté ou supporté par CLI pour
  un déploiement NAS/Trim OS où la réception de défi fonctionne mais la preuve de dispositif se ferme
  avec le code 1002.
- #54616 a demandé un timeout de handshake WebSocket configurable ; les résultats d'archive montrent
  qu'il est fermé comme implémenté.

## Preuves

Docs :

- `docs/gateway/protocol.md:15` - Trames texte WS, première trame `connect`, capacité de préauthentification, limites de politique post-établissement de connexion et diagnostics.
- `docs/gateway/protocol.md:27` - `connect.challenge`, `connect`, `hello-ok`, démarrage-sidecar `UNAVAILABLE`, champs de charge utile requis et `pluginSurfaceUrls`.
- `docs/gateway/protocol.md:641` - négociation de version de protocole et constantes client.
- `docs/gateway/protocol.md:775` - toutes les connexions signent le nonce `connect.challenge`.
- `docs/concepts/architecture.md:10` - les clients du plan de contrôle et des nœuds se connectent via WebSocket.
- `docs/concepts/architecture.md:76` - résumé du protocole filaire et première trame `connect` obligatoire.
- `docs/concepts/architecture.md:143` - invariant obligatoire d'établissement de connexion.
- Commande exécutée avant la lecture des docs : `pnpm docs:list`.

Source :

- `src/gateway/protocol/schema/frames.ts:20` - schéma des paramètres de connexion.
- `src/gateway/protocol/schema/frames.ts:73` - schéma `hello-ok`.
- `src/gateway/server-constants.ts:1` - limites de charge utile post-authentification, en mémoire tampon et préauthentification.
- `src/gateway/handshake-timeouts.ts:1` - modèle de délai d'expiration par défaut pour préauthentification/connect-challenge et résolution env/config.
- `src/gateway/server-runtime-state.ts:223` - serveur WS créé avant l'écoute HTTP avec limite de charge utile préauthentification.
- `src/gateway/server-http.ts:924` - la mise à niveau WS rejette les gestionnaires manquants et applique le budget de préauthentification.
- `src/gateway/server/ws-connection.ts:313` - le serveur envoie `connect.challenge`.
- `src/gateway/server/ws-connection.ts:433` - délai d'expiration d'établissement de connexion préauthentification.
- `src/gateway/server/ws-connection/message-handler.ts:481` - limite d'octet de charge utile préauthentification et diagnostics.
- `src/gateway/server/ws-connection/message-handler.ts:523` - application de la première trame `connect`.
- `src/gateway/server/ws-connection/message-handler.ts:598` - démarrage-sidecar `UNAVAILABLE` réessayable.
- `src/gateway/server/ws-connection/message-handler.ts:614` - négociation de protocole.
- `src/gateway/server/ws-connection/message-handler.ts:913` - validation du nonce de l'appareil par rapport au défi.
- `src/gateway/server/ws-connection/message-handler.ts:1598` - création d'URL de surface de plugin lors de la connexion.
- `src/gateway/server/ws-connection/message-handler.ts:1790` - assemblage et envoi de charge utile `hello-ok`.
- `src/gateway/client.ts:552` - le client envoie la connexion uniquement après le nonce du défi.
- `src/gateway/client.ts:600` - gestion des tentatives de démarrage-sidecar du client.
- `src/gateway/client.ts:664` - assemblage des paramètres de connexion du client.
- `src/gateway/client.ts:997` - gestion des événements de défi du client.

Tests d'intégration :

- `src/gateway/gateway.test.ts:156` - Gateway e2e réelle connecte un client WS et émet une demande d'agent.
- `src/gateway/test-helpers.e2e.ts:31` - assistant de connexion GatewayClient e2e.
- `src/gateway/test-helpers.e2e.ts:125` - demande de connexion d'authentification d'appareil signée e2e attend `connect.challenge` et envoie une preuve d'appareil liée au nonce.
- `src/gateway/test-helpers.e2e.ts:242` - l'assistant e2e démarre un serveur Gateway et se connecte via `ws://127.0.0.1:<port>`.
- `src/gateway/server.auth.default-token.suite.ts:124` - la connexion WS du serveur retourne `hello-ok`.
- `src/gateway/server.auth.default-token.suite.ts:404` - le serveur envoie `connect.challenge` à l'ouverture.
- `src/gateway/server.auth.default-token.suite.ts:418` - rejet de non-concordance de protocole.
- `src/gateway/server.auth.default-token.suite.ts:470` - rejet de première demande non-connexion.
- `src/gateway/server.auth.default-token.suite.ts:481` - nonce requis pour l'authentification d'appareil.
- `src/gateway/server.auth.default-token.suite.ts:524` - réponse de paramètres de connexion invalides et raison de fermeture.
- `src/gateway/server.preauth-hardening.test.ts:195` - trame de préauthentification surdimensionnée rejetée avant réponse d'authentification d'application avec diagnostics `payload.large`.

Tests unitaires :

- `src/gateway/client.test.ts:600` - le client traite le démarrage-sidecar `UNAVAILABLE` comme réessayable et ferme avec 1013 sans exposer une erreur de connexion terminale.
- `src/gateway/server/ws-connection.startup.test.ts:31` - le gestionnaire retourne un démarrage réessayable `UNAVAILABLE` et enregistre la cause de fermeture attendue.
- `src/gateway/gateway-misc.test.ts:104` - la charge utile maximale WS du client est de 25 Mo.
- `src/gateway/gateway-misc.test.ts:640` - la limite d'octet en mémoire tampon sortante émet `payload.large`.
- `src/gateway/server/ws-connection.test.ts:171` - le contexte d'URL de surface de plugin est transmis au gestionnaire d'établissement de connexion.
- `src/gateway/server-methods/nodes.invoke-wake.test.ts:432` - gestionnaire générique d'actualisation d'URL de capacité de surface de plugin.
- `src/gateway/plugin-node-capability.test.ts:141` - URL de surface de plugin client et actualisation de capacité stockée.

Requêtes Gitcrawl :

- `gitcrawl doctor --json` - actuel ; voir Fraîcheur de l'archive.
- `gitcrawl search issues "gateway websocket handshake timeout" -R openclaw/openclaw --state all --json number,title,state,url`
  - 20 lignes plafonnées, toutes fermées ; lignes clés #73631, #56254, #54616, #61554, #52453, #48297, #64911.
- `gitcrawl search issues "connect.challenge" -R openclaw/openclaw --state all --json number,title,state,url`
  - 20 lignes plafonnées ; principalement des régressions de défi/nonce fermées.
- `gitcrawl search issues "hello-ok" -R openclaw/openclaw --state all --json number,title,state,url`
  - 20 lignes plafonnées ; lignes pertinentes #6411, #46560, #64911, #41652.
- `gitcrawl search issues "startup-sidecars" -R openclaw/openclaw --state all --json number,title,state,url`
  - 20 lignes plafonnées ; lignes ouvertes #85366, #78954, #84771.
- `gitcrawl search issues "websocket handshake timeout" -R openclaw/openclaw --state open --json number,title,state,url`
  - 9 lignes ; lignes ouvertes pertinentes #79603, #79601, #49599.
- `gitcrawl search issues "connect.challenge" -R openclaw/openclaw --state open --json number,title,state,url`
  - 7 lignes ; lignes ouvertes pertinentes #86778, #49178, #87058.
- `gitcrawl search issues "startup-sidecars" -R openclaw/openclaw --state open --json number,title,state,url`
  - 13 lignes ; lignes ouvertes pertinentes #85366, #78954, #84771.
- `gitcrawl search issues "configurable WebSocket handshake timeout" -R openclaw/openclaw --state all --json number,title,state,url`
  - 19 lignes ; #54616 fermé comme implémenté.
- `gitcrawl search issues "pluginSurfaceUrls node.pluginSurface.refresh" -R openclaw/openclaw --state all --json number,title,state,url`
  - 0 lignes.
- `gitcrawl search issues "node.pluginSurface.refresh" -R openclaw/openclaw --state all --json number,title,state,url`
  - 0 lignes.
- `gitcrawl threads openclaw/openclaw --numbers 86778 --json` - rapport de fermeture de preuve d'appareil Trim OS ouvert 1002.
- `gitcrawl threads openclaw/openclaw --numbers 78954 --json` - demande de core-ready-before-sidecars ouverte.
- `gitcrawl threads openclaw/openclaw --numbers 79603 --json` - demande de journalisation de phase d'établissement de connexion ouverte.
- `gitcrawl threads openclaw/openclaw --numbers 49178 --json` - demande de SDK client WS réutilisable ouverte.

Requêtes Discrawl :

- `discrawl status --json` - actuel ; voir Fraîcheur de l'archive.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "connect.challenge"`
  - 10 lignes ; note de scénario de durcissement du responsable pertinente plus miroirs de problèmes corrigés.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "hello-ok"`
  - 10 lignes ; `hello-ok.server.version`, `hello-ok.auth` pertinents et discussions de nouvelle tentative d'authentification de nœud Windows.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "websocket handshake timeout"`
  - 10 lignes ; question de support utilisateur plus miroirs de problèmes corrigés.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "startup-sidecars"`
  - 10 lignes ; discussions de nouvelle tentative de démarrage et d'ordre des sidecars.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "preauth handshake timeout"`
  - 10 lignes ; délai d'expiration de préauthentification de 3 s corrigé et miroirs de configurabilité.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Gateway websocket handlers unavailable"`
  - 3 lignes ; discussion d'examen sur le comportement de mise à niveau WS sans écouteur et budget de préauthentification.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "pluginSurfaceUrls"`
  - 0 lignes.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "node.pluginSurface.refresh"`
  - 0 lignes.
