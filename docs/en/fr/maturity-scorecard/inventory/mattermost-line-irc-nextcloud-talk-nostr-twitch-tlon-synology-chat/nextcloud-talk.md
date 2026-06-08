---
title: "Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de Maturité Nextcloud Talk"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de Maturité Nextcloud Talk

## Résumé

Nextcloud Talk est en Alpha. C'est un bot webhook fourni avec la documentation pour `occ talk:bot:install`, configuration de secret partagé, URL webhook, DMs, salons, réactions, markdown, recherche de salons, fichiers secrets et référence de configuration. Le code source et les tests couvrent l'authentification webhook, les informations de salon, l'autorisation entrante, la relecture du moniteur, l'envoi de threads, les actions de message, le docteur et la configuration. Le score reste Alpha car les preuves d'archive montrent les problèmes actuels de charge utile invalide, placeholder de mention, partage de fichier et outil de message ignoré.

## Portée de la Catégorie

- Installation du bot Nextcloud Talk, secret partagé/identifiants API, route webhook, paramètres de salon, secrets sauvegardés dans des fichiers et configuration du runtime du plugin.
- Ingestion webhook, validation de signature/secret, recherche salon-vs-DM, politique DM/groupe, appairage, gating de mention, protection contre la relecture et métadonnées de salon.
- Markdown/texte sortant, fallback média URL, réactions/actions de message, threading, statut, docteur, configuration et dépannage.

## Fonctionnalités

- Installation du bot Nextcloud Talk : installation du bot Nextcloud Talk, secret partagé/identifiants API, route webhook, paramètres de salon, secrets sauvegardés dans des fichiers et configuration du runtime du plugin
- Ingestion webhook : ingestion webhook, validation de signature/secret, recherche salon-vs-DM, politique DM/groupe, appairage, gating de mention, protection contre la relecture et métadonnées de salon
- Markdown/texte sortant : markdown/texte sortant, fallback média URL, réactions/actions de message, threading, statut, docteur, configuration et dépannage

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Alpha (68%)`
- Signaux positifs : la documentation couvre la configuration, la commande d'installation du bot, les fichiers secrets, la politique de salon, les capacités et la référence de configuration ; le code source couvre la configuration, webhook/entrée, authz, informations de salon, moniteur, garde de relecture, envoi, actions de message, docteur et routage de session.
- Signaux négatifs : aucun scénario Nextcloud server en direct récurrent n'a été trouvé ; plusieurs threads de problèmes actuels sont des défaillances d'opérateur/runtime plutôt que seulement des lacunes théoriques.
- Lacunes d'intégration : l'installation réelle du bot Nextcloud AIO/server, POST webhook, détection de mention de salon, gestion d'événement de partage de fichier, livraison d'outil de message, recherche de salon API et fallback média URL ne sont pas prouvés ensemble dans un scénario engagé.

## Score de Qualité

- Score : `Alpha (62%)`
- Rapports Gitcrawl : les résultats actuels incluent `#81566` charge utile invalide sur les événements Talk non-message, `#76980` outil `message` ignoré, `#66700` détection de mention cassée par les placeholders, `#49869` analyse d'objet riche de partage de fichier et `#79397` analyse de mention structurée.
- Rapports Discrawl : les messages de support et de miroir GitHub du 2026-04-01/07 montrent les opérateurs rencontrant `400 Bad Request` `Invalid payload format` lors de la configuration du webhook Nextcloud Talk et ayant besoin d'une guidance précise sur la fonctionnalité `occ talk:bot:install`.
- Bonnes qualités : la documentation documente la disponibilité du webhook, les fichiers secrets, les avertissements de recherche de salon et les limitations de l'API bot ; le code source sépare les identifiants API, la vérification préalable du bot, les informations de salon, la garde de relecture, la politique et le comportement d'envoi.
- Mauvaises qualités : la diversité de charge utile, l'encodage de mention, l'ambiguïté salon/DM et les détails de configuration de l'API bot sont à friction élevée ; la documentation appelle même que la charge utile webhook ne distingue pas les DMs des salons sans identifiants API.
- Exclu de la qualité : preuves unitaires, intégration, e2e, en direct et flux runtime ; celles-ci affectent uniquement la Couverture.

## Score de Complétude

- Score : `Alpha (68%)`
- Instructions de surface : évaluées par rapport à `references/completeness/mattermost-line-irc-nextcloud-talk-nostr-twitch-tlon-synology-chat.md`.
- Signaux positifs : les preuves de documentation archivée, code source, test, Gitcrawl et Discrawl couvrent la portée de taxonomie pour l'installation du bot Nextcloud Talk, l'ingestion webhook, le markdown/texte sortant.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- La preuve d'installation du bot Nextcloud server/en direct est manquante.
- L'analyseur webhook et la documentation doivent continuer à être renforcés pour les événements non-message, les partages de fichier, les mentions structurées et l'orthographe/sélection de fonctionnalité de configuration.
- Le média est basé sur URL car les téléchargements de média de l'API bot ne sont pas supportés, ce qui limite les attentes des utilisateurs par rapport aux canaux plus riches.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/nextcloud-talk.md` lignes 8-35 décrivent le statut du plugin fourni/téléchargeable.
- `/Users/kevinlin/code/openclaw/docs/channels/nextcloud-talk.md` lignes 35-97 documentent la configuration pour débutants, `occ talk:bot:install`, secret partagé, URL webhook, fichiers secrets et avertissements de recherche salon/DM.
- `/Users/kevinlin/code/openclaw/docs/channels/nextcloud-talk.md` lignes 99-170 documentent l'accès DM, la politique de salon, les capacités, la référence de configuration, le plafond média et la documentation connexe.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/nextcloud-talk.md` déclare `@openclaw/nextcloud-talk` et la surface de canal `nextcloud-talk`.

### Code Source

- `/Users/kevinlin/code/openclaw/extensions/nextcloud-talk/openclaw.plugin.json` déclare l'id de plugin `nextcloud-talk` et le canal `nextcloud-talk`.
- `/Users/kevinlin/code/openclaw/extensions/nextcloud-talk/package.json` nomme le package `@openclaw/nextcloud-talk`.
- `/Users/kevinlin/code/openclaw/extensions/nextcloud-talk/src/inbound.ts`, `monitor.ts`, `monitor-runtime.ts`, `signature.ts`, `replay-guard.ts` et `room-info.ts` implémentent l'ingestion webhook, moniteur/runtime, relecture et faits de salon.
- `/Users/kevinlin/code/openclaw/extensions/nextcloud-talk/src/send.ts`, `message-actions.ts`, `policy.ts`, `session-route.ts` et `message-adapter.ts` implémentent le comportement sortant, actions, politique, routage et adaptateur.
- `/Users/kevinlin/code/openclaw/extensions/nextcloud-talk/src/setup-core.ts`, `setup-surface.ts`, `doctor.ts`, `api-credentials.ts` et `bot-preflight.ts` implémentent la configuration, docteur, identifiants et comportement de vérification préalable du bot.

### Tests d'intégration

- Aucun scénario Nextcloud Talk server en direct engagé n'a été trouvé sous `/Users/kevinlin/code/openclaw/qa` ou `/Users/kevinlin/code/openclaw/test`.
- `/Users/kevinlin/code/openclaw/extensions/nextcloud-talk/src/channel.lifecycle.test.ts`, `monitor.replay.test.ts` et `send.cfg-threading.test.ts` couvrent les contrats de cycle de vie, relecture et livraison de type runtime avec des mocks locaux.
- `/Users/kevinlin/code/openclaw/extensions/nextcloud-talk/src/send.cfg-threading.test.ts` enregistre les résultats de preuve pour la gestion des capacités de texte, média et replyTo.

### Tests unitaires

- Nextcloud Talk a 15 tests ciblés, incluant `accounts.test.ts`, `approval-auth.test.ts`, `bot-preflight.test.ts`, `channel.core.test.ts`, `channel.status.test.ts`, `core.test.ts`, `doctor.test.ts`, `inbound.authz.test.ts`, `inbound.behavior.test.ts`, `message-actions.test.ts`, `room-info.test.ts` et `setup.test.ts`.

### Requêtes Gitcrawl

Requête : `nextcloud-talk`

Résultats :

- `#79397` PR ouverte : `fix(nextcloud-talk): parse structured mention payloads`.
- `#81566` problème ouvert : `nextcloud-talk channel returns 400 "Invalid payload format" on non-message Talk events (file shares)`.
- `#76980` problème ouvert : `Nextcloud Talk channel agent silently skips message tool, marks reply completed without posting`.
- `#66700` problème ouvert : `NC Talk plugin: mention detection broken due to {mention-user1} placeholders`.
- `#49869` PR ouverte : `fix(nextcloud-talk): parse rich object file shares from webhook payload`.

Requête : `Nextcloud Talk webhook room reaction bot setup`

Résultats :

- `#76980` a été retourné à nouveau comme le résultat principal ciblé pour cette requête.

### Requêtes Discrawl

Requête : `Nextcloud Talk invalid payload`

Résultats :

- Les commentaires du miroir GitHub du 2026-04-07 sur le problème `#34111` montrent `400 Bad Request` / `Invalid payload format` lors de la configuration du webhook et la confusion de configuration de fonctionnalité de mention.
- Le thread de support du 2026-04-01 a signalé une configuration Nextcloud AIO/Raspberry Pi bloquée sur la même erreur webhook de charge utile invalide.

Requête : `nextcloud talk`

Résultats :

- La discussion utilisateur du 2026-05-21 a référencé des salons multi-agents construits dans Nextcloud Talk et Matrix mais pas encore généralisés dans une fonctionnalité maintenue.
