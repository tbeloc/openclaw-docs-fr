---
read_when:
  - Vous souhaitez choisir un fournisseur de modèle
  - Vous avez besoin de comprendre rapidement les backends LLM supportés
summary: Fournisseurs de modèles (LLM) supportés par OpenClaw
title: Fournisseurs de modèles
x-i18n:
  generated_at: "2026-02-03T07:53:32Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: eb4a97438adcf610499253afcf8b2af6624f4be098df389a6c3746f14c4a901b
  source_path: providers/index.md
  workflow: 15
---

# Fournisseurs de modèles

OpenClaw peut utiliser de nombreux fournisseurs LLM. Choisissez un fournisseur, authentifiez-vous, puis définissez le modèle par défaut comme `fournisseur/modèle`.

Vous cherchez la documentation des canaux de chat (WhatsApp/Telegram/Discord/Slack/Mattermost (plugin), etc.) ? Consultez [Canaux](/channels).

## Point fort : Venice (Venice AI)

Venice est notre configuration Venice AI recommandée pour l'inférence axée sur la confidentialité, avec la possibilité d'utiliser Opus pour les tâches difficiles.

- Par défaut : `venice/llama-3.3-70b`
- Meilleur compromis : `venice/claude-opus-45` (Opus reste le plus puissant)

Consultez [Venice AI](/providers/venice).

## Démarrage rapide

1. Authentifiez-vous auprès du fournisseur (généralement via `openclaw onboard`).
2. Définissez le modèle par défaut :

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-5" } } },
}
```

## Documentation des fournisseurs

- [Amazon Bedrock](/providers/bedrock)
- [Anthropic (API + Claude Code CLI)](/providers/anthropic)
- [Modèles GLM](/providers/glm)
- [MiniMax](/providers/minimax)
- [Moonshot AI (Kimi + Kimi Coding)](/providers/moonshot)
- [Ollama (modèles locaux)](/providers/ollama)
- [OpenAI (API + Codex)](/providers/openai)
- [OpenCode Zen](/providers/opencode)
- [OpenRouter](/providers/openrouter)
- [Qwen (OAuth)](/providers/qwen)
- [Venice (Venice AI, axé sur la confidentialité)](/providers/venice)
- [Xiaomi](/providers/xiaomi)
- [Z.AI](/providers/zai)

## Fournisseurs de transcription

- [Deepgram (transcription audio)](/providers/deepgram)

## Outils communautaires

- [Claude Max API Proxy](/providers/claude-max-api-proxy) - Utilisez votre abonnement Claude Max/Pro comme point de terminaison API compatible OpenAI

Pour un répertoire complet des fournisseurs (xAI, Groq, Mistral, etc.) et une configuration avancée,
consultez [Fournisseurs de modèles](/concepts/model-providers).
