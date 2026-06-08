---
version: 3
---

# Authentification et appairage des appareils

## Résumé

Couverture : 88/100, Oui. Qualité : 72/100, Moyen.

La surface d'identité, d'authentification et d'appairage des appareils Gateway/WebSocket est implémentée dans les documents de protocole, les décisions d'authentification à l'exécution, les magasins d'appairage des appareils/nœuds, les jetons d'amorçage, le comportement de nouvelle tentative du client et les tests réels de Gateway/serveur. Le score de couverture est Oui car plusieurs tests d'intégration exercent des flux réels WebSocket/Gateway pour l'appairage local, le comportement du proxy de confiance de l'interface utilisateur de contrôle, l'amorçage du code de configuration, la réutilisation du jeton d'appareil, la rotation/révocation des jetons et l'appairage des nœuds.

La qualité reste Moyen. Le code actuel présente de nombreux signaux de renforcement positifs, mais l'historique des archives montre des régressions répétées autour de la priorité des jetons, de l'état des appareils obsolètes, de la suppression de la portée du proxy de confiance, des boucles d'appairage et de la sécurité des jetons d'amorçage. Les rapports ouverts demandent toujours la limitation du débit, les corrections des courses d'amorçage, les commandes de gestion d'appairage, la documentation du proxy de confiance, l'isolation des jetons multi-utilisateurs et les améliorations du cycle de vie mobile/nœud.

## Fonctionnalités

- Connexion par secret partagé : authentification par secret partagé par jeton ou mot de passe.
- Authentification du proxy de confiance : modes d'authentification du proxy de confiance et porteurs d'identité.
- Mode d'entrée privée : comportement `gateway.auth.mode: "none"` d'entrée privée et ses limites.
- Signature de défi d'appareil : signature d'identité d'appareil par rapport au nonce de défi.
- Jetons d'appareil : émission de jetons d'appareil, persistance, réutilisation de reconnexion, rotation et révocation.
- Amorçage du code de configuration : flux de jetons de code de configuration d'amorçage et remise de jetons d'opérateur délimitée.
- Récupération d'erreur d'authentification : sémantique de récupération pour `AUTH_TOKEN_MISMATCH` et `AUTH_SCOPE_MISMATCH`.
- Migration d'authentification d'appareil : erreurs de migration d'authentification d'appareil et comportement de signature v2/v3 requis.
- Appairage du client : exigences d'appairage d'appareil pour les nouveaux clients.
- Appairage des nœuds : flux d'appairage des nœuds, y compris les demandes en attente, les approbations, l'expiration et les limites d'approbation automatique du CIDR de confiance ou de la mise à niveau des métadonnées.

## Fraîcheur des archives

- `gitcrawl doctor --json`: `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, `repository_count=2`.
- `discrawl status --json`: `generated_at=2026-05-30T00:04:12Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Couverture

Score : 88/100.

Étiquette : Oui.

Signaux positifs :

- Les documents de protocole définissent l'authentification par défi/réponse, l'émission de jetons d'appareil, l'amorçage du code de configuration, les détails de nouvelle tentative requis d'appairage, les limites de nouvelle tentative d'erreur de jeton, la signature d'identité d'appareil, l'approbation automatique locale et les exceptions sans appareil (`docs/gateway/protocol.md:27`, `docs/gateway/protocol.md:118`, `docs/gateway/protocol.md:676`, `docs/gateway/protocol.md:707`, `docs/gateway/protocol.md:721`, `docs/gateway/protocol.md:741`, `docs/gateway/protocol.md:748`, `docs/gateway/protocol.md:775`, `docs/gateway/protocol.md:784`).
- Les documents d'appairage distinguent l'appairage d'appareil Gateway de l'appairage de nœud et documentent l'état en attente, la durée de vie du jeton, les flux d'approbation/rejet, la limitation des commandes de nœud, l'approbation automatique du CIDR de confiance, les règles de localité des en-têtes transférés et le comportement du stockage (`docs/gateway/pairing.md:10`, `docs/gateway/pairing.md:25`, `docs/gateway/pairing.md:48`, `docs/gateway/pairing.md:90`, `docs/gateway/pairing.md:125`, `docs/gateway/pairing.md:173`, `docs/gateway/pairing.md:183`).
- L'exécution vérifie les identités d'appareil signées par rapport au défi du serveur, mappe l'authentification d'appareil invalide à des erreurs structurées, résout l'authentification partagée/appareil/amorçage/proxy de confiance séparément et émet les détails d'appairage et de jeton réessayables/non réessayables (`src/gateway/server/ws-connection/handshake-auth-helpers.ts:307`, `src/gateway/server/ws-connection/message-handler.ts:880`, `src/gateway/server/ws-connection/message-handler.ts:944`, `src/gateway/protocol/connect-error-details.ts:4`, `src/gateway/protocol/connect-error-details.ts:97`).
- Les tests d'intégration réels de Gateway/serveur couvrent l'appairage automatique local de l'interface utilisateur de contrôle, l'approbation de la mise à niveau de portée, l'amorçage et la remise du code de configuration QR, les mises à niveau de rôle d'amorçage, la révocation de jetons d'appareil, la rotation de jetons partagés avec préservation de jetons d'appareil, l'autorisation de rotation/révocation de jetons d'appareil, l'autorisation d'appairage de nœud, l'approbation automatique du CIDR de confiance de nœud et l'authentification de sonde (`src/gateway/server.auth.control-ui.suite.ts:848`, `src/gateway/server.auth.control-ui.suite.ts:1031`, `src/gateway/server.auth.control-ui.suite.ts:1451`, `src/gateway/server.auth.control-ui.suite.ts:1840`, `src/gateway/server.shared-auth-rotation.test.ts:170`, `src/gateway/server.device-token-rotate-authz.test.ts:188`, `src/gateway/server.node-pairing-authz.test.ts:157`, `src/gateway/server.node-pairing-auto-approve.test.ts:88`, `src/gateway/probe.auth.integration.test.ts:71`).
- La couverture inter-processus/e2e existe pour la connexion et l'état du nœud appairé en utilisant deux passerelles, des crochets HTTP et l'appairage de nœud WebSocket (`test/gateway.multi.e2e.test.ts:27`).

Signaux négatifs :

- La fonctionnalité est répartie sur l'identité d'appareil, l'authentification WebSocket, le jeton d'amorçage, l'appairage d'appareil, l'appairage de nœud, le proxy de confiance, la nouvelle tentative du client et le code d'autorisation de méthode. Cette largeur rend les régressions plausibles et se reflète dans l'historique des archives.
- Plusieurs comportements sont sensibles à la sécurité et ont eu des régressions répétées : priorité des jetons, état appairé obsolète, mises à niveau de rôle/portée, boucles de nouvelle tentative d'erreur de jeton, suppression de la portée du proxy de confiance et persistance d'appairage.
- Les tests de plus haute fidélité sont toujours principalement des tests de serveur réel local. Ils ne remplacent pas la preuve de cycle de vie mobile, proxy distant, Tailscale Serve, Docker ou mise à jour du système d'exploitation en direct.

Lacunes d'intégration :

- Aucune preuve iOS/Android/Tailscale Serve/Docker en direct actuelle n'a été trouvée pour cette tranche d'audit, même si les rapports d'archives mentionnent les scénarios d'application mobile, de boucle Docker, de proxy de confiance et de parité de nœud Windows.
- Les problèmes de course de jetons d'amorçage et de limitation de débit de pré-authentification restent ouverts dans les résultats de gitcrawl, donc le chemin d'amorçage a un risque d'intégration non fermé connu.
- Le comportement du proxy de confiance est couvert par les documents et les tests, mais les rapports d'archives ouverts demandent toujours une clarification et une isolation multi-utilisateurs.

## Qualité

Score : 72/100.

Étiquette : Moyen.

Rapports Gitcrawl :

- Les bogues fermés répétés montrent un vrai travail de renforcement : blocages d'amorçage d'appairage d'appareil, boucles d'erreur de jeton, défaillances de diffusion de l'interface utilisateur de contrôle, persistance d'appairage d'appareil, épinglage de métadonnées, auto-désappairage d'état obsolète, priorité des jetons, classification d'erreur de portée, IDOR de rotation/révocation, déconnexions du magasin d'appairage de nœud/appareil et réappairage de redémarrage de boucle.
- Les problèmes/PR ouverts montrent le risque de qualité restant : commandes de liste/révocation d'appairage (#56621), limitation/verrouillage/alerte de débit d'amorçage (#77980, #77978, #77527), courses de jetons de code de configuration (#78276, #78277), limitation de débit RPC de gestion d'appareil/jeton (#84617), documentation de suppression de portée du proxy de confiance (#80063), actualisation de la dernière consultation de l'appareil appairé (#81189), isolation de jetons multi-utilisateurs (#43903), authentification Tailscale secondaire (#57110) et comportement de fermeture Android/appairage de nœud (#85966).

Rapports Discrawl :

- Les discussions récentes des utilisateurs et des responsables mentionnent à plusieurs reprises les boucles requises d'appairage, la récupération d'erreur de jeton d'appareil, les cas limites de l'interface utilisateur de contrôle/proxy local, la confusion d'appairage mobile/nœud et les lignes de base de portée obsolètes.
- La discussion des responsables confirme que certains correctifs sont pertinents pour la version et non triviaux, y compris le comportement de nouvelle tentative de confiance unique, les jetons d'appareil appairé mis en cache, la persistance de remise d'amorçage et les contrats d'approbation fermés à l'échec.
- Les discussions des utilisateurs montrent toujours une confusion des opérateurs autour des appareils appairés en tant que nœud mais pas opérateur, l'absence de réapprobation de portée et les commandes bloquées par les réponses requises d'appairage.

Bonnes qualités :

- L'identité d'appareil utilise les clés Ed25519, dérive les ID d'appareil stables à partir des clés publiques, migre l'identité persistée en toute sécurité et signe les charges utiles liées au nonce (`src/infra/device-identity.ts:97`, `src/infra/device-identity.ts:219`, `src/infra/device-identity.ts:278`).
- L'authentification d'appareil préfère la charge utile v3 tout en acceptant v2 pour la compatibilité à la limite de vérification (`src/gateway/device-auth.ts:20`, `src/gateway/server/ws-connection/handshake-auth-helpers.ts:307`).
- Les décisions de jeton d'appareil, de jeton d'amorçage et de jeton partagé sont séparées, limitées en débit dans le contexte d'authentification et mappées à des raisons non autorisées spécifiques (`src/gateway/server/ws-connection/auth-context.ts:83`, `src/gateway/server/ws-connection/auth-context.ts:160`).
- La vérification d'approbation d'appairage vérifie le rôle/portée de l'appelant, la portée personnelle et les limites d'administrateur pour les méthodes d'approbation/suppression/rotation/révocation (`src/gateway/server-methods/devices.ts:174`, `src/gateway/server-methods/devices.ts:341`, `src/gateway/server-methods/devices.ts:400`).
- L'émission de profil d'amorçage est délimitée aux listes d'autorisation de rôle/portée explicites et vérifie la liaison d'appareil/clé publique avant utilisation (`src/shared/device-bootstrap-profile.ts:13`, `src/infra/device-bootstrap.ts:407`).
- La logique de reconnexion du client utilise les détails de nouvelle tentative explicites et ne réessaye automatiquement l'erreur de jeton que pour les points de terminaison de confiance (`src/gateway/client.ts:605`, `src/gateway/client.ts:877`, `src/gateway/client.ts:929`).

Mauvaises qualités :

- La politique d'authentification et d'appairage reste assez complexe pour que la correction dépende de la préservation des invariants inter-fichiers sur les aides d'authentification du serveur, la gestion des messages, la persistance d'appairage d'appareil, la persistance d'appairage de nœud, les profils d'amorçage et l'état de nouvelle tentative du client.
- Les exceptions sans appareil, l'approbation automatique locale, l'identité du proxy de confiance, la sémantique des jetons partagés et la remise d'amorçage altèrent tous la même surface de rôle/portée effective.
- Les rapports d'archives montrent que les modes de défaillance visibles par l'utilisateur sont souvent déroutants : boucles requises d'appairage, boucles d'erreur de jeton d'appareil et confusion de rôle nœud/opérateur.
- Le renforcement des jetons d'amorçage est incomplet tandis que les rapports de limitation de débit/course ouverts restent.

## Lacunes connues

- Ligne de base de capacité implémentée : authentification par nonce de défi, identité d'appareil signée, authentification par jeton partagé/proxy de confiance, appairage d'appareil approuver/supprimer/lister plus rotation/révocation de jeton, amorçage du code de configuration, appairage de nœud, réutilisation de jeton stocké, nouvelle tentative d'erreur de jeton et classification de reconnexion requise d'appairage.
- La limitation de débit de pré-authentification des jetons d'amorçage, le verrouillage/alerte et la fermeture de la course du code de configuration restent des risques de qualité ouverts dans les résultats des archives (#77980, #77978, #78276, #78277).
- La limitation de débit RPC de gestion d'appareil et de jeton reste ouverte (#84617).
- L'expérience utilisateur de gestion d'appairage est toujours incomplète pour les flux de travail de style liste-approuvée/révocation-mainteneur (#56621).
- La documentation de suppression de portée du proxy de confiance et l'histoire d'isolation des jetons multi-utilisateurs restent assez peu claires pour créer des lacunes d'attente des opérateurs (#80063, #43903, #57110).
- L'actualisation de la dernière consultation de l'appareil appairé est toujours demandée (#81189).
- Les flux de mise à niveau de rôle nœud/mobile restent déroutants pour les utilisateurs et les responsables, y compris le rapport de fermeture WebSocket de l'opérateur Android après l'appairage de nœud (#85966).
- Les lacunes de preuve de cycle de vie distant/mobile/proxy sont enregistrées sous Couverture, pas Qualité.

## Preuve

### Docs

- `docs/gateway/protocol.md:27` documente `connect.challenge`.
- `docs/gateway/protocol.md:75` documente le flux `connect` authentifié.
- `docs/gateway/protocol.md:118` documente `auth.deviceTokens`.
- `docs/gateway/protocol.md:676` documente les modes d'authentification Gateway.
- `docs/gateway/protocol.md:707` documente la sortie du jeton bootstrap de code de configuration.
- `docs/gateway/protocol.md:721` documente le comportement du détail de nouvelle tentative `PAIRING_REQUIRED`.
- `docs/gateway/protocol.md:741` documente le comportement de rotation/révocation et les exigences d'auto-portée/admin.
- `docs/gateway/protocol.md:748` documente l'identité de l'appareil et l'appairage.
- `docs/gateway/protocol.md:775` documente l'approbation automatique locale.
- `docs/gateway/pairing.md:10` documente l'état d'appairage détenu par Gateway.
- `docs/gateway/pairing.md:25` documente l'appairage d'appareil en attente et l'expiration de 5 minutes.
- `docs/gateway/pairing.md:48` documente les événements/méthodes d'appairage de nœud.
- `docs/gateway/pairing.md:90` documente le contrôle de commande de nœud.
- `docs/gateway/pairing.md:125` documente l'approbation automatique de nœud CIDR de confiance.
- `docs/gateway/pairing.md:173` documente les limites de localité des en-têtes transférés.
- `docs/gateway/security/index.md:166` documente la confiance Gateway/nœud.
- `docs/gateway/security/index.md:187` documente les limites de confiance.
- `docs/gateway/security/index.md:222` documente les CIDR de confiance désactivés par défaut.
- `docs/gateway/configuration-reference.md:450` affiche la configuration d'authentification Gateway, d'interface utilisateur de contrôle et d'appairage de nœud.
- `docs/gateway/configuration-reference.md:527` documente les exigences d'authentification et le mode aucun local uniquement.
- `docs/gateway/configuration-reference.md:544` documente l'origine du navigateur, TLS, le proxy de confiance et les paramètres d'appairage CIDR.
- `docs/gateway/trusted-proxy-auth.md:52` documente l'appairage de l'interface utilisateur de contrôle en mode proxy de confiance.
- `docs/gateway/trusted-proxy-auth.md:75` documente la configuration du proxy de confiance et le comportement de secours direct local.

### Source

- `src/gateway/device-auth.ts:20` construit les charges utiles d'authentification d'appareil.
- `src/infra/device-identity.ts:97` définit la forme d'identité d'appareil persistée.
- `src/infra/device-identity.ts:219` charge ou crée l'identité d'appareil.
- `src/infra/device-identity.ts:278` signe les charges utiles d'authentification d'appareil.
- `src/gateway/server/ws-connection/handshake-auth-helpers.ts:76` définit l'admissibilité d'appairage local silencieux.
- `src/gateway/server/ws-connection/handshake-auth-helpers.ts:197` résout la localité d'appairage.
- `src/gateway/server/ws-connection/handshake-auth-helpers.ts:253` ignore l'appairage pour les cas de backend local/auto.
- `src/gateway/server/ws-connection/handshake-auth-helpers.ts:307` vérifie l'authentification d'appareil signée.
- `src/gateway/server/ws-connection/auth-context.ts:83` extrait les candidats de jeton d'appareil.
- `src/gateway/server/ws-connection/auth-context.ts:98` résout l'état d'authentification WebSocket.
- `src/gateway/server/ws-connection/auth-context.ts:160` vérifie les jetons bootstrap et d'appareil.
- `src/gateway/server/ws-connection/message-handler.ts:880` valide les erreurs d'authentification d'appareil.
- `src/gateway/server/ws-connection/message-handler.ts:944` résout l'authentification de connexion et la localité d'appairage.
- `src/gateway/server/ws-connection/message-handler.ts:1100` gère les flux d'appairage requis et d'approbation automatique.
- `src/gateway/server/ws-connection/message-handler.ts:1350` gère l'épinglage de métadonnées et les mises à niveau de portée.
- `src/gateway/server/ws-connection/message-handler.ts:1480` émet les jetons d'appareil et de remise.
- `src/gateway/server/ws-connection/message-handler.ts:1788` émet `hello-ok.auth`.
- `src/infra/device-pairing.ts:143` définit l'expiration de la demande en attente.
- `src/infra/device-pairing.ts:252` échoue fermé pour les enregistrements d'appairage hérités sans jeton.
- `src/infra/device-pairing.ts:347` préserve les horodatages en attente dans les demandes actualisées.
- `src/infra/device-pairing.ts:559` demande/réconcilie l'appairage d'appareil.
- `src/infra/device-pairing.ts:617` approuve l'appairage d'appareil.
- `src/infra/device-pairing.ts:734` approuve l'appairage d'appareil bootstrap.
- `src/infra/device-bootstrap.ts:228` émet les jetons bootstrap.
- `src/infra/device-bootstrap.ts:407` vérifie les liaisons de jeton bootstrap.
- `src/shared/device-bootstrap-profile.ts:13` définit les rôles/portées bootstrap limités.
- `src/gateway/server-methods/devices.ts:174` implémente `device.pair.list` et `device.pair.approve`.
- `src/gateway/server-methods/devices.ts:341` implémente la suppression et l'invalidation d'appareil.
- `src/gateway/server-methods/devices.ts:400` implémente l'autorisation de rotation/révocation de jeton.
- `src/gateway/node-pairing-auto-approve.ts:30` vérifie l'approbation automatique de nœud CIDR de confiance.
- `src/infra/node-pairing.ts:279` demande l'appairage de nœud.
- `src/infra/node-pairing.ts:316` approuve l'appairage de nœud.
- `src/infra/node-pairing.ts:401` vérifie les jetons de nœud.
- `src/gateway/client.ts:571` stocke les jetons d'appareil de `hello-ok`.
- `src/gateway/client.ts:605` réessaie avec le jeton d'appareil stocké après une non-correspondance.
- `src/gateway/client.ts:877` contrôle la nouvelle tentative d'authentification automatique.
- `src/gateway/client.ts:929` restreint la confiance de nouvelle tentative à la boucle locale ou au TLS épinglé.
- `src/gateway/client.ts:948` sélectionne les jetons d'authentification.

### Tests d'intégration

- `src/gateway/server.auth.control-ui.suite.ts:848` couvre l'appairage automatique direct local de l'interface utilisateur de contrôle et l'approbation de mise à niveau de portée.
- `src/gateway/server.auth.control-ui.suite.ts:1031` couvre la remise de jeton bootstrap de code de configuration QR et le comportement de jeton d'opérateur limité.
- `src/gateway/server.auth.control-ui.suite.ts:1451` couvre les mises à niveau de rôle d'authentification bootstrap nécessitant une approbation.
- `src/gateway/server.auth.control-ui.suite.ts:1543` couvre l'appairage d'opérateur d'authentification bootstrap en dehors de la ligne de base QR.
- `src/gateway/server.auth.control-ui.suite.ts:1588` couvre l'approbation automatique d'appairage de nœud direct local suivie de l'approbation de portée d'opérateur.
- `src/gateway/server.auth.control-ui.suite.ts:1840` couvre le rejet de jeton d'appareil révoqué.
- `src/gateway/server.auth.control-ui.suite.ts:1863` couvre l'authentification partagée de boucle de backend local sans appairage d'appareil.
- `src/gateway/probe.auth.integration.test.ts:71` couvre l'authentification réelle de sonde Gateway et l'authentification d'appareil en cache.
- `src/gateway/server.shared-auth-rotation.test.ts:170` couvre la rotation de jeton partagé préservant les sessions de jeton d'appareil.
- `src/gateway/server.shared-auth-rotation.test.ts:246` couvre le comportement de rotation de jeton partagé marqué par l'émetteur.
- `src/gateway/server.device-token-rotate-authz.test.ts:188` couvre le déni de rotation inter-appareil et l'approbation admin.
- `src/gateway/server.device-token-rotate-authz.test.ts:279` couvre les limites d'autorisation de révocation.
- `src/gateway/server.device-pair-approve-authz.test.ts:163` couvre les limites d'autorisation d'approbation d'appareil.
- `src/gateway/server.node-pairing-authz.test.ts:157` couvre la portée d'approbation d'appairage de nœud.
- `src/gateway/server.node-pairing-auto-approve.test.ts:88` couvre l'exigence d'appairage de nœud direct non-boucle par défaut.
- `src/gateway/server.node-pairing-auto-approve.test.ts:122` couvre l'approbation automatique CIDR de confiance de nœud pour la première fois.
- `test/gateway.multi.e2e.test.ts:27` couvre la connexion de nœud appairé dans un flux e2e multi-gateway.

### Tests unitaires

- `src/gateway/device-auth.test.ts:8` couvre les vecteurs de charge utile d'authentification d'appareil.
- `src/gateway/auth.test.ts:245` couvre le comportement d'authentification Gateway jeton/mot de passe/aucun.
- `src/gateway/auth.test.ts:563` couvre le comportement d'authentification proxy de confiance.
- `src/gateway/auth.test.ts:1028` couvre le comportement proxy de confiance direct local.
- `src/gateway/protocol/connect-error-details.test.ts:56` couvre la classification des détails d'erreur de connexion.
- `src/gateway/client.test.ts:1429` couvre la priorité explicite de jeton d'appareil.
- `src/gateway/client.test.ts:1453` couvre la portée d'authentification stockée de secours.
- `src/gateway/client.test.ts:1476` couvre la nouvelle tentative avec jeton stocké après non-correspondance de jeton de confiance.
- `src/gateway/client.test.ts:1597` couvre le comportement de reconnexion `PAIRING_REQUIRED`.
- `src/gateway/server.auth.compat-baseline.test.ts:115` couvre les lignes de base de compatibilité jeton partagé/appareil/authentification.
- `src/gateway/server.auth.browser-hardening.test.ts:389` couvre le durcissement d'appairage de boucle locale du navigateur.
- `src/gateway/node-pairing-auto-approve.test.ts:1` couvre les cas d'aide d'approbation automatique de nœud.

### Requêtes Gitcrawl

Toutes les requêtes gitcrawl ont utilisé l'archive actualisée de `last_sync_at=2026-05-28T05:29:12.208862Z`.

Requête : `gitcrawl search issues "device pairing" -R openclaw/openclaw --state all --json number,title,state,url --limit 20`

Résultats :

- #76349 fermé `[Bug]: openclaw devices approve fails with missing operator.admin / device-ownership-mismatch`
- #19352 fermé `[Bug]: Device pairing bootstrap impossible - chicken-and-egg problem when CLI also requires pairing`
- #21688 fermé `Pairing scope-upgrade loop: repeated 'pairing required' reconnects for same device`
- #24189 fermé `sessions_spawn fails with 'pairing required' despite device being paired and approved`
- #20447 fermé `Control UI does not receive device.pair.requested broadcast (pairing approval UI broken)`
- #29908 fermé `Enhancement: token-authenticated clients should bypass device pairing`
- #23498 fermé `Device pairing recovery can self-unpair on token mismatch and legacy paired.json arrays break approve persistence`
- #44574 fermé `[Bug]: WS node pairing auto-approved at runtime but never persists (device-auth.json never created)`
- #7715 fermé `Feature: hot-reload device pairing approvals without gateway restart`
- #22400 fermé `[Bug]: Device pairing not persisted after Gateway restart - requires manual re-approval`
- #56377 fermé `[Bug]: Device pairing gets stuck after macOS minor update because paired device metadata pins old OS version`
- #50079 fermé `Control UI Chat view freezes after successful auth/pairing (reproduces in incognito)`
- #14561 fermé `Device pairing: pending requests not created for Control UI via Tailscale Serve`
- #44672 fermé `[Bug]: macOS app can stay stuck on generic 'pairing required' after node->operator upgrade approval`
- #21470 fermé `CLI device paired with operator.read scope only - cron list, gateway status fail with 'pairing required'`
- #55995 fermé `[Bug]: /pair approve bypasses the admin scope guard for device pairing`
- #21647 fermé `Loopback connections require device pairing on every gateway restart (2026.2.19)`
- #6836 fermé `Node pairing: device-pairing and node-pairing stores are disconnected - nodes pending/approve tools don't work`
- #3795 fermé `[Feature]: Auto-approve device pairing for Tailscale Serve requests`
- #69214 fermé `[Bug]: Gateway client gets stuck in scope-upgrade repair loop for Telegram Native Approvals`

Requête : `gitcrawl search issues "device token" -R openclaw/openclaw --state all --json number,title,state,url --limit 20`

Résultats :

- #21572 fermé `CLI device auth persists stale device token after identity reset and breaks shared-token reconnect`
- #19681 fermé `Internal callGateway retries AUTH_TOKEN_MISMATCH when both device identity and static token are present`
- #18562 fermé `gateway status RPC probe fails with device_token_mismatch after first paired call`
- #39417 fermé `Control UI signs device auth with a different token than it sends`
- #35944 fermé `dangerouslyDisableDeviceAuth still rejects with device token mismatch`
- #71609 fermé `Control UI device token mismatch loop after scope upgrade causes rate-limit lockout`
- #20679 fermé `Device token mismatch persists after rotate/fresh pairing`
- #17270 fermé `Device token auth regression: shared token wins over paired token on reconnect`
- #83358 fermé `Explicit --url/--token device management path appears to leak paired-device state`
- #39861 fermé `Token-authenticated webchat cannot obtain device token`
- #79292 fermé `operator scope mismatch silently rejected as device token mismatch`
- #50626 fermé `device.token.rotate lets paired operators mint tokens for other devices`
- #19244 fermé `Gateway device keypair auth fails after upgrade`
- #18175 fermé `Device token mismatch after re-pairing; cron list fails`
- #23891 fermé `persistent device_token_mismatch after identity wipe/restart`
- #52085 fermé `Device token accepted but scopes missing despite full paired token`
- #18936 fermé `Gateway tools/CLI commands fail after first successful paired connection`
- #71990 fermé `device.token.revoke skips containment check for other-device tokens`
- #18643 fermé `Device token mismatch after config patch`
- #21191 fermé `device-auth.json tokens never persist on macOS managed app`

Requête : `gitcrawl search issues "gateway pairing" -R openclaw/openclaw --state all --json number,title,state,url --limit 20`

Résultats :

- #22908 fermé `Web UI Pairing Broken`
- #21796 fermé `Discord pairing policy blocks DM/subagent replies until manual gateway action`
- #57688 fermé `cron add fails with pairing required and no approval path`
- #21604 fermé `dmPolicy=everyone still loses Discord pairing state on restart`
- #362 fermé `WhatsApp pairing flow spams reconnection attempts`
- #56621 ouvert `Feature: pairing list-approved and pairing revoke commands`
- #24189 fermé `sessions_spawn fails with 'pairing required' despite device being paired and approved`
- #6836 fermé `Node pairing: device-pairing and node-pairing stores are disconnected - nodes pending/approve tools don't work`
- #28299 fermé `Gateway pairing prompt never appears in browser after token auth`
- #2501 fermé `Gateway pairing status command should show pending device`
- #21146 fermé `pair approve should require operator.admin`
- #69284 fermé `Gateway pairing loop after Telegram Native Approvals startup`
- #23187 fermé `Node pairing request disappears after restart`
- #21688 fermé `Pairing scope-upgrade loop: repeated 'pairing required' reconnects for same device`
- #20447 fermé `Control UI does not receive device.pair.requested broadcast (pairing approval UI broken)`
- #29908 fermé `Enhancement: token-authenticated clients should bypass device pairing`
- #85577 fermé `Gateway pairing policy allows stale browser metadata after approval`
- #19352 fermé `Device pairing bootstrap impossible - chicken-and-egg problem when CLI also requires pairing`
- #13596 fermé `Gateway pairing request lacks role/scope detail`
- #21470 fermé `CLI device paired with operator.read scope only - cron list, gateway status fail with 'pairing required'`

Requête : `gitcrawl search issues "bootstrap token" -R openclaw/openclaw --state all --json number,title,state,url --limit 20`

Résultats :

- #66100 fermé `Android bootstrap token is not cleared after successful spend on plain LAN ws://, causing auth loop`
- #77980 ouvert `bootstrap token path lacks rate limiting/lockout/alerting`
- #78276 ouvert `setup-code races can revive consumed bootstrap tokens`
- #77978 ouvert `pre-auth bootstrap-token verify allows mutex-stall DoS without rate limit`
- #47887 fermé `iOS LAN onboarding forces wss and bootstrap-only setup codes fail`
- #79292 fermé `operator scope mismatch silently rejected as device token mismatch`
- #12441 ouvert `Control UI should accept gateway token from Authorization header`
- #48471 ouvert `one-line local bootstrap daemon/dashboard auth/Telegram owner setup`
- #59231 fermé `bootstrap token loses priority behind tailscale/trusted proxy auth`
- #76291 fermé `bootstrap token verify holds auth mutex too long`
- #80895 fermé `bootstrap token can bind without device-key proof`
- #81291 fermé `setup-code device pairing skips approval`
- #85689 fermé `setup-code bootstrap grants talk secrets to operator handoff`
- #78013 fermé `bootstrap token auth has no rate limit`
- #77526 fermé `bootstrap token pre-auth verification can be abused`
- #58381 fermé `QR bootstrap operator handoff lost after approval`
- #64423 fermé `stale paired token beats fresh setup-code token`
- #80975 fermé `bootstrap pairing allows role/scope changes after token issue`
- #26897 fermé `bootstrap pairing tokens bypass WS auth safeguards`
- #83683 fermé `QR setup-code operator handoff regression`

Requête : `gitcrawl search prs "device pairing" -R openclaw/openclaw --state all --json number,title,state,url --limit 20`

Résultats :

- #22071 fermé `clear pairing state on device token mismatch`
- #23503 fermé `preserve pairing state on mismatch and migrate legacy paired.json`
- #20703 fermé `Device Token Scope Escalation via Rotate Endpoint`
- #69375 fermé `limit paired-device pairing actions to caller device`
- #10621 fermé `Plugin add device-pair`
- #55996 fermé `pair approve admin guard`
- #31988 fermé `add device pairing HTTP endpoints`
- #14863 fermé `pre-pair CLI operator device during onboarding`
- #81189 ouvert `refresh paired device last-seen metadata`
- #77688 fermé `avoid impossible rotation advice`
- #70239 fermé `clear stale pairing requests on removal`
- #6846 fermé `bridge node.pair tools to device pairing store`
- #52059 fermé `gateway.auth.scopes for device-less token/password connections`
- #60462 fermé `reject unapproved device token roles`
- #21830 fermé `ios onboarding operator scopes regression`
- #81292 fermé `Require approval for setup-code device pairing`
- #36427 fermé `restore loopback-bound pairing bypass for Docker deployments`
- #21659 fermé `Fix/ios pairing flow`
- #63086 fermé `coerce array state files`
- #85690 fermé `gate talk secret bootstrap handoff`

Requête : `gitcrawl search prs "device token" -R openclaw/openclaw --state all --json number,title,state,url --limit 20`

Résultats :

- #17296 fermé `restore device token priority`
- #17379 fermé `restore device token priority in client auth selection`
- #79314 fermé `classify scope mismatch separately from device token mismatch`
- #79296 fermé `surface auth scope mismatch reason`
- #79295 fermé `fix scope mismatch error detail`
- #37382 fermé `separate device token from shared auth token`
- #1314 fermé `allow token auth to bypass device identity`
- #18188 fermé `clear stale device-auth token on token mismatch`
- #50627 fermé `device.token.rotate IDOR`
- #84617 ouvert `rate-limit device pairing and token management RPCs`
- #81189 ouvert `refresh paired device last-seen metadata`
- #71991 fermé `containment check for device.token.revoke`
- #41511 fermé `Control UI token signing fix`
- #39420 fermé `Control UI uses matching token for signing and auth`
- #81067 fermé `admin scope for node token management`
- #23503 fermé `preserve pairing state on mismatch and migrate legacy paired.json`
- #78732 fermé `separate trusted-proxy device token ownership`
- #22071 fermé `clear pairing state on device token mismatch`
- #78015 fermé `rate-limit bootstrap and device signature auth`
- #64165 fermé `persist device token after setup-code bootstrap`

Requête : `gitcrawl search issues "trusted proxy device identity" -R openclaw/openclaw --state all --json number,title,state,url --limit 20`

Résultats :

- #80063 ouvert `docs clarify trusted-proxy WebSocket scope clearing`
- #45217 fermé `trusted-proxy auth blocks internal exec tool without device identity`
- #43903 ouvert `multiple gateway tokens for multi-user isolation`
- #80589 fermé `WebChat missing operator.read behind Nginx trusted proxy`
- #50022 fermé `trusted-proxy strips operator scopes with missing Origin header`
- #69066 ouvert `RFC: separate internal service identity from user auth`
- #60225 fermé `shared-auth API clients lose scopes after device-less auth regression`
- #57087 fermé `trusted-proxy lacks guardrails`
- #78731 fermé `trusted-proxy HTTP auth bypasses per-session ownership`
- #30092 fermé `Control UI still device-required behind local HTTPS reverse proxy`
- #78508 fermé `trusted-proxy missing operator.read for chat history`
- #82607 fermé `trusted-proxy + allowLoopback rejects internal loopback callers`
- #57110 ouvert `Tailscale Serve optional secondary auth`
- #47402 fermé `WebSocket device auth regression behind trusted proxy`
- #17270 fermé `Device token auth regression: shared token wins over paired token`
- #17608 fermé `trusted proxy docs mismatch for device-less scopes`
- #50626 fermé `device.token.rotate lets paired operators mint tokens for other devices`
- #73636 fermé `trusted-proxy clears scopes for local direct fallback`
- #29416 fermé `Control UI pairing behind trusted-proxy loops`

Requête : `gitcrawl search issues "node pairing auto approve" -R openclaw/openclaw --state all --json number,title,state,url --limit 20`

Résultats :

- #6836 fermé `Node pairing: device-pairing and node-pairing stores are disconnected - nodes pending/approve tools don't work`
- #37749 fermé `onboard should auto-approve local node host pairing`
- #70600 fermé `docs say approve --latest but CLI only previews pending pairing`
- #22400 fermé `Device pairing not persisted after Gateway restart`
- #29908 fermé `token-authenticated clients should bypass device pairing`
- #22062 fermé `node pairing approval should carry scopes`
- #62176 fermé `trusted-CIDR node auto-approve should reject browser/control clients`
- #21812 fermé `node pairing fails after gateway restart`
- #19352 fermé `Device pairing bootstrap impossible`
- #17443 fermé `node pairing status missing approval details`
- #25779 fermé `local node pairing requires manual approval in Docker`
- #21647 fermé `Loopback connections require device pairing on every gateway restart`
- #36973 fermé `node pairing command missing docs`
- #62765 ouvert `msteams dmPolicy pairing drops unpaired node state`
- #23661 fermé `node pair approve requires wrong scope`
- #29622 fermé `node reconnect loses pairing metadata`
- #85966 ouvert `Android UI/operator WS closes silently after node pair`
- #21470 fermé `CLI device paired with operator.read scope only`
- #25808 fermé `node pairing auto-approve ignores CIDR boundary`
- #22655 fermé `node pair request not visible in Control UI`

Requête : `gitcrawl search prs "bootstrap token" -R openclaw/openclaw --state all --json number,title,state,url --limit 20`

Résultats :

- #59232 fermé `prefer bootstrap auth over tailscale`
- #76322 ouvert `bootstrap token mutex-stall DoS no rate limit`
- #78015 fermé `rate-limit bootstrap and device signature auth`
- #58382 fermé `restore qr bootstrap onboarding handoff`
- #77527 ouvert `rate-limit pre-auth bootstrap-token verify`
- #83684 fermé `restore QR bootstrap operator handoff`
- #80896 ouvert `require device key proof for bootstrap token binding`
- #78277 ouvert `setup-code races revive consumed tokens`
- #26898 fermé `secure bootstrap pairing tokens and restore WS auth safeguards`
- #64424 fermé `prioritize fresh bootstrap setup codes over cached device tokens`
- #81292 fermé `require setup-code pairing approval`
- #80976 fermé `prevent bootstrap pairing scope changes`
- #85690 fermé `gate talk secret bootstrap handoff`
- #66101 fermé `clear Android bootstrap token after successful spend`
- #47888 fermé `support LAN ws:// setup-code bootstrap`
- #79296 fermé `surface auth scope mismatch reason`
- #12442 ouvert `Control UI Authorization-header gateway token bootstrap`
- #48472 ouvert `local bootstrap daemon/dashboard auth flow`
- #76292 fermé `avoid holding auth mutex during bootstrap verify`
- #78016 fermé `device signature rate-limit follow-up`

### Requêtes Discrawl

Toutes les requêtes discrawl ont utilisé `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search --limit 10 "<query>"` contre `state=current`, `last_sync_at=2026-05-28T00:14:43Z`.

Requête : `"device pairing"`

Résultats :

- Retourné 10 résultats.
- Les résultats à haut signal incluaient des conseils de support utilisateur du 2026-05-26 selon lesquels la configuration de nœud mobile signifie l'appairage d'un téléphone/appareil à Gateway et l'exposition des capacités de nœud.
- Les résultats à haut signal incluaient des journaux utilisateur du 2026-05-23 montrant `device pairing auto-approved` avec le rôle `operator`.
- Les résultats à haut signal incluaient une discussion générale du 2026-05-22 où les commandes CLI/appareil étaient bloquées car l'appareil avait besoin d'une réapprobation de portée.
- Les résultats à haut signal incluaient une discussion générale du 2026-05-22 où un appareil était appairé en tant que `node` mais pas encore opérateur.
- Les résultats à haut signal incluaient une discussion de mainteneur du 2026-05-22 d'un contrat d'approbation de remplacement fermé et une mise en garde sur le changement de comportement de limite d'authentification.
- Les résultats à haut signal incluaient une discussion Android du 2026-05-19 demandant si une défaillance de connexion Gateway devrait créer une demande d'appairage en attente.

Requête : `"device token mismatch"`

Résultats :

- Retourné 10 résultats.
- Les résultats à haut signal incluaient une discussion de mainteneur du 2026-05-01 sur la récupération de jeton partagé obsolète, le comportement de budget de nouvelle tentative/boucle annulée, l'effacement agressif de jeton d'appareil et la non-correspondance de persistance de remise bootstrap.
- Les résultats à haut signal incluaient une discussion de problème du 2026-04-25 indiquant que le main actuel limite la reconnexion `AUTH_TOKEN_MISMATCH` de l'interface utilisateur de contrôle avec le jeton d'appareil appairé en cache et une nouvelle tentative de confiance.
- Les résultats à haut signal incluaient une discussion de problème du 2026-04-25 pour les boucles de non-correspondance de jeton d'appareil de l'interface utilisateur de contrôle après la mise à niveau de portée.
- Les résultats à haut signal incluaient une discussion de mainteneur du 2026-04-25 où le routage Twilio était bloqué par `unauthorized: device token mismatch`.
- Les résultats à haut signal incluaient des commentaires de problème du 2026-04-24 selon lesquels le main actuel attache l'identité d'appareil et lit le nonce de défi pour les flux de commande/sonde.
- Les résultats à haut signal incluaient des commentaires de problème du 2026-04-24 selon lesquels le stockage/la signature de jeton de l'interface utilisateur de contrôle et la nouvelle tentative limitée ont été implémentés avec des tests de régression.

Requête : `"pairing required gateway"`

Résultats :

- Retourné 10 résultats.
- Les résultats à haut signal incluaient des journaux généraux du 2026-05-03 montrant une boucle d'appairage requis `scope-upgrade` d'un appareil CLI authentifié par mot de passe demandant les portées admin/pairing/talk/write à partir d'une ligne de base de lecture.
- Les résultats à haut signal incluaient une discussion utilisateur du 2026-05-02 où `cron add` était bloqué par l'appairage requis.
- Les résultats à haut signal incluaient une discussion Docker du 2026-05-01 décrivant un chemin d'effacement d'identité/secours local et une défaillance d'identité d'opérateur.pairing-scoped obsolète.
- Les résultats à haut signal incluaient une discussion de mainteneur du 2026-04-29 selon laquelle l'approbation native au démarrage peut utiliser l'identité persistée et atteindre les lignes de base appairées obsolètes.
- Les résultats à haut signal incluaient une discussion utilisateur du 2026-04-26 où une boucle d'appairage requis a été résolue en réduisant au silence un canal qui réessayait et en approuvant la demande en attente.
- Les résultats à haut signal incluaient des commentaires de problème du 2026-04-26 pour les corrections de détail d'appairage requis exploitables.

Requête : `"bootstrap token"`

Résultats :

- La plupart des résultats étaient des discussions bootstrap/contexte plus larges plutôt que des preuves directes de WebSocket d'appairage Gateway.
- Une discussion de mainteneur du 2026-05-20 a connecté la douleur de configuration aux canaux primaires et à l'intégration locale, mais n'a pas fermé les problèmes actuels de course/limite de débit de jeton bootstrap.

Requête : `"trusted proxy device identity"`

Résultats :

- Retourné 10 résultats.
- Les résultats à haut signal incluaient une discussion de problème du 2026-04-26 selon laquelle les connexions d'opérateur sans jeton/mot de passe/proxy de confiance effacent les portées, avec une exception de client de passerelle de backend.
- Les résultats à haut signal incluaient une discussion de problème du 2026-04-25 selon laquelle le mode proxy de confiance prend en charge les déploiements gérés par opérateur sans identité par appareil.
- Les résultats à haut signal incluaient une discussion d'examen de PR du 2026-04-24 sur la formulation `dangerouslyDisableDeviceAuth` et les exceptions à l'effacement de portée.
- Les résultats à haut signal incluaient des journaux d'audit utilisateur du 2026-04-22 et 2026-04-20 avertissant que `allowInsecureAuth` ne contourne pas le contexte sécurisé/l'identité d'appareil et que les en-têtes de proxy inverse ne sont pas approuvés par défaut.

Requête : `"node pairing"`

Résultats :

- Retourné 10 résultats.
- Les résultats à haut signal incluaient des réponses d'automatisation mobile du 2026-05-26 selon lesquelles les intégrations de téléphone/appareil se connectent et s'appairent en tant que nœuds.
- Les résultats à haut signal incluaient une discussion générale du 2026-05-22 où une application mobile était uniquement appairée en tant que nœud et avait besoin de rôles/portées d'opérateur pour le comportement de l'interface utilisateur.
- Les résultats à haut signal incluaient une discussion générale du 2026-05-13 proposant des subventions d'appairage qui portent l'intention de rôle.
- Les résultats à haut signal incluaient un rapport utilisateur du 2026-05-11 où les DM de configuration utilisaient l'appairage mais aucun code/demande en attente n'était visible.
- Les résultats à haut signal incluaient une discussion de mainteneur du 2026-05-06 selon laquelle la parité de nœud Windows et l'appairage n'étaient pas encore aussi robustes que souhaité.
- Les résultats à haut signal incluaient une discussion Docker du 2026-05-01 où l'appairage CLI accordait uniquement operator.pairing mais avait besoin de operator.admin.

### Vérification

- Audit de note uniquement ; aucune modification de code de produit ou de rapport de matrice.
- Exécution de validation : `git diff --check -- .mem/main/specs/25-lts-release-placeholder`.
