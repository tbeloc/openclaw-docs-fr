---
summary: "Runtime Gateway sur macOS (service launchd externe)"
read_when:
  - Empaquetage d'OpenClaw.app
  - Débogage du service launchd Gateway macOS
  - Installation de la CLI Gateway pour macOS
title: "Gateway sur macOS"
---

# Gateway sur macOS (launchd externe)

OpenClaw.app ne regroupe plus Node/Bun ou le runtime Gateway. L'application macOS
s'attend à une installation **externe** de la CLI `openclaw`, ne lance pas le Gateway en tant que processus enfant,
et gère un service launchd par utilisateur pour maintenir le Gateway en fonctionnement (ou se connecte à un Gateway local existant s'il en existe déjà un).

## Installer la CLI (requis pour le mode local)

Node 24 est le runtime par défaut sur Mac. Node 22 LTS, actuellement `22.16+`, fonctionne toujours pour la compatibilité. Ensuite, installez `openclaw` globalement :

```bash
npm install -g openclaw@<version>
```

Le bouton **Install CLI** de l'application macOS exécute le même flux via npm/pnpm (bun non recommandé pour le runtime Gateway).

## Launchd (Gateway en tant que LaunchAgent)

Étiquette :

- `ai.openclaw.gateway` (ou `ai.openclaw.<profile>` ; l'ancien `com.openclaw.*` peut subsister)

Emplacement du plist (par utilisateur) :

- `~/Library/LaunchAgents/ai.openclaw.gateway.plist`
  (ou `~/Library/LaunchAgents/ai.openclaw.<profile>.plist`)

Gestionnaire :

- L'application macOS gère l'installation/mise à jour de LaunchAgent en mode Local.
- La CLI peut également l'installer : `openclaw gateway install`.

Comportement :

- « OpenClaw Active » active/désactive le LaunchAgent.
- La fermeture de l'application n'arrête **pas** le gateway (launchd le maintient actif).
- Si un Gateway est déjà en cours d'exécution sur le port configuré, l'application s'y connecte
  au lieu de démarrer un nouveau.

Journalisation :

- stdout/err launchd : `/tmp/openclaw/openclaw-gateway.log`

## Compatibilité des versions

L'application macOS vérifie la version du gateway par rapport à sa propre version. S'ils sont
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
