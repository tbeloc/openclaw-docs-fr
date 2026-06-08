---
title: "Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux - Note de maturité du canal QQ Bot"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux - Note de maturité du canal QQ Bot

## Résumé

QQ Bot est une implémentation de canal officiel substantielle avec documentation pour la configuration des identifiants, C2C, groupes, canaux de guilde, médias, voix, commandes, cibles, comportement multi-compte et identifiants SecretRef. La source est large et les tests couvrent la connexion de passerelle, le traitement entrant/sortant, l'authentification des commandes, les médias, l'accès, la configuration et le comportement d'approbation. Le canal présente toujours une dégradation active de la qualité en raison de problèmes ouverts concernant la normalisation des cibles, les chemins de stockage, la préservation de la reconnexion/session, le nettoyage des médias obsolètes, l'isolation des identifiants et le comportement de délai d'expiration du modèle local.

## Portée des catégories

- Configuration AppID/AppSecret de la plateforme ouverte QQ et gestion des comptes par défaut via env/config.
- Chat privé C2C, messages de groupe, messages de canal de guilde et analyse des cibles.
- Activation de groupe, portes de mention, historique de groupe, politiques d'outils et listes blanches d'expéditeurs.
- Médias enrichis entrants et sortants incluant images, voix, vidéo, fichiers, STT/TTS et envois de voix natifs.
- Commandes slash, boutons d'approbation, outils de rappel/canal et enregistrement de commandes de framework.
- Connexions de passerelle multi-compte, cache de jetons, sauvegardes d'identifiants, diagnostics et comportement de reconnexion.

## Fonctionnalités

- Configuration AppID/AppSecret de la plateforme ouverte QQ : Configuration AppID/AppSecret de la plateforme ouverte QQ et gestion des comptes par défaut via env/config
- Chat privé C2C : Chat privé C2C, messages de groupe, messages de canal de guilde et analyse des cibles
- Activation de groupe : Activation de groupe, portes de mention, historique de groupe, politiques d'outils et listes blanches d'expéditeurs
- Messages médias enrichis : Médias enrichis entrants et sortants incluant images, voix, vidéo, fichiers, STT/TTS et envois de voix natifs
- Commandes slash : Commandes slash, boutons d'approbation, outils de rappel/canal et enregistrement de commandes de framework
- Connexions de passerelle multi-compte : Connexions de passerelle multi-compte, cache de jetons, sauvegardes d'identifiants, diagnostics et comportement de reconnexion

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : l'extension QQ Bot dispose de tests larges et ciblés couvrant la connexion, le pipeline entrant, les portes de groupe, la distribution sortante, l'authentification des commandes, la gestion des médias, la configuration, les identifiants, le comportement d'approbation et l'adaptation des messages de canal.
- Signaux négatifs : aucun scénario actuel de plateforme ouverte QQ n'a été trouvé qui crée un bot, démarre la WebSocket de passerelle, exerce C2C, groupe, guilde, commandes slash, approbations, médias, voix, reconnexion/reprise et comportement multi-compte par rapport au service en amont.
- Lacunes d'intégration : la preuve en direct est mince pour l'actualisation des jetons en amont, la sémantique officielle de reconnexion de passerelle, les médias volumineux, le routage groupe/guilde, les réponses lentes du modèle local et l'UX réel du client QQ.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel dans le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : une large recherche `QQBot` a retourné des rapports ouverts concernant la normalisation des cibles cron, la gestion des chemins, les messages d'erreur exploitables, l'incohérence des cibles de livraison, l'interruption du modèle local/réseau, l'isolation de la sauvegarde des identifiants, la reprise de reconnexion et le nettoyage des médias obsolètes.
- Rapports Discrawl : la recherche QQBot a retourné une discussion de maintenant sur les correctifs de délai d'expiration QQBot, la livraison de progression de streaming partiel, la confusion d'installation officielle qui a exposé un outil `qqbot` inattendu et les préoccupations de régression canal/plugin de fenêtre de version.
- Bonnes qualités : la séparation des sources est forte, avec des couches moteur/pont pour la passerelle, les commandes, la messagerie, les médias, la configuration, l'accès, l'approbation, la configuration et les outils ; la documentation est explicite sur les OpenID spécifiques au compte, les formats de cible, la gestion de SecretRef, la politique de groupe et les réactions/threads non pris en charge.
- Mauvaises qualités : les archives de support et de problèmes montrent une confusion récurrente de routage, délai d'expiration, chemin, stockage et mise à niveau ; l'API en amont QQ Bot a plusieurs surfaces de chat et des ID spécifiques au compte, ce qui augmente le risque d'erreur opérateur.
- Exclu de la qualité : présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel ; ce sont uniquement des entrées de couverture.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score d'exhaustivité

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/feishu-qq-bot-wechat-yuanbao-zalo-zalo-personal-regional-channels.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration AppID/AppSecret de la plateforme ouverte QQ, le chat privé C2C, l'activation de groupe, les messages médias enrichis, les commandes slash, les connexions de passerelle multi-compte.
- Signaux négatifs : la note archivée a précédé la notation d'exhaustivité de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un scénario QQ Bot en direct qui couvre l'enregistrement d'application, C2C, groupe, canal de guilde, commande slash, approbation, médias enrichis, voix, délai d'expiration, reconnexion/reprise et comportement multi-compte.
- Continuer à renforcer les diagnostics orientés opérateur pour le format de cible, la configuration AppID/AppSecret, SecretRef, les chemins de stockage, les délais d'expiration du modèle local et les états de reconnexion de passerelle en amont.
- Clarifier le nettoyage des médias obsolètes et l'isolation de la sauvegarde des identifiants dans la documentation ou l'état d'exécution.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/qqbot.md` décrit QQ Bot comme un plugin téléchargeable utilisant la passerelle WebSocket officielle QQ Bot, prenant en charge le chat privé C2C, les messages @groupe, les messages de canal de guilde et les médias enrichis, tout en déclarant que les réactions et les threads ne sont pas pris en charge.
- `/Users/kevinlin/code/openclaw/docs/channels/qqbot.md` documente l'installation, la configuration de la plateforme ouverte, le format de jeton AppID/AppSecret, SecretRef, la configuration multi-compte, la politique de groupe, la voix STT/TTS, les formats de cible et les commandes slash.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/qqbot.md` identifie le paquet `@openclaw/qqbot`, la route d'installation `npm; ClawHub` et la surface `channels: qqbot; contracts: tools; skills`.

### Source

- `/Users/kevinlin/code/openclaw/extensions/qqbot/src/channel.ts`, `channel.setup.ts`, `config-schema.ts`, `secret-contract.ts`, `exec-approvals.ts` et `qqbot-test-support.ts` ancrent l'entrée de canal, la configuration, la configuration, le secret et les surfaces d'approbation.
- `/Users/kevinlin/code/openclaw/extensions/qqbot/src/engine/gateway/*` implémente la connexion WebSocket, la distribution d'événements, les étapes entrantes, la mise en file d'attente, la reconnexion, la conservation de la saisie, le délai d'expiration de la réponse et la distribution sortante.
- `/Users/kevinlin/code/openclaw/extensions/qqbot/src/engine/messaging/*`, `engine/api/*`, `engine/commands/*`, `engine/group/*`, `engine/access/*`, `engine/config/*` et `engine/tools/*` implémentent l'analyse des cibles, les médias, les appels API QQ, les commandes slash, la politique de groupe, les listes blanches, la configuration, les outils de rappel/canal et le formatage.
- `/Users/kevinlin/code/openclaw/extensions/qqbot/src/bridge/*` adapte le moteur à l'exécution du plugin, la configuration, l'entrée de canal, l'enregistrement des commandes, l'exécution d'approbation et la surface SDK.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qqbot/src/channel.message-adapter.test.ts`, `exec-approvals.test.ts`, `bridge/commands/framework-registration.test.ts`, `bridge/commands/framework-context-adapter.test.ts`, `engine/gateway/outbound-dispatch.test.ts`, `engine/gateway/inbound-pipeline.self-echo.test.ts`, `engine/gateway/interaction-handler.test.ts`, `engine/commands/slash-command-handler.test.ts` et `engine/api/media-chunked.test.ts` exercent le comportement du flux de canal via la surface du plugin.
- Aucun scénario WebSocket actuel de plateforme ouverte QQ n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/qqbot/src/config.test.ts`, `secret-contract.test.ts`, `engine/config/*.test.ts`, `engine/access/*.test.ts`, `engine/group/*.test.ts`, `engine/gateway/stages/*.test.ts`, `engine/utils/*.test.ts`, `engine/api/*.test.ts`, `engine/approval/index.test.ts` et `engine/ref/*.test.ts` couvrent la logique ciblée pour la configuration, les identifiants, la correspondance, les groupes, les étapes de pipeline, les médias, le comportement des jetons/API, les approbations et les références.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "QQBot media OPENCLAW_HOME slash command approval timeout" --json --limit 6`
- `gitcrawl search openclaw/openclaw --query "QQBot" --json --limit 8`

Résultats :

- La requête spécifique à la fonctionnalité n'a retourné aucun résultat.
- La large requête QQBot a retourné des résultats ouverts incluant `#78916` normalisation de cible de livraison cron, `#39461` problème de chemin/répertoire de données, `#65868` demande de message d'erreur exploitable, `#78893` incohérence de cible cron, `#87262` interruption du modèle local/réseau, `#84314` isolation de sauvegarde d'identifiants, `#78898` préservation de session de reconnexion et `#78895` nettoyage des médias obsolètes.

### Requêtes Discrawl

Requête :

- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 6 "QQBot OPENCLAW_HOME media slash command approval"`
- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "QQBot"`

Résultats :

- La requête spécifique à la fonctionnalité n'a retourné aucun résultat.
- La large requête QQBot a retourné une mention Clawsweeper du 2026-05-27 d'un problème qqbot/ollama, une mise à jour du maintenant du 2026-05-25 citant un correctif de délai d'expiration QQBot, une demande d'examen du 2026-05-22 pour la livraison de progression de streaming partiel QQBot et des notes de fenêtre de version du 2026-05-14 concernant un outil `qqbot` inattendu après l'installation officielle.
