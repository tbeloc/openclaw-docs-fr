---
read_when:
  - Vous souhaitez une configuration guidée de Gateway, l'espace de travail, l'authentification, les canaux et les Skills
summary: "Référence CLI pour `openclaw onboard` (assistant de configuration interactif pour les nouveaux utilisateurs)"
title: onboard
x-i18n:
  generated_at: "2026-02-03T07:45:00Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a661049a6983233986a880a68440a3bcc6869ee2c4c6f5e9f3ab8ff973e22f60
  source_path: cli/onboard.md
  workflow: 15
---

# `openclaw onboard`

Assistant de configuration interactif pour les nouveaux utilisateurs (configuration de Gateway locale ou distante).

Contenu connexe :

- Guide de l'assistant : [Intégration](/start/onboarding)

## Exemples

```bash
openclaw onboard
openclaw onboard --flow quickstart
openclaw onboard --flow manual
openclaw onboard --mode remote --remote-url ws://gateway-host:18789
```

Description des flux :

- `quickstart` : invites minimales, génération automatique du jeton Gateway.
- `manual` : invites complètes pour les ports/liaisons/authentification (alias de `advanced`).
- Démarrage le plus rapide pour discuter : `openclaw dashboard` (interface de contrôle, sans configuration de canal requise).
