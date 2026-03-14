---
read_when:
  - 手动引导工作区
summary: Modèle d'espace de travail pour TOOLS.md
x-i18n:
  generated_at: "2026-02-01T21:38:05Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 3ed08cd537620749c40ab363f5db40a058d8ddab4d0192a1f071edbfcf37a739
  source_path: reference/templates/TOOLS.md
  workflow: 15
---

# TOOLS.md - Notes locales

Les Skills définissent *comment* les outils fonctionnent. Ce fichier sert à documenter *vos* informations spécifiques — le contenu qui est unique à votre environnement.

## Ce qu'il faut ajouter

Par exemple :

- Noms et emplacements des caméras
- Hôtes SSH et alias
- Voix préférées pour la synthèse vocale
- Noms des haut-parleurs/pièces
- Surnoms des appareils
- Tout contenu spécifique à votre environnement

## Exemple

```markdown
### Cameras

- living-room → 主区域，180° 広角
- front-door → 入口，运动触发

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova"（温暖，略带英式口音）
- Default speaker: Kitchen HomePod
```

## Pourquoi les séparer ?

Les Skills sont partagés. Votre configuration vous appartient. Les séparer signifie que vous pouvez mettre à jour les Skills sans perdre vos notes, et partager les Skills sans révéler vos informations d'infrastructure.

---

Ajoutez tout ce qui vous est utile. C'est votre aide-mémoire.
