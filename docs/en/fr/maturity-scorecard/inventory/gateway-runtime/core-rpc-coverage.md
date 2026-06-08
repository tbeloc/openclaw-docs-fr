---
title: Gateway Runtime WebSocket Feature Matrix - Gateway RPC APIs and Events
version: 3
last_refreshed: 2026-05-29
last_refreshed_by: codex
feature_family: Gateway RPC APIs and Events
feature_slug: core-rpc-coverage
---

# Gateway RPC APIs and Events

## Résumé

La couverture RPC principale est large en source et en documentation : la Gateway dispose de descripteurs typés, de métadonnées de portée, de découverte de méthodes annoncées et d'événements, de modules de gestionnaires paresseux, de cadrage de requête/réponse/événement, de sémantique de résultats acceptés-puis-finaux en deux étapes, et de nombreuses implémentations de gestionnaires pour les familles système, identité, modèle, utilisation, session, canal, configuration, assistant, agent, automatisation, tâche, outil et compétence.

La limite de maturité n'est pas la largeur brute de l'implémentation. La famille est trop large pour un score `Coverage: Yes` car les tests réels de flux Gateway/serveur couvrent plusieurs chemins représentatifs, mais de nombreux groupes de méthodes importants s'appuient toujours sur des tests de gestionnaire ou d'unité plutôt que sur une preuve WS/RPC de bout en bout. Les preuves d'archive montrent également une douleur utilisateur/opérateur historique substantielle autour de `agent.wait`, `cron.run`, `tools.invoke`, `commands.list`, `skills.status`, et les rapports de statut/canal.

## Fonctionnalités

- APIs de santé : RPC `health` et `status`.
- APIs d'identité et de présence : `gateway.identity.get`, `system-presence`, `system-event`, et RPC de battement cardiaque.
- APIs de modèle : RPC `models.list`.
- APIs d'utilisation et de mémoire : Résumés d'utilisation et RPC de disponibilité de la mémoire.
- APIs de session : RPC `sessions.*`.
- APIs de chat : RPC `chat.*` et `agent.wait`.
- APIs de canal : RPC `channels.status` et `channels.logout`.
- APIs de connexion Web et de réveil : RPC `web.login.*`, `push.test`, et `voicewake.*`.
- APIs de configuration et de secrets : RPC `config.*` et `secrets.*`.
- APIs de mise à jour et de configuration : RPC `update.*` et `wizard.*`.
- APIs d'agent et d'artefact : RPC `agents.*`, fichiers d'agent, environnements et artefacts.
- APIs de tâche et d'automatisation : RPC `wake`, `cron.*`, et `tasks.*`.
- APIs d'outil et de compétence : RPC `commands.list`, `tools.*`, et `skills.*`.
- Enveloppes de requête et d'événement : Formes de cadre de requête, réponse et événement.
- Effets secondaires idempotents : Exigences d'idempotence pour les méthodes avec effets secondaires.
- Découverte de méthode : Découverte de méthode via `hello-ok.features.methods`.
- Découverte d'événement : Découverte d'événement via `hello-ok.features.events`.
- Résultats acceptés-puis-finaux : Accusé de réception accepté immédiat plus résultat final ultérieur.
- Ordre des événements : Gestion de la séquence et ordre monotone des événements par client.
- Actualisation d'état après les lacunes : Modèle sans relecture et récupération explicite des lacunes via actualisation d'état.

## Fraîcheur de l'archive

- `gitcrawl doctor --json`: `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, `repository_count=2`.
- `discrawl status --json`: `generated_at=2026-05-30T00:04:12Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Couverture

Score : 68

Étiquette : Partielle

Signaux positifs :

- La documentation énumère les familles RPC principales en un seul endroit : les méthodes d'aide système/identité, modèles/utilisation, canaux/connexion, configuration/mise à jour/assistant, agent/espace de travail, automatisation/compétences/outils, et opérateur sont décrites dans `docs/gateway/protocol.md:334`, `docs/gateway/protocol.md:346`, `docs/gateway/protocol.md:358`, `docs/gateway/protocol.md:400`, `docs/gateway/protocol.md:415`, `docs/gateway/protocol.md:474`, et `docs/gateway/protocol.md:543`.
- `docs/gateway/index.md:312` indique que `hello-ok.features.methods` est la liste de découverte conservatrice, et `docs/gateway/index.md:331` décrit les vérifications de vivacité/disponibilité qui utilisent les RPC Gateway.
- `src/gateway/methods/core-descriptors.ts:18` déclare les spécifications et portées de méthode principale, y compris les familles d'inventaire à `src/gateway/methods/core-descriptors.ts:87`, `src/gateway/methods/core-descriptors.ts:94`, `src/gateway/methods/core-descriptors.ts:109`, `src/gateway/methods/core-descriptors.ts:128`, `src/gateway/methods/core-descriptors.ts:174`, et `src/gateway/methods/core-descriptors.ts:182`.
- `src/gateway/server-methods-list.ts:11` construit la liste de méthode principale annoncée, et `src/gateway/server/ws-connection/message-handler.ts:1799` inclut la liste de méthode dans `hello-ok.features`.
- `src/gateway/server-methods.ts:248` câble les gestionnaires principaux paresseux dans la plupart des groupes d'inventaire, avec des regroupements visibles pour santé/statut, canaux, cron, configuration, assistant, outils, compétences, sessions, identité/présence système, mise à jour, utilisation, agent, agents, et artefacts à `src/gateway/server-methods.ts:265`, `src/gateway/server-methods.ts:269`, `src/gateway/server-methods.ts:281`, `src/gateway/server-methods.ts:356`, `src/gateway/server-methods.ts:368`, `src/gateway/server-methods.ts:398`, `src/gateway/server-methods.ts:423`, `src/gateway/server-methods.ts:439`, `src/gateway/server-methods.ts:467`, `src/gateway/server-methods.ts:477`, `src/gateway/server-methods.ts:523`, `src/gateway/server-methods.ts:533`, `src/gateway/server-methods.ts:537`, et `src/gateway/server-methods.ts:549`.
- Une preuve réelle de Gateway/WS ou de flux en direct existe pour les représentants importants : `health`, `status`, `system-presence`, battement cardiaque, et `system-event` dans `src/gateway/server.health.test.ts:28`, `src/gateway/server.health.test.ts:55`, et `src/gateway/server.health.test.ts:110` ; `sessions.create` plus `agent.wait` dans `src/gateway/server.sessions.create.test.ts:246` ; `chat.send` et `chat.history` dans `src/gateway/server.chat.gateway-server-chat-b.test.ts:123` et `src/gateway/server.chat.gateway-server-chat-b.test.ts:1002` ; `models.list` et `voicewake.*` dans `src/gateway/server.models-voicewake-misc.test.ts:148`, `src/gateway/server.models-voicewake-misc.test.ts:230`, et `src/gateway/server.models-voicewake-misc.test.ts:473` ; `config.get` / `config.set` dans `src/gateway/server.config-patch.test.ts:145` ; `channels.status` dans `src/gateway/server.channels.test.ts:106` ; `tools.catalog` dans `src/gateway/server.tools-catalog.test.ts:7` ; et `wizard.start` dans `src/gateway/gateway.test.ts:391`.
- Les tests en direct utilisent `chat.send`, `chat.history`, `agent.wait`, et `sessions.list` contre les clients Gateway en direct dans `src/gateway/gateway-acp-bind.live.test.ts:391`, `src/gateway/gateway-acp-bind.live.test.ts:422`, `src/gateway/gateway-acp-bind.live.test.ts:456`, `src/gateway/gateway-codex-harness.live.test.ts:369`, `src/gateway/gateway-codex-harness.live.test.ts:418`, et `src/gateway/gateway-codex-harness.live.test.ts:795`.

Signaux négatifs :

- Plusieurs groupes d'inventaire sont implémentés et testés au niveau des unités, mais manquent de preuve Gateway/WS réelle comparable dans les preuves trouvées ici : `commands.list`, `skills.status/search/detail/install/update`, `skills.upload.*`, `tasks.*`, plusieurs méthodes `cron.*`, `web.login.*`, `push.test`, `environments.*`, et la plupart des `artifacts.*`.
- `tools.invoke` a des tests de gestionnaire RPC directs dans `src/gateway/tools-invoke-http.test.ts:966`, mais les preuves trouvées ici ne montrent pas un flux client WS complet exerçant la méthode via le registre Gateway en direct.
- Les rapports d'archive montrent que les méthodes d'exécution les plus importantes ont régulièrement régressé ou confus les opérateurs, en particulier autour des attentes longues, des exécutions manuelles de cron, de l'invocation d'outils, de la découverte de commandes, de la visibilité des compétences, et des résumés de canal/statut.

Lacunes d'intégration :

- Ajouter une suite de serveur-flux "Core RPC smoke" explicite qui connecte un client WS réel, lit `hello-ok.features.methods`, et échantillonne chaque famille de méthodes avec des appels en lecture seule inoffensifs ou des écritures contrôlées.
- Ajouter une preuve Gateway/WS réelle pour `commands.list`, `skills.status`, `skills.search`, `skills.detail`, `tasks.list`, `tasks.get`, `cron.list`, `cron.status`, corrélation `cron.run`, `web.login.*` via un canal de fixture, et `tools.invoke`.
- Ajouter des vérifications de découverte inter-méthodes afin que les méthodes documentées, les descripteurs principaux, les listes de méthodes annoncées, et les gestionnaires disponibles ne puissent pas dériver indépendamment.

## Qualité

Score : 57

Étiquette : Moyen

Rapports Gitcrawl :

- `gitcrawl search issues "channels.status" -R openclaw/openclaw --state all --json number,title,url,state`
  a retourné 20 résultats. Signaux de qualité notables : bugs fermés pour les tables de statut/canal vides ou mal appariées dans #73525, #73824, #72993, #73518, #73582,
  #46494, #72906, #17105, #67937, #67938, #75340, #53544, #11094, #55032, et
  #73605 ; le rapport ouvert #77709 signale que Feishu est omis de `status --deep`.
- `gitcrawl search issues "tools.invoke" -R openclaw/openclaw --state all --json number,title,url,state`
  a retourné 20 résultats. Signaux de qualité notables : bugs/fonctionnalités fermés pour le support cron/outils manquant et la disponibilité des outils dans #55430, #54391, #68874, #74705,
  #52888, #44071, #79849, #76616, et #74019 ; les demandes de fonctionnalités ouvertes #13948
  et #8287 demandent le refus des outils au niveau des actions et les outils des agents enregistrés au nœud.
- `gitcrawl search issues "agent.wait" -R openclaw/openclaw --state all --json number,title,url,state`
  a retourné 20 résultats. Signaux de qualité notables : rapports fermés sur les délais d'expiration,
  les sous-agents orphelins, les chutes de livraison et les plantages dans #4133, #19506, #49494,
  #45926, #63718, #61947, et #40862 ; les rapports ouverts #74363, #58067, #54622,
  #78656, et #68065 pointent toujours vers les aspérités d'attente/voie/livraison.
- `gitcrawl search issues "cron.run" -R openclaw/openclaw --state all --json number,title,url,state`
  a retourné 20 résultats. Signaux de qualité notables : blocages/délais d'expiration/lacunes d'historique de cron manuel fermés dans #19601, #52898, #44232, #38755, #20288,
  #25981, #29601, #62876, #42579, #43008, #54320, et #19300 ; #80019 a ajouté une
  portée d'inspection cron en lecture seule et #16799 a demandé une meilleure UX de statut pour
  les configurations lourdes en cron.
- `gitcrawl search issues "skills.status" -R openclaw/openclaw --state all --json number,title,url,state`
  a retourné 20 résultats. Signaux de qualité notables : bugs fermés #57678, #1843,
  #8290, #21094, #57599, #58712, #64816, et fonctionnalité #37595 ; les rapports ouverts #78553,
  #85015, #80206, #59078, et #73082 montrent une pression persistante sur les attentes UI/configuration.
- `gitcrawl search issues "commands.list" -R openclaw/openclaw --state all --json number,title,url,state`
  a retourné 20 résultats. Signaux de qualité notables : #80061 indique que l'API RPC Gateway a été
  silencieusement supprimée tandis que la documentation l'annonçait toujours, #52919 a ajouté l'API RPC pour
  les clients distants, et #38856/#38857/#38858/#38863 plus #29012 montrent une pression sur l'autocomplétion
  et la configuration des commandes par agent/par canal.
- `gitcrawl search issues "config.schema Gateway RPC" -R openclaw/openclaw --state all --json number,title,url,state`
  a retourné 20 résultats. Signaux de qualité notables : #36508 et #81409 fermés autour du
  comportement de `config.get` / schéma de configuration ; #86136 ouvert demande d'autoriser le renforcement de `config.patch` de l'agent pour la découverte groupée ; #46656 et #74632 ouverts demandent une forme d'API RPC d'enveloppe de rappel/session supplémentaire.
- `gitcrawl search issues "gateway identity get system-presence system-event heartbeat" -R openclaw/openclaw --state all --json number,title,url,state`
  a retourné `[]`.

Rapports Discrawl :

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json sql "<FTS count query>"` a compté
  les résultats d'archive de terme exact : `channels.status=6302`, `agent.wait=332`,
  `tools.invoke=501`, `cron.run=1984`, `skills.status=268`,
  `commands.list=143`, et `config.schema=2451`.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "channels.status"`
  a retourné des rapports d'utilisateurs s'entraidant des 2026-05-25 et 2026-05-06 où
  `channels status --probe` a signalé un fonctionnement sain/correct tandis que la livraison entrante Slack ou Telegram a échoué ; il a également retourné un extrait de journal du 2026-05-23 avec une réponse WS `channels.status` réussie lors de changements de configuration/compétences.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "agent.wait"` a retourné
  des commentaires de miroir GitHub pour #49494, #42233, #66978, #64519, #63724, #62787,
  et #62469, principalement sur les délais d'expiration, l'auto-appel, le maintien de la connexion et les correctifs de course à la complétion.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "tools.invoke"` a retourné
  une note du responsable du 2026-05-14 indiquant que l'API RPC Gateway directe `tools.invoke` et la boucle MCP exécutent `before_tool_call` mais n'exécutent pas systématiquement `after_tool_call`,
  plus les conseils d'authentification/réponse de fil `/tools/invoke` orientés utilisateur du 2026-04-27.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "cron.run"` a retourné
  une discussion responsable/utilisateur du 2026-05-17 sur le comportement de `openclaw cron run --wait`
  et un commentaire du responsable du 2026-05-15 indiquant que la forme d'attente exacte-`runId` de #81929 semblait sûre tout en gardant l'API RPC Gateway elle-même non-bloquante.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "skills.status"` a retourné
  des commentaires de miroir GitHub fermant #57678, #60504, #46063, #42095, et #37595,
  plus des sorties de docteur/statut de compétences utilisateur montrant un état d'exigence manquante et d'éligibilité visible.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "commands.list"` a retourné
  des extraits de journal utilisateur des 2026-05-25 et 2026-05-02 montrant des réponses WS lentes
  pour `commands.list`, `models.list`, `sessions.list`, et `chat.history`, plus des commentaires de miroir GitHub pour l'autocomplétion des commandes et le comportement d'annonce des commandes.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "config.schema Gateway RPC"`
  a retourné des commentaires d'examen du responsable sur la compatibilité du schéma de configuration et l'enregistrement de chemin sensible, plus des conseils utilisateur indiquant que la construction de `config.get` / schéma peut être coûteuse et fait partie du comportement de sonde Gateway.

Bonnes qualités :

- La propriété des méthodes est explicite et typée via les descripteurs de base et les portées de méthode,
  plutôt que via des chaînes de dispatch ad hoc.
- Le chargement des gestionnaires est paresseux et groupé par famille de capacités, ce qui protège
  les chemins chauds de Gateway de l'importation enthousiaste de chaque implémentation de fonctionnalité.
- L'archive montre que de nombreux problèmes historiques ont été fermés avec des correctifs ciblés
  et des rapports de suivi, ce qui suggère que la surface est activement maintenue.

Mauvaises qualités :

- L'API RPC de base est une large surface opérationnelle, donc la dérive entre la documentation, les descripteurs,
  les méthodes annoncées, les portées et la disponibilité des gestionnaires est difficile à détecter jusqu'à ce qu'un
  utilisateur rencontre la famille de méthodes spécifique.
- L'archive montre des régressions répétées dans les résumés de statut/canal, le comportement de cron run,
  la visibilité/invocation des outils, la découverte des commandes et la sémantique de complétion d'attente d'agent.
- Certains chemins d'invocation directe ne semblent pas partager tous les crochets de cycle de vie ou
  les diagnostics avec l'exécution normale des outils d'agent, selon la note du responsable Discrawl `tools.invoke`.
- Le comportement de `config.get` / schéma est puissant mais peut être coûteux et a un historique d'examen de compatibilité/sensibilité.
- La visibilité/configuration des compétences et la personnalisation des commandes restent des lacunes d'attente dans
  les rapports ouverts tels que #78553, #85015, #73082, et #29012.
- Les demandes de rappel, d'enveloppe de session et de renforcement de configuration dans #46656, #74632,
  et #86136 montrent des attentes de forme d'API RPC adjacentes au contrat Core RPC actuel.

## Lacunes connues

- Les lacunes de couverture persistent pour la recherche/détail/installation/mise à jour et téléchargement de compétences,
  l'énumération des commandes, l'inspection/annulation du registre des tâches, la corrélation d'inspection/exécution manuelle de cron, le flux de fixture de connexion web, le test push, l'invocation des outils et les artefacts/environnements.
- L'invocation directe des outils Gateway ne semble pas systématiquement partager le chemin des crochets de cycle de vie et les diagnostics de l'exécution normale des outils d'agent.
- L'historique #80061 a signalé une incompatibilité docs/source pour `commands.list`, ce qui est
  le type de dérive auquel cette surface Core RPC reste sensible.
- Les rapports ouverts demandent la visibilité multi-agent des compétences, la clarté de la configuration des compétences,
  la personnalisation des commandes, le refus des outils au niveau des actions, les outils des agents enregistrés au nœud,
  les API RPC de rappel en ligne, les enveloppes par session et le renforcement de la configuration de l'agent.

## Preuves

Docs :

- `docs/gateway/protocol.md:334` documente les RPC système/identité.
- `docs/gateway/protocol.md:346` documente les RPC modèles/utilisation/préparation mémoire.
- `docs/gateway/protocol.md:358` documente les RPC canal/connexion/notification/activation vocale.
- `docs/gateway/protocol.md:400` documente les RPC secrets/configuration/mise à jour/assistant.
- `docs/gateway/protocol.md:415` documente agent/espace de travail/tâches/artefacts et
  `agent.wait`.
- `docs/gateway/protocol.md:474` documente les RPC activation/cron/outils/compétences.
- `docs/gateway/protocol.md:543` documente les contrats d'aide opérateur `commands.list`, `tools.*` et
  `skills.*`.
- `docs/gateway/index.md:312` documente la découverte du protocole opérateur et la
  forme d'exécution d'agent en deux étapes.
- `docs/gateway/index.md:331` documente les appels de vivacité/préparation opérationnelle et de récupération d'écart.

Source :

- `src/gateway/methods/core-descriptors.ts:18` déclare les spécifications de méthode principale.
- `src/gateway/methods/core-descriptors.ts:224` dérive les noms de méthode annoncés.
- `src/gateway/server-methods-list.ts:11` construit les méthodes principales + auxiliaires + canal annoncées.
- `src/gateway/server.impl.ts:1143` charge les gestionnaires principaux et auxiliaires lors du démarrage de la passerelle ; `src/gateway/server.impl.ts:1191` publie la liste des méthodes attachées.
- `src/gateway/server/ws-connection/message-handler.ts:1799` envoie les méthodes dans
  `hello-ok.features`.
- `src/gateway/server-methods.ts:248` définit les `coreGatewayHandlers` paresseux.
- `src/gateway/server-methods.ts:592` achemine les demandes de passerelle via l'autorisation de méthode et le registre de méthode.

Tests d'intégration :

- `src/gateway/server.health.test.ts:28` couvre `connect`, `health`, `status`,
  et `system-presence` via un harnais WS réel.
- `src/gateway/server.health.test.ts:55` couvre la diffusion d'événement de battement cardiaque,
  `last-heartbeat` et `set-heartbeats` via le harnais WS.
- `src/gateway/server.health.test.ts:110` couvre `system-event` et la séquençage d'événement de présence via le harnais WS.
- `src/gateway/server.sessions.create.test.ts:246` couvre `sessions.create`
  démarrage automatique plus `agent.wait` via un client de passerelle.
- `src/gateway/server.chat.gateway-server-chat-b.test.ts:123` couvre
  `chat.history` ; `src/gateway/server.chat.gateway-server-chat-b.test.ts:1002`
  couvre `chat.send`.
- `src/gateway/server.models-voicewake-misc.test.ts:148` et
  `src/gateway/server.models-voicewake-misc.test.ts:473` couvrent `models.list`
  via RPC de passerelle.
- `src/gateway/server.models-voicewake-misc.test.ts:230` couvre
  `voicewake.get` / `voicewake.set` plus diffusion d'événement.
- `src/gateway/server.config-patch.test.ts:145` couvre `config.get` /
  `config.set` ; `src/gateway/server.config-patch.test.ts:266` couvre
  la rédaction de `config.get`.
- `src/gateway/server.channels.test.ts:106` couvre `channels.status`.
- `src/gateway/server.tools-catalog.test.ts:7` couvre `tools.catalog`.
- `src/gateway/gateway.test.ts:391` couvre `wizard.start`.
- `src/gateway/gateway-acp-bind.live.test.ts:391`,
  `src/gateway/gateway-acp-bind.live.test.ts:422` et
  `src/gateway/gateway-acp-bind.live.test.ts:456` couvrent `chat.history`,
  `agent.wait` et `chat.send` en direct.
- `src/gateway/gateway-codex-harness.live.test.ts:369`,
  `src/gateway/gateway-codex-harness.live.test.ts:418` et
  `src/gateway/gateway-codex-harness.live.test.ts:795` couvrent `chat.send`,
  `agent.wait` et `sessions.list` en direct.

Tests unitaires :

- `src/gateway/server-methods-list.test.ts:12` couvre le comportement de la liste de méthode annoncée.
- `src/gateway/method-scopes.test.ts:38` couvre la résolution de portée de moindre privilège
  pour les méthodes RPC principales ; `src/gateway/method-scopes.test.ts:379`
  protège la classification pour chaque méthode de gestionnaire principal exposée.
- `src/gateway/server-methods/commands.test.ts:203` couvre `commands.list`.
- `src/gateway/server-methods/tasks.test.ts:80` couvre `tasks.list`,
  `src/gateway/server-methods/tasks.test.ts:122` couvre `tasks.get` et
  `src/gateway/server-methods/tasks.test.ts:197` couvre `tasks.cancel`.
- `src/gateway/server-methods/cron.validation.test.ts:91` couvre l'invocation directe du gestionnaire
  `cron.add/get/update/remove` ; `src/gateway/server-methods/cron.validation.test.ts:717`
  couvre `wake`.
- `src/gateway/server-methods/web.start.test.ts:82` couvre `web.login.start`
  et `src/gateway/server-methods/web.start.test.ts:152` couvre
  `web.login.wait`.
- `src/gateway/server-methods/push.test.ts:124` couvre `push.test`.
- `src/gateway/server-methods/environments.test.ts:64` couvre
  `environments.list` / `environments.status`.
- `src/gateway/tools-invoke-http.test.ts:966` couvre le comportement direct de l'enveloppe RPC de passerelle
  `tools.invoke`.

Requêtes Gitcrawl :

- Commande :
  `gitcrawl search issues "channels.status" -R openclaw/openclaw --state all --json number,title,url,state`
  - Résultats : 20 lignes, incluant #73525, #69341, #73824, #72993, #56949,
    #33070, #73518, #73582, #55744, #77709, #46494, #72906, #17105, #67937,
    #67938, #75340, #53544, #11094, #55032, #73605.
- Commande :
  `gitcrawl search issues "tools.invoke" -R openclaw/openclaw --state all --json number,title,url,state`
  - Résultats : 20 lignes, incluant #55430, #54391, #42471, #68874, #74705,
    #46052, #50279, #68979, #52888, #3906, #44071, #79849, #76616, #74019,
    #17356, #65975, #13948, #9857, #8287, #14363.
- Commande :
  `gitcrawl search issues "agent.wait" -R openclaw/openclaw --state all --json number,title,url,state`
  - Résultats : 20 lignes, incluant #4343, #4133, #74363, #10334, #11284, #19506,
    #82791, #58067, #49494, #54622, #45926, #78656, #68065, #40040, #63718,
    #65505, #30581, #61947, #12423, #40862.
- Commande :
  `gitcrawl search issues "cron.run" -R openclaw/openclaw --state all --json number,title,url,state`
  - Résultats : 20 lignes, incluant #19601, #52898, #44232, #38755, #33577,
    #80019, #20288, #69162, #83605, #25981, #87174, #13947, #29601, #16799,
    #62876, #42579, #14356, #43008, #54320, #19300.
- Commande :
  `gitcrawl search issues "skills.status" -R openclaw/openclaw --state all --json number,title,url,state`
  - Résultats : 20 lignes, incluant #57678, #1843, #78553, #7993, #8290, #40853,
    #85015, #21094, #80206, #57599, #58712, #73082, #57053, #85263, #8969,
    #37595, #52572, #84968, #59078, #64816.
- Commande :
  `gitcrawl search issues "commands.list" -R openclaw/openclaw --state all --json number,title,url,state`
  - Résultats : 20 lignes, incluant #12985, #80061, #52919, #53253, #17061,
    #38857, #38856, #38863, #38858, #66958, #81183, #68333, #74195, #29012,
    #77730, #66975, #51865, #62803, #56621, #62335.
- Commande :
  `gitcrawl search issues "config.schema Gateway RPC" -R openclaw/openclaw --state all --json number,title,url,state`
  - Résultats : 20 lignes, incluant #61559, #36508, #46656, #75780, #50195, #8374,
    #70318, #3644, #72496, #74632, #76600, #81409, #17328, #74918, #81311,
    #52830, #86136, #77753, #50174, #52071.
- Commande :
  `gitcrawl search issues "gateway identity get system-presence system-event heartbeat" -R openclaw/openclaw --state all --json number,title,url,state`
  - Résultats : `[]`.

Requêtes Discrawl :

- Commande :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "channels.status"`
  - Résultats : 5 messages. Les meilleurs résultats incluaient des rapports Slack Socket Mode du 2026-05-25 dans users-helping-users
    où le statut du canal semblait sain mais les événements entrants étaient absents ; un extrait de journal du 2026-05-23 avec `channels.status` ; un
    rapport Telegram du 2026-05-06 où `channels status --probe` disait fonctionner mais les messages/journaux entrants étaient absents ; et une
    note du responsable du 2026-05-03 sur le suivi des appels d'outils aux messages.
- Commande :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "agent.wait"`
  - Résultats : 10 messages. Les meilleurs résultats incluaient des commentaires du miroir GitHub pour
    #49494, #42233, #66978, #64519, #63724, #62787 et #62469, plus une
    mention de surface d'outil de session `clawtributors`.
- Commande :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "tools.invoke"`
  - Résultats : 10 messages. Les meilleurs résultats incluaient une note du responsable du 2026-05-14
    que la `tools.invoke` directe de passerelle manque de couverture `after_tool_call` cohérente, plus des conseils n8n/Feishu `/tools/invoke` du 2026-04-27 orientés utilisateur.
- Commande :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "cron.run"`
  - Résultats : 10 messages. Les meilleurs résultats incluaient une discussion du 2026-05-17 sur la
    preuve forcée de cron-run et un commentaire du responsable du 2026-05-15 que la forme `cron run --wait` de #81929 était sûre car elle attend un `runId` exact.
- Commande :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "skills.status"`
  - Résultats : 10 messages. Les meilleurs résultats incluaient des commentaires du miroir GitHub fermant
    #57678, #60504, #46063, #42095 et #37595, plus des sorties de statut de compétences et de docteur visibles par l'utilisateur.
- Commande :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "commands.list"`
  - Résultats : 10 messages. Les meilleurs résultats incluaient des extraits de journal utilisateur du 2026-05-25 et 2026-05-02 avec des RPC lents `commands.list` / `models.list` / `sessions.list`
    et des commentaires du miroir GitHub pour l'autocomplétion de l'interface utilisateur de contrôle.
- Commande :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "config.schema Gateway RPC"`
  - Résultats : 10 messages. Les meilleurs résultats incluaient des commentaires d'examen de schéma de configuration
    et des conseils utilisateur/responsable que `config.get` et la construction de schéma peuvent
    être coûteux ou sensibles à la compatibilité.
- Commande :
  `DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json sql "select ... from message_fts where message_fts match '\"<term>\"' ..."`
  - Résultats :
    `channels.status=6302`, `agent.wait=332`, `tools.invoke=501`,
    `cron.run=1984`, `skills.status=268`, `commands.list=143`,
    `config.schema=2451`.
