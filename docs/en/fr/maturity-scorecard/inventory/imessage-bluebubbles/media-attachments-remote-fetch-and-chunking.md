---
title: "iMessage / BlueBubbles - Note de maturité des médias et du contenu enrichi"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iMessage / BlueBubbles - Note de maturité des médias et du contenu enrichi

## Résumé

Les médias, les pièces jointes, la récupération à distance et le chunking sont en version Bêta. La fonctionnalité dispose d'une implémentation réelle pour les listes blanches de pièces jointes entrantes, la mise en scène des médias, les récupérations de pièces jointes à distance, les envois de médias sortants, le chunking de texte et les reçus de réponse/média. Elle est maintenue en version Bêta car le comportement des médias est toujours en évolution active : les envois de médias par handle direct, les médias de groupe, les racines de pièces jointes et les pièces jointes de réponse montrent tous une activité d'archive récente.

## Normalisation

Catégorie active après la normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Médias et contenu enrichi`
- Fusionnée à partir de : `Messages enrichis et actions`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Médias : Couvre les médias dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes à distance, les récupérations SCP `remoteHost`, la conversion HEIC, les limites de taille, les envois de médias sortants, `send-attachment`, le chunking de texte et les reçus de médias.
- Pièces jointes : Couvre les pièces jointes dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes à distance, les récupérations SCP `remoteHost`, la conversion HEIC, les limites de taille, les envois de médias sortants, `send-attachment`, le chunking de texte et les reçus de médias.
- Récupération à distance : Couvre la récupération à distance dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes à distance, les récupérations SCP `remoteHost`, la conversion HEIC, les limites de taille, les envois de médias sortants, `send-attachment`, le chunking de texte et les reçus de médias.
- Chunking : Couvre le chunking dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes à distance, les récupérations SCP `remoteHost`, la conversion HEIC, les limites de taille, les envois de médias sortants, `send-attachment`, le chunking de texte et les reçus de médias.
- Actions natives : Couvre les actions natives dans le sondage d'API privée, la disponibilité des actions, les portes de configuration des actions, le mappage des tapbacks, l'édition/l'annulation/la réponse/les effets/la gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/la grammaire cible et les erreurs de dispatch d'action.
- API privée : Couvre l'API privée dans le sondage d'API privée, la disponibilité des actions, les portes de configuration des actions, le mappage des tapbacks, l'édition/l'annulation/la réponse/les effets/la gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/la grammaire cible et les erreurs de dispatch d'action.
- Outil de message : Couvre l'outil de message dans le sondage d'API privée, la disponibilité des actions, les portes de configuration des actions, le mappage des tapbacks, l'édition/l'annulation/la réponse/les effets/la gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/la grammaire cible et les erreurs de dispatch d'action.

## Fonctionnalités

- Médias : Couvre les médias dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes à distance, les récupérations SCP `remoteHost`, la conversion HEIC, les limites de taille, les envois de médias sortants, `send-attachment`, le chunking de texte et les reçus de médias.
- Pièces jointes : Couvre les pièces jointes dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes à distance, les récupérations SCP `remoteHost`, la conversion HEIC, les limites de taille, les envois de médias sortants, `send-attachment`, le chunking de texte et les reçus de médias.
- Récupération à distance : Couvre la récupération à distance dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes à distance, les récupérations SCP `remoteHost`, la conversion HEIC, les limites de taille, les envois de médias sortants, `send-attachment`, le chunking de texte et les reçus de médias.
- Chunking : Couvre le chunking dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes à distance, les récupérations SCP `remoteHost`, la conversion HEIC, les limites de taille, les envois de médias sortants, `send-attachment`, le chunking de texte et les reçus de médias.
- Actions natives : Couvre les actions natives dans le sondage d'API privée, la disponibilité des actions, les portes de configuration des actions, le mappage des tapbacks, l'édition/l'annulation/la réponse/les effets/la gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/la grammaire cible et les erreurs de dispatch d'action.
- API privée : Couvre l'API privée dans le sondage d'API privée, la disponibilité des actions, les portes de configuration des actions, le mappage des tapbacks, l'édition/l'annulation/la réponse/les effets/la gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/la grammaire cible et les erreurs de dispatch d'action.
- Outil de message : Couvre l'outil de message dans le sondage d'API privée, la disponibilité des actions, les portes de configuration des actions, le mappage des tapbacks, l'édition/l'annulation/la réponse/les effets/la gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/la grammaire cible et les erreurs de dispatch d'action.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (74%)`
- Signaux positifs :
  - La documentation couvre l'opt-in des pièces jointes, la récupération des pièces jointes à distance, les limites des médias et les avertissements de migration.
  - La source résout les racines de pièces jointes locales et à distance, met en scène les médias avec des vérifications de chemin et de taille, gère la conversion HEIC et dispose de solutions de secours pour l'envoi sortant.
  - Les tests couvrent la mise en scène des médias, la sécurité des chemins SCP à distance, l'accès à la racine des outils image/média, les routes d'envoi de médias directs et la plomberie des pièces jointes de réponse.
  - La graine e2e du canal MCP inclut un message de pièce jointe iMessage et un chemin de récupération.
- Signaux négatifs :
  - Aucune voie d'envoi/réception de pièce jointe iMessage en direct n'a été trouvée.
  - Les archives GitHub et Discord montrent des corrections récentes spécifiques aux médias et des problèmes ouverts.
  - Le comportement des pièces jointes à distance dépend du contexte SSH/SCP et des chemins de fichiers hôtes.
- Lacunes d'intégration :
  - Ajouter des scénarios de médias iMessage en direct/faux pour l'image entrante, la voix/vidéo entrante, la récupération de pièce jointe à distance, les médias de handle direct sortants, les médias de groupe et la réponse avec pièce jointe.

## Score de qualité

- Score : `Bêta (72%)`
- Rapports Gitcrawl :
  - `iMessage media attachments` a retourné le problème ouvert #87597 pour les envois de médias par handle direct utilisant le chemin RPC hérité au lieu de `send.attachment`, la PR ouverte #87715 pour les légendes de médias directs via les pièces jointes et le problème #47856 concernant les racines de médias configurables.
  - `iMessage send-rich` a retourné #84329, #87597 et #85954, reflétant le travail d'envoi enrichi, de médias et de formatage des invites d'approbation.
- Rapports Discrawl :
  - `iMessage media attachments` a retourné une note de responsable de 2026-05 listant le travail des médias iMessage : pièces jointes hydratées sur réponse, racines de pièces jointes d'image, médias de groupe, historique DM, réponses en double et bruit stderr d'AddressBook.
  - La même requête a retourné des commentaires d'archive pour les racines de pièces jointes et le comportement des espaces réservés de médias.
- Bonnes qualités :
  - L'ingestion de pièces jointes est opt-in et contrainte par la racine.
  - Les récupérations à distance distinguent les racines à distance des racines locales et assainissent les chemins SCP.
  - Le code d'envoi sortant dispose de solutions de secours explicites et signale les envois de pièces jointes échoués au lieu de prétendre au succès.
  - Les racines de médias sont intégrées aux outils image et média au lieu d'être isolées à l'intérieur du canal.
- Mauvaises qualités :
  - L'activité d'archive récente montre que le comportement des médias est toujours en cours de réparation dans des cas limites importants.
  - Les médias à distance dépendent du `remoteHost` fourni par l'opérateur et des racines du système de fichiers Mac correspondantes.
  - Les pièces jointes entrantes sont désactivées par défaut, créant un piège de configuration courant « suppression silencieuse ».
- Exclu de la qualité :
  - Les preuves de test unitaire, d'intégration, e2e, en direct et de flux d'exécution sont enregistrées sous Couverture uniquement.

## Score de complétude

- Score : `Bêta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/imessage-bluebubbles.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les médias, les pièces jointes, la récupération à distance, le chunking, les actions natives, l'API privée et l'outil de message.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connus utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La preuve de médias en direct est manquante.
- Les médias de handle direct et de groupe ont une agitation d'archive actuelle/ouverte.
- Les récupérations SCP à distance restent sensibles à l'environnement.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:458` : l'ingestion des pièces jointes entrantes est désactivée par défaut.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:459` : les chemins des pièces jointes distantes peuvent être récupérés par SCP lorsque `remoteHost` est défini.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage-from-bluebubbles.md:111` : le `includeAttachments` migré doit être défini explicitement sur iMessage.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage-from-bluebubbles.md:113` : `remoteAttachmentRoots` est utilisé lorsque `remoteHost` active les récupérations SCP.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage-from-bluebubbles.md:114` : la taille maximale des médias iMessage est par défaut de 16 Mo.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md:642` : la référence de configuration indique que `includeAttachments` est désactivé par défaut.

### Source

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:227` : l'exécution définit par défaut `includeAttachments` à false.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:228` : l'exécution définit par défaut la taille maximale des médias à 16 Mo.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:452` : les pièces jointes ne sont lues que lorsque l'ingestion des pièces jointes est activée.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:621` : les messages d'hôte distant conservent les pièces jointes multimédias brutes pour la récupération à distance.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/media-contract.ts:25` : les racines des pièces jointes distantes fusionnent la configuration du compte et du canal.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/send.ts:715` : les médias sortants peuvent utiliser `send-attachment`.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/send.ts:797` : le chemin d'envoi transmet le `remoteHost` du compte.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/send.ts:808` : le chemin d'envoi applique la taille maximale des médias configurée.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-seed.ts:80` : les données de canal ensemencées incluent un message avec pièce jointe.
- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-docker-client.ts:203` : le client Docker MCP appelle `attachments_fetch`.
- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-docker-client.ts:212` : la récupération de pièce jointe ensemencée retourne une pièce jointe.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply.stage-sandbox-media.scp-remote-path.test.ts:99` : les noms de fichiers de pièces jointes distantes contenant des métacaractères shell sont rejetés avant le lancement de SCP.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/media-staging.test.ts:24` : les pièces jointes iMessage autorisées sont copiées dans le magasin de médias entrants.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/media-staging.test.ts:49` : les chemins s'échappant des racines autorisées sont supprimés.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/media-staging.test.ts:80` : les pièces jointes HEIC sont converties en JPEG avant la mise en scène.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/media-staging.test.ts:105` : les pièces jointes surdimensionnées sont supprimées.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/send.test.ts:94` : les charges utiles explicites de médias uniquement du chat sont acheminées via le transport automatique `send-attachment`.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/send.test.ts:174` : l'envoi revient à RPC lorsque `send-attachment` n'est pas disponible.
- `/Users/kevinlin/code/openclaw/src/agents/tools/image-tool.test.ts:1782` : les chemins d'images des racines de pièces jointes du compte iMessage actuel sont autorisés.
- `/Users/kevinlin/code/openclaw/src/agents/tools/media-tool-shared.test.ts:87` : les racines des pièces jointes entrantes du canal restent séparées des racines locales.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "iMessage media attachments" --json --limit 6`

Résultats :

- Problème ouvert #87597 : les envois de médias iMessage à poignée directe utilisent le chemin RPC hérité au lieu de `send.attachment`.
- PR ouvert #87715 : acheminer les légendes de médias directs via les pièces jointes.
- Problème ouvert #47856 : racines de médias locales configurables.

Requête :

`gitcrawl search openclaw/openclaw --query "iMessage send-rich" --json --limit 6`

Résultats :

- Problème ouvert #84329 pour la préférence de transport IMCore/API privée configurable.
- Problème ouvert #87597 pour les envois de médias à poignée directe.
- Problème ouvert #85954 pour le formatage de l'invite d'approbation via le corps attribué.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "iMessage media attachments" --limit 6`

Résultats :

- Le fil de discussion du responsable de 2026-05 a énuméré les travaux sur les médias iMessage autour des pièces jointes de réponse hydratées, des racines de pièces jointes d'images, des médias de groupe, de l'historique des messages directs, des réponses en double et du bruit stderr d'AddressBook.
- Les commentaires d'archive ont référencé les racines des pièces jointes et le comportement visible du placeholder de médias.

Requête :

`/Users/kevinlin/.local/bin/discrawl search "iMessage send-rich" --limit 6`

Résultats :

- Les extraits du responsable ont référencé le travail fusionné pour les pièces jointes de réponse iMessage via `send-rich --file`.
