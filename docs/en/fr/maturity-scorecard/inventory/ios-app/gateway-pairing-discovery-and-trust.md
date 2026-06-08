---
title: "Application iOS - Note de maturité sur l'appairage, la découverte et la confiance de la passerelle"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application iOS - Note de maturité sur l'appairage, la découverte et la confiance de la passerelle

## Résumé

L'application iOS dispose d'une implémentation native substantielle pour la découverte de passerelle, la configuration manuelle/QR, la confiance d'empreinte TLS, l'authentification des appareils, les sessions de nœud/opérateur à portée de rôle, et les diagnostics visibles par l'utilisateur. Le principal limiteur de maturité est la preuve d'exécution : le référentiel dispose d'une couverture au niveau de la passerelle et de clients synthétiques pour l'appairage de nœud en forme iOS, mais je n'ai pas trouvé de flux natif iOS de première exécution/en direct qui exerce la découverte, la configuration QR/manuelle, la confiance TLS, l'approbation, l'authentification de nœud+opérateur, et l'enregistrement soutenu par relais de bout en bout.

## Portée de la catégorie

- Découverte de passerelle Bonjour/locale et étendue.
- Intégration manuelle d'hôte/port et intégration QR/code de configuration.
- Persistance de la configuration de connexion de passerelle.
- Comportement d'invite de confiance d'empreinte TLS et d'épinglage.
- Approbation d'appairage, stockage d'authentification/trousseau d'appareil, et authentification de session de nœud+opérateur.
- Diagnostics d'appairage/authentification pour les utilisateurs et les opérateurs.

## Fonctionnalités

- Bonjour/locale : Découverte de passerelle Bonjour/locale et étendue
- Hôte/port manuel : Intégration manuelle d'hôte/port et intégration QR/code de configuration
- Persistance de la configuration de connexion de passerelle : Comportement, statut et vérification visible par l'opérateur de la persistance de la configuration de connexion de passerelle.
- Invite de confiance d'empreinte TLS : Comportement d'invite de confiance d'empreinte TLS et d'épinglage
- Approbation d'appairage : Approbation d'appairage, stockage d'authentification/trousseau d'appareil, et authentification de session de nœud+opérateur
- Diagnostics d'appairage/authentification pour les utilisateurs : Diagnostics d'appairage/authentification pour les utilisateurs et les opérateurs

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (46%)`

Le signal de couverture le plus fort n'est pas l'automatisation native de l'application iOS ; c'est la couverture d'intégration/e2e au niveau de la passerelle qui connecte un client de nœud en forme iOS à travers le chemin d'appairage de passerelle réel, plus les tests de comportement de rôle et de push côté serveur. Cela prouve une compatibilité de protocole importante, mais n'exerce pas l'interface utilisateur de première exécution de l'application native, le scanner QR, le résolveur Bonjour, l'invite de confiance TLS, la remise soutenue par trousseau, l'expérience utilisateur d'hôte/port manuel, le démarrage de session double nœud+opérateur, ou l'enregistrement de relais dans une version iOS en direct, donc le score reste en dessous d'Alpha.

La couverture unitaire est large et utile comme preuve à l'appui pour l'analyse, l'épinglage, le trousseau, la charge utile d'authentification, et le comportement de reconnexion, mais selon la politique, elle ne rend pas ces fonctionnalités couvertes par elle-même.

## Score de qualité

- Score : `Expérimental (48%)`

La qualité de l'implémentation est plus forte que la preuve d'exécution, mais reste Expérimentale pour cette ligne de support public. La source et la documentation montrent un modèle de confiance cohérent : le TXT Bonjour n'est pas approuvé pour le routage, la configuration en texte brut non-loopback est bloquée, les passerelles découvertes nécessitent une confiance TLS stockée avant la connexion automatique, les empreintes TLS résident dans le stockage soutenu par trousseau, l'identité de l'appareil utilise des charges utiles signées, les jetons émis sont à portée de rôle, et l'application sépare les sessions de nœud et d'opérateur. Les diagnostics d'appairage/authentification sont également structurés suffisamment pour distinguer l'appairage requis, les défaillances de jeton/mot de passe/bootstrap, l'inadéquation d'épingle TLS, la mise à niveau des métadonnées, le proxy/limite de débit, et les états de pause de reconnexion.

La qualité reste en dessous de Beta car l'enregistrement du produit/opérateur est encore brut pour les utilisateurs réels. La discussion d'archive montre une confusion récurrente autour de la configuration `wss://` d'adresse IP publique, les certificats DNS valides, le comportement de Tailscale Serve/WebSocket, les régressions d'appairage réseau local iOS, la récupération de rotation de jetons, la remise de bootstrap QR, la découverte d'URL de base de relais, et l'accès interne/TestFlight uniquement.

## Score de complétude

- Score : `Expérimental (46%)`
- Instructions de surface : évaluées par rapport à `references/completeness/ios-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Bonjour/locale, Hôte/port manuel, Persistance de la configuration de connexion de passerelle, Invite de confiance d'empreinte TLS, Approbation d'appairage, Diagnostics d'appairage/authentification pour les utilisateurs.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre d'écarts connus utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Écarts connus

- Ajouter une exécution native iOS de fumée de première exécution d'appairage ou en direct qui couvre la passerelle LAN découverte, la découverte étendue/Tailnet, l'hôte/port manuel, le code QR/configuration, l'invite de confiance TLS, l'approbation d'appairage, les sessions de nœud+opérateur, et l'enregistrement de push soutenu par relais.
- Renforcer la documentation de l'opérateur pour les points de terminaison `wss://` publics, l'inadéquation de certificat d'adresse IP brute, les noms DNS approuvés, les exigences de Tailscale Serve/WebSocket, et les distinctions d'échec d'appairage/authentification/réseau.
- Rendre l'URL de relais officielle/TestFlight et le chemin d'accès plus découvrables.
- Maintenir les flux de réinitialisation d'intégration, de rotation de certificat, et de rotation de jeton de passerelle visibles dans un manuel iOS.

## Preuve

### Docs

- `docs/platforms/ios.md` décrit l'application iOS comme un aperçu interne, non distribué publiquement pour le moment, et indique qu'elle se connecte via LAN ou WebSocket tailnet en utilisant Bonjour, tailnet unicast DNS-SD, ou hôte/port manuel. Le démarrage rapide nécessite de choisir une passerelle découverte ou un hôte manuel, d'approuver avec `openclaw devices approve <requestId>`, puis de vérifier `nodes.status` et `node.list`.
- `docs/platforms/ios.md` documente les sessions de nœud et d'opérateur authentifiées, `gateway.identity.get`, l'enregistrement `push.apns.register` soutenu par relais, App Attest plus JWS de transaction d'application StoreKit, et la passerelle signant les demandes d'envoi de relais pour les versions officielles/TestFlight.
- `apps/ios/README.md` étiquette l'application Super Alpha/usage interne uniquement, indique qu'aucune distribution publique n'existe, et documente les flux d'archive locale plus bêta TestFlight. Ses notes de dépannage mettent en évidence le comportement au premier plan, les erreurs d'appairage/authentification mettant en pause les boucles de reconnexion, l'agitation de reconnexion approximative, les journaux de découverte, l'hôte/port manuel, et les vérifications TLS.
- `apps/ios/CHANGELOG.md` enregistre le support de configuration par code QR, l'analyse du code de configuration copié, le blocage de `ws://` non-loopback, et la récupération de reconnexion après les modifications de certificat de confiance.

### Source

- `apps/ios/Sources/Gateway/GatewayDiscoveryModel.swift` parcourt les domaines de service Bonjour configurés pour `_openclaw-gw._tcp` et enregistre les détails de découverte/débogage, y compris le nom d'affichage, l'hôte LAN, le DNS tailnet, le port de la passerelle, le mode TLS, et les champs TXT SHA-256 TLS.
- `apps/ios/Sources/Gateway/GatewayServiceResolver.swift` résout les services Bonjour via les données SRV/adresse `NetService` et évite explicitement de faire confiance aux données TXT pour le routage.
- `apps/ios/Sources/Gateway/GatewayConnectionController.swift` implémente les chemins de connexion découverts et manuels, les exigences TLS, le sondage d'empreinte digitale, l'état de l'invite de confiance, l'autoconnexion de broche stockée, la persistance du dernier point de terminaison manuel, et les options de connexion de passerelle avec `role: node`.
- `apps/ios/Sources/Gateway/GatewayTrustPromptAlert.swift`, `apps/ios/Sources/Onboarding/QRScannerView.swift`, et `apps/ios/Sources/Onboarding/OnboardingWizardView.swift` implémentent l'invite de confiance, le scanner QR, la configuration manuelle d'hôte/port, l'analyse du code de configuration, la préparation de l'appairage d'amorçage, et l'interface utilisateur d'approbation d'appairage.
- `apps/ios/Sources/Gateway/GatewaySettingsStore.swift`, `apps/ios/Sources/Gateway/KeychainStore.swift`, et `apps/shared/OpenClawKit/Sources/OpenClawKit/GenericPasswordKeychainStore.swift` persistent les ID d'instance, les identifiants de passerelle, les jetons d'amorçage, les mots de passe, les broches TLS, les métadonnées de dernière connexion, et les diagnostics en utilisant le stockage soutenu par Keychain et les fichiers protégés.
- `apps/shared/OpenClawKit/Sources/OpenClawKit/GatewayTLSPinning.swift`, `DeepLinks.swift`, `DeviceIdentity.swift`, `DeviceAuthStore.swift`, `DeviceAuthPayload.swift`, et `GatewayChannel.swift` implémentent la validation de broche TLS, l'analyse sécurisée des liens profonds, l'identité de dispositif Ed25519, le stockage de jetons limités par rôle, les charges utiles d'authentification signées, la gestion des nonces de défi, la remise d'amorçage, et les règles de nouvelle tentative de jetons de point de terminaison de confiance.
- `apps/ios/Sources/Model/NodeAppModel.swift` exécute des sessions de passerelle de nœud et d'opérateur séparées et utilise la session d'opérateur pour récupérer l'identité de la passerelle avant l'enregistrement APNs soutenu par relais.
- `apps/shared/OpenClawKit/Sources/OpenClawKit/GatewayConnectionProblem.swift` et `apps/ios/Sources/Gateway/GatewayConnectionIssue.swift` mappent les défaillances d'appairage, d'authentification, de TLS, de proxy, de limite de débit, de rôle/portée, et de métadonnées dans des diagnostics structurés.

### Tests d'intégration

- `test/gateway.multi.e2e.test.ts` et `test/helpers/gateway-e2e-harness.ts` exercent les flux WebSocket/HTTP multi-passerelle et connectent un client de nœud en forme iOS avec une identité de dispositif réelle, un jeton, un rôle `node`, des capacités, des commandes, et un statut de nœud appairé.
- `src/gateway/server.roles-allowlist-update.test.ts`, `src/gateway/server.node-pairing-auto-approve.test.ts`, `src/gateway/exec-approval-ios-push.test.ts`, `src/gateway/server-node-events.test.ts`, et `src/gateway/server-methods/push.test.ts` couvrent le nœud iOS adjacent de la passerelle, l'appairage, le rôle, l'événement, et le comportement de poussée.
- Aucun scénario iOS en direct/e2e natif n'a été trouvé qui installe ou lance l'application iOS et pilote la découverte, la configuration QR/manuelle, la confiance TLS, l'approbation, l'authentification du dispositif, le démarrage de la session nœud+opérateur, et l'enregistrement de relais de poussée de bout en bout.

### Tests unitaires

- `apps/ios/Tests/GatewayConnectionSecurityTests.swift` couvre la confiance de broche TLS, la méfiance d'empreinte digitale annoncée, les exigences de broche d'autoconnexion, l'application TLS non-loopback, les valeurs par défaut Tailscale, et le comportement de rotation de certificat de confiance.
- `apps/ios/Tests/GatewayConnectionControllerTests.swift` couvre la configuration de connexion de passerelle, le filtrage de capacité/commande, les portées d'opérateur, la seconde chance du point de terminaison manuel enregistré, les décisions de reconnexion, et les métadonnées de dernière connexion chargées par keychain.
- `apps/ios/Tests/KeychainStoreTests.swift`, `apps/shared/OpenClawKit/Tests/OpenClawKitTests/GatewayTLSPinningTests.swift`, et `DeviceIdentityStoreTests.swift` couvrent le comportement de stockage keychain, de broche TLS, et d'identité de dispositif.
- `apps/shared/OpenClawKit/Tests/OpenClawKitTests/DeepLinksSecurityTests.swift` couvre l'analyse sécurisée du code de configuration, les messages de code de configuration copié, le rejet non-loopback non sécurisé, l'autorisation loopback/LAN privé, et le rejet plaintext tailnet.
- `apps/shared/OpenClawKit/Tests/OpenClawKitTests/GatewayNodeSessionTests.swift`, `DeviceAuthPayloadTests.swift`, et `apps/ios/Tests/GatewayConnectionIssueTests.swift` couvrent la précédence bootstrap/device-token, les charges utiles d'authentification signées, la persistance des jetons, les portes de nouvelle tentative de point de terminaison de confiance, et la détection structurée des problèmes d'appairage/authentification.

### Requêtes Gitcrawl

- `gitcrawl search openclaw/openclaw --query "iOS app gateway pairing discovery TLS fingerprint keychain operator session" --json` n'a retourné aucun résultat.
- `gitcrawl search openclaw/openclaw --query "iOS QR setup code TLS fingerprint pairing manual host port" --json` n'a retourné aucun résultat.
- `gitcrawl search openclaw/openclaw --query "iOS device signature invalid pairing required gateway token" --json` a retourné la PR `#80656` ouverte, `fix(swift): keep device auth compatible with v2 gateways`, avec un extrait indiquant que la passerelle en direct a changé de `device-signature-invalid` avant l'appairage à `pairing required`.
- `gitcrawl search openclaw/openclaw --query "iOS pairing" --json` a retourné les PR/problèmes ouverts incluant `#80656` compatibilité d'authentification de dispositif, `#78807` authentification d'appairage LAN privé, `#55914` codes d'invitation partageables pour l'appairage mobile, `#63123` support de balise vivante en arrière-plan, `#11887` relais cloud pour l'accès mobile à distance, et `#81402` état d'exécution vers SQLite.
- `gitcrawl search openclaw/openclaw --query "iOS TestFlight relay push gateway identity" --json` n'a retourné aucun résultat.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "iOS gateway pairing TLS fingerprint setup code"` n'a retourné aucun résultat.
- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "iOS TestFlight push relay gateway identity pairing"` n'a retourné aucun résultat.
- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "iOS pairing"` a retourné la discussion iOS Alpha/support du 2026-05-29 au 2026-03-30 sur l'appairage QR sur VPS/réseaux publics nécessitant HTTPS/WSS avec un certificat de confiance, le risque d'inadéquation de certificat d'adresse IP brute, le flux `/pair qr` et `/pair approve`, la régression WebSocket de réseau local nécessitant des tests de fumée, l'aperçu interne/pas de lien public, la restauration de remise d'amorçage QR, la réinitialisation de confiance TLS d'intégration, et les problèmes de mise à niveau WebSocket Tailscale Serve.
- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "iPhone pairing gateway"` a retourné une discussion sur l'appairage iPhone à distance après la rotation du jeton de passerelle, l'appairage interne/dev avec `openclaw devices list` et `openclaw devices approve <requestId>`, les problèmes d'appairage Tailscale Serve, et le même jeton `/pair` supportant les sessions d'opérateur et de nœud.
- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "device signature invalid iOS"` a retourné un fil de construction/débogage iOS du 2026-02-12 sur les paramètres de connexion invalides, le rôle `operator` par rapport à `node`, et les signatures de dispositif.
- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "TestFlight relay"` a retourné une discussion d'avril et mars 2026 indiquant que TestFlight peut recevoir une poussée via ClawPushRelay avec validation App Attest/App Store, les versions officielles/TestFlight nécessitent des installations TestFlight/App Store réelles, et les opérateurs demandaient toujours ce que `gateway.push.apns.relay.baseUrl` devrait être.
