---
title: "Linux Gateway host - Host Setup and Updates Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Linux Gateway host - Host Setup and Updates Maturity Note

## Summary

Les chemins d'installation et de mise à jour Linux sont largement couverts : la documentation inclut l'installation par script, l'installation par gestionnaire de paquets, l'installation avec préfixe local, le changement de canal, la sortie de simulation/statut, la mise à jour npm par étapes, la récupération de fichiers appartenant à root, et la remise du redémarrage de Gateway géré. La qualité est encore en version bêta car les preuves d'archive récentes montrent des changements visibles pour les utilisateurs autour de la propriété, de la dénomination du gestionnaire de paquets, et des valeurs par défaut du runtime du programme d'installation.

## Category Scope

Inclus dans cette catégorie :

- Installation de Linux CLI : chemins d'installation de Linux CLI et vérification de l'opérateur après l'installation.
- Prérequis du runtime Node : exigences de version du runtime Node et vérifications des prérequis de l'hôte pour l'opération de Linux Gateway.
- Politique du gestionnaire de paquets : politique du gestionnaire de paquets et de la plateforme prise en charge pour les chemins d'installation et de mise à jour Linux.
- Chemin de mise à jour : flux de travail de mise à jour Linux, remise de paquet ou git, et vérification post-mise à jour.

## Features

- Installation de Linux CLI : chemins d'installation de Linux CLI et vérification de l'opérateur après l'installation.
- Prérequis du runtime Node : exigences de version du runtime Node et vérifications des prérequis de l'hôte pour l'opération de Linux Gateway.
- Politique du gestionnaire de paquets : politique du gestionnaire de paquets et de la plateforme prise en charge pour les chemins d'installation et de mise à jour Linux.
- Chemin de mise à jour : flux de travail de mise à jour Linux, remise de paquet ou git, et vérification post-mise à jour.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Stable (82%)`
- Rationale: la documentation d'installation et de mise à jour couvre tous les points d'entrée Linux normaux, et le code source de mise à jour gère les installations par étapes, le changement de canal, les invites de réparation, et la remise du redémarrage du daemon.
- Gaps: la documentation Linux répartit le risque de mise à jour spécifique à Linux sur les pages d'installation, de mise à jour, de plateforme et de doctor, de sorte que les opérateurs doivent connecter plusieurs pages pour les cas de réparation de fichiers appartenant à root ou de runtime de service.

## Quality Score

- Score: `Beta (78%)`
- Rationale: le comportement d'installation/mise à jour recommandé est utilisable, mais les preuves de problèmes actuels montrent que la confusion visible par l'opérateur et les modes de défaillance sont toujours en cours de clarification.
- Excluded from Quality: unit, integration, e2e, live, and runtime-flow test evidence.

## Completeness Score

- Score: `Stable (82%)`
- Surface instructions: evaluated against `references/completeness/linux-gateway-host.md`.
- Positive signals: archived docs, source, test, Gitcrawl, and Discrawl evidence cover the taxonomy scope for Linux CLI install, Node runtime prerequisites, Package-manager policy, Update path.
- Negative signals: la note archivée a précédé le scoring de Completeness de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de Coverage archivé.
- Missing capability branches: see `## Known Gaps` and `## Evidence` below for the recorded missing branches and operator-visible caveats.

## Known Gaps

- Collapse Linux install/update troubleshooting into a single operator checklist for root-owned paths, package-manager identity, service restarts, and managed Node.
- Ensure update/status/doctor text consistently names the active package manager and install root.

## Evidence

### Docs

- `docs/install/index.md:16-48` documents the installer script and Linux/macOS detection; `docs/install/index.md:52-66` documents the local-prefix managed runtime path.
- `docs/install/index.md:151-163` documents verification plus Linux systemd user service startup.
- `docs/install/updating.md:11-14` says `openclaw update` detects install type, fetches the latest version, runs doctor, and restarts Gateway.
- `docs/install/updating.md:19-46` covers channel switch, dry-run, JSON, and status output.
- `docs/install/updating.md:105-148` covers manual package-manager updates and Linux root-owned EACCES recovery.

### Source

- `src/cli/update-cli/update-command.ts` coordinates update mode, doctor repair guidance, service restart, and daemon install refresh.
- `src/infra/package-update-steps.ts:166-189` performs staged npm install behavior before replacing package contents.
- `src/infra/package-update-steps.ts:200-270` packages git-source installs for safer replacement.
- `src/cli/daemon-cli/install.ts:278-340` refreshes service metadata when token or wrapper drift is detected.

### Integration tests

- `test/scripts/install-cli.test.ts` covers local-prefix installer behavior.
- `test/scripts/test-install-sh-docker.test.ts` exercises installer behavior in a Linux container setting.
- `src/cli/update-cli.test.ts` covers service environment inheritance, systemd stopped-service handling, and service restart/update interactions.

### Unit tests

- `src/infra/package-update-steps.test.ts` covers package update planning behavior.
- `src/cli/update-cli.test.ts` covers package-manager update modes and Linux service handoff branches.

### Gitcrawl queries

- Specific query `Linux install.sh install-cli update channel npm git package manager root` returned no hits.
- Broader query `install.sh update` returned PR #81278 for local-prefix managed Node runtime clarity, issue #79558 for Node defaults between installer paths, issue #87732 for npm install being called pnpm, issue #78493 for mixed ownership after `sudo openclaw update`, and PR #82955 for downloaded-script validation.

### Discrawl queries

- Query `install.sh openclaw update` found beta-release support threads asking users to test updating existing installs, `openclaw status`, and `openclaw doctor`.
- The same query found maintainer discussion that update/doctor became harder because package-swap repair must cover more local install states.
