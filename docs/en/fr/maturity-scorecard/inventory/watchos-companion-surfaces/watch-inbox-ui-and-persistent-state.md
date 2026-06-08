---
title: "watchOS companion surfaces - Watch App UI Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# watchOS companion surfaces - Watch App UI Maturity Note

## Résumé

L'extension Watch dispose d'une véritable boîte de réception SwiftUI qui peut afficher des invites génériques, des boutons d'action, des listes/détails d'approbation d'exécution, des états de chargement/nouvelle tentative, des horodatages et un état persistant. La couverture est Expérimentale car elle est soutenue par la source sans rendu d'interface utilisateur watch, snapshot ou scénario d'appareil réel. La qualité est Alpha car l'interface utilisateur est intentionnellement petite et avec état, mais elle dispose de peu de documentation publique, aucun diagnostic visible par l'utilisateur et aucune preuve de comportement d'accessibilité ou de complication.

## Portée de la catégorie

Inclus dans cette catégorie :

- Point d'entrée de l'application Watch : Point d'entrée de l'application Watch et navigation SwiftUI
- Boîte de réception générique : Boîte de réception générique, actions d'invite, vues de chargement/liste/détail d'approbation d'exécution
- État persistant de la boîte de réception watch : État persistant de la boîte de réception watch et suppression de la livraison en double

## Fonctionnalités

- Point d'entrée de l'application Watch : Point d'entrée de l'application Watch et navigation SwiftUI
- Boîte de réception générique : Boîte de réception générique, actions d'invite, vues de chargement/liste/détail d'approbation d'exécution
- État persistant de la boîte de réception watch : État persistant de la boîte de réception watch et suppression de la livraison en double

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (42%)`
- Signaux positifs : La source de l'extension Watch implémente le point d'entrée de l'application, le magasin de boîte de réception, la vue de boîte de réception générique, la vue de chargement d'approbation d'exécution, la vue de liste, la vue de détail, l'état persistant, les clés de déduplication et l'autorisation de notification.
- Signaux négatifs : Aucun rendu d'interface utilisateur watch, snapshot, passage d'accessibilité ou scénario Apple Watch en direct n'a été trouvé.
- Lacunes d'intégration : Besoin d'un scénario d'interface utilisateur sur appareil pour le premier lancement, l'affichage de notification générique, l'affichage de liste d'approbation multiple, le détail d'approbation, l'état de nouvelle tentative/chargement, le nettoyage d'approbation expiré/résolu et la persistance après le relancement de l'application.

## Score de qualité

- Score : `Alpha (58%)`
- Rapports Gitcrawl : `gitcrawl search openclaw/openclaw --query "Apple Watch companion MVP" --json` n'a retourné aucun résultat. `gitcrawl search openclaw/openclaw --query "Apple Watch" --json` a trouvé principalement des résultats non liés et des idées futures mobiles/watch.
- Rapports Discrawl : `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "Apple Watch"` a trouvé une discussion d'intérêt produit autour d'un modèle d'interaction haptic/watch à faible bande passante, mais aucune archive de bug d'interface utilisateur actuelle. `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS app watch"` a trouvé des demandes de notifications et de réponses vocales rapides, qui ne sont pas encore représentées comme des documents d'interface utilisateur watch publics.
- Bonnes qualités : L'interface utilisateur se concentre sur les décisions petit écran plutôt que sur le chat complet. Elle gère plusieurs approbations, l'état du dernier résultat, l'état de nouvelle tentative, les boutons destructeurs, la livraison en double et l'état persistant.
- Mauvaises qualités : Il n'y a aucune promesse publique soutenue par la source pour l'interface utilisateur watch au-delà de l'aperçu interne. La réponse vocale, les haptics, les complications et les captures d'écran ne sont pas documentés comme un comportement watch pris en charge.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Expérimental (42%)`
- Instructions de surface : évaluées par rapport à `references/completeness/watchos-companion-surfaces.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour le point d'entrée de l'application Watch, la boîte de réception générique, l'état persistant de la boîte de réception watch.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter des captures d'écran d'interface utilisateur watch ou un document d'aperçu du responsable qui indique ce que l'application watch prend actuellement en charge.
- Ajouter une couverture smoke/snapshot d'interface utilisateur watch pour les états d'invite, de liste d'approbation, de détail d'approbation et de nouvelle tentative/chargement.
- Définir si les réponses vocales, les haptics et les complications sont planifiés, expérimentaux ou hors de portée.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` ne décrit pas actuellement l'interface utilisateur watch.
- `/Users/kevinlin/code/openclaw/apps/ios/README.md` décrit l'application iOS comme super-alpha/usage interne uniquement et ne fournit pas de docs d'utilisation d'interface utilisateur watch.

### Source

- `/Users/kevinlin/code/openclaw/apps/ios/WatchExtension/Sources/OpenClawWatchApp.swift` crée `WatchInboxStore`, active `WatchConnectivityReceiver` et actualise l'examen d'approbation au lancement/phase de scène active.
- `/Users/kevinlin/code/openclaw/apps/ios/WatchExtension/Sources/WatchInboxView.swift` implémente les vues de boîte de réception générique, de chargement d'approbation d'exécution, de liste et de détail.
- `/Users/kevinlin/code/openclaw/apps/ios/WatchExtension/Sources/WatchInboxStore.swift` persiste l'état de la boîte de réception dans `UserDefaults`, élague les approbations expirées, déduplique les livraisons et suit le texte d'état de réponse/approbation.

### Tests d'intégration

- Aucun test d'intégration d'interface utilisateur watch ou de lancement d'application watch n'a été trouvé.

### Tests unitaires

- Aucun test direct pour `WatchInboxStore`, `WatchInboxView` ou `OpenClawWatchApp` n'a été trouvé.
- Les tests iOS couvrent indirectement les charges utiles d'invite et d'approbation envoyées vers la watch, mais pas le rendu de l'interface utilisateur watch.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "Apple Watch companion MVP" --json`

Résultats :

- Aucun résultat.

Requête :

`gitcrawl search openclaw/openclaw --query "Apple Watch" --json`

Résultats :

- Principalement des résultats non liés plus des idées de file d'attente mobile/watch futures adjacentes dans #46664.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "Apple Watch"`

Résultats :

- La discussion d'intérêt produit a souligné l'interaction watch/haptic à faible bande passante et privée, mais n'a pas fourni de preuves d'incident d'interface utilisateur OpenClaw watch actuelle.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS app watch"`

Résultats :

- Les utilisateurs ont demandé des notifications Apple Watch et des réponses vocales rapides ; l'archive n'a pas montré de docs de support d'interface utilisateur watch publics.
