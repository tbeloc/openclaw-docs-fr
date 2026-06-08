---
title: "Raspberry Pi / small Linux devices - Hardware Support Boundary Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Raspberry Pi / small Linux devices - Hardware Support Boundary Maturity Note

## Résumé

Cette note migre les preuves de maturité archivées pour `Raspberry Pi / small Linux devices` / `Hardware-specific Release Smoke and Support Boundary` dans l'inventaire du scorecard de la version actuelle du processus-version-3.

## Portée de la catégorie

Cette catégorie évalue la zone de capacité Raspberry Pi / small Linux devices représentée par ces fonctionnalités de taxonomie :

- Hardware-specific Release Smoke and Support Boundary: Portée des preuves pour Hardware-specific Release Smoke and Support Boundary.

## Fonctionnalités

- Supported Pi model selection: Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour Supported Pi model selection pour Hardware Support Boundary.
- 64-bit ARM boundary: Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour 64-bit ARM boundary pour Hardware Support Boundary.
- Unsupported device guidance: Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour Unsupported device guidance pour Hardware Support Boundary.
- Slow-device caveats: Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour Slow-device caveats pour Hardware Support Boundary.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score: `Alpha (55%)`
- Signaux positifs: La documentation Raspberry Pi fournit une limite de support réelle pour les niveaux de modèles, la RAM, le stockage, l'architecture du système d'exploitation, Node, le swap, l'évitement des LLM locaux et les avertissements binaires ARM.
- Signaux négatifs: Aucun smoke matériel récurrent, aucune porte de version ou artefact enregistré n'a été trouvé pour Pi 4, Pi 5, Pi Zero ou Pi OS.
- Lacunes d'intégration: Le smoke Docker arm64 n'est pas identique au smoke matériel pour les E/S de carte SD, la pression RAM, la persistance du démarrage systemd, Tailscale, le runtime du canal ou les binaires d'aide natifs.

## Score de qualité

- Score: `Alpha (58%)`
- Rapports Gitcrawl: les recherches de smoke matériel n'ont pas trouvé de porte de version positive, tandis que les problèmes Pi connexes continuent d'apparaître.
- Rapports Discrawl: les vrais utilisateurs exploitent OpenClaw sur des appareils Pi et rencontrent des problèmes de performance, d'appairage, d'authentification, de QMD/natif et de gestionnaire de paquets.
- Bonnes qualités: La limite de support documentée est honnête concernant Pi Zero, Pi 3B+, la mémoire, le stockage et les limites des LLM locaux.
- Mauvaises qualités: Sans signal de version, les revendications de qualité pour cette surface dépendent de Linux générique plus l'utilisation anecdotique de Pi.
- Exclus de la qualité: preuves de test unitaire, intégration, e2e, en direct, flux d'exécution et smoke test manuel.

## Score de complétude

- Score: `Alpha (55%)`
- Instructions de surface: évaluées par rapport à `references/completeness/raspberry-pi-small-linux-devices.md`.
- Signaux positifs: les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Supported Pi model selection, 64-bit ARM boundary, Unsupported device guidance, Slow-device caveats.
- Signaux négatifs: la note archivée a précédé le score de complétude du processus-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucun flux de travail inspecté ne prouve l'installation, le démarrage du daemon, la disponibilité de Gateway, l'accès à l'interface utilisateur de contrôle, l'authentification et un canal sur le matériel Pi.
- Aucun artefact détenu par le scorecard n'enregistre le modèle Pi, l'image du système d'exploitation, l'architecture, la RAM, le stockage, la version de Node et la version d'OpenClaw à partir d'une exécution de smoke.
- Aucun libellé de triage de problème récurrent ou liste de contrôle de version n'a été trouvé pour les petits appareils Linux.

## Preuves

### Docs

- `docs/install/raspberry-pi.md:12-24` répertorie Pi 5, les niveaux de mémoire Pi 4, Pi 3B+, Pi Zero 2 W et le matériel minimum/recommandé.
- `docs/install/raspberry-pi.md:26-33` nécessite Raspberry Pi OS 64 bits ou Debian/Ubuntu ARM64.
- `docs/install/raspberry-pi.md:193-196` énonce la mise en garde ARM64 pour les outils CLI Go/Rust optionnels.
- `docs/help/faq-first-run.md:158-178` donne une réponse de support Pi large et des conseils pratiques.
- `docs/help/faq.md:833-842` présente un modèle courant d'une Gateway sur un Raspberry Pi plus des nœuds et des agents ailleurs.
- `docs/help/faq.md:969-978` dit que les petites boîtes VPS/classe Pi peuvent héberger Gateway tandis que les nœuds laptop/téléphone fournissent des outils locaux.

### Source

- `scripts/test-install-sh-docker.sh:16-34` peut choisir une plateforme Docker smoke `linux/arm64`, mais l'inspection du code source n'a pas montré de cible matérielle Pi réelle.
- `scripts/install.sh:144-150` reconnaît les architectures ARM.
- `scripts/install-cli.sh:338-346` supporte les chemins Node arm64/aarch64 et x64 local-prefix.

### Tests d'intégration

- `package.json:1735` et `package.json:1738` définissent les scripts e2e/smoke du programme d'installation.
- `package.json:1778` définit les vérifications de mémoire au démarrage.
- Aucun script de smoke de version matérielle Pi ou artefact enregistré n'a été trouvé.

### Tests unitaires

- Les tests unitaires couvrent des éléments du comportement pertinent pour Linux/ARM tels que l'encapsulation OOM, mais aucun test unitaire ne peut remplacer le smoke matériel.

### Requêtes Gitcrawl

Requête: `gitcrawl search openclaw/openclaw --json --query "hardware smoke Raspberry Pi release OpenClaw"`

Résultats:

- Aucun fil correspondant retourné.

Requête: `gitcrawl search openclaw/openclaw --json --query "small Linux device OpenClaw"`

Résultats:

- Discussions Linux et plateforme générales retournées, mais aucune porte de version axée sur les petits appareils.

### Requêtes Discrawl

Requête: `/Users/kevinlin/.local/bin/discrawl search --limit 5 "Raspberry Pi OpenClaw"`

Résultats:

- Rapports d'utilisateurs et de contributeurs trouvés sur l'utilisation prévue et réelle de Raspberry Pi, y compris Pi 3B+ et Pi 4 2GB.

Requête: `/Users/kevinlin/.local/bin/discrawl search --limit 5 "Pi 5 aarch64 OpenClaw gateway"`

Résultats:

- Problèmes de support Pi 5/aarch64 trouvés autour de la latence, des plantages d'installation, des poignées de main Gateway, du comportement QMD/natif et de la charge CPU du plugin.
