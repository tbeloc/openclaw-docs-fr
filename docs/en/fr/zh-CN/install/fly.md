---
description: Déployer OpenClaw sur Fly.io
title: Fly.io
x-i18n:
  generated_at: "2026-02-03T07:52:55Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a00bae43e416112eb269126445c51492a30abe9e136d89e161fc4193314a876f
  source_path: platforms/fly.md
  workflow: 15
---

# Déploiement sur Fly.io

**Objectif :** Exécuter la passerelle OpenClaw Gateway sur une machine [Fly.io](https://fly.io) avec stockage persistant, HTTPS automatique et accès Discord/canaux.

## Ce dont vous avez besoin

- [flyctl CLI](https://fly.io/docs/hands-on/install-flyctl/) installé
- Un compte Fly.io (forfait gratuit disponible)
- Authentification du modèle : clé API Anthropic (ou clé d'un autre fournisseur)
- Identifiants des canaux : token bot Discord, token Telegram, etc.

## Chemin rapide pour les débutants

1. Cloner le dépôt → personnaliser `fly.toml`
2. Créer l'application + volume → configurer les secrets
3. Déployer avec `fly deploy`
4. SSH dans la machine pour créer la configuration ou utiliser l'interface Control UI

## 1) Créer une application Fly

```bash
# Clone the repo
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Create a new Fly app (pick your own name)
fly apps create my-openclaw

# Create a persistent volume (1GB is usually enough)
fly volumes create openclaw_data --size 1 --region iad
```

**Conseil :** Choisissez une région proche de vous. Options courantes : `lhr` (Londres), `iad` (Virginie), `sjc` (San José).

## 2) Configurer fly.toml

Modifiez `fly.toml` pour correspondre au nom de votre application et à vos besoins.

**Avertissement de sécurité :** La configuration par défaut expose une URL publique. Pour un déploiement renforcé sans IP publique, consultez [Déploiement privé (renforcé)](#déploiement-privé-renforcé) ou utilisez `fly.private.toml`.

```toml
app = "my-openclaw"  # Your app name
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "production"
  OPENCLAW_PREFER_PNPM = "1"
  OPENCLAW_STATE_DIR = "/data"
  NODE_OPTIONS = "--max-old-space-size=1536"

[processes]
  app = "node dist/index.js gateway --allow-unconfigured --port 3000 --bind lan"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1
  processes = ["app"]

[[vm]]
  size = "shared-cpu-2x"
  memory = "2048mb"

[mounts]
  source = "openclaw_data"
  destination = "/data"
```

**Paramètres clés :**

| Paramètre                      | Raison                                                                                |
| ------------------------------ | ------------------------------------------------------------------------------------- |
| `--bind lan`                   | Se lie à `0.0.0.0` pour que le proxy Fly puisse accéder à la passerelle Gateway      |
| `--allow-unconfigured`         | Démarrer sans fichier de configuration (vous en créerez un plus tard)                 |
| `internal_port = 3000`         | Doit correspondre à `--port 3000` (ou `OPENCLAW_GATEWAY_PORT`) pour les vérifications de santé Fly |
| `memory = "2048mb"`            | 512 Mo est trop petit ; 2 Go recommandé                                               |
| `OPENCLAW_STATE_DIR = "/data"` | Persister l'état sur le volume                                                       |

## 3) Configurer les secrets

```bash
# Required: Gateway token (for non-loopback binding)
fly secrets set OPENCLAW_GATEWAY_TOKEN=$(openssl rand -hex 32)

# Model provider API keys
fly secrets set ANTHROPIC_API_KEY=sk-ant-...

# Optional: Other providers
fly secrets set OPENAI_API_KEY=sk-...
fly secrets set GOOGLE_API_KEY=...

# Channel tokens
fly secrets set DISCORD_BOT_TOKEN=MTQ...
```

**Points importants :**

- La liaison non-loopback (`--bind lan`) nécessite `OPENCLAW_GATEWAY_TOKEN` pour des raisons de sécurité.
- Traitez ces tokens comme des mots de passe.
- **Préférez les variables d'environnement aux fichiers de configuration** pour stocker toutes les clés API et tokens. Cela évite que les secrets n'apparaissent dans `openclaw.json`, prévenant les expositions accidentelles ou la journalisation.

## 4) Déployer

```bash
fly deploy
```

Le premier déploiement construit l'image Docker (environ 2-3 minutes). Les déploiements suivants sont plus rapides.

Vérifiez après le déploiement :

```bash
fly status
fly logs
```

Vous devriez voir :

```
[gateway] listening on ws://0.0.0.0:3000 (PID xxx)
[discord] logged in to discord as xxx
```

## 5) Créer le fichier de configuration

SSH dans la machine pour créer la configuration appropriée :

```bash
fly ssh console
```

Créez le répertoire de configuration et le fichier :

```bash
mkdir -p /data
cat > /data/openclaw.json << 'EOF'
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-5",
        "fallbacks": ["anthropic/claude-sonnet-4-5", "openai/gpt-4o"]
      },
      "maxConcurrent": 4
    },
    "list": [
      {
        "id": "main",
        "default": true
      }
    ]
  },
  "auth": {
    "profiles": {
      "anthropic:default": { "mode": "token", "provider": "anthropic" },
      "openai:default": { "mode": "token", "provider": "openai" }
    }
  },
  "bindings": [
    {
      "agentId": "main",
      "match": { "channel": "discord" }
    }
  ],
  "channels": {
    "discord": {
      "enabled": true,
      "groupPolicy": "allowlist",
      "guilds": {
        "YOUR_GUILD_ID": {
          "channels": { "general": { "allow": true } },
          "requireMention": false
        }
      }
    }
  },
  "gateway": {
    "mode": "local",
    "bind": "auto"
  },
  "meta": {
    "lastTouchedVersion": "2026.1.29"
  }
}
EOF
```

**Remarque :** Avec `OPENCLAW_STATE_DIR=/data`, le chemin de configuration est `/data/openclaw.json`.

**Remarque :** Le token Discord peut provenir de :

- Variable d'environnement : `DISCORD_BOT_TOKEN` (recommandé pour les secrets)
- Fichier de configuration : `channels.discord.token`

Si vous utilisez une variable d'environnement, pas besoin d'ajouter le token à la configuration. La passerelle Gateway lira automatiquement `DISCORD_BOT_TOKEN`.

Redémarrez pour appliquer :

```bash
exit
fly machine restart <machine-id>
```

## 6) Accéder à la passerelle Gateway

### Interface Control UI

Ouvrez dans votre navigateur :

```bash
fly open
```

Ou visitez `https://my-openclaw.fly.dev/`

Collez votre token de passerelle Gateway (celui de `OPENCLAW_GATEWAY_TOKEN`) pour vous authentifier.

### Journaux

```bash
fly logs              # Live logs
fly logs --no-tail    # Recent logs
```

### Console SSH

```bash
fly ssh console
```

## Dépannage

### "App is not listening on expected address"

La passerelle Gateway se lie à `127.0.0.1` au lieu de `0.0.0.0`.

**Correction :** Ajoutez `--bind lan` à la commande de processus dans `fly.toml`.

### Vérification de santé échouée / Connexion refusée

Fly ne peut pas accéder à la passerelle Gateway sur le port configuré.

**Correction :** Assurez-vous que `internal_port` correspond au port de la passerelle Gateway (définissez `--port 3000` ou `OPENCLAW_GATEWAY_PORT=3000`).

### OOM / Problèmes de mémoire

Le conteneur redémarre continuellement ou est arrêté. Signes : `SIGABRT`, `v8::internal::Runtime_AllocateInYoungGeneration` ou redémarrages silencieux.

**Correction :** Augmentez la mémoire dans `fly.toml` :

```toml
[[vm]]
  memory = "2048mb"
```

Ou mettez à jour une machine existante :

```bash
fly machine update <machine-id> --vm-memory 2048 -y
```

**Remarque :** 512 Mo est trop petit. 1 Go peut fonctionner mais peut faire OOM sous charge ou avec journalisation détaillée. **2 Go recommandé.**

### Problème de verrou de la passerelle Gateway

La passerelle Gateway refuse de démarrer avec une erreur "already running".

Cela se produit quand le conteneur redémarre mais le fichier de verrou PID persiste sur le volume.

**Correction :** Supprimez le fichier de verrou :

```bash
fly ssh console --command "rm -f /data/gateway.*.lock"
fly machine restart <machine-id>
```

Les fichiers de verrou sont dans `/data/gateway.*.lock` (pas dans les sous-répertoires).

### Configuration non lue

Si vous utilisez `--allow-unconfigured`, la passerelle Gateway crée une configuration minimale. Votre configuration personnalisée dans `/data/openclaw.json` devrait être lue au redémarrage.

Vérifiez que la configuration existe :

```bash
fly ssh console --command "cat /data/openclaw.json"
```

### Écrire la configuration via SSH

La commande `fly ssh console -C` ne supporte pas les redirections shell. Pour écrire un fichier de configuration :

```bash
# Use echo + tee (pipe from local to remote)
echo '{"your":"config"}' | fly ssh console -C "tee /data/openclaw.json"

# Or use sftp
fly sftp shell
> put /local/path/config.json /data/openclaw.json
```

**Remarque :** Si le fichier existe déjà, `fly sftp` peut échouer. Supprimez-le d'abord :

```bash
fly ssh console --command "rm /data/openclaw.json"
```

### État non persistant

Si vous perdez les identifiants ou sessions après redémarrage, le répertoire d'état écrit dans le système de fichiers du conteneur.

**Correction :** Assurez-vous que `OPENCLAW_STATE_DIR=/data` est défini dans `fly.toml` et redéployez.

## Mises à jour

```bash
# Pull latest changes
git pull

# Redeploy
fly deploy

# Check health
fly status
fly logs
```

### Mettre à jour la commande de la machine

Si vous devez modifier la commande de démarrage sans redéploiement complet :

```bash
# Get machine ID
fly machines list

# Update command
fly machine update <machine-id> --command "node dist/index.js gateway --port 3000 --bind lan" -y

# Or with memory increase
fly machine update <machine-id> --vm-memory 2048 --command "node dist/index.js gateway --port 3000 --bind lan" -y
```

**Remarque :** Après `fly deploy`, la commande de la machine peut être réinitialisée au contenu de `fly.toml`. Si vous avez apporté des modifications manuelles, réappliquez-les après le déploiement.

## Déploiement privé (renforcé)

Par défaut, Fly alloue une IP publique, rendant votre passerelle Gateway accessible via `https://your-app.fly.dev`. C'est pratique, mais cela signifie que votre déploiement peut être découvert par les scanners Internet (Shodan, Censys, etc.).

Pour un déploiement renforcé **sans exposition publique**, utilisez le modèle privé.

### Quand utiliser le déploiement privé

- Vous effectuez uniquement des appels/messages **sortants** (pas de webhooks entrants)
- Vous utilisez des tunnels **ngrok ou Tailscale** pour les rappels de webhooks
- Vous accédez à la passerelle Gateway via **SSH, proxy ou WireGuard** plutôt que le navigateur
- Vous voulez que le déploiement soit **caché des scanners Internet**

### Configuration

Utilisez `fly.private.toml` à la place de la configuration standard :

```bash
# Deploy with private config
fly deploy -c fly.private.toml
```

Ou convertissez un déploiement existant :

```bash
# List current IPs
fly ips list -a my-openclaw

# Release public IPs
fly ips release <public-ipv4> -a my-openclaw
fly ips release <public-ipv6> -a my-openclaw

# Switch to private config so future deploys don't re-allocate public IPs
# (remove [http_service] or deploy with the private template)
fly deploy -c fly.private.toml

# Allocate private-only IPv6
fly ips allocate-v6 --private -a my-openclaw
```

Après cela, `fly ips list` ne devrait afficher que des IPs de type `private` :

```
VERSION  IP                   TYPE             REGION
v6       fdaa:x:x:x:x::x      private          global
```

### Accéder au déploiement privé

Sans URL publique, utilisez l'une des méthodes suivantes :

**Option 1 : Proxy local (plus simple)**

```bash
# Forward local port 3000 to the app
fly proxy 3000:3000 -a my-openclaw

# Then open http://localhost:3000 in browser
```

**Option 2 : VPN WireGuard**

```bash
# Create WireGuard config (one-time)
fly wireguard create

# Import to WireGuard client, then access via internal IPv6
# Example: http://[fdaa:x:x:x:x::x]:3000
```

**Option 3 : SSH uniquement**

```bash
fly ssh console -a my-openclaw
```

### Webhooks pour déploiement privé

Si vous avez besoin de rappels de webhooks (Twilio, Telnyx, etc.) sans exposition publique :

1. **Tunnel ngrok**
