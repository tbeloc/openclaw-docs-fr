---
read_when:
  - Configurer OpenClaw sur DigitalOcean
  - Chercher un hébergement VPS bon marché pour exécuter OpenClaw
summary: Exécuter OpenClaw sur DigitalOcean (option VPS payante simple)
title: DigitalOcean
x-i18n:
  generated_at: "2026-02-03T07:51:55Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: d60559b8751da37413e5364e83c88254b476b2283386a0b07b2ca6b4e16157fc
  source_path: platforms/digitalocean.md
  workflow: 15
---

# Exécuter OpenClaw sur DigitalOcean

## Objectif

Exécuter une passerelle OpenClaw Gateway persistante sur DigitalOcean pour **$6/mois** (ou $4/mois avec la tarification réservée).

Si vous cherchez une option à $0/mois et que vous ne craignez pas une configuration ARM + spécifique à un fournisseur, consultez le [guide Oracle Cloud](/platforms/oracle).

## Comparaison des coûts (2026)

| Fournisseur  | Plan            | Configuration             | Prix/mois   | Remarques                    |
| ------------ | --------------- | ------------------------- | ----------- | ---------------------------- |
| Oracle Cloud | Always Free ARM | Jusqu'à 4 OCPU, 24GB RAM  | $0          | ARM, capacité limitée / pièges d'inscription |
| Hetzner      | CX22            | 2 vCPU, 4GB RAM           | €3.79 (~$4) | Option payante la moins chère |
| DigitalOcean | Basic           | 1 vCPU, 1GB RAM           | $6          | Interface simple, documentation complète |
| Vultr        | Cloud Compute   | 1 vCPU, 1GB RAM           | $6          | Plusieurs régions disponibles |
| Linode       | Nanode          | 1 vCPU, 1GB RAM           | $5          | Maintenant sous Akamai       |

**Choisir un fournisseur :**

- DigitalOcean : expérience utilisateur la plus simple + configuration prévisible (ce guide)
- Hetzner : meilleur rapport qualité-prix (voir [guide Hetzner](/install/hetzner))
- Oracle Cloud : peut être gratuit, mais plus compliqué et ARM uniquement (voir [guide Oracle](/platforms/oracle))

---

## Prérequis

- Compte DigitalOcean ([inscrivez-vous pour $200 de crédit gratuit](https://m.do.co/c/signup))
- Paire de clés SSH (ou volonté d'utiliser l'authentification par mot de passe)
- Environ 20 minutes

## 1) Créer un Droplet

1. Connectez-vous à [DigitalOcean](https://cloud.digitalocean.com/)
2. Cliquez sur **Create → Droplets**
3. Sélectionnez :
   - **Region :** la région la plus proche de vous (ou de vos utilisateurs)
   - **Image :** Ubuntu 24.04 LTS
   - **Size :** Basic → Regular → **$6/mo** (1 vCPU, 1GB RAM, 25GB SSD)
   - **Authentication :** Clé SSH (recommandé) ou mot de passe
4. Cliquez sur **Create Droplet**
5. Notez l'adresse IP

## 2) Se connecter via SSH

```bash
ssh root@YOUR_DROPLET_IP
```

## 3) Installer OpenClaw

```bash
# Update system
apt update && apt upgrade -y

# Install Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs

# Install OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# Verify
openclaw --version
```

## 4) Exécuter l'assistant d'intégration

```bash
openclaw onboard --install-daemon
```

L'assistant vous guidera à travers :

- Authentification du modèle (clé API ou OAuth)
- Configuration des canaux (Telegram, WhatsApp, Discord, etc.)
- Jeton de passerelle (généré automatiquement)
- Installation du démon (systemd)

## 5) Vérifier la passerelle

```bash
# Check status
openclaw status

# Check service
systemctl --user status openclaw-gateway.service

# View logs
journalctl --user -u openclaw-gateway.service -f
```

## 6) Accéder au tableau de bord

La passerelle est liée par défaut à loopback. Pour accéder à l'interface de contrôle :

**Option A : Tunnel SSH (recommandé)**

```bash
# From your local machine
ssh -L 18789:localhost:18789 root@YOUR_DROPLET_IP

# Then open: http://localhost:18789
```

**Option B : Tailscale Serve (HTTPS, loopback uniquement)**

```bash
# On the droplet
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up

# Configure Gateway to use Tailscale Serve
openclaw config set gateway.tailscale.mode serve
openclaw gateway restart
```

Ouvrez : `https://<magicdns>/`

Remarques :

- Serve maintient la passerelle en loopback uniquement et s'authentifie via les en-têtes d'identité Tailscale.
- Pour exiger plutôt un jeton/mot de passe, définissez `gateway.auth.allowTailscale: false` ou utilisez `gateway.auth.mode: "password"`.

**Option C : Liaison Tailnet (sans Serve)**

```bash
openclaw config set gateway.bind tailnet
openclaw gateway restart
```

Ouvrez : `http://<tailscale-ip>:18789` (jeton requis).

## 7) Connecter vos canaux

### Telegram

```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

### WhatsApp

```bash
openclaw channels login whatsapp
# Scan QR code
```

Consultez [Canaux](/channels) pour les autres fournisseurs.

---

## Optimisations pour 1GB RAM

Le droplet à $6 n'a que 1GB RAM. Pour maintenir une exécution fluide :

### Ajouter du swap (recommandé)

```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### Utiliser des modèles plus légers

Si vous rencontrez des OOM, envisagez :

- Utiliser des modèles basés sur API (Claude, GPT) plutôt que des modèles locaux
- Définir `agents.defaults.model.primary` sur un modèle plus petit

### Surveiller la mémoire

```bash
free -h
htop
```

---

## Persistance

Tous les états sont stockés dans :

- `~/.openclaw/` — configuration, identifiants, données de session
- `~/.openclaw/workspace/` — espace de travail (SOUL.md, mémoires, etc.)

Ceux-ci sont conservés après redémarrage. Sauvegardez régulièrement :

```bash
tar -czvf openclaw-backup.tar.gz ~/.openclaw ~/.openclaw/workspace
```

---

## Alternative gratuite Oracle Cloud

Oracle Cloud offre des instances ARM **Always Free** qui sont beaucoup plus puissantes que n'importe quelle option payante ici — $0/mois.

| Ce que vous obtenez | Configuration        |
| ------------------- | -------------------- |
| **4 OCPUs**         | ARM Ampere A1        |
| **24GB RAM**        | Largement suffisant  |
| **200GB de stockage** | Volume de stockage en bloc |
| **Toujours gratuit** | Pas de frais de carte de crédit |

**Avertissements :**

- L'inscription peut être un peu délicate (réessayez si cela échoue)
- Architecture ARM — la plupart des choses fonctionnent, mais certains binaires nécessitent des builds ARM

Pour le guide de configuration complet, consultez [Oracle Cloud](/platforms/oracle). Pour les conseils d'inscription et le dépannage du processus d'inscription, consultez ce [guide communautaire](https://gist.github.com/rssnyder/51e3cfedd730e7dd5f4a816143b25dbd).

---

## Dépannage

### La passerelle ne démarre pas

```bash
openclaw gateway status
openclaw doctor --non-interactive
journalctl -u openclaw --no-pager -n 50
```

### Port déjà utilisé

```bash
lsof -i :18789
kill <PID>
```

### Mémoire insuffisante

```bash
# Check memory
free -h

# Add more swap
# Or upgrade to $12/mo droplet (2GB RAM)
```

---

## Voir aussi

- [Guide Hetzner](/install/hetzner) — moins cher et plus puissant
- [Installation Docker](/install/docker) — configuration conteneurisée
- [Tailscale](/gateway/tailscale) — accès à distance sécurisé
- [Configuration](/gateway/configuration) — référence de configuration complète
