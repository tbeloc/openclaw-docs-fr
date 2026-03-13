---
read_when:
  - Vous souhaitez utiliser les modèles GLM dans OpenClaw
  - Vous devez comprendre les conventions de nommage des modèles et les méthodes de configuration
summary: Aperçu de la famille de modèles GLM + Comment utiliser dans OpenClaw
title: Modèles GLM
x-i18n:
  generated_at: "2026-02-01T21:34:53Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 2d7b457f033f26f28c230a9cd2310151f825fc52c3ee4fb814d08fd2d022d041
  source_path: providers/glm.md
  workflow: 15
---

# Modèles GLM

GLM est une **famille de modèles** (et non une entreprise), fournie via la plateforme Z.AI. Dans OpenClaw, les modèles GLM sont accessibles via le fournisseur `zai`, avec des ID de modèle au format `zai/glm-4.7`.

## Configuration CLI

```bash
openclaw onboard --auth-choice zai-api-key
```

## Fragment de configuration

```json5
{
  env: { ZAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "zai/glm-4.7" } } },
}
```

## Remarques

- Les versions de GLM et la disponibilité peuvent varier ; consultez la documentation de Z.AI pour les informations les plus récentes.
- Les exemples d'ID de modèle incluent `glm-4.7` et `glm-4.6`.
- Pour plus de détails sur le fournisseur, consultez [/providers/zai](/providers/zai).
