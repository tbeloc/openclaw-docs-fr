---
summary: "Configuration du canal WeChat via le plugin externe openclaw-weixin"
read_when:
  - You want to connect OpenClaw to WeChat or Weixin
  - You are installing or troubleshooting the openclaw-weixin channel plugin
  - You need to understand how external channel plugins run beside the Gateway
title: "WeChat"
---

# WeChat

OpenClaw se connecte à WeChat via le plugin de canal externe `@tencent-weixin/openclaw-weixin` de Tencent.

Statut : plugin externe. Les chats directs et les médias sont supportés. Les chats de groupe ne sont pas annoncés par les métadonnées de capacité du plugin actuel.

## Nomenclature

- **WeChat** est le nom visible pour l'utilisateur dans cette documentation.
- **Weixin** est le nom utilisé par le package de Tencent et par l'identifiant du plugin.
- `openclaw-weixin` est l'identifiant du canal OpenClaw.
- `@tencent-weixin/openclaw-weixin` est le package npm.

Utilisez `openclaw-weixin` dans les commandes CLI et les chemins de configuration.

## Fonctionnement

Le code WeChat ne se trouve pas dans le dépôt principal d'OpenClaw. OpenClaw fournit le contrat générique du plugin de canal, et le plugin externe fournit le runtime spécifique à WeChat :

1. `openclaw plugins install` installe `@tencent-weixin/openclaw-weixin`.
2. La Gateway découvre le manifeste du plugin et charge le point d'entrée du plugin.
3. Le plugin enregistre l'identifiant du canal `openclaw-weixin`.
4. `openclaw channels login --channel openclaw-weixin` démarre la connexion par code QR.
5. Le plugin stocke les identifiants du compte dans le répertoire d'état d'OpenClaw.
6. Lorsque la Gateway démarre, le plugin démarre son moniteur Weixin pour chaque compte configuré.
7. Les messages WeChat entrants sont normalisés via le contrat du canal, routés vers l'agent OpenClaw sélectionné, et renvoyés via le chemin sortant du plugin.

Cette séparation est importante : le cœur d'OpenClaw doit rester agnostique aux canaux. La connexion WeChat, les appels API Tencent iLink, le téléchargement/téléversement de médias, les jetons de contexte et la surveillance des comptes sont gérés par le plugin externe.

## Installation

Installation rapide :

```bash
npx -y @tencent-weixin/openclaw-weixin-cli install
```

Installation manuelle :

```bash
openclaw plugins install "@tencent-weixin/openclaw-weixin"
openclaw config set plugins.entries.openclaw-weixin.enabled true
```

Redémarrez la Gateway après l'installation :

```bash
openclaw gateway restart
```

## Connexion

Exécutez la connexion par code QR sur la même machine que celle qui exécute la Gateway :

```bash
openclaw channels login --channel openclaw-weixin
```

Scannez le code QR avec WeChat sur votre téléphone et confirmez la connexion. Le plugin enregistre le jeton du compte localement après un scan réussi.

Pour ajouter un autre compte WeChat, exécutez la même commande de connexion. Pour plusieurs comptes, isolez les sessions de messages directs par compte, canal et expéditeur :

```bash
openclaw config set session.dmScope per-account-channel-peer
```

## Contrôle d'accès

Les messages directs utilisent le modèle normal d'appairage et de liste d'autorisation d'OpenClaw pour les plugins de canal.

Approuvez les nouveaux expéditeurs :

```bash
openclaw pairing list openclaw-weixin
openclaw pairing approve openclaw-weixin <CODE>
```

Pour le modèle complet de contrôle d'accès, consultez [Appairage](/fr/channels/pairing).

## Compatibilité

Le plugin vérifie la version d'OpenClaw de l'hôte au démarrage.

| Ligne du plugin | Version d'OpenClaw      | Balise npm |
| --------------- | ----------------------- | ---------- |
| `2.x`           | `>=2026.3.22`           | `latest`   |
| `1.x`           | `>=2026.1.0 <2026.3.22` | `legacy`   |

Si le plugin signale que votre version d'OpenClaw est trop ancienne, mettez à jour OpenClaw ou installez la ligne de plugin héritée :

```bash
openclaw plugins install @tencent-weixin/openclaw-weixin@legacy
```

## Processus auxiliaire

Le plugin WeChat peut exécuter des tâches auxiliaires à côté de la Gateway tout en surveillant l'API Tencent iLink. Dans le problème #68451, ce chemin auxiliaire a exposé un bug dans le nettoyage générique de Gateway obsolète d'OpenClaw : un processus enfant pouvait essayer de nettoyer le processus Gateway parent, causant des boucles de redémarrage sous les gestionnaires de processus tels que systemd.

Le nettoyage de démarrage actuel d'OpenClaw exclut le processus actuel et ses ancêtres, donc un assistant de canal ne doit pas arrêter la Gateway qui l'a lancé. Ce correctif est générique ; ce n'est pas un chemin spécifique à WeChat dans le cœur.

## Dépannage

Vérifiez l'installation et le statut :

```bash
openclaw plugins list
openclaw channels status --probe
openclaw --version
```

Si le canal s'affiche comme installé mais ne se connecte pas, confirmez que le plugin est activé et redémarrez :

```bash
openclaw config set plugins.entries.openclaw-weixin.enabled true
openclaw gateway restart
```

Si la Gateway redémarre à plusieurs reprises après l'activation de WeChat, mettez à jour OpenClaw et le plugin :

```bash
npm view @tencent-weixin/openclaw-weixin version
openclaw plugins install "@tencent-weixin/openclaw-weixin" --force
openclaw gateway restart
```

Désactivation temporaire :

```bash
openclaw config set plugins.entries.openclaw-weixin.enabled false
openclaw gateway restart
```

## Documentation connexe

- Aperçu des canaux : [Canaux de chat](/fr/channels)
- Appairage : [Appairage](/fr/channels/pairing)
- Routage des canaux : [Routage des canaux](/fr/channels/channel-routing)
- Architecture des plugins : [Architecture des plugins](/fr/plugins/architecture)
- SDK des plugins de canal : [SDK des plugins de canal](/fr/plugins/sdk-channel-plugins)
- Package externe : [@tencent-weixin/openclaw-weixin](https://www.npmjs.com/package/@tencent-weixin/openclaw-weixin)
