---
title: "macOS Gateway host - Gateway Service Lifecycle Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# macOS Gateway host - Gateway Service Lifecycle Maturity Note

## Résumé

Le cycle de vie LaunchAgent est une implémentation de service macOS réelle orientée vers l'opérateur.
L'interface CLI relie install/start/stop/restart/status via l'adaptateur de service Darwin, le shell d'application appelle l'interface CLI en mode local, et l'adaptateur launchd gère les labels, les profils, KeepAlive, RunAtLoad, les fichiers env sécurisés, la dérive de token, la réparation du bootstrap, le nettoyage des PID obsolètes et l'inspection à l'exécution.

La couverture est Stable car il existe une suite d'intégration launchd Darwin en direct plus une couverture CLI/status/unit plus large. La qualité est Beta car les preuves d'archive montrent toujours des défaillances launchd ouvertes autour de la ré-amorçage d'auto-mise à jour, l'exécution du wrapper env sur les volumes home externes et la sortie d'audit de statut trompeuse.

## Portée de la catégorie

Inclus dans cette catégorie :

- Installation de LaunchAgent Gateway par utilisateur : Installation, mise en scène, désinstallation, démarrage, arrêt, redémarrage et statut de LaunchAgent Gateway par utilisateur
- launchctl bootstrap : launchctl bootstrap, bootout, enable, disable, kickstart, analyse d'exécution, réparation installée mais non chargée et sémantique --disable
- Labels LaunchAgent : Labels LaunchAgent, labels de profil, nettoyage hérité, métadonnées de service, génération de plist, KeepAlive, RunAtLoad, logs, répertoire de travail et gestion du répertoire temporaire
- Gestion des tokens/env Gateway : Gestion des tokens/env Gateway, fichiers/wrappers env réservés au propriétaire, clés env de service gérées et sortie d'audit/statut de configuration
- Remise de LaunchAgent gérée par l'application : Intégration d'application macOS qui gère le LaunchAgent Gateway en mode local et l'évite en modes distant ou attach-only.
- Remise du package de mise à jour openclaw/git : Remise du package de mise à jour openclaw/git sur macOS
- Actualisation du service géré : Actualisation du service géré et ré-amorçage LaunchAgent après les mises à jour
- Détection des tâches launchd de mise à jour obsolètes : Détection et nettoyage des tâches launchd de mise à jour obsolètes
- Désinstallation openclaw : Désinstallation openclaw, désinstallation de service, nettoyage d'état et suppression manuelle de launchd
- Récupération du service bloqué : Récupération après des services Gateway macOS partiellement mis à jour ou bloqués.

## Fonctionnalités

- Installation de LaunchAgent Gateway par utilisateur : Installation, mise en scène, désinstallation, démarrage, arrêt, redémarrage et statut de LaunchAgent Gateway par utilisateur
- launchctl bootstrap : launchctl bootstrap, bootout, enable, disable, kickstart, analyse d'exécution, réparation installée mais non chargée et sémantique --disable
- Labels LaunchAgent : Labels LaunchAgent, labels de profil, nettoyage hérité, métadonnées de service, génération de plist, KeepAlive, RunAtLoad, logs, répertoire de travail et gestion du répertoire temporaire
- Gestion des tokens/env Gateway : Gestion des tokens/env Gateway, fichiers/wrappers env réservés au propriétaire, clés env de service gérées et sortie d'audit/statut de configuration
- Remise de LaunchAgent gérée par l'application : Intégration d'application macOS qui gère le LaunchAgent Gateway en mode local et l'évite en modes distant ou attach-only.
- Remise du package de mise à jour openclaw/git : Remise du package de mise à jour openclaw/git sur macOS
- Actualisation du service géré : Actualisation du service géré et ré-amorçage LaunchAgent après les mises à jour
- Détection des tâches launchd de mise à jour obsolètes : Détection et nettoyage des tâches launchd de mise à jour obsolètes
- Désinstallation openclaw : Désinstallation openclaw, désinstallation de service, nettoyage d'état et suppression manuelle de launchd
- Récupération du service bloqué : Récupération après des services Gateway macOS partiellement mis à jour ou bloqués.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (86%)`
- Signaux positifs : la couverture launchd Darwin en direct couvre l'installation, le redémarrage avec remplacement de PID, la récupération KeepAlive SIGTERM brute, stop/start, stop/restart et la réparation du bootstrap manquant.
- Signaux négatifs : les appels de preuve en direct les plus forts appellent directement les fonctions de l'adaptateur launchd plutôt que d'exercer les commandes `openclaw gateway install/status --deep/restart` packagées de bout en bout à partir du binaire CLI.
- Lacunes d'intégration : aucune preuve en direct visible ne couvre l'exécution du wrapper env sur home externe, l'analyse du statut du service enveloppé par shell ou un basculement d'application qui installe, vérifie le statut, redémarre et désactive le LaunchAgent via l'interface utilisateur.

## Score de qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : les recherches axées sur launchd ont trouvé le problème ouvert #85133 pour la mise à jour automatique laissant `ai.openclaw.gateway` non enregistré, le problème ouvert #87199 pour l'échec du wrapper env/permission sur les volumes home externes, le problème ouvert #81751 pour le faux audit de statut "sous-commande gateway manquante" sur les LaunchAgents enveloppés par shell et la PR ouverte #75545 pour rendre `gateway start` idempotent quand déjà en cours d'exécution.
- Rapports Discrawl : les recherches d'archive launchd ont retourné les défaillances historiques de restart/bootout maintenant marquées comme implémentées, les rapports d'opérateurs de LaunchAgent bootout à partir de contextes SSH/headless et la sortie de statut répétée montrant la dérive du service token/PATH/version-manager.
- Bonnes qualités : l'adaptateur launchd a des permissions plist/env-file sécurisées, des fichiers wrapper env réservés au propriétaire, des conseils de bootstrap du domaine GUI, des labels conscients du profil, un nettoyage hérité, un bootout stop par défaut préservant le KeepAlive futur, un `--disable` persistant, des assertions de libération de port, un support de remise de redémarrage et des surfaces de statut/audit approfondies.
- Mauvaises qualités : les rapports actifs montrent que le service peut toujours être perdu après une mise à jour, échouer sur l'exécution du wrapper env dans certaines configurations de volume home ou produire des diagnostics trompeurs.
- Exclu de la qualité : Les preuves de couverture uniquement ont été considérées uniquement dans le score de couverture, pas dans ce score de qualité.

## Score d'exhaustivité

- Score : `Stable (86%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-gateway-host.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'installation de LaunchAgent Gateway par utilisateur, launchctl bootstrap, les labels LaunchAgent, la gestion des tokens/env Gateway, la remise de LaunchAgent gérée par l'application, la remise du package de mise à jour openclaw/git, l'actualisation du service géré, la détection des tâches launchd de mise à jour obsolètes, la désinstallation openclaw, la récupération du service bloqué.
- Signaux négatifs : la note archivée a précédé la notation d'exhaustivité du processus-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La remise de LaunchAgent d'auto-mise à jour n'est pas entièrement prouvée robuste par les preuves d'archive : #85133 signale un plist valide réécrit alors que launchd ne supervise plus la tâche.
- L'exécution du wrapper env a toujours un risque de cas limite sur les volumes home externes.
- L'intégration d'application est soutenue par la source et couverte par les unités mais manque d'un chemin de preuve app-to-launchd visible en direct dans les preuves inspectées.

## Preuves

### Docs

- `docs/platforms/macos.md:24`: le mode local s'attache à une Gateway locale en cours d'exécution ou active launchd avec `openclaw gateway install`; le mode distant se connecte via SSH/Tailscale et ne démarre jamais une Gateway locale.
- `docs/platforms/macos.md:35`: documente les étiquettes LaunchAgent par utilisateur, les étiquettes de profil, le nettoyage des étiquettes héritées, `launchctl kickstart -k`, et `launchctl bootout`.
- `docs/platforms/mac/bundled-gateway.md:27`: documente l'étiquette, le chemin plist, les gestionnaires app/CLI, la sémantique du bouton Active, le comportement de fermeture de l'app, et les chemins stdout/stderr.
- `docs/cli/gateway.md:267`: documente `gateway status`, la sortie JSON, `--require-rpc`, `--no-probe`, et `--deep`.
- `docs/cli/gateway.md:449`: documente le cycle de vie du service, le wrapper, les SecretRefs d'authentification, et le comportement d'arrêt sur macOS.
- `docs/gateway/index.md:209`: documente l'installation/statut/redémarrage/arrêt launchd sur macOS, bootout/disable, les étiquettes, et les audits doctor.

### Source

- `src/daemon/service.ts:73`: définit l'abstraction du service Gateway.
- `src/daemon/service.ts:261`: lie Darwin à l'installation/désinstallation/arrêt/redémarrage/isLoaded/readCommand/readRuntime de LaunchAgent.
- `src/daemon/launchd.ts:111`: calcule les étiquettes LaunchAgent et les chemins plist.
- `src/daemon/launchd.ts:189`: écrit les fichiers env et les scripts wrapper env en lecture seule pour le propriétaire.
- `src/daemon/launchd.ts:441`: active avant le bootstrap et gère les domaines GUI non supportés avec des conseils exploitables.
- `src/daemon/launchd.ts:533`: lit l'état de charge/runtime launchd via `launchctl print`.
- `src/daemon/launchd.ts:596`: répare les LaunchAgents installés mais non chargés.
- `src/daemon/launchd.ts:779`: par défaut l'arrêt à bootout et préserve la récupération KeepAlive future sauf si `--disable` est demandé.
- `src/daemon/launchd.ts:1016`: redémarre via la remise détachée en service, le nettoyage des ports obsolètes, la réécriture/rechargement plist, kickstart, le fallback bootstrap, et la réparation chargée-après-échec.
- `apps/macos/Sources/OpenClaw/GatewayLaunchAgentManager.swift:57`: l'app ignore les modifications launchd en mode distant, respecte le marqueur attach-only, installe avec `openclaw gateway install --force --port ... --runtime node`, désinstalle quand désactivé, et redémarre via la CLI.

### Tests d'intégration

- `src/daemon/launchd.integration.e2e.test.ts:177`: la suite launchd Darwin en direct crée une étiquette LaunchAgent isolée et un home temporaire, puis exerce le comportement réel de launchctl.
- `src/daemon/launchd.integration.e2e.test.ts:205`: redémarre le service launchd et vérifie que le runtime continue de s'exécuter avec un nouveau PID.
- `src/daemon/launchd.integration.e2e.test.ts:213`: tue le processus avec SIGTERM brut et vérifie que la supervision LaunchAgent remplace le PID.
- `src/daemon/launchd.integration.e2e.test.ts:222`: arrête, vérifie non-exécution, démarre via `startGatewayService`, et vérifie un nouveau PID.
- `src/daemon/launchd.integration.e2e.test.ts:246`: bootout un plist installé valide et vérifie que la réparation réenregistre et redémarre sans kickstart supplémentaire.
- `src/daemon/cli/install.integration.test.ts:136`: l'installation génère automatiquement un token et évite d'intégrer `OPENCLAW_GATEWAY_TOKEN` dans l'env du service.

### Tests unitaires

- `src/daemon/launchd.test.ts:597`: la réparation bootstrap couvre l'ordre enable/bootstrap, la gestion déjà-chargée, et le comportement kickstart.
- `src/daemon/launchd.test.ts:685`: les tests d'installation couvrent enable-before-bootstrap, les fichiers env en lecture seule pour le propriétaire, la réparation env-wrapper, la création TMPDIR, la politique KeepAlive, la réécriture plist, et le renforcement des permissions.
- `src/daemon/launchd.test.ts:897`: les tests d'arrêt couvrent le bootout par défaut, les postconditions de libération de port, `--disable`, le fallback dégradé, et la propagation d'échec.
- `src/daemon/launchd.test.ts:1208`: les tests de redémarrage couvrent kickstart, le rechargement après réécriture plist, le nettoyage obsolète, l'échec de port occupé, le fallback bootstrap, les conseils de domaine GUI, et les étiquettes invalides.
- `src/cli/daemon-cli/lifecycle.test.ts:276`: le démarrage CLI ré-amorce un LaunchAgent installé quand non chargé.
- `apps/macos/Tests/OpenClawIPCTests/GatewayLaunchAgentManagerTests.swift:5`: le remplacement attach-only écrit le marqueur et ne désinstalle pas le LaunchAgent Gateway.
- `apps/macos/Tests/OpenClawIPCTests/GatewayLaunchAgentManagerTests.swift:29`: l'analyse plist LaunchAgent côté app extrait le port, bind, token, et password.

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search issues "macOS LaunchAgent gateway install restart status ai.openclaw.gateway" -R openclaw/openclaw --state open --json number,title,url,state --limit 5
```

Résultats :

- Ouvert #87199 : `[Bug]: macOS LaunchAgent generated by 2026.5.22 uses env-wrapper and missing gateway run, causing EX_CONFIG / Permission denied on external home volumes`.

Requête :

```bash
gitcrawl search issues "self-update macOS LaunchAgent not loaded gateway" -R openclaw/openclaw --state open --json number,title,url,state --limit 5
```

Résultats :

- Ouvert #85133 : `Gateway launchd agent gets unloaded during self-update and never re-bootstrapped (macOS)`.
- Ouvert #75250 : `Bug: OpenClaw breaks after Homebrew updates due to mixed Homebrew Node/runtime/plugin cache drift`.

### Requêtes Discrawl

Requête :

```bash
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "gateway service launchd"
```

Résultats :

- Rapports de mainteneurs du 2026-05-14 sur les échecs de self-update sur trois instances LaunchAgent macOS, incluant un package actuel avec Gateway hors ligne et un LaunchAgent non chargé.
- Notes de version du 2026-05-06 pour les correctifs rendant `gateway stop` utilisant bootout par défaut et évitant les kickstart inutiles.
- Analyse de tâche updater obsolète où une tâche de mise à jour launchd sœur continuait à terminer la Gateway.
