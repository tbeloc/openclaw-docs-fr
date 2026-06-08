---
title: "watchOS companion surfaces - Distribution and Support Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# watchOS companion surfaces - Distribution and Support Maturity Note

## Summary

Le compagnon watchOS est câblé en tant qu'une application Watch intégrée et une extension WatchKit à l'intérieur du projet iOS, avec des variables de signature, des ressources d'icônes, l'automatisation des versions Fastlane/TestFlight, et le support du versioning des applications iOS. La couverture est Expérimentale car les preuves proviennent du projet/source et des outils de version du mainteneur plutôt que d'un scénario d'installation publique de montre reproductible. La qualité est Expérimentale car la limite de construction est explicite et maintenable, mais la limite de support public indique toujours un aperçu interne et aucune distribution publique.

## Category Scope

Inclus dans cette catégorie :

- Application Watch : cibles d'application Watch et d'extension WatchKit
- Variables de signature/profil : variables de signature/profil, identifiants de bundle, ressources d'icônes, et flux de version bêta iOS
- Statut public/support : statut public/support du compagnon watch tel que distribué via l'application iOS
- Journal des modifications : preuves du journal des modifications et de l'historique du référentiel pour la maturité du compagnon watchOS
- Métadonnées de version : métadonnées de version et preuves de préparation App Store/TestFlight
- Thèmes historiques de bogues/régressions pertinents pour la notation : thèmes historiques de bogues/régressions pertinents pour la notation de la qualité actuelle de la source

## Features

- Application Watch : cibles d'application Watch et d'extension WatchKit
- Variables de signature/profil : variables de signature/profil, identifiants de bundle, ressources d'icônes, et flux de version bêta iOS
- Statut public/support : statut public/support du compagnon watch tel que distribué via l'application iOS
- Journal des modifications : preuves du journal des modifications et de l'historique du référentiel pour la maturité du compagnon watchOS
- Métadonnées de version : métadonnées de version et preuves de préparation App Store/TestFlight
- Thèmes historiques de bogues/régressions pertinents pour la notation : thèmes historiques de bogues/régressions pertinents pour la notation de la qualité actuelle de la source

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Experimental (38%)`
- Positive signals: `apps/ios/project.yml` déclare `OpenClawWatchApp` et `OpenClawWatchExtension`, intègre la cible watch depuis l'application iOS, et pointe les deux cibles vers les variables de signature/profil. `apps/ios/README.md`, la configuration Fastlane, la documentation de versioning, et les scripts de package couvrent les constructions source, l'archive/upload bêta, et le versioning du train TestFlight stable.
- Negative signals: La documentation publique indique toujours que l'application iOS est en aperçu interne et n'est pas distribuée publiquement. Aucun chemin d'installation TestFlight public, preuve d'installation watch App Store, ou smoke test de version watch-target reproductible n'a été trouvé dans le référentiel.
- Integration gaps: Besoin d'un scénario de release-gate qui construit l'application iOS avec l'application watch intégrée, la télécharge ou l'installe via le chemin de distribution prévu, appaire une vraie montre, et vérifie que l'application watch se lance depuis l'installation du compagnon.

## Quality Score

- Score: `Experimental (48%)`
- Gitcrawl reports: `gitcrawl search openclaw/openclaw --query "watch app" --json` a trouvé principalement des résultats non liés, plus des frictions de signature iOS dans la PR #41284 et un problème adjacent de file d'attente hors ligne mobile #46664. `gitcrawl search openclaw/openclaw --query "Apple Watch" --json` n'a trouvé aucun bogue d'implémentation watchOS direct actuel ; le résultat adjacent le plus proche était #46664 mentionnant des idées futures de complication/file d'attente iOS/Apple Watch.
- Discrawl reports: `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS app watch"` a trouvé un intérêt public et une discussion sur les limites de support, y compris une demande d'accès TestFlight qui a reçu la réponse « pas de TestFlight public » et des conseils de construction source. `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "WatchOS support"` a trouvé un résumé d'aperçu du mainteneur : les constructions source fonctionnent, pas de TestFlight public général, et les approbations d'exécution WatchOS nécessitent une compilation iOS manuelle et une configuration APNs locale.
- Good qualities: Les cibles watch ne sont pas des fichiers ad hoc cachés ; elles vivent dans le modèle de projet Xcode généré, utilisent des variables de version/signature, et partagent la lane de version/release iOS.
- Bad qualities: La distribution a toujours une forme bêta interne/mainteneur. La documentation de l'opérateur ne fournit pas de chemin d'installation, d'appairage ou de dépannage spécifique à la montre.
- Excluded from quality: La couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la qualité.

## Completeness Score

- Score: `Experimental (38%)`
- Surface instructions: évaluées par rapport à `references/completeness/watchos-companion-surfaces.md`.
- Positive signals: les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'application Watch, les variables de signature/profil, le statut public/support, le journal des modifications, les métadonnées de version, les thèmes historiques de bogues/régressions pertinents pour la notation.
- Negative signals: la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Missing capability branches: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Known Gaps

- Publier une limite d'installation/support spécifique à la montre qui correspond à l'état TestFlight ou de construction source réel.
- Ajouter un smoke test qui prouve que l'application Watch intégrée survit à la génération du projet, l'archive, la signature et l'installation.
- Documenter comment les identifiants de bundle watch et les profils doivent être configurés pour les constructions locales par rapport aux constructions officielles.

## Evidence

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` indique que l'application iOS est « en aperçu interne » et n'est pas distribuée publiquement.
- `/Users/kevinlin/code/openclaw/apps/ios/README.md` décrit « Super Alpha », le déploiement Xcode local, la distribution bêta interne, et le téléchargement TestFlight via Fastlane.
- `/Users/kevinlin/code/openclaw/apps/ios/VERSIONING.md` documente le versioning du train TestFlight.
- `/Users/kevinlin/code/openclaw/apps/ios/fastlane/SETUP.md` documente l'authentification App Store Connect et la configuration de l'archive/upload bêta.

### Source

- `/Users/kevinlin/code/openclaw/apps/ios/project.yml` définit `OpenClawWatchApp` comme `application.watchapp2` et `OpenClawWatchExtension` comme `watchkit2-extension`, avec les dépendances WatchConnectivity et UserNotifications.
- `/Users/kevinlin/code/openclaw/apps/ios/WatchApp/Info.plist` et `/Users/kevinlin/code/openclaw/apps/ios/WatchExtension/Info.plist` sont les fichiers info plist des cibles watch.
- `/Users/kevinlin/code/openclaw/apps/ios/WatchApp/Assets.xcassets/AppIcon.appiconset/` contient les ressources d'icône de l'application watch.
- `/Users/kevinlin/code/openclaw/package.json` définit les scripts `ios:gen`, `ios:open`, `ios:build`, `ios:beta:archive`, et `ios:beta`.

### Integration tests

- Aucun scénario d'installation/archive/appareil en direct watchOS n'a été trouvé.
- `/Users/kevinlin/code/openclaw/scripts/dev/ios-node-e2e.ts` exerce les commandes de nœud iOS connectées, mais il ne couvre pas l'application Watch ou le chemin WatchConnectivity.

### Unit tests

- `/Users/kevinlin/code/openclaw/test/scripts/ios-version.test.ts`, `ios-pin-version.test.ts`, et `ios-team-id.test.ts` couvrent le comportement des assistants de version/signature iOS, pas le succès d'installation spécifique à la montre.
- Aucune cible watch build smoke ou cible de test d'extension WatchKit n'a été trouvée.

### Gitcrawl queries

Query:

`gitcrawl search openclaw/openclaw --query "watch app" --json`

Results:

- Principalement des résultats de mots-clés « watch » non liés ; les résultats adjacents pertinents incluent la PR #41284 pour les frictions de signature iOS et le problème #46664 pour les concepts futurs de file d'attente hors ligne mobile/watch.

Query:

`gitcrawl search openclaw/openclaw --query "Apple Watch" --json`

Results:

- Aucun bogue d'implémentation watchOS direct actuel ; le problème adjacent #46664 mentionne les idées futures de complication iOS/Apple Watch.

### Discrawl queries

Query:

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS app watch"`

Results:

- La discussion TestFlight/accès public indique que l'application peut être construite à partir de la source mais aucun TestFlight public n'est généralement ouvert.
- Une demande d'accès TestFlight mentionne spécifiquement l'utilisation du compagnon Apple Watch pour les notifications et les réponses vocales rapides.

Query:

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "WatchOS support"`

Results:

- Le résumé d'aperçu du mainteneur indique que iOS et WatchOS sont dans le référentiel, les approbations d'exécution watchOS fonctionnent dans les constructions actuelles, mais le chemin nécessite toujours une compilation iOS manuelle et une configuration APNs locale.
