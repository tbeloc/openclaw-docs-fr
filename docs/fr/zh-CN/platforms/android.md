---
read_when:
  - Appairage ou reconnexion d'un nœud Android
  - Débogage de la découverte ou de l'authentification de la passerelle Android Gateway
  - Vérification de la cohérence de l'historique de chat entre clients
summary: Application Android (nœud) : Manuel de connexion + Canvas/Chat/Camera
title: Application Android
x-i18n:
  generated_at: "2026-02-03T07:51:34Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 9cd02f12065ce2bc483379c9afd7537489d9076094f4a412cf9f21ccc47f0e38
  source_path: platforms/android.md
  workflow: 15
---

# Application Android (nœud)

## Aperçu du support

- Rôle : Application nœud compagnon (Android n'héberge pas la passerelle Gateway).
- Nécessite une passerelle Gateway : Oui (s'exécutant sur macOS, Linux ou Windows via WSL2).
- Installation : [Guide de démarrage](/start/getting-started) + [Appairage](/gateway/pairing).
- Passerelle Gateway : [Manuel](/gateway) + [Configuration](/gateway/configuration).
  - Protocole : [Protocole Gateway](/gateway/protocol) (nœud + plan de contrôle).

## Contrôle système

Le contrôle système (launchd/systemd) se trouve sur l'hôte de la passerelle Gateway. Voir [Passerelle Gateway](/gateway).

## Manuel de connexion

Nœud Android ⇄ (mDNS/NSD + WebSocket) ⇄ **Passerelle Gateway**

Android se connecte directement au WebSocket de la passerelle Gateway (par défaut `ws://<host>:18789`) et utilise l'appairage détenu par la passerelle Gateway.

### Conditions préalables

- Vous pouvez exécuter la passerelle Gateway sur la machine « principale ».
- L'appareil/émulateur Android peut accéder au WebSocket de la passerelle Gateway :
  - Même réseau local utilisant mDNS/NSD, **ou**
  - Même tailnet Tailscale utilisant Wide-Area Bonjour / unicast DNS-SD (voir ci-dessous), **ou**
  - Hôte/port de passerelle Gateway manuel (plan de secours)
- Vous pouvez exécuter l'interface de ligne de commande (`openclaw`) sur la machine de la passerelle Gateway (ou via SSH).

### 1) Démarrer la passerelle Gateway

```bash
openclaw gateway --port 18789 --verbose
```

Confirmez dans les journaux que vous voyez quelque chose comme :

- `listening on ws://0.0.0.0:18789`

Pour une configuration tailnet uniquement (recommandée pour Vienne ⇄ Londres), liez la passerelle Gateway à l'IP tailnet :

- Définissez `gateway.bind: "tailnet"` dans `~/.openclaw/openclaw.json` sur l'hôte de la passerelle Gateway.
- Redémarrez la passerelle Gateway / application de la barre de menus macOS.

### 2) Vérifier la découverte (optionnel)

À partir de la machine de la passerelle Gateway :

```bash
dns-sd -B _openclaw-gw._tcp local.
```

Plus d'instructions de débogage : [Bonjour](/gateway/bonjour).

#### Découverte Tailnet via unicast DNS-SD (Vienne ⇄ Londres)

La découverte NSD/mDNS d'Android ne peut pas traverser les réseaux. Si votre nœud Android et votre passerelle Gateway se trouvent sur des réseaux différents mais sont connectés via Tailscale, utilisez plutôt Wide-Area Bonjour / unicast DNS-SD :

1. Configurez une zone DNS-SD sur l'hôte de la passerelle Gateway (exemple `openclaw.internal.`) et publiez les enregistrements `_openclaw-gw._tcp`.
2. Configurez le DNS fractionné Tailscale pour pointer le domaine de votre choix vers ce serveur DNS.

Détails et exemple de configuration CoreDNS : [Bonjour](/gateway/bonjour).

### 3) Connexion depuis Android

Dans l'application Android :

- L'application maintient la connexion à la passerelle Gateway via un **service de premier plan** (notification persistante).
- Ouvrez **Paramètres**.
- Sous **Passerelles Gateway découvertes**, sélectionnez votre passerelle Gateway et cliquez sur **Connecter**.
- Si mDNS est bloqué, utilisez **Avancé → Passerelle Gateway manuelle** (hôte + port) et **Connecter (manuel)**.

Après un appairage initial réussi, Android se reconnecte automatiquement au démarrage :

- Point de terminaison manuel (s'il est activé), sinon
- Passerelle Gateway découverte en dernier (meilleur effort).

### 4) Approuver l'appairage (CLI)

Sur la machine de la passerelle Gateway :

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
```

Détails d'appairage : [Appairage de la passerelle Gateway](/gateway/pairing).

### 5) Vérifier que le nœud est connecté

- Via l'état du nœud :
  ```bash
  openclaw nodes status
  ```
- Via la passerelle Gateway :
  ```bash
  openclaw gateway call node.list --params "{}"
  ```

### 6) Chat + Historique

Le panneau Chat du nœud Android utilise la **clé de session principale** de la passerelle Gateway (`main`), donc l'historique et les réponses sont partagés avec WebChat et d'autres clients :

- Historique : `chat.history`
- Envoi : `chat.send`
- Mises à jour push (meilleur effort) : `chat.subscribe` → `event:"chat"`

### 7) Canvas + Caméra

#### Hôte Canvas de la passerelle Gateway (recommandé pour le contenu web)

Si vous souhaitez que le nœud affiche du vrai HTML/CSS/JS que l'agent peut modifier sur le disque, pointez le nœud vers l'hôte canvas de la passerelle Gateway.

Remarque : Le nœud utilise un hôte canvas indépendant sur `canvasHost.port` (par défaut `18793`).

1. Créez `~/.openclaw/workspace/canvas/index.html` sur l'hôte de la passerelle Gateway.

2. Naviguez le nœud vers celui-ci (réseau local) :

```bash
openclaw nodes invoke --node "<Android Node>" --command canvas.navigate --params '{"url":"http://<gateway-hostname>.local:18793/__openclaw__/canvas/"}'
```

Tailnet (optionnel) : Si les deux appareils sont sur Tailscale, utilisez le nom MagicDNS ou l'IP tailnet au lieu de `.local`, par exemple `http://<gateway-magicdns>:18793/__openclaw__/canvas/`.

Ce serveur rechargera en temps réel le HTML injecté du client et rechargera lors des modifications de fichiers.
L'hôte A2UI se trouve à `http://<gateway-host>:18793/__openclaw__/a2ui/`.

Commandes Canvas (premier plan uniquement) :

- `canvas.eval`, `canvas.snapshot`, `canvas.navigate` (utilisez `{"url":""}` ou `{"url":"/"}` pour revenir à l'échafaudage par défaut). `canvas.snapshot` retourne `{ format, base64 }` (par défaut `format="jpeg"`).
- A2UI : `canvas.a2ui.push`, `canvas.a2ui.reset` (alias hérité `canvas.a2ui.pushJSONL`)

Commandes caméra (premier plan uniquement ; restrictions de permissions) :

- `camera.snap` (jpg)
- `camera.clip` (mp4)

Voir [Nœud Camera](/nodes/camera) pour les paramètres et les assistants CLI.
