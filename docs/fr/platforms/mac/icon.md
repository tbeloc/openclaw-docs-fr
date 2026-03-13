---
summary: "États et animations des icônes de la barre de menu pour OpenClaw sur macOS"
read_when:
  - Changing menu bar icon behavior
title: "Icône de la barre de menu"
---

# États de l'icône de la barre de menu

Author: steipete · Updated: 2025-12-06 · Scope: macOS app (`apps/macos`)

- **Inactif :** Animation d'icône normale (clignotement, léger tremblement occasionnel).
- **En pause :** L'élément de statut utilise `appearsDisabled` ; aucun mouvement.
- **Déclenchement vocal (grandes oreilles) :** Le détecteur de réveil vocal appelle `AppState.triggerVoiceEars(ttl: nil)` quand le mot de réveil est entendu, en maintenant `earBoostActive=true` pendant la capture de l'énoncé. Les oreilles s'agrandissent (1,9x), obtiennent des trous d'oreille circulaires pour la lisibilité, puis disparaissent via `stopVoiceEars()` après 1s de silence. Déclenché uniquement à partir du pipeline vocal intégré à l'application.
- **En cours de traitement (agent actif) :** `AppState.isWorking=true` déclenche un micro-mouvement de « queue/jambe qui s'agite » : tremblement des jambes plus rapide et léger décalage pendant que le travail est en cours. Actuellement basculé autour des exécutions de l'agent WebChat ; ajoutez le même basculement autour d'autres tâches longues quand vous les connecterez.

Points de connexion

- Réveil vocal : appelez `AppState.triggerVoiceEars(ttl: nil)` au déclenchement et `stopVoiceEars()` après 1s de silence pour correspondre à la fenêtre de capture.
- Activité de l'agent : définissez `AppStateStore.shared.setWorking(true/false)` autour des périodes de travail (déjà fait dans l'appel de l'agent WebChat). Gardez les périodes courtes et réinitialisez dans les blocs `defer` pour éviter les animations bloquées.

Formes et tailles

- Icône de base dessinée dans `CritterIconRenderer.makeIcon(blink:legWiggle:earWiggle:earScale:earHoles:)`.
- L'échelle des oreilles par défaut est `1.0` ; le renforcement vocal définit `earScale=1.9` et bascule `earHoles=true` sans modifier le cadre global (image de modèle 18×18 pt rendue dans un magasin de support Retina 36×36 px).
- L'agitation utilise un tremblement des jambes jusqu'à ~1.0 avec un léger jiggle horizontal ; c'est additif à tout tremblement inactif existant.

Notes comportementales

- Aucun basculement CLI/broker externe pour les oreilles/travail ; gardez-le interne aux propres signaux de l'application pour éviter les battements accidentels.
- Gardez les TTL courts (<10s) pour que l'icône revienne à l'état de base rapidement si un travail se bloque.
