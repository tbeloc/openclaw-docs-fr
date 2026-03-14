---
summary: "Fournisseurs de modèles (LLM) supportés par OpenClaw"
read_when:
  - You want to choose a model provider
  - You need a quick overview of supported LLM backends
title: "Fournisseurs de modèles"
---

# Fournisseurs de modèles

OpenClaw peut utiliser de nombreux fournisseurs de LLM. Choisissez un fournisseur, authentifiez-vous, puis définissez le modèle par défaut comme `provider/model`.

Vous cherchez la documentation des canaux de chat (WhatsApp/Telegram/Discord/Slack/Mattermost (plugin)/etc.) ? Voir [Canaux](/channels).

## Démarrage rapide

1. Authentifiez-vous auprès du fournisseur (généralement via `openclaw onboard`).
2. Définissez le modèle par défaut :

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

## Documentation des fournisseurs

- [Amazon Bedrock](/providers/bedrock)
- [Anthropic (API + Claude Code CLI)](/providers/anthropic)
- [Cloudflare AI Gateway](/providers/cloudflare-ai-gateway)
- [Modèles GLM](/providers/glm)
- [Hugging Face (Inference)](/providers/huggingface)
- [Kilocode](/providers/kilocode)
- [LiteLLM (passerelle unifiée)](/providers/litellm)
- [MiniMax](/providers/minimax)
- [Mistral](/providers/mistral)
- [Moonshot AI (Kimi + Kimi Coding)](/providers/moonshot)
- [NVIDIA](/providers/nvidia)
- [Ollama (modèles cloud + locaux)](/providers/ollama)
- [OpenAI (API + Codex)](/providers/openai)
- [OpenCode (Zen + Go)](/providers/opencode)
- [OpenRouter](/providers/openrouter)
- [Qianfan](/providers/qianfan)
- [Qwen (OAuth)](/providers/qwen)
- [Together AI](/providers/together)
- [Vercel AI Gateway](/providers/vercel-ai-gateway)
- [Venice (Venice AI, axé sur la confidentialité)](/providers/venice)
- [vLLM (modèles locaux)](/providers/vllm)
- [Xiaomi](/providers/xiaomi)
- [Z.AI](/providers/zai)

## Fournisseurs de transcription

- [Deepgram (transcription audio)](/providers/deepgram)

## Outils communautaires

- [Claude Max API Proxy](/providers/claude-max-api-proxy) - Proxy communautaire pour les identifiants d'abonnement Claude (vérifiez la politique/les conditions d'Anthropic avant utilisation)

Pour le catalogue complet des fournisseurs (xAI, Groq, Mistral, etc.) et la configuration avancée,
voir [Fournisseurs de modèles](/concepts/model-providers).
