---
read_when:
  - 你想要可复现、可回滚的安装
  - 你已经在使用 Nix/NixOS/Home Manager
  - 你想要所有内容都固定并以声明式管理
summary: 使用 Nix 声明式安装 OpenClaw
title: Nix
x-i18n:
  generated_at: "2026-02-03T07:49:51Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: f1452194cfdd74613b5b3ab90b0d506eaea2d16b147497987710d6ad658312ba
  source_path: install/nix.md
  workflow: 15
---

# Installation Nix

La façon recommandée d'exécuter OpenClaw avec Nix est via **[nix-openclaw](https://github.com/openclaw/nix-openclaw)** — un module Home Manager prêt à l'emploi.

## Démarrage rapide

Collez ceci à votre agent IA (Claude, Cursor, etc.) :

```text
I want to set up nix-openclaw on my Mac.
Repository: github:openclaw/nix-openclaw

What I need you to do:
1. Check if Determinate Nix is installed (if not, install it)
2. Create a local flake at ~/code/openclaw-local using templates/agent-first/flake.nix
3. Help me create a Telegram bot (@BotFather) and get my chat ID (@userinfobot)
4. Set up secrets (bot token, Anthropic key) - plain files at ~/.secrets/ is fine
5. Fill in the template placeholders and run home-manager switch
6. Verify: launchd running, bot responds to messages

Reference the nix-openclaw README for module options.
```

> **📦 Guide complet : [github.com/openclaw/nix-openclaw](https://github.com/openclaw/nix-openclaw)**
>
> Le dépôt nix-openclaw est la source faisant autorité pour l'installation Nix. Cette page n'est qu'un aperçu rapide.

## Ce que vous obtiendrez

- Passerelle Gateway + application macOS + outils (whisper, spotify, cameras) — tous avec versions figées
- Service Launchd qui continue de fonctionner après redémarrage
- Système de plugins avec configuration déclarative
- Retour en arrière instantané : `home-manager switch --rollback`

---

## Comportement d'exécution en mode Nix

Lorsque `OPENCLAW_NIX_MODE=1` est défini (nix-openclaw le définit automatiquement) :

OpenClaw supporte le **mode Nix**, qui rend la configuration déterministe et désactive les processus d'installation automatique.
Activez-le en exportant la variable d'environnement suivante :

```bash
OPENCLAW_NIX_MODE=1
```

Sur macOS, les applications GUI n'héritent pas automatiquement des variables d'environnement shell. Vous pouvez également activer le mode Nix via defaults :

```bash
defaults write bot.molt.mac openclaw.nixMode -bool true
```

### Chemins de configuration + état

OpenClaw lit la configuration JSON5 depuis `OPENCLAW_CONFIG_PATH` et stocke les données mutables dans `OPENCLAW_STATE_DIR`.

- `OPENCLAW_STATE_DIR` (par défaut : `~/.openclaw`)
- `OPENCLAW_CONFIG_PATH` (par défaut : `$OPENCLAW_STATE_DIR/openclaw.json`)

Lors de l'exécution sous Nix, définissez explicitement ces chemins vers des emplacements gérés par Nix, afin que l'état d'exécution et la configuration ne se retrouvent pas dans le stockage immuable.

### Comportement d'exécution en mode Nix

- Les processus d'installation automatique et d'auto-modification sont désactivés
- Les dépendances manquantes affichent des messages de correction spécifiques à Nix
- L'interface utilisateur affiche une bannière de mode Nix en lecture seule le cas échéant

## Remarques sur l'empaquetage (macOS)

Le processus d'empaquetage macOS s'attend à trouver un modèle Info.plist stable à l'emplacement suivant :

```
apps/macos/Sources/OpenClaw/Resources/Info.plist
```

[`scripts/package-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/package-mac-app.sh) copie ce modèle dans le paquet d'application et corrige les champs dynamiques (ID de bundle, numéro de version/build, SHA Git, clé Sparkle). Cela rend le plist déterministe pour l'empaquetage SwiftPM et les constructions Nix (ils ne dépendent pas de la chaîne d'outils Xcode complète).

## Contenu connexe

- [nix-openclaw](https://github.com/openclaw/nix-openclaw) — Guide de configuration complet
- [Assistant](/start/wizard) — Configuration CLI non-Nix
- [Docker](/install/docker) — Configuration conteneurisée
