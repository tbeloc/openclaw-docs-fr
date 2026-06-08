---
title: "watchOS companion surfaces - Watchconnectivity Session Status and Delivery Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# watchOS companion surfaces - Watchconnectivity Session Status and Delivery Maturity Note

## Résumé

Le côté iPhone expose un service WatchConnectivity qui signale le support, l'appairage, l'installation, la disponibilité et l'état d'activation, puis livre les charges utiles de la montre via `sendMessage`, `transferUserInfo` ou `applicationContext`. La couverture est Expérimentale car des tests de source et de commande adjacents aux unités existent, mais aucun scénario réel de session téléphone-montre n'a été trouvé.

La qualité est Alpha car le code de transport a un comportement de secours raisonnable et une émission de statut, tandis que la documentation et les conseils de réparation des opérateurs sont rares.

## Portée de la catégorie

- Transport WatchConnectivity côté iPhone et snapshot de statut.
- Activation du récepteur côté montre et gestion des charges utiles entrantes.
- Secours de livraison parmi les messages accessibles, les informations utilisateur en file d'attente et les snapshots de contexte d'application.
- Hors de portée : la sémantique du contenu des notifications de montre et des décisions d'approbation.

## Fonctionnalités

- Transport WatchConnectivity côté iPhone : transport WatchConnectivity côté iPhone et snapshot de statut
- Activation du récepteur côté montre : activation du récepteur côté montre et gestion des charges utiles entrantes
- Secours de livraison parmi les messages accessibles : secours de livraison parmi les messages accessibles, les informations utilisateur en file d'attente et les snapshots de contexte d'application

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (46%)`
- Signaux positifs : la source implémente les snapshots de statut, les boucles d'attente d'activation, la gestion des changements de disponibilité, le secours d'envoi de message à la livraison en file d'attente et l'activation/réception côté montre. Les tests d'invocation de nœud iOS couvrent le routage des services `watch.status` et `watch.notify` via un service de montre simulé.
- Signaux négatifs : aucun test d'intégration WatchConnectivity, test d'appairage de simulateur ou artefact de test réel iPhone plus Apple Watch n'a été trouvé.
- Lacunes d'intégration : besoin d'un scénario d'appareil réel pour l'état d'appairage, l'état d'installation de l'application de montre, la livraison au premier plan accessible, la livraison en arrière-plan en file d'attente, la livraison de snapshot de contexte d'application et la réactivation de session.

## Score de qualité

- Score : `Alpha (60%)`
- Rapports Gitcrawl : `gitcrawl search openclaw/openclaw --query "WatchConnectivity" --json` n'a retourné aucun résultat. `gitcrawl search openclaw/openclaw --query "iOS Watch reply reliability" --json` n'a également retourné aucun résultat.
- Rapports Discrawl : `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "WatchConnectivity"` a retourné une discussion de conception OpenClaw-adjacente plus ancienne et non actuelle plutôt que des incidents d'implémentation actuels. `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS / WatchOS"` a montré un travail de support de montre en cours et des questions de date de sortie, pas une ligne de base de support public résolue.
- Bonnes qualités : le transport distingue les états non supportés, non appairés, application non installée, accessible et d'activation. Il bascule de `sendMessage` à la livraison en file d'attente et enregistre les transitions de statut.
- Mauvaises qualités : les messages d'échec de connectivité de montre sont principalement des erreurs d'implémentation/champs de statut ; il n'y a pas de guide de réparation de montre visible par l'utilisateur. Le code dépend du comportement d'exécution iOS/watchOS qui n'est pas capturé par les tests locaux.
- Exclu de la qualité : la couverture des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Expérimental (46%)`
- Instructions de surface : évaluées par rapport à `references/completeness/watchos-companion-surfaces.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour le transport WatchConnectivity côté iPhone, l'activation du récepteur côté montre, le secours de livraison parmi les messages accessibles.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un chemin QA WatchConnectivity pour la livraison au premier plan et en arrière-plan.
- Documenter ce que les opérateurs doivent faire pour les états non appairés, non installés, non accessibles et inactifs.
- Ajouter une preuve d'appareil réel autour de la réactivation après la désactivation de session.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` documente l'appairage et le push d'application iOS, mais ne documente pas l'appairage de montre ou la réparation WatchConnectivity.
- `/Users/kevinlin/code/openclaw/apps/ios/README.md` documente l'installation de source et la version bêta, mais pas les diagnostics de transport de montre.

### Source

- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Services/WatchConnectivityTransport.swift` implémente les snapshots de statut côté iPhone, l'activation, les gestionnaires de statut, `sendPayload`, `sendSnapshotPayload` et les rappels de délégué WCSession.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Services/WatchMessagingService.swift` enveloppe le transport en tant que `WatchMessagingServicing`.
- `/Users/kevinlin/code/openclaw/apps/ios/WatchExtension/Sources/WatchConnectivityReceiver.swift` active WCSession sur la montre, reçoit les messages/informations utilisateur/contexte d'application et envoie les réponses ou résolutions d'approbation à l'iPhone.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Services/NodeServiceProtocols.swift` définit `WatchMessagingStatus`, `WatchQuickReplyEvent` et les types d'événements d'approbation de montre.

### Tests d'intégration

- Aucun scénario réel d'appareil, simulateur ou intégration WatchConnectivity n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/ios/Tests/NodeAppModelInvokeTests.swift` couvre `watch.status` retournant un snapshot de service simulé et `watch.notify` routant vers un service simulé.
- Aucun test n'instancie directement `WatchConnectivityTransport` ou `WatchConnectivityReceiver`.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "WatchConnectivity" --json`

Résultats :

- Aucun résultat.

Requête :

`gitcrawl search openclaw/openclaw --query "iOS Watch reply reliability" --json`

Résultats :

- Aucun résultat.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "WatchConnectivity"`

Résultats :

- A retourné du contenu de planification WatchConnectivity OpenClaw-adjacent plus ancien et non actuel, pas des incidents de produit actuels.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS / WatchOS"`

Résultats :

- Le canal Discord actif avait des questions récentes de sortie/support et des commentaires sur l'amélioration du support de montre, indiquant un travail en cours plutôt qu'un support stable.
