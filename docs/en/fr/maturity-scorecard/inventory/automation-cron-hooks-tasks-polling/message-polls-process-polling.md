---
title: "Automatisation : cron, hooks, tâches, polling - Note de Maturité des Contrôles de Polling"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automatisation : cron, hooks, tâches, polling - Note de Maturité des Contrôles de Polling

## Résumé

Ce composant couvre deux significations visibles par l'utilisateur du polling : la création de sondages de canal via l'outil de message/CLI, et le polling de processus pour les commandes longues. Les actions de sondage de message sont prises en charge pour plusieurs canaux, tandis que le polling de processus dispose de garde-fous pour les attentes longues et les boucles sans progression répétées. La qualité est limitée par les rapports d'archive autour des boucles de polling infinies/répétées et les opérateurs devant choisir le bon modèle `exec`/`process` pour les travaux longs.

## Portée de la Catégorie

Inclus dans cette catégorie :

- openclaw message poll : Couvre openclaw message poll sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- Sondages Telegram : Couvre les sondages Telegram sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- Sondages Teams : Couvre les sondages Teams sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- Drapeaux de sondage : Couvre les drapeaux de sondage sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- Portes de capacité de canal : Couvre les portes de capacité de canal sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- process poll : Couvre process poll sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- process log : Couvre process log sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- Statut du processus en arrière-plan : Couvre le statut du processus en arrière-plan sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- Détection de boucle sans progression : Couvre la détection de boucle sans progression sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- Contrôles d'entrée de processus : Couvre les contrôles d'entrée de processus sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.

## Fonctionnalités

- openclaw message poll : Couvre openclaw message poll sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- Sondages Telegram : Couvre les sondages Telegram sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- Sondages Teams : Couvre les sondages Teams sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- Drapeaux de sondage : Couvre les drapeaux de sondage sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- Portes de capacité de canal : Couvre les portes de capacité de canal sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- process poll : Couvre process poll sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- process log : Couvre process log sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- Statut du processus en arrière-plan : Couvre le statut du processus en arrière-plan sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- Détection de boucle sans progression : Couvre la détection de boucle sans progression sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.
- Contrôles d'entrée de processus : Couvre les contrôles d'entrée de processus sur `openclaw message poll`, adaptateurs de sondage de canal, normalisation des paramètres de sondage, support des sondages Teams/Matrix/Telegram, et comportement de sondage de message et polling de processus associés.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (74%)`
- Signaux positifs : L'analyse des paramètres de sondage, l'enregistrement des commandes de sondage de message, les actions de sondage sortantes, les adaptateurs de sondage spécifiques au canal, le polling de processus, le backoff de sondage de commande, et la détection de boucle de polling ont des tests ciblés.
- Signaux négatifs : Le support des sondages de canal est fragmenté par les capacités du canal, et le comportement du polling de processus dépend du timing réel du processus enfant, de l'état du terminal/PTY, et de l'invite de l'agent.
- Lacunes d'intégration : Ajouter un e2e qui démarre un processus long, le sonde avec des cas de progression et sans progression, puis envoie un sondage de canal via un adaptateur compatible en direct et vérifie le message/ID de sondage retourné.

## Score de Qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : Le problème #62432 signale que les agents relancent répétitivement exec au lieu de passer au polling de processus ; la PR #81157 corrige l'action `process.action` invalide causant des boucles de retry infinies ; le problème #65223 discute de l'abandon des boucles de polling de processus tout en gardant l'exec sous-jacent actif ; le problème #69582 signale l'injection de paramètres causant une boucle d'outil infinie.
- Rapports Discrawl : La discussion du 17 mai sur cron dit que le travail cron déterministe long devrait utiliser `exec` OpenClaw plus le polling de `process` plutôt que la garde de shell native Codex. Le rapport Clawsweeper mentionne un blocage de sondage fermé rapidement comme un problème notable.
- Bonnes qualités : L'outil de processus a des actions `poll` explicites, un serrage du timeout, un état de backoff, une détection de boucle sans progression, et une orientation du système-prompt contre le polling occupé. Les actions de sondage de message passent par des portes de capacité de canal.
- Mauvaises qualités : La surface reste facile à mal utiliser pour les agents : relancement répétitif d'exec, boucles d'action de processus malformées, et sondages sans progression apparaissent tous dans les rapports d'archive.
- Exclu de la qualité : L'inventaire des tests et la profondeur de la preuve d'exécution ; ils sont uniquement des entrées de couverture.

## Score de Complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/automation-cron-hooks-tasks-polling.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour openclaw message poll, sondages Telegram, sondages Teams, drapeaux de sondage, portes de capacité de canal, process poll, process log, statut du processus en arrière-plan, détection de boucle sans progression, contrôles d'entrée de processus.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Les conseils aux agents devraient dire plus directement quand passer de `exec` à `process poll` et quand arrêter le polling.
- La documentation des sondages de canal devrait rendre les différences de support/capacité plus découvrables à partir de l'index d'automatisation.
- La détection de boucle devrait continuer à bloquer les modèles de polling malformés ou sans progression avant qu'ils ne consomment le runtime.

## Preuves

### Docs

- `docs/automation/poll.md` redirige vers `docs/cli/message.md` pour la documentation du polling.
- `docs/cli/message.md` documente l'utilisation du polling de message.
- `docs/channels/telegram.md` documente l'utilisation de `openclaw message poll` Telegram et les drapeaux de sondage spécifiques à Telegram.
- `docs/channels/msteams.md` documente les sondages Teams en tant que cartes adaptatives.
- `docs/gateway/background-process.md` documente le polling/logging de processus pour les processus en arrière-plan.

### Source

- `src/polls.ts`, `src/poll-params.ts`, `src/cli/program/message/register.poll.ts`, et `src/infra/outbound/message-action-runner.poll.test.ts` couvrent les données de sondage de message et l'exécution des actions.
- `src/agents/bash-tools.process.ts`, `src/agents/command-poll-backoff.ts`, et `src/agents/tool-loop-detection.ts` implémentent le polling de processus et le comportement anti-boucle.
- `extensions/msteams/src/polls.ts`, `extensions/matrix/src/matrix/actions/polls.ts`, et le support des actions de canal Telegram implémentent le comportement de sondage spécifique au canal.

### Tests d'intégration

- `src/agents/agent-tools.before-tool-call.e2e.test.ts` inclut le comportement de boucle de sondage via l'exécution d'outil d'agent.
- `src/infra/outbound/message-action-runner.poll.test.ts` exerce l'exécution des actions de sondage sortantes.
- Les tests de sondage de canal sont principalement au niveau de l'adaptateur plutôt que e2e de canal en direct.

### Tests unitaires

- `src/polls.test.ts` et `src/poll-params.test.ts` couvrent les primitives de sondage.
- `src/agents/bash-tools.process.poll-timeout.test.ts`, `src/agents/command-poll-backoff.test.ts`, et `src/agents/tool-loop-detection.test.ts` couvrent le polling de processus et la détection de boucle.
- `extensions/msteams/src/polls.test.ts`, `extensions/matrix/src/matrix/actions/polls.test.ts`, et `extensions/matrix/src/matrix/poll-types.test.ts` couvrent les adaptateurs de sondage de canal.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "message poll process poll polling loop no progress" --json --limit 5`

Résultats :

- Aucun résultat pour la requête exacte.

Requête de secours :

`gitcrawl search openclaw/openclaw --query "poll loop" --json --limit 5`

Résultats :

- Le problème #65223 discute de la gestion du signal d'abandon du polling de processus.
- La PR #81157 corrige l'action `process.action` invalide à la limite d'invocation d'outil pour prévenir les boucles infinies.
- Le problème #62432 signale le relancement répétitif d'exec au lieu de passer au polling de processus.
- Le problème #69582 signale l'injection de paramètres causant une boucle d'invocation d'outil infinie.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "poll loop"`

Résultats :

- Le rapport Clawsweeper appelle le problème #86477 comme un blocage de sondage fermé rapidement.
- Le fil de discussion du 17 mai sur cron recommande `exec` plus le polling de `process` pour le travail déterministe long et avertit contre Codex possédant la boucle de shell.
