---
summary: "Référence CLI pour `openclaw completion` (générer/installer les scripts de complétion shell)"
read_when:
  - Vous voulez des complétions shell pour zsh/bash/fish/PowerShell
  - Vous devez mettre en cache les scripts de complétion sous l'état OpenClaw
title: "completion"
---

# `openclaw completion`

Générez les scripts de complétion shell et installez-les optionnellement dans votre profil shell.

## Utilisation

```bash
openclaw completion
openclaw completion --shell zsh
openclaw completion --install
openclaw completion --shell fish --install
openclaw completion --write-state
openclaw completion --shell bash --write-state
```

## Options

- `-s, --shell <shell>`: cible shell (`zsh`, `bash`, `powershell`, `fish`; par défaut: `zsh`)
- `-i, --install`: installer la complétion en ajoutant une ligne source à votre profil shell
- `--write-state`: écrire le(s) script(s) de complétion dans `$OPENCLAW_STATE_DIR/completions` sans imprimer sur stdout
- `-y, --yes`: ignorer les invites de confirmation d'installation

## Notes

- `--install` écrit un petit bloc "OpenClaw Completion" dans votre profil shell et le pointe vers le script mis en cache.
- Sans `--install` ou `--write-state`, la commande imprime le script sur stdout.
- La génération de complétion charge avidement les arbres de commandes afin que les sous-commandes imbriquées soient incluses.
