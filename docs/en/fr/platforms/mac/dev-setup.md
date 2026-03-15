---
summary: "Guide de configuration pour les développeurs travaillant sur l'application macOS OpenClaw"
read_when:
  - Setting up the macOS development environment
title: "Configuration du développement macOS"
---

# Configuration du développeur macOS

Ce guide couvre les étapes nécessaires pour construire et exécuter l'application macOS OpenClaw à partir des sources.

## Prérequis

Avant de construire l'application, assurez-vous que les éléments suivants sont installés :

1. **Xcode 26.2+** : Requis pour le développement Swift.
2. **Node.js 24 & pnpm** : Recommandé pour la passerelle, l'interface de ligne de commande et les scripts d'empaquetage. Node 22 LTS, actuellement `22.16+`, reste pris en charge pour la compatibilité.

## 1. Installer les dépendances

Installez les dépendances du projet :

```bash
pnpm install
```

## 2. Construire et empaqueter l'application

Pour construire l'application macOS et l'empaqueter dans `dist/OpenClaw.app`, exécutez :

```bash
./scripts/package-mac-app.sh
```

Si vous n'avez pas de certificat Apple Developer ID, le script utilisera automatiquement la **signature ad-hoc** (`-`).

Pour les modes d'exécution de développement, les drapeaux de signature et le dépannage de l'ID d'équipe, consultez le fichier README de l'application macOS :
[https://github.com/openclaw/openclaw/blob/main/apps/macos/README.md](https://github.com/openclaw/openclaw/blob/main/apps/macos/README.md)

> **Remarque** : Les applications signées ad-hoc peuvent déclencher des invites de sécurité. Si l'application se bloque immédiatement avec « Abort trap 6 », consultez la section [Dépannage](#dépannage).

## 3. Installer l'interface de ligne de commande

L'application macOS s'attend à une installation globale de l'interface de ligne de commande `openclaw` pour gérer les tâches en arrière-plan.

**Pour l'installer (recommandé) :**

1. Ouvrez l'application OpenClaw.
2. Allez à l'onglet des paramètres **Général**.
3. Cliquez sur **« Installer l'interface de ligne de commande »**.

Vous pouvez également l'installer manuellement :

```bash
npm install -g openclaw@<version>
```

## Dépannage

### La construction échoue : Incompatibilité de la chaîne d'outils ou du SDK

La construction de l'application macOS s'attend au dernier SDK macOS et à la chaîne d'outils Swift 6.2.

**Dépendances système (requises) :**

- **Dernière version de macOS disponible dans Mise à jour logicielle** (requise par les SDK Xcode 26.2)
- **Xcode 26.2** (chaîne d'outils Swift 6.2)

**Vérifications :**

```bash
xcodebuild -version
xcrun swift --version
```

Si les versions ne correspondent pas, mettez à jour macOS/Xcode et relancez la construction.

### L'application se bloque lors de l'octroi de permission

Si l'application se bloque lorsque vous essayez d'autoriser l'accès à la **Reconnaissance vocale** ou au **Microphone**, cela peut être dû à un cache TCC corrompu ou à une incompatibilité de signature.

**Solution :**

1. Réinitialisez les permissions TCC :

   ```bash
   tccutil reset All ai.openclaw.mac.debug
   ```

2. Si cela échoue, modifiez temporairement le `BUNDLE_ID` dans [`scripts/package-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/package-mac-app.sh) pour forcer un « démarrage propre » de macOS.

### La passerelle « Démarrage... » indéfiniment

Si l'état de la passerelle reste sur « Démarrage... », vérifiez si un processus zombie bloque le port :

```bash
openclaw gateway status
openclaw gateway stop

# Si vous n'utilisez pas de LaunchAgent (mode développement / exécutions manuelles), trouvez l'écouteur :
lsof -nP -iTCP:18789 -sTCP:LISTEN
```

Si une exécution manuelle bloque le port, arrêtez ce processus (Ctrl+C). En dernier recours, tuez le PID que vous avez trouvé ci-dessus.
