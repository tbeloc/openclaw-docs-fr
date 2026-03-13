---
read_when:
  - Ajuster le comportement de la superposition vocale
summary: Cycle de vie de la superposition vocale lors du chevauchement du mot de réveil et de la parole à la touche
title: Superposition vocale
x-i18n:
  generated_at: "2026-02-01T21:33:26Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 3be1a60aa7940b2368ff62cd49f04b2b8422876030e8ea206b467f66a5a6bd4d
  source_path: platforms/mac/voice-overlay.md
  workflow: 15
---

# Cycle de vie de la superposition vocale (macOS)

Audience : contributeurs d'applications macOS. Objectif : maintenir un comportement prévisible de la superposition vocale lors du chevauchement du mot de réveil et de la parole à la touche.

### Intention actuelle

- Si la superposition s'affiche déjà en raison du mot de réveil, lorsque l'utilisateur appuie sur la touche de raccourci, la session de parole à la touche *reprend* le texte existant plutôt que de le réinitialiser. La superposition reste affichée pendant que la touche est maintenue enfoncée. Lorsque l'utilisateur la relâche : si du texte reste après suppression des espaces, il est envoyé ; sinon, la superposition se ferme.
- Lors de l'utilisation seule du mot de réveil, l'envoi automatique se fait toujours après le silence ; la parole à la touche s'envoie immédiatement au relâchement.

### Implémenté (9 décembre 2025)

- Les sessions de superposition portent désormais un jeton pour chaque capture (mot de réveil ou parole à la touche). Lorsque le jeton ne correspond pas, les mises à jour partielles/finales/d'envoi/de fermeture/de volume sont supprimées, évitant les rappels obsolètes.
- La parole à la touche reprend tout texte de superposition visible comme préfixe (ainsi, appuyer sur la touche de raccourci lorsque la superposition de réveil s'affiche conserve le texte et ajoute la nouvelle parole). Elle attend au maximum 1,5 seconde pour obtenir le résultat de transcription final, puis revient au texte actuel.
- Les sons et journaux de superposition sont générés au niveau `info`, catégorisés comme `voicewake.overlay`, `voicewake.ptt` et `voicewake.chime` (début de session, partiel, final, envoi, fermeture, raison du son).

### Étapes suivantes

1. **VoiceSessionCoordinator (acteur)**
   - Détient une seule `VoiceSession` à la fois.
   - API (basée sur jeton) : `beginWakeCapture`, `beginPushToTalk`, `updatePartial`, `endCapture`, `cancel`, `applyCooldown`.
   - Supprime les rappels portant des jetons obsolètes (empêche les anciens reconnaisseurs de rouvrir la superposition).
2. **VoiceSession (modèle)**
   - Champs : `token`, `source` (wakeWord|pushToTalk), texte soumis/temporaire, drapeau de son, minuteurs (envoi automatique, inactivité), `overlayMode` (display|editing|sending), délai d'expiration du refroidissement.
3. **Liaisons de superposition**
   - `VoiceSessionPublisher` (`ObservableObject`) reflète la session active vers SwiftUI.
   - `VoiceWakeOverlayView` ne s'affiche que via le publisher ; ne modifie jamais directement le singleton global.
   - Les actions utilisateur de la superposition (`sendNow`, `dismiss`, `edit`) rappellent le coordinateur avec le jeton de session.
4. **Chemin d'envoi unifié**
   - À `endCapture` : si le texte après suppression des espaces est vide → fermeture ; sinon `performSend(session:)` (joue le son d'envoi une fois, transfère, ferme).
   - Parole à la touche : sans délai ; mot de réveil : délai d'envoi automatique optionnel.
   - Applique un refroidissement bref au runtime de réveil après la fin de la parole à la touche, empêchant le mot de réveil de se déclencher immédiatement.
5. **Journalisation**
   - Le coordinateur génère des journaux au niveau `.info` sous le sous-système `bot.molt`, catégories `voicewake.overlay` et `voicewake.chime`.
   - Événements clés : `session_started`, `adopted_by_push_to_talk`, `partial`, `finalized`, `send`, `dismiss`, `cancel`, `cooldown`.

### Liste de contrôle de débogage

- Lors de la reproduction des problèmes de superposition collante, consultez les journaux en continu :

  ```bash
  sudo log stream --predicate 'subsystem == "bot.molt" AND category CONTAINS "voicewake"' --level info --style compact
  ```

- Vérifiez qu'un seul jeton de session actif existe ; les rappels obsolètes doivent être supprimés par le coordinateur.
- Assurez-vous que la parole à la touche appelle toujours `endCapture` avec le jeton actif au relâchement ; si le texte est vide, attendez-vous à `dismiss` sans son ni envoi.

### Étapes de migration (recommandées)

1. Ajoutez `VoiceSessionCoordinator`, `VoiceSession` et `VoiceSessionPublisher`.
2. Refactorisez `VoiceWakeRuntime` pour créer/mettre à jour/terminer les sessions plutôt que de manipuler directement `VoiceWakeOverlayController`.
3. Refactorisez `VoicePushToTalk` pour reprendre la session existante et appeler `endCapture` au relâchement ; appliquez le refroidissement du runtime.
4. Connectez `VoiceWakeOverlayController` au publisher ; supprimez les appels directs du runtime/PTT.
5. Ajoutez des tests d'intégration pour la reprise de session, le refroidissement et la fermeture de texte vide.
