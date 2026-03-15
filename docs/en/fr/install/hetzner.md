---
summary: "Exécutez OpenClaw Gateway 24/7 sur un VPS Hetzner bon marché (Docker) avec état durable et binaires intégrés"
read_when:
  - You want OpenClaw running 24/7 on a cloud VPS (not your laptop)
  - You want a production-grade, always-on Gateway on your own VPS
  - You want full control over persistence, binaries, and restart behavior
  - You are running OpenClaw in Docker on Hetzner or a similar provider
title: "Hetzner"
---

# OpenClaw sur Hetzner (Docker, Guide VPS Production)

## Objectif

Exécuter une passerelle OpenClaw persistante sur un VPS Hetzner en utilisant Docker, avec état durable, binaires intégrés et comportement de redémarrage sûr.

Si vous voulez « OpenClaw 24/7 pour ~5 $ », c'est la configuration fiable la plus simple.
Les tarifs de Hetzner changent ; choisissez le plus petit VPS Debian/Ubuntu et augmentez la taille si vous rencontrez des OOMs.

Rappel du modèle de sécurité :

- Les agents partagés par l'entreprise conviennent lorsque tout le monde se trouve dans la même limite de confiance et que l'exécution est réservée aux affaires.
- Maintenez une séparation stricte : VPS/exécution dédiés + comptes dédiés ; aucun profil personnel Apple/Google/navigateur/gestionnaire de mots de passe sur cet hôte.
- Si les utilisateurs sont adversaires les uns envers les autres, divisez par passerelle/hôte/utilisateur du système d'exploitation.

Voir [Sécurité](/gateway/security) et [Hébergement VPS](/vps).

## Que faisons-nous (en termes simples) ?

- Louer un petit serveur Linux (VPS Hetzner)
- Installer Docker (exécution d'application isolée)
- Démarrer la passerelle OpenClaw dans Docker
- Persister `~/.openclaw` + `~/.openclaw/workspace` sur l'hôte (survit aux redémarrages/reconstructions)
- Accéder à l'interface de contrôle depuis votre ordinateur portable via un tunnel SSH

La passerelle est accessible via :

- Redirection de port SSH depuis votre ordinateur portable
- Exposition directe du port si vous gérez vous-même le pare-feu et les jetons

Ce guide suppose Ubuntu ou Debian sur Hetzner.  
Si vous êtes sur un autre VPS Linux, mappez les packages en conséquence.
Pour le flux Docker générique, voir [Docker](/install/docker).

---

## Chemin rapide (opérateurs expérimentés)

1. Provisionner le VPS Hetzner
2. Installer Docker
3. Cloner le référentiel OpenClaw
4. Créer des répertoires hôtes persistants
5. Configurer `.env` et `docker-compose.yml`
6. Intégrer les binaires requis dans l'image
7. `docker compose up -d`
8. Vérifier la persistance et l'accès à la passerelle

---

## Ce dont vous avez besoin

- VPS Hetzner avec accès root
- Accès SSH depuis votre ordinateur portable
- Confort de base avec SSH + copier/coller
- ~20 minutes
- Docker et Docker Compose
- Identifiants d'authentification du modèle
- Identifiants de fournisseur optionnels
  - Code QR WhatsApp
  - Jeton bot Telegram
  - OAuth Gmail

---

## 1) Provisionner le VPS

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

## 3) Cloner le référentiel OpenClaw

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
```

Ce guide suppose que vous allez créer une image personnalisée pour garantir la persistance des binaires.

---

## 4) Créer des répertoires hôtes persistants

Les conteneurs Docker sont éphémères.
Tout état de longue durée doit vivre sur l'hôte.

```bash
mkdir -p /root/.openclaw/workspace

# Définir la propriété sur l'utilisateur du conteneur (uid 1000):
chown -R 1000:1000 /root/.openclaw
```

---

## 5) Configurer les variables d'environnement

Créez `.env` à la racine du référentiel.

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

Générer des secrets forts :

```bash
openssl rand -hex 32
```

**Ne validez pas ce fichier.**

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
      # Recommandé : garder la passerelle en boucle locale uniquement sur le VPS ; accès via tunnel SSH.
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
        "--allow-unconfigured",
      ]
```

`--allow-unconfigured` est uniquement pour la commodité d'amorçage, ce n'est pas un remplacement pour une configuration de passerelle appropriée. Définissez toujours l'authentification (`gateway.auth.token` ou mot de passe) et utilisez des paramètres de liaison sûrs pour votre déploiement.

---

## 7) Étapes d'exécution Docker VM partagées

Utilisez le guide d'exécution partagé pour le flux hôte Docker commun :

- [Intégrer les binaires requis dans l'image](/install/docker-vm-runtime#bake-required-binaries-into-the-image)
- [Construire et lancer](/install/docker-vm-runtime#build-and-launch)
- [Ce qui persiste où](/install/docker-vm-runtime#what-persists-where)
- [Mises à jour](/install/docker-vm-runtime#updates)

---

## 8) Accès spécifique à Hetzner

Après les étapes de construction et de lancement partagées, créez un tunnel depuis votre ordinateur portable :

```bash
ssh -N -L 18789:127.0.0.1:18789 root@YOUR_VPS_IP
```

Ouvrir :

`http://127.0.0.1:18789/`

Collez votre jeton de passerelle.

---

La carte de persistance partagée se trouve dans [Docker VM Runtime](/install/docker-vm-runtime#what-persists-where).

## Infrastructure en tant que code (Terraform)

Pour les équipes préférant les flux de travail d'infrastructure en tant que code, une configuration Terraform maintenue par la communauté fournit :

- Configuration Terraform modulaire avec gestion d'état à distance
- Provisionnement automatisé via cloud-init
- Scripts de déploiement (amorçage, déploiement, sauvegarde/restauration)
- Durcissement de la sécurité (pare-feu, UFW, accès SSH uniquement)
- Configuration du tunnel SSH pour l'accès à la passerelle

**Référentiels :**

- Infrastructure : [openclaw-terraform-hetzner](https://github.com/andreesg/openclaw-terraform-hetzner)
- Configuration Docker : [openclaw-docker-config](https://github.com/andreesg/openclaw-docker-config)

Cette approche complète la configuration Docker ci-dessus avec des déploiements reproductibles, une infrastructure contrôlée par version et une récupération après sinistre automatisée.

> **Remarque :** Maintenu par la communauté. Pour les problèmes ou les contributions, consultez les liens du référentiel ci-dessus.
