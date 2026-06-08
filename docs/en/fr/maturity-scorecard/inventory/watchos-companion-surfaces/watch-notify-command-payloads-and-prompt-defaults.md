---
title: "watchOS companion surfaces - Notifications and Replies Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# watchOS companion surfaces - Notifications and Replies Maturity Note

## Résumé

Le nœud iOS annonce une capacité `watch` et expose `watch.status` plus `watch.notify`, avec des charges utiles typées, normalisation de la priorité/risque, limitation des actions, et actions d'approbation/invite par défaut. La couverture est Alpha à la limite car la gestion des commandes est implémentée et testée unitairement via le modèle de nœud iOS, mais elle manque d'une preuve réelle Gateway-to-iPhone-to-Watch.

La qualité est Alpha car le contrat de commande est typé et contraint, tandis que la documentation destinée aux opérateurs n'est pas spécifique à la montre.

## Portée de la catégorie

Inclus dans cette catégorie :

- watch.status : contrats de commande watch.status et watch.notify
- Normalisation des charges utiles : Normalisation des charges utiles pour titre/corps, métadonnées d'invite/session, priorité, risque et boutons d'action
- Secours de notification iOS en miroir lorsque watch : Secours de notification iOS en miroir lorsque la livraison à la montre est en file d'attente
- Boutons d'action de montre à partir d'une invite générique : Boutons d'action de montre à partir de notifications d'invite générique
- Charges utiles de réponse Watch-to-iPhone : Comportement des charges utiles de réponse Watch-to-iPhone, statut et vérification visible par l'opérateur.
- Déduplications côté iPhone : Déduplications côté iPhone, mise en file d'attente hors ligne et transfert de demande d'agent
- Action de notification iOS en miroir : Secours d'action de notification iOS en miroir

## Fonctionnalités

- watch.status : contrats de commande watch.status et watch.notify
- Normalisation des charges utiles : Normalisation des charges utiles pour titre/corps, métadonnées d'invite/session, priorité, risque et boutons d'action
- Secours de notification iOS en miroir lorsque watch : Secours de notification iOS en miroir lorsque la livraison à la montre est en file d'attente
- Boutons d'action de montre à partir d'une invite générique : Boutons d'action de montre à partir de notifications d'invite générique
- Charges utiles de réponse Watch-to-iPhone : Comportement des charges utiles de réponse Watch-to-iPhone, statut et vérification visible par l'opérateur.
- Déduplications côté iPhone : Déduplications côté iPhone, mise en file d'attente hors ligne et transfert de demande d'agent
- Action de notification iOS en miroir : Secours d'action de notification iOS en miroir

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (50%)`
- Signaux positifs : Le nœud iOS annonce les commandes de montre lorsque la capacité de montre est présente. Les tests unitaires couvrent `watch.status`, `watch.notify`, rejet de message vide, actions par défaut, approbations par défaut, dérivation de priorité/risque, limitation des actions et erreurs de livraison indisponible.
- Signaux négatifs : Aucun test d'intégration n'a été trouvé qui invoque `watch.notify` via une Gateway en direct dans un iPhone et vérifie que la charge utile apparaît sur une Apple Watch ou une notification locale en miroir.
- Lacunes d'intégration : Besoin d'un scénario de commande en direct pour livraison réussie accessible, livraison en file d'attente, secours de notification en miroir, rejet de charge utile invalide et rendu d'action.

## Score de qualité

- Score : `Alpha (58%)`
- Rapports Gitcrawl : `gitcrawl search openclaw/openclaw --query "watch.notify" --json` n'a pas trouvé d'incidents watch notify actuels directs ; les résultats connexes étaient des correspondances de mots-clés génériques notification/watch et #46664 pour le comportement futur de la file d'attente mobile hors ligne.
- Rapports Discrawl : `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS app watch"` a trouvé une demande TestFlight pour les notifications et les réponses vocales rapides, ce qui renforce l'intérêt des utilisateurs mais aussi l'absence de support public. `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "WatchOS support"` indique que les chemins WatchOS sont utilisables à partir de la source mais restent en aperçu du responsable.
- Bonnes qualités : Les modèles typés vivent dans OpenClawKit partagé. La normalisation supprime les champs de texte non fiables, dérive le risque/priorité, limite les actions à quatre et fournit les approbations/non-approbations par défaut uniquement lorsqu'un ID d'invite existe.
- Mauvaises qualités : Il n'y a pas de référence de commande publique pour `watch.status` ou `watch.notify`. Le secours à la notification iOS en miroir est utile mais ajoute une autre surface de livraison dont le comportement utilisateur n'est pas documenté.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Alpha (50%)`
- Instructions de surface : évaluées par rapport à `references/completeness/watchos-companion-surfaces.md`.
- Signaux positifs : les documents archivés, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour watch.status, Normalisation des charges utiles, Secours de notification iOS en miroir lorsque watch, Boutons d'action de montre à partir d'une invite générique, Charges utiles de réponse Watch-to-iPhone, Déduplications côté iPhone, Action de notification iOS en miroir.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Documenter le schéma de commande de montre, le comportement d'action par défaut et les erreurs non supportées/indisponibles.
- Ajouter un scénario Gateway `node.invoke watch.notify` avec une montre physique et secours de notification en miroir.
- Clarifier si `watch.notify` est une capacité de nœud publique ou une API d'aperçu du responsable/interne.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` documente l'application du nœud iOS mais ne liste pas `watch.status` ou `watch.notify`.
- `/Users/kevinlin/code/openclaw/apps/ios/README.md` décrit le statut bêta interne/construction à partir de la source.

### Source

- `/Users/kevinlin/code/openclaw/apps/shared/OpenClawKit/Sources/OpenClawKit/WatchCommands.swift` définit `OpenClawWatchCommand`, les types de charge utile de montre, les niveaux de risque, les modèles d'action, les charges utiles de statut, les paramètres de notification et les charges utiles de résultat de notification.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Gateway/GatewayConnectionController.swift` annonce `watch.status` et `watch.notify` lorsque la capacité de montre est présente et inclut les champs de statut de montre dans les permissions.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Model/NodeAppModel.swift` gère `watch.status` et `watch.notify`.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Model/NodeAppModel+WatchNotifyNormalization.swift` normalise les paramètres de notification de montre et les actions par défaut.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/OpenClawApp.swift` définit `WatchPromptNotificationBridge` pour les notifications iOS en miroir lorsque la livraison est en file d'attente.

### Tests d'intégration

- Aucun scénario `node.invoke watch.notify` en direct n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/ios/Tests/NodeAppModelInvokeTests.swift` couvre `handleInvokeWatchStatusReturnsServiceSnapshot`, `handleInvokeWatchNotifyRoutesToWatchService`, rejet de message vide, actions par défaut, approbations par défaut, dérivation de priorité/risque, limitation des actions et livraison indisponible.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "watch.notify" --json`

Résultats :

- Aucun incident watch notify actuel direct ; les résultats connexes étaient des correspondances de mots-clés génériques notification/watch et #46664 pour le comportement futur de la file d'attente mobile.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS app watch"`

Résultats :

- Les mentions de demande TestFlight/accès incluent les notifications Apple Watch companion et les réponses vocales rapides comme utilisation souhaitée.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "WatchOS support"`

Résultats :

- Le résumé d'aperçu du responsable indique que les chemins source iOS et WatchOS existent mais ne sont pas un chemin TestFlight public.
