---
title: "Linux Gateway host - Systemd User Service Lifecycle Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Linux Gateway host - Systemd User Service Lifecycle Maturity Note

## Résumé

Le chemin du service utilisateur systemd est le chemin d'hôte Linux Gateway le mieux documenté. La documentation couvre `openclaw gateway install`, `systemctl --user enable --now`, `loginctl enable-linger`, les unités manuelles, les alternatives de service au niveau du système, et la réparation via doctor. Le code source soutient la génération d'unités, l'analyse des fichiers env, l'actualisation de l'installation et la réparation de service. La qualité est bêta car les preuves d'archive récentes montrent la détection au niveau du système, EnvironmentFile, WSL/user-bus, et les bords de provenance.

## Portée de la catégorie

Cette catégorie évalue la zone de capacité Linux Gateway host représentée par ces fonctionnalités de taxonomie :

- Systemd User Service Lifecycle : Portée des preuves pour Systemd User Service Lifecycle.

## Fonctionnalités

- Configuration de Systemd User Service Lifecycle : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour Systemd User Service Lifecycle.
- Opération de Systemd User Service Lifecycle : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour Systemd User Service Lifecycle.
- Statut de Systemd User Service Lifecycle : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour Systemd User Service Lifecycle.
- Récupération de Systemd User Service Lifecycle : Définit le comportement de configuration, d'authentification, de configuration et de vérification de l'opérateur pour Systemd User Service Lifecycle.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Justification : la documentation et le code source couvrent le chemin heureux du service utilisateur, linger, les unités manuelles, l'alternative de service système, la réparation de service, la gestion des fichiers env, et la sémantique de redémarrage.
- Lacunes : la documentation du service est divisée entre les pages Gateway, Linux platform, VPS et doctor, et les avertissements WSL/user-bus sont plus visibles dans les preuves de problèmes que dans le chemin de l'opérateur principal.

## Score de qualité

- Score : `Beta (78%)`
- Justification : le chemin de service recommandé est mature, mais les preuves d'archive actives montrent des cas limites importants autour des services au niveau du système, l'utilisation d'EnvironmentFile, la disponibilité du user-bus, et la provenance de systemd.
- Exclus de la qualité : preuves de test unitaire, intégration, e2e, live et runtime-flow.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/linux-gateway-host.md`.
- Signaux positifs : les preuves archivées de documentation, code source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration de Systemd User Service Lifecycle, l'opération de Systemd User Service Lifecycle, le statut de Systemd User Service Lifecycle, la récupération de Systemd User Service Lifecycle.
- Signaux négatifs : la note archivée a précédé le score de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Rendre la détection de service au niveau du système et le comportement du statut du service utilisateur visibles dans la documentation et la sortie de statut.
- Ajouter des conseils d'opérateur pour les défaillances WSL/user-bus et quand choisir le service utilisateur, le service système, tmux ou la supervision du processus conteneur.

## Preuves

### Documentation

- `docs/gateway/index.md:231-266` documente l'onglet du service utilisateur systemd Linux, `openclaw gateway install`, `systemctl --user enable --now`, `loginctl enable-linger`, et la création d'unité manuelle.
- `docs/gateway/index.md:284-298` documente le chemin du service au niveau du système et note le refus de doctor quand un service au niveau du système possède déjà l'hôte.
- `docs/platforms/linux.md:36-70` documente les commandes d'installation du service et le comportement par défaut du service utilisateur systemd.
- `docs/platforms/linux.md:72-99` fournit une unité systemd manuelle.
- `docs/vps.md:97-132` documente l'ajustement systemd VPS, les limites de redémarrage, le cache de compilation, `OPENCLAW_NO_RESPAWN`, et les contrôles de mémoire.

### Code source

- `src/daemon/systemd-unit.ts:49-94` construit l'unité avec l'ordre network-online, la politique de redémarrage, `RestartPreventExitStatus=78`, `KillMode=control-group`, et l'ordre EnvironmentFile.
- `src/daemon/systemd.ts:60-79` résout le chemin de l'unité utilisateur et le nom du service.
- `src/daemon/systemd.ts:85-146` lit l'état ExecStart, WorkingDirectory, Environment et EnvironmentFile à partir des unités systemd.
- `src/daemon/service.ts:134-165` collecte les problèmes de réparation pour la dérive de service de version, temporaire et de programme manquant.
- `src/cli/daemon-cli/install.ts:241-275` construit et installe le plan de service.

### Tests d'intégration

- `src/cli/daemon-cli/install.integration.test.ts` couvre les chemins d'intégration d'installation de service.
- `src/commands/doctor-gateway-services.test.ts` couvre les réécritures de service, les sauts de service actif, la persistance des jetons et la gestion systemd héritée.
- `src/commands/gateway-readiness.test.ts` couvre les attentes de disponibilité de Gateway pour les flux de service gérés.

### Tests unitaires

- `src/daemon/systemd-unit.test.ts:42-53` couvre l'ordre EnvironmentFile avant Environment en ligne.
- `src/daemon/systemd.test.ts` couvre l'analyse d'EnvironmentFile, la nouvelle tentative d'installation, les défaillances du user-bus et le contrôle du service.
- `src/cli/daemon-cli/lifecycle.test.ts`, `src/cli/daemon-cli/lifecycle-core.test.ts` et `src/cli/daemon-cli/install.test.ts` couvrent les branches du cycle de vie du daemon.

### Requêtes Gitcrawl

- La requête spécifique `systemd user service loginctl enable-linger daemon install Linux gateway` a retourné la PR #68400 sur la distinction entre l'absence de socket D-Bus utilisateur WSL et `systemctl` manquant.
- La requête plus large `systemd` a retourné le problème #87577 pour le statut/redémarrage ne détectant pas les services au niveau du système, le problème #80595 pour le répertoire d'état `.env` comme EnvironmentFile systemd Linux, la PR #80140 pour la pulsation du watchdog, la PR #85151 pour la détection d'unité au niveau du système, la PR #66735 pour la remise de redémarrage automatique, la PR #57276 pour les unités à portée système, la PR #68909 pour la déduplication consciente de cgroup, et la PR #81019 pour la provenance de l'unité.

### Requêtes Discrawl

- La requête `systemd user service loginctl enable-linger daemon install Linux gateway` a trouvé des threads d'assistance utilisant `openclaw onboard --install-daemon`, `openclaw gateway install`, `systemctl --user enable --now openclaw-gateway.service`, et `sudo loginctl enable-linger <user>`.
- La même requête a trouvé des conseils de secours pour tmux ou les services système où `systemctl --user` n'est pas disponible.
