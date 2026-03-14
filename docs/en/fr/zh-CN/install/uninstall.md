---
read_when:
  - 你想从机器上移除 OpenClaw
  - 卸载后 Gateway 网关服务仍在运行
summary: 完全卸载 OpenClaw（CLI、服务、状态、工作区）
title: 卸载
x-i18n:
  generated_at: "2026-02-03T07:50:10Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 6673a755c5e1f90a807dd8ac92a774cff6d1bc97d125c75e8bf72a40e952a777
  source_path: install/uninstall.md
  workflow: 15
---

# Désinstallation

Deux méthodes :

- Si `openclaw` est toujours installé, utilisez la **méthode simple**.
- Si le CLI a été supprimé mais le service s'exécute toujours, utilisez la **suppression manuelle du service**.

## Méthode simple (CLI toujours installé)

Recommandé : utilisez le programme de désinstallation intégré :

```bash
openclaw uninstall
```

Non-interactif (automatisation / npx) :

```bash
openclaw uninstall --all --yes --non-interactive
npx -y openclaw uninstall --all --yes --non-interactive
```

Étapes manuelles (effet identique) :

1. Arrêtez le service Gateway :

```bash
openclaw gateway stop
```

2. Désinstallez le service Gateway (launchd/systemd/schtasks) :

```bash
openclaw gateway uninstall
```

3. Supprimez l'état + la configuration :

```bash
rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
```

Si vous avez défini `OPENCLAW_CONFIG_PATH` à un emplacement personnalisé en dehors du répertoire d'état, supprimez également ce fichier.

4. Supprimez votre espace de travail (optionnel, supprime les fichiers d'agent) :

```bash
rm -rf ~/.openclaw/workspace
```

5. Supprimez l'installation du CLI (choisissez celle que vous avez utilisée) :

```bash
npm rm -g openclaw
pnpm remove -g openclaw
bun remove -g openclaw
```

6. Si vous avez installé l'application macOS :

```bash
rm -rf /Applications/OpenClaw.app
```

Remarques :

- Si vous avez utilisé un profil (`--profile` / `OPENCLAW_PROFILE`), répétez l'étape 3 pour chaque répertoire d'état (par défaut `~/.openclaw-<profile>`).
- En mode distant, le répertoire d'état se trouve sur l'**hôte Gateway**, vous devez donc y exécuter les étapes 1-4 également.

## Suppression manuelle du service (CLI non installé)

Utilisez cette méthode si le service Gateway continue de s'exécuter mais que `openclaw` est manquant.

### macOS (launchd)

L'étiquette par défaut est `bot.molt.gateway` (ou `bot.molt.<profile>` ; les anciennes versions `com.openclaw.*` peuvent toujours exister) :

```bash
launchctl bootout gui/$UID/bot.molt.gateway
rm -f ~/Library/LaunchAgents/bot.molt.gateway.plist
```

Si vous avez utilisé un profil, remplacez l'étiquette et le nom du plist par `bot.molt.<profile>`. S'il existe des anciens plist `com.openclaw.*`, supprimez-les.

### Linux (unités utilisateur systemd)

Le nom d'unité par défaut est `openclaw-gateway.service` (ou `openclaw-gateway-<profile>.service`) :

```bash
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

### Windows (Tâches planifiées)

Le nom de tâche par défaut est `OpenClaw Gateway` (ou `OpenClaw Gateway (<profile>)`).
Le script de tâche se trouve dans votre répertoire d'état.

```powershell
schtasks /Delete /F /TN "OpenClaw Gateway"
Remove-Item -Force "$env:USERPROFILE\.openclaw\gateway.cmd"
```

Si vous avez utilisé un profil, supprimez le nom de tâche correspondant et `~\.openclaw-<profile>\gateway.cmd`.

## Installation standard vs extraction de source

### Installation standard (install.sh / npm / pnpm / bun)

Si vous avez utilisé `https://openclaw.ai/install.sh` ou `install.ps1`, le CLI a été installé via `npm install -g openclaw@latest`.
Supprimez-le avec `npm rm -g openclaw` (ou `pnpm remove -g` / `bun remove -g`, si c'est la méthode que vous avez utilisée).

### Extraction de source (git clone)

Si vous exécutez depuis une extraction de référentiel (`git clone` + `openclaw ...` / `bun run openclaw ...`) :

1. Désinstallez le service Gateway **avant** de supprimer le référentiel (utilisez la méthode simple ci-dessus ou la suppression manuelle du service).
2. Supprimez le répertoire du référentiel.
3. Supprimez l'état + l'espace de travail comme décrit ci-dessus.
