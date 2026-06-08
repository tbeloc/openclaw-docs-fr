---
title: "Android app - Connection Setup Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Android app - Connection Setup Maturity Note

## Résumé

L'appairage Android et la sécurité de la passerelle ont une profondeur de mise en œuvre substantielle : flux de code de configuration/manuel, découverte mDNS et DNS-SD large bande, validation de point de terminaison sécurisé, persistance de jeton d'appareil, gestion d'empreinte TLS, rôles de nœud et d'opérateur, et politique de reconnexion. La couverture est Alpha proche de Beta car les tests source et unitaires sont solides mais la preuve d'appairage Android en direct est précondition plutôt que clé en main. La qualité reste Alpha car les preuves d'archive montrent une confusion répétée de l'opérateur autour de l'authentification, de l'adressage LAN, de l'asymétrie de protocole/version et de l'analyse manuelle `ws://`.

## Portée de la catégorie

Inclus dans cette catégorie :

- Découverte de passerelle : découverte de passerelle, analyse de code de configuration et de point de terminaison manuel, configuration de connexion WS/WSS, décisions de confiance TLS, identité d'appareil, jetons d'appareil stockés, authentification de nœud/opérateur et gestion des erreurs de connexion

## Fonctionnalités

- Découverte de passerelle : découverte de passerelle, analyse de code de configuration et de point de terminaison manuel, configuration de connexion WS/WSS, décisions de confiance TLS, identité d'appareil, jetons d'appareil stockés, authentification de nœud/opérateur et gestion des erreurs de connexion

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (68%)`
- Signaux positifs : la documentation décrit mDNS, connexion par code de configuration/manuel, règles de point de terminaison distant sécurisé, guide Tailscale Serve, commandes d'approbation d'appairage, reconnexion automatique et vérifications d'état de nœud. Les tests unitaires couvrent l'analyse de point de terminaison, les charges utiles d'authentification, le stockage de jeton, le nettoyage de sonde TLS, la reconnexion et la logique de flux de configuration.
- Signaux négatifs : la suite de capacités Android en direct principale suppose que l'application est déjà installée, accessible, appairée, approuvée et au premier plan. Aucun scénario de connexion à l'approbation en direct Android au premier démarrage propre n'a été trouvé.
- Lacunes d'intégration : besoin d'un scénario en direct unique qui démarre une passerelle fraîche, connecte Android par code de configuration et URL manuelle, exerce la politique de confiance/texte clair TLS, approuve l'appairage, vérifie les sessions de nœud/opérateur et enregistre la reconnexion après l'échec de l'authentification.

## Score de qualité

- Score : `Alpha (64%)`
- Rapports Gitcrawl : `Android pairing websocket TLS manual LAN setup protocol mismatch` a trouvé le problème #87216 pour l'analyse d'analyse de configuration LAN manuelle `ws://` en tant qu'hôte `ws`. La recherche plus large `Android app` a également surfacé #85966 pour la fermeture WebSocket silencieuse après l'appairage de nœud et #78807 pour l'authentification d'appairage LAN privé.
- Rapports Discrawl : la recherche a trouvé un commentaire du miroir GitHub du 7 mars sur #16638 où l'appairage Android avec `gateway.auth.token` a toujours atteint `device signature invalid`, plus un fil de support de février guidant un utilisateur à travers le diagnostic IP LAN, la réachabilité et l'authentification/appairage.
- Bonnes qualités : l'analyseur de point de terminaison bloque les `ws://` distants non sécurisés tout en permettant la boucle locale, le pont d'émulateur et les hôtes LAN privés ; les jetons d'appareil stockés sont limités par appareil et rôle ; les indices TXT de découverte ne sont pas traités comme des épingles TLS faisant autorité ; les rôles de nœud et d'opérateur sont séparés.
- Mauvaises qualités : la surface d'échec visible par l'utilisateur est toujours facile à atteindre : mauvais hôte LAN, authentification de jeton, protocole obsolète, confiance TLS et états de nouvelle tentative d'appairage peuvent tous ressembler à un échec de connexion générique.
- Exclu de la qualité : la couverture des tests et la preuve de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Alpha (68%)`
- Instructions de surface : évaluées par rapport à `references/completeness/android-app.md`.
- Signaux positifs : les preuves d'archive, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la découverte de passerelle.
- Signaux négatifs : la note d'archive a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture d'archive.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un test de fumée d'appairage au premier démarrage scriptée pour le code de configuration, le LAN manuel et le WSS distant.
- Améliorer la copie d'opérateur autour de l'appairage/authentification par rapport à une adresse incorrecte par rapport à la confiance TLS.
- Garder visible l'asymétrie de version Play Store dans les erreurs d'appairage afin que les anciens clients échouent avec un message de mise à niveau exploitable.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/android.md` documente le chemin WebSocket Android vers passerelle, le rôle d'appairage d'appareil, les règles de point de terminaison sécurisé, les modes de code de configuration/manuel, l'approbation d'appairage, la reconnexion automatique et la vérification d'état.
- `/Users/kevinlin/code/openclaw/apps/android/README.md` documente les tests de passerelle USB uniquement avec `adb reverse` et les étapes de connexion/appairage.
- `/Users/kevinlin/code/openclaw/docs/gateway/bonjour.md` est lié depuis le runbook Android pour le débogage de découverte.

### Source

- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/gateway/GatewayDiscovery.kt` implémente la découverte NSD/mDNS locale plus la découverte DNS-SD large bande optionnelle.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/ui/GatewayConfigResolver.kt` décode les codes de configuration, analyse les points de terminaison manuels et applique les règles d'URL distantes sécurisées.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/gateway/GatewaySession.kt` gère la connexion WebSocket, les sources d'authentification de nœud/opérateur, les RPC, la reconnexion et la gestion des appels.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/gateway/DeviceAuthStore.kt` persiste les jetons d'appareil et les étendues par appareil et rôle normalisés.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/node/ConnectionManager.kt` construit les options de connexion de nœud/opérateur et résout les paramètres TLS.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/android-node.capabilities.live.test.ts` connecte un client de passerelle, sélectionne un nœud Android, vérifie l'état appairé/connecté et utilise la configuration distante pour les exécutions distantes, mais nécessite une configuration manuelle d'abord.
- Aucun e2e d'appairage au premier démarrage Android propre n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/gateway/GatewaySessionReconnectTest.kt` couvre le comportement de pause/nouvelle tentative de reconnexion et d'appairage requis.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/gateway/GatewaySessionInvokeTest.kt`, `GatewaySessionInvokeTimeoutTest.kt`, `DeviceAuthPayloadTest.kt`, `DeviceAuthStoreTest.kt`, `GatewayBootstrapAuthTest.kt`, `GatewayConfigResolverTest.kt` et `OnboardingFlowLogicTest.kt` couvrent la logique d'authentification, d'appel, d'analyse et d'intégration de base.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "Android pairing websocket TLS manual LAN setup protocol mismatch" --json`

Résultats :

- Problème #87216 `Android manual LAN setup parses ws:// as host ws and resolves http://ws:<port>`.

Contexte de requête supplémentaire :

- `gitcrawl search openclaw/openclaw --query "Android app" --json` a trouvé #85966 `Android UI/operator WebSocket closes silently ... after successful node pair` et #78807 `fix(mobile): allow private LAN pairing auth`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "Android manual LAN ws host pairing"`

Résultats :

- Commentaire du miroir GitHub du 7 mars 2026 sur #16638 signale que le nœud Android ne peut pas s'appairer lorsque `gateway.auth.token` est configuré et atteint toujours `device signature invalid`.
- Fil de support du 6 février 2026 explique l'IP LAN, la réachabilité, le pare-feu/isolement client et l'authentification/appairage comme bloqueurs de connexion Android probables.
