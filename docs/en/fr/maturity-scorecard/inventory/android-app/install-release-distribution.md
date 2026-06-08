---
title: "Android app - Distribution Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Android app - Distribution Maturity Note

## Résumé

L'application Android dispose d'un chemin d'installation public Google Play, de documentation de construction/exécution source, de saveurs de produits Play et tiers, d'automatisation de publication AAB signée, d'auto-incrémentation du code de version et de scripts de démarrage/performance. La couverture reste Alpha car le README de l'application marque toujours la reconstruction comme extrêmement alpha et laisse l'assurance qualité complète de bout en bout et le durcissement de la publication non vérifiés. La qualité est également Alpha : la division de la politique Play est un choix de conception solide, mais les preuves d'archive incluent une incompatibilité de protocole Play Store obsolète et une demande ouverte pour les artefacts de publication APK précompilés.

## Portée de la catégorie

Inclus dans cette catégorie :

- Chemin d'installation public Google Play : Chemin d'installation public Google Play et points d'entrée de construction/exécution source
- Chemin d'installation manuel : Chemin d'installation manuel et comportement de distribution Google Play.
- Vérifications de performance de démarrage et de fumée de publication : Vérifications de performance de démarrage et de fumée de publication pour la distribution d'applications Android.

## Fonctionnalités

- Chemin d'installation public Google Play : Chemin d'installation public Google Play et points d'entrée de construction/exécution source
- Chemin d'installation manuel : Chemin d'installation manuel et comportement de distribution Google Play.
- Vérifications de performance de démarrage et de fumée de publication : Vérifications de performance de démarrage et de fumée de publication pour la distribution d'applications Android.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (60%)`
- Signaux positifs : L'installation publique est documentée, les commandes de construction/exécution source existent, les scripts de package exposent les tâches assemble/install/test/release, l'automatisation de publication construit des AAB Play et tiers signés, et les scripts de benchmark Android couvrent les chemins de démarrage et d'interface utilisateur en ligne.
- Signaux négatifs : Le README de l'application marque toujours la reconstruction comme extrêmement alpha et laisse l'assurance qualité complète de bout en bout et le durcissement de la publication incomplets. Le chemin de publication est principalement documenté et scripté, mais aucun enregistrement public récurrent de fumée de publication n'a été trouvé.
- Lacunes d'intégration : Besoin d'une liste de contrôle de publication reproductible qui installe l'artefact Play, l'associe à une Gateway actuelle, exécute des scénarios de chat/voix/caméra/arrière-plan, vérifie la compatibilité des versions et enregistre l'état de la politique Play Console.

## Score de qualité

- Score : `Alpha (62%)`
- Rapports Gitcrawl : `Play Store Android app protocol mismatch` a trouvé le problème #85971 pour l'incompatibilité de protocole de l'application Android Play Store v2026.4.5 contre Gateway >= v2026.5.12 et le problème #87216 comme rapport d'incompatibilité de protocole de configuration LAN manuel connexe. `Android APK releases` a trouvé le problème #9443 demandant des publications APK Android précompilées.
- Rapports Discrawl : La recherche a trouvé un message d'assistance du 19 mai indiquant que l'application Play Store était obsolète et avait une incompatibilité de protocole ; l'utilisateur a construit une application plus récente localement puis a rencontré un état connecté/opérateur hors ligne.
- Bonnes qualités : Les saveurs Play et tiers séparent les permissions restreintes de Google Play des surfaces SMS, journal des appels et photos réservées au chargement latéral. Les propriétés de signature de publication sont conservées localement uniquement, les bundles de publication sont copiés dans un répertoire de sortie prévisible, et les signatures AAB de publication sont vérifiées.
- Mauvaises qualités : La distribution est toujours fragile pour les utilisateurs ordinaires car Play peut être en retard sur les changements de protocole Gateway, les artefacts APK ne sont pas entièrement productisés, et la documentation dit explicitement que le durcissement de la publication est inachevé.
- Exclu de la qualité : La couverture des tests et la preuve du flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Alpha (60%)`
- Instructions de surface : évaluées par rapport à `references/completeness/android-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le chemin d'installation public Google Play, le chemin d'installation manuel, les vérifications de performance de démarrage et de fumée de publication.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Publier et enregistrer un chemin de fumée Play actuel par rapport au protocole Gateway actuel.
- Décider si les APK de publication GitHub ou les artefacts AAB/APK tiers font partie de la promesse de distribution prise en charge.
- Ajouter des preuves de durcissement de publication pour les déclarations de politique Play, la signature d'application, l'asymétrie de version, la restauration et l'appairage d'installation fraîche.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/android.md` lie l'application Google Play officielle, décrit Android comme un nœud compagnon et pointe vers la source sous `apps/android`.
- `/Users/kevinlin/code/openclaw/apps/android/README.md` marque la reconstruction comme extrêmement alpha, énumère les éléments de la liste de contrôle de reconstruction, documente les constructions Play et tiers, et appelle l'assurance qualité complète de bout en bout et le durcissement de la publication comme non vérifiés.
- `/Users/kevinlin/code/openclaw/README.md` énumère Android comme un nœud optionnel avec les familles Connect, Chat, Voice, Canvas, Camera, Screen et device command.

### Source

- `/Users/kevinlin/code/openclaw/package.json` définit `android:assemble`, `android:install`, `android:bundle:release`, `android:test`, `android:test:integration`, lint et variantes tiers.
- `/Users/kevinlin/code/openclaw/apps/android/app/build.gradle.kts` définit `applicationId = "ai.openclaw.app"`, `minSdk = 31`, `targetSdk = 36`, saveurs Play et tiers, vérifications de signature de publication, réduction R8/ressource, avertissements lint comme erreurs et version `2026.5.28`.
- `/Users/kevinlin/code/openclaw/apps/android/scripts/build-release-aab.ts` auto-incrémente le nom/code de version, construit les bundles de publication Play et tiers, vérifie les signatures avec `jarsigner` et imprime les hachages SHA-256.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/play/AndroidManifest.xml` supprime les permissions média restreintes de la saveur Play ; `/Users/kevinlin/code/openclaw/apps/android/app/src/thirdParty/AndroidManifest.xml` ajoute les permissions SMS et journal des appels pour la saveur tiers.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/apps/android/benchmark/src/main/java/ai/openclaw/app/benchmark/StartupMacrobenchmark.kt` et `apps/android/scripts/perf-startup-benchmark.sh` couvrent la mesure du démarrage.
- `/Users/kevinlin/code/openclaw/apps/android/scripts/perf-online-benchmark.sh` mesure les chemins de lancement vers connexion, onglet Screen et onglet Chat sur un appareil connecté.
- Aucune installation Play Store actuelle vers artefact de fumée de publication Gateway appairé n'a été trouvée.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/ui/OnboardingFlowLogicTest.kt` couvre la logique de flux d'intégration adjacente à l'installation.
- `/Users/kevinlin/code/openclaw/apps/android/app/src/test/java/ai/openclaw/app/SecurePrefsTest.kt` et `SecurePrefsNotificationForwardingTest.kt` couvrent l'état de l'application stockée utilisé après l'installation.
- L'automatisation AAB de publication elle-même ne semble pas avoir de test unitaire dédié.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "Play Store Android app protocol mismatch" --json`

Résultats :

- Problème #85971 `[Bug] Play Store Android app v2026.4.5 protocol mismatch against Gateway >= v2026.5.12 - clawx user report`.
- Problème #87216 `Android manual LAN setup parses ws:// as host ws and resolves http://ws:<port>`.

Requête :

`gitcrawl search openclaw/openclaw --query "Android APK releases" --json`

Résultats :

- Problème #9443 `Request: Prebuilt Android APK releases`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "Android Play Store protocol mismatch"`

Résultats :

- Message d'assistance du 2026-05-19 : un utilisateur a construit l'application Android localement car l'application Play Store était obsolète et avait une incompatibilité de protocole ; la construction locale plus récente s'est connectée via Tailscale mais a signalé l'opérateur hors ligne.
