---
title: "Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de maturité IRC Chat"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de maturité IRC Chat

## Résumé

IRC est en Alpha. Il est fourni en bundle et dispose de documentation claire pour la configuration du serveur/nick, TLS, la politique DM et groupe, la mention gating, les listes blanches d'expéditeurs de canal, NickServ, les variables d'environnement et le dépannage. Le code source et les tests couvrent les contrats locaux importants, mais il n'y a pas de preuve IRC-réseau en direct récurrente et les archives incluent toujours une confusion NickServ/login et une pression plus large de refactorisation d'ingress autour des arbres d'authentification de canal dupliqués.

## Portée de la catégorie

Inclus dans cette catégorie :

- Configuration IRC serveur/nick/TLS/NickServ : Configuration IRC serveur/nick/TLS/NickServ, chargement env/config, résolution de compte et configuration du runtime du plugin
- Réception/envoi IRC brut : Réception/envoi IRC brut, messages directs, messages de canal, normalisation de l'identité de l'expéditeur, gestion des caractères de contrôle, politique d'accès, mention gating et politique par expéditeur
- Sonde/statut : Sonde/statut, normalisation du texte sortant, cycle de vie reconnexion/surveillance et valeurs par défaut de sécurité autour de la sortie IRC directe
- Configuration du compte bot Twitch : Configuration du compte bot Twitch, jetons d'accès/actualisation OAuth, ID client/secret, configuration de jointure de canal, configuration multi-compte et comportement d'installation en bundle
- Cycle de vie du moniteur/client IRC Twitch : Cycle de vie du moniteur/client IRC Twitch, actualisation des jetons, statut/sonde, contrôle d'accès par ID utilisateur/rôles, requireMention et livraison de chat sortant
- Action d'outil d'envoi de message : Action d'outil d'envoi de message, surface d'action orientée modération, sécurité/ops et dépannage

## Fonctionnalités

- Configuration IRC serveur/nick/TLS/NickServ : Configuration IRC serveur/nick/TLS/NickServ, chargement env/config, résolution de compte et configuration du runtime du plugin
- Réception/envoi IRC brut : Réception/envoi IRC brut, messages directs, messages de canal, normalisation de l'identité de l'expéditeur, gestion des caractères de contrôle, politique d'accès, mention gating et politique par expéditeur
- Sonde/statut : Sonde/statut, normalisation du texte sortant, cycle de vie reconnexion/surveillance et valeurs par défaut de sécurité autour de la sortie IRC directe
- Configuration du compte bot Twitch : Configuration du compte bot Twitch, jetons d'accès/actualisation OAuth, ID client/secret, configuration de jointure de canal, configuration multi-compte et comportement d'installation en bundle
- Cycle de vie du moniteur/client IRC Twitch : Cycle de vie du moniteur/client IRC Twitch, actualisation des jetons, statut/sonde, contrôle d'accès par ID utilisateur/rôles, requireMention et livraison de chat sortant
- Action d'outil d'envoi de message : Action d'outil d'envoi de message, surface d'action orientée modération, sécurité/ops et dépannage

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (64%)`
- Signaux positifs : la documentation et le code source couvrent la configuration rapide, les valeurs par défaut de sécurité, le contrôle d'accès, la mention gating, les avertissements de canal public, les outils par expéditeur, NickServ, les variables env et le dépannage ; les tests d'extension couvrent les comptes, le client, le schéma de configuration, les options de connexion, le comportement entrant, le moniteur, la politique, le protocole, la sonde, l'envoi et la configuration.
- Signaux négatifs : il n'y a pas de scénario IRC réseau en direct enregistré ; de nombreuses preuves sont des mocks locaux ou une couverture de parseur/unité.
- Lacunes d'intégration : la connexion au serveur réel, les variantes TLS/SASL/NickServ, la reconnexion, la jointure de canal, le message direct, la réponse de canal avec mention gating et les garde-fous de réseau public ne sont pas prouvés dans un flux runtime récurrent.

## Score de qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl : les résultats de requête incluent `#55901` pour markdown via draft/multiline, `#56283` pour supprimer markdown pour les canaux en texte brut, `#86039/#86166` autour des avertissements de configuration de canal en bundle et un travail plus large de courtier de canal/ingress.
- Rapports Discrawl : un commentaire d'archive du 2026-03-09 sur le problème `#26059` a montré une confusion IRC login/NickServ autour du surnom déjà utilisé et du formatage du mot de passe ; les notes du responsable du 2026-05-07 décrivaient la duplication d'authentification d'ingress de canal qui mentionne explicitement les faits de mention IRC.
- Bonnes qualités : la documentation est explicite sur la sortie IRC directe, TLS, la correspondance de nick mutable, les portes canal-vs-expéditeur et les journaux de mention gating ; le code source sépare la normalisation, la politique, le protocole et les chemins d'envoi.
- Mauvaises qualités : l'identité IRC est intrinsèquement mutable, le comportement du réseau varie selon le serveur, la configuration NickServ est fragile et le transport TCP/TLS brut se situe en dehors du routage de proxy avant géré par l'opérateur.
- Exclu de la qualité : les preuves unitaires, d'intégration, e2e, en direct et de flux runtime ; celles-ci affectent uniquement la couverture.

## Score de complétude

- Score : `Alpha (64%)`
- Instructions de surface : évaluées par rapport à `references/completeness/mattermost-line-irc-nextcloud-talk-nostr-twitch-tlon-synology-chat.md`.
- Signaux positifs : les preuves archivées de documentation, code source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration IRC serveur/nick/TLS/NickServ, la réception/envoi IRC brut, la sonde/statut, la configuration du compte bot Twitch, le cycle de vie du moniteur/client IRC Twitch, l'action d'outil d'envoi de message.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Pas de preuve IRC réseau en direct récurrente pour TLS, NickServ, jointure de canal, reconnexion, DM, message de groupe et mention gating.
- La documentation de l'opérateur avertit sur la correspondance de nick mutable et le risque de canal public, mais il n'y a pas de rapport de scénario prouvant les valeurs par défaut sûres sur les réseaux publics.
- La sémantique d'ingress de canal est implémentée localement et aura probablement besoin d'un travail de parité avec le refactorisation d'ingress partagée plus large.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/irc.md` lignes 9-32 documentent le démarrage rapide, l'hôte, le port, le nick, TLS, le canal et la configuration de la politique.
- `/Users/kevinlin/code/openclaw/docs/channels/irc.md` lignes 40-63 documentent les valeurs par défaut de sécurité, la sortie directe, la politique DM/groupe, TLS, les identités stables et la correspondance de nick mutable.
- `/Users/kevinlin/code/openclaw/docs/channels/irc.md` lignes 65-187 documentent l'accès au canal, les listes blanches d'expéditeurs, la mention gating, les avertissements de canal public, les outils par expéditeur et les liens de comportement de groupe.
- `/Users/kevinlin/code/openclaw/docs/channels/irc.md` lignes 189-245 documentent NickServ, les variables d'environnement et le dépannage.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/irc.md` déclare `@openclaw/irc` et la surface de canal `irc`.

### Code source

- `/Users/kevinlin/code/openclaw/extensions/irc/openclaw.plugin.json` déclare l'ID de plugin `irc` et le canal `irc`.
- `/Users/kevinlin/code/openclaw/extensions/irc/package.json` nomme le package `@openclaw/irc`.
- `/Users/kevinlin/code/openclaw/extensions/irc/src/channel-runtime.ts`, `monitor.ts`, `client.ts`, `protocol.ts`, `inbound.ts` et `send.ts` implémentent le moniteur runtime, le protocole, la réception et le comportement d'envoi.
- `/Users/kevinlin/code/openclaw/extensions/irc/src/policy.ts`, `normalize.ts`, `control-chars.ts`, `connect-options.ts` et `accounts.ts` implémentent l'identité, la politique et la configuration de connexion.
- `/Users/kevinlin/code/openclaw/extensions/irc/src/probe.ts`, `doctor.ts`, `setup-core.ts` et `setup-surface.ts` implémentent les surfaces de statut/doctor/configuration.

### Tests d'intégration

- Aucun scénario e2e ou QA de serveur IRC en direct enregistré n'a été trouvé sous `/Users/kevinlin/code/openclaw/qa` ou `/Users/kevinlin/code/openclaw/test`.
- `/Users/kevinlin/code/openclaw/test/vitest/vitest.extension-irc.config.ts` définit une voie de test d'extension IRC délimitée, mais ce n'est pas un scénario de réseau en direct.
- `/Users/kevinlin/code/openclaw/extensions/irc/src/inbound.behavior.test.ts`, `monitor.test.ts` et `runtime-api.test.ts` couvrent le comportement adjacent au runtime avec des doublures de test locales.

### Tests unitaires

- IRC a 16 tests ciblés, incluant `accounts.test.ts`, `channel.test.ts`, `client.test.ts`, `config-schema.test.ts`, `connect-options.test.ts`, `control-chars.test.ts`, `normalize.test.ts`, `policy.test.ts`, `probe.test.ts`, `protocol.test.ts`, `send.test.ts` et `setup.test.ts`.

### Requêtes Gitcrawl

Requête : `irc`

Résultats :

- `#55901` PR ouverte : `feat(irc): support markdown messages via draft/multiline`.
- `#86039` problème ouvert : les entrées de configuration de canal en bundle émettent des avertissements lorsque les modules générés sont manquants, en ignorant la configuration désactivée.
- `#86166` PR ouverte : `fix #86039: skip disabled bundled setup fallbacks`.
- `#56283` PR ouverte : `feat(outbound): strip markdown for plain-text channels`.
- `#69926` problème ouvert référence la parité allowFrom par groupe avec IRC/LINE/Telegram/Nextcloud Talk.

Requête : `IRC channel setup nickserv tls mention allowlist`

Résultats :

- Les résultats supérieurs affichés étaient clairsemés pour cette requête exacte ; la simple requête `irc` a retourné les éléments actuels utiles liés à IRC ci-dessus.

### Requêtes Discrawl

Requête : `IRC nickserv tls`

Résultats :

- Un commentaire du miroir GitHub du 2026-03-09 sur le problème `#26059` a décrit l'échec de connexion IRC `433` surnom déjà utilisé et une solution de contournement d'opérateur utilisant `nickname:password` plus la configuration NickServ.

Requête : `IRC channel missing mention`

Résultats :

- Une note du responsable du 2026-05-07 sur le refactorisation d'ingress de canal a explicitement appelé les mentions de nick IRC appartenant au plugin et les arbres d'autorisation locaux répétés comme un domaine nécessitant une parité AccessGraph de base.
