---
title: "Slack - Note de Maturité du Routage et de la Livraison des Conversations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Slack - Note de Maturité du Routage et de la Livraison des Conversations

## Résumé

Le routage des canaux et threads Slack est l'une des familles Slack les mieux documentées. Les docs et le modèle source couvrent les ID de canaux, les portes de mention, les listes blanches de bot/utilisateur, `replyToMode`, `thread_ts`, les suffixes de session, le contexte du démarreur de thread, et le suivi/l'isolation des threads en direct. La qualité reste Beta car l'historique des archives montre des corrections actives autour de la continuité des sessions de thread, du fan-out des threads DM d'assistant, du statut des threads d'interaction, et des attentes confuses de `replyToMode`.

## Normalisation

Catégorie active après la normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Conversation Routing and Delivery`
- Fusionnée à partir de : `Conversation Access and Routing`, `Message Delivery and Media`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Listes blanches de canaux : Couvre les listes blanches de canaux, `groupPolicy`, les portes de canal/utilisateur, les portes de mention, et le comportement des mentions de sous-équipe.
- Routage des threads : Couvre le routage des threads Slack, le ciblage des réponses conscientes des threads, et la liaison de session pour les threads de canal.
- Isolation de Session : Couvre l'Isolation de Session sur les listes blanches de canaux, `groupPolicy`, les portes de canal/utilisateur, le comportement des mentions et des mentions de sous-équipe, et le routage de canal/thread et le comportement d'isolation de session associés.
- Appairage DM : Couvre l'Appairage DM sur le routage DM Slack, `dmPolicy`, `allowFrom`, les approbations d'appairage, les DM de groupe/MPIM, l'héritage de la liste blanche au niveau du compte, l'autorisation des commandes dans les DM, et la normalisation de l'identité de l'expéditeur.
- Autorisation de l'Expéditeur : Couvre l'Autorisation de l'Expéditeur sur le routage DM Slack, `dmPolicy`, `allowFrom`, les approbations d'appairage, les DM de groupe/MPIM, l'héritage de la liste blanche au niveau du compte, l'autorisation des commandes dans les DM, et la normalisation de l'identité de l'expéditeur.
- Livraison Sortante : Couvre la Livraison Sortante sur la livraison de texte/bloc `message.send`, les réponses de thread, `replyBroadcast`, le chunking, et le comportement associé de livraison sortante, streaming, et réactions.
- Streaming : Couvre le Streaming sur la livraison de texte/bloc `message.send`, les réponses de thread, `replyBroadcast`, le chunking, et le comportement associé de livraison sortante, streaming, et réactions.
- Réactions : Couvre les Réactions sur la livraison de texte/bloc `message.send`, les réponses de thread, `replyBroadcast`, le chunking, et le comportement associé de livraison sortante, streaming, et réactions.
- Média : Couvre le Média sur les fichiers entrants Slack, le téléchargement/l'authentification d'URL privée, les plafonds de taille de média, le contexte du média du démarreur de thread, et le comportement associé de média, pièces jointes, fichiers, et vision.
- Pièces Jointes : Couvre les Pièces Jointes sur les fichiers entrants Slack, le téléchargement/l'authentification d'URL privée, les plafonds de taille de média, le contexte du média du démarreur de thread, et le comportement associé de média, pièces jointes, fichiers, et vision.
- Fichiers : Couvre les Fichiers sur les fichiers entrants Slack, le téléchargement/l'authentification d'URL privée, les plafonds de taille de média, le contexte du média du démarreur de thread, et le comportement associé de média, pièces jointes, fichiers, et vision.
- Vision : Couvre la Vision sur les fichiers entrants Slack, le téléchargement/l'authentification d'URL privée, les plafonds de taille de média, le contexte du média du démarreur de thread, et le comportement associé de média, pièces jointes, fichiers, et vision.
- Livraison Sortante : Couvre la Livraison Sortante sur la livraison de texte/bloc `message.send`, les réponses de thread, `replyBroadcast`, le chunking, et le comportement associé de livraison sortante, streaming, et réactions
- Streaming : Couvre le Streaming sur la livraison de texte/bloc `message.send`, les réponses de thread, `replyBroadcast`, le chunking, et le comportement associé de livraison sortante, streaming, et réactions
- Réactions : Couvre les Réactions sur la livraison de texte/bloc `message.send`, les réponses de thread, `replyBroadcast`, le chunking, et le comportement associé de livraison sortante, streaming, et réactions
- Média : Couvre le Média sur les fichiers entrants Slack, le téléchargement/l'authentification d'URL privée, les plafonds de taille de média, le contexte du média du démarreur de thread, et le comportement associé de média, pièces jointes, fichiers, et vision
- Pièces Jointes : Couvre les Pièces Jointes sur les fichiers entrants Slack, le téléchargement/l'authentification d'URL privée, les plafonds de taille de média, le contexte du média du démarreur de thread, et le comportement associé de média, pièces jointes, fichiers, et vision
- Fichiers : Couvre les Fichiers sur les fichiers entrants Slack, le téléchargement/l'authentification d'URL privée, les plafonds de taille de média, le contexte du média du démarreur de thread, et le comportement associé de média, pièces jointes, fichiers, et vision
- Vision : Couvre la Vision sur les fichiers entrants Slack, le téléchargement/l'authentification d'URL privée, les plafonds de taille de média, le contexte du média du démarreur de thread, et le comportement associé de média, pièces jointes, fichiers, et vision

## Fonctionnalités

- Listes blanches de canaux : Couvre les listes blanches de canaux, `groupPolicy`, les portes de canal/utilisateur, les portes de mention, et le comportement des mentions de sous-équipe.
- Routage des threads : Couvre le routage des threads Slack, le ciblage des réponses conscientes des threads, et la liaison de session pour les threads de canal.
- Isolation de Session : Couvre l'Isolation de Session sur les listes blanches de canaux, `groupPolicy`, les portes de canal/utilisateur, le comportement des mentions et des mentions de sous-équipe, et le routage de canal/thread et le comportement d'isolation de session associés.
- Appairage DM : Couvre l'Appairage DM sur le routage DM Slack, `dmPolicy`, `allowFrom`, les approbations d'appairage, les DM de groupe/MPIM, l'héritage de la liste blanche au niveau du compte, l'autorisation des commandes dans les DM, et la normalisation de l'identité de l'expéditeur.
- Autorisation de l'Expéditeur : Couvre l'Autorisation de l'Expéditeur sur le routage DM Slack, `dmPolicy`, `allowFrom`, les approbations d'appairage, les DM de groupe/MPIM, l'héritage de la liste blanche au niveau du compte, l'autorisation des commandes dans les DM, et la normalisation de l'identité de l'expéditeur.

## Fraîcheur des Archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (80%)`
- Signaux positifs : La voie Slack en direct inclut les portes de mention, le bloc de liste blanche, la forme de réponse de haut niveau, le redémarrage-reprise, le suivi des threads, et l'isolation des threads ; les tests unitaires couvrent le routage des threads, les clés de session, le contournement des mentions, les modes de réponse, les portes de canal, et le contexte du thread d'assistant.
- Signaux négatifs : La couverture en direct n'exerce pas encore les mentions de groupe d'utilisateurs, les messages de salle créés par un bot, la migration des noms de canaux, les échecs d'adhésion à l'audience du canal, ou toutes les variantes de `replyToMode`.
- Lacunes d'intégration : Ajouter des tests en direct pour `replyToMode=first|batched`, `thread.inheritParent`, `thread.requireExplicitMention`, les messages de canal créés par un bot, le routage des mentions de sous-équipe, et la migration des ID de canal.

## Score de Qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : `#78061`, `#80632`, `#85904`, `#82895`, `#63230`, `#87019`, `#63840`, `#63904`, `#61502`, et `#62066` montrent des préoccupations actives concernant le routage des threads, les threads d'assistant, la diffusion des réponses, et les mentions implicites.
- Rapports Discrawl : Le thread de support `replyToMode: all` de Slack décrit un vrai flux de travail d'examen de document où le premier tour de canal et la division de session de thread ultérieure divisent le contexte de manière inattendue.
- Bonnes qualités : La source ensemence maintenant les racines de haut niveau éligibles dans les sessions de thread, préserve le `thread_ts` de Slack, garde les réponses de haut niveau isolées, et enregistre la participation aux threads Slack.
- Mauvaises qualités : Le comportement des threads est difficile à raisonner car Slack cache les réponses de thread du canal, les événements de thread d'assistant introduisent des formes `thread_ts` supplémentaires, et les attentes des opérateurs diffèrent souvent de la sémantique du modèle de session.
- Exclu de la qualité : Nombre de tests unitaires, largeur de voie en direct, et profondeur d'intégration.

## Score de Complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/slack.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour les Listes blanches de canaux, le Routage des threads, l'Isolation de Session, l'Appairage DM, l'Autorisation de l'Expéditeur.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter un scénario d'examen de document en direct prouvant que la première mention de canal plus le téléchargement de fichier passe proprement à une session de portée de thread.
- Ajouter une trace de décision de routage de thread générée pour `replyToMode`, `thread.inheritParent`, et le contournement des mentions implicites.
- Ajouter une couverture de scorecard explicite pour l'effondrement des threads DM de l'application d'assistant Slack par rapport à l'isolation par thread.

## Preuves

### Docs

- `docs/channels/slack.md` documente la politique des canaux, les exigences d'ID de canal stable, les sources de mention, les contrôles par canal, les clés de session de thread, `replyToMode`, `thread.requireExplicitMention`, et les balises de réponse manuelle.
- `docs/channels/bot-loop-protection.md` et `docs/channels/channel-routing.md` sont des références de comportement partagé liées.

### Source

- `extensions/slack/src/monitor/message-handler/prepare.ts` résout l'autorisation, l'état de mention, le routage de thread ensemencé, le contexte de thread assistant, l'historique du démarreur de thread, et les métadonnées de tour final.
- `extensions/slack/src/threading.ts`, `extensions/slack/src/thread-ts.ts`, `extensions/slack/src/threading-tool-context.ts`, et `extensions/slack/src/action-threading.ts` normalisent les identifiants de thread Slack et l'héritage de thread d'action.
- `extensions/slack/src/channel.ts` expose le comportement de threading Slack au plugin de canal.
- `extensions/slack/src/monitor/message-handler/subteam-mentions.ts` gère le comportement de mention de groupe d'utilisateurs Slack.

### Tests d'intégration

- `extensions/qa-lab/src/live-transports/slack/slack-live.runtime.ts` définit `slack-mention-gating`, `slack-allowlist-block`, `slack-top-level-reply-shape`, `slack-thread-follow-up`, et `slack-thread-isolation`.
- `extensions/qa-lab/src/live-transports/slack/slack-live.runtime.test.ts` affirme que la liste de scénario de transport en direct standard inclut le suivi de thread et l'isolation.

### Tests unitaires

- `extensions/slack/src/action-threading.test.ts` couvre le threading automatique du même canal et l'échec fermé des horodatages de thread manquants.
- `extensions/slack/src/action-runtime.test.ts` couvre `replyToMode=all|first|off`, les remplacements de thread explicites, les lectures dans les threads, et les lectures de cible autorisées.
- `extensions/slack/src/monitor/message-handler/prepare-thread-context.test.ts`, `prepare-thread-context-root.test.ts`, `prepare.thread-session-key.test.ts`, `monitor.threading.missing-thread-ts.test.ts`, et `threading.test.ts` couvrent la préparation de thread Slack.
- `src/auto-reply/reply/session.test.ts`, `reply-plumbing.test.ts`, et `route-reply.test.ts` couvrent le routage de session/thread Slack à partir du chemin de réponse partagé.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "Slack channel requireMention thread_ts replyToMode session routing" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10`
- `gitcrawl search openclaw/openclaw --query "slack thread" --json`

Résultats :

- La recherche de problème ciblée a retourné `[]`.
- La requête plus large a retourné des éléments de thread/session Slack ouverts incluant `#80632`, `#85904`, `#49747`, `#82895`, `#78061`, `#82886`, `#63230`, `#87019`, `#63904`, `#61502`, et `#62066`.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Slack thread replyToMode requireExplicitMention"`

Résultats :

- A retourné un fil de support détaillé sur `replyToMode: all` traitant le premier message dans la session principale du canal, puis créant une nouvelle session de thread sans contexte d'outil/réflexion antérieur ; a également retourné `#63389` sur `thread.requireExplicitMention` documenté étant rejeté par une configuration plus ancienne.
