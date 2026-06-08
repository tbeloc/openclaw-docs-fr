---
title: "Android app - Settings Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Android app - Settings Maturity Note

## Summary

Les paramètres et diagnostics Android couvrent une large surface d'opérateur : profil, paramètres de passerelle, autorisations de caméra/localisation/micro/photos/mouvement/SMS/journal d'appels/notifications, politique de transfert de notifications, vue des nœuds/appareils, état du fournisseur/modèle et diagnostics de passerelle copiables. La couverture est Alpha car la source et la couverture unitaire sont larges mais aucun scénario de récupération d'opérateur intégré n'a été trouvé. La qualité est Alpha mais plus forte que le service d'arrière-plan car l'application dispose de contrôles de sécurité clairs, de filtres de politique et de texte de diagnostic copiable.

## Category Scope

Inclus dans cette catégorie :

- Feuille de paramètres : Feuille de paramètres et écrans de détails des paramètres, UX de demande d'autorisation, contrôles de transfert de notifications, état des nœuds et appareils, diagnostics du fournisseur/modèle, préférences sécurisées et rapport de diagnostic de passerelle copiable

## Features

- Feuille de paramètres : Feuille de paramètres et écrans de détails des paramètres, UX de demande d'autorisation, contrôles de transfert de notifications, état des nœuds et appareils, diagnostics du fournisseur/modèle, préférences sécurisées et rapport de diagnostic de passerelle copiable

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Alpha (64%)`
- Positive signals: La documentation décrit les prérequis d'autorisation et les contrôles de transfert de notifications. La source implémente les lanceurs d'autorisation, les dialogues de justification/paramètres, les contrôles de liste d'autorisation/blocage/heures calmes/limite de débit/session de notification, les panneaux d'état des nœuds/appareils et la copie de rapport de diagnostic. Les tests unitaires couvrent plusieurs paramètres et assistants de politique.
- Negative signals: Aucun flux de récupération d'opérateur Android intégré n'a été trouvé pour « Passerelle hors ligne », « échec d'appairage/authentification », « autorisation manquante », « écouteur de notification désactivé » et « capacité de nœud indisponible » à partir d'un chemin d'interface utilisateur.
- Integration gaps: Besoin d'un scénario de paramètres/diagnostics qui commence par des défaillances courantes, copie les diagnostics, modifie les autorisations/politique, reconnecte la passerelle et vérifie les changements d'état de commande/capacité correspondants.

## Quality Score

- Score: `Alpha (66%)`
- Gitcrawl reports: `Android light mode theme toggle` found issue #87688 requesting a light mode/theme toggle. More capability-specific searches found future Health Connect and Google Home requests, which imply settings will need more capability management as Android expands.
- Discrawl reports: `Android settings permissions diagnostics notification forwarding` returned no direct hits.
- Good qualities: Les invites d'autorisation sont centralisées et peuvent afficher des dialogues de justification/paramètres ; le transfert de notifications dispose d'une liste d'autorisation/blocage, d'heures calmes, de limitation de débit, de clé de session, d'une gestion plus sûre des auto-paquets et d'une interface de sélecteur d'applications ; le texte de diagnostic de passerelle indique aux utilisateurs quelles commandes et faits fournir.
- Bad qualities: La récupération d'opérateur est répartie sur plusieurs écrans, la personnalisation du thème/accessibilité est incomplète et il n'y a pas de flux en direct enregistré reliant les changements de paramètres aux changements de capacité de passerelle/nœud.
- Excluded from quality: La couverture des tests et la preuve du flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer la qualité.

## Completeness Score

- Score: `Alpha (64%)`
- Surface instructions: evaluated against `references/completeness/android-app.md`.
- Positive signals: Les documents archivés, la source, les tests, Gitcrawl et les preuves Discrawl couvrent l'étendue de la taxonomie pour la feuille de paramètres.
- Negative signals: La note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Missing capability branches: see `## Known Gaps` and `## Evidence` below for the recorded missing branches and operator-visible caveats.

## Known Gaps

- Ajouter un guide de dépannage de diagnostics Android compact pour la connexion, les autorisations, le transfert de notifications et la disponibilité des commandes de nœud.
- Ajouter une preuve en direct que les bascules de paramètres mettent à jour les capacités annoncées sans état de passerelle obsolète.
- Décider si les options de thème/accessibilité font partie de la promesse de support de l'application Android avant la promotion.

## Evidence

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/android.md` documents Android permissions, notification forwarding controls, connection diagnostics, and related troubleshooting links.
- `/Users/kevinlin/code/openclaw/apps/android/README.md` documents rebuild items for settings restyle, permission requests in onboarding/settings, push notifications, security hardening, and Play restricted permissions.

### Source

- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/ui/SettingsSheet.kt` implements broad settings and permission controls, notification forwarding UI, assistant role state, camera/location/mic/photos/motion/SMS/call-log availability, and installed-app picker state.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/ui/NodesDevicesSettingsScreen.kt` shows live nodes, paired devices, pending device requests, status badges, and refresh/error states.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/PermissionRequester.kt` centralizes missing-permission requests, rationale dialogs, timeouts, and settings redirects.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/NotificationForwardingPolicy.kt` implements package allow/block filtering, quiet-hours evaluation, and burst limiting.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/ui/GatewayDiagnostics.kt` builds a copyable diagnostic prompt with screen, app version, device, Android SDK, gateway address, and status/error.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/SecurePrefs.kt` persists app, Gateway, notification, and device settings.

### Integration tests

- No integrated Android settings/operator recovery scenario was found.
- `/Users/kevinlin/code/openclaw/src/gateway/android-node.capabilities.live.test.ts` indirectly depends on settings-controlled command availability and policy allowlists.

### Unit tests

- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/PermissionRequesterTest.kt`, `NotificationForwardingPolicyTest.kt`, `SecurePrefsTest.kt`, and `SecurePrefsNotificationForwardingTest.kt` cover permission and settings helpers.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/ui/SettingsSheetNotificationAppsTest.kt`, `ProviderModelStatusTest.kt`, and `GatewayConfigResolverTest.kt` cover settings UI helpers.

### Gitcrawl queries

Query:

`gitcrawl search openclaw/openclaw --query "Android light mode theme toggle" --json`

Results:

- Issue #87688 `Android app: Add light mode / theme toggle`.
- Issue #28300 `Theme Customization System - Preset Themes + Custom Theme Studio` as adjacent theme work.

Query:

`gitcrawl search openclaw/openclaw --query "Android app settings permissions diagnostics" --json`

Results:

- No direct hits.

### Discrawl queries

Query:

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "Android settings permissions diagnostics notification forwarding"`

Results:

- No direct hits.
