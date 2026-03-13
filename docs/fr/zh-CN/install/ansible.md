---
read_when:
  - Vous souhaitez un déploiement de serveur automatisé avec renforcement de sécurité
  - Vous avez besoin d'une configuration de pare-feu isolée avec accès VPN
  - Vous déployez sur un serveur Debian/Ubuntu distant
summary: Installation automatisée et renforcée d'OpenClaw avec Ansible, Tailscale VPN et isolation du pare-feu
title: Ansible
x-i18n:
  generated_at: "2026-02-03T07:49:29Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 896807f344d923f09039f377c13b4bf4a824aa94eec35159fc169596a3493b29
  source_path: install/ansible.md
  workflow: 15
---

# Installation Ansible

La méthode recommandée pour déployer OpenClaw sur un serveur de production est via **[openclaw-ansible](https://github.com/openclaw/openclaw-ansible)** — un programme d'installation automatisé avec une architecture axée sur la sécurité.

## Démarrage rapide

Installation en une seule commande :

```bash
curl -fsSL https://raw.githubusercontent.com/openclaw/openclaw-ansible/main/install.sh | bash
```

> **📦 Guide complet : [github.com/openclaw/openclaw-ansible](https://github.com/openclaw/openclaw-ansible)**
>
> Le dépôt openclaw-ansible est la source faisant autorité pour les déploiements Ansible. Cette page est un aperçu rapide.

## Ce que vous obtenez

- 🔒 **Sécurité axée sur le pare-feu** : UFW + isolation Docker (accessible uniquement via SSH + Tailscale)
- 🔐 **VPN Tailscale** : Accès à distance sécurisé sans exposition publique des services
- 🐳 **Docker** : Conteneurs sandbox isolés, liés uniquement à localhost
- 🛡️ **Défense en profondeur** : Architecture de sécurité à 4 couches
- 🚀 **Configuration en une commande** : Déploiement en quelques minutes
- 🔧 **Intégration Systemd** : Démarrage automatique avec renforcement

## Exigences

- **Système d'exploitation** : Debian 11+ ou Ubuntu 20.04+
- **Accès** : Droits root ou sudo
- **Réseau** : Connexion Internet pour l'installation des paquets
- **Ansible** : 2.14+ (installé automatiquement par le script de démarrage rapide)

## Contenu de l'installation

Le playbook Ansible installe et configure :

1. **Tailscale** (VPN mesh pour accès à distance sécurisé)
2. **Pare-feu UFW** (autorise uniquement les ports SSH + Tailscale)
3. **Docker CE + Compose V2** (pour sandbox d'agents)
4. **Node.js 22.x + pnpm** (dépendances d'exécution)
5. **OpenClaw** (basé sur l'hôte, non conteneurisé)
6. **Service Systemd** (démarrage automatique avec renforcement)

Remarque : La passerelle **s'exécute directement sur l'hôte** (pas dans Docker), mais les sandbox d'agents utilisent Docker pour l'isolation. Voir [Isolation Sandbox](/gateway/sandboxing) pour plus de détails.

## Configuration après installation

Une fois l'installation terminée, basculez vers l'utilisateur openclaw :

```bash
sudo -i -u openclaw
```

Le script post-installation vous guidera à travers :

1. **Assistant d'intégration** : Configuration des paramètres OpenClaw
2. **Connexion aux fournisseurs** : Connexion à WhatsApp/Telegram/Discord/Signal
3. **Test de la passerelle** : Vérification de l'installation
4. **Configuration Tailscale** : Connexion à votre mesh VPN

### Commandes courantes

```bash
# Vérifier l'état du service
sudo systemctl status openclaw

# Afficher les journaux en temps réel
sudo journalctl -u openclaw -f

# Redémarrer la passerelle
sudo systemctl restart openclaw

# Connexion aux fournisseurs (exécuter en tant qu'utilisateur openclaw)
sudo -i -u openclaw
openclaw channels login
```

## Architecture de sécurité

### Défense à 4 couches

1. **Pare-feu (UFW)** : Expose uniquement SSH (22) + Tailscale (41641/udp)
2. **VPN (Tailscale)** : La passerelle est accessible uniquement via le mesh VPN
3. **Isolation Docker** : Chaîne iptables DOCKER-USER empêche l'exposition des ports externes
4. **Renforcement Systemd** : NoNewPrivileges, PrivateTmp, utilisateur non privilégié

### Vérification

Testez la surface d'attaque externe :

```bash
nmap -p- YOUR_SERVER_IP
```

Devrait afficher **uniquement le port 22** (SSH) ouvert. Tous les autres services (passerelle, Docker) sont verrouillés.

### Disponibilité Docker

Docker est utilisé pour les **sandbox d'agents** (exécution d'outils isolée), pas pour exécuter la passerelle elle-même. La passerelle est liée uniquement à localhost et accessible via le VPN Tailscale.

Voir [Multi-Agent Sandbox et Outils](/tools/multi-agent-sandbox-tools) pour la configuration des sandbox.

## Installation manuelle

Si vous préférez le contrôle manuel plutôt que l'automatisation :

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

# Ou exécuter directement (puis exécuter manuellement /tmp/openclaw-setup.sh)
# ansible-playbook playbook.yml --ask-become-pass
```

## Mettre à jour OpenClaw

Le programme d'installation Ansible configure OpenClaw pour les mises à jour manuelles. Voir [Mise à jour](/install/updating) pour le processus de mise à jour standard.

Pour réexécuter le playbook Ansible (par exemple, pour les modifications de configuration) :

```bash
cd openclaw-ansible
./run-playbook.sh
```

Remarque : C'est idempotent et peut être exécuté en toute sécurité plusieurs fois.

## Dépannage

### Le pare-feu a bloqué ma connexion

Si vous êtes verrouillé :

- Assurez-vous de pouvoir d'abord accéder via le VPN Tailscale
- L'accès SSH (port 22) est toujours autorisé
- La passerelle est accessible **uniquement** via Tailscale, c'est intentionnel

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
# Vérifier que Docker s'exécute
sudo systemctl status docker

# Vérifier les images sandbox
sudo docker images | grep openclaw-sandbox

# Construire l'image sandbox si manquante
cd /opt/openclaw/openclaw
sudo -u openclaw ./scripts/sandbox-setup.sh
```

### Échec de la connexion aux fournisseurs

Assurez-vous d'exécuter en tant qu'utilisateur `openclaw` :

```bash
sudo -i -u openclaw
openclaw channels login
```

## Configuration avancée

Architecture de sécurité détaillée et dépannage :

- [Architecture de sécurité](https://github.com/openclaw/openclaw-ansible/blob/main/docs/security.md)
- [Détails techniques](https://github.com/openclaw/openclaw-ansible/blob/main/docs/architecture.md)
- [Guide de dépannage](https://github.com/openclaw/openclaw-ansible/blob/main/docs/troubleshooting.md)

## Contenu connexe

- [openclaw-ansible](https://github.com/openclaw/openclaw-ansible) — Guide de déploiement complet
- [Docker](/install/docker) — Configuration de passerelle conteneurisée
- [Isolation Sandbox](/gateway/sandboxing) — Configuration des sandbox d'agents
- [Multi-Agent Sandbox et Outils](/tools/multi-agent-sandbox-tools) — Isolation par agent
