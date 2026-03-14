---
read_when:
  - Vous souhaitez choisir un fournisseur de modèle
  - Vous souhaitez un exemple de configuration rapide pour l'authentification LLM + la sélection de modèle
summary: Fournisseurs de modèles supportés par OpenClaw (LLM)
title: Démarrage rapide des fournisseurs de modèles
x-i18n:
  generated_at: "2026-02-03T07:53:35Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 2f5b99207dc7860e0a7b541b61e984791f5d7ab1953b3e917365a248a09b025b
  source_path: providers/models.md
  workflow: 15
---

# Fournisseurs de modèles

OpenClaw peut utiliser de nombreux fournisseurs LLM. Choisissez-en un, authentifiez-vous, puis définissez le modèle par défaut sur `provider/model`.

## Recommandé : Venice (Venice AI)

Venice est notre configuration Venice AI recommandée pour l'inférence axée sur la confidentialité, avec la possibilité d'utiliser Opus pour les tâches les plus difficiles.

- Par défaut : `venice/llama-3.3-70b`
- Meilleur compromis : `venice/claude-opus-45` (Opus reste le plus puissant)

Voir [Venice AI](/providers/venice).

## Démarrage rapide (deux étapes)

1. Authentifiez-vous auprès du fournisseur (généralement via `openclaw onboard`).
2. Définissez le modèle par défaut :

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-5" } } },
}
```

## Fournisseurs supportés (ensemble de démarrage)

- [OpenAI (API + Codex)](/providers/openai)
- [Anthropic (API + Claude Code CLI)](/providers/anthropic)
- [OpenRouter](/providers/openrouter)
- [Vercel AI Gateway](/providers/vercel-ai-gateway)
- [Moonshot AI (Kimi + Kimi Coding)](/providers/moonshot)
- [Synthetic](/providers/synthetic)
- [OpenCode Zen](/providers/opencode)
- [Z.AI](/providers/zai)
- [Modèles GLM](/providers/glm)
- [MiniMax](/providers/minimax)
- [Venice (Venice AI)](/providers/venice)
- [Amazon Bedrock](/providers/bedrock)

Pour un répertoire complet des fournisseurs (xAI, Groq, Mistral, etc.) et une configuration avancée, consultez [Fournisseurs de modèles](/concepts/model-providers).
