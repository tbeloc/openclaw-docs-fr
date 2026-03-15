---
summary: "Référence CLI pour `openclaw health` (endpoint de santé de la passerelle via RPC)"
read_when:
  - You want to quickly check the running Gateway's health
title: "health"
---

# `openclaw health`

Récupérez l'état de santé de la passerelle en cours d'exécution.

```bash
openclaw health
openclaw health --json
openclaw health --verbose
```

Notes :

- `--verbose` exécute des sondes en direct et affiche les délais par compte lorsque plusieurs comptes sont configurés.
- La sortie inclut les magasins de sessions par agent lorsque plusieurs agents sont configurés.
