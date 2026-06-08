---
title: "Application Android - Note de Maturité du Runtime Appareil"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application Android - Note de Maturité du Runtime Appareil

## Résumé

Les capacités des nœuds Android sont larges : statut/info/permissions/santé de l'appareil, notifications, notification système, contacts, calendrier, localisation, mouvement, caméra, Canvas/A2UI, Talk PTT, et SMS/journal des appels/photos contrôlés par flavor. La couverture atteint Beta car le test de capacité en direct de la Gateway exécute la surface de commande non-interactive annoncée contre un nœud Android appairé. La qualité reste Alpha car les preuves d'archive incluent des défaillances d'annonce de commande zéro, un risque de transfert de notification entre sessions, et plusieurs demandes ouvertes pour des familles de capacités Android natives supplémentaires.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Reconnexion en arrière-plan et présence : comportement de présence du service de premier plan, reconnexion et comportement de présence du nœud.
- Disponibilité des commandes d'appareil : disponibilité des commandes d'appareil Android et annonce de capacité.

## Fonctionnalités

- Reconnexion en arrière-plan et présence : comportement de présence du service de premier plan, reconnexion et comportement de présence du nœud.
- Disponibilité des commandes d'appareil : disponibilité des commandes d'appareil Android et annonce de capacité.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (70%)`
- Signaux positifs : La documentation énumère les familles de commandes Android et la disponibilité dépendante du flavor. La source dispose d'un registre central pour les capacités et commandes annoncées, de portes de dispatcher pour les commandes sensibles au premier plan et aux permissions, et de gestionnaires sur les principales surfaces d'appareil. Le test de capacité en direct lit `node.describe`, applique la liste blanche Gateway effective, invoque les commandes non-interactives annoncées, et échoue sur les profils de commande non mappés.
- Signaux négatifs : La suite en direct est précondition et exclut le consentement d'enregistrement d'écran interactif. Elle valide les contrats de commande mais ne prouve pas chaque octroi de permission visible par l'utilisateur ou flux de travail d'état d'appareil de longue durée.
- Lacunes d'intégration : Besoin d'une fiche de pointage complète des commandes de nœud Android qui enregistre la disponibilité des commandes sur les versions Play et tierces, les permissions refusées/accordées, l'état de premier plan/arrière-plan, et la politique de liste blanche/liste noire Gateway.

## Score de Qualité

- Score : `Alpha (63%)`
- Rapports Gitcrawl : `notifications.list Android node` a trouvé le problème #48516 pour le transfert de notification causant des réponses entre sessions et le problème #87058 pour le nœud Android se connectant mais annonçant zéro commandes. `Android Health Connect read-only node commands` a trouvé #78611, et `Google Home API bridge Android app native smart-home` a trouvé #78476 comme demandes de capacité future.
- Rapports Discrawl : La recherche a trouvé une note d'examen du miroir GitHub indiquant que la suite Android en direct filtre maintenant les commandes déclarées par la liste blanche de politique effective, une note d'examen demandant d'ajouter `callLog.search` aux profils de capacité en direct, et des conseils de support indiquant que les commandes Canvas/caméra/écran échouent lorsqu'un nœud mobile est en arrière-plan ou n'annonce pas la capacité.
- Bonnes qualités : L'annonce de capacité est basée sur les données, les surfaces sensibles sont contrôlées par flavor de build et disponibilité à l'exécution, la dispatch de commande retourne des erreurs structurées, et la politique Gateway est appliquée avant l'exécution de la commande en direct.
- Mauvaises qualités : La forme de capacité est grande et dépendante des permissions ; les événements de notification peuvent affecter le routage de chat/session ; le flavor Play supprime plusieurs commandes d'appareil de haute valeur ; et les demandes de capacité Android native future s'accumulent déjà.
- Exclu de la qualité : La couverture de test et la preuve de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer la Qualité.

## Score de Complétude

- Score : `Beta (70%)`
- Instructions de surface : évaluées par rapport à `references/completeness/android-app.md`.
- Signaux positifs : les preuves de docs archivées, source, test, Gitcrawl et Discrawl couvrent la portée de taxonomie pour Reconnexion en arrière-plan et présence, Disponibilité des commandes d'appareil.
- Signaux négatifs : la note archivée a précédé le score de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Enregistrer les matrices de disponibilité des commandes pour Play par rapport au flavor tiers.
- Ajouter des preuves de smoke de version pour le routage de session de transfert de notification et les filtres de politique.
- Maintenir les profils de capacité en direct en synchronisation avec chaque commande Android nouvellement annoncée.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/android.md` énumère les familles de commandes : statut/info/permissions/santé de l'appareil, notifications, photos, contacts, calendrier, journal des appels, SMS, mouvement, caméra, Canvas et Talk.
- `/Users/kevinlin/code/openclaw/apps/android/README.md` documente les permissions restreintes de Google Play et la division flavor Play par rapport aux tiers.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-runtime.md` documente l'invocation de nœud appairé à partir des plugins chargés par Gateway et des commandes CLI.

### Source

- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/NodeRuntime.kt` câble les gestionnaires, les drapeaux de capacité, les sessions nœud/opérateur, la config de fonctionnalité sensible et la dispatch de commande.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/node/InvokeCommandRegistry.kt` définit les capacités et commandes annoncées plus les portes de disponibilité.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/node/InvokeDispatcher.kt` achemine les commandes et applique les erreurs de premier plan, debug, permission, flavor et disponibilité.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/node/DeviceHandler.kt`, `NotificationsHandler.kt`, `ContactsHandler.kt`, `CalendarHandler.kt`, `LocationHandler.kt`, `MotionHandler.kt`, `SystemHandler.kt`, `SmsHandler.kt`, et `CallLogHandler.kt` implémentent les familles de commandes.
- `/Users/kevinlin/code/openclaw/src/gateway/android-node.capabilities.live.test.ts` est le harnais de capacité en direct côté Gateway.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/android-node.capabilities.live.test.ts` se connecte à une Gateway, sélectionne un nœud Android appairé, lit `node.describe`, résout la politique de liste blanche, invoque chaque commande non-interactive annoncée mappée, et vérifie les contrats de charge utile ou les erreurs déterministes attendues.
- La suite ignore explicitement le consentement d'enregistrement d'écran interactif.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/node/InvokeCommandRegistryTest.kt`, `InvokeDispatcherTest.kt`, `DeviceHandlerTest.kt`, `NotificationsHandlerTest.kt`, `DeviceNotificationListenerServiceTest.kt`, `ContactsHandlerTest.kt`, `CalendarHandlerTest.kt`, `LocationHandlerTest.kt`, `MotionHandlerTest.kt`, et `SystemHandlerTest.kt` couvrent le comportement de commande principal.
- `/Users/kevinlin/code/openclaw/src/gateway/android-node.capabilities.policy-config.test.ts` et `android-node.capabilities.policy-source.test.ts` couvrent le comportement de config de politique de suite en direct.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "notifications.list Android node" --json`

Résultats :

- Problème #48516 `Android node notification forwarding causes cross-session replies (WhatsApp duplicate sends to wrong group)`.
- Problème #87058 `Android node connects but advertises zero commands ...`.

Requête :

`gitcrawl search openclaw/openclaw --query "Android Health Connect read-only node commands" --json`

Résultats :

- Problème #78611 `[Feature]: Android Health Connect read-only node commands`.

Requête :

`gitcrawl search openclaw/openclaw --query "Google Home API bridge Android app native smart-home" --json`

Résultats :

- Problème #78476 `Feature: Google Home API bridge in Android app for native smart-home control`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "Android node capabilities gateway commands"`

Résultats :

- 2026-03-19 Note d'examen du miroir GitHub indiquant que la suite en direct traite maintenant la liste blanche de politique comme faisant partie des préconditions exécutables.
- 2026-03-13 Note d'examen du miroir GitHub demandant d'ajouter un profil `callLog.search` aux vérifications de capacité Android en direct.
- 2026-03-13 Thread de support expliquant les défaillances de capacité Canvas/caméra/écran lorsqu'aucun nœud appairé n'est connecté, l'application mobile est en arrière-plan, ou les capacités ne sont pas annoncées.
