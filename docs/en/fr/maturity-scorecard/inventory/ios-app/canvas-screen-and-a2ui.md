---
title: "iOS app - Canvas and Screen Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iOS app - Canvas and Screen Maturity Note

## Résumé

Canvas et A2UI sont des fonctionnalités réelles de nœud iOS : l'application héberge un scaffold WKWebView, peut naviguer vers des pages Canvas/A2UI hébergées par Gateway, évalue JavaScript, capture des instantanés, traite les actions JSON/JSONL A2UI et expose l'enregistrement d'écran. La couverture reste Expérimentale car la preuve la plus solide est le code source, les tests unitaires, la documentation et l'invocation manuelle de nœud plutôt qu'un flux Canvas automatisé sur appareil réel. La qualité est Expérimentale élevée car l'implémentation inclut le blocage de la boucle locale et les vérifications de confiance, mais les exigences de premier plan et l'accessibilité de l'hôte restent des pièges courants pour les opérateurs.

## Portée de la catégorie

Inclus dans cette catégorie :

- Canvas present/hide/navigate/eval/snapshot : Canvas present/hide/navigate/eval/snapshot, A2UI reset/push/pushJSONL, chargement du scaffold WKWebView, pont d'action A2UI de confiance, enregistrement d'écran, portes de commande de premier plan et gestion des URL d'hôte Canvas Gateway

## Fonctionnalités

- Canvas present/hide/navigate/eval/snapshot : Canvas present/hide/navigate/eval/snapshot, A2UI reset/push/pushJSONL, chargement du scaffold WKWebView, pont d'action A2UI de confiance, enregistrement d'écran, portes de commande de premier plan et gestion des URL d'hôte Canvas Gateway

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (44%)`
- Signaux positifs : La documentation fournit des exemples concrets de `canvas.navigate`, `canvas.eval` et `canvas.snapshot`. `scripts/dev/ios-node-e2e.ts` peut exécuter le dangereux `screen.record` contre un nœud iOS connecté. Les tests unitaires couvrent les assistants Canvas et A2UI dans le code Swift partagé.
- Signaux négatifs : Aucun e2e Canvas iOS automatisé n'a été trouvé qui démarre l'application, l'appaire, ouvre l'onglet Screen, valide la disponibilité d'A2UI et capture un instantané à partir d'un appareil réel ou d'un simulateur.
- Lacunes d'intégration : Besoin d'une preuve Canvas iOS de premier plan répétable pour le chargement du scaffold, le chargement de l'hôte Gateway, le push A2UI, la confiance du rappel d'action, l'évaluation JavaScript, l'instantané JPEG/PNG et l'enregistrement d'écran.

## Score de qualité

- Score : `Expérimental (47%)`
- Rapports Gitcrawl : `iOS canvas screen A2UI` a trouvé la PR #80802 pour le renforcement de Talk/Canvas et le problème #68497 concernant l'exposition du comportement du pont d'action A2UI en dehors des nœuds natifs. La recherche plus large `ios-node` a trouvé le problème #66983 notant que les commandes Canvas sont actuellement centrées sur les nœuds natifs.
- Rapports Discrawl : `iOS canvas screen A2UI snapshot node` a trouvé une note d'assistance décrivant Canvas/WKWebView iOS, A2UI, capture d'instantané et interception de lien profond. `iOS node commands foreground background unavailable` a trouvé des conseils d'assistance indiquant que `canvas.*` et `screen.*` nécessitent que l'application soit au premier plan.
- Bonnes qualités : Les URL Canvas de boucle locale sont bloquées pour les chargements Gateway distants, la comparaison d'URL de confiance A2UI normalise la casse/les fragments, la disponibilité d'A2UI réessaie avec actualisation des capacités et les valeurs par défaut d'instantané sont limitées.
- Mauvaises qualités : Le succès de l'opérateur dépend de l'état de premier plan et de la configuration accessible de l'hôte Canvas Gateway ; `A2UI_HOST_NOT_CONFIGURED` et le comportement de premier plan uniquement sont documentés mais restent faciles à rencontrer lors de la première utilisation.
- Exclu de la qualité : Les tests Canvas et le script de nœud manuel n'ont pas été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Expérimental (44%)`
- Instructions de surface : évaluées par rapport à `references/completeness/ios-app.md`.
- Signaux positifs : les documents archivés, le code source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour Canvas present/hide/navigate/eval/snapshot.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un artefact de fumée de version Canvas iOS qui prouve un WKWebView non vierge, l'application de message A2UI, le rappel d'action de confiance et la sortie d'instantané.
- Rendre les exigences de premier plan et l'accessibilité de l'hôte Gateway plus visibles dans l'onglet Screen de l'application.
- Ajouter une limite de support public pour le comportement Canvas dans les versions internes/TestFlight.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` documente l'utilisation de Canvas/A2UI, les chemins d'hôte Canvas Gateway, la relation de premier plan et les exemples de `node.invoke`.
- `/Users/kevinlin/code/openclaw/apps/ios/README.md` répertorie `canvas present/navigate/eval/snapshot` et l'enregistrement d'écran comme commandes de nœud iPhone de premier plan.
- `/Users/kevinlin/code/openclaw/docs/refactor/canvas.md` et `/Users/kevinlin/code/openclaw/extensions/canvas/` documentent la surface d'hôte/plugin Canvas adjacente.

### Source

- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Model/NodeAppModel+Canvas.swift` résout les URL Canvas et A2UI Gateway, bloque les hôtes de boucle locale et actualise les capacités d'hôte.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Screen/ScreenController.swift` héberge Canvas WKWebView, évalue JS, capture des instantanés et valide les origines d'action A2UI de confiance.
- `/Users/kevinlin/code/openclaw/apps/ios/Sources/Screen/ScreenRecordService.swift` implémente l'enregistrement d'écran.
- `/Users/kevinlin/code/openclaw/apps/shared/OpenClawKit/Sources/OpenClawKit/CanvasCommands.swift` et `CanvasA2UICommands.swift` définissent les contrats de commande partagés.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/dev/ios-node-e2e.ts` peut invoquer `screen.record` contre un nœud iOS connecté lorsque `--dangerous` est défini.
- Aucun artefact e2e Canvas/A2UI iOS automatisé sur appareil réel n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/ios/Tests/ScreenControllerTests.swift` et `ScreenRecordServiceTests.swift` couvrent le comportement d'écran et les limites des paramètres d'enregistrement d'écran.
- `/Users/kevinlin/code/openclaw/apps/shared/OpenClawKit/Tests/OpenClawKitTests/CanvasA2UITests.swift`, `CanvasA2UIActionTests.swift` et `CanvasSnapshotFormatTests.swift` couvrent les contrats Canvas partagés.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "iOS canvas screen A2UI" --json`

Résultats :

- PR #80802 `[codex] Harden Talk, Canvas, and add macOS ambient overlay`.

Contexte de requête supplémentaire :

- `gitcrawl search openclaw/openclaw --query "ios-node" --json` a trouvé le problème #68497 concernant le comportement du pont d'action A2UI et le problème #66983 concernant le support de nœud Canvas étant centré sur les nœuds natifs.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "iOS canvas screen A2UI snapshot node"`

Résultats :

- La note d'assistance Discord décrit Canvas iOS comme un WKWebView avec scaffold groupé, A2UI, évaluation JS, capture d'instantané et interception de lien profond.
- Une note d'assistance distincte sous `iOS node commands foreground background unavailable` indique que `canvas.*` et `screen.*` sont de premier plan uniquement sur les nœuds mobiles.
