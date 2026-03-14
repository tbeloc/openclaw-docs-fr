---
summary: "Référence CLI pour `openclaw health` (endpoint de santé de la passerelle via RPC)"
read_when:
  - Vous voulez vérifier rapidement la santé de la passerelle en cours d'exécution
title: "health"
---

# `openclaw health`

Récupère l'état de santé de la passerelle en cours d'exécution.

```bash
openclaw health
openclaw health --json
openclaw health --verbose
```

Notes :

- `--verbose` exécute les sondes en direct et affiche les délais par compte lorsque plusieurs comptes sont configurés.
- La sortie inclut les magasins de sessions par agent lorsque plusieurs agents sont configurés.
