---
title: "Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de Maturité Accès et Identité"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de Maturité Accès et Identité

## Résumé

Cette note est la note de maturité normalisée active pour `Accès et Identité` sur la surface de canal `Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat`. Elle consolide les notes de preuve antérieures spécifiques aux canaux tout en préservant ces notes plus anciennes dans le répertoire d'inventaire pour les détails historiques.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Accès et Identité`
- Fusionnée à partir de : `Chat d'Espace de Travail`, `Messagerie Webhook`, `Chat IRC`, `Messagerie Décentralisée`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Configuration du compte bot Mattermost : Configuration du compte bot Mattermost, configuration du token bot/URL de base, configuration multi-compte et empaquetage de plugin
- Surveillance inbound WebSocket : Surveillance inbound WebSocket, routage DM/canal, contrôle d'accès, appairage, mention gating et threading de session
- Livraison outbound : Livraison outbound, streaming d'aperçu de brouillon, réactions, boutons interactifs, commandes slash, recherche d'annuaire, diagnostics et comportement du docteur
- Configuration du webhook LINE Messaging API : Configuration du webhook LINE Messaging API, gestion du token d'accès au canal/secret du canal, routage multi-compte et installation de plugin
- Événements webhook inbound signés : Événements webhook inbound signés, accusé de réception immédiat, autorisation DM/groupe, appairage, clés de groupe, contexte de message, déduplication de renvoi et livraison de réponse durable
- Charges utiles LINE enrichies : Charges utiles LINE enrichies, réponses rapides, emplacements, cartes Flex/template, médias image/audio/vidéo outbound, menus enrichis, statut et dépannage
- Installation du bot Nextcloud Talk : Installation du bot Nextcloud Talk, secret partagé/identifiants API, route webhook, paramètres de salle, secrets sauvegardés sur fichier et configuration du runtime du plugin
- Ingress webhook : Ingress webhook, validation de signature/secret, recherche salle-vs-DM, politique DM/groupe, appairage, mention gating, protection contre la relecture et métadonnées de salle
- Markdown/texte outbound : Markdown/texte outbound, secours média URL, réactions/actions de message, threading, statut, docteur, configuration et dépannage
- Configuration du webhook entrant/sortant Synology Chat : Configuration du webhook entrant/sortant Synology Chat, configuration du token/URL entrant, variables env, surface de configuration et configuration du routage multi-compte
- Vérification du token webhook : Vérification du token webhook, politique DM, ID utilisateur autorisés, appairage, limitation de débit, verrouillage de token invalide, clés de session, contexte inbound de message direct et sémantique ACK webhook
- Texte outbound : Texte outbound et livraison de médias URL, gardes SSRF de réseau privé, audit de sécurité, configuration/statut et dépannage
- Configuration du serveur IRC/nick/TLS/NickServ : Configuration du serveur IRC/nick/TLS/NickServ, chargement env/config, résolution de compte et configuration du runtime du plugin
- Réception/envoi IRC brut : Réception/envoi IRC brut, messages directs, messages de canal, normalisation de l'identité de l'expéditeur, gestion des caractères de contrôle, politique d'accès, mention gating et politique outils-par-expéditeur
- Sonde/statut : Sonde/statut, normalisation du texte outbound, cycle de vie reconnexion/surveillance et valeurs par défaut de sécurité autour de l'egress IRC direct
- Configuration du compte bot Twitch : Configuration du compte bot Twitch, tokens d'accès/actualisation OAuth, ID client/secret, configuration de jointure de canal, configuration multi-compte et comportement d'installation groupée/fournie
- Cycle de vie du moniteur/client IRC Twitch : Cycle de vie du moniteur/client IRC Twitch, actualisation du token, statut/sonde, contrôle d'accès par ID utilisateur/rôles, requireMention et livraison de chat outbound
- Action d'envoi de l'outil de message : Action d'envoi de l'outil de message, surface d'action orientée modération, sécurité/ops et dépannage
- Configuration de clé Nostr : Configuration de clé Nostr, configuration de relais, métadonnées de profil, gestion de clé privée, installation de plugin et statut de configuration
- Réception/envoi DM chiffré NIP-04 : Réception/envoi DM chiffré NIP-04, vérification de signature d'événement, politique d'expéditeur, bus de relais, suivi des doublons/vus, test de relais local et stockage d'état
- Importation/publication de profil : Importation/publication de profil, sécurité URL de relais, métriques, routage de session et limitations autour des médias et des protocoles DM chiffrés plus récents
- Configuration de l'URL/code du navire Tlon/Urbit : Configuration de l'URL/code du navire Tlon/Urbit, opt-in de réseau privé, configuration du canal de groupe, navire propriétaire, listes blanches, acceptation automatique et comportement de configuration/docteur
- Auth/session API Urbit : Auth/session API Urbit, moniteur SSE, découverte DM/groupe, gestion des mentions de groupe, réponses de thread, approbations, suivi des messages traités et assistants de paramètres
- Conversion de texte enrichi : Conversion de texte enrichi, téléchargement d'image via stockage Tlon/Memex, cibles de livraison, compétence Tlon groupée et dépannage de sécurité
- Configuration du webhook entrant/sortant Synology Chat : Couvre la configuration du webhook entrant/sortant Synology Chat, configuration du token/URL entrant, variables env, surface de configuration et comportement de configuration du routage multi-compte.
- Vérification du token webhook : Couvre la vérification du token webhook, politique DM, ID utilisateur autorisés, appairage, limitation de débit, verrouillage de token invalide, clés de session, contexte inbound de message direct et comportement de sémantique ACK webhook.
- Livraison de texte outbound et médias URL : Couvre la livraison de texte outbound et médias URL, gardes SSRF de réseau privé, audit de sécurité, configuration/statut et comportement de dépannage.
- Configuration de l'URL/code du navire Tlon/Urbit : Couvre la configuration de l'URL/code du navire Tlon/Urbit, opt-in de réseau privé, configuration du canal de groupe, navire propriétaire, listes blanches, acceptation automatique et comportement de configuration/docteur.
- Auth/session API Urbit : Couvre l'auth/session API Urbit, moniteur SSE, découverte DM/groupe, gestion des mentions de groupe, réponses de thread, approbations, suivi des messages traités et comportement des assistants de paramètres.
- Conversion de texte enrichi : Couvre la conversion de texte enrichi, téléchargement d'image via stockage Tlon/Memex, cibles de livraison, compétence Tlon groupée et comportement de dépannage de sécurité.

## Fonctionnalités

- Accès et Identité : Portée de preuve pour Accès et Identité.

## Preuve

- Les notes sources historiques restent dans ce répertoire d'inventaire de surface et ont été utilisées comme preuve source pour la ligne de taxonomie normalisée.
