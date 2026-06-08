---
title: "iOS app - Distribution Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iOS app - Distribution Maturity Note

## Résumé

L'application iOS dispose d'un chemin d'aperçu interne source-first, d'une génération de projet XcodeGen, de remplacements de signature locaux, de lanes d'archive/upload Fastlane, d'un versioning CalVer épinglé, de fichiers de métadonnées App Store et de drapeaux de build push locaux-vs-officiels explicites. La couverture est Expérimentale car le chemin de distribution est principalement manuel et aucun smoke test d'archive/upload TestFlight en direct récurrent n'a été trouvé. La qualité est Expérimentale car l'implémentation sépare la signature locale, les identifiants de bundle officiels, les secrets App Store Connect soutenus par Keychain, les builds officiels relay-only et les métadonnées de version générées, mais les preuves d'archive montrent toujours des demandes d'accès confuses, une distribution opérée par les mainteneurs et aucune route d'installation publique.

## Portée de la catégorie

Inclus dans cette catégorie :

- Statut d'aperçu interne : Statut d'aperçu interne, déploiement manuel source/Xcode, signature locale, génération de projet XcodeGen, archive/upload TestFlight Fastlane, versioning/changelog/métadonnées, artefacts de version et drapeaux de build officiels-vs-locaux

## Fonctionnalités

- Statut d'aperçu interne : Statut d'aperçu interne, déploiement manuel source/Xcode, signature locale, génération de projet XcodeGen, archive/upload TestFlight Fastlane, versioning/changelog/métadonnées, artefacts de version et drapeaux de build officiels-vs-locaux

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimentale (42%)`
- Signaux positifs : Les étapes d'installation source et de déploiement Xcode sont documentées, les scripts de package câblent la préparation de signature/version dans XcodeGen et xcodebuild, et Fastlane dispose de lanes d'archive locale et d'upload TestFlight.
- Signaux négatifs : La distribution publique est explicitement indisponible, TestFlight est opéré par les mainteneurs, aucun workflow CI n'a été trouvé pour le chemin de build/archive/upload du projet Xcode iOS, et aucun enregistrement de smoke test d'upload TestFlight en direct ou de version de release install-to-gateway n'a été trouvé.
- Lacunes d'intégration : Besoin d'un smoke test de version récurrent qui exécute la préparation bêta, archive l'application, upload ou dry-run TestFlight avec un numéro de build enregistré, installe le build résultant, l'apparie à une Gateway actuelle et vérifie les drapeaux relay officiels dans l'application construite.

## Score de qualité

- Score : `Expérimentale (45%)`
- Rapports Gitcrawl : `iOS TestFlight` a trouvé les problèmes de demande d'accès fermés #75684, #72763 et #64526 ; `TestFlight` a également trouvé les demandes d'accès fermées #61639 et #74869. Des recherches plus spécifiques pour `iOS TestFlight signing fastlane`, `iOS beta TestFlight OPENCLAW_PUSH_RELAY_BASE_URL`, `iOS version changelog TestFlight metadata`, `public TestFlight`, `beta_archive` et `OPENCLAW_PUSH_DISTRIBUTION official` n'ont retourné aucun résultat correspondant issue/PR.
- Rapports Discrawl : Les résultats de l'archive Discord incluent un miroir PR du 11 mars pour #42991 ajoutant le flux Fastlane/TestFlight local, un commentaire d'examen du 18 mars sur #48667 avertissant de ne pas publier la sortie `beta_archive` comme IPA téléchargeable car elle intègre les drapeaux relay officiels, des réponses répétées de demande d'accès en avril disant qu'il n'y avait pas de TestFlight public et que les utilisateurs devraient construire à partir de la source, un résumé du 26 avril disant que l'application était toujours en pré-alpha/aperçu mainteneur, et un utilisateur du 23 mai demandant la route d'installation iOS correcte car aucun lien App Store ou TestFlight public n'était visible.
- Bonnes qualités : Les remplacements de signature locale sont gitignorés et générés par développeur, les clés privées App Store Connect sont soutenus par Keychain, la préparation bêta refuse les sorties de build symlinked, les URL de base relay sont validées avant d'entrer xcconfig, les builds officiels utilisent les identifiants de bundle canoniques et `OpenClawPushDistribution=official`, les builds locaux utilisent par défaut push direct/local et le versioning iOS épinglé pilote xcconfig et les notes de version Fastlane vérifiés.
- Mauvaises qualités : L'accès opérateur reste peu clair en dehors des mainteneurs, les artefacts de version sont locaux uniquement, `apps/ios/Config/Signing.xcconfig` porte les défauts d'équipe/bundle canoniques que les contributeurs locaux doivent remplacer, il n'y a pas de route d'installation publique et les enregistrements d'archive montrent des messages de disponibilité publique obsolètes ou contradictoires autour du statut TestFlight/App Store.
- Exclu de la qualité : La couverture de test, la profondeur CI et la preuve de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Expérimentale (42%)`
- Instructions de surface : évaluées par rapport à `references/completeness/ios-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le statut d'aperçu interne.
- Signaux négatifs : la note archivée a précédé le scoring de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Publier un statut d'installation/accès unique et faisant autorité pour l'aperçu interne, TestFlight et toute future route App Store publique.
- Ajouter un artefact de smoke test répétable pour l'archive/upload bêta, la vérification du build TestFlight installé et les drapeaux de build relay officiels.
- Décider si les artefacts IPA non signés/signés téléchargeables ne sont intentionnellement pas pris en charge et documenter cela à côté du chemin d'archive Fastlane.
- Enregistrer la propriété de l'application App Store Connect, l'opération de liste de testeurs, la restauration et les attentes de remise de version pour les mainteneurs.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/apps/ios/README.md` marque l'application comme super-alpha/usage interne uniquement, indique que la distribution publique n'est pas disponible, documente le déploiement manuel via Xcode, et documente l'archive locale plus le téléchargement TestFlight via Fastlane.
- `/Users/kevinlin/code/openclaw/docs/platforms/ios.md` indique que la disponibilité est en aperçu interne et décrit les builds distribués officiellement en utilisant le relais de push externe au lieu de publier les tokens APNs bruts à la passerelle.
- `/Users/kevinlin/code/openclaw/apps/ios/VERSIONING.md` définit les versions iOS CalVer épinglées, le comportement du train TestFlight, les fichiers de synchronisation des versions, et la promotion à partir de la version de la passerelle uniquement par action explicite du mainteneur.
- `/Users/kevinlin/code/openclaw/apps/ios/fastlane/metadata/README.md` documente le téléchargement de métadonnées, l'authentification App Store Connect, la génération des notes de version à partir du changelog iOS, et les fichiers d'informations d'examen.

## Source

- `/Users/kevinlin/code/openclaw/package.json` définit `ios:open`, `ios:gen`, `ios:build`, `ios:run`, `ios:beta:archive`, `ios:beta`, et les commandes de version iOS.
- `/Users/kevinlin/code/openclaw/apps/ios/project.yml` génère le projet Xcode, inclut les scripts de pré-compilation SwiftFormat et SwiftLint, mappe les paramètres de bundle/version, et définit par défaut Debug/Release sur les drapeaux de push direct/local.
- `/Users/kevinlin/code/openclaw/apps/ios/Config/Signing.xcconfig`, `apps/ios/LocalSigning.xcconfig.example`, et `scripts/ios-configure-signing.sh` définissent les valeurs par défaut de signature canoniques plus la génération locale des remplacements d'équipe et de bundle.
- `/Users/kevinlin/code/openclaw/scripts/ios-beta-prepare.sh`, `scripts/ios-beta-archive.sh`, `scripts/ios-beta-release.sh`, et `apps/ios/fastlane/Fastfile` préparent la xcconfig bêta, résolvent les numéros de build TestFlight, archivage, et téléchargement vers TestFlight.
- `/Users/kevinlin/code/openclaw/scripts/ios-asc-keychain-setup.sh` stocke le contenu `.p8` d'App Store Connect dans le Keychain macOS et écrit uniquement les clés env Fastlane non-secrètes.
- `/Users/kevinlin/code/openclaw/apps/ios/version.json`, `apps/ios/Config/Version.xcconfig`, `apps/ios/CHANGELOG.md`, et `apps/ios/fastlane/metadata/en-US/release_notes.txt` contiennent la version iOS épinglée, les valeurs par défaut xcconfig générées, le changelog, et les notes de version dérivées.
- `/Users/kevinlin/code/openclaw/.gitignore` ignore les projets Xcode générés, `.local-signing.xcconfig`, `LocalSigning.xcconfig`, `apps/ios/build/`, les artefacts IPA/dSYM locaux, les fichiers de provisionnement, et `apps/ios/fastlane/.env`.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/.github/workflows/ci.yml` installe XcodeGen/SwiftLint/SwiftFormat dans la lane Swift macOS, mais le workflow vérifié n'exécute pas la compilation `OpenClaw.xcodeproj` iOS, l'archive bêta Fastlane, ou le chemin de téléchargement TestFlight.
- `/Users/kevinlin/code/openclaw/package.json` expose les commandes locales `ios:build` et `ios:run` qui exercent la préparation de la signature, la génération de xcconfig de version, XcodeGen, xcodebuild, et le lancement du simulateur lorsqu'elles sont exécutées par un développeur.
- Aucun artefact de fumée de version TestFlight d'archive/téléchargement/installation-à-passerelle automatisé n'a été trouvé.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/test/scripts/ios-version.test.ts` couvre l'analyse CalVer épinglée, la normalisation de la version de passerelle, le rendu de Version.xcconfig, et l'extraction des notes de version.
- `/Users/kevinlin/code/openclaw/test/scripts/ios-pin-version.test.ts` couvre l'épinglage explicite et dérivé de la version iOS de la passerelle plus le comportement de synchronisation des artefacts générés.
- `/Users/kevinlin/code/openclaw/test/scripts/ios-team-id.test.ts` couvre l'analyse des candidats d'ID d'équipe Apple et la sélection utilisée par la configuration de signature.
- `/Users/kevinlin/code/openclaw/test/scripts/changed-lanes.test.ts` couvre le routage des modifications de fichiers de version iOS vers la lane `ios:version:check`.

## Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "iOS TestFlight" --json`

Résultats :

- Problème fermé #75684 `Request: iOS TestFlight Invite`.
- Problème fermé #72763 `Request iOS TestFlight Access - Adam J. Graham`.
- Problème fermé #64526 `Request iOS TestFlight Access`.

Requête :

`gitcrawl search openclaw/openclaw --query "TestFlight" --json`

Résultats :

- Problème fermé #75684 `Request: iOS TestFlight Invite`.
- Problème fermé #74869 `Request: iOS Node TestFlight invite`.
- Problème fermé #61639 `Request: TestFlight access for iOS app`.
- Problème fermé #72763 `Request iOS TestFlight Access - Adam J. Graham`.
- Problème fermé #64526 `Request iOS TestFlight Access`.

Requête :

`gitcrawl search openclaw/openclaw --query "iOS TestFlight signing fastlane" --json`

Résultats :

- Aucun résultat.

Requête :

`gitcrawl search openclaw/openclaw --query "iOS beta TestFlight OPENCLAW_PUSH_RELAY_BASE_URL" --json`

Résultats :

- Aucun résultat.

Requête :

`gitcrawl search openclaw/openclaw --query "iOS version changelog TestFlight metadata" --json`

Résultats :

- Aucun résultat.

Requête :

`gitcrawl search openclaw/openclaw --query "public TestFlight" --json`

Résultats :

- Aucun résultat.

Requête :

`gitcrawl search openclaw/openclaw --query "beta_archive" --json`

Résultats :

- Aucun résultat.

Requête :

`gitcrawl search openclaw/openclaw --query "OPENCLAW_PUSH_DISTRIBUTION official" --json`

Résultats :

- Aucun résultat.

## Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS TestFlight signing fastlane"`

Résultats :

- 2026-03-11 `iOS Alpha` : message du mainteneur disant qu'il allait fusionner la PR #42991 pour le flux de version bêta TestFlight.
- 2026-03-11 Miroir GitHub : PR #42991 `feat(ios): add local beta release flow`, résumant la préparation Fastlane/TestFlight, la régénération du projet Xcode, l'archive/export/téléchargement à partir de la source, la recherche du numéro de build App Store Connect, et l'empaquetage bêta de l'application de montre.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS beta TestFlight relay"`

Résultats :

- 2026-03-18 Miroir GitHub : commentaire d'examen sur la PR #48667 avertit de ne pas télécharger la sortie `beta_archive` en tant qu'IPA téléchargeable car le chemin de version bêta officiel intègre `OpenClawPushTransport=relay` et `OpenClawPushDistribution=official`.
- 2026-03-14 Miroir GitHub : problème #46446 `Request iOS TestFlight Beta Access - @catallo`.
- 2026-03-12 Résumé du mainteneur : les invitations TestFlight iOS ont été envoyées et le relais de notification push pré-alpha officiel était expédié ce jour-là.
- 2026-03-11 Miroir GitHub : PR #43369 `feat(push): add iOS APNs relay gateway`, incluant l'enregistrement du relais iOS, App Attest, et la configuration de push de build officiel.
- 2026-02-24 et 2026-02-25 Messages de support TestFlight expliquent les retards d'invitation, la gestion des adresses de relais Hide My Email, et les vérifications de rafraîchissement/boîte aux lettres TestFlight.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS TestFlight beta access"`

Résultats :

- 2026-04-25 Miroir GitHub : problème #61639 commentaire fermé comme implémenté après qu'un examen Codex ait affirmé que l'application avait dépassé la bêta réservée aux invités, tout en notant les docs obsolètes.
- 2026-04-18 Miroir GitHub : problème #68525 a demandé l'accès TestFlight iOS et a été fermé avec `Not available, build from source.`
- 2026-04-13 et 2026-04-08 Miroirs GitHub : demandes d'accès TestFlight iOS supplémentaires pour les capacités de nœud.
- 2026-04-05 Miroirs GitHub : les commentaires répétés ont dit qu'il n'y avait pas de TestFlight public et que les utilisateurs pouvaient construire à partir de la source avec Xcode.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "iOS TestFlight invite"`

Résultats :

- 2026-05-23 `general` : l'utilisateur a demandé le chemin d'accès iOS correct car la documentation mentionnait l'aperçu interne/TestFlight officiel mais aucun lien public App Store ou TestFlight n'était visible.
- 2026-04-26 Résumé : la lecture actuelle était toujours pré-alpha/aperçu mainteneur, la construction à partir de la source fonctionne, aucun flux TestFlight public officiel/chemin d'invitation n'existe, et la remise du compte développeur/organisation était toujours en cours de tri.
- 2026-04-13 `iOS node` : la réponse a dit qu'il n'y avait pas encore de chemin TestFlight iOS officiel/public d'invitation.
- 2026-04-03 `iOS App Testflight request` : l'utilisateur a signalé des difficultés à demander une invitation car son message Apple ID était bloqué.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "beta_archive official distribution iOS"`

Résultats :

- Aucun résultat.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "iOS build from source Xcode TestFlight"`

Résultats :

- 2026-03-11 Miroir GitHub : PR #42991 `feat(ios): add local beta release flow`.
- 2026-02-19 `Openclaw iOS Node app?` : la réponse a dit qu'il n'y avait pas de lien TestFlight public et que le chemin actuel était l'installation Xcode uniquement à partir de la source.
- 2026-02-15 `How can I get access to test the iPhone app with TestFlight` : la réponse a dit qu'il n'y avait pas de TestFlight public et a recommandé `pnpm ios:open`.
- 2026-02-14 `Access request for ios app` : la réponse a dit que l'application était alpha/aperçu interne, la construction à partir de la source était la plus rapide, et TestFlight nécessitait de partager une adresse e-mail Apple ID avec les mainteneurs.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "public TestFlight iOS source Xcode"`

Résultats :

- 2026-04-05 Miroirs GitHub : commentaires répétés sur les problèmes d'accès TestFlight ont dit qu'il n'y avait pas de TestFlight public, que les utilisateurs devraient surveiller Discord pour les annonces de bêta publique, et que l'application pouvait être construite à partir de la source avec Xcode.
