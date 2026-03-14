---
read_when:
  - Vous utilisez le mode d'appairage pour les messages privés et devez approuver l'expéditeur
summary: "Référence CLI pour `openclaw pairing` (approuver/lister les demandes d'appairage)"
title: pairing
x-i18n:
  generated_at: "2026-02-03T07:45:02Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: e0bc9707294463c95d13e0deb67d834cfad6a105ab44baf4c25592e5de65ddf5
  source_path: cli/pairing.md
  workflow: 15
---

# `openclaw pairing`

Approuvez ou vérifiez les demandes d'appairage de messages privés (pour les canaux prenant en charge l'appairage).

Contenu connexe :

- Flux d'appairage : [Appairage](/channels/pairing)

## Commandes

```bash
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <code> --notify
```
