---
read_when:
  - Lors de la recherche du support du système d'exploitation ou du chemin d'installation
  - Lors de la décision du lieu d'exécution de la passerelle Gateway
summary: Aperçu du support des plates-formes (passerelle Gateway + applications complémentaires)
title: Plates-formes
x-i18n:
  generated_at: "2026-02-03T07:52:07Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 254852a5ed1996982a52eed4a72659477609e08d340c625d24ef6d99c21eece6
  source_path: platforms/index.md
  workflow: 15
---

# Plates-formes

Le noyau OpenClaw est écrit en TypeScript. **Node est l'environnement d'exécution recommandé**.
Bun n'est pas recommandé pour la passerelle Gateway (bugs avec WhatsApp/Telegram).

Les applications complémentaires sont disponibles pour macOS (application de barre de menu) et les nœuds mobiles (iOS/Android). Les applications complémentaires Windows et
Linux sont en cours de planification, mais la passerelle Gateway est actuellement entièrement supportée.
Une application complémentaire native Windows est également en cours de planification ; l'utilisation de la passerelle Gateway via WSL2 est recommandée.

## Choisissez votre système d'exploitation

- macOS : [macOS](/platforms/macos)
- iOS : [iOS](/platforms/ios)
- Android : [Android](/platforms/android)
- Windows : [Windows](/platforms/windows)
- Linux : [Linux](/platforms/linux)

## VPS et hébergement

- Centre VPS : [Hébergement VPS](/vps)
- Fly.io : [Fly.io](/install/fly)
- Hetzner (Docker) : [Hetzner](/install/hetzner)
- GCP (Compute Engine) : [GCP](/install/gcp)
- exe.dev (VM + proxy HTTPS) : [exe.dev](/install/exe-dev)

## Liens courants

- Guide d'installation : [Guide de démarrage](/start/getting-started)
- Manuel d'exécution de la passerelle Gateway : [Passerelle Gateway](/gateway)
- Configuration de la passerelle Gateway : [Configuration](/gateway/configuration)
- État du service : `openclaw gateway status`

## Installation du service de passerelle Gateway (CLI)

Utilisez l'une des méthodes suivantes (toutes sont supportées) :

- Assistant (recommandé) : `openclaw onboard --install-daemon`
- Installation directe : `openclaw gateway install`
- Flux de configuration : `openclaw configure` → sélectionnez **Gateway service**
- Réparation/Migration : `openclaw doctor` (fournit l'installation ou la réparation du service)

La cible du service dépend du système d'exploitation :

- macOS : LaunchAgent (`bot.molt.gateway` ou `bot.molt.<profile>` ; anciennes versions `com.openclaw.*`)
- Linux/WSL2 : service utilisateur systemd (`openclaw-gateway[-<profile>].service`)
