---
title: "Hôte macOS Gateway - Note de maturité pour la mise à jour, la désinstallation et la récupération"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Hôte macOS Gateway - Note de maturité pour la mise à jour, la désinstallation et la récupération

## Résumé

La mise à jour, la désinstallation et la récupération sont documentées et implémentées avec une gestion spécifique de macOS LaunchAgent. La documentation de mise à jour CLI met en évidence le transfert du gestionnaire de paquets et le réamorçage de LaunchAgent, la documentation de désinstallation sépare le nettoyage du service/des données/CLI, et la documentation de dépannage couvre les services abandonnés, les tâches de mise à jour obsolètes et la réparation manuelle de launchd.

La couverture est Stable car la documentation/source/preuve unitaire couvre la mise à jour, la désinstallation, la réparation du docteur, les tâches obsolètes et l'actualisation du service. La qualité est Beta car la mise à jour auto-invoquée par l'agent et les tâches de mise à jour launchd obsolètes apparaissent toujours dans les rapports des opérateurs en direct.

## Portée de la catégorie

- Transfert de paquet/git `openclaw update` sur macOS.
- Actualisation du service géré et réamorçage de LaunchAgent après les mises à jour.
- Détection et nettoyage des tâches launchd de mise à jour obsolètes.
- `openclaw uninstall`, désinstallation du service, nettoyage d'état et suppression manuelle de launchd.
- Récupération après les services macOS Gateway partiellement mis à jour ou abandonnés.

## Fonctionnalités

- Transfert de paquet/git openclaw update : Transfert de paquet/git openclaw update sur macOS
- Actualisation du service géré : Actualisation du service géré et réamorçage de LaunchAgent après les mises à jour
- Détection des tâches launchd de mise à jour obsolètes : Détection et nettoyage des tâches launchd de mise à jour obsolètes
- openclaw uninstall : openclaw uninstall, désinstallation du service, nettoyage d'état et suppression manuelle de launchd
- Récupération du service abandonné : Récupération après les services macOS Gateway partiellement mis à jour ou abandonnés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : documentation de mise à jour/désinstallation, source du cycle de vie launchd, source de mise à jour obsolète, tests du docteur et tous les tests de fumée de mise à jour Parallels couvrent les chemins de récupération importants.
- Signaux négatifs : la véritable mise à jour auto-invoquée par l'agent tandis que la Gateway supervise la session est difficile à prouver et présente des défaillances d'archive actives.
- Lacunes d'intégration : aucune voie en direct inspectée ne met à jour à plusieurs reprises depuis une session d'agent macOS active et ne vérifie que LaunchAgent reste supervisé sans réparation SSH externe.

## Score de qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : `self-update macOS LaunchAgent not loaded gateway` a retourné le problème ouvert #85133 pour LaunchAgent déchargé lors de la mise à jour automatique et le problème ouvert #75250 pour la dérive du cache Node/runtime/plugin Homebrew mixte. La requête de transfert de mise à jour fermée n'a retourné aucun résultat supplémentaire.
- Rapports Discrawl : `gateway update LaunchAgent not loaded` a retourné un rapport du 2026-05-14 d'échec de mise à jour automatique sur trois instances macOS LaunchAgent, plus des commentaires de miroir GitHub fermant les problèmes de mise à jour/LaunchAgent plus anciens comme implémentés.
- Bonnes qualités : la documentation avertit explicitement sur le transfert de service, la source détecte les tâches de mise à jour obsolètes, le code du cycle de vie peut réparer les services launchd installés mais non chargés, et la documentation de désinstallation donne les étapes de nettoyage manuel de launchd.
- Mauvaises qualités : la mise à jour est auto-référentielle sur un hôte Gateway : le processus peut mettre à jour le runtime qui supervise la session, et les wrappers de mise à jour launchd obsolètes peuvent continuer à tuer la Gateway jusqu'à suppression manuelle.
- Exclu de la qualité : Les preuves couvrant uniquement la couverture ont été considérées uniquement dans le score de couverture, pas dans ce score de qualité.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-gateway-host.md`.
- Signaux positifs : la documentation archivée, la source, le test, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour le transfert de paquet/git openclaw update, l'actualisation du service géré, la détection des tâches launchd de mise à jour obsolètes, openclaw uninstall, la récupération du service abandonné.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une voie de résilience de mise à jour en direct qui commence à partir d'une session macOS LaunchAgent active et prouve la supervision du service après la mise à jour.
- Mettre en évidence les tâches launchd de mise à jour obsolètes de manière plus visible dans la documentation de récupération macOS.
- Rendre explicite la récupération de désinstallation/réinstallation à partir des installations d'applications avec préfixe local à côté de la récupération d'installation npm/source globale.

## Preuves

### Documentation

- `docs/cli/update.md:34` : documente les drapeaux de mise à jour et les diagnostics.
- `docs/cli/update.md:101` : documente le transfert du gestionnaire de paquets et le réamorçage de macOS LaunchAgent après la mise à jour.
- `docs/install/updating.md:11` : documente la commande de mise à jour.
- `docs/install/updating.md:48` : documente le changement des racines d'installation npm/git et les métadonnées/redémarrage du service.
- `docs/install/updating.md:213` : documente le transfert du service géré et la récupération de macOS LaunchAgent.
- `docs/install/uninstall.md:14` : documente `openclaw uninstall` et les drapeaux non interactifs.
- `docs/install/uninstall.md:31` : documente l'arrêt/la désinstallation du service et la gestion d'état.
- `docs/install/uninstall.md:80` : documente la suppression manuelle de launchd macOS.
- `docs/gateway/troubleshooting.md:30` : documente les commandes de réparation après mise à jour.
- `docs/gateway/troubleshooting.md:420` : documente le service installé mais non exécuté, les conflits de port, l'état profond et l'inadéquation du port de service.

### Source

- `src/daemon/launchd.ts:291` : analyse et trouve les tâches de mise à jour obsolètes.
- `src/daemon/launchd.ts:330` : supprime/désactive les tâches de mise à jour obsolètes.
- `src/daemon/launchd.ts:596` : répare les LaunchAgents installés mais non chargés.
- `src/cli/daemon-cli/lifecycle.ts:221` : démarre/désinstalle avec le comportement de récupération macOS.
- `src/cli/daemon-cli/lifecycle.ts:275` : redémarre avec récupération, nettoyage des PID obsolètes et vérifications de santé.
- `src/cli/daemon-cli/install.ts:155` : détecte les services existants chargés et actualise si nécessaire.
- `src/commands/doctor-platform-notes.launchctl-env-overrides.test.ts:124` : teste le comportement d'avertissement/nettoyage des tâches de mise à jour obsolètes.

### Tests d'intégration

- `scripts/e2e/parallels/macos-smoke.ts:873` : exécute une mise à jour de développement via le flux git/paquet sur un invité macOS.
- `scripts/e2e/parallels/macos-smoke.ts:923` : vérifie l'état profond de Gateway après installation/mise à jour.
- `src/daemon/launchd.integration.e2e.test.ts:246` : prouve la réparation d'un état d'amorçage installé mais manquant.

### Tests unitaires

- `src/commands/doctor-platform-notes.launchctl-env-overrides.test.ts:124` : couvre l'avertissement et le nettoyage des mises à jour obsolètes.
- `src/daemon/launchd.test.ts:1208` : couvre les chemins de secours de redémarrage et le réamorçage après déchargement de kickstart.
- `src/cli/daemon-cli/lifecycle.test.ts:276` : couvre le réamorçage d'un LaunchAgent installé lorsqu'il n'est pas chargé.
- `src/cli/daemon-cli/lifecycle.test.ts:555` : couvre le réamorçage de redémarrage lorsqu'aucun écouteur non géré n'existe.
- `src/daemon/diagnostics.test.ts:23` : couvre la suppression de stderr launchd et la gestion de stderr obsolète.

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search issues "macOS LaunchAgent update handoff not loaded stale updater launchd job" -R openclaw/openclaw --state open --json number,title,url,state --limit 5
```

Résultats :

- Retourné `[]`.

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
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "gateway update LaunchAgent not loaded"
```

Résultats :

- Retourné un rapport du responsable du 2026-05-14 d'échec de mise à jour automatique sur trois instances macOS LaunchAgent, incluant les services déchargés qui ont nécessité une réparation SSH externe.
- Retourné des commentaires de miroir GitHub fermant les problèmes de point d'entrée launchd obsolète et de redémarrage non chargé plus anciens comme implémentés sur le main actuel.
