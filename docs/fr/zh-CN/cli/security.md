---
read_when:
  - Vous souhaitez exécuter un audit de sécurité rapide sur la configuration/l'état
  - Vous souhaitez appliquer des recommandations de sécurité "correctives" (chmod, resserrer les valeurs par défaut)
summary: "Référence CLI pour `openclaw security` (audit et correction des failles de sécurité courantes)"
title: security
x-i18n:
  generated_at: "2026-02-03T07:45:13Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 19705b0fff848fa6f302b4ed09b7660c64e09048dba517c7f6a833d2db40bebf
  source_path: cli/security.md
  workflow: 15
---

# `openclaw security`

Outil de sécurité (audit + correction optionnelle).

Voir aussi :

- Guide de sécurité : [Sécurité](/gateway/security)

## Audit

```bash
openclaw security audit
openclaw security audit --deep
openclaw security audit --fix
```

L'audit émet un avertissement lorsque plusieurs expéditeurs de messages privés partagent une session principale, et recommande d'utiliser `session.dmScope="per-channel-peer"` pour les boîtes de réception partagées (ou `per-account-channel-peer` pour les canaux multi-comptes).
Il émet également un avertissement lors de l'utilisation de petits modèles (`<=300B`) sans isolation sandbox activée mais avec des outils web/navigateur activés.
