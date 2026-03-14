---
summary: "Configuration du tunnel SSH pour OpenClaw.app se connectant à une passerelle distante"
read_when: "Connexion de l'application macOS à une passerelle distante via SSH"
title: "Configuration de la Passerelle Distante"
---

# Exécution d'OpenClaw.app avec une Passerelle Distante

OpenClaw.app utilise le tunneling SSH pour se connecter à une passerelle distante. Ce guide vous montre comment le configurer.

## Aperçu

```mermaid
flowchart TB
    subgraph Client["Machine Client"]
        direction TB
        A["OpenClaw.app"]
        B["ws://127.0.0.1:18789\n(port local)"]
        T["Tunnel SSH"]

        A --> B
        B --> T
    end
    subgraph Remote["Machine Distante"]
        direction TB
        C["Gateway WebSocket"]
        D["ws://127.0.0.1:18789"]

        C --> D
    end
    T --> C
```

## Configuration Rapide

### Étape 1 : Ajouter la Configuration SSH

Modifiez `~/.ssh/config` et ajoutez :

```ssh
Host remote-gateway
    HostName <REMOTE_IP>          # ex. 172.27.187.184
    User <REMOTE_USER>            # ex. jefferson
    LocalForward 18789 127.0.0.1:18789
    IdentityFile ~/.ssh/id_rsa
```

Remplacez `<REMOTE_IP>` et `<REMOTE_USER>` par vos valeurs.

### Étape 2 : Copier la Clé SSH

Copiez votre clé publique sur la machine distante (entrez le mot de passe une fois) :

```bash
ssh-copy-id -i ~/.ssh/id_rsa <REMOTE_USER>@<REMOTE_IP>
```

### Étape 3 : Définir le Jeton de Passerelle

```bash
launchctl setenv OPENCLAW_GATEWAY_TOKEN "<your-token>"
```

### Étape 4 : Démarrer le Tunnel SSH

```bash
ssh -N remote-gateway &
```

### Étape 5 : Redémarrer OpenClaw.app

```bash
# Quittez OpenClaw.app (⌘Q), puis rouvrez :
open /path/to/OpenClaw.app
```

L'application se connectera maintenant à la passerelle distante via le tunnel SSH.

---

## Démarrage Automatique du Tunnel à la Connexion

Pour que le tunnel SSH démarre automatiquement lors de votre connexion, créez un Agent de Lancement.

### Créer le fichier PLIST

Enregistrez ceci sous `~/Library/LaunchAgents/ai.openclaw.ssh-tunnel.plist` :

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.openclaw.ssh-tunnel</string>
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

### Charger l'Agent de Lancement

```bash
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.openclaw.ssh-tunnel.plist
```

Le tunnel va maintenant :

- Démarrer automatiquement lors de votre connexion
- Redémarrer s'il plante
- Continuer à fonctionner en arrière-plan

Note sur l'héritage : supprimez tout ancien Agent de Lancement `com.openclaw.ssh-tunnel` s'il est présent.

---

## Dépannage

**Vérifier si le tunnel est en cours d'exécution :**

```bash
ps aux | grep "ssh -N remote-gateway" | grep -v grep
lsof -i :18789
```

**Redémarrer le tunnel :**

```bash
launchctl kickstart -k gui/$UID/ai.openclaw.ssh-tunnel
```

**Arrêter le tunnel :**

```bash
launchctl bootout gui/$UID/ai.openclaw.ssh-tunnel
```

---

## Comment Cela Fonctionne

| Composant                            | Ce qu'il fait                                                |
| ------------------------------------ | ------------------------------------------------------------ |
| `LocalForward 18789 127.0.0.1:18789` | Transfère le port local 18789 au port distant 18789          |
| `ssh -N`                             | SSH sans exécuter de commandes distantes (juste le transfert de ports) |
| `KeepAlive`                          | Redémarre automatiquement le tunnel s'il plante              |
| `RunAtLoad`                          | Démarre le tunnel au chargement de l'agent                   |

OpenClaw.app se connecte à `ws://127.0.0.1:18789` sur votre machine client. Le tunnel SSH transfère cette connexion au port 18789 sur la machine distante où la Passerelle est en cours d'exécution.
