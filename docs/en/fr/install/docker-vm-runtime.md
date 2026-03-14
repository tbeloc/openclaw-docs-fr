---
summary: "Étapes partagées du runtime Docker VM pour les hôtes OpenClaw Gateway de longue durée"
read_when:
  - You are deploying OpenClaw on a cloud VM with Docker
  - You need the shared binary bake, persistence, and update flow
title: "Docker VM Runtime"
---

# Docker VM Runtime

Étapes de runtime partagées pour les installations Docker basées sur VM telles que GCP, Hetzner et les fournisseurs VPS similaires.

## Intégrer les binaires requis dans l'image

Installer des binaires à l'intérieur d'un conteneur en cours d'exécution est un piège.
Tout ce qui est installé au moment de l'exécution sera perdu au redémarrage.

Tous les binaires externes requis par les compétences doivent être installés au moment de la construction de l'image.

Les exemples ci-dessous montrent trois binaires courants uniquement :

- `gog` pour l'accès à Gmail
- `goplaces` pour Google Places
- `wacli` pour WhatsApp

Ce sont des exemples, pas une liste complète.
Vous pouvez installer autant de binaires que nécessaire en utilisant le même modèle.

Si vous ajoutez de nouvelles compétences ultérieurement qui dépendent de binaires supplémentaires, vous devez :

1. Mettre à jour le Dockerfile
2. Reconstruire l'image
3. Redémarrer les conteneurs

**Exemple de Dockerfile**

```dockerfile
FROM node:24-bookworm

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# Example binary 1: Gmail CLI
RUN curl -L https://github.com/steipete/gog/releases/latest/download/gog_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/gog

# Example binary 2: Google Places CLI
RUN curl -L https://github.com/steipete/goplaces/releases/latest/download/goplaces_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/goplaces

# Example binary 3: WhatsApp CLI
RUN curl -L https://github.com/steipete/wacli/releases/latest/download/wacli_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/wacli

# Add more binaries below using the same pattern

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

## Construire et lancer

```bash
docker compose build
docker compose up -d openclaw-gateway
```

Si la construction échoue avec `Killed` ou `exit code 137` pendant `pnpm install --frozen-lockfile`, la VM n'a pas assez de mémoire.
Utilisez une classe de machine plus grande avant de réessayer.

Vérifier les binaires :

```bash
docker compose exec openclaw-gateway which gog
docker compose exec openclaw-gateway which goplaces
docker compose exec openclaw-gateway which wacli
```

Résultat attendu :

```
/usr/local/bin/gog
/usr/local/bin/goplaces
/usr/local/bin/wacli
```

Vérifier la Gateway :

```bash
docker compose logs -f openclaw-gateway
```

Résultat attendu :

```
[gateway] listening on ws://0.0.0.0:18789
```

## Ce qui persiste où

OpenClaw s'exécute dans Docker, mais Docker n'est pas la source de vérité.
Tout état de longue durée doit survivre aux redémarrages, reconstructions et reboots.

| Composant           | Localisation                      | Mécanisme de persistance | Notes                            |
| ------------------- | --------------------------------- | ---------------------- | -------------------------------- |
| Configuration Gateway | `/home/node/.openclaw/`           | Montage de volume hôte      | Inclut `openclaw.json`, tokens |
| Profils d'authentification de modèle | `/home/node/.openclaw/`           | Montage de volume hôte      | Jetons OAuth, clés API           |
| Configurations de compétences | `/home/node/.openclaw/skills/`    | Montage de volume hôte      | État au niveau des compétences                |
| Espace de travail de l'agent | `/home/node/.openclaw/workspace/` | Montage de volume hôte      | Code et artefacts de l'agent         |
| Session WhatsApp    | `/home/node/.openclaw/`           | Montage de volume hôte      | Préserve la connexion par code QR               |
| Trousseau Gmail       | `/home/node/.openclaw/`           | Volume hôte + mot de passe | Nécessite `GOG_KEYRING_PASSWORD`  |
| Binaires externes   | `/usr/local/bin/`                 | Image Docker           | Doit être intégré au moment de la construction      |
| Runtime Node        | Système de fichiers du conteneur              | Image Docker           | Reconstruit à chaque construction d'image        |
| Paquets OS         | Système de fichiers du conteneur              | Image Docker           | Ne pas installer au moment de l'exécution        |
| Conteneur Docker    | Éphémère                         | Redémarrable            | Sûr à détruire                  |

## Mises à jour

Pour mettre à jour OpenClaw sur la VM :

```bash
git pull
docker compose build
docker compose up -d
```
