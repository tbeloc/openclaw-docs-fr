---
summary: "Modes de réveil vocal et push-to-talk plus détails de routage dans l'app mac"
read_when:
  - Working on voice wake or PTT pathways
title: "Voice Wake"
---

# Voice Wake & Push-to-Talk

## Modes

- **Mode wake-word** (par défaut) : le reconnaisseur de parole toujours actif attend les tokens de déclenchement (`swabbleTriggerWords`). À la correspondance, il démarre la capture, affiche l'overlay avec le texte partiel et envoie automatiquement après le silence.
- **Push-to-talk (maintien de la touche Option droite)** : maintenez la touche Option droite pour capturer immédiatement—aucun déclenchement nécessaire. L'overlay apparaît pendant que vous maintenez ; le relâchement finalise et envoie après un court délai pour que vous puissiez ajuster le texte.

## Comportement à l'exécution (wake-word)

- Le reconnaisseur de parole réside dans `VoiceWakeRuntime`.
- Le déclenchement ne s'active que s'il y a une **pause significative** entre le wake word et le mot suivant (~0,55s d'écart). L'overlay/carillon peut démarrer à la pause même avant que la commande ne commence.
- Fenêtres de silence : 2,0s quand la parole s'écoule, 5,0s si seul le déclenchement a été entendu.
- Arrêt dur : 120s pour éviter les sessions qui s'éternisent.
- Débounce entre les sessions : 350ms.
- L'overlay est piloté via `VoiceWakeOverlayController` avec coloration engagée/volatile.
- Après l'envoi, le reconnaisseur redémarre proprement pour écouter le prochain déclenchement.

## Invariants du cycle de vie

- Si Voice Wake est activé et les permissions accordées, le reconnaisseur wake-word doit être à l'écoute (sauf lors d'une capture push-to-talk explicite).
- La visibilité de l'overlay (y compris le rejet manuel via le bouton X) ne doit jamais empêcher le reconnaisseur de reprendre.

## Mode d'échec overlay collant (précédent)

Auparavant, si l'overlay restait visible et que vous le fermiez manuellement, Voice Wake pouvait sembler « mort » car la tentative de redémarrage du runtime pouvait être bloquée par la visibilité de l'overlay et aucun redémarrage ultérieur n'était programmé.

Renforcement :

- Le redémarrage du wake runtime n'est plus bloqué par la visibilité de l'overlay.
- Le rejet de l'overlay déclenche un `VoiceWakeRuntime.refresh(...)` via `VoiceSessionCoordinator`, donc le rejet manuel du X reprend toujours l'écoute.

## Spécificités du push-to-talk

- La détection de raccourci utilise un moniteur global `.flagsChanged` pour **Option droite** (`keyCode 61` + `.option`). Nous observons uniquement les événements (pas d'interception).
- Le pipeline de capture réside dans `VoicePushToTalk` : démarre la parole immédiatement, diffuse les partiels à l'overlay et appelle `VoiceWakeForwarder` au relâchement.
- Quand push-to-talk démarre, nous mettons en pause le runtime wake-word pour éviter les robinets audio concurrents ; il redémarre automatiquement après le relâchement.
- Permissions : nécessite Microphone + Speech ; voir les événements nécessite l'approbation Accessibility/Input Monitoring.
- Claviers externes : certains peuvent ne pas exposer Option droite comme prévu—offrez un raccourci de secours si les utilisateurs signalent des manques.

## Paramètres visibles par l'utilisateur

- Bascule **Voice Wake** : active le runtime wake-word.
- **Maintenez Cmd+Fn pour parler** : active le moniteur push-to-talk. Désactivé sur macOS < 26.
- Sélecteurs de langue et de micro, jauge de niveau en direct, tableau des mots de déclenchement, testeur (local uniquement ; ne transfère pas).
- Le sélecteur de micro préserve la dernière sélection si un appareil se déconnecte, affiche un indice de déconnexion et bascule temporairement vers le système par défaut jusqu'à son retour.
- **Sons** : carillons à la détection de déclenchement et à l'envoi ; par défaut le son système macOS « Glass ». Vous pouvez choisir n'importe quel fichier chargeable par `NSSound` (par ex. MP3/WAV/AIFF) pour chaque événement ou choisir **Aucun son**.

## Comportement de transfert

- Quand Voice Wake est activé, les transcriptions sont transférées à la passerelle/l'agent actif (le même mode local vs distant utilisé par le reste de l'app mac).
- Les réponses sont livrées au **dernier fournisseur principal utilisé** (WhatsApp/Telegram/Discord/WebChat). Si la livraison échoue, l'erreur est enregistrée et l'exécution reste visible via WebChat/journaux de session.

## Charge utile de transfert

- `VoiceWakeForwarder.prefixedTranscript(_:)` ajoute l'indice machine avant l'envoi. Partagé entre les chemins wake-word et push-to-talk.

## Vérification rapide

- Activez push-to-talk, maintenez Cmd+Fn, parlez, relâchez : l'overlay doit afficher les partiels puis envoyer.
- Pendant que vous maintenez, les oreilles de la barre de menu doivent rester agrandies (utilise `triggerVoiceEars(ttl:nil)`); elles chutent après le relâchement.
