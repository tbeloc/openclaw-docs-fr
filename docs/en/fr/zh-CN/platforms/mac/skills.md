---
read_when:
  - 更新 macOS Skills 设置 UI
  - 更改 Skills 门控或安装行为
summary: macOS Skills 设置 UI 和基于 Gateway 网关的状态
title: Skills
x-i18n:
  generated_at: "2026-02-03T10:08:09Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: ecd5286bbe49eed89319686c4f7d6da55ef7b0d3952656ba98ef5e769f3fbf79
  source_path: platforms/mac/skills.md
  workflow: 15
---

# Skills (macOS)

Les applications macOS affichent OpenClaw Skills via Gateway ; elles ne les analysent pas localement.

## Sources de données

- `skills.status` (Gateway) retourne tous les Skills ainsi que les qualifications et les exigences manquantes
  (y compris le blocage de la liste blanche pour les Skills intégrés).
- Les exigences proviennent de `metadata.openclaw.requires` dans chaque `SKILL.md`.

## Opérations d'installation

- `metadata.openclaw.install` définit les options d'installation (brew/node/go/uv).
- L'application appelle `skills.install` pour exécuter le programme d'installation sur l'hôte Gateway.
- Lorsque plusieurs programmes d'installation sont fournis, Gateway affiche un seul programme d'installation préféré
  (utilise brew s'il est disponible, sinon utilise le gestionnaire node de `skills.install`, npm par défaut).

## Variables d'environnement/Clés API

- L'application stocke les clés sous `skills.entries.<skillKey>` dans `~/.openclaw/openclaw.json`.
- `skills.update` met à jour `enabled`, `apiKey` et `env`.

## Mode distant

- L'installation + les mises à jour de configuration se produisent sur l'hôte Gateway (pas sur le Mac local).
