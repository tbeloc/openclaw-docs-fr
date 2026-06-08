---
title: "Raspberry Pi / petits appareils Linux - Note de maturité du service systemd et de la persistance au démarrage"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Raspberry Pi / petits appareils Linux - Note de maturité du service systemd et de la persistance au démarrage

## Résumé

Cette note migre les preuves de maturité archivées pour `Raspberry Pi / petits appareils Linux` / `Persistance au démarrage systemd et cycle de vie du service` dans l'inventaire actuel de la fiche d'évaluation process-version-3.

## Portée de la catégorie

Cette catégorie évalue la zone de capacité Raspberry Pi / petits appareils Linux représentée par ces fonctionnalités de taxonomie :

- Persistance au démarrage systemd et cycle de vie du service : Portée des preuves pour la persistance au démarrage systemd et le cycle de vie du service.

## Fonctionnalités

- Installation du service utilisateur : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour l'installation du service utilisateur pour la persistance au démarrage systemd et le cycle de vie du service.
- Persistance linger/démarrage : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour la persistance linger/démarrage pour la persistance au démarrage systemd et le cycle de vie du service.
- Drop-ins de service : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour les drop-ins de service pour la persistance au démarrage systemd et le cycle de vie du service.
- Ajustement du redémarrage : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour l'ajustement du redémarrage pour la persistance au démarrage systemd et le cycle de vie du service.
- Inspection du statut/journal : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour l'inspection du statut/journal pour la persistance au démarrage systemd et le cycle de vie du service.
- Sauvegarde/restauration : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour la sauvegarde/restauration pour la persistance au démarrage systemd et le cycle de vie du service.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : La documentation des services utilisateur systemd Linux, la vérification du service Raspberry Pi, la gestion de linger, les commandes de statut du service, l'ajustement du démarrage et les protections systemd au niveau du code source sont solides.
- Signaux négatifs : Les problèmes de cycle de vie du service spécifiques à Pi apparaissent toujours dans les rapports d'archive, en particulier autour des unités système dupliquées, de l'état obsolète et de l'état d'authentification/session de longue durée.
- Lacunes d'intégration : Le démarrage et le comportement systemd ont une couverture source/test large, mais aucune porte de cycle de vie du service Pi matériel inspectée n'a été trouvée.

## Score de qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : La PR #83489 traite une course au démarrage du service Gateway et nomme Raspberry Pi/Linux systemd dans le scénario ; d'autres rapports mentionnent la perte d'état systemd Linux arm64.
- Rapports Discrawl : Les répétitions systemd Pi 5 Debian arm64, les jetons obsolètes et les problèmes de reconnexion apparaissent dans l'historique du support.
- Bonnes qualités : Le cycle de vie du service est l'une des parties les plus matures de l'histoire Linux, avec des docs et des sources convergeant sur les services utilisateur, linger, le statut et le comportement de redémarrage.
- Mauvaises qualités : Les modes de défaillance sont subtils pour les utilisateurs Pi sans interface et peuvent impliquer à la fois l'état du service et l'état d'authentification.
- Exclus de la qualité : preuves de test unitaire, intégration, e2e, live, runtime-flow et smoke test manuel.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/raspberry-pi-small-linux-devices.md`.
- Signaux positifs : les preuves archivées docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'installation du service utilisateur, la persistance linger/démarrage, les drop-ins de service, l'ajustement du redémarrage, l'inspection du statut/journal, la sauvegarde/restauration.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucun fixture systemd spécifique à Pi ou smoke matériel n'a été trouvé.
- L'état du service obsolète et les problèmes d'unité dupliquée sont traités de manière réactive plutôt que représentés dans une liste de contrôle de l'opérateur Pi.
- La persistance au démarrage est documentée, mais n'est pas liée à un signal de version de bout en bout pour les petits appareils Linux.

## Preuves

### Docs

- `docs/platforms/linux.md:64-70` oriente les utilisateurs Linux vers les unités utilisateur systemd par défaut.
- `docs/platforms/linux.md:72-99` donne une unité utilisateur systemd minimale.
- `docs/install/raspberry-pi.md:92-104` utilise l'intégration avec `--install-daemon`.
- `docs/install/raspberry-pi.md:107-128` vérifie le statut du daemon et de la Gateway et affiche l'interface utilisateur de contrôle en tunnel SSH.
- `docs/install/raspberry-pi.md:150-172` documente les drop-ins systemd réduisant la mémoire, le comportement de redémarrage, les délais d'expiration et `loginctl enable-linger`.
- `docs/vps.md:97-127` fournit une liste de contrôle d'ajustement systemd qui s'applique également aux petits hôtes ARM.

### Source

- `src/commands/systemd-linger.ts:14-25` restreint la gestion de linger à Linux et vérifie la disponibilité de systemd.
- `src/commands/systemd-linger.ts:48-83` émet les raisons/actions de linger visibles par l'utilisateur et peut activer linger.
- `src/commands/status.daemon.ts:18-39` résume le statut du daemon.
- `src/cli/gateway-cli/run.ts:350-358` gère les codes de sortie du verrou systemd.
- `src/cli/gateway-cli/run.ts:398-460` gère la récupération du verrou supervisé et l'évitement de la boucle de redémarrage systemd.

### Tests d'intégration

- `package.json:1777` définit le benchmark de redémarrage de la Gateway.
- Les scripts e2e et smoke de l'installateur vérifient généralement les chemins daemon/install, mais pas sur le matériel systemd Pi.

### Tests unitaires

- La logique de redémarrage de la Gateway et du statut du daemon est testée dans les suites CLI/Gateway.
- Aucun fixture de test unitaire Raspberry Pi systemd n'a été trouvé.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --json --query "Raspberry Pi systemd linger gateway"`

Résultats :

- A retourné la PR #83489, "Fix gateway service startup race", avec des extraits mentionnant Raspberry Pi, Linux/systemd, le port Gateway `18789` et les anciennes unités système dupliquées.

Requête : `gitcrawl search openclaw/openclaw --json --query "Raspberry Pi low memory OpenClaw"`

Résultats :

- A retourné un rapport Raspberry Pi Linux arm64 systemd Gateway où l'historique cron a perdu l'état de session de sauvegarde.

### Requêtes Discrawl

Requête : `/Users/kevinlin/.local/bin/discrawl search --limit 5 "Raspberry Pi systemd OpenClaw"`

Résultats :

- A trouvé des threads de support Pi/Linux systemd, y compris des agents Telegram avec des défaillances d'authentification Codex et une boucle systemd Pi 5 Debian arm64 avec des symptômes de reconnexion/certificat.
