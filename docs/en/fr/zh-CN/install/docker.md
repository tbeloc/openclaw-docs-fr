---
read_when:
  - Vous souhaitez conteneuriser la passerelle Gateway plutôt que l'installer localement
  - Vous validez le processus Docker
summary: Configuration Docker optionnelle et onboarding pour OpenClaw
title: Docker
x-i18n:
  generated_at: "2026-02-03T07:51:20Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: bd823e49b6ce76fe1136a42bf48f436b316ed1cd2f9612e3f4919f1e6b2cdee9
  source_path: install/docker.md
  workflow: 15
---

# Docker (Optionnel)

Docker est **optionnel**. Utilisez-le uniquement si vous souhaitez conteneuriser la passerelle Gateway ou valider le processus Docker.

## Docker est-il fait pour moi ?

- **Oui** : Vous souhaitez un environnement Gateway isolé et jetable, ou exécuter OpenClaw sur un hôte sans installation locale.
- **Non** : Vous exécutez sur votre propre machine et souhaitez simplement la boucle de développement la plus rapide. Utilisez plutôt le processus d'installation normal.
- **Remarque sur le bac à sable** : L'isolation du bac à sable des agents utilise également Docker, mais elle **ne nécessite pas** que la passerelle Gateway complète s'exécute dans Docker. Consultez [Isolation du bac à sable](/gateway/sandboxing).

Ce guide couvre :

- Conteneurisation de la passerelle Gateway (OpenClaw complet dans Docker)
- Bac à sable des agents par session (Gateway hôte + outils d'agent isolés par Docker)

Détails sur l'isolation du bac à sable : [Isolation du bac à sable](/gateway/sandboxing)

## Exigences

- Docker Desktop (ou Docker Engine) + Docker Compose v2
- Espace disque suffisant pour les images + journaux

## Passerelle Gateway conteneurisée (Docker Compose)

### Démarrage rapide (recommandé)

À partir du répertoire racine du dépôt :

```bash
./docker-setup.sh
```

Ce script :

- Construit l'image de la passerelle Gateway
- Exécute l'assistant d'onboarding
- Affiche les conseils de configuration des fournisseurs optionnels
- Démarre la passerelle Gateway via Docker Compose
- Génère un jeton Gateway et l'écrit dans `.env`

Variables d'environnement optionnelles :

- `OPENCLAW_DOCKER_APT_PACKAGES` — Installer des paquets apt supplémentaires lors de la construction
- `OPENCLAW_EXTRA_MOUNTS` — Ajouter des montages de liaison d'hôte supplémentaires
- `OPENCLAW_HOME_VOLUME` — Persister `/home/node` dans un volume nommé

Une fois terminé :

- Ouvrez `http://127.0.0.1:18789/` dans votre navigateur.
- Collez le jeton dans l'interface de contrôle (Paramètres → token).
- Besoin de récupérer à nouveau l'URL avec le jeton ? Exécutez `docker compose run --rm openclaw-cli dashboard --no-open`.

Il écrit la configuration/espace de travail sur l'hôte :

- `~/.openclaw/`
- `~/.openclaw/workspace`

Exécution sur un VPS ? Consultez [Hetzner (Docker VPS)](/install/hetzner).

### Processus manuel (compose)

```bash
docker build -t openclaw:local -f Dockerfile .
docker compose run --rm openclaw-cli onboard
docker compose up -d openclaw-gateway
```

Remarque : Exécutez `docker compose ...` à partir du répertoire racine du dépôt. Si vous avez activé `OPENCLAW_EXTRA_MOUNTS` ou `OPENCLAW_HOME_VOLUME`, le script de configuration écrit `docker-compose.extra.yml` ; incluez-le lors de l'exécution de Compose ailleurs :

```bash
docker compose -f docker-compose.yml -f docker-compose.extra.yml <command>
```

### Jeton de l'interface de contrôle + Appairage (Docker)

Si vous voyez « unauthorized » ou « disconnected (1008): pairing required », obtenez un nouveau lien de tableau de bord et approuvez l'appareil du navigateur :

```bash
docker compose run --rm openclaw-cli dashboard --no-open
docker compose run --rm openclaw-cli devices list
docker compose run --rm openclaw-cli devices approve <requestId>
```

Plus de détails : [Tableau de bord](/web/dashboard), [Appareils](/cli/devices).

### Montages supplémentaires (optionnel)

Si vous souhaitez monter des répertoires d'hôte supplémentaires dans le conteneur, définissez `OPENCLAW_EXTRA_MOUNTS` avant d'exécuter `docker-setup.sh`. Cela accepte une liste de montages de liaison Docker séparés par des virgules et les applique à `openclaw-gateway` et `openclaw-cli` en générant `docker-compose.extra.yml`.

Exemple :

```bash
export OPENCLAW_EXTRA_MOUNTS="$HOME/.codex:/home/node/.codex:ro,$HOME/github:/home/node/github:rw"
./docker-setup.sh
```

Remarques :

- Les chemins doivent être partagés avec Docker Desktop sur macOS/Windows.
- Si vous modifiez `OPENCLAW_EXTRA_MOUNTS`, réexécutez `docker-setup.sh` pour régénérer le fichier compose supplémentaire.
- `docker-compose.extra.yml` est généré. Ne le modifiez pas manuellement.

### Persistance du répertoire home du conteneur entier (optionnel)

Si vous souhaitez que `/home/node` persiste après la reconstruction du conteneur, définissez un volume nommé via `OPENCLAW_HOME_VOLUME`. Cela crée un volume Docker et le monte sur `/home/node`, tout en conservant les montages de liaison standard pour la configuration/espace de travail. Utilisez un volume nommé ici (pas un chemin de liaison) ; pour les montages de liaison, utilisez `OPENCLAW_EXTRA_MOUNTS`.

Exemple :

```bash
export OPENCLAW_HOME_VOLUME="openclaw_home"
./docker-setup.sh
```

Vous pouvez le combiner avec des montages supplémentaires :

```bash
export OPENCLAW_HOME_VOLUME="openclaw_home"
export OPENCLAW_EXTRA_MOUNTS="$HOME/.codex:/home/node/.codex:ro,$HOME/github:/home/node/github:rw"
./docker-setup.sh
```

Remarques :

- Si vous modifiez `OPENCLAW_HOME_VOLUME`, réexécutez `docker-setup.sh` pour régénérer le fichier compose supplémentaire.
- Les volumes nommés persistent jusqu'à suppression avec `docker volume rm <name>`.

### Installation de paquets apt supplémentaires (optionnel)

Si vous avez besoin de paquets système dans l'image (par exemple, outils de construction ou bibliothèques multimédia), définissez `OPENCLAW_DOCKER_APT_PACKAGES` avant d'exécuter `docker-setup.sh`. Cela installe les paquets lors de la construction de l'image, ils persistent donc même si le conteneur est supprimé.

Exemple :

```bash
export OPENCLAW_DOCKER_APT_PACKAGES="ffmpeg build-essential"
./docker-setup.sh
```

Remarques :

- Cela accepte une liste de noms de paquets apt séparés par des espaces.
- Si vous modifiez `OPENCLAW_DOCKER_APT_PACKAGES`, réexécutez `docker-setup.sh` pour reconstruire l'image.

### Utilisateurs avancés / Conteneur complet en fonctionnalités (opt-in)

L'image Docker par défaut est **sécurité d'abord**, exécutée en tant qu'utilisateur non-root `node`. Cela maintient une surface d'attaque réduite, mais cela signifie :

- Impossible d'installer des paquets système au moment de l'exécution
- Pas de Homebrew par défaut
- Pas de navigateur Chromium/Playwright fourni

Si vous souhaitez un conteneur plus complet en fonctionnalités, utilisez ces options opt-in :

1. **Persistez `/home/node`** pour que les téléchargements de navigateur et les caches d'outils soient conservés :

```bash
export OPENCLAW_HOME_VOLUME="openclaw_home"
./docker-setup.sh
```

2. **Intégrez les dépendances système dans l'image** (répétable + persistant) :

```bash
export OPENCLAW_DOCKER_APT_PACKAGES="git curl jq"
./docker-setup.sh
```

3. **Installez les navigateurs Playwright sans utiliser `npx`** (évitez les conflits de couverture npm) :

```bash
docker compose run --rm openclaw-cli \
  node /app/node_modules/playwright-core/cli.js install chromium
```

Si vous avez besoin que Playwright installe les dépendances système, reconstruisez l'image avec `OPENCLAW_DOCKER_APT_PACKAGES` plutôt que d'utiliser `--with-deps` au moment de l'exécution.

4. **Persistez les téléchargements de navigateur Playwright** :

- Définissez `PLAYWRIGHT_BROWSERS_PATH=/home/node/.cache/ms-playwright` dans `docker-compose.yml`.
- Assurez-vous que `/home/node` persiste via `OPENCLAW_HOME_VOLUME`, ou montez `/home/node/.cache/ms-playwright` via `OPENCLAW_EXTRA_MOUNTS`.

### Permissions + EACCES

L'image s'exécute en tant que `node` (uid 1000). Si vous voyez des erreurs de permission sur `/home/node/.openclaw`, assurez-vous que votre montage de liaison d'hôte est détenu par uid 1000.

Exemple (hôte Linux) :

```bash
sudo chown -R 1000:1000 /path/to/openclaw-config /path/to/openclaw-workspace
```

Si vous choisissez de s'exécuter en tant que root pour la commodité, vous acceptez les compromis de sécurité.

### Reconstruction plus rapide (recommandé)

Pour accélérer les reconstructions, ordonnez votre Dockerfile pour que les couches de dépendances soient mises en cache. Cela évite de réexécuter `pnpm install` sauf si le fichier de verrouillage change :

```dockerfile
FROM node:22-bookworm

# Installer Bun (requis par les scripts de construction)
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"

RUN corepack enable

WORKDIR /app

# Mettre en cache les dépendances, sauf si les métadonnées de paquets changent
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY ui/package.json ./ui/package.json
COPY scripts ./scripts

RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build
RUN pnpm ui:install
RUN pnpm ui:build

ENV NODE_ENV=production

CMD ["node","dist/index.js"]
```

### Configuration des canaux (optionnel)

Utilisez le conteneur CLI pour configurer les canaux, puis redémarrez la passerelle Gateway si nécessaire.

WhatsApp (QR) :

```bash
docker compose run --rm openclaw-cli channels login
```

Telegram (jeton bot) :

```bash
docker compose run --rm openclaw-cli channels add --channel telegram --token "<token>"
```

Discord (jeton bot) :

```bash
docker compose run --rm openclaw-cli channels add --channel discord --token "<token>"
```

Documentation : [WhatsApp](/channels/whatsapp), [Telegram](/channels/telegram), [Discord](/channels/discord)

### OpenAI Codex OAuth (Docker sans tête)

Si vous sélectionnez OpenAI Codex OAuth dans l'assistant, il ouvrira une URL de navigateur et tentera de capturer le rappel à `http://127.0.0.1:1455/auth/callback`. Dans Docker ou les configurations sans tête, ce rappel peut afficher une erreur de navigateur. Copiez l'URL de redirection complète à laquelle vous êtes arrivé et collez-la dans l'assistant pour terminer l'authentification.

### Vérification de santé

```bash
docker compose exec openclaw-gateway node dist/index.js health --token "$OPENCLAW_GATEWAY_TOKEN"
```

### Test de fumée E2E (Docker)

```bash
scripts/e2e/onboard-docker.sh
```

### Test de fumée d'importation QR (Docker)

```bash
pnpm test:docker:qr
```

### Remarques

- La passerelle Gateway se lie par défaut à `lan` pour l'utilisation du conteneur.
- Le CMD Dockerfile utilise `--allow-unconfigured` ; la configuration montée démarrera quand même si `gateway.mode` n'est pas `local`. Remplacez CMD pour forcer la vérification.
- Le conteneur Gateway est la source de vérité pour les sessions (`~/.openclaw/agents/<agentId>/sessions/`).

## Bac à sable des agents (Gateway hôte + outils Docker)

Approfondissez : [Isolation du bac à sable](/gateway/sandboxing)

### Ce qu'il fait

Lorsque `agents.defaults.sandbox` est activé, les **sessions non-principales** exécutent les outils dans un conteneur Docker. La passerelle Gateway reste sur votre hôte, mais l'exécution des outils est isolée :

- scope : par défaut `"agent"` (un conteneur + espace de travail par agent)
- scope : `"session"` pour l'isolation par session
- Dossier d'espace de travail par scope monté sur `/workspace`
- Accès optionnel à l'espace de travail de l'agent (`agents.defaults.sandbox.workspaceAccess`)
- Politiques d'outils d'autorisation/refus (refus prioritaire)
- Les médias entrants sont copiés dans l'espace de travail du bac à sable actif (`media/inbound/*`), afin que les outils puissent les lire (avec `workspaceAccess: "rw"`, cela se trouve dans l'espace de travail de l'agent)

Avertissement : `scope: "shared"` désactive l'isolation entre sessions. Toutes les sessions partagent un conteneur et un espace de travail.

### Fichier de configuration du bac à sable par agent (multi-agent)

Si vous utilisez le routage multi-agent, chaque agent peut remplacer les paramètres du bac à sable + outils : `agents.list[].sandbox` et `agents.list[].tools` (plus `agents.list[].tools.sandbox.tools`). Cela vous permet d'exécuter des niveaux d'accès mixtes dans une seule passerelle Gateway :

- Accès complet (agent personnel)
- Outils en lecture
