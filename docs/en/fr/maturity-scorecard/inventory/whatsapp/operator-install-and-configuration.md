---
title: "WhatsApp - Note de maturité de la configuration du canal et des opérations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# WhatsApp - Note de maturité de la configuration du canal et des opérations

## Résumé

L'installation et la configuration de l'opérateur WhatsApp sont en version bêta. Le package de plugin externe officiel dispose d'une documentation claire, de métadonnées de manifeste, d'un schéma de configuration, d'un câblage de configuration, d'une guidance d'installation ClawHub/npm, et de mises en garde du docteur/configuration. Il reste en dessous de Stable car le chemin d'accès de l'opérateur réel dépend toujours du comportement volatil de Baileys/session et manque d'une preuve WhatsApp-spécifique d'installation vers compte lié.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Channel Setup and Operations`
- Fusionnée à partir de : `Channel Operations`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Métadonnées du plugin officiel @openclaw/whatsapp : Métadonnées du plugin officiel @openclaw/whatsapp, points d'entrée du package et découverte de configuration.
- Installation du plugin openclaw whatsapp : Installation du plugin openclaw whatsapp et guidance de configuration en premier.
- Schéma de configuration du canal : Schéma de configuration du canal, hooks de plugin, finalisation de configuration, compte par défaut et gestion des secrets.
- Cycle de vie du socket Baileys : Cycle de vie du socket Baileys, état du contrôleur de connexion, décisions de reconnexion et statut de réparation.
- Dépannage de l'opérateur : Dépannage de l'opérateur pour les boucles de reconnexion, les sockets obsolètes, runtime Bun/Node
- Cycle de vie du socket Baileys : Couvre le cycle de vie du socket Baileys, l'état du contrôleur de connexion, le comportement des décisions de reconnexion.
- Dépannage de l'opérateur pour les boucles de reconnexion : Couvre le dépannage de l'opérateur pour les boucles de reconnexion, les sockets obsolètes, le comportement du runtime Bun/Node.

## Fonctionnalités

- Métadonnées du plugin officiel @openclaw/whatsapp : Métadonnées du plugin officiel @openclaw/whatsapp, points d'entrée du package et découverte de configuration.
- Installation du plugin openclaw whatsapp : Installation du plugin openclaw whatsapp et guidance de configuration en premier.
- Schéma de configuration du canal : Schéma de configuration du canal, hooks de plugin, finalisation de configuration, compte par défaut et gestion des secrets.
- Cycle de vie du socket Baileys : Cycle de vie du socket Baileys, état du contrôleur de connexion, décisions de reconnexion et statut de réparation.
- Dépannage de l'opérateur : Dépannage de l'opérateur pour les boucles de reconnexion, les sockets obsolètes, runtime Bun/Node

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : la documentation couvre l'installation du plugin, la configuration du compte, la configuration QR, le dépannage, les mises en garde Node/Bun et la référence du plugin ; la source déclare le manifeste du plugin externe, les scripts du package, le schéma de configuration, les hooks de configuration, la résolution du compte et la finalisation de la configuration.
- Signaux négatifs : la preuve d'installation est principalement soutenue par la documentation/source et les tests unitaires ; les résultats actuels de l'archive incluent la confusion configuration/setup et le risque de boucle de redémarrage Docker.
- Lacunes d'intégration : une preuve générique d'installation de plugin existe, mais aucun scénario WhatsApp-spécifique localisé ne prouve l'installation ClawHub/npm, les écritures de configuration de configuration, le lien QR et la sortie de statut/docteur comme un flux de travail d'opérateur.

## Score de qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : `whatsapp plugin install config auth dir` a surfacé le problème ouvert #86612 Boucle de redémarrage de la passerelle Docker après l'installation du plugin externe officiel, le problème ouvert #87604 confusion d'avertissement plugin-disabled-but-config-present, et l'historique PR adjacent d'empaquetage/cache. `@openclaw/whatsapp package external plugin install` a surfacé #85869 sur la compatibilité des versions plugin/core après installation flottante.
- Rapports Discrawl : `whatsapp plugin install config auth dir` a retourné des discussions héritées de configuration/aide/installation ; `WhatsApp Baileys session QR login channels login` a retourné des rapports de volatilité de session/auth et des guidance de déconnexion/reliaison.
- Bonnes qualités : le package est explicitement marqué comme officiel, les défauts stable/bêta par défaut à l'installation ClawHub de confiance, le fallback npm et le comportement de développement local sont séparés, les métadonnées déclarent la compatibilité hôte/API, la configuration évite de charger Baileys dans les chemins de métadonnées uniquement, et la résolution du chemin compte/auth est explicite.
- Mauvaises qualités : l'empaquetage du plugin externe, le comportement de l'hôte Node/Bun, la configuration QR uniquement, la compatibilité des versions plugin/core, et les choix du répertoire d'authentification restent faciles à mal configurer ; les avertissements plugin-disabled peuvent toujours confondre les opérateurs lorsque la configuration est présente.
- Exclu de la qualité : la couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas augmenté ou diminué ce score de qualité.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/whatsapp.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les métadonnées du plugin officiel @openclaw/whatsapp, l'installation du plugin openclaw whatsapp, le schéma de configuration du canal, le cycle de vie du socket Baileys, le dépannage de l'opérateur.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les mises en garde visibles par l'opérateur.

## Lacunes connues

- Ajouter un scénario WhatsApp-spécifique d'installation-à-configuration-à-connexion pour ClawHub et le fallback npm.
- Fermer la boucle sur la garde de version plugin/core, le crash de démarrage du compte secondaire et la récupération du canal coincé sans reliaison forcée.
- Rendre les diagnostics plugin-disabled-but-config-present plus faciles à distinguer des défaillances de résolution de package.
- Garder les mises en garde du runtime Bun et Node près du chemin d'installation plutôt que seulement dans le dépannage.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:10` documente l'installation du plugin à la demande, la résolution en priorité ClawHub et le fallback npm.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:43` documente les points d'entrée de configuration rapide et de connexion QR.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:557` documente la sélection du compte, les chemins d'accès aux identifiants et le comportement de déconnexion.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:592` documente le dépannage, la reconnexion, l'acceptation du fournisseur, les problèmes de groupe et les mises en garde Bun.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md:93` documente la configuration du canal WhatsApp, les délais de reconnexion, la configuration multi-compte et la migration d'authentification héritée.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/whatsapp.md:12` documente le package officiel, la disponibilité ClawHub/npm et la surface du canal.

### Source

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/openclaw.plugin.json:1` déclare l'ID du plugin WhatsApp officiel, le nom, le canal, le schéma de configuration et les hooks.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/package.json:1` déclare `@openclaw/whatsapp`, les scripts de publication ClawHub/npm et la dépendance Baileys.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/channel.ts:69` construit le canal du plugin avec configuration, appairage, sortant, helpers de groupe, liste d'autorisation, résolveur de cible, actions et approbations.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/channel.setup.ts:17` câble la configuration et les migrations héritées.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/accounts.ts:23` définit les champs de compte résolus, le comportement du répertoire d'authentification et l'activation du compte.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/setup-core.ts:1` et `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/setup-finalize.ts:1` implémentent la mutation de configuration au moment de la configuration et la finalisation.
- `/Users/kevinlin/code/openclaw/scripts/lib/official-external-channel-catalog.json:488` répertorie WhatsApp comme une installation de canal externe officielle.
- `/Users/kevinlin/code/openclaw/src/commands/onboarding-plugin-install.ts:303` choisit les défauts distants stable/bêta et sépare la gestion des sources ClawHub, npm et développement local.
- `/Users/kevinlin/code/openclaw/src/plugins/install.ts:145` vérifie la compatibilité de l'API hôte et du plugin.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/vitest/vitest.extension-whatsapp.config.ts:11` définit la voie de test d'extension WhatsApp délimitée.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/whatsapp/whatsapp-live.runtime.ts:387` construit une configuration QA en direct avec activation du plugin, configuration du compte, allowFrom, politique de groupe et approbations.
- `/Users/kevinlin/code/openclaw/docs/concepts/qa-e2e-automation.md:694` documente les scénarios QA WhatsApp et le comportement du pool d'identifiants.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/sweep.sh:40` couvre le comportement générique d'installation/runtime/désinstallation du plugin groupé.
- `/Users/kevinlin/code/openclaw/.github/workflows/qa-live-transports-convex.yml:671` exécute une voie QA WhatsApp en direct adjacente au comportement du runtime.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/config-schema.test.ts:1` couvre le comportement du schéma de configuration WhatsApp.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/setup-surface.test.ts:1` couvre le comportement de la surface de configuration.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/channel.setup.test.ts:1` couvre le câblage de la configuration.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/accounts.test.ts:1` et `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/accounts.whatsapp-auth.test.ts:1` couvrent la résolution du compte et du chemin d'authentification.
- `/Users/kevinlin/code/openclaw/src/commands/channel-setup/plugin-install.test.ts:364` couvre l'installation npm, le répertoire d'installation du profil actif, les défauts dev/bêta, la source ClawHub, le fallback et le rechargement du registre de configuration uniquement.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "whatsapp plugin install config auth dir" --json`

Résultats :

- Le problème ouvert #86612 a signalé une boucle de redémarrage du conteneur de passerelle Docker après l'installation du plugin externe WhatsApp officiel et incluait des avertissements de configuration.
- Le problème ouvert #87604 a signalé un état d'avertissement plugin-disabled-but-config-present.
- Les résultats adjacents ont couvert le travail de plugin/cache groupé et les refactorisations de politique de compte WhatsApp.

Requête :

`gitcrawl search openclaw/openclaw --query "@openclaw/whatsapp package external plugin install" --json`

Résultats :

- A surfacé #85869 pour la compatibilité des versions plugin/core après installation flottante, plus les PR de durcissement d'installation de plugin.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl --json search "whatsapp plugin install config auth dir" --limit 5`

Résultats :

- A retourné des messages hérités de configuration/aide/installation de Clawdbot et aucun défaut d'installation plus fort que les résultats de Gitcrawl.

Requête :

`/Users/kevinlin/.local/bin/discrawl --json search "WhatsApp Baileys session QR login channels login" --limit 5`

Résultats :

- A retourné des rapports de volatilité de session/auth, y compris une discussion de réécriture d'identifiants atomiques, des rapports de boucle de redémarrage et une guidance de support pour se déconnecter/reliaison après les défaillances de Baileys.
