---
title: "Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux - Note de Maturité du Routage et de la Livraison des Conversations"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux - Note de Maturité du Routage et de la Livraison des Conversations

## Résumé

Cette note est la note de maturité normalisée active pour `Routage et Livraison des Conversations` sur la surface de canal `Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux`. Elle consolide les notes de preuve antérieures spécifiques aux canaux tout en préservant ces notes plus anciennes dans le répertoire d'inventaire pour les détails historiques.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Routage et Livraison des Conversations`
- Fusionnée à partir de : `Canaux de Bot`, `Canaux de Compte Personnel`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Configuration du canal bot Feishu/Lark : Configuration du canal bot Feishu/Lark via App ID/App Secret manuel ou enregistrement d'application QR
- Mode WebSocket par défaut : Mode WebSocket par défaut et mode webhook optionnel
- Appairage DM : Appairage DM, listes blanches, politique de groupe, portes de mention, remplacements par groupe et restrictions d'expéditeur
- Livraison de messages : Livraison de messages, réponses, cartes de streaming, réactions, commentaires, menus de bot et actions de carte
- Document Feishu : Document Feishu, wiki, lecteur, bitable et outils d'agent dynamique
- Gestion des identifiants multi-comptes : Gestion des identifiants multi-comptes et dépannage pour les déploiements régionaux Feishu/Lark
- Configuration AppID/AppSecret de la Plateforme Ouverte QQ : Configuration AppID/AppSecret de la Plateforme Ouverte QQ et gestion des comptes par défaut env/config
- Chat privé C2C : Chat privé C2C, messages de groupe, messages de canal de guilde et analyse des cibles
- Activation de groupe : Activation de groupe, portes de mention, historique de groupe, politiques d'outils et listes blanches d'expéditeurs
- Messages multimédias enrichis : Médias entrants et sortants incluant images, voix, vidéo, fichiers, STT/TTS et envois de voix natifs
- Commandes slash : Commandes slash, boutons d'approbation, outils de rappel/canal et enregistrement de commandes de framework
- Connexions de passerelle multi-comptes : Connexions de passerelle multi-comptes, cache de jetons, sauvegardes d'identifiants, diagnostics et comportement de reconnexion
- Canal externe Tencent Yuanbao : Canal externe Tencent Yuanbao openclaw-plugin-yuanbao
- Configuration AppKey/AppSecret : Configuration AppKey/AppSecret, assistant de connexion, config multi-comptes et routage de compte par défaut
- DMs : DMs, groupes, exigences de mention, mode réponse, contexte d'historique de groupe, menus de commandes slash et réponses de secours
- Stratégie de file d'attente sortante : Stratégie de file d'attente sortante, réglage de fusion de texte, caractères max, plafonds multimédias, comportement de débordement et streaming au niveau des blocs
- Catalogue externe officiel côté noyau : Catalogue externe officiel côté noyau, métadonnées d'installation, alias, descriptions d'assistant et contrats de catalogue de canaux
- Bot Zalo Bot Creator / Marketplace : Canal DM du bot Zalo Bot Creator / Marketplace
- Mode d'interrogation longue par défaut : Mode d'interrogation longue par défaut et mode webhook HTTPS optionnel
- Jeton de bot : Jeton de bot, fichier de jeton, multi-comptes, appairage DM et comportement de liste blanche
- Schéma de politique de groupe : Schéma de politique de groupe et portes de groupe fermées même lorsque les groupes Marketplace ne sont pas utilisables
- Texte : Texte, espaces réservés multimédias, chunking sortant, déduplication de relecture, limitation de débit, secrets webhook et support proxy
- Sondes d'état : Sondes d'état et dépannage pour les problèmes de jeton/config/webhook
- Messagerie personnelle WeChat/Weixin : Messagerie personnelle WeChat/Weixin via package externe @tencent-weixin/openclaw-weixin
- Installation du plugin : Installation du plugin, activation, compatibilité, connexion QR, jetons de compte enregistrés et identifiant de canal openclaw-weixin
- Appairage de message direct : Appairage de message direct et isolation de session par compte
- Métadonnées du catalogue côté noyau : Métadonnées du catalogue côté noyau, alias, plans d'installation, marqueurs de confiance de plugin, indices de statut/réparation, redirections de docs et découverte de canal
- Comportement du processus sidecar/helper externe : Comportement du processus sidecar/helper externe et protections de nettoyage de processus obsolètes
- Plugin de canal zalouser : Plugin de canal zalouser pour l'automatisation du Compte Personnel Zalo via zca-js natif
- Connexion QR : Connexion QR, profils enregistrés, sélection multi-comptes/profils et runtime local de passerelle
- Appairage DM : Appairage DM, politique de groupe, gating de groupe, pairs de répertoire et routage d'expéditeur/session
- Envoi de message : Envoi de message, médias image/lien/document, réactions, statut, outils amis/groupes/moi et normalisation de style de texte
- Vérifications Doctor/statut pour la disponibilité du runtime : Vérifications Doctor/statut pour la disponibilité du runtime et la santé du profil/session
- Risque de compte non officiel explicite : Risque de compte non officiel explicite et protections de l'opérateur
- Configuration AppID/AppSecret de la Plateforme Ouverte QQ et : Couvre la configuration AppID/AppSecret de la Plateforme Ouverte QQ et le comportement de gestion des comptes par défaut env/config.
- Chat privé C2C : Couvre le chat privé C2C, les messages de groupe, les messages de canal de guilde et le comportement d'analyse des cibles.
- Activation de groupe : Couvre le comportement d'activation de groupe, de portes de mention, d'historique de groupe, de politiques d'outils et de listes blanches d'expéditeurs.
- Médias entrants et sortants enrichis incluant : Couvre le comportement des médias entrants et sortants enrichis incluant images, voix, vidéo, fichiers, STT/TTS et envois de voix natifs.
- Commandes slash : Couvre le comportement des commandes slash, des boutons d'approbation, des outils de rappel/canal et de l'enregistrement de commandes de framework.
- Connexions de passerelle multi-comptes : Couvre le comportement des connexions de passerelle multi-comptes, du cache de jetons, des sauvegardes d'identifiants, des diagnostics et du comportement de reconnexion.
- Canal externe Tencent Yuanbao `openclaw-plugin-yuanbao` : Portée de preuve pour le canal externe Tencent Yuanbao `openclaw-plugin-yuanbao`.
- Configuration AppKey/AppSecret : Couvre le comportement de configuration AppKey/AppSecret, d'assistant de connexion, de config multi-comptes et de routage de compte par défaut.
- DMs : Couvre le comportement des DMs, des groupes, des exigences de mention, du mode réponse, du contexte d'historique de groupe, des menus de commandes slash et des réponses de secours.
- Stratégie de file d'attente sortante : Couvre le comportement de la stratégie de file d'attente sortante, du réglage de fusion de texte, des caractères max, des plafonds multimédias, du comportement de débordement et du streaming au niveau des blocs.
- Catalogue externe officiel côté noyau : Couvre le comportement du catalogue externe officiel côté noyau, des métadonnées d'installation, des alias, des descriptions d'assistant et des contrats de catalogue de canaux.
- Bot Zalo Bot Creator / Marketplace : Couvre le comportement du canal DM du bot Zalo Bot Creator / Marketplace.
- Mode d'interrogation longue par défaut et webhook HTTPS optionnel : Couvre le comportement du mode d'interrogation longue par défaut et du mode webhook HTTPS optionnel.
- Jeton de bot : Couvre le comportement du jeton de bot, du fichier de jeton, des multi-comptes, de l'appairage DM et de la liste blanche.
- Schéma de politique de groupe et portes de groupe fermées : Couvre le comportement du schéma de politique de groupe et des portes de groupe fermées même lorsque les groupes Marketplace ne sont pas utilisables.
- Texte : Couvre le comportement du texte, des espaces réservés multimédias, du chunking sortant, de la déduplication de relecture, de la limitation de débit, des secrets webhook et du support proxy.
- Sondes d'état et dépannage pour les problèmes de jeton/config/webhook : Portée de preuve pour les sondes d'état et le dépannage pour les problèmes de jeton/config/webhook.
- Plugin de canal `zalouser` pour Zalo Personnel : Couvre le comportement du plugin de canal `zalouser` pour l'automatisation du Compte Personnel Zalo via `zca-js` natif.
- Connexion QR : Couvre le comportement de connexion QR, des profils enregistrés, de la sélection multi-comptes/profils et du runtime local de passerelle.
- Appairage DM : Couvre le comportement de l'appairage DM, de la politique de groupe, du gating de groupe, des pairs de répertoire et du routage d'expéditeur/session.
- Envoi de message : Couvre le comportement de l'envoi de message, des médias image/lien/document, des réactions, du statut, des outils amis/groupes/moi et de la normalisation de style de texte.
- Vérifications Doctor/statut pour la disponibilité du runtime et : Couvre le comportement des vérifications Doctor/statut pour la disponibilité du runtime et la santé du profil/session.
- Risque de compte non officiel explicite et protections de l'opérateur : Portée de preuve pour le risque de compte non officiel explicite et les protections de l'opérateur.

## Fonctionnalités

- Routage et Livraison des Conversations : Portée de preuve pour le Routage et la Livraison des Conversations.

## Preuve

- Les notes sources historiques restent dans le répertoire d'inventaire de cette surface et ont été utilisées comme preuve source pour la ligne de taxonomie normalisée.
