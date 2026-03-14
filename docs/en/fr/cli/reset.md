```markdown
---
summary: "Référence CLI pour `openclaw reset` (réinitialiser l'état/la configuration locale)"
read_when:
  - Vous voulez effacer l'état local tout en gardant la CLI installée
  - Vous voulez un aperçu de ce qui serait supprimé
title: "reset"
---

# `openclaw reset`

Réinitialiser la configuration/l'état local (garde la CLI installée).

```bash
openclaw backup create
openclaw reset
openclaw reset --dry-run
openclaw reset --scope config+creds+sessions --yes --non-interactive
```

Exécutez `openclaw backup create` d'abord si vous voulez un snapshot restaurable avant de supprimer l'état local.
```
