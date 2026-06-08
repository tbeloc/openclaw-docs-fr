---
title: "Native Windows - Updates Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Native Windows - Updates Maturity Note

## Résumé

Le comportement de mise à jour Windows a un véritable investissement produit : la documentation des mises à jour avertit du transfert de passerelle géré, la source contient du texte de récupération spécifique à Windows et du code de transfert détaché, et la validation des versions inclut des tests de fumée pour les packages/installations Windows. Le chemin score toujours en dessous de stable car les preuves d'archive montrent que les problèmes EBUSY, de transfert par étapes, de fenêtre enfant cachée, de secours obsolète et de redémarrage après mise à jour sont toujours actifs.

## Portée de la catégorie

Inclus dans cette catégorie :

- mise à jour openclaw sur package Windows natif : installations de mise à jour openclaw sur package Windows natif
- Arrêt/redémarrage de la passerelle gérée : arrêt/redémarrage de la passerelle gérée et actualisation des métadonnées de service lors de la mise à jour
- Transfert de mise à jour détaché : transfert de mise à jour détaché à partir d'une passerelle en cours d'exécution.
- Verrous de package Windows : verrous de package Windows, comportement EBUSY/EPERM, échanges par étapes, fenêtre enfant

## Fonctionnalités

- mise à jour openclaw sur package Windows natif : installations de mise à jour openclaw sur package Windows natif
- Arrêt/redémarrage de la passerelle gérée : arrêt/redémarrage de la passerelle gérée et actualisation des métadonnées de service lors de la mise à jour
- Transfert de mise à jour détaché : transfert de mise à jour détaché à partir d'une passerelle en cours d'exécution.
- Verrous de package Windows : verrous de package Windows, comportement EBUSY/EPERM, échanges par étapes, fenêtre enfant

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : la documentation de mise à jour couvre les mises à jour du gestionnaire de packages et le transfert de service géré ; la source contient du texte de récupération pour l'état de la tâche planifiée Windows/élément de connexion ; la documentation CI mentionne les voies d'installation et de package Windows ; les tests couvrent la récupération de mise à jour et le comportement Windows empaqueté.
- Signaux négatifs : la preuve de mise à jour Windows en direct existe en tant qu'infrastructure de version, mais pas en tant qu'artefact de scénario local simple joint à cet audit.
- Lacunes d'intégration : aucune preuve d'exécution unique n'a été trouvée pour la mise à jour de package tandis qu'une passerelle de tâche planifiée Windows native est en cours d'exécution, redémarrage du service après mise à jour, nettoyage du secours obsolète et vérification de la version/accessibilité de la passerelle après mise à jour.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : `Windows update` a retourné la PR #79694 pour les fenêtres enfants cachées après mise à jour/achèvement du noyau, la PR #75649 pour la préservation du transfert de mise à jour Windows par étapes, le problème #40540 pour les défaillances de mise à jour EBUSY, et le problème #87156 pour le secours du dossier de démarrage obsolète après la mise à jour du docteur.
- Rapports Discrawl : les résumés des responsables décrivent les correctifs de mise à jour Windows pour les blocages post-noyau, les échanges de mise à jour obsolètes, l'arrêt de la passerelle avant la mise à jour, le redémarrage après la mise à jour, la récupération du délai d'attente empaqueté et la stabilité npm.
- Bonnes qualités : le chemin de mise à jour reconnaît les racines de service gérées, bloque les mises à jour non sécurisées en passerelle, utilise le transfert détaché pour les mises à jour du plan de contrôle et imprime les conseils de récupération spécifiques à Windows.
- Mauvaises qualités : le verrouillage des fichiers Windows et le transfert de service restent des risques produits actifs, et l'état du lanceur de secours obsolète peut survivre à la mise à jour/réparation.
- Exclu de la qualité : les preuves de test unitaire, d'intégration, e2e, en direct et de flux d'exécution sont enregistrées uniquement sous Couverture et Preuves.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/native-windows-cli-and-gateway.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la mise à jour openclaw sur package Windows natif, l'arrêt/redémarrage de la passerelle gérée, le transfert de mise à jour détaché, les verrous de package Windows.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un scénario de mise à jour Windows natif couvrant la ligne de base du package installé, la passerelle gérée en cours d'exécution, `openclaw update`, transfert de redémarrage, vérification de version, état du service et nettoyage du lanceur obsolète.
- Ajouter une documentation opérateur pour reconnaître les défaillances EBUSY/verrou de fichier Windows et récupérer en toute sécurité avec `gateway stop`, réinstallation de package et `gateway install --force`.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/install/updating.md:11` recommande
  `openclaw update` et dit qu'il redémarre la passerelle.
- `/Users/kevinlin/code/openclaw/docs/install/updating.md:71` dit que les mises à jour de passerelle gérée actualisent les métadonnées de service et redémarrent sauf si `--no-restart` est passé.
- `/Users/kevinlin/code/openclaw/docs/install/updating.md:111` avertit d'arrêter une passerelle supervisée avant le remplacement manuel du gestionnaire de packages.
- `/Users/kevinlin/code/openclaw/docs/install/updating.md:213` décrit le transfert du plan de contrôle du service géré.
- `/Users/kevinlin/code/openclaw/docs/ci.md:303` dit que les voies fraîches d'installation et de package Windows vérifient le comportement du package installé.

### Source

- `/Users/kevinlin/code/openclaw/src/cli/update-cli/update-command.ts:717`
  formate les conseils de récupération post-mise à jour spécifiques à la plateforme.
- `/Users/kevinlin/code/openclaw/src/cli/update-cli/update-command.ts:733`
  dit aux utilisateurs Windows de récupérer l'état manquant/obsolète de la tâche planifiée ou de l'élément de connexion avec `gateway install --force` et `gateway status --deep`.
- `/Users/kevinlin/code/openclaw/src/cli/update-cli/update-command.ts:823`
  inspecte et arrête les services gérés avant la mise à jour du package.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/update-managed-service-handoff.ts:25`
  contient le script de transfert de mise à jour gérée détaché.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/update-managed-service-handoff.ts:205`
  génère la commande de mise à jour gérée après la sortie de la passerelle parent.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels-windows-smoke.sh:1`
  distribue la voie de fumée Windows.
- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels-npm-update-smoke.sh`
  distribue l'infrastructure de fumée de mise à jour de package.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/upgrade-survivor/probe-gateway.mjs`
  sonde la santé de la passerelle après les scénarios de mise à jour.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/upgrade-survivor/config-recipe/gateway.json`
  inclut la couverture de recette de configuration de passerelle pour les voies upgrade-survivor.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/cli/update-cli/update-command.test.ts:684`
  couvre le blocage de redémarrage post-noyau de configuration invalide.
- `/Users/kevinlin/code/openclaw/src/cli/update-cli/restart-helper.test.ts`
  couvre le comportement du helper de redémarrage de mise à jour.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/update-managed-service-handoff.test.ts`
  couvre le comportement du transfert de mise à jour du service géré.
- `/Users/kevinlin/code/openclaw/src/infra/update-startup.test.ts` couvre le comportement de démarrage de mise à jour.
- `/Users/kevinlin/code/openclaw/test/scripts/parallels-npm-update-smoke.test.ts`
  couvre les helpers de fumée de mise à jour npm Parallels.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Windows update gateway restart npm package locks scheduled task" --mode keyword --limit 5 --json`
- `gitcrawl search openclaw/openclaw --query "Windows update" --mode keyword --limit 8 --json`

Résultats :

- La requête de mise à jour étroite a retourné 0 résultats.
- `Windows update` a retourné la PR #79694, la PR #59705, la PR #75649, le problème #40540,
  le problème #87156 et le problème #70788, couvrant les fenêtres enfants cachées, la journalisation de mise à jour Parallels, la préservation du transfert par étapes, les défaillances EBUSY, l'état du secours obsolète et le polissage de la fenêtre de démarrage.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 4 "Windows update gateway restart npm package locks scheduled task"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 4 "install.ps1 Windows PowerShell installer"`

Résultats :

- La requête de mise à jour étroite a retourné une sortie de résumé Windows notant la validation des versions avec une fumée d'installation/mise à jour Windows réelle, une mise à niveau empaqueté, un démarrage de passerelle et des vérifications de récupération.
- La requête du programme d'installation a retourné des résumés Windows natifs que la mise à jour a obtenu des correctifs pour les blocages post-noyau, les échanges de mise à jour obsolètes, l'arrêt de la passerelle avant la mise à jour, le redémarrage après la mise à jour, la récupération du délai d'attente empaqueté et la stabilité npm/installation.
