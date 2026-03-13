---
read_when:
  - 你想了解 `openclaw.ai/install.sh` 的工作机制
  - 你想自动化安装（CI / 无头环境）
  - 你想从 GitHub 检出安装
summary: 安装器脚本的工作原理（install.sh + install-cli.sh）、参数和自动化
title: 安装器内部机制
x-i18n:
  generated_at: "2026-02-01T21:07:55Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 9e0a19ecb5da0a395030e1ccf0d4bedf16b83946b3432c5399d448fe5d298391
  source_path: install/installer.md
  workflow: 14
---

# Mécanismes internes du programme d'installation

OpenClaw fournit deux scripts d'installation (hébergés sur `openclaw.ai`) :

- `https://openclaw.ai/install.sh` — Programme d'installation « recommandé » (installation npm globale par défaut ; peut également être installé à partir d'une extraction GitHub)
- `https://openclaw.ai/install-cli.sh` — Programme d'installation CLI sans privilèges root (installation dans un répertoire préfixé avec Node indépendant)
- `https://openclaw.ai/install.ps1` — Programme d'installation Windows PowerShell (npm par défaut ; installation git optionnelle)

Pour afficher les paramètres/comportements actuels, exécutez :

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --help
```

Aide Windows (PowerShell) :

```powershell
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -?
```

Si le programme d'installation se termine mais que vous ne trouvez pas `openclaw` dans un nouveau terminal, c'est généralement un problème de PATH Node/npm. Voir : [Installation](/install#nodejs--npm-path-sanity).

## install.sh (Recommandé)

Aperçu des fonctionnalités :

- Détecte le système d'exploitation (macOS / Linux / WSL).
- Assure Node.js **22+** (macOS via Homebrew ; Linux via NodeSource).
- Choisit la méthode d'installation :
  - `npm` (par défaut) : `npm install -g openclaw@latest`
  - `git` : Clone/construit l'extraction du code source et installe les scripts wrapper
- Sur Linux : bascule le préfixe npm vers `~/.npm-global` si nécessaire, pour éviter les erreurs de permissions npm globales.
- Si c'est une mise à niveau d'une installation existante : exécute `openclaw doctor --non-interactive` (meilleur effort).
- Pour les installations git : exécute `openclaw doctor --non-interactive` après installation/mise à jour (meilleur effort).
- Atténue les problèmes d'installation native `sharp` en définissant par défaut `SHARP_IGNORE_GLOBAL_LIBVIPS=1` (évite de compiler avec le libvips système).

Si vous *souhaitez* que `sharp` se lie au libvips installé globalement (ou si vous déboguez), définissez :

```bash
SHARP_IGNORE_GLOBAL_LIBVIPS=0 curl -fsSL https://openclaw.ai/install.sh | bash
```

### Découverte / Suggestion « installation git »

Si vous exécutez le programme d'installation dans un **répertoire d'extraction OpenClaw existant** (détecté via `package.json` + `pnpm-workspace.yaml`), il vous suggère :

- Mettre à jour et utiliser cette extraction (`git`)
- Ou migrer vers une installation npm globale (`npm`)

Dans un contexte non interactif (pas de TTY / `--no-prompt`), vous devez passer `--install-method git|npm` (ou définir `OPENCLAW_INSTALL_METHOD`), sinon le script quittera avec le code de sortie `2`.

### Pourquoi Git est nécessaire

Le chemin `--install-method git` (clone / pull) nécessite Git.

Pour les installations `npm`, Git n'est *généralement* pas nécessaire, mais certains environnements le nécessitent toujours (par exemple lors de la récupération de paquets ou de dépendances via des URL git). Le programme d'installation s'assure actuellement que Git existe pour éviter les erreurs `spawn git ENOENT` sur les distributions toutes neuves.

### Pourquoi npm signale `EACCES` sur une nouvelle Linux

Dans certaines configurations Linux (en particulier après l'installation de Node via le gestionnaire de paquets système ou NodeSource), le préfixe global de npm pointe vers un emplacement appartenant à root. À ce moment, `npm install -g ...` signale une erreur de permissions `EACCES` / `mkdir`.

`install.sh` atténue ce problème en basculant le préfixe vers :

- `~/.npm-global` (et l'ajoute à `PATH` dans `~/.bashrc` / `~/.zshrc` si elle existe)

## install-cli.sh (Programme d'installation CLI sans privilèges root)

Ce script installe `openclaw` dans un répertoire préfixé (par défaut : `~/.openclaw`), tout en installant un runtime Node dédié sous ce préfixe, ce qui permet de l'utiliser sur des machines où vous ne voulez pas modifier le Node/npm système.

Aide :

```bash
curl -fsSL https://openclaw.ai/install-cli.sh | bash -s -- --help
```

## install.ps1 (Windows PowerShell)

Aperçu des fonctionnalités :

- Assure Node.js **22+** (winget/Chocolatey/Scoop ou installation manuelle).
- Choisit la méthode d'installation :
  - `npm` (par défaut) : `npm install -g openclaw@latest`
  - `git` : Clone/construit l'extraction du code source et installe les scripts wrapper
- Exécute `openclaw doctor --non-interactive` lors des mises à niveau et des installations git (meilleur effort).

Exemples :

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex -InstallMethod git
```

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex -InstallMethod git -GitDir "C:\\openclaw"
```

Variables d'environnement :

- `OPENCLAW_INSTALL_METHOD=git|npm`
- `OPENCLAW_GIT_DIR=...`

Exigences Git :

Si vous choisissez `-InstallMethod git` mais que Git n'est pas installé, le programme d'installation affichera un lien vers Git for Windows (`https://git-scm.com/download/win`) et quittera.

Problèmes Windows courants :

- **npm error spawn git / ENOENT** : Installez Git for Windows et rouvrez PowerShell, puis réexécutez le programme d'installation.
- **« openclaw » n'est pas une commande reconnue** : Votre dossier bin global npm n'est pas dans PATH. La plupart des systèmes utilisent `%AppData%\\npm`. Vous pouvez également exécuter `npm config get prefix` et ajouter `\\bin` à PATH, puis rouvrir PowerShell.
