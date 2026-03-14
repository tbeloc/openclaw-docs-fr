---
title: "Vercel AI Gateway"
summary: "Configuration de Vercel AI Gateway (authentification + sélection de modèle)"
read_when:
  - You want to use Vercel AI Gateway with OpenClaw
  - You need the API key env var or CLI auth choice
---

# Vercel AI Gateway

[Vercel AI Gateway](https://vercel.com/ai-gateway) fournit une API unifiée pour accéder à des centaines de modèles via un seul point de terminaison.

- Provider: `vercel-ai-gateway`
- Auth: `AI_GATEWAY_API_KEY`
- API: Compatible avec Anthropic Messages
- OpenClaw découvre automatiquement le catalogue `/v1/models` de la Gateway, donc `/models vercel-ai-gateway`
  inclut les références de modèles actuels tels que `vercel-ai-gateway/openai/gpt-5.4`.

## Démarrage rapide

1. Définissez la clé API (recommandé : stockez-la pour la Gateway) :

```bash
openclaw onboard --auth-choice ai-gateway-api-key
```

2. Définissez un modèle par défaut :

```json5
{
  agents: {
    defaults: {
      model: { primary: "vercel-ai-gateway/anthropic/claude-opus-4.6" },
    },
  },
}
```

## Exemple non-interactif

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice ai-gateway-api-key \
  --ai-gateway-api-key "$AI_GATEWAY_API_KEY"
```

## Note sur l'environnement

Si la Gateway s'exécute en tant que daemon (launchd/systemd), assurez-vous que `AI_GATEWAY_API_KEY`
est disponible pour ce processus (par exemple, dans `~/.openclaw/.env` ou via
`env.shellEnv`).

## Raccourci pour l'ID de modèle

OpenClaw accepte les références de modèles Claude raccourcis de Vercel et les normalise à
l'exécution :

- `vercel-ai-gateway/claude-opus-4.6` -> `vercel-ai-gateway/anthropic/claude-opus-4.6`
- `vercel-ai-gateway/opus-4.6` -> `vercel-ai-gateway/anthropic/claude-opus-4-6`
