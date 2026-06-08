---
title: "Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, regional channels - Personal Account Channels Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, regional channels - Personal Account Channels Maturity Note

## Résumé

Le support WeChat est intentionnellement externalisé via le package `@tencent-weixin/openclaw-weixin` de Tencent. Le cœur OpenClaw fournit la documentation, les métadonnées du catalogue, la gestion de l'installation/statut des plugins, les alias d'identifiants de canal, la documentation d'appairage et les contrats génériques du runtime des plugins, mais le runtime spécifique à WeChat n'est pas présent dans le dépôt source. La couverture est donc faible pour cet audit : la source prouve les hooks d'intégration et les métadonnées d'installation, mais pas la connexion par code QR, le comportement de Tencent iLink, les internals du moniteur/runtime ou la livraison réelle WeChat. La qualité est limitée par les preuves d'archives de dérive de version, les problèmes d'initialisation du runtime, les échecs d'enregistrement, les réponses perdues, les bugs de média/session, les frictions d'installation Nix et les contraintes de compte en amont.

## Portée de la catégorie

Inclus dans cette catégorie :

- Messagerie personnelle WeChat/Weixin : Messagerie personnelle WeChat/Weixin via le package externe @tencent-weixin/openclaw-weixin
- Installation du plugin : Installation du plugin, activation, compatibilité, connexion par code QR, jetons de compte sauvegardés et identifiant de canal openclaw-weixin
- Appairage de messages directs : Appairage de messages directs et isolation de session par compte
- Métadonnées du catalogue côté cœur : Métadonnées du catalogue côté cœur, alias, plans d'installation, marqueurs de confiance des plugins, indices de statut/réparation, redirections de documentation et découverte de canal
- Comportement du processus sidecar/helper externe : Comportement du processus sidecar/helper externe et protections de nettoyage des processus obsolètes
- Plugin de canal zalouser : Plugin de canal zalouser pour l'automatisation du compte personnel Zalo via zca-js natif
- Connexion par code QR : Connexion par code QR, profils sauvegardés, sélection multi-compte/profil et runtime local de passerelle
- Appairage DM : Appairage DM, politique de groupe, gating de groupe, pairs de répertoire et routage de l'expéditeur/session
- Envoi de message : Envoi de message, média image/lien/document, réactions, statut, outils amis/groupes/moi et normalisation du style de texte
- Vérifications Doctor/statut pour la disponibilité du runtime : Vérifications Doctor/statut pour la disponibilité du runtime et la santé du profil/session
- Risque explicite de compte non officiel : Risque explicite de compte non officiel et protections de l'opérateur

## Fonctionnalités

- Messagerie personnelle WeChat/Weixin : Messagerie personnelle WeChat/Weixin via le package externe @tencent-weixin/openclaw-weixin
- Installation du plugin : Installation du plugin, activation, compatibilité, connexion par code QR, jetons de compte sauvegardés et identifiant de canal openclaw-weixin
- Appairage de messages directs : Appairage de messages directs et isolation de session par compte
- Métadonnées du catalogue côté cœur : Métadonnées du catalogue côté cœur, alias, plans d'installation, marqueurs de confiance des plugins, indices de statut/réparation, redirections de documentation et découverte de canal
- Comportement du processus sidecar/helper externe : Comportement du processus sidecar/helper externe et protections de nettoyage des processus obsolètes
- Plugin de canal zalouser : Plugin de canal zalouser pour l'automatisation du compte personnel Zalo via zca-js natif
- Connexion par code QR : Connexion par code QR, profils sauvegardés, sélection multi-compte/profil et runtime local de passerelle
- Appairage DM : Appairage DM, politique de groupe, gating de groupe, pairs de répertoire et routage de l'expéditeur/session
- Envoi de message : Envoi de message, média image/lien/document, réactions, statut, outils amis/groupes/moi et normalisation du style de texte
- Vérifications Doctor/statut pour la disponibilité du runtime : Vérifications Doctor/statut pour la disponibilité du runtime et la santé du profil/session
- Risque explicite de compte non officiel : Risque explicite de compte non officiel et protections de l'opérateur

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Experimental (42%)`
- Signaux positifs : la documentation et la source prouvent le catalogue externe officiel, les alias de canal, les flux d'installation/activation/statut des plugins, la documentation d'appairage, les notes de compatibilité de version et l'intégration générique du runtime des plugins.
- Signaux négatifs : la source du runtime spécifique à WeChat et les tests sont externes à ce dépôt ; aucun scénario actuel de connexion par code QR ou de livraison de message n'a été trouvé dans le dépôt source.
- Lacunes d'intégration : cet audit n'a pas pu vérifier les internals du package externe pour la connexion Tencent iLink, le moniteur de compte, le téléchargement/téléversement de média, la persistance des jetons, la livraison de messages directs, la gestion des groupes, la reconnexion ou le cycle de vie du sidecar au-delà des hooks cœur et des archives.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux de runtime réel dans le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Experimental (44%)`
- Rapports Gitcrawl : une large recherche `openclaw-weixin` a retourné des rapports ouverts pour la connexion par code QR qui s'accroche, les réponses perdues par intermittence, l'échec d'enregistrement du canal runtime, le canal non supporté dans la livraison cron, les directives de média autonomes supprimées, l'envoi proactif faux succès/chunks manquants, le routage du type de session incorrect et la fuite d'accountId.
- Rapports Discrawl : la recherche `openclaw-weixin` a retourné l'échec d'installation du plugin Nix, l'échec de connexion du canal indéfini, la dérive du catalogue bêta de `2.4.1` à `2.4.3`, la prudence du mainteneur autour des problèmes de sécurité récents et les rapports des utilisateurs autour des problèmes d'initialisation du runtime.
- Bonnes qualités : la documentation indique explicitement que le runtime spécifique à WeChat est externe, les chats de groupe ne sont pas annoncés par les métadonnées de capacité actuelles, les chats directs et les médias sont supportés par le plugin externe et le nettoyage du démarrage cœur a une protection générique contre le nettoyage du parent sidecar.
- Mauvaises qualités : opacité du runtime externe, dérive de version du package, sensibilité de l'environnement d'installation, fragilité de la connexion par code QR et plusieurs rapports récents de livraison de message/session rendent le risque de support public élevé.
- Exclu de la qualité : présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux de runtime réel ; ce sont uniquement des entrées de couverture.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou de flux de runtime réel comme entrée de notation.

## Score de complétude

- Score : `Experimental (42%)`
- Instructions de surface : évaluées par rapport à `references/completeness/feishu-qq-bot-wechat-yuanbao-zalo-zalo-personal-regional-channels.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la messagerie personnelle WeChat/Weixin, l'installation du plugin, l'appairage de messages directs, les métadonnées du catalogue côté cœur, le comportement du processus sidecar/helper externe, le plugin de canal zalouser, la connexion par code QR, l'appairage DM, l'envoi de message, les vérifications Doctor/statut pour la disponibilité du runtime, le risque explicite de compte non officiel.
- Signaux négatifs : la note archivée a précédé la notation de complétude du processus-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter ou lier une fiche d'évaluation actuelle du package externe pour la connexion par code QR, le chat direct, les médias, la persistance des jetons de compte, la reconnexion, les envois proactifs et le routage de session.
- Garder le catalogue cœur épinglé à une version de package externe validée et préserver les conseils de mise à niveau/réparation lorsque les métadonnées du package externe dérivent.
- Clarifier le support d'installation du plugin Nix/non-npm et les modes d'échec pour les packages de canal externes.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/wechat.md` explique que le code WeChat ne réside pas dans le cœur OpenClaw et qu'OpenClaw fournit le contrat générique du plugin de canal tandis que le paquet externe possède la connexion par code QR, les appels API Tencent iLink, le téléchargement/téléversement de médias, les jetons de contexte et la surveillance.
- `/Users/kevinlin/code/openclaw/docs/channels/wechat.md` documente le paquet `@tencent-weixin/openclaw-weixin`, l'ID de canal `openclaw-weixin`, les chats directs et le support des médias, les chats de groupe non annoncés, les commandes d'installation, la connexion par code QR, l'isolation de session par compte, les commandes d'appairage, la compatibilité des versions, le contexte de nettoyage du sidecar, le dépannage et les commandes de désactivation/réparation.
- `/Users/kevinlin/code/openclaw/docs/channels/index.md` répertorie WeChat comme plugin Tencent iLink Bot via connexion par code QR et chats privés uniquement.

### Source

- `/Users/kevinlin/code/openclaw/scripts/lib/official-external-channel-catalog.json` définit l'entrée externe officielle `@tencent-weixin/openclaw-weixin` avec les ID de plugin/canal, les alias `weixin`, `wechat` et `微信`, le chemin de documentation `/channels/wechat` et la spécification npm `@tencent-weixin/openclaw-weixin@2.4.3`.
- `/Users/kevinlin/code/openclaw/src/channels/registry.helpers.test.ts` valide l'enregistrement des alias `openclaw-weixin` et la normalisation.
- `/Users/kevinlin/code/openclaw/src/commands/channel-setup/channel-plugin-resolution.test.ts`, `src/cli/directory-cli.test.ts`, `src/config/channel-configured.test.ts`, `src/commands/doctor/shared/preview-warnings.test.ts` et `src/commands/doctor/shared/stale-plugin-config.test.ts` couvrent les interactions de résolution côté cœur, de configuration, de répertoire et de docteur.
- `/Users/kevinlin/code/openclaw/src/infra/restart-stale-pids.test.ts` inclut le contexte de régression pour un processus enfant sidecar `openclaw-weixin` tentant de nettoyer la passerelle parent.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/cli/plugins-cli.install.test.ts`, `src/cli/plugin-install-plan.test.ts`, `src/plugins/official-external-plugin-catalog.test.ts`, `src/channels/plugins/catalog.test.ts` et `src/channels/plugins/contracts/channel-catalog.contract.test.ts` exercent le catalogue de plugins externes officiels, l'installation et le comportement d'installation de confiance sur lesquels WeChat s'appuie.
- Aucun scénario de connexion par code QR WeChat en direct ou de livraison de messages dans le référentiel n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/channels/registry.helpers.test.ts`, `src/plugins/channel-catalog-registry.test.ts`, `src/config/config.plugin-validation.test.ts`, `src/commands/channels.list.test.ts` et `src/commands/channels.status.command-flow.test.ts` couvrent le comportement d'alias, de catalogue, de validation, de liste et de statut ciblé pour les canaux externes incluant `openclaw-weixin`.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "openclaw-weixin QR login sidecar compiled runtime output version too old" --json --limit 6`
- `gitcrawl search openclaw/openclaw --query "openclaw-weixin" --json --limit 8`

Résultats :

- La requête spécifique à la fonctionnalité a été représentée par la requête large car la correspondance de phrase exacte n'a retourné aucun résultat ciblé supplémentaire.
- La requête large a retourné des résultats ouverts incluant `#62120` la connexion par code QR se bloque avant l'apparition du code QR, `#86877` les réponses de l'assistant perdues par intermittence, `#86314` le canal non enregistré dans le runtime de la passerelle sur WSL2, `#78754` le cron ne supporte pas le canal, `#78697` la directive de média autonome supprimée, `#79293` l'envoi proactif faux succès/chunks manquants, `#81723` type de session WeChat incorrect et `#69525` fuite d'accountId.

### Requêtes Discrawl

Requête :

- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "openclaw-weixin"`

Résultats :

- A retourné la discussion d'installation Nix/openclaw-weixin du 2026-05-17 et l'échec de connexion de canal indéfini, la discussion de dérive de catalogue du 2026-05-14 autour de `@tencent-weixin/openclaw-weixin@2.4.1` par rapport à `2.4.3`, et les commentaires du mainteneur selon lesquels les préoccupations de sécurité rendent ces paquets externes sensibles.
