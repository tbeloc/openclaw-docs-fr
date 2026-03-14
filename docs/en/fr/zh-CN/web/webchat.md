---
read_when:
  - Débogage ou configuration de l'accès WebChat
summary: Utilisation du loopback WebChat statique et de la passerelle Gateway WS pour l'interface utilisateur de chat
title: WebChat
x-i18n:
  generated_at: "2026-02-03T10:13:28Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b5ee2b462c8c979ac27f80dea0cf12cf62b3c799cf8fd0a7721901e26efeb1a0
  source_path: web/webchat.md
  workflow: 15
---

# WebChat (Interface utilisateur Gateway WebSocket)

État : L'interface utilisateur de chat SwiftUI macOS/iOS communique directement avec la passerelle Gateway WebSocket.

## Qu'est-ce que c'est

- Interface utilisateur de chat native de la passerelle Gateway (pas de navigateur intégré, pas de serveur statique local).
- Utilise les mêmes règles de session et de routage que les autres canaux.
- Routage déterministe : les réponses sont toujours renvoyées à WebChat.

## Démarrage rapide

1. Démarrez la passerelle Gateway.
2. Ouvrez l'interface utilisateur WebChat (application macOS/iOS) ou l'onglet chat de l'interface de contrôle.
3. Assurez-vous que l'authentification de la passerelle Gateway est configurée (requise par défaut, même sur loopback).

## Fonctionnement (Comportement)

- L'interface utilisateur se connecte à la passerelle Gateway WebSocket et utilise `chat.history`, `chat.send` et `chat.inject`.
- `chat.inject` ajoute directement les annotations de l'assistant à la transcription et les diffuse à l'interface utilisateur (aucune exécution d'agent).
- L'historique est toujours récupéré à partir de la passerelle Gateway (pas d'écoute de fichiers locaux).
- Si la passerelle Gateway est inaccessible, WebChat est en mode lecture seule.

## Utilisation à distance

- Le mode distant tunnelise la passerelle Gateway WebSocket via SSH/Tailscale.
- Vous n'avez pas besoin d'exécuter un serveur WebChat séparé.

## Référence de configuration (WebChat)

Configuration complète : [Configuration](/gateway/configuration)

Options de canal :

- Pas de bloc `webchat.*` dédié. WebChat utilise les paramètres de point de terminaison + authentification de la passerelle Gateway ci-dessous.

Options globales pertinentes :

- `gateway.port`, `gateway.bind` : hôte/port WebSocket.
- `gateway.auth.mode`, `gateway.auth.token`, `gateway.auth.password` : authentification WebSocket.
- `gateway.remote.url`, `gateway.remote.token`, `gateway.remote.password` : cible de passerelle Gateway distante.
- `session.*` : valeurs par défaut du stockage de session et de la clé primaire.
