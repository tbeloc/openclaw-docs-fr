---
title: "watchOS companion surfaces - Delivery and Recovery Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# watchOS companion surfaces - Delivery and Recovery Maturity Note

## Summary

Le chemin d'approbation de la montre dépend du réveil de l'iPhone, de la reconnexion, de la récupération de l'état d'approbation en attente et du nettoyage des invites d'approbation résolues/obsolètes. Le code source et les tests couvrent des éléments importants de ce chemin de récupération. La couverture est Alpha à la limite inférieure car la logique de récupération est implémentée et testée par morceaux, mais aucune preuve TestFlight/APNs/montre n'est vérifiée.

La qualité est Alpha car la conception tient compte de la poussée soutenue par relais, des APNs directs, du nettoyage obsolète et des ID de récupération en attente, mais la configuration opérationnelle reste complexe et interne.

## Category Scope

Inclus dans cette catégorie :

- Enregistrement du relais/direct APNs tel qu'il affecte : l'enregistrement du relais/direct APNs tel qu'il affecte le réveil/la récupération d'approbation de la montre
- Poussée silencieuse : poussée silencieuse, actualisation en arrière-plan et chemins de réveil par localisation importante
- ID de récupération d'approbation en attente : ID de récupération d'approbation en attente, actualisation d'instantané et nettoyage résolu/obsolète
- Approbation d'exécution iOS côté passerelle : approbation d'exécution iOS côté passerelle ciblage APNs
- Transport WatchConnectivity côté iPhone : transport WatchConnectivity côté iPhone et instantané d'état
- Activation du récepteur côté montre : activation du récepteur côté montre et gestion de la charge utile entrante
- Secours de livraison parmi les messages accessibles : secours de livraison parmi les messages accessibles, informations utilisateur en file d'attente et instantanés de contexte d'application

## Features

- Enregistrement du relais/direct APNs tel qu'il affecte : l'enregistrement du relais/direct APNs tel qu'il affecte le réveil/la récupération d'approbation de la montre
- Poussée silencieuse : poussée silencieuse, actualisation en arrière-plan et chemins de réveil par localisation importante
- ID de récupération d'approbation en attente : ID de récupération d'approbation en attente, actualisation d'instantané et nettoyage résolu/obsolète
- Approbation d'exécution iOS côté passerelle : approbation d'exécution iOS côté passerelle ciblage APNs
- Transport WatchConnectivity côté iPhone : transport WatchConnectivity côté iPhone et instantané d'état
- Activation du récepteur côté montre : activation du récepteur côté montre et gestion de la charge utile entrante
- Secours de livraison parmi les messages accessibles : secours de livraison parmi les messages accessibles, informations utilisateur en file d'attente et instantanés de contexte d'application

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Alpha (50%)`
- Positive signals: Les tests iOS couvrent la reconnexion consciente de l'arrière-plan pour la montre et les chemins de poussée, l'hydratation de l'ID de récupération en attente, le nettoyage des notifications de poussée résolues et la normalisation du déclenchement en arrière-plan. Les tests de passerelle couvrent le ciblage d'approbation APNs iOS, les décisions d'authentification relais/direct et le filtrage d'enregistrement.
- Negative signals: Aucune APNs en direct, TestFlight ou scénario de récupération de montre réelle n'a été trouvé.
- Integration gaps: Besoin d'un scénario de build officiel/TestFlight avec APNs soutenu par relais, un iPhone en arrière-plan, une montre accessible, une approbation en attente, réveil par poussée, chargement d'instantané de montre, résolution de montre et nettoyage de poussée résolue.

## Quality Score

- Score: `Alpha (60%)`
- Gitcrawl reports: `gitcrawl search openclaw/openclaw --query "iOS Watch exec approvals" --json` returned no hits, and direct PR-number searches for older watch changelog items returned no hits. Cette absence est neutre après des requêtes de fraîcheur et spécifiques aux fonctionnalités réussies.
- Discrawl reports: `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS app watch"` found a PR #61757 review comment warning that foreground snapshot-request skipping could leave recovery IDs stuck after a failed push request. `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "WatchOS support"` summarized background behavior as limited by iOS and said watchOS exec approvals need manual compilation plus local APNs config.
- Good qualities: L'implémentation traite la récupération en arrière-plan comme un chemin distinct, persiste les ID de récupération d'approbation en attente, nettoie les notifications résolues, distingue les APNs directs par rapport aux APNs relayés et nécessite une portée d'approbation d'opérateur avant que les approbations de passerelle ne ciblent les appareils iOS.
- Bad qualities: La configuration traverse les droits Apple, la configuration du relais/direct APNs, la portée de l'opérateur de passerelle, les limites d'arrière-plan iOS et WatchConnectivity. C'est trop complexe pour une fonctionnalité publique sans runbook et fumée de version.
- Excluded from quality: La couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la qualité.

## Completeness Score

- Score: `Alpha (50%)`
- Surface instructions: evaluated against `references/completeness/watchos-companion-surfaces.md`.
- Positive signals: Les docs archivées, le code source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour l'enregistrement du relais/direct APNs tel qu'il affecte, la poussée silencieuse, les ID de récupération d'approbation en attente, l'approbation d'exécution iOS côté passerelle, le transport WatchConnectivity côté iPhone, l'activation du récepteur côté montre, le secours de livraison parmi les messages accessibles.
- Negative signals: la note archivée a précédé le score de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Missing capability branches: see `## Known Gaps` and `## Evidence` below for the recorded missing branches and operator-visible caveats.

## Known Gaps

- Add a live APNs/watch approval recovery runbook and proof artifact.
- Document direct APNs versus relay-backed behavior specifically for watch approval recovery.
- Add a regression scenario for the foreground snapshot-request recovery gap discussed in PR #61757.

## Evidence

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` documents relay-backed push, direct APNs for local/manual builds, background alive beacons, and relay trust model.
- `/Users/kevinlin/code/openclaw/apps/ios/README.md` documents APNs expectations for local/manual builds and official builds.

### Source

- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Model/NodeAppModel.swift` handles silent push wakes, background refresh wakes, significant-location wakes, APNs registration, push-relay gateway identity, exec approval requested/resolved pushes, pending watch recovery IDs, and watch snapshot sync.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Push/ExecApprovalNotificationBridge.swift` parses exec approval notification payloads and removes matching notifications.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Push/PushRegistrationManager.swift` and `PushRelayClient.swift` implement relay/direct registration support.
- `/Users/kevinlin/code/openclaw/src/gateway/exec-approval-ios-push.ts` targets paired iOS/iPadOS operator devices with `operator.approvals` scope and sends direct or relay APNs approval alerts/resolved wakes.

### Integration tests

- No live APNs or real watch recovery scenario was found.

### Unit tests

- `/Users/kevinlin/code/openclaw/apps/ios/Tests/NodeAppModelInvokeTests.swift` covers background-aware watch/push reconnect selection and pending watch recovery behavior.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/ExecApprovalNotificationBridgeTests.swift` covers resolved-push cleanup.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/BackgroundAliveBeaconTests.swift` covers wake trigger normalization.
- `/Users/kevinlin/code/openclaw/src/gateway/exec-approval-ios-push.test.ts` covers Gateway-side APNs target selection, operator approval scope, direct/relay config handling, and delivery accounting.

### Gitcrawl queries

Query:

`gitcrawl search openclaw/openclaw --query "iOS Watch exec approvals" --json`

Results:

- No hits.

Query:

`gitcrawl search openclaw/openclaw --query "61757" --json`

Results:

- No hits from the local gitcrawl store.

### Discrawl queries

Query:

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS app watch"`

Results:

- PR #61757 review comment highlighted a recovery gap where skipping watch snapshot requests in foreground could leave pending recovery IDs stuck after a failed push request.
- Discord summary said no public TestFlight path exists and watchOS exec approvals need manual build/APNs setup.

Query:

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "WatchOS support"`

Results:

- Maintainer-preview summary flagged iOS background limits, manual APNs config, and lack of public TestFlight.
