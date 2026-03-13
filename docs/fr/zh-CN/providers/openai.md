---
read_when:
  - Vous souhaitez utiliser des modèles OpenAI dans OpenClaw
  - Vous souhaitez utiliser l'authentification par abonnement Codex plutôt que par clé API
summary: Utiliser OpenAI dans OpenClaw via clé API ou abonnement Codex
title: OpenAI
x-i18n:
  generated_at: "2026-02-01T21:35:10Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: f15365d5d616258f6035b986d80fe6acd1be5836a07e5bb68236688ef2952ef7
  source_path: providers/openai.md
  workflow: 15
---

# OpenAI

OpenAI fournit une API développeur pour les modèles GPT. Codex supporte la **connexion ChatGPT** pour l'accès par abonnement, ou la **clé API** pour l'accès à la facturation à l'usage. Codex Cloud nécessite une connexion ChatGPT.

## Méthode A : Clé API OpenAI (Plateforme OpenAI)

**Applicable à :** accès direct à l'API et facturation à l'usage.
Obtenez votre clé API depuis la console OpenAI.

### Configuration CLI

```bash
openclaw onboard --auth-choice openai-api-key
# ou non-interactif
openclaw onboard --openai-api-key "$OPENAI_API_KEY"
```

### Extrait de configuration

```json5
{
  env: { OPENAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "openai/gpt-5.2" } } },
}
```

## Méthode B : Code OpenAI (Abonnement Codex)

**Applicable à :** utiliser l'accès par abonnement ChatGPT/Codex plutôt que par clé API.
Codex Cloud nécessite une connexion ChatGPT, tandis que Codex CLI supporte la connexion ChatGPT ou par clé API.

### Configuration CLI

```bash
# Exécuter Codex OAuth dans l'assistant
openclaw onboard --auth-choice openai-codex

# ou exécuter directement OAuth
openclaw models auth login --provider openai-codex
```

### Extrait de configuration

```json5
{
  agents: { defaults: { model: { primary: "openai-codex/gpt-5.2" } } },
}
```

## Remarques

- Les références de modèles utilisent toujours le format `provider/model` (voir [/concepts/models](/concepts/models)).
- Pour les détails d'authentification et les règles de réutilisation, consultez [/concepts/oauth](/concepts/oauth).
