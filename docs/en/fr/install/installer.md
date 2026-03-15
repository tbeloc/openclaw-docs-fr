---
summary: "Comment fonctionnent les scripts d'installation (install.sh, install-cli.sh, install.ps1), les drapeaux et l'automatisation"
read_when:
  - You want to understand `openclaw.ai/install.sh`
  - You want to automate installs (CI / headless)
  - You want to install from a GitHub checkout
title: "Installer Internals"
---

# Installer internals

OpenClaw est livré avec trois scripts d'installation, servis depuis `openclaw.ai`.

| Script                             | Plateforme           | Ce qu'il fait                                                                                 |
| ---------------------------------- | -------------------- | -------------------------------------------------------------------------------------------- |
| [`install.sh`](#installsh)         | macOS / Linux / WSL  | Installe Node si nécessaire, installe OpenClaw via npm (par défaut) ou git, et peut exécuter l'intégration. |
| [`install-cli.sh`](#install-clish) | macOS / Linux / WSL  | Installe Node + OpenClaw dans un préfixe local (`~/.openclaw`). Aucun accès root requis.              |
| [`install.ps1`](#installps1)       | Windows (PowerShell) | Installe Node si nécessaire, installe OpenClaw via npm (par défaut) ou git, et peut exécuter l'intégration. |

## Commandes rapides

<Tabs>
  <Tab title="install.sh">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
    ```

    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --help
    ```

  </Tab>
  <Tab title="install-cli.sh">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash
    ```

    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --help
    ```

  </Tab>
  <Tab title="install.ps1">
    ```powershell
    iwr -useb https://openclaw.ai/install.ps1 | iex
    ```

    ```powershell
    & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -Tag beta -NoOnboard -DryRun
    ```

  </Tab>
</Tabs>

<Note>
Si l'installation réussit mais que `openclaw` n'est pas trouvé dans un nouveau terminal, consultez [Dépannage Node.js](/install/node#troubleshooting).
</Note>

---

## install.sh

<Tip>
Recommandé pour la plupart des installations interactives sur macOS/Linux/WSL.
</Tip>

### Flux (install.sh)

<Steps>
  <Step title="Détecter le système d'exploitation">
    Supporte macOS et Linux (y compris WSL). Si macOS est détecté, installe Homebrew s'il est manquant.
  </Step>
  <Step title="Assurer Node.js 24 par défaut">
    Vérifie la version de Node et installe Node 24 si nécessaire (Homebrew sur macOS, scripts de configuration NodeSource sur Linux apt/dnf/yum). OpenClaw supporte toujours Node 22 LTS, actuellement `22.16+`, pour la compatibilité.
  </Step>
  <Step title="Assurer Git">
    Installe Git s'il est manquant.
  </Step>
  <Step title="Installer OpenClaw">
    - Méthode `npm` (par défaut) : installation npm globale
    - Méthode `git` : cloner/mettre à jour le dépôt, installer les dépendances avec pnpm, construire, puis installer le wrapper à `~/.local/bin/openclaw`
  </Step>
  <Step title="Tâches post-installation">
    - Exécute `openclaw doctor --non-interactive` sur les mises à niveau et les installations git (meilleur effort)
    - Tente l'intégration si approprié (TTY disponible, intégration non désactivée, et vérifications de bootstrap/config réussies)
    - Définit par défaut `SHARP_IGNORE_GLOBAL_LIBVIPS=1`
  </Step>
</Steps>

### Détection de checkout source

Si exécuté dans un checkout OpenClaw (`package.json` + `pnpm-workspace.yaml`), le script propose :

- utiliser le checkout (`git`), ou
- utiliser l'installation globale (`npm`)

Si aucun TTY n'est disponible et aucune méthode d'installation n'est définie, il utilise par défaut `npm` et avertit.

Le script se termine avec le code `2` pour une sélection de méthode invalide ou des valeurs `--install-method` invalides.

### Exemples (install.sh)

<Tabs>
  <Tab title="Par défaut">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
    ```
  </Tab>
  <Tab title="Ignorer l'intégration">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-onboard
    ```
  </Tab>
  <Tab title="Installation Git">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git
    ```
  </Tab>
  <Tab title="Exécution à vide">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --dry-run
    ```
  </Tab>
</Tabs>

<AccordionGroup>
  <Accordion title="Référence des drapeaux">

| Drapeau                         | Description                                                |
| ------------------------------- | ---------------------------------------------------------- |
| `--install-method npm\|git`     | Choisir la méthode d'installation (par défaut : `npm`). Alias : `--method`  |
| `--npm`                         | Raccourci pour la méthode npm                                    |
| `--git`                         | Raccourci pour la méthode git. Alias : `--github`                 |
| `--version <version\|dist-tag>` | Version npm ou dist-tag (par défaut : `latest`)                |
| `--beta`                        | Utiliser le dist-tag beta s'il est disponible, sinon revenir à `latest`  |
| `--git-dir <path>`              | Répertoire de checkout (par défaut : `~/openclaw`). Alias : `--dir` |
| `--no-git-update`               | Ignorer `git pull` pour le checkout existant                      |
| `--no-prompt`                   | Désactiver les invites                                            |
| `--no-onboard`                  | Ignorer l'intégration                                            |
| `--onboard`                     | Activer l'intégration                                          |
| `--dry-run`                     | Afficher les actions sans appliquer les modifications                     |
| `--verbose`                     | Activer la sortie de débogage (`set -x`, journaux au niveau notice npm)      |
| `--help`                        | Afficher l'utilisation (`-h`)                                          |

  </Accordion>

  <Accordion title="Référence des variables d'environnement">

| Variable                                    | Description                                   |
| ------------------------------------------- | --------------------------------------------- |
| `OPENCLAW_INSTALL_METHOD=git\|npm`          | Méthode d'installation                                |
| `OPENCLAW_VERSION=latest\|next\|<semver>`   | Version npm ou dist-tag                       |
| `OPENCLAW_BETA=0\|1`                        | Utiliser beta s'il est disponible                         |
| `OPENCLAW_GIT_DIR=<path>`                   | Répertoire de checkout                            |
| `OPENCLAW_GIT_UPDATE=0\|1`                  | Basculer les mises à jour git                            |
| `OPENCLAW_NO_PROMPT=1`                      | Désactiver les invites                               |
| `OPENCLAW_NO_ONBOARD=1`                     | Ignorer l'intégration                               |
| `OPENCLAW_DRY_RUN=1`                        | Mode exécution à vide                                  |
| `OPENCLAW_VERBOSE=1`                        | Mode débogage                                    |
| `OPENCLAW_NPM_LOGLEVEL=error\|warn\|notice` | Niveau de journalisation npm                                 |
| `SHARP_IGNORE_GLOBAL_LIBVIPS=0\|1`          | Contrôler le comportement sharp/libvips (par défaut : `1`) |

  </Accordion>
</AccordionGroup>

---

## install-cli.sh

<Info>
Conçu pour les environnements où vous voulez tout sous un préfixe local (par défaut `~/.openclaw`) et aucune dépendance système Node.
</Info>

### Flux (install-cli.sh)

<Steps>
  <Step title="Installer le runtime Node local">
    Télécharge une archive Node supportée épinglée (actuellement par défaut `22.22.0`) vers `<prefix>/tools/node-v<version>` et vérifie SHA-256.
  </Step>
  <Step title="Assurer Git">
    Si Git est manquant, tente l'installation via apt/dnf/yum sur Linux ou Homebrew sur macOS.
  </Step>
  <Step title="Installer OpenClaw sous le préfixe">
    Installe avec npm en utilisant `--prefix <prefix>`, puis écrit le wrapper à `<prefix>/bin/openclaw`.
  </Step>
</Steps>

### Exemples (install-cli.sh)

<Tabs>
  <Tab title="Par défaut">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash
    ```
  </Tab>
  <Tab title="Préfixe personnalisé + version">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --prefix /opt/openclaw --version latest
    ```
  </Tab>
  <Tab title="Sortie JSON d'automatisation">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw
    ```
  </Tab>
  <Tab title="Exécuter l'intégration">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --onboard
    ```
  </Tab>
</Tabs>

<AccordionGroup>
  <Accordion title="Référence des drapeaux">

| Drapeau                | Description                                                                     |
| ---------------------- | ------------------------------------------------------------------------------- |
| `--prefix <path>`      | Préfixe d'installation (par défaut : `~/.openclaw`)                                         |
| `--version <ver>`      | Version OpenClaw ou dist-tag (par défaut : `latest`)                                |
| `--node-version <ver>` | Version Node (par défaut : `22.22.0`)                                               |
| `--json`               | Émettre des événements NDJSON                                                              |
| `--onboard`            | Exécuter `openclaw onboard` après l'installation                                            |
| `--no-onboard`         | Ignorer l'intégration (par défaut)                                                       |
| `--set-npm-prefix`     | Sur Linux, forcer le préfixe npm à `~/.npm-global` si le préfixe actuel n'est pas accessible en écriture |
| `--help`               | Afficher l'utilisation (`-h`)                                                               |

  </Accordion>

  <Accordion title="Référence des variables d'environnement">

| Variable                                    | Description                                                                       |
| ------------------------------------------- | --------------------------------------------------------------------------------- |
| `OPENCLAW_PREFIX=<path>`                    | Préfixe d'installation                                                                    |
| `OPENCLAW_VERSION=<ver>`                    | Version OpenClaw ou dist-tag                                                      |
| `OPENCLAW_NODE_VERSION=<ver>`               | Version Node                                                                      |
| `OPENCLAW_NO_ONBOARD=1`                     | Ignorer l'intégration                                                                   |
| `OPENCLAW_NPM_LOGLEVEL=error\|warn\|notice` | Niveau de journalisation npm                                                                     |
| `OPENCLAW_GIT_DIR=<path>`                   | Chemin de recherche de nettoyage hérité (utilisé lors de la suppression de l'ancien checkout du sous-module `Peekaboo`) |
| `SHARP_IGNORE_GLOBAL_LIBVIPS=0\|1`          | Contrôler le comportement sharp/libvips (par défaut : `1`)                                     |

  </Accordion>
</AccordionGroup>

---

## install.ps1

### Flux (install.ps1)

<Steps>
  <Step title="Assurer PowerShell + environnement Windows">
    Nécessite PowerShell 5+.
  </Step>
  <Step title="Assurer Node.js 24 par défaut">
    S'il est manquant, tente une installation via winget, puis Chocolatey, puis Scoop. Node 22 LTS, actuellement `22.16+`, reste supporté pour la compatibilité.
  </Step>
  <Step title="Installer OpenClaw">
    - Méthode `npm` (par défaut) : installation npm globale en utilisant le `-Tag` sélectionné
    - Méthode `git` : cloner/mettre à jour le dépôt, installer/compiler avec pnpm, et installer le wrapper à `%USERPROFILE%\.local\bin\openclaw.cmd`
  </Step>
  <Step title="Tâches post-installation">
    Ajoute le répertoire bin nécessaire au PATH utilisateur si possible, puis exécute `openclaw doctor --non-interactive` lors des mises à niveau et installations git (meilleur effort).
  </Step>
</Steps>

### Exemples (install.ps1)

<Tabs>
  <Tab title="Par défaut">
    ```powershell
    iwr -useb https://openclaw.ai/install.ps1 | iex
    ```
  </Tab>
  <Tab title="Installation git">
    ```powershell
    & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git
    ```
  </Tab>
  <Tab title="Répertoire git personnalisé">
    ```powershell
    & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git -GitDir "C:\openclaw"
    ```
  </Tab>
  <Tab title="Exécution à blanc">
    ```powershell
    & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -DryRun
    ```
  </Tab>
  <Tab title="Trace de débogage">
    ```powershell
    # install.ps1 n'a pas encore de flag -Verbose dédié.
    Set-PSDebug -Trace 1
    & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
    Set-PSDebug -Trace 0
    ```
  </Tab>
</Tabs>

<AccordionGroup>
  <Accordion title="Référence des flags">

| Flag                      | Description                                            |
| ------------------------- | ------------------------------------------------------ |
| `-InstallMethod npm\|git` | Méthode d'installation (par défaut : `npm`)            |
| `-Tag <tag>`              | npm dist-tag (par défaut : `latest`)                   |
| `-GitDir <path>`          | Répertoire de checkout (par défaut : `%USERPROFILE%\openclaw`) |
| `-NoOnboard`              | Ignorer l'onboarding                                   |
| `-NoGitUpdate`            | Ignorer `git pull`                                     |
| `-DryRun`                 | Afficher les actions uniquement                        |

  </Accordion>

  <Accordion title="Référence des variables d'environnement">

| Variable                           | Description        |
| ---------------------------------- | ------------------ |
| `OPENCLAW_INSTALL_METHOD=git\|npm` | Méthode d'installation |
| `OPENCLAW_GIT_DIR=<path>`          | Répertoire de checkout |
| `OPENCLAW_NO_ONBOARD=1`            | Ignorer l'onboarding |
| `OPENCLAW_GIT_UPDATE=0`            | Désactiver git pull |
| `OPENCLAW_DRY_RUN=1`               | Mode exécution à blanc |

  </Accordion>
</AccordionGroup>

<Note>
Si `-InstallMethod git` est utilisé et que Git est manquant, le script se termine et affiche le lien Git for Windows.
</Note>

---

## CI et automatisation

Utilisez les flags/variables d'environnement non-interactifs pour des exécutions prévisibles.

<Tabs>
  <Tab title="install.sh (npm non-interactif)">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-prompt --no-onboard
    ```
  </Tab>
  <Tab title="install.sh (git non-interactif)">
    ```bash
    OPENCLAW_INSTALL_METHOD=git OPENCLAW_NO_PROMPT=1 \
      curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
    ```
  </Tab>
  <Tab title="install-cli.sh (JSON)">
    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw
    ```
  </Tab>
  <Tab title="install.ps1 (ignorer l'onboarding)">
    ```powershell
    & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
    ```
  </Tab>
</Tabs>

---

## Dépannage

<AccordionGroup>
  <Accordion title="Pourquoi Git est-il requis ?">
    Git est requis pour la méthode d'installation `git`. Pour les installations `npm`, Git est toujours vérifié/installé pour éviter les défaillances `spawn git ENOENT` lorsque les dépendances utilisent des URLs git.
  </Accordion>

  <Accordion title="Pourquoi npm rencontre-t-il EACCES sur Linux ?">
    Certaines configurations Linux pointent le préfixe global npm vers des chemins appartenant à root. `install.sh` peut basculer le préfixe vers `~/.npm-global` et ajouter les exports PATH aux fichiers rc du shell (lorsque ces fichiers existent).
  </Accordion>

  <Accordion title="Problèmes sharp/libvips">
    Les scripts définissent par défaut `SHARP_IGNORE_GLOBAL_LIBVIPS=1` pour éviter que sharp ne compile contre la libvips système. Pour remplacer :

    ```bash
    SHARP_IGNORE_GLOBAL_LIBVIPS=0 curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
    ```

  </Accordion>

  <Accordion title='Windows : "npm error spawn git / ENOENT"'>
    Installez Git for Windows, rouvrez PowerShell, réexécutez l'installateur.
  </Accordion>

  <Accordion title='Windows : "openclaw is not recognized"'>
    Exécutez `npm config get prefix` et ajoutez ce répertoire à votre PATH utilisateur (pas de suffixe `\bin` nécessaire sur Windows), puis rouvrez PowerShell.
  </Accordion>

  <Accordion title="Windows : comment obtenir une sortie d'installateur détaillée">
    `install.ps1` n'expose pas actuellement un switch `-Verbose`.
    Utilisez le traçage PowerShell pour les diagnostics au niveau du script :

    ```powershell
    Set-PSDebug -Trace 1
    & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
    Set-PSDebug -Trace 0
    ```

  </Accordion>

  <Accordion title="openclaw introuvable après l'installation">
    Généralement un problème de PATH. Voir [Dépannage Node.js](/install/node#troubleshooting).
  </Accordion>
</AccordionGroup>
