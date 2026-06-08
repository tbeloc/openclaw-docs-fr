---
title: "Discord - Note de Maturité d'Accès et d'Identité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Discord - Note de Maturité d'Accès et d'Identité

## Résumé

L'appairage DM Discord et l'autorisation de l'expéditeur sont implémentés comme une surface d'autorisation d'entrée de canal partagée avec normalisation d'identité spécifique à Discord, héritage de liste d'autorisation conscient du compte, approbation du magasin d'appairage, vérifications dynamiques d'appartenance aux groupes d'accès et portes de groupe-DM explicites. La documentation et le code source s'accordent sur la ligne de base prévue : les expéditeurs directs inconnus reçoivent des défis d'appairage par défaut, les DM ouverts nécessitent un caractère générique explicite, les DM de groupe sont désactivés sauf s'ils sont configurés, et l'accès à l'audience de canal Discord dynamique échoue de manière fermée.

Le plafond de maturité est maintenu en dessous de Stable en raison de la couverture en direct manquante pour la boucle d'appairage DM de premier contact principal et des rapports d'archive actifs de chutes Discord entrantes silencieuses, d'incompatibilités d'identité et d'ambiguïté d'autorisation de l'expéditeur. L'implémentation dispose de bonnes primitives de fermeture en cas d'échec, mais les preuves de terrain montrent suffisamment de cas limites spécifiques à Discord pour que ce composant soit traité comme Beta jusqu'à ce que les chemins d'appairage et de liste d'autorisation aient des régressions en direct et que les bogues ouverts soient résolus.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Accès et Identité`
- Fusionnée à partir de : `Appairage DM et Accès`
- Report de score : minimum conservateur des scores de catégorie source fusionnés.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Modes de politique DM : Couvre les modes de politique DM sur les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open` et `disabled`. Résolution canonique et héritée de `allowFrom` sur la configuration Discord de niveau supérieur, et comportement d'appairage DM et d'autorisation de l'expéditeur associé.
- Héritage de liste d'autorisation : Couvre l'héritage de liste d'autorisation sur les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open` et `disabled`. Résolution canonique et héritée de `allowFrom` sur la configuration Discord de niveau supérieur, et comportement d'appairage DM et d'autorisation de l'expéditeur associé.
- Approbation du code d'appairage : Couvre l'approbation du code d'appairage sur les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open` et `disabled`. Résolution canonique et héritée de `allowFrom` sur la configuration Discord de niveau supérieur, et comportement d'appairage DM et d'autorisation de l'expéditeur associé.
- Autorisation de l'expéditeur : Couvre l'autorisation de l'expéditeur sur les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open` et `disabled`. Résolution canonique et héritée de `allowFrom` sur la configuration Discord de niveau supérieur, et comportement d'appairage DM et d'autorisation de l'expéditeur associé.
- Autorisation du groupe d'accès : Couvre l'autorisation du groupe d'accès sur les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open` et `disabled`. Résolution canonique et héritée de `allowFrom` sur la configuration Discord de niveau supérieur, et comportement d'appairage DM et d'autorisation de l'expéditeur associé.
- Autorisation du groupe DM : Couvre l'autorisation du groupe DM sur les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open` et `disabled`. Résolution canonique et héritée de `allowFrom` sur la configuration Discord de niveau supérieur, et comportement d'appairage DM et d'autorisation de l'expéditeur associé.

## Fonctionnalités

- Modes de politique DM : Couvre les modes de politique DM sur les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open` et `disabled`. Résolution canonique et héritée de `allowFrom` sur la configuration Discord de niveau supérieur, et comportement d'appairage DM et d'autorisation de l'expéditeur associé.
- Héritage de liste d'autorisation : Couvre l'héritage de liste d'autorisation sur les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open` et `disabled`. Résolution canonique et héritée de `allowFrom` sur la configuration Discord de niveau supérieur, et comportement d'appairage DM et d'autorisation de l'expéditeur associé.
- Approbation du code d'appairage : Couvre l'approbation du code d'appairage sur les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open` et `disabled`. Résolution canonique et héritée de `allowFrom` sur la configuration Discord de niveau supérieur, et comportement d'appairage DM et d'autorisation de l'expéditeur associé.
- Autorisation de l'expéditeur : Couvre l'autorisation de l'expéditeur sur les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open` et `disabled`. Résolution canonique et héritée de `allowFrom` sur la configuration Discord de niveau supérieur, et comportement d'appairage DM et d'autorisation de l'expéditeur associé.
- Autorisation du groupe d'accès : Couvre l'autorisation du groupe d'accès sur les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open` et `disabled`. Résolution canonique et héritée de `allowFrom` sur la configuration Discord de niveau supérieur, et comportement d'appairage DM et d'autorisation de l'expéditeur associé.
- Autorisation du groupe DM : Couvre l'autorisation du groupe DM sur les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open` et `disabled`. Résolution canonique et héritée de `allowFrom` sur la configuration Discord de niveau supérieur, et comportement d'appairage DM et d'autorisation de l'expéditeur associé.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (74%)`

Ce score utilise uniquement les preuves d'intégration, e2e, en direct et de flux d'exécution.

Signaux de couverture positifs :

- L'assurance qualité Discord en direct exerce l'affichage et l'interrogation réels de Discord pour le comportement de canary de canal et de gating de mention, avec une configuration d'exécution qui utilise des listes d'autorisation de guilde/canal et un utilisateur pilote autorisé (`extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:291`, `extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:307`, `extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:451`, `extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:671`, `extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:1120`).
- Le script e2e Discord macOS configure un jeton réel, une guilde, un canal et une liste d'autorisation de l'expéditeur, puis exécute le sondage d'état, l'envoi sortant, l'affichage de l'hôte entrant et la relecture (`scripts/e2e/parallels/macos-discord.ts:27`, `scripts/e2e/parallels/macos-discord.ts:48`).
- L'e2e d'intégration du paquet accepte Discord comme canal pris en charge, l'installe/le configure, exécute les étapes d'état/docteur et exécute un tour d'agent local (`scripts/e2e/npm-onboard-channel-agent-docker.sh:27`, `scripts/e2e/npm-onboard-channel-agent-docker.sh:86`, `scripts/e2e/npm-onboard-channel-agent-docker.sh:163`, `scripts/e2e/npm-onboard-channel-agent-docker.sh:172`).
- Une intégration bind-here ACP Discord prouve qu'un chemin d'exécution de message direct peut être acheminé dans une session ACP existante lorsqu'elle est configurée avec `dmPolicy: "open"` et `allowFrom: ["*"]` (`extensions/discord/src/monitor/acp-bind-here.integration.test.ts:139`, `extensions/discord/src/monitor/acp-bind-here.integration.test.ts:196`, `extensions/discord/src/monitor/acp-bind-here.integration.test.ts:210`).
- Les tests de flux d'exécution couvrent les réponses d'appairage, l'autorisation du magasin d'appairage, la classification DM directe/groupe, l'autorisation d'interaction de composant et le rejet de groupe-DM de commande native (`extensions/discord/src/monitor/monitor.agent-components.test.ts:157`, `extensions/discord/src/monitor/monitor.agent-components.test.ts:221`, `extensions/discord/src/monitor/monitor.agent-components.test.ts:276`, `extensions/discord/src/monitor/native-command.plugin-dispatch.test.ts:827`).

Lacunes de couverture :

- Aucun scénario en direct ou e2e situé ne prouve la boucle DM Discord complète de premier contact : l'expéditeur inconnu reçoit le code, le propriétaire approuve le code et un DM ultérieur de cet expéditeur est admis via le magasin d'appairage approuvé.
- Aucun scénario en direct ou e2e situé ne prouve le refus de liste d'autorisation Discord, le refus DM désactivé ou le refus DM ouvert sans caractère générique.
- Aucun scénario en direct ou e2e situé ne prouve l'appartenance dynamique à `discord.channelAudience` par rapport aux autorisations Discord, y compris les cas d'accès manquant, de mauvaise guilde et de membre non résolu échouant de manière fermée.
- Aucun scénario en direct ou e2e situé ne prouve le gating de groupe DM via `dm.groupEnabled` et `dm.groupChannels`.
- Aucun scénario en direct ou e2e situé ne prouve la portée du magasin d'appairage multi-compte pour les comptes Discord nommés.

## Score de Qualité

- Score : `Bêta (72%)`

Résultats positifs pour la qualité :

- La sémantique des politiques est documentée en un seul endroit avec `channels.discord.dmPolicy` canonique, `channels.discord.allowFrom` canonique, alias hérités, formats cibles, précédence multi-compte, expiration du code d'appairage et exigences de caractère générique `open` (`docs/channels/discord.md:425`, `docs/channels/discord.md:456`, `docs/channels/pairing.md:24`, `docs/channels/pairing.md:79`).
- Le schéma de configuration rejette les modes DM non sécurisés ou ambigus : `dmPolicy: "open"` nécessite un caractère générique effectif, `dmPolicy: "allowlist"` nécessite une liste d'autorisation effective, et les comptes nommés héritent des listes d'autorisation parentes pour la validation (`src/config/zod-schema.providers-core.ts:830`).
- Le résolveur d'accès aux messages partagés sépare les politiques directes et de groupe, développe les groupes d'accès, lit l'état d'appairage uniquement lorsque la politique le permet, et convertit les décisions d'appairage requis en un résultat d'admission distinct (`src/channels/message-access/runtime.ts:237`, `src/channels/message-access/runtime.ts:610`, `src/channels/message-access/sender-gates.ts:37`, `src/channels/message-access/decision.ts:290`).
- L'autorisation spécifique à Discord normalise les ID d'utilisateur stables et les alias de nom d'utilisateur/tag dangereux, enfile l'ID de compte dans l'accès au magasin d'appairage, et prend en charge les vérifications dynamiques `discord.channelAudience` (`extensions/discord/src/monitor/dm-command-auth.ts:58`, `extensions/discord/src/monitor/dm-command-auth.ts:93`, `extensions/discord/src/monitor/dm-command-auth.ts:128`).
- L'autorisation d'audience de canal est explicitement fermée en cas d'échec : la recherche de permission retourne false en cas de canal manquant, mauvaise guilde, membre non résolu ou erreurs de récupération Discord (`extensions/discord/src/send.permissions.ts:180`).
- Les DM de groupe sont désactivés par défaut et nécessitent une liste d'autorisation de canal explicite ; la politique de groupe n'est pas traitée silencieusement comme une politique de DM direct (`src/config/types.discord.ts:28`, `extensions/discord/src/monitor/message-handler.preflight.ts:318`).
- La documentation d'approbation Discord prévient un chemin d'inférence risqué : les approbateurs d'approbation exec sont résolus à partir de la configuration exec/owner et ne sont pas déduits de `allowFrom` de canal, `dm.allowFrom` hérité, ou `defaultTo` DM (`docs/channels/discord.md:1078`).
- Le code d'audit de sécurité signale la posture DM ouverte et les entrées de liste d'autorisation de nom/tag risquées (`extensions/discord/src/security-audit.ts:50`, `src/security/audit-channel.ts:203`).

Résultats négatifs pour la qualité :

- Gitcrawl a des rapports ouverts selon lesquels les utilisateurs de liste d'autorisation Discord directe peuvent être silencieusement ignorés ou supprimés : #48641 signale les DM entrants sur liste blanche silencieusement supprimés tandis que les canaux sortants et de guilde fonctionnent, et #79043 signale un utilisateur de liste d'autorisation Discord résolu étant ignoré avec injection de propriétaire de bot non documentée dans les listes d'autorisation d'exécution.
- Gitcrawl #86332 signale une non-concordance d'identité d'appairage Discord DM pour les utilisateurs de PluralKit, où le chemin d'autorisation et le gestionnaire d'appairage utilisent des identités différentes et peuvent laisser les utilisateurs dans une boucle d'appairage infinie.
- Gitcrawl #81876 signale l'exposition d'appairage post-bootstrap : après le bootstrap du premier propriétaire, le comportement d'appairage par défaut peut continuer à répondre avec des codes d'appairage à des expéditeurs aléatoires au lieu de se restreindre automatiquement au propriétaire.
- Gitcrawl #84447 identifie l'absence de limitation DM entrant par expéditeur pour les politiques d'appairage et de liste d'autorisation, ce qui laisse les surfaces de code d'appairage et d'expéditeur bloqué vulnérables au spam et à la défaillance opérationnelle bruyante.
- Gitcrawl #53198 signale l'incohérence de secours et de diagnostics `allowFrom` Discord autour de l'autorisation élevée, montrant que la sémantique de configuration d'autorisation d'expéditeur adjacente est toujours fragile.
- L'historique du support Discrawl montre à plusieurs reprises la confusion d'appairage et d'authentification d'expéditeur autour des DM Discord par rapport aux canaux de serveur, aux comptes nommés, aux DM de groupe et aux commandes silencieusement ignorées ; le modèle est documenté, mais les diagnostics visibles par l'utilisateur ne sont pas encore systématiquement explicatifs.
- Discrawl n'a pas surfacé les preuves d'adoption opérationnelle actuelles pour `discord.channelAudience`, donc le chemin d'accès au groupe dynamique semble soutenu par la source mais non éprouvé sur le terrain dans l'instantané d'archive.

## Score de Complétude

- Score : `Bêta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/discord.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent l'étendue de la taxonomie pour les modes de politique DM, l'héritage de liste d'autorisation, l'approbation du code d'appairage, l'autorisation d'expéditeur, l'autorisation du groupe d'accès, l'autorisation DM de groupe.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une régression Discord en direct pour l'appairage DM de premier contact : défi, `openclaw pairing approve discord <CODE>`, et admission de message post-approbation.
- Ajouter une régression Discord en direct ou enregistrée pour `discord.channelAudience`, y compris le succès ViewChannel et l'accès manquant, mauvaise guilde, membre non résolu et comportement fermé en cas d'erreur de récupération.
- Ajouter une couverture en direct ou e2e pour les modes de refus DM direct et l'autorisation `dm.groupChannels` DM de groupe.
- Résoudre ou concevoir explicitement autour de #86332, #48641, #79043, #81876 et #84447 avant de noter cette surface d'authentification d'expéditeur Stable.
- Améliorer les diagnostics de suppression Discord afin que les messages directs non autorisés, les messages réservés aux commandes, les non-concordances d'étendue de compte et les défaillances de politique DM de groupe soient distinguables de l'extérieur.

## Preuves

### Docs

- `docs/channels/discord.md:8` indique que Discord supporte les DM et les canaux de guilde, les DM étant par défaut en mode d'appairage.
- `docs/channels/discord.md:183` documente l'approbation d'appairage par premier DM, les commandes pairing-list et pairing-approve, et l'expiration du code en une heure.
- `docs/channels/discord.md:425` documente le contrôle d'accès Discord, `dmPolicy`, `allowFrom` canonique, `pairing`, `allowlist`, `open`, `disabled`, les alias hérités, et les formats de cible.
- `docs/channels/discord.md:456` documente les groupes d'accès, `message.senders`, `discord.channelAudience`, l'autorisation ViewChannel, l'intention des membres du serveur, et le comportement de fermeture en cas d'échec.
- `docs/channels/discord.md:577` documente les mentions et les DM de groupe, les DM de groupe étant ignorés par défaut et l'allowlisting optionnel `dm.groupChannels`.
- `docs/channels/discord.md:1078` documente l'autorisation d'approbation Discord et rejette explicitement l'inférence à partir des allowlists de canaux et des valeurs par défaut des DM.
- `docs/channels/pairing.md:10` définit l'appairage comme une approbation d'accès explicite ; les expéditeurs de DM inconnus reçoivent un code d'appairage et leur message original n'est pas traité.
- `docs/channels/pairing.md:24` documente les exigences de caractère générique DM ouvert, les codes d'appairage de 8 caractères, l'expiration en une heure, et les plafonds de demandes en attente.
- `docs/channels/pairing.md:79` documente l'état d'appairage et d'allowlist limité au compte sous `~/.openclaw/credentials`.
- `docs/channels/access-groups.md:149` documente `discord.channelAudience`, l'appartenance à ViewChannel, et le comportement de fermeture en cas d'échec pour Missing Access/member/guild.
- `docs/channels/groups.md:291` documente que les approbations d'appairage DM s'appliquent uniquement aux DM et que les DM de groupe Discord sont séparément contrôlés par `channels.discord.dm.*`.

### Source

- `src/config/types.discord.ts:28` définit la politique DM Discord, l'allowlist direct, le comportement par défaut des DM de groupe désactivé, et l'allowlisting des canaux de groupe.
- `src/config/types.discord.ts:399` définit les clés canoniques de niveau supérieur `dmPolicy` et `allowFrom` plus les clés héritées.
- `src/config/zod-schema.providers-core.ts:830` valide la sécurité de la politique DM Discord, y compris les exigences de caractère générique et d'allowlist non vide.
- `extensions/discord/src/accounts.ts:61` résout `allowFrom` Discord conscient du compte ; `extensions/discord/src/accounts.ts:78` résout `dmPolicy` conscient du compte avec la valeur par défaut `pairing`.
- `src/channels/plugins/dm-access.ts:125` résout les valeurs de politique et d'allowlist de message direct canoniques et héritées dans les portées de compte et parent.
- `extensions/discord/src/monitor/provider.ts:183` résout le compte au moment du moniteur, l'allowlist DM configuré, la politique de groupe de secours, l'activation des DM, et la politique d'appairage par défaut.
- `extensions/discord/src/monitor/message-handler.preflight.ts:252` classe les DM directs par rapport aux DM de groupe et supprime le trafic DM direct ou de groupe désactivé avant le routage.
- `extensions/discord/src/monitor/message-handler.dm-preflight.ts:27` bloque les DM directs désactivés, invoque l'accès à la commande DM Discord, et envoie des réponses d'appairage pour les décisions d'appairage requis.
- `extensions/discord/src/monitor/dm-command-auth.ts:58` construit les identités d'expéditeur stables et d'alias ; `extensions/discord/src/monitor/dm-command-auth.ts:93` câble `discord.channelAudience` ; `extensions/discord/src/monitor/dm-command-auth.ts:171` résout l'accès à la commande de message direct.
- `src/channels/message-access/runtime.ts:100` lit le magasin d'appairage uniquement lorsque la politique le permet ; `src/channels/message-access/runtime.ts:237` définit les politiques directes/groupe par défaut ; `src/channels/message-access/runtime.ts:610` produit la décision d'accès effective.
- `src/channels/message-access/sender-gates.ts:37` applique les portes d'expéditeur direct pour les modes désactivé, ouvert, allowlist et appairage.
- `src/plugin-sdk/access-groups.ts:50` résout les états des groupes d'accès, y compris manquant, non supporté, échoué, `message.senders` statique, et les correspondances de résolveur dynamique.
- `extensions/discord/src/send.permissions.ts:180` implémente les vérifications d'appartenance à ViewChannel Discord avec des retours faux pour les mauvaises guildes et les échecs de récupération.
- `extensions/discord/src/channel.ts:700` câble l'adaptateur d'appairage Discord, y compris les étiquettes `discordUserId`, la normalisation des entrées, et la notification d'approbation.
- `src/pairing/pairing-store.ts:47` définit les demandes d'appairage et le chemin du magasin ; `src/pairing/pairing-store.ts:265` applique la portée du compte.
- `src/pairing/pairing-challenge.ts:20` émet ou réutilise les défis d'appairage et envoie les réponses uniquement pour les demandes nouvellement créées.
- `extensions/discord/src/security-audit.ts:50` lit la configuration Discord et les allowlists d'appairage pour les avertissements d'audit.

### Tests d'intégration

- `extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:291` exécute les scénarios de canari Discord en direct et de mention-gating par rapport aux boucles réelles d'envoi/sondage de messages Discord.
- `extensions/qa-lab/src/live-transports/discord/discord-live.runtime.test.ts:108` vérifie que la configuration Discord QA en direct injecte les allowlists de compte, guilde, canal et utilisateur du pilote.
- `scripts/e2e/parallels/macos-discord.ts:27` configure un jeton Discord réel/guilde/canal/allowlist d'expéditeur, sonde l'état, envoie sortant, et vérifie la relecture entrante.
- `scripts/e2e/npm-onboard-channel-agent-docker.sh:27` inclut Discord dans la configuration e2e d'intégration de paquet, l'ajout/statut/médecin de canal, et le flux d'agent-tour local.
- `scripts/e2e/lib/upgrade-survivor/config-recipe/channels-discord.json:1` préserve le jeton Discord, la politique d'allowlist DM héritée, la politique de groupe, et la configuration d'outil de guilde/canal dans la couverture de survivant de mise à niveau.
- `extensions/discord/src/monitor/acp-bind-here.integration.test.ts:133` vérifie qu'un chemin d'exécution DM Discord peut s'attacher à une session ACP existante sous la politique DM ouverte.

### Tests unitaires

- `extensions/discord/src/monitor/dm-command-auth.test.ts:113` vérifie que les DM ouverts sont bloqués sans caractère générique ou avec des allowlists non correspondants.
- `extensions/discord/src/monitor/dm-command-auth.test.ts:142` vérifie les décisions d'appairage requis et l'admission du magasin d'appairage.
- `extensions/discord/src/monitor/dm-command-auth.test.ts:170` vérifie l'admission du groupe d'accès `discord.channelAudience`.
- `extensions/discord/src/monitor/dm-command-auth.test.ts:235` vérifie que la recherche d'audience de canal échoue fermée.
- `extensions/discord/src/monitor/message-handler.preflight.test.ts:530` vérifie le comportement de préflight DM direct et la réserve de compte par défaut.
- `extensions/discord/src/monitor/monitor.agent-components.test.ts:157` vérifie les réponses d'appairage pour les DM non allowlistés.
- `extensions/discord/src/monitor/monitor.agent-components.test.ts:179` vérifie le blocage DM en mode allowlist.
- `extensions/discord/src/monitor/monitor.agent-components.test.ts:198` vérifie la classification DM de groupe.
- `extensions/discord/src/monitor/monitor.agent-components.test.ts:221` vérifie le blocage DM de groupe lorsqu'il n'est pas allowlisté même si les DM directs sont ouverts.
- `extensions/discord/src/monitor/monitor.agent-components.test.ts:276` vérifie les interactions de composant DM à partir du magasin d'appairage et du mode ouvert.
- `extensions/discord/src/monitor/native-command.plugin-dispatch.test.ts:827` vérifie que les commandes slash DM de groupe sont rejetées en dehors des canaux de groupe configurés.
- `extensions/discord/src/config-schema.test.ts:23` vérifie que `dmPolicy: "open"` rejette les configurations sans `*` et accepte les alias hérités.
- `extensions/discord/src/accounts.test.ts:101` vérifie la précédence Discord allowFrom dans les comptes par défaut et nommés.

### Requêtes Gitcrawl

- `gitcrawl doctor --json`
  - Résultat : archive saine pour l'instantané requis ; fraîcheur enregistrée ci-dessus.
- `gitcrawl search issues "discord dmPolicy allowFrom" -R openclaw/openclaw --state all --json number,title,url,state`
  - Résultat : problèmes d'authentification d'expéditeur direct ouverts surfacés, y compris #48641, #53198, #81876, #84447, #86332, et #79043.
- `gitcrawl search issues "Discord DM pairing code" -R openclaw/openclaw --state all --json number,title,url,state`
  - Résultat : problèmes liés à l'appairage surfacés, y compris la non-correspondance d'identité #86332 et l'exposition d'appairage post-bootstrap #81876.
- `gitcrawl search issues "discord channelAudience accessGroup" -R openclaw/openclaw --state all --json number,title,url,state`
  - Résultat : aucun résultat de problème direct pour les groupes d'accès d'audience de canal Discord dynamiques.
- `gitcrawl search issues "Discord group DM" -R openclaw/openclaw --state all --json number,title,url,state`
  - Résultat : problèmes de routage DM de groupe et de chat de groupe adjacents surfacés, y compris #51805 et #59933.
- `gitcrawl search issues "Discord unauthorized sender allowlist" -R openclaw/openclaw --state all --json number,title,url,state`
  - Résultat : aucun résultat direct sous cette requête.
- `gitcrawl search issues "Discord allowFrom channelAudience Missing Access" -R openclaw/openclaw --state all --json number,title,url,state`
  - Résultat : aucun résultat direct sous cette requête.
- `gitcrawl threads openclaw/openclaw --numbers 48641,53198,81876,84447,86332,79043 --include-closed --json`
  - Résultat : problèmes ouverts confirmés pour les suppressions silencieuses de DM Discord, la confusion de secours allowFrom élevée, l'exposition d'appairage post-bootstrap, l'écart de limite de débit DM entrant, la non-correspondance d'identité d'appairage PluralKit, et les utilisateurs d'allowlist résolus étant ignorés.

### Requêtes Discrawl

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "discord dmPolicy allowFrom"`
  - Résultat : discussion de refactorisation d'entrée de canal surfacée couvrant la politique DM partagée, les magasins d'appairage, les allowlists, la provenance du groupe d'accès, et les états de fermeture en cas d'échec ; également surfacé l'historique de configuration/débogage utilisateur pour la politique DM Discord et les allowlists.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord DM pairing code"`
  - Résultat : conseils de support surfacés pour envoyer un DM au bot, approuver les codes d'appairage réels, l'expiration du code, l'utilisation du compte nommé `--account`, et les paramètres de membre du serveur DM Discord.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "discord channelAudience accessGroup"`
  - Résultat : aucun résultat direct dans l'instantané.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord group DM"`
  - Résultat : préoccupations concernant la confidentialité de l'approbation d'origine de groupe et la divergence de route DM par rapport au chat de groupe Discord surfacées.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 8 "Discord channel audience ViewChannel"`
  - Résultat : aucun résultat direct dans l'instantané.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 8 "Discord allowFrom silently ignored"`
  - Résultat : historique de support surfacé autour des messages de commande uniquement ignorés silencieusement et des messages de groupe avec des allowlists vides.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 8 "Discord DMs inbound silently dropped"`
  - Résultat : rapports utilisateur et discussion de problème surfacés pour les DM Discord entrants supprimés silencieusement tandis que d'autres chemins fonctionnaient.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 8 "dmPolicy pairing allowFrom accessGroups"`
  - Résultat : journaux d'exécution surfacés montrant la politique Discord résolue `dmPolicy`, `allowFrom`, la politique de groupe, et la configuration des groupes d'accès.
