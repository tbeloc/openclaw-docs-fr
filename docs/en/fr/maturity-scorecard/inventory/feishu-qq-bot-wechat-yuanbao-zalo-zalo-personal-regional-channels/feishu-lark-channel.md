---
title: "Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux - Note de Maturité des Canaux Bot"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux - Note de Maturité des Canaux Bot

## Résumé

Feishu/Lark est le composant de canal régional le plus robuste de cette surface. La documentation décrit le canal comme prêt pour la production pour les DM de bot et les chats de groupe, la source couvre le démarrage WebSocket et webhook, la configuration QR/manuelle, la politique d'accès DM et groupe, les actions de carte, les agents dynamiques, les outils document/wiki/drive, les médias, les cartes de streaming, les réactions, les commentaires et les liaisons de thread, et l'extension dispose de tests ciblés larges. Le principal limitant est la qualité actuelle en direct : gitcrawl et discrawl montrent tous deux des régressions récentes de livraison/statut/injection d'outils Feishu et des frictions d'intégration/support.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Configuration du canal bot Feishu/Lark : configuration du canal bot Feishu/Lark via App ID/App Secret manuel ou enregistrement d'application QR
- Mode WebSocket par défaut : mode WebSocket par défaut et mode webhook optionnel
- Appairage DM : appairage DM, listes blanches, politique de groupe, portes de mention, remplacements par groupe et restrictions d'expéditeur
- Livraison de messages : livraison de messages, réponses, cartes de streaming, réactions, commentaires, menus de bot et actions de carte
- Document Feishu : outils document, wiki, drive, bitable et agent dynamique Feishu
- Gestion des identifiants multi-comptes : gestion des identifiants multi-comptes et dépannage pour les déploiements régionaux Feishu/Lark
- Configuration AppID/AppSecret de la plateforme ouverte QQ : configuration AppID/AppSecret de la plateforme ouverte QQ et gestion des comptes par défaut env/config
- Chat privé C2C : chat privé C2C, messages de groupe, messages de canal de guilde et analyse des cibles
- Activation de groupe : activation de groupe, portes de mention, historique de groupe, politiques d'outils et listes blanches d'expéditeurs
- Messages médias enrichis : médias enrichis entrants et sortants incluant images, voix, vidéo, fichiers, STT/TTS et envois de voix natifs
- Commandes slash : commandes slash, boutons d'approbation, outils de rappel/canal et enregistrement de commande de framework
- Connexions de passerelle multi-comptes : connexions de passerelle multi-comptes, cache de token, sauvegardes d'identifiants, diagnostics et comportement de reconnexion
- Canal externe Tencent Yuanbao : canal externe Tencent Yuanbao openclaw-plugin-yuanbao
- Configuration AppKey/AppSecret : configuration AppKey/AppSecret, assistant de connexion, config multi-comptes et routage de compte par défaut
- DM : DM, groupes, exigences de mention, mode réponse, contexte d'historique de groupe, menus de commande slash et réponses de secours
- Stratégie de file d'attente sortante : stratégie de file d'attente sortante, réglage de fusion de texte, caractères max, plafonds médias, comportement de débordement et streaming au niveau des blocs
- Catalogue externe officiel côté noyau : catalogue externe officiel côté noyau, métadonnées d'installation, alias, blurbs d'assistant et contrats de catalogue de canaux
- Bot Zalo Bot Creator / Marketplace : canal DM du bot Zalo Bot Creator / Marketplace
- Mode d'interrogation longue par défaut : mode d'interrogation longue par défaut et mode webhook HTTPS optionnel
- Token de bot : token de bot, token-file, multi-comptes, appairage DM et comportement de liste blanche
- Schéma de politique de groupe : schéma de politique de groupe et portes de groupe fermées par défaut même où les groupes Marketplace ne sont pas utilisables
- Texte : texte, espaces réservés médias, chunking sortant, déduplication de relecture, limitation de débit, secrets webhook et support proxy
- Sondes de statut : sondes de statut et dépannage pour les problèmes de token/config/webhook

## Fonctionnalités

- Configuration du canal bot Feishu/Lark : configuration du canal bot Feishu/Lark via App ID/App Secret manuel ou enregistrement d'application QR
- Mode WebSocket par défaut : mode WebSocket par défaut et mode webhook optionnel
- Appairage DM : appairage DM, listes blanches, politique de groupe, portes de mention, remplacements par groupe et restrictions d'expéditeur
- Livraison de messages : livraison de messages, réponses, cartes de streaming, réactions, commentaires, menus de bot et actions de carte
- Document Feishu : outils document, wiki, drive, bitable et agent dynamique Feishu
- Gestion des identifiants multi-comptes : gestion des identifiants multi-comptes et dépannage pour les déploiements régionaux Feishu/Lark
- Configuration AppID/AppSecret de la plateforme ouverte QQ : configuration AppID/AppSecret de la plateforme ouverte QQ et gestion des comptes par défaut env/config
- Chat privé C2C : chat privé C2C, messages de groupe, messages de canal de guilde et analyse des cibles
- Activation de groupe : activation de groupe, portes de mention, historique de groupe, politiques d'outils et listes blanches d'expéditeurs
- Messages médias enrichis : médias enrichis entrants et sortants incluant images, voix, vidéo, fichiers, STT/TTS et envois de voix natifs
- Commandes slash : commandes slash, boutons d'approbation, outils de rappel/canal et enregistrement de commande de framework
- Connexions de passerelle multi-comptes : connexions de passerelle multi-comptes, cache de token, sauvegardes d'identifiants, diagnostics et comportement de reconnexion
- Canal externe Tencent Yuanbao : canal externe Tencent Yuanbao openclaw-plugin-yuanbao
- Configuration AppKey/AppSecret : configuration AppKey/AppSecret, assistant de connexion, config multi-comptes et routage de compte par défaut
- DM : DM, groupes, exigences de mention, mode réponse, contexte d'historique de groupe, menus de commande slash et réponses de secours
- Stratégie de file d'attente sortante : stratégie de file d'attente sortante, réglage de fusion de texte, caractères max, plafonds médias, comportement de débordement et streaming au niveau des blocs
- Catalogue externe officiel côté noyau : catalogue externe officiel côté noyau, métadonnées d'installation, alias, blurbs d'assistant et contrats de catalogue de canaux
- Bot Zalo Bot Creator / Marketplace : canal DM du bot Zalo Bot Creator / Marketplace
- Mode d'interrogation longue par défaut : mode d'interrogation longue par défaut et mode webhook HTTPS optionnel
- Token de bot : token de bot, token-file, multi-comptes, appairage DM et comportement de liste blanche
- Schéma de politique de groupe : schéma de politique de groupe et portes de groupe fermées par défaut même où les groupes Marketplace ne sont pas utilisables
- Texte : texte, espaces réservés médias, chunking sortant, déduplication de relecture, limitation de débit, secrets webhook et support proxy
- Sondes de statut : sondes de statut et dépannage pour les problèmes de token/config/webhook

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (78%)`
- Signaux positifs : le comportement du canal soutenu par la source couvre la configuration, les tours entrants/sortants, les cartes, les réactions, les commentaires, les outils, les agents dynamiques, le streaming, la politique et les chemins multi-comptes ; Feishu dispose d'un projet de test d'extension dédié et de tests de cycle de vie/webhook.
- Signaux négatifs : aucun scénario de plateforme Feishu en direct n'a été trouvé qui commence à partir d'une application nouvelle, complète la configuration, publie/approuve les permissions de plateforme, exerce les DM, les groupes, les cartes, les médias, les outils et le comportement de reconnexion par rapport à Feishu/Lark lui-même.
- Lacunes d'intégration : la preuve de scénario public reproductible manque pour le secours de configuration QR, l'approbation/les portées de plateforme, les réponses de sujet, les rappels de carte, l'injection d'outils et l'état de livraison entre les modes WebSocket et webhook.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel à travers le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : la recherche large `Feishu` a retourné des rapports ouverts pour la propagation de contrat d'outils, l'omission de statut configuré et connecté, les commandes slash livrées-false, l'aperçu de livraison cron, l'injection d'outils DM, la normalisation d'ID de réaction et le secours de streaming.
- Rapports Discrawl : la recherche Feishu a retourné une discussion de mainteneur du 2026-05-28 autour de la disparition de la livraison `/compact` sur Feishu/WebChat, le routage de continuation de redémarrage de passerelle, les rapports récents de livraison de messages Feishu, un problème de stress 8-agent/7-canal-Feishu et une plainte d'utilisateur du 2026-05-25 liant un rapport de timeout de passerelle Feishu.
- Bonnes qualités : l'implémentation a des limites de source cohérentes pour la configuration, la politique, la résolution de compte, les actions de carte, la liaison de thread, le routage d'outils et la gestion de la sécurité ; la documentation appelle le secours manuel, les portées de plateforme, la politique de groupe et la rotation des secrets.
- Mauvaises qualités : les preuves récentes de problèmes/archive montrent la visibilité du statut, la livraison, la commande, l'injection d'outils et les bords rugueux de configuration ; Feishu a également assez de comportement d'approbation de plateforme et de division domestique/Lark pour que le support public puisse être fragile sans un runbook maintenu.
- Exclu de la qualité : présence ou absence de test unitaire, intégration, e2e, en direct et flux d'exécution réel ; ce sont des entrées de couverture uniquement.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture de test unitaire, intégration, e2e, en direct ou flux d'exécution réel comme entrée de notation.

## Score de Complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/feishu-qq-bot-wechat-yuanbao-zalo-zalo-personal-regional-channels.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de taxonomie pour la configuration du canal bot Feishu/Lark, le mode WebSocket par défaut, l'appairage DM, la livraison de messages, le document Feishu, la gestion des identifiants multi-comptes, la configuration AppID/AppSecret de la plateforme ouverte QQ, le chat privé C2C, l'activation de groupe, les messages médias enrichis, les commandes slash, les connexions de passerelle multi-comptes, le canal externe Tencent Yuanbao, la configuration AppKey/AppSecret, les DM, la stratégie de file d'attente sortante, le catalogue externe officiel côté noyau, le bot Zalo Bot Creator / Marketplace, le mode d'interrogation longue par défaut, le token de bot, le schéma de politique de groupe, le texte et les sondes de statut.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter une fiche de pointage Feishu/Lark en direct actuelle qui exécute la configuration, l'approbation de plateforme, la livraison WebSocket, la livraison webhook, l'appairage DM, les mentions de groupe, les rappels de carte, les médias et les appels d'outils.
- Maintenir la documentation Feishu alignée avec le comportement de configuration actuel pour l'enregistrement d'application QR, le secours manuel, la terminologie de plateforme Lark par rapport à Feishu et les portées requises.
- Fermer ou documenter explicitement les bords rugueux récents de livraison/statut/injection d'outils visibles dans gitcrawl et discrawl.

# Feishu

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/feishu.md` indique que Feishu/Lark est prêt pour la production pour les DM de bot et les chats de groupe, avec WebSocket par défaut et le mode webhook optionnel.
- `/Users/kevinlin/code/openclaw/docs/channels/feishu.md` documente `openclaw channels login --channel feishu`, la configuration manuelle de l'ID d'application/Secret d'application, la configuration de secours QR, le redémarrage de la passerelle, la politique DM, la politique de groupe, les exigences de mention, les restrictions d'expéditeur, les commandes courantes, les portées de plateforme requises, le dépannage, la rotation du secret d'application et la configuration multi-compte.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/feishu.md` identifie le paquet `@openclaw/feishu`, la route d'installation `npm; ClawHub`, et la surface `channels: feishu; contracts: tools; skills`.

### Source

- `/Users/kevinlin/code/openclaw/extensions/feishu/src/channel.ts`, `channel.runtime.ts`, `monitor.ts`, `monitor.startup.ts`, `monitor.transport.ts`, et `monitor.webhook-security.test.ts` ancrent l'enregistrement du canal, le démarrage, le transport et le comportement de sécurité webhook.
- `/Users/kevinlin/code/openclaw/extensions/feishu/src/setup-surface.ts`, `setup-core.ts`, `app-registration.ts`, `secret-input.ts`, `accounts.ts`, et `config-schema.ts` implémentent la configuration, l'entrée des identifiants, l'enregistrement de l'application, les comptes et la validation de la configuration.
- `/Users/kevinlin/code/openclaw/extensions/feishu/src/policy.ts`, `conversation-id.ts`, `session-conversation.ts`, `thread-bindings.ts`, `reply-dispatcher.ts`, et `send-target.ts` implémentent l'accès, la liaison conversation/session, le routage des threads et le ciblage des réponses.
- `/Users/kevinlin/code/openclaw/extensions/feishu/src/card-action.ts`, `card-ux-approval.ts`, `card-ux-launcher.ts`, `streaming-card.ts`, `reactions.ts`, `comment-handler.ts`, `directory.ts`, `docx.ts`, `bitable.ts`, `perm.ts`, `pins.ts`, et `dynamic-agent.ts` couvrent les surfaces Feishu plus riches.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/vitest/vitest.extension-feishu.config.ts` définit le projet de test Feishu dédié.
- `/Users/kevinlin/code/openclaw/extensions/feishu/src/monitor.webhook-e2e.test.ts`, `monitor.lifecycle.test.ts`, `monitor.bot-menu.test.ts`, `monitor.reaction.test.ts`, `monitor.comment.test.ts`, `reply-dispatcher.test.ts`, `subagent-hooks.test.ts`, `thread-bindings.test.ts`, et les fichiers de support de test du cycle de vie exercent le comportement du transport et du flux du canal.
- Aucun scénario actuel de plateforme Feishu/Lark en direct n'a été trouvé qui prouve l'ensemble du flux de configuration-à-message-à-outil par rapport à un locataire Feishu/Lark réel.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/feishu/src/config-schema.test.ts`, `setup-surface.test.ts`, `accounts.test.ts`, `policy.test.ts`, `conversation-id.test.ts`, `send.test.ts`, `outbound.test.ts`, `media.test.ts`, `tool-result.test.ts`, `streaming-card.test.ts`, `bot.card-action.test.ts`, `approval-auth.test.ts`, `security-audit.test.ts`, et les tests de document/wiki/drive couvrent le comportement ciblé.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Feishu webhook encrypt key card action group topic reply" --json --limit 6`
- `gitcrawl search openclaw/openclaw --query "Feishu" --json --limit 8`

Résultats :

- La requête spécifique à la fonctionnalité n'a retourné aucun résultat.
- La requête Feishu large a retourné des résultats de PR/issue ouverts incluant `#77882` outils bitable contrôlés par la configuration des outils, `#77982` contrats d'outil Lark non propagés, `#77709` `openclaw status --deep` omettant Feishu configuré/connecté, `#77653` normalisation de l'ID de message de réaction, `#82356` commandes slash livrées-false, `#77712` copie de canal non supporté d'aperçu de livraison cron, `#84095` outils Feishu non injectés dans les sessions DM, et `#74808` secours de streaming recherchable.

### Requêtes Discrawl

Requête :

- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 6 "Feishu QR setup manual App ID App Secret"`
- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "Feishu"`

Résultats :

- La requête de configuration QR/manuelle a retourné la PR `#65680` décrivant l'intégration Feishu rationalisée car la configuration manuelle de l'ID d'application/Secret d'application était sujette aux erreurs.
- La requête Feishu large a retourné une discussion du responsable du 2026-05-28 sur la disparition de la livraison `/compact` sur Feishu/WebChat, les rapports Clawsweeper impliquant la livraison Feishu et les problèmes de canal configuré, le stress de 8 agents/7 canaux Feishu, et un rapport d'utilisateur liant un problème de délai d'expiration de la passerelle Feishu.
