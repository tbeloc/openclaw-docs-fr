---
summary: "Aperçu du support des plateformes (Gateway + applications compagnon)"
read_when:
  - À la recherche du support OS ou des chemins d'installation
  - Décider où exécuter la Gateway
title: "Plateformes"
---

# Plateformes

Le cœur d'OpenClaw est écrit en TypeScript. **Node est le runtime recommandé**.
Bun n'est pas recommandé pour la Gateway (bugs WhatsApp/Telegram).

Des applications compagnon existent pour macOS (application de barre de menu) et les nœuds mobiles (iOS/Android). Les applications compagnon Windows et Linux sont prévues, mais la Gateway est entièrement supportée aujourd'hui.
Les applications compagnon natives pour Windows sont également prévues ; la Gateway est recommandée via WSL2.

## Choisissez votre OS

- macOS: [macOS](/platforms/macos)
- iOS: [iOS](/platforms/ios)
- Android: [Android](/platforms/android)
- Windows: [Windows](/platforms/windows)
- Linux: [Linux](/platforms/linux)

## VPS et hébergement

- Hub VPS: [Hébergement VPS](/vps)
- Fly.io: [Fly.io](/install/fly)
- Hetzner (Docker): [Hetzner](/install/hetzner)
- GCP (Compute Engine): [GCP](/install/gcp)
- exe.dev (VM + proxy HTTPS): [exe.dev](/install/exe-dev)

## Liens courants

- Guide d'installation: [Démarrage](/start/getting-started)
- Runbook Gateway: [Gateway](/gateway)
- Configuration Gateway: [Configuration](/gateway/configuration)
- État du service: `openclaw gateway status`

## Installation du service Gateway (CLI)

Utilisez l'un de ceux-ci (tous supportés):

- Assistant (recommandé): `openclaw onboard --install-daemon`
- Direct: `openclaw gateway install`
- Flux de configuration: `openclaw configure` → sélectionnez **Service Gateway**
- Réparation/migration: `openclaw doctor` (propose d'installer ou de corriger le service)

La cible du service dépend de l'OS:

- macOS: LaunchAgent (`ai.openclaw.gateway` ou `ai.openclaw.<profile>`; ancien `com.openclaw.*`)
- Linux/WSL2: service utilisateur systemd (`openclaw-gateway[-<profile>].service`)
