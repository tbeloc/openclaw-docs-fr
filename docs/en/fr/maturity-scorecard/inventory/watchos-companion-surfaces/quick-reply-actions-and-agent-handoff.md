---
title: "watchOS companion surfaces - Quick Reply Actions and Agent Handoff Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# watchOS companion surfaces - Quick Reply Actions and Agent Handoff Maturity Note

## Résumé

Les actions de prompt Watch peuvent revenir à l'iPhone sous forme d'événements `watch.reply`, puis le nœud iOS les met en file d'attente ou les transfère dans la session OpenClaw sélectionnée en tant que lien profond d'agent à faible réflexion. La couverture est Expérimentale car le chemin de file d'attente hors ligne est testé unitairement, mais aucune preuve complète de bouton watch vers agent turn n'a été trouvée.

La qualité est Alpha car le handoff dispose de la déduplication, de la mise en file d'attente hors ligne, des clés de session et de la notification miroir de secours, mais la sémantique de livraison n'est pas documentée pour les utilisateurs.

## Portée de la catégorie

- Boutons d'action Watch à partir de notifications de prompt générique.
- Charges utiles de réponse Watch-to-iPhone.
- Déduplication côté iPhone, mise en file d'attente hors ligne et transfert de demande d'agent.
- Notification iOS miroir action de secours.
- Hors de portée : décisions d'approbation spécifiques à l'exécution autoriser/refuser.

## Fonctionnalités

- Boutons d'action Watch à partir de prompt générique : Boutons d'action Watch à partir de notifications de prompt générique
- Charges utiles de réponse Watch-to-iPhone : Comportement des charges utiles de réponse Watch-to-iPhone, statut et vérification visible par l'opérateur.
- Déduplication côté iPhone : Déduplication côté iPhone, mise en file d'attente hors ligne et transfert de demande d'agent
- Action de notification iOS miroir : Notification iOS miroir action de secours

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (44%)`
- Signaux positifs : La source implémente l'encodage/décodage de réponse watch, la livraison directe ou en file d'attente WatchConnectivity, la déduplication côté iPhone, la mise en file d'attente hors ligne de la passerelle, le drainage de file d'attente à la reconnexion et le transfert de lien profond d'agent.
- Signaux négatifs : Un seul test direct pour la mise en file d'attente d'une réponse watch hors ligne a été trouvé. Aucun scénario en direct ne prouve qu'une action watch produit le message d'agent prévu dans la session prévue.
- Lacunes d'intégration : Besoin d'un scénario de bouton watch réel pour la livraison immédiate, la livraison en file d'attente, la suppression des réponses en double, le drainage de reconnexion de passerelle, le routage par clé de session et la remise en file d'attente en cas d'échec.

## Score de qualité

- Score : `Alpha (57%)`
- Rapports Gitcrawl : `gitcrawl search openclaw/openclaw --query "watch reply" --json` a retourné principalement des résultats de mots-clés reply/watch non liés et une PR Wear OS, pas les bugs watchOS reply actuels. `gitcrawl search openclaw/openclaw --query "watch quick-action notification" --json` a retourné un résultat Wear OS quick-reply, pas le chemin Apple Watch.
- Rapports Discrawl : `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS app watch"` a trouvé l'intérêt des utilisateurs pour les réponses vocales rapides et les notifications watch. `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "watch reply"` n'a pas surfacé les incidents Apple Watch quick-reply actuels.
- Bonnes qualités : Les réponses portent l'ID de réponse, l'ID de prompt, l'ID d'action, le libellé d'action, la clé de session, la note, l'horodatage et le transport. Le côté iPhone déduplique par ID de réponse et met en file d'attente lorsque la passerelle est hors ligne.
- Mauvaises qualités : Le handoff d'agent transforme un appui watch en message d'agent généré, ce qui nécessite une formulation plus claire visible par l'utilisateur et une auditabilité. Il n'y a pas d'explication d'opérateur pour les réponses en file d'attente ou le transfert échoué.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Expérimental (44%)`
- Instructions de surface : évaluées par rapport à `references/completeness/watchos-companion-surfaces.md`.
- Signaux positifs : les docs archivées, la source, le test, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour les boutons d'action Watch à partir de prompt générique, les charges utiles de réponse Watch-to-iPhone, la déduplication côté iPhone, l'action de notification iOS miroir.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une preuve e2e qu'un bouton d'action watch atteint la session OpenClaw attendue exactement une fois.
- Documenter ce que l'agent voit à partir d'une réponse watch et comment fonctionne le routage de session.
- Ajouter des tests pour les ID de réponse en double, le drainage de file d'attente, la remise en file d'attente en cas d'échec et les actions de notification iOS miroir.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` ne documente pas les réponses rapides watch.
- `/Users/kevinlin/code/openclaw/apps/ios/README.md` ne documente pas le comportement de réponse rapide watch.

### Source

- `/Users/kevinlin/code/openclaw/apps/ios/WatchExtension/Sources/WatchConnectivityReceiver.swift` construit des charges utiles `watch.reply` et les envoie via `sendMessage` ou `transferUserInfo`.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Services/WatchMessagingPayloadCodec.swift` analyse les charges utiles de réponse rapide dans `WatchQuickReplyEvent`.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Model/WatchReplyCoordinator.swift` déduplique les ID de réponse, met en file d'attente les réponses lors de la déconnexion, draine à la reconnexion et supporte la remise en file d'attente en cas d'échec de transfert.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Model/NodeAppModel.swift` gère les réponses rapides watch et les transfère en tant que liens profonds d'agent.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/OpenClawApp.swift` achemine les actions de notification iOS miroir watch prompt dans le même pont de réponse.

### Tests d'intégration

- Aucun scénario en direct ou d'intégration d'action watch vers agent-turn n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/ios/Tests/NodeAppModelInvokeTests.swift` inclut `watchReplyQueuesWhenGatewayOffline`.
- Aucun test direct n'a été trouvé pour la suppression des doublons, le drainage de reconnexion, le transfert d'agent réussi ou l'analyse d'action de notification miroir.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "watch reply" --json`

Résultats :

- Principalement des résultats de mots-clés reply/watch non liés et une PR Wear OS ; aucun bug Apple Watch quick-reply actuel surfacé.

Requête :

`gitcrawl search openclaw/openclaw --query "watch quick-action notification" --json`

Résultats :

- Résultat Wear OS quick-reply uniquement ; aucun chemin Apple Watch atteint.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS app watch"`

Résultats :

- L'intérêt des utilisateurs incluait les notifications Apple Watch et les réponses vocales rapides ; aucun chemin de support public n'a été identifié.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "watch reply"`

Résultats :

- Aucun incident d'implémentation Apple Watch quick-reply actuel surfacé.
