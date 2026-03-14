---
summary: "Comment l'application macOS intègre le WebChat de la passerelle et comment le déboguer"
read_when:
  - Débogage de la vue WebChat mac ou du port de bouclage
title: "WebChat"
---

# WebChat (application macOS)

L'application de barre de menu macOS intègre l'interface utilisateur WebChat en tant que vue SwiftUI native. Elle se connecte à la passerelle et utilise par défaut la **session principale** pour l'agent sélectionné (avec un sélecteur de session pour les autres sessions).

- **Mode local** : se connecte directement au WebSocket de la passerelle locale.
- **Mode distant** : transfère le port de contrôle de la passerelle via SSH et utilise ce tunnel comme plan de données.

## Lancement et débogage

- Manuel : Menu Lobster → « Open Chat ».
- Ouverture automatique pour les tests :

  ```bash
  dist/OpenClaw.app/Contents/MacOS/OpenClaw --webchat
  ```

- Journaux : `./scripts/clawlog.sh` (sous-système `ai.openclaw`, catégorie `WebChatSwiftUI`).

## Comment c'est connecté

- Plan de données : méthodes WS de la passerelle `chat.history`, `chat.send`, `chat.abort`,
  `chat.inject` et événements `chat`, `agent`, `presence`, `tick`, `health`.
- Session : utilise par défaut la session principale (`main`, ou `global` quand la portée est
  globale). L'interface utilisateur peut basculer entre les sessions.
- L'intégration utilise une session dédiée pour garder la configuration de première exécution séparée.

## Surface de sécurité

- Le mode distant transfère uniquement le port de contrôle WebSocket de la passerelle via SSH.

## Limitations connues

- L'interface utilisateur est optimisée pour les sessions de chat (pas un bac à sable de navigateur complet).
