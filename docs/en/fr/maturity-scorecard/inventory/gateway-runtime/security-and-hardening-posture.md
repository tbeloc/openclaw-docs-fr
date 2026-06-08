---
title: Gateway Runtime and WebSocket Feature Note - Security Controls
version: 3
last_refreshed: 2026-05-29
last_refreshed_by: codex
feature_family: Security controls
feature_slug: security-and-hardening-posture
---

# Contrôles de sécurité

## Résumé

Couverture : 84/100, Oui. Qualité : 74/100, Moyen.

La posture de sécurité Gateway/WebSocket est implémentée dans la documentation, la politique d'authentification du runtime, l'application de la poignée de main WebSocket, les vérifications de proxy de confiance, l'appairage des appareils et des nœuds, les garde-fous de portée de diffusion, la liaison d'approbation d'exécution de nœud distant et le renforcement du relais de contrôle de navigateur. La couverture est Oui car plusieurs tests réels de flux Gateway/serveur exercent la politique d'origine du navigateur, les exceptions de proxy de confiance, l'authentification de style Tailscale, les défaillances de protocole d'authentification, l'approbation automatique de nœud CIDR de confiance, la liaison d'approbation node.invoke et l'authentification HTTP de contrôle de navigateur.

La qualité reste Moyen. L'implémentation actuelle présente des signaux de renforcement solides, mais l'historique des archives montre des régressions graves répétées autour des limites de proxy de confiance, l'exposition auth.mode=none, l'authentification de contrôle de navigateur, l'approbation d'appairage de nœud, la confiance de passerelle malveillante et les contournements d'approbation node.invoke. Les lacunes de couverture uniquement restent pour la preuve de topologie renforcée, la preuve d'épinglage TLS, la preuve de flux serveur d'événement inconnu et la preuve de relais de contrôle de navigateur distant ; les lacunes de produit et opérationnelles restent autour de la séparation d'identité de service, des contrôles de refus dur d'exécution supplémentaires, des pièges d'ingestion privée et de la clarté de configuration à distance.

## Fonctionnalités

- Authentification non-loopback : Exposition non-loopback requérant l'authentification.
- Exceptions de proxy de confiance : Exceptions d'authentification d'appareil de proxy de confiance et plan de contrôle.
- Limites de confiance Gateway et nœud : Définition du domaine de confiance Gateway/nœud.
- Approbation automatique CIDR de confiance : Limites CIDR de confiance pour l'approbation automatique de nœud.
- Gestion de protocole en cas d'échec fermé : Comportement en cas d'échec rapide/fermé pour les violations de protocole et les familles d'événements inconnues.
- Garanties d'exécution à distance : Posture de sécurité autour de l'exécution de nœud distant et du relais de contrôle de navigateur.

## Fraîcheur des archives

- `gitcrawl doctor --json`: `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, `repository_count=2`.
- `discrawl status --json`: `generated_at=2026-05-30T00:04:12Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Couverture

Score : 84/100.

Étiquette : Oui.

### Signaux positifs

- La documentation de sécurité définit explicitement la limite de confiance Gateway/nœud, le risque d'exécution à distance, l'appairage d'appareil par rapport aux limites d'authentification, les limites CIDR de confiance et la sensibilité du contrôle de navigateur (`docs/gateway/security/index.md:166`, `docs/gateway/security/index.md:193`, `docs/gateway/security/index.md:214`, `docs/gateway/security/index.md:494`, `docs/gateway/security/index.md:1208`).
- La documentation d'exposition réseau couvre la valeur par défaut loopback, le risque non-loopback, les règles de proxy inverse et de proxy de confiance, les limites d'identité Tailscale Serve et l'évitement d'ingestion publique (`docs/gateway/security/index.md:429`, `docs/gateway/security/index.md:473`, `docs/gateway/security/index.md:821`, `docs/gateway/security/index.md:927`, `docs/gateway/security/index.md:986`, `docs/gateway/security/index.md:1025`).
- La documentation de protocole couvre les modes d'authentification, les exceptions sans appareil, les limites de nouvelle tentative de point de terminaison de confiance, la liaison d'approbation d'exécution et les familles d'événements inconnues échouant fermées lors de l'évaluation de la portée de diffusion (`docs/gateway/protocol.md:315`, `docs/gateway/protocol.md:621`, `docs/gateway/protocol.md:676`, `docs/gateway/protocol.md:704`, `docs/gateway/protocol.md:748`).
- L'authentification du runtime applique une configuration d'authentification explicite, rejette les combinaisons de jeton/mot de passe invalides, nécessite la validation de la source du proxy de confiance, rejette les sources de proxy de confiance loopback sauf si elles sont explicitement acceptées et sérialise les défaillances d'authentification d'origine du navigateur (`src/gateway/startup-auth.ts:125`, `src/gateway/auth-mode-policy.ts:21`, `src/gateway/auth.ts:222`, `src/gateway/auth.ts:270`, `src/gateway/auth.ts:400`).
- Le code de poignée de main WebSocket échoue fermé pour les charges utiles de pré-authentification malformées, les demandes non-connect en premier, les incompatibilités de protocole, l'incompatibilité d'origine du navigateur, l'identité d'appareil manquante ou invalide et les appels non autorisés (`src/gateway/server/ws-connection/message-handler.ts:480`, `src/gateway/server/ws-connection/message-handler.ts:523`, `src/gateway/server/ws-connection/message-handler.ts:614`, `src/gateway/server/ws-connection/message-handler.ts:670`, `src/gateway/server/ws-connection/message-handler.ts:805`, `src/gateway/server/ws-connection/message-handler.ts:879`, `src/gateway/server/ws-connection/message-handler.ts:997`, `src/gateway/server/ws-connection/message-handler.ts:1941`).
- Les tests réels de flux Gateway/serveur couvrent les origines du navigateur de proxy de confiance, l'effacement de la portée de l'interface utilisateur de contrôle non-Control, les listes blanches d'origine du navigateur, les limites de taux d'échec d'authentification à distance, l'appairage automatique de l'interface utilisateur de contrôle local, l'authentification de style Tailscale, le comportement de fermeture d'incompatibilité de protocole, les paramètres de connexion invalides, le rejet de nonce manquant, l'approbation automatique de nœud CIDR de confiance, la liaison d'approbation node.invoke et le comportement d'échec fermé d'authentification de contrôle de navigateur (`src/gateway/server.auth.browser-hardening.test.ts:152`, `src/gateway/server.auth.browser-hardening.test.ts:177`, `src/gateway/server.auth.browser-hardening.test.ts:217`, `src/gateway/server.auth.browser-hardening.test.ts:283`, `src/gateway/server.auth.browser-hardening.test.ts:427`, `src/gateway/server.auth.modes.suite.ts:181`, `src/gateway/server.auth.default-token.suite.ts:418`, `src/gateway/server.auth.default-token.suite.ts:481`, `src/gateway/server.auth.default-token.suite.ts:524`, `src/gateway/server.node-pairing-auto-approve.test.ts:122`, `src/gateway/server.node-invoke-approval-bypass.test.ts:503`, `extensions/browser/src/browser/server.auth-fail-closed.test.ts:94`).

### Signaux négatifs

- La couverture de flux réel la plus forte est la couverture de flux serveur local. Je n'ai pas trouvé un seul test de topologie renforcée en direct ou e2e qui prouve le proxy inverse, Tailscale Serve, tailnet, LAN, ingestion publique, épinglage TLS et authentification d'appareil/nœud ensemble.
- `auth.mode=none` reste un mode d'ingestion privée explicite. Le produit avertit et documente le risque, mais l'exposition non-loopback n'est pas un échec dur de démarrage universel car les déploiements privés sont intentionnellement pris en charge (`src/gateway/auth.ts:504`, `docs/gateway/protocol.md:676`).
- Les familles d'événements de diffusion inconnues échouent fermées dans une surface d'unité ciblée, mais je n'ai pas trouvé un test d'intégration WebSocket/serveur réel qui envoie une famille d'événements inconnue via le chemin de diffusion (`src/gateway/server-broadcast.ts:62`, `src/gateway/gateway-misc.test.ts:461`).
- L'approbation automatique CIDR de confiance a de bons tests directs, mais le chemin heureux d'intégration est conditionnel à une auto-connexion non-loopback disponible dans l'environnement d'exécution (`src/gateway/server.node-pairing-auto-approve.test.ts:122`).
- Les résultats des archives montrent plusieurs régressions historiques de haute gravité dans ce domaine, notamment auth.mode=none sur Tailscale Serve, les lacunes d'authentification de contrôle de navigateur, l'appairage de nœud avant approbation, la confiance de passerelle malveillante et les contournements d'approbation node.invoke.

### Lacunes d'intégration

- Ajouter une preuve de topologie renforcée réelle pour le proxy inverse et Tailscale Serve qui exerce l'authentification, les origines autorisées, la confiance d'en-tête transféré, l'identité d'appareil et le comportement de mise à niveau WebSocket contre une Gateway réelle.
- Ajouter une preuve d'ingestion publique ou d'ingestion hostile simulée qui montre que l'authentification non autorisée ou mal configurée échoue fermée sans s'appuyer uniquement sur la documentation ou les avertissements de démarrage.
- Ajouter une preuve d'empreinte digitale WSS/TLS distante qui couvre la première confiance, l'épingle obsolète et le rejet de passerelle malveillante pour le même itinéraire utilisé par les nœuds ou clients distants.
- Ajouter un test d'intégration pour le comportement de refus de famille d'événements inconnue via le chemin de diffusion du serveur, pas seulement l'assistant de portée d'événement.
- Ajouter une voie d'intégration CIDR de confiance non-conditionnelle ou une preuve Testbox/Crabbox pour l'approbation automatique de nœud non-loopback réelle.

## Qualité

Score: 74/100.

Label: Moyen.

### Rapports gitcrawl

- `gateway auth non-loopback trusted proxy` a retourné 16 résultats de problèmes. Résultats notables : #69066 ouvert "[RFC] Separate internal service identity from user auth in OpenClaw gateway"; #50630 fermé "Tailscale serve + auth.mode=none exposes gateway to full Tailnet without authentication"; #50628 fermé "Browser control server installs no authentication when gateway auth mode is trusted-proxy"; #50644 fermé "gateway.auth.mode=none propagates silently to browser control server"; #82607 fermé trusted-proxy loopback fallback bug.
- `gateway trusted cidr node pairing auto approve` a retourné 0 résultats de problèmes. La requête plus spécifique `autoApproveCidrs` a retourné #72857 fermé "PR #22280 Regression: scope upgrade still requires pairing on 2026.4.25 (VPS/lan bind)".
- `trusted CIDR node pairing` a retourné #84447 ouvert "[Feature]: Per-sender inbound DM rate limit for channel pairing/allowlist policies", qui est un travail adjacent de politique/limite de débit plutôt qu'un bug direct de trusted-CIDR.
- `gateway protocol unknown event fail closed` a retourné #74632 ouvert "Add per-session envelope to sessions.create / sessions.patch", qui est un travail adjacent de forme de protocole, pas un rapport de sécurité direct d'événement inconnu.
- `browser control gateway auth trusted proxy node proxy security` a retourné 7 résultats de problèmes. Résultats notables : #50644 fermé exposition d'API browser-control non authentifiée; #30092 fermé comportement device-required de l'interface utilisateur de contrôle derrière un proxy inverse HTTPS local; #41047 fermé problème de livraison de jeton de l'interface utilisateur de contrôle du tableau de bord; #66983 ouvert support de nœud de toile web.
- `node.invoke system.run approval bypass` a retourné 3 résultats de problèmes fermés : #65542 "Device pairing alone exposes exec-capable nodes before admin node approval"; #65168 "node.invoke stays reachable before node pairing approval exists"; #50642 "macOS node auto-trusts first TLS certificate and accepts rogue gateway control".
- `gateway auth non-loopback trusted proxy browser control security` la recherche de PR a retourné 13 PR, y compris les PR de durcissement fermées #20686, #61004, #63379, #64122, #65639, #79643, et #58812.
- `node invoke approval bypass system.run` la recherche de PR a retourné 18 PR, y compris les PR de durcissement fermées #8683, #10129, #24682, #24826, #25733, #25749, #65169, #65543, #79781, et ouvert #81827 "add tools.exec.denyPathPatterns hard-deny gate (#74379)".

### Rapports discrawl

- `gateway auth non-loopback trusted proxy` a retourné des discussions récentes de support et d'examen autour de loopback par rapport aux liaisons LAN/tailnet/personnalisées, token/password par rapport au mode trusted-proxy, guidance Tailscale Serve, comportement du proxy inverse sur le même hôte, `NODE_EXTRA_CA_CERTS`, et PR #59190 durcissement trusted-proxy loopback.
- `auth.mode=none exposes gateway` a retourné le cluster d'incident #50630/#50631 : Tailscale Serve plus `auth.mode=none` a été décrit comme un risque d'exposition complète du Tailnet et l'examen a demandé aux chemins de configuration/installation de rejeter la combinaison dangereuse.
- `trusted CIDR node pairing auto approve` a retourné le fil d'implémentation #61004 plus des preuves d'examen que le changement avait une portée étroite et un examen P1 a détecté le risque d'auto-approbation de re-pair pour les ID d'appareil existants.
- `browser control auth gateway trusted proxy` a retourné le cluster de durcissement #63280/#65639 : génération de jeton d'authentification browser-control pour les modes none/trusted-proxy, démarrage fail-closed lorsque l'amorçage d'authentification est manquant, vérifications d'origine, et discussion que 45+ routes browser-control avaient été accessibles aux appelants loopback/SSRF.
- `node invoke system run approval bypass` a retourné des discussions de support montrant que la couche de commande de nœud achemine intentionnellement via `system.run.prepare` et liaison d'approbation, y compris les frictions visibles par l'utilisateur autour des commandes d'interpréteur en ligne et des commandes autorisées.
- `node.invoke system.run approval bypass` n'a retourné aucun résultat Discrawl visible; la requête adjacente sans point ci-dessus était nécessaire pour capturer la discussion pertinente.
- `unknown event fail closed gateway protocol` n'a retourné aucun résultat Discrawl visible. Les requêtes adjacentes ont trouvé des discussions de non-concordance de protocole et de violation de politique 1008 mais pas un rapport direct de fail-closed d'événement inconnu.
- `unknown gateway event protocol` a retourné une discussion de mise à niveau bêta où une sonde de redémarrage a utilisé le protocole WebSocket 3 contre une Gateway de protocole 4, plus un rapport utilisateur séparé sur les champs d'événement manquants et la fuite de jeton d'appel brut.
- `gateway protocol invalid message close 1008` a retourné des conseils de support indiquant que 1008 signifie une fermeture intentionnelle de violation de politique pour les défaillances d'authentification, d'origine, de protocole, de limite de débit ou de message invalide.

### Bonnes qualités

- La configuration d'authentification est fail-closed pour les jetons/mots de passe manquants et la configuration de mode mixte invalide, tandis que le mode jeton peut générer un jeton de démarrage au lieu d'accepter silencieusement l'accès non authentifié (`src/gateway/startup-auth.ts:125`, `src/gateway/auth-mode-policy.ts:21`, `src/gateway/auth.ts:222`).
- L'authentification trusted-proxy distingue les adresses IP sources de confiance, les exceptions de source loopback, les sources d'interface locale, les en-têtes d'identité requis et les utilisateurs autorisés (`src/gateway/auth.ts:270`, `src/gateway/auth.ts:454`).
- Les en-têtes transférés à partir d'adresses non fiables ne créent pas de confiance locale, ce qui protège les raccourcis loopback uniquement derrière les proxies (`src/gateway/server/ws-connection/message-handler.ts:411`).
- L'auto-approbation de nœud est étroite : désactivée sauf si des CIDR explicites sont configurés, seules les demandes de rôle=nœud fraîches non appairées sans portées demandées sont éligibles, et les cas de navigateur, interface utilisateur de contrôle, WebChat, trusted-proxy loopback, IP manquante et mise à niveau sont rejetés (`src/gateway/node-pairing-auto-approve.ts:30`).
- L'éventail d'événements utilise des gardes allow-by-scope et refuse les familles d'événements inconnues par défaut (`src/gateway/server-broadcast.ts:18`, `src/gateway/server-broadcast.ts:62`).
- `node.invoke` supprime ou bloque les mutations d'approbation et browser.proxy fournies par l'appelant avant le transfert, et la validation d'approbation system.run lie le contexte exact d'exécution, de nœud, de commande, de répertoire de travail, d'agent et de session (`src/gateway/server-methods/nodes.ts:1046`, `src/gateway/node-invoke-system-run-approval.ts:214`, `src/gateway/node-invoke-system-run-approval.ts:257`, `src/gateway/node-invoke-system-run-approval.ts:340`).
- Le contrôle du navigateur dispose d'assistants d'authentification à secret partagé, de démarrage de pont fail-closed, de blocs de mutation de profil persistant, de protections SSRF et de conclusions d'audit de sécurité pour les routes browser-control non authentifiées (`extensions/browser/src/browser/http-auth.ts:40`, `extensions/browser/src/browser/bridge-server.ts:78`, `extensions/browser/src/gateway/browser-request.ts:147`, `extensions/browser/src/node-host/invoke-browser.ts:223`, `extensions/browser/src/security-audit.ts:68`).

### Mauvaises qualités

- La politique de sécurité est intentionnellement large et transversale. La correction dépend de la configuration d'authentification, de la politique de connexion WebSocket, de l'authentification d'appareil, de la confiance d'en-tête trusted-proxy, des vérifications d'origine du navigateur, de l'appairage de nœud, de la portée de diffusion, du transfert d'invocation de nœud et du code du plugin de contrôle du navigateur restant alignés.
- L'historique d'archive contient plusieurs régressions fermées graves, donc la famille de fonctionnalités a une tendance démontrée à régresser aux limites entre trusted proxy, ingress privé, contrôle du navigateur, appairage de nœud et exécution à distance.
- `auth.mode=none` reste un piège puissant pour les opérateurs pour les déploiements privés non-loopback. La documentation met en garde contre l'exposition publique, mais le runtime le supporte comme un contrat d'ingress privé.
- Le durcissement du contrôle du navigateur est divisé entre le transfert Gateway principal et l'hôte du plugin du navigateur. Cette division est raisonnable pour la propriété, mais elle augmente le coût pour l'opérateur et le mainteneur de maintenir l'authentification, SSRF, mutation de profil et politique de commande de nœud alignées sur les deux surfaces.
- L'identité du service et l'authentification de l'utilisateur sont toujours suffisamment couplées pour que #69066 reste ouvert, et #81827 montre que les contrôles de hard-deny d'exécution supplémentaires attendus n'ont pas encore été déployés.
- Les fils de support Discrawl montrent une friction récurrente de l'opérateur autour de la configuration de Gateway à distance, de la sélection du mode trusted-proxy, de la guidance Tailscale Serve et du comportement d'approbation de commande de nœud.

## Lacunes connues

### Capacités implémentées dans la portée

- L'exposition non-loopback requise par authentification est documentée et largement appliquée par la génération d'authentification de démarrage, les modes d'authentification explicites, le blocage côté client de WS distant non sécurisé, les vérifications d'origine autorisée du navigateur et les avertissements non-loopback (`docs/gateway/security/index.md:821`, `docs/gateway/security/index.md:927`, `src/gateway/startup-auth.ts:125`, `src/gateway/client.ts:312`, `src/gateway/net.ts:474`, `src/gateway/server-runtime-state.ts:210`).
- Les exceptions d'authentification trusted-proxy et Control UI device-auth sont documentées et implémentées avec des vérifications de source/en-tête étroites et des conditions de break-glass explicites (`docs/gateway/trusted-proxy-auth.md:52`, `docs/gateway/trusted-proxy-auth.md:77`, `src/gateway/server/ws-connection/connect-policy.ts:37`, `src/gateway/server/ws-connection/connect-policy.ts:102`).
- Les définitions de domaine de confiance Gateway/nœud, les avertissements d'exécution à distance, la guidance de topologie, les limites de trusted-CIDR, le comportement de fail-fast du protocole, le durcissement de l'exécution de nœud à distance et le durcissement de relais de contrôle du navigateur sont documentés ou implémentés dans les surfaces docs/source citées.

### Lacunes de produit et opérationnelles

- Le runtime supporte `auth.mode=none` pour l'ingress privé; ceci est documenté, mais il reste un piège puissant pour les opérateurs pour les déploiements non-loopback.
- #69066 reste ouvert pour séparer l'identité du service interne de l'authentification de l'utilisateur dans OpenClaw Gateway.
- #81827 reste ouvert pour ajouter la porte hard-deny `tools.exec.denyPathPatterns`.
- #84447 est un travail adjacent de politique d'appairage/limite de débit, et #66983 ajouterait une autre surface de confiance navigateur/nœud si accepté.
- Les fils de support Discrawl montrent des demandes continues de l'opérateur pour une configuration de Gateway à distance plus claire, une sélection du mode trusted-proxy, une guidance Tailscale Serve et un comportement d'approbation de commande de nœud.

### Lacunes de couverture uniquement

- Aucune preuve complète de topologie à distance durcie en direct/e2e n'a été trouvée pour proxy inverse, Tailscale Serve, tailnet/LAN, simulation d'ingress public, épinglage TLS et authentification d'appareil/nœud ensemble.
- Le comportement de refus de famille d'événements inconnus manque de couverture de flux Gateway/serveur réel.
- La guidance de topologie à distance du contrôle du navigateur est forte, mais l'audit n'a pas trouvé une preuve complète de relais de nœud à distance/contrôle du navigateur qui combine l'authentification, l'appairage de nœud, l'authentification de route du navigateur, la politique SSRF et les contrôles de mutation de profil.

## Preuves

### Docs

- `docs/gateway/security/index.md:166` définit les domaines de confiance de la passerelle et des nœuds.
- `docs/gateway/security/index.md:193` résume les limites de sécurité de l'authentification de la passerelle, de l'appairage des nœuds, de la commande de nœud et du CIDR de confiance.
- `docs/gateway/security/index.md:214` documente l'approbation automatique du CIDR de confiance comme désactivée par défaut avec une admissibilité étroite.
- `docs/gateway/security/index.md:429` documente la confiance des en-têtes de proxy inverse et le comportement de fermeture en cas d'échec de la boucle de rétroaction du proxy de confiance.
- `docs/gateway/security/index.md:473` documente l'origine de l'interface utilisateur de contrôle non-loopback et le renforcement du rebinding DNS/hôte proxy.
- `docs/gateway/security/index.md:494` documente le nœud macOS appairé system.run comme exécution de code à distance et explique la liaison d'approbation.
- `docs/gateway/security/index.md:821` documente la valeur par défaut loopback et l'expansion de la surface d'attaque non-loopback.
- `docs/gateway/security/index.md:927` documente les valeurs par défaut d'authentification de la passerelle, l'authentification non résolue en fermeture en cas d'échec, et l'épingle TLS optionnelle.
- `docs/gateway/security/index.md:963` documente l'appairage des appareils locaux et les limites de localité des en-têtes transférés.
- `docs/gateway/security/index.md:986` documente les en-têtes d'identité Tailscale Serve et les compromis Serve sans jeton.
- `docs/gateway/security/index.md:1025` documente la configuration du proxy inverse de confiance.
- `docs/gateway/security/index.md:1033` documente les conseils de topologie de contrôle de navigateur à distance.
- `docs/gateway/security/index.md:1208` documente la sensibilité du profil de navigateur et les limites d'authentification du contrôle de navigateur.
- `docs/gateway/security/index.md:1225` documente la politique SSRF du navigateur.
- `docs/gateway/protocol.md:315` documente la limitation de la portée de diffusion et l'échec fermé des familles d'événements inconnues.
- `docs/gateway/protocol.md:621` documente la liaison d'approbation `systemRunPlan`.
- `docs/gateway/protocol.md:676` documente les modes d'authentification et les avertissements `none` d'ingestion privée.
- `docs/gateway/protocol.md:704` documente les limites des points de terminaison de confiance pour la nouvelle tentative de jeton d'appareil en cache.
- `docs/gateway/protocol.md:748` documente l'identité de l'appareil, l'appairage et les exceptions sans appareil.
- `docs/gateway/discovery.md:79` documente les indices de découverte non authentifiés et la priorité de l'épingle TLS.
- `docs/gateway/discovery.md:111` documente que les indices de découverte ne relâchent pas la sécurité du transport.
- `docs/gateway/trusted-proxy-auth.md:52` documente le comportement d'appairage du proxy de confiance de l'interface utilisateur de contrôle.
- `docs/gateway/trusted-proxy-auth.md:77` documente la configuration du proxy de confiance et les valeurs par défaut `allowLoopback=false`.
- `docs/gateway/pairing.md:125` documente l'approbation automatique des nœuds du CIDR de confiance.
- `docs/gateway/pairing.md:173` documente les limites de localité des en-têtes transférés.
- `docs/tools/browser-control.md:37` documente l'authentification par secret partagé du contrôle de navigateur et les limites loopback.
- `docs/tools/browser-control.md:360` documente la sensibilité du profil de navigateur et le risque CDP à distance.

### Source

- `src/gateway/startup-auth.ts:125` résout l'authentification au démarrage et génère ou rejette les identifiants.
- `src/gateway/auth-mode-policy.ts:21` rejette la configuration du jeton/mot de passe sans mode d'authentification explicite.
- `src/gateway/auth.ts:222` affirme que l'authentification est configurée.
- `src/gateway/auth.ts:270` autorise les demandes de proxy de confiance.
- `src/gateway/auth.ts:400` limite le taux d'échecs d'authentification de l'origine du navigateur.
- `src/gateway/auth.ts:454` résout l'authentification de connexion de la passerelle sur les chemins partagés, proxy de confiance et direct local.
- `src/gateway/auth.ts:504` implémente `auth.mode=none`.
- `src/gateway/server-runtime-state.ts:210` avertit sur la liaison non-loopback.
- `src/gateway/client.ts:312` bloque les URL WebSocket distantes non sécurisées.
- `src/gateway/net.ts:474` classe les URL WebSocket sécurisées.
- `src/gateway/server/ws-connection/message-handler.ts:411` rejette la localité des en-têtes transférés non fiables.
- `src/gateway/server/ws-connection/message-handler.ts:480` ferme sur les charges utiles pré-authentification surdimensionnées.
- `src/gateway/server/ws-connection/message-handler.ts:523` exige que la première trame soit `connect`.
- `src/gateway/server/ws-connection/message-handler.ts:614` ferme les incompatibilités de protocole.
- `src/gateway/server/ws-connection/message-handler.ts:670` applique la politique d'origine du navigateur.
- `src/gateway/server/ws-connection/message-handler.ts:805` applique la politique d'identité d'appareil manquante.
- `src/gateway/server/ws-connection/message-handler.ts:879` valide l'authentification d'appareil signée.
- `src/gateway/server/ws-connection/message-handler.ts:997` exige une authentification réussie avant la connexion.
- `src/gateway/server/ws-connection/message-handler.ts:1888` rejette les trames non-demande post-établissement de liaison.
- `src/gateway/server/ws-connection/message-handler.ts:1919` ferme les générations d'authentification partagée obsolètes.
- `src/gateway/server/ws-connection/message-handler.ts:1941` ferme les appels non autorisés répétés.
- `src/gateway/server/ws-connection/connect-policy.ts:37` limite les contournements d'appairage de l'interface utilisateur de contrôle.
- `src/gateway/server/ws-connection/connect-policy.ts:102` gère les exceptions et rejets d'identité d'appareil manquante.
- `src/gateway/node-pairing-auto-approve.ts:30` implémente l'admissibilité d'approbation automatique des nœuds du CIDR de confiance.
- `src/gateway/server-broadcast.ts:18` définit les gardes de portée d'événement.
- `src/gateway/server-broadcast.ts:62` refuse les familles d'événements inconnues.
- `src/gateway/server-broadcast.ts:144` filtre la livraison d'événements par portée client.
- `src/gateway/node-invoke-system-run-approval.ts:214` limite les drapeaux d'approbation fournis par l'appelant derrière un enregistrement d'approbation d'exécution réel.
- `src/gateway/node-invoke-system-run-approval.ts:257` valide l'existence, l'expiration et la liaison de nœud de l'approbation.
- `src/gateway/node-invoke-system-run-approval.ts:340` lie les approbations au contexte `systemRunPlan` canonique.
- `src/gateway/server-methods/nodes.ts:1046` rejette les charges utiles node.invoke malformées et interdites.
- `src/gateway/server-methods/nodes.ts:1180` applique les listes blanches de commandes de nœud et l'assainissement du transfert.
- `src/node-host/invoke-system-run.ts:547` rejette la dérive d'opérande de script/fichier mutable.
- `extensions/browser/src/browser/http-auth.ts:40` autorise les demandes HTTP de contrôle de navigateur avec authentification par jeton porteur ou mot de passe.
- `extensions/browser/src/browser/bridge-server.ts:78` exige l'authentification du serveur de pont et installe le middleware d'authentification du navigateur.
- `extensions/browser/src/gateway/browser-request.ts:147` bloque les méthodes de relais de navigateur invalides et la mutation de profil persistant.
- `extensions/browser/src/gateway/browser-request.ts:187` exige la permission de commande de nœud `browser.proxy`.
- `extensions/browser/src/node-host/invoke-browser.ts:223` bloque la mutation de profil persistant sur le chemin du navigateur du nœud-hôte.
- `extensions/browser/src/security-audit.ts:68` signale le contrôle du navigateur sans authentification.

### Tests d'intégration

- `src/gateway/server.auth.browser-hardening.test.ts:152` couvre la politique d'origine du navigateur du proxy de confiance.
- `src/gateway/server.auth.browser-hardening.test.ts:177` couvre les sessions de navigateur non-interface utilisateur de contrôle avec authentification du proxy de confiance effaçant les portées.
- `src/gateway/server.auth.browser-hardening.test.ts:217` couvre les listes blanches d'origine du navigateur.
- `src/gateway/server.auth.browser-hardening.test.ts:241` rejette les origines de navigateur non-locales et les revendications TUI d'origine du navigateur.
- `src/gateway/server.auth.browser-hardening.test.ts:283` limite le taux d'échecs d'authentification à distance.
- `src/gateway/server.auth.browser-hardening.test.ts:427` appaire automatiquement les clients de navigateur de l'interface utilisateur de contrôle local avec un jeton valide.
- `src/gateway/server.auth.modes.suite.ts:137` couvre la connexion loopback en mode authentification aucune.
- `src/gateway/server.auth.modes.suite.ts:181` couvre l'authentification Tailscale exigeant toujours l'identité de l'appareil.
- `src/gateway/server.auth.default-token.suite.ts:418` rejette les incompatibilités de protocole.
- `src/gateway/server.auth.default-token.suite.ts:470` rejette les demandes non-connexion en premier.
- `src/gateway/server.auth.default-token.suite.ts:481` exige un nonce pour l'authentification de l'appareil.
- `src/gateway/server.auth.default-token.suite.ts:524` rejette les paramètres de connexion invalides et ferme 1008.
- `src/gateway/server.node-pairing-auto-approve.test.ts:88` maintient les nœuds directs non-loopback manuels par défaut.
- `src/gateway/server.node-pairing-auto-approve.test.ts:122` couvre l'approbation automatique du CIDR de confiance des nœuds pour la première fois lorsqu'une auto-connexion non-loopback est disponible.
- `src/gateway/server.node-invoke-approval-bypass.test.ts:409` rejette les charges utiles node.invoke malformées et interdites avant le transfert.
- `src/gateway/server.node-invoke-approval-bypass.test.ts:470` rejette les mutations de profil persistant browser.proxy avant le transfert.
- `src/gateway/server.node-invoke-approval-bypass.test.ts:503` lie les approbations system.run à la décision et à l'appareil et supprime les champs injectés.
- `src/gateway/server.node-invoke-approval-bypass.test.ts:581` bloque les incompatibilités de relecture de reconnexion du backend.
- `extensions/browser/src/browser/server.auth-token-gates-http.test.ts:47` exige l'authentification du jeton porteur de la route de contrôle du navigateur.
- `extensions/browser/src/browser/server.auth-token-gates-http.test.ts:70` rejette les identifiants du mode d'authentification incorrect.
- `extensions/browser/src/browser/server.auth-fail-closed.test.ts:94` échoue fermé lorsque l'amorçage d'authentification du contrôle du navigateur échoue.

### Tests unitaires

- `src/gateway/client.test.ts:318` bloque les URL WebSocket en texte brut non-loopback.
- `src/gateway/call.test.ts:890` signale les erreurs d'URL de passerelle distante non sécurisée.
- `src/gateway/node-pairing-auto-approve.test.ts:68` prouve que l'approbation automatique est désactivée par défaut.
- `src/gateway/node-pairing-auto-approve.test.ts:78` couvre l'acceptation de correspondance CIDR/IP.
- `src/gateway/node-pairing-auto-approve.test.ts:102` couvre les cas de rejet du CIDR de confiance.
- `src/gateway/node-pairing-auto-approve.test.ts:147` rejette les tentatives de mise à niveau de rôle/portée et de métadonnées.
- `src/gateway/gateway-misc.test.ts:357` filtre les événements d'approbation et d'appairage par portée.
- `src/gateway/gateway-misc.test.ts:405` exige operator.read pour les événements de classe chat.
- `src/gateway/gateway-misc.test.ts:437` exige l'écriture/administration pour les événements de plugin.
- `src/gateway/gateway-misc.test.ts:461` refuse les événements inconnus par défaut.
- `src/gateway/gateway-misc.test.ts:534` préserve les numéros de séquence par client récepteur lorsque les événements délimités sont filtrés.
- `extensions/browser/src/node-host/invoke-browser.test.ts:390` couvre le rejet de mutation de profil persistant.
- `extensions/browser/src/security-audit.test.ts:28` signale les routes de contrôle du navigateur sans authentification.

### Requêtes gitcrawl

- Requête :
  `gitcrawl search issues 'gateway auth non-loopback trusted proxy' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 16 problèmes. Résultats directs ou adjacents notables : #26007 fermé demande de fonctionnalité trustedProxy.loopbackUser ; #82607 fermé bug de secours loopback proxy de confiance ; #50580 fermé échec d'authentification cron/outil proxy de confiance ; #69066 ouvert RFC d'identité de service interne ; #50630 fermé exposition Tailscale Serve plus auth none ; #71103 fermé bug d'appairage WS loopbackUser trustedProxies ; #50628 fermé contrôle de navigateur sans authentification sous proxy de confiance ; #50022 fermé contournement de suppression de portée d'origine manquante ; #82406 fermé ingestion Slack proxy de confiance ; #68403 fermé contournement de garde de secret faible ; #50644 fermé propagation auth none du contrôle de navigateur.
- Requête :
  `gitcrawl search issues 'gateway trusted cidr node pairing auto approve' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 0 problèmes.
- Requête :
  `gitcrawl search issues 'gateway protocol unknown event fail closed' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 1 problème, #74632 ouvert « Ajouter une enveloppe par session à sessions.create / sessions.patch » ; travail de protocole adjacent, pas un rapport d'événement inconnu direct.
- Requête :
  `gitcrawl search issues 'browser control gateway auth trusted proxy node proxy security' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 7 problèmes. Résultats notables : #30092 fermé comportement d'appareil requis du proxy inverse HTTPS local de l'interface utilisateur de contrôle ; #50644 fermé propagation sans authentification du contrôle de navigateur ; #66983 ouvert support de nœud de canevas web ; #41047 fermé problème de livraison de jeton du tableau de bord.
- Requête :
  `gitcrawl search issues 'node.invoke system.run approval bypass remote execution' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 3 problèmes fermés : #65542, #65168, #50642.
- Requête :
  `gitcrawl search issues 'autoApproveCidrs' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 1 problème fermé, #72857.
- Requête :
  `gitcrawl search issues 'trusted CIDR node pairing' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 1 problème ouvert, #84447, travail de politique d'appairage/limitation de taux adjacent.
- Requête :
  `gitcrawl search prs 'gateway auth non-loopback trusted proxy browser control security' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 13 RP. RP de renforcement fermés notables : #20686, #61004, #63379, #64122, #65639, #79643, #58812.
- Requête :
  `gitcrawl search prs 'node.invoke system.run approval bypass browser.proxy' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 0 RP.
- Requête :
  `gitcrawl search prs 'node invoke approval bypass system.run' -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20`
  Résultat : 18 RP. Résultats notables : #79781, #25733, #8683, #25749, #24826, #10129, #65169, #65543, #59182, #62439, #81827 ouvert, #24682, #81197, #65713, #62078, #78518.

### Requêtes discrawl

- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "gateway auth non-loopback trusted proxy"`
  Résultat : résultats de support et d'examen retournés sur loopback/local uniquement par rapport à LAN/tailnet/liaisons personnalisées, jeton/mot de passe par rapport au mode proxy de confiance, Tailscale Serve, Cloudflared, proxies inverses du même hôte, comportement de source loopback du proxy de confiance, `NODE_EXTRA_CA_CERTS`, et discussions RP #59190/#63379/#43820.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "auth.mode=none exposes gateway"`
  Résultat : cluster d'incident #50630/#50631 retourné et notes d'examen appelant Tailscale Serve plus `auth.mode=none` un risque d'exposition complète du tailnet.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "trusted CIDR node pairing auto approve"`
  Résultat : implémentation #61004 et discussion d'examen retournées, y compris une note de couverture au niveau de l'assistant et une préoccupation P1 concernant l'approbation automatique de ré-appairage.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "browser control auth gateway trusted proxy"`
  Résultat : discussion de renforcement du contrôle de navigateur #63280/#65639 retournée, y compris la génération de jeton d'authentification pour les modes aucun/proxy de confiance, démarrage en fermeture en cas d'échec, vérifications d'origine et préoccupations d'exposition de route de contrôle de navigateur.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "unknown event fail closed gateway protocol"`
  Résultat : aucun résultat visible.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "node.invoke system.run approval bypass"`
  Résultat : aucun résultat visible.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "node invoke system run approval bypass"`
  Résultat : threads de support retournés expliquant les routes `nodes run` via `system.run.prepare`, `exec.approval.request` et liaison d'approbation ; également capturé les frictions visibles par l'utilisateur autour des commandes d'interpréteur en ligne et des commandes en liste blanche invitant toujours.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "unknown gateway event protocol"`
  Résultat : discussions de non-concordance de protocole et de forme d'événement retournées, y compris une mise à niveau bêta où la sonde CLI protocole 3 a frappé une passerelle protocole 4 et un rapport utilisateur sur toolName manquant dans after_tool_call plus fuite de jeton d'appel brut.
- Requête :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 20 "gateway protocol invalid message close 1008"`
  Résultat : conseils de support retournés que 1008 est une fermeture intentionnelle de violation de politique pour l'authentification, l'origine, le protocole, la limitation de taux ou les échecs de message invalide.
