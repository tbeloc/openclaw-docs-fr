---
read_when:
  - Vous voulez vérifier rapidement l'état de santé de la Gateway en cours d'exécution
summary: "`openclaw health` référence CLI (obtenir le point de terminaison de santé de la Gateway via RPC)"
title: health
x-i18n:
  generated_at: "2026-02-03T07:44:55Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 82a78a5a97123f7a5736699ae8d793592a736f336c5caced9eba06d14d973fd7
  source_path: cli/health.md
  workflow: 15
---

# `openclaw health`

Obtenir l'état de santé de la Gateway en cours d'exécution.

```bash
openclaw health
openclaw health --json
openclaw health --verbose
```

Remarques :

- `--verbose` exécute des sondes en temps réel et affiche le temps écoulé pour chaque compte lorsque plusieurs comptes sont configurés.
- Lorsque plusieurs agents sont configurés, la sortie inclut le stockage de session pour chaque agent.
