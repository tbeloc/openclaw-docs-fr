---
read_when:
  - Modifier le comportement de l'icône de la barre de menus
summary: État et animations de l'icône de la barre de menus OpenClaw sur macOS
title: Icône de la barre de menus
x-i18n:
  generated_at: "2026-02-01T21:32:49Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a67a6e6bbdc2b611ba365d3be3dd83f9e24025d02366bc35ffcce9f0b121872b
  source_path: platforms/mac/icon.md
  workflow: 15
---

# États de l'icône de la barre de menus

Auteur : steipete · Mise à jour : 2025-12-06 · Portée : Application macOS (`apps/macos`)

- **Inactif :** Animation d'icône normale (clignement, balancement occasionnel).
- **Suspendu :** L'élément d'état utilise `appearsDisabled` ; pas d'animation.
- **Déclenchement vocal (grandes oreilles) :** Le détecteur de réveil vocal appelle `AppState.triggerVoiceEars(ttl: nil)` lorsqu'il détecte le mot de réveil, maintenant `earBoostActive=true` pendant la capture vocale. Les oreilles sont agrandies (1,9×), affichant des trous d'oreille circulaires pour une meilleure lisibilité, puis restaurées via `stopVoiceEars()` après 1 seconde de silence. Déclenché uniquement par le pipeline vocal interne de l'application.
- **En cours de travail (agent en cours d'exécution) :** `AppState.isWorking=true` pilote la micro-animation « balancement rapide de la queue/des jambes » : les jambes se balancent plus rapidement avec un léger décalage pendant le travail. Actuellement basculé lors de l'exécution de l'agent WebChat ; ajoutez la même logique de basculement lors de l'intégration d'autres tâches longues.

Points d'intégration

- Réveil vocal : Le runtime/testeur appelle `AppState.triggerVoiceEars(ttl: nil)` au déclenchement, puis `stopVoiceEars()` après 1 seconde de silence pour correspondre à la fenêtre de capture.
- Activité de l'agent : Définissez `AppStateStore.shared.setWorking(true/false)` avant et après l'intervalle de travail (déjà effectué dans les appels d'agent WebChat). Gardez l'intervalle court et réinitialisez dans un bloc `defer` pour éviter que l'animation ne se bloque.

Formes et dimensions

- L'icône de base est dessinée dans `CritterIconRenderer.makeIcon(blink:legWiggle:earWiggle:earScale:earHoles:)`.
- L'échelle des oreilles est par défaut `1.0` ; lors du renforcement vocal, définissez `earScale=1.9` et basculez `earHoles=true`, sans modifier le cadre global (image de modèle 18×18 pt rendue en stockage Retina 36×36 px).
- Le balancement rapide utilise une amplitude de jambe d'environ 1.0 maximum avec un léger tremblement horizontal ; il se superpose au balancement inactif existant.

Notes de comportement

- Pas de basculement CLI/agent externe pour les états des oreilles/travail ; gardez-le contrôlé uniquement par les signaux de l'application elle-même pour éviter les tremblements d'état inattendus.
- Gardez le TTL court (&lt;10 secondes) afin que l'icône puisse revenir rapidement à l'état de base si une tâche se suspend.
