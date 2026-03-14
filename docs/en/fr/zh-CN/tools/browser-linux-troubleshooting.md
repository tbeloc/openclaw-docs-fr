---
read_when: Browser control fails on Linux, especially with snap Chromium
summary: 修复 Linux 上 OpenClaw 浏览器控制的 Chrome/Brave/Edge/Chromium CDP 启动问题
title: 浏览器故障排除
x-i18n:
  generated_at: "2026-02-03T07:55:07Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: bac2301022511a0bf8ebe1309606cc03e8a979ff74866c894f89d280ca3e514e
  source_path: tools/browser-linux-troubleshooting.md
  workflow: 15
---

# Dépannage du navigateur (Linux)

## Problème : « Failed to start Chrome CDP on port 18800 »

Le serveur de contrôle du navigateur OpenClaw ne peut pas démarrer Chrome/Brave/Edge/Chromium avec l'erreur suivante :

```
{"error":"Error: Failed to start Chrome CDP on port 18800 for profile \"openclaw\"."}
```

### Cause racine

Sur Ubuntu (et de nombreuses distributions Linux), l'installation par défaut de Chromium est un **paquet snap**. Les restrictions AppArmor de Snap interfèrent avec la façon dont OpenClaw démarre et surveille les processus du navigateur.

La commande `apt install chromium` installe un paquet stub qui redirige vers snap :

```
Note, selecting 'chromium-browser' instead of 'chromium'
chromium-browser is already the newest version (2:1snap1-0ubuntu2).
```

Ce n'est pas un vrai navigateur — c'est juste un wrapper.

### Solution 1 : Installer Google Chrome (recommandé)

Installez le paquet officiel Google Chrome `.deb`, qui n'est pas soumis aux restrictions du bac à sable snap :

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y  # if there are dependency errors
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

### Solution 2 : Utiliser le mode attachement uniquement avec Snap Chromium

Si vous devez utiliser snap Chromium, configurez OpenClaw pour s'attacher à un navigateur lancé manuellement :

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

2. Lancez Chromium manuellement :

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

Activez-le : `systemctl --user enable --now openclaw-browser.service`

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

| Option                   | Description                                                                      | Valeur par défaut                                                |
| ------------------------ | -------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `browser.enabled`        | Activer le contrôle du navigateur                                               | `true`                                                           |
| `browser.executablePath` | Chemin vers le binaire du navigateur de type Chromium (Chrome/Brave/Edge/Chromium) | Détection automatique (priorité au navigateur par défaut Chromium) |
| `browser.headless`       | Exécuter sans GUI                                                                | `false`                                                          |
| `browser.noSandbox`      | Ajouter le drapeau `--no-sandbox` (requis pour certaines configurations Linux)   | `false`                                                          |
| `browser.attachOnly`     | Ne pas démarrer le navigateur, s'attacher uniquement à un navigateur existant    | `false`                                                          |
| `browser.cdpPort`        | Port du protocole Chrome DevTools                                                | `18800`                                                          |

### Problème : « Chrome extension relay is running, but no tab is connected »

Vous utilisez le profil `chrome` (relais d'extension). Il s'attend à ce que l'extension OpenClaw soit attachée à un onglet actif.

Options de correction :

1. **Utiliser un navigateur géré :** `openclaw browser start --browser-profile openclaw`
   (ou définir `browser.defaultProfile: "openclaw"`).
2. **Utiliser le relais d'extension :** Installez l'extension, ouvrez un onglet, puis cliquez sur l'icône de l'extension OpenClaw pour l'attacher.

Remarques :

- Le profil `chrome` utilise votre **navigateur Chromium par défaut du système** si possible.
- Le profil local `openclaw` attribue automatiquement `cdpPort`/`cdpUrl` ; définissez-les uniquement pour CDP distant.
