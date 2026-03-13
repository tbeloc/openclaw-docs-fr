---
read_when:
  - Vous voulez un hôte Linux résident bon marché pour exécuter la passerelle Gateway
  - Vous voulez un accès à l'interface utilisateur contrôlé à distance sans exécuter votre propre VPS
summary: Exécutez OpenClaw Gateway sur exe.dev (VM + proxy HTTPS) pour un accès à distance
title: exe.dev
x-i18n:
  generated_at: "2026-02-03T07:51:36Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 8d57ee7dd6029f0b778465c147092b824a0f1b0680af13032aaf116ff3d4d671
  source_path: platforms/exe-dev.md
  workflow: 15
---

# exe.dev

Objectif : OpenClaw Gateway s'exécute sur une VM exe.dev et est accessible depuis votre ordinateur portable via : `https://<vm-name>.exe.xyz`

Cette page suppose l'utilisation de l'image **exeuntu** par défaut d'exe.dev. Si vous avez choisi une distribution différente, veuillez mapper les paquets en conséquence.

## Chemin rapide pour les débutants

1. [https://exe.new/openclaw](https://exe.new/openclaw)
2. Remplissez votre clé d'authentification/jeton selon vos besoins
3. Cliquez sur « Agent » à côté de la VM, puis attendez...
4. ???
5. Terminé

## Ce dont vous avez besoin

- Un compte exe.dev
- Accès `ssh exe.dev` à la machine virtuelle [exe.dev](https://exe.dev) (optionnel)

## Installation automatique avec Shelley

Shelley, l'agent d'[exe.dev](https://exe.dev), peut installer OpenClaw instantanément en utilisant notre invite. L'invite utilisée est la suivante :

```
Set up OpenClaw (https://docs.openclaw.ai/install) on this VM. Use the non-interactive and accept-risk flags for openclaw onboarding. Add the supplied auth or token as needed. Configure nginx to forward from the default port 18789 to the root location on the default enabled site config, making sure to enable Websocket support. Pairing is done by "openclaw devices list" and "openclaw device approve <request id>". Make sure the dashboard shows that OpenClaw's health is OK. exe.dev handles forwarding from port 8000 to port 80/443 and HTTPS for us, so the final "reachable" should be <vm-name>.exe.xyz, without port specification.
```

## Installation manuelle

## 1) Créer une VM

Depuis votre appareil :

```bash
ssh exe.dev new
```

Puis connectez-vous :

```bash
ssh <vm-name>.exe.xyz
```

Conseil : gardez cette VM **avec état**. OpenClaw stocke l'état sous `~/.openclaw/` et `~/.openclaw/workspace/`.

## 2) Installer les prérequis (sur la VM)

```bash
sudo apt-get update
sudo apt-get install -y git curl jq ca-certificates openssl
```

## 3) Installer OpenClaw

Exécutez le script d'installation d'OpenClaw :

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

## 4) Configurer nginx pour proxifier OpenClaw vers le port 8000

Modifiez `/etc/nginx/sites-enabled/default` :

```
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    listen 8000;
    listen [::]:8000;

    server_name _;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;

        # Support WebSocket
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # En-têtes de proxy standard
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Paramètres de délai d'expiration de connexion longue
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
```

## 5) Accéder à OpenClaw et accorder les permissions

Accédez à `https://<vm-name>.exe.xyz/?token=YOUR-TOKEN-FROM-TERMINAL` (voir la sortie de l'interface utilisateur de contrôle dans le guide de démarrage). Utilisez `openclaw devices list` et `openclaw devices approve <requestId>` pour approuver les appareils. En cas de doute, utilisez Shelley depuis votre navigateur !

## Accès à distance

L'accès à distance est géré par l'authentification d'[exe.dev](https://exe.dev). Par défaut, le trafic HTTP du port 8000 est transféré via authentification par e-mail vers `https://<vm-name>.exe.xyz`.

## Mise à jour

```bash
npm i -g openclaw@latest
openclaw doctor
openclaw gateway restart
openclaw health
```

Guide : [Mise à jour](/install/updating)
