---
title: "Windows natif - Note de maturité des diagnostics Windows, du statut, du docteur et de la réparation"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Windows natif - Note de maturité des diagnostics Windows, du statut, du docteur et de la réparation

## Résumé

Les diagnostics Windows réutilisent les surfaces larges `status`, `gateway status`, `doctor`, logs et service-audit. L'implémentation peut inspecter l'état du Planificateur de tâches, les scripts générés, la dérive de service, la santé de la passerelle et les problèmes de configuration/authentification. La couverture est significative, mais la qualité reste alpha car les preuves d'archive montrent que la réparation Windows peut laisser des solutions de secours obsolètes dans le dossier Démarrage, induire en erreur sur l'état du Planificateur de tâches ou afficher du bruit d'achèvement/plugin difficile à traiter.

## Portée de la catégorie

- `openclaw status`, `openclaw gateway status`, `gateway status --deep`,
  `openclaw doctor`, `doctor --fix` et support des logs/stabilité sur Windows.
- Inspection des services Windows, analyse du runtime du Planificateur de tâches, inspection des solutions de secours du dossier Démarrage, santé de l'authentification de la passerelle et réparation de la dérive de service.
- Diagnostics attendus après l'installation, la mise à jour ou le démarrage échoué de la passerelle.

## Fonctionnalités

- openclaw status : openclaw status, openclaw gateway status, gateway status --deep et conseils de réparation Windows.
- Inspection des services Windows : inspection des services Windows, analyse du runtime du Planificateur de tâches, dossier Démarrage
- Diagnostics post-installation : diagnostics, statut et comportement de réparation attendus après l'installation native de Windows.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (72%)`
- Signaux positifs : la documentation couvre les commandes doctor/status ; la source contient des vérifications de santé structurées, un audit de service, des analyses de service approfondies, la santé de la passerelle et l'analyse du Planificateur de tâches Windows ; les tests couvrent de nombreux chemins status/doctor.
- Signaux négatifs : la preuve de réparation spécifique à Windows est principalement au niveau unitaire et basée sur le support plutôt que sur des scénarios de réparation en direct répétés.
- Lacunes d'intégration : aucun scénario de réparation Windows en direct n'a été trouvé pour la tâche planifiée obsolète, la solution de secours Démarrage obsolète, l'échec du chargement de l'achèvement/plugin, l'échec de la santé de la passerelle et l'accessibilité réussie de la passerelle après réparation.

## Score de qualité

- Score : `Alpha (64%)`
- Rapports Gitcrawl : `Windows doctor gateway status schtasks completion` a retourné un signal ouvert pour la solution de secours obsolète du dossier Démarrage après la mise à jour du docteur et le suivi de la plateforme Windows.
- Rapports Discrawl : les discussions de sortie du docteur Windows incluent la confusion sur l'état du Planificateur de tâches, la duplication du lanceur de solution de secours et les problèmes de chargement de commande du cache d'achèvement/plugin.
- Bonnes qualités : le docteur a un contrat lint/réparation structuré, une politique de réparation de service, l'analyse du Planificateur de tâches Windows et une sémantique d'analyse de service deep-status explicite.
- Mauvaises qualités : Windows a plusieurs sources d'état de service et la réparation peut toujours produire un état de lanceur confus ou obsolète.
- Exclu de la qualité : les preuves de test unitaire, intégration, e2e, en direct et de flux d'exécution sont enregistrées uniquement sous Couverture et Preuves.

## Score de complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/native-windows-cli-and-gateway.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour openclaw status, inspection des services Windows, diagnostics post-installation.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un scénario de docteur Windows qui commence à partir d'états connus-mauvais de tâche planifiée et de solution de secours Démarrage, exécute la réparation et vérifie l'état du service de passerelle résultant.
- Ajouter un bundle de diagnostic prêt pour le support pour Windows natif qui capture le Planificateur de tâches, les lanceurs du dossier Démarrage, les scripts générés, les logs et les URL de passerelle accessibles dans un artefact édité.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/cli/doctor.md:18` définit le docteur comme la surface de santé principale.
- `/Users/kevinlin/code/openclaw/docs/cli/doctor.md:25` documente les postures d'inspection, réparation et lint.
- `/Users/kevinlin/code/openclaw/docs/cli/doctor.md:67` documente les analyses de service `--deep`.
- `/Users/kevinlin/code/openclaw/docs/cli/doctor.md:196` dit que `doctor --fix` non-interactif rapporte les définitions de service obsolètes/manquantes mais ne les installe ou réécrit pas en dehors du mode de réparation de mise à jour.
- `/Users/kevinlin/code/openclaw/docs/gateway/index.md:40` documente les commandes status, health et logs.

### Source

- `/Users/kevinlin/code/openclaw/src/commands/doctor-gateway-services.ts:1` implémente les diagnostics et la politique de réparation du service de passerelle.
- `/Users/kevinlin/code/openclaw/src/commands/gateway-status.ts:38` implémente la sonde de statut de la passerelle.
- `/Users/kevinlin/code/openclaw/src/commands/status.gateway-connection.ts:20` formate les détails de connexion de la passerelle.
- `/Users/kevinlin/code/openclaw/src/daemon/inspect.ts` trouve les services de passerelle supplémentaires sur les gestionnaires de services.
- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.ts:304` analyse la sortie de la requête `schtasks`.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/doctor-install-switch-docker.sh` exerce le changement doctor/install dans un environnement de type service.
- `/Users/kevinlin/code/openclaw/test/cli-json-stdout.e2e.test.ts` couvre le comportement de sortie CLI structuré.
- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels-windows-smoke.sh:1` distribue l'infrastructure de fumée Windows native.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/commands/doctor-gateway-services.test.ts` couvre le comportement du docteur du service de passerelle.
- `/Users/kevinlin/code/openclaw/src/commands/doctor-gateway-health.test.ts` couvre les diagnostics de santé de la passerelle.
- `/Users/kevinlin/code/openclaw/src/commands/status.daemon.test.ts` couvre le comportement du statut du daemon.
- `/Users/kevinlin/code/openclaw/src/daemon/inspect.test.ts` couvre l'inspection de service approfondie incluant les détails du service Windows.
- `/Users/kevinlin/code/openclaw/src/daemon/schtasks.test.ts:24` couvre l'analyse du runtime du Planificateur de tâches Windows.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Windows doctor gateway status schtasks completion" --mode keyword --limit 5 --json`
- `gitcrawl search openclaw/openclaw --query "windows gateway schtasks scheduled task fallback startup folder" --mode keyword --limit 5 --json`

Résultats :

- La requête doctor/status a retourné la PR #74163 avec des références de problème de solution de secours obsolète du docteur Windows.
- La requête scheduled-task a retourné la PR ouverte #51486, le problème #87156 et la PR #74163 autour de l'interrogation du runtime du Planificateur de tâches et de la solution de secours obsolète du dossier Démarrage.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 4 "Windows doctor gateway status schtasks completion"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "windows gateway schtasks"`

Résultats :

- La requête doctor/status étroite n'a retourné aucun résultat direct.
- `windows gateway schtasks` a retourné une discussion de sortie du docteur Windows montrant les détails de la passerelle arrêtée/résultat de tâche, les conseils de solution de contournement du cache d'achèvement et l'analyse de la solution de secours du Planificateur de tâches.
