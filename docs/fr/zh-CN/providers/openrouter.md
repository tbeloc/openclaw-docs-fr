---
read_when:
  - Vous souhaitez accéder à plusieurs LLM avec une seule clé API
  - Vous souhaitez exécuter des modèles via OpenRouter dans OpenClaw
summary: Accédez à plusieurs modèles dans OpenClaw en utilisant l'API unifiée d'OpenRouter
title: OpenRouter
x-i18n:
  generated_at: "2026-02-01T21:35:19Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b7e29fc9c456c64d567dd909a85166e6dea8388ebd22155a31e69c970e081586
  source_path: providers/openrouter.md
  workflow: 15
---

# OpenRouter

OpenRouter fournit une **API unifiée** qui achemine les requêtes vers plusieurs modèles via un seul point de terminaison et une clé API. Elle est compatible avec OpenAI, donc la plupart des SDK OpenAI peuvent être utilisés en changeant simplement l'URL de base.

## Configuration CLI

```bash
openclaw onboard --auth-choice apiKey --token-provider openrouter --token "$OPENROUTER_API_KEY"
```

## Extrait de configuration

```json5
{
  env: { OPENROUTER_API_KEY: "sk-or-..." },
  agents: {
    defaults: {
      model: { primary: "openrouter/anthropic/claude-sonnet-4-5" },
    },
  },
}
```

## Remarques

- Le format de référence du modèle est `openrouter/<provider>/<model>`.
- Pour plus d'options de modèles/fournisseurs, consultez [Fournisseurs de modèles](/concepts/model-providers).
- OpenRouter utilise en interne les jetons Bearer et votre clé API pour l'authentification.
