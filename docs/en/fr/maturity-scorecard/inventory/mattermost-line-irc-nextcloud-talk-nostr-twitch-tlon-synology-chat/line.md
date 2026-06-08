---
title: "Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de maturité de la messagerie par webhook"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de maturité de la messagerie par webhook

## Résumé

LINE est un canal Beta dans cette surface. La documentation et le code source couvrent la configuration de l'API Messaging, la vérification de la signature webhook, les fichiers de token/secret, la politique DM et groupe, les messages enrichis, les cartes Flex, les emplacements, les médias, les liaisons ACP et les médias sortants. Cela reste en dessous de Stable car les preuves d'archive actuelles montrent toujours des cas limites de route multi-compte, route webhook, taille des médias et limites de débit.

## Portée de la catégorie

Inclus dans cette catégorie :

- Configuration du webhook de l'API LINE Messaging : configuration du webhook de l'API LINE Messaging, gestion du token d'accès au canal/secret du canal, routage multi-compte et installation du plugin
- Événements webhook entrants signés : événements webhook entrants signés, accusé de réception immédiat, autorisation DM/groupe, appairage, clés de groupe, contexte du message, déduplication de renvoi et livraison de réponse durable
- Charges utiles LINE enrichies : charges utiles LINE enrichies, réponses rapides, emplacements, cartes Flex/template, médias image/audio/vidéo sortants, menus enrichis, statut et dépannage
- Installation du bot Nextcloud Talk : installation du bot Nextcloud Talk, secret partagé/identifiants API, route webhook, paramètres de salle, secrets sauvegardés sur fichier et configuration du runtime du plugin
- Ingestion webhook : ingestion webhook, validation de signature/secret, recherche salle-vs-DM, politique DM/groupe, appairage, mention gating, protection contre la relecture et métadonnées de salle
- Markdown/texte sortant : markdown/texte sortant, secours média URL, réactions/actions de message, threading, statut, doctor, configuration et dépannage
- Configuration du webhook entrant/sortant Synology Chat : configuration du webhook entrant/sortant Synology Chat, config token/URL entrant, variables env, surface de configuration et config de route multi-compte
- Vérification du token webhook : vérification du token webhook, politique DM, IDs utilisateur autorisés, appairage, limitation de débit, verrouillage de token invalide, clés de session, contexte entrant de message direct et sémantique ACK webhook
- Texte sortant : texte sortant et livraison de médias URL, gardes SSRF de réseau privé, audit de sécurité, configuration/statut et dépannage

## Fonctionnalités

- Configuration du webhook de l'API LINE Messaging : configuration du webhook de l'API LINE Messaging, gestion du token d'accès au canal/secret du canal, routage multi-compte et installation du plugin
- Événements webhook entrants signés : événements webhook entrants signés, accusé de réception immédiat, autorisation DM/groupe, appairage, clés de groupe, contexte du message, déduplication de renvoi et livraison de réponse durable
- Charges utiles LINE enrichies : charges utiles LINE enrichies, réponses rapides, emplacements, cartes Flex/template, médias image/audio/vidéo sortants, menus enrichis, statut et dépannage
- Installation du bot Nextcloud Talk : installation du bot Nextcloud Talk, secret partagé/identifiants API, route webhook, paramètres de salle, secrets sauvegardés sur fichier et configuration du runtime du plugin
- Ingestion webhook : ingestion webhook, validation de signature/secret, recherche salle-vs-DM, politique DM/groupe, appairage, mention gating, protection contre la relecture et métadonnées de salle
- Markdown/texte sortant : markdown/texte sortant, secours média URL, réactions/actions de message, threading, statut, doctor, configuration et dépannage
- Configuration du webhook entrant/sortant Synology Chat : configuration du webhook entrant/sortant Synology Chat, config token/URL entrant, variables env, surface de configuration et config de route multi-compte
- Vérification du token webhook : vérification du token webhook, politique DM, IDs utilisateur autorisés, appairage, limitation de débit, verrouillage de token invalide, clés de session, contexte entrant de message direct et sémantique ACK webhook
- Texte sortant : texte sortant et livraison de médias URL, gardes SSRF de réseau privé, audit de sécurité, configuration/statut et dépannage

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (75%)`
- Signaux positifs : la documentation et le code source couvrent l'installation/configuration, la vérification de la signature webhook, le comportement ack, le contrôle d'accès, les téléchargements de médias, les charges utiles enrichies, les médias sortants, les liaisons ACP, le statut, la configuration et la gestion des comptes.
- Signaux négatifs : aucune exécution e2e LINE Messaging API en direct engagée n'a été trouvée ; les problèmes récents couvrent toujours l'enregistrement de la route webhook, les valeurs par défaut multi-compte, les précontrôles de médias et le comportement du timeout d'inactivité des chunks.
- Lacunes d'intégration : la vérification du webhook en direct, le POST signé, l'admission DM/groupe, le téléchargement de médias, la livraison de cartes enrichies et la preuve de médias sortants ne sont pas capturés comme un scénario récurrent.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : les résultats de requête incluent les PRs/problèmes ouverts pour le chargement `accounts.default` et l'activation par défaut des comptes nommés, les 404 de route webhook multi-compte, les cibles de secret d'identifiants, le précontrôle de médias sortants et le timeout d'inactivité des chunks de médias entrants.
- Rapports Discrawl : les messages d'archive incluent un examen de cas/registre de route webhook LINE du 2026-04-25 et un problème fermé pour la route webhook non enregistrée dans le gestionnaire HTTP de la passerelle.
- Bonnes qualités : la gestion de la signature du corps brut est explicite, le comportement ACK webhook est documenté, la gestion des fichiers token/secret rejette les liens symboliques, les protections SSRF des URL de médias sont documentées et la déduplication de renvoi apparaît dans le code source.
- Mauvaises qualités : l'enregistrement de la route multi-compte, la casse du chemin webhook, la gestion du corps brut signé, la taille des médias et la sémantique de retry/limite de débit en amont sont subtils et ont généré des travaux de réparation répétés.
- Exclus de la qualité : preuves unitaires, d'intégration, e2e, en direct et de flux runtime ; celles-ci affectent uniquement la couverture.

## Score de complétude

- Score : `Beta (75%)`
- Instructions de surface : évaluées par rapport à `references/completeness/mattermost-line-irc-nextcloud-talk-nostr-twitch-tlon-synology-chat.md`.
- Signaux positifs : les preuves archivées de documentation, code source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration du webhook de l'API LINE Messaging, les événements webhook entrants signés, les charges utiles LINE enrichies, l'installation du bot Nextcloud Talk, l'ingestion webhook, le markdown/texte sortant, la configuration du webhook entrant/sortant Synology Chat, la vérification du token webhook et le texte sortant.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Une exécution webhook réelle de la console développeur LINE n'est pas engagée pour la configuration, les événements entrants signés, les médias, les messages enrichis et les médias sortants.
- Le comportement de la route multi-compte a besoin de preuves continues car l'enregistrement de la route et la sémantique du compte par défaut ont eu des bugs récents.
- La documentation est large, mais les modes de défaillance opérationnels autour des limites de retry/débit LINE et des URL de médias ont besoin d'une capture de scénario plus forte.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/line.md` lignes 10-18 décrivent le récepteur webhook de l'API LINE Messaging et les messages directs, groupes, médias, emplacements, messages Flex et templates supportés.
- `/Users/kevinlin/code/openclaw/docs/channels/line.md` lignes 32-54 documentent la configuration, l'URL webhook, la validation de signature, les limites de corps et la gestion des octets de requête bruts.
- `/Users/kevinlin/code/openclaw/docs/channels/line.md` lignes 56-145 documentent la configuration token/secret, les identifiants sauvegardés sur fichier, les chemins multi-compte, le contrôle d'accès DM/groupe et les valeurs par défaut de la politique de groupe.
- `/Users/kevinlin/code/openclaw/docs/channels/line.md` lignes 153-226 documentent le comportement du message, les limites de téléchargement de médias, les messages enrichis, le support ACP, les médias sortants et les restrictions SSRF des URL de médias.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/line.md` déclare `@openclaw/line` et la surface de canal `line`.

### Code source

- `/Users/kevinlin/code/openclaw/extensions/line/openclaw.plugin.json` déclare l'id du plugin `line` et le canal `line`.
- `/Users/kevinlin/code/openclaw/extensions/line/package.json` nomme le package `@openclaw/line`.
- `/Users/kevinlin/code/openclaw/extensions/line/src/webhook.ts`, `webhook-node.ts`, `signature.ts`, `bot-handlers.ts` et `monitor.ts` implémentent l'ingestion webhook, les vérifications de signature, la gestion des événements bot et le cycle de vie du moniteur.
- `/Users/kevinlin/code/openclaw/extensions/line/src/group-policy.ts`, `group-keys.ts`, `bot-access.ts`, `accounts.ts` et `config-schema.ts` implémentent l'autorisation et la configuration.
- `/Users/kevinlin/code/openclaw/extensions/line/src/outbound.ts`, `outbound-media.ts`, `reply-payload-transform.ts`, `flex-templates/*`, `rich-menu.ts` et `send.ts` implémentent la livraison enrichie/sortante.

### Tests d'intégration

- Aucun scénario LINE Messaging API en direct engagé n'a été trouvé sous `/Users/kevinlin/code/openclaw/qa` ou `/Users/kevinlin/code/openclaw/test`.
- `/Users/kevinlin/code/openclaw/extensions/line/src/monitor.lifecycle.test.ts` exerce l'enregistrement de la route webhook et le comportement du cycle de vie avec des dépendances runtime simulées.
- `/Users/kevinlin/code/openclaw/extensions/line/src/webhook-node.test.ts` couvre le contrat POST partagé, le rappel de libération de requête authentifiée, la gestion de la charge utile brute et le comportement de la charge utile du middleware.
- `/Users/kevinlin/code/openclaw/extensions/line/src/channel.sendPayload.test.ts` enregistre les résultats de preuve de capacité de l'adaptateur pour le texte, les médias, les hooks d'envoi de message et les politiques ACK de réception.

### Tests unitaires

- LINE a 24 tests d'extension ciblés, incluant `accounts.test.ts`, `auto-reply-delivery.test.ts`, `bot-handlers.test.ts`, `bot-message-context.test.ts`, `config-schema.test.ts`, `download.test.ts`, `group-keys.test.ts`, `markdown-to-line.test.ts`, `message-cards.test.ts`, `outbound-media.test.ts`, `reply-chunks.test.ts`, `reply-payload-transform.test.ts`, `rich-menu.test.ts`, `send.test.ts`, `setup-surface.test.ts` et `signature.test.ts`.
- `/Users/kevinlin/code/openclaw/test/vitest/vitest.extension-line.config.ts` définit une voie d'extension LINE à portée dédiée.

### Requêtes Gitcrawl

Requête : `line`

Résultats :

- `#81471` PR ouverte : `fix(line): load accounts.default and default-enable named accounts`.
- `#47264` problème ouvert : `LINE plugin: multi-account mode breaks webhook route registration (404)`.
- `#85003` PR ouverte : `fix(line): register credential secret targets`.
- `#84229` PR ouverte : `fix(line): precheck outbound LINE media size`.
- `#86873` PR ouverte : `fix(line): add chunk-idle timeout to inbound media download`.

Requête : `LINE webhook setup routing media flex`

Résultats :

- `#65656` problème ouvert : `LINE reply - table flex messages silently dropped with 429 when text + table are returned together`.

### Requêtes Discrawl

Requête : `LINE webhook route`

Résultats :

- Message miroir GitHub du 2026-04-25 PR fermée `#48120` sur la casse du chemin de la route webhook LINE sur Windows comme non reproductible sur le main actuel.
- L'archive du 2026-04-25 incluait également la fermeture du problème `#49803` pour la route webhook du plugin LINE non enregistrée dans le gestionnaire HTTP de la passerelle.

Requête : `LINE group media`

Résultats :

- Aucune transcription opérationnelle LINE groupe/médias ciblée n'a été retournée dans les résultats supérieurs affichés ; les preuves actuelles pertinentes se trouvent dans les problèmes/PRs gitcrawl et le code source.
