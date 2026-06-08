---
title: "ClawHub - Note de maturité du cycle de vie et de la santé des plugins"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# ClawHub - Note de maturité du cycle de vie et de la santé des plugins

## Résumé

La sélection de la source du plugin, les flux d'installation/mise à jour/désinstallation et la réparation des dépendances post-installation forment un cycle de vie opérateur en pratique. Les utilisateurs peuvent installer à partir de ClawHub, npm, archives npm-pack, git, chemins locaux, archives et raccourcis de marketplace, tandis que le runtime maintient des racines npm gérées par plugin, une réparation des pairs, un nettoyage du docteur et une vérification post-redémarrage séparés du chargement de la passerelle. La couverture est Beta car le cycle de vie et le comportement de réparation sont documentés et testés. La qualité reste Beta car la résolution de spécifications nues, les replis de catalogue, la réparation des dépendances et l'état d'installation obsolète créent toujours une confusion opérateur et des régressions récentes.

## Portée de la catégorie

Inclus dans cette catégorie :

- Préfixes de source : Préfixes de source et résolution de raccourcis pour clawhub:, npm:,
- Comportement des packages nus lors du lancement : Comportement des packages nus lors de la transition de lancement
- Versions explicitement épinglées : Versions explicitement épinglées, balises de préversion et comportement de repli stable
- Enregistrements d'installation gérés qui préservent la source : Enregistrements d'installation gérés qui préservent les métadonnées de source pour la mise à jour/désinstallation
- Codex : Détection de bundle compatible Codex, Claude et Cursor
- Local : Chemins d'installation locaux, d'archive et de marketplace
- Liste Marketplace : Liste Marketplace, raccourci et flux d'installation
- Fonctionnalités mappées supportées : Fonctionnalités mappées supportées et capacités détectées mais non exécutées
- Sécurité du chemin de marketplace distant : Sécurité du chemin de marketplace distant et protections de téléchargement d'archive
- Mise à jour par ID de plugin : Mise à jour par ID de plugin, spécification npm, spécification ClawHub, canal bêta et marketplace
- Sémantique de réinstallation vs mise à jour : Portée des preuves pour la sémantique de réinstallation vs mise à jour.
- Rétrogradation : Rétrogradation et sélecteurs épinglés
- Nettoyage de config/index/policy/fichier de désinstallation : Portée des preuves pour le nettoyage de config/index/policy/fichier de désinstallation.
- Exigences de redémarrage/rechargement de la passerelle après : Exigences de redémarrage/rechargement de la passerelle après installation/mise à jour/désinstallation
- Racines de projet npm gérées par plugin : Racines de projet npm gérées par plugin
- Installations de candidat à la version locale npm-pack : Installations de candidat à la version locale npm-pack via la sémantique npm
- Propriété des dépendances entre les packages de plugins : Propriété des dépendances entre les packages de plugins et OpenClaw
- Reliaison des dépendances de pairs : Reliaison des dépendances de pairs pour openclaw/plugin-sdk/\*
- Nettoyage de la racine des dépendances héritées : Nettoyage de la racine des dépendances héritées et réparation du docteur
- Liste des plugins : Liste des plugins, inspection des plugins, inspection du runtime, docteur des plugins, et
- Index de plugin local : Index de plugin local et état du registre froid persistant
- Dépannage de la config obsolète : Dépannage de la config obsolète, chemins bloqués, dépendances, plugins manquants,
- Vérification du runtime après la passerelle : Vérification du runtime après redémarrage de la passerelle

## Fonctionnalités

- Préfixes de source : Préfixes de source et résolution de raccourcis pour clawhub:, npm:,
- Comportement des packages nus lors du lancement : Comportement des packages nus lors de la transition de lancement
- Versions explicitement épinglées : Versions explicitement épinglées, balises de préversion et comportement de repli stable
- Enregistrements d'installation gérés qui préservent la source : Enregistrements d'installation gérés qui préservent les métadonnées de source pour la mise à jour/désinstallation
- Codex : Détection de bundle compatible Codex, Claude et Cursor
- Local : Chemins d'installation locaux, d'archive et de marketplace
- Liste Marketplace : Liste Marketplace, raccourci et flux d'installation
- Fonctionnalités mappées supportées : Fonctionnalités mappées supportées et capacités détectées mais non exécutées
- Sécurité du chemin de marketplace distant : Sécurité du chemin de marketplace distant et protections de téléchargement d'archive
- Mise à jour par ID de plugin : Mise à jour par ID de plugin, spécification npm, spécification ClawHub, canal bêta et marketplace
- Sémantique de réinstallation vs mise à jour : Portée des preuves pour la sémantique de réinstallation vs mise à jour.
- Rétrogradation : Rétrogradation et sélecteurs épinglés
- Nettoyage de config/index/policy/fichier de désinstallation : Portée des preuves pour le nettoyage de config/index/policy/fichier de désinstallation.
- Exigences de redémarrage/rechargement de la passerelle après : Exigences de redémarrage/rechargement de la passerelle après installation/mise à jour/désinstallation
- Racines de projet npm gérées par plugin : Racines de projet npm gérées par plugin
- Installations de candidat à la version locale npm-pack : Installations de candidat à la version locale npm-pack via la sémantique npm
- Propriété des dépendances entre les packages de plugins : Propriété des dépendances entre les packages de plugins et OpenClaw
- Reliaison des dépendances de pairs : Reliaison des dépendances de pairs pour openclaw/plugin-sdk/\*
- Nettoyage de la racine des dépendances héritées : Nettoyage de la racine des dépendances héritées et réparation du docteur
- Liste des plugins : Liste des plugins, inspection des plugins, inspection du runtime, docteur des plugins, et
- Index de plugin local : Index de plugin local et état du registre froid persistant
- Dépannage de la config obsolète : Dépannage de la config obsolète, chemins bloqués, dépendances, plugins manquants,
- Vérification du runtime après la passerelle : Vérification du runtime après redémarrage de la passerelle
- Installations de compétences ClawHub : Installer et mettre à jour les compétences d'espace de travail ou globales suivies par ClawHub.
- Chemin d'installation de téléchargement de compétence : Téléchargement d'archive privée de confiance et installation via les API de téléchargement de compétences.
- Installateurs de dépendances de compétence : Installateurs Brew, Node, Go, uv ou téléchargement déclarés pour les packages de compétences.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : la documentation et l'interface de ligne de commande couvrent les principales formes de source, les chemins d'installation spécifiques à la source sont implémentés, les racines npm gérées et la réparation des pairs sont explicites, et les tests du cycle de vie exercent l'installation npm, la mise à jour, la rétrogradation, la désinstallation et les assertions d'état des dépendances.
- Signaux négatifs : l'audit n'a pas trouvé une seule voie de version en direct établie qui couvre ClawHub plus npm plus git plus réparation du docteur après la perturbation récente de la racine gérée.
- Lacunes d'intégration : le comportement de spécification nue, le repli de catalogue officiel, la réparation des dépendances et la récupération d'arbre corrompu nécessitent une matrice de fumée visible par l'utilisateur pour les chemins d'installation et de réparation courants.

## Score de qualité

- Score : `Beta (71%)`
- Bonnes qualités : la sélection de source est explicite lorsqu'elle est préfixée, les installations locales et liées sont séparées, les spécifications du registre npm sont contraintes, les enregistrements d'installation préservent les métadonnées de source, les racines gérées maintiennent le nettoyage limité, et les liens de pairs obsolètes sont réparés explicitement.
- Mauvaises qualités : le comportement de spécification nue change selon l'état du catalogue officiel et la propriété du plugin fourni, tandis que les preuves d'archive montrent toujours une perturbation de la racine des dépendances, des chemins de réparation obsolètes et des régressions du scanner au moment de l'installation.
- Exclu de la qualité : les preuves de test unitaire, d'intégration, e2e, en direct et de flux d'exécution ne sont comptées que sous Couverture, pas Qualité.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/clawhub-and-external-plugin-distribution.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les préfixes de source, le comportement des packages nus lors du lancement, les versions explicitement épinglées, les enregistrements d'installation gérés qui préservent la source, Codex, Local, la liste Marketplace, les fonctionnalités mappées supportées, la sécurité du chemin de marketplace distant, la mise à jour par ID de plugin, la sémantique de réinstallation vs mise à jour, la rétrogradation, le nettoyage de config/index/policy/fichier de désinstallation, les exigences de redémarrage/rechargement de la passerelle après, les racines de projet npm gérées par plugin, les installations de candidat à la version locale npm-pack, la propriété des dépendances entre les packages de plugins, la reliaison des dépendances de pairs, le nettoyage de la racine des dépendances héritées, la liste des plugins, l'index de plugin local, le dépannage de la config obsolète, la vérification du runtime après la passerelle, les installations de compétences ClawHub, le chemin d'installation de téléchargement de compétence, les installateurs de dépendances de compétence.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un petit tableau de liste de contrôle de version pour `clawhub:`, `npm:`, ID officiel nu, `@openclaw/*` brut, git, archive, npm-pack, lien local, marketplace et récupération de réparation du docteur.
- Améliorer le langage de diagnostic visible par l'utilisateur lorsqu'un arbre de dépendances de plugin est corrompu mais que la correction est mise à jour vs réinstallation vs docteur.
- Envisager de rendre la sortie de résolution de source plus explicite avant le téléchargement/installation pour chaque package non préfixé.

## Preuves

### Docs

- `docs/tools/plugin.md:50` : le démarrage rapide inclut ClawHub, npm, git et les installations locales.
- `docs/tools/plugin.md:120` : le tableau des sources explique ClawHub, npm, git, le chemin local et la marketplace.
- `docs/tools/plugin.md:128` : les spécifications de paquets nus préfèrent le comportement du catalogue groupé/officiel avant le recours à npm.
- `docs/cli/plugins.md:102` : la référence de commande liste les formes de recherche et d'installation pour tous les types de sources supportés.
- `docs/cli/plugins.md:207` : les installations ClawHub utilisent des localisateurs explicites `clawhub:<package>`.
- `docs/plugins/dependency-resolution.md:11` : le travail de dépendance est effectué au moment de l'installation/mise à jour, pas à l'exécution.
- `docs/plugins/dependency-resolution.md:35` : les paquets npm s'installent dans des projets par plugin.
- `docs/plugins/dependency-resolution.md:49` : npm-pack utilise la même racine de projet par plugin et vérifie les métadonnées du fichier de verrouillage.
- `docs/plugins/dependency-resolution.md:90` : les liens de pairs `openclaw` hôtes sont réaffirmés après l'installation/mise à jour.
- `docs/plugins/dependency-resolution.md:132` : le docteur peut nettoyer l'état des dépendances héritées et récupérer les plugins téléchargeables manquants.

### Source

- `src/cli/plugins-cli.ts:130` : la commande d'installation accepte les entrées de chemin, archive, npm, git, ClawHub ou marketplace.
- `src/infra/clawhub-spec.ts:3` : analyse les spécifications `clawhub:<name>[@version]`.
- `src/plugins/install.ts:2012` : valide les spécifications du registre npm, résout les métadonnées, gère le recours à la compatibilité et délègue à l'installateur de racine npm géré.
- `src/plugins/install.ts:770` : installe dans une racine de projet npm gérée.
- `src/plugins/install.ts:823` : enregistre la cible d'installation npm gérée et répare les dépendances de pairs hôtes obsolètes.
- `src/plugins/install.ts:839` : annule les installations npm gérées échouées.
- `src/plugins/install.ts:1855` : l'installation d'archive nécessite un manifeste de plugin avant d'écrire les enregistrements d'installation.
- `src/plugins/install.ts:1899` : chemin d'installation du répertoire local.
- `src/plugins/install-security-scan.ts:82` : analyse les arbres de dépendances installés.
- `src/plugins/uninstall.ts:538` : planifie le nettoyage de la désinstallation pour les installations gérées par npm et la suppression sécurisée du répertoire.

### Tests d'intégration

- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:41` : installe un plugin de fixture à partir de npm.
- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:53` : met à jour le plugin installé via npm vers une version ultérieure.
- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:57` : rétrograde le plugin via le chemin de mise à jour.
- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:43` : affirme que le plugin installé a une racine de projet npm.
- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:55` : affirme la racine du projet npm après la mise à niveau.
- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:59` : affirme la racine du projet npm après la rétrogradation.
- `scripts/e2e/lib/release-plugin-marketplace/scenario.sh:79` : installe un plugin marketplace à partir d'une CLI OpenClaw installée en tant que paquet.

### Tests unitaires

- `src/plugins/clawhub.test.ts:312` : installe un plugin de code ClawHub via l'installateur d'archive.
- `src/plugins/marketplace.test.ts:403` : résout les raccourcis de style Claude `plugin@marketplace`.
- `src/plugins/update.test.ts:788` : répare les liens de pairs `openclaw` manquants avant de sauter les plugins npm inchangés.
- `src/plugins/update.test.ts:2148` : met à jour les plugins installés via ClawHub via les métadonnées de paquet enregistrées.
- `src/plugins/uninstall.test.ts:967` : désinstalle les paquets gérés par npm via npm avant de supprimer les répertoires de paquets.
- `src/plugins/uninstall.test.ts:1028` : désinstalle les paquets de projet npm par plugin via leur racine de projet.
- `src/plugins/uninstall.test.ts:1093` : répare les liens de pairs des plugins npm restants après que npm uninstall les ait supprimés.
- `src/commands/doctor/shared/plugin-dependency-cleanup.test.ts:32` : supprime les racines d'état des dépendances de plugins héritées.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "plugins install clawhub npm git local archive marketplace npm-pack source resolver" --limit 5 --json`
- `gitcrawl search openclaw/openclaw --query "plugin management install update uninstall ClawHub npm" --limit 5 --json`
- `gitcrawl search openclaw/openclaw --query "plugin dependency cleanup managed npm root" --limit 5 --json`

Résultats :

- La première requête n'a retourné aucun résultat.
- La deuxième requête a retourné #75186, notant les RPC de gestion des plugins et appelant explicitement que l'installation, la mise à jour et la désinstallation en direct npm/ClawHub nécessitaient toujours une vérification.
- La requête de nettoyage des dépendances a retourné #87647, `fix: isolate npm plugin installs per package`, expliquant pourquoi les racines gérées partagées ont été supprimées après qu'un plugin ait évincé les dépendances d'un autre.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "plugins install ClawHub npm git local marketplace"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "plugin dependency install managed npm root"`

Résultats :

- La requête de source d'installation n'a retourné aucun résultat, donc l'archive Discord n'a pas ajouté de preuve de résolution de source au-delà du code/docs/tests.
- La requête de dépendance a retourné des notes de mainteneur du 2026-05-13 indiquant que les tests d'installation de plugins ne pouvaient pas s'exécuter localement, le scanner de dépendances au moment de l'installation avait un rayon d'impact frais, les liens de pairs npm gérés nécessitaient une réparation, et la bêta 5 devrait être traitée comme obsolète/cassée pour l'installation de plugins jusqu'à une bêta plus récente.
