---
read_when: Connecting the macOS app to a remote gateway over SSH
summary: Configurer le tunnel SSH pour connecter OpenClaw.app à une Gateway distante
title: Configuration de la Gateway distante
x-i18n:
  generated_at: "2026-02-03T07:48:37Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b1ae266a7cb4911b82ae3ec6cb98b1b57aca592aeb1dc8b74bbce9b0ea9dd1d1
  source_path: gateway/remote-gateway-readme.md
  workflow: 15
---

# Exécuter OpenClaw.app avec une Gateway distante

OpenClaw.app utilise un tunnel SSH pour se connecter à une Gateway distante. Ce guide vous montre comment le configurer.

## Aperçu

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Machine                          │
│                                                              │
│  OpenClaw.app ──► ws://127.0.0.1:18789 (local port)           │
│                     │                                        │
│                     ▼                                        │
│  SSH Tunnel ────────────────────────────────────────────────│
│                     │                                        │
└─────────────────────┼──────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                         Remote Machine                        │
│                                                              │
│  Gateway WebSocket ──► ws://127.0.0.1:18789 ──►              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Configuration rapide

### Étape 1 : Ajouter la configuration SSH

Modifiez `~/.ssh/config` et ajoutez :

```ssh
Host remote-gateway
    HostName <REMOTE_IP>          # e.g., 172.27.187.184
    User <REMOTE_USER>            # e.g., jefferson
    LocalForward 18789 127.0.0.1:18789
    IdentityFile ~/.ssh/id_rsa
```

Remplacez `<REMOTE_IP>` et `<REMOTE_USER>` par vos valeurs.

### Étape 2 : Copier la clé SSH

Copiez votre clé publique sur la machine distante (entrez le mot de passe une fois) :

```bash
ssh-copy-id -i ~/.ssh/id_rsa <REMOTE_USER>@<REMOTE_IP>
```

### Étape 3 : Configurer le jeton de la Gateway

```bash
launchctl setenv OPENCLAW_GATEWAY_TOKEN "<your-token>"
```

### Étape 4 : Démarrer le tunnel SSH

```bash
ssh -N remote-gateway &
```

### Étape 5 : Redémarrer OpenClaw.app

```bash
# Quitter OpenClaw.app (⌘Q), puis rouvrir :
open /path/to/OpenClaw.app
```

L'application se connectera maintenant à la Gateway distante via le tunnel SSH.

---

## Démarrer automatiquement le tunnel à la connexion

Pour démarrer automatiquement le tunnel SSH à la connexion, créez un Launch Agent.

### Créer un fichier PLIST

Enregistrez ceci sous `~/Library/LaunchAgents/bot.molt.ssh-tunnel.plist` :

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>bot.molt.ssh-tunnel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/ssh</string>
        <string>-N</string>
        <string>remote-gateway</string>
    </array>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

### Charger le Launch Agent

```bash
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/bot.molt.ssh-tunnel.plist
```

Le tunnel va maintenant :

- Démarrer automatiquement à la connexion
- Redémarrer en cas de plantage
- S'exécuter continuellement en arrière-plan

Note sur les versions antérieures : Si un LaunchAgent `com.openclaw.ssh-tunnel` hérité existe, supprimez-le.

---

## Dépannage

**Vérifier si le tunnel est en cours d'exécution :**

```bash
ps aux | grep "ssh -N remote-gateway" | grep -v grep
lsof -i :18789
```

**Redémarrer le tunnel :**

```bash
launchctl kickstart -k gui/$UID/bot.molt.ssh-tunnel
```

**Arrêter le tunnel :**

```bash
launchctl bootout gui/$UID/bot.molt.ssh-tunnel
```

---

## Fonctionnement

| Composant                            | Fonction                                      |
| ------------------------------------ | --------------------------------------------- |
| `LocalForward 18789 127.0.0.1:18789` | Transfère le port local 18789 au port distant 18789 |
| `ssh -N`                             | SSH n'exécute pas de commande distante (transfert de port uniquement) |
| `KeepAlive`                          | Redémarre automatiquement le tunnel en cas de plantage |
| `RunAtLoad`                          | Démarre le tunnel au chargement de l'agent |

OpenClaw.app se connecte à `ws://127.0.0.1:18789` sur votre machine cliente. Le tunnel SSH transfère cette connexion au port 18789 de la machine distante exécutant la Gateway.
