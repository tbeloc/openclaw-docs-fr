---
summary: "Installer OpenClaw — script d'installation, npm/pnpm, depuis la source, Docker, et plus"
read_when:
  - You need an install method other than the Getting Started quickstart
  - You want to deploy to a cloud platform
  - You need to update, migrate, or uninstall
title: "Installation"
---

# Installation

Vous avez déjà suivi [Getting Started](/start/getting-started) ? Vous êtes prêt — cette page est destinée aux méthodes d'installation alternatives, aux instructions spécifiques à la plateforme et à la maintenance.

## Configuration requise

- **[Node 24 (recommandé)](/install/node)** (Node 22 LTS, actuellement `22.16+`, est toujours supporté pour la compatibilité ; le [script d'installation](#install-methods) installera Node 24 s'il est manquant)
- macOS, Linux ou Windows
- `pnpm` uniquement si vous compilez depuis la source

<Note>
Sur Windows, nous recommandons vivement d'exécuter OpenClaw sous [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).
</Note>

## Méthodes d'installation

<Tip>
Le **script d'installation** est la méthode recommandée pour installer OpenClaw. Il gère la détection de Node, l'installation et l'intégration en une seule étape.
</Tip>

<Warning>
Pour les VPS/hôtes cloud, évitez autant que possible les images marketplace « 1-clic » tierces. Préférez une image de système d'exploitation de base propre (par exemple Ubuntu LTS), puis installez OpenClaw vous-même avec le script d'installation.
</Warning>

<AccordionGroup>
  <Accordion title="Script d'installation" icon="rocket" defaultOpen>
    Télécharge la CLI, l'installe globalement via npm et lance l'assistant d'intégration.

    <Tabs>
      <Tab title="macOS / Linux / WSL2">
        ```bash
        curl -fsSL https://openclaw.ai/install.sh | bash
        ```
      </Tab>
      <Tab title="Windows (PowerShell)">
        ```powershell
        iwr -useb https://openclaw.ai/install.ps1 | iex
        ```
      </Tab>
    </Tabs>

    C'est tout — le script gère la détection de Node, l'installation et l'intégration.

    Pour ignorer l'intégration et installer uniquement le binaire :

    <Tabs>
      <Tab title="macOS / Linux / WSL2">
        ```bash
        curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
        ```
      </Tab>
      <Tab title="Windows (PowerShell)">
        ```powershell
        & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
        ```
      </Tab>
    </Tabs>

    Pour tous les drapeaux, variables d'environnement et options CI/automatisation, voir [Installer internals](/install/installer).

  </Accordion>

  <Accordion title="npm / pnpm" icon="package">
    Si vous gérez déjà Node vous-même, nous recommandons Node 24. OpenClaw supporte toujours Node 22 LTS, actuellement `22.16+`, pour la compatibilité :

    <Tabs>
      <Tab title="npm">
        ```bash
        npm install -g openclaw@latest
        openclaw onboard --install-daemon
        ```

        <Accordion title="Erreurs de compilation sharp ?">
          Si vous avez libvips installé globalement (courant sur macOS via Homebrew) et que `sharp` échoue, forcez les binaires précompilés :

          ```bash
          SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
          ```

          Si vous voyez `sharp: Please add node-gyp to your dependencies`, installez soit les outils de compilation (macOS : Xcode CLT + `npm install -g node-gyp`) soit utilisez la variable d'environnement ci-dessus.
        </Accordion>
      </Tab>
      <Tab title="pnpm">
        ```bash
        pnpm add -g openclaw@latest
        pnpm approve-builds -g        # approve openclaw, node-llama-cpp, sharp, etc.
        openclaw onboard --install-daemon
        ```

        <Note>
        pnpm nécessite une approbation explicite pour les packages avec des scripts de compilation. Après que la première installation affiche l'avertissement « Ignored build scripts », exécutez `pnpm approve-builds -g` et sélectionnez les packages listés.
        </Note>
      </Tab>
    </Tabs>

  </Accordion>

  <Accordion title="Depuis la source" icon="github">
    Pour les contributeurs ou quiconque souhaite exécuter depuis un checkout local.

    <Steps>
      <Step title="Cloner et compiler">
        Clonez le [dépôt OpenClaw](https://github.com/openclaw/openclaw) et compilez :

        ```bash
        git clone https://github.com/openclaw/openclaw.git
        cd openclaw
        pnpm install
        pnpm ui:build
        pnpm build
        ```
      </Step>
      <Step title="Lier la CLI">
        Rendez la commande `openclaw` disponible globalement :

        ```bash
        pnpm link --global
        ```

        Alternativement, ignorez le lien et exécutez les commandes via `pnpm openclaw ...` depuis l'intérieur du dépôt.
      </Step>
      <Step title="Exécuter l'intégration">
        ```bash
        openclaw onboard --install-daemon
        ```
      </Step>
    </Steps>

    Pour des flux de travail de développement plus approfondis, voir [Setup](/start/setup).

  </Accordion>
</AccordionGroup>

## Autres méthodes d'installation

<CardGroup cols={2}>
  <Card title="Docker" href="/install/docker" icon="container">
    Déploiements conteneurisés ou sans interface.
  </Card>
  <Card title="Podman" href="/install/podman" icon="container">
    Conteneur sans root : exécutez `setup-podman.sh` une fois, puis le script de lancement.
  </Card>
  <Card title="Nix" href="/install/nix" icon="snowflake">
    Installation déclarative via Nix.
  </Card>
  <Card title="Ansible" href="/install/ansible" icon="server">
    Provisionnement automatisé de flotte.
  </Card>
  <Card title="Bun" href="/install/bun" icon="zap">
    Utilisation CLI uniquement via le runtime Bun.
  </Card>
</CardGroup>

## Après l'installation

Vérifiez que tout fonctionne :

```bash
openclaw doctor         # check for config issues
openclaw status         # gateway status
openclaw dashboard      # open the browser UI
```

Si vous avez besoin de chemins d'exécution personnalisés, utilisez :

- `OPENCLAW_HOME` pour les chemins internes basés sur le répertoire personnel
- `OPENCLAW_STATE_DIR` pour l'emplacement de l'état mutable
- `OPENCLAW_CONFIG_PATH` pour l'emplacement du fichier de configuration

Voir [Environment vars](/help/environment) pour la précédence et les détails complets.

## Dépannage : `openclaw` introuvable

<Accordion title="Diagnostic et correction du PATH">
  Diagnostic rapide :

```bash
node -v
npm -v
npm prefix -g
echo "$PATH"
```

Si `$(npm prefix -g)/bin` (macOS/Linux) ou `$(npm prefix -g)` (Windows) n'est **pas** dans votre `$PATH`, votre shell ne peut pas trouver les binaires npm globaux (y compris `openclaw`).

Correction — ajoutez-le à votre fichier de démarrage du shell (`~/.zshrc` ou `~/.bashrc`) :

```bash
export PATH="$(npm prefix -g)/bin:$PATH"
```

Sur Windows, ajoutez la sortie de `npm prefix -g` à votre PATH.

Ouvrez ensuite un nouveau terminal (ou `rehash` dans zsh / `hash -r` dans bash).
</Accordion>

## Mise à jour / désinstallation

<CardGroup cols={3}>
  <Card title="Mise à jour" href="/install/updating" icon="refresh-cw">
    Gardez OpenClaw à jour.
  </Card>
  <Card title="Migration" href="/install/migrating" icon="arrow-right">
    Déplacez-vous vers une nouvelle machine.
  </Card>
  <Card title="Désinstallation" href="/install/uninstall" icon="trash-2">
    Supprimez complètement OpenClaw.
  </Card>
</CardGroup>
