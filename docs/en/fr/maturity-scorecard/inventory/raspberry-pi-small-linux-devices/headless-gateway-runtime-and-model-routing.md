---
title: "Raspberry Pi / small Linux devices - Gateway Runtime Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Raspberry Pi / small Linux devices - Gateway Runtime Maturity Note

## Résumé

Cette note migre les preuves de maturité archivées pour `Raspberry Pi / small Linux devices` / `Headless Gateway Runtime and Model Routing` dans l'inventaire actuel du scorecard process-version-3.

## Portée de la catégorie

Inclus dans cette catégorie :

- Processus Always-on Gateway : Définit la configuration du processus Always-on Gateway, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Headless Gateway et Model Setup.
- Configuration du modèle cloud : Définit la configuration du modèle cloud, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Headless Gateway et Model Setup.
- Démarrage du canal : Définit la configuration du démarrage du canal, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Headless Gateway et Model Setup.
- Santé/statut de la passerelle : Définit la configuration de la santé/statut de la passerelle, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Headless Gateway et Model Setup.
- Installation du service utilisateur : Définit la configuration de l'installation du service utilisateur, les identifiants, la configuration et le comportement de vérification de l'opérateur pour systemd Service et Boot Persistence.
- linger/boot persistence : Définit la configuration de linger/boot persistence, les identifiants, la configuration et le comportement de vérification de l'opérateur pour systemd Service et Boot Persistence.
- Service drop-ins : Définit la configuration des Service drop-ins, les identifiants, la configuration et le comportement de vérification de l'opérateur pour systemd Service et Boot Persistence.
- Restart tuning : Définit la configuration de Restart tuning, les identifiants, la configuration et le comportement de vérification de l'opérateur pour systemd Service et Boot Persistence.
- Status/log inspection : Définit la configuration de Status/log inspection, les identifiants, la configuration et le comportement de vérification de l'opérateur pour systemd Service et Boot Persistence.
- Backup/restore : Définit la configuration de Backup/restore, les identifiants, la configuration et le comportement de vérification de l'opérateur pour systemd Service et Boot Persistence.

## Fonctionnalités

- Processus Always-on Gateway : Définit la configuration du processus Always-on Gateway, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Headless Gateway et Model Setup.
- Configuration du modèle cloud : Définit la configuration du modèle cloud, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Headless Gateway et Model Setup.
- Démarrage du canal : Définit la configuration du démarrage du canal, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Headless Gateway et Model Setup.
- Santé/statut de la passerelle : Définit la configuration de la santé/statut de la passerelle, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Headless Gateway et Model Setup.
- Installation du service utilisateur : Définit la configuration de l'installation du service utilisateur, les identifiants, la configuration et le comportement de vérification de l'opérateur pour systemd Service et Boot Persistence.
- linger/boot persistence : Définit la configuration de linger/boot persistence, les identifiants, la configuration et le comportement de vérification de l'opérateur pour systemd Service et Boot Persistence.
- Service drop-ins : Définit la configuration des Service drop-ins, les identifiants, la configuration et le comportement de vérification de l'opérateur pour systemd Service et Boot Persistence.
- Restart tuning : Définit la configuration de Restart tuning, les identifiants, la configuration et le comportement de vérification de l'opérateur pour systemd Service et Boot Persistence.
- Status/log inspection : Définit la configuration de Status/log inspection, les identifiants, la configuration et le comportement de vérification de l'opérateur pour systemd Service et Boot Persistence.
- Backup/restore : Définit la configuration de Backup/restore, les identifiants, la configuration et le comportement de vérification de l'opérateur pour systemd Service et Boot Persistence.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : La documentation Gateway définit le processus always-on, la valeur par défaut loopback, l'exigence d'authentification, les modes de démarrage, l'accès à distance et les points de terminaison de santé. La documentation Raspberry Pi oriente explicitement les opérateurs vers les modèles cloud plutôt que les LLM locaux.
- Signaux négatifs : Les charges de travail des canaux sur petits appareils sont documentées par exemple mais ne sont pas prouvées par une porte de version matérielle. Les conseils OAuth/API-key sans tête existent mais peuvent toujours échouer dans les contextes systemd de longue durée.
- Lacunes d'intégration : Le runtime et le démarrage de la passerelle ont une couverture d'intégration large, mais aucune exécution de test inspectée n'exécute l'automatisation des canaux sur du matériel Raspberry Pi.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : Les rapports Raspberry Pi Telegram/systemd et plugin-loader montrent une utilisation réelle sans tête avec des défaillances de bord.
- Rapports Discrawl : les utilisateurs décrivent les tentatives Telegram, WhatsApp et modèle local/QMD basées sur Pi, y compris les problèmes d'authentification et de latence répétés.
- Bonnes qualités : La documentation rend le choix du modèle cloud clair et évite d'impliquer que les petits appareils Pi devraient exécuter des LLM locaux.
- Mauvaises qualités : Les rapports d'opérateurs réels mélangent toujours l'authentification sans tête, la configuration des canaux et les problèmes de performance des petits appareils, donc l'histoire du runtime n'est pas encore stable pour les utilisateurs non experts.
- Exclus de la qualité : preuves de test unitaire, intégration, e2e, live, runtime-flow et smoke test manuel.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/raspberry-pi-small-linux-devices.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le processus Always-on Gateway, la configuration du modèle cloud, le démarrage du canal, la santé/statut de la passerelle, l'installation du service utilisateur, linger/boot persistence, Service drop-ins, Restart tuning, Status/log inspection, Backup/restore.
- Signaux négatifs : la note archivée a précédé le scoring de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucune preuve de version étiquetée matérielle n'a été trouvée pour une passerelle Pi servant un connecteur de canal au fil du temps.
- La configuration spécifique au canal n'est pas présentée comme une matrice sûre pour Pi.
- Le comportement QMD/modèle local sur Pi est principalement représenté par des avertissements et des douleurs d'archive, pas une limite de support nette.

## Preuves

### Docs

- `docs/gateway/index.md:71-83` définit un processus Always-on Gateway, un port unique, la valeur par défaut loopback et les exigences d'authentification.
- `docs/gateway/index.md:135-147` énumère les capacités de commande de l'opérateur derrière Gateway.
- `docs/cli/gateway.md:25-48` documente le comportement de run/startup de Gateway, les garde-fous de configuration et les gardes d'authentification non-loopback.
- `docs/install/raspberry-pi.md:174-191` recommande les modèles API hébergés dans le cloud et dit de ne pas exécuter les LLM locaux sur un Pi.
- `README.md:116-128` décrit le mode daemon par rapport au mode foreground/debug.

### Source

- `src/cli/gateway-cli/run.ts:367-395` sonde la santé de Gateway lors du démarrage.
- `src/cli/gateway-cli/run-loop.ts:220-253` supporte le repli de redémarrage en processus et `OPENCLAW_NO_RESPAWN`.
- `src/shared/gateway-bind-url.ts:21-46` résout les URL de liaison personnalisées, tailnet et LAN.
- `src/commands/status.gateway-probe.ts:8-21` résout l'authentification de la sonde Gateway.

### Tests d'intégration

- `package.json:1731` définit la suite de tests Gateway.
- `package.json:1776` et `package.json:1777` définissent les benchmarks de démarrage et redémarrage de Gateway.
- Aucun chemin d'intégration inspecté ne nomme le matériel Raspberry Pi.

### Tests unitaires

- La logique de liaison/authentification/démarrage de Gateway a des tests ciblés dans les suites de tests Gateway et CLI, mais pas de fixtures Pi.
- `scripts/check-cli-startup-memory.mjs:96-120` inclut les cas de démarrage-mémoire du statut Gateway.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --json --query "Raspberry Pi WhatsApp Telegram gateway"`

Résultats :

- Aucun thread ciblé retourné pour la requête combinée WhatsApp/Telegram.

Requête : `gitcrawl search openclaw/openclaw --json --query "Raspberry Pi low memory OpenClaw"`

Résultats :

- Problèmes de performance du plugin-loader et Raspberry Pi OS arm64 retournés qui affectent l'utilisation de Gateway sans tête.

### Requêtes Discrawl

Requête : `/Users/kevinlin/.local/bin/discrawl search --limit 5 "Raspberry Pi Codex auth systemd"`

Résultats :

- Trouvé un commentaire Pi/Linux systemd décrivant les agents Telegram et les défaillances OAuth Codex répétées.

Requête : `/Users/kevinlin/.local/bin/discrawl search --limit 5 "Pi 5 aarch64 OpenClaw gateway"`

Résultats :

- Trouvé les rapports de latence Pi 5 aarch64, crash npm install, timeout QMD/native et timeout de poignée de main CLI.
