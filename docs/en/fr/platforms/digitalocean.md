---
summary: "OpenClaw sur DigitalOcean (option VPS payante simple)"
read_when:
  - Configuration d'OpenClaw sur DigitalOcean
  - Recherche d'hébergement VPS bon marché pour OpenClaw
title: "DigitalOcean"
---

# OpenClaw sur DigitalOcean

## Objectif

Exécuter une passerelle OpenClaw persistante sur DigitalOcean pour **6 $/mois** (ou 4 $/mois avec tarification réservée).

Si vous voulez une option à 0 $/mois et que vous ne craignez pas ARM + configuration spécifique au fournisseur, consultez le [guide Oracle Cloud](/fr/platforms/oracle).

## Comparaison des coûts (2026)

| Fournisseur  | Plan            | Spécifications         | Prix/mois   | Notes                                      |
| ------------ | --------------- | ---------------------- | ----------- | ------------------------------------------ |
| Oracle Cloud | Always Free ARM | jusqu'à 4 OCPU, 24GB RAM | $0          | ARM, capacité limitée / problèmes d'inscription |
| Hetzner      | CX22            | 2 vCPU, 4GB RAM        | €3,79 (~$4) | Option payante la moins chère              |
| DigitalOcean | Basic           | 1 vCPU, 1GB RAM        | $6          | Interface facile, bonne documentation      |
| Vultr        | Cloud Compute   | 1 vCPU, 1GB RAM        | $6          | Nombreux emplacements                      |
| Linode       | Nanode          | 1 vCPU, 1GB RAM        | $5          | Maintenant partie d'Akamai                 |

**Choisir un fournisseur :**

- DigitalOcean : UX la plus simple + configuration prévisible (ce guide)
- Hetzner : bon rapport prix/performance (voir [guide Hetzner](/fr/install/hetzner))
- Oracle Cloud : peut être gratuit, mais plus délicat et ARM uniquement (voir [guide Oracle](/fr/platforms/oracle))

---

## Prérequis

- Compte DigitalOcean ([inscription avec 200 $ de crédit gratuit](https://m.do.co/c/signup))
- Paire de clés SSH (ou volonté d'utiliser l'authentification par mot de passe)
- ~20 minutes

## 1) Créer un Droplet

<Warning>
Utilisez une image de base propre (Ubuntu 24.04 LTS). Évitez les images Marketplace tierces en un clic à moins d'avoir examiné leurs scripts de démarrage et paramètres de pare-feu par défaut.
</Warning>

1. Connectez-vous à [DigitalOcean](https://cloud.digitalocean.com/)
2. Cliquez sur **Create → Droplets**
3. Choisissez :
   - **Region :** La plus proche de vous (ou de vos utilisateurs)
   - **Image :** Ubuntu 24.04 LTS
   - **Size :** Basic → Regular → **$6/mois** (1 vCPU, 1GB RAM, 25GB SSD)
   - **Authentication :** Clé SSH (recommandé) ou mot de passe
4. Cliquez sur **Create Droplet**
5. Notez l'adresse IP

## 2) Connexion via SSH

```bash
ssh root@YOUR_DROPLET_IP
```

## 3) Installer OpenClaw

```bash
# Mettre à jour le système
apt update && apt upgrade -y

# Installer Node.js 24
curl -fsSL https://deb.nodesource.com/setup_24.x | bash -
apt install -y nodejs

# Installer OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# Vérifier
openclaw --version
```

## 4) Exécuter l'intégration

```bash
openclaw onboard --install-daemon
```

L'assistant vous guidera à travers :

- Authentification du modèle (clés API ou OAuth)
- Configuration des canaux (Telegram, WhatsApp, Discord, etc.)
- Jeton de passerelle (généré automatiquement)
- Installation du daemon (systemd)

## 5) Vérifier la passerelle

```bash
# Vérifier le statut
openclaw status

# Vérifier le service
systemctl --user status openclaw-gateway.service

# Afficher les journaux
journalctl --user -u openclaw-gateway.service -f
```

## 6) Accéder au tableau de bord

La passerelle se lie à la boucle locale par défaut. Pour accéder à l'interface de contrôle :

**Option A : Tunnel SSH (recommandé)**

```bash
# Depuis votre machine locale
ssh -L 18789:localhost:18789 root@YOUR_DROPLET_IP

# Puis ouvrez : http://localhost:18789
```

**Option B : Tailscale Serve (HTTPS, boucle locale uniquement)**

```bash
# Sur le droplet
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up

# Configurer la passerelle pour utiliser Tailscale Serve
openclaw config set gateway.tailscale.mode serve
openclaw gateway restart
```

Ouvrez : `https://<magicdns>/`

Notes :

- Serve maintient la passerelle en boucle locale uniquement et authentifie le trafic de l'interface de contrôle/WebSocket via les en-têtes d'identité Tailscale (l'authentification sans jeton suppose un hôte de passerelle de confiance ; les API HTTP nécessitent toujours un jeton/mot de passe).
- Pour exiger un jeton/mot de passe à la place, définissez `gateway.auth.allowTailscale: false` ou utilisez `gateway.auth.mode: "password"`.

**Option C : Liaison Tailnet (pas de Serve)**

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
# Scanner le code QR
```

Voir [Channels](/fr/channels) pour les autres fournisseurs.

---

## Optimisations pour 1GB RAM

Le droplet à 6 $ n'a que 1GB RAM. Pour que tout fonctionne correctement :

### Ajouter du swap (recommandé)

```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### Utiliser un modèle plus léger

Si vous rencontrez des OOM, envisagez :

- Utiliser des modèles basés sur API (Claude, GPT) au lieu de modèles locaux
- Définir `agents.defaults.model.primary` sur un modèle plus petit

### Surveiller la mémoire

```bash
free -h
htop
```

---

## Persistance

Tous les états se trouvent dans :

- `~/.openclaw/` — configuration, identifiants, données de session
- `~/.openclaw/workspace/` — espace de travail (SOUL.md, mémoire, etc.)

Ceux-ci survivent aux redémarrages. Sauvegardez-les périodiquement :

```bash
tar -czvf openclaw-backup.tar.gz ~/.openclaw ~/.openclaw/workspace
```

---

## Alternative gratuite Oracle Cloud

Oracle Cloud offre des instances ARM **Always Free** qui sont considérablement plus puissantes que n'importe quelle option payante ici — pour 0 $/mois.

| Ce que vous obtenez | Spécifications         |
| ------------------- | ---------------------- |
| **4 OCPUs**         | ARM Ampere A1          |
| **24GB RAM**        | Plus que suffisant     |
| **200GB stockage**  | Volume de bloc         |
| **Gratuit à jamais** | Aucun frais de carte de crédit |

**Mises en garde :**

- L'inscription peut être délicate (réessayez si elle échoue)
- Architecture ARM — la plupart des choses fonctionnent, mais certains binaires nécessitent des builds ARM

Pour le guide de configuration complet, voir [Oracle Cloud](/fr/platforms/oracle). Pour les conseils d'inscription et le dépannage du processus d'inscription, voir ce [guide communautaire](https://gist.github.com/rssnyder/51e3cfedd730e7dd5f4a816143b25dbd).

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
# Vérifier la mémoire
free -h

# Ajouter plus de swap
# Ou passer à un droplet à 12 $/mois (2GB RAM)
```

---

## Voir aussi

- [Guide Hetzner](/fr/install/hetzner) — moins cher, plus puissant
- [Installation Docker](/fr/install/docker) — configuration conteneurisée
- [Tailscale](/fr/gateway/tailscale) — accès à distance sécurisé
- [Configuration](/fr/gateway/configuration) — référence de configuration complète
