---
read_when:
  - Déboguer la vue WebChat macOS ou le port loopback
summary: Comment les applications macOS intègrent Gateway WebChat et comment déboguer
title: WebChat
x-i18n:
  generated_at: "2026-02-03T07:52:46Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 04ff448758e530098e2004625f33e42fc3dbe31137cd3beec2d55590e507de08
  source_path: platforms/mac/webchat.md
  workflow: 15
---

# WebChat (application macOS)

L'application de barre de menus macOS intègre l'interface utilisateur WebChat en tant que vue SwiftUI native. Elle se connecte à Gateway, en utilisant par défaut la **session principale** de l'agent sélectionné (avec un sélecteur de session pour les autres sessions).

- **Mode local** : connexion directe au WebSocket Gateway local.
- **Mode distant** : transfert du port de contrôle Gateway via SSH, et utilisation de ce tunnel comme plan de données.

## Lancement et débogage

- Manuel : Menu Lobster → "Open Chat".
- Ouverture automatique lors des tests :
  ```bash
  dist/OpenClaw.app/Contents/MacOS/OpenClaw --webchat
  ```
- Journaux : `./scripts/clawlog.sh` (sous-système `bot.molt`, catégorie `WebChatSwiftUI`).

## Fonctionnement

- Plan de données : méthodes Gateway WS `chat.history`, `chat.send`, `chat.abort`, `chat.inject` et événements `chat`, `agent`, `presence`, `tick`, `health`.
- Sessions : par défaut la session principale (`main`, ou `global` si la portée est globale). L'interface utilisateur peut basculer entre les sessions.
- L'assistant utilise une session dédiée pour séparer la configuration du premier lancement.

## Aspects de sécurité

- Le mode distant transfère uniquement le port de contrôle Gateway WebSocket via SSH.

## Limitations connues

- L'interface utilisateur est optimisée pour les sessions de chat (pas un bac à sable de navigateur complet).
