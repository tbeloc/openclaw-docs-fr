---
title: "Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux - Note de Maturité de Configuration et d'Exploitation des Canaux"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux - Note de Maturité de Configuration et d'Exploitation des Canaux

## Résumé

La couche partagée de catalogue/installation/statut est le composant transversal qui rend les canaux régionaux découvrables et opérables. Elle couvre la navigation des docs, les entrées du sélecteur de canaux, les enregistrements officiels du catalogue externe, les alias, les plans d'installation, les marqueurs d'installation officielle de confiance, les indices de réparation des plugins manquants, la validation des plugins, la sortie du statut/liste des canaux et la localisation de l'assistant. Cette couche partagée est mieux couverte que plusieurs runtimes externes individuels, mais les preuves d'archive récentes montrent une confusion installation/liste/statut, des lignes de sélecteur/statut indéfinies, des défaillances de démarrage de canaux optionnels et une rotation du chemin de confiance des canaux externes.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Configuration et Exploitation des Canaux`
- Fusionnée à partir de : `Catalogue et Configuration`, `Canaux de Bot`, `Canaux de Compte Personnel`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Index des canaux docs : Index des canaux docs, pages de référence des plugins, redirections et liste de support d'appairage pour les canaux régionaux
- Entrées du catalogue de canaux externes officiels : Entrées du catalogue de canaux externes officiels pour WeCom, Yuanbao, Weixin et canaux externes adjacents
- Catalogue principal canal-plugin : Catalogue principal canal-plugin, normalisation des alias, résolution du plan d'installation, drapeaux de source de confiance, indices de réparation et sortie de statut/liste
- Assistant de configuration des canaux : Assistant de configuration des canaux et blurbs i18n pour les canaux régionaux
- Plugin manquant : Plugin manquant, plugin obsolète, mise à niveau brute du gestionnaire de paquets et chemins de docteur/réparation
- Préoccupations d'ingress/accès/refactorisation entre canaux : Préoccupations d'ingress/accès/refactorisation entre canaux pour les plugins régionaux
- Configuration du canal bot Feishu/Lark : Configuration du canal bot Feishu/Lark via App ID/App Secret manuel ou enregistrement d'application QR
- Mode par défaut WebSocket : Mode par défaut WebSocket et mode webhook optionnel
- Appairage DM : Appairage DM, listes blanches, politique de groupe, portes de mention, remplacements par groupe et restrictions d'expéditeur
- Livraison de messages : Livraison de messages, réponses, cartes de streaming, réactions, commentaires, menus de bot et actions de carte
- Document Feishu : Document Feishu, wiki, lecteur, bitable et outils d'agent dynamique
- Gestion des identifiants multi-comptes : Gestion des identifiants multi-comptes et dépannage pour les déploiements régionaux Feishu/Lark
- Configuration AppID/AppSecret de QQ Open Platform : Configuration AppID/AppSecret de QQ Open Platform et gestion des comptes par défaut env/config
- Chat privé C2C : Chat privé C2C, messages de groupe, messages de canal de guilde et analyse des cibles
- Activation de groupe : Activation de groupe, portes de mention, historique de groupe, politiques d'outils et listes blanches d'expéditeurs
- Messages multimédias enrichis : Messages multimédias enrichis entrants et sortants incluant images, voix, vidéo, fichiers, STT/TTS et envois de voix natifs
- Commandes slash : Commandes slash, boutons d'approbation, outils de rappel/canal et enregistrement de commandes de framework
- Connexions de passerelle multi-comptes : Connexions de passerelle multi-comptes, cache de jetons, sauvegardes d'identifiants, diagnostics et comportement de reconnexion
- Canal externe Tencent Yuanbao : Canal externe Tencent Yuanbao openclaw-plugin-yuanbao
- Configuration AppKey/AppSecret : Configuration AppKey/AppSecret, assistant de connexion, config multi-comptes et routage de compte par défaut
- DMs : DMs, groupes, exigences de mention, mode réponse, contexte d'historique de groupe, menus de commande slash et réponses de secours
- Stratégie de file d'attente sortante : Stratégie de file d'attente sortante, réglage de fusion de texte, caractères max, plafonds multimédias, comportement de débordement et streaming au niveau des blocs
- Catalogue externe officiel côté noyau : Catalogue externe officiel côté noyau, métadonnées d'installation, alias, blurbs d'assistant et contrats de catalogue de canaux
- Bot Zalo Bot Creator / Marketplace : Canal DM du bot Zalo Bot Creator / Marketplace
- Mode par défaut d'interrogation longue : Mode par défaut d'interrogation longue et mode webhook HTTPS optionnel
- Jeton de bot : Jeton de bot, fichier de jeton, multi-comptes, appairage DM et comportement de liste blanche
- Schéma de politique de groupe : Schéma de politique de groupe et portes de groupe fermées même où les groupes Marketplace ne sont pas utilisables
- Texte : Texte, espaces réservés multimédias, chunking sortant, déduplication de relecture, limitation de débit, secrets webhook et support proxy
- Sondes de statut : Sondes de statut et dépannage pour les problèmes de jeton/config/webhook
- Messagerie personnelle WeChat/Weixin : Messagerie personnelle WeChat/Weixin via paquet externe @tencent-weixin/openclaw-weixin
- Installation du plugin : Installation du plugin, activation, compatibilité, connexion QR, jetons de compte enregistrés et id de canal openclaw-weixin
- Appairage de message direct : Appairage de message direct et isolation de session par compte
- Métadonnées du catalogue côté noyau : Métadonnées du catalogue côté noyau, alias, plans d'installation, marqueurs de confiance des plugins, indices de statut/réparation, redirections docs et découverte de canaux
- Comportement du processus sidecar/helper externe : Comportement du processus sidecar/helper externe et protections de nettoyage de processus obsolètes
- Plugin de canal zalouser : Plugin de canal zalouser pour l'automatisation du compte personnel Zalo via zca-js natif
- Connexion QR : Connexion QR, profils enregistrés, sélection multi-comptes/profil et runtime local de passerelle
- Appairage DM : Appairage DM, politique de groupe, gating de groupe, pairs de répertoire et routage d'expéditeur/session
- Envoi de message : Envoi de message, médias image/lien/document, réactions, statut, outils amis/groupes/moi et normalisation du style de texte
- Vérifications de docteur/statut pour la disponibilité du runtime : Vérifications de docteur/statut pour la disponibilité du runtime et santé du profil/session
- Risque de compte non officiel explicite : Risque de compte non officiel explicite et protections de l'opérateur
- Configuration AppID/AppSecret de QQ Open Platform et : Couvre la configuration AppID/AppSecret de QQ Open Platform et le comportement de gestion des comptes par défaut env/config.
- Chat privé C2C : Couvre le chat privé C2C, les messages de groupe, les messages de canal de guilde et le comportement d'analyse des cibles.
- Activation de groupe : Couvre l'activation de groupe, les portes de mention, l'historique de groupe, les politiques d'outils et le comportement des listes blanches d'expéditeurs.
- Messages multimédias enrichis entrants et sortants incluant : Couvre les messages multimédias enrichis entrants et sortants incluant images, voix, vidéo, fichiers, STT/TTS et le comportement des envois de voix natifs.
- Commandes slash : Couvre les commandes slash, les boutons d'approbation, les outils de rappel/canal et le comportement d'enregistrement de commandes de framework.
- Connexions de passerelle multi-comptes : Couvre les connexions de passerelle multi-comptes, le cache de jetons, les sauvegardes d'identifiants, les diagnostics et le comportement de reconnexion.
- Canal externe Tencent Yuanbao `openclaw-plugin-yuanbao` : Portée des preuves pour le canal externe Tencent Yuanbao `openclaw-plugin-yuanbao`.
- Configuration AppKey/AppSecret : Couvre la configuration AppKey/AppSecret, l'assistant de connexion, la config multi-comptes et le comportement de routage de compte par défaut.
- DMs : Couvre les DMs, les groupes, les exigences de mention, le mode réponse, le contexte d'historique de groupe, les menus de commande slash et le comportement des réponses de secours.
- Stratégie de file d'attente sortante : Couvre la stratégie de file d'attente sortante, le réglage de fusion de texte, les caractères max, les plafonds multimédias, le comportement de débordement et le streaming au niveau des blocs.
- Catalogue externe officiel côté noyau : Couvre le catalogue externe officiel côté noyau, les métadonnées d'installation, les alias, les blurbs d'assistant et le comportement des contrats de catalogue de canaux.
- Bot Zalo Bot Creator / Marketplace : Couvre le comportement du canal DM du bot Zalo Bot Creator / Marketplace.
- Mode par défaut d'interrogation longue et webhook HTTPS optionnel : Couvre le mode par défaut d'interrogation longue et le comportement du mode webhook HTTPS optionnel.
- Jeton de bot : Couvre le jeton de bot, le fichier de jeton, le multi-comptes, l'appairage DM et le comportement de liste blanche.
- Schéma de politique de groupe et portes de groupe fermées : Couvre le schéma de politique de groupe et le comportement des portes de groupe fermées même où les groupes Marketplace ne sont pas utilisables.
- Texte : Couvre le texte, les espaces réservés multimédias, le chunking sortant, la déduplication de relecture, la limitation de débit, les secrets webhook et le comportement du support proxy.
- Sondes de statut et dépannage pour les problèmes de jeton/config/webhook : Portée des preuves pour les sondes de statut et le dépannage pour les problèmes de jeton/config/webhook.
- Plugin de canal `zalouser` pour Zalo Personnel : Couvre le plugin de canal `zalouser` pour l'automatisation du compte personnel Zalo via le comportement natif `zca-js`.
- Connexion QR : Couvre la connexion QR, les profils enregistrés, la sélection multi-comptes/profil et le comportement du runtime local de passerelle.
- Appairage DM : Couvre l'appairage DM, la politique de groupe, le gating de groupe, les pairs de répertoire et le comportement du routage d'expéditeur/session.
- Envoi de message : Couvre l'envoi de message, les médias image/lien/document, les réactions, le statut, les outils amis/groupes/moi et le comportement de normalisation du style de texte.
- Vérifications de docteur/statut pour la disponibilité du runtime et : Couvre les vérifications de docteur/statut pour la disponibilité du runtime et le comportement de santé du profil/session.
- Risque de compte non officiel explicite et protections de l'opérateur : Portée des preuves pour le risque de compte non officiel explicite et les protections de l'opérateur.

## Fonctionnalités

- Index des canaux docs : Index des canaux docs, pages de référence des plugins, redirections et liste de support d'appairage pour les canaux régionaux
- Entrées du catalogue de canaux externes officiels : Entrées du catalogue de canaux externes officiels pour WeCom, Yuanbao, Weixin et canaux externes adjacents
- Catalogue principal canal-plugin : Catalogue principal canal-plugin, normalisation des alias, résolution du plan d'installation, drapeaux de source de confiance, indices de réparation et sortie de statut/liste
- Assistant de configuration des canaux : Assistant de configuration des canaux et blurbs i18n pour les canaux régionaux
- Plugin manquant : Plugin manquant, plugin obsolète, mise à niveau brute du gestionnaire de paquets et chemins de docteur/réparation
- Préoccupations d'ingress/accès/refactorisation entre canaux : Préoccupations d'ingress/accès/refactorisation entre canaux pour les plugins régionaux

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (72%)`
- Signaux positifs : les tests principaux couvrent le catalogue externe officiel, le plan d'installation, l'installation du plugin CLI, la liste/statut des canaux, la validation de la configuration, les indices de réparation, la normalisation des alias, le registre des manifestes et les contrats de catalogue de canaux.
- Signaux négatifs : la couverture est la plus forte pour le comportement du plan de contrôle/métadonnées, pas pour les runtimes des canaux externes eux-mêmes.
- Lacunes d'intégration : aucun scénario de catalogue de canaux régionaux unique n'a été trouvé qui installe tous les types de canaux/comptes nommés, vérifie la sortie de statut/liste, exécute la configuration/connexion, envoie un message et vérifie les indices de réparation sur les plugins groupés et externes.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves du flux de runtime réel sur le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : les recherches larges de catalogue régional ont trouvé des rapports autour des canaux externes officiels configurés manquant des plugins, dérive d'id/version de catalogue, comportement de canal non supporté openclaw-weixin, omissions de statut Feishu, et échecs d'amorçage de plugin/canal.
- Rapports Discrawl : `official external plugin catalog` a retourné l'examen du mainteneur de la dérivation d'installation officielle de confiance, les notes de version du plugin indiquant que 25/25 plugins officiels gérés par version ont été publiés, et les avertissements autour des tests de chemin de confiance plus larges ; `regional channel` a retourné l'échec de démarrage Feishu régional optionnel et les commentaires régionaux/proxy.
- Bonnes qualités : la conception du catalogue sépare les chemins de plugin groupés, officiels externes et tiers ; les docs et les conseils de réparation indiquent généralement aux opérateurs comment installer les plugins officiels manquants ; l'état d'installation de confiance est dérivé des enregistrements d'installation et de la correspondance catalogue/package plutôt que d'une assertion de manifeste brute.
- Mauvaises qualités : la sortie de liste/statut de canal a montré des lignes indéfinies et des entrées régionales dupliquées, le support de package externe est sensible aux chemins Nix/gestionnaire de package brut, et les canaux régionaux optionnels ont précédemment cassé le démarrage CLI non lié.
- Exclu de la qualité : présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel ; ce sont uniquement des entrées de Couverture.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score de Complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/feishu-qq-bot-wechat-yuanbao-zalo-zalo-personal-regional-channels.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent l'étendue de la taxonomie pour l'index de canal Docs, les entrées du catalogue de canal externe officiel, le catalogue de canal-plugin principal, l'assistant de configuration de canal, le plugin manquant, les préoccupations d'ingress/accès/refactorisation inter-canaux.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter un scénario de catalogue qui exerce install/list/status/setup/repair sur Feishu, QQ Bot, WeChat, Yuanbao, Zalo et Zalo Personal.
- Garder les entrées du catalogue externe épinglées avec des spécifications npm validées et des chemins de docs, en particulier après les versions de plugin en amont.
- Continuer à renforcer le chargement optionnel de plugin régional afin que les non-utilisateurs d'un canal régional ne puissent pas rencontrer d'échecs de démarrage CLI non liés.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/index.md` répertorie WeChat et Yuanbao parmi les canaux et les identifie comme des plugins externes.
- `/Users/kevinlin/code/openclaw/docs/channels/pairing.md` répertorie les ids de canal supportés incluant `feishu`, `openclaw-weixin`, `zalo` et `zalouser`.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/feishu.md`, `qqbot.md`, `zalo.md` et `zalouser.md` fournissent des entrées de référence de plugin pour les plugins régionaux groupés/officiels.
- `/Users/kevinlin/code/openclaw/docs/plugins/architecture-internals.md` décrit la fusion du catalogue de canal externe.

### Source

- `/Users/kevinlin/code/openclaw/scripts/lib/official-external-channel-catalog.json` contient des enregistrements de canal externe officiel incluant Yuanbao et Weixin avec ids, labels, aliases, chemins de docs et spécifications npm.
- `/Users/kevinlin/code/openclaw/src/channels/plugins/catalog.ts`, `src/plugins/official-external-plugin-catalog.ts`, `src/cli/plugin-install-plan.ts`, `src/cli/plugins-install-command.ts`, `src/commands/channels/status-config-format.ts` et `src/plugins/official-external-plugin-repair-hints.ts` implémentent le catalogue, l'installation, le statut et le comportement de réparation.
- `/Users/kevinlin/code/openclaw/src/wizard/setup.official-plugins.ts` et les fichiers de locale de l'assistant exposent le sélecteur de configuration et les descriptions de canal localisées.
- `/Users/kevinlin/code/openclaw/src/config/config.plugin-validation.test.ts`, `src/plugins/manifest-registry.test.ts` et `src/plugins/install-security-scan.runtime.ts` définissent la validation et le comportement du chemin de confiance pour les plugins externes/officiels.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/cli/plugins-cli.install.test.ts`, `src/cli/plugin-install-plan.test.ts`, `src/commands/channels.list.test.ts`, `src/commands/channels.status.command-flow.test.ts`, `src/plugins/official-external-plugin-catalog.test.ts`, `src/plugins/official-external-plugin-repair-hints.test.ts`, `src/channels/plugins/contracts/channel-catalog.contract.test.ts`, `src/channels/plugins/contracts/test-helpers/channel-plugin-catalog-contract-suites.ts` et `src/wizard/setup.official-plugins.test.ts` exercent les flux du plan de contrôle partagé.
- Aucun scénario de bout en bout unique n'a été trouvé qui installe et teste chaque type de canal/compte régional nommé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/channels/registry.helpers.test.ts`, `src/channels/plugins/catalog.test.ts`, `src/config/config.plugin-validation.test.ts`, `src/plugins/channel-catalog-registry.test.ts`, `src/plugins/manifest-registry.test.ts`, `src/plugins/update.test.ts` et `src/commands/doctor/shared/preview-warnings.test.ts` couvrent le comportement d'alias, catalogue, validation, manifeste, mise à jour et doctor ciblé.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "official external channel catalog missing plugin repair hints Feishu WhatsApp Yuanbao" --json --limit 6`
- `gitcrawl search openclaw/openclaw --query "regional channels Chinese memory navigation Feishu Zalo profile env vars" --json --limit 6`
- `gitcrawl search openclaw/openclaw --query "openclaw-weixin" --json --limit 8`
- `gitcrawl search openclaw/openclaw --query "Yuanbao" --json --limit 8`

Résultats :

- Les requêtes larges du catalogue externe ont retourné des rapports ouverts dans les recherches de composants adjacents : omissions de statut Feishu, problèmes d'enregistrement/routage/message de canal non supporté openclaw-weixin, précédent de catalogue Yuanbao et problèmes de profil et média Zalo/Zalo Personal.
- La requête `openclaw-weixin` a retourné plusieurs problèmes d'installation/routage/message de canal externe, et la requête `Yuanbao` a retourné une RP de précédent de catalogue externe officiel.

### Requêtes Discrawl

Requête :

- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "official external plugin catalog"`
- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "regional channel"`

Résultats :

- La requête du catalogue de plugin externe officiel a retourné une discussion du mainteneur du 2026-05-18 selon laquelle `trustedOfficialInstall` est dérivée des enregistrements d'installation plus la correspondance catalogue/package externe officielle, pas l'auto-assertion de manifeste ; elle a également retourné les notes de version indiquant que 25/25 plugins officiels gérés par version ont été publiés.
- La requête de canal régional a retourné le problème `#69959` concernant une dépendance Feishu/Lark optionnelle cassant le démarrage CLI non-Lark, les commentaires sur la question de savoir si WhatsApp devrait être optionnel/régional, et les commentaires d'examen de support proxy/régional.
