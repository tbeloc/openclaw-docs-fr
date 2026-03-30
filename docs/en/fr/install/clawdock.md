---
summary: "Assistants shell pour ClawDock pour les installations OpenClaw basées sur Docker"
read_when:
  - Vous exécutez OpenClaw avec Docker souvent et voulez des commandes plus courtes au quotidien
  - Vous voulez une couche d'assistance pour le tableau de bord, les journaux, la configuration des jetons et les flux d'appairage
title: "ClawDock"
---

# ClawDock

ClawDock est une petite couche d'assistance shell pour les installations OpenClaw basées sur Docker.

Elle vous donne des commandes courtes comme `clawdock-start`, `clawdock-dashboard` et `clawdock-fix-token` au lieu d'invocations `docker compose ...` plus longues.

Si vous n'avez pas encore configuré Docker, commencez par [Docker](/fr/install/docker).

## Installation

Utilisez le chemin d'assistance canonique :

```bash
mkdir -p ~/.clawdock && curl -sL https://raw.githubusercontent.com/openclaw/openclaw/main/scripts/clawdock/clawdock-helpers.sh -o ~/.clawdock/clawdock-helpers.sh
echo 'source ~/.clawdock/clawdock-helpers.sh' >> ~/.zshrc && source ~/.zshrc
```

Si vous avez précédemment installé ClawDock à partir de `scripts/shell-helpers/clawdock-helpers.sh`, réinstallez à partir du nouveau chemin `scripts/clawdock/clawdock-helpers.sh`. L'ancien chemin GitHub brut a été supprimé.

## Ce que vous obtenez

### Opérations de base

| Commande           | Description            |
| ------------------ | ---------------------- |
| `clawdock-start`   | Démarrer la passerelle |
| `clawdock-stop`    | Arrêter la passerelle  |
| `clawdock-restart` | Redémarrer la passerelle |
| `clawdock-status`  | Vérifier l'état des conteneurs |
| `clawdock-logs`    | Suivre les journaux de la passerelle |

### Accès aux conteneurs

| Commande                  | Description                                   |
| ------------------------- | --------------------------------------------- |
| `clawdock-shell`          | Ouvrir un shell à l'intérieur du conteneur de passerelle |
| `clawdock-cli <command>`  | Exécuter des commandes CLI OpenClaw dans Docker |
| `clawdock-exec <command>` | Exécuter une commande arbitraire dans le conteneur |

### Interface Web et appairage

| Commande                | Description                  |
| ----------------------- | ---------------------------- |
| `clawdock-dashboard`    | Ouvrir l'URL de l'interface de contrôle |
| `clawdock-devices`      | Lister les appairages d'appareils en attente |
| `clawdock-approve <id>` | Approuver une demande d'appairage |

### Configuration et maintenance

| Commande             | Description                                      |
| -------------------- | ------------------------------------------------ |
| `clawdock-fix-token` | Configurer le jeton de passerelle à l'intérieur du conteneur |
| `clawdock-update`    | Extraire, reconstruire et redémarrer |
| `clawdock-rebuild`   | Reconstruire uniquement l'image Docker |
| `clawdock-clean`     | Supprimer les conteneurs et les volumes |

### Utilitaires

| Commande               | Description                             |
| ---------------------- | --------------------------------------- |
| `clawdock-health`      | Exécuter une vérification de santé de la passerelle |
| `clawdock-token`       | Afficher le jeton de passerelle |
| `clawdock-cd`          | Accéder au répertoire du projet OpenClaw |
| `clawdock-config`      | Ouvrir `~/.openclaw` |
| `clawdock-show-config` | Afficher les fichiers de configuration avec les valeurs masquées |
| `clawdock-workspace`   | Ouvrir le répertoire de l'espace de travail |

## Flux de première utilisation

```bash
clawdock-start
clawdock-fix-token
clawdock-dashboard
```

Si le navigateur indique que l'appairage est requis :

```bash
clawdock-devices
clawdock-approve <request-id>
```

## Configuration et secrets

ClawDock fonctionne avec la même division de configuration Docker décrite dans [Docker](/fr/install/docker) :

- `<project>/.env` pour les valeurs spécifiques à Docker comme le nom de l'image, les ports et le jeton de passerelle
- `~/.openclaw/.env` pour les clés de fournisseur et les jetons de bot
- `~/.openclaw/openclaw.json` pour la configuration du comportement

Utilisez `clawdock-show-config` lorsque vous voulez inspecter rapidement ces fichiers. Elle masque les valeurs `.env` dans sa sortie imprimée.

## Pages connexes

- [Docker](/fr/install/docker)
- [Docker VM Runtime](/fr/install/docker-vm-runtime)
- [Mise à jour](/fr/install/updating)
