---
summary: "Référence CLI pour `openclaw logs` (afficher les logs de la passerelle via RPC)"
read_when:
  - Vous devez afficher les logs de la passerelle à distance (sans SSH)
  - Vous voulez des lignes de log JSON pour les outils
title: "logs"
---

# `openclaw logs`

Afficher les logs de fichier de la passerelle via RPC (fonctionne en mode distant).

Connexes :

- Aperçu de la journalisation : [Logging](/logging)

## Exemples

```bash
openclaw logs
openclaw logs --follow
openclaw logs --json
openclaw logs --limit 500
openclaw logs --local-time
openclaw logs --follow --local-time
```

Utilisez `--local-time` pour afficher les horodatages dans votre fuseau horaire local.
