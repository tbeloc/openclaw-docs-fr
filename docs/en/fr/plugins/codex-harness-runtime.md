---
summary: "Limites d'exécution, hooks, outils, permissions et diagnostics pour le harnais Codex"
title: "Runtime du harnais Codex"
read_when:
  - You need the Codex harness runtime support contract
  - You are debugging native Codex tools, hooks, compaction, or feedback upload
  - You are changing plugin behavior across PI and Codex harness turns
---

Cette page documente le contrat d'exécution pour les tours du harnais Codex. Pour la configuration et le routage, commencez par [Codex harness](/fr/plugins/codex-harness). Pour les champs de configuration, voir [Codex harness reference](/fr/plugins/codex-harness-reference).

## Aperçu

Le mode Codex n'est pas PI avec un appel de modèle différent en dessous. Codex possède davantage de la boucle de modèle natif, et OpenClaw adapte ses surfaces de plugin, d'outil, de session et de diagnostic autour de cette limite.

OpenClaw possède toujours le routage des canaux, les fichiers de session, la livraison des messages visibles, les outils dynamiques OpenClaw, les approbations, la livraison des médias et un miroir de transcription. Codex possède le thread natif canonique, la boucle de modèle natif, la continuation d'outil natif et la compaction natif sauf si le moteur de contexte OpenClaw actif déclare qu'il possède la compaction.

Le routage des invites suit le runtime sélectionné, pas seulement la chaîne du fournisseur. Un tour Codex natif reçoit les instructions du développeur du serveur d'applications Codex, tandis qu'une route de compatibilité PI explicite conserve l'invite système OpenClaw/PI normale même lorsqu'elle utilise l'authentification ou le transport OpenAI de saveur Codex.

Codex natif conserve les instructions de base/modèle/personnalité détenues par Codex et le comportement project-doc selon la configuration de thread Codex active. Les exécutions OpenClaw légères conservent toujours leur suppression project-doc existante. Les instructions du développeur OpenClaw sont limitées aux préoccupations du runtime OpenClaw telles que la livraison du canal source, les outils dynamiques OpenClaw, la délégation ACP et le contexte de l'adaptateur. Les catalogues de compétences OpenClaw et les fichiers d'amorçage de l'espace de travail non-AGENTS sont projetés comme contexte de référence d'entrée de tour pour Codex natif au lieu d'être promus dans les instructions du développeur Codex.

## Liaisons de thread et changements de modèle

Lorsqu'une session OpenClaw est attachée à un thread Codex existant, le tour suivant envoie le modèle OpenAI actuellement sélectionné, la politique d'approbation, le sandbox et le niveau de service au serveur d'applications à nouveau. Le passage de `openai/gpt-5.5` à `openai/gpt-5.2` conserve la liaison de thread mais demande à Codex de continuer avec le modèle nouvellement sélectionné.

## Réponses visibles et battements de cœur

Lorsqu'un tour de chat direct/source s'exécute via le harnais Codex, les réponses visibles sont par défaut l'outil de message : le texte assistant final reste privé sauf si l'agent appelle `message(action="send")`. Cela correspond bien aux modèles GPT car ils peuvent décider si la sortie du canal source est utile. Définissez `messages.visibleReplies: "automatic"` pour restaurer l'ancien mode où le texte assistant final est publié automatiquement.

Les tours de battement de cœur Codex obtiennent également `heartbeat_respond` dans le catalogue d'outils OpenClaw consultable par défaut, afin que l'agent puisse enregistrer si le réveil doit rester silencieux ou notifier sans encoder ce flux de contrôle dans le texte final.

Les conseils d'initiative spécifiques au battement de cœur sont envoyés comme une instruction du développeur en mode collaboration Codex sur le tour de battement de cœur lui-même. Les tours de chat ordinaires restaurent le mode Codex par défaut au lieu de porter la philosophie du battement de cœur dans leur invite d'exécution normale.

## Limites des hooks

Le harnais Codex a trois couches de hook :

| Couche                                 | Propriétaire                    | Objectif                                                             |
| ------------------------------------- | ------------------------ | ------------------------------------------------------------------- |
| Hooks de plugin OpenClaw                 | OpenClaw                 | Compatibilité produit/plugin entre les harnais PI et Codex.         |
| Middleware d'extension du serveur d'applications Codex | Plugins OpenClaw groupés | Comportement de l'adaptateur par tour autour des outils dynamiques OpenClaw.            |
| Hooks natifs Codex                    | Codex                    | Politique de cycle de vie Codex bas niveau et d'outil natif à partir de la configuration Codex. |

OpenClaw n'utilise pas les fichiers `hooks.json` Codex au niveau du projet ou global pour router le comportement du plugin OpenClaw. Pour le pont d'outil natif et de permission pris en charge, OpenClaw injecte la configuration Codex par thread pour `PreToolUse`, `PostToolUse`, `PermissionRequest` et `Stop`.

Lorsque les approbations du serveur d'applications Codex sont activées, ce qui signifie que `approvalPolicy` n'est pas `"never"`, la configuration de hook natif injectée par défaut omet `PermissionRequest` afin que l'examinateur du serveur d'applications Codex et le pont d'approbation OpenClaw gèrent les escalades réelles après examen. Les opérateurs peuvent explicitement ajouter `permission_request` à `nativeHookRelay.events` lorsqu'ils ont besoin du relais de compatibilité.

Les autres hooks Codex tels que `SessionStart` et `UserPromptSubmit` restent des contrôles au niveau Codex. Ils ne sont pas exposés comme des hooks de plugin OpenClaw dans le contrat v1.

Pour les outils dynamiques OpenClaw, OpenClaw exécute l'outil après que Codex demande l'appel, donc OpenClaw déclenche le comportement du plugin et du middleware qu'il possède dans l'adaptateur du harnais. Pour les outils natifs Codex, Codex possède l'enregistrement d'outil canonique. OpenClaw peut refléter les événements sélectionnés, mais il ne peut pas réécrire le thread Codex natif sauf si Codex expose cette opération via le serveur d'applications ou les rappels de hook natifs.

Les notifications d'élément du serveur d'applications Codex fournissent également des observations asynchrones `after_tool_call` pour les complétions d'outils natifs qui ne sont pas déjà couvertes par le relais natif `PostToolUse`. Ces observations sont uniquement pour la télémétrie et la compatibilité des plugins ; elles ne peuvent pas bloquer, retarder ou muter l'appel d'outil natif.

Les projections de compaction et de cycle de vie LLM proviennent des notifications du serveur d'applications Codex et de l'état de l'adaptateur OpenClaw, pas des commandes de hook natif Codex. Les événements `before_compaction`, `after_compaction`, `llm_input` et `llm_output` d'OpenClaw sont des observations au niveau de l'adaptateur, pas des captures octet par octet des charges utiles de demande ou de compaction internes de Codex.

Les notifications du serveur d'applications Codex natif `hook/started` et `hook/completed` sont projetées comme des événements d'agent `codex_app_server.hook` pour la trajectoire et le débogage. Elles n'invoquent pas les hooks de plugin OpenClaw.

## Contrat de support V1

Pris en charge dans le runtime Codex v1 :

| Surface                                       | Support                                                                          | Raison                                                                                                                                                                                                                                                                                                                                                                 |
| --------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Boucle de modèle OpenAI via Codex               | Pris en charge                                                                        | Le serveur d'application Codex possède le tour OpenAI, la reprise de thread native et la continuation d'outil native.                                                                                                                                                                                                                                                                          |
| Routage et livraison de canal OpenClaw         | Pris en charge                                                                        | Telegram, Discord, Slack, WhatsApp, iMessage et autres canaux restent en dehors du runtime du modèle.                                                                                                                                                                                                                                                                    |
| Outils dynamiques OpenClaw                        | Pris en charge                                                                        | Codex demande à OpenClaw d'exécuter ces outils, donc OpenClaw reste dans le chemin d'exécution.                                                                                                                                                                                                                                                                                |
| Plugins de prompt et de contexte                    | Pris en charge                                                                        | OpenClaw projette le prompt/contexte spécifique à OpenClaw dans le tour Codex tout en laissant les prompts de base, de modèle, de personnalité et de documentation de projet appartenant à Codex dans la voie Codex native. Les instructions de développeur Codex native n'acceptent que les conseils de commande explicitement limités à `codex_app_server` ; les indices de commande globaux hérités restent pour les surfaces de prompt non-Codex. |
| Cycle de vie du moteur de contexte                      | Pris en charge                                                                        | L'assemblage, l'ingestion, la maintenance après tour et la coordination de compaction du moteur de contexte s'exécutent pour les tours Codex.                                                                                                                                                                                                                                                           |
| Hooks d'outil dynamique                            | Pris en charge                                                                        | `before_tool_call`, `after_tool_call` et le middleware de résultat d'outil s'exécutent autour des outils dynamiques appartenant à OpenClaw.                                                                                                                                                                                                                                                          |
| Hooks de cycle de vie                               | Pris en charge en tant qu'observations d'adaptateur                                                | `llm_input`, `llm_output`, `agent_end`, `before_compaction` et `after_compaction` se déclenchent avec des charges utiles en mode Codex honnête.                                                                                                                                                                                                                                           |
| Portail de révision de réponse finale                    | Pris en charge via relais de hook native                                              | Codex `Stop` est relayé à `before_agent_finalize` ; `revise` demande à Codex un autre passage de modèle avant la finalisation.                                                                                                                                                                                                                                                |
| Shell native, patch et bloc MCP ou observation | Pris en charge via relais de hook native                                              | Codex `PreToolUse` et `PostToolUse` sont relayés pour les surfaces d'outil native engagées, y compris les charges utiles MCP sur Codex app-server `0.125.0` ou plus récent. Le blocage est pris en charge ; la réécriture d'arguments ne l'est pas.                                                                                                                                               |
| Politique de permission native                      | Pris en charge via les approbations du serveur d'application Codex et le relais de hook native de compatibilité | Les demandes d'approbation du serveur d'application Codex sont acheminées via OpenClaw après examen par Codex. Le relais de hook native `PermissionRequest` est opt-in pour les modes d'approbation native car Codex l'émet avant l'examen du gardien.                                                                                                                                                          |
| Capture de trajectoire du serveur d'application                 | Pris en charge                                                                        | OpenClaw enregistre la demande qu'il a envoyée au serveur d'application et les notifications du serveur d'application qu'il reçoit.                                                                                                                                                                                                                                                                    |

Non pris en charge dans le runtime Codex v1 :

| Surface                                             | Limite V1                                                                                                                                     | Chemin futur                                                                               |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Mutation d'argument d'outil native                       | Les hooks de pré-outil native Codex peuvent bloquer, mais OpenClaw ne réécrit pas les arguments d'outil natifs Codex.                                                                               | Nécessite le support de hook/schéma Codex pour le remplacement de l'entrée d'outil.                            |
| Historique de transcription Codex-native modifiable            | Codex possède l'historique de thread native canonique. OpenClaw possède un miroir et peut projeter le contexte futur, mais ne doit pas muter les internals non pris en charge. | Ajouter des API explicites du serveur d'application Codex si la chirurgie de thread native est nécessaire.                    |
| `tool_result_persist` pour les enregistrements d'outil Codex-native | Ce hook transforme les écritures de transcription appartenant à OpenClaw, pas les enregistrements d'outil natifs Codex.                                                                           | Pourrait refléter les enregistrements transformés, mais la réécriture canonique nécessite le support Codex.              |
| Métadonnées de compaction native riche                     | OpenClaw observe le début et l'achèvement de la compaction, mais ne reçoit pas de liste stable conservée/supprimée, de delta de token ou de charge utile de résumé.            | Nécessite des événements de compaction Codex plus riches.                                                     |
| Intervention de compaction                             | Les hooks de compaction OpenClaw actuels sont au niveau de la notification en mode Codex.                                                                         | Ajouter des hooks de compaction pré/post Codex si les plugins doivent opposer un veto ou réécrire la compaction native. |
| Capture de demande d'API de modèle octet pour octet                 | OpenClaw peut capturer les demandes du serveur d'application et les notifications, mais le noyau Codex construit la demande d'API OpenAI finale en interne.                      | Nécessite un événement de traçage de demande de modèle Codex ou une API de débogage.                                   |

## Permissions natives et élicitations MCP

Pour `PermissionRequest`, OpenClaw ne retourne que des décisions d'autorisation ou de refus explicites
lorsque la politique en décide. Un résultat sans décision n'est pas une autorisation. Codex le traite comme aucune
décision de hook et bascule vers son propre chemin d'approbation du gardien ou de l'utilisateur.

Les modes d'approbation du serveur d'application Codex omettent ce hook native par défaut. Ce comportement
s'applique lorsque `permission_request` est explicitement inclus dans
`nativeHookRelay.events` ou qu'un runtime de compatibilité l'installe.

Lorsqu'un opérateur choisit `allow-always` pour une demande de permission native Codex,
OpenClaw se souvient de cette empreinte digitale exacte du fournisseur/session/entrée d'outil/cwd pour une
fenêtre de session délimitée. La décision mémorisée est intentionnellement exacte uniquement : une commande modifiée, des arguments, une charge utile d'outil ou un cwd crée une
approbation nouvelle.

Les élicitations d'approbation d'outil MCP Codex sont acheminées via le flux d'approbation du plugin OpenClaw lorsque Codex marque `_meta.codex_approval_kind` comme
`"mcp_tool_call"`. Les prompts Codex `request_user_input` sont renvoyés au
chat d'origine, et le prochain message de suivi en file d'attente répond à cette demande de serveur native au lieu d'être dirigé comme contexte supplémentaire. Les autres demandes d'élicitation MCP échouent fermées.

## Direction de la file d'attente

La direction de la file d'attente d'exécution active correspond à Codex app-server `turn/steer`. Avec le
mode par défaut `messages.queue.mode: "steer"`, OpenClaw regroupe les messages de chat en mode steer pour la fenêtre silencieuse configurée et les envoie comme une seule demande `turn/steer` dans l'ordre d'arrivée.

Les tours d'examen Codex et de compaction manuelle peuvent rejeter la direction du même tour. Dans ce
cas, OpenClaw attend la fin de l'exécution active avant de démarrer le prompt.
Utilisez `/queue followup` ou `/queue collect` lorsque les messages doivent être mis en file d'attente par défaut
au lieu de diriger. Voir [Direction de la file d'attente](/fr/concepts/queue-steering).

## Téléchargement de retours Codex

Lorsque `/diagnostics [note]` est approuvé pour une session utilisant le harnais Codex native,
OpenClaw appelle également Codex app-server `feedback/upload` pour les threads Codex pertinents. Le téléchargement demande au serveur d'application d'inclure les journaux pour chaque thread listé
et les sous-threads Codex générés lorsqu'ils sont disponibles.

Le téléchargement passe par le chemin de retours normal de Codex vers les serveurs OpenAI. Si les retours Codex
sont désactivés dans ce serveur d'application, la commande retourne l'erreur du serveur d'application. La réponse de diagnostics complétée répertorie les canaux, les identifiants de session OpenClaw,
les identifiants de thread Codex et les commandes locales `codex resume <thread-id>` pour les threads
qui ont été envoyés.

Si vous refusez ou ignorez l'approbation, OpenClaw n'imprime pas ces identifiants Codex et
n'envoie pas de retours Codex. Le téléchargement ne remplace pas l'export de diagnostics Gateway local. Voir [Export de diagnostics](/fr/gateway/diagnostics) pour le
comportement d'approbation, de confidentialité, de bundle local et de chat de groupe.

Utilisez `/codex diagnostics [note]` uniquement lorsque vous souhaitez spécifiquement le
téléchargement de retours Codex pour le thread actuellement attaché sans le
bundle de diagnostics Gateway complet.

## Compaction et miroir de transcription

Lorsque le modèle sélectionné utilise le harnais Codex, la compaction native des threads est
déléguée au serveur d'application Codex sauf si un moteur de contexte actif déclare
`ownsCompaction: true`. Les moteurs de contexte propriétaires compactent d'abord et causent OpenClaw
à abandonner l'ancien thread backend Codex afin que le prochain tour puisse réhydrater un thread frais
à partir du contexte géré par le moteur. OpenClaw maintient un miroir de transcription pour
l'historique des canaux, la recherche, `/new`, `/reset`, et les futurs changements de modèle ou de harnais.

Lorsqu'un moteur de contexte demande une projection de bootstrap de thread Codex, OpenClaw
projette les noms et identifiants des appels d'outils, les formes d'entrée, et le contenu des résultats d'outils
rédactés dans le nouveau thread Codex. Il ne copie pas les valeurs d'arguments d'appels d'outils bruts dans
cette projection.

Le miroir inclut l'invite utilisateur, le texte assistant final, et les enregistrements légers de
raisonnement ou de plan Codex lorsque le serveur d'application les émet. Actuellement, OpenClaw
enregistre uniquement les signaux de début et de fin de compaction native. Il n'expose pas encore un
résumé de compaction lisible par l'homme ou une liste vérifiable des entrées que Codex
a conservées après compaction.

Parce que Codex possède le thread natif canonique, `tool_result_persist` ne réécrit pas
actuellement les enregistrements de résultats d'outils natifs de Codex. Il s'applique uniquement lorsque
OpenClaw écrit un résultat d'outil de transcription de session détenu par OpenClaw.

## Médias et livraison

OpenClaw continue de posséder la livraison de médias et la sélection du fournisseur de médias. Image,
vidéo, musique, PDF, TTS, et la compréhension des médias utilisent des paramètres de fournisseur/modèle correspondants
tels que `agents.defaults.imageGenerationModel`, `videoGenerationModel`,
`pdfModel`, et `messages.tts`.

Le texte, les images, la vidéo, la musique, le TTS, les approbations, et la sortie de l'outil de messagerie continuent
par le chemin de livraison normal d'OpenClaw. La génération de médias ne nécessite pas PI.
Lorsque Codex émet un élément de génération d'image natif avec un `savedPath`, OpenClaw
transmet ce fichier exact par le chemin de réponse-média normal même si le
tour Codex n'a pas de texte assistant.

## Connexes

- [Harnais Codex](/fr/plugins/codex-harness)
- [Référence du harnais Codex](/fr/plugins/codex-harness-reference)
- [Plugins Codex natifs](/fr/plugins/codex-native-plugins)
- [Crochets de plugin](/fr/plugins/hooks)
- [Plugins de harnais d'agent](/fr/plugins/sdk-agent-harness)
- [Export de diagnostics](/fr/gateway/diagnostics)
- [Export de trajectoire](/fr/tools/trajectory)
