---
summary: "Comment OpenClaw valide les chemins de mise à jour, les migrations de paquets et le comportement d'installation/mise à jour des plugins"
read_when:
  - Modification du comportement de mise à jour, doctor, acceptation de paquets ou installation de plugins OpenClaw
  - Préparation ou approbation d'un candidat de version
  - Débogage des régressions de mise à jour de paquets, nettoyage des dépendances de plugins ou installation de plugins
title: "Tests : mises à jour et plugins"
sidebarTitle: "Tests de mise à jour et de plugins"
---

Ceci est la liste de contrôle dédiée à la validation des mises à jour et des plugins. L'objectif est simple : prouver que le paquet installable peut mettre à jour l'état réel de l'utilisateur, réparer l'état hérité obsolète via `doctor`, et installer, charger, mettre à jour et désinstaller des plugins à partir des sources prises en charge.

Pour la carte plus large du testeur, voir [Testing](/fr/help/testing). Pour les clés de fournisseur en direct et les suites touchant le réseau, voir [Testing live](/fr/help/testing-live).

## Ce que nous protégeons

Les tests de mise à jour et de plugins protègent ces contrats :

- Une archive de paquet est complète, a un `dist/postinstall-inventory.json` valide, et ne dépend pas de fichiers de dépôt déballés.
- Un utilisateur peut passer d'un paquet publié plus ancien au paquet candidat sans perdre la configuration, les agents, les sessions, les espaces de travail, les listes blanches de plugins ou la configuration des canaux.
- `openclaw doctor --fix --non-interactive` possède les chemins de nettoyage et de réparation hérités. Le démarrage ne doit pas développer de migrations de compatibilité cachées pour l'état de plugin obsolète.
- Les installations de plugins fonctionnent à partir de répertoires locaux, de dépôts git, de paquets npm et du chemin du registre ClawHub.
- Les dépendances npm des plugins sont installées dans la racine npm gérée, analysées avant la confiance, et supprimées via npm lors de la désinstallation afin que les dépendances remontées ne subsistent pas.
- La mise à jour du plugin est stable quand rien n'a changé : les enregistrements d'installation, la source résolue, la disposition des dépendances installées et l'état activé restent intacts.

## Preuve locale pendant le développement

Commencez étroitement :

```bash
pnpm changed:lanes --json
pnpm check:changed
pnpm test:changed
```

Pour les modifications d'installation, désinstallation, dépendance ou inventaire de paquets de plugins, exécutez également les tests ciblés qui couvrent la couture modifiée :

```bash
pnpm test src/plugins/uninstall.test.ts src/infra/package-dist-inventory.test.ts test/scripts/package-acceptance-workflow.test.ts
```

Avant que toute voie Docker de paquet ne consomme une archive, prouvez l'artefact de paquet :

```bash
pnpm release:check
```

`release:check` exécute les vérifications de dérive de configuration/docs/API, écrit l'inventaire de distribution de paquet, exécute `npm pack --dry-run`, rejette les fichiers empaquetés interdits, installe l'archive dans un préfixe temporaire, exécute postinstall et teste les points d'entrée de canal groupés.

## Voies Docker

Les voies Docker sont la preuve au niveau du produit. Elles installent ou mettent à jour un paquet réel dans des conteneurs Linux et affirment le comportement via des commandes CLI, le démarrage de Gateway, les sondes HTTP, l'état RPC et l'état du système de fichiers.

Utilisez des voies ciblées lors de l'itération :

```bash
pnpm test:docker:plugins
pnpm test:docker:plugin-lifecycle-matrix
pnpm test:docker:plugin-update
pnpm test:docker:upgrade-survivor
pnpm test:docker:published-upgrade-survivor
pnpm test:docker:update-restart-auth
pnpm test:docker:update-migration
```

Voies importantes :

- `test:docker:plugins` valide l'installation de plugins smoke, les installations de dossiers locaux, le comportement de saut de mise à jour de dossiers locaux, les dossiers locaux avec dépendances préinstallées, les installations de paquets `file:`, les installations git avec exécution CLI, les mises à jour de références mobiles git, les installations de registre npm avec dépendances transitives remontées, les mises à jour npm sans opération, le rejet de métadonnées de paquets npm mal formées, les installations de fixtures ClawHub locales et les mises à jour sans opération, le comportement de mise à jour de la place de marché et l'activation/inspection du bundle Claude. Définissez `OPENCLAW_PLUGINS_E2E_CLAWHUB=0` pour garder le bloc ClawHub hermétique/hors ligne.
- `test:docker:plugin-lifecycle-matrix` installe le paquet candidat dans un conteneur nu, exécute un plugin npm via l'installation, l'inspection, la désactivation, l'activation, la mise à niveau explicite, la rétrogradation explicite et la désinstallation après suppression du code du plugin. Il enregistre les métriques RSS et CPU pour chaque phase.
- `test:docker:plugin-update` valide qu'un plugin installé inchangé ne se réinstalle pas et ne perd pas les métadonnées d'installation lors de `openclaw plugins update`.
- `test:docker:upgrade-survivor` installe l'archive candidate sur une fixture d'ancien utilisateur sale, exécute la mise à jour du paquet plus doctor non-interactif, puis démarre une Gateway de boucle de retour et vérifie la préservation de l'état.
- `test:docker:published-upgrade-survivor` installe d'abord une ligne de base publiée, la configure via une recette `openclaw config set` cuite, la met à jour vers l'archive candidate, exécute doctor, vérifie le nettoyage hérité, démarre la Gateway et sonde `/healthz`, `/readyz` et l'état RPC.
- `test:docker:update-restart-auth` installe le paquet candidat, démarre une Gateway d'authentification par jeton gérée, désactive l'env d'authentification de gateway d'appelant pour `openclaw update --yes --json`, et exige que la commande de mise à jour candidate redémarre la Gateway avant les sondes normales.
- `test:docker:update-migration` est la voie de mise à jour publiée lourde en nettoyage. Elle commence à partir d'un état utilisateur configuré de style Discord/Telegram, exécute le doctor de base afin que les dépendances de plugins configurées aient une chance de se matérialiser, amorce les débris de dépendance de plugins hérités pour un plugin emballé configuré, met à jour vers l'archive candidate, et exige que le doctor post-mise à jour supprime les racines de dépendance hérités.

Variantes utiles de survivant de mise à niveau publiée :

```bash
OPENCLAW_UPGRADE_SURVIVOR_BASELINE_SPEC=openclaw@2026.4.23 \
OPENCLAW_UPGRADE_SURVIVOR_SCENARIO=versioned-runtime-deps \
pnpm test:docker:published-upgrade-survivor

OPENCLAW_UPGRADE_SURVIVOR_BASELINE_SPEC=openclaw@latest \
OPENCLAW_UPGRADE_SURVIVOR_SCENARIO=bootstrap-persona \
pnpm test:docker:published-upgrade-survivor
```

Les scénarios disponibles sont `base`, `feishu-channel`, `bootstrap-persona`, `plugin-deps-cleanup`, `configured-plugin-installs`, `stale-source-plugin-shadow`, `tilde-log-path` et `versioned-runtime-deps`. Dans les exécutions agrégées, `OPENCLAW_UPGRADE_SURVIVOR_SCENARIOS=reported-issues` se développe en tous les scénarios de forme de problème signalés, y compris la migration d'installation de plugin configurée.

La migration de mise à jour complète est intentionnellement séparée de Full Release CI. Utilisez le flux de travail manuel `Update Migration` quand la question de version est « chaque version stable publiée de 2026.4.23 en avant peut-elle se mettre à jour vers ce candidat et nettoyer les débris de dépendance de plugins ? » :

```bash
gh workflow run update-migration.yml \
  --ref main \
  -f workflow_ref=main \
  -f package_ref=main \
  -f baselines=all-since-2026.4.23 \
  -f scenarios=plugin-deps-cleanup
```

## Acceptation de paquet

Package Acceptance est la porte de paquet native GitHub. Elle résout un paquet candidat en une archive `package-under-test`, enregistre la version et SHA-256, puis exécute des voies Docker E2E réutilisables contre cette archive exacte. La référence du harnais de flux de travail est séparée de la référence source du paquet, afin que la logique de test actuelle puisse valider les versions de confiance plus anciennes.

Sources candidates :

- `source=npm` : valider `openclaw@beta`, `openclaw@latest` ou une version publiée exacte.
- `source=ref` : empaqueter une branche, une étiquette ou un commit de confiance avec le harnais actuel sélectionné.
- `source=url` : valider une archive HTTPS avec `package_sha256` requis.
- `source=artifact` : réutiliser une archive téléchargée par une autre exécution Actions.

Full Release Validation utilise `source=artifact` par défaut, construit à partir du SHA de version résolu. Pour la preuve post-publication, passez `package_acceptance_package_spec=openclaw@YYYY.M.D` afin que la même matrice de mise à niveau cible le paquet npm expédié à la place.

Les vérifications de version appellent Package Acceptance avec l'ensemble paquet/mise à jour/redémarrage/plugin :

```text
doctor-switch update-channel-switch update-corrupt-plugin upgrade-survivor published-upgrade-survivor update-restart-auth plugins-offline plugin-update
```

Quand le trempage de version est activé, ils passent également :

```text
published_upgrade_survivor_baselines=last-stable-4 2026.4.23 2026.5.2 2026.4.15
published_upgrade_survivor_scenarios=reported-issues
telegram_mode=mock-openai
```

Cela maintient la migration de paquet, le changement de canal de mise à jour, la tolérance de plugin géré corrompu, le nettoyage de dépendance de plugin obsolète, la couverture de plugin hors ligne, le comportement de mise à jour de plugin et l'assurance qualité de paquet Telegram sur le même artefact résolu sans faire marcher la porte de paquet de version par défaut chaque version OpenClaw publiée.

`last-stable-4` se résout aux quatre dernières versions OpenClaw stables publiées sur npm. L'acceptation de paquet de version épingle `2026.4.23` comme première limite de compatibilité de mise à jour de plugin, `2026.5.2` comme limite de churn d'architecture de plugin, et `2026.4.15` comme ligne de base de mise à jour publiée 2026.4.1x plus ancienne ; le résolveur déduplique les épingles qui sont déjà dans les quatre dernières. Pour une couverture de migration de mise à jour publiée exhaustive, utilisez `all-since-2026.4.23` dans le flux de travail Update Migration séparé au lieu de Full Release CI. `release-history` reste disponible pour l'échantillonnage manuel plus large quand vous voulez aussi l'ancre de pré-date hérité.

Quand plusieurs lignes de base de survivant de mise à niveau publiée sont sélectionnées, le flux de travail Docker réutilisable divise chaque ligne de base en sa propre tâche de coureur ciblée. Chaque partition de ligne de base exécute toujours l'ensemble de scénarios sélectionné, mais les journaux et artefacts restent par ligne de base et le temps mural est limité par la partition la plus lente au lieu d'une grande tâche série.

Exécutez un profil de paquet manuellement lors de la validation d'un candidat avant la version :

```bash
gh workflow run package-acceptance.yml \
  --ref main \
  -f workflow_ref=main \
  -f source=npm \
  -f package_spec=openclaw@beta \
  -f suite_profile=package \
  -f published_upgrade_survivor_baselines="last-stable-4 2026.4.23 2026.5.2 2026.4.15" \
  -f published_upgrade_survivor_scenarios=reported-issues \
  -f telegram_mode=mock-openai
```

Utilisez `suite_profile=product` quand la question de version inclut les canaux MCP, le nettoyage cron/subagent, la recherche web OpenAI ou OpenWebUI. Utilisez `suite_profile=full` uniquement quand vous avez besoin d'une couverture complète du chemin de version Docker.

## Version par défaut

Pour les candidats de version, la pile de preuve par défaut est :

1. `pnpm check:changed` et `pnpm test:changed` pour les régressions au niveau source.
2. `pnpm release:check` pour l'intégrité de l'artefact de paquet.
3. Package Acceptance profil `package` ou les voies de paquet personnalisées de vérification de version pour les contrats d'installation/mise à jour/redémarrage/plugin.
4. Vérifications de version multi-OS pour le comportement d'installateur, d'intégration et de plateforme spécifique au système d'exploitation.
5. Suites en direct uniquement quand la surface modifiée touche le comportement du fournisseur ou du service hébergé.

Sur les machines de mainteneur, les portes larges et la preuve de produit Docker/paquet doivent s'exécuter dans Testbox sauf si vous faites explicitement une preuve locale.

## Compatibilité hérité

La clémence de compatibilité est étroite et limitée dans le temps :

- Les paquets via `2026.4.25`, y compris `2026.4.25-beta.*`, peuvent tolérer les lacunes de métadonnées de paquet déjà expédiées dans Package Acceptance.
- Le paquet publié `2026.4.26` peut avertir pour les fichiers d'horodatage de métadonnées de construction locaux déjà expédiés.
- Les paquets ultérieurs doivent satisfaire les contrats modernes. Les mêmes lacunes échouent au lieu d'avertir ou de sauter.

N'ajoutez pas de nouvelles migrations de démarrage pour ces anciennes formes. Ajoutez ou étendez une réparation doctor, puis prouvez-la avec `upgrade-survivor`, `published-upgrade-survivor` ou `update-restart-auth` quand la commande de mise à jour possède le redémarrage.

## Ajouter une couverture

Lors de la modification du comportement des mises à jour ou des plugins, ajoutez une couverture au niveau le plus bas qui peut échouer pour la bonne raison :

- Logique de chemin ou de métadonnées pur : test unitaire à côté de la source.
- Inventaire des packages ou comportement des fichiers empaquetés : test `package-dist-inventory` ou vérificateur de tarball.
- Comportement d'installation/mise à jour CLI : assertion de lane Docker ou test de fixture.
- Comportement de migration de version publiée : scénario `published-upgrade-survivor`.
- Comportement de redémarrage détenu par la mise à jour : `update-restart-auth`.
- Comportement de la source du registre/package : fixture `test:docker:plugins` ou serveur de fixture ClawHub.
- Comportement de disposition des dépendances ou de nettoyage : affirmer à la fois l'exécution à l'exécution et la limite du système de fichiers. Les dépendances npm peuvent être remontées sous la racine npm gérée, donc les tests doivent prouver que la racine est analysée/nettoyée au lieu de supposer un arbre `node_modules` local au package.

Gardez les nouvelles fixtures Docker hermétiques par défaut. Utilisez des registres de fixtures locaux et des packages factices sauf si le point du test est le comportement du registre en direct.

## Triage des défaillances

Commencez par l'identité de l'artefact :

- Résumé `resolve_package` d'acceptation de package : source, version, SHA-256 et nom de l'artefact.
- Artefacts Docker : `.artifacts/docker-tests/**/summary.json`, `failures.json`, journaux de lane et commandes de réexécution.
- Résumé du survivant de mise à niveau : `.artifacts/upgrade-survivor/summary.json`, incluant la version de base, la version candidate, le scénario, les délais de phase et les étapes de recette.

Préférez réexécuter la lane exacte défaillante avec le même artefact de package plutôt que de réexécuter tout le parapluie de version.
