---
read_when:
  - 设置 macOS 开发环境
summary: 为在 OpenClaw macOS 应用上工作的开发者提供的设置指南
title: macOS 开发设置
x-i18n:
  generated_at: "2026-02-03T07:52:36Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 4ea67701bd58b7512f945fce58d79e1b3d990fbf45183323a1e3ab9688827623
  source_path: platforms/mac/dev-setup.md
  workflow: 15
---

# Configuration de développement macOS

Ce guide couvre les étapes nécessaires pour construire et exécuter l'application OpenClaw macOS à partir du code source.

## Prérequis

Avant de construire l'application, assurez-vous d'avoir installé les éléments suivants :

1.  **Xcode 26.2+** : Requis pour le développement Swift.
2.  **Node.js 22+ & pnpm** : Requis pour la passerelle Gateway, l'interface CLI et les scripts d'empaquetage.

## 1. Installer les dépendances

Installez les dépendances au niveau du projet :

```bash
pnpm install
```

## 2. Construire et empaqueter l'application

Pour construire l'application macOS et l'empaqueter dans `dist/OpenClaw.app`, exécutez :

```bash
./scripts/package-mac-app.sh
```

Si vous n'avez pas de certificat Apple Developer ID, le script utilisera automatiquement la **signature ad-hoc** (`-`).

Pour plus d'informations sur les modes d'exécution de développement, les drapeaux de signature et la résolution des problèmes d'ID d'équipe, consultez le fichier README de l'application macOS :
https://github.com/openclaw/openclaw/blob/main/apps/macos/README.md

> **Remarque** : Les applications signées ad-hoc peuvent déclencher des avertissements de sécurité. Si l'application se bloque immédiatement avec "Abort trap 6", consultez la section [Dépannage](#dépannage).

## 3. Installer l'interface CLI

L'application macOS s'attend à ce que l'interface CLI `openclaw` soit installée globalement pour gérer les tâches en arrière-plan.

**Méthode d'installation (recommandée) :**

1.  Ouvrez l'application OpenClaw.
2.  Accédez à l'onglet des paramètres **General**.
3.  Cliquez sur **"Install CLI"**.

Ou installez manuellement :

```bash
npm install -g openclaw@<version>
```

## Dépannage

### Échec de la construction : chaîne d'outils ou SDK incompatible

La construction de l'application macOS s'attend au dernier SDK macOS et à la chaîne d'outils Swift 6.2.

**Dépendances système (obligatoires) :**

- **Dernière version de macOS disponible dans les mises à jour logicielles** (requise pour le SDK Xcode 26.2)
- **Xcode 26.2** (chaîne d'outils Swift 6.2)

**Vérification :**

```bash
xcodebuild -version
xcrun swift --version
```

Si les versions ne correspondent pas, mettez à jour macOS/Xcode et relancez la construction.

### L'application se bloque lors de l'octroi de permissions

Si l'application se bloque lors de la tentative d'autorisation d'accès à la **reconnaissance vocale** ou au **microphone**, cela peut être dû à un cache TCC corrompu ou à une incompatibilité de signature.

**Correction :**

1. Réinitialisez les permissions TCC :
   ```bash
   tccutil reset All bot.molt.mac.debug
   ```
2. Si cela ne fonctionne pas, modifiez temporairement le `BUNDLE_ID` dans [`scripts/package-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/package-mac-app.sh) pour forcer macOS à recommencer à partir d'un "état vierge".

### La passerelle Gateway reste indéfiniment "Starting..."

Si l'état de la passerelle Gateway reste bloqué sur "Starting...", vérifiez s'il y a des processus zombies occupant le port :

```bash
openclaw gateway status
openclaw gateway stop

# Si vous n'utilisez pas LaunchAgent (mode développement/exécution manuelle), trouvez l'écouteur :
lsof -nP -iTCP:18789 -sTCP:LISTEN
```

Si une exécution manuelle occupe le port, arrêtez ce processus (Ctrl+C). En dernier recours, tuez le PID que vous avez trouvé.
