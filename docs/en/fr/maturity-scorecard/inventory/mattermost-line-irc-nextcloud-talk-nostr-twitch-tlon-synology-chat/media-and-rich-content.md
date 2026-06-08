---
title: "Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de Maturité Média et Contenu Enrichi"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat - Note de Maturité Média et Contenu Enrichi

## Résumé

Cette note est la note de maturité normalisée active pour `Média et Contenu Enrichi` sur la surface de canal `Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat`. Elle consolide les notes de preuve antérieures spécifiques aux canaux tout en préservant ces notes plus anciennes dans le répertoire d'inventaire pour les détails historiques.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Média et Contenu Enrichi`
- Fusionnée à partir de : `Messagerie par Webhook`, `Messagerie Décentralisée`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Configuration du webhook de l'API LINE Messaging : configuration du webhook de l'API LINE Messaging, gestion du jeton d'accès au canal/secret du canal, routage multi-compte et installation du plugin
- Événements webhook entrants signés : événements webhook entrants signés, accusé de réception immédiat, autorisation DM/groupe, appairage, clés de groupe, contexte du message, déduplications de renvoi et livraison de réponse durable
- Charges utiles LINE enrichies : charges utiles LINE enrichies, réponses rapides, emplacements, cartes Flex/modèles, médias image/audio/vidéo sortants, menus enrichis, statut et dépannage
- Installation du bot Nextcloud Talk : installation du bot Nextcloud Talk, secret partagé/identifiants API, route webhook, paramètres de salle, secrets sauvegardés sur fichier et configuration du runtime du plugin
- Entrée webhook : entrée webhook, validation de signature/secret, recherche salle-vs-DM, politique DM/groupe, appairage, mention gating, protection contre la relecture et métadonnées de salle
- Markdown/texte sortant : markdown/texte sortant, secours aux médias URL, réactions/actions de message, threading, statut, doctor, configuration et dépannage
- Configuration du webhook entrant/sortant Synology Chat : configuration du webhook entrant/sortant Synology Chat, configuration du jeton/URL entrant, variables env, surface de configuration et configuration du routage multi-compte
- Vérification du jeton webhook : vérification du jeton webhook, politique DM, ID utilisateur autorisés, appairage, limitation de débit, verrouillage de jeton invalide, clés de session, contexte entrant de message direct et sémantique ACK webhook
- Texte sortant : texte sortant et livraison de médias URL, gardes SSRF de réseau privé, audit de sécurité, configuration/statut et dépannage
- Configuration de clé Nostr : configuration de clé Nostr, configuration de relais, métadonnées de profil, gestion de clé privée, installation du plugin et statut de configuration
- Réception/envoi DM chiffré NIP-04 : réception/envoi DM chiffré NIP-04, vérification de signature d'événement, politique d'expéditeur, bus de relais, suivi des doublons/vus, test de relais local et stockage d'état
- Importation/publication de profil : importation/publication de profil, sécurité des URL de relais, métriques, routage de session et limitations autour des médias et des protocoles DM chiffrés plus récents
- Configuration d'URL/code de navire Tlon/Urbit : configuration d'URL/code de navire Tlon/Urbit, opt-in de réseau privé, configuration de canal de groupe, navire propriétaire, listes blanches, acceptation automatique et comportement de configuration/doctor
- Auth/session API Urbit : auth/session API Urbit, moniteur SSE, découverte DM/groupe, gestion des mentions de groupe, réponses de thread, approbations, suivi des messages traités et assistants de paramètres
- Conversion de texte enrichi : conversion de texte enrichi, téléchargement d'image via stockage Tlon/Memex, cibles de livraison, compétence Tlon groupée et dépannage de sécurité
- Configuration d'URL/code de navire Tlon/Urbit : couvre la configuration d'URL/code de navire Tlon/Urbit, opt-in de réseau privé, configuration de canal de groupe, navire propriétaire, listes blanches, acceptation automatique et comportement de configuration/doctor.
- Auth/session API Urbit : couvre l'auth/session API Urbit, moniteur SSE, découverte DM/groupe, gestion des mentions de groupe, réponses de thread, approbations, suivi des messages traités et comportement des assistants de paramètres.
- Conversion de texte enrichi : couvre la conversion de texte enrichi, téléchargement d'image via stockage Tlon/Memex, cibles de livraison, compétence Tlon groupée et comportement de dépannage de sécurité.

## Fonctionnalités

- Média et Contenu Enrichi : portée de preuve pour Média et Contenu Enrichi.

## Preuve

- Les notes sources historiques restent dans ce répertoire d'inventaire de surface et ont été utilisées comme preuve source pour la ligne de taxonomie normalisée.
