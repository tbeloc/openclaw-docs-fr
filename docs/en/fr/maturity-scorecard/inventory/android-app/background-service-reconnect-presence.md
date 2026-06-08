---
title: "Application Android - Service d'arrière-plan, Reconnexion et Note de Maturité de Présence"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application Android - Service d'arrière-plan, Reconnexion et Note de Maturité de Présence

## Résumé

L'opération d'arrière-plan Android est implémentée autour d'un service au premier plan, d'une notification persistante, de sessions Gateway reconnectées, de balises de présence active, d'état d'écouteur de notification et de commutation de type de microphone de service au premier plan. La couverture est Alpha car la documentation et le code source couvrent le comportement prévu, mais aucun tableau de bord de backgrounding en direct n'a été trouvé. La qualité est le composant Android le plus faible : les preuves d'archive incluent un problème de crash de service au premier plan et une PR active pour éviter l'utilisation persistante du service au premier plan `dataSync`.

## Portée de la catégorie

- `NodeForegroundService`, notification persistante, reconnexion d'arrière-plan, balises de présence de nœud, état d'écouteur de notification, reconnexion de session Gateway et reconnexion après mise en arrière-plan de l'application.
- Hors de portée : gestionnaires de commandes de nœud individuels sauf lorsque les changements d'état au premier plan/arrière-plan modifient la disponibilité des commandes.

## Fonctionnalités

- Reconnexion et présence d'arrière-plan : Comportement de présence de service au premier plan, reconnexion et présence de nœud.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (62%)`
- Signaux positifs : La documentation indique explicitement qu'Android maintient la connexion Gateway active via un service au premier plan, se reconnecte automatiquement après l'appairage initial et envoie `node.presence.alive` lors de la mise en arrière-plan tout en étant connecté. Le code source implémente l'état de notification au premier plan, la boucle de reconnexion, la logique de charge utile/saut de balise de présence et les tests de reconnexion.
- Signaux négatifs : Aucun scénario de backgrounding Android en direct n'a été trouvé qui prouve la mise en arrière-plan de l'application, la notification du service au premier plan, la gestion de la balise de présence, le redémarrage de Gateway, la perte de réseau et le relancement de l'application ensemble.
- Lacunes d'intégration : Besoin d'un tableau de bord de background/reconnexion sur appareil réel couvrant les restrictions de service Android 14/15, l'économiseur de batterie, les changements de réseau, le redémarrage de Gateway et la promotion/rétrogradation du service de microphone Talk Mode.

## Score de qualité

- Score : `Alpha (55%)`
- Rapports Gitcrawl : `ForegroundServiceStartNotAllowedException Android` a trouvé le problème #64903 pour les crashes d'application Android sur `NodeForegroundService startForeground` avec `ForegroundServiceStartNotAllowedException` et la PR #80082 `fix(android): avoid dataSync FGS for persistent node`.
- Rapports Discrawl : `Android foreground service reconnect presence` n'a retourné aucun résultat direct. Le contexte de support plus large sous les recherches de capacité de nœud note que l'état d'arrière-plan du nœud mobile provoque des défaillances Canvas/caméra/écran.
- Bonnes qualités : Le service utilise une notification persistante de faible importance, met à jour le titre/texte à partir de l'état d'exécution, ajoute une action Déconnecter, commute le type de service pour Talk Mode et les réponses de balise de présence nécessitent `handled: true` avant de compter les mises à jour durables de dernière visualisation.
- Mauvaises qualités : La politique de service au premier plan Android est un risque de crash en direct, l'opération de nœud persistant touche les quotas de service du système d'exploitation et la documentation ne fournit pas de recette d'opérateur actuelle pour l'optimisation de la batterie, le refus de service ou le triage de reconnexion.
- Exclu de la qualité : La couverture des tests et la preuve du flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Alpha (62%)`
- Instructions de surface : évaluées par rapport à `references/completeness/android-app.md`.
- Signaux positifs : la documentation archivée, le code source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la reconnexion et la présence d'arrière-plan.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Prouver la reconnexion et la présence d'arrière-plan sur les versions actuelles du système d'exploitation Android avec des appareils réels.
- Ajouter des conseils d'opérateur pour le refus de service au premier plan, l'économiseur de batterie, les restrictions d'arrière-plan OEM et les états de permission de notification.
- Clarifier quelles commandes échouent intentionnellement lorsque l'application est en arrière-plan et comment récupérer.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/platforms/android.md` documente la conservation de la connexion du service au premier plan, la reconnexion automatique au lancement et les balises de présence active après la connexion de session de nœud authentifiée et la mise en arrière-plan.
- `/Users/kevinlin/code/openclaw/apps/android/README.md` répertorie les balises de présence d'arrière-plan authentifiées et les notifications push dans la liste de contrôle de reconstruction.
- `/Users/kevinlin/code/openclaw/docs/nodes/troubleshooting.md` est lié comme dépannage de nœud Android connexe.

### Code source

- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/NodeForegroundService.kt` démarre un service au premier plan, maintient la notification persistante, expose Déconnecter et promeut les types de service pour Talk Mode.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/node/ConnectionManager.kt` construit les options de connexion de nœud, l'agent utilisateur, les capacités annoncées et la politique TLS utilisée lors de la reconnexion.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/node/NodePresenceAliveBeacon.kt` construit et décode `node.presence.alive`, limite les succès récents et assainit les raisons d'échec.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/gateway/GatewaySession.kt` possède la connexion, la déconnexion, la reconnexion, la pause après échec d'authentification et la fermeture de connexion actuelle.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/main/java/ai/openclaw/app/node/DeviceNotificationListenerService.kt` suit l'état de connexion de l'écouteur de notification et émet des événements `notifications.changed`.

### Tests d'intégration

- Aucun scénario Android de background/reconnexion en direct n'a été trouvé.
- `/Users/kevinlin/code/openclaw/src/gateway/android-node.capabilities.live.test.ts` exige que l'application reste déverrouillée et au premier plan pour l'exécution des capacités, ce qui met en évidence le scénario d'arrière-plan manquant.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/NodeForegroundServiceTest.kt` couvre le comportement de notification/type du service au premier plan.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/gateway/GatewaySessionReconnectTest.kt` couvre le remplacement des connexions actives et le comportement de pause de reconnexion.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/node/NodePresenceAliveBeaconTest.kt` couvre le comportement d'aide de charge utile/réponse de balise de présence.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/node/ConnectionManagerTest.kt` couvre le comportement du gestionnaire de connexion.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "ForegroundServiceStartNotAllowedException Android" --json`

Résultats :

- Problème #64903 `Android app crashes on NodeForegroundService startForeground with ForegroundServiceStartNotAllowedException`.
- PR #80082 `fix(android): avoid dataSync FGS for persistent node`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "Android foreground service reconnect presence"`

Résultats :

- Aucun résultat direct.

Contexte de requête supplémentaire :

- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "Android node capabilities gateway commands"` a trouvé des conseils de support indiquant que les commandes Canvas/caméra/écran du nœud mobile échouent lorsque l'application est en arrière-plan.
