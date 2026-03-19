---
summary: "Exécutez OpenClaw Gateway 24h/24 et 7j/7 sur une VM Azure Linux avec état durable"
read_when:
  - You want OpenClaw running 24/7 on Azure with Network Security Group hardening
  - You want a production-grade, always-on OpenClaw Gateway on your own Azure Linux VM
  - You want secure administration with Azure Bastion SSH
  - You want repeatable deployments with Azure Resource Manager templates
title: "Azure"
---

# OpenClaw sur VM Azure Linux

Ce guide configure une VM Azure Linux, applique le renforcement du groupe de sécurité réseau (NSG), configure Azure Bastion (point d'entrée SSH géré par Azure) et installe OpenClaw.

## Ce que vous allez faire

- Déployer les ressources de calcul et réseau Azure avec les modèles Azure Resource Manager (ARM)
- Appliquer les règles du groupe de sécurité réseau (NSG) Azure pour que SSH de la VM soit autorisé uniquement depuis Azure Bastion
- Utiliser Azure Bastion pour l'accès SSH
- Installer OpenClaw avec le script d'installation
- Vérifier la passerelle

## Avant de commencer

Vous aurez besoin de :

- Un abonnement Azure avec la permission de créer des ressources de calcul et réseau
- Azure CLI installé (voir [les étapes d'installation d'Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) si nécessaire)

## 1) Se connecter à Azure CLI

```bash
az login # Sign in and select your Azure subscription
az extension add -n ssh # Extension required for Azure Bastion SSH management
```

## 2) Enregistrer les fournisseurs de ressources requis (une seule fois)

```bash
az provider register --namespace Microsoft.Compute
az provider register --namespace Microsoft.Network
```

Vérifiez l'enregistrement du fournisseur de ressources Azure. Attendez que les deux affichent `Registered`.

```bash
az provider show --namespace Microsoft.Compute --query registrationState -o tsv
az provider show --namespace Microsoft.Network --query registrationState -o tsv
```

## 3) Définir les variables de déploiement

```bash
RG="rg-openclaw"
LOCATION="westus2"
TEMPLATE_URI="https://raw.githubusercontent.com/openclaw/openclaw/main/infra/azure/templates/azuredeploy.json"
PARAMS_URI="https://raw.githubusercontent.com/openclaw/openclaw/main/infra/azure/templates/azuredeploy.parameters.json"
```

## 4) Sélectionner la clé SSH

Utilisez votre clé publique existante si vous en avez une :

```bash
SSH_PUB_KEY="$(cat ~/.ssh/id_ed25519.pub)"
```

Si vous n'avez pas encore de clé SSH, exécutez ce qui suit :

```bash
ssh-keygen -t ed25519 -a 100 -f ~/.ssh/id_ed25519 -C "you@example.com"
SSH_PUB_KEY="$(cat ~/.ssh/id_ed25519.pub)"
```

## 5) Sélectionner la taille de la VM et la taille du disque du système d'exploitation

Définissez les variables de dimensionnement de la VM et du disque :

```bash
VM_SIZE="Standard_B2as_v2"
OS_DISK_SIZE_GB=64
```

Choisissez une taille de VM et une taille de disque du système d'exploitation disponibles dans votre abonnement/région Azure et correspondant à votre charge de travail :

- Commencez plus petit pour une utilisation légère et augmentez l'échelle plus tard
- Utilisez plus de vCPU/RAM/taille de disque du système d'exploitation pour une automatisation plus lourde, plus de canaux ou des charges de travail de modèle/outil plus importantes
- Si une taille de VM n'est pas disponible dans votre région ou quota d'abonnement, choisissez la SKU disponible la plus proche

Lister les tailles de VM disponibles dans votre région cible :

```bash
az vm list-skus --location "${LOCATION}" --resource-type virtualMachines -o table
```

Vérifiez votre utilisation/quota actuel de vCPU et de taille de disque du système d'exploitation :

```bash
az vm list-usage --location "${LOCATION}" -o table
```

## 6) Créer le groupe de ressources

```bash
az group create -n "${RG}" -l "${LOCATION}"
```

## 7) Déployer les ressources

Cette commande applique votre clé SSH sélectionnée, la taille de la VM et la taille du disque du système d'exploitation.

```bash
az deployment group create \
  -g "${RG}" \
  --template-uri "${TEMPLATE_URI}" \
  --parameters "${PARAMS_URI}" \
  --parameters location="${LOCATION}" \
  --parameters vmSize="${VM_SIZE}" \
  --parameters osDiskSizeGb="${OS_DISK_SIZE_GB}" \
  --parameters sshPublicKey="${SSH_PUB_KEY}"
```

## 8) SSH dans la VM via Azure Bastion

```bash
RG="rg-openclaw"
VM_NAME="vm-openclaw"
BASTION_NAME="bas-openclaw"
ADMIN_USERNAME="openclaw"
VM_ID="$(az vm show -g "${RG}" -n "${VM_NAME}" --query id -o tsv)"

az network bastion ssh \
  --name "${BASTION_NAME}" \
  --resource-group "${RG}" \
  --target-resource-id "${VM_ID}" \
  --auth-type ssh-key \
  --username "${ADMIN_USERNAME}" \
  --ssh-key ~/.ssh/id_ed25519
```

## 9) Installer OpenClaw (dans le shell de la VM)

```bash
curl -fsSL https://openclaw.ai/install.sh -o /tmp/openclaw-install.sh
bash /tmp/openclaw-install.sh
rm -f /tmp/openclaw-install.sh
openclaw --version
```

Le script d'installation gère la détection/installation de Node et exécute l'intégration par défaut.

## 10) Vérifier la passerelle

Une fois l'intégration terminée :

```bash
openclaw gateway status
```

La plupart des équipes Azure d'entreprise ont déjà des licences GitHub Copilot. Si c'est votre cas, nous vous recommandons de choisir le fournisseur GitHub Copilot dans l'assistant d'intégration OpenClaw. Voir [fournisseur GitHub Copilot](/fr/providers/github-copilot).

Le modèle ARM inclus utilise l'image Ubuntu `version: "latest"` pour des raisons de commodité. Si vous avez besoin de builds reproductibles, épinglez une version d'image spécifique dans `infra/azure/templates/azuredeploy.json` (vous pouvez lister les versions avec `az vm image list --publisher Canonical --offer ubuntu-24_04-lts --sku server --all -o table`).

## Étapes suivantes

- Configurer les canaux de messagerie : [Canaux](/fr/channels)
- Associer les appareils locaux en tant que nœuds : [Nœuds](/fr/nodes)
- Configurer la passerelle : [Configuration de la passerelle](/fr/gateway/configuration)
- Pour plus de détails sur le déploiement OpenClaw Azure avec le fournisseur de modèle GitHub Copilot : [OpenClaw sur Azure avec GitHub Copilot](https://github.com/johnsonshi/openclaw-azure-github-copilot)
