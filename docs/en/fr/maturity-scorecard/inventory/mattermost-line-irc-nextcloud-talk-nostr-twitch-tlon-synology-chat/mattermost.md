---
title: "Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de Maturité du Chat d'Espace de Travail"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de Maturité du Chat d'Espace de Travail

## Résumé

Mattermost est l'un des canaux les plus solides de cette surface de longue traîne. Il dispose de documentation de première classe, d'un plugin téléchargeable, de réception WebSocket, de configuration de jeton de bot, de commandes slash, de threads, de streaming d'aperçu de brouillon, de réactions, de boutons interactifs, de recherche d'annuaire, de configuration multi-compte et d'une suite de tests d'extension importante. Il reste en Beta plutôt que Stable car les preuves d'archive actuelles incluent toujours thread-root, no-visible-reply, slash callback auth et interaction-token hardening churn.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Configuration du compte bot Mattermost : configuration du compte bot Mattermost, configuration du jeton bot/URL de base, configuration multi-compte et empaquetage de plugin
- Surveillance inbound WebSocket : surveillance inbound WebSocket, routage DM/canal, contrôle d'accès, appairage, mention gating et session threading
- Livraison sortante : livraison sortante, streaming d'aperçu de brouillon, réactions, boutons interactifs, commandes slash, recherche d'annuaire, diagnostics et comportement doctor

## Fonctionnalités

- Configuration du compte bot Mattermost : configuration du compte bot Mattermost, configuration du jeton bot/URL de base, configuration multi-compte et empaquetage de plugin
- Surveillance inbound WebSocket : surveillance inbound WebSocket, routage DM/canal, contrôle d'accès, appairage, mention gating et session threading
- Livraison sortante : livraison sortante, streaming d'aperçu de brouillon, réactions, boutons interactifs, commandes slash, recherche d'annuaire, diagnostics et comportement doctor

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (78%)`
- Signaux positifs : la documentation couvre l'installation, la configuration, les callbacks slash, les DM, les groupes, le threading, les cibles sortantes, le streaming, les réactions, les boutons, la recherche d'annuaire, le multi-compte et la résolution des problèmes ; la source dispose d'un plugin large avec les modules monitor, send, slash, interaction, reconnect, doctor, setup, auth et directory.
- Signaux négatifs : la preuve du serveur en direct est ad hoc plutôt que récurrente ; les preuves d'archive incluent des régressions de thread/contexte visibles par l'utilisateur et des diagnostics no-visible-reply.
- Lacunes d'intégration : aucun scénario de serveur Mattermost en direct engagé ou route e2e prouvant setup-to-message-to-reply sur les commandes slash, les réponses de thread, les boutons et le streaming en une seule exécution.

## Score de Qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl : les résultats de requête incluent des PR ouvertes pour le sélecteur de dialogue `/model`, le hardening du token d'interaction, le hardening de l'auth de callback slash, l'hydratation du démarreur de thread, les réactions d'ack automatiques et la résolution de réponse thread-root.
- Rapports Discrawl : un message de mainteneur du 2026-05-27 a signalé un test de fumée rapide avec un dev claw et le canal Mattermost semblait OK ; un rapport de support utilisateur du 2026-05-20 a signalé une perte de contexte de thread dans les anciens threads Mattermost ; les entrées d'archive du 2026-03-25/28 ont décrit les défaillances `RootId` invalides et les abandons silencieux.
- Bonnes qualités : alignement fort docs/source, validation explicite de callback slash fail-closed, vérification de bouton HMAC, retry de canal direct, fallback de finalisation de streaming et diagnostics ciblés pour les réponses no-visible.
- Mauvaises qualités : la sémantique des threads, l'état du callback slash, l'auth d'interaction et la réachabilité du callback auto-hébergé restent opérationnellement fragiles et continuent de générer du trafic de correction de bugs.
- Exclu de la qualité : preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution ; celles-ci affectent uniquement la Couverture.

## Score de Complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/mattermost-line-irc-nextcloud-talk-nostr-twitch-tlon-synology-chat.md`.
- Signaux positifs : les preuves de documentation archivée, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration du compte bot Mattermost, la surveillance inbound WebSocket et la livraison sortante.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- La preuve de scénario Mattermost en direct récurrente manque pour la configuration initiale, la réception WebSocket, la réponse de thread, la commande slash, le callback de bouton, la réaction et la finalisation de draft-stream.
- Les URL de callback auto-hébergées et la configuration du serveur Mattermost (`AllowedUntrustedInternalConnections`, intégration d'action de post, tokens de commande slash) restent des pièges fréquents pour les opérateurs.
- La recherche d'annuaire multi-équipe et le contexte des anciens threads restent des zones de risque visibles.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/mattermost.md` lignes 10-31 décrivent le statut, l'installation et la configuration rapide.
- `/Users/kevinlin/code/openclaw/docs/channels/mattermost.md` lignes 62-101 documentent les commandes slash natives, le comportement de l'URL de callback et la validation du token de commande.
- `/Users/kevinlin/code/openclaw/docs/channels/mattermost.md` lignes 185-220 documentent le contrôle d'accès DM, la politique de groupe et les cibles sortantes.
- `/Users/kevinlin/code/openclaw/docs/channels/mattermost.md` lignes 266-480 documentent le streaming d'aperçu de brouillon, les réactions, les boutons interactifs, la vérification de bouton HMAC et le comportement de l'adaptateur d'annuaire.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/mattermost.md` déclare `@openclaw/mattermost` et la surface de canal `mattermost`.

### Source

- `/Users/kevinlin/code/openclaw/extensions/mattermost/openclaw.plugin.json` déclare l'id de plugin `mattermost` et le canal `mattermost`.
- `/Users/kevinlin/code/openclaw/extensions/mattermost/package.json` nomme le package `@openclaw/mattermost`.
- `/Users/kevinlin/code/openclaw/extensions/mattermost/src/mattermost/monitor.ts`, `monitor-auth.ts`, `monitor-websocket.ts` et `monitor-slash.ts` implémentent les chemins de surveillance WebSocket inbound et slash.
- `/Users/kevinlin/code/openclaw/extensions/mattermost/src/mattermost/send.ts`, `reply-delivery.ts`, `draft-stream.ts`, `reactions.ts`, `interactions.ts` et `target-resolution.ts` implémentent la livraison sortante, le streaming, les réactions, les boutons et la résolution de cible.
- `/Users/kevinlin/code/openclaw/extensions/mattermost/src/setup-core.ts`, `setup-surface.ts`, `doctor.ts` et `config-schema-core.ts` implémentent le comportement de configuration, statut, doctor et config.

### Tests d'intégration

- Aucun scénario e2e ou QA de serveur Mattermost en direct engagé n'a été trouvé sous `/Users/kevinlin/code/openclaw/qa` ou `/Users/kevinlin/code/openclaw/test`.
- `/Users/kevinlin/code/openclaw/extensions/mattermost/src/channel.message-adapter.test.ts` valide les preuves de capacité de l'adaptateur pour le comportement de draft preview/finalizer.
- `/Users/kevinlin/code/openclaw/extensions/mattermost/src/mattermost/monitor-websocket.test.ts`, `slash-http.test.ts` et `reply-delivery.test.ts` exercent les limites d'exécution avec les clients Mattermost et les requêtes HTTP simulés.

### Tests unitaires

- Mattermost dispose de 39 tests de composants dans l'arborescence d'extension, incluant `approval-auth.test.ts`, `config-schema.test.ts`, `doctor.test.ts`, `setup.test.ts`, `monitor-auth.test.ts`, `monitor-gating.test.ts`, `reconnect.test.ts`, `slash-commands.test.ts`, `slash-state.test.ts`, `interactions.test.ts`, `directory.test.ts` et `no-visible-reply-diagnostic.test.ts`.
- `/Users/kevinlin/code/openclaw/src/commands/status-all/channels.mattermost-token-summary.test.ts` couvre le comportement du résumé de token de statut.

### Requêtes Gitcrawl

Requête : `mattermost`

Résultats :

- `#83573` PR ouverte : `feat(mattermost): add /model dialog picker`.
- `#64546` PR ouverte : `fix: Mattermost interaction token forgeable via hardcoded HMAC...`.
- `#65655` PR ouverte : `fix: harden Mattermost slash callback auth`.
- `#73061` PR ouverte : `fix(mattermost): hydrate thread starter context`.
- `#80426` PR ouverte : `feat(mattermost): add automatic ack reactions`.
- `#76634` PR ouverte : `fix(mattermost): resolve reply root before sending thread replies`.

Requête : `Mattermost bug auth token thread reply no visible`

Résultats :

- La recherche a retourné un trafic de maintenance inter-canaux plus large, incluant `#74163` ; le signal d'archive actuel plus utile spécifique à Mattermost provenait de la requête simple `mattermost` ci-dessus.

### Requêtes Discrawl

Requête : `mattermost`

Résultats :

- Le message du canal mainteneur du 2026-05-27 a signalé un test de fumée rapide avec un dev claw et le canal Mattermost semblait OK.
- Le message de support Mattermost du 2026-05-20 a signalé une perte de contexte de thread ancien et de post initial.

Requête : `Mattermost no visible reply thread`

Résultats :

- Le message du miroir GitHub du 2026-03-28 pour la PR `#56305` a décrit un `RootId` Mattermost obsolète causant un comportement de non-réponse silencieux.
- La discussion de support Mattermost du 2026-03-25 a décrit les défaillances de thread multi-tour causées par un comportement `RootId` invalide.
