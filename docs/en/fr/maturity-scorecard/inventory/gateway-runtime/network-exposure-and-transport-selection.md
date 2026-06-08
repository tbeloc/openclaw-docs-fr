---
title: Gateway Runtime and WebSocket Feature Note - Network Access and Discovery
version: 3
last_refreshed: 2026-05-29
last_refreshed_by: codex
feature_family: Network access and discovery
feature_slug: network-exposure-and-transport-selection
---

# Accès réseau et découverte

## Résumé

OpenClaw dispose d'une implémentation substantielle pour l'exposition de Gateway et la sélection de transport : modes de liaison loopback/LAN/tailnet documentés, transport direct à distance par rapport à SSH, découverte Bonjour et DNS-SD à large zone, indices MagicDNS/Tailscale, support TLS à l'exécution, et épinglage d'empreinte TLS côté client. Les preuves de couverture sont les plus solides dans la documentation, les contrats de configuration/source, les tests de client macOS et mobile, et les tranches de gestionnaire/serveur. La qualité est limitée par les régressions signalées dans les archives et la confusion des opérateurs autour de la configuration de Gateway à distance, des modes de liaison, du comportement du tunnel SSH, de Tailscale Serve et de l'épinglage TLS.

Scores :

- Couverture : 68 % - Partielle
- Qualité : 62 % - Moyen

## Fonctionnalités

- Accès loopback et LAN : Exposition de Gateway loopback et LAN.
- Accès Tailnet : Exposition de Gateway orientée Tailnet et routage MagicDNS/Tailscale.
- Tunnels SSH : Tunnelisation SSH comme chemin distant de secours.
- Découverte de points de terminaison : Découverte Bonjour/DNS-SD, DNS-SD à large zone, et indices de transport annoncés.
- Points de terminaison enregistrés : Points de terminaison Gateway distants enregistrés et ordre de préférence des routes.
- Épinglage TLS : Activation TLS et épinglage d'empreinte de certificat optionnel.

## Fraîcheur des archives

- `gitcrawl doctor --json`: `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, `repository_count=2`.
- `discrawl status --json`: `generated_at=2026-05-30T00:04:12Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Couverture

Score : 68 %

Étiquette : Partielle

### Signaux positifs

- Des preuves réelles de flux Gateway/serveur existent pour le renforcement du réseau d'origine du navigateur et d'origine du proxy via les tests WebSocket `withGatewayServer` :
  `src/gateway/server.auth.browser-hardening.test.ts:109`,
  `src/gateway/server.auth.browser-hardening.test.ts:152`,
  `src/gateway/server.auth.browser-hardening.test.ts:217`.
- Les tests d'authentification de l'interface utilisateur de contrôle incluent un chemin WebSocket de style Tailscale :
  `src/gateway/server.auth.control-ui.suite.ts:954`.
- Le démarrage de Gateway dispose d'un test réseau d'exécution de style e2e qui démarre un serveur Gateway avec liaison loopback dans un environnement d'exécution réel :
  `src/gateway/server-network-runtime.e2e.test.ts:68`,
  `src/gateway/server-network-runtime.e2e.test.ts:104`.
- Les tests unitaires et clients couvrent la résolution de liaison, la sélection d'URL directe/distante, le blocage distant en texte brut, les exceptions ws privées, le transfert d'empreinte TLS, le contexte de découverte Bonjour/large zone, et le comportement d'aide Tailscale :
  `src/gateway/net.test.ts:668`,
  `src/gateway/call.test.ts:490`,
  `src/gateway/call.test.ts:537`,
  `src/gateway/call.test.ts:750`,
  `src/gateway/server-discovery-runtime.test.ts:85`,
  `src/gateway/server-discovery-runtime.test.ts:215`,
  `src/infra/tls/gateway.test.ts:79`,
  `src/infra/tailscale.test.ts:62`.
- La découverte macOS et la sélection de transport distant ont des tests ciblés :
  `apps/macos/Tests/OpenClawIPCTests/GatewayDiscoveryModelTests.swift:84`,
  `apps/macos/Tests/OpenClawIPCTests/GatewayDiscoveryModelTests.swift:130`,
  `apps/macos/Tests/OpenClawIPCTests/GatewayDiscoveryHelpersTests.swift:45`,
  `apps/macos/Tests/OpenClawIPCTests/GatewayDiscoveryHelpersTests.swift:72`.
- Les tests de sécurité de connexion iOS couvrent la confiance d'épingle TLS découverte, le forçage TLS manuel non-loopback, l'autorisation de texte brut LAN privé, et la récupération d'épingle obsolète :
  `apps/ios/Tests/GatewayConnectionSecurityTests.swift:39`,
  `apps/ios/Tests/GatewayConnectionSecurityTests.swift:106`,
  `apps/ios/Tests/GatewayConnectionSecurityTests.swift:122`,
  `apps/ios/Tests/GatewayConnectionSecurityTests.swift:159`.

### Signaux négatifs

- Aucun test d'intégration/e2e/en direct unique n'a été trouvé qui prouve la famille de fonctionnalités entière en tant que flux de travail : découvrir une Gateway, choisir direct/SSH à partir de la préférence de route, persister la cible, se connecter sur la route sélectionnée, et valider l'épinglage TLS.
- La liaison LAN/tailnet et le routage distant direct sont bien couverts par les tests de source et unitaires, mais pas par un test de topologie réseau réelle complète.
- Le comportement du tunnel SSH est implémenté et testé dans les unités macOS/CLI ciblées, mais les preuves ne montrent pas un tunnel SSH réel connecté à une Gateway réelle dans une voie d'intégration.
- TLS et l'épinglage ont des tests d'exécution/unitaires/clients, plus des tests d'application, mais pas une large intégration serveur-plus-client WSS d'empreinte qui exerce la sélection directe distante de bout en bout.

### Lacunes d'intégration

- Ajouter un scénario Gateway réel qui utilise `gateway.bind=tailnet` ou un équivalent d'interface privée et prouve qu'un client distant l'atteint sans revenir à loopback.
- Ajouter un scénario de transport SSH qui démarre un vrai transfert de port local et prouve que `gateway.remote.transport="ssh"` atteint la Gateway distante.
- Ajouter un scénario de découverte-à-connexion pour Bonjour ou DNS-SD à large zone qui vérifie la préférence de point de terminaison de service résolue par rapport aux indices TXT non authentifiés.
- Ajouter un scénario WSS/empreinte qui prouve que les épingles configurées et stockées sont honorées sur le même chemin de connexion utilisé par les clients distants.

## Qualité

Score : 62%

Label : Moyen

### Rapports gitcrawl

Les recherches de problèmes spécifiques aux fonctionnalités ont trouvé plusieurs bugs actuels ou historiques autour de la même surface :

- `gitcrawl search issues "gateway remote" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné 20 résultats. Résultats notables : #65355 ouvert
  « gateway probe false-negatives on remote configRemote because non-loopback
  targets are hard-capped to 1500ms » ; #40527 ouvert « Remote skill bin probe times
  out when node is co-located with gateway » ; #67336 fermé « macOS Remote over
  SSH rewrites browser path to discovered ws:// host URL » ; #16674 fermé « macOS
  remote onboarding ... token/pairing/SSH path flow is too fragile » ; #53128
  fermé « `onboard --install-daemon` does not set `gateway.remote.token` ».
- `gitcrawl search issues "gateway bind tailnet lan loopback" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné 20 résultats. Résultats notables : #9275 fermé « Improve gateway.bind
  validation error messages and auth enforcement » ; #8823 fermé « CLI RPC probe
  hardcodes ws://127.0.0.1 when gateway.bind is lan » ; #50607 fermé « CLI
  management commands fail when gateway.bind=tailnet » ; #24011 fermé
  « sessions_spawn broken with bind=tailnet » ; #49253 fermé « Feature request:
  grant operator scopes to token-authenticated non-loopback connections » ; #50630
  fermé « Tailscale serve + auth.mode=none exposes gateway ».
- `gitcrawl search issues "gateway discovery Bonjour DNS-SD MagicDNS" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné 0 résultats.
- `gitcrawl search issues "gateway ssh tunnel remote" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné 20 résultats. Résultats notables : #26250 ouvert « SSH transport security
  check rejects connection before tunnel is established » ; #47342 ouvert « Node
  host: no SSH transport support + challenge auth fails behind reverse proxy » ;
  #69135 ouvert « `gateway probe`: false positive multiple reachable gateways when
  SSH tunnel + remote.url hit the same gateway » ; #3296 fermé « Node frequently
  disconnects when connected via SSH tunnel over Tailscale » ; #21227 fermé
  « nodes tool: SECURITY ERROR blocks ws:// LAN gateway ».
- `gitcrawl search issues "Tailscale Serve gateway remote" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné 20 résultats. Résultats notables : #84959 fermé « Node pairing fails over
  Tailscale Serve » ; #54008 fermé « WebSocket upgrade fails via Tailscale Serve
  HTTPS proxy » ; #14561 fermé « Device pairing: pending requests not created for
  Control UI via Tailscale Serve » ; #55218 fermé « Control UI throws missing
  scope ... over Tailscale Serve » ; #42931 fermé « Remote Control UI over
  Tailscale stays stuck on pairing required ».
- `gitcrawl search issues "tlsFingerprint" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné 6 résultats : #66279 ouvert « TUI fails against local TLS gateway unless
  Node TLS verification is disabled » ; #41740 ouvert « discord exec approvals fails
  against local self-signed TLS gateway » ; #68438 fermé « Android node: TLS
  fingerprint mismatch after certificate renewal » ; #50642 fermé « macOS node
  auto-trusts first TLS certificate » ; #15906 fermé « Remote Code Execution via
  Rogue Gateway Impersonation ».
- `gitcrawl search issues "gateway.remote.tlsFingerprint" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné 2 résultats : #50642 fermé et #15906 fermé.
- `gitcrawl search prs "gateway remote tls fingerprint" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné 12 PRs, incluant #80204 ouvert « propagate gateway TLS fingerprints to
  bootstrap clients », #58378 ouvert « macOS: confirm discovered gateway trust »,
  #75228 ouvert « auto-repair stale gateway TLS pins », et plusieurs PRs fermées de
  renforcement ou de réparation.
- `gitcrawl search prs "gateway discovery tailscale serve" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné 6 PRs, incluant #40167 fermée « improve tailscale gateway discovery »
  et #32860 fermée « add tailscale serve discovery fallback for remote gateways ».
- `gitcrawl search prs "gateway bind remote" -R openclaw/openclaw --state all --json number,title,state,url`
  a retourné 20 PRs, incluant #81981 fermée « Policy: add gateway exposure
  checks », #2035 fermée « add gateway network exposure security check », #19057
  fermée « use loopback for local CLI connections when bind=lan », et #6715
  fermée « add SSH tunnel example for loopback-bound gateway ».

### Rapports discrawl

Les recherches d'archives Discord spécifiques aux fonctionnalités ont trouvé des conseils d'opérateurs actuels et des discussions récentes de mainteneurs :

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway remote"`
  a retourné 10 résultats. Les résultats pertinents incluaient une discussion mainteneurs/onboarding du 2026-05-21 décrivant la configuration Gateway locale par rapport à distante, WS direct et tunnel SSH ; une note de mainteneur du 2026-05-21 pour revérifier une PR avec configuration Gateway distante ; et des rapports d'aide utilisateur sur les défaillances de capacité navigateur/nœud distant après mise à jour.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway bind tailnet lan loopback"`
  a retourné 10 résultats. Les résultats pertinents incluaient des conseils du 2026-04-22 expliquant l'exposition loopback par rapport à non-loopback, une confusion utilisateur du 2026-04-16 sur `gateway.bind` invalide, et des conseils du 2026-04-14 orientant les utilisateurs vers loopback sauf s'ils ont explicitement besoin d'exposition tailnet/LAN.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway discovery bonjour dns-sd magicdns"`
  a retourné 1 résultat, un message de conseils Android du 2026-02-17 indiquant que la découverte ne fonctionne pas sur les réseaux sauf si DNS-SD unicast/Bonjour large zone est configuré.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway ssh tunnel remote"`
  a retourné 10 résultats. Les résultats pertinents incluaient une discussion du 2026-04-20 sur #69135 où `gateway probe` voit à la fois le tunnel SSH et l'URL directe comme accessibles, plus des conseils de support utilisateur recommandant les tunnels SSH ou Tailscale au lieu d'exposition de port public.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway tls fingerprint pin"`
  a retourné 10 résultats. Les résultats pertinents incluaient une liste de contrôle de mainteneur du 2026-05-01 mettant en évidence la rotation d'empreinte TLS, les pins obsolètes et les courses challenge/startup ; des commentaires d'examen de PR sur le fallback de pin TLS distant et les pins TLS nouvellement sauvegardés ; et des conseils utilisateur pour utiliser WSS plus pinning d'empreinte optionnel.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Tailscale Serve gateway remote"`
  a retourné 10 résultats. Les résultats pertinents incluaient des conseils de support utilisateur répétés selon lesquels loopback plus Tailscale Serve ou SSH est la valeur par défaut sûre, des demandes de statut/dépannage Tailscale Serve, et des avertissements sur HTTP brut sur tailnet.

### Bonnes qualités

- Le code source a des types de configuration étroits et explicites pour les modes de liaison, les champs de transport distant et les empreintes TLS : `src/config/types.gateway.ts:3`,
  `src/config/types.gateway.ts:224`.
- La résolution de liaison Gateway est centralisée au lieu d'être dispersée dans les appelants : `src/gateway/net.ts:262`, `src/gateway/net.ts:333`.
- Les appels CLI locaux préfèrent délibérément loopback même lorsque la Gateway elle-même est liée à LAN/tailnet, réduisant l'auto-exposition accidentelle : `src/gateway/connection-details.ts:41`, `src/gateway/connection-details.ts:54`.
- Le `ws://` distant en texte brut est bloqué pour les hôtes non-privés avec des conseils d'opérateur exploitables : `src/gateway/connection-details.ts:70`,
  `src/gateway/client.ts:318`.
- La validation du pin TLS est appliquée dans le client WebSocket et vérifiée à nouveau après l'ouverture du socket : `src/gateway/client.ts:313`, `src/gateway/client.ts:348`,
  `src/gateway/client.ts:1179`.
- La publication de découverte porte des indices TLS, d'accessibilité directe, SSH et tailnet tout en gardant la découverte locale optionnelle : `src/gateway/server-discovery-runtime.ts:25`,
  `src/gateway/server-discovery-runtime.ts:40`,
  `src/gateway/server-discovery-runtime.ts:68`,
  `src/gateway/server-discovery-runtime.ts:146`.
- Les assistants de découverte macOS évitent le routage à partir d'indices TXT non authentifiés et préfèrent les points de terminaison de service résolus : `apps/macos/Sources/OpenClaw/GatewayDiscoveryHelpers.swift:41`,
  `apps/macos/Sources/OpenClaw/GatewayDiscoveryHelpers.swift:53`.

### Mauvaises qualités

- L'historique d'archive est dense avec des régressions autour de loopback codé en dur, bind=tailnet, comportement de sonde distant, Tailscale Serve, détection de tunnel SSH et propagation de pin TLS. Cela réduit la qualité même si de nombreux problèmes ont des PRs de réparation.
- Plusieurs éléments GitHub actifs restent ouverts sur la même surface : #65355, #40527, #26250, #47342, #69135, #66279, #41740, #80204, #58378, #75228.
- Les problèmes ouverts décrivent des lacunes opérationnelles dans le comportement de sonde distant, le support de transport SSH, la détection de tunnel/direct dupliquée, la compatibilité TLS locale et la propagation d'empreinte TLS.
- La logique de sélection de transport est divisée entre le code Gateway/CLI TypeScript, le code d'application Swift macOS, le code client iOS/Android et la documentation. Les pièces importantes sont présentes, mais la cohérence entre clients est facile à régresser.

## Lacunes connues

- Le support de transport SSH du nœud-hôte est explicitement signalé comme manquant dans le problème ouvert #47342, même si le fallback SSH existe pour les flux macOS/opérateur.
- `gateway probe` peut toujours confondre une Gateway logique atteinte à la fois par tunnel et URL directe selon le problème ouvert #69135.
- Les budgets de sonde distant/non-loopback ont un rapport de faux négatif ouvert (#65355).
- La propagation TLS locale et TLS auto-signé client ont toujours des rapports/PRs ouverts (#66279, #41740, #80204).
- #49253 a demandé des portées d'opérateur pour les connexions non-loopback authentifiées par jeton.
- #12506 demande un système de profil de sécurité unifié avec des scénarios prédéfinis.
- Les mainteneurs Discord le 2026-05-01 ont appelé à un timing challenge/nonce, une rotation de jeton, une rotation d'empreinte TLS et un renforcement de la course auth-startup au démarrage sur les scénarios Gateway distant.

## Preuves

### Docs

- `docs/gateway/remote.md:8` explique l'accès à la passerelle distante comme une passerelle sur un hôte dédié avec des clients s'y connectant.
- `docs/gateway/remote.md:15` documente la valeur par défaut de loopback et l'exposition distante via Tailscale Serve, la liaison LAN/tailnet de confiance, ou SSH.
- `docs/gateway/remote.md:67` documente la commande de tunnel SSH et comment la santé et le statut atteignent la passerelle distante via le transfert de loopback.
- `docs/gateway/remote.md:88` documente `gateway.mode="remote"` et `gateway.remote.url` persistants.
- `docs/gateway/remote.md:104` distingue l'URL locale du tunnel SSH du `gateway.remote.sshTarget` découvert.
- `docs/gateway/remote.md:157` documente les règles de sécurité pour loopback, les liaisons LAN/tailnet/personnalisées, `wss://` public, et l'épinglage TLS distant.
- `docs/gateway/discovery.md:43` documente les entrées de découverte Bonjour/DNS-SD.
- `docs/gateway/discovery.md:62` énumère les clés TXT de balise incluant `gatewayTlsSha256`, `tailnetDns`, et `sshPort`.
- `docs/gateway/discovery.md:79` indique que les valeurs TXT ne sont pas authentifiées et ne doivent pas remplacer les épingles TLS stockées.
- `docs/gateway/discovery.md:124` documente l'ordre de sélection du transport client préféré.
- `docs/gateway/configuration-reference.md:522` documente le `mode` de passerelle, `port`, `bind`, les exigences d'authentification non-loopback, le mode Tailscale, le transport distant, et TLS.
- `docs/gateway/protocol.md:680` documente l'authentification Tailscale Serve/trusted-proxy.
- `docs/gateway/protocol.md:803` documente TLS et l'épinglage optionnel.

### Source

- `src/config/types.gateway.ts:3` définit les modes de liaison.
- `src/config/types.gateway.ts:224` définit l'URL `gateway.remote`, le transport, remotePort, l'authentification, l'empreinte TLS, et les champs SSH.
- `src/gateway/net.ts:262` résout l'hôte de liaison pour loopback, tailnet, LAN, personnalisé, et auto.
- `src/gateway/net.ts:333` force loopback par défaut quand Tailscale Serve/Funnel est actif.
- `src/gateway/connection-details.ts:21` construit les détails de connexion et les étiquettes de source.
- `src/gateway/connection-details.ts:70` rejette le WS en texte brut distant non sécurisé sauf si l'échappatoire du réseau privé est activée.
- `src/gateway/call.ts:464` résout le contexte d'appel de passerelle à partir des entrées d'URL CLI/env/config.
- `src/gateway/call.ts:547` résout la précédence de l'empreinte TLS.
- `src/gateway/client.ts:313` rejette les empreintes TLS avec des URL non-WSS.
- `src/gateway/client.ts:348` installe la vérification de l'empreinte du certificat.
- `src/gateway/server-discovery-runtime.ts:25` démarre la découverte locale et étendue avec le contexte TLS/direct/SSH/tailnet.
- `apps/macos/Sources/OpenClaw/GatewayRemoteConfig.swift:46` résout le transport direct par rapport à SSH.
- `apps/macos/Sources/OpenClaw/RemotePortTunnel.swift:68` crée un transfert de port local SSH.
- `apps/macos/Sources/OpenClawDiscovery/GatewayDiscoveryModel.swift:99` démarre la découverte Bonjour/étendue/Tailscale Serve.
- `apps/macos/Sources/OpenClaw/GatewayDiscoveryHelpers.swift:53` évite le routage à partir d'indices TXT non authentifiés.

### Tests d'intégration

- `src/gateway/server.auth.browser-hardening.test.ts:109` utilise les aides du serveur WebSocket de passerelle réelle pour tester les connexions trusted-proxy d'origine du navigateur.
- `src/gateway/server.auth.browser-hardening.test.ts:217` teste les origines de navigateur autorisées et non autorisées par rapport à un serveur de passerelle en cours d'exécution.
- `src/gateway/server.auth.control-ui.suite.ts:954` ouvre une connexion WS de style Tailscale dans un flux d'authentification Control UI.
- `src/gateway/server-network-runtime.e2e.test.ts:68` démarre un serveur de passerelle dans un test de runtime réseau.

### Tests unitaires

- `src/gateway/net.test.ts:668` couvre la résolution de l'hôte de liaison.
- `src/gateway/call.test.ts:490` couvre le comportement de remplacement d'URL distante env.
- `src/gateway/call.test.ts:537` couvre le transfert d'empreinte TLS distant.
- `src/gateway/call.test.ts:750` couvre les étiquettes de source de détails de connexion, les notes de secours, la sélection d'URL distante, et le comportement WS privé/texte brut.
- `src/gateway/server-discovery-runtime.test.ts:85` couvre le contexte d'annonce de découverte.
- `src/gateway/server-discovery-runtime.test.ts:215` couvre DNS-SD étendu quand la découverte locale est désactivée.
- `src/infra/tls/gateway.test.ts:79` couvre le chargement du certificat TLS/clé/empreinte.
- `src/infra/tailscale.test.ts:62` couvre l'analyse de MagicDNS.
- `apps/macos/Tests/OpenClawIPCTests/GatewayDiscoveryHelpersTests.swift:72` couvre la construction d'URL directe et le rejet de texte brut public.
- `apps/ios/Tests/GatewayConnectionSecurityTests.swift:39` couvre le comportement de confiance d'épingle TLS découvert.

### Requêtes gitcrawl

Les commandes exactes suivantes ont été exécutées :

```bash
gitcrawl doctor --json
gitcrawl search issues "gateway remote" -R openclaw/openclaw --state all --json number,title,state,url | jq -c '{count:length, results:.}'
gitcrawl search issues "gateway bind tailnet lan loopback" -R openclaw/openclaw --state all --json number,title,state,url | jq -c '{count:length, results:.}'
gitcrawl search issues "gateway discovery Bonjour DNS-SD MagicDNS" -R openclaw/openclaw --state all --json number,title,state,url | jq -c '{count:length, results:.}'
gitcrawl search issues "gateway ssh tunnel remote" -R openclaw/openclaw --state all --json number,title,state,url | jq -c '{count:length, results:.}'
gitcrawl search issues "Tailscale Serve gateway remote" -R openclaw/openclaw --state all --json number,title,state,url | jq -c '{count:length, results:.}'
gitcrawl search issues "tlsFingerprint" -R openclaw/openclaw --state all --json number,title,state,url | jq -c '{count:length, results:.}'
gitcrawl search issues "gateway.remote.tlsFingerprint" -R openclaw/openclaw --state all --json number,title,state,url | jq -c '{count:length, results:.}'
gitcrawl search prs "gateway remote tls fingerprint" -R openclaw/openclaw --state all --json number,title,state,url | jq -c '{count:length, results:.}'
gitcrawl search prs "gateway discovery tailscale serve" -R openclaw/openclaw --state all --json number,title,state,url | jq -c '{count:length, results:.}'
gitcrawl search prs "gateway bind remote" -R openclaw/openclaw --state all --json number,title,state,url | jq -c '{count:length, results:.}'
```

Les résultats sont résumés sous « Qualité / rapports gitcrawl » ci-dessus. Une requête plus large `gitcrawl search issues "gateway tls fingerprint" ...` a été interrompue après qu'elle n'ait produit aucune sortie pendant plus de 20 secondes ; les recherches plus étroites `tlsFingerprint` et `gateway.remote.tlsFingerprint` ont retourné rapidement et constituent la preuve de requête TLS pour cette note.

### Requêtes discrawl

Les commandes exactes suivantes ont été exécutées :

```bash
discrawl status --json
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway remote"
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway bind tailnet lan loopback"
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway discovery bonjour dns-sd magicdns"
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway ssh tunnel remote"
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway tls fingerprint pin"
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Tailscale Serve gateway remote"
```

Les résultats sont résumés sous « Qualité / rapports discrawl » ci-dessus. Les nombres de résultats de recherche étaient respectivement 10, 10, 1, 10, 10, et 10.
