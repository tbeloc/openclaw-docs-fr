---
summary: "Corriger les problèmes de démarrage CDP Chrome/Brave/Edge/Chromium pour le contrôle du navigateur OpenClaw sur Linux"
read_when: "Le contrôle du navigateur échoue sur Linux, en particulier avec Chromium snap"
title: "Dépannage du navigateur"
---

# Dépannage du navigateur (Linux)

## Problème : « Impossible de démarrer Chrome CDP sur le port 18800 »

Le serveur de contrôle du navigateur OpenClaw ne parvient pas à lancer Chrome/Brave/Edge/Chromium avec l'erreur :

```
{"error":"Error: Failed to start Chrome CDP on port 18800 for profile \"openclaw\"."}
```

### Cause racine

Sur Ubuntu (et de nombreuses distributions Linux), l'installation Chromium par défaut est un **paquet snap**. Le confinement AppArmor de Snap interfère avec la façon dont OpenClaw génère et surveille le processus du navigateur.

La commande `apt install chromium` installe un paquet stub qui redirige vers snap :

```
Note, selecting 'chromium-browser' instead of 'chromium'
chromium-browser is already the newest version (2:1snap1-0ubuntu2).
```

Ce n'est PAS un vrai navigateur — c'est juste un wrapper.

### Solution 1 : Installer Google Chrome (Recommandé)

Installez le paquet officiel Google Chrome `.deb`, qui n'est pas sandboxé par snap :

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y  # en cas d'erreurs de dépendances
```

Ensuite, mettez à jour votre configuration OpenClaw (`~/.openclaw/openclaw.json`) :

```json
{
  "browser": {
    "enabled": true,
    "executablePath": "/usr/bin/google-chrome-stable",
    "headless": true,
    "noSandbox": true
  }
}
```

### Solution 2 : Utiliser Snap Chromium en mode Attach-Only

Si vous devez utiliser snap Chromium, configurez OpenClaw pour se connecter à un navigateur démarré manuellement :

1. Mettez à jour la configuration :

```json
{
  "browser": {
    "enabled": true,
    "attachOnly": true,
    "headless": true,
    "noSandbox": true
  }
}
```

2. Démarrez Chromium manuellement :

```bash
chromium-browser --headless --no-sandbox --disable-gpu \
  --remote-debugging-port=18800 \
  --user-data-dir=$HOME/.openclaw/browser/openclaw/user-data \
  about:blank &
```

3. Créez optionnellement un service utilisateur systemd pour démarrer automatiquement Chrome :

```ini
# ~/.config/systemd/user/openclaw-browser.service
[Unit]
Description=OpenClaw Browser (Chrome CDP)
After=network.target

[Service]
ExecStart=/snap/bin/chromium --headless --no-sandbox --disable-gpu --remote-debugging-port=18800 --user-data-dir=%h/.openclaw/browser/openclaw/user-data about:blank
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

Activez avec : `systemctl --user enable --now openclaw-browser.service`

### Vérifier que le navigateur fonctionne

Vérifiez l'état :

```bash
curl -s http://127.0.0.1:18791/ | jq '{running, pid, chosenBrowser}'
```

Testez la navigation :

```bash
curl -s -X POST http://127.0.0.1:18791/start
curl -s http://127.0.0.1:18791/tabs
```

### Référence de configuration

| Option                   | Description                                                          | Défaut                                                      |
| ------------------------ | -------------------------------------------------------------------- | ----------------------------------------------------------- |
| `browser.enabled`        | Activer le contrôle du navigateur                                    | `true`                                                      |
| `browser.executablePath` | Chemin vers un binaire de navigateur basé sur Chromium (Chrome/Brave/Edge/Chromium) | auto-détecté (préfère le navigateur par défaut basé sur Chromium) |
| `browser.headless`       | Exécuter sans interface graphique                                    | `false`                                                     |
| `browser.noSandbox`      | Ajouter le drapeau `--no-sandbox` (nécessaire pour certaines configurations Linux) | `false`                                                     |
| `browser.attachOnly`     | Ne pas lancer le navigateur, seulement se connecter à un existant    | `false`                                                     |
| `browser.cdpPort`        | Port du protocole Chrome DevTools                                    | `18800`                                                     |

### Problème : « L'extension relay Chrome est en cours d'exécution, mais aucun onglet n'est connecté »

Vous utilisez le profil `chrome` (extension relay). Il s'attend à ce que l'extension du navigateur OpenClaw soit attachée à un onglet actif.

Options de correction :

1. **Utilisez le navigateur géré :** `openclaw browser start --browser-profile openclaw`
   (ou définissez `browser.defaultProfile: "openclaw"`).
2. **Utilisez l'extension relay :** installez l'extension, ouvrez un onglet, et cliquez sur l'icône de l'extension OpenClaw pour l'attacher.

Remarques :

- Le profil `chrome` utilise votre **navigateur Chromium par défaut du système** si possible.
- Les profils `openclaw` locaux attribuent automatiquement `cdpPort`/`cdpUrl` ; définissez-les uniquement pour CDP distant.
