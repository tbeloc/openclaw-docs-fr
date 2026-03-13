---
summary: "Référence CLI pour `openclaw uninstall` (supprimer le service de passerelle + données locales)"
read_when:
  - Vous souhaitez supprimer le service de passerelle et/ou l'état local
  - Vous souhaitez d'abord faire un essai à blanc
title: "uninstall"
---

# `openclaw uninstall`

Désinstaller le service de passerelle + données locales (CLI reste).

```bash
openclaw backup create
openclaw uninstall
openclaw uninstall --all --yes
openclaw uninstall --dry-run
```

Exécutez d'abord `openclaw backup create` si vous souhaitez un instantané restaurable avant de supprimer l'état ou les espaces de travail.
