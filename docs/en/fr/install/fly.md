---
title: Fly.io
description: Déployer OpenClaw sur Fly.io
summary: "Déploiement étape par étape sur Fly.io pour OpenClaw avec stockage persistant et HTTPS"
read_when:
  - Deploying OpenClaw on Fly.io
  - Setting up Fly volumes, secrets, and first-run config
---

# Déploiement Fly.io

**Objectif :** OpenClaw Gateway s'exécutant sur une machine [Fly.io](https://fly.io) avec stockage persistant, HTTPS automatique et accès Discord/canal.

## Ce dont vous avez besoin

- [flyctl CLI](https://fly.io/docs/hands-on/install-flyctl/) installé
- Compte Fly.io (le niveau gratuit fonctionne)
- Authentification du modèle : clé API pour votre fournisseur de modèle choisi
- Identifiants du canal : jeton bot Discord, jeton Telegram, etc.

## Chemin rapide pour les débutants

1. Cloner le repo → personnaliser `fly.toml`
2. Créer l'app + volume → définir les secrets
3. Déployer avec `fly deploy`
4. SSH pour créer la config ou utiliser l'interface de contrôle

## 1) Créer l'app Fly

```bash
# Cloner le repo
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Créer une nouvelle app Fly (choisissez votre propre nom)
fly apps create my-openclaw

# Créer un volume persistant (1 Go est généralement suffisant)
fly volumes create openclaw_data --size 1 --region iad
```

**Conseil :** Choisissez une région proche de vous. Options courantes : `lhr` (Londres), `iad` (Virginie), `sjc` (San Jose).

## 2) Configurer fly.toml

Modifiez `fly.toml` pour correspondre à votre nom d'app et vos exigences.

**Note de sécurité :** La configuration par défaut expose une URL publique. Pour un déploiement renforcé sans IP publique, voir [Déploiement privé](#private-deployment-hardened) ou utiliser `fly.private.toml`.

```toml
app = "my-openclaw"  # Votre nom d'app
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

| Paramètre                      | Pourquoi                                                                    |
| ------------------------------ | --------------------------------------------------------------------------- |
| `--bind lan`                   | Se lie à `0.0.0.0` pour que le proxy Fly puisse atteindre la gateway       |
| `--allow-unconfigured`         | Démarre sans fichier config (vous en créerez un après)                     |
| `internal_port = 3000`         | Doit correspondre à `--port 3000` (ou `OPENCLAW_GATEWAY_PORT`) pour les vérifications de santé Fly |
| `memory = "2048mb"`            | 512 Mo est trop petit ; 2 Go recommandé                                    |
| `OPENCLAW_STATE_DIR = "/data"` | Persiste l'état sur le volume                                              |

## 3) Définir les secrets

```bash
# Requis : jeton Gateway (pour la liaison non-loopback)
fly secrets set OPENCLAW_GATEWAY_TOKEN=$(openssl rand -hex 32)

# Clés API du fournisseur de modèle
fly secrets set ANTHROPIC_API_KEY=sk-ant-...

# Optionnel : autres fournisseurs
fly secrets set OPENAI_API_KEY=sk-...
fly secrets set GOOGLE_API_KEY=...

# Jetons de canal
fly secrets set DISCORD_BOT_TOKEN=MTQ...
```

**Notes :**

- Les liaisons non-loopback (`--bind lan`) nécessitent `OPENCLAW_GATEWAY_TOKEN` pour la sécurité.
- Traitez ces jetons comme des mots de passe.
- **Préférez les variables d'environnement au fichier config** pour toutes les clés API et jetons. Cela garde les secrets hors de `openclaw.json` où ils pourraient être accidentellement exposés ou enregistrés.

## 4) Déployer

```bash
fly deploy
```

Le premier déploiement construit l'image Docker (~2-3 minutes). Les déploiements suivants sont plus rapides.

Après le déploiement, vérifiez :

```bash
fly status
fly logs
```

Vous devriez voir :

```
[gateway] listening on ws://0.0.0.0:3000 (PID xxx)
[discord] logged in to discord as xxx
```

## 5) Créer le fichier config

SSH dans la machine pour créer une config appropriée :

```bash
fly ssh console
```

Créer le répertoire et le fichier config :

```bash
mkdir -p /data
cat > /data/openclaw.json << 'EOF'
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-6",
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

**Note :** Avec `OPENCLAW_STATE_DIR=/data`, le chemin config est `/data/openclaw.json`.

**Note :** Le jeton Discord peut provenir de :

- Variable d'environnement : `DISCORD_BOT_TOKEN` (recommandé pour les secrets)
- Fichier config : `channels.discord.token`

Si vous utilisez une variable d'environnement, pas besoin d'ajouter le jeton à la config. La gateway lit `DISCORD_BOT_TOKEN` automatiquement.

Redémarrer pour appliquer :

```bash
exit
fly machine restart <machine-id>
```

## 6) Accéder à la Gateway

### Interface de contrôle

Ouvrir dans le navigateur :

```bash
fly open
```

Ou visiter `https://my-openclaw.fly.dev/`

Collez votre jeton gateway (celui de `OPENCLAW_GATEWAY_TOKEN`) pour vous authentifier.

### Logs

```bash
fly logs              # Logs en direct
fly logs --no-tail    # Logs récents
```

### Console SSH

```bash
fly ssh console
```

## Dépannage

### "App is not listening on expected address"

La gateway se lie à `127.0.0.1` au lieu de `0.0.0.0`.

**Solution :** Ajoutez `--bind lan` à votre commande de processus dans `fly.toml`.

### Les vérifications de santé échouent / connexion refusée

Fly ne peut pas atteindre la gateway sur le port configuré.

**Solution :** Assurez-vous que `internal_port` correspond au port de la gateway (définissez `--port 3000` ou `OPENCLAW_GATEWAY_PORT=3000`).

### OOM / Problèmes de mémoire

Le conteneur continue de redémarrer ou se fait tuer. Signes : `SIGABRT`, `v8::internal::Runtime_AllocateInYoungGeneration`, ou redémarrages silencieux.

**Solution :** Augmentez la mémoire dans `fly.toml` :

```toml
[[vm]]
  memory = "2048mb"
```

Ou mettez à jour une machine existante :

```bash
fly machine update <machine-id> --vm-memory 2048 -y
```

**Note :** 512 Mo est trop petit. 1 Go peut fonctionner mais peut faire un OOM sous charge ou avec un enregistrement détaillé. **2 Go est recommandé.**

### Problèmes de verrouillage de Gateway

La gateway refuse de démarrer avec des erreurs "already running".

Cela se produit quand le conteneur redémarre mais le fichier de verrouillage PID persiste sur le volume.

**Solution :** Supprimez le fichier de verrouillage :

```bash
fly ssh console --command "rm -f /data/gateway.*.lock"
fly machine restart <machine-id>
```

Le fichier de verrouillage est à `/data/gateway.*.lock` (pas dans un sous-répertoire).

### Config non lue

Si vous utilisez `--allow-unconfigured`, la gateway crée une config minimale. Votre config personnalisée à `/data/openclaw.json` devrait être lue au redémarrage.

Vérifiez que la config existe :

```bash
fly ssh console --command "cat /data/openclaw.json"
```

### Écrire la config via SSH

La commande `fly ssh console -C` ne supporte pas la redirection shell. Pour écrire un fichier config :

```bash
# Utiliser echo + tee (pipe du local au distant)
echo '{"your":"config"}' | fly ssh console -C "tee /data/openclaw.json"

# Ou utiliser sftp
fly sftp shell
> put /local/path/config.json /data/openclaw.json
```

**Note :** `fly sftp` peut échouer si le fichier existe déjà. Supprimez d'abord :

```bash
fly ssh console --command "rm /data/openclaw.json"
```

### L'état ne persiste pas

Si vous perdez les identifiants ou les sessions après un redémarrage, le répertoire d'état écrit dans le système de fichiers du conteneur.

**Solution :** Assurez-vous que `OPENCLAW_STATE_DIR=/data` est défini dans `fly.toml` et redéployez.

## Mises à jour

```bash
# Récupérer les derniers changements
git pull

# Redéployer
fly deploy

# Vérifier la santé
fly status
fly logs
```

### Mise à jour de la commande de machine

Si vous devez changer la commande de démarrage sans redéploiement complet :

```bash
# Obtenir l'ID de la machine
fly machines list

# Mettre à jour la commande
fly machine update <machine-id> --command "node dist/index.js gateway --port 3000 --bind lan" -y

# Ou avec augmentation de mémoire
fly machine update <machine-id> --vm-memory 2048 --command "node dist/index.js gateway --port 3000 --bind lan" -y
```

**Note :** Après `fly deploy`, la commande de la machine peut réinitialiser à ce qui est dans `fly.toml`. Si vous avez fait des modifications manuelles, réappliquez-les après le déploiement.

## Déploiement privé (renforcé)

Par défaut, Fly alloue des IPs publiques, rendant votre gateway accessible à `https://your-app.fly.dev`. C'est pratique mais cela signifie que votre déploiement est découvrable par les scanners Internet (Shodan, Censys, etc.).

Pour un déploiement renforcé **sans exposition publique**, utilisez le modèle privé.

### Quand utiliser le déploiement privé

- Vous ne faites que des appels/messages **sortants** (pas de webhooks entrants)
- Vous utilisez des tunnels **ngrok ou Tailscale** pour les rappels de webhook
- Vous accédez à la gateway via **SSH, proxy ou WireGuard** au lieu du navigateur
- Vous voulez que le déploiement soit **caché des scanners Internet**

### Configuration

Utilisez `fly.private.toml` au lieu de la config standard :

```bash
# Déployer avec la config privée
fly deploy -c fly.private.toml
```

Ou convertir un déploiement existant :

```bash
# Lister les IPs actuelles
fly ips list -a my-openclaw

# Libérer les IPs publiques
fly ips release <public-ipv4> -a my-openclaw
fly ips release <public-ipv6> -a my-openclaw

# Basculer vers la config privée pour que les futurs déploiements ne réallouent pas les IPs publiques
# (supprimer [http_service] ou déployer avec le modèle privé)
fly deploy -c fly.private.toml

# Allouer IPv6 privée uniquement
fly ips allocate-v6 --private -a my-openclaw
```

Après cela, `fly ips list` devrait afficher uniquement une IP de type `private` :

```
VERSION  IP                   TYPE             REGION
v6       fdaa:x:x:x:x::x      private          global
```

### Accéder à un déploiement privé

Puisqu'il n'y a pas d'URL publique, utilisez l'une de ces méthodes :

**Option 1 : Proxy local (le plus simple)**

```bash
# Transférer le port local 3000 vers l'app
fly proxy 3000:3000 -a my-openclaw

# Puis ouvrir http://localhost:3000 dans le navigateur
```

**Option 2 : VPN WireGuard**

```bash
# Créer la config WireGuard (une seule fois)
fly wireguard create

# Importer dans le client WireGuard, puis accéder via IPv6 interne
# Exemple : http://[fdaa:x:x:x:x::x]:3000
```

**Option 3 : SSH uniquement**

```bash
fly ssh console -a my-openclaw
```

### Webhooks avec déploiement privé

Si vous avez besoin de rappels de webhook (Twilio, Telnyx, etc.) sans exposition publique :

1. **Tunnel ngrok** - Exécuter ngrok à l'intérieur du conteneur ou en tant que sidecar
2. **Tailscale Funnel** - Exposer des chemins spécifiques via Tailscale
3. **Sortant uniquement** - Certains fournisseurs (Twilio) fonctionnent bien pour les appels sortants sans webhooks

Exemple de config d'appel vocal avec ngrok :

```json
{
  "plugins": {
    "entries": {
      "voice-call": {
        "enabled": true,
        "config": {
          "provider": "twilio",
          "tunnel": { "provider": "ngrok" },
          "webhookSecurity": {
            "allowedHosts": ["example.ngrok.app"]
          }
        }
      }
    }
  }
}
```

Le tunnel ngrok s'exécute à l'intérieur du conteneur et fournit une URL de webhook publique sans exposer l'app Fly elle-même. Définissez `webhookSecurity.allowedHosts` au nom d'hôte du tunnel public pour que les en-têtes d'hôte transférés soient acceptés.

### Avantages de sécurité

| Aspect            | Public       | Privé      |
| ----------------- | ------------ | ---------- |
| Scanners Internet | Découvrable  | Caché      |
| Attaques directes | Possible     | Bloqué     |
| Accès UI contrôle | Navigateur   | Proxy/VPN  |
| Livraison webhook | Directe      | Via tunnel |

## Notes

- Fly.io utilise l'architecture **x86** (pas ARM)
- Le Dockerfile est compatible avec les deux architectures
- Pour l'intégration WhatsApp/Telegram, utilisez `fly ssh console`
- Les données persistantes se trouvent sur le volume à `/data`
- Signal nécessite Java + signal-cli ; utilisez une image personnalisée et maintenez la mémoire à 2GB+.

## Coût

Avec la configuration recommandée (`shared-cpu-2x`, 2GB RAM) :

- ~10-15$/mois selon l'utilisation
- Le niveau gratuit inclut une certaine allocation

Consultez [Fly.io pricing](https://fly.io/docs/about/pricing/) pour plus de détails.
