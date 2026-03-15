---
summary: "Application Android (nœud) : runbook de connexion + surface de commande Connect/Chat/Voice/Canvas"
read_when:
  - Appairage ou reconnexion du nœud Android
  - Débogage de la découverte de passerelle Android ou de l'authentification
  - Vérification de la parité de l'historique de chat entre les clients
title: "Application Android"
---

# Application Android (Nœud)

> **Remarque :** L'application Android n'a pas encore été publiquement lancée. Le code source est disponible dans le [référentiel OpenClaw](https://github.com/openclaw/openclaw) sous `apps/android`. Vous pouvez le compiler vous-même en utilisant Java 17 et le SDK Android (`./gradlew :app:assembleDebug`). Consultez [apps/android/README.md](https://github.com/openclaw/openclaw/blob/main/apps/android/README.md) pour les instructions de compilation.

## Aperçu du support

- Rôle : application nœud compagnon (Android n'héberge pas la passerelle).
- Passerelle requise : oui (exécutez-la sur macOS, Linux ou Windows via WSL2).
- Installation : [Démarrage](/start/getting-started) + [Appairage](/channels/pairing).
- Passerelle : [Runbook](/gateway) + [Configuration](/gateway/configuration).
  - Protocoles : [Protocole de passerelle](/gateway/protocol) (nœuds + plan de contrôle).

## Contrôle système

Le contrôle système (launchd/systemd) réside sur l'hôte de la passerelle. Voir [Passerelle](/gateway).

## Runbook de connexion

Nœud application Android ⇄ (mDNS/NSD + WebSocket) ⇄ **Passerelle**

Android se connecte directement à la WebSocket de la passerelle (par défaut `ws://<host>:18789`) et utilise l'appairage d'appareil (`role: node`).

### Prérequis

- Vous pouvez exécuter la passerelle sur la machine « maître ».
- L'appareil/émulateur Android peut atteindre la WebSocket de la passerelle :
  - Même LAN avec mDNS/NSD, **ou**
  - Même tailnet Tailscale utilisant Wide-Area Bonjour / unicast DNS-SD (voir ci-dessous), **ou**
  - Hôte/port de passerelle manuel (secours)
- Vous pouvez exécuter l'interface de ligne de commande (`openclaw`) sur la machine de la passerelle (ou via SSH).

### 1) Démarrer la passerelle

```bash
openclaw gateway --port 18789 --verbose
```

Confirmez dans les journaux que vous voyez quelque chose comme :

- `listening on ws://0.0.0.0:18789`

Pour les configurations réservées au tailnet (recommandé pour Vienne ⇄ Londres), liez la passerelle à l'IP du tailnet :

- Définissez `gateway.bind: "tailnet"` dans `~/.openclaw/openclaw.json` sur l'hôte de la passerelle.
- Redémarrez la passerelle / application de barre de menus macOS.

### 2) Vérifier la découverte (optionnel)

À partir de la machine de la passerelle :

```bash
dns-sd -B _openclaw-gw._tcp local.
```

Plus de notes de débogage : [Bonjour](/gateway/bonjour).

#### Découverte Tailnet (Vienne ⇄ Londres) via unicast DNS-SD

La découverte NSD/mDNS d'Android ne traversera pas les réseaux. Si votre nœud Android et la passerelle se trouvent sur des réseaux différents mais sont connectés via Tailscale, utilisez plutôt Wide-Area Bonjour / unicast DNS-SD :

1. Configurez une zone DNS-SD (exemple `openclaw.internal.`) sur l'hôte de la passerelle et publiez les enregistrements `_openclaw-gw._tcp`.
2. Configurez le DNS fractionné de Tailscale pour votre domaine choisi pointant vers ce serveur DNS.

Détails et exemple de configuration CoreDNS : [Bonjour](/gateway/bonjour).

### 3) Se connecter depuis Android

Dans l'application Android :

- L'application maintient sa connexion à la passerelle active via un **service de premier plan** (notification persistante).
- Ouvrez l'onglet **Connexion**.
- Utilisez le mode **Code de configuration** ou **Manuel**.
- Si la découverte est bloquée, utilisez l'hôte/port manuel (et TLS/token/mot de passe si nécessaire) dans les **contrôles avancés**.

Après le premier appairage réussi, Android se reconnecte automatiquement au lancement :

- Point de terminaison manuel (s'il est activé), sinon
- La dernière passerelle découverte (meilleur effort).

### 4) Approuver l'appairage (CLI)

Sur la machine de la passerelle :

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
```

Détails d'appairage : [Appairage](/channels/pairing).

### 5) Vérifier que le nœud est connecté

- Via l'état des nœuds :

  ```bash
  openclaw nodes status
  ```

- Via la passerelle :

  ```bash
  openclaw gateway call node.list --params "{}"
  ```

### 6) Chat + historique

L'onglet Chat Android prend en charge la sélection de session (par défaut `main`, plus d'autres sessions existantes) :

- Historique : `chat.history`
- Envoyer : `chat.send`
- Mises à jour push (meilleur effort) : `chat.subscribe` → `event:"chat"`

### 7) Canvas + caméra

#### Hôte Canvas de passerelle (recommandé pour le contenu web)

Si vous souhaitez que le nœud affiche du vrai HTML/CSS/JS que l'agent peut modifier sur le disque, pointez le nœud vers l'hôte canvas de la passerelle.

Remarque : les nœuds chargent le canvas à partir du serveur HTTP de la passerelle (même port que `gateway.port`, par défaut `18789`).

1. Créez `~/.openclaw/workspace/canvas/index.html` sur l'hôte de la passerelle.

2. Naviguez le nœud vers celui-ci (LAN) :

```bash
openclaw nodes invoke --node "<Android Node>" --command canvas.navigate --params '{"url":"http://<gateway-hostname>.local:18789/__openclaw__/canvas/"}'
```

Tailnet (optionnel) : si les deux appareils sont sur Tailscale, utilisez un nom MagicDNS ou une IP tailnet au lieu de `.local`, par exemple `http://<gateway-magicdns>:18789/__openclaw__/canvas/`.

Ce serveur injecte un client de rechargement en direct dans le HTML et recharge lors des modifications de fichiers.
L'hôte A2UI se trouve à `http://<gateway-host>:18789/__openclaw__/a2ui/`.

Commandes Canvas (premier plan uniquement) :

- `canvas.eval`, `canvas.snapshot`, `canvas.navigate` (utilisez `{"url":""}` ou `{"url":"/"}` pour revenir à l'échafaudage par défaut). `canvas.snapshot` retourne `{ format, base64 }` (par défaut `format="jpeg"`).
- A2UI : `canvas.a2ui.push`, `canvas.a2ui.reset` (alias hérité `canvas.a2ui.pushJSONL`)

Commandes de caméra (premier plan uniquement ; contrôlées par permission) :

- `camera.snap` (jpg)
- `camera.clip` (mp4)

Voir [Nœud caméra](/nodes/camera) pour les paramètres et les assistants CLI.

### 8) Voice + surface de commande Android étendue

- Voice : Android utilise un flux unique d'activation/désactivation du microphone dans l'onglet Voice avec capture de transcription et lecture TTS (ElevenLabs si configuré, secours TTS système). La voix s'arrête lorsque l'application quitte le premier plan.
- Les bascules de réveil vocal/mode conversation sont actuellement supprimées de l'UX/runtime Android.
- Familles de commandes Android supplémentaires (la disponibilité dépend de l'appareil + permissions) :
  - `device.status`, `device.info`, `device.permissions`, `device.health`
  - `notifications.list`, `notifications.actions`
  - `photos.latest`
  - `contacts.search`, `contacts.add`
  - `calendar.events`, `calendar.add`
  - `callLog.search`
  - `motion.activity`, `motion.pedometer`
