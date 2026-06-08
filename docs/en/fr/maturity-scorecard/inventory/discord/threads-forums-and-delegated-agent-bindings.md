---
title: "Discord - Threads, Forums, and Delegated-agent Bindings Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Discord - Threads, Forums, and Delegated-agent Bindings Maturity Note

## Résumé

Discord dispose d'une large surface de threads documentée : posts parents forum/média, actions explicites de création/liste/réponse de threads, routage auto-thread, contexte parent/starter de thread, sessions de sous-agent liées aux threads, et liaisons ACP current/thread. L'implémentation est substantielle et généralement bien factorisée, avec analyse explicite des cibles, mise en forme des requêtes forum/média, enregistrements de liaison persistants, livraison de persona webhook, balayeurs idle/max-age, réconciliation de santé ACP, et intégration de hook de canal.

Le score est limité par la forme de preuve. Une couverture intégration/runtime existe pour la liaison current-conversation, le routage d'action, le suivi générique de thread, les hooks de cycle de vie du sous-agent, et les sondes ACP live/manuelles, mais l'audit n'a pas trouvé un seul scénario Discord live toujours actif qui exerce la création de thread forum/média plus le suivi délégué ACP/sous-agent de bout en bout. La qualité est également réduite par un dossier de bugs vécu dense autour de la liaison de thread ACP Discord, le routage de suivi, les cibles préfixées, la clé de canal parent, et la confusion de l'opérateur entre `--bind here` et `--thread auto|here`.

## Portée de la catégorie

- Posts de canal forum/média Discord créés en tant que threads à partir de cibles de canal parent.
- Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`.
- Analyse de cible Discord pour `channel:<id>`, cibles utilisateur, et IDs nus avec un canal par défaut.
- Résolution du contexte de thread : recherche de canal parent, recherche de message starter, comportement starter forum/média, ciblage de réponse, assainissement de titre, titres générés optionnels, et héritage de session/modèle parent.
- Routage de session lié aux threads pour `/focus`, `/unfocus`, `/agents`, `/session idle`, `/session max-age`, `sessions_spawn({ thread: true })`, et cibles de livraison du sous-agent.
- Liaisons ACP current-conversation et spawns ACP thread sur Discord, y compris les liaisons ACP configurées persistantes.
- Comportement du cycle de vie de liaison : persistance de liaison, livraison webhook, touches d'activité, expiration idle/max-age, nettoyage de thread stale/supprimé, et réconciliation de démarrage ACP.

## Fonctionnalités

- Posts de thread de canal forum et média : Couvre les posts de thread de canal forum et média sur les posts de canal forum/média Discord créés en tant que threads à partir de cibles de canal parent. Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles utilisateur, et comportement associé des threads, forums, et liaisons d'agent délégué.
- Actions de thread : Couvre les actions de thread sur les posts de canal forum/média Discord créés en tant que threads à partir de cibles de canal parent. Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles utilisateur, et comportement associé des threads, forums, et liaisons d'agent délégué.
- Analyse de cible : Couvre l'analyse de cible sur les posts de canal forum/média Discord créés en tant que threads à partir de cibles de canal parent. Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles utilisateur, et comportement associé des threads, forums, et liaisons d'agent délégué.
- Résolution du contexte de thread : Couvre la résolution du contexte de thread sur les posts de canal forum/média Discord créés en tant que threads à partir de cibles de canal parent. Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles utilisateur, et comportement associé des threads, forums, et liaisons d'agent délégué.
- Routage de session lié aux threads : Couvre le routage de session lié aux threads sur les posts de canal forum/média Discord créés en tant que threads à partir de cibles de canal parent. Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles utilisateur, et comportement associé des threads, forums, et liaisons d'agent délégué.
- Liaisons ACP : Couvre les liaisons ACP sur les posts de canal forum/média Discord créés en tant que threads à partir de cibles de canal parent. Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles utilisateur, et comportement associé des threads, forums, et liaisons d'agent délégué.
- Cycle de vie de liaison : Couvre le cycle de vie de liaison sur les posts de canal forum/média Discord créés en tant que threads à partir de cibles de canal parent. Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles utilisateur, et comportement associé des threads, forums, et liaisons d'agent délégué.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : La liaison ACP current-conversation Discord a un test d'intégration qui lie une conversation Discord DM et vérifie que le prochain tour route vers la clé de session ACP liée. Les tests runtime couvrent la création de thread message-tool, les messages initiaux du forum, le routage d'action, la liaison de hook du sous-agent, le routage de préflight de thread lié, la suppression d'écho webhook, le cycle de vie de liaison idle/max-age, et le comportement de cycle de vie générique `sessions_spawn`. Les artefacts QA incluent un scénario de suivi de thread générique et un smoke ACP Discord manuel qui envoie une invite Discord, attend une liaison de thread ACP, et vérifie un ACK dans le thread lié.
- Signaux négatifs : La plupart des preuves de thread/forum Discord sont des couvertures REST moquées ou action-runtime, pas l'exécution live de forum/média Discord. Le test de liaison ACP live toujours actif est générique et synthétique plutôt que spécifique à Discord forum/thread. La couverture du sous-agent délégué et du thread ACP est divisée entre les tests de spawn génériques, les tests de hook Discord, et l'outillage de smoke manuel au lieu d'une exécution Discord live canonique.
- Lacunes d'intégration : Aucun scénario CI-live observé ne prouve la création de thread forum/média, les tags appliqués, le spawn ACP/sous-agent délégué, le routage de suivi, et le nettoyage dans un flux de serveur Discord. Aucune preuve de flux runtime large n'a été trouvée pour les liaisons ACP configurées persistantes sur le redémarrage de la passerelle Discord plus l'héritage de thread.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : L'archive montre plusieurs rapports ouverts ou récents directement dans cette zone de composant, y compris #64199 pour les liaisons configurées ACP partageant une clé de session de canal parent sur les threads Discord, #81341 pour la livraison de suivi de thread lié ACP, #87599 pour la restauration de session ACP après le nettoyage des métadonnées, #53548 pour `mode="session"` étant couplé à la liaison de thread, et #79281 pour la complexité de la plomberie de liaison de thread de canal tiers. Il montre également des régressions récentes mais corrigées autour des IDs de canal Discord préfixés et des défaillances de liaison de thread de session (#63927, #70315, #68034).
- Rapports Discrawl : Les résultats de l'archive Discord incluent des discussions d'opérateur où `/acp spawn ... --bind here` a réussi mais les messages de thread Discord de suivi ou les commandes `/acp` natives n'ont pas atteint la session liée, plus des conseils répétés selon lesquels les sessions ACP Discord persistantes nécessitent un chemin lié aux threads et que les canaux forum/média doivent être traités comme des posts de thread.
- Bonnes qualités : L'implémentation a une normalisation explicite de cible Discord, des corps de requête spécifiques au forum/média, un comportement de secours sûr lorsque la création de thread ou la livraison de message initial échoue partiellement, la résolution du starter et du parent de thread, l'expiration du cycle de vie de liaison, le nettoyage de thread stale, la suppression d'écho webhook, la réconciliation de santé ACP de démarrage avec concurrence bornée, et une documentation d'opérateur claire pour `--bind here`, `--thread auto|here`, `spawnSessions`, et les limitations forum/média.
- Mauvaises qualités : Le composant a une complexité d'état et de routage élevée, avec des liaisons current-conversation séparées, des liaisons de thread, des liaisons ACP configurées de haut niveau, des hooks de cycle de vie du sous-agent, et des chemins de commande natifs Discord. Le dossier de bugs vécu montre que de petites incompatibilités dans les IDs de conversation, les IDs parent/thread, la sélection de compte, ou le contexte de commande natif peuvent casser le routage tout en semblant réussis aux opérateurs.
- Exclu de la qualité : La couverture de test, le manque de tests, et la profondeur d'intégration n'ont pas été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/discord.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl, et Discrawl couvrent la portée de taxonomie pour les posts de thread de canal forum et média, les actions de thread, l'analyse de cible, la résolution du contexte de thread, le routage de session lié aux threads, les liaisons ACP, le cycle de vie de liaison.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du dossier de lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Discord a une documentation solide pour la création de thread forum/média, mais l'archive montre toujours une confusion utilisateur autour des parents du forum, `--message-id`, et si un flux de travail poste sur un canal parent ou un thread.
- Le routage de thread ACP et sous-agent est implémenté via plusieurs contrats adjacents. La source est robuste par endroits, mais le modèle d'opérateur reste subtil : les liaisons actuelles, les spawns de thread enfant, les liaisons ACP configurées, et les liaisons de thread temporaires peuvent se chevaucher.
- Le smoke ACP Discord manuel existant est précieux, mais le composant serait plus facile à exploiter si sa preuve runtime canonique vivait dans la même matrice QA/lab que les scénarios de transport Discord de base.
- Les éléments d'archive ouverts autour de la livraison de suivi de thread lié et de la clé de session de canal parent doivent être traités comme un risque de qualité actif jusqu'à ce qu'ils soient fermés ou explicitement remplacés par une preuve source.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:318` documente les canaux forum/média en tant que parents thread-only, deux chemins de création supportés, et la syntaxe `openclaw message thread create`.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:748` documente le routage des threads Discord en tant que sessions de canal, l'héritage de la configuration du canal parent, le fallback du modèle parent, et l'héritage optionnel des transcriptions.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:760` documente les sessions liées aux threads pour les sous-agents, incluant `/focus`, `/unfocus`, `/agents`, `/session idle`, `/session max-age`, `spawnSessions`, et `defaultSpawnContext`.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:809` documente les liaisons de canal ACP persistantes pour Discord et indique que `/acp spawn codex --bind here` lie le canal/thread actuel tandis que `spawnSessions` contrôle la création de threads enfants via `--thread auto|here`.
- `/Users/kevinlin/code/openclaw/docs/tools/acp-agents.md:267` documente les liaisons ACP de conversation actuelle et le routage des suites, tandis que `/Users/kevinlin/code/openclaw/docs/tools/acp-agents.md:286` sépare `--bind here` de `--thread ...` et clarifie Discord `spawnSessions`.
- `/Users/kevinlin/code/openclaw/docs/tools/subagents.md:294` nomme les clés de configuration de liaison de thread Discord pour les sessions de sous-agent liées aux threads.

## Source

- `/Users/kevinlin/code/openclaw/extensions/discord/src/target-parsing.ts:16` analyse les cibles Discord et `/Users/kevinlin/code/openclaw/extensions/discord/src/target-parsing.ts:67` résout les cibles de canal avec `defaultKind: "channel"`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.messages.ts:136` implémente `createThreadDiscord`; `/Users/kevinlin/code/openclaw/extensions/discord/src/send.messages.ts:160` détecte les parents forum/média, `/Users/kevinlin/code/openclaw/extensions/discord/src/send.messages.ts:166` transmet `applied_tags`, et `/Users/kevinlin/code/openclaw/extensions/discord/src/send.messages.ts:179` envoie le contenu initial séparément pour les threads non-forum.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/threading.starter.ts:44` résout les canaux de thread Discord, `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/threading.starter.ts:84` résout les informations parent, et `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/threading.starter.ts:150` utilise l'ID du thread lui-même pour la recherche du starter forum/média.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/threading.auto-thread.ts:38` construit le contexte de session auto-thread, `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/threading.auto-thread.ts:71` enregistre la liaison modèle/session parent, et `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/threading.auto-thread.ts:123` crée des auto-threads quand configuré.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/thread-bindings.manager.ts:298` lie les cibles, crée ou réutilise les webhooks, persiste les enregistrements, et enregistre un adaptateur de liaison de session à `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/thread-bindings.manager.ts:528`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/thread-bindings.lifecycle.ts:101` lie automatiquement les sous-agents Discord générés et `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/thread-bindings.lifecycle.ts:236` réconcilie les liaisons de thread ACP au démarrage avec un plafond de concurrence de sonde de santé borné à `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/thread-bindings.lifecycle.ts:52`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/subagent-hooks.ts:93` gère la génération de sous-agents Discord, vérifie la politique de génération de liaison de thread à `/Users/kevinlin/code/openclaw/extensions/discord/src/subagent-hooks.ts:108`, et retourne une origine de livraison de thread Discord à `/Users/kevinlin/code/openclaw/extensions/discord/src/subagent-hooks.ts:156`.
- `/Users/kevinlin/code/openclaw/src/agents/subagent-spawn.ts:638` exige le succès du hook de liaison de thread pour les générations de session liées aux threads et `/Users/kevinlin/code/openclaw/src/agents/acp-spawn.ts:1338` mappe les échecs de liaison préparés à `thread_binding_invalid`.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/acp-bind-here.integration.test.ts:133` couvre le flux Discord ACP bind-here et `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/acp-bind-here.integration.test.ts:213` affirme que le prochain tour Discord route vers la session ACP liée et l'agent.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.test.ts:1299` vérifie que la création de thread du runtime d'action porte le corps du post forum initial dans l'action Discord.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.test.ts:799` vérifie que les messages de bot réguliers liés aux threads peuvent circuler quand autorisés, et `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.test.ts:996` vérifie que le contrôle de mention est contourné pour les threads liés.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-acp-bind.live.test.ts:563` définit un scénario de liaison ACP en direct, `/Users/kevinlin/code/openclaw/src/gateway/gateway-acp-bind.live.test.ts:730` affirme l'annonce de liaison, et `/Users/kevinlin/code/openclaw/src/gateway/gateway-acp-bind.live.test.ts:912` vérifie la continuité de transcription de session liée. Ceci est générique/synthétique, non spécifique aux forums Discord.
- `/Users/kevinlin/code/openclaw/qa/scenarios/channels/thread-follow-up.md:4` définit un scénario QA de suivi de thread, `/Users/kevinlin/code/openclaw/qa/scenarios/channels/thread-follow-up.md:40` crée un thread, et `/Users/kevinlin/code/openclaw/qa/scenarios/channels/thread-follow-up.md:72` affirme que la réponse n'a pas fui vers le canal racine.
- `/Users/kevinlin/code/openclaw/scripts/dev/discord-acp-plain-language-smoke.ts:245` décrit un smoke Discord ACP en direct manuel; `/Users/kevinlin/code/openclaw/scripts/dev/discord-acp-plain-language-smoke.ts:846` attend une nouvelle liaison de thread ACP et `/Users/kevinlin/code/openclaw/scripts/dev/discord-acp-plain-language-smoke.ts:925` signale un échec si le thread lié ne reçoit pas le jeton ACK attendu.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.creates-thread.test.ts:144` couvre la création de thread forum avec un message initial, `/Users/kevinlin/code/openclaw/extensions/discord/src/send.creates-thread.test.ts:157` couvre la création de thread média, et `/Users/kevinlin/code/openclaw/extensions/discord/src/send.creates-thread.test.ts:173` couvre `applied_tags`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/threading.auto-thread.test.ts:162` couvre le comportement du titre auto-thread généré et `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/thread-title.generate.test.ts:95` couvre les appels de modèle de génération de titre.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/subagent-hooks.test.ts:210` couvre le routage de liaison de thread sur `subagent_spawning`, `/Users/kevinlin/code/openclaw/extensions/discord/src/subagent-hooks.test.ts:249` couvre les erreurs de génération de sous-agent lié aux threads désactivés, et `/Users/kevinlin/code/openclaw/extensions/discord/src/subagent-hooks.test.ts:426` résout les cibles de livraison à partir des threads liés correspondants.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/thread-bindings.lifecycle.test.ts:294` couvre le texte d'introduction inactif/max-age et le comportement du cycle de vie, incluant l'auto-unfocus et le nettoyage des threads obsolètes/supprimés dans les cas adjacents.
- `/Users/kevinlin/code/openclaw/src/cli/program/message/register.thread.test.ts:120` vérifie que la CLI `message thread create` distribue `thread-create`, tandis que `/Users/kevinlin/code/openclaw/extensions/discord/src/channel-actions.test.ts:71` vérifie que Discord annonce `thread-create`, `thread-list`, et `thread-reply`.

## Requêtes Gitcrawl

Requête :

```text
gitcrawl doctor --json
```

Résultats :

- Succès ; fraîcheur enregistrée : version=0.2.1, last_sync_at=2026-05-28T19:09:52.784704Z, thread_count=29810, open_thread_count=11181, cluster_count=18594, repository_count=2.

Requête :

```text
gitcrawl search --query "discord thread binding" openclaw/openclaw --json
```

Résultats :

- Retourné le problème ouvert #64199, "ACP configured binding uses parent channel ID for session key — all threads under same channel share one persistent Claude Code process."
- Retourné la PR ouverte #64322, "fix(acp): assign distinct session keys to Discord threads under the same parent channel."
- Retourné le problème ouvert #53548, "Decouple mode=\"session\" from thread binding requirement."
- Retourné le problème ouvert #50798, "Visible agent-to-agent messaging for ACP thread-bound sessions."
- Retourné la PR ouverte #81341, "Fix ACP bound thread follow-up delivery."

Requête :

```text
gitcrawl search --query "discord acp sessions_spawn thread binding" openclaw/openclaw --json
```

Résultats :

- Retourné le problème ouvert #64199 et le problème ouvert #87599 en tant que risques actifs Discord/ACP/thread-binding.
- Retourné le problème ouvert #79281, "Default ACP thread-binding preset ... third-party channels currently re-implement ~870 LOC each."
- Retourné le problème ouvert #53548, renforçant l'ambiguïté opérateur/API autour de `mode="session"` et de la liaison de thread.

Requête :

```text
gitcrawl search --query "Discord forum media thread create" openclaw/openclaw --json
```

Résultats :

- Aucun résultat. Étant donné la vérification de fraîcheur réussie, l'absence est traitée comme neutre pour la Qualité, non comme preuve positive.

Requête :

```text
gitcrawl search --query "Discord bound thread follow-up delivery" openclaw/openclaw --json
```

Résultats :

- Retourné la PR ouverte #81341, "Fix ACP bound thread follow-up delivery."
- Retourné la PR ouverte #80008, "feat(plugins): expose ACP spawn and prompt in plugin runtime," avec un extrait sur la livraison des réponses d'agent dans un thread Discord lié.

## Requêtes Discrawl

Requête :

```text
discrawl status --json
```

Résultats :

- Succès ; fraîcheur enregistrée : generated_at=2026-05-28T20:13:14Z, state=current, last_sync_at=2026-05-28T19:15:50Z, messages=1485267, channels=25766, threads=25539, members=173089, embedding_backlog=0, partage distant `git@github.com-personal:openclaw/discord-store.git`.

Requête :

```text
discrawl search --mode hybrid --limit 10 "Discord thread binding ACP spawn"
```

Résultats :

- Retourné les conseils du responsable du 2026-05-13 indiquant que la liaison native du serveur d'application Codex et la liaison ACP existent, mais l'attachement d'une session Discord/chat à une session CLI Codex appairée déjà en cours d'exécution arbitraire n'est pas un flux de travail documenté.
- Retourné les entrées du miroir de problème OpenClaw pour #65801, #63927, #63354, et #55569, chacune liée aux correctifs de liaison/thread-binding Discord ACP ou de préparation de passerelle.
- Retourné le miroir de problème #43756 notant que la parité Slack manque toujours tandis que Discord/Telegram implémentent déjà le cycle de vie de génération de liaison de thread.

Requête :

```text
discrawl search --mode hybrid --limit 10 "forum media channel thread create Discord"
```

Résultats :

- Retourné le miroir de problème #40262, "message action=thread-create silently fails on Discord forum channels (type 15)," fermé comme implémenté après que le `main` actuel ait géré la création de thread forum/média avec des messages initiaux et des tags.
- Retourné un fil de support "Claw cannot create new Discord threads or forum channel posts" avec des conseils pour envoyer aux parents forum/média en tant que posts de thread et ne pas passer `--message-id` pour les canaux forum.
- Retourné les entrées de miroir PR/problème #30358, #33857, et #33930 sur le support `applied_tags` pour les threads forum/média.

Requête :

```text
discrawl search --mode hybrid --limit 10 "Discord ACP bind here thread follow-up"
```

Résultats :

- Retourné le miroir de problème #65801, "Messages are not passed to ACP," fermé comme implémenté après examen de la liaison ACP de conversation actuelle Discord actuelle.
- Retourné les discussions Discord "acp commands not working in threads" et "messages re not reaching ACP" où `/acp spawn ... --bind here` a réussi mais les messages de thread de suivi ou les commandes `/acp` natives n'ont pas atteint de manière fiable la session ACP liée.
- Retourné les conseils expliquant que `--bind here` et `--thread ...` sont des chemins distincts et que le travail persistant utilise couramment une salle de contrôle plus des threads Discord par tâche.

Requête :

```text
discrawl search --mode hybrid --limit 10 "Discord sessions_spawn thread binding fails"
```

Résultats :

- Retourné le miroir de problème #63927, fermé comme implémenté après que le `main` actuel ait normalisé les cibles `channel:<snowflake>` avant la liaison de thread Discord.
- Retourné le problème #70315 et la PR #68034 pour les échecs `thread_binding_invalid` causés par les ID de canal Discord préfixés.
- Retourné le problème #40077 pour `sessions_spawn thread=true` échouant sur les canaux de guilde Discord, fermé ultérieurement comme implémenté après les correctifs du gestionnaire de liaison de thread et du routage de compte.
