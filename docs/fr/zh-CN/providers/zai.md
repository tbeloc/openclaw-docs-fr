---
read_when:
  - Vous souhaitez utiliser les modèles Z.AI / GLM dans OpenClaw
  - Vous avez besoin d'une simple configuration ZAI_API_KEY
summary: Utiliser Zhipu AI (modèles GLM) dans OpenClaw
title: Z.AI
x-i18n:
  generated_at: "2026-02-01T21:36:13Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 2c24bbad86cf86c38675a58e22f9e1b494f78a18fdc3051c1be80d2d9a800711
  source_path: providers/zai.md
  workflow: 15
---

# Z.AI

Z.AI est une plateforme API pour les modèles **GLM**. Elle fournit une API REST pour GLM et utilise une clé API pour l'authentification. Veuillez créer votre clé API dans la console Z.AI. OpenClaw utilise Z.AI via le fournisseur `zai` associé à votre clé API Z.AI.

## Configuration CLI

```bash
openclaw onboard --auth-choice zai-api-key
# ou non-interactif
openclaw onboard --zai-api-key "$ZAI_API_KEY"
```

## Extrait de configuration

```json5
{
  env: { ZAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "zai/glm-4.7" } } },
}
```

## Remarques

- Les modèles GLM sont fournis sous la forme `zai/<model>` (par exemple : `zai/glm-4.7`).
- Consultez [/providers/glm](/providers/glm) pour un aperçu de la famille de modèles.
- Z.AI utilise l'authentification Bearer avec votre clé API.
