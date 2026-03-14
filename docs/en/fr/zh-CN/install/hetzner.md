---
read_when:
  - Vous voulez que OpenClaw s'exécute 24/7 sur un VPS cloud (plutôt que sur votre ordinateur portable)
  - Vous voulez exécuter une Gateway de niveau production et toujours en ligne sur votre propre VPS
  - Vous voulez un contrôle total sur la persistance, les binaires et le comportement de redémarrage
  - Vous exécutez OpenClaw avec Docker sur Hetzner ou un fournisseur similaire
summary: Exécutez OpenClaw Gateway 24/7 sur un VPS Hetzner bon marché (Docker) avec état persistant et binaires intégrés
title: Hetzner
x-i18n:
  generated_at: "2026-02-03T07:52:17Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 84d9f24f1a803aa15faa52a05f25fe557ec3e2c2f48a00c701d49764bd3bc21a
  source_path: platforms/hetzner.md
  workflow: 15
---

# Exécuter OpenClaw sur Hetzner (Docker, Guide VPS Production)

## Objectif

Exécuter une Gateway OpenClaw persistante sur un VPS Hetzner avec Docker, avec état persistant, binaires intégrés et comportement de redémarrage sécurisé.

Si vous voulez « OpenClaw 24/7 pour environ 5 $ », c'est la configuration la plus simple et la plus fiable.
Les tarifs Hetzner varient ; choisissez le plus petit VPS Debian/Ubuntu et augmentez la capacité si vous rencontrez des problèmes de mémoire.

## Qu'est-ce que nous faisons (explication simple) ?

- Louer un petit serveur Linux (VPS Hetzner)
- Installer Docker (environnement d'exécution d'application isolé)
- Démarrer OpenClaw Gateway dans Docker
- Persister `~/.openclaw` + `~/.openclaw/workspace` sur l'hôte (conservé après redémarrage/reconstruction)
- Accéder à l'interface de contrôle depuis votre ordinateur portable via tunnel SSH

La Gateway est accessible via :

- Transfert de port SSH depuis votre ordinateur portable
- Exposition directe du port si vous gérez vous-même le pare-feu et les jetons

Ce guide suppose Ubuntu ou Debian sur Hetzner.
Si vous utilisez un autre VPS Linux, mappez les paquets en conséquence.
Pour le processus Docker générique, consultez [Docker](/install/docker).

---

## Chemin rapide (pour les opérateurs expérimentés)

1. Configurer le VPS Hetzner
2. Installer Docker
3. Cloner le dépôt OpenClaw
4. Créer des répertoires hôtes persistants
5. Configurer `.env` et `docker-compose.yml`
6. Intégrer les binaires requis dans l'image
7. `docker compose up -d`
8. Vérifier la persistance et l'accès à la Gateway

---

## Ce dont vous avez besoin

- Un VPS Hetzner avec accès root
- Accès SSH depuis votre ordinateur portable
- Familiarité basique avec SSH + copier/coller
- Environ 20 minutes
- Docker et Docker Compose
- Identifiants d'authentification du modèle
- Identifiants de fournisseur optionnels
  - Code QR WhatsApp
  - Jeton bot Telegram
  - OAuth Gmail

---

## 1) Configurer le VPS

Créez un VPS Ubuntu ou Debian dans Hetzner.

Connectez-vous en tant que root :

```bash
ssh root@YOUR_VPS_IP
```

Ce guide suppose que le VPS est avec état.
Ne le traitez pas comme une infrastructure jetable.

---

## 2) Installer Docker (sur le VPS)

```bash
apt-get update
apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sh
```

Vérifier :

```bash
docker --version
docker compose version
```

---

## 3) Cloner le dépôt OpenClaw

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
```

Ce guide suppose que vous allez construire une image personnalisée pour assurer la persistance des binaires.

---

## 4) Créer des répertoires hôtes persistants

Les conteneurs Docker sont temporaires.
Tout état à long terme doit être stocké sur l'hôte.

```bash
mkdir -p /root/.openclaw
mkdir -p /root/.openclaw/workspace

# Définir la propriété à l'utilisateur du conteneur (uid 1000) :
chown -R 1000:1000 /root/.openclaw
chown -R 1000:1000 /root/.openclaw/workspace
```

---

## 5) Configurer les variables d'environnement

Créez `.env` à la racine du dépôt.

```bash
OPENCLAW_IMAGE=openclaw:latest
OPENCLAW_GATEWAY_TOKEN=change-me-now
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789

OPENCLAW_CONFIG_DIR=/root/.openclaw
OPENCLAW_WORKSPACE_DIR=/root/.openclaw/workspace

GOG_KEYRING_PASSWORD=change-me-now
XDG_CONFIG_HOME=/home/node/.openclaw
```

Générer des clés fortes :

```bash
openssl rand -hex 32
```

**Ne commitez pas ce fichier.**

---

## 6) Configuration Docker Compose

Créez ou mettez à jour `docker-compose.yml`.

```yaml
services:
  openclaw-gateway:
    image: ${OPENCLAW_IMAGE}
    build: .
    restart: unless-stopped
    env_file:
      - .env
    environment:
      - HOME=/home/node
      - NODE_ENV=production
      - TERM=xterm-256color
      - OPENCLAW_GATEWAY_BIND=${OPENCLAW_GATEWAY_BIND}
      - OPENCLAW_GATEWAY_PORT=${OPENCLAW_GATEWAY_PORT}
      - OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN}
      - GOG_KEYRING_PASSWORD=${GOG_KEYRING_PASSWORD}
      - XDG_CONFIG_HOME=${XDG_CONFIG_HOME}
      - PATH=/home/linuxbrew/.linuxbrew/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    volumes:
      - ${OPENCLAW_CONFIG_DIR}:/home/node/.openclaw
      - ${OPENCLAW_WORKSPACE_DIR}:/home/node/.openclaw/workspace
    ports:
      # Recommandé : garder la Gateway limitée à loopback sur le VPS ; accéder via tunnel SSH.
      # Pour exposer publiquement, supprimez le préfixe `127.0.0.1:` et configurez le pare-feu en conséquence.
      - "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"

      # Optionnel : uniquement si vous exécutez des nœuds iOS/Android sur ce VPS et avez besoin d'un hôte Canvas.
      # Si vous exposez ce port publiquement, lisez /gateway/security et configurez le pare-feu en conséquence.
      # - "18793:18793"
    command:
      [
        "node",
        "dist/index.js",
        "gateway",
        "--bind",
        "${OPENCLAW_GATEWAY_BIND}",
        "--port",
        "${OPENCLAW_GATEWAY_PORT}",
      ]
```

---

## 7) Intégrer les binaires requis dans l'image (critique)

Installer des binaires dans un conteneur en cours d'exécution est un piège.
Tout ce qui est installé à l'exécution sera perdu au redémarrage.

Tous les binaires externes requis par les skills doivent être installés au moment de la construction de l'image.

L'exemple suivant montre seulement trois binaires courants :

- `gog` pour l'accès Gmail
- `goplaces` pour Google Places
- `wacli` pour WhatsApp

Ce sont des exemples, pas une liste complète.
Vous pouvez installer n'importe quel nombre de binaires en utilisant le même modèle.

Si vous ajoutez ultérieurement de nouveaux skills qui nécessitent des binaires supplémentaires, vous devez :

1. Mettre à jour le Dockerfile
2. Reconstruire l'image
3. Redémarrer le conteneur

**Exemple Dockerfile**

```dockerfile
FROM node:22-bookworm

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# Exemple binaire 1 : Gmail CLI
RUN curl -L https://github.com/steipete/gog/releases/latest/download/gog_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/gog

# Exemple binaire 2 : Google Places CLI
RUN curl -L https://github.com/steipete/goplaces/releases/latest/download/goplaces_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/goplaces

# Exemple binaire 3 : WhatsApp CLI
RUN curl -L https://github.com/steipete/wacli/releases/latest/download/wacli_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/wacli

# Ajouter plus de binaires ci-dessous en utilisant le même modèle

WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY ui/package.json ./ui/package.json
COPY scripts ./scripts

RUN corepack enable
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build
RUN pnpm ui:install
RUN pnpm ui:build

ENV NODE_ENV=production

CMD ["node","dist/index.js"]
```

---

## 8) Construire et démarrer

```bash
docker compose build
docker compose up -d openclaw-gateway
```

Vérifier les binaires :

```bash
docker compose exec openclaw-gateway which gog
docker compose exec openclaw-gateway which goplaces
docker compose exec openclaw-gateway which wacli
```

Sortie attendue :

```
/usr/local/bin/gog
/usr/local/bin/goplaces
/usr/local/bin/wacli
```

---

## 9) Vérifier la Gateway

```bash
docker compose logs -f openclaw-gateway
```

Succès :

```
[gateway] listening on ws://0.0.0.0:18789
```

Depuis votre ordinateur portable :

```bash
ssh -N -L 18789:127.0.0.1:18789 root@YOUR_VPS_IP
```

Ouvrir :

`http://127.0.0.1:18789/`

Collez votre jeton Gateway.

---

## Emplacements persistants (source de vérité)

OpenClaw s'exécute dans Docker, mais Docker n'est pas la source de vérité.
Tout état à long terme doit persister après redémarrage, reconstruction et redémarrage.

| Composant              | Emplacement                       | Mécanisme de persistance | Description                    |
| ---------------------- | --------------------------------- | ------------------------ | ------------------------------ |
| Configuration Gateway  | `/home/node/.openclaw/`           | Montage de volume hôte   | Inclut `openclaw.json`, jetons |
| Fichiers d'authentification du modèle | `/home/node/.openclaw/`           | Montage de volume hôte   | Jetons OAuth, clés API         |
| Configuration Skill    | `/home/node/.openclaw/skills/`    | Montage de volume hôte   | État au niveau du skill        |
| Espace de travail agent | `/home/node/.openclaw/workspace/` | Montage de volume hôte   | Code et artefacts d'agent      |
| Session WhatsApp       | `/home/node/.openclaw/`           | Montage de volume hôte   | Conserve la connexion QR       |
| Trousseau Gmail        | `/home/node/.openclaw/`           | Volume hôte + mot de passe | Nécessite `GOG_KEYRING_PASSWORD` |
| Binaires externes      | `/usr/local/bin/`                 | Image Docker             | Doit être intégré au moment de la construction |
| Runtime Node           | Système de fichiers du conteneur  | Image Docker             | Reconstruit à chaque construction d'image |
| Paquets du système d'exploitation | Système de fichiers du conteneur  | Image Docker             | Ne pas installer à l'exécution |
| Conteneur Docker       | Temporaire                        | Redémarrable             | Peut être détruit en toute sécurité |
