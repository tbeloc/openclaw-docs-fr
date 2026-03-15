---
summary: "Aperçu du support des plateformes (Gateway + applications compagnon)"
read_when:
  - À la recherche du support du système d'exploitation ou des chemins d'installation
  - Décider où exécuter la Gateway
title: "Plateformes"
---

# Plateformes

Le cœur d'OpenClaw est écrit en TypeScript. **Node est le runtime recommandé**.
Bun n'est pas recommandé pour la Gateway (bugs WhatsApp/Telegram).

Des applications compagnon existent pour macOS (application de barre de menu) et les nœuds mobiles (iOS/Android). Les applications compagnon Windows et Linux sont prévues, mais la Gateway est entièrement supportée aujourd'hui.
Les applications compagnon natives pour Windows sont également prévues ; la Gateway est recommandée via WSL2.

## Choisissez votre système d'exploitation

- macOS : [macOS](/fr/platforms/macos)
- iOS : [iOS](/fr/platforms/ios)
- Android : [Android](/fr/platforms/android)
- Windows : [Windows](/fr/platforms/windows)
- Linux : [Linux](/fr/platforms/linux)

## VPS et hébergement

- Hub VPS : [Hébergement VPS](/fr/vps)
- Fly.io : [Fly.io](/fr/install/fly)
- Hetzner (Docker) : [Hetzner](/fr/install/hetzner)
- GCP (Compute Engine) : [GCP](/fr/install/gcp)
- exe.dev (VM + proxy HTTPS) : [exe.dev](/fr/install/exe-dev)

## Liens courants

- Guide d'installation : [Démarrage](/fr/start/getting-started)
- Runbook Gateway : [Gateway](/fr/gateway)
- Configuration Gateway : [Configuration](/fr/gateway/configuration)
- État du service : `openclaw gateway status`

## Installation du service Gateway (CLI)

Utilisez l'un de ceux-ci (tous supportés) :

- Assistant (recommandé) : `openclaw onboard --install-daemon`
- Direct : `openclaw gateway install`
- Flux de configuration : `openclaw configure` → sélectionnez **Service Gateway**
- Réparation/migration : `openclaw doctor` (propose d'installer ou de corriger le service)

La cible du service dépend du système d'exploitation :

- macOS : LaunchAgent (`ai.openclaw.gateway` ou `ai.openclaw.<profile>` ; ancien `com.openclaw.*`)
- Linux/WSL2 : service utilisateur systemd (`openclaw-gateway[-<profile>].service`)
