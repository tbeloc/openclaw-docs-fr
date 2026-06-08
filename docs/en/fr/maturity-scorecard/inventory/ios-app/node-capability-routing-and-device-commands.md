---
title: "iOS app - Device Commands Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iOS app - Device Commands Maturity Note

## Résumé

Le nœud iOS dispose d'une large surface de commandes et d'un routeur d'invocation centralisé pour les commandes de périphérique, système, chat, montre, photos, contacts, calendrier, rappels, mouvement, localisation, caméra, écran, Canvas et Talk. La couverture reste Expérimentale car la preuve en direct est un script exécuté par un responsable de maintenance sur un nœud iOS déjà connecté, et non un test de fumée de version reproductible qui provisionne, apparie, met au premier plan et exerce la matrice de commandes complète. La qualité est près du sommet de la catégorie Expérimentale car le routage des commandes est explicite et les erreurs de premier plan/arrière-plan sont productisées, mais les preuves d'archive montrent toujours des demandes non résolues concernant la mise en file d'attente hors ligne et la disponibilité des capacités mobiles.

## Portée de la catégorie

Inclus dans cette catégorie :

- Modes de localisation : modes de localisation, localisation actuelle, événements de localisation significatifs, activité de mouvement et podomètre, contacts, calendrier, rappels, ponts de demande de permission et charges utiles de commande de contexte personnel
- Gestion des commandes de périphérique : gestion des commandes de périphérique iOS, contrôle d'accès au premier plan/arrière-plan, spécifications de commandes et visibilité des capacités.

## Fonctionnalités

- Modes de localisation : modes de localisation, localisation actuelle, événements de localisation significatifs, activité de mouvement et podomètre, contacts, calendrier, rappels, ponts de demande de permission et charges utiles de commande de contexte personnel
- Gestion des commandes de périphérique : gestion des commandes de périphérique iOS, contrôle d'accès au premier plan/arrière-plan, spécifications de commandes et visibilité des capacités.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Experimental (45%)`
- Signaux positifs : `scripts/dev/ios-node-e2e.ts` peut se connecter en tant qu'opérateur, sélectionner un nœud iOS connecté et invoquer des commandes représentatives incluant `device.info`, `device.status`, `system.notify`, contacts, calendrier, rappels, mouvement, photos, caméra et enregistrement d'écran. Les tests Swift couvrent l'annonce des capacités et les décisions de routage.
- Signaux négatifs : le script en direct nécessite un jeton Gateway déjà accessible et un nœud iOS connecté/appairable, et il ne semble pas être intégré à un CI récurrent ou à un tableau de bord de version. Aucun artefact d'exécution de matrice de commandes de périphérique complet n'a été trouvé pour la ligne actuelle.
- Lacunes d'intégration : besoin d'une fiche d'évaluation TestFlight ou de périphérique réel qui commence par l'installation/l'appairage, vérifie les commandes annoncées, exécute les commandes sûres, exécute les commandes réservées au premier plan en étant au premier plan, vérifie les défaillances attendues en arrière-plan et enregistre les états de permission.

## Score de qualité

- Score : `Experimental (48%)`
- Rapports Gitcrawl : `iOS node capabilities` a trouvé la PR #63123 pour le support de balise en arrière-plan et le problème #46664 demandant une file d'attente de commandes hors ligne pour les applications de nœud iOS/Android. `iOS node commands foreground background` et `NODE_BACKGROUND_UNAVAILABLE` n'ont retourné aucun résultat direct.
- Rapports Discrawl : `iOS node commands foreground background unavailable` a trouvé une explication de support indiquant que les commandes Canvas, caméra et écran sont réservées au premier plan sur iOS/Android et échouent généralement avec `NODE_BACKGROUND_UNAVAILABLE` lorsque l'application est en arrière-plan.
- Bonnes qualités : le routage des commandes est centralisé, les commandes inconnues retournent des erreurs de demande invalide explicites, les commandes réservées au premier plan partagent une porte d'arrière-plan commune, les commandes shell d'hôte dangereuses sont absentes de l'annonce des commandes iOS et les services ont des erreurs de permission délimitées.
- Mauvaises qualités : l'inventaire des commandes est large pour un aperçu interne, et les opérateurs ont toujours besoin d'une meilleure orientation dans l'application et dans la documentation sur les commandes sûres en arrière-plan, celles qui nécessitent le premier plan et celles qui nécessitent des permissions Apple.
- Exclu de la qualité : la couverture unitaire et du script en direct n'a pas été utilisée pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Experimental (45%)`
- Instructions de surface : évaluées par rapport à `references/completeness/ios-app.md`.
- Signaux positifs : les preuves d'archive, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les modes de localisation et la gestion des commandes de périphérique.
- Signaux négatifs : la note d'archive a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture d'archive.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un tableau de disponibilité des commandes iOS publié pour les modes premier plan, arrière-plan, construction locale et construction TestFlight.
- Promouvoir le script e2e du nœud manuel en un test de fumée de périphérique réel récurrent et produisant des artefacts.
- Clarifier le comportement des commandes hors ligne ou en file d'attente au lieu de s'appuyer sur l'exécution immédiate du nœud connecté.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` énumère les capacités du nœud iOS et encadre explicitement les limites du premier plan/arrière-plan.
- `/Users/kevinlin/code/openclaw/apps/ios/README.md` énumère les commandes concrètes du nœud iPhone et indique que l'utilisation au premier plan est le mode fiable.
- `/Users/kevinlin/code/openclaw/docs/gateway/protocol.md` documente `node.invoke`, `push.test` et des exemples de protocole de nœud iOS.

### Source

- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Capabilities/NodeCapabilityRouter.swift` mappe les chaînes de commande aux gestionnaires.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Model/NodeAppModel.swift` gère `node.invoke`, applique `NODE_BACKGROUND_UNAVAILABLE` et enregistre les gestionnaires de commandes.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Device/DeviceStatusService.swift`, `ContactsService.swift`, `CalendarService.swift`, `RemindersService.swift`, `MotionService.swift` et `PhotoLibraryService.swift` implémentent les charges utiles de commande de périphérique.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Gateway/GatewayConnectionController.swift` construit les capacités et commandes annoncées à partir des paramètres actuels.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/dev/ios-node-e2e.ts` est un script en direct du responsable de maintenance pour invoquer un nœud iOS déjà connecté.
- Aucun artefact e2e de matrice de commandes iOS automatisé ou test de fumée de version TestFlight n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/ios/Tests/GatewayConnectionControllerTests.swift` vérifie l'annonce des capacités, l'inclusion des commandes de localisation et l'absence de commandes exec système dangereuses.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/NodeAppModelInvokeTests.swift` exerce les assistants d'invocation, les clés de session et le comportement des invites de notification.
- `/Users/kevinlin/code/openclaw/apps/ios/Tests/AppCoverageTests.swift` vérifie les transitions d'état d'arrière-plan.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "iOS node capabilities" --json`

Résultats :

- PR #63123 `feat(ios): add background alive beacon support`.
- Issue #46664 `[Feature]: Offline Command Queue for iOS/Android Node App`.

Contexte de requête supplémentaire :

- `gitcrawl search openclaw/openclaw --query "iOS node commands foreground background" --json` n'a retourné aucun résultat.
- `gitcrawl search openclaw/openclaw --query "NODE_BACKGROUND_UNAVAILABLE" --json` n'a retourné aucun résultat.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "iOS node commands foreground background unavailable"`

Résultats :

- La note de support Discord explique que `canvas.*`, `camera.*` et `screen.*` sont réservés au premier plan sur les nœuds iOS/Android et échouent généralement avec `NODE_BACKGROUND_UNAVAILABLE` lorsqu'ils sont en arrière-plan.
