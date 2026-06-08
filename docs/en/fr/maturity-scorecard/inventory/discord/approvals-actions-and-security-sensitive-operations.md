---
title: "Discord - Approvals and Sensitive Actions Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Discord - Approvals and Sensitive Actions Maturity Note

## Summary

Discord dispose d'un modèle de sécurité au niveau du code source solide pour les approbations exec/plugin natives et les actions de canal privilégiées, mais la preuve externe est inégale. Les documents d'implémentation appliquent et renforcent les boutons d'approbation réservés aux approbateurs, la confidentialité du propriétaire en priorité aux MP, les portes d'action par compte, les vérifications de permissions Discord pour les modifications d'administration/modération pilotées par l'expéditeur, et les listes blanches de cibles de lecture. La couverture reste Alpha car le contrôle qualité Discord en direct situé couvre les flux de canal adjacents, pas la livraison d'approbation native sur `dm`/`channel`/`both` ou l'exécution réelle d'actions privilégiées. La qualité est Beta car la conception est défendable, mais les preuves d'archive ouvertes et récentes montrent toujours des régressions de livraison d'approbation, des défaillances d'approbation-client TLS local, des changements de route-notice/token-boundary, une porte d'action de message destructif grossière, et des lacunes antérieures en matière d'autorisation d'action d'administration.

## Category Scope

Inclus dans cette catégorie :

- Approbations exec/plugin Discord natives : Approbations exec/plugin Discord natives, y compris la résolution des approbateurs, le routage des cibles dm/channel/both, l'autorisation des boutons d'approbation, la gestion des clics périmés/expirés, la résolution de la passerelle, et le comportement de route-notice/confidentialité
- Routage de commande réservé au propriétaire pour les invites : Routage de commande réservé au propriétaire pour les invites et les résultats finaux, en particulier /diagnostics et /export-trajectory
- Actions de message Discord : Actions de message Discord pour les messages, réactions, épingles, lectures/recherche, permissions, administration de canal/guilde, changements de rôle, modération, événements programmés, statut vocal et présence
- Portes d'action sous channels.discord.actions._ : Portes d'action sous channels.discord.actions._, remplacements par compte, confiance du demandeur, vérifications de permissions Discord basées sur senderUserId, vérifications de hiérarchie de rôle, et listes blanches de cibles de lecture

## Features

- Approbations exec/plugin Discord natives : Approbations exec/plugin Discord natives, y compris la résolution des approbateurs, le routage des cibles dm/channel/both, l'autorisation des boutons d'approbation, la gestion des clics périmés/expirés, la résolution de la passerelle, et le comportement de route-notice/confidentialité
- Routage de commande réservé au propriétaire pour les invites : Routage de commande réservé au propriétaire pour les invites et les résultats finaux, en particulier /diagnostics et /export-trajectory
- Actions de message Discord : Actions de message Discord pour les messages, réactions, épingles, lectures/recherche, permissions, administration de canal/guilde, changements de rôle, modération, événements programmés, statut vocal et présence
- Portes d'action sous channels.discord.actions._ : Portes d'action sous channels.discord.actions._, remplacements par compte, confiance du demandeur, vérifications de permissions Discord basées sur senderUserId, vérifications de hiérarchie de rôle, et listes blanches de cibles de lecture

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Alpha (58%)`
- Positive signals:
  - Discord dispose d'un runtime QA en direct avec un inventaire de scénarios Discord réels pour canary, mention gating, enregistrement de commande d'aide native, réactions de statut, auto-join vocal, et flux d'attachement de thread.
  - Les tests e2e d'approbation de passerelle partagée prouvent qu'une approbation de passerelle réelle peut être demandée et résolue sur des connexions WebSocket séparées, et les tests e2e du client d'approbation d'opérateur couvrent l'autorité d'exécution d'approbation générée-locale par rapport à la boucle de retour distante.
  - Les tests d'exécution local exercent la normalisation des cibles d'approbation Discord, le ciblage de thread, la suppression d'origine de session DM, la liaison de compte, l'autorisation de bouton, la gestion des clics périmés, le comportement de porte d'action, les listes blanches de cibles de lecture, les vérifications de permissions de l'expéditeur, les vérifications de hiérarchie de rôle, la modération, les réactions, les permissions, et la présence.
- Negative signals:
  - Aucune preuve en direct/e2e située ne couvre les cartes/boutons d'approbation natives Discord de bout en bout pour `target: "dm"`, `target: "channel"`, et `target: "both"`, y compris les clics de non-approbateurs, les clics périmés, le nettoyage après résolution, et les avis de secours de même chat.
  - Aucune preuve en direct/e2e située ne couvre l'approbation et la confidentialité des résultats de `/diagnostics` ou `/export-trajectory` réservées au propriétaire via une origine de groupe Discord.
  - Aucune preuve en direct/e2e située ne couvre les mutations réelles de rôle/canal/modération/présence Discord sous les permissions Discord réelles et les portes d'action OpenClaw.
  - La ligne de base QA Discord en direct elle-même enregistre les scénarios de transport standard manquants : blocage de liste blanche, forme de réponse de haut niveau, et reprise de redémarrage.
- Integration gaps:
  - Ajouter QA Discord en direct pour les approbations exec avec `dm`, `channel`, et `both`, y compris le refus de non-approbateur, les décisions approuvées/refusées, l'expiration, le nettoyage, les avis de route, le TLS local auto-signé, et le mode de passerelle distante.
  - Ajouter QA Discord en direct pour `/diagnostics` et `/export-trajectory` privés au propriétaire à partir d'un canal de groupe, vérifiant la confidentialité des invites/résultats et les routes de propriétaire de secours.
  - Ajouter QA Discord en direct pour l'ajout/suppression de rôle, la création/édition/suppression de canal, le remplacement de permission, le timeout/kick/ban, et la mutation de présence avec les identités de demandeur autorisées et non autorisées.
  - Ajouter un scénario en direct ou e2e qui prouve que les portes d'action empêchent les éditions/suppressions de messages destructifs tout en préservant le comportement de lecture/envoi autorisé une fois que les portes granulaires existent.

## Quality Score

- Score: `Beta (72%)`
- Gitcrawl reports:
  - Open #73802 reports Discord exec approval card/buttons not delivered while manual `/approve` works.
  - Open #41740 reports Discord exec approvals fail against local self-signed TLS Gateway.
  - Open #78738 reports approval dispatch failures silently dropping commands; open PR #82506 proposes surfacing delivery failures.
  - Open #53250 requests clearer approval-timeout guidance and Control UI setup hints.
  - Open #7234 requests granular Discord message gates because the current `actions.messages` boolean gates read, send, edit, and delete together.
  - Open #34004 requests a separate, safe, bot-self-only profile action; current implementation only covers presence/status.
- Discrawl reports:
  - La discussion du mainteneur du 2026-05-27 a favorisé l'exec originaire du groupe routé vers DM par défaut car les cartes d'approbation visibles sur le canal peuvent divulguer les détails de la commande même lorsque l'autorisation des boutons est appliquée.
  - La discussion du mainteneur autour des PR #86771, #87104, et #87105 divise l'UX de bouton Discord périmé, l'authentification de passerelle de route-notice avec le moindre privilège, et le comportement de token de socket partagé en préoccupations de limite de sécurité séparées.
  - L'historique du support Discord montre une confusion répétée de l'opérateur autour des approbations natives non configurées, des portes d'action, des permissions Discord, et des capacités d'administration du bot.
  - Les messages d'archive enregistrent les lacunes antérieures en matière d'autorisation d'administration de guilde et de modération Discord de haute gravité, suivies de correctifs nécessitant une identité de demandeur de confiance et des vérifications de permissions Discord.
- Good qualities:
  - Les approbateurs d'approbation sont explicites : Discord accepte `execApprovals.approvers` ou `commands.ownerAllowFrom`, et la source ne déduit pas les approbateurs de `allowFrom`, legacy `dm.allowFrom`, ou `defaultTo`.
  - La cible d'approbation par défaut est DM, la livraison channel/both est opt-in, les docs avertissent que les invites de canal exposent le texte de la commande, et les non-approbateurs reçoivent un refus éphémère.
  - Le routage d'approbation native sépare les cibles d'origine des cibles DM d'approbateur, supprime la livraison d'origine pour les sessions DM Discord, préserve les cibles de thread, et rejette les demandes liées à un autre compte Discord.
  - Les boutons d'approbation Discord codent les ID d'approbation, limitent les décisions aux approbateurs résolus, reconnaissent les clics valides, et classent les réponses de passerelle périmées/expirées.
  - Les groupes d'actions privilégiées sont fermés, avec les rôles/modération/présence désactivés par défaut ; les chemins de canal/guilde/admin vérifient les permissions Discord lorsqu'une identité d'expéditeur de confiance est présente et appliquent les vérifications de hiérarchie de rôle pour les mutations de rôle.
  - Les actions de message de type lecture autorisent les cibles de guilde/canal/thread configurées avant de lire les messages, les épingles, les permissions, les réactions, ou les résultats de recherche.
- Bad qualities:
  - Les problèmes d'approbation-livraison ouverts sont directement sur le chemin d'approbation sensible à la sécurité et incluent des régressions où la commande manuelle fonctionne mais les cartes natives ne le font pas, le TLS local casse les clients d'approbation, ou la livraison échouée laisse l'agent sans erreur visible.
  - La discussion récente du mainteneur montre que le comportement de route-notice et de token partagé est toujours en révision active de limite de sécurité plutôt qu'un contrat de canal établi.
  - Le chemin d'administration/modération a eu des défauts d'authz graves antérieurs où les mutations de guilde privilégiées par bot pouvaient s'exécuter sans vérifications de permissions du demandeur ; la source actuelle est plus forte, mais l'historique réduit la certitude pour ce composant.
  - `actions.messages` est trop grossier pour le moindre privilège car les déploiements ne peuvent pas autoriser l'envoi/lecture tout en refusant séparément l'édition/suppression.
  - L'application des permissions dépend de l'identité du demandeur de confiance attachée pour les actions pilotées par l'expéditeur ; la source intentionnellement ignore intentionnellement la vérification de permission Discord pour les flux CLI/manuels sans `senderUserId`, donc le câblage d'identité d'appelant reste une limite critique.
- Excluded from quality:
  - La présence ou l'absence de tests unitaires, d'intégration, e2e, en direct, et de flux d'exécution n'ont pas été utilisées pour augmenter ou diminuer la qualité.

## Completeness Score

- Score: `Alpha (58%)`
- Surface instructions: evaluated against `references/completeness/discord.md`.
- Positive signals: archived docs, source, test, Gitcrawl, and Discrawl evidence cover the taxonomy scope for Native Discord exec/plugin approvals, Sensitive owner-only command routing for prompts, Discord message actions, Action gates under channels.discord.actions.\*.
- Negative signals: the archived note predated process-version-3 Completeness scoring, so this score is initialized from the same evidence breadth and known-gap record used for the archived Coverage score.
- Missing capability branches: see `## Known Gaps` and `## Evidence` below for the recorded missing branches and operator-visible caveats.

## Known Gaps

- La preuve d'approbation en direct est manquante pour les cartes/boutons natifs Discord sur toutes les cibles de livraison et les modes de défaillance.
- La confidentialité de la commande réservée au propriétaire sensible nécessite une preuve d'origine de groupe Discord en direct.
- La preuve d'action privilégiée Discord réelle est manquante pour les identités de demandeur autorisées et non autorisées.
- Les portes d'action de message Discord ont besoin de contrôles de moindre privilège plus granulaires pour la lecture/envoi/édition/suppression.
- La mutation de profil personnel/profil reste en dehors de la source actuelle malgré la demande ouverte pour une action réservée au bot-self uniquement et explicitement fermée.
- Les avis de route d'approbation et le comportement de token d'exécution d'approbation partagé ont besoin d'une décision de limite de sécurité établie et d'une preuve fusionnée.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:429` documente `dmPolicy` et la liste d'autorisation DM canonique `allowFrom`.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:457` documente les groupes d'accès dynamiques pour l'autorisation des commandes DM et texte Discord.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:482` définit l'appartenance à `discord.channelAudience` via la permission `ViewChannel` actuelle.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1003` documente les mises à jour de présence via la configuration de statut/activité.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1078` documente les approbations basées sur des boutons dans les DM et les invites de canal d'origine optionnelles.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1083` énumère `channels.discord.execApprovals.enabled`, `approvers` et `target`.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1088` indique que Discord s'active automatiquement uniquement lorsque les approbateurs se résolvent et ne déduit pas les approbateurs du `allowFrom` du canal, du `dm.allowFrom` hérité ou du `defaultTo`.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1090` documente le routage privé pour les commandes de groupe sensibles réservées au propriétaire.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1092` avertit que les invites d'approbation de canal/les deux sont visibles et seuls les approbateurs résolus peuvent utiliser les boutons.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1104` documente la résolution d'approbation Gateway et l'expiration par défaut de 30 minutes.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1113` énumère les actions de messagerie, d'administration de canal, de modération, de présence et de métadonnées.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1124` documente les portes d'action sous `channels.discord.actions.*`.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1130` montre les réactions/messages/threads/épingles/recherche/métadonnées/permissions activées par défaut et les rôles/modération/présence désactivés par défaut.

## Source

- `/Users/kevinlin/code/openclaw/extensions/discord/src/exec-approvals.ts:41` résout les approbateurs explicites, les approbateurs au niveau du compte ou `commands.ownerAllowFrom`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/exec-approvals.ts:71` vérifie si un expéditeur est un approbateur d'exécution Discord configuré.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-native.ts:72` résout les cibles de canal d'origine pour la livraison d'approbation native.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-native.ts:99` supprime la livraison d'origine lorsque la session d'initiation est un DM Discord.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-native.ts:148` résout les cibles DM de l'approbateur.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-native.ts:163` crée la capacité d'approbation native restreinte à l'approbateur.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-native.ts:183` résout le mode de livraison native à partir de `execApprovals.target`, par défaut `dm`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-native.ts:190` enregistre la gestion du runtime d'approbation native paresseuse pour les événements d'approbation d'exécution et de plugin.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-handler.runtime.ts:189` construit des conteneurs de demande d'approbation d'exécution avec aperçu de commande, métadonnées, boutons, expiration et ID.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-handler.runtime.ts:351` construit des ID personnalisés d'approbation Discord codés.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-handler.runtime.ts:414` configure le runtime natif pour les événements d'exécution et de plugin.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-handler.runtime.ts:510` prépare les cibles d'origine par rapport aux DM d'approbateur et crée des canaux DM utilisateur.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-handler.runtime.ts:550` envoie les cartes d'approbation en attente à la cible de canal/DM Discord préparée.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/accounts.ts:95` construit des portes d'action Discord par compte.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.ts:9` distribue les familles d'actions de messagerie, de guilde, de modération et de présence.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.guild.ts:113` définit les gardes d'action d'administration et les valeurs par défaut désactivées pour les changements de rôle.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.guild.ts:253` vérifie les permissions de l'expéditeur pour les actions d'administration de guilde.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.guild.ts:297` vérifie la hiérarchie des rôles et la gérabilité des rôles des membres pour les mutations de rôle.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.guild.ts:313` vérifie la gérabilité des remplacements de rôle pour les changements de permissions de canal.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.guild.ts:668` applique les actions d'ensemble/suppression de permissions de canal derrière la porte de canal.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.moderation.ts:29` vérifie les permissions de modération de l'expéditeur lorsque l'identité du demandeur est présente.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.moderation.ts:60` maintient la modération désactivée sauf si la porte est activée.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.messaging.shared.ts:313` autorise les cibles de lecture par rapport aux listes d'autorisation de guilde/canal/thread.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.messaging.messages.ts:52` porte les lectures de permissions et autorise le canal cible.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.messaging.messages.ts:117` porte les éditions de messages derrière `actions.messages`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.messaging.messages.ts:136` porte les suppressions de messages derrière `actions.messages`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.messaging.reactions.ts:10` porte les actions d'ajout/suppression/liste de réactions.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.presence.ts:23` implémente les mises à jour de présence portées via la Gateway active.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.test.ts:288` énumère les scénarios Discord en direct : canary, mention gating, enregistrement de commande d'aide native, réactions de statut, auto-join vocal et pièce jointe de thread.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.test.ts:403` attend que le compte Discord devienne connecté avant que les scénarios en direct ne se poursuivent.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.test.ts:472` enregistre que la couverture en direct standard manque toujours de liste d'autorisation-bloc, de forme de réponse de haut niveau et de redémarrage-reprise.
- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-gateway-approval.e2e.test.ts:63` prouve qu'une approbation d'exécution hébergée par Gateway peut être demandée et résolue sur des connexions séparées.
- `/Users/kevinlin/code/openclaw/src/gateway/operator-approvals-client.e2e.test.ts:62` prouve que l'autorité du runtime d'approbation est limitée aux URL Gateway locales générées et rejette la résolution d'approbation de boucle distante sans cette autorité.
- Aucun test en direct/e2e situé ne prouve la livraison de carte d'approbation native Discord et la résolution de bouton via Discord réel pour `dm`, `channel` et `both`.
- Aucun test en direct/e2e situé ne prouve les mutations de rôle/canal/modération/présence Discord par rapport aux permissions Discord réelles et aux identités du demandeur.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/discord/src/exec-approvals.test.ts:24` couvre l'activation, les approbateurs explicites, aucune déduction d'approbateur à partir de `allowFrom`/routes par défaut et le repli `commands.ownerAllowFrom`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-native.test.ts:35` couvre le rapport d'état de disponibilité et de capacité de livraison.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-native.test.ts:76` couvre le repli `ownerAllowFrom` pour le portage des demandes d'approbation.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-native.test.ts:124` couvre la normalisation de la cible d'origine.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-native.test.ts:148` et `:173` couvrent la suppression d'origine de session DM.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-native.test.ts:258` couvre les ID de thread explicites sur les cibles d'origine.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-native.test.ts:306` couvre le rejet de la livraison d'origine pour un autre compte Discord.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-handler.runtime.test.ts:5` couvre les mises à jour d'approbation d'origine acheminées vers les canaux de thread.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/exec-approvals.test.ts:86` couvre le refus de charge utile de bouton d'approbation invalide.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/exec-approvals.test.ts:101` couvre le refus de non-approbateur.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/exec-approvals.test.ts:116` couvre l'accusé de réception valide et la résolution.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/exec-approvals.test.ts:147` couvre le suivi d'approbation déjà résolu/obsolète.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/exec-approvals.test.ts:164` couvre le routage de résolution Gateway à partir du contexte de bouton.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.test.ts:438` couvre le refus de cible de lecture pour les lectures de permissions non autorisées.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.test.ts:1455` couvre la gestion de canal désactivée.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.test.ts:1466` couvre le refus de permission de l'expéditeur pour les actions de canal.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.test.ts:1659` couvre les actions de rôle de propriétaire/manuel de confiance sans ID d'expéditeur.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.test.ts:1670` couvre le refus de hiérarchie de rôle.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.test.ts:1920` couvre `ManageRoles` limité au canal pour les éditions de permissions.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.test.ts:1999` couvre le portage et l'exécution de la modération.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.presence.test.ts:132` couvre le portage de présence.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.moderation.authz.test.ts:34` couvre l'application de `BAN_MEMBERS`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.moderation.authz.test.ts:54` couvre l'application de `KICK_MEMBERS`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/actions/runtime.moderation.authz.test.ts:74` couvre l'application de `MODERATE_MEMBERS`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/send.permissions.authz.test.ts:122` couvre le rejet de hiérarchie de rôle.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/channel-actions.contract.test.ts:6` couvre le rapport de contrat d'action/capacité pour les portes Discord configurées.

## Requêtes Gitcrawl

- `gitcrawl doctor --json`
  Résultat : `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `repository_count=2`.
- `gitcrawl search issues "discord exec approvals" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : #53250 ouvert, #41740 ouvert, #9987 ouvert, #73802 ouvert, #78738 ouvert, #41152 ouvert, #67440 ouvert, #72545 ouvert, #81901 ouvert et éléments d'approbation d'exécution/plugin connexes.
- `gitcrawl search issues "channels.discord.execApprovals" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : #53250 ouvert, #78738 ouvert, #41152 ouvert.
- `gitcrawl search issues "discord approval buttons" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : #73802 ouvert, #82218 ouvert, #8959 ouvert, #85954 ouvert, #46656 ouvert, #77278 ouvert, #86777 ouvert.
- `gitcrawl search issues "discord moderation actions permissions" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : aucun résultat.
- `gitcrawl search issues "Discord channel actions gates" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : aucun résultat.
- `gitcrawl search issues "discord owner privacy diagnostics export trajectory" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : aucun résultat.
- `gitcrawl search issues "discord role add permissions" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : #69629 ouvert et #68955 ouvert.
- `gitcrawl search issues "discord permissions action" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : #79445 ouvert, #81232 ouvert, #83164 ouvert, #14785 ouvert, #87486 ouvert, #84724 ouvert, #78196 ouvert, #61368 ouvert.
- `gitcrawl search issues "discord setPresence" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : aucun résultat.
- `gitcrawl search prs "discord exec approval" -R openclaw/openclaw --state all --json number,title,url,state`
  Résultat : #82506 ouvert, #87105 ouvert, #80922 ouvert, #78813 ouvert, #81864 ouvert, #84485 ouvert et PR d'approbation/runtime connexes.
- `gitcrawl threads openclaw/openclaw --numbers 73802,41740,78738,53250 --include-closed --json`
  Résultat : #73802, #41740, #78738 et #53250 sont ouverts avec des rapports détaillés sur la livraison d'approbation Discord, TLS, défaillance silencieuse et orientation de délai d'expiration.
- `gitcrawl threads openclaw/openclaw --numbers 68716,68705,19008,70215 --include-closed --json`
  Résultat : #68716 ouvert enregistre les actions d'administration de guilde Discord s'exécutant sans contexte de demandeur.
- `gitcrawl threads openclaw/openclaw --numbers 7234,33270,34004,64402 --include-closed --json`
  Résultat : #7234 portes d'action granulaires ouvertes, #34004 action de profil personnel ouvert, #33270 division auto-présence/profil personnel fermée, #64402 problème de chemin d'invocation d'action fermé.
- `gitcrawl threads openclaw/openclaw --numbers 86771,87104,87105,82506 --include-closed --json`
  Résultat : #87105 jeton de socket runtime d'approbation partagé ouvert ; #82506 défaillances de livraison d'approbation d'exécution de surface ouvertes.

## Requêtes Discrawl

- `discrawl status --json`
  Résultat : `generated_at=2026-05-28T20:13:14Z`, `state=current`, `last_sync_at=2026-05-28T19:15:50Z`, `messages=1485267`, `channels=25766`, `threads=25539`, `members=173089`, `embedding_backlog=0`, `share remote git@github.com-personal:openclaw/discord-store.git`.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord exec approvals"`
  Résultat : discussion des responsables le 2026-05-27 favorisant l'approbation d'exécution d'origine de groupe acheminée vers DM, avis de route fractionnée de large `operator.write` et UX de clic obsolète séparé de topologie de jeton/Docker CLI partagée.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "channels.discord.execApprovals"`
  Résultat : messages de support répétés où les approbations d'exécution de chat natif n'étaient pas configurées et les utilisateurs ont été invités à configurer `channels.discord.execApprovals.approvers` ou `commands.ownerAllowFrom` ; également fermeture de configurabilité de délai d'expiration #49825.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord approval buttons"`
  Résultat : discussion des responsables avertissant que les cartes d'approbation visibles par canal peuvent divulguer des arguments, des chemins, des chaînes de type env ou des descriptions d'outils ; les notes divisent également l'avis de route et les préoccupations concernant le jeton de socket partagé.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord moderation actions"`
  Résultat : exemples de mai 2026 d'opérateurs activant toutes les portes d'action ; historique de support et d'examen PR de mars 2026 pour le routage d'outils d'administration/modération et les vérifications de permissions d'expéditeur de confiance.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "channels.discord.actions"`
  Résultat : threads de support d'opérateur vérifiant les portes d'action, les défaillances de gestion de canal et l'examen de porte granulaire #7234 ouvert.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord role permissions"`
  Résultat : support en direct des responsables/serveur autour de la visibilité des permissions Discord, porte de changement de rôle désactivée, PR d'autorisation d'administration de guilde antérieures #68705/#68716 et préoccupations concernant les mutations sûres.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord channel management is disabled"`
  Résultat : orientation de support que les opérations d'administration Discord dépendent à la fois de l'exposition d'outils et des portes `channels.discord.actions.*`.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord sender channel actions"`
  Résultat : note de durcissement des opérations de sécurité des responsables plus fermeture archivée #19008 citant les correctifs pour l'autorisation d'action de modération.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "approval.routeNotice.send"`
  Résultat : thread des responsables divisant #86771 UX de clic obsolète, #87104 méthode d'avis de route de moindre privilège et #87105 comportement de jeton de socket runtime d'approbation partagé.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord self-profile"`
  Résultat : commentaire ouvert #34004/#33270 que le main actuel implémente autoPresence/santé du runtime mais pas l'action et la porte de profil personnel demandées.
