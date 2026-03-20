---
summary: "Héberger OpenClaw sur un Droplet DigitalOcean"
read_when:
  - Setting up OpenClaw on DigitalOcean
  - Looking for a simple paid VPS for OpenClaw
title: "DigitalOcean"
---

# DigitalOcean

Exécutez une passerelle OpenClaw persistante sur un Droplet DigitalOcean.

## Prérequis

- Compte DigitalOcean ([inscription](https://cloud.digitalocean.com/registrations/new))
- Paire de clés SSH (ou volonté d'utiliser l'authentification par mot de passe)
- Environ 20 minutes

## Configuration

<Steps>
  <Step title="Créer un Droplet">
    <Warning>
    Utilisez une image de base propre (Ubuntu 24.04 LTS). Évitez les images Marketplace tiers en un clic à moins d'avoir examiné leurs scripts de démarrage et paramètres de pare-feu par défaut.
    </Warning>

    1. Connectez-vous à [DigitalOcean](https://cloud.digitalocean.com/).
    2. Cliquez sur **Create > Droplets**.
    3. Choisissez :
       - **Region:** La plus proche de vous
       - **Image:** Ubuntu 24.04 LTS
       - **Size:** Basic, Regular, 1 vCPU / 1 GB RAM / 25 GB SSD
       - **Authentication:** Clé SSH (recommandé) ou mot de passe
    4. Cliquez sur **Create Droplet** et notez l'adresse IP.

  </Step>

  <Step title="Connecter et installer">
    ```bash
    ssh root@YOUR_DROPLET_IP

    apt update && apt upgrade -y

    # Install Node.js 24
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash -
    apt install -y nodejs

    # Install OpenClaw
    curl -fsSL https://openclaw.ai/install.sh | bash
    openclaw --version
    ```

  </Step>

  <Step title="Exécuter l'intégration">
    ```bash
    openclaw onboard --install-daemon
    ```

    L'assistant vous guide à travers l'authentification du modèle, la configuration des canaux, la génération du jeton de passerelle et l'installation du daemon (systemd).

  </Step>

  <Step title="Ajouter du swap (recommandé pour les Droplets 1 GB)">
    ```bash
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    ```
  </Step>

  <Step title="Vérifier la passerelle">
    ```bash
    openclaw status
    systemctl --user status openclaw-gateway.service
    journalctl --user -u openclaw-gateway.service -f
    ```
  </Step>

  <Step title="Accéder à l'interface de contrôle">
    La passerelle se lie à la boucle locale par défaut. Choisissez l'une de ces options.

    **Option A: Tunnel SSH (la plus simple)**

    ```bash
    # Depuis votre machine locale
    ssh -L 18789:localhost:18789 root@YOUR_DROPLET_IP
    ```

    Ouvrez ensuite `http://localhost:18789`.

    **Option B: Tailscale Serve**

    ```bash
    curl -fsSL https://tailscale.com/install.sh | sh
    tailscale up
    openclaw config set gateway.tailscale.mode serve
    openclaw gateway restart
    ```

    Ouvrez ensuite `https://<magicdns>/` depuis n'importe quel appareil de votre tailnet.

    **Option C: Liaison tailnet (sans Serve)**

    ```bash
    openclaw config set gateway.bind tailnet
    openclaw gateway restart
    ```

    Ouvrez ensuite `http://<tailscale-ip>:18789` (jeton requis).

  </Step>
</Steps>

## Dépannage

**La passerelle ne démarre pas** -- Exécutez `openclaw doctor --non-interactive` et vérifiez les journaux avec `journalctl --user -u openclaw-gateway.service -n 50`.

**Port déjà utilisé** -- Exécutez `lsof -i :18789` pour trouver le processus, puis arrêtez-le.

**Mémoire insuffisante** -- Vérifiez que le swap est actif avec `free -h`. Si vous continuez à rencontrer des problèmes OOM, utilisez des modèles basés sur l'API (Claude, GPT) plutôt que des modèles locaux, ou passez à un Droplet 2 GB.

## Étapes suivantes

- [Channels](/fr/channels) -- connectez Telegram, WhatsApp, Discord, et plus
- [Configuration de la passerelle](/fr/gateway/configuration) -- toutes les options de configuration
- [Mise à jour](/fr/install/updating) -- gardez OpenClaw à jour
