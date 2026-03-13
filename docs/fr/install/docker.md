---
summary: "Configuration Docker optionnelle et intégration pour OpenClaw"
read_when:
  - You want a containerized gateway instead of local installs
  - You are validating the Docker flow
title: "Docker"
---

# Docker (optionnel)

Docker est **optionnel**. Utilisez-le uniquement si vous souhaitez une passerelle conteneurisée ou valider le flux Docker.

## Docker est-il fait pour moi ?

- **Oui** : vous souhaitez un environnement de passerelle isolé et jetable, ou exécuter OpenClaw sur un hôte sans installations locales.
- **Non** : vous exécutez sur votre propre machine et souhaitez simplement la boucle de développement la plus rapide. Utilisez plutôt le flux d'installation normal.
- **Note sur le sandboxing** : le sandboxing des agents utilise également Docker, mais il ne nécessite **pas** que la passerelle complète s'exécute dans Docker. Voir [Sandboxing](/gateway/sandboxing).

Ce guide couvre :

- Passerelle conteneurisée (OpenClaw complet dans Docker)
- Sandbox d'agent par session (passerelle hôte + outils d'agent isolés Docker)

Détails du sandboxing : [Sandboxing](/gateway/sandboxing)

## Exigences

- Docker Desktop (ou Docker Engine) + Docker Compose v2
- Au moins 2 Go de RAM pour la construction d'image (`pnpm install` peut être tué par OOM sur les hôtes 1 Go avec sortie 137)
- Espace disque suffisant pour les images + journaux
- Si vous exécutez sur un VPS/hôte public, consultez
  [Durcissement de la sécurité pour l'exposition réseau](/gateway/security#04-network-exposure-bind--port--firewall),
  en particulier la politique de pare-feu Docker `DOCKER-USER`.

## Passerelle conteneurisée (Docker Compose)

### Démarrage rapide (recommandé)

<Note>
Les paramètres par défaut de Docker supposent ici des modes de liaison (`lan`/`loopback`), pas des alias d'hôte. Utilisez les valeurs du mode de liaison dans `gateway.bind` (par exemple `lan` ou `loopback`), pas les alias d'hôte comme `0.0.0.0` ou `localhost`.
</Note>

À partir de la racine du dépôt :

```bash
./docker-setup.sh
```

Ce script :

- construit l'image de la passerelle localement (ou récupère une image distante si `OPENCLAW_IMAGE` est défini)
- exécute l'assistant d'intégration
- imprime des conseils de configuration de fournisseur optionnels
- démarre la passerelle via Docker Compose
- génère un jeton de passerelle et l'écrit dans `.env`

Variables d'environnement optionnelles :

- `OPENCLAW_IMAGE` — utiliser une image distante au lieu de construire localement (par exemple `ghcr.io/openclaw/openclaw:latest`)
- `OPENCLAW_DOCKER_APT_PACKAGES` — installer des packages apt supplémentaires lors de la construction
- `OPENCLAW_EXTENSIONS` — pré-installer les dépendances d'extension au moment de la construction (noms d'extension séparés par des espaces, par exemple `diagnostics-otel matrix`)
- `OPENCLAW_EXTRA_MOUNTS` — ajouter des montages de liaison d'hôte supplémentaires
- `OPENCLAW_HOME_VOLUME` — persister `/home/node` dans un volume nommé
- `OPENCLAW_SANDBOX` — opter pour le bootstrap du sandbox de passerelle Docker. Seules les valeurs explicitement vraies l'activent : `1`, `true`, `yes`, `on`
- `OPENCLAW_INSTALL_DOCKER_CLI` — passage d'argument de construction pour les constructions d'image locales (`1` installe Docker CLI dans l'image). `docker-setup.sh` le définit automatiquement quand `OPENCLAW_SANDBOX=1` pour les constructions locales.
- `OPENCLAW_DOCKER_SOCKET` — remplacer le chemin du socket Docker (par défaut : chemin `DOCKER_HOST=unix://...`, sinon `/var/run/docker.sock`)
- `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` — break-glass : autoriser les cibles `ws://` de réseau privé approuvées pour les chemins du client CLI/intégration (par défaut loopback uniquement)
- `OPENCLAW_BROWSER_DISABLE_GRAPHICS_FLAGS=0` — désactiver les drapeaux de durcissement du navigateur conteneur `--disable-3d-apis`, `--disable-software-rasterizer`, `--disable-gpu` quand vous avez besoin de compatibilité WebGL/3D.
- `OPENCLAW_BROWSER_DISABLE_EXTENSIONS=0` — garder les extensions activées quand les flux de navigateur les nécessitent (par défaut garde les extensions désactivées dans le navigateur sandbox).
- `OPENCLAW_BROWSER_RENDERER_PROCESS_LIMIT=<N>` — définir la limite de processus de rendu Chromium ; définir à `0` pour ignorer le drapeau et utiliser le comportement par défaut de Chromium.

Après son exécution :

- Ouvrez `http://127.0.0.1:18789/` dans votre navigateur.
- Collez le jeton dans l'interface utilisateur de contrôle (Paramètres → jeton).
- Besoin de l'URL à nouveau ? Exécutez `docker compose run --rm openclaw-cli dashboard --no-open`.

### Activer le sandbox d'agent pour la passerelle Docker (opt-in)

`docker-setup.sh` peut également bootstrap `agents.defaults.sandbox.*` pour les déploiements Docker.

Activez avec :

```bash
export OPENCLAW_SANDBOX=1
./docker-setup.sh
```

Chemin de socket personnalisé (par exemple Docker sans racine) :

```bash
export OPENCLAW_SANDBOX=1
export OPENCLAW_DOCKER_SOCKET=/run/user/1000/docker.sock
./docker-setup.sh
```

Notes :

- Le script monte `docker.sock` uniquement après que les prérequis du sandbox réussissent.
- Si la configuration du sandbox ne peut pas être complétée, le script réinitialise `agents.defaults.sandbox.mode` à `off` pour éviter une configuration de sandbox obsolète/cassée lors des réexécutions.
- Si `Dockerfile.sandbox` est manquant, le script imprime un avertissement et continue ; construisez `openclaw-sandbox:bookworm-slim` avec `scripts/sandbox-setup.sh` si nécessaire.
- Pour les valeurs `OPENCLAW_IMAGE` non locales, l'image doit déjà contenir le support Docker CLI pour l'exécution du sandbox.

### Automatisation/CI (non-interactif, sans bruit TTY)

Pour les scripts et CI, désactivez l'allocation pseudo-TTY de Compose avec `-T` :

```bash
docker compose run -T --rm openclaw-cli gateway probe
docker compose run -T --rm openclaw-cli devices list --json
```

Si votre automatisation n'exporte aucune variable de session Claude, les laisser non définies se résout maintenant en valeurs vides par défaut dans `docker-compose.yml` pour éviter les avertissements répétés « variable is not set ».

### Note de sécurité réseau partagé (CLI + passerelle)

`openclaw-cli` utilise `network_mode: "service:openclaw-gateway"` pour que les commandes CLI puissent atteindre de manière fiable la passerelle sur `127.0.0.1` dans Docker.

Traitez ceci comme une limite de confiance partagée : la liaison loopback n'est pas une isolation entre ces deux conteneurs. Si vous avez besoin d'une séparation plus forte, exécutez les commandes à partir d'un chemin de conteneur/réseau hôte séparé au lieu du service `openclaw-cli` fourni.

Pour réduire l'impact si le processus CLI est compromis, la configuration compose supprime `NET_RAW`/`NET_ADMIN` et active `no-new-privileges` sur `openclaw-cli`.

Il écrit la configuration/espace de travail sur l'hôte :

- `~/.openclaw/`
- `~/.openclaw/workspace`

Exécution sur un VPS ? Voir [Hetzner (Docker VPS)](/install/hetzner).

### Utiliser une image distante (ignorer la construction locale)

Les images pré-construites officielles sont publiées à :

- [Package GitHub Container Registry](https://github.com/openclaw/openclaw/pkgs/container/openclaw)

Utilisez le nom d'image `ghcr.io/openclaw/openclaw` (pas les images Docker Hub portant des noms similaires).

Balises courantes :

- `main` — dernière construction de `main`
- `<version>` — constructions de balises de version (par exemple `2026.2.26`)
- `latest` — dernière balise de version stable

### Métadonnées d'image de base

L'image Docker principale utilise actuellement :

- `node:24-bookworm`

L'image docker publie maintenant les annotations de base-image OCI (sha256 est un exemple et pointe vers la liste de manifeste multi-arch épinglée pour cette balise) :

- `org.opencontainers.image.base.name=docker.io/library/node:24-bookworm`
- `org.opencontainers.image.base.digest=sha256:3a09aa6354567619221ef6c45a5051b671f953f0a1924d1f819ffb236e520e6b`
- `org.opencontainers.image.source=https://github.com/openclaw/openclaw`
- `org.opencontainers.image.url=https://openclaw.ai`
- `org.opencontainers.image.documentation=https://docs.openclaw.ai/install/docker`
- `org.opencontainers.image.licenses=MIT`
- `org.opencontainers.image.title=OpenClaw`
- `org.opencontainers.image.description=OpenClaw gateway and CLI runtime container image`
- `org.opencontainers.image.revision=<git-sha>`
- `org.opencontainers.image.version=<tag-or-main>`
- `org.opencontainers.image.created=<rfc3339 timestamp>`

Référence : [Annotations d'image OCI](https://github.com/opencontainers/image-spec/blob/main/annotations.md)

Contexte de version : l'historique balisé de ce dépôt utilise déjà Bookworm dans `v2026.2.22` et les balises 2026 antérieures (par exemple `v2026.2.21`, `v2026.2.9`).

Par défaut, le script de configuration construit l'image à partir de la source. Pour récupérer une image pré-construite à la place, définissez `OPENCLAW_IMAGE` avant d'exécuter le script :

```bash
export OPENCLAW_IMAGE="ghcr.io/openclaw/openclaw:latest"
./docker-setup.sh
```

Le script détecte que `OPENCLAW_IMAGE` n'est pas la valeur par défaut `openclaw:local` et exécute `docker pull` au lieu de `docker build`. Tout le reste (intégration, démarrage de la passerelle, génération de jeton) fonctionne de la même manière.

`docker-setup.sh` s'exécute toujours à partir de la racine du dépôt car il utilise le `docker-compose.yml` local et les fichiers d'aide. `OPENCLAW_IMAGE` ignore le temps de construction d'image locale ; il ne remplace pas le flux de composition/configuration.

### Assistants Shell (optionnel)

Pour une gestion Docker plus facile au quotidien, installez `ClawDock` :

```bash
mkdir -p ~/.clawdock && curl -sL https://raw.githubusercontent.com/openclaw/openclaw/main/scripts/shell-helpers/clawdock-helpers.sh -o ~/.clawdock/clawdock-helpers.sh
```

**Ajouter à votre configuration shell (zsh) :**

```bash
echo 'source ~/.clawdock/clawdock-helpers.sh' >> ~/.zshrc && source ~/.zshrc
```

Utilisez ensuite `clawdock-start`, `clawdock-stop`, `clawdock-dashboard`, etc. Exécutez `clawdock-help` pour toutes les commandes.

Voir [README d'aide `ClawDock`](https://github.com/openclaw/openclaw/blob/main/scripts/shell-helpers/README.md) pour les détails.

### Flux manuel (compose)

```bash
docker build -t openclaw:local -f Dockerfile .
docker compose run --rm openclaw-cli onboard
docker compose up -d openclaw-gateway
```

Remarque : exécutez `docker compose ...` à partir de la racine du dépôt. Si vous avez activé `OPENCLAW_EXTRA_MOUNTS` ou `OPENCLAW_HOME_VOLUME`, le script de configuration écrit `docker-compose.extra.yml` ; incluez-le lors de l'exécution de Compose ailleurs :

```bash
docker compose -f docker-compose.yml -f docker-compose.extra.yml <command>
```

### Jeton de l'interface utilisateur de contrôle + appairage (Docker)

Si vous voyez « unauthorized » ou « disconnected (1008): pairing required », récupérez un lien de tableau de bord frais et approuvez l'appareil du navigateur :

```bash
docker compose run --rm openclaw-cli dashboard --no-open
docker compose run --rm openclaw-cli devices list
docker compose run --rm openclaw-cli devices approve <requestId>
```

Plus de détails : [Dashboard](/web/dashboard), [Devices](/cli/devices).

### Montages supplémentaires (optionnel)

Si vous souhaitez monter des répertoires d'hôte supplémentaires dans les conteneurs, définissez `OPENCLAW_EXTRA_MOUNTS` avant d'exécuter `docker-setup.sh`. Ceci accepte une liste de montages de liaison Docker séparée par des virgules et les applique à la fois à `openclaw-gateway` et `openclaw-cli` en générant `docker-compose.extra.yml`.

Exemple :

```bash
export OPENCLAW_EXTRA_MOUNTS="$HOME/.codex:/home/node/.codex:ro,$HOME/github:/home/node/github:rw"
./docker-setup.sh
```

Notes :

- Les chemins doivent être partagés avec Docker Desktop sur macOS/Windows.
- Chaque entrée doit être `source:target[:options]` sans espaces, tabulations ou sauts de ligne.
- Si vous modifiez `OPENCLAW_EXTRA_MOUNTS`, réexécutez `docker-setup.sh` pour régénérer le fichier compose supplémentaire.
- `docker-compose.extra.yml` est généré. Ne le modifiez pas manuellement.

### Persister l'intégralité du répertoire personnel du conteneur (optionnel)

Si vous souhaitez que `/home/node` persiste lors de la recréation du conteneur, définissez un volume nommé via `OPENCLAW_
