---
title: "Session, memory, and context engine - Session Routing Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Session, memory, and context engine - Session Routing Maturity Note

## Résumé

Le routage de session est un plan de contrôle mature et documenté pour décider quel compartiment de conversation reçoit chaque message. La source dispose d'une normalisation explicite des clés de session, d'une liaison de conversation de canal, d'une liaison de session sortante et de chemins de résolution de session Gateway. La couverture est la plus forte autour des RPC de session Gateway et des flux SDK, tandis que l'interception de route inter-canaux et certains scénarios de liaison de plugin restent des risques de qualité actifs.

## Portée de la catégorie

Cette catégorie couvre la construction de `sessionKey`, la résolution de cible, les liaisons de conversation, les étiquettes de session, l'isolation par conversation, la liaison de thread, la continuité de sélection de modèle liée aux sessions et le ciblage du magasin agent/workspace.

## Fonctionnalités

- Session Routing: Couvre le routage de session sur la construction de `sessionKey`, la résolution de cible, les liaisons de conversation, les étiquettes de session, l'isolation par conversation, la liaison de thread, la continuité de sélection de modèle liée aux sessions et le ciblage du magasin agent/workspace.
- Conversation routing: Couvre la liaison de conversation sur la construction de `sessionKey`, la résolution de cible, les liaisons de conversation, les étiquettes de session, l'isolation par conversation, la liaison de thread, la continuité de sélection de modèle liée aux sessions et le ciblage du magasin agent/workspace.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score: `Stable (82%)`
- Signaux positifs: la documentation définit les familles de routes et les emplacements de persistance; la source centralise la normalisation des clés de session et des liaisons; les tests Gateway et SDK couvrent `sessions.list`, `sessions.resolve`, `sessions.patch`, `sessions.compact` et les événements de flux limités à la session.
- Signaux négatifs: l'interception de route avant la sélection de session finale est toujours une demande ouverte, et les variantes de liaison de canal/plugin ont des preuves inégales en environnement réel.
- Lacunes d'intégration: ajouter un scénario qui envoie la même conversation via WebChat, un thread de canal et une route liée à un plugin, puis prouve la même clé de magasin attendue, la sélection de modèle et le comportement de dernière route.

## Score de qualité

- Score: `Beta (74%)`
- Rapports Gitcrawl: un problème adjacent à la route ouvert a été trouvé pour l'interception pré-routage.
- Rapports Discrawl: la requête Discord spécifique à la fonctionnalité n'a retourné aucune ligne correspondante.
- Bonnes qualités: le modèle de routage est explicite, soutenu par la source et documenté sur les surfaces de concepts, routage de canal et RPC Gateway.
- Mauvaises qualités: les cas d'utilisation de pont/proxy pré-routage et le comportement de liaison de plugin de canal dépendent toujours de chemins spécialisés plutôt que d'une histoire d'opérateur évidente.
- Exclu de la qualité: profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution.

## Score de complétude

- Score: `Stable (82%)`
- Instructions de surface: évaluées par rapport à `references/completeness/session-memory-and-context-engine.md`.
- Signaux positifs: les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le routage de session et le routage de conversation.
- Signaux négatifs: la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'interception pré-routage n'est pas de première classe pour les opérateurs de pont/proxy de canal.
- Le comportement de liaison est documenté lourdement pour les canaux majeurs, mais le modèle d'opérateur inter-plugin est plus difficile à valider à partir de la documentation seule.

## Preuves

### Docs

- `docs/concepts/session.md:10` dit que chaque message est routé vers une session en fonction de l'origine; `docs/concepts/session.md:90` enregistre la propriété Gateway de l'état de session.
- `docs/channels/channel-routing.md:21` définit `SessionKey`; `docs/channels/channel-routing.md:57` explique le partage de session principale de message direct; `docs/channels/channel-routing.md:79` liste la priorité de liaison.
- `docs/channels/discord.md:310` documente les clés de session DM, canal de guilde et commande slash; `docs/channels/slack.md:1020` documente le routage de thread/session Slack.

### Source

- `src/routing/session-key.ts:26` définit les clés agent et principale par défaut; `src/routing/session-key.ts:197` construit les clés de session pair; `src/routing/session-key.ts:314` résout les clés de session de thread.
- `src/channels/conversation-resolution.ts:296` résout les cibles de conversation de commande avec participation de plugin/fournisseur.
- `src/infra/outbound/session-binding-service.ts:142` enregistre les adaptateurs de liaison; `src/infra/outbound/session-binding-service.ts:354` résout les liaisons par conversation.
- `src/gateway/sessions-resolve.ts:93` résout les clés de session visibles à partir de la clé, l'étiquette ou l'id de session.

### Tests d'intégration

- `src/gateway/server.sessions.store-rpc.test.ts:35` exerce les RPC Gateway `sessions.*` et les méthodes annoncées.
- `packages/sdk/src/index.e2e.test.ts:427` couvre les assistants d'espace de noms documentés sur une WebSocket Gateway, y compris les méthodes de sessions.
- `packages/sdk/src/index.e2e.test.ts:566` inclut le streaming e2e Gateway réel avec les clés de session.

### Tests unitaires

- `src/routing/session-key.test.ts` et `src/routing/session-key.continuity.test.ts` couvrent la normalisation et la continuité des clés de session.
- `src/channels/conversation-resolution.test.ts` et `src/channels/plugins/session-conversation.test.ts` couvrent la résolution de conversation/session.
- `src/sessions/session-id-resolution.test.ts` couvre la correspondance de session-id ambiguë et structurelle.

### Requêtes Gitcrawl

Requête:

`gitcrawl search issues "sessionKey conversation binding sessions.resolve" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats:

- Retourné 1 problème ouvert: `#81061 Hook: before_route_inbound_message - pre-routing interception for channel bridging/proxying`.

### Requêtes Discrawl

Requête:

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "sessionKey conversation binding sessions.resolve"`

Résultats:

- Aucune ligne correspondante retournée.
