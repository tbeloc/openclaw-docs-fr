---
title: "iMessage / BlueBubbles - Native Controls and Approvals Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iMessage / BlueBubbles - Native Controls and Approvals Maturity Note

## Résumé

Les approbations natives, les réactions et le contrôle opérateur sont en version Bêta. Le composant est bien structuré : iMessage peut fournir des approbations natives exec/plugin, ajouter des indices de choix de réaction, résoudre les tapbacks en décisions d'approbation, exiger des approbateurs explicites, persister les cibles de réaction, interroger les réactions après redémarrage et supprimer les invites locales en double. Il reste en version Bêta car l'expérience utilisateur dépend des métadonnées de tapback structurées des clients Apple et d'une configuration prudente de `allowFrom` par l'opérateur.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Native Controls and Approvals`
- Fusionnée à partir de : `Approvals and Operator Control`, `Rich Messages and Actions`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Native Approvals : Couvre les approbations natives dans la livraison d'approbation native, le routage d'approbation exec/plugin, les décisions d'approbation basées sur les réactions, les modifications d'autorisation `/approve` et le comportement associé des approbations natives, réactions et contrôle opérateur.
- Reactions : Couvre les réactions dans la livraison d'approbation native, le routage d'approbation exec/plugin, les décisions d'approbation basées sur les réactions, les modifications d'autorisation `/approve` et le comportement associé des approbations natives, réactions et contrôle opérateur.
- Operator Control : Couvre le contrôle opérateur dans la livraison d'approbation native, le routage d'approbation exec/plugin, les décisions d'approbation basées sur les réactions, les modifications d'autorisation `/approve` et le comportement associé des approbations natives, réactions et contrôle opérateur.
- Media : Couvre les médias dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes distantes, les récupérations SCP `remoteHost`, la conversion HEIC, les limites de taille, les envois de médias sortants, `send-attachment`, la segmentation de texte et les reçus de médias.
- Attachments : Couvre les pièces jointes dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes distantes, les récupérations SCP `remoteHost`, la conversion HEIC, les limites de taille, les envois de médias sortants, `send-attachment`, la segmentation de texte et les reçus de médias.
- Remote Fetch : Couvre la récupération distante dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes distantes, les récupérations SCP `remoteHost`, la conversion HEIC, les limites de taille, les envois de médias sortants, `send-attachment`, la segmentation de texte et les reçus de médias.
- Chunking : Couvre la segmentation dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes distantes, les récupérations SCP `remoteHost`, la conversion HEIC, les limites de taille, les envois de médias sortants, `send-attachment`, la segmentation de texte et les reçus de médias.
- Native Actions : Couvre les actions natives dans le sondage d'API privée, la disponibilité des actions, les portes de configuration d'action, le mappage de tapback, la modification/suppression/réponse/effets/gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/grammaire cible et les erreurs de dispatch d'action.
- Private API : Couvre l'API privée dans le sondage d'API privée, la disponibilité des actions, les portes de configuration d'action, le mappage de tapback, la modification/suppression/réponse/effets/gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/grammaire cible et les erreurs de dispatch d'action.
- Message Tool : Couvre l'outil de message dans le sondage d'API privée, la disponibilité des actions, les portes de configuration d'action, le mappage de tapback, la modification/suppression/réponse/effets/gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/grammaire cible et les erreurs de dispatch d'action.
- Native Actions : Couvre les actions natives dans le sondage d'API privée, la disponibilité des actions, les portes de configuration d'action, le mappage de tapback, la modification/suppression/réponse/effets/gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/grammaire cible et les erreurs de dispatch d'action
- Private API : Couvre l'API privée dans le sondage d'API privée, la disponibilité des actions, les portes de configuration d'action, le mappage de tapback, la modification/suppression/réponse/effets/gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/grammaire cible et les erreurs de dispatch d'action
- Message Tool : Couvre l'outil de message dans le sondage d'API privée, la disponibilité des actions, les portes de configuration d'action, le mappage de tapback, la modification/suppression/réponse/effets/gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/grammaire cible et les erreurs de dispatch d'action

## Fonctionnalités

- Native Approvals : Couvre les approbations natives dans la livraison d'approbation native, le routage d'approbation exec/plugin, les décisions d'approbation basées sur les réactions, les modifications d'autorisation `/approve` et le comportement associé des approbations natives, réactions et contrôle opérateur.
- Reactions : Couvre les réactions dans la livraison d'approbation native, le routage d'approbation exec/plugin, les décisions d'approbation basées sur les réactions, les modifications d'autorisation `/approve` et le comportement associé des approbations natives, réactions et contrôle opérateur.
- Operator Control : Couvre le contrôle opérateur dans la livraison d'approbation native, le routage d'approbation exec/plugin, les décisions d'approbation basées sur les réactions, les modifications d'autorisation `/approve` et le comportement associé des approbations natives, réactions et contrôle opérateur.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs :
  - La documentation décrit le routage d'approbation native, les décisions de tapback, les approbateurs explicites, l'authentification `/approve`, la persistance, la gestion des tapbacks multi-appareils et les limites de tapback hérités.
  - La source a des modules séparés pour la livraison d'approbation native, l'autorisation, l'état de réaction, l'interrogation de réaction et le routage de raccourci de moniteur.
  - Les tests sont étendus sur la disponibilité de livraison d'approbation, la correspondance de cible, la sécurité d'origine de groupe, le rendu d'invite, la suppression de secours, la résolution de réaction, la persistance, l'interrogation et l'autorisation.
  - L'archive Discord montre la discussion produit et le rapport du responsable autour des réactions d'approbation.
- Signaux négatifs :
  - Aucune voie d'invite/tapback d'approbation iMessage en direct n'a été trouvée.
  - Les tapbacks de style texte hérité ne peuvent pas résoudre les approbations.
  - Les raccourcis de réaction d'approbation dépendent de la liaison GUID de message exacte et des charges utiles de réaction structurées Apple.
- Lacunes d'intégration :
  - Ajouter une voie Mac contrôlée pour l'approbation exec native, l'approbation plugin, la résolution de tapback Like/Dislike, le refus de tapback non autorisé, le redémarrage avant tapback et l'exigence d'approbateur d'origine de groupe.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl :
  - `iMessage approval reactions` a retourné #85954 pour le formatage d'invite d'approbation de corps attribué et le contexte du travail de réaction antérieur.
  - `iMessage send-rich` a également retourné #85954.
  - `iMessage approval reaction approve allowFrom` n'a retourné aucun résultat direct dans la dernière passe gitcrawl.
- Rapports Discrawl :
  - `iMessage approval reactions` a retourné un rapport du responsable 2026-05 mentionnant les réactions d'approbation iMessage et une discussion sur le support des approbations via les réactions dans les clients sans meilleure UX d'approbation.
  - `iMessage approval reaction approve allowFrom` n'a retourné aucun extrait.
- Bonnes qualités :
  - L'autorisation d'approbateur explicite est séparée de l'admission DM/groupe plus large.
  - Le routage d'approbation d'origine de groupe nécessite des approbateurs configurés avant d'autoriser l'approbation de réaction.
  - La liaison persistante protège les fenêtres de redémarrage court.
  - Les tapbacks supprimés et les cas limites d'auto-approbation sont gérés.
  - La suppression de secours réduit les invites locales en double lorsque la livraison native a la même cible.
- Mauvaises qualités :
  - L'opérateur doit configurer `allowFrom` avec soin ; les approbateurs génériques sont puissants et risqués.
  - Les métadonnées de tapback structurées sont requises pour l'approbation de réaction robuste.
  - Le formatage d'invite et les affordances d'action sont toujours en cours de raffinement dans les problèmes d'archive.
- Exclu de la qualité :
  - Les preuves de test unitaire, intégration, e2e, en direct et flux d'exécution sont enregistrées sous Couverture uniquement.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/imessage-bluebubbles.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de taxonomie pour les approbations natives, réactions, contrôle opérateur.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La preuve d'approbation/tapback en direct est manquante.
- La résolution d'approbation dépend des métadonnées de tapback et de la liaison GUID.
- Les erreurs de liste blanche d'opérateur peuvent rendre les approbations trop larges ou indisponibles.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:576` : les invites d'approbation exec/plugin peuvent être acheminées vers iMessage et accepter les tapbacks.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:582` : la gestion des réactions nécessite que l'utilisateur réagissant soit un approbateur explicite de `allowFrom`.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:584` : l'autorisation de la commande texte `/approve` utilise désormais la liste des approbateurs lorsqu'elle n'est pas vide.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:587` : les liaisons de réaction sont stockées en mémoire et dans un état de clé persistant.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:588` : les tapbacks auto multi-appareils sont ignorés.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:589` : les tapbacks de style texte hérité ne peuvent pas résoudre les approbations.

### Source

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:487` : le raccourci de réaction d'approbation achemine les tapbacks correspondants avant la distribution normale.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:1042` : le moniteur enregistre le contexte d'exécution d'approbation natif.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:1058` : le moniteur démarre l'état d'interrogation de réaction d'approbation.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-native.ts:505` : les conversations de groupe nécessitent des approbateurs explicites avant d'acheminer les invites d'approbation.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-native.ts:612` : la description de la capacité de livraison indique aux opérateurs de configurer `allowFrom`.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-reactions.ts:17` : l'espace de noms persistant est `imessage.approval-reactions`.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-reactions.ts:272` : l'analyseur de ligne de commande `/approve` gère les identifiants d'approbation et les décisions.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-reactions.ts:514` : le résolveur de réaction lit les approbateurs explicites.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-reaction-poller.ts:87` : l'interrogateur limite la découverte via `chats.list`.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-reaction-poller.ts:261` : l'interrogateur convertit les réactions de message en charges utiles de réaction d'approbation.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-seed.ts:51` : la session iMessage ensemencée existe pour les surfaces MCP au niveau du canal.
- `/Users/kevinlin/code/openclaw/src/agents/tools/message-tool.test.ts:1493` : l'outil de message dispose d'une fixture de plugin iMessage pour les surfaces action/target.
- Aucune voie d'approbation native ou de tapback en direct n'a été trouvée.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-native.test.ts:133` : la livraison exec en mode session fonctionne pour les origines iMessage correspondantes.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-native.test.ts:188` : les cibles d'origine de groupe sont rejetées sans approbateurs.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-native.test.ts:202` : les cibles d'origine de groupe sont autorisées avec des approbateurs explicites.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-native.test.ts:292` : les invites d'approbation exec affichent des indices de réaction.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-native.test.ts:459` : la suppression de secours s'applique uniquement lorsque la cible native d'origine de session exacte correspond.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-reactions.test.ts:80` : allow-always se résout via le choix de réaction partagé.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-reactions.test.ts:509` : les réactions d'approbation directes se résolvent à partir des expéditeurs autorisés.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-reactions.test.ts:582` : les réactions des expéditeurs ne figurant pas sur la liste des approbateurs sont refusées.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-reaction-poller.test.ts:63` : la découverte de chat récent délimitée observe les invites d'approbation.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-auth.test.ts:128` : les entrées de cible de chat sont rejetées comme approbateurs même avec des préfixes de service.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "iMessage approval reactions" --json --limit 6`

Résultats :

- Problème ouvert #85954 : formatage du corps attribué iMessage pour les invites d'approbation,
  référençant les travaux antérieurs de réaction d'approbation iMessage.

Requête :

`gitcrawl search openclaw/openclaw --query "iMessage approval reaction approve allowFrom" --json --limit 6`

Résultats :

- Aucun résultat direct dans la dernière passe.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "iMessage approval reactions" --limit 6`

Résultats :

- Le rapport de maintenance 2026-05 a mentionné les réactions d'approbation iMessage.
- La discussion de maintenance 2026-05 a posé des questions sur les approbations dans iMessage et WhatsApp
  via des réactions pour les clients sans meilleure interface utilisateur d'approbation.

Requête :

`/Users/kevinlin/.local/bin/discrawl search "iMessage approval reaction approve allowFrom" --limit 6`

Résultats :

- Aucun extrait retourné.
