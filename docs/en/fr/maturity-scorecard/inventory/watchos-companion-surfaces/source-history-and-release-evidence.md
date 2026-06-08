---
title: "watchOS companion surfaces - Source History and Release Evidence Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# watchOS companion surfaces - Source History and Release Evidence Maturity Note

## Résumé

Le journal des modifications montre plusieurs améliorations axées sur watchOS dans la chronologie iOS/Watch : MVP de compagnon Watch, actions rapides, actions de notification en pont, normalisation des actions rapides, fiabilité des réponses, icônes, préparation de l'App Store Connect et récupération d'approbation exécutive. La couverture est Expérimentale car il s'agit d'enregistrements de modifications historiques et non d'artefacts de fumée de version actuelle. La qualité est Alpha car l'historique montre une itération réelle sur des modes de défaillance importants, mais la documentation publique actuelle ne présente toujours pas watchOS comme une fonctionnalité utilisateur.

## Portée de la catégorie

- Preuve du journal des modifications et de l'historique du référentiel pour la maturité du compagnon watchOS.
- Métadonnées de version et preuve de préparation de l'App Store/TestFlight.
- Thèmes historiques de bogues/régressions pertinents pour évaluer la qualité actuelle de la source.
- Hors de portée : traiter les anciennes entrées du journal des modifications comme preuve du support en direct actuel.

## Fonctionnalités

- Journal des modifications : Preuve du journal des modifications et de l'historique du référentiel pour la maturité du compagnon watchOS
- Métadonnées de version : Métadonnées de version et preuve de préparation de l'App Store/TestFlight
- Thèmes historiques de bogues/régressions pertinents pour l'évaluation : Thèmes historiques de bogues/régressions pertinents pour évaluer la qualité actuelle de la source

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (48%)`
- Signaux positifs : Le journal des modifications racine inclut plusieurs entrées spécifiques à watch, et le journal des modifications iOS enregistre l'hygiène de construction récente pour l'application Watch. Cela donne une piste d'historique source pour ce qui a changé et pourquoi.
- Signaux négatifs : Les entrées du journal des modifications ne prouvent pas que la version actuelle, la version, le relais APNs, l'installation réelle de watch ou le scénario utilisateur réussit aujourd'hui.
- Lacunes d'intégration : Convertir les modifications historiques en une liste de contrôle de version watch actuelle avec des liens de preuve pour la version, l'installation, l'appairage, la notification, la réponse rapide, l'approbation et la récupération en arrière-plan.

## Score de qualité

- Score : `Alpha (56%)`
- Rapports Gitcrawl : Les recherches de numéros de PR pour les anciennes entrées du journal des modifications watch n'ont retourné aucun résultat du magasin gitcrawl actuel, donc la qualité actuelle ne peut pas être augmentée à partir du détail du problème/PR. `gitcrawl search openclaw/openclaw --query "watch app" --json` a trouvé des frictions de signature iOS et des idées futures mobiles/watch plutôt que des preuves de version watchOS actuelle.
- Rapports Discrawl : `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS / WatchOS"` a montré des travaux actifs récents, des questions de date de version et un suivi « meilleur support ipad et watch ». `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS app watch"` a montré des frictions d'accès à la version source/TestFlight et une limite de support ouverte.
- Bonnes qualités : L'historique montre que le chemin watch a reçu un durcissement de suivi plutôt qu'un prototype unique. Il inclut la fiabilité, la sécurité des acteurs, la normalisation des charges utiles, la préparation des icônes/versions et le travail de récupération.
- Mauvaises qualités : La preuve est fragmentée entre le journal des modifications, la source et Discord plutôt qu'une fiche de pointage de version watchOS maintenue. La documentation publique traite toujours l'application iOS parente comme un aperçu interne.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Expérimental (48%)`
- Instructions de surface : évaluées par rapport à `references/completeness/watchos-companion-surfaces.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le journal des modifications, les métadonnées de version, les thèmes historiques de bogues/régressions pertinents pour l'évaluation.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuve` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une liste de contrôle de version watchOS actuelle qui lie les revendications du journal des modifications à la preuve actuelle.
- Maintenir une section des problèmes connus spécifiques à watch pour la confidentialité des notifications push, la récupération en arrière-plan et l'état d'appairage/distribution.
- Ne pas promouvoir la maturité publique jusqu'à ce que le support watch ait un chemin de distribution annoncé et des scénarios utilisateur reproductibles.

## Preuve

### Docs

- `/Users/kevinlin/code/openclaw/apps/ios/CHANGELOG.md` inclut une entrée récente pour l'hygiène de construction dans l'application iOS, l'extension Share, le widget Activity, l'application Watch et les sources Swift partagées.
- `/Users/kevinlin/code/openclaw/CHANGELOG.md` inclut des entrées spécifiques à watch pour le MVP compagnon (#20054), l'approbation/rejet watch exploitable et les réponses rapides (#21996), les actions de notification d'invite watch en pont (#22123), la normalisation de la charge utile des actions rapides (#23636), la fiabilité des réponses (#33306), la préparation de l'App Store Connect/icône watch (#38936) et la récupération d'approbation watch verrouillée/en arrière-plan (#61757).
- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` reste un aperçu interne et ne promeut pas watchOS comme support public.

### Source

- `/Users/kevinlin/code/openclaw/apps/ios/WatchExtension/Sources/` contient l'implémentation actuelle de l'extension watch.
- `/Users/kevinlin/code/openclaw/apps/ios/project.yml` inclut les cibles actuelles de l'application Watch et de l'extension WatchKit.
- `/Users/kevinlin/code/openclaw/apps/ios/fastlane/` et `/Users/kevinlin/code/openclaw/apps/ios/VERSIONING.md` contiennent l'automatisation de la version iOS qui porte l'application watch intégrée.

### Tests d'intégration

- Aucune liste de contrôle de version actuelle ou preuve de scénario en direct n'a été trouvée pour les éléments historiques du journal des modifications watch.

### Tests unitaires

- Les tests iOS actuels couvrent la gestion des commandes watch et les éléments de récupération d'approbation, mais aucun test de cible watch ne correspond directement aux entrées historiques du journal des modifications.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "20054" --json`

Résultats :

- Aucun résultat.

Requête :

`gitcrawl search openclaw/openclaw --query "33306" --json`

Résultats :

- Aucun résultat.

Requête :

`gitcrawl search openclaw/openclaw --query "61757" --json`

Résultats :

- Aucun résultat.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS / WatchOS"`

Résultats :

- La discussion récente du canal inclut des questions de date de version, l'état d'atterrissage et le travail de suivi pour un meilleur support iPad/watch.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS app watch"`

Résultats :

- La discussion d'accès public pointe toujours vers l'état de version source/aperçu interne plutôt qu'un chemin TestFlight public.
