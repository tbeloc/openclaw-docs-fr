---
read_when:
  - 开发语音唤醒或按键通话路径
summary: Mac 应用中的语音唤醒和按键通话模式及路由详情
title: 语音唤醒
x-i18n:
  generated_at: "2026-02-03T10:08:23Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: f6440bb89f349ba5c1c9aacffe95e568681beb9899ca736dedfe2f4a366cb5e4
  source_path: platforms/mac/voicewake.md
  workflow: 15
---

# Activation vocale et appel par touche

## Modes

- **Mode mot de réveil** (par défaut) : Reconnaissance vocale résidente attendant un mot déclencheur (`swabbleTriggerWords`). À la correspondance, commence la capture, affiche une fenêtre flottante avec du texte partiel, et envoie automatiquement après le silence.
- **Appel par touche (maintien de la touche Option droite)** : Maintenir la touche Option droite démarre immédiatement la capture — aucun mot de réveil requis. Affiche la fenêtre flottante pendant le maintien ; après relâchement, attend un court délai avant transmission finale, vous permettant d'ajuster le texte.

## Comportement à l'exécution (mot de réveil)

- Le moteur de reconnaissance vocale se trouve dans `VoiceWakeRuntime`.
- Se déclenche uniquement lorsqu'il y a une **pause notable** (intervalle d'environ 0,55 seconde) entre le mot de réveil et le mot suivant. La fenêtre flottante/le son peut s'activer pendant la pause avant le début de la commande.
- Fenêtre de silence : 2,0 secondes pour la parole fluide, 5,0 secondes si seul le mot de réveil est entendu.
- Arrêt dur : 120 secondes, pour éviter que la session ne s'échappe.
- Dédoublonnage entre sessions : 350 millisecondes.
- La fenêtre flottante est pilotée par `VoiceWakeOverlayController`, avec distinction de couleur pour les états soumis/temporaires.
- Après envoi, le moteur redémarre proprement pour écouter le prochain mot de réveil.

## Invariants du cycle de vie

- Si l'activation vocale est activée et les permissions accordées, le moteur de reconnaissance du mot de réveil doit être à l'écoute (sauf lors d'une capture d'appel par touche explicite).
- La visibilité de la fenêtre flottante (y compris la fermeture manuelle via le bouton X) ne doit jamais empêcher le moteur de reprendre.

## Mode de défaillance : fenêtre flottante bloquée (problème antérieur)

Auparavant, si la fenêtre flottante restait visible et que vous la fermiez manuellement, l'activation vocale pouvait sembler « cassée » car les tentatives de redémarrage du moteur pouvaient être bloquées par la visibilité de la fenêtre flottante, sans redémarrage ultérieur planifié.

Mesures de renforcement :

- Le redémarrage du moteur d'activation vocale n'est plus bloqué par la visibilité de la fenêtre flottante.
- À la fin de la fermeture de la fenêtre flottante, `VoiceSessionCoordinator` déclenche `VoiceWakeRuntime.refresh(...)`, donc fermer manuellement avec X restaure toujours l'écoute.

## Détails de l'appel par touche

- La détection de la touche de raccourci utilise un moniteur global `.flagsChanged` pour détecter la **touche Option droite** (`keyCode 61` + `.option`). Nous observons simplement les événements (sans les intercepter).
- Le pipeline de capture se trouve dans `VoicePushToTalk` : démarre immédiatement la reconnaissance vocale, diffuse les résultats partiels vers la fenêtre flottante, et appelle `VoiceWakeForwarder` au relâchement.
- Au démarrage de l'appel par touche, nous suspendons le moteur du mot de réveil pour éviter les conflits de capture audio ; redémarre automatiquement après relâchement.
- Permissions : nécessite microphone + permissions de reconnaissance vocale ; l'observation d'événements nécessite l'approbation d'accessibilité/surveillance d'entrée.
- Claviers externes : certains claviers peuvent ne pas exposer la touche Option droite comme prévu — si l'utilisateur signale une non-réactivité, fournissez un raccourci alternatif.

## Paramètres orientés utilisateur

- **Activation vocale** : active le moteur du mot de réveil.
- **Maintenir Cmd+Fn pour parler** : active le moniteur d'appel par touche. Désactivé sur macOS < 26.
- Sélecteurs de langue et microphone, indicateur de niveau en temps réel, tableau des mots de réveil, testeur (local uniquement ; pas de transmission).
- Le sélecteur de microphone conserve la dernière sélection lors de la déconnexion du périphérique, affiche une indication de déconnexion, et bascule temporairement vers le périphérique par défaut du système jusqu'à la récupération du périphérique.
- **Sons** : sons pour la détection de déclenchement et l'envoi ; par défaut le son système macOS « Glass ». Vous pouvez sélectionner n'importe quel fichier chargeable par `NSSound` (par exemple MP3/WAV/AIFF) pour chaque événement ou choisir **Pas de son**.

## Comportement de transmission

- Lorsque l'activation vocale est activée, le texte transcrit est transmis à la passerelle/l'agent Gateway actif (utilisant le même mode local/distant que le reste de l'application Mac).
- Les réponses sont livrées au **dernier fournisseur principal utilisé** (WhatsApp/Telegram/Discord/WebChat). En cas d'échec de livraison, l'erreur est enregistrée et l'exécution reste visible via WebChat/journaux de session.

## Charge utile de transmission

- `VoiceWakeForwarder.prefixedTranscript(_:)` ajoute un préfixe d'invite machine avant l'envoi. Les chemins du mot de réveil et de l'appel par touche partagent cette méthode.

## Vérification rapide

- Activez l'appel par touche, maintenez Cmd+Fn, parlez, relâchez : la fenêtre flottante doit afficher les résultats partiels puis envoyer.
- Pendant le maintien, l'icône d'oreille de la barre de menus doit rester agrandie (utilisant `triggerVoiceEars(ttl:nil)`); se rétablit après relâchement.
