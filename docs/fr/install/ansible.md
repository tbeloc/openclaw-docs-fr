```markdown
---
summary: "Installation automatisée et renforcée d'OpenClaw avec Ansible, Tailscale VPN et isolation par pare-feu"
read_when:
  - You want automated server deployment with security hardening
  - You need firewall-isolated setup with VPN access
  - You're deploying to remote Debian/Ubuntu servers
title: "Ansible"
---

# Installation Ansible

La méthode recommandée pour déployer OpenClaw sur des serveurs de production est via **[openclaw-ansible](https://github.com/openclaw/openclaw-ansible)** — un installateur automatisé avec une architecture axée sur la sécurité.

## Démarrage rapide

Installation en une seule commande :

```bash
curl -fsSL https://raw.githubusercontent.com/openclaw/openclaw-ansible/main/install.sh | bash
```

> **📦 Guide complet : [github.com/openclaw/openclaw-ansible](https://github.com/openclaw/openclaw-ansible)**
>
> Le dépôt openclaw-ansible est la source de vérité pour le déploiement Ansible. Cette page est un aperçu rapide.

## Ce que vous obtenez

- 🔒 **Sécurité basée sur le pare-feu** : UFW + isolation Docker (seuls SSH + Tailscale accessibles)
- 🔐 **VPN Tailscale** : Accès à distance sécurisé sans exposer les services publiquement
- 🐳 **Docker** : Conteneurs sandbox isolés, liaisons localhost uniquement
- 🛡️ **Défense en profondeur** : Architecture de sécurité à 4 niveaux
- 🚀 **Configuration en une commande** : Déploiement complet en quelques minutes
- 🔧 **Intégration Systemd** : Démarrage automatique au boot avec renforcement

## Prérequis

- **OS** : Debian 11+ ou Ubuntu 20.04+
- **Accès** : Privilèges root ou sudo
- **Réseau** : Connexion Internet pour l'installation des paquets
- **Ansible** : 2.14+ (installé automatiquement par le script de démarrage rapide)

## Ce qui est installé

Le playbook Ansible installe et configure :

1. **Tailscale** (VPN maillé pour l'accès à distance sécurisé)
2. **Pare-feu UFW** (ports SSH + Tailscale uniquement)
3. **Docker CE + Compose V2** (pour les sandboxes d'agents)
4. **Node.js 24 + pnpm** (dépendances d'exécution ; Node 22 LTS, actuellement `22.16+`, reste supporté pour la compatibilité)
5. **OpenClaw** (basé sur l'hôte, non conteneurisé)
6. **Service Systemd** (démarrage automatique avec renforcement de sécurité)

Remarque : La passerelle s'exécute **directement sur l'hôte** (pas dans Docker), mais les sandboxes d'agents utilisent Docker pour l'isolation. Voir [Sandboxing](/gateway/sandboxing) pour plus de détails.

## Configuration post-installation

Une fois l'installation terminée, basculez vers l'utilisateur openclaw :

```bash
sudo -i -u openclaw
```

Le script post-installation vous guidera à travers :

1. **Assistant d'intégration** : Configurer les paramètres d'OpenClaw
2. **Connexion au fournisseur** : Connecter WhatsApp/Telegram/Discord/Signal
3. **Test de la passerelle** : Vérifier l'installation
4. **Configuration de Tailscale** : Se connecter à votre maillage VPN

### Commandes rapides

```bash
# Vérifier l'état du service
sudo systemctl status openclaw

# Afficher les journaux en direct
sudo journalctl -u openclaw -f

# Redémarrer la passerelle
sudo systemctl restart openclaw

# Connexion au fournisseur (exécuter en tant qu'utilisateur openclaw)
sudo -i -u openclaw
openclaw channels login
```

## Architecture de sécurité

### Défense à 4 niveaux

1. **Pare-feu (UFW)** : Seuls SSH (22) + Tailscale (41641/udp) exposés publiquement
2. **VPN (Tailscale)** : Passerelle accessible uniquement via le maillage VPN
3. **Isolation Docker** : Chaîne iptables DOCKER-USER empêche l'exposition des ports externes
4. **Renforcement Systemd** : NoNewPrivileges, PrivateTmp, utilisateur non privilégié

### Vérification

Testez la surface d'attaque externe :

```bash
nmap -p- YOUR_SERVER_IP
```

Devrait afficher **uniquement le port 22** (SSH) ouvert. Tous les autres services (passerelle, Docker) sont verrouillés.

### Disponibilité de Docker

Docker est installé pour les **sandboxes d'agents** (exécution d'outils isolée), pas pour exécuter la passerelle elle-même. La passerelle se lie à localhost uniquement et est accessible via le VPN Tailscale.

Voir [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools) pour la configuration du sandbox.

## Installation manuelle

Si vous préférez un contrôle manuel sur l'automatisation :

```bash
# 1. Installer les prérequis
sudo apt update && sudo apt install -y ansible git

# 2. Cloner le dépôt
git clone https://github.com/openclaw/openclaw-ansible.git
cd openclaw-ansible

# 3. Installer les collections Ansible
ansible-galaxy collection install -r requirements.yml

# 4. Exécuter le playbook
./run-playbook.sh

# Ou exécuter directement (puis exécuter manuellement /tmp/openclaw-setup.sh après)
# ansible-playbook playbook.yml --ask-become-pass
```

## Mise à jour d'OpenClaw

L'installateur Ansible configure OpenClaw pour les mises à jour manuelles. Voir [Updating](/install/updating) pour le flux de mise à jour standard.

Pour réexécuter le playbook Ansible (par exemple, pour les modifications de configuration) :

```bash
cd openclaw-ansible
./run-playbook.sh
```

Remarque : C'est idempotent et sûr d'exécuter plusieurs fois.

## Dépannage

### Le pare-feu bloque ma connexion

Si vous êtes verrouillé :

- Assurez-vous de pouvoir accéder via le VPN Tailscale d'abord
- L'accès SSH (port 22) est toujours autorisé
- La passerelle est **uniquement** accessible via Tailscale par conception

### Le service ne démarre pas

```bash
# Vérifier les journaux
sudo journalctl -u openclaw -n 100

# Vérifier les permissions
sudo ls -la /opt/openclaw

# Tester le démarrage manuel
sudo -i -u openclaw
cd ~/openclaw
pnpm start
```

### Problèmes de sandbox Docker

```bash
# Vérifier que Docker est en cours d'exécution
sudo systemctl status docker

# Vérifier l'image du sandbox
sudo docker images | grep openclaw-sandbox

# Construire l'image du sandbox si manquante
cd /opt/openclaw/openclaw
sudo -u openclaw ./scripts/sandbox-setup.sh
```

### La connexion au fournisseur échoue

Assurez-vous d'exécuter en tant qu'utilisateur `openclaw` :

```bash
sudo -i -u openclaw
openclaw channels login
```

## Configuration avancée

Pour l'architecture de sécurité détaillée et le dépannage :

- [Security Architecture](https://github.com/openclaw/openclaw-ansible/blob/main/docs/security.md)
- [Technical Details](https://github.com/openclaw/openclaw-ansible/blob/main/docs/architecture.md)
- [Troubleshooting Guide](https://github.com/openclaw/openclaw-ansible/blob/main/docs/troubleshooting.md)

## Connexes

- [openclaw-ansible](https://github.com/openclaw/openclaw-ansible) — guide de déploiement complet
- [Docker](/install/docker) — configuration de la passerelle conteneurisée
- [Sandboxing](/gateway/sandboxing) — configuration du sandbox d'agent
- [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools) — isolation par agent
```
