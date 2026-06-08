---
title: "iOS app - Location, Motion, Calendar, Contacts, and Reminders Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iOS app - Location, Motion, Calendar, Contacts, and Reminders Maturity Note

## Résumé

L'application iOS expose des commandes de contexte personnel significatives : localisation actuelle, mises à jour de localisation importante, mouvement/podomètre, recherche/ajout de contacts, événements calendrier/ajout, et liste de rappels/ajout. La couverture est faible Expérimental car ces fonctionnalités disposent de preuves de source et d'unité plus un script de nœud manuel, mais pas de fiche de notation QA d'appareil actuelle pour les états de permission Apple, la localisation en arrière-plan, ou les effets d'automatisation. La qualité est mi-Expérimental car les chemins source sont directs et limités par permission, tandis que les preuves d'archive montrent que la localisation en arrière-plan, les APNs wake, les Raccourcis, HealthKit, et les limites de plateforme Apple restent des points actifs de confusion des opérateurs.

## Portée de la catégorie

- Modes de localisation, localisation actuelle, événements de localisation importante, activité de mouvement et podomètre, contacts, calendrier, rappels, ponts de demande de permission, et charges utiles de commande de contexte personnel.
- Hors de portée : la livraison APNs elle-même, les travaux futurs HealthKit, et la localisation du service de premier plan Android.

## Fonctionnalités

- Modes de localisation : Modes de localisation, localisation actuelle, événements de localisation importante, activité de mouvement et podomètre, contacts, calendrier, rappels, ponts de demande de permission, et charges utiles de commande de contexte personnel

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (37%)`
- Signaux positifs : La documentation décrit les modes de localisation et l'intention d'automatisation du mouvement. `scripts/dev/ios-node-e2e.ts` peut invoquer des commandes de contacts, calendrier, rappels, mouvement et photos contre un nœud connecté. Les tests Swift couvrent l'annonce de capacité de localisation et le comportement du helper de permission.
- Signaux négatifs : Aucune preuve d'appareil automatisée n'a été trouvée pour la localisation Toujours, la livraison de localisation importante en arrière-plan, la récupération de permission refusée, les mutations calendrier/rappel, les écritures de contact, la permission de mouvement, ou les automatisations de type géofence.
- Lacunes d'intégration : Besoin d'une fiche de notation de contexte personnel d'appareil réel qui exerce chaque état de permission et vérifie les événements Gateway après les transitions de premier plan et d'arrière-plan.

## Score de qualité

- Score : `Expérimental (45%)`
- Rapports Gitcrawl : `iOS background location` a trouvé le problème #86217 questionnant si les revendications de localisation en arrière-plan iOS devraient inclure `UIBackgroundModes=location`, PR #63123 pour le support alive en arrière-plan, problème #68581 référençant les modes de localisation de style iOS, et problème #46664 pour la file d'attente de commande hors ligne.
- Rapports Discrawl : `iOS background location` a trouvé un fil de support sur les tests de compagnon iOS BetterClaw/background, un fil iOS/watchOS de mars où APNs wake a échoué avec `path=no-registration` pour le `nodes location get` en arrière-plan, et un commentaire d'opérateur que la localisation de premier plan fonctionne tandis que le wake en arrière-plan reste la partie difficile.
- Bonnes qualités : Les portes de mode de localisation distinguent `off`, premier plan, et `always` ; le `location.get` en arrière-plan nécessite l'autorisation Always ; les mises à jour de localisation importante émettent `location.update` ; le code EventKit et Contacts demande l'accès de portée minimale où possible.
- Mauvaises qualités : La documentation et la source ne s'accordent pas sur le fait que la localisation en arrière-plan dispose de tous les modes de plateforme requis, la localisation en arrière-plan dépend du comportement push/wake, et plusieurs fonctionnalités de contexte personnel ont besoin d'attentes de produit plus claires sous les restrictions Apple.
- Exclu de la qualité : Les tests unitaires et le script live manuel n'ont pas été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Expérimental (37%)`
- Instructions de surface : évaluées par rapport à `references/completeness/ios-app.md`.
- Signaux positifs : les preuves de documentation archivée, source, test, Gitcrawl et Discrawl couvrent la portée de taxonomie pour les modes de localisation.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Décider et documenter si la localisation en arrière-plan iOS nécessite d'ajouter `UIBackgroundModes=location` pour la promesse de support actuelle.
- Ajouter QA d'appareil réel pour le wake de localisation importante, `location.update`, et `nodes location get` en arrière-plan.
- Clarifier les attentes adjacentes non supportées telles que la lecture de notifications, HealthKit, et le GPS continu.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` documente la localisation, le comportement alive en arrière-plan, l'automatisation de localisation, et les limites d'arrière-plan communes.
- `/Users/kevinlin/code/openclaw/apps/ios/README.md` documente les tests d'automatisation de localisation, la permission Always, le mouvement significatif, et les effets Gateway attendus.

### Source

- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Location/LocationService.swift` implémente la localisation actuelle, l'autorisation Always, les flux de mise à jour, et la surveillance de localisation importante.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Location/SignificantLocationMonitor.swift` envoie les événements `location.update` à la Gateway.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Contacts/ContactsService.swift`, `CalendarService.swift`, `RemindersService.swift`, et `MotionService.swift` implémentent les familles de commande de contexte personnel.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Settings/PrivacyAccessSectionView.swift` expose les actions de permission pour les contacts, le calendrier, et les rappels.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/dev/ios-node-e2e.ts` inclut les vérifications de commande de contacts, calendrier, rappels, mouvement et photos contre un nœud iOS connecté.
- Aucun artefact e2e de localisation en arrière-plan d'appareil réel automatisé ou de permission de données personnelles n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/ios/Tests/GatewayConnectionControllerTests.swift` vérifie la capacité de localisation et l'annonce de commande.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/PermissionRequestBridgeTests.swift` vérifie le comportement de continuation de permission.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/SettingsNetworkingHelpersTests.swift` couvre les diagnostics et le comportement du helper de paramètres connexe.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "iOS background location" --json`

Résultats :

- Problème #86217 `Question: should iOS background location claims include UIBackgroundModes=location?`.
- PR #63123 `feat(ios): add background alive beacon support`.
- Problème #46664 `[Feature]: Offline Command Queue for iOS/Android Node App`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "iOS background location"`

Résultats :

- Le rapport du 1er mai note que le focus de test de compagnon iOS BetterClaw/background tourne autour de l'intégration, des reconnexions, de la batterie, des Raccourcis, et des géofences.
- Le fil iOS/watchOS de mars rapporte que le `nodes location get` de premier plan fonctionne, mais le wake en arrière-plan échoue avec APNs `path=no-registration`.
- La note de support de février dit que la localisation est supportée avec les contraintes iOS While Using versus Always et que HealthKit n'est pas intégré dans la surface actuelle de l'application iOS.
