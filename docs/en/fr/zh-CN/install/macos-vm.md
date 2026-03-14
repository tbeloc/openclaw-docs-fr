---
read_when:
  - Vous voulez isoler OpenClaw de votre environnement macOS principal
  - Vous voulez intégrer iMessage (BlueBubbles) dans un bac à sable
  - Vous voulez un environnement macOS réinitialisable et clonable
  - Vous voulez comparer les options de VM macOS locales et hébergées
summary: Exécutez OpenClaw dans une VM macOS isolée en bac à sable (locale ou hébergée) quand vous avez besoin d'isolation ou d'iMessage
title: Machine virtuelle macOS
x-i18n:
  generated_at: "2026-02-03T07:53:09Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 4d1c85a5e4945f9f0796038cd5960edecb71ec4dffb6f9686be50adb75180716
  source_path: platforms/macos-vm.md
  workflow: 15
---

# Exécuter OpenClaw sur une machine virtuelle macOS (isolée en bac à sable)

## Approche par défaut recommandée (pour la plupart des utilisateurs)

- **Petit VPS Linux** pour une passerelle toujours en ligne à faible coût. Voir [Hébergement VPS](/vps).
- **Matériel dédié** (Mac mini ou machine Linux) si vous voulez un contrôle total et une **adresse IP résidentielle** pour l'automatisation du navigateur. De nombreux sites bloquent les adresses IP des centres de données, donc la navigation locale fonctionne généralement mieux.
- **Approche hybride :** Gardez la passerelle sur un VPS bon marché, connectez votre Mac en tant que **nœud** quand vous avez besoin d'automatisation du navigateur/UI. Voir [Nœuds](/nodes) et [Passerelle distante](/gateway/remote).

Utilisez une VM macOS quand vous avez particulièrement besoin de fonctionnalités exclusives à macOS (iMessage/BlueBubbles) ou quand vous voulez une isolation stricte par rapport à votre Mac quotidien.

## Options de VM macOS

### Exécuter une VM locale sur votre Mac Apple Silicon (Lume)

Exécutez OpenClaw dans une VM macOS en bac à sable sur votre Mac Apple Silicon existant en utilisant [Lume](https://cua.ai/docs/lume).

Cela vous offre :

- Un environnement macOS complet isolé (votre hôte reste propre)
- Support d'iMessage via BlueBubbles (impossible sur Linux/Windows)
- Réinitialisation instantanée en clonant la VM
- Aucun matériel supplémentaire ni coût cloud

### Fournisseurs Mac hébergés (cloud)

Si vous voulez macOS dans le cloud, les fournisseurs Mac hébergés peuvent aussi fonctionner :

- [MacStadium](https://www.macstadium.com/) (Mac hébergé)
- D'autres fournisseurs Mac hébergés peuvent aussi fonctionner ; suivez leur documentation VM + SSH

Une fois que vous avez accès SSH à votre VM macOS, continuez à l'étape 6 ci-dessous.

---

## Chemin rapide (Lume, utilisateurs expérimentés)

1. Installez Lume
2. `lume create openclaw --os macos --ipsw latest`
3. Terminez l'assistant de configuration, activez la connexion à distance (SSH)
4. `lume run openclaw --no-display`
5. SSH dedans, installez OpenClaw, configurez les canaux
6. Terminé

---

## Ce dont vous avez besoin (Lume)

- Mac Apple Silicon (M1/M2/M3/M4)
- macOS Sequoia ou plus récent installé sur l'hôte
- Environ 60 Go d'espace disque disponible par VM
- Environ 20 minutes

---

## 1) Installer Lume

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/lume/scripts/install.sh)"
```

Si `~/.local/bin` n'est pas dans votre PATH :

```bash
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.zshrc && source ~/.zshrc
```

Vérifiez :

```bash
lume --version
```

Documentation : [Installation de Lume](https://cua.ai/docs/lume/guide/getting-started/installation)

---

## 2) Créer une VM macOS

```bash
lume create openclaw --os macos --ipsw latest
```

Cela télécharge macOS et crée la VM. Une fenêtre VNC s'ouvrira automatiquement.

Remarque : Le téléchargement peut prendre un certain temps selon votre connexion réseau.

---

## 3) Terminer l'assistant de configuration

Dans la fenêtre VNC :

1. Sélectionnez la langue et la région
2. Ignorez l'Apple ID (ou connectez-vous si vous voulez iMessage plus tard)
3. Créez un compte utilisateur (mémorisez le nom d'utilisateur et le mot de passe)
4. Ignorez toutes les fonctionnalités optionnelles

Une fois la configuration terminée, activez SSH :

1. Ouvrez Paramètres système → Général → Partage
2. Activez "Connexion à distance"

---

## 4) Obtenir l'adresse IP de la VM

```bash
lume get openclaw
```

Recherchez l'adresse IP (généralement `192.168.64.x`).

---

## 5) SSH dans la VM

```bash
ssh youruser@192.168.64.X
```

Remplacez `youruser` par le compte que vous avez créé et l'IP par celle de votre VM.

---

## 6) Installer OpenClaw

À l'intérieur de la VM :

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

Suivez les invites d'intégration pour configurer votre fournisseur de modèle (Anthropic, OpenAI, etc.).

---

## 7) Configurer les canaux

Modifiez le fichier de configuration :

```bash
nano ~/.openclaw/openclaw.json
```

Ajoutez vos canaux :

```json
{
  "channels": {
    "whatsapp": {
      "dmPolicy": "allowlist",
      "allowFrom": ["+15551234567"]
    },
    "telegram": {
      "botToken": "YOUR_BOT_TOKEN"
    }
  }
}
```

Puis connectez-vous à WhatsApp (scannez le code QR) :

```bash
openclaw channels login
```

---

## 8) Exécuter la VM sans affichage

Arrêtez la VM et redémarrez-la en mode sans affichage :

```bash
lume stop openclaw
lume run openclaw --no-display
```

La VM s'exécute en arrière-plan. Le démon OpenClaw garde la passerelle en fonctionnement.

Vérifiez l'état :

```bash
ssh youruser@192.168.64.X "openclaw status"
```

---

## Bonus : Intégration iMessage

C'est la fonctionnalité killer en exécutant sur macOS. Utilisez [BlueBubbles](https://bluebubbles.app) pour ajouter iMessage à OpenClaw.

À l'intérieur de la VM :

1. Téléchargez BlueBubbles depuis bluebubbles.app
2. Connectez-vous avec votre Apple ID
3. Activez l'API Web et définissez un mot de passe
4. Pointez les webhooks BlueBubbles vers votre passerelle (exemple : `https://your-gateway-host:3000/bluebubbles-webhook?password=<password>`)

Ajoutez à votre configuration OpenClaw :

```json
{
  "channels": {
    "bluebubbles": {
      "serverUrl": "http://localhost:1234",
      "password": "your-api-password",
      "webhookPath": "/bluebubbles-webhook"
    }
  }
}
```

Redémarrez la passerelle. Maintenant vos agents peuvent envoyer et recevoir des iMessages.

Détails de configuration complets : [Canal BlueBubbles](/channels/bluebubbles)

---

## Sauvegarder l'image dorée

Avant de personnaliser davantage, créez un snapshot de votre état propre :

```bash
lume stop openclaw
lume clone openclaw openclaw-golden
```

Réinitialisez à tout moment :

```bash
lume stop openclaw && lume delete openclaw
lume clone openclaw-golden openclaw
lume run openclaw --no-display
```

---

## Exécution 24/7

Gardez la VM en fonctionnement en :

- Gardant votre Mac branché
- Désactivant la mise en veille dans Paramètres système → Économie d'énergie
- Utilisant `caffeinate` si nécessaire

Pour une véritable disponibilité permanente, envisagez un Mac mini dédié ou un petit VPS. Voir [Hébergement VPS](/vps).

---

## Dépannage

| Problème                      | Solution                                                                    |
| ----------------------------- | ---------------------------------------------------------------------------- |
| Impossible de SSH dans la VM  | Vérifiez que "Connexion à distance" est activée dans les paramètres système de la VM |
| L'IP de la VM ne s'affiche pas | Attendez que la VM démarre complètement, exécutez `lume get openclaw` à nouveau |
| Commande Lume introuvable     | Ajoutez `~/.local/bin` à votre PATH                                        |
| Échec du scan du code QR WhatsApp | Assurez-vous d'exécuter `openclaw channels login` en étant connecté à la VM (pas l'hôte) |

---

## Documentation connexe

- [Hébergement VPS](/vps)
- [Nœuds](/nodes)
- [Passerelle distante](/gateway/remote)
- [Canal BlueBubbles](/channels/bluebubbles)
- [Démarrage rapide Lume](https://cua.ai/docs/lume/guide/getting-started/quickstart)
- [Référence CLI Lume](https://cua.ai/docs/lume/reference/cli-reference)
- [Configuration de VM sans surveillance](https://cua.ai/docs/lume/guide/fundamentals/unattended-setup) (avancé)
- [Isolation Docker](/install/docker) (approche d'isolation alternative)
