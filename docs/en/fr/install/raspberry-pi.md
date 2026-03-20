---
summary: "Hébergez OpenClaw sur un Raspberry Pi pour un auto-hébergement toujours actif"
read_when:
  - Setting up OpenClaw on a Raspberry Pi
  - Running OpenClaw on ARM devices
  - Building a cheap always-on personal AI
title: "Raspberry Pi"
---

# Raspberry Pi

Exécutez une passerelle OpenClaw persistante et toujours active sur un Raspberry Pi. Puisque le Pi n'est que la passerelle (les modèles s'exécutent dans le cloud via API), même un Pi modeste gère bien la charge de travail.

## Prérequis

- Raspberry Pi 4 ou 5 avec 2 GB+ de RAM (4 GB recommandé)
- Carte MicroSD (16 GB+) ou SSD USB (meilleures performances)
- Alimentation officielle Pi
- Connexion réseau (Ethernet ou WiFi)
- Raspberry Pi OS 64 bits (obligatoire -- ne pas utiliser 32 bits)
- Environ 30 minutes

## Configuration

<Steps>
  <Step title="Flasher le système d'exploitation">
    Utilisez **Raspberry Pi OS Lite (64-bit)** -- aucun bureau n'est nécessaire pour un serveur sans écran.

    1. Téléchargez [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
    2. Choisissez le système d'exploitation : **Raspberry Pi OS Lite (64-bit)**.
    3. Dans la boîte de dialogue des paramètres, préconfigurer :
       - Nom d'hôte : `gateway-host`
       - Activer SSH
       - Définir le nom d'utilisateur et le mot de passe
       - Configurer le WiFi (si vous n'utilisez pas Ethernet)
    4. Flashez sur votre carte SD ou lecteur USB, insérez-la et démarrez le Pi.

  </Step>

  <Step title="Se connecter via SSH">
    ```bash
    ssh user@gateway-host
    ```
  </Step>

  <Step title="Mettre à jour le système">
    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y git curl build-essential

    # Définir le fuseau horaire (important pour cron et les rappels)
    sudo timedatectl set-timezone America/Chicago
    ```

  </Step>

  <Step title="Installer Node.js 24">
    ```bash
    curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
    sudo apt install -y nodejs
    node --version
    ```
  </Step>

  <Step title="Ajouter de la mémoire virtuelle (important pour 2 GB ou moins)">
    ```bash
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

    # Réduire la swappiness pour les appareils à faible RAM
    echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
    sudo sysctl -p
    ```

  </Step>

  <Step title="Installer OpenClaw">
    ```bash
    curl -fsSL https://openclaw.ai/install.sh | bash
    ```
  </Step>

  <Step title="Exécuter l'intégration">
    ```bash
    openclaw onboard --install-daemon
    ```

    Suivez l'assistant. Les clés API sont recommandées plutôt que OAuth pour les appareils sans écran. Telegram est le canal le plus facile pour commencer.

  </Step>

  <Step title="Vérifier">
    ```bash
    openclaw status
    sudo systemctl status openclaw
    journalctl -u openclaw -f
    ```
  </Step>

  <Step title="Accéder à l'interface de contrôle">
    Sur votre ordinateur, obtenez une URL de tableau de bord à partir du Pi :

    ```bash
    ssh user@gateway-host 'openclaw dashboard --no-open'
    ```

    Ensuite, créez un tunnel SSH dans un autre terminal :

    ```bash
    ssh -N -L 18789:127.0.0.1:18789 user@gateway-host
    ```

    Ouvrez l'URL imprimée dans votre navigateur local. Pour un accès à distance toujours actif, consultez [l'intégration Tailscale](/fr/gateway/tailscale).

  </Step>
</Steps>

## Conseils de performance

**Utilisez un SSD USB** -- Les cartes SD sont lentes et s'usent. Un SSD USB améliore considérablement les performances. Consultez le [guide de démarrage USB du Pi](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#usb-mass-storage-boot).

**Activer le cache de compilation des modules** -- Accélère les invocations CLI répétées sur les hôtes Pi moins puissants :

```bash
grep -q 'NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache' ~/.bashrc || cat >> ~/.bashrc <<'EOF' # pragma: allowlist secret
export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
mkdir -p /var/tmp/openclaw-compile-cache
export OPENCLAW_NO_RESPAWN=1
EOF
source ~/.bashrc
```

**Réduire l'utilisation de la mémoire** -- Pour les configurations sans écran, libérez la mémoire GPU et désactivez les services inutilisés :

```bash
echo 'gpu_mem=16' | sudo tee -a /boot/config.txt
sudo systemctl disable bluetooth
```

## Dépannage

**Mémoire insuffisante** -- Vérifiez que la mémoire virtuelle est active avec `free -h`. Désactivez les services inutilisés (`sudo systemctl disable cups bluetooth avahi-daemon`). Utilisez uniquement les modèles basés sur les API.

**Performances lentes** -- Utilisez un SSD USB au lieu d'une carte SD. Vérifiez l'accélération du CPU avec `vcgencmd get_throttled` (devrait retourner `0x0`).

**Le service ne démarre pas** -- Vérifiez les journaux avec `journalctl -u openclaw --no-pager -n 100` et exécutez `openclaw doctor --non-interactive`.

**Problèmes de binaires ARM** -- Si une compétence échoue avec "exec format error", vérifiez si le binaire a une version ARM64. Vérifiez l'architecture avec `uname -m` (devrait afficher `aarch64`).

**WiFi se déconnecte** -- Désactivez la gestion de l'alimentation WiFi : `sudo iwconfig wlan0 power off`.

## Étapes suivantes

- [Canaux](/fr/channels) -- connectez Telegram, WhatsApp, Discord, et plus
- [Configuration de la passerelle](/fr/gateway/configuration) -- toutes les options de configuration
- [Mise à jour](/fr/install/updating) -- gardez OpenClaw à jour
