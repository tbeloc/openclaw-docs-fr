---
title: "Application compagnon Windows native - Note de maturité Installation et Mises à jour"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagnon Windows native - Note de maturité Installation et Mises à jour

## Résumé

Windows native dispose d'une machinerie CLI et Gateway d'installation significative, incluant
`install.ps1`, la gestion des Tâches planifiées, le repli du dossier Démarrage, et les scripts de smoke Parallels
Windows. Aucun de ceux-ci n'est une application compagnon Windows officielle empaquetée. L'histoire de l'empaquetage d'application reste un travail ouvert, avec des preuves d'archive pointant
vers les téléchargements officiels et les combinaisons x64/ARM/WSL comme non résolues.

## Portée de la catégorie

Inclus dans cette catégorie :

- Téléchargement officiel de l'application : chemin de téléchargement ou d'installation officiel de l'application pour l'application compagnon Windows native.
- Empaquetage MSI/MSIX/App Installer/winget : empaquetage MSI/MSIX/App Installer/winget, signature, mise à jour, restauration, désinstallation et entrées de bureau
- Gestion de l'architecture Windows pour x64 : gestion de l'architecture Windows pour x64 et ARM64
- Canal de version de l'application : canal de version de l'application, gestion de l'architecture et disponibilité des mises à jour.

## Fonctionnalités

- Téléchargement officiel de l'application : chemin de téléchargement ou d'installation officiel de l'application pour l'application compagnon Windows native.
- Empaquetage MSI/MSIX/App Installer/winget : empaquetage MSI/MSIX/App Installer/winget, signature, mise à jour, restauration, désinstallation et entrées de bureau
- Gestion de l'architecture Windows pour x64 : gestion de l'architecture Windows pour x64 et ARM64
- Canal de version de l'application : canal de version de l'application, gestion de l'architecture et disponibilité des mises à jour.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (5%)`
- Signaux positifs : les flux CLI/Gateway d'installation et de mise à jour Windows native disposent d'un programme d'installation PowerShell et d'une couverture de smoke Parallels.
- Signaux négatifs : il n'existe pas de paquet d'application compagnon Windows officiel, de cible d'installation, de canal de mise à jour, de métadonnées de version ou d'intégration de bureau dans le main actuel.
- Lacunes d'intégration : aucun chemin d'installation/mise à jour/désinstallation d'application, signature de paquet, lancement d'application, enregistrement de barre d'état système ou preuve de mise à niveau d'application n'existe pour cette surface.

Étiquettes de couverture :

- `Adorable` : 95-100
- `Stable` : 80-95
- `Bêta` : 70-80
- `Alpha` : 50-70
- `Expérimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel sur
le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par
eux-mêmes.

## Score de qualité

- Score : `Expérimental (25%)`
- Rapports Gitcrawl : `#81673` suit les téléchargements officiels de compagnon Windows/Linux ; `#73315` propose un MVP de compagnon de bureau mais reste ouvert.
- Rapports Discrawl : la discussion du responsable dit que l'installation n'est pas encore robuste et l'application a des combinaisons x64/ARM/Windows/WSL à gérer.
- Bonnes qualités : le code d'installation CLI Windows native adjacent est conscient de la plateforme et la documentation sépare clairement le CLI/Gateway native de l'application compagnon prévue.
- Mauvaises qualités : la propriété de l'empaquetage d'application, le canal de version, la signature d'application et la sémantique de mise à jour/désinstallation ne sont pas définis dans le dépôt supporté.
- Exclu de la qualité : les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel n'ont pas été utilisées pour augmenter ou diminuer la Qualité.

Étiquettes de qualité :

- `Adorable` : 95-100
- `Stable` : 80-95
- `Bêta` : 70-80
- `Alpha` : 50-70
- `Expérimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel
comme entrée de notation.

## Score de complétude

- Score : `Expérimental (5%)`
- Instructions de surface : évaluées par rapport à `references/completeness/native-windows-companion-app.md`.
- Signaux positifs : les preuves de docs archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le téléchargement officiel de l'application, l'empaquetage MSI/MSIX/App Installer/winget, la gestion de l'architecture Windows pour x64, le canal de version de l'application.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucun téléchargement ou cible d'empaquetage officiel d'application compagnon Windows n'est présent.
- Aucun contrat de signature d'application, d'identité d'application, de mise à jour, de restauration ou de désinstallation n'est documenté.
- Le travail externe/prototype d'application compagnon Windows n'est pas intégré au chemin de version supporté.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:27-43` documente l'état d'installation CLI/Gateway Windows native et les avertissements de repli de Tâche planifiée.
- `/Users/kevinlin/code/openclaw/docs/install/index.md` documente `install.ps1` pour l'installation CLI Windows et identifie l'installation du service Windows native comme Tâche planifiée plus repli du dossier Démarrage.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:246-249` dit qu'il n'existe pas encore d'application compagnon Windows.

### Source

- `/Users/kevinlin/code/openclaw/scripts/install.ps1` implémente le programme d'installation CLI Windows et gère l'architecture Node avec `Get-WindowsNodeArchitecture`.
- `/Users/kevinlin/code/openclaw/src/daemon/service.ts:288-300` enregistre le support du service Gateway `win32` comme une Tâche planifiée.
- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.ts:45-52` bascule des échecs `schtasks` vers les entrées du dossier Démarrage.
- Aucun `apps/windows`, `apps/desktop`, `.msix`, `.appinstaller` ou manifeste de paquet compagnon n'a été trouvé dans le main actuel.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels-windows-smoke.sh` pilote le harnais de smoke Parallels Windows pour l'installation et la mise à jour CLI/Gateway Windows native.
- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels/windows-smoke.ts` exerce l'installation fraîche, la configuration du fournisseur, le tour d'agent, le démarrage de Gateway, la mise à jour et les vérifications de récupération pour la voie CLI/Gateway, pas un paquet d'application.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.install.test.ts`
- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.startup-fallback.test.ts`
- `/Users/kevinlin/code/openclaw/src/infra/windows-install-roots.test.ts`
- Aucun test unitaire d'empaquetage d'application compagnon n'a été trouvé.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "official companion downloads Windows Linux" --json`
- `gitcrawl search openclaw/openclaw --query "Tauri desktop companion Windows Linux" --json`

Résultats :

- `#81673` problème ouvert : construire les téléchargements officiels de compagnon OpenClaw pour Windows et Linux.
- `#73315` PR ouvert : ajouter le MVP de compagnon de bureau Tauri v2 sous `apps/desktop` pour Linux/Windows.

### Requêtes Discrawl

Requête :

- `/Users/kevinlin/.local/bin/discrawl search --limit 6 "official companion downloads Windows Linux"`
- `/Users/kevinlin/.local/bin/discrawl search --limit 6 "Windows companion pairing install x64 arm WSL"`

Résultats :

- La première requête n'a retourné aucun message.
- La deuxième requête a retourné un message du responsable du `2026-05-06` disant que l'objectif de l'application native Windows inclut la parité d'installation et de paramètres, mais l'appairage et l'installation ne sont pas robustes et les combinaisons x64/ARM/Windows/WSL restent une préoccupation.
