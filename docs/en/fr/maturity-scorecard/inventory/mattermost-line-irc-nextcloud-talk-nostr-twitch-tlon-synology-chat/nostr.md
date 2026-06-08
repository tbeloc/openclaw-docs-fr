---
title: "Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de Maturité de la Messagerie Décentralisée"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de Maturité de la Messagerie Décentralisée

## Résumé

Nostr est en Alpha. C'est un plugin optionnel documenté et fourni en bundle pour les messages directs chiffrés NIP-04, les relais, les métadonnées de profil, les formats de clés et les conseils de sécurité. Le code source et les tests couvrent le comportement du bus Nostr, les chemins chiffrés entrants/sortants, les profils, l'état des relais et la configuration. Il reste en dessous de Beta car le comportement des relais en direct et la durée de vie des abonnements ont un historique de bugs récents, et la documentation marque explicitement le support des médias et NIP-17/NIP-44 comme non encore implémentés.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Configuration des clés Nostr : configuration des clés Nostr, configuration des relais, métadonnées de profil, gestion des clés privées, installation du plugin et statut de configuration
- Réception/envoi de DM chiffrés NIP-04 : réception/envoi de DM chiffrés NIP-04, vérification de la signature d'événement, politique d'expéditeur, bus de relais, suivi des doublons/vus, test de relais local et stockage d'état
- Importation/publication de profil : importation/publication de profil, sécurité des URL de relais, métriques, routage de session et limitations autour des médias et des protocoles DM chiffrés plus récents
- Configuration de l'URL/code du navire Tlon/Urbit : configuration de l'URL/code du navire Tlon/Urbit, opt-in du réseau privé, configuration du canal de groupe, propriété du navire, listes blanches, acceptation automatique et comportement de configuration/docteur
- Authentification/session de l'API Urbit : authentification/session de l'API Urbit, moniteur SSE, découverte DM/groupe, gestion des mentions de groupe, réponses aux threads, approbations, suivi des messages traités et assistants de paramètres
- Conversion de texte enrichi : conversion de texte enrichi, téléchargement d'images via le stockage Tlon/Memex, cibles de livraison, compétence Tlon fournie en bundle, sécurité et dépannage

## Fonctionnalités

- Configuration des clés Nostr : configuration des clés Nostr, configuration des relais, métadonnées de profil, gestion des clés privées, installation du plugin et statut de configuration
- Réception/envoi de DM chiffrés NIP-04 : réception/envoi de DM chiffrés NIP-04, vérification de la signature d'événement, politique d'expéditeur, bus de relais, suivi des doublons/vus, test de relais local et stockage d'état
- Importation/publication de profil : importation/publication de profil, sécurité des URL de relais, métriques, routage de session et limitations autour des médias et des protocoles DM chiffrés plus récents
- Configuration de l'URL/code du navire Tlon/Urbit : configuration de l'URL/code du navire Tlon/Urbit, opt-in du réseau privé, configuration du canal de groupe, propriété du navire, listes blanches, acceptation automatique et comportement de configuration/docteur
- Authentification/session de l'API Urbit : authentification/session de l'API Urbit, moniteur SSE, découverte DM/groupe, gestion des mentions de groupe, réponses aux threads, approbations, suivi des messages traités et assistants de paramètres
- Conversion de texte enrichi : conversion de texte enrichi, téléchargement d'images via le stockage Tlon/Memex, cibles de livraison, compétence Tlon fournie en bundle, sécurité et dépannage

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Alpha (62%)`
- Signaux positifs : la documentation couvre les clés, les relais, la politique DM, les listes blanches, les métadonnées de profil, le support du protocole, les tests de relais local, le dépannage et la sécurité ; les tests incluent une couverture de style intégration du bus Nostr et des tests de fuzzing.
- Signaux négatifs : aucune exécution engagée de relais public en direct ou de relais local n'a été trouvée ; les problèmes de durée de vie des abonnements et de boucles de redémarrage sont des préoccupations actuelles de l'archive.
- Lacunes d'intégration : configuration-vers-abonnement de relais, DM entrant chiffré, réponse sortante chiffré, reconnexion de relais, suppression des doublons et importation/publication de profil ne sont pas prouvés comme un scénario en direct récurrent.

## Score de Qualité

- Score : `Alpha (58%)`
- Rapports Gitcrawl : les résultats actuels incluent `#53858` boucle de redémarrage, `#87457` maintien des abonnements DM en vie jusqu'à l'abandon, `#72216` correction de la portée du statut de configuration, `#63673` pas de messages entrants après la mise à jour et un travail plus large du courtier de canal.
- Rapports Discrawl : le message du contributeur du 2026-05-28 a lié la PR `#87457` pour le cycle de vie des abonnements DM Nostr sur les relais stricts ; le problème `#55409` du 2026-03-26 a décrit les fermetures immédiates des abonnements WebSocket et les boucles de redémarrage ; l'examen de l'archive a également référencé la validation des URL de relais et le nettoyage de l'état des clés privées.
- Bonnes qualités : la documentation avertit clairement sur les clés privées, les NIPs supportés, la redondance des relais, les réponses dupliquées et le flux de politique d'expéditeur avant déchiffrement ; le code source a des modules séparés pour les clés, les profils, le bus de relais, le suivi des vus et le magasin d'état.
- Mauvaises qualités : le comportement des relais Nostr est décentralisé et à variance élevée, la gestion stricte des abonnements aux relais a des corrections actives, la validation des URL de relais a un historique de PR obsolète et NIP-17/NIP-44/médias ne font pas partie du contrat actuel.
- Exclu de la qualité : preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution ; celles-ci affectent uniquement la Couverture.

## Score de Complétude

- Score : `Alpha (62%)`
- Instructions de surface : évaluées par rapport à `references/completeness/mattermost-line-irc-nextcloud-talk-nostr-twitch-tlon-synology-chat.md`.
- Signaux positifs : les preuves archivées de documentation, code source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration des clés Nostr, la réception/envoi de DM chiffrés NIP-04, l'importation/publication de profil, la configuration de l'URL/code du navire Tlon/Urbit, l'authentification/session de l'API Urbit, la conversion de texte enrichi.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Aucun scénario en direct soutenu par relais récurrent n'est enregistré.
- Les DM enveloppés en cadeau NIP-17, le chiffrement versionnée NIP-44 et les pièces jointes multimédias sont documentés comme non encore supportés.
- La validation des URL de relais, la durée de vie des abonnements aux relais stricts et le comportement de redémarrage nécessitent un renforcement opérationnel plus solide.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/nostr.md` lignes 9-48 décrivent le statut du plugin optionnel fourni en bundle, l'installation et la configuration non-interactive.
- `/Users/kevinlin/code/openclaw/docs/channels/nostr.md` lignes 48-87 documentent la configuration rapide, la clé privée, les relais, la politique DM, allowFrom et la configuration du profil.
- `/Users/kevinlin/code/openclaw/docs/channels/nostr.md` lignes 89-187 documentent les métadonnées de profil, le contrôle d'accès, les formats de clés, les conseils de relais et le support du protocole.
- `/Users/kevinlin/code/openclaw/docs/channels/nostr.md` lignes 187-245 documentent les tests de relais local, les tests manuels, le dépannage, la sécurité et les limitations.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/nostr.md` déclare `@openclaw/nostr` et la surface du canal `nostr`.
- `/Users/kevinlin/code/openclaw/extensions/nostr/README.md` répète la portée DM NIP-04, les tests de relais local, le tableau des protocoles et les notes de sécurité.

### Code Source

- `/Users/kevinlin/code/openclaw/extensions/nostr/openclaw.plugin.json` déclare l'id du plugin `nostr` et le canal `nostr`.
- `/Users/kevinlin/code/openclaw/extensions/nostr/package.json` nomme le package `@openclaw/nostr`.
- `/Users/kevinlin/code/openclaw/extensions/nostr/src/nostr-bus.ts`, `inbound-direct-dm-runtime.ts`, `seen-tracker.ts` et `nostr-state-store.ts` implémentent le bus de relais, l'exécution DM entrant, le suivi des doublons et l'état.
- `/Users/kevinlin/code/openclaw/extensions/nostr/src/nostr-key-utils.ts`, `nostr-profile.ts`, `nostr-profile-http.ts`, `nostr-profile-import.ts` et `nostr-profile-url-safety.ts` implémentent la gestion des clés/profils et la sécurité des URL de profil.
- `/Users/kevinlin/code/openclaw/extensions/nostr/src/channel.ts`, `channel.setup.ts`, `setup-adapter.ts`, `setup-surface.ts` et `session-route.ts` implémentent l'exécution du canal, la configuration et le routage.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/nostr/src/nostr-bus.integration.test.ts` fournit une couverture de style intégration local du comportement du bus, mais aucune exécution engagée de relais public en direct n'a été trouvée.
- Aucun scénario QA Nostr n'a été trouvé sous `/Users/kevinlin/code/openclaw/qa`.

### Tests unitaires

- Nostr a 13 tests ciblés, incluant `channel.inbound.test.ts`, `channel.lifecycle.test.ts`, `channel.outbound.test.ts`, `channel.test.ts`, `nostr-bus.fuzz.test.ts`, `nostr-bus.inbound.test.ts`, `nostr-bus.test.ts`, `nostr-profile-http.test.ts`, `nostr-profile-import.test.ts`, `nostr-profile.fuzz.test.ts`, `nostr-profile.test.ts` et `nostr-state-store.test.ts`.

### Requêtes Gitcrawl

Requête : `nostr`

Résultats :

- `#72216` PR ouverte : `fix(nostr): keep setup status off full surface`.
- `#53858` problème ouvert : `Nostr channel restart loop - provider starts and immediately stops without error`.
- `#87457` PR ouverte : `fix(nostr): keep DM subscriptions alive until abort`.
- `#63673` problème ouvert : `Keychat Bridge receives no inbound messages after OpenClaw update to 2026.4.8`.

Requête : `Nostr bug relay NIP-04 duplicate private key`

Résultats :

- La requête exacte n'a pas retourné de résultats ciblés au top, mais la requête simple `nostr` et les requêtes de relais/redémarrage discrawl ont retourné les preuves pertinentes d'abonnement Nostr et d'historique de clés.

### Requêtes Discrawl

Requête : `nostr relay`

Résultats :

- Le message du contributeur du 2026-05-28 a lié la PR `#87457` pour le cycle de vie des abonnements DM Nostr, le démarrage/redémarrage des relais stricts et le nettoyage à l'arrêt.
- L'examen de l'archive du 2026-04-26 a gardé la PR de validation des URL de relais `#39748` ouverte car le main actuel permettait toujours une configuration large des relais et une utilisation directe à l'exécution.
- L'examen de l'archive du 2026-04-24 a fermé le problème de clé privée dans l'état `#12545` comme implémenté après le nettoyage du magasin d'état.

Requête : `Nostr restart loop`

Résultats :

- Le problème `#55409` du 2026-03-26 a signalé les fermetures immédiates des abonnements WebSocket avec des délais d'expiration/erreurs de connexion et une boucle de redémarrage infinie.
- Le commentaire du 2026-03-25 sur le problème `#53858` a signalé une cause racine dans la gestion des abonnements `nostr-tools` fournie en bundle.
