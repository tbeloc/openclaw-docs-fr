---
read_when:
  - Lors de la configuration d'OpenClaw sur Raspberry Pi
  - Lors de l'exécution d'OpenClaw sur un appareil ARM
  - Lors de la construction d'une IA personnelle résidente à faible coût
summary: Exécuter OpenClaw sur Raspberry Pi (configuration auto-hébergée à faible coût)
title: Raspberry Pi
x-i18n:
  generated_at: "2026-02-03T07:53:30Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 6741eaf0115a4fa0efd6599a99e0526a20ceb30eda1d9b04cba9dd5dec84bee2
  source_path: platforms/raspberry-pi.md
  workflow: 15
---

# Exécuter OpenClaw sur Raspberry Pi

## Objectif

Exécuter une passerelle OpenClaw persistante et résidente sur un Raspberry Pi, **avec un coût unique d'environ 35-80 $** (sans frais mensuels).

Idéal pour :

- Assistant IA personnel 24/7
- Centre domotique
- Robot Telegram/WhatsApp à faible consommation d'énergie et toujours disponible

## Configuration matérielle requise

| Modèle Pi       | Mémoire | Disponible ? | Notes                          |
| --------------- | ------- | ------------ | ------------------------------ |
| **Pi 5**        | 4GB/8GB | ✅ Optimal   | Le plus rapide, recommandé     |
| **Pi 4**        | 4GB     | ✅ Bon       | Meilleur choix pour la plupart |
| **Pi 4**        | 2GB     | ✅ Possible  | Fonctionne, ajoutez du swap    |
| **Pi 4**        | 1GB     | ⚠️ Serré     | Faisable avec swap, minimal    |
| **Pi 3B+**      | 1GB     | ⚠️ Lent      | Fonctionne mais plus lent      |
| **Pi Zero 2 W** | 512MB   | ❌           | Non recommandé                 |

**Configuration minimale :** 1 GB de RAM, 1 cœur, 500 MB de disque  
**Recommandé :** 2 GB+ de RAM, système 64 bits, carte SD 16 GB+ (ou SSD USB)

## Ce dont vous avez besoin

- Raspberry Pi 4 ou 5 (recommandé 2 GB+)
- Carte microSD (16 GB+) ou SSD USB (meilleure performance)
- Alimentation (alimentation officielle Pi recommandée)
- Connexion réseau (Ethernet ou WiFi)
- Environ 30 minutes

## 1) Flasher le système

Utilisez **Raspberry Pi OS Lite (64-bit)** — pas besoin de bureau pour un serveur sans tête.

1. Téléchargez [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Sélectionnez le système : **Raspberry Pi OS Lite (64-bit)**
3. Cliquez sur l'icône d'engrenage (⚙️) pour préconfigurer :
   - Définissez le nom d'hôte : `gateway-host`
   - Activez SSH
   - Définissez le nom d'utilisateur/mot de passe
   - Configurez le WiFi (si vous n'utilisez pas Ethernet)
4. Flashez sur votre carte SD / lecteur USB
5. Insérez et démarrez le Pi

## 2) Connexion via SSH

```bash
ssh user@gateway-host
# ou utiliser l'adresse IP
ssh user@192.168.x.x
```

## 3) Configuration du système

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer les paquets nécessaires
sudo apt install -y git curl build-essential

# Définir le fuseau horaire (important pour cron/rappels)
sudo timedatectl set-timezone America/Chicago  # Changez selon votre fuseau
```

## 4) Installer Node.js 22 (ARM64)

```bash
# Installer Node.js via NodeSource
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# Vérifier
node --version  # Devrait afficher v22.x.x
npm --version
```

## 5) Ajouter de l'espace d'échange (important pour 2 GB de RAM ou moins)

L'espace d'échange prévient les plantages dus à la mémoire insuffisante :

```bash
# Créer un fichier d'échange de 2 GB
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Rendre permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Optimiser pour faible mémoire (réduire swappiness)
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## 6) Installer OpenClaw

### Option A : Installation standard (recommandée)

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### Option B : Installation modifiable (pour le débogage)

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
npm install
npm run build
npm link
```

L'installation modifiable vous permet d'accéder directement aux journaux et au code — utile pour déboguer les problèmes spécifiques à ARM.

## 7) Exécuter l'assistant d'intégration

```bash
openclaw onboard --install-daemon
```

Suivez l'assistant :

1. **Mode passerelle :** Local
2. **Authentification :** Clé API recommandée (OAuth peut être instable sur Pi sans tête)
3. **Canaux :** Telegram est le plus facile pour commencer
4. **Démon :** Oui (systemd)

## 8) Vérifier l'installation

```bash
# Vérifier le statut
openclaw status

# Vérifier le service
sudo systemctl status openclaw

# Afficher les journaux
journalctl -u openclaw -f
```

## 9) Accéder au tableau de bord

Puisque le Pi est sans tête, utilisez un tunnel SSH :

```bash
# Depuis votre ordinateur portable/bureau
ssh -L 18789:localhost:18789 user@gateway-host

# Puis ouvrez dans le navigateur
open http://localhost:18789
```

Ou utilisez Tailscale pour un accès résidant :

```bash
# Sur le Pi
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Mettre à jour la configuration
openclaw config set gateway.bind tailnet
sudo systemctl restart openclaw
```

---

## Optimisation des performances

### Utiliser un SSD USB (amélioration énorme)

Les cartes SD sont lentes et s'usent. Un SSD USB améliore considérablement les performances :

```bash
# Vérifier si vous démarrez depuis USB
lsblk
```

Consultez le [guide de démarrage USB Pi](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#usb-mass-storage-boot).

### Réduire l'utilisation de la mémoire

```bash
# Désactiver l'allocation de mémoire GPU (mode sans tête)
echo 'gpu_mem=16' | sudo tee -a /boot/config.txt

# Désactiver le Bluetooth si non utilisé
sudo systemctl disable bluetooth
```

### Surveiller les ressources

```bash
# Vérifier la mémoire
free -h

# Vérifier la température du CPU
vcgencmd measure_temp

# Surveillance en temps réel
htop
```

---

## Notes spécifiques à ARM

### Compatibilité binaire

La plupart des fonctionnalités d'OpenClaw fonctionnent sur ARM64, mais certains binaires externes peuvent nécessiter des constructions ARM :

| Outil              | Statut ARM64 | Notes                                  |
| ------------------ | ------------ | -------------------------------------- |
| Node.js            | ✅           | Fonctionne bien                        |
| WhatsApp (Baileys) | ✅           | Pur JS, pas de problème                |
| Telegram           | ✅           | Pur JS, pas de problème                |
| gog (Gmail CLI)    | ⚠️           | Vérifier la disponibilité de version ARM |
| Chromium (browser) | ✅           | `sudo apt install chromium-browser`   |

Si une compétence échoue, vérifiez si son binaire a une construction ARM. Beaucoup d'outils Go/Rust en ont ; certains non.

### 32 bits vs 64 bits

**Utilisez toujours un système 64 bits.** Node.js et de nombreux outils modernes le nécessitent. Vérifiez avec :

```bash
uname -m
# Devrait afficher : aarch64 (64 bits) et non armv7l (32 bits)
```

---

## Configuration de modèle recommandée

Puisque le Pi n'est qu'une passerelle (les modèles s'exécutent dans le cloud), utilisez des modèles basés sur API :

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-20250514",
        "fallbacks": ["openai/gpt-4o-mini"]
      }
    }
  }
}
```

**N'essayez pas d'exécuter un LLM local sur le Pi** — même les petits modèles sont trop lents. Laissez Claude/GPT faire le travail lourd.

---

## Démarrage automatique

L'assistant d'intégration configure cela, mais vérifiez :

```bash
# Vérifier si le service est activé
sudo systemctl is-enabled openclaw

# Sinon, l'activer
sudo systemctl enable openclaw

# Démarrer au démarrage
sudo systemctl start openclaw
```

---

## Dépannage

### Mémoire insuffisante (OOM)

```bash
# Vérifier la mémoire
free -h

# Ajouter plus d'espace d'échange (voir étape 5)
# Ou réduire les services exécutés sur le Pi
```

### Performance lente

- Utilisez un SSD USB au lieu d'une carte SD
- Désactivez les services inutilisés : `sudo systemctl disable cups bluetooth avahi-daemon`
- Vérifiez la réduction de fréquence du CPU : `vcgencmd get_throttled` (devrait retourner `0x0`)

### Le service ne démarre pas

```bash
# Vérifier les journaux
journalctl -u openclaw --no-pager -n 100

# Correction courante : reconstruire
cd ~/openclaw  # Si vous utilisez l'installation modifiable
npm run build
sudo systemctl restart openclaw
```

### Problèmes binaires ARM

Si une compétence échoue avec "exec format error" :

1. Vérifiez si ce binaire a une construction ARM64
2. Essayez de construire à partir de la source
3. Ou utilisez un conteneur Docker compatible ARM

### Déconnexion WiFi

Pour un Pi sans tête utilisant le WiFi :

```bash
# Désactiver la gestion de l'énergie WiFi
sudo iwconfig wlan0 power off

# Rendre permanent
echo 'wireless-power off' | sudo tee -a /etc/network/interfaces
```

---

## Comparaison des coûts

| Configuration      | Coût unique | Frais mensuels | Notes              |
| ------------------ | ----------- | -------------- | ------------------ |
| **Pi 4 (2GB)**     | ~45 $       | 0 $            | + électricité (~5 $/an) |
| **Pi 4 (4GB)**     | ~55 $       | 0 $            | Recommandé         |
| **Pi 5 (4GB)**     | ~60 $       | 0 $            | Meilleures performances |
| **Pi 5 (8GB)**     | ~80 $       | 0 $            | Excessif mais à l'épreuve du temps |
| DigitalOcean       | 0 $         | 6 $/mois       | 72 $/an            |
| Hetzner            | 0 $         | 3,79 €/mois    | ~50 $/an           |

**Retour sur investissement :** Le Pi se rentabilise en environ 6-12 mois par rapport à un VPS cloud.

---

## Voir aussi

- [Guide Linux](/platforms/linux) — Configuration Linux générique
- [Guide DigitalOcean](/platforms/digitalocean) — Alternative cloud
- [Guide Hetzner](/install/hetzner) — Configuration Docker
- [Tailscale](/gateway/tailscale) — Accès à distance
- [Nœuds](/nodes) — Appairez votre ordinateur portable/téléphone avec la passerelle Pi
