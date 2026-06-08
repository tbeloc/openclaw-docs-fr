---
title: "iOS app - Gateway Setup and Diagnostics Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iOS app - Gateway Setup and Diagnostics Maturity Note

## Summary

L'application iOS dispose d'une surface Settings et diagnostics substantielle : sélection de passerelle, host/port/TLS manuel, intake de code de configuration et QR, bascules caméra/localisation/Talk/activation vocale, état des notifications, lignes d'accès à la confidentialité, journaux de découverte, bannières/détails de problème de passerelle, ID de requête/commandes copiables et comptage des problèmes de diagnostics. La couverture est Experimental car la preuve est principalement SwiftUI/source et tests unitaires, et non une procédure pas à pas d'application de bout en bout du premier lancement à la récupération après défaillance. La qualité est Experimental élevée car les erreurs et paramètres visibles par l'opérateur sont concrets, mais les preuves d'archive montrent que l'appairage, TLS, les permissions et le support mobile nécessitent toujours des conseils pratiques du responsable de la maintenance.

## Category Scope

Inclus dans cette catégorie :

- Bonjour/local : découverte de passerelle Bonjour/local et zone étendue
- Manual host/port : intégration manuelle de host/port et onboarding QR/code de configuration
- Gateway connect configuration persistence : comportement de persistance de la configuration de connexion de passerelle, état et vérification visible par l'opérateur.
- TLS fingerprint trust prompt : invite de confiance d'empreinte TLS et comportement d'épinglage
- Pairing approval : approbation d'appairage, authentification d'appareil/stockage de trousseau et authentification de session nœud+opérateur
- Pairing/auth diagnostics for users : diagnostics d'appairage/authentification pour les utilisateurs et les opérateurs
- Settings tab : onglet Settings, paramètres de passerelle, assistants de mise en réseau manuel, intake QR/code de configuration, bascules et demandes de permission, journaux de découverte, détails de problème de passerelle, liste de problèmes de diagnostics, état d'autorisation des notifications et actions de récupération visibles

## Features

- Bonjour/local : découverte de passerelle Bonjour/local et zone étendue
- Manual host/port : intégration manuelle de host/port et onboarding QR/code de configuration
- Gateway connect configuration persistence : comportement de persistance de la configuration de connexion de passerelle, état et vérification visible par l'opérateur.
- TLS fingerprint trust prompt : invite de confiance d'empreinte TLS et comportement d'épinglage
- Pairing approval : approbation d'appairage, authentification d'appareil/stockage de trousseau et authentification de session nœud+opérateur
- Pairing/auth diagnostics for users : diagnostics d'appairage/authentification pour les utilisateurs et les opérateurs
- Settings tab : onglet Settings, paramètres de passerelle, assistants de mise en réseau manuel, intake QR/code de configuration, bascules et demandes de permission, journaux de découverte, détails de problème de passerelle, liste de problèmes de diagnostics, état d'autorisation des notifications et actions de récupération visibles

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Experimental (41%)`
- Positive signals: Les tests unitaires couvrent les assistants de mise en réseau des paramètres, la classification du statut de passerelle, le comportement du pont de demande de permission, le basculement de point de terminaison manuel, les bascules de capacité et l'état de connexion adjacent QR/code de configuration. Les docs et README fournissent des listes de contrôle de dépannage manuel.
- Negative signals: Aucune procédure pas à pas d'interface utilisateur automatisée n'a été trouvée pour l'onboarding, la sélection de passerelle, l'analyse QR, les permissions, les diagnostics, les journaux de découverte, l'autorisation des notifications et la récupération après une défaillance d'appairage/TLS/réseau.
- Integration gaps: Besoin d'une fiche de pointage d'interface utilisateur sur appareil réel qui commence au premier lancement, se connecte via QR et host manuel, exerce les lignes de permission, enregistre les journaux de découverte, déclenche les erreurs de passerelle connues et vérifie la copie de récupération de l'opérateur.

## Quality Score

- Score: `Experimental (47%)`
- Gitcrawl reports: `iOS settings gateway` found PR #80656 for Swift device-auth compatibility with a live iOS simulator and live per-user Gateway, PR #80802 for iOS settings persistence and hardening, and issue #68581 referencing iOS-style location mode settings. `iOS permissions` found PR #40877 for main-thread warnings in CLLocationManager/SFSpeechRecognizer and several permission-adjacent records.
- Discrawl reports: `iOS settings permissions diagnostics gateway` returned no hits. Broader `iOS app` returned a same-day iOS Alpha support exchange where a `wss://<IP>:28443` QR path was likely failing iOS TLS trust because a bare IP lacked a valid certificate SAN, with guidance to use a real DNS name and valid cert.
- Good qualities: Les problèmes de passerelle ont des champs propriétaire/action/docs structurés, les feuilles de détails copient les ID de requête et les commandes, les journaux de découverte sont copiables, les paramètres distinguent TLS/host/port manuel et les diagnostics comptent les vérifications visibles du réviseur.
- Bad qualities: La récupération dépend toujours de l'interprétation d'expert de l'appairage, du jeton, de TLS, des APNs, de Bonjour et des contraintes de premier plan/arrière-plan ; il n'y a pas encore de promesse de support public ou de flux de défaillance au premier lancement entièrement guidé.
- Excluded from quality: Les tests unitaires Settings et Gateway n'ont pas été utilisés comme entrées de qualité.

## Completeness Score

- Score: `Experimental (41%)`
- Surface instructions: evaluated against `references/completeness/ios-app.md`.
- Positive signals: Les preuves archivées docs, source, test, Gitcrawl et Discrawl couvrent l'étendue de la taxonomie pour Bonjour/local, Manual host/port, Gateway connect configuration persistence, TLS fingerprint trust prompt, Pairing approval, Pairing/auth diagnostics for users, Settings tab.
- Negative signals: la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Missing capability branches: see `## Known Gaps` and `## Evidence` below for the recorded missing branches and operator-visible caveats.

## Known Gaps

- Add an iOS onboarding/settings failure-recovery scorecard with screenshots or logs for QR, manual host, TLS trust, and pairing approval.
- Surface TLS/IP certificate mismatch more directly in app copy.
- Add a single copyable diagnostics export that includes gateway config source, discovery logs, permission states, notification state, and last Gateway problem.

## Evidence

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` includes quick start, manual host/port, common errors, debugging checklist, and related docs.
- `/Users/kevinlin/code/openclaw/apps/ios/README.md` includes super-alpha limitations, exact Xcode deployment, APNs setup expectations, known issues, and a debugging checklist.
- `/Users/kevinlin/code/openclaw/docs/channels/pairing.md` documents the recommended pairing path used by iOS.

### Source

- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Design/SettingsProTab.swift` defines settings state for Gateway, manual host/port/TLS, camera, location, Talk, voice wake, diagnostics, QR, and notification status.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Settings/PrivacyAccessSectionView.swift` exposes contacts, calendar, and reminders permission actions.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Gateway/GatewayProblemView.swift` presents structured connection recovery details.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Gateway/GatewayDiscoveryDebugLogView.swift` exposes copyable discovery logs.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Status/GatewayStatusBuilder.swift` maps connection state into UI status.

### Integration tests

- No automated iOS settings/onboarding UI e2e artifact was found.
- Manual docs instruct Xcode/local device operation and troubleshooting.

### Unit tests

- `/Users/kevinlin/code/openclaw/apps/ios/Tests/SettingsNetworkingHelpersTests.swift` covers diagnostics issue counting and host/port parsing.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/GatewayStatusBuilderTests.swift` covers paused error status versus transient reconnect status.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/PermissionRequestBridgeTests.swift` covers permission request continuation behavior.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/GatewayConnectionControllerTests.swift` covers manual endpoint fallback and capability toggles.

### Gitcrawl queries

Query:

`gitcrawl search openclaw/openclaw --query "iOS settings gateway" --json`

Results:

- PR #80656 `fix(swift): keep device auth compatible with v2 gateways`.
- PR #80802 `[codex] Harden Talk, Canvas, and add macOS ambient overlay`.
- Issue #68581 `Android node: support location.enabledMode: always`, referencing iOS-style settings.

Additional query context:

- `gitcrawl search openclaw/openclaw --query "iOS permissions" --json` found PR #40877 for main-thread warnings in CLLocationManager and SFSpeechRecognizer.

### Discrawl queries

Query:

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "iOS settings permissions diagnostics gateway"`

Results:

- No hits.

Additional query context:

- `discrawl search --mode fts --limit 5 "iOS app"` found a 2026-05-29 iOS Alpha support exchange explaining that a `wss://<IP>:28443` QR path is likely to fail iOS TLS policy without a real DNS name and valid certificate SAN.
