---
summary: "Fournisseurs de modèles (LLM) supportés par OpenClaw"
read_when:
  - You want to choose a model provider
  - You want quick setup examples for LLM auth + model selection
title: "Démarrage rapide des fournisseurs de modèles"
---

# Fournisseurs de modèles

OpenClaw peut utiliser de nombreux fournisseurs LLM. Choisissez-en un, authentifiez-vous, puis définissez le modèle par défaut comme `provider/model`.

## Démarrage rapide (deux étapes)

1. Authentifiez-vous auprès du fournisseur (généralement via `openclaw onboard`).
2. Définissez le modèle par défaut :

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

## Fournisseurs supportés (ensemble de démarrage)

- [OpenAI (API + Codex)](/providers/openai)
- [Anthropic (API + Claude Code CLI)](/providers/anthropic)
- [OpenRouter](/providers/openrouter)
- [Vercel AI Gateway](/providers/vercel-ai-gateway)
- [Cloudflare AI Gateway](/providers/cloudflare-ai-gateway)
- [Moonshot AI (Kimi + Kimi Coding)](/providers/moonshot)
- [Mistral](/providers/mistral)
- [Synthetic](/providers/synthetic)
- [OpenCode (Zen + Go)](/providers/opencode)
- [Z.AI](/providers/zai)
- [GLM models](/providers/glm)
- [MiniMax](/providers/minimax)
- [Venice (Venice AI)](/providers/venice)
- [Amazon Bedrock](/providers/bedrock)
- [Qianfan](/providers/qianfan)

Pour le catalogue complet des fournisseurs (xAI, Groq, Mistral, etc.) et la configuration avancée,
consultez [Fournisseurs de modèles](/concepts/model-providers).
