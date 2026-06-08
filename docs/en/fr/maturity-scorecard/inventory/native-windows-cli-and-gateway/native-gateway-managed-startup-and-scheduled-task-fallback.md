---
title: "Native Windows - Native Gateway Managed Startup and Scheduled Task Fallback Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Native Windows - Native Gateway Managed Startup and Scheduled Task Fallback Maturity Note

## Résumé

Le démarrage géré natif de Windows est implémenté et activement maintenu via
le Planificateur de tâches, un script de commande Gateway généré et un
mécanisme de secours du dossier Démarrage lorsque la création de tâche est
bloquée. La couverture est plus forte que le chemin avant-plan uniquement
car le code dispose de nombreux tests Windows ciblés, mais la qualité reste
en dessous de la version bêta car les preuves d'archive actuelles montrent
toujours des lanceurs de secours obsolètes, la détection du runtime des
tâches, le polissage des fenêtres cachées et la fiabilité du démarrage comme
risques opérateurs actifs.

## Portée des catégories

- `openclaw gateway install`, `status`, `start`, `stop`, `restart` et
  désinstallation lorsque le gestionnaire de services est le Planificateur
  de tâches Windows.
- Fichiers `gateway.cmd` générés ou lanceurs cachés sous le répertoire d'état
  OpenClaw et le dossier Démarrage.
- Statut du runtime de la tâche planifiée, sélection de l'utilisateur de la
  tâche, secours listener/PID, taskkill et comportement des lanceurs obsolètes.
- Secours du dossier Démarrage lorsque le Planificateur de tâches est
  indisponible ou refusé.

## Fonctionnalités

- openclaw gateway install: openclaw gateway install, status, start, stop, restart et comportement de démarrage géré.
- Fichiers lanceurs Gateway: Fichiers gateway.cmd générés et fichiers lanceurs cachés pour le démarrage géré.
- Statut du runtime de la tâche planifiée: Statut du runtime de la tâche planifiée, sélection de l'utilisateur de la tâche, secours listener/PID et réparation des tâches.
- Secours du dossier Démarrage: Secours du dossier Démarrage lorsque le Planificateur de tâches est indisponible.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score: `Beta (74%)`
- Signaux positifs: la documentation couvre le démarrage géré natif; la source
  dispose de la génération XML du Planificateur de tâches dédiée, des lanceurs
  de secours, de l'analyse du runtime, de l'inspection PID et des chemins de
  terminaison; les tests couvrent de nombreux cas de secours Windows.
- Signaux négatifs: les preuves sont lourdes sur les fixtures unitaires/runtime
  et plus légères sur la preuve d'installation/redémarrage/réparation de service
  Windows en direct répétable.
- Lacunes d'intégration: aucun scénario en direct actuel n'a été trouvé qui
  installe une tâche planifiée native, vérifie le démarrage automatique
  post-connexion, exerce le secours des tâches refusées, répare l'état de
  secours obsolète et prouve la disponibilité de Gateway après redémarrage.

## Score de qualité

- Score: `Alpha (64%)`
- Rapports Gitcrawl: les requêtes de tâche planifiée ont retourné la PR ouverte
  #51486 pour l'interrogation directe du runtime des tâches Windows, le problème
  #87156 pour le secours du dossier Démarrage obsolète après la mise à jour du
  docteur et le signal de style problème #70788 / PR #81330 autour des fenêtres
  de commande visibles.
- Rapports Discrawl: les discussions de support Windows décrivent la contention
  des lanceurs Démarrage en double, la confusion des résultats de dernière
  exécution des tâches, le comportement des lanceurs de secours et le polissage
  continu des tâches/fenêtres.
- Bonnes qualités: l'implémentation encode le XML du Planificateur de tâches
  spécifique à Windows, la gestion localisée de l'accès refusé, le support des
  lanceurs cachés, le secours basé sur les écouteurs et la terminaison de
  l'arborescence des processus Windows.
- Mauvaises qualités: il existe toujours plusieurs modes de lanceur avec risque
  de dérive, et les preuves de support montrent que les opérateurs peuvent se
  retrouver avec des chemins de démarrage obsolètes ou en double.
- Exclu de la qualité: les preuves de test unitaire, intégration, e2e, en direct
  et de flux runtime ne sont enregistrées que sous Couverture et Preuves.

## Score de complétude

- Score: `Beta (74%)`
- Instructions de surface: évaluées par rapport à `references/completeness/native-windows-cli-and-gateway.md`.
- Signaux positifs: les preuves archivées de docs, source, test, Gitcrawl et
  Discrawl couvrent la portée de la taxonomie pour openclaw gateway install,
  fichiers lanceurs Gateway, statut du runtime de la tâche planifiée, secours
  du dossier Démarrage.
- Signaux négatifs: la note archivée a précédé la notation de complétude de la
  version 3 du processus, donc ce score est initialisé à partir de la même
  largeur de preuves et du registre des lacunes connues utilisés pour le score
  de couverture archivé.
- Branches de capacité manquantes: voir `## Lacunes connues` et `## Preuves`
  ci-dessous pour les branches manquantes enregistrées et les avertissements
  visibles par l'opérateur.

## Lacunes connues

- Ajouter une preuve de démarrage géré Windows en direct pour l'installation,
  le statut, le redémarrage/connexion de démarrage automatique, le secours du
  Planificateur de tâches refusé, `gateway install --force` et le nettoyage
  des lanceurs du dossier Démarrage obsolètes.
- Ajouter une explication orientée utilisateur sur la façon de détecter et
  supprimer les lanceurs Windows en double lorsque le Planificateur de tâches
  et le secours du dossier Démarrage existent tous les deux.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:37` énumère les
  avertissements de démarrage géré natif.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:52` documente
  `openclaw gateway install` et `openclaw gateway status --json` pour le
  démarrage géré natif.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:59` indique que le
  mode de secours démarre automatiquement via le dossier Démarrage de
  l'utilisateur actuel.
- `/Users/kevinlin/code/openclaw/docs/gateway/index.md:135` énumère l'ensemble
  des commandes opérateur, y compris install/restart/stop/status.

### Source

- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.ts:45` définit les
  déclencheurs de secours pour l'accès refusé, le délai d'expiration et la
  sortie manquante.
- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.ts:121` construit le XML
  du Planificateur de tâches avec le comportement ONLOGON et les paramètres
  de batterie.
- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.ts:379` rend le script
  de commande Gateway généré.
- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.ts:433` rend un lanceur
  VBS caché pour le démarrage Windows.
- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.ts:673` bascule vers la
  détection du runtime basée sur les écouteurs lorsque `schtasks` ne signale
  pas l'exécution.
- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.ts:746` utilise `taskkill`
  pour la terminaison de l'arborescence des processus Windows.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels-windows-smoke.sh:1`
  distribue le pilote de fumée Windows Parallels.
- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels/windows-smoke.ts`
  contient les phases de fumée Windows natives pour le comportement du
  package/installation/Gateway.
- `/Users/kevinlin/code/openclaw/.github/workflows/windows-blacksmith-testbox.yml`
  définit l'infrastructure de validation native Windows.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.test.ts:24` teste
  l'analyse du runtime, le statut localisé, les chemins des scripts de tâches
  et l'analyse des commandes générées.
- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.startup-fallback.test.ts:224`
  teste le secours aux lanceurs du dossier Démarrage et le comportement des
  lanceurs cachés.
- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.install.test.ts` couvre
  le comportement d'installation des tâches Windows.
- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.stop.test.ts` couvre le
  comportement d'arrêt des tâches.
- `/Users/kevinlin/code/openclaw/src/daemon/inspect.test.ts` couvre
  l'inspection approfondie des services Windows.

### Requêtes Gitcrawl

Requête:

- `gitcrawl search openclaw/openclaw --query "windows gateway schtasks scheduled task fallback startup folder" --mode keyword --limit 5 --json`
- `gitcrawl search openclaw/openclaw --query "windows gateway schtasks" --mode keyword --limit 5 --json`

Résultats:

- La requête de tâche planifiée a retourné la PR ouverte #51486, le problème
  #87156 et la PR #74163 avec le signal de secours/tâche planifiée obsolète
  Windows.
- `windows gateway schtasks` a retourné les PR #51486, #76245, #63651, #68149
  et le problème #44559 couvrant la requête du runtime, le secours de sortie
  anticipée, le message de redémarrage en double, la création de tâche
  planifiée PowerShell et les déconnexions de fenêtre PowerShell.

### Requêtes Discrawl

Requête:

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 4 "windows gateway schtasks scheduled task fallback startup folder"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "windows gateway schtasks"`

Résultats:

- La requête de tâche planifiée a retourné des rapports Windows sur la
  contention des lanceurs Démarrage en double, `doctor --fix` réparation du
  service créant un secours Démarrage et les boucles de nouvelle tentative
  de passerelle du Planificateur de tâches.
- `windows gateway schtasks` a retourné les résumés des responsables du travail
  de secours de la tâche planifiée, la gestion localisée de l'accès refusé,
  les vérifications de santé du redémarrage et le polissage de la fenêtre
  visible.
