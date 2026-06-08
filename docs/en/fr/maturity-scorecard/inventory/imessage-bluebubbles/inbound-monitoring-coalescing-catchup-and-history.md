---
title: "iMessage / BlueBubbles - Note de maturité du routage et de la livraison des conversations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iMessage / BlueBubbles - Note de maturité du routage et de la livraison des conversations

## Résumé

La surveillance des messages entrants, la coalescence, la récupération et l'historique sont en version Bêta. Le composant dispose d'un code d'exécution substantiel et de tests ciblés pour `watch.subscribe`, la réessai au démarrage, la coalescence/débounce, la suppression d'écho, l'historique des messages directs, les événements de réaction et les curseurs de récupération. Il n'est pas Stable car `watch.subscribe` en direct est un risque récurrent et la correction de la récupération dépend du tri réel de chat.db, du timing de redémarrage/sommeil de la passerelle et du comportement du client Apple.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Routage et livraison des conversations`
- Fusionnée à partir de : `Ingestion et historique des messages`, `Routage et accès aux conversations`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Surveiller les messages en direct : Couvre la surveillance des messages en direct sur `watch.subscribe` entrant, l'analyse des notifications, les garde-fous d'écho et d'auto-chat, le cache des messages envoyés, la coalescence des messages directs du même expéditeur, l'historique des messages directs, le routage des événements de réaction, la relecture du curseur de récupération et l'avancement du curseur en direct.
- Fusionner les messages directs divisés : Couvre la fusion des messages directs divisés sur `watch.subscribe` entrant, l'analyse des notifications, les garde-fous d'écho et d'auto-chat, le cache des messages envoyés, la coalescence des messages directs du même expéditeur, l'historique des messages directs, le routage des événements de réaction, la relecture du curseur de récupération et l'avancement du curseur en direct.
- Relire les messages manqués : Couvre la relecture des messages manqués sur `watch.subscribe` entrant, l'analyse des notifications, les garde-fous d'écho et d'auto-chat, le cache des messages envoyés, la coalescence des messages directs du même expéditeur, l'historique des messages directs, le routage des événements de réaction, la relecture du curseur de récupération et l'avancement du curseur en direct.
- Amorcer l'historique des conversations : Couvre l'amorçage de l'historique des conversations sur `watch.subscribe` entrant, l'analyse des notifications, les garde-fous d'écho et d'auto-chat, le cache des messages envoyés, la coalescence des messages directs du même expéditeur, l'historique des messages directs, le routage des événements de réaction, la relecture du curseur de récupération et l'avancement du curseur en direct.
- Autoriser les expéditeurs directs : Couvre l'autorisation des expéditeurs directs sur `dmPolicy`, `allowFrom`, l'appairage, la normalisation de l'identité de l'expéditeur et le comportement d'appairage, d'accès et de routage de session dm associé.
- Acheminer les conversations directes : Couvre l'acheminement des conversations directes sur `dmPolicy`, `allowFrom`, l'appairage, la normalisation de l'identité de l'expéditeur et le comportement d'appairage, d'accès et de routage de session dm associé.
- Lier les sessions ACP : Couvre la liaison des sessions ACP sur `dmPolicy`, `allowFrom`, l'appairage, la normalisation de l'identité de l'expéditeur et le comportement d'appairage, d'accès et de routage de session dm associé.
- Politique de groupe : Couvre la politique de groupe sur `groupPolicy`, `groupAllowFrom`, `groups`, les entrées du registre générique, `requireMention`, les modèles de mention, les outils par groupe, les invites système par groupe, les sessions de groupe et les avertissements pour la mauvaise configuration de la liste d'autorisation.
- Mentions : Couvre les mentions sur `groupPolicy`, `groupAllowFrom`, `groups`, les entrées du registre générique, `requireMention`, les modèles de mention, les outils par groupe, les invites système par groupe, les sessions de groupe et les avertissements pour la mauvaise configuration de la liste d'autorisation.
- Invites système : Couvre les invites système sur `groupPolicy`, `groupAllowFrom`, `groups`, les entrées du registre générique, `requireMention`, les modèles de mention, les outils par groupe, les invites système par groupe, les sessions de groupe et les avertissements pour la mauvaise configuration de la liste d'autorisation.

## Fonctionnalités

- Surveiller les messages en direct : Couvre la surveillance des messages en direct sur `watch.subscribe` entrant, l'analyse des notifications, les garde-fous d'écho et d'auto-chat, le cache des messages envoyés, la coalescence des messages directs du même expéditeur, l'historique des messages directs, le routage des événements de réaction, la relecture du curseur de récupération et l'avancement du curseur en direct.
- Fusionner les messages directs divisés : Couvre la fusion des messages directs divisés sur `watch.subscribe` entrant, l'analyse des notifications, les garde-fous d'écho et d'auto-chat, le cache des messages envoyés, la coalescence des messages directs du même expéditeur, l'historique des messages directs, le routage des événements de réaction, la relecture du curseur de récupération et l'avancement du curseur en direct.
- Relire les messages manqués : Couvre la relecture des messages manqués sur `watch.subscribe` entrant, l'analyse des notifications, les garde-fous d'écho et d'auto-chat, le cache des messages envoyés, la coalescence des messages directs du même expéditeur, l'historique des messages directs, le routage des événements de réaction, la relecture du curseur de récupération et l'avancement du curseur en direct.
- Amorcer l'historique des conversations : Couvre l'amorçage de l'historique des conversations sur `watch.subscribe` entrant, l'analyse des notifications, les garde-fous d'écho et d'auto-chat, le cache des messages envoyés, la coalescence des messages directs du même expéditeur, l'historique des messages directs, le routage des événements de réaction, la relecture du curseur de récupération et l'avancement du curseur en direct.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (74%)`
- Signaux positifs :
  - La documentation décrit la récupération après arrêt, l'ordre de surveillance, les chemins de curseur, la coalescence et le dépannage.
  - La source implémente la réessai au démarrage, le raccourci de réaction d'approbation, la distribution normale, les clés de coalescence, la relecture de récupération et la protection du curseur.
  - Les tests couvrent l'épuisement des réessais, les cas limites de coalescence, la monotonie du curseur de récupération, la réessai en cas d'échec, la persistance du cache d'écho et les décisions de réaction entrante.
  - La preuve e2e du canal amorcé MCP prouve l'accès aux métadonnées de conversation et à la transcription pour un canal iMessage, bien que pas pour `imsg` en direct.
- Signaux négatifs :
  - Aucune preuve de `watch.subscribe` en direct n'a été trouvée.
  - Les rapports d'archive incluent les délais d'expiration de `watch.subscribe` et la dégradation de la disponibilité de la passerelle lors du changement de canal iMessage.
  - La récupération a de nombreuses branches de correction qui sont bien testées unitairement mais non prouvées contre les historiques réels de sommeil/redémarrage de chat.db.
- Lacunes d'intégration :
  - Ajouter une voie Mac contrôlée qui exerce les messages entrants en direct, le redémarrage de la passerelle, la récupération après arrêt, la prévention des doublons et la coalescence du même expéditeur.
  - Ajouter une intégration fake-imsg autour de `messages.history` hors ordre et de lignes en direct/relues qui se chevauchent.

## Score de qualité

- Score : `Bêta (73%)`
- Rapports Gitcrawl :
  - `imsg rpc timeout gateway` a retourné #87263 pour le délai d'expiration de `watch.subscribe` à chaque démarrage de la passerelle.
  - `iMessage catchup coalesce history watch.subscribe echo` n'a retourné aucun résultat direct lors de la dernière passe gitcrawl.
- Rapports Discrawl :
  - `imsg rpc timeout gateway` a retourné des extraits de support avec les boucles de redémarrage `imsg rpc not ready` et les délais de disponibilité de la passerelle.
  - `iMessage catchup coalesce history watch.subscribe echo` n'a retourné aucun extrait.
- Bonnes qualités :
  - L'ordre de démarrage est intentionnel : attendre le transport, s'abonner, puis exécuter la récupération avant d'entrer dans la boucle de distribution en direct.
  - La logique du curseur de récupération protège contre le saut des lignes échouées et a un comportement d'abandon explicite.
  - La détection d'écho/auto-chat utilise à la fois l'état des messages envoyés transitoire et persistant.
  - La coalescence préserve les métadonnées de pièce jointe et GUID au lieu de simplement fusionner le texte.
- Mauvaises qualités :
  - `watch.subscribe` est opérationnellement fragile et peut mettre le canal hors ligne.
  - La récupération et la prévention d'écho dépendent du timing et des identifiants de l'état Messages externe.
  - Le sommeil de la passerelle, le sommeil du Mac et le comportement d'écho multi-appareils sont difficiles à modéliser dans les vérifications locales uniquement.
- Exclu de la qualité :
  - Les preuves de test unitaire, d'intégration, e2e, en direct et de flux d'exécution sont enregistrées sous Couverture uniquement.

## Score de complétude

- Score : `Bêta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/imessage-bluebubbles.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Surveiller les messages en direct, Fusionner les messages directs divisés, Relire les messages manqués, Amorcer l'historique des conversations.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La preuve entrante/récupération en direct est manquante.
- Les délais d'expiration de `watch.subscribe` sont des preuves de terrain actives.
- Le comportement de sommeil/redémarrage n'est pas prouvé sous l'historique réel de Messages.app.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:12` : la rattrapage est optionnel et rejoue les messages arrivés pendant que Gateway était arrêté.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:672` : les paramètres de coalescence BlueBubbles doivent migrer vers `channels.imessage.coalesceSameSenderDms`.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:711` : le rattrapage est séquencé comme suit : `imsg` prêt, `watch.subscribe`, rattrapage, puis dispatch en direct.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:717` : le chemin du curseur de rattrapage se trouve sous le répertoire d'état OpenClaw.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:729` : les lignes traitées en direct font avancer le même curseur uniquement après la réussite du rattrapage au démarrage.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:730` : les défaillances répétées de lignes forcent finalement l'avancement au-delà d'un message bloqué.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:736` : les journaux de rattrapage incluent les comptages de rejeu, ignoré, échoué et récupéré.

## Source

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:261` : les modifications de coalescence modifient le comportement de débounce lorsqu'elles sont activées.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:297` : les DM coalescés sont indexés par chat et expéditeur.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:487` : le raccourci de réaction d'approbation contourne le dispatch normal pour la résolution d'approbation.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:989` : l'exécution s'abonne via `watch.subscribe`.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.ts:1086` : le rattrapage s'exécute entre `watch.subscribe` et le dispatch en direct.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/catchup.ts:368` : `performIMessageCatchup` est le point d'entrée de rejeu.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/catchup.ts:527` : le rattrapage évite le chevauchement de dispatch en double.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/coalesce.ts:13` : les messages coalescés préservent le suivi GUID pour les chemins de rejeu.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-seed.ts:58` : les données de départ incluent un aperçu de transcription iMessage.
- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-docker-client.ts:172` : le client MCP Docker lit les messages de transcription ensemencés.
- Aucune voie d'intégration `watch.subscribe` en direct ou de rattrapage n'a été trouvée.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor.watch-subscribe-retry.test.ts:81` : le délai d'expiration transitoire de `watch.subscribe` réessaie sans démonter le moniteur.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor.watch-subscribe-retry.test.ts:122` : les tentatives limitées finissent par échouer.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/catchup.test.ts:244` : les nouvelles lignes entrantes sont rejouées et le curseur avance.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/catchup.test.ts:311` : les lignes défaillantes maintiennent le curseur en dessous du nombre maximum de tentatives.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/catchup.test.ts:413` : un succès ultérieur ne dépasse pas une défaillance maintenue.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/coalesce.test.ts:36` : le texte et l'URL envoyés séparément fusionnent en une seule charge utile.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/coalesce.test.ts:61` : la coalescence préserve les pièces jointes.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/monitor-provider.echo-cache.test.ts:128` : le cache d'écho conserve les entrées assez longtemps pour le rejeu de rattrapage.

## Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "imsg rpc timeout gateway" --json --limit 6`

Résultats :

- Problème ouvert #87263 : délai d'expiration de `watch.subscribe` à chaque démarrage de Gateway.

Requête :

`gitcrawl search openclaw/openclaw --query "iMessage catchup coalesce history watch.subscribe echo" --json --limit 6`

Résultats :

- Aucun résultat direct dans la dernière analyse.

## Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "imsg rpc timeout gateway" --limit 6`

Résultats :

- Les extraits Discord ont signalé des boucles `imsg rpc not ready`, des sorties de canal et une dégradation de la disponibilité de Gateway.

Requête :

`/Users/kevinlin/.local/bin/discrawl search "iMessage catchup coalesce history watch.subscribe echo" --limit 6`

Résultats :

- Aucun extrait retourné.
