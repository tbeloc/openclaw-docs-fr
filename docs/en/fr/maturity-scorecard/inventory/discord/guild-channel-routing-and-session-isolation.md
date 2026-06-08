---
title: "Discord - Note de Maturité du Routage et de la Livraison des Conversations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Discord - Note de Maturité du Routage et de la Livraison des Conversations

## Résumé

Le routage des canaux de guilde Discord est un chemin d'exécution réel et documenté avec une politique de guilde/canal à défaut fermé, un contrôle d'accès par mention, des clés de session par canal, l'héritage des threads, les liaisons configurées/d'exécution, le routage conscient des rôles et l'isolation du contexte entrant. La preuve en direct la plus solide couvre les canaux canary, le contrôle d'accès par mention et les allers-retours guilde-canal. La principale limitation est que plusieurs flux négatifs et de récupération importants ne sont pas encore prouvés par des scénarios en direct ou E2E, en particulier le comportement de liste blanche-blocage, le routage par rôle dans un canal de guilde, le redémarrage/reprise, la forme de réponse de haut niveau et le comportement de la fenêtre d'historique.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Routage et Livraison des Conversations`
- Fusionnée à partir de : `Routage des Canaux et des Threads`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Admission de guilde et de canal : Couvre l'admission de guilde et de canal sur la liste blanche de guilde et l'admission `groupPolicy` pour les canaux de guilde Discord et les threads. `requireMention`, prévention des boucles de bot, contournements de commande/mention et historique des événements de salle non mentionnés. Routage des canaux et des canaux de guilde associés et comportement d'isolation de session.
- Contrôle d'accès par mention : Couvre le contrôle d'accès par mention sur la liste blanche de guilde et l'admission `groupPolicy` pour les canaux de guilde Discord et les threads. `requireMention`, prévention des boucles de bot, contournements de commande/mention et historique des événements de salle non mentionnés. Routage des canaux et des canaux de guilde associés et comportement d'isolation de session.
- Isolation des clés de session : Couvre l'isolation des clés de session sur la liste blanche de guilde et l'admission `groupPolicy` pour les canaux de guilde Discord et les threads. `requireMention`, prévention des boucles de bot, contournements de commande/mention et historique des événements de salle non mentionnés. Routage des canaux et des canaux de guilde associés et comportement d'isolation de session.
- Routage configuré et d'exécution : Couvre les liaisons configurées et d'exécution sur la liste blanche de guilde et l'admission `groupPolicy` pour les canaux de guilde Discord et les threads. `requireMention`, prévention des boucles de bot, contournements de commande/mention et historique des événements de salle non mentionnés. Routage des canaux et des canaux de guilde associés et comportement d'isolation de session.
- Visibilité du contexte entrant : Couvre la visibilité du contexte entrant sur la liste blanche de guilde et l'admission `groupPolicy` pour les canaux de guilde Discord et les threads. `requireMention`, prévention des boucles de bot, contournements de commande/mention et historique des événements de salle non mentionnés. Routage des canaux et des canaux de guilde associés et comportement d'isolation de session.
- Publications de threads de forum et de canal média : Couvre les publications de threads de forum et de canal média sur les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et outil de message : `thread-create`, `thread-list` et `thread-reply`. Analyse des cibles Discord pour `channel:<id>`, cibles utilisateur et comportement associé des threads, forums et liaisons d'agent délégué.
- Actions de thread : Couvre les actions de thread sur les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et outil de message : `thread-create`, `thread-list` et `thread-reply`. Analyse des cibles Discord pour `channel:<id>`, cibles utilisateur et comportement associé des threads, forums et liaisons d'agent délégué.
- Analyse des cibles : Couvre l'analyse des cibles sur les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et outil de message : `thread-create`, `thread-list` et `thread-reply`. Analyse des cibles Discord pour `channel:<id>`, cibles utilisateur et comportement associé des threads, forums et liaisons d'agent délégué.
- Résolution du contexte de thread : Couvre la résolution du contexte de thread sur les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et outil de message : `thread-create`, `thread-list` et `thread-reply`. Analyse des cibles Discord pour `channel:<id>`, cibles utilisateur et comportement associé des threads, forums et liaisons d'agent délégué.
- Routage de session lié au thread : Couvre le routage de session lié au thread sur les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et outil de message : `thread-create`, `thread-list` et `thread-reply`. Analyse des cibles Discord pour `channel:<id>`, cibles utilisateur et comportement associé des threads, forums et liaisons d'agent délégué.
- Routage d'agent ACP : Couvre les liaisons ACP sur les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et outil de message : `thread-create`, `thread-list` et `thread-reply`. Analyse des cibles Discord pour `channel:<id>`, cibles utilisateur et comportement associé des threads, forums et liaisons d'agent délégué.
- Cycle de vie du routage : Couvre le cycle de vie des liaisons sur les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et outil de message : `thread-create`, `thread-list` et `thread-reply`. Analyse des cibles Discord pour `channel:<id>`, cibles utilisateur et comportement associé des threads, forums et liaisons d'agent délégué.
- Publications de canal forum/média Discord créées en tant que : Couvre le comportement des publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent.
- Actions de thread CLI et outil de message : `thread-create`, `thread-list` et `thread-reply`
- Analyse des cibles Discord pour `channel:<id>` : Couvre l'analyse des cibles Discord pour `channel:<id>`, cibles utilisateur et IDs nus avec un comportement par défaut de canal.
- Résolution du contexte de thread : recherche de canal parent, recherche de message de démarrage, comportement de démarrage de forum/média, ciblage de réponse, assainissement de titre, titres générés optionnels et héritage de session/modèle parent
- Routage de session lié au thread pour `/focus`, `/unfocus`, `/agents`, `/session idle`, `/session max-age`, `sessions_spawn({ thread: true })` et cibles de livraison de sous-agent
- Liaisons ACP de conversation actuelle et spawns ACP thread : Couvre les liaisons ACP de conversation actuelle et les spawns ACP thread sur Discord, y compris le comportement de liaisons ACP configurées persistantes.
- Comportement du cycle de vie des liaisons : persistance des liaisons, livraison webhook, touches d'activité, expiration d'inactivité/max-age, nettoyage de thread obsolète/supprimé et réconciliation de démarrage ACP
- Envois directs et de thread : Couvre les envois directs et de thread sur Ce score de note le chemin de message sortant Discord : envois directs, réponses de thread, segmentation de texte, suivi média et comportement de rendu et de livraison de message sortant associé
- Segmentation de texte et mode de réponse : Couvre la segmentation de texte et le mode de réponse sur Ce score de note le chemin de message sortant Discord : envois directs, réponses de thread, segmentation de texte, suivi média et comportement de rendu et de livraison de message sortant associé
- Brouillons et éditions de progression : Couvre les brouillons et éditions de progression sur Ce score de note le chemin de message sortant Discord : envois directs, réponses de thread, segmentation de texte, suivi média et comportement de rendu et de livraison de message sortant associé
- Rendu des mentions et des intégrations : Couvre le rendu des mentions et des intégrations sur Ce score de note le chemin de message sortant Discord : envois directs, réponses de thread, segmentation de texte, suivi média et comportement de rendu et de livraison de message sortant associé
- Nouvelle tentative REST et livraison finale : Couvre la nouvelle tentative REST et la livraison finale sur Ce score de note le chemin de message sortant Discord : envois directs, réponses de thread, segmentation de texte, suivi média et comportement de rendu et de livraison de message sortant associé
- Téléchargements de fichiers : Téléchargements de fichiers sortants à partir d'URL et de chemins locaux, y compris les contraintes de livraison et le comportement de suivi
- Blocs de fichier de composant et galerie média : Blocs de fichier et galerie média du composant v2 pour la livraison de médias Discord
- Suivi de légende vidéo : Gestion des légendes vidéo et livraison de suivi réservée aux médias dans les conversations Discord
- Téléchargement de message vocal : Envois de message vocal Discord avec conversion OGG/Opus, génération de forme d'onde, métadonnées de durée et gestion d'URL de téléchargement
- Contexte de pièce jointe entrante : Contexte de pièce jointe entrante mis à disposition pour les réponses Discord et les tours d'agent

## Fonctionnalités

- Admission de guild et de canal : Couvre l'admission de guild et de canal sur les listes blanches de guild et l'admission `groupPolicy` pour les canaux et threads de guild Discord. `requireMention`, prévention des boucles de bot, contournements de commande/mention, et historique des événements de salle non mentionnés. Routage de canal et de guild associé, et comportement d'isolation de session.
- Mention gating : Couvre le mention gating sur les listes blanches de guild et l'admission `groupPolicy` pour les canaux et threads de guild Discord. `requireMention`, prévention des boucles de bot, contournements de commande/mention, et historique des événements de salle non mentionnés. Routage de canal et de guild associé, et comportement d'isolation de session.
- Isolation de clé de session : Couvre l'isolation de clé de session sur les listes blanches de guild et l'admission `groupPolicy` pour les canaux et threads de guild Discord. `requireMention`, prévention des boucles de bot, contournements de commande/mention, et historique des événements de salle non mentionnés. Routage de canal et de guild associé, et comportement d'isolation de session.
- Routage configuré et à l'exécution : Couvre les liaisons configurées et à l'exécution sur les listes blanches de guild et l'admission `groupPolicy` pour les canaux et threads de guild Discord. `requireMention`, prévention des boucles de bot, contournements de commande/mention, et historique des événements de salle non mentionnés. Routage de canal et de guild associé, et comportement d'isolation de session.
- Visibilité du contexte entrant : Couvre la visibilité du contexte entrant sur les listes blanches de guild et l'admission `groupPolicy` pour les canaux et threads de guild Discord. `requireMention`, prévention des boucles de bot, contournements de commande/mention, et historique des événements de salle non mentionnés. Routage de canal et de guild associé, et comportement d'isolation de session.
- Publications de threads de forum et de canal média : Couvre les publications de threads de forum et de canal média sur les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles d'utilisateur, et comportement associé des threads, forums, et liaisons d'agent délégué.
- Actions de thread : Couvre les actions de thread sur les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles d'utilisateur, et comportement associé des threads, forums, et liaisons d'agent délégué.
- Analyse de cible : Couvre l'analyse de cible sur les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles d'utilisateur, et comportement associé des threads, forums, et liaisons d'agent délégué.
- Résolution du contexte de thread : Couvre la résolution du contexte de thread sur les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles d'utilisateur, et comportement associé des threads, forums, et liaisons d'agent délégué.
- Routage de session lié au thread : Couvre le routage de session lié au thread sur les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles d'utilisateur, et comportement associé des threads, forums, et liaisons d'agent délégué.
- Routage d'agent ACP : Couvre les liaisons ACP sur les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles d'utilisateur, et comportement associé des threads, forums, et liaisons d'agent délégué.
- Cycle de vie du routage : Couvre le cycle de vie de liaison sur les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et message-tool : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles d'utilisateur, et comportement associé des threads, forums, et liaisons d'agent délégué.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`

Ce score est basé uniquement sur les preuves d'intégration, E2E, en direct et de flux d'exécution. La couverture est suffisamment solide pour la version bêta car le référentiel dispose de scénarios d'exécution Discord en direct et de trajets aller-retour de canal de guild multi-OS qui configurent `groupPolicy: "allowlist"`, ciblent une véritable guild/canal, redémarrent la passerelle, envoient des messages de canal Discord sortants, et lisent les messages de canal entrants via la CLI installée. Le mention-gating dispose également d'un scénario QA en direct, et la liaison ACP dispose d'un flux d'exécution au niveau de l'intégration qui prouve que le routage de session lié survit au tour suivant.

Le score s'arrête avant la stabilité car la liste de scénarios QA en direct elle-même enregistre les scénarios standard manquants pour `allowlist-block`, `top-level-reply-shape`, et `restart-resume`, et je n'ai pas trouvé de preuve E2E/en direct pour le routage de guild basé sur les rôles, le refus de liste blanche de canal, ou le comportement de fenêtre d'historique/contexte de thread. Ces domaines sont couverts dans la documentation, la source et les vérifications au niveau des unités, mais il n'existe pas suffisamment de preuves d'exécution pour les évaluer plus haut.

## Score de qualité

- Score : `Stable (84%)`

La qualité de l'implémentation est stable. La source utilise une résolution de politique de guild/canal explicite, par défaut la participation de guild vers le comportement de liste blanche, maintient `requireMention` activé par défaut sauf si une substitution de guild/canal le désactive, traite la correspondance de nom comme un comportement d'activation dangereux, utilise les ID de rôle pour la correspondance de route, résout les canaux parents pour les threads, et construit des clés de session déterministes par canal. Le contexte entrant traite les métadonnées de canal comme non fiables, et le chemin de contrôle préalable enregistre les messages de guild avec mention-gating ignorés comme historique de salle au lieu de perdre silencieusement le contexte.

Les risques de qualité sont principalement la complexité et les cas limites opérationnels, pas la quantité de tests manquante. L'admission, la résolution de route, le mention gating, les liaisons configurées, les liaisons à l'exécution, l'enregistrement d'historique et la construction de contexte sont répartis sur plusieurs modules Discord et de routage principal. Les preuves d'archive montrent également les frictions actuelles visibles par l'utilisateur dans ce domaine : les messages de canal de guild fonctionnant dans les DM mais pas dans les canaux, les messages de liste blanche étant silencieusement ignorés, les régressions de disponibilité de passerelle, les chutes de réponse de canal, et la divergence du harnais de session de groupe. La documentation avertit également explicitement que les listes blanches de canal sont des portes de déclenchement plutôt qu'une limite de rédaction universelle, donc l'isolation de contexte sécurisée dépend de la nouvelle machinerie de visibilité de contexte et de la configuration de l'opérateur.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/discord.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent l'étendue de la taxonomie pour l'admission de guild et de canal, le mention gating, l'isolation de clé de session, le routage configuré et à l'exécution, la visibilité du contexte entrant, les publications de threads de forum et de canal média, les actions de thread, l'analyse de cible, la résolution du contexte de thread, le routage de session lié au thread, le routage d'agent ACP, le cycle de vie du routage.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les listes QA en direct répertorient `allowlist-block`, `top-level-reply-shape`, et `restart-resume` comme des scénarios Discord standard manquants.
- Le routage de guild basé sur les rôles est bien spécifié et vérifié au niveau des unités, mais je n'ai pas trouvé de preuve directe en direct/E2E pour un rôle de membre causant un routage de canal de guild Discord vers un agent différent.
- Le comportement de fenêtre d'historique et d'événement de salle avec mention ignorée sont implémentés et vérifiés au niveau des unités, mais je n'ai pas trouvé de preuve en direct/E2E ou de résultats gitcrawl pour `historyLimit` sur les threads de canal Discord.
- Les archives Gitcrawl et discrawl montrent une confusion répétée de l'opérateur et des régressions autour de `groupPolicy`, `requireMention`, la disponibilité de la passerelle, les réponses de canal, et la sélection d'exécution de session de groupe.
- L'arbre de décision d'entrée local reste spécifique à Discord et complexe ; l'archive du mainteneur en direct contient un plan de refactorisation d'entrée de canal pour centraliser la sémantique de politique tout en gardant les faits de plateforme appartenant au plugin.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:215` documente la forme d'espace de travail de guilde recommandée, avec `groupPolicy: "allowlist"` et `requireMention` par guilde.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:285` indique que les canaux de guilde ne chargent pas automatiquement `MEMORY.md` et que chaque canal obtient sa propre session isolée.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:302` définit le modèle d'exécution, y compris les chats directs partageant le principal par défaut et les canaux de guilde utilisant des clés de session isolées `agent:<agentId>:discord:channel:<channelId>`.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:531` documente la politique de guilde `open`, `allowlist` et `disabled`, la ligne de base sécurisée, les listes blanches de canaux et le comportement de liste blanche de secours.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:577` documente le contrôle d'accès par mention, `requireMention` par guilde/canal, le comportement de réponse au bot et les valeurs par défaut des DM de groupe.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:599` documente le routage basé sur les rôles via `bindings[].match.roles`.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:736` documente les valeurs par défaut de l'historique de guilde, l'héritage de canal/thread, le routage de thread et l'avertissement selon lequel les listes blanches sont des portes de déclenchement plutôt qu'une limite de rédaction.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:760` et `/Users/kevinlin/code/openclaw/docs/channels/discord.md:809` documentent les sessions liées aux threads et les liaisons ACP persistantes.
- `/Users/kevinlin/code/openclaw/docs/channels/channel-routing.md:30` documente les formes de clé de session Discord, y compris les clés de canal et de thread isolées.
- `/Users/kevinlin/code/openclaw/docs/channels/channel-routing.md:75` documente la précédence des routes : pair, pair parent, guilde plus rôles, guilde, équipe, compte, canal, par défaut.
- `/Users/kevinlin/code/openclaw/docs/channels/groups.md:17` documente les valeurs par défaut de groupe, les exigences de mention et le comportement de réponse visible.
- `/Users/kevinlin/code/openclaw/docs/channels/groups.md:108` documente les limites de visibilité du contexte et note que les listes blanches ne créent pas une limite de rédaction universelle.
- `/Users/kevinlin/code/openclaw/docs/channels/access-groups.md:149` documente `discord.channelAudience` et son comportement de fermeture en cas d'échec lors de la recherche de membre ou de la correspondance de canal.

## Source

- `/Users/kevinlin/code/openclaw/extensions/discord/src/group-policy.ts:21` résout les entrées de politique de guilde et de canal, y compris la recherche de guilde consciente du compte et les remplacements de `requireMention` canal-sur-guilde.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.ts:360` résout les threads parents, les ID de rôle de membre, les liaisons configurées/d'exécution, les clés de session de base et l'état de route avant les vérifications d'accès.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.ts:450` refuse les messages de guilde lorsque la guilde n'est pas configurée ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.ts:531` applique `requireMention` ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.ts:543` bloque les membres non autorisés avant les travaux médias coûteux.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.ts:633` gère les décisions de mention/saut et enregistre l'historique en attente pour les messages de guilde contrôlés par mention.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.ts:767` retourne la route effective, la liaison, la liste blanche, la mention, l'historique et l'état d'événement entrant utilisés par la distribution.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight-channel-access.ts:10` évalue l'état désactivé du canal, les listes blanches DM de groupe, les listes blanches de canal configurées et l'admission `groupPolicy`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/allow-list.ts:56` normalise les entrées de liste blanche Discord ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/allow-list.ts:427` résout les configurations de canal/thread et le secours parent ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/allow-list.ts:529` applique la politique de liste blanche/désactivée.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.routing-preflight.ts:21` construit la route de conversation Discord avec l'ID de guilde, les rôles de membre, le pair et le pair parent.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/route-resolution.ts:28` appelle la résolution de route principale avec le canal Discord, la guilde, les rôles, le pair et le pair parent ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/route-resolution.ts:84` gère les clés de session liées.
- `/Users/kevinlin/code/openclaw/src/routing/resolve-route.ts:610` normalise les liaisons et les clés de session ; `/Users/kevinlin/code/openclaw/src/routing/resolve-route.ts:722` implémente l'ordre des niveaux de route.
- `/Users/kevinlin/code/openclaw/src/routing/session-key.ts:200` construit les clés de session directes et non directes ; les canaux Discord non directs utilisent `agent:<agentId>:<channel>:<peerKind>:<peerId>`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.context.ts:120` construit le contexte d'accès entrant avec les métadonnées de canal non fiables ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.context.ts:167` inclut l'historique de canal en attente ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.context.ts:212` gère le contexte de session du démarreur de thread et du parent ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.context.ts:321` construit le contexte d'événement entrant final.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/channel.conversation.ts:98` résout les ID de conversation de commande sur le canal actuel, le thread parent et la conversation entrante.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/outbound-session-route.ts:16` analyse les cibles Discord sortantes et retourne les détails de route/session conscients des threads.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/inbound-event-delivery.ts:26` sépare la corrélation d'événement de salle de la corrélation de livraison de message normale.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/acp-bind-here.integration.test.ts:133` exerce un flux d'exécution où une conversation Discord est liée à une session ACP et le tour suivant résout `boundSessionKey`, `boundAgentId` et l'état de route.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.test.ts:108` injecte la configuration Discord QA en direct avec `groupPolicy: "allowlist"`, `requireMention: true` par guilde/canal et une liste blanche d'utilisateurs.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.test.ts:195` configure un scénario outil uniquement/statut avec `requireMention: false` et des réponses visibles de l'outil de message.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.test.ts:288` inclut les scénarios en direct `discord-canary`, `discord-mention-gating` et commande/statut/thread/pièce jointe.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.test.ts:472` enregistre la couverture en direct standard actuelle comme canary plus mention-gating et répertorie `allowlist-block`, `top-level-reply-shape` et `restart-resume` comme manquants.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/live-smoke.live.test.ts:7` contrôle un smoke en direct Discord par rapport à `DISCORD_LIVE_TEST` et valide les métadonnées d'identité/passerelle du bot.
- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels/macos-discord.ts:27` configure une guilde/canal Discord VM avec `groupPolicy: "allowlist"` et `requireMention: false`, puis `/Users/kevinlin/code/openclaw/scripts/e2e/parallels/macos-discord.ts:48` effectue des allers-retours de canal sortants et entrants.
- `/Users/kevinlin/code/openclaw/scripts/openclaw-cross-os-release-checks.ts:2368` configure la politique de guilde/canal Discord de smoke de version, et `/Users/kevinlin/code/openclaw/scripts/openclaw-cross-os-release-checks.ts:2601` envoie sortant, attend la visibilité Discord, publie entrant, attend la relecture CLI installée et nettoie.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/src/routing/resolve-route.test.ts:348` vérifie la précédence de liaison de pair de canal Discord et la forme de clé de session.
- `/Users/kevinlin/code/openclaw/src/routing/resolve-route.test.ts:683` vérifie l'héritage de liaison de pair parent pour les conversations en thread.
- `/Users/kevinlin/code/openclaw/src/routing/resolve-route.test.ts:898` vérifie le routage guilde plus rôle, la spécificité, la précédence pair/parent, les rôles multiples et le secours guilde uniquement.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.test.ts:315` vérifie la résolution des exigences de mention.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.test.ts:1180` vérifie le comportement de commande non mentionnée autorisée sous `requireMention`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.test.ts:1387` et `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.test.ts:1423` vérifient le comportement de guilde et de thread en liste blanche lorsque les objets de guilde sont manquants.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.test.ts:1553` vérifie l'enregistrement des médias d'image locaux pour l'historique de guilde contrôlé par mention ignoré.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.test.ts:2010` vérifie que l'audio de guilde non autorisé n'est pas transcrit, et `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.preflight.test.ts:2070` vérifie la liaison configurée plus `requireMention`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/inbound-context.test.ts:10` vérifie le contexte d'accès de guilde à partir de la configuration et du sujet du canal.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/inbound-context.test.ts:71` vérifie la correspondance du contexte supplémentaire de l'expéditeur via les listes blanches de rôles.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/message-handler.inbound-context.test.ts:14` vérifie que les métadonnées de canal restent en dehors de `GroupSystemPrompt` et restent un contexte non fiable structuré.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/inbound-context.contract.test.ts:5` vérifie le contrat de contexte entrant Discord finalisé.

## Requêtes Gitcrawl

- `gitcrawl doctor --json` : correspondance `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594` et `repository_count=2`.
- `gitcrawl search openclaw/openclaw --query '"Discord" "groupPolicy" "requireMention" guild channel' --json` : a surfacé les problèmes ouverts pour les messages de canal ne fonctionnant pas tandis que les DM fonctionnent (#87753), les utilisateurs en liste blanche étant silencieusement ignorés (#79043), la passerelle READY ne se déclenchant jamais pour les messages de guilde (#79794) et les réponses de canal supprimées sous la configuration multi-agent allowlist/`requireMention: false` (#87157).
- `gitcrawl search openclaw/openclaw --query '"Discord" "sessionKey" "guild"' --json` : a surfacé la suppression de réponse de canal (#87157), la voix en tant qu'IO nécessitant des clés de session de route Discord (#73699), la discussion du hook de pré-routage pour les clés de session de canal canoniques (#81061) et le travail du hook d'activité entrant (#79855).
- `gitcrawl search openclaw/openclaw --query '"Discord" "bindings" "roles" guild' --json` : a surfacé un problème de routage/mention-gating impliquant les liaisons Discord configurées (#44502).
- `gitcrawl search openclaw/openclaw --query '"Discord" "historyLimit" thread channel' --json` : n'a retourné aucun résultat, ce qui soutient l'écart de preuve en direct de la fenêtre d'historique.

## Requêtes Discrawl

- `discrawl status --json` : fraîcheur demandée enregistrée ci-dessus ; la revérification locale avait le même état, les mêmes comptes, le même arriéré et partageait le distant avec un horodatage généré ultérieurement.
- `discrawl search --mode fts --limit 10 "discord requireMention"` : a montré les opérations de mainteneur en direct basculant `requireMention` guilde/canal, activant les événements de salle non mentionnés et discutant du comportement `allowBots: "mentions"` sûr pour les boucles de bot.
- `discrawl search --mode fts --limit 10 "discord groupPolicy"` : a montré les cas de support utilisateur où les DM fonctionnaient mais les sessions de groupe/canal Discord échouaient en raison de la divergence de route harnais/exécution, plus les exemples de configuration utilisant `groupPolicy: "allowlist"` et les listes blanches d'utilisateurs de guilde.
- `discrawl search --mode fts --limit 10 "discord guild session"` : a montré les références d'archive selon lesquelles les canaux de guilde utilisent des sessions isolées `agent:<agentId>:discord:channel:<channelId>`, plus les conseils de débogage pour le comportement spécifique aux threads, `requireMention`, les listes blanches et le routage de session.
- `discrawl search --mode fts --limit 10 "discord channel binding"` : a montré la discussion en direct des réponses de canal Discord fonctionnant dans un canal tandis qu'un agent/session spécifique ressemblait à un bug de routage ou de liaison de session, et un autre cas encadré comme un problème de configuration de liaison de canal/agent.
