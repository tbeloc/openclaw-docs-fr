---
read_when:
  - 安装 OpenClaw
  - 你想从 GitHub 安装
summary: 安装 OpenClaw（推荐安装器、全局安装或从源代码安装）
title: 安装
x-i18n:
  generated_at: "2026-02-03T10:07:43Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b26f48c116c26c163ee0090fb4c3e29622951bd427ecaeccba7641d97cfdf17a
  source_path: install/index.md
  workflow: 15
---

# Installation

Sauf raison particulière, veuillez utiliser l'installateur. Il configurera l'interface de ligne de commande et exécutera l'assistant d'intégration.

## Installation rapide (recommandée)

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Windows (PowerShell) :

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

Étapes suivantes (si vous avez ignoré l'assistant d'intégration) :

```bash
openclaw onboard --install-daemon
```

## Configuration requise

- **Node >=22**
- macOS, Linux ou Windows via WSL2
- `pnpm` requis uniquement lors de la construction à partir du code source

## Choisir votre chemin d'installation

### 1) Script d'installation (recommandé)

Installez `openclaw` globalement via npm et exécutez l'assistant d'intégration.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Drapeaux de l'installateur :

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --help
```

Détails : [Fonctionnement interne de l'installateur](/install/installer).

Non-interactif (ignorer l'assistant d'intégration) :

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

### 2) Installation globale (manuelle)

Si vous avez déjà Node :

```bash
npm install -g openclaw@latest
```

Si vous avez libvips installé globalement (courant sur macOS via Homebrew) et que l'installation de `sharp` échoue, forcez l'utilisation de binaires précompilés :

```bash
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
```

Si vous voyez `sharp: Please add node-gyp to your dependencies`, installez soit les outils de construction (macOS : Xcode CLT + `npm install -g node-gyp`), soit utilisez la solution de contournement `SHARP_IGNORE_GLOBAL_LIBVIPS=1` ci-dessus pour ignorer la construction native.

Ou utilisez pnpm :

```bash
pnpm add -g openclaw@latest
pnpm approve-builds -g                # Approuvez openclaw, node-llama-cpp, sharp, etc.
pnpm add -g openclaw@latest           # Réexécutez pour exécuter les scripts postinstall
```

pnpm nécessite une approbation explicite des packages avec des scripts de construction. Après le premier avertissement "Ignored build scripts" lors de l'installation, exécutez `pnpm approve-builds -g` et sélectionnez les packages listés, puis réexécutez l'installation pour exécuter les scripts postinstall.

Ensuite :

```bash
openclaw onboard --install-daemon
```

### 3) À partir du code source (contributeurs/développement)

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build # Installe automatiquement les dépendances de l'interface utilisateur à la première exécution
pnpm build
openclaw onboard --install-daemon
```

Conseil : Si vous n'avez pas d'installation globale, exécutez les commandes du dépôt via `pnpm openclaw ...`.

### 4) Autres options d'installation

- Docker : [Docker](/install/docker)
- Nix : [Nix](/install/nix)
- Ansible : [Ansible](/install/ansible)
- Bun (CLI uniquement) : [Bun](/install/bun)

## Après l'installation

- Exécutez l'assistant d'intégration : `openclaw onboard --install-daemon`
- Vérification rapide : `openclaw doctor`
- Vérifiez l'état de santé de la passerelle : `openclaw status` + `openclaw health`
- Ouvrez le tableau de bord : `openclaw dashboard`

## Méthodes d'installation : npm vs git (installateur)

L'installateur prend en charge deux méthodes :

- `npm` (par défaut) : `npm install -g openclaw@latest`
- `git` : Clonez/construisez à partir de GitHub et exécutez à partir du code source

### Drapeaux CLI

```bash
# npm explicite
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method npm

# Installation à partir de GitHub (extraction du code source)
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
```

Drapeaux courants :

- `--install-method npm|git`
- `--git-dir <path>` (par défaut : `~/openclaw`)
- `--no-git-update` (ignorer `git pull` lors de l'utilisation d'une extraction existante)
- `--no-prompt` (désactiver les invites ; requis en CI/automatisation)
- `--dry-run` (imprimer les opérations à effectuer ; ne rien modifier)
- `--no-onboard` (ignorer l'assistant d'intégration)

### Variables d'environnement

Variables d'environnement équivalentes (utiles pour l'automatisation) :

- `OPENCLAW_INSTALL_METHOD=git|npm`
- `OPENCLAW_GIT_DIR=...`
- `OPENCLAW_GIT_UPDATE=0|1`
- `OPENCLAW_NO_PROMPT=1`
- `OPENCLAW_DRY_RUN=1`
- `OPENCLAW_NO_ONBOARD=1`
- `SHARP_IGNORE_GLOBAL_LIBVIPS=0|1` (par défaut : `1` ; éviter que `sharp` ne se construise par rapport à libvips système)

## Dépannage : `openclaw` introuvable (PATH)

Diagnostic rapide :

```bash
node -v
npm -v
npm prefix -g
echo "$PATH"
```

Si `$(npm prefix -g)/bin` (macOS/Linux) ou `$(npm prefix -g)` (Windows) **n'est pas** dans la sortie de `echo "$PATH"`, votre shell ne peut pas trouver les binaires npm globaux (y compris `openclaw`).

Correction : Ajoutez-le à votre fichier de démarrage du shell (zsh : `~/.zshrc`, bash : `~/.bashrc`) :

```bash
# macOS / Linux
export PATH="$(npm prefix -g)/bin:$PATH"
```

Sur Windows, ajoutez la sortie de `npm prefix -g` à votre PATH.

Ouvrez ensuite un nouveau terminal (ou exécutez `rehash` dans zsh / `hash -r` dans bash).

## Mise à jour/Désinstallation

- Mise à jour : [Mise à jour](/install/updating)
- Migration vers une nouvelle machine : [Migration](/install/migrating)
- Désinstallation : [Désinstallation](/install/uninstall)
