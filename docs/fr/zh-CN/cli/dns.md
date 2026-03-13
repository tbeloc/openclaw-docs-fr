---
read_when:
  - Vous souhaitez implémenter la découverte de périphériques à grande échelle (DNS-SD) via Tailscale + CoreDNS
  - You're setting up split DNS for a custom discovery domain (example: openclaw.internal)
summary: "Référence CLI pour `openclaw dns` (outil auxiliaire de découverte de périphériques à grande échelle)"
title: dns
x-i18n:
  generated_at: "2026-02-03T07:44:52Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: d2011e41982ffb4b71ab98211574529bc1c8b7769ab1838abddd593f42b12380
  source_path: cli/dns.md
  workflow: 15
---

# `openclaw dns`

Outil auxiliaire DNS pour la découverte de périphériques à grande échelle (Tailscale + CoreDNS). Actuellement axé sur macOS + Homebrew CoreDNS.

Contenu connexe :

- Découverte de périphériques Gateway : [Découverte](/gateway/discovery)
- Configuration de découverte de périphériques à grande échelle : [Configuration](/gateway/configuration)

## Configuration

```bash
openclaw dns setup
openclaw dns setup --apply
```
