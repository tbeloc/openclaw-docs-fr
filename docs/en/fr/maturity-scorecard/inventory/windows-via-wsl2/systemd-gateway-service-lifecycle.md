---
title: "Windows via WSL2 - Gateway Service Lifecycle Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Windows via WSL2 - Gateway Service Lifecycle Maturity Note

## Résumé

Le cycle de vie de la passerelle WSL2 hérite de l'implémentation du service utilisateur systemd Linux. Les commandes documentées sont simples, et la base source/test pour les unités systemd, les métadonnées de service, le comportement de redémarrage et la réparation est substantielle. La qualité reste Beta car WSL2 ajoute des cas limites de bus utilisateur et d'environnement qui apparaissent toujours dans les rapports d'archive.

## Portée de la catégorie

Inclus dans cette catégorie :

- Installation systemd intégrée : installation du démon openclaw onboard à l'intérieur de WSL2.
- Installation du service Gateway : comportement d'installation de la passerelle openclaw sous WSL2 systemd.
- Rendu de l'unité utilisateur systemd : rendu de l'unité utilisateur systemd et métadonnées du cycle de vie.
- Conseils systemd conscients de WSL indisponibles : conseils opérateur lorsque systemd n'est pas disponible dans la distribution WSL.
- Réparation du service Doctor : comportement de réparation de Doctor pour les services Gateway WSL2.
- Linger du service utilisateur WSL : comportement du linger du service utilisateur WSL, statut et vérification visible par l'opérateur.
- Disponibilité de Systemd après le démarrage de Windows : disponibilité de Systemd après le démarrage de Windows et le démarrage de la distribution WSL.
- Tâche de démarrage Windows pour WSL : comportement de la tâche de démarrage Windows pour lancer WSL avant la connexion.
- Vérification avant la connexion Windows : comportement de vérification avant la connexion Windows, statut et vérification visible par l'opérateur.
- Attentes claires autour de l'alimentation du PC : attentes claires autour de l'alimentation du PC, de la mise en veille, du démarrage de Windows, du démarrage de WSL et de la disponibilité de la passerelle

## Fonctionnalités

- Installation systemd intégrée : installation du démon openclaw onboard à l'intérieur de WSL2.
- Installation du service Gateway : comportement d'installation de la passerelle openclaw sous WSL2 systemd.
- Rendu de l'unité utilisateur systemd : rendu de l'unité utilisateur systemd et métadonnées du cycle de vie.
- Conseils systemd conscients de WSL indisponibles : conseils opérateur lorsque systemd n'est pas disponible dans la distribution WSL.
- Réparation du service Doctor : comportement de réparation de Doctor pour les services Gateway WSL2.
- Linger du service utilisateur WSL : comportement du linger du service utilisateur WSL, statut et vérification visible par l'opérateur.
- Disponibilité de Systemd après le démarrage de Windows : disponibilité de Systemd après le démarrage de Windows et le démarrage de la distribution WSL.
- Tâche de démarrage Windows pour WSL : comportement de la tâche de démarrage Windows pour lancer WSL avant la connexion.
- Vérification avant la connexion Windows : comportement de vérification avant la connexion Windows, statut et vérification visible par l'opérateur.
- Attentes claires autour de l'alimentation du PC : attentes claires autour de l'alimentation du PC, de la mise en veille, du démarrage de Windows, du démarrage de WSL et de la disponibilité de la passerelle

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : les docs donnent les commandes de service WSL2 ; le runbook Gateway documente les unités utilisateur systemd Linux ; la source rend les paramètres par défaut systemd renforcés ; les tests couvrent le rendu de l'unité systemd, la disponibilité, la réparation du bus utilisateur et le comportement du commutateur doctor/install e2e Docker.
- Signaux négatifs : la couverture du service spécifique à WSL2 est principalement héritée des tests Linux/systemd plutôt que d'un e2e du cycle de vie Windows/WSL2 dédié.
- Lacunes d'intégration : aucune preuve WSL2 en direct n'a été trouvée pour l'installation, le statut, le redémarrage, la réparation doctor et la transmission de mise à jour à travers les limites de redémarrage de Windows et de redémarrage de WSL.

## Score de qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : `Windows WSL2 gateway systemd` a retourné la PR ouverte #58853 pour les diagnostics d'environnement WSL, le problème #55563 pour le cyclage de la passerelle après doctor, la PR #68400 pour la détection du socket D-Bus utilisateur WSL, le problème #80696 pour le timing RestartSec/lock systemd, le problème #84610 pour les boucles SIGTERM WSL2, et d'autres rapports WSL2/systemd.
- Rapports Discrawl : la recherche WSL2 systemd a retourné des threads d'assistance où les sondes de service WSL2 échouent avec `No medium found`, les utilisateurs sont rappelés que systemd démarre au démarrage de WSL, et les utilisateurs ont besoin d'aide pour distinguer les installations Windows natives des services WSL2.
- Bonnes qualités : les paramètres par défaut de l'unité sont robustes et soutenus par la source, avec des limites de redémarrage, le mode de suppression du groupe de contrôle, l'ordre du fichier d'environnement et les conseils spécifiques à WSL.
- Mauvaises qualités : le comportement du bus utilisateur WSL2 et la sémantique de démarrage Windows/WSL produisent toujours un statut de service trompeur et une confusion opérateur répétée.
- Exclu de la qualité : les preuves de test unitaire, intégration, e2e, en direct et de flux d'exécution sont exclues de ce score de qualité.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/windows-via-wsl2.md`.
- Signaux positifs : les preuves archivées docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'installation systemd intégrée, l'installation du service Gateway, le rendu de l'unité utilisateur systemd, les conseils systemd conscients de WSL indisponibles, la réparation du service Doctor, le linger du service utilisateur WSL, la disponibilité de Systemd après le démarrage de Windows, la tâche de démarrage Windows pour WSL, la vérification avant la connexion Windows, les attentes claires autour de l'alimentation du PC.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Besoin d'une fumée du cycle de vie du service WSL2 dédiée qui prouve l'installation/statut/redémarrage/arrêt/doctor sous une distro WSL2 réelle.
- Besoin de diagnostics de statut de service WSL2 plus clairs pour les défaillances du bus utilisateur telles que `No medium found`.
- Besoin de conseils d'assistance qui distinguent clairement le service utilisateur systemd WSL2 du comportement de la tâche planifiée Windows native.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:66` : les commandes d'installation du service Gateway WSL2 sont documentées.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:68` : les utilisateurs WSL2 exécutent `openclaw onboard --install-daemon`.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:76` : les utilisateurs WSL2 peuvent exécuter `openclaw gateway install`.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:88` : les points de réparation/migration WSL2 pointent vers `openclaw doctor`.
- `/Users/kevinlin/code/openclaw/docs/gateway/index.md:231` : le runbook Gateway documente les commandes du service utilisateur systemd Linux.
- `/Users/kevinlin/code/openclaw/docs/gateway/doctor.md:529` : doctor audite et répare la dérive de la configuration du superviseur pour launchd/systemd/schtasks.

### Source

- `/Users/kevinlin/code/openclaw/src/daemon/systemd-unit.ts:49` : le rendu de l'unité systemd construit l'unité OpenClaw Gateway.
- `/Users/kevinlin/code/openclaw/src/daemon/systemd-unit.ts:68` : l'unité inclut `After=network-online.target` et `Wants=network-online.target`.
- `/Users/kevinlin/code/openclaw/src/daemon/systemd-unit.ts:75` : l'unité utilise `Restart=always`, `RestartSec=5` et `RestartPreventExitStatus=78`.
- `/Users/kevinlin/code/openclaw/src/daemon/systemd-unit.ts:81` : l'unité garde les enfants du service dans le groupe de contrôle pour le nettoyage.
- `/Users/kevinlin/code/openclaw/src/daemon/systemd-hints.ts:27` : les conseils systemd spécifiques à WSL indisponibles disent aux utilisateurs d'activer systemd dans `/etc/wsl.conf`.
- `/Users/kevinlin/code/openclaw/src/cli/daemon-cli/lifecycle-core.ts:68` : le code du cycle de vie augmente les conseils de service avec des conseils systemd conscients de WSL.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/doctor-install-switch/scenario.sh:12` : Docker e2e stub systemd/loginctl pour que les flux doctor et daemon s'exécutent.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/doctor-install-switch/scenario.sh:122` : e2e vérifie l'installation du service avec une variante d'installation et la réparation doctor avec une autre.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/doctor-install-switch/scenario.sh:145` : e2e affirme que l'unité utilisateur systemd existe.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/daemon/systemd-unit.test.ts:15` : les tests unitaires affirment le mode de suppression du groupe de contrôle, les délais d'attente, la limite de redémarrage et la protection de sortie 78.
- `/Users/kevinlin/code/openclaw/src/daemon/systemd-unit.test.ts:42` : les tests unitaires affirment que les entrées EnvironmentFile se rendent avant les valeurs Environment en ligne.
- `/Users/kevinlin/code/openclaw/src/daemon/systemd.test.ts:158` : le test de disponibilité systemd retourne true lorsque `systemctl --user` réussit.
- `/Users/kevinlin/code/openclaw/src/daemon/systemd.test.ts:165` : le test de disponibilité systemd répare l'environnement du bus utilisateur manquant lorsque le bus d'exécution existe.
- `/Users/kevinlin/code/openclaw/src/cli/daemon-cli/response.test.ts:13` : les tests de réponse daemon classifient les conseils systemd WSL.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Windows WSL2 gateway systemd" --mode keyword --limit 10 --json`
- `gitcrawl search openclaw/openclaw --query "WSL2 systemd gateway install loginctl portproxy" --mode keyword --limit 10 --json`

Résultats :

- `Windows WSL2 gateway systemd` a retourné 10 résultats, incluant la PR #58853, le problème #55563, la PR #68400, le problème #56733, le problème #80696, le problème #84610 et les rapports de canal/runtime WSL2.
- La requête plus étroite install/loginctl/portproxy a retourné 0 résultats, ce qui est neutre après la vérification de fraîcheur car les requêtes WSL2/systemd plus larges ont retourné des problèmes de service pertinents.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "Windows WSL2 gateway systemd"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "WSL2 systemd gateway install loginctl portproxy"`

Résultats :

- Windows WSL2 gateway systemd a retourné 8 résultats, incluant les défaillances de sonde de service systemd `No medium found`, les conseils de redémarrage de la passerelle et les commentaires d'assistance distinguant le comportement du service systemd WSL2 du démarrage automatique Windows natif.
- WSL2 systemd/install/loginctl/portproxy a retourné une réponse d'assistance qui énumère les compromis de mise en réseau WSL2, d'E/S de fichier, de démarrage automatique/services et d'intégration Windows native.
