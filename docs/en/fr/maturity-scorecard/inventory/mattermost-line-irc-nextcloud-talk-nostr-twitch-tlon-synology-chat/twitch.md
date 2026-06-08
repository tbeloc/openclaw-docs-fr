---
title: "Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de Maturité Twitch"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de Maturité Twitch

## Résumé

Twitch est en Alpha. C'est un plugin fourni avec la documentation pour le chat IRC Twitch, les jetons OAuth, l'actualisation des jetons, la configuration multi-compte, le contrôle d'accès, les actions d'outils, la sécurité et le dépannage. Le code source inclut les hooks client, jeton, statut, sortant, contrôle d'accès et test en direct. Il reste en Alpha car la vérification en direct est optionnelle et protégée par les identifiants, et les archives montrent des préoccupations récentes concernant les boucles de redémarrage, la résolution des jetons et le cycle de vie de `client.connect()`.

## Portée de la Catégorie

- Configuration du compte bot Twitch, jetons d'accès/actualisation OAuth, ID client/secret, configuration de jointure de canal, configuration multi-compte et comportement d'installation groupée/fournie.
- Cycle de vie du moniteur/client IRC Twitch, actualisation des jetons, statut/sonde, contrôle d'accès par ID utilisateur/rôles, `requireMention` et livraison de chat sortant.
- Action d'envoi d'outil de message, surface d'action orientée modération, sécurité/opérations et dépannage.

## Fonctionnalités

- Configuration du compte bot Twitch : configuration du compte bot Twitch, jetons d'accès/actualisation OAuth, ID client/secret, configuration de jointure de canal, configuration multi-compte et comportement d'installation groupée/fournie
- Cycle de vie du moniteur/client IRC Twitch : cycle de vie du moniteur/client IRC Twitch, actualisation des jetons, statut/sonde, contrôle d'accès par ID utilisateur/rôles, requireMention et livraison de chat sortant
- Action d'envoi d'outil de message : action d'envoi d'outil de message, surface d'action orientée modération, sécurité/opérations et dépannage

## Fraîcheur des Archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Alpha (66%)`
- Signaux positifs : la documentation couvre la configuration, l'actualisation OAuth/jeton, le contrôle d'accès, la configuration multi-compte, les sondes de statut, les actions d'outils et les limites opérationnelles ; le code source dispose du cycle de vie du plugin, du gestionnaire client, du client Twitch, de la gestion des jetons, du statut/sonde, du sortant, de l'envoi, des actions et des surfaces de configuration.
- Signaux négatifs : la seule preuve Twitch en direct trouvée est un test optionnel protégé par `TWITCH_LIVE_TEST=1` et les identifiants ; aucun artefact d'exécution validé ne prouve un chemin de compte/canal Twitch réel.
- Lacunes d'intégration : la connexion IRC en direct, l'actualisation des jetons, le chat entrant, la distribution protégée par mention, l'envoi sortant, l'accès par rôle/utilisateur, la reconnexion et le routage multi-compte ne sont pas capturés dans un scénario récurrent.

## Score de Qualité

- Score : `Alpha (63%)`
- Rapports Gitcrawl : les résultats actuels incluent `#55341` jetons Twitch actualisés persistants, `#83885` `client.connect()` non attendu avec connexion échouée stockée, `#62387` suppression de promotion de compte nommé par défaut et travail de courtier plus large.
- Rapports Discrawl : le message du contributeur du 2026-05-15 décrivait un correctif de boucle de redémarrage Twitch après connexion et fournissait des instructions de vérification protégées par identifiants ; les commentaires d'examen du 2026-04-17 ont signalé la recherche de jetons normalisée dans une PR d'entrée de configuration groupée.
- Bonnes qualités : la documentation est exceptionnellement explicite sur la portée des jetons, les limitations d'actualisation, les listes blanches d'ID utilisateur, les rôles, la configuration multi-compte et la sécurité/opérations ; le code source sépare les préoccupations de jeton, client, accès, sortant, statut et configuration.
- Mauvaises qualités : le cycle de vie des jetons OAuth, le mappage des ID de compte/canal, le cycle de vie de la connexion IRC en direct et la normalisation des entrées de configuration restent fragiles ; la documentation s'appuie sur des générateurs de jetons tiers et des identifiants manuels.
- Exclu de la qualité : les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution ; celles-ci affectent uniquement la Couverture.

## Score de Complétude

- Score : `Alpha (66%)`
- Instructions de surface : évaluées par rapport à `references/completeness/mattermost-line-irc-nextcloud-talk-nostr-twitch-tlon-synology-chat.md`.
- Signaux positifs : les archives de documentation, code source, test, Gitcrawl et preuves Discrawl couvrent la portée de la taxonomie pour la configuration du compte bot Twitch, le cycle de vie du moniteur/client IRC Twitch, l'action d'envoi d'outil de message.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Aucune exécution Twitch validée en direct ne prouve la boucle complète de réception/réponse.
- L'actualisation des jetons, la persistance des jetons et la résolution normalisée des ID de compte nécessitent une preuve continue du scénario de version.
- Le contrôle d'accès utilise les ID utilisateur Twitch et les rôles, qui peuvent être hostiles aux opérateurs sans validation de configuration plus forte.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/twitch.md` lignes 9-37 décrivent le support du chat Twitch via IRC et le comportement d'installation du plugin fourni.
- `/Users/kevinlin/code/openclaw/docs/channels/twitch.md` lignes 37-90 documentent la configuration pour débutants, les portées du générateur de jetons, la configuration, le contrôle d'accès et la configuration minimale.
- `/Users/kevinlin/code/openclaw/docs/channels/twitch.md` lignes 97-179 documentent la configuration détaillée, le contrôle d'accès, l'actualisation des jetons et la journalisation d'actualisation.
- `/Users/kevinlin/code/openclaw/docs/channels/twitch.md` lignes 179-431 documentent le support multi-compte, le dépannage, la référence de configuration, les actions d'outils, la sécurité/opérations, les limites et la documentation connexe.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/twitch.md` déclare `@openclaw/twitch` et la surface du canal `twitch`.
- `/Users/kevinlin/code/openclaw/extensions/twitch/README.md` documente l'installation locale/npm, la configuration minimale, la configuration et les pointeurs de documentation complète.

### Code Source

- `/Users/kevinlin/code/openclaw/extensions/twitch/openclaw.plugin.json` déclare l'ID de plugin `twitch` et le canal `twitch`.
- `/Users/kevinlin/code/openclaw/extensions/twitch/package.json` nomme le package `@openclaw/twitch`.
- `/Users/kevinlin/code/openclaw/extensions/twitch/src/plugin.ts`, `monitor.ts`, `twitch-client.ts`, `client-manager-registry.ts` et `runtime.ts` implémentent le cycle de vie, le moniteur, le client et le comportement d'exécution.
- `/Users/kevinlin/code/openclaw/extensions/twitch/src/token.ts`, `access-control.ts`, `status.ts`, `probe.ts` et `config-schema.ts` implémentent les identifiants, l'accès, le statut, la sonde et la configuration.
- `/Users/kevinlin/code/openclaw/extensions/twitch/src/outbound.ts`, `send.ts`, `actions.ts` et `resolver.ts` implémentent le chat sortant et le comportement d'action.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/twitch/src/plugin.live.test.ts` est une vérification IRC Twitch en direct protégée par identifiants gardée par `TWITCH_LIVE_TEST=1`.
- Aucun artefact de résultat Twitch en direct validé ou scénario QA n'a été trouvé sous `/Users/kevinlin/code/openclaw/qa`.

### Tests unitaires

- Twitch a 16 tests ciblés, incluant `access-control.test.ts`, `actions.test.ts`, `client-manager-registry.test.ts`, `config-schema.test.ts`, `config.test.ts`, `outbound.test.ts`, `plugin.lifecycle.test.ts`, `plugin.test.ts`, `probe.test.ts`, `send.test.ts`, `setup-surface.test.ts`, `status.test.ts`, `token.test.ts` et `twitch-client.test.ts`.
- `/Users/kevinlin/code/openclaw/test/plugin-npm-package-manifest.test.ts`, `test/official-channel-catalog.test.ts` et `test/plugin-npm-release.test.ts` incluent la couverture du package/catalogue/version Twitch.

### Requêtes Gitcrawl

Requête : `twitch`

Résultats :

- `#55341` PR ouverte : `Persist refreshed Twitch tokens and fix OpenProse fast-loop exits`.
- `#83885` problème ouvert : `client.connect() not awaited - failed connection stored in clients map`.
- `#62387` problème ouvert : la plupart des canaux manquent `namedAccountPromotionKeys`, ce qui fait que la promotion multi-compte supprime les valeurs par défaut partagées.
- `#86113` problème ouvert : Channel Broker Phase 3.
- `#84560` PR ouverte : Support CLI pour `--dm-policy` et `--dm-allowlist` dans `channels add`.

Requête : `Twitch chat OAuth token refresh setup`

Résultats :

- La requête exacte n'a pas retourné de résultats ciblés de premier plan ; la requête simple `twitch` et les requêtes de jeton discrawl ont retourné des preuves de jeton/cycle de vie actuelles.

### Requêtes Discrawl

Requête : `twitch token`

Résultats :

- Le message du contributeur du 2026-05-15 décrivait un correctif de boucle de redémarrage Twitch après connexion et donnait une commande de vérification en direct utilisant `TWITCH_LIVE_TEST=1`, `TWITCH_USERNAME`, `TWITCH_ACCESS_TOKEN`, `TWITCH_CLIENT_ID` et `TWITCH_CHANNEL`.
- Le commentaire d'examen du miroir GitHub du 2026-04-17 sur la PR `#68008` a signalé l'alignement de la résolution des jetons avec les ID de compte normalisés.

Requête : `Twitch client connect`

Résultats :

- Aucun résultat de premier plan affiché pour cette requête exacte ; le problème gitcrawl `#83885` est la preuve d'archive plus forte pour la préoccupation du cycle de vie de `client.connect()`.
