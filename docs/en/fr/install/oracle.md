---
summary: "Héberger OpenClaw sur le niveau ARM Always Free d'Oracle Cloud"
read_when:
  - Setting up OpenClaw on Oracle Cloud
  - Looking for free VPS hosting for OpenClaw
  - Want 24/7 OpenClaw on a small server
title: "Oracle Cloud"
---

# Oracle Cloud

Exécutez une passerelle OpenClaw persistante sur le niveau ARM **Always Free** d'Oracle Cloud (jusqu'à 4 OCPU, 24 GB RAM, 200 GB de stockage) sans frais.

## Prérequis

- Compte Oracle Cloud ([inscription](https://www.oracle.com/cloud/free/)) -- voir [guide d'inscription communautaire](https://gist.github.com/rssnyder/51e3cfedd730e7dd5f4a816143b25dbd) si vous rencontrez des problèmes
- Compte Tailscale (gratuit sur [tailscale.com](https://tailscale.com))
- Une paire de clés SSH
- Environ 30 minutes

## Configuration

<Steps>
  <Step title="Créer une instance OCI">
    1. Connectez-vous à la [console Oracle Cloud](https://cloud.oracle.com/).
    2. Accédez à **Compute > Instances > Create Instance**.
    3. Configurez :
       - **Name:** `openclaw`
       - **Image:** Ubuntu 24.04 (aarch64)
       - **Shape:** `VM.Standard.A1.Flex` (Ampere ARM)
       - **OCPUs:** 2 (ou jusqu'à 4)
       - **Memory:** 12 GB (ou jusqu'à 24 GB)
       - **Boot volume:** 50 GB (jusqu'à 200 GB gratuits)
       - **SSH key:** Ajoutez votre clé publique
    4. Cliquez sur **Create** et notez l'adresse IP publique.

    <Tip>
    Si la création d'instance échoue avec "Out of capacity", essayez un domaine de disponibilité différent ou réessayez plus tard. La capacité du niveau gratuit est limitée.
    </Tip>

  </Step>

  <Step title="Se connecter et mettre à jour le système">
    ```bash
    ssh ubuntu@YOUR_PUBLIC_IP

    sudo apt update && sudo apt upgrade -y
    sudo apt install -y build-essential
    ```

    `build-essential` est requis pour la compilation ARM de certaines dépendances.

  </Step>

  <Step title="Configurer l'utilisateur et le nom d'hôte">
    ```bash
    sudo hostnamectl set-hostname openclaw
    sudo passwd ubuntu
    sudo loginctl enable-linger ubuntu
    ```

    L'activation de linger maintient les services utilisateur en cours d'exécution après la déconnexion.

  </Step>

  <Step title="Installer Tailscale">
    ```bash
    curl -fsSL https://tailscale.com/install.sh | sh
    sudo tailscale up --ssh --hostname=openclaw
    ```

    À partir de maintenant, connectez-vous via Tailscale : `ssh ubuntu@openclaw`.

  </Step>

  <Step title="Installer OpenClaw">
    ```bash
    curl -fsSL https://openclaw.ai/install.sh | bash
    source ~/.bashrc
    ```

    Lorsque vous êtes invité "How do you want to hatch your bot?", sélectionnez **Do this later**.

  </Step>

  <Step title="Configurer la passerelle">
    Utilisez l'authentification par jeton avec Tailscale Serve pour un accès à distance sécurisé.

    ```bash
    openclaw config set gateway.bind loopback
    openclaw config set gateway.auth.mode token
    openclaw doctor --generate-gateway-token
    openclaw config set gateway.tailscale.mode serve
    openclaw config set gateway.trustedProxies '["127.0.0.1"]'

    systemctl --user restart openclaw-gateway
    ```

  </Step>

  <Step title="Verrouiller la sécurité du VCN">
    Bloquez tout le trafic sauf Tailscale à la périphérie du réseau :

    1. Allez à **Networking > Virtual Cloud Networks** dans la console OCI.
    2. Cliquez sur votre VCN, puis **Security Lists > Default Security List**.
    3. **Supprimez** toutes les règles d'entrée sauf `0.0.0.0/0 UDP 41641` (Tailscale).
    4. Conservez les règles de sortie par défaut (autoriser tout le trafic sortant).

    Cela bloque SSH sur le port 22, HTTP, HTTPS et tout le reste à la périphérie du réseau. Vous ne pouvez vous connecter que via Tailscale à partir de ce moment.

  </Step>

  <Step title="Vérifier">
    ```bash
    openclaw --version
    systemctl --user status openclaw-gateway
    tailscale serve status
    curl http://localhost:18789
    ```

    Accédez à l'interface de contrôle depuis n'importe quel appareil de votre tailnet :

    ```
    https://openclaw.<tailnet-name>.ts.net/
    ```

    Remplacez `<tailnet-name>` par le nom de votre tailnet (visible dans `tailscale status`).

  </Step>
</Steps>

## Secours : tunnel SSH

Si Tailscale Serve ne fonctionne pas, utilisez un tunnel SSH depuis votre machine locale :

```bash
ssh -L 18789:127.0.0.1:18789 ubuntu@openclaw
```

Ouvrez ensuite `http://localhost:18789`.

## Dépannage

**La création d'instance échoue ("Out of capacity")** -- Les instances ARM du niveau gratuit sont populaires. Essayez un domaine de disponibilité différent ou réessayez pendant les heures creuses.

**Tailscale ne se connecte pas** -- Exécutez `sudo tailscale up --ssh --hostname=openclaw --reset` pour vous réauthentifier.

**La passerelle ne démarre pas** -- Exécutez `openclaw doctor --non-interactive` et vérifiez les journaux avec `journalctl --user -u openclaw-gateway -n 50`.

**Problèmes de binaires ARM** -- La plupart des packages npm fonctionnent sur ARM64. Pour les binaires natifs, recherchez les versions `linux-arm64` ou `aarch64`. Vérifiez l'architecture avec `uname -m`.

## Étapes suivantes

- [Channels](/fr/channels) -- connectez Telegram, WhatsApp, Discord, et plus
- [Gateway configuration](/fr/gateway/configuration) -- toutes les options de configuration
- [Updating](/fr/install/updating) -- gardez OpenClaw à jour
