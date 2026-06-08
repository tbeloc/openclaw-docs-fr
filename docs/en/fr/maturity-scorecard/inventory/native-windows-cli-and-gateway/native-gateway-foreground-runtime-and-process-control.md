---
title: "Native Windows - Gateway Management Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Native Windows - Gateway Management Maturity Note

## Résumé

Native Windows peut exécuter la Gateway au premier plan et l'interroger via la même famille de commandes `openclaw gateway` que sur les autres plates-formes. La documentation indique clairement que cela suffit pour une utilisation en ligne de commande uniquement, mais les preuves archivées montrent toujours un comportement fragile lorsque les utilisateurs ferment PowerShell, s'appuient sur un comportement de redémarrage non géré, ou rencontrent des différences de processus/signaux spécifiques à Windows.

## Portée de la catégorie

Inclus dans cette catégorie :

- openclaw gateway : openclaw gateway, openclaw gateway run, openclaw gateway status, et comportement du processus au premier plan.
- Santé/disponibilité du runtime au premier plan : Santé/disponibilité du runtime au premier plan et cibles Gateway de boucle locale
- Redémarrage/signal spécifique à Windows : Redémarrage/signal spécifique à Windows et comportement de contrôle de processus
- Mode premier plan non géré : Attentes des opérateurs lors de l'exécution sans une tâche planifiée gérée.
- openclaw gateway install : openclaw gateway install, status, start, stop, restart, et comportement de démarrage géré.
- Fichiers lanceur Gateway : Fichiers gateway.cmd générés et fichiers lanceur masqués pour le démarrage géré.
- Statut du runtime de la tâche planifiée : Statut du runtime de la tâche planifiée, sélection de l'utilisateur de la tâche, secours listener/PID, et réparation de tâche.
- Secours du dossier de démarrage : Secours du dossier de démarrage lorsque le Planificateur de tâches n'est pas disponible.
- openclaw status : openclaw status, openclaw gateway status, gateway status --deep, et conseils de réparation Windows.
- Inspection du service Windows : Inspection du service Windows, analyse du runtime du Planificateur de tâches, dossier de démarrage
- Diagnostics post-installation : Comportement diagnostique, statut et réparation attendus après l'installation native de Windows.

## Fonctionnalités

- openclaw gateway : openclaw gateway, openclaw gateway run, openclaw gateway status, et comportement du processus au premier plan.
- Santé/disponibilité du runtime au premier plan : Santé/disponibilité du runtime au premier plan et cibles Gateway de boucle locale
- Redémarrage/signal spécifique à Windows : Redémarrage/signal spécifique à Windows et comportement de contrôle de processus
- Mode premier plan non géré : Attentes des opérateurs lors de l'exécution sans une tâche planifiée gérée.
- openclaw gateway install : openclaw gateway install, status, start, stop, restart, et comportement de démarrage géré.
- Fichiers lanceur Gateway : Fichiers gateway.cmd générés et fichiers lanceur masqués pour le démarrage géré.
- Statut du runtime de la tâche planifiée : Statut du runtime de la tâche planifiée, sélection de l'utilisateur de la tâche, secours listener/PID, et réparation de tâche.
- Secours du dossier de démarrage : Secours du dossier de démarrage lorsque le Planificateur de tâches n'est pas disponible.
- openclaw status : openclaw status, openclaw gateway status, gateway status --deep, et conseils de réparation Windows.
- Inspection du service Windows : Inspection du service Windows, analyse du runtime du Planificateur de tâches, dossier de démarrage
- Diagnostics post-installation : Comportement diagnostique, statut et réparation attendus après l'installation native de Windows.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (68%)`
- Signaux positifs : la documentation documente l'utilisation native en ligne de commande au premier plan uniquement ; la documentation Gateway partagée couvre les options run/status/health/restart ; la source contient les aides Gateway health/readiness, restart, process, et Windows port/PID.
- Signaux négatifs : la principale preuve en environnement réel trouvée pour Windows natif est l'infrastructure de fumée Parallels et les rapports d'archive, pas une suite de scénarios Gateway au premier plan large et actuelle.
- Lacunes d'intégration : aucune preuve native Windows en direct actuelle n'a été trouvée pour le démarrage au premier plan, le comportement de fermeture de PowerShell, le redémarrage non géré, le statut, la santé, et un tour d'agent dans un scénario reproductible.

## Score de qualité

- Score : `Alpha (62%)`
- Rapports Gitcrawl : `windows gateway` a retourné un signal de problème/PR ouvert pour la lenteur de Windows Server, la gestion de redémarrage `SIGUSR1` non supportée, la journalisation de fumée Parallels, et les problèmes de chemin/runtime.
- Rapports Discrawl : les rapports Windows natifs incluent les déconnexions de fermeture de fenêtre PowerShell, l'investigation de boucle de retry, et les commentaires selon lesquels la stabilité native de Gateway reste fragile sous certaines charges.
- Bonnes qualités : l'opération au premier plan utilise le même contrat de commande Gateway que sur les autres plates-formes, les commandes de statut sont explicites, et la source contient des aides de processus conscientes de Windows plutôt que d'assumer les signaux POSIX.
- Mauvaises qualités : la propriété du processus natif au premier plan est facile à mal interpréter pour les utilisateurs, et le comportement de signal/processus spécifique à Windows produit toujours un trafic actif de support et de PR.
- Exclu de la qualité : les preuves de test unitaire, intégration, e2e, en direct et de flux de runtime sont enregistrées uniquement sous Couverture et Preuves.

## Score de complétude

- Score : `Alpha (68%)`
- Instructions de surface : évaluées par rapport à `references/completeness/native-windows-cli-and-gateway.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour openclaw gateway, Santé/disponibilité du runtime au premier plan, Redémarrage/signal spécifique à Windows, Mode premier plan non géré, openclaw gateway install, Fichiers lanceur Gateway, Statut du runtime de la tâche planifiée, Secours du dossier de démarrage, openclaw status, Inspection du service Windows, Diagnostics post-installation.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un scénario Gateway Windows natif au premier plan reproductible couvrant le démarrage, la santé, le statut, le comportement de redémarrage, les attentes de fermeture de fenêtre PowerShell, et une simple demande d'agent ou d'interface utilisateur de contrôle.
- Clarifier dans la documentation quand `gateway run` au premier plan est censé s'arrêter avec le terminal et quand un chemin de démarrage géré est requis.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:23` documente le statut et les avertissements Windows natifs.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:45` donne le chemin CLI natif uniquement : `openclaw onboard --non-interactive --skip-health` et `openclaw gateway run`.
- `/Users/kevinlin/code/openclaw/docs/gateway/index.md:25` documente le démarrage au premier plan local et les commandes de vérification de santé.
- `/Users/kevinlin/code/openclaw/docs/cli/gateway.md:25` documente `openclaw gateway` et l'alias `gateway run`.
- `/Users/kevinlin/code/openclaw/docs/cli/gateway.md:113` documente les modes de redémarrage et le comportement de redémarrage `--safe`.

### Source

- `/Users/kevinlin/code/openclaw/src/commands/gateway-status.ts:38` implémente la commande de statut Gateway et le sondage de cible.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/restart.ts` implémente la gestion des demandes de redémarrage Gateway.
- `/Users/kevinlin/code/openclaw/src/infra/gateway-processes.ts` contient la découverte de processus Gateway et les aides de redémarrage utilisées par les chemins de service/runtime.
- `/Users/kevinlin/code/openclaw/src/infra/windows-port-pids.ts` gère la découverte de port-à-processus Windows.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/gateway.multi.e2e.test.ts` exerce le comportement du runtime multi-Gateway.
- `/Users/kevinlin/code/openclaw/test/helpers/gateway-e2e-harness.ts` fournit le harnais e2e Gateway partagé.
- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels-windows-smoke.sh:1` distribue la voie de fumée Windows Parallels.
- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels/windows-smoke.ts` contient le pilote de fumée Windows natif.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/infra/gateway-processes.test.ts` couvre le comportement de découverte de processus Gateway.
- `/Users/kevinlin/code/openclaw/src/infra/gateway-process-argv.test.ts` couvre la reconnaissance d'argv du processus Gateway.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/restart.test.ts` couvre le comportement de la méthode de redémarrage Gateway.
- `/Users/kevinlin/code/openclaw/src/commands/gateway-readiness.test.ts` couvre le comportement de la commande de disponibilité Gateway.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Windows gateway run PowerShell closes disconnected SIGUSR1" --mode keyword --limit 5 --json`
- `gitcrawl search openclaw/openclaw --query "windows gateway" --mode keyword --limit 8 --json`

Résultats :

- La requête étroite au premier plan a retourné 0 résultats.
- `windows gateway` a retourné la PR ouverte #84280 pour le redémarrage `SIGUSR1` non supporté sur Windows, le problème #72922 pour la Gateway/CLI Windows Server lente et instable, la PR #59705 pour la journalisation de fumée Windows Parallels, et les problèmes de runtime Windows connexes.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 4 "Windows gateway run PowerShell closes disconnected SIGUSR1"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "windows gateway schtasks"`

Résultats :

- La requête étroite au premier plan n'a retourné aucun résultat direct.
- `windows gateway schtasks` a retourné des discussions de support Windows sur les déconnexions de fermeture de PowerShell, les chemins de démarrage en double, les échecs de sonde `gateway/ws`, le comportement de secours du Planificateur de tâches, et le travail de stabilité Windows natif.
