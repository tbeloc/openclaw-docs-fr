---
title: "Application iOS - Note de maturité des notifications et de l'arrière-plan"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application iOS - Note de maturité des notifications et de l'arrière-plan

## Résumé

L'application iOS possède l'un des flux les plus explicitement conçus pour mobile uniquement dans OpenClaw : enregistrement APNs, APNs locaux/directs pour les builds manuels, enregistrement push avec relais pour les builds officiels/TestFlight, App Attest plus preuve StoreKit, délégation d'identité de passerelle, balises de vie en arrière-plan, gestion de réveil par localisation importante, et état de connexion Live Activity. La couverture est Expérimentale car des tests de relais et de passerelle existent, mais il n'y a actuellement pas de scorecard d'enregistrement push TestFlight de bout en bout et de réveil en arrière-plan. La qualité est Expérimentale car le modèle de confiance est soigneusement documenté, tandis que les preuves d'archive montrent que les identifiants APNs, l'enregistrement de réveil en arrière-plan et la politique réseau iOS restent des risques de support actifs.

## Portée de la catégorie

Inclus dans cette catégorie :

- Enregistrement APNs et livraison par relais : enregistrement APNs direct et avec relais, confiance du relais push, poignées de relais stockées, fenêtres de vie en arrière-plan, et mises à jour Live Activity.

## Fonctionnalités

- Enregistrement APNs et livraison par relais : enregistrement APNs direct et avec relais, confiance du relais push, poignées de relais stockées, fenêtres de vie en arrière-plan, et mises à jour Live Activity.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimentale (44%)`
- Signaux positifs : la documentation donne le flux de relais officiel/TestFlight ; les tests TypeScript couvrent la signature et la configuration du relais APNs ; les tests Swift couvrent le comportement de la charge utile de vie en arrière-plan ; la source de l'application enregistre APNs après l'appairage et utilise l'identité de passerelle pour le mode relais.
- Signaux négatifs : aucune preuve TestFlight en direct actuelle n'a été trouvée qui installe une build officielle, s'appaire à une passerelle avec une URL de relais correspondante, enregistre APNs avec relais, envoie `push.test`, réveille l'application en arrière-plan, et enregistre `node.presence.alive`.
- Lacunes d'intégration : besoin d'un scorecard de relais TestFlight avec enregistrement de relais, push.test, réveil de reconnexion, push silencieux, réveil par localisation importante, et transitions d'état Live Activity.

## Score de qualité

- Score : `Expérimentale (46%)`
- Rapports Gitcrawl : `iOS APNs relay push` a trouvé la PR #81402 mentionnant les enregistrements APNs dans l'état d'exécution. `iOS background alive` a trouvé la PR #63123 pour le support de balise de vie en arrière-plan. `APNs` a également trouvé le problème #61041 et le problème #67031 liés aux limites push/média et à la PR #81402.
- Rapports Discrawl : `iOS APNs relay background alive push` n'a retourné aucun résultat. `iOS background location` a trouvé un fil de support iOS/watchOS de mars où le réveil APNs de la passerelle a tenté `node wake` mais a échoué avec `path=no-registration`, et a demandé comment les utilisateurs auto-hébergés devraient configurer les identifiants APNs.
- Bonnes qualités : l'enregistrement du relais nécessite une distribution officielle, des APNs de production, App Attest, une preuve de transaction d'application StoreKit, et une délégation à une identité de passerelle appairée. L'expéditeur de relais de la passerelle signe les envois de relais et rejette les URL de relais non sécurisées/malformées.
- Mauvaises qualités : le support push a plusieurs modes opérationnels et surfaces d'identifiants ; les builds locaux ont toujours besoin d'identifiants APNs directs, les builds officiels ont besoin d'URL de relais correspondantes, et le succès du réveil en arrière-plan est difficile à distinguer sans un scorecard dédié.
- Exclu de la qualité : les tests de relais APNs et les tests unitaires de balise en arrière-plan n'ont pas été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Expérimentale (44%)`
- Instructions de surface : évaluées par rapport à `references/completeness/ios-app.md`.
- Signaux positifs : les preuves de docs archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'enregistrement APNs et la livraison par relais.
- Signaux négatifs : la note archivée a précédé le scoring de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un scorecard push TestFlight actuel pour l'enregistrement de relais, le stockage de passerelle, `push.test`, le réveil en arrière-plan, et la gestion de balise de vie.
- Documenter la configuration APNs directe auto-hébergée par rapport à la configuration de relais officielle comme arbres de décision d'opérateur séparés.
- Ajouter des diagnostics d'opérateur pour `path=no-registration`, poignées de relais obsolètes, URL de base de relais non correspondantes, et incompatibilités de sujet production/sandbox.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` documente le push avec relais, le flux d'authentification/confiance, APNs directs pour les builds locaux, les balises de vie en arrière-plan, et les étapes de l'opérateur.
- `/Users/kevinlin/code/openclaw/apps/ios/README.md` documente les attentes APNs pour les builds locaux/manuels et officiels.
- `/Users/kevinlin/code/openclaw/docs/gateway/configuration.md` documente `gateway.push.apns.relay.baseUrl` et le flux de build officiel avec relais.

### Source

- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Push/PushRegistrationManager.swift` construit les charges utiles d'enregistrement de passerelle directes et avec relais.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Push/PushRelayClient.swift` s'enregistre auprès du relais en utilisant App Attest et la preuve de transaction d'application StoreKit.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Push/BackgroundAliveBeacon.swift` enveloppe les charges utiles `node.presence.alive`.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Model/NodeAppModel.swift` enregistre APNs après la connexion de l'opérateur, gère les réveils en arrière-plan, et coordonne la suppression de reconnexion.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/LiveActivity/LiveActivityManager.swift` suit les états de connexion et d'attention.
- `/Users/kevinlin/code/openclaw/src/infra/push-apns.ts` et `push-apns.relay.ts` implémentent l'enregistrement APNs côté passerelle et l'envoi de relais.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/infra/push-apns-http2.live.test.ts` existe pour le comportement en direct HTTP/2 APNs direct, mais ce n'est pas une preuve de relais push TestFlight iOS.
- Aucun artefact de relais push TestFlight iOS de bout en bout ou de réveil en arrière-plan n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/ios/Tests/BackgroundAliveBeaconTests.swift` couvre l'enveloppe de charge utile de vie et la gestion des accusés de réception de passerelle ancienne.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/ExecApprovalNotificationBridgeTests.swift` couvre le comportement adjacent du pont de notification push.
- `/Users/kevinlin/code/openclaw/src/infra/push-apns.relay.test.ts`, `push-apns.auth.test.ts`, `push-apns.store.test.ts`, et `push-apns.test.ts` couvrent la logique de relais APNs, d'authentification, de stockage et d'enregistrement de la passerelle.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "iOS background alive" --json`

Résultats :

- PR #63123 `feat(ios): add background alive beacon support`.

Contexte de requête supplémentaire :

- `gitcrawl search openclaw/openclaw --query "iOS APNs relay push" --json` a trouvé la PR #81402 avec des enregistrements APNs dans l'inventaire de migration d'état SQLite.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "iOS APNs relay background alive push"`

Résultats :

- Aucun résultat.

Contexte de requête supplémentaire :

- `discrawl search --mode fts --limit 5 "iOS background location"` a trouvé un fil de support iOS/watchOS de mars où `nodes location get` en arrière-plan dépendait du réveil APNs mais a échoué avec `path=no-registration`.
