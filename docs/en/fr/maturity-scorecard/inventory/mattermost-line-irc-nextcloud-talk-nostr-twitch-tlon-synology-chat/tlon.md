---
title: "Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de maturité Tlon"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de maturité Tlon

## Résumé

Tlon est en Alpha. C'est un plugin Tlon/Urbit fourni avec la documentation pour la configuration du navire, les navires privés/LAN, les canaux de groupe, l'approbation du propriétaire, l'acceptation automatique, les cibles de livraison, la compétence fournie, le texte enrichi, les images et le dépannage. Le code source couvre l'authentification Urbit, SSE, les opérations de canal, l'envoi/téléchargement, les paramètres de surveillance, les approbations, la découverte, les médias et le suivi des messages traités. Il reste en Alpha car il n'y a pas de scénario de navire en direct engagé, les preuves d'archive montrent la complexité du routage des fils et des réseaux privés, et les réactions/sondages ne sont explicitement pas pris en charge.

## Portée de la catégorie

- Configuration de l'URL/code du navire Tlon/Urbit, adhésion au réseau privé, configuration du canal de groupe, propriété du navire, listes blanches, acceptation automatique et comportement de configuration/docteur.
- Authentification/session de l'API Urbit, moniteur SSE, découverte DM/groupe, gestion des mentions de groupe, réponses aux fils, approbations, suivi des messages traités et assistants de paramètres.
- Conversion de texte enrichi, téléchargement d'images via le stockage Tlon/Memex, cibles de livraison, compétence Tlon fournie, sécurité et dépannage.

## Fonctionnalités

- Configuration de l'URL/code du navire Tlon/Urbit : Configuration de l'URL/code du navire Tlon/Urbit, adhésion au réseau privé, configuration du canal de groupe, propriété du navire, listes blanches, acceptation automatique et comportement de configuration/docteur
- Authentification/session de l'API Urbit : Authentification/session de l'API Urbit, moniteur SSE, découverte DM/groupe, gestion des mentions de groupe, réponses aux fils, approbations, suivi des messages traités et assistants de paramètres
- Conversion de texte enrichi : Conversion de texte enrichi, téléchargement d'images via le stockage Tlon/Memex, cibles de livraison, compétence Tlon fournie, sécurité et dépannage

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (64%)`
- Signaux positifs : la documentation et le code source couvrent la configuration, les navires privés, les groupes, les approbations du propriétaire, l'acceptation automatique, les cibles de livraison, la compétence Tlon, le texte enrichi, les images, le dépannage, le docteur, l'authentification Urbit, SSE, l'envoi et le téléchargement.
- Signaux négatifs : aucune preuve engagée de navire Urbit/Tlon en direct n'a été trouvée ; le comportement à l'exécution est prouvé principalement par des tests d'API unitaires/simulés.
- Lacunes d'intégration : la connexion, la réception SSE, l'acceptation automatique des invitations DM, l'acceptation automatique des invitations de groupe, la distribution des mentions de groupe, le routage des réponses aux fils, le téléchargement d'images et l'approbation du propriétaire ne sont pas prouvés dans un scénario récurrent de navire réel.

## Score de qualité

- Score : `Alpha (63%)`
- Rapports Gitcrawl : la recherche actuelle `tlon` était bruyante et clairsemée, renvoyant des éléments plus larges de réseau privé et de courtier de canal plutôt que de nombreux rapports Tlon ciblés ; cela ne compte pas comme un signal positif.
- Rapports Discrawl : le commentaire d'examen du 2026-04-23 avertissait que traiter uniquement Slack/Mattermost/Google Chat comme des canaux basés sur les fils pourrait casser le routage des fils sortants de Tlon sur les envois multi-charges ; la sortie de support répertorie Tlon comme un canal de messagerie Urbit décentralisé lors de la configuration.
- Bonnes qualités : la documentation est explicite sur l'adhésion au réseau privé, le comportement de propriété, les paramètres d'acceptation automatique, les exigences de mention de groupe, les réactions/sondages non pris en charge, le texte enrichi et le comportement de téléchargement d'images ; le code source sépare l'authentification Urbit et la sécurité de l'URL de téléchargement du chemin de surveillance de niveau supérieur.
- Mauvaises qualités : le déploiement Urbit/Tlon est intrinsèquement spécialisé, le support des navires privés/LAN nécessite des adhésions risquées, et la sémantique du routage des fils, de la gestion des invitations et de l'approbation du propriétaire sont complexes.
- Exclu de la qualité : preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution ; celles-ci affectent uniquement la couverture.

## Score de complétude

- Score : `Alpha (64%)`
- Instructions de surface : évaluées par rapport à `references/completeness/mattermost-line-irc-nextcloud-talk-nostr-twitch-tlon-synology-chat.md`.
- Signaux positifs : la documentation archivée, le code source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la configuration de l'URL/code du navire Tlon/Urbit, l'authentification/session de l'API Urbit, la conversion de texte enrichi.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucun scénario récurrent de navire Tlon/Urbit en direct n'est enregistré.
- Les réactions et les sondages sont documentés comme non pris en charge.
- Le support des navires de réseau privé, la découverte de groupe, le routage des fils et le téléchargement d'images nécessitent des artefacts de preuve d'opérateur avant la version bêta.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/tlon.md` lignes 8-15 décrivent le statut de support Tlon/Urbit, les DM, les mentions de groupe, les réponses aux fils, le texte enrichi, les images et les réactions/sondages non pris en charge.
- `/Users/kevinlin/code/openclaw/docs/channels/tlon.md` lignes 40-90 documentent la configuration et le comportement des navires privés/LAN.
- `/Users/kevinlin/code/openclaw/docs/channels/tlon.md` lignes 92-207 documentent les canaux de groupe, le contrôle d'accès, l'approbation du propriétaire et les paramètres d'acceptation automatique.
- `/Users/kevinlin/code/openclaw/docs/channels/tlon.md` lignes 209-290 documentent les cibles de livraison, la compétence fournie, les capacités, le dépannage, la référence de configuration et les notes.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/tlon.md` déclare `@openclaw/tlon` et la surface du canal `tlon`.
- `/Users/kevinlin/code/openclaw/extensions/tlon/README.md` résume le plugin comme prenant en charge les DM, les mentions de groupe et les réponses aux fils.

### Code source

- `/Users/kevinlin/code/openclaw/extensions/tlon/openclaw.plugin.json` déclare l'id du plugin `tlon` et le canal `tlon`.
- `/Users/kevinlin/code/openclaw/extensions/tlon/package.json` nomme le package `@openclaw/tlon`.
- `/Users/kevinlin/code/openclaw/extensions/tlon/src/urbit/auth.ts`, `base-url.ts`, `sse-client.ts`, `channel-ops.ts`, `send.ts` et `upload.ts` implémentent l'authentification Urbit, la gestion des URL, SSE, les opérations, l'envoi et le téléchargement.
- `/Users/kevinlin/code/openclaw/extensions/tlon/src/monitor/index.ts`, `authorization.ts`, `approval.ts`, `approval-runtime.ts`, `discovery.ts`, `history.ts`, `media.ts`, `processed-messages.ts` et `settings-helpers.ts` implémentent le comportement du moniteur.
- `/Users/kevinlin/code/openclaw/extensions/tlon/src/channel.ts`, `channel.runtime.ts`, `setup-core.ts`, `setup-surface.ts`, `doctor.ts`, `security.ts` et `session-route.ts` implémentent le runtime du canal, la configuration, le docteur, la sécurité et le routage.

### Tests d'intégration

- Aucun scénario engagé de navire Urbit/Tlon en direct n'a été trouvé sous `/Users/kevinlin/code/openclaw/qa` ou `/Users/kevinlin/code/openclaw/test`.
- `/Users/kevinlin/code/openclaw/extensions/tlon/src/tlon-api.test.ts`, `urbit/sse-client.test.ts`, `urbit/send.test.ts` et `urbit/upload.test.ts` utilisent un comportement HTTP/SSE/téléchargement simulé plutôt qu'un navire réel.

### Tests unitaires

- Tlon a 15 tests ciblés, incluant `channel.message-adapter.test.ts`, `core.test.ts`, `doctor.test.ts`, `monitor/approval.test.ts`, `monitor/media.test.ts`, `monitor/processed-messages.test.ts`, `monitor/settings-helpers.test.ts`, `security.test.ts`, `tlon-api.test.ts`, `urbit/auth.ssrf.test.ts`, `urbit/base-url.test.ts`, `urbit/channel-ops.test.ts`, `urbit/send.test.ts`, `urbit/sse-client.test.ts` et `urbit/upload.test.ts`.

### Requêtes Gitcrawl

Requête : `tlon`

Résultats :

- `#39604` problème ouvert : fonctionnalité de liste blanche de récupération de réseau privé, pertinente pour le support des navires privés/LAN.
- `#86113` problème ouvert : Channel Broker Phase 3, pertinent pour la migration future du framework de canal.
- Les autres résultats principaux étaient larges ou non liés au comportement spécifique de Tlon.

Requête : `Tlon Urbit ship setup group DM image upload`

Résultats :

- Aucun résultat principal ciblé n'a été renvoyé pour cette requête exacte.

### Requêtes Discrawl

Requête : `tlon urbit`

Résultats :

- Le commentaire d'examen du 2026-04-23 avertissait que le routage des fils Tlon pourrait être perdu sur les envois multi-charges lorsque le noyau sortant traitait uniquement Slack/Mattermost/Google Chat comme des canaux basés sur les fils.
- La sortie de support de configuration du 2026-04-19 répertoriait Tlon comme un canal de messagerie Urbit décentralisé dans la sélection des canaux.

Requête : `Tlon group`

Résultats :

- La note de refactorisation de l'entrée de canal du 2026-05-07 nommait les mentions de navire Tlon comme des faits appartenant au plugin dans la migration plus large de l'autorisation des canaux.
