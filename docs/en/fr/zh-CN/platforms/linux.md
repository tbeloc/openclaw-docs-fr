---
read_when:
  - Lors de la recherche du statut des applications complémentaires Linux
  - Lors de la planification de la couverture de plateforme ou des contributions
summary: Support Linux + statut des applications complémentaires
title: Applications Linux
x-i18n:
  generated_at: "2026-02-03T07:52:18Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a9bbbcecf2fd522a2f5ac8f3b9068febbc43658465bfb9276bff6c3e946789d2
  source_path: platforms/linux.md
  workflow: 15
---

# Applications Linux

La passerelle Gateway est entièrement supportée sur Linux. **Node est le runtime recommandé**.
Bun n'est pas recommandé pour la passerelle Gateway (bugs avec WhatsApp/Telegram).

Les applications complémentaires natives Linux sont en cours de planification. Si vous souhaitez aider à les construire, les contributions sont bienvenues.

## Chemin rapide pour les débutants (VPS)

1. Installez Node 22+
2. `npm i -g openclaw@latest`
3. `openclaw onboard --install-daemon`
4. Depuis votre ordinateur portable : `ssh -N -L 18789:127.0.0.1:18789 <user>@<host>`
5. Ouvrez `http://127.0.0.1:18789/` et collez votre jeton

Guide VPS étape par étape : [exe.dev](/install/exe-dev)

## Installation

- [Guide de démarrage](/start/getting-started)
- [Installation et mise à jour](/install/updating)
- Processus optionnels : [Bun (expérimental)](/install/bun), [Nix](/install/nix), [Docker](/install/docker)

## Installation du service Gateway (CLI)

Utilisez l'une des méthodes suivantes :

```
openclaw onboard --install-daemon
```

ou :

```
openclaw gateway install
```

ou :

```
openclaw configure
```

Sélectionnez **Gateway service** lorsque vous y êtes invité.

Réparation/Migration :

```
openclaw doctor
```

## Contrôle système (unités utilisateur systemd)

OpenClaw installe par défaut un service systemd **utilisateur**. Pour les serveurs partagés ou résidents, utilisez un service **système**.
Des exemples d'unités complets et des guides se trouvent dans le [Manuel d'exécution de la passerelle Gateway](/gateway).

Configuration minimale :

Créez `~/.config/systemd/user/openclaw-gateway[-<profile>].service` :

```
[Unit]
Description=OpenClaw Gateway (profile: <profile>, v<version>)
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/openclaw gateway --port 18789
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

Activez-le :

```
systemctl --user enable --now openclaw-gateway[-<profile>].service
```
