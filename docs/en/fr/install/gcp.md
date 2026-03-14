# OpenClaw sur GCP Compute Engine (Docker, Guide VPS Production)

## Objectif

Exécuter une passerelle OpenClaw persistante sur une VM GCP Compute Engine en utilisant Docker, avec un état durable, des binaires intégrés et un comportement de redémarrage sûr.

Si vous voulez « OpenClaw 24/7 pour ~5-12 $/mois », c'est une configuration fiable sur Google Cloud.
Les tarifs varient selon le type de machine et la région ; choisissez la plus petite VM adaptée à votre charge de travail et augmentez la taille si vous rencontrez des OOM.

## Qu'allons-nous faire (en termes simples) ?

- Créer un projet GCP et activer la facturation
- Créer une VM Compute Engine
- Installer Docker (runtime d'application isolé)
- Démarrer la passerelle OpenClaw dans Docker
- Persister `~/.openclaw` + `~/.openclaw/workspace` sur l'hôte (survit aux redémarrages/reconstructions)
- Accéder à l'interface de contrôle depuis votre ordinateur portable via un tunnel SSH

La passerelle peut être accessible via :

- Redirection de port SSH depuis votre ordinateur portable
- Exposition directe du port si vous gérez vous-même le pare-feu et les jetons

Ce guide utilise Debian sur GCP Compute Engine.
Ubuntu fonctionne également ; mappez les paquets en conséquence.
Pour le flux Docker générique, voir [Docker](/install/docker).

---

## Chemin rapide (opérateurs expérimentés)

1. Créer un projet GCP + activer l'API Compute Engine
2. Créer une VM Compute Engine (e2-small, Debian 12, 20GB)
3. SSH dans la VM
4. Installer Docker
5. Cloner le référentiel OpenClaw
6. Créer des répertoires hôtes persistants
7. Configurer `.env` et `docker-compose.yml`
8. Cuire les binaires requis, construire et lancer

---

## Ce dont vous avez besoin

- Compte GCP (éligible au niveau gratuit pour e2-micro)
- CLI gcloud installé (ou utiliser Cloud Console)
- Accès SSH depuis votre ordinateur portable
- Confort de base avec SSH + copier/coller
- ~20-30 minutes
- Docker et Docker Compose
- Identifiants d'authentification du modèle
- Identifiants de fournisseur optionnels
  - Code QR WhatsApp
  - Jeton bot Telegram
  - OAuth Gmail

---

## 1) Installer gcloud CLI (ou utiliser Console)

**Option A : gcloud CLI** (recommandé pour l'automatisation)

Installer depuis [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

Initialiser et authentifier :

```bash
gcloud init
gcloud auth login
```

**Option B : Cloud Console**

Toutes les étapes peuvent être effectuées via l'interface Web à [https://console.cloud.google.com](https://console.cloud.google.com)

---

## 2) Créer un projet GCP

**CLI :**

```bash
gcloud projects create my-openclaw-project --name="OpenClaw Gateway"
gcloud config set project my-openclaw-project
```

Activer la facturation à [https://console.cloud.google.com/billing](https://console.cloud.google.com/billing) (requis pour Compute Engine).

Activer l'API Compute Engine :

```bash
gcloud services enable compute.googleapis.com
```

**Console :**

1. Aller à IAM & Admin > Créer un projet
2. Le nommer et créer
3. Activer la facturation pour le projet
4. Naviguer vers APIs & Services > Activer les APIs > rechercher « Compute Engine API » > Activer

---

## 3) Créer la VM

**Types de machines :**

| Type      | Spécifications           | Coût               | Notes                                                    |
| --------- | ------------------------ | ------------------ | -------------------------------------------------------- |
| e2-medium | 2 vCPU, 4GB RAM          | ~25 $/mois         | Plus fiable pour les builds Docker locaux               |
| e2-small  | 2 vCPU, 2GB RAM          | ~12 $/mois         | Minimum recommandé pour le build Docker                 |
| e2-micro  | 2 vCPU (partagé), 1GB RAM | Éligible au niveau gratuit | Échoue souvent avec OOM du build Docker (exit 137)      |

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

1. Aller à Compute Engine > Instances de VM > Créer une instance
2. Nom : `openclaw-gateway`
3. Région : `us-central1`, Zone : `us-central1-a`
4. Type de machine : `e2-small`
5. Disque de démarrage : Debian 12, 20GB
6. Créer

---

## 4) SSH dans la VM

**CLI :**

```bash
gcloud compute ssh openclaw-gateway --zone=us-central1-a
```

**Console :**

Cliquez sur le bouton « SSH » à côté de votre VM dans le tableau de bord Compute Engine.

Remarque : La propagation de la clé SSH peut prendre 1-2 minutes après la création de la VM. Si la connexion est refusée, attendez et réessayez.

---

## 5) Installer Docker (sur la VM)

```bash
sudo apt-get update
sudo apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

Déconnectez-vous et reconnectez-vous pour que le changement de groupe prenne effet :

```bash
exit
```

Puis SSH à nouveau :

```bash
gcloud compute ssh openclaw-gateway --zone=us-central1-a
```

Vérifier :

```bash
docker --version
docker compose version
```

---

## 6) Cloner le référentiel OpenClaw

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
```

Ce guide suppose que vous allez construire une image personnalisée pour garantir la persistance des binaires.

---

## 7) Créer des répertoires hôtes persistants

Les conteneurs Docker sont éphémères.
Tout état de longue durée doit vivre sur l'hôte.

```bash
mkdir -p ~/.openclaw
mkdir -p ~/.openclaw/workspace
```

---

## 8) Configurer les variables d'environnement

Créer `.env` à la racine du référentiel.

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

Générer des secrets forts :

```bash
openssl rand -hex 32
```

**Ne pas valider ce fichier.**

---

## 9) Configuration Docker Compose

Créer ou mettre à jour `docker-compose.yml`.

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
      # Recommandé : garder la passerelle en boucle locale sur la VM ; accéder via tunnel SSH.
      # Pour l'exposer publiquement, supprimez le préfixe `127.0.0.1:` et configurez le pare-feu en conséquence.
      - "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"
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

## 10) Étapes partagées du runtime Docker VM

Utiliser le guide du runtime partagé pour le flux hôte Docker commun :

- [Cuire les binaires requis dans l'image](/install/docker-vm-runtime#bake-required-binaries-into-the-image)
- [Construire et lancer](/install/docker-vm-runtime#build-and-launch)
- [Ce qui persiste où](/install/docker-vm-runtime#what-persists-where)
- [Mises à jour](/install/docker-vm-runtime#updates)

---

## 11) Notes de lancement spécifiques à GCP

Sur GCP, si le build échoue avec `Killed` ou `exit code 137` pendant `pnpm install --frozen-lockfile`, la VM n'a pas assez de mémoire. Utilisez `e2-small` au minimum, ou `e2-medium` pour des premiers builds plus fiables.

Lors de la liaison à LAN (`OPENCLAW_GATEWAY_BIND=lan`), configurez une origine de navigateur de confiance avant de continuer :

```bash
docker compose run --rm openclaw-cli config set gateway.controlUi.allowedOrigins '["http://127.0.0.1:18789"]' --strict-json
```

Si vous avez modifié le port de la passerelle, remplacez `18789` par votre port configuré.

## 12) Accéder depuis votre ordinateur portable

Créer un tunnel SSH pour rediriger le port de la passerelle :

```bash
gcloud compute ssh openclaw-gateway --zone=us-central1-a -- -L 18789:127.0.0.1:18789
```

Ouvrir dans votre navigateur :

`http://127.0.0.1:18789/`

Récupérer un lien de tableau de bord tokenisé frais :

```bash
docker compose run --rm openclaw-cli dashboard --no-open
```

Coller le jeton de cette URL.

Si l'interface de contrôle affiche `unauthorized` ou `disconnected (1008): pairing required`, approuver l'appareil du navigateur :

```bash
docker compose run --rm openclaw-cli devices list
docker compose run --rm openclaw-cli devices approve <requestId>
```

Besoin de la référence de persistance partagée et de mise à jour à nouveau ?
Voir [Docker VM Runtime](/install/docker-vm-runtime#what-persists-where) et [Mises à jour Docker VM Runtime](/install/docker-vm-runtime#updates).

---

## Dépannage

**Connexion SSH refusée**

La propagation de la clé SSH peut prendre 1-2 minutes après la création de la VM. Attendez et réessayez.

**Problèmes OS Login**

Vérifier votre profil OS Login :

```bash
gcloud compute os-login describe-profile
```

Assurez-vous que votre compte dispose des autorisations IAM requises (Compute OS Login ou Compute OS Admin Login).

**Mémoire insuffisante (OOM)**

Si le build Docker échoue avec `Killed` et `exit code 137`, la VM a été tuée par OOM. Mettez à niveau vers e2-small (minimum) ou e2-medium (recommandé pour les builds locaux fiables) :

```bash
# Arrêter la VM d'abord
gcloud compute instances stop openclaw-gateway --zone=us-central1-a

# Changer le type de machine
gcloud compute instances set-machine-type openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small

# Démarrer la VM
gcloud compute instances start openclaw-gateway --zone=us-central1-a
```

---

## Comptes de service (bonne pratique de sécurité)

Pour un usage personnel, votre compte utilisateur par défaut fonctionne bien.

Pour les pipelines d'automatisation ou CI/CD, créer un compte de service dédié avec des autorisations minimales :

1. Créer un compte de service :

   ```bash
   gcloud iam service-accounts create openclaw-deploy \
     --display-name="OpenClaw Deployment"
   ```

2. Accorder le rôle Compute Instance Admin (ou un rôle personnalisé plus étroit) :

   ```bash
   gcloud projects add-iam-policy-binding my-openclaw-project \
     --member="serviceAccount:openclaw-deploy@my-openclaw-project.iam.gserviceaccount.com" \
     --role="roles/compute.instanceAdmin.v1"
   ```

Éviter d'utiliser le rôle Owner pour l'automatisation. Utiliser le principe du moindre privilège.

Voir [https://cloud.google.com/iam/docs/understanding-roles](https://cloud.google.com/iam/docs/understanding-roles) pour les détails des rôles IAM.

---

## Étapes suivantes

- Configurer les canaux de messagerie : [Canaux](/channels)
- Appairer les appareils locaux en tant que nœuds : [Nœuds](/nodes)
- Configurer la passerelle : [Configuration de la passerelle](/gateway/configuration)
