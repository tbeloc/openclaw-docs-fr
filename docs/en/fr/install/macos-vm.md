---
summary: "Exécutez OpenClaw dans une VM macOS en sandbox (locale ou hébergée) quand vous avez besoin d'isolation ou d'iMessage"
read_when:
  - You want OpenClaw isolated from your main macOS environment
  - You want iMessage integration (BlueBubbles) in a sandbox
  - You want a resettable macOS environment you can clone
  - You want to compare local vs hosted macOS VM options
title: "macOS VMs"
---

# OpenClaw sur les VMs macOS (Sandboxing)

## Configuration par défaut recommandée (la plupart des utilisateurs)

- **Petit VPS Linux** pour une Gateway toujours active et un coût réduit. Voir [Hébergement VPS](/fr/vps).
- **Matériel dédié** (Mac mini ou boîtier Linux) si vous voulez un contrôle total et une **adresse IP résidentielle** pour l'automatisation de navigateur. De nombreux sites bloquent les adresses IP des data centers, donc la navigation locale fonctionne souvent mieux.
- **Hybride :** gardez la Gateway sur un VPS bon marché et connectez votre Mac en tant que **nœud** quand vous avez besoin d'automatisation de navigateur/UI. Voir [Nœuds](/fr/nodes) et [Gateway distante](/fr/gateway/remote).

Utilisez une VM macOS quand vous avez spécifiquement besoin de capacités macOS uniquement (iMessage/BlueBubbles) ou quand vous voulez une isolation stricte de votre Mac quotidien.

## Options de VM macOS

### VM locale sur votre Mac Apple Silicon (Lume)

Exécutez OpenClaw dans une VM macOS en sandbox sur votre Mac Apple Silicon existant en utilisant [Lume](https://cua.ai/docs/lume).

Cela vous donne :

- Environnement macOS complet en isolation (votre hôte reste propre)
- Support iMessage via BlueBubbles (impossible sur Linux/Windows)
- Réinitialisation instantanée en clonant les VMs
- Aucun coût matériel ou cloud supplémentaire

### Fournisseurs Mac hébergés (cloud)

Si vous voulez macOS dans le cloud, les fournisseurs Mac hébergés fonctionnent aussi :

- [MacStadium](https://www.macstadium.com/) (Macs hébergés)
- D'autres fournisseurs Mac hébergés fonctionnent aussi ; suivez leur documentation VM + SSH

Une fois que vous avez accès SSH à une VM macOS, continuez à l'étape 6 ci-dessous.

---

## Chemin rapide (Lume, utilisateurs expérimentés)

1. Installez Lume
2. `lume create openclaw --os macos --ipsw latest`
3. Complétez l'Assistant de configuration, activez la Connexion à distance (SSH)
4. `lume run openclaw --no-display`
5. SSH, installez OpenClaw, configurez les canaux
6. Terminé

---

## Ce dont vous avez besoin (Lume)

- Mac Apple Silicon (M1/M2/M3/M4)
- macOS Sequoia ou ultérieur sur l'hôte
- ~60 GB d'espace disque libre par VM
- ~20 minutes

---

## 1) Installez Lume

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

## 2) Créez la VM macOS

```bash
lume create openclaw --os macos --ipsw latest
```

Cela télécharge macOS et crée la VM. Une fenêtre VNC s'ouvre automatiquement.

Remarque : Le téléchargement peut prendre un certain temps selon votre connexion.

---

## 3) Complétez l'Assistant de configuration

Dans la fenêtre VNC :

1. Sélectionnez la langue et la région
2. Ignorez Apple ID (ou connectez-vous si vous voulez iMessage plus tard)
3. Créez un compte utilisateur (mémorisez le nom d'utilisateur et le mot de passe)
4. Ignorez toutes les fonctionnalités optionnelles

Après la fin de la configuration, activez SSH :

1. Ouvrez Réglages Système → Général → Partage
2. Activez « Connexion à distance »

---

## 4) Obtenez l'adresse IP de la VM

```bash
lume get openclaw
```

Recherchez l'adresse IP (généralement `192.168.64.x`).

---

## 5) SSH dans la VM

```bash
ssh youruser@192.168.64.X
```

Remplacez `youruser` par le compte que vous avez créé, et l'IP par l'IP de votre VM.

---

## 6) Installez OpenClaw

À l'intérieur de la VM :

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

Suivez les invites d'intégration pour configurer votre fournisseur de modèle (Anthropic, OpenAI, etc.).

---

## 7) Configurez les canaux

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

Ensuite, connectez-vous à WhatsApp (scannez le QR) :

```bash
openclaw channels login
```

---

## 8) Exécutez la VM sans interface graphique

Arrêtez la VM et redémarrez-la sans affichage :

```bash
lume stop openclaw
lume run openclaw --no-display
```

La VM s'exécute en arrière-plan. Le daemon d'OpenClaw maintient la gateway en fonctionnement.

Pour vérifier l'état :

```bash
ssh youruser@192.168.64.X "openclaw status"
```

---

## Bonus : intégration iMessage

C'est la fonctionnalité clé de l'exécution sur macOS. Utilisez [BlueBubbles](https://bluebubbles.app) pour ajouter iMessage à OpenClaw.

À l'intérieur de la VM :

1. Téléchargez BlueBubbles depuis bluebubbles.app
2. Connectez-vous avec votre Apple ID
3. Activez l'API Web et définissez un mot de passe
4. Pointez les webhooks BlueBubbles vers votre gateway (exemple : `https://your-gateway-host:3000/bluebubbles-webhook?password=<password>`)

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

Redémarrez la gateway. Maintenant votre agent peut envoyer et recevoir des iMessages.

Détails de configuration complets : [Canal BlueBubbles](/fr/channels/bluebubbles)

---

## Enregistrez une image de référence

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
- Désactivant la mise en veille dans Réglages Système → Économie d'énergie
- Utilisant `caffeinate` si nécessaire

Pour une véritable disponibilité permanente, envisagez un Mac mini dédié ou un petit VPS. Voir [Hébergement VPS](/fr/vps).

---

## Dépannage

| Problème                 | Solution                                                                                    |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| Impossible de SSH dans la VM | Vérifiez que « Connexion à distance » est activée dans les Réglages Système de la VM       |
| L'IP de la VM ne s'affiche pas | Attendez que la VM démarre complètement, exécutez `lume get openclaw` à nouveau             |
| Commande Lume non trouvée | Ajoutez `~/.local/bin` à votre PATH                                                        |
| QR WhatsApp ne scanne pas | Assurez-vous d'être connecté à la VM (pas l'hôte) lors de l'exécution de `openclaw channels login` |

---

## Documentation connexe

- [Hébergement VPS](/fr/vps)
- [Nœuds](/fr/nodes)
- [Gateway distante](/fr/gateway/remote)
- [Canal BlueBubbles](/fr/channels/bluebubbles)
- [Démarrage rapide Lume](https://cua.ai/docs/lume/guide/getting-started/quickstart)
- [Référence CLI Lume](https://cua.ai/docs/lume/reference/cli-reference)
- [Configuration de VM sans surveillance](https://cua.ai/docs/lume/guide/fundamentals/unattended-setup) (avancé)
- [Sandboxing Docker](/fr/install/docker) (approche d'isolation alternative)
