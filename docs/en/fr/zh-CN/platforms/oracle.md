---
read_when:
  - 在 Oracle Cloud 上设置 OpenClaw
  - 寻找 OpenClaw 的低成本 VPS 托管
  - 想要在小型服务器上 24/7 运行 OpenClaw
summary: 在 Oracle Cloud 上运行 OpenClaw（Always Free ARM）
title: Oracle Cloud
x-i18n:
  generated_at: "2026-02-03T07:53:25Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: d3cc337b40ea512b5756ac15ec4341fecad417ede75f717fea3035678c7c6697
  source_path: platforms/oracle.md
  workflow: 15
---

# Exécuter OpenClaw sur Oracle Cloud (OCI)

## Objectif

Exécuter une passerelle OpenClaw persistante sur le niveau **Always Free** ARM d'Oracle Cloud.

Le niveau gratuit d'Oracle est excellent pour OpenClaw (surtout si vous avez déjà un compte OCI), mais il y a quelques compromis :

- Architecture ARM (la plupart des choses fonctionnent, mais certains binaires peuvent être x86 uniquement)
- La capacité et l'inscription peuvent être un peu délicates

## Comparaison des coûts (2026)

| Fournisseur  | Plan            | Configuration             | Prix/mois | Remarques                |
| ------------ | --------------- | ------------------------- | --------- | ------------------------ |
| Oracle Cloud | Always Free ARM | Jusqu'à 4 OCPU, 24 GB RAM | $0        | ARM, capacité limitée    |
| Hetzner      | CX22            | 2 vCPU, 4 GB RAM          | ~ $4      | Option payante la moins chère |
| DigitalOcean | Basic           | 1 vCPU, 1 GB RAM          | $6        | Interface conviviale, documentation complète |
| Vultr        | Cloud Compute   | 1 vCPU, 1 GB RAM          | $6        | Plusieurs régions        |
| Linode       | Nanode          | 1 vCPU, 1 GB RAM          | $5        | Maintenant partie d'Akamai |

---

## Prérequis

- Compte Oracle Cloud ([s'inscrire](https://www.oracle.com/cloud/free/)) — consultez le [guide d'inscription communautaire](https://gist.github.com/rssnyder/51e3cfedd730e7dd5f4a816143b25dbd) si vous rencontrez des problèmes
- Compte Tailscale (gratuit sur [tailscale.com](https://tailscale.com))
- Environ 30 minutes

## 1) Créer une instance OCI

1. Connectez-vous à la [console Oracle Cloud](https://cloud.oracle.com/)
2. Accédez à **Compute → Instances → Create Instance**
3. Configurez :
   - **Name:** `openclaw`
   - **Image:** Ubuntu 24.04 (aarch64)
   - **Shape:** `VM.Standard.A1.Flex` (Ampere ARM)
   - **OCPUs:** 2 (ou jusqu'à 4)
   - **Memory:** 12 GB (ou jusqu'à 24 GB)
   - **Boot volume:** 50 GB (jusqu'à 200 GB gratuit)
   - **SSH key:** Ajoutez votre clé publique
4. Cliquez sur **Create**
5. Notez l'adresse IP publique

**Conseil :** Si la création d'instance échoue avec "Out of capacity", essayez un domaine de disponibilité différent ou réessayez plus tard. La capacité du niveau gratuit est limitée.

## 2) Se connecter et mettre à jour

```bash
# Se connecter via l'IP publique
ssh ubuntu@YOUR_PUBLIC_IP

# Mettre à jour le système
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential
```

**Remarque :** `build-essential` est nécessaire pour la compilation ARM de certaines dépendances.

## 3) Configurer l'utilisateur et le nom d'hôte

```bash
# Définir le nom d'hôte
sudo hostnamectl set-hostname openclaw

# Définir un mot de passe pour l'utilisateur ubuntu
sudo passwd ubuntu

# Activer lingering (maintenir les services utilisateur après la déconnexion)
sudo loginctl enable-linger ubuntu
```

## 4) Installer Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --ssh --hostname=openclaw
```

Cela active Tailscale SSH, vous pouvez donc vous connecter à partir de n'importe quel appareil sur votre tailnet via `ssh openclaw` — pas besoin d'IP publique.

Vérifiez :

```bash
tailscale status
```

**À partir de maintenant, connectez-vous via Tailscale :** `ssh ubuntu@openclaw` (ou utilisez l'IP Tailscale).

## 5) Installer OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
source ~/.bashrc
```

Quand on vous demande "How do you want to hatch your bot?", sélectionnez **"Do this later"**.

> Remarque : Si vous rencontrez des problèmes de construction native ARM, commencez par les paquets système avant d'utiliser Homebrew (par exemple `sudo apt install -y build-essential`).

## 6) Configurer la passerelle (loopback + authentification par jeton) et activer Tailscale Serve

Utilisez l'authentification par jeton comme valeur par défaut. C'est prévisible et évite d'avoir besoin de drapeaux d'interface de contrôle "authentification non sécurisée".

```bash
# Garder la passerelle privée sur la VM
openclaw config set gateway.bind loopback

# Exiger l'authentification pour la passerelle + l'interface de contrôle
openclaw config set gateway.auth.mode token
openclaw doctor --generate-gateway-token

# Exposer via Tailscale Serve (HTTPS + accès tailnet)
openclaw config set gateway.tailscale.mode serve
openclaw config set gateway.trustedProxies '["127.0.0.1"]'

systemctl --user restart openclaw-gateway
```

## 7) Vérifier

```bash
# Vérifier la version
openclaw --version

# Vérifier l'état du démon
systemctl --user status openclaw-gateway

# Vérifier Tailscale Serve
tailscale serve status

# Tester la réponse locale
curl http://localhost:18789
```

## 8) Verrouiller la sécurité du VCN

Maintenant que tout fonctionne, verrouillez le VCN pour bloquer tout le trafic sauf Tailscale. Le réseau cloud virtuel d'OCI agit comme un pare-feu à la limite du réseau — le trafic est bloqué avant d'atteindre votre instance.

1. Dans la console OCI, accédez à **Networking → Virtual Cloud Networks**
2. Cliquez sur votre VCN → **Security Lists** → Default Security List
3. **Supprimez** toutes les règles d'entrée sauf :
   - `0.0.0.0/0 UDP 41641` (Tailscale)
4. Conservez les règles de sortie par défaut (autoriser tout le trafic sortant)

Cela bloque SSH sur le port 22, HTTP, HTTPS et tout le reste à la limite du réseau. À partir de maintenant, vous ne pouvez vous connecter que via Tailscale.

---

## Accéder à l'interface de contrôle

À partir de n'importe quel appareil sur votre réseau Tailscale :

```
https://openclaw.<tailnet-name>.ts.net/
```

Remplacez `<tailnet-name>` par le nom de votre tailnet (visible dans `tailscale status`).

Aucun tunnel SSH nécessaire. Tailscale fournit :

- Chiffrement HTTPS (certificats automatiques)
- Authentification via Tailscale
- Accès à partir de n'importe quel appareil sur votre tailnet (ordinateur portable, téléphone, etc.)

---

## Sécurité : VCN + Tailscale (ligne de base recommandée)

En verrouillant le VCN (ouverture uniquement d'UDP 41641) et en liant la passerelle à loopback, vous obtenez une défense en profondeur solide : le trafic public est bloqué à la limite du réseau, l'accès administratif se fait via votre tailnet.

Cette configuration élimine généralement le *besoin* de règles de pare-feu supplémentaires basées sur l'hôte purement pour bloquer les attaques par force brute SSH à l'échelle d'Internet — mais vous devriez toujours maintenir le système d'exploitation à jour, exécuter `openclaw security audit`, et vérifier que vous n'écoutez pas accidentellement sur des interfaces publiques.

### Ce qui est déjà protégé

| Étape traditionnelle | Nécessaire ? | Raison                                           |
| -------------------- | ------------ | ------------------------------------------------ |
| Pare-feu UFW         | Non          | Le VCN bloque avant que le trafic n'atteigne l'instance |
| fail2ban             | Non          | Pas d'attaque par force brute si le port 22 est bloqué au VCN |
| Durcissement sshd    | Non          | Tailscale SSH n'utilise pas sshd                 |
| Désactiver la connexion root | Non | Tailscale utilise l'identité Tailscale, pas les utilisateurs système |
| Authentification par clé SSH uniquement | Non | Tailscale s'authentifie via votre tailnet |
| Durcissement IPv6    | Généralement non | Dépend de votre configuration VCN/sous-réseau ; vérifiez ce qui est réellement alloué/exposé |

### Toujours recommandé

- **Permissions des identifiants :** `chmod 700 ~/.openclaw`
- **Audit de sécurité :** `openclaw security audit`
- **Mises à jour système :** `sudo apt update && sudo apt upgrade` régulièrement
- **Surveiller Tailscale :** Consultez la [console d'administration Tailscale](https://login.tailscale.com/admin) pour les appareils

### Vérifier la posture de sécurité

```bash
# Confirmer qu'aucun port public n'écoute
sudo ss -tlnp | grep -v '127.0.0.1\|::1'

# Vérifier que Tailscale SSH est actif
tailscale status | grep -q 'offers: ssh' && echo "Tailscale SSH active"

# Optionnel : désactiver complètement sshd
sudo systemctl disable --now ssh
```

---

## Alternative : Tunnel SSH

Si Tailscale Serve ne fonctionne pas, utilisez un tunnel SSH :

```bash
# À partir de votre machine locale (via Tailscale)
ssh -L 18789:127.0.0.1:18789 ubuntu@openclaw
```

Puis ouvrez `http://localhost:18789`.

---

## Dépannage

### Échec de la création d'instance ("Out of capacity")

Les instances ARM du niveau gratuit sont populaires. Essayez :

- Un domaine de disponibilité différent
- Réessayer en dehors des heures de pointe (tôt le matin)
- Utiliser le filtre "Always Free" lors de la sélection de la forme

### Tailscale ne peut pas se connecter

```bash
# Vérifier l'état
sudo tailscale status

# Se réauthentifier
sudo tailscale up --ssh --hostname=openclaw --reset
```

### La passerelle ne démarre pas

```bash
openclaw gateway status
openclaw doctor --non-interactive
journalctl --user -u openclaw-gateway -n 50
```

### Impossible d'accéder à l'interface de contrôle

```bash
# Vérifier que Tailscale Serve s'exécute
tailscale serve status

# Vérifier que la passerelle écoute
curl http://localhost:18789

# Redémarrer si nécessaire
systemctl --user restart openclaw-gateway
```

### Problèmes de binaires ARM

Certains outils peuvent ne pas avoir de construction ARM. Vérifiez :

```bash
uname -m  # Devrait afficher aarch64
```

La plupart des paquets npm fonctionnent correctement. Pour les binaires, recherchez les versions `linux-arm64` ou `aarch64`.

---

## Persistance

Tous les états sont stockés dans :

- `~/.openclaw/` — configuration, identifiants, données de session
- `~/.openclaw/workspace/` — espace de travail (SOUL.md, mémoire, artefacts)

Sauvegardez régulièrement :

```bash
tar -czvf openclaw-backup.tar.gz ~/.openclaw ~/.openclaw/workspace
```

---

## Voir aussi

- [Accès distant à la passerelle](/gateway/remote) — autres modes d'accès distant
- [Intégration Tailscale](/gateway/tailscale) — documentation Tailscale complète
- [Configuration de la passerelle](/gateway/configuration) — toutes les options de configuration
- [Guide DigitalOcean](/platforms/digitalocean) — si vous préférez payant + inscription plus facile
- [Guide Hetzner](/install/hetzner) — alternative basée sur Docker
