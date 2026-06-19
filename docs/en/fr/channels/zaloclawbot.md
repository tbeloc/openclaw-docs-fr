---
summary: "Configuration du canal Zalo ClawBot via le plugin externe openclaw-zaloclawbot"
read_when:
  - Vous souhaitez un bot assistant Zalo personnel avec connexion par code QR
  - Vous installez ou dépannez le plugin de canal openclaw-zaloclawbot
title: "Zalo ClawBot"
---

OpenClaw se connecte à Zalo ClawBot via le plugin externe `@zalo-platforms/openclaw-zaloclawbot` listé dans le catalogue. La connexion utilise un code QR de Mini App Zalo.

## Compatibilité

| Version du Plugin | Version OpenClaw | npm dist-tag | Statut        |
| ----------------- | ----------------- | ------------ | ------------- |
| 0.1.x             | >=2026.4.10       | `latest`     | Active / Beta |

## Prérequis

- Node.js **>= 22**
- [OpenClaw](https://docs.openclaw.ai/install) doit être installé (CLI `openclaw` disponible).
- Un compte Zalo sur un appareil mobile pour scanner le code QR de connexion.

## Installation avec l'assistant d'intégration (recommandé)

Exécutez l'assistant d'intégration OpenClaw et sélectionnez **Zalo ClawBot** dans le menu des canaux :

```bash
openclaw onboard
```

L'assistant installe le plugin depuis le catalogue officiel (vérification d'intégrité), affiche le code QR de connexion directement dans le terminal, et finalise le canal une fois que vous l'avez scanné avec l'application Zalo. Aucune commande supplémentaire n'est nécessaire.

## Installation manuelle

Pour ajouter le canal à une passerelle déjà intégrée, suivez ces étapes :

### 1. Installer le plugin

```bash
openclaw plugins install "@zalo-platforms/openclaw-zaloclawbot@0.1.4"
```

Utilisez la version exacte épinglée ci-dessus (elle correspond à l'entrée du catalogue officiel), afin qu'OpenClaw vérifie le paquet par rapport au hash d'intégrité du catalogue lors de l'installation.

### 2. Activer le plugin dans la configuration

```bash
openclaw config set plugins.entries.openclaw-zaloclawbot.enabled true
```

### 3. Générer le code QR et se connecter

```bash
openclaw channels login --channel openclaw-zaloclawbot
```

Scannez le code QR affiché dans le terminal à l'aide de l'application mobile Zalo, acceptez les Conditions d'utilisation dans la Mini App Zalo, et autorisez la session.

### 4. Redémarrer la passerelle

```bash
openclaw gateway restart
```

---

## Fonctionnement

Contrairement au canal Zalo développeur standard qui vous oblige à enregistrer votre propre Compte Officiel Zalo (OA) et à coller des identifiants développeur statiques, Zalo ClawBot fonctionne comme un **assistant personnel lié au propriétaire** utilisant une infrastructure officielle partagée :

1. **Intégration sécurisée :** Le code QR se résout en une Mini App Zalo sécurisée qui lie un bot nouvellement provisionné et privé sous un OA officiel partagé directement à votre ID utilisateur Zalo.
2. **Confidentialité liée au propriétaire :** Par conception, le bot est limité à la communication _uniquement_ avec son propriétaire. Les messages d'autres utilisateurs sont supprimés au niveau de la plateforme, rendant la connexion privée et sécurisée.
3. **Chemin API officiel :** Le plugin utilise les API Zalo Bot Platform au lieu de l'automatisation de navigateur ou de session web.

## Sous le capot

Le plugin Zalo ClawBot communique avec les API Zalo via une boucle de messages avec interrogation longue persistante. Pour maintenir un runtime propre et léger :

- Les connexions d'interrogation longue utilisent le point de terminaison `getUpdates`.
- Les webhooks sont désactivés par défaut pour les exécutions de passerelle locale sur bureau/terminal.
- Les messages sont traités côté client et mappés directement à votre runtime d'agent local.

Le plugin externe gère les identifiants du bot dans le répertoire d'état OpenClaw. Traitez ce répertoire comme sensible et incluez-le dans la même politique de contrôle d'accès et de sauvegarde que le reste de votre état OpenClaw.

---

## Dépannage

- **Délai d'expiration de la connexion QR :** Le jeton de connexion (`zbsk`) expire après 5 minutes pour des raisons de sécurité. Si le code QR expire avant que vous le scanniez, réexécutez simplement la commande de connexion pour en générer un nouveau.
- **La passerelle ne se charge pas :** Assurez-vous que votre version d'hôte OpenClaw est `2026.4.10` ou supérieure. Les versions antérieures ne supportent pas le registre d'installation de plugin npm externe.
