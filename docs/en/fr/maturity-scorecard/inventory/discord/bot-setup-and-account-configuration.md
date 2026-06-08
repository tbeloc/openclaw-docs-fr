---
title: "Discord - Note de Maturité de Configuration et Opérations de Canal"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Discord - Note de Maturité de Configuration et Opérations de Canal

## Résumé

La configuration du bot Discord et la configuration du compte sont utilisables pour le chemin normal à bot unique et disposent de documentation approfondie, de sources conscientes du compte, de sondes d'exécution et d'une couverture QA en direct. Le composant n'est pas Stable car les preuves d'archive actuelles montrent une confusion répétée des opérateurs et des régressions actives autour de l'activation des plugins, de la résolution de l'ID d'application, des SecretRefs de compte nommé et de l'enregistrement de commandes multi-compte.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Configuration et Opérations de Canal`
- Fusionnée à partir de : `Configuration et Exécution`
- Report de score : minimum conservateur des scores de catégorie source fusionnés.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Configuration de l'application et du bot : Couvre la configuration de l'application et du bot sur les conseils de création d'application/bot Discord, la configuration du jeton bot et `applicationId`, la résolution des jetons env et SecretRef, l'assistant de configuration/inspection de compte et le comportement de configuration de bot et de compte associé.
- Configuration du jeton et de l'ID d'application : Couvre la configuration du jeton et de l'ID d'application sur les conseils de création d'application/bot Discord, la configuration du jeton bot et `applicationId`, la résolution des jetons env et SecretRef, l'assistant de configuration/inspection de compte et le comportement de configuration de bot et de compte associé.
- Assistant de configuration et inspection de compte : Couvre l'assistant de configuration et l'inspection de compte sur les conseils de création d'application/bot Discord, la configuration du jeton bot et `applicationId`, la résolution des jetons env et SecretRef, l'assistant de configuration/inspection de compte et le comportement de configuration de bot et de compte associé.
- Vérifications de statut, docteur et intention : Couvre les vérifications de statut, docteur et intention sur les conseils de création d'application/bot Discord, la configuration du jeton bot et `applicationId`, la résolution des jetons env et SecretRef, l'assistant de configuration/inspection de compte et le comportement de configuration de bot et de compte associé.
- Configuration de bot multi-compte : Couvre la configuration de bot multi-compte sur les conseils de création d'application/bot Discord, la configuration du jeton bot et `applicationId`, la résolution des jetons env et SecretRef, l'assistant de configuration/inspection de compte et le comportement de configuration de bot et de compte associé.
- Démarrage du moniteur de compte : Couvre le démarrage du moniteur de compte sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement du moniteur de passerelle et du cycle de vie d'exécution associé.
- Cycle de vie de la passerelle WebSocket : Couvre le cycle de vie de la passerelle WebSocket sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement du moniteur de passerelle et du cycle de vie d'exécution associé.
- Gestion de la reconnexion et du battement cardiaque : Couvre la gestion de la reconnexion et du battement cardiaque sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement du moniteur de passerelle et du cycle de vie d'exécution associé.
- Limites de débit et métadonnées de passerelle : Couvre les limites de débit et les métadonnées de passerelle sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement du moniteur de passerelle et du cycle de vie d'exécution associé.
- Récupération de statut, sonde et moniteur de santé : Couvre la récupération de statut, sonde et moniteur de santé sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement du moniteur de passerelle et du cycle de vie d'exécution associé.

## Fonctionnalités

- Configuration de l'application et du bot : Couvre la configuration de l'application et du bot sur les conseils de création d'application/bot Discord, la configuration du jeton bot et `applicationId`, la résolution des jetons env et SecretRef, l'assistant de configuration/inspection de compte et le comportement de configuration de bot et de compte associé.
- Configuration du jeton et de l'ID d'application : Couvre la configuration du jeton et de l'ID d'application sur les conseils de création d'application/bot Discord, la configuration du jeton bot et `applicationId`, la résolution des jetons env et SecretRef, l'assistant de configuration/inspection de compte et le comportement de configuration de bot et de compte associé.
- Assistant de configuration et inspection de compte : Couvre l'assistant de configuration et l'inspection de compte sur les conseils de création d'application/bot Discord, la configuration du jeton bot et `applicationId`, la résolution des jetons env et SecretRef, l'assistant de configuration/inspection de compte et le comportement de configuration de bot et de compte associé.
- Vérifications de statut, docteur et intention : Couvre les vérifications de statut, docteur et intention sur les conseils de création d'application/bot Discord, la configuration du jeton bot et `applicationId`, la résolution des jetons env et SecretRef, l'assistant de configuration/inspection de compte et le comportement de configuration de bot et de compte associé.
- Configuration de bot multi-compte : Couvre la configuration de bot multi-compte sur les conseils de création d'application/bot Discord, la configuration du jeton bot et `applicationId`, la résolution des jetons env et SecretRef, l'assistant de configuration/inspection de compte et le comportement de configuration de bot et de compte associé.
- Démarrage du moniteur de compte : Couvre le démarrage du moniteur de compte sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement du moniteur de passerelle et du cycle de vie d'exécution associé.
- Cycle de vie de la passerelle WebSocket : Couvre le cycle de vie de la passerelle WebSocket sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement du moniteur de passerelle et du cycle de vie d'exécution associé.
- Gestion de la reconnexion et du battement cardiaque : Couvre la gestion de la reconnexion et du battement cardiaque sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement du moniteur de passerelle et du cycle de vie d'exécution associé.
- Limites de débit et métadonnées de passerelle : Couvre les limites de débit et les métadonnées de passerelle sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement du moniteur de passerelle et du cycle de vie d'exécution associé.
- Récupération de statut, sonde et moniteur de santé : Couvre la récupération de statut, sonde et moniteur de santé sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement du moniteur de passerelle et du cycle de vie d'exécution associé.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (74%)`
- Signaux positifs : Des voies Discord en direct réelles existent. La voie de transport QA en direct nécessite des ID de guilde/canal réels, des jetons de pilote et de SUT bot, et un ID d'application SUT, injecte `plugins.entries.discord.enabled`, `channels.discord.enabled`, un jeton de compte nommé, `defaultAccount`, des listes blanches de guilde/canal, puis démarre une passerelle et attend que le compte de canal Discord SUT s'exécute avant d'exercer l'enregistrement de commande canary, mention gating et natif. Une fumée en direct séparée vérifie un jeton bot réel contre les métadonnées Discord REST et de passerelle.
- Signaux négatifs : Les voies en direct couvrent une configuration QA organisée, pas le chemin de configuration humain complet du Portail des Développeurs via `openclaw config patch`, `openclaw channels add`, les invites de l'assistant de configuration, la propagation de l'env de service et `openclaw doctor --fix`. Il n'y a pas de preuve en direct large dans les preuves pour la parité de commande slash multi-compte, la parité d'envoi/recherche SecretRef de compte nommé ou le cas de plugin-entry désactivé silencieux.
- Lacunes d'intégration : Ajouter un scénario de configuration en direct qui commence à partir d'une configuration documentée minimale, vérifie le comportement d'activation des plugins, vérifie le repli `applicationId` et `applicationId` configuré, exécute les actions d'envoi et de recherche SecretRef env de compte nommé et affirme que `channels status --probe` affiche les intentions et permissions manquantes dans le langage orienté opérateur.

## Score de Qualité

- Score : `Beta (71%)`
- Rapports Gitcrawl : Les rapports ouverts actuels incluent #83212 pour un canal Discord restant désactivé sans avertissement sauf si `plugins.entries.discord.enabled` est défini, #77359 pour les commandes slash manquantes sur les comptes Discord non par défaut malgré un `applicationId` valide par compte, #87656 et #84530 pour les incompatibilités de résolution SecretRef env de compte nommé sur le démarrage du fournisseur, les envois et les actions de recherche/admin, #77429 pour un ordre de démarrage multi-compte confus, #53198 pour un repli de liste blanche documentée et élevée ne fonctionnant pas pour Discord et #79043 pour les utilisateurs en liste blanche étant silencieusement ignorés tandis que le propriétaire du bot est implicitement injecté.
- Rapports Discrawl : La discussion d'archive Discord répète la même douleur de l'opérateur : les fils de configuration du bot mentionnent la saisie bloquée, la résolution d'ID d'application échouée, les boucles de réinitialisation/reconfiguration de jeton, le besoin de définir manuellement `plugins.entries.discord.enabled true`, les listes de contrôle d'intention Message Content/Server Members répétées et les rapports « en attente de disponibilité de la passerelle » malgré la présence visible du bot et les intentions activées. La discussion Discord spécifique à SecretRef n'avait pas de résultats directs dans l'archive Discord interrogée, donc le signal de qualité SecretRef provient de gitcrawl.
- Bonnes qualités : La documentation publique donne un flux de configuration détaillé pour la création de bot, les intentions privilégiées, les portées d'invitation OAuth, les ID en mode développeur, la configuration de jeton sécurisée, la propagation de l'env de service, l'appairage, les comptes multi-bot, les ID d'application, la précédence des jetons, la gestion des jetons en double, la politique DM, la politique de guilde, le dépannage et la référence de configuration. La source a un état de configuration conscient du compte, l'inspection de précédence des jetons et SecretRef, la sélection d'instantané de configuration d'exécution, le filtrage du propriétaire de jeton en double, l'analyse de l'ID d'application avant le repli REST, la sonde d'intention privilégiée, les problèmes d'état d'audit des permissions, la réparation du docteur d'ID numérique et la journalisation de phase de démarrage.
- Mauvaises qualités : L'alignement docs/source est toujours fragile autour de l'activation des plugins car la configuration rapide affiche `channels.discord.enabled` et la configuration des jetons tandis que les preuves d'archive montrent que les opérateurs peuvent toujours avoir besoin de `plugins.entries.discord.enabled`. Le comportement des jetons de compte nommé est incohérent sur les surfaces d'exécution. Le comportement multi-compte est implémenté mais a toujours des lacunes de produit visibles autour de l'enregistrement des commandes et de l'ordre de démarrage. Certains modes de défaillance sont silencieux ou trop indirects pour les opérateurs, en particulier l'état du plugin désactivé, les jetons de compte non résolus dans les chemins d'action, les chutes de liste blanche et les blocages de disponibilité de la passerelle.
- Exclu de la qualité : La présence/profondeur des tests unitaires, d'intégration, e2e, en direct et les tests absents n'ont pas été utilisés pour augmenter ou diminuer ce score de Qualité.

## Score de Complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/discord.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent l'étendue de la taxonomie pour la configuration de l'application et du bot, la configuration du jeton et de l'ID d'application, l'assistant de configuration et l'inspection de compte, les vérifications de statut, de doctor et d'intention, la configuration de bot multi-compte, le démarrage du moniteur de compte, le cycle de vie de la passerelle WebSocket, la gestion de la reconnexion et du battement cardiaque, les limites de débit et les métadonnées de passerelle, la récupération du statut, de la sonde et du moniteur de santé.
- Signaux négatifs : la note archivée a précédé le score de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Rendre impossible la dérive entre la configuration de démarrage rapide documentée et le contrat d'activation réel du plugin : soit activer implicitement le plugin Discord à partir de `channels.discord.enabled`, soit documenter et valider `plugins.entries.discord.enabled` dans le même flux.
- Normaliser la résolution de SecretRef d'env de compte nommé afin que le démarrage du fournisseur, les envois visibles, les actions de recherche/message d'administration et les sondes de statut consomment tous le même état de compte résolu à l'exécution.
- Ajouter des avertissements de démarrage/statut explicites pour les entrées de registre de plugin désactivées, les SecretRefs non résolus, les intentions privilégiées manquantes ou limitées, les commandes natives non enregistrées sur les comptes secondaires et les suppressions de liste d'autorisation.
- Prioriser le `channels.discord.defaultAccount` configuré lors du démarrage multi-compte, ou rendre l'ordre explicite dans la sortie de statut.
- Améliorer l'UX de configuration pour les défaillances d'ID d'application : la source actuelle peut analyser les ID à partir de jetons ou les récupérer, mais les preuves d'archive montrent que les utilisateurs rencontrent toujours des boucles opaques « Impossible de résoudre l'ID d'application Discord ».

## Preuves

### Docs

- `docs/channels/discord.md` : « Quick setup » explique la création d'une application Discord et d'un bot, l'activation des intents Message Content/Server Members/Presence, la copie du token du bot, les scopes OAuth/permissions d'invitation, les IDs en mode développeur, la confidentialité des DM, la configuration sécurisée du token SecretRef, les conseils de secours `applicationId`, la configuration CLI/config, l'approbation d'appairage, les `accounts` multi-bot, la précédence des tokens, la gestion des tokens en doublon, les politiques d'accès DM/guild, le dépannage et la référence de configuration.
- `docs/plugins/reference/discord.md` : la référence du plugin identifie `@openclaw/discord`, la distribution npm/ClawHub, la surface de canal `discord` et la documentation associée.
- `docs/install/fly.md` et `docs/start/setup.md` : les docs de déploiement/configuration mentionnent `DISCORD_BOT_TOKEN` comme credential de canal et expliquent le placement du token soutenu par env dans les configurations hébergées ou de développement.
- `docs/tools/slash-commands.md` : documente les valeurs par défaut d'enregistrement de commandes natives Discord et l'impact de `commands.native=false`.

### Source

- `extensions/discord/openclaw.plugin.json` : déclare l'id/nom/description du plugin, `channels: ["discord"]` et `channelEnvVars.discord: ["DISCORD_BOT_TOKEN"]`.
- `extensions/discord/src/setup-core.ts` et `extensions/discord/src/setup-surface.ts` : définissent l'assistant de configuration Discord, les invites de credential de token, la variable env préférée `DISCORD_BOT_TOKEN`, la politique DM scoped au compte, la liste d'autorisation de groupe, les invites allow-from et la résolution de liste d'autorisation utilisateur/canal en direct quand un token est disponible.
- `extensions/discord/src/setup-account-state.ts`, `extensions/discord/src/account-inspect.ts`, `extensions/discord/src/token.ts` et `extensions/discord/src/accounts.ts` : implémentent l'énumération de compte, la résolution de `defaultAccount`, la précédence de token racine/compte, le secours env pour défaut uniquement, l'inspection SecretRef, la sélection de snapshot d'exécution, la configuration de compte fusionnée, le filtrage du propriétaire de token en doublon et le rapport de raison désactivée.
- `extensions/discord/src/probe.ts` : sonde Discord REST, résume les intents privilégiés à partir des drapeaux d'application, dérive les IDs d'application à partir des tokens de bot avant la recherche REST et récupère les IDs d'application avec gestion du rate-limit.
- `extensions/discord/src/channel.ts` et `extensions/discord/src/monitor/provider.ts` : câblent les sondes de statut, les audits de permission, les snapshots de compte, le comportement fail-fast de SecretRef avant le démarrage du fournisseur, l'échelonnement du démarrage, le démarrage du fournisseur Discord, l'avertissement de secours de politique de groupe, la résolution d'ID d'application, l'enregistrement de commande et le statut du cycle de vie.
- `extensions/discord/src/status-issues.ts`, `extensions/discord/src/doctor.ts` et `extensions/discord/src/security-doctor.ts` : surface l'Intent Message Content manquant, les échecs d'audit de permission, les IDs de canal non résolus, la réparation d'ID numérique, les avertissements de token env manquant et les avertissements d'entrée de liste d'autorisation mutable.
- `src/plugin-sdk/discord.ts` : la façade de compatibilité exporte les assistants de configuration/statut/compte Discord et les méthodes d'exécution utilisées par le câblage Discord fourni.

### Tests d'intégration

- `extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts` : l'exécution QA en direct nécessite des IDs réels de guild/canal Discord, un token de bot du pilote, un token de bot SUT et un ID d'application SUT ; construit une configuration de passerelle avec `plugins.entries.discord.enabled`, `channels.discord.enabled`, `defaultAccount`, token de compte nommé, listes d'autorisation de guild/canal, puis démarre une passerelle en direct, attend que le compte de canal Discord s'exécute, vérifie l'identité SUT et exerce le canary Discord, le gating par mention, l'enregistrement de commande d'aide native, plus les scénarios optionnels de voix/statut/thread.
- `extensions/qa-lab/src/live-transports/discord/discord-live.runtime.test.ts` : valide le contrat d'environnement QA Discord en direct, l'analyse de charge utile de credential, la validation de flocon de neige et la forme de configuration de compte Discord injectée utilisée par l'exécution en direct.
- `extensions/discord/src/internal/live-smoke.live.test.ts` : la fumée en direct contrôlée utilise `DISCORD_BOT_TOKEN` et `DISCORD_LIVE_TEST` pour appeler Discord REST pour l'identité du bot et les métadonnées de passerelle, et vérifie que l'ID d'application dérivé du token correspond à l'utilisateur du bot.

### Tests unitaires

- `extensions/discord/src/setup-surface.test.ts` : couvre la politique DM de compte nommé, les clés de configuration scoped au compte, les écritures de politique ouverte, la sélection de defaultAccount de l'état configuré et les écritures de liste d'autorisation de guild/canal.
- `extensions/discord/src/setup-account-state.test.ts` : couvre les IDs de compte de configuration normalisés, la résolution de configuration de compte, le compte par défaut configuré, les tokens de compte vides explicites et l'état de token de compte SecretRef non résolu.
- `extensions/discord/src/token.test.ts` : couvre la précédence config-over-env, le secours env, la précédence de token de compte, les tokens de compte vides explicites empêchant le secours, la résolution SecretRef de snapshot d'exécution et les SecretRefs configurés-indisponibles.
- `extensions/discord/src/accounts.test.ts` : couvre le comportement d'omission de defaultAccount, la précédence de allowFrom, la précédence de fusion de configuration de compte, le filtrage de token en doublon, la sélection de configuration d'exécution et la préservation de token configurée-indisponible.
- `extensions/discord/src/config-schema.test.ts` : couvre les valeurs par défaut sécurisées telles que `dmPolicy="open"` nécessitant `allowFrom: ["*"]`, la politique de groupe par défaut à liste d'autorisation, l'acceptation/rejet d'ID d'application, la coercition/rejet d'ID numérique et les champs de configuration scoped au compte.
- `extensions/discord/src/probe.intents.test.ts` et `extensions/discord/src/probe.parse-token.test.ts` : couvrent l'interprétation du drapeau d'intent privilégié, la dérivation d'ID d'application à partir de tokens, la préservation de flocon de neige volumineux et la gestion du rate-limit Cloudflare lors de la recherche d'ID d'application.
- `extensions/discord/src/channel.test.ts`, `extensions/discord/src/monitor/provider.test.ts`, `extensions/discord/src/monitor/provider.startup.test.ts`, `extensions/discord/src/monitor/provider.lifecycle.test.ts`, `extensions/discord/src/monitor/gateway-plugin.test.ts`, `extensions/discord/src/monitor/gateway-supervisor.test.ts` et `extensions/discord/src/monitor/startup-status.test.ts` : couvrent les sondes de démarrage, le comportement fail-fast de SecretRef non résolu, la journalisation de phase de démarrage, la préférence de résolution d'ID d'application, la classification de cycle de vie/reconnexion/erreur de passerelle, la configuration de file d'attente d'événement, le gating d'intent de voix et la formulation de statut.
- `extensions/discord/src/doctor.test.ts` et `extensions/discord/src/security-doctor.test.ts` : couvrent la migration/réparation de configuration, les avertissements et réparations d'ID numérique, les avertissements de token env manquant et la détection d'entrée de liste d'autorisation mutable.
- `src/plugin-sdk/discord.test.ts` : couvre les exports de façade SDK Discord dépréciés et le transfert d'exécution utilisés par le câblage de plugin fourni.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues discord --repo openclaw/openclaw --limit 5 --json number,title,state,updatedAt,url`

Résultats :

- A retourné les problèmes pertinents pour la configuration/compte ouverts #53198, #83212, #87656 et #77429 parmi les principaux résultats Discord. #81107 concernait une boucle CPU de commande de compétence Discord et a été traité comme preuve de qualité d'exécution adjacente, non comme preuve de configuration de compte/configuration.

Requête :

`gitcrawl search issues "Discord setup bot token applicationId" --repo openclaw/openclaw --limit 10 --json number,title,state,updatedAt,url`

Résultats :

- A retourné #77359, un rapport multi-bot ouvert où un compte Discord secondaire avait un token valide, un `applicationId` par compte et un chat fonctionnant, mais aucune commande slash enregistrée et aucune erreur de démarrage visible.

Requête :

`gitcrawl search issues "Discord plugins.entries enabled setup disabled warning" --repo openclaw/openclaw --limit 10 --json number,title,state,updatedAt,url`

Résultats :

- A retourné #83212, un rapport ouvert que `channels.discord.enabled: true` avec un token valide peut toujours laisser Discord « installé, non configuré, désactivé » sans journaux à moins que `plugins.entries.discord.enabled` ne soit également défini. Un problème de boucle de redémarrage Docker non lié a été ignoré.

Requête :

`gitcrawl search issues "Discord multi-account token default account applicationId" --repo openclaw/openclaw --limit 10 --json number,title,state,updatedAt,url`

Résultats :

- A retourné #77359 à nouveau, confirmant que le problème d'enregistrement de commande/`applicationId` multi-compte est le problème actuel principal pour cette requête. `gitcrawl gh issue view 77429` a également été lu car la requête Discord plus large a surfacé un problème de startup-order de compte par défaut connexe.

Requête :

`gitcrawl search issues "Discord SecretRef named account token" --repo openclaw/openclaw --limit 10 --json number,title,state,updatedAt,url`

Résultats :

- A retourné #87656 et #84530. Les deux sont des rapports SecretRef de compte nommé ouverts : l'un dit que le démarrage du fournisseur réussit tandis que l'envoi de l'outil de message échoue, et l'autre dit que la recherche/admin `channel-info` échoue tandis que le comportement d'entrée/envoi fonctionne dans le même exécution.

Requête :

`gitcrawl search issues "Discord Message Content Intent privileged intents setup" --repo openclaw/openclaw --limit 10 --json number,title,state,updatedAt,url`

Résultats :

- A retourné #79043, un rapport ouvert où les intents Message Content et Server Members étaient activés mais un utilisateur autorisé a été silencieusement ignoré et l'allowlisting implicite du propriétaire du bot a confondu le diagnostic d'exécution.

Lecture de détail de problème supplémentaire :

- `gitcrawl gh issue view 83212`, `77359`, `87656`, `84530`, `77429`, `53198` et `79043` ont été lus pour les résumés, les étapes, le comportement attendu/réel, les environnements et l'impact de l'opérateur.

### Requêtes Discrawl

Requête :

`discrawl search "Discord bot token setup applicationId" --limit 10`

Résultats :

- A retourné un fil de configuration de mars où le bot était en ligne mais bloqué en train de taper, les journaux affichaient « Failed to resolve Discord application id », l'ajout de `applicationId` a causé une erreur de clé non reconnue avant la réparation du docteur, une réinitialisation de token a été tentée et le symptôme a persisté après la mise à jour. A également retourné une liste de contrôle de configuration d'ID d'application plus ancienne mettant l'accent sur les permissions d'invitation du bot, l'Intent Server Members, l'Intent Message Content, la configuration et le redémarrage de la passerelle.

Requête :

`discrawl search "plugins.entries.discord.enabled" --limit 10`

Résultats :

- A retourné plusieurs messages d'opérateur/aide où Discord n'est pas venu en ligne ou est resté désactivé jusqu'à ce que les utilisateurs définissent manuellement `plugins.entries.discord.enabled: true`, y compris une recommandation de commande explicite et des configurations montrant `plugins.entries.discord.enabled` basculé faux/vrai. Cela corrobore la confusion d'activation de plugin de #83212.

Requête :

`discrawl search "Discord multi account applicationId" --limit 10`

Résultats :

- A retourné un commentaire/examen de PR OpenClaw sur la propriété de réclamation de canal multi-compte utilisant la mauvaise clé de bot dans les configurations de guild/canal partagées. Aucun fil de configuration d'utilisateur large n'a été retourné pour cette requête exacte, donc le signal principal de configuration/compte multi-compte reste gitcrawl #77359 et #77429.

Requête :

`discrawl search "Discord SecretRef named account token" --limit 10`

Résultats :

- N'a retourné aucun résultat direct d'archive Discord. C'est neutre après les vérifications de fraîcheur réussies ; gitcrawl a fourni la preuve de régression SecretRef concrète.

Requête :

`discrawl search "Discord Message Content Intent setup" --limit 10`

Résultats :

- A retourné plusieurs fils de configuration/aide répétant les exigences d'Intent Message Content et Server Members Intent, les explications `intents:content=limited`, un rapport « awaiting gateway readiness » bloqué malgré l'activation de tous les trois intents privilégiés, et un commentaire/problème OpenClaw sur la configuration guidée disant que Discord n'était pas activé et ignorant l'entrée de token.
