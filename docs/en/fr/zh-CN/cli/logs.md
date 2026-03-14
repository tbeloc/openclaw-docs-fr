---
read_when:
  - Vous devez suivre à distance les journaux de la passerelle Gateway (sans SSH)
  - Vous avez besoin de lignes de journaux JSON pour le traitement des outils
summary: "`openclaw logs` référence CLI (suivi des journaux de la passerelle Gateway via RPC)"
title: logs
x-i18n:
  generated_at: "2026-02-03T07:44:57Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 911a57f0f3b78412c26312f7bf87a5a26418ab7b74e5e2eb40f16edefb6c6b8e
  source_path: cli/logs.md
  workflow: 15
---

# `openclaw logs`

Suivre les journaux de fichiers de la passerelle Gateway via RPC (disponible en mode distant).

Contenu connexe :

- Aperçu des journaux : [Journalisation](/logging)

## Exemples

```bash
openclaw logs
openclaw logs --follow
openclaw logs --json
openclaw logs --limit 500
```
