---
title: "Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux - Note de Maturité d'Accès et d'Identité"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux - Note de Maturité d'Accès et d'Identité

## Résumé

Cette note est la note de maturité normalisée active pour `Accès et Identité` sur la surface de canal `Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux`. Elle consolide les notes de preuve antérieures spécifiques aux canaux tout en préservant ces notes plus anciennes dans le répertoire d'inventaire pour les détails historiques.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Accès et Identité`
- Fusionnée à partir de : `Canaux Bot`, `Canaux de Compte Personnel`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Configuration du canal bot Feishu/Lark : Configuration du canal bot Feishu/Lark via App ID/App Secret manuel ou enregistrement d'application QR
- Mode WebSocket par défaut : Mode WebSocket par défaut et mode webhook optionnel
- Appairage DM : Appairage DM, listes blanches, politique de groupe, portes de mention, remplacements par groupe et restrictions d'expéditeur
- Livraison de messages : Livraison de messages, réponses, cartes de streaming, réactions, commentaires, menus bot et actions de carte
- Document Feishu : Document Feishu, wiki, lecteur, bitable et outils d'agent dynamique
- Gestion des identifiants multi-comptes : Gestion des identifiants multi-comptes et dépannage pour les déploiements régionaux Feishu/Lark
- Configuration AppID/AppSecret de QQ Open Platform : Configuration AppID/AppSecret de QQ Open Platform et gestion des comptes par défaut env/config
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
- Bot Zalo Bot Creator / Marketplace : Bot Zalo Bot Creator / Marketplace canal DM
- Mode d'interrogation longue par défaut : Mode d'interrogation longue par défaut et mode webhook HTTPS optionnel
- Jeton bot : Jeton bot, fichier de jeton, multi-comptes, appairage DM et comportement de liste blanche
- Schéma de politique de groupe : Schéma de politique de groupe et portes de groupe fermées par défaut même où les groupes Marketplace ne sont pas utilisables
- Texte : Texte, espaces réservés multimédias, chunking sortant, déduplication de relecture, limitation de débit, secrets webhook et support proxy
- Sondes d'état : Sondes d'état et dépannage pour les problèmes de jeton/config/webhook
- Messagerie personnelle WeChat/Weixin : Messagerie personnelle WeChat/Weixin via package externe @tencent-weixin/openclaw-weixin
- Installation du plugin : Installation du plugin, activation, compatibilité, connexion QR, jetons de compte enregistrés et identifiant de canal openclaw-weixin
- Appairage de message direct : Appairage de message direct et isolation de session par compte
- Métadonnées du catalogue côté noyau : Métadonnées du catalogue côté noyau, alias, plans d'installation, marqueurs de confiance de plugin, indices de statut/réparation, redirections de docs et découverte de canaux
- Comportement du processus sidecar/helper externe : Comportement du processus sidecar/helper externe et protections de nettoyage de processus obsolètes
- Plugin de canal zalouser : Plugin de canal zalouser pour l'automatisation du compte personnel Zalo via zca-js natif
- Connexion QR : Connexion QR, profils enregistrés, sélection multi-comptes/profils et runtime local de passerelle
- Appairage DM : Appairage DM, politique de groupe, gating de groupe, pairs de répertoire et routage d'expéditeur/session
- Envoi de message : Envoi de message, médias image/lien/document, réactions, statut, outils amis/groupes/moi et normalisation de style de texte
- Vérifications Doctor/statut pour la disponibilité du runtime : Vérifications Doctor/statut pour la disponibilité du runtime et santé du profil/session
- Risque de compte non officiel explicite : Risque de compte non officiel explicite et protections de l'opérateur
- Configuration AppID/AppSecret de QQ Open Platform et : Couvre la configuration AppID/AppSecret de QQ Open Platform et le comportement de gestion des comptes par défaut env/config.
- Chat privé C2C : Couvre le chat privé C2C, les messages de groupe, les messages de canal de guilde et le comportement d'analyse des cibles.
- Activation de groupe : Couvre l'activation de groupe, les portes de mention, l'historique de groupe, les politiques d'outils et le comportement des listes blanches d'expéditeurs.
- Médias multimédias enrichis entrants et sortants incluant : Couvre les médias multimédias enrichis entrants et sortants incluant images, voix, vidéo, fichiers, STT/TTS et le comportement des envois de voix natifs.
- Commandes slash : Couvre les commandes slash, les boutons d'approbation, les outils de rappel/canal et le comportement d'enregistrement de commandes de framework.
- Connexions de passerelle multi-comptes : Couvre les connexions de passerelle multi-comptes, le cache de jetons, les sauvegardes d'identifiants, les diagnostics et le comportement de reconnexion.
- Canal externe Tencent Yuanbao `openclaw-plugin-yuanbao` : Portée de preuve pour le canal externe Tencent Yuanbao `openclaw-plugin-yuanbao`.
- Configuration AppKey/AppSecret : Couvre la configuration AppKey/AppSecret, l'assistant de connexion, la config multi-comptes et le comportement de routage de compte par défaut.
- DMs : Couvre les DMs, les groupes, les exigences de mention, le mode réponse, le contexte d'historique de groupe, les menus de commandes slash et le comportement des réponses de secours.
- Stratégie de file d'attente sortante : Couvre la stratégie de file d'attente sortante, le réglage de fusion de texte, les caractères max, les plafonds multimédias, le comportement de débordement et le streaming au niveau des blocs.
- Catalogue externe officiel côté noyau : Couvre le catalogue externe officiel côté noyau, les métadonnées d'installation, les alias, les descriptions d'assistant et le comportement des contrats de catalogue de canaux.
- Plugin de canal `zalouser` pour Zalo Personnel : Couvre le plugin de canal `zalouser` pour l'automatisation du compte personnel Zalo via le comportement natif `zca-js`.
- Connexion QR : Couvre la connexion QR, les profils enregistrés, la sélection multi-comptes/profils et le comportement du runtime local de passerelle.
- Appairage DM : Couvre l'appairage DM, la politique de groupe, le gating de groupe, les pairs de répertoire et le comportement de routage d'expéditeur/session.
- Envoi de message : Couvre l'envoi de message, les médias image/lien/document, les réactions, le statut, les outils amis/groupes/moi et le comportement de normalisation de style de texte.
- Vérifications Doctor/statut pour la disponibilité du runtime et : Couvre les vérifications Doctor/statut pour la disponibilité du runtime et le comportement de santé du profil/session.
- Risque de compte non officiel explicite et protections de l'opérateur : Portée de preuve pour le risque de compte non officiel explicite et les protections de l'opérateur.

## Fonctionnalités

- Accès et Identité : Portée de preuve pour Accès et Identité.

## Preuve

- Les notes sources historiques restent dans le répertoire d'inventaire de cette surface et ont été utilisées comme preuve source pour la ligne de taxonomie normalisée.
