---
read_when:
  - Vous voulez exécuter OpenClaw 24/7 sur GCP
  - Vous voulez exécuter une Gateway de production, résidente sur votre propre VM
  - Vous voulez un contrôle total sur la persistance, les binaires et le comportement de redémarrage
summary: Exécutez OpenClaw Gateway 24/7 sur une VM GCP Compute Engine (Docker) avec état persistant
title: GCP
x-i18n:
  generated_at: "2026-02-03T07:52:50Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: abb236dd421505d307bb3869340c9a0c940de095b93af9ad1f130cc08a9deadb
  source_path: platforms/gcp.md
  workflow: 15
---

# Exécuter OpenClaw sur GCP Compute Engine (Docker, Guide VPS Production)

## Objectif

Exécutez une Gateway OpenClaw persistante sur une VM GCP Compute Engine avec Docker, avec état persistant, binaires intégrés et comportement de redémarrage sécurisé.

Si vous voulez « OpenClaw 24/7 pour environ $5-12/mois », c'est une configuration fiable sur Google Cloud.
Les prix varient selon le type de machine et la région ; choisissez la VM minimale adaptée à votre charge de travail, et augmentez si vous rencontrez des OOM.

## Qu'est-ce que nous faisons (explication simple) ?

- Créer un projet GCP et activer la facturation
- Créer une VM Compute Engine
- Installer Docker (runtime d'application isolé)
- Démarrer OpenClaw Gateway dans Docker
- Persister `~/.openclaw` + `~/.openclaw/workspace` sur l'hôte (survit aux redémarrages/reconstructions)
- Accéder à l'interface de contrôle depuis votre ordinateur portable via tunnel SSH

La Gateway est accessible via :

- Transfert de port SSH depuis votre ordinateur portable
- Exposition directe du port si vous gérez vous-même le pare-feu et les jetons

Ce guide utilise Debian sur GCP Compute Engine.
Ubuntu fonctionne aussi ; mappez les paquets en conséquence.
Pour les processus Docker génériques, consultez [Docker](/install/docker).

---

## Chemin rapide (opérateurs expérimentés)

1. Créer un projet GCP + activer l'API Compute Engine
2. Créer une VM Compute Engine (e2-small, Debian 12, 20GB)
3. SSH dans la VM
4. Installer Docker
5. Cloner le dépôt OpenClaw
6. Créer un répertoire hôte persistant
7. Configurer `.env` et `docker-compose.yml`
8. Intégrer les binaires requis, construire et démarrer

---

## Ce dont vous avez besoin

- Compte GCP (e2-micro est éligible au niveau gratuit)
- gcloud CLI installé (ou utiliser Cloud Console)
- Accès SSH depuis votre ordinateur portable
- Compréhension basique de SSH + copier/coller
- Environ 20-30 minutes
- Docker et Docker Compose
- Identifiants d'authentification du modèle
- Identifiants de fournisseur optionnels
  - QR WhatsApp
  - Jeton bot Telegram
  - OAuth Gmail

---

## 1) Installer gcloud CLI (ou utiliser Console)

**Option A : gcloud CLI** (recommandé pour l'automatisation)

Installez depuis https://cloud.google.com/sdk/docs/install

Initialisez et authentifiez :

```bash
gcloud init
gcloud auth login
```

**Option B : Cloud Console**

Toutes les étapes peuvent être complétées via l'interface Web sur https://console.cloud.google.com

---

## 2) Créer un projet GCP

**CLI :**

```bash
gcloud projects create my-openclaw-project --name="OpenClaw Gateway"
gcloud config set project my-openclaw-project
```

Activez la facturation sur https://console.cloud.google.com/billing (requis pour Compute Engine).

Activez l'API Compute Engine :

```bash
gcloud services enable compute.googleapis.com
```

**Console :**

1. Allez à IAM & Admin > Create Project
2. Nommez et créez
3. Activez la facturation pour le projet
4. Naviguez vers APIs & Services > Enable APIs > Recherchez « Compute Engine API » > Enable

---

## 3) Créer une VM

**Type de machine :**

| Type     | Configuration           | Coût       | Description        |
| -------- | ----------------------- | ---------- | ------------------ |
| e2-small | 2 vCPU, 2GB RAM         | ~$12/mois  | Recommandé         |
| e2-micro | 2 vCPU (partagés), 1GB RAM | Niveau gratuit | Peut OOM sous charge |

**CLI :**

```bash
gcloud compute instances create openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small \
  --boot-disk-size=20GB \
  --image-family=debian-12 \
  --image-project=debian-cloud
```

**Console :**

1. Allez à Compute Engine > VM instances > Create instance
2. Name : `openclaw-gateway`
3. Region : `us-central1`, Zone : `us-central1-a`
4. Machine type : `e2-small`
5. Boot disk : Debian 12, 20GB
6. Create

---

## 4) SSH dans la VM

**CLI :**

```bash
gcloud compute ssh openclaw-gateway --zone=us-central1-a
```

**Console :**

Cliquez sur le bouton « SSH » à côté de la VM dans le tableau de bord Compute Engine.

Remarque : La propagation des clés SSH peut prendre 1-2 minutes après la création de la VM. Si la connexion est refusée, attendez et réessayez.

---

## 5) Installer Docker (sur la VM)

```bash
sudo apt-get update
sudo apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

Déconnectez-vous et reconnectez-vous pour que les modifications de groupe prennent effet :

```bash
exit
```

Puis reconnectez-vous via SSH :

```bash
gcloud compute ssh openclaw-gateway --zone=us-central1-a
```

Vérifiez :

```bash
docker --version
docker compose version
```

---

## 6) Cloner le dépôt OpenClaw

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
```

Ce guide suppose que vous allez construire une image personnalisée pour assurer la persistance des binaires.

---

## 7) Créer un répertoire hôte persistant

Les conteneurs Docker sont temporaires.
Tout état à long terme doit exister sur l'hôte.

```bash
mkdir -p ~/.openclaw
mkdir -p ~/.openclaw/workspace
```

---

## 8) Configurer les variables d'environnement

Créez un `.env` à la racine du dépôt.

```bash
OPENCLAW_IMAGE=openclaw:latest
OPENCLAW_GATEWAY_TOKEN=change-me-now
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789

OPENCLAW_CONFIG_DIR=/home/$USER/.openclaw
OPENCLAW_WORKSPACE_DIR=/home/$USER/.openclaw/workspace

GOG_KEYRING_PASSWORD=change-me-now
XDG_CONFIG_HOME=/home/node/.openclaw
```

Générez des clés fortes :

```bash
openssl rand -hex 32
```

**Ne commitez pas ce fichier.**

---

## 9) Configuration Docker Compose

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
      # Recommandé : gardez la Gateway liée à loopback sur la VM ; accédez via tunnel SSH.
      # Pour exposer publiquement, supprimez le préfixe `127.0.0.1:` et configurez le pare-feu en conséquence.
      - "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"

      # Optionnel : uniquement si vous exécutez des nœuds iOS/Android contre cette VM et avez besoin d'un hôte Canvas.
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

## 10) Intégrer les binaires requis dans l'image (critique)

Installer des binaires dans un conteneur en cours d'exécution est un piège.
Tout ce qui est installé au moment de l'exécution est perdu au redémarrage.

Tous les binaires externes requis par les Skills doivent être installés au moment de la construction de l'image.

L'exemple suivant montre seulement trois binaires courants :

- `gog` pour l'accès Gmail
- `goplaces` pour Google Places
- `wacli` pour WhatsApp

Ce sont des exemples, pas une liste complète.
Vous pouvez installer n'importe quel nombre de binaires en utilisant le même modèle.

Si vous ajoutez ultérieurement de nouvelles Skills qui dépendent de binaires supplémentaires, vous devez :

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

# Ajoutez plus de binaires ci-dessous en utilisant le même modèle

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

## 11) Construire et démarrer

```bash
docker compose build
docker compose up -d openclaw-gateway
```

Vérifiez les binaires :

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

## 12) Vérifier la Gateway

```bash
docker compose logs -f openclaw-gateway
```

Succès :

```
[gateway] listening on ws://0.0.0.0:18789
```

---

## 13) Accéder depuis votre ordinateur portable

Créez un tunnel SSH pour transférer le port de la Gateway :

```bash
gcloud compute ssh openclaw-gateway --zone=us-central1-a -- -L 18789:127.0.0.1:18789
```

Ouvrez dans votre navigateur :

`http://127.0.0.1:18789/`

Collez votre jeton Gateway.

---

## Ce qui persiste où (source de vérité)

OpenClaw s'exécute dans Docker, mais Docker n'est pas la source de vérité.
Tout état à long terme doit survivre aux redémarrages, reconstructions et redémarrages.

| Composant              | Emplacement                       | Mécanisme de persistance | Description                    |
| ---------------------- | --------------------------------- | ------------------------ | ------------------------------ |
| Configuration Gateway  | `/home/node/.openclaw/`           | Montage de volume hôte   | Inclut `openclaw.json`, jetons |
| Fichiers d'authentification du modèle | `/home/node/.openclaw/`           | Montage de volume hôte   | Jetons OAuth, clés API         |
| Configuration Skill    | `/home/node/.openclaw/skills/`    | Montage de volume hôte   | État au niveau Skill           |
| Espace de travail agent | `/home/node/.openclaw/workspace/` | Montage de volume hôte   | Code et artefacts agent        |
| Session WhatsApp       | `/home/node/.openclaw/`           | Montage de volume hôte   | Conserve la connexion QR       |
| Trousseau Gmail        | `/home/node/.openclaw/`           | Montage de volume + mot de passe | Nécessite `GOG_KEYRING_PASSWORD` |
| Binaires externes      | `/usr/local/bin/`                 | Image Docker             | Doit être intégré au moment de la construction |
| Runtime Node           | Système de fichiers du conteneur  | Image Docker             | Reconstruit à chaque construction d'
