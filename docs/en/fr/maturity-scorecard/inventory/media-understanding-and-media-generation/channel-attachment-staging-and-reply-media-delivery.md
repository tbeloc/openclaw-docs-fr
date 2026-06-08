---
title: "Compréhension des médias et génération de médias - Note de maturité de la gestion des médias de canal"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Compréhension des médias et génération de médias - Note de maturité de la gestion des médias de canal

## Résumé

La mise en scène des médias de canal et la livraison des réponses ont une large couverture source : les médias entrants sont normalisés, mis en scène dans des chemins visibles par le sandbox, représentés sous forme de `MediaPaths`/`MediaUrls`, et les médias sortants peuvent être livrés via les outils de message, les solutions de secours directes et les routes natives du canal. La qualité reste en dessous de stable car les preuves d'archive montrent des bogues de livraison visibles après la réussite de la génération et le comportement des médias spécifiques au canal varie toujours.

## Portée de la catégorie

Inclus dans cette catégorie :

- Mise en scène des pièces jointes entrantes : Couvre la mise en scène des pièces jointes entrantes sur la mise en scène des pièces jointes entrantes, les réécritures de sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias et le comportement associé de mise en scène des pièces jointes de canal et de livraison des médias de réponse.
- Réécritures de médias de sandbox : Couvre les réécritures de médias de sandbox sur la mise en scène des pièces jointes entrantes, les réécritures de sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias et le comportement associé de mise en scène des pièces jointes de canal et de livraison des médias de réponse.
- Modèle de médias de réponse : Couvre le modèle de médias de réponse sur la mise en scène des pièces jointes entrantes, les réécritures de sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias et le comportement associé de mise en scène des pièces jointes de canal et de livraison des médias de réponse.
- Livraison des pièces jointes de l'outil de message : Couvre la livraison des pièces jointes de l'outil de message sur la mise en scène des pièces jointes entrantes, les réécritures de sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias et le comportement associé de mise en scène des pièces jointes de canal et de livraison des médias de réponse.
- Suppression de la livraison en double : Couvre la suppression de la livraison en double sur la mise en scène des pièces jointes entrantes, les réécritures de sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias et le comportement associé de mise en scène des pièces jointes de canal et de livraison des médias de réponse.

## Fonctionnalités

- Mise en scène des pièces jointes entrantes : Couvre la mise en scène des pièces jointes entrantes sur la mise en scène des pièces jointes entrantes, les réécritures de sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias et le comportement associé de mise en scène des pièces jointes de canal et de livraison des médias de réponse.
- Réécritures de médias de sandbox : Couvre les réécritures de médias de sandbox sur la mise en scène des pièces jointes entrantes, les réécritures de sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias et le comportement associé de mise en scène des pièces jointes de canal et de livraison des médias de réponse.
- Modèle de médias de réponse : Couvre le modèle de médias de réponse sur la mise en scène des pièces jointes entrantes, les réécritures de sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias et le comportement associé de mise en scène des pièces jointes de canal et de livraison des médias de réponse.
- Livraison des pièces jointes de l'outil de message : Couvre la livraison des pièces jointes de l'outil de message sur la mise en scène des pièces jointes entrantes, les réécritures de sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias et le comportement associé de mise en scène des pièces jointes de canal et de livraison des médias de réponse.
- Suppression de la livraison en double : Couvre la suppression de la livraison en double sur la mise en scène des pièces jointes entrantes, les réécritures de sandbox, le modèle `MediaPath`/`MediaPaths`/`MediaUrls`, les notes de médias et le comportement associé de mise en scène des pièces jointes de canal et de livraison des médias de réponse.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs : La mise en scène entrante, la réécriture des chemins de sandbox, les notes de médias, la normalisation des charges utiles, la déduplication, la livraison de suivi et les charges utiles sortantes du canal sont représentées dans la source et les tests ciblés. La documentation des canaux couvre plusieurs avertissements spécifiques aux médias.
- Signaux négatifs : La couverture est large mais distribuée entre la réponse automatique, la passerelle, les plugins de canal et la livraison des outils d'agent plutôt qu'un seul sous-système délimité.
- Lacunes d'intégration : Le chemin de génération de médias à l'outil de message a une friction récurrente live/Discord qui n'est que partiellement capturée par les tests locaux.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : #86034 et #86279 montrent que la génération de médias a réussi tandis que l'échec de la livraison de la complétion a été signalé comme un échec de génération ; #87741 couvre le secours du verrou de remise des médias générés ; #86447 montre une inadéquation de réveil/source de complétion Slack ; #77265 couvre `agent --deliver` retournant une URL de médias sans livraison Telegram ; #68770 couvre les journaux de succès Telegram manquants pour les médias.
- Rapports Discrawl : Les archives des responsables et des clawtributors décrivent la génération réussie de médias suivie d'une remise de pièce jointe cassée, des réponses finales privées contenant des chemins `MEDIA:` et la nécessité d'appliquer ou d'effectuer la livraison de l'outil de message pour les contextes de canal.
- Bonnes qualités : La source distingue le succès de la tâche générée de la livraison, suit les médias envoyés par les outils de message, normalise les charges utiles de médias sortants, déduplique les médias déjà envoyés et met en scène les médias de sandbox avec des vérifications de source explicites.
- Mauvaises qualités : La livraison des médias est très sensible au contexte du canal et de la session ; les réveils de complétion asynchrones peuvent réussir tandis que la livraison visible des pièces jointes échoue.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, live et de flux d'exécution.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/media-understanding-and-media-generation.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la mise en scène des pièces jointes entrantes, les réécritures de médias de sandbox, le modèle de médias de réponse, la livraison des pièces jointes de l'outil de message, la suppression de la livraison en double.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La livraison des médias générés asynchrones reste le point faible opérationnel le plus visible.
- Les fonctionnalités de médias natifs du canal ont des légendes inégales, une gestion des notes vocales, des limites de taille de fichier et une journalisation du succès inégales.
- Les diagnostics des opérateurs nécessitent souvent de corréler l'état de la tâche, le réveil de l'agent, l'utilisation de l'outil de message et les journaux de livraison du canal.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/nodes/images.md` documente les médias entrants vers les commandes, les réécritures `MediaPath` de sandbox, `MediaPaths`, la compréhension des médias et les limites des canaux.
- `/Users/kevinlin/code/openclaw/docs/tools/media-overview.md` explique la livraison asynchrone de la génération de médias et la solution de secours directe.
- Les docs des canaux tels que `/Users/kevinlin/code/openclaw/docs/channels/discord.md`, `/Users/kevinlin/code/openclaw/docs/channels/line.md`, `/Users/kevinlin/code/openclaw/docs/channels/googlechat.md`, `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md` et `/Users/kevinlin/code/openclaw/docs/channels/telegram.md` documentent la gestion des médias spécifique au canal.

### Source

- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/stage-sandbox-media.ts`
- `/Users/kevinlin/code/openclaw/src/auto-reply/media-note.ts`
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/reply-delivery.ts`
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-payloads.ts`
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/reply-payloads-dedupe.ts`
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-subscribe.handlers.tools.ts`
- `/Users/kevinlin/code/openclaw/src/channels/inbound-event/media.ts`
- `/Users/kevinlin/code/openclaw/src/channels/plugins/outbound/direct-text-media.ts`
- `/Users/kevinlin/code/openclaw/src/media/store.ts`

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/stage-sandbox-media.runtime.ts`
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner.final-media-runreplyagent.test.ts`
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner.media-paths.test.ts`
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-subscribe.tools.media.test.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/chat-reply-media.test.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/chat-webchat-media.test.ts`

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/auto-reply/media-note.test.ts`
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-payloads.test.ts`
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/reply-delivery.test.ts`
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/reply-payloads-dedupe.test.ts`
- `/Users/kevinlin/code/openclaw/src/channels/inbound-event/media.test.ts`
- `/Users/kevinlin/code/openclaw/src/channels/plugins/outbound/direct-text-media.test.ts`

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search openclaw/openclaw --query "media generation completion delivery" --json
```

Résultats :

- A retourné #86034 la génération de médias réussit mais la livraison de la complétion échoue, #86279 maintenir le succès de la génération en cas d'échec de la livraison, #87741 secours du verrou de remise des médias générés, #86447 inadéquation du réveil de complétion Slack, et #87466 instabilité de la livraison vocale Telegram liée aux balises de médias générées par le modèle.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "inbound media staging sandbox MediaPaths" --json
```

Résultats :

- N'a retourné aucun résultat de mot-clé, donc la note a également utilisé les requêtes gitcrawl/discrawl de livraison de médias plus larges plus les preuves de source/test locales pour la mise en scène.

### Requêtes Discrawl

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "media generation completion delivery" --limit 5
```

Résultats :

- A retourné les rapports des clawtributors du 2026-05-23 et 2026-05-15 selon lesquels la génération a fonctionné mais la remise des pièces jointes a échoué car la session de complétion n'a pas exposé/utilisé la livraison des pièces jointes de l'outil de message.
- A retourné le rapport du responsable du 2026-05-05 avec l'échec exact `completion agent did not deliver through the message tool` ; l'injection du fournisseur et du réveil a réussi, la livraison Discord visible a échoué.

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "media store MediaPaths media://inbound" --limit 5
```

Résultats :

- A retourné un commentaire d'archive OpenClaw pour #63285 disant que les médias entrants étaient autrefois mis en scène dans le `~/.openclaw/media/inbound/` global et sont devenus inaccessibles aux agents en sandbox ; le main actuel met en scène les médias entrants gérés autorisés dans l'espace de travail du sandbox et réécrit `MediaPath`/`MediaPaths`.
