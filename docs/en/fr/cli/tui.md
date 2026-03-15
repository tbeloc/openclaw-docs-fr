---
summary: "Référence CLI pour `openclaw tui` (interface utilisateur terminal connectée à la Gateway)"
read_when:
  - Vous voulez une interface utilisateur terminal pour la Gateway (compatible à distance)
  - Vous voulez passer url/token/session à partir de scripts
title: "tui"
---

# `openclaw tui`

Ouvrez l'interface utilisateur terminal connectée à la Gateway.

Connexes :

- Guide TUI : [TUI](/web/tui)

Notes :

- `tui` résout les SecretRefs d'authentification de gateway configurés pour l'authentification par token/mot de passe si possible (fournisseurs `env`/`file`/`exec`).
- Lorsqu'il est lancé depuis l'intérieur d'un répertoire d'espace de travail d'agent configuré, TUI sélectionne automatiquement cet agent pour la clé de session par défaut (sauf si `--session` est explicitement `agent:<id>:...`).

## Exemples

```bash
openclaw tui
openclaw tui --url ws://127.0.0.1:18789 --token <token>
openclaw tui --session main --deliver
# when run inside an agent workspace, infers that agent automatically
openclaw tui --session bugfix
```
