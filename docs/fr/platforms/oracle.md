---
summary: "OpenClaw sur Oracle Cloud (Always Free ARM)"
read_when:
  - Configuration d'OpenClaw sur Oracle Cloud
  - Recherche d'un hébergement VPS à faible coût pour OpenClaw
  - Vous voulez OpenClaw 24/7 sur un petit serveur
title: "Oracle Cloud"
---

# OpenClaw sur Oracle Cloud (OCI)

## Objectif

Exécuter une passerelle OpenClaw persistante sur le niveau ARM **Always Free** d'Oracle Cloud.

Le niveau gratuit d'Oracle peut être un excellent choix pour OpenClaw (surtout si vous avez déjà un compte OCI), mais il comporte des compromis :

- Architecture ARM (la plupart des choses fonctionnent, mais certains binaires peuvent être x86 uniquement)
- La capacité et l'inscription peuvent être capricieuses

## Comparaison des coûts (2026)

| Fournisseur  | Plan            | Spécifications         | Prix/mois | Remarques                |
| ------------ | --------------- | ---------------------- | --------- | ------------------------ |
| Oracle Cloud | Always Free ARM | jusqu'à 4 OCPU, 24GB RAM | $0        | ARM, capacité limitée    |
| Hetzner      | CX22            | 2 vCPU, 4GB RAM        | ~ $4      | Option payante la moins chère |
| DigitalOcean | Basic           | 1 vCPU, 1GB RAM        | $6        | Interface facile, bonne documentation |
| Vultr        | Cloud Compute   | 1 vCPU, 1GB RAM        | $6        | Nombreux emplacements    |
| Linode       | Nanode          | 1 vCPU, 1GB RAM        | $5        | Maintenant partie d'Akamai |

---

## Prérequis

- Compte Oracle Cloud ([inscription](https://www.oracle.com/cloud/free/)) — voir [guide d'inscription communautaire](https://gist.github.com/rssnyder/51e3cfedd730e7dd5f4a816143b25dbd) si vous rencontrez des problèmes
- Compte Tailscale (gratuit sur [tailscale.com](https://tailscale.com))
- ~30 minutes

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

## 2) Connexion et mise à jour

```bash
# Connectez-vous via l'IP publique
ssh ubuntu@YOUR_PUBLIC_IP

# Mettez à jour le système
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential
```

**Remarque :** `build-essential` est requis pour la compilation ARM de certaines dépendances.

## 3) Configurer l'utilisateur et le nom d'hôte

```bash
# Définir le nom d'hôte
sudo hostnamectl set-hostname openclaw

# Définir le mot de passe pour l'utilisateur ubuntu
sudo passwd ubuntu

# Activer lingering (garde les services utilisateur actifs après la déconnexion)
sudo loginctl enable-linger ubuntu
```

## 4) Installer Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --ssh --hostname=openclaw
```

Cela active Tailscale SSH, vous permettant de vous connecter via `ssh openclaw` depuis n'importe quel appareil sur votre tailnet — pas besoin d'IP publique.

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

Lorsqu'on vous demande "How do you want to hatch your bot?", sélectionnez **"Do this later"**.

> Remarque : Si vous rencontrez des problèmes de compilation natifs ARM, commencez par les paquets système (par exemple `sudo apt install -y build-essential`) avant de recourir à Homebrew.

## 6) Configurer la passerelle (loopback + authentification par token) et activer Tailscale Serve

Utilisez l'authentification par token par défaut. C'est prévisible et évite d'avoir besoin de drapeaux "insecure auth" Control UI.

```bash
# Gardez la passerelle privée sur la VM
openclaw config set gateway.bind loopback

# Exigez l'authentification pour la passerelle + Control UI
openclaw config set gateway.auth.mode token
openclaw doctor --generate-gateway-token

# Exposez via Tailscale Serve (HTTPS + accès tailnet)
openclaw config set gateway.tailscale.mode serve
openclaw config set gateway.trustedProxies '["127.0.0.1"]'

systemctl --user restart openclaw-gateway
```

## 7) Vérifier

```bash
# Vérifier la version
openclaw --version

# Vérifier l'état du daemon
systemctl --user status openclaw-gateway

# Vérifier Tailscale Serve
tailscale serve status

# Tester la réponse locale
curl http://localhost:18789
```

## 8) Verrouiller la sécurité du VCN

Maintenant que tout fonctionne, verrouillez le VCN pour bloquer tout le trafic sauf Tailscale. Le Virtual Cloud Network d'OCI agit comme un pare-feu à la périphérie du réseau — le trafic est bloqué avant d'atteindre votre instance.

1. Allez à **Networking → Virtual Cloud Networks** dans la console OCI
2. Cliquez sur votre VCN → **Security Lists** → Default Security List
3. **Supprimez** toutes les règles d'entrée sauf :
   - `0.0.0.0/0 UDP 41641` (Tailscale)
4. Conservez les règles de sortie par défaut (autoriser tout le trafic sortant)

Cela bloque SSH sur le port 22, HTTP, HTTPS et tout le reste à la périphérie du réseau. À partir de maintenant, vous ne pouvez vous connecter que via Tailscale.

---

## Accéder à l'interface de contrôle

Depuis n'importe quel appareil sur votre réseau Tailscale :

```
https://openclaw.<tailnet-name>.ts.net/
```

Remplacez `<tailnet-name>` par le nom de votre tailnet (visible dans `tailscale status`).

Aucun tunnel SSH nécessaire. Tailscale fournit :

- Chiffrement HTTPS (certificats automatiques)
- Authentification via l'identité Tailscale
- Accès depuis n'importe quel appareil sur votre tailnet (ordinateur portable, téléphone, etc.)

---

## Sécurité : VCN + Tailscale (ligne de base recommandée)

Avec le VCN verrouillé (seul UDP 41641 ouvert) et la passerelle liée à loopback, vous obtenez une défense en profondeur solide : le trafic public est bloqué à la périphérie du réseau, et l'accès administrateur se fait via votre tailnet.

Cette configuration supprime souvent le _besoin_ de règles de pare-feu supplémentaires basées sur l'hôte uniquement pour arrêter les attaques par force brute SSH à l'échelle d'Internet — mais vous devriez toujours maintenir le système à jour, exécuter `openclaw security audit`, et vérifier que vous n'écoutez pas accidentellement sur des interfaces publiques.

### Ce qui est déjà protégé

| Étape traditionnelle | Nécessaire ? | Pourquoi                                                                     |
| -------------------- | ------------ | ---------------------------------------------------------------------------- |
| Pare-feu UFW         | Non          | Le VCN bloque avant que le trafic n'atteigne l'instance                      |
| fail2ban             | Non          | Pas de force brute si le port 22 est bloqué au VCN                          |
| Durcissement sshd    | Non          | Tailscale SSH n'utilise pas sshd                                            |
| Désactiver la connexion root | Non   | Tailscale utilise l'identité Tailscale, pas les utilisateurs système        |
| Authentification par clé SSH uniquement | Non | Tailscale s'authentifie via votre tailnet                                   |
| Durcissement IPv6    | Généralement non | Dépend de vos paramètres VCN/subnet ; vérifiez ce qui est réellement assigné/exposé |

### Toujours recommandé

- **Permissions des credentials :** `chmod 700 ~/.openclaw`
- **Audit de sécurité :** `openclaw security audit`
- **Mises à jour système :** `sudo apt update && sudo apt upgrade` régulièrement
- **Surveiller Tailscale :** Examinez les appareils dans la [console d'administration Tailscale](https://login.tailscale.com/admin)

### Vérifier la posture de sécurité

```bash
# Confirmez qu'aucun port public n'écoute
sudo ss -tlnp | grep -v '127.0.0.1\|::1'

# Vérifiez que Tailscale SSH est actif
tailscale status | grep -q 'offers: ssh' && echo "Tailscale SSH active"

# Optionnel : désactiver complètement sshd
sudo systemctl disable --now ssh
```

---

## Secours : tunnel SSH

Si Tailscale Serve ne fonctionne pas, utilisez un tunnel SSH :

```bash
# Depuis votre machine locale (via Tailscale)
ssh -L 18789:127.0.0.1:18789 ubuntu@openclaw
```

Ouvrez ensuite `http://localhost:18789`.

---

## Dépannage

### La création d'instance échoue ("Out of capacity")

Les instances ARM du niveau gratuit sont populaires. Essayez :

- Un domaine de disponibilité différent
- Réessayez pendant les heures creuses (tôt le matin)
- Utilisez le filtre "Always Free" lors de la sélection de la forme

### Tailscale ne se connecte pas

```bash
# Vérifiez l'état
sudo tailscale status

# Réauthentifiez-vous
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
# Vérifiez que Tailscale Serve est en cours d'exécution
tailscale serve status

# Vérifiez que la passerelle écoute
curl http://localhost:18789

# Redémarrez si nécessaire
systemctl --user restart openclaw-gateway
```

### Problèmes de binaires ARM

Certains outils peuvent ne pas avoir de builds ARM. Vérifiez :

```bash
uname -m  # Devrait afficher aarch64
```

La plupart des paquets npm fonctionnent bien. Pour les binaires, recherchez les versions `linux-arm64` ou `aarch64`.

---

## Persistance

Tous les états se trouvent dans :

- `~/.openclaw/` — config, credentials, données de session
- `~/.openclaw/workspace/` — workspace (SOUL.md, mémoire, artefacts)

Sauvegardez régulièrement :

```bash
tar -czvf openclaw-backup.tar.gz ~/.openclaw ~/.openclaw/workspace
```

---

## Voir aussi

- [Gateway remote access](/gateway/remote) — autres modèles d'accès à distance
- [Tailscale integration](/gateway/tailscale) — documentation complète de Tailscale
- [Gateway configuration](/gateway/configuration) — toutes les options de configuration
- [DigitalOcean guide](/platforms/digitalocean) — si vous préférez payant + inscription plus facile
- [Hetzner guide](/install/hetzner) — alternative basée sur Docker
