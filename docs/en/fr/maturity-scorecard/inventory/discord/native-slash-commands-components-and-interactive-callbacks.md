---
title: "Discord - Native Controls and Approvals Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Discord - Native Controls and Approvals Maturity Note

## Résumé

Les commandes slash natives Discord, le sélecteur `/model`, les messages Components v2, les rappels de bouton/sélection/modal, les registres de rappel soutenus par TTL et l'autorisation de rappel sont implémentés et documentés dans l'extension Discord OpenClaw.

Les scores de couverture sont Stable car les tests de flux d'exécution et de style d'intégration exercent la distribution de commandes natives, l'authz, le routage, les liaisons ACP, le comportement de soumission/application du sélecteur de modèle, l'enregistrement d'envoi/édition de composants et la consommation de rappels. L'écart principal est la preuve e2e Discord en direct : le smoke en direct localisé ne prouve que l'identité du bot/métadonnées d'exécution, pas l'enregistrement de commande slash de bout en bout, l'interaction réelle du sélecteur ou l'exécution réelle du rappel de composant par rapport à Discord.

Les scores de qualité sont Beta car la forme source est en couches et défensive, mais les preuves d'archive actuelles montrent toujours des frictions actives spécifiques à Discord autour du déploiement de commandes slash, de l'enregistrement multi-compte, du timing d'accusé de réception de commande de plugin, des limites de sélecteur volumineux, de l'exposition du schéma de composant, des métadonnées de rappel manquantes et du timing d'interaction Discord.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Native Controls and Approvals`
- Fusionnée à partir de : `Native Commands and Components`, `Approvals and Sensitive Actions`
- Report de score : minimum conservateur des scores de catégorie source fusionnés.

## Portée de la catégorie

Inclus dans cette catégorie :

- Enregistrement de commande slash native : Enregistrement et réconciliation de commande slash native pour les commandes d'application Discord
- Exécution de commande slash native : Exécution de commande slash native, autocomplétion, authz et distribution d'interaction
- Commandes du sélecteur de modèle : Couvre les commandes du sélecteur de modèle dans l'enregistrement et la réconciliation de commande slash native pour les commandes d'application Discord. Exécution de commande slash native, autocomplétion, authz et distribution d'interaction. Flux du sélecteur `/model` et `/models`, et comportement des commandes slash natives, composants et rappels interactifs associés.
- Messages Components v2 : Messages Components v2, boutons, sélections de chaîne/utilisateur/rôle/mentionnable/canal, déclencheurs modaux et soumissions modales
- TTL de rappel : TTL de rappel, rappels réutilisables par rapport à usage unique, entrées de registre de rappel persistant, allowedUsers, authz guild/DM/groupe et distribution de rappel interactif de plugin
- Approbations natives Discord exec/plugin : Approbations natives Discord exec/plugin, y compris la résolution d'approbateur, le routage de cible dm/canal/les deux, l'autorisation du bouton d'approbation, la gestion des clics périmés/expirés, la résolution de passerelle et le comportement de route-notice/confidentialité
- Routage de commande sensible réservé au propriétaire pour les invites : Routage de commande sensible réservé au propriétaire pour les invites et les résultats finaux, en particulier /diagnostics et /export-trajectory
- Actions de message Discord : Actions de message Discord pour les messages, réactions, épingles, lectures/recherche, permissions, administration de canal/guild, changements de rôle, modération, événements programmés, statut vocal et présence
- Portes d'action sous channels.discord.actions._ : Portes d'action sous channels.discord.actions._, remplacements par compte, confiance du demandeur, vérifications de permission Discord basées sur senderUserId, vérifications de hiérarchie de rôle et liste blanche de cible de lecture

## Fonctionnalités

- Enregistrement de commande slash native : Enregistrement et réconciliation de commande slash native pour les commandes d'application Discord
- Exécution de commande slash native : Exécution de commande slash native, autocomplétion, authz et distribution d'interaction
- Commandes du sélecteur de modèle : Couvre les commandes du sélecteur de modèle dans l'enregistrement et la réconciliation de commande slash native pour les commandes d'application Discord. Exécution de commande slash native, autocomplétion, authz et distribution d'interaction. Flux du sélecteur `/model` et `/models`, et comportement des commandes slash natives, composants et rappels interactifs associés.
- Messages Components v2 : Messages Components v2, boutons, sélections de chaîne/utilisateur/rôle/mentionnable/canal, déclencheurs modaux et soumissions modales
- TTL de rappel : TTL de rappel, rappels réutilisables par rapport à usage unique, entrées de registre de rappel persistant, allowedUsers, authz guild/DM/groupe et distribution de rappel interactif de plugin

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Base de couverture : preuves d'intégration, e2e, en direct et de flux d'exécution uniquement.
- Signaux positifs : la distribution de commandes natives et l'authz sont exercés par des tests de flux d'exécution ciblés pour l'accès guild, DM, canal, les restrictions de propriétaire, les liaisons ACP, les sessions routées par secours, les commandes natives détenues par plugin, l'autocomplétion, la gestion des interactions expirées et la livraison de réponse de commande.
- Signaux positifs : le comportement du sélecteur `/model` est exercé par des tests de flux d'exécution couvrant l'affichage du sélecteur, l'application différée jusqu'à la soumission, la persistance d'exécution, la gestion du délai d'expiration, les récents, la vérification d'état par rapport aux sessions de thread liées et la persistance de remplacement de session obsolète.
- Signaux positifs : les composants et rappels ont une couverture de flux d'exécution pour l'enregistrement d'envoi/édition Components v2, la propagation TTL, l'enregistrement modal, la consommation de rappel de composant, les entrées persistantes, l'invalidation de frère usage unique et les API d'interaction de suivi/édition v2.
- Signaux positifs : les tests de couche de distribution couvrent le comportement de report de commande d'application, la gestion de l'autocomplétion, le comportement de report avant exécution de sous-commande et la gestion `with_components` de suivi/édition Components v2.
- Lacunes de couverture : aucun test e2e Discord en direct localisé n'invoque une commande slash réellement enregistrée, n'ouvre et ne soumet le sélecteur `/model` dans un guild/DM réel, ne clique sur un bouton/sélection v2 réel, ne soumet un modal réel ou ne vérifie l'authz/TTL de rappel par rapport à l'API Discord.
- Lacunes de couverture : le smoke Discord en direct localisé valide l'identité du bot et les métadonnées d'exécution uniquement ; la canary d'exécution Discord en direct QA est au niveau du transport et ne prouve pas les flux de rappel slash/composant de ce composant.
- Lacunes de couverture : aucun flux en direct localisé ne prouve l'enregistrement/réconciliation de commande slash sur les applications Discord par défaut et non par défaut, y compris le déploiement modifié uniquement, le déploiement désactivé ou le comportement de nettoyage de commande global/guild.

## Score de qualité

- Score : `Beta (76%)`
- Base de qualité : architecture source, comportement documenté, contrats d'exécution et preuves de problème opérationnel/archive actuelles. La couverture de test et l'absence de tests ne sont pas utilisés comme entrées de qualité.
- Bonnes qualités : l'implémentation sépare la définition de commande, le déploiement de commande, la distribution d'interaction, la construction de contexte de commande native, l'authz, l'état/vue/application du sélecteur de modèle, les constructeurs de composants, la persistance du registre, la plomberie d'envoi/édition et les rappels interactifs de plugin.
- Bonnes qualités : les commandes slash sont sérialisées avec des descriptions, localisations, options, types d'intégration, contextes et permissions de membre par défaut, puis réconciliées via des chemins de déploiement guild/devGuild/global avec des hachages de commande persistants.
- Bonnes qualités : l'exécution de commande native construit un contexte de session cible de commande explicite, supporte l'authz d'autocomplétion, préserve les métadonnées de route/session, contrôle l'accès via `commands.allowFrom`, politique de propriétaire/membre, appairage DM et vérifications de groupe DM, et gère les interactions expirées avant la distribution.
- Bonnes qualités : le sélecteur `/model` est délibérément stateful et limité par les limites de la plateforme Discord : ID personnalisés compressés, limites de ligne/bouton/option de sélection, pagination de fournisseur/modèle, vérifications d'interaction réservées au propriétaire, choix en attente et un chemin d'application `/model` caché avec délai d'expiration et vérification.
- Bonnes qualités : les rappels de composant utilisent des ID personnalisés structurés, des défauts TTL, des registres persistants, une sémantique de consommation réutilisable/usage unique, `allowedUsers`, des vérifications d'authz guild/DM/groupe, la gestion de soumission modale et des aides de contexte de rappel de plugin pour ack/reply/follow-up/edit/clear-components.
- Mauvaises qualités : gitcrawl montre que le déploiement de commande slash reste opérationnellement bruyant : les redémarrages peuvent redéployer les commandes et atteindre les limites de débit Discord, le mode de déploiement modifié uniquement/désactivé est toujours suivi et l'enregistrement de compte Discord non par défaut est toujours un problème ouvert.
- Mauvaises qualités : gitcrawl et discrawl montrent que le timing d'interaction reste un mode de défaillance Discord récurrent, en particulier les commandes slash de plugin manquant la fenêtre d'accusé de réception de 3 secondes Discord et les incidents historiques `Unknown interaction` dans des conditions d'écouteur lent ou de réseau.
- Mauvaises qualités : gitcrawl montre que le sélecteur de modèle a toujours une pression UX difficile des limites Discord de 25 options, 5 lignes et 100 caractères d'ID personnalisé ; discrawl confirme que le travail récent de performance et de pagination était toujours actif fin mai 2026.
- Mauvaises qualités : gitcrawl montre que les problèmes de qualité des composants restent actifs ou récemment actifs autour de l'exposition de composant native, de la surexposition du schéma de message, des champs de registre indéfinis, des métadonnées de rappel et du comportement de charge utile de composant/modal.
- Mauvaises qualités : la source gère de nombreux cas limites, mais la surface d'interaction est large et spécifique à Discord : enregistrement slash, distribution de commande de plugin, état du sélecteur, rappels, soumissions modales, expiration TTL et authz ont chacun des modes de défaillance séparés que les opérateurs rencontrent toujours.
- Exclu de la qualité : profondeur de test unitaire, profondeur de test d'intégration, profondeur de test en direct, profondeur de test de flux d'exécution et absence de tests spécifiques.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/discord.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'enregistrement de commande slash native, l'exécution de commande slash native, les commandes du sélecteur de modèle, les messages Components v2, le TTL de rappel.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacune connue utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une couverture e2e Discord en direct pour l'enregistrement de commande, l'invocation de commande, la soumission du sélecteur, le rappel de composant, la soumission modale, le refus de rappel non autorisé, l'expiration TTL et la persistance du rappel après redémarrage du processus.
- Résoudre ou fermer les problèmes actuels de déploiement/enregistrement slash couvrant le mode de déploiement modifié uniquement ou désactivé, la portée du cache de déploiement, l'enregistrement de compte non par défaut et les limites de débit de redéploiement de commande.
- Fermer l'écart d'accusé de réception slash de plugin afin que les commandes natives détenues par plugin accusent fiablement réception dans la fenêtre d'interaction de 3 secondes Discord.
- Continuer à renforcer les configurations de sélecteur de modèle volumineux autour des limites d'option, de ligne et d'ID personnalisé Discord, y compris le comportement visible par l'opérateur lorsque les listes de fournisseur/modèle dépassent le budget du sélecteur.
- Resserrer l'exposition du schéma de composant et les métadonnées de rappel afin que les charges utiles de composant générées restent explicites et que les gestionnaires de rappel reçoivent suffisamment de contexte sans surexposer les éléments internes spécifiques à Discord.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:313` documente les commandes slash natives comme des sessions de commande isolées avec la clé `CommandTargetSessionKey`.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:341` à `357` documente les conteneurs Components v2 interactifs, les limites de lignes d'action, les types de sélection, les contrôles à usage unique par rapport aux contrôles réutilisables, `allowedUsers`, le TTL par défaut de 30 minutes, le TTL maximum de 24 heures, et le comportement du sélecteur `/model` réservé au propriétaire.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:367` à `369` documente les formulaires modaux, les types de champs pris en charge, et le bouton déclencheur.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:625` à `638` documente l'activation des commandes natives, `commands.native=false`, les politiques d'authentification Discord partagées, les réponses non autorisées, et les réponses de commande éphémères par défaut.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1078` à `1105` documente les boutons d'approbation, la livraison ciblée DM/canal/les deux, l'interaction réservée à l'approbateur, le `/approve` de secours, la résolution d'approbation plugin par rapport à exec, et l'expiration de 30 minutes.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1135` à `1142` documente la configuration de l'interface utilisateur Components v2, `ui.components.accentColor`, `agentComponents.ttlMs`, et le comportement des intégrations avec les composants v2.
- `/Users/kevinlin/code/openclaw/docs/tools/slash-commands.md:64` à `72` documente `commands.native`, les compétences natives, et les spécifications de commandes Discord natives incluant les localisations de description.
- `/Users/kevinlin/code/openclaw/docs/tools/slash-commands.md:114` à `121` documente les sources de commandes : les éléments intégrés principaux, les commandes de dock, et le `registerCommand` du plugin.
- `/Users/kevinlin/code/openclaw/docs/tools/slash-commands.md:145` à `147` documente `/model` et `/models`.
- `/Users/kevinlin/code/openclaw/docs/tools/slash-commands.md:164` à `168` documente `/approve`.

## Source

- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/commands.ts:38` à `47` reporte les interactions de commande avec support éphémère.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/commands.ts:83` à `96` gère les options d'autocomplétion ciblées.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/commands.ts:98` à `134` sérialise les métadonnées de commande d'application natives, les localisations, les options, les types d'intégration, les contextes, et les permissions.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/commands.ts:160` à `188` distribue les sous-commandes et reporte avant l'exécution de la sous-commande.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/command-deploy.ts:41` à `99` déploie les commandes de guilde, de guilde de développement, et globales.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/command-deploy.ts:101` à `138` réconcilie les actions de création/édition/suppression de commandes avec les hachages persistants.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/client.ts:273` à `287` câble la liste/déploiement/réconciliation des commandes et la distribution des interactions dans le client Discord.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/interaction-dispatch.ts:43` à `115` distribue les interactions d'autocomplétion, de commande d'application, de composant de message, et de soumission modale.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/interactions.ts:153` à `247` enveloppe les interactions de rappel, réponse, report, édition, et suivi incluant les requêtes Components v2.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/provider.interactions.ts:33` à `70` construit les commandes natives à partir des spécifications de commande.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/provider.interactions.ts:105` à `157` enregistre les gestionnaires de composants de secours, les contrôles d'approbation exec, les contrôles de composants d'agent, et les rappels modaux.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.ts:89` à `197` crée les commandes natives Discord, analyse les options, reporte, et distribue l'exécution de la commande.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.ts:244` à `475` résout le contexte de l'expéditeur/canal et applique les listes blanches, l'authentification de groupe/DM, les vérifications de propriétaire, et les autorisateurs de commande.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.ts:477` à `600` exécute les commandes natives détenues par le plugin directement.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.ts:603` à `619` ouvre le sélecteur `/model` et `/models` lorsque la commande n'a pas d'arguments.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.ts:621` à `714` résout les cibles de session de commande native, construit l'état de route, et distribue les réponses de l'agent.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command-context.ts:41` à `108` construit le contexte de commande native incluant la session cible de commande, `From`, `To`, les métadonnées de groupe, `CommandTurn.kind="native"`, et la cible d'origine.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command-auth.ts:23` à `64` implémente `commands.allowFrom`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command-auth.ts:96` à `156` implémente l'authentification de commande de guilde via la politique de groupe, le propriétaire, et les autorisateurs de membre.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command-auth.ts:158` à `260` implémente l'authentification de groupe DM et d'autocomplétion.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command-agent-reply.ts:31` à `124` livre les réponses de commande native et les réponses de sélection de modèle vers Discord.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command-model-picker-ui.ts:64` à `81` détecte les formulaires de commande d'ouverture de sélecteur.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command-model-picker-ui.ts:179` à `340` résout le contexte du sélecteur, la route/modèle actuel, les récents, la page du fournisseur, et la réponse initiale.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command-model-picker-interaction.ts:265` à `333` analyse les interactions du sélecteur, vérifie l'accès réservé au propriétaire, reconnaît, résout l'état de route/données/courant, et met à jour le sélecteur.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command-model-picker-interaction.ts:473` à `657` gère les interactions de fournisseur, modèle, runtime, soumission, réinitialisation, et sélection rapide.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command-model-picker-apply.ts:76` à `183` distribue la commande `/model` cachée, vérifie les remplacements persistants/runtime, et enregistre les récents.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/model-picker.state.ts:6` à `15` définit les limites d'ID personnalisé, de ligne, de bouton, et d'option Discord.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/model-picker.state.ts:216` à `360` construit, limite, analyse, et valide les ID personnalisés du sélecteur.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/model-picker.view.ts:121` à `203` construit les boutons du sélecteur et les sélections compressées sous les limites d'option/ID personnalisé Discord.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/model-picker.view.ts:319` à `349` rend les lignes de sélection du fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/component-custom-id.ts:3` à `72` définit les clés d'ID personnalisé de composant/modal, l'analyse, et le mappage de registre avec caractères génériques.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/components.builders.ts:48` à `207` construit les composants de bouton et de sélection avec les données de rappel, les drapeaux réutilisables, et `allowedUsers`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/components.builders.ts:226` à `410` construit les messages de composant, les lignes d'action, les modaux, et les conteneurs v2.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/components-registry.ts:6` définit le TTL de rappel par défaut comme 30 minutes.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/components-registry.ts:124` à `157` crée des magasins clés persistants avec TTL et limites de taille.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/components-registry.ts:165` à `397` implémente l'expiration, la consommation à usage unique, l'enregistrement, la résolution de composant, et la résolution modale.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.components.ts:171` à `191` enregistre les messages de composant Discord construits avec le TTL configuré.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.components.ts:264` à `388` envoie et édite les messages de composant tout en enregistrant ou en actualisant les entrées du registre.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/agent-components.ts:54` à `69` enregistre les contrôles de composant d'agent, les contrôles de composant Discord, et les gestionnaires modaux.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/agent-components-guild-auth.ts:124` à `322` applique `allowedUsers`, l'authentification de guilde, et l'autorisation de commande de composant.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/agent-components-dm-auth.ts:22` à `135` applique l'authentification de composant DM et de groupe DM.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/agent-components.handlers.ts:27` à `298` gère les composants expirés, l'authz, la consommation à usage unique, la distribution de rappel de plugin, les événements d'agent synthétisés, l'authz de déclenchement modal, et l'affichage modal.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/agent-components.modal.ts:29` à `159` gère les soumissions modales manquantes/expirées, l'authz, les utilisateurs autorisés, la consommation, la distribution de plugin, et la distribution d'agent.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/agent-components.plugin-interactive.ts:24` à `172` définit l'entrée interactive du plugin et les aides de réponse/suivi/édition.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/agent-components.dispatch.ts:89` à `358` construit le contexte de rappel de composant et distribue les événements de clic/formulaire à l'agent et au chemin de réponse Discord.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/acp-bind-here.integration.test.ts:133` à `139` vérifie qu'un flux de liaison ACP Discord achemine le prochain tour DM Discord vers la liaison ACP existante.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.plugin-dispatch.test.ts:463` à `487` vérifie les commandes Discord natives de plugin soutenues par le registre et les alias via le chemin de commande native.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.plugin-dispatch.test.ts:524` à `535` vérifie les agents de liaison configurés pour les sessions de commande Discord détenues par le plugin.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.plugin-dispatch.test.ts:1122` à `1142` vérifie le routage slash natif via les liaisons de canal Discord ACP configurées.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.plugin-dispatch.test.ts:1144` à `1224` vérifie le secours vers les clés de session slash/canal routées lorsqu'aucune session liée n'existe.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.plugin-dispatch.test.ts:1226` à `1275` vérifie les liaisons ACP slash natives DM et que `/new` ne contourne pas la préparation ACP.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.plugin-dispatch.test.ts:1277` à `1292` vérifie que les commandes de récupération s'exécutent toujours via les liaisons ACP lorsque l'assurance échoue.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.commands-allowfrom.test.ts:138` à `143` vérifie l'authentification slash de guilde via `commands.allowFrom`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.commands-allowfrom.test.ts:263` à `370` vérifie les restrictions de canal, l'exclusion de membre, les restrictions de propriétaire, et le rejet de liste blanche.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.commands-allowfrom.test.ts:509` à `532` vérifie que les interactions slash expirées sont avalées avant la distribution lorsque le report retourne `Unknown interaction`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.model-picker.test.ts:357` à `387` vérifie que la sélection de modèle ne distribue pas jusqu'à la soumission.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.model-picker.test.ts:414` à `430` vérifie la persistance du runtime en dehors du pipeline `/model` caché.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.model-picker.test.ts:612` à `645` vérifie le statut de délai d'expiration et le comportement des récents.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.model-picker.test.ts:681` à `853` vérifie les récents, la vérification d'état par rapport aux sessions de fil liées, et la persistance de remplacement de session obsolète.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/interaction-dispatch.test.ts:15` à `125` vérifie le comportement de report de commande, la gestion de l'autocomplétion, et la distribution de report-avant-exécution de sous-commande.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/interactions.test.ts:50` à `82` vérifie que les appels de suivi et d'édition Components v2 utilisent `with_components`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.components.test.ts:103` à `173` vérifie l'enregistrement d'envoi de composant et la gestion du TTL.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.components.test.ts:220` à `257` vérifie l'enregistrement du déclenchement modal.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.components.test.ts:302` à `343` vérifie le comportement d'actualisation d'édition de composant.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/live-smoke.live.test.ts:12` vérifie uniquement l'identité/les métadonnées du bot en direct ; c'est une preuve en direct pour le transport Discord, mais pas pour les flux de rappel de slash/composant de ce composant.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.test.ts:9` et `473` à `476` définissent les scénarios de canari du runtime en direct Discord ; les scénarios situés sont au niveau du transport plutôt que les flux de rappel de slash natif/composant.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/discord/src/components.test.ts:28` à `60` vérifie les conteneurs v2 avec déclencheurs modaux et `allowedUsers`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/components.test.ts:98` à `116` vérifie les options de sélection modale et la validation de référence de pièce jointe.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/components.test.ts:131` à `191` vérifie le registre de composant et la consommation de frère à usage unique.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/components.test.ts:218` à `304` vérifie les entrées de composant et modal persistantes.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/components.test.ts:308` à `355` vérifie la suppression d'entrée persistante de frère lorsqu'un groupe est consommé.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/components.test.ts:355` à `380` vérifie le secours vers le registre en mémoire lorsque l'état persistant ne peut pas s'ouvrir.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/model-picker.test.ts:98` à `249` vérifie l'analyse d'ID personnalisé du sélecteur et l'application de la longueur maximale.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/model-picker.test.ts:265` à `383` vérifie la pagination du fournisseur/modèle et les plafonds d'option.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/model-picker.test.ts:474` à `1120` vérifie le rendu du fournisseur/modèle, la compression d'ID personnalisé, les sélections de modèle, les boutons de soumission, et le rendu du sélecteur de runtime.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/model-picker.test.ts:1240` à `1437` vérifie le rendu des récents.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/model-picker-preferences.test.ts:27` à `66` vérifie l'ordre des récents, le filtrage, et le secours de fichier corrompu.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/command-deploy.test.ts:16` vérifie le comportement d'égalité de commande pour la réconciliation de déploiement.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command.options.test.ts:214` à `506` vérifie le câblage d'option de commande native, l'authentification d'autocomplétion, la troncature, et les localisations.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command-context.test.ts:4` à `44` vérifie le contexte slash natif direct et de guilde.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/native-command-reply.test.ts:16` à `64` vérifie les réponses de commande native réservées aux composants.

## Requêtes Gitcrawl

Commandes :

```sh
gitcrawl search openclaw/openclaw --query "Discord native slash commands interaction dispatch" --json
gitcrawl search openclaw/openclaw --query "Discord model picker /model /models" --json
gitcrawl search openclaw/openclaw --query "Discord components v2 buttons select modal callback ttl" --json
gitcrawl search openclaw/openclaw --query "Discord component callback expired allowedUsers modal" --json
gitcrawl search openclaw/openclaw --query "Discord slash command registration cleanup commands.native" --json
gitcrawl search openclaw/openclaw --query "discord slash" --json
gitcrawl search openclaw/openclaw --query "discord components" --json
gitcrawl search openclaw/openclaw --query "discord model picker" --json
gitcrawl search openclaw/openclaw --query "agentComponents ttlMs" --json
gitcrawl search openclaw/openclaw --query "interaction expired discord" --json
gitcrawl search openclaw/openclaw --query "Discord modal payloads components" --json
gitcrawl search openclaw/openclaw --query "Discord INTERACTION_CREATE wildcard handler components v2" --json
gitcrawl search openclaw/openclaw --query "Discord components v2" --json
gitcrawl search openclaw/openclaw --query "Discord modal" --json
gitcrawl search openclaw/openclaw --query "Discord INTERACTION_CREATE" --json
```

Résultats :

- Les requêtes ciblées directes pour `"Discord native slash commands interaction dispatch"`, `"Discord components v2 buttons select modal callback ttl"`, `"Discord component callback expired allowedUsers modal"`, `"Discord slash command registration cleanup commands.native"`, `"agentComponents ttlMs"`, et `"Discord INTERACTION_CREATE wildcard handler components v2"` n'ont retourné aucun résultat, donc des requêtes Discord slash/composant/modèle/modal plus larges ont été nécessaires.
- `"discord slash"` a retourné des problèmes opérationnels actifs et des PR incluant `#75888 [discord] expose slashCommandDeploy mode in config (changed-only / disabled)`, `#39605 Discord/Telegram/Slack slash commands ignore session.dmScope routing`, `#39341 security audit doesn't check top-level channels.discord.allowFrom for slash commands`, `#77359 slash commands not registered for non-default Discord accounts in multi-bot setup`, `#73978 plugin slash commands miss 3s ack deadline / Unknown interaction`, `#79458 i18n fields for slash command descriptions`, `#69629 per-channel command visibility multi-bot`, `#51041 expose Discord slash interaction response controls to plugin commands`, et `#77367 scope command-deploy cache by application id`.
- `"discord model picker"` et `"Discord model picker /model /models"` ont retourné `#86182 discord/picker: structural 25-option / 5-row / 100-char limits constrain large wildcard configs`, plus les travaux connexes du sélecteur de modèle et du sélecteur de runtime tels que `#83573`, `#83805`, et `#82224`.
- `"discord components"`, `"Discord components v2"`, `"Discord modal"`, et `"Discord modal payloads components"` ont retourné des problèmes et des PR de composant/modal incluant `#73967 fix(discord): expose native components on message sends`, `#78813 feat(gateway): add components field to SendParamsSchema for Discord`, `#43015 message.send schema overexposes poll/components/modal causing GPT auto-population breakages`, `#85979 fix(discord): omit undefined component registry fields`, `#41805 Include interaction metadata in Discord button callbacks`, `#53641 attachment silently dropped with components`, et `#84937 minimal Discord /ask command`.
- `"interaction expired discord"` a retourné `#73978 plugin slash commands miss 3s ack deadline / Unknown interaction`, `#86716 harden reply delivery accounting`, et `#68538 timebox native-command defer before dispatch`.
- `"Discord INTERACTION_CREATE"` a retourné des preuves de synchronisation d'interaction historiques adjacentes, incluant des rapports d'auditeur lent et d'interaction Discord déjà reconnue.

## Requêtes Discrawl

Commandes :

```sh
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord slash commands"
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord model picker"
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord components"
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord modal"
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Unknown interaction Discord slash"
```

Résultats :

- `"Discord slash commands"` a retourné des rapports de mainteneur et d'utilisateur de mai 2026 sur les corrections de performance du sélecteur de modèle découvertes lors du test des commandes slash, le travail d'approbation CLI/slash, la désactivation des commandes slash de compétence native, le maximum de 100 commandes slash de Discord, les commandes slash bêta n'apparaissant pas, et les questions sur les commandes slash multi-agent/bot unique.
- `"Discord model picker"` a retourné la discussion de note de version de mai 2026 et de mainteneur autour du sélecteur de modèle Discord, incluant les corrections de fin mai, la pagination pour les pools de fournisseur/modèle au-dessus de 25 options, et les notes de version bêta pour les corrections du sélecteur de modèle.
- `"Discord components"` a retourné la discussion du mainteneur selon laquelle Discord a un chemin de message de composant plus riche et un registre dans `extensions/discord/src/send.components.ts`, plus les problèmes fermés pour la validation modale de l'outil de message, la gestion des caractères génériques INTERACTION_CREATE pour les boutons Components v2, la gestion des pièces jointes avec composants, et le comportement du registre de composant/modal partagé.
- `"Discord modal"` a retourné la discussion actuelle et historique de la charge modale, incluant le triage des problèmes de mai 2026 et les problèmes fermés d'avril 2026 pour la validation modale explicite, les charges interactives vides/par défaut normalisées, le registre modal partagé, et la gestion directe du déclenchement modal/showModal.
- `"Unknown interaction Discord slash"` a retourné des preuves de synchronisation d'interaction historiques et actuelles : les problèmes fermés pour le slash natif manquant `deferReply`, les sous-commandes slash expirées, les erreurs répétées `Interaction already acknowledged`, la synchronisation de l'auditeur lent autour de la fenêtre de 3 secondes de Discord, et les préoccupations concernant la reconnaissance de la commande slash du plugin.
