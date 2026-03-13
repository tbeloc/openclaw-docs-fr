---
read_when:
  - Vous souhaitez utiliser Vercel AI Gateway avec OpenClaw
  - Vous avez besoin de variables d'environnement de clé API ou d'options d'authentification CLI
summary: Configuration de Vercel AI Gateway (authentification + sélection de modèle)
title: Vercel AI Gateway
x-i18n:
  generated_at: "2026-02-03T07:53:39Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: c6482f047a31b09c7a691d40babbd1f9fb3aa2042b61cc42956ad9b791da8285
  source_path: providers/vercel-ai-gateway.md
  workflow: 15
---

# Vercel AI Gateway

[Vercel AI Gateway](https://vercel.com/ai-gateway) fournit une API unifiée pour accéder à des centaines de modèles via un seul point de terminaison.

- Fournisseur : `vercel-ai-gateway`
- Authentification : `AI_GATEWAY_API_KEY`
- API : Compatible avec Anthropic Messages

## Démarrage rapide

1. Configurez la clé API (recommandé : stockez-la pour la passerelle) :

```bash
openclaw onboard --auth-choice ai-gateway-api-key
```

2. Définissez le modèle par défaut :

```json5
{
  agents: {
    defaults: {
      model: { primary: "vercel-ai-gateway/anthropic/claude-opus-4.5" },
    },
  },
}
```

## Exemple non interactif

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice ai-gateway-api-key \
  --ai-gateway-api-key "$AI_GATEWAY_API_KEY"
```

## Explication des variables d'environnement

Si la passerelle s'exécute en tant que processus démon (launchd/systemd), assurez-vous que `AI_GATEWAY_API_KEY`
est disponible pour ce processus (par exemple, dans `~/.openclaw/.env` ou via
`env.shellEnv`).
