---
summary: "OpenClaw sur Raspberry Pi (configuration auto-hébergée économique)"
read_when:
  - Configuration d'OpenClaw sur un Raspberry Pi
  - Exécution d'OpenClaw sur des appareils ARM
  - Construction d'une IA personnelle bon marché toujours active
title: "Raspberry Pi"
---

# OpenClaw sur Raspberry Pi

## Objectif

Exécuter une passerelle OpenClaw persistante et toujours active sur un Raspberry Pi pour un coût unique de **~35-80 $** (sans frais mensuels).

Parfait pour :

- Assistant IA personnel 24/7
- Hub domotique
- Bot Telegram/WhatsApp à faible consommation et toujours disponible

## Configuration matérielle requise

| Modèle Pi       | RAM     | Fonctionne ? | Notes                              |
| --------------- | ------- | ------------ | ---------------------------------- |
| **Pi 5**        | 4GB/8GB | ✅ Meilleur | Le plus rapide, recommandé         |
| **Pi 4**        | 4GB     | ✅ Bon      | Équilibre optimal pour la plupart  |
| **Pi 4**        | 2GB     | ✅ OK       | Fonctionne, ajouter du swap        |
| **Pi 4**        | 1GB     | ⚠️ Serré    | Possible avec swap, config minimale |
| **Pi 3B+**      | 1GB     | ⚠️ Lent     | Fonctionne mais lentement          |
| **Pi Zero 2 W** | 512MB   | ❌          | Non recommandé                     |

**Spécifications minimales :** 1 Go de RAM, 1 cœur, 500 Mo de disque  
**Recommandé :** 2 Go+ de RAM, OS 64 bits, carte SD 16 Go+ (ou SSD USB)

## Ce dont vous aurez besoin

- Raspberry Pi 4 ou 5 (2 Go+ recommandé)
- Carte microSD (16 Go+) ou SSD USB (meilleure performance)
- Alimentation (PSU Pi officiel recommandé)
- Connexion réseau (Ethernet ou WiFi)
- ~30 minutes

## 1) Flasher l'OS

Utilisez **Raspberry Pi OS Lite (64 bits)** — aucun bureau nécessaire pour un serveur sans écran.

1. Téléchargez [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Choisissez l'OS : **Raspberry Pi OS Lite (64-bit)**
3. Cliquez sur l'icône d'engrenage (⚙️) pour préconfigurer :
   - Définir le nom d'hôte : `gateway-host`
   - Activer SSH
   - Définir le nom d'utilisateur/mot de passe
   - Configurer le WiFi (si vous n'utilisez pas Ethernet)
4. Flasher sur votre carte SD / lecteur USB
5. Insérer et démarrer le Pi

## 2) Se connecter via SSH

```bash
ssh user@gateway-host
# ou utiliser l'adresse IP
ssh user@192.168.x.x
```

## 3) Configuration du système

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer les paquets essentiels
sudo apt install -y git curl build-essential

# Définir le fuseau horaire (important pour cron/rappels)
sudo timedatectl set-timezone America/Chicago  # Changer selon votre fuseau horaire
```

## 4) Installer Node.js 24 (ARM64)

```bash
# Installer Node.js via NodeSource
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt install -y nodejs

# Vérifier
node --version  # Devrait afficher v24.x.x
npm --version
```

## 5) Ajouter du Swap (Important pour 2 Go ou moins)

Le swap prévient les plantages dus à un manque de mémoire :

```bash
# Créer un fichier swap de 2 Go
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Rendre permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Optimiser pour faible RAM (réduire swappiness)
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## 6) Installer OpenClaw

### Option A : Installation standard (Recommandée)

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### Option B : Installation modifiable (Pour bricoler)

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
npm install
npm run build
npm link
```

L'installation modifiable vous donne un accès direct aux journaux et au code — utile pour déboguer les problèmes spécifiques à ARM.

## 7) Exécuter l'intégration

```bash
openclaw onboard --install-daemon
```

Suivez l'assistant :

1. **Mode passerelle :** Local
2. **Authentification :** Clés API recommandées (OAuth peut être capricieux sur Pi sans écran)
3. **Canaux :** Telegram est le plus facile pour commencer
4. **Daemon :** Oui (systemd)

## 8) Vérifier l'installation

```bash
# Vérifier le statut
openclaw status

# Vérifier le service
sudo systemctl status openclaw

# Afficher les journaux
journalctl -u openclaw -f
```

## 9) Accéder au tableau de bord OpenClaw

Remplacez `user@gateway-host` par le nom d'utilisateur et le nom d'hôte ou l'adresse IP de votre Pi.

Sur votre ordinateur, demandez au Pi d'imprimer une URL de tableau de bord fraîche :

```bash
ssh user@gateway-host 'openclaw dashboard --no-open'
```

La commande affiche `Dashboard URL:`. Selon la configuration de `gateway.auth.token`,
l'URL peut être un lien simple `http://127.0.0.1:18789/` ou un lien
qui inclut `#token=...`.

Dans un autre terminal sur votre ordinateur, créez le tunnel SSH :

```bash
ssh -N -L 18789:127.0.0.1:18789 user@gateway-host
```

Puis ouvrez l'URL du tableau de bord imprimée dans votre navigateur local.

Si l'interface demande une authentification, collez le jeton de `gateway.auth.token`
(ou `OPENCLAW_GATEWAY_TOKEN`) dans les paramètres de l'interface de contrôle.

Pour un accès distant toujours actif, voir [Tailscale](/gateway/tailscale).

---

## Optimisations de performance

### Utiliser un SSD USB (Amélioration énorme)

Les cartes SD sont lentes et s'usent. Un SSD USB améliore considérablement les performances :

```bash
# Vérifier si le démarrage se fait depuis USB
lsblk
```

Voir [guide de démarrage USB Pi](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#usb-mass-storage-boot) pour la configuration.

### Accélérer le démarrage CLI (cache de compilation de modules)

Sur les hôtes Pi moins puissants, activez le cache de compilation de modules de Node pour que les exécutions CLI répétées soient plus rapides :

```bash
grep -q 'NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache' ~/.bashrc || cat >> ~/.bashrc <<'EOF' # pragma: allowlist secret
export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
mkdir -p /var/tmp/openclaw-compile-cache
export OPENCLAW_NO_RESPAWN=1
EOF
source ~/.bashrc
```

Notes :

- `NODE_COMPILE_CACHE` accélère les exécutions suivantes (`status`, `health`, `--help`).
- `/var/tmp` survit mieux aux redémarrages que `/tmp`.
- `OPENCLAW_NO_RESPAWN=1` évite le coût de démarrage supplémentaire du respawn CLI.
- La première exécution réchauffe le cache ; les exécutions ultérieures en bénéficient le plus.

### Réglage du démarrage systemd (optionnel)

Si ce Pi exécute principalement OpenClaw, ajoutez un drop-in de service pour réduire
les variations de redémarrage et maintenir l'environnement de démarrage stable :

```bash
sudo systemctl edit openclaw
```

```ini
[Service]
Environment=OPENCLAW_NO_RESPAWN=1
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
Restart=always
RestartSec=2
TimeoutStartSec=90
```

Puis appliquez :

```bash
sudo systemctl daemon-reload
sudo systemctl restart openclaw
```

Si possible, conservez l'état/cache d'OpenClaw sur un stockage soutenu par SSD pour éviter
les goulots d'étranglement d'E/S aléatoires de carte SD lors des démarrages à froid.

Comment les politiques `Restart=` aident à la récupération automatisée :
[systemd peut automatiser la récupération de service](https://www.redhat.com/en/blog/systemd-automate-recovery).

### Réduire l'utilisation de la mémoire

```bash
# Désactiver l'allocation de mémoire GPU (sans écran)
echo 'gpu_mem=16' | sudo tee -a /boot/config.txt

# Désactiver Bluetooth si non utilisé
sudo systemctl disable bluetooth
```

### Surveiller les ressources

```bash
# Vérifier la mémoire
free -h

# Vérifier la température du CPU
vcgencmd measure_temp

# Surveillance en direct
htop
```

---

## Notes spécifiques à ARM

### Compatibilité binaire

La plupart des fonctionnalités d'OpenClaw fonctionnent sur ARM64, mais certains binaires externes peuvent nécessiter des builds ARM :

| Outil              | Statut ARM64 | Notes                               |
| ------------------ | ------------ | ----------------------------------- |
| Node.js            | ✅           | Fonctionne très bien                |
| WhatsApp (Baileys) | ✅           | JS pur, pas de problèmes            |
| Telegram           | ✅           | JS pur, pas de problèmes            |
| gog (Gmail CLI)    | ⚠️           | Vérifier la version ARM             |
| Chromium (browser) | ✅           | `sudo apt install chromium-browser` |

Si une compétence échoue, vérifiez si son binaire a une build ARM. Beaucoup d'outils Go/Rust l'ont ; certains non.

### 32 bits vs 64 bits

**Toujours utiliser l'OS 64 bits.** Node.js et de nombreux outils modernes l'exigent. Vérifiez avec :

```bash
uname -m
# Devrait afficher : aarch64 (64-bit) pas armv7l (32-bit)
```

---

## Configuration de modèle recommandée

Puisque le Pi n'est que la passerelle (les modèles s'exécutent dans le cloud), utilisez des modèles basés sur API :

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

**N'essayez pas d'exécuter des LLM locaux sur un Pi** — même les petits modèles sont trop lents. Laissez Claude/GPT faire le travail lourd.

---

## Démarrage automatique au démarrage

L'assistant d'intégration configure cela, mais pour vérifier :

```bash
# Vérifier que le service est activé
sudo systemctl is-enabled openclaw

# Activer si ce n'est pas le cas
sudo systemctl enable openclaw

# Démarrer au démarrage
sudo systemctl start openclaw
```

---

## Dépannage

### Manque de mémoire (OOM)

```bash
# Vérifier la mémoire
free -h

# Ajouter plus de swap (voir étape 5)
# Ou réduire les services exécutés sur le Pi
```

### Performance lente

- Utiliser un SSD USB au lieu d'une carte SD
- Désactiver les services inutilisés : `sudo systemctl disable cups bluetooth avahi-daemon`
- Vérifier la limitation du CPU : `vcgencmd get_throttled` (devrait retourner `0x0`)

### Le service ne démarre pas

```bash
# Vérifier les journaux
journalctl -u openclaw --no-pager -n 100

# Correctif courant : reconstruire
cd ~/openclaw  # si utilisant l'installation modifiable
npm run build
sudo systemctl restart openclaw
```

### Problèmes de binaires ARM

Si une compétence échoue avec "exec format error" :

1. Vérifier si le binaire a une build ARM64
2. Essayer de construire à partir de la source
3. Ou utiliser un conteneur Docker avec support ARM

### Les chutes WiFi

Pour les Pi sans écran sur WiFi :

```bash
# Désactiver la gestion de l'alimentation WiFi
sudo iwconfig wlan0 power off

# Rendre permanent
echo 'wireless-power off' | sudo tee -a /etc/network/interfaces
```

---

## Comparaison des coûts

| Configuration      | Coût unique | Coût mensuel | Notes                     |
| ------------------ | ----------- | ------------ | ------------------------- |
| **Pi 4 (2GB)**     | ~45 $       | 0 $          | + alimentation (~5 $/an)  |
| **Pi 4 (4GB)**     | ~55 $       | 0 $          | Recommandé                |
| **Pi 5 (4GB)**     | ~60 $       | 0 $          | Meilleure performance     |
| **Pi 5 (8GB)**     | ~80 $       | 0 $          | Excessif mais futur-proof |
| DigitalOcean       | 0 $         | 6 $/mois     | 72 $/an                   |
| Hetzner            | 0 $         | 3,79 €/mois  | ~50 $/an                  |

**Seuil de rentabilité :** Un Pi se rembourse en ~6-12 mois par rapport à un VPS cloud.

---

## Voir aussi

- [Guide Linux](/platforms/linux) — configuration Linux générale
- [Guide DigitalOcean](/platforms/digitalocean) — alternative cloud
- [Guide Hetzner](/install/hetzner) — configuration
