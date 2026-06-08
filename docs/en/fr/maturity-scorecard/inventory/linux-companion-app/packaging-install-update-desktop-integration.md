---
title: "Application compagne Linux - Note de maturité de distribution d'application"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne Linux - Note de maturité de distribution d'application

## Résumé

Les chemins d'installation de la CLI Linux et de la passerelle sont documentés et testés en fumée, mais l'empaquetage natif de l'application compagne n'est pas livré. L'enregistrement d'archive actif signale les téléchargements officiels de compagnons Windows/Linux comme un besoin ouvert, et les PR Linux ouvertes excluent ou reportent explicitement les artefacts de distribution tels que `.deb`, `.rpm`, Snap, Flatpak et AppImage.

## Portée de la catégorie

Inclus dans cette catégorie :

- Paquet d'application natif : disponibilité du paquet d'application compagne Linux natif et chemin d'installation.
- Cibles de paquet de distribution : cibles de paquet de distribution, fichiers de bureau, icônes, démarrage automatique et métadonnées de mise à jour
- Métadonnées de version officielle : métadonnées de version officielle pour les consoles en aval

## Fonctionnalités

- Paquet d'application natif : disponibilité du paquet d'application compagne Linux natif et chemin d'installation.
- Cibles de paquet de distribution : cibles de paquet de distribution, fichiers de bureau, icônes, démarrage automatique et métadonnées de mise à jour
- Métadonnées de version officielle : métadonnées de version officielle pour les consoles en aval

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (0%)`
- Signaux positifs : un test en fumée du programme d'installation CLI Linux existe et la documentation décrit le chemin d'installation de la passerelle pris en charge.
- Signaux négatifs : aucun programme d'installation d'application compagne Linux enregistré, manifeste de paquet, fichier de bureau, métadonnées appstream, flux de mise à jour ou chemin d'artefact de version n'existe dans l'arborescence source actuelle.
- Lacunes d'intégration : aucun test en fumée d'installation/mise à jour d'application compagne Linux natif n'a été trouvé.

## Score de qualité

- Score : `Expérimental (18%)`
- Rapports Gitcrawl : le problème #81673 est ouvert pour les téléchargements officiels de compagnons Windows/Linux ; la PR #59859 indique qu'elle n'ajoute pas d'artefacts `.deb`, `.rpm` ou Snap ; la PR #61576 indique qu'il n'y a pas encore d'empaquetage Flatpak/deb/AppImage.
- Rapports Discrawl : les recherches spécifiques à l'empaquetage n'ont retourné aucune résolution de support direct ou annonce de version pour les téléchargements officiels de compagnons Linux.
- Bonnes qualités : la documentation actuelle ne fait pas de fausse publicité pour un téléchargement d'application Linux, et le problème ouvert énonce les critères d'acceptation de l'empaquetage en aval.
- Mauvaises qualités : il n'existe pas de cible d'empaquetage officielle, de contrat de métadonnées, de matrice de support de distribution, de canal de mise à jour ou d'interface utilisateur d'installation pour une application compagne Linux.
- Exclu de la qualité : les preuves de test unitaire, d'intégration, e2e, en direct et de flux d'exécution réel sont exclues de ce score de qualité.

## Score de complétude

- Score : `Expérimental (0%)`
- Instructions de surface : évaluées par rapport à `references/completeness/linux-companion-app.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le paquet d'application natif, les cibles de paquet de distribution, les métadonnées de version officielle.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Définir les cibles de paquet initiales telles que Flatpak, AppImage, `.deb`, `.rpm` ou source-build-only.
- Définir les métadonnées de version et la sémantique de mise à jour pour la documentation et les consoles en aval.
- Ajouter la vérification de paquet pour l'installation, le lancement, la mise à jour, la restauration et la désinstallation.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/platforms/linux.md:15` : le chemin rapide pour les débutants est Gateway-on-Linux, pas une installation d'application native.
- `/Users/kevinlin/code/openclaw/docs/platforms/linux.md:25` : les liens d'installation sont des chemins CLI/Gateway génériques.
- `/Users/kevinlin/code/openclaw/docs/platforms/index.md:42` : les conseils d'installation de service couvrent les services Gateway gérés par CLI, pas l'empaquetage d'application compagne Linux.
- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md:162` : macOS dispose d'un flux de travail de construction/développement natif et d'un script d'empaquetage d'application, montrant que l'empaquetage d'application native existe pour macOS mais pas pour Linux.

### Source

- `find apps -maxdepth 3 -type f \( -name "Package.swift" -o -name "build.gradle.kts" -o -name "package.json" -o -name "*.plist" -o -name "*.desktop" -o -name "*.service" \)` a retourné des fichiers Gradle Android, des plists iOS/macOS, des paquets Swift et des paquets partagés, mais aucun `.desktop` Linux, appstream, Flatpak, Snap, AppImage, Meson, Cargo ou manifeste de paquet dans l'extraction actuelle.
- `/Users/kevinlin/code/openclaw/package.json` publie les actifs CLI/runtime et la documentation via npm, pas les artefacts d'application de bureau Linux natifs.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/.github/workflows/install-smoke.yml:476` : le test en fumée du programme d'installation Rocky Linux vérifie `install.sh` et `openclaw --version`.
- `/Users/kevinlin/code/openclaw/.github/workflows/install-smoke.yml:485` : le test en fumée du programme d'installation CLI Rocky Linux vérifie `install-cli.sh`, pas une application compagne.
- Aucun test d'intégration d'installation, de lancement de bureau, de mise à jour ou de désinstallation d'application compagne Linux natif n'a été trouvé.

### Tests unitaires

- Aucun test unitaire d'empaquetage d'application Linux enregistré n'a été trouvé.
- `/Users/kevinlin/code/openclaw/test/scripts/package-mac-app.test.ts:56` : les tests d'empaquetage existent pour l'application macOS, illustrant l'équivalent Linux manquant.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "official companion downloads windows linux" --mode keyword --limit 8 --json`
- `gitcrawl search openclaw/openclaw --query "Linux app AppImage Flatpak Snap tray" --mode keyword --limit 8 --json`
- `gitcrawl gh issue view 81673 --repo openclaw/openclaw --json number,title,state,author,updatedAt,body,url`
- `gitcrawl gh pr view 59859 --repo openclaw/openclaw --json number,title,state,author,updatedAt,body,headRefName,baseRefName,url`
- `gitcrawl gh pr view 61576 --repo openclaw/openclaw --json number,title,state,author,updatedAt,body,headRefName,baseRefName,url`

Résultats :

- La requête de téléchargements officiels a retourné le problème ouvert #81673, `Build official OpenClaw companion downloads for Windows and Linux`, plus une référence de PR de suivi large.
- La requête AppImage/Flatpak/Snap n'a retourné aucun résultat.
- Le problème #81673 demande des cibles d'empaquetage officielles, des artefacts ou manifestes de version, une documentation de matrice de support et des URL stables pour la liaison en aval.
- La PR #59859 indique explicitement que les artefacts d'empaquetage de distribution tels que `.deb`, `.rpm` et Snap ne sont pas inclus.
- La PR #61576 énumère aucun empaquetage Flatpak/deb/AppImage comme une lacune connue.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "official companion downloads windows linux"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "Linux app AppImage Flatpak Snap tray"`

Résultats :

- Les deux recherches spécifiques à l'empaquetage n'ont retourné aucune preuve de version/téléchargement d'application compagne Linux directe.
- L'absence de preuve de version directe est neutre pour la qualité après les vérifications de fraîcheur, mais elle ne fournit aucun signal positif pour une surface de paquet prise en charge.
