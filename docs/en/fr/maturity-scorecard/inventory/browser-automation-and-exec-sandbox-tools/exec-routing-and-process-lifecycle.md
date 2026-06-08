---
title: "Browser automation and exec/sandbox tools - Tool Invocation and Execution Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Browser automation and exec/sandbox tools - Tool Invocation and Execution Maturity Note

## Résumé

Le routage exec et le cycle de vie des processus sont Stables. La surface dispose d'une documentation complète, d'une centralisation des sources, d'un comportement détaillé des délais d'attente/sorties, d'une gestion PTY et stdin, d'un suivi des processus en arrière-plan, d'actions de suivi des processus et d'un routage d'hôte entre auto, sandbox, gateway et node. Les risques restants proviennent de la survivabilité des commandes longue durée, de l'état des processus en arrière-plan après redémarrage/compaction, et de la complexité inhérente du routage de l'exécution shell sur plusieurs hôtes.

## Portée de la catégorie

Inclus dans cette catégorie :

- Exec Routing : Couvre le routage Exec sur l'exécution `exec` au premier plan et en arrière-plan, `yieldMs`, délais d'attente, PTY et le comportement associé du routage exec et du cycle de vie des processus.
- Process Lifecycle : Couvre le cycle de vie des processus sur l'exécution `exec` au premier plan et en arrière-plan, `yieldMs`, délais d'attente, PTY et le comportement associé du routage exec et du cycle de vie des processus.
- Direct Tool Invoke API : Couvre l'API Direct Tool Invoke sur HTTP `POST /tools/invoke`, Gateway RPC `tools.invoke`, sémantique du corps de la requête et de l'authentification, restauration de la portée de l'opérateur à secret partagé, et le comportement associé de l'API d'invocation d'outil direct et du système node system.run.
- Node System.run : Couvre Node System.run sur HTTP `POST /tools/invoke`, Gateway RPC `tools.invoke`, sémantique du corps de la requête et de l'authentification, restauration de la portée de l'opérateur à secret partagé, et le comportement associé de l'API d'invocation d'outil direct et du système node system.run.
- Host Exec Approvals : Couvre les approbations Host Exec sur la politique d'approbation exec, l'état des approbations locales, l'enregistrement et l'attente des demandes d'approbation, la consommation allow-once, et le comportement associé des approbations host exec et du mode élevé.
- Elevated Mode : Couvre le mode élevé sur la politique d'approbation exec, l'état des approbations locales, l'enregistrement et l'attente des demandes d'approbation, la consommation allow-once, et le comportement associé des approbations host exec et du mode élevé.

## Fonctionnalités

- Exec Routing : Couvre le routage Exec sur l'exécution `exec` au premier plan et en arrière-plan, `yieldMs`, délais d'attente, PTY et le comportement associé du routage exec et du cycle de vie des processus.
- Process Lifecycle : Couvre le cycle de vie des processus sur l'exécution `exec` au premier plan et en arrière-plan, `yieldMs`, délais d'attente, PTY et le comportement associé du routage exec et du cycle de vie des processus.
- Direct Tool Invoke API : Couvre l'API Direct Tool Invoke sur HTTP `POST /tools/invoke`, Gateway RPC `tools.invoke`, sémantique du corps de la requête et de l'authentification, restauration de la portée de l'opérateur à secret partagé, et le comportement associé de l'API d'invocation d'outil direct et du système node system.run.
- Node System.run : Couvre Node System.run sur HTTP `POST /tools/invoke`, Gateway RPC `tools.invoke`, sémantique du corps de la requête et de l'authentification, restauration de la portée de l'opérateur à secret partagé, et le comportement associé de l'API d'invocation d'outil direct et du système node system.run.
- Host Exec Approvals : Couvre les approbations Host Exec sur la politique d'approbation exec, l'état des approbations locales, l'enregistrement et l'attente des demandes d'approbation, la consommation allow-once, et le comportement associé des approbations host exec et du mode élevé.
- Elevated Mode : Couvre le mode élevé sur la politique d'approbation exec, l'état des approbations locales, l'enregistrement et l'attente des demandes d'approbation, la consommation allow-once, et le comportement associé des approbations host exec et du mode élevé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (88%)`
- Signaux positifs :
  - La documentation Exec couvre le routage d'hôte, le repli sandbox, le routage node, le comportement PATH, les approbations, les remplacements de session et le suivi des processus en arrière-plan.
  - La source centralise la résolution des cibles, l'assainissement env/path, le cycle de vie des processus, l'agrégation des sorties, l'enregistrement en arrière-plan et la classification des défaillances.
  - Les tests couvrent la résolution des cibles, PTY, les abandons en arrière-plan, les conseils de délai d'attente, le routage d'hôte node/gateway/sandbox, le comportement path, la vérification préalable des scripts et le routage des événements de processus.
  - Les preuves d'exécution incluent la documentation des processus en arrière-plan Gateway et les diagnostics source émis à la fin de l'exécution exec.
- Signaux négatifs :
  - Les problèmes d'archive persistent autour de la mise en arrière-plan finie, des arbres de processus orphelins, de la fuite de charge utile et du relancement répété au lieu du sondage `process`.
  - La même commande peut se comporter différemment selon l'hôte cible, la disponibilité du sandbox, le mode PTY et l'état des approbations.
- Lacunes d'intégration :
  - Ajouter une matrice de survivabilité des processus de redémarrage/compaction pour l'exec en arrière-plan.
  - Ajouter une voie exec inter-hôte qui exécute la même commande sur sandbox, gateway et node avec routage explicite et vérifie l'état de suivi du processus.

## Score de qualité

- Score : `Stable (84%)`
- Rapports Gitcrawl :
  - `exec process background` a retourné le problème #82178 sur la mise en arrière-plan finie, le problème #65983 sur les arbres de processus orphelins après redémarrage/perte de session, PR #59719 suivi de la vivacité exec en arrière-plan avec les tâches CLI, le problème #70797 sur la fuite de charge utile, et le problème #62432 sur le relancement exec au lieu du sondage process.
  - `exec process background pty timeout host auto` a retourné le problème #75811 sur les champs de schéma `security`/`elevated`/`ask` contrôlables par le modèle.
- Rapports Discrawl :
  - `exec process background` a retourné les conseils du 2026-05-17 selon lesquels `exec` démarre le travail et `process` le suit/sonde ; le délai d'attente cron est la barrière de sécurité externe, pas la supervision des processus.
- Bonnes qualités :
  - La résolution de cible `exec` est explicite et échoue fermée lorsqu'un remplacement d'hôte demandé n'est pas autorisé.
  - La gestion env et PATH d'hôte est centralisée, avec les variables env héritées dangereuses bloquées pour l'exécution d'hôte.
  - Le suivi des processus expose list/poll/log/write/send-keys/submit/paste/kill/clear/remove et signale l'état d'attente d'entrée.
  - Les messages d'erreur dirigent le travail longue durée vers l'exec en arrière-plan enregistré au lieu de la mise en arrière-plan shell avec `&`.
- Mauvaises qualités :
  - Le suivi des processus en arrière-plan a toujours des cas limites de fiabilité et d'UX réels après redémarrage, compaction et nouvelles tentatives du fournisseur.
  - `exec` reste une surface shell ; même avec un outillage de processus fort, l'intention de l'utilisateur et les effets secondaires des commandes sont difficiles à modéliser.
  - Le routage sur sandbox/gateway/node est puissant mais augmente la charge cognitive pour les opérateurs et les agents.
- Exclu de la qualité :
  - Les preuves de test unitaire, intégration, e2e, live et runtime-flow affectées couverture uniquement.

## Score de complétude

- Score : `Stable (88%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-automation-and-exec-sandbox-tools.md`.
- Signaux positifs : les preuves archivées docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Exec Routing, Process Lifecycle, Direct Tool Invoke API, Node System.run, Host Exec Approvals, Elevated Mode.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'état du processus en arrière-plan devrait devenir plus durable sur les redémarrages Gateway et la perte de session.
- Les conseils de suivi des processus devraient être constamment visibles pour tous les harnais de fournisseur afin d'éviter les boucles de relancement.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/tools/exec.md:9` : exec est documenté comme une surface shell mutante avec support des processus.
- `/Users/kevinlin/code/openclaw/docs/tools/exec.md:44` : les docs couvrent les paramètres `host=auto`, sandbox, gateway, node, ask et elevated.
- `/Users/kevinlin/code/openclaw/docs/tools/exec.md:68` : les docs décrivent le comportement du routage d'hôte et le comportement fail-closed pour sandbox/node.
- `/Users/kevinlin/code/openclaw/docs/tools/exec.md:130` : les docs décrivent la gestion de PATH sur host, sandbox et node.
- `/Users/kevinlin/code/openclaw/docs/gateway/background-process.md:13` : les docs de processus en arrière-plan définissent les paramètres et le comportement d'exec.
- `/Users/kevinlin/code/openclaw/docs/gateway/background-process.md:59` : les docs de processus en arrière-plan énumèrent les actions de processus.

## Source

- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec.ts:71` : les résultats au premier plan contiennent le statut, le code de sortie, la durée, la sortie, le timeout et les détails du répertoire courant.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-runtime.ts:78` : l'assainissement de l'environnement de base d'hôte supprime les variables héritées dangereuses.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-runtime.ts:117` : les constantes de sortie par défaut, sortie en attente et timeout d'approbation sont centralisées.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-runtime.ts:186` : la fin d'exec émet des événements de diagnostic avec la cible, le mode, la durée, le résultat et les métadonnées d'échec.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-runtime.ts:241` : la résolution de cible d'hôte contrôle les remplacements de cible demandés et mappe auto à sandbox ou gateway.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-runtime.ts:504` : les conseils de timeout/échec pointent vers le travail de longue durée sur exec en arrière-plan enregistré et l'interrogation de processus.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.process.ts:176` : l'outil de processus expose list/poll/log/write/send-keys/submit/paste/kill/clear/remove.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.process.ts:193` : le runtime de processus rapporte la capacité d'écriture stdin, l'état en attente d'entrée, le temps d'inactivité et l'heure de la dernière sortie.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.process.ts:223` : la suppression de processus revient à la terminaison de l'arborescence des processus.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-gateway-approval.e2e.test.ts:1` : la couverture e2e existe pour l'exécution d'approbation exec Gateway.
- `/Users/kevinlin/code/openclaw/src/agents/sessions/exec.test.ts:1` : la couverture exec au niveau de la session existe.
- `/Users/kevinlin/code/openclaw/src/agents/sessions/bash-executor.test.ts:1` : la couverture de session bash executor existe.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-runtime.test.ts:110` : vérifie la résolution de cible exec.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-runtime.test.ts:177` : vérifie le rejet du remplacement gateway/node tandis que sandbox est actif.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-runtime.test.ts:383` : vérifie la suppression de notify-on-exit et le comportement du timeout pour exec en arrière-plan.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-runtime.test.ts:611` : vérifie les conseils de timeout et la classification des échecs.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec.pty.test.ts:87` : le comportement PTY est couvert.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec.background-abort.test.ts:1` : le comportement d'abandon en arrière-plan est couvert.

## Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "exec process background" --json`

Résultats :

- Problème ouvert #82178 : backgrounding exec fini quand le processus est caché.
- Problème ouvert #65983 : exec PTY en arrière-plan peut survivre au redémarrage/perte de session et devenir non suivi.
- PR ouvert #59719 : suivi de la vivacité d'exec en arrière-plan avec les tâches CLI.
- Problème ouvert #70797 : fuite de charge utile d'appel d'outil lors des flux exec/processus en arrière-plan.
- Problème ouvert #62432 : les sessions peuvent relancer exec après « Commande toujours en cours d'exécution » au lieu de basculer vers l'interrogation de processus.

## Requêtes Discrawl

Requête :

`discrawl search --mode fts --limit 5 "exec process background"`

Résultats :

- Archive du 2026-05-17 : les conseils distinguent `exec` comme le démarreur de commande et `process` comme le handle de suivi/interrogation ; il recommande exec en arrière-plan/traçable avec interrogation de processus pour le travail de longue durée.
