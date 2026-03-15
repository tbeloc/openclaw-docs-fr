---
summary: "Référence CLI pour `openclaw pairing` (approuver/lister les demandes d'appairage)"
read_when:
  - You're using pairing-mode DMs and need to approve senders
title: "pairing"
---

# `openclaw pairing`

Approuver ou inspecter les demandes d'appairage DM (pour les canaux qui supportent l'appairage).

Connexes :

- Flux d'appairage : [Pairing](/fr/channels/pairing)

## Commandes

```bash
openclaw pairing list telegram
openclaw pairing list --channel telegram --account work
openclaw pairing list telegram --json

openclaw pairing approve telegram <code>
openclaw pairing approve --channel telegram --account work <code> --notify
```

## Notes

- Entrée de canal : passez-la positivement (`pairing list telegram`) ou avec `--channel <channel>`.
- `pairing list` supporte `--account <accountId>` pour les canaux multi-comptes.
- `pairing approve` supporte `--account <accountId>` et `--notify`.
- Si un seul canal compatible avec l'appairage est configuré, `pairing approve <code>` est autorisé.
