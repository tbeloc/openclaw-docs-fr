---
title: "Windows via WSL2 - Update, Package-manager, and Source-dev Workflow Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Windows via WSL2 - Update, Package-manager, and Source-dev Workflow Maturity Note

## Résumé

Le flux de travail de mise à jour et de développement est adéquat pour WSL2 car il réutilise le chemin Linux/systemd, et la documentation montre explicitement la configuration source à l'intérieur de WSL. `openclaw update` a un comportement considérable conscient des services, incluant la détection de la racine des paquets, le changement de mode d'installation, l'actualisation des métadonnées de service et la transmission de mise à jour systemd. La faiblesse est l'acceptation spécifique à WSL2 : les preuves actuelles montrent des frictions de support autour des installations pnpm/npm, des ressources source, des points d'entrée de service obsolètes et des Gateways qui s'exécutent mais sont inaccessibles après les mises à jour.

## Portée de la catégorie

- Flux d'installation/construction source à l'intérieur de WSL2.
- `openclaw update`, changement de canal, diagnostics de simulation/statut.
- Changement de mode d'installation et racine de paquet npm/pnpm/git.
- Redémarrage Gateway systemd géré et transmission de mise à jour.
- Actualisation des métadonnées de service après les mises à jour.
- Avertissements du gestionnaire de paquets tels que vus par les utilisateurs de WSL2.

## Fonctionnalités

- Installation et construction source à l'intérieur de WSL2 : Flux de travail d'installation et de construction source à l'intérieur de la distribution WSL2.
- openclaw update : openclaw update, changement de canal, diagnostics de simulation/statut
- npm/pnpm/git package-root : npm/pnpm/git package-root et changement de mode d'installation
- Redémarrage Gateway systemd géré : Redémarrage Gateway systemd géré et transmission de mise à jour
- Actualisation des métadonnées de service : Actualisation des métadonnées de service après les mises à jour de Gateway WSL2.
- Avertissements du gestionnaire de paquets : Avertissements du gestionnaire de paquets vus à partir des installations source et paquet WSL2.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : La documentation Windows inclut les commandes de construction/intégration source WSL2 ; la documentation de mise à jour couvre `openclaw update`, les canaux, la gestion de la racine des paquets, l'actualisation des métadonnées de service et la vérification du service ; les tests couvrent la transmission de mise à jour systemd et le comportement de mise à jour conscient des services.
- Signaux négatifs : la plupart des preuves sont générales Linux/systemd plutôt que spécifiques à WSL2, et la documentation du flux source repose toujours sur les utilisateurs exécutant le bon shell et le gestionnaire de paquets à l'intérieur de WSL.
- Lacunes d'intégration : aucune fiche de pointage de mise à jour WSL2 actuelle n'a été trouvée qui commence à partir d'un service installé, applique la mise à jour, actualise les métadonnées systemd, redémarre, vérifie le tableau de bord/l'interface utilisateur de contrôle et exécute doctor.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : `WSL2 update npm pnpm openclaw gateway` a retourné 0 résultats. `WSL2 install Node openclaw onboard` a retourné le problème #63740 pour l'échec de syntaxe source/runtime WSL2 et le problème #86612 pour les interactions de chemin Docker/WSL2. Les requêtes WSL2/systemd plus larges ont retourné des problèmes d'unité obsolète et de boucle de redémarrage.
- Rapports Discrawl : La requête de mise à jour WSL2 a retourné des extraits de statut à partir d'installations WSL2 avec état de mise à jour pnpm/npm, gateway inaccessible après mise à jour, journaux de redémarrage de service et conseils pour utiliser `openclaw update` plutôt que npm/pnpm brut.
- Bonnes qualités : la documentation de mise à jour et la source gèrent les racines de service gérées avec soin, et la logique de transmission systemd est explicite plutôt que d'assumer les mises à jour CLI au premier plan.
- Mauvaises qualités : les utilisateurs de WSL2 rencontrent toujours une dérive du gestionnaire de paquets et du point d'entrée de service, en particulier à travers les installations source/paquet et les limites du système de fichiers WSL.
- Exclu de la qualité : les preuves de test unitaire, intégration, e2e, live et flux d'exécution sont exclues de ce score de qualité.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/windows-via-wsl2.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'installation et la construction source à l'intérieur de WSL2, openclaw update, npm/pnpm/git package-root, redémarrage Gateway systemd géré, actualisation des métadonnées de service, avertissements du gestionnaire de paquets.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Besoin de couverture de fumée de mise à jour spécifique à WSL2 avec npm, pnpm et installations source.
- Besoin de documentation qui appelle l'emplacement du système de fichiers WSL et les attentes du gestionnaire de paquets dans la page Windows.
- Besoin d'une orientation de statut/doctor plus claire lorsque l'état de mise à jour WSL2 est sain mais que la boucle de retour Gateway est inaccessible.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:221` : La section d'installation WSL2 suit le démarrage Linux à l'intérieur de WSL.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:226` : le flux source clone le repo, exécute `pnpm install`, `pnpm build`, `pnpm ui:build` et `pnpm openclaw onboard --install-daemon`.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:234` : la boucle de développement source pointe vers `pnpm openclaw setup` et `pnpm gateway:watch`.
- `/Users/kevinlin/code/openclaw/docs/install/updating.md:11` : `openclaw update` détecte le type d'installation, récupère la dernière version, exécute doctor et redémarre la Gateway.
- `/Users/kevinlin/code/openclaw/docs/install/updating.md:48` : la documentation de mise à jour décrit le changement entre les installations npm et git.
- `/Users/kevinlin/code/openclaw/docs/install/updating.md:69` : le canal dev assure un checkout git, le construit et installe l'interface de ligne de commande globale.
- `/Users/kevinlin/code/openclaw/docs/install/updating.md:71` : les mises à jour actualisent les métadonnées de service et redémarrent la Gateway sauf si `--no-restart` est passé.
- `/Users/kevinlin/code/openclaw/docs/install/updating.md:111` : les mises à jour du gestionnaire de paquets manuel sur les installations supervisées doivent arrêter la Gateway avant de remplacer les fichiers de paquet.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/update-managed-service-handoff.ts` : la transmission de mise à jour de service géré gère le mode superviseur systemd.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/update.ts` : la méthode de mise à jour Gateway coordonne le comportement de mise à jour de service géré.
- `/Users/kevinlin/code/openclaw/src/infra/update-package-manager.ts` : la détection du gestionnaire de paquets et le comportement de mise à jour sont centralisés.
- `/Users/kevinlin/code/openclaw/src/infra/update-startup.ts` : la gestion du démarrage de mise à jour suit l'état de redémarrage/mise à jour.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/doctor-install-switch/scenario.sh:160` : e2e vérifie le changement de point d'entrée de service npm-to-git via doctor.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/doctor-install-switch/scenario.sh:167` : e2e vérifie le changement de point d'entrée de service git-to-npm via doctor.
- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels-npm-update-smoke.sh` : la fumée de mise à jour npm existe, bien que non spécifique à WSL2.
- `/Users/kevinlin/code/openclaw/scripts/e2e/update-channel-switch-docker.sh` : la fumée de changement de canal de mise à jour e2e existe, bien que Docker/Linux plutôt que WSL2.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/cli/update-cli.test.ts:2740` : les tests de mise à jour arrêtent un service systemd lors de la mise à jour du paquet sans fuir la sortie d'arrêt brute dans JSON.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/update-managed-service-handoff.test.ts:190` : les tests de transmission de mise à jour lancent les transmissions systemd via la portée utilisateur transitoire.
- `/Users/kevinlin/code/openclaw/src/infra/update-package-manager.test.ts` : le comportement de mise à jour du gestionnaire de paquets a une couverture unitaire.
- `/Users/kevinlin/code/openclaw/src/infra/update-runner.test.ts` : le comportement du coureur de mise à jour a une couverture unitaire.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "WSL2 update npm pnpm openclaw gateway" --mode keyword --limit 8 --json`
- `gitcrawl search openclaw/openclaw --query "WSL2 install Node openclaw onboard" --mode keyword --limit 8 --json`
- `gitcrawl search openclaw/openclaw --query "Windows WSL2 gateway systemd" --mode keyword --limit 10 --json`

Résultats :

- La requête de mise à jour/npm/pnpm WSL2 a retourné 0 résultats.
- L'installation/intégration WSL2 a retourné le problème #63740, PR #74163 et le problème #86612.
- La requête gateway systemd WSL2 Windows a retourné des problèmes d'unité obsolète, de boucle de redémarrage et de service systemd qui chevauchent la dérive de mise à jour/métadonnées de service.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "WSL2 update npm pnpm openclaw gateway"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "WSL2 install Node openclaw onboard"`

Résultats :

- La requête de mise à jour/npm/pnpm WSL2 a retourné 8 résultats, incluant les sorties de statut WSL2 avec état de mise à jour pnpm/npm, service gateway en cours d'exécution mais Gateway inaccessible, journaux de redémarrage de mise à jour et conseils pour préférer `openclaw update`.
- La requête d'installation/intégration WSL2 a retourné 8 résultats, incluant les conseils d'installation WSL2, les avertissements Windows natifs, les rapports d'installation source et les prérequis de configuration.
