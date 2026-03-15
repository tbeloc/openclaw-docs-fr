---
summary: "Runtime de passerelle sur macOS (service launchd externe)"
read_when:
  - Empaquetage d'OpenClaw.app
  - Débogage du service launchd de passerelle macOS
  - Installation de la CLI de passerelle pour macOS
title: "Passerelle sur macOS"
---

# Passerelle sur macOS (launchd externe)

OpenClaw.app ne regroupe plus Node/Bun ou le runtime de passerelle. L'application macOS
s'attend à une installation CLI `openclaw` **externe**, ne lance pas la passerelle en tant que
processus enfant, et gère un service launchd par utilisateur pour maintenir la passerelle
en fonctionnement (ou se connecte à une passerelle locale existante si l'une est déjà en cours d'exécution).

## Installer la CLI (obligatoire pour le mode local)

Node 24 est le runtime par défaut sur Mac. Node 22 LTS, actuellement `22.16+`, fonctionne toujours pour la compatibilité. Ensuite, installez `openclaw` globalement :

```bash
npm install -g openclaw@<version>
```

Le bouton **Install CLI** de l'application macOS exécute le même flux via npm/pnpm (bun non recommandé pour le runtime de passerelle).

## Launchd (Passerelle en tant que LaunchAgent)

Étiquette :

- `ai.openclaw.gateway` (ou `ai.openclaw.<profile>` ; l'héritage `com.openclaw.*` peut subsister)

Emplacement Plist (par utilisateur) :

- `~/Library/LaunchAgents/ai.openclaw.gateway.plist`
  (ou `~/Library/LaunchAgents/ai.openclaw.<profile>.plist`)

Gestionnaire :

- L'application macOS possède l'installation/mise à jour de LaunchAgent en mode Local.
- La CLI peut également l'installer : `openclaw gateway install`.

Comportement :

- « OpenClaw Active » active/désactive le LaunchAgent.
- La fermeture de l'application n'arrête **pas** la passerelle (launchd la maintient en vie).
- Si une passerelle est déjà en cours d'exécution sur le port configuré, l'application s'y connecte
  au lieu de démarrer une nouvelle.

Journalisation :

- stdout/err de launchd : `/tmp/openclaw/openclaw-gateway.log`

## Compatibilité des versions

L'application macOS vérifie la version de la passerelle par rapport à sa propre version. Si elles sont
incompatibles, mettez à jour la CLI globale pour qu'elle corresponde à la version de l'application.

## Vérification rapide

```bash
openclaw --version

OPENCLAW_SKIP_CHANNELS=1 \
OPENCLAW_SKIP_CANVAS_HOST=1 \
openclaw gateway --port 18999 --bind loopback
```

Ensuite :

```bash
openclaw gateway call health --url ws://127.0.0.1:18999 --timeout 3000
```
