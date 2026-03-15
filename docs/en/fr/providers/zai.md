---
summary: "Utiliser Z.AI (modèles GLM) avec OpenClaw"
read_when:
  - Vous voulez les modèles Z.AI / GLM dans OpenClaw
  - Vous avez besoin d'une simple configuration ZAI_API_KEY
title: "Z.AI"
---

# Z.AI

Z.AI est la plateforme API pour les modèles **GLM**. Elle fournit des API REST pour GLM et utilise des clés API
pour l'authentification. Créez votre clé API dans la console Z.AI. OpenClaw utilise le fournisseur `zai`
avec une clé API Z.AI.

## Configuration CLI

```bash
# Coding Plan Global, recommandé pour les utilisateurs de Coding Plan
openclaw onboard --auth-choice zai-coding-global

# Coding Plan CN (région Chine), recommandé pour les utilisateurs de Coding Plan
openclaw onboard --auth-choice zai-coding-cn

# API générale
openclaw onboard --auth-choice zai-global

# API générale CN (région Chine)
openclaw onboard --auth-choice zai-cn
```

## Extrait de configuration

```json5
{
  env: { ZAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "zai/glm-5" } } },
}
```

## Notes

- Les modèles GLM sont disponibles sous la forme `zai/<model>` (exemple : `zai/glm-5`).
- `tool_stream` est activé par défaut pour le streaming d'appels d'outils Z.AI. Définissez
  `agents.defaults.models["zai/<model>"].params.tool_stream` à `false` pour le désactiver.
- Voir [/providers/glm](/fr/providers/glm) pour un aperçu de la famille de modèles.
- Z.AI utilise l'authentification Bearer avec votre clé API.
