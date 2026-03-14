---
summary: "Cycle de vie de la superposition vocale lorsque le mot de réveil et la transmission par appui se chevauchent"
read_when:
  - Adjusting voice overlay behavior
title: "Superposition vocale"
---

# Cycle de vie de la superposition vocale (macOS)

Audience : contributeurs d'applications macOS. Objectif : maintenir la superposition vocale prévisible lorsque le mot de réveil et la transmission par appui se chevauchent.

## Intention actuelle

- Si la superposition est déjà visible à partir du mot de réveil et que l'utilisateur appuie sur la touche de raccourci, la session de raccourci _adopte_ le texte existant au lieu de le réinitialiser. La superposition reste visible tant que la touche est enfoncée. Lorsque l'utilisateur relâche : envoyer s'il y a du texte coupé, sinon fermer.
- Le mot de réveil seul envoie toujours automatiquement au silence ; la transmission par appui envoie immédiatement au relâchement.

## Implémenté (9 décembre 2025)

- Les sessions de superposition portent désormais un jeton par capture (mot de réveil ou transmission par appui). Les mises à jour partielles/finales/d'envoi/de fermeture/de niveau sont supprimées lorsque le jeton ne correspond pas, évitant les rappels obsolètes.
- La transmission par appui adopte tout texte de superposition visible comme préfixe (donc appuyer sur la touche de raccourci tandis que la superposition de réveil est active conserve le texte et ajoute la nouvelle parole). Elle attend jusqu'à 1,5 s une transcription finale avant de revenir au texte actuel.
- La journalisation des carillons/superpositions est émise à `info` dans les catégories `voicewake.overlay`, `voicewake.ptt` et `voicewake.chime` (démarrage de session, partiel, final, envoi, fermeture, raison du carillon).

## Prochaines étapes

1. **VoiceSessionCoordinator (acteur)**
   - Possède exactement une `VoiceSession` à la fois.
   - API (basée sur les jetons) : `beginWakeCapture`, `beginPushToTalk`, `updatePartial`, `endCapture`, `cancel`, `applyCooldown`.
   - Supprime les rappels qui portent des jetons obsolètes (empêche les anciens reconnaisseurs de rouvrir la superposition).
2. **VoiceSession (modèle)**
   - Champs : `token`, `source` (wakeWord|pushToTalk), texte engagé/volatil, drapeaux de carillon, minuteurs (envoi automatique, inactivité), `overlayMode` (display|editing|sending), délai d'expiration du refroidissement.
3. **Liaison de superposition**
   - `VoiceSessionPublisher` (`ObservableObject`) reflète la session active dans SwiftUI.
   - `VoiceWakeOverlayView` ne s'affiche que via l'éditeur ; elle ne modifie jamais directement les singletons globaux.
   - Les actions de l'utilisateur de superposition (`sendNow`, `dismiss`, `edit`) rappellent le coordinateur avec le jeton de session.
4. **Chemin d'envoi unifié**
   - Sur `endCapture` : si le texte coupé est vide → fermer ; sinon `performSend(session:)` (joue le carillon d'envoi une fois, transfère, ferme).
   - Transmission par appui : sans délai ; mot de réveil : délai optionnel pour l'envoi automatique.
   - Appliquer un court refroidissement au runtime de réveil après la fin de la transmission par appui afin que le mot de réveil ne se déclenche pas immédiatement.
5. **Journalisation**
   - Le coordinateur émet des journaux `.info` dans le sous-système `ai.openclaw`, catégories `voicewake.overlay` et `voicewake.chime`.
   - Événements clés : `session_started`, `adopted_by_push_to_talk`, `partial`, `finalized`, `send`, `dismiss`, `cancel`, `cooldown`.

## Liste de contrôle de débogage

- Diffusez les journaux lors de la reproduction d'une superposition collante :

  ```bash
  sudo log stream --predicate 'subsystem == "ai.openclaw" AND category CONTAINS "voicewake"' --level info --style compact
  ```

- Vérifiez qu'un seul jeton de session actif existe ; les rappels obsolètes doivent être supprimés par le coordinateur.
- Assurez-vous que le relâchement de la transmission par appui appelle toujours `endCapture` avec le jeton actif ; si le texte est vide, attendez-vous à une `dismiss` sans carillon ni envoi.

## Étapes de migration (suggérées)

1. Ajoutez `VoiceSessionCoordinator`, `VoiceSession` et `VoiceSessionPublisher`.
2. Refactorisez `VoiceWakeRuntime` pour créer/mettre à jour/terminer des sessions au lieu de toucher directement `VoiceWakeOverlayController`.
3. Refactorisez `VoicePushToTalk` pour adopter les sessions existantes et appeler `endCapture` au relâchement ; appliquez le refroidissement du runtime.
4. Connectez `VoiceWakeOverlayController` à l'éditeur ; supprimez les appels directs du runtime/PTT.
5. Ajoutez des tests d'intégration pour l'adoption de session, le refroidissement et la fermeture de texte vide.
