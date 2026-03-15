---
summary: "Désinstaller complètement OpenClaw (CLI, service, état, workspace)"
read_when:
  - You want to remove OpenClaw from a machine
  - The gateway service is still running after uninstall
title: "Désinstallation"
---

# Désinstallation

Deux chemins :

- **Chemin facile** si `openclaw` est toujours installé.
- **Suppression manuelle du service** si le CLI est parti mais le service fonctionne toujours.

## Chemin facile (CLI toujours installé)

Recommandé : utilisez le désinstalleur intégré :

```bash
openclaw uninstall
```

Non-interactif (automatisation / npx) :

```bash
openclaw uninstall --all --yes --non-interactive
npx -y openclaw uninstall --all --yes --non-interactive
```

Étapes manuelles (même résultat) :

1. Arrêtez le service de passerelle :

```bash
openclaw gateway stop
```

2. Désinstallez le service de passerelle (launchd/systemd/schtasks) :

```bash
openclaw gateway uninstall
```

3. Supprimez l'état + la configuration :

```bash
rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
```

Si vous avez défini `OPENCLAW_CONFIG_PATH` à un emplacement personnalisé en dehors du répertoire d'état, supprimez également ce fichier.

4. Supprimez votre workspace (optionnel, supprime les fichiers d'agent) :

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

Notes :

- Si vous avez utilisé des profils (`--profile` / `OPENCLAW_PROFILE`), répétez l'étape 3 pour chaque répertoire d'état (les valeurs par défaut sont `~/.openclaw-<profile>`).
- En mode distant, le répertoire d'état se trouve sur l'**hôte de passerelle**, donc exécutez également les étapes 1-4 là-bas.

## Suppression manuelle du service (CLI non installé)

Utilisez ceci si le service de passerelle continue de fonctionner mais que `openclaw` est manquant.

### macOS (launchd)

Le libellé par défaut est `ai.openclaw.gateway` (ou `ai.openclaw.<profile>` ; les anciens `com.openclaw.*` peuvent toujours exister) :

```bash
launchctl bootout gui/$UID/ai.openclaw.gateway
rm -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

Si vous avez utilisé un profil, remplacez le libellé et le nom du plist par `ai.openclaw.<profile>`. Supprimez tous les anciens plists `com.openclaw.*` s'ils sont présents.

### Linux (unité utilisateur systemd)

Le nom d'unité par défaut est `openclaw-gateway.service` (ou `openclaw-gateway-<profile>.service`) :

```bash
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

### Windows (Tâche planifiée)

Le nom de tâche par défaut est `OpenClaw Gateway` (ou `OpenClaw Gateway (<profile>)`).
Le script de tâche se trouve dans votre répertoire d'état.

```powershell
schtasks /Delete /F /TN "OpenClaw Gateway"
Remove-Item -Force "$env:USERPROFILE\.openclaw\gateway.cmd"
```

Si vous avez utilisé un profil, supprimez le nom de tâche correspondant et `~\.openclaw-<profile>\gateway.cmd`.

## Installation normale vs extraction de source

### Installation normale (install.sh / npm / pnpm / bun)

Si vous avez utilisé `https://openclaw.ai/install.sh` ou `install.ps1`, le CLI a été installé avec `npm install -g openclaw@latest`.
Supprimez-le avec `npm rm -g openclaw` (ou `pnpm remove -g` / `bun remove -g` si vous avez installé de cette façon).

### Extraction de source (git clone)

Si vous exécutez à partir d'une extraction de dépôt (`git clone` + `openclaw ...` / `bun run openclaw ...`) :

1. Désinstallez le service de passerelle **avant** de supprimer le dépôt (utilisez le chemin facile ci-dessus ou la suppression manuelle du service).
2. Supprimez le répertoire du dépôt.
3. Supprimez l'état + le workspace comme indiqué ci-dessus.
