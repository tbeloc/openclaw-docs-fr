---
title: "Cloudflare AI Gateway"
summary: "Configuration de Cloudflare AI Gateway (authentification + sélection de modèle)"
read_when:
  - You want to use Cloudflare AI Gateway with OpenClaw
  - You need the account ID, gateway ID, or API key env var
---

# Cloudflare AI Gateway

Cloudflare AI Gateway se place devant les API des fournisseurs et vous permet d'ajouter des analyses, de la mise en cache et des contrôles. Pour Anthropic, OpenClaw utilise l'API Anthropic Messages via votre endpoint Gateway.

- Provider: `cloudflare-ai-gateway`
- Base URL: `https://gateway.ai.cloudflare.com/v1/<account_id>/<gateway_id>/anthropic`
- Default model: `cloudflare-ai-gateway/claude-sonnet-4-5`
- API key: `CLOUDFLARE_AI_GATEWAY_API_KEY` (votre clé API du fournisseur pour les requêtes via la Gateway)

Pour les modèles Anthropic, utilisez votre clé API Anthropic.

## Démarrage rapide

1. Définissez la clé API du fournisseur et les détails de la Gateway :

```bash
openclaw onboard --auth-choice cloudflare-ai-gateway-api-key
```

2. Définissez un modèle par défaut :

```json5
{
  agents: {
    defaults: {
      model: { primary: "cloudflare-ai-gateway/claude-sonnet-4-5" },
    },
  },
}
```

## Exemple non-interactif

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice cloudflare-ai-gateway-api-key \
  --cloudflare-ai-gateway-account-id "your-account-id" \
  --cloudflare-ai-gateway-gateway-id "your-gateway-id" \
  --cloudflare-ai-gateway-api-key "$CLOUDFLARE_AI_GATEWAY_API_KEY"
```

## Gateways authentifiées

Si vous avez activé l'authentification Gateway dans Cloudflare, ajoutez l'en-tête `cf-aig-authorization` (ceci s'ajoute à votre clé API du fournisseur).

```json5
{
  models: {
    providers: {
      "cloudflare-ai-gateway": {
        headers: {
          "cf-aig-authorization": "Bearer <cloudflare-ai-gateway-token>",
        },
      },
    },
  },
}
```

## Note sur l'environnement

Si la Gateway s'exécute en tant que daemon (launchd/systemd), assurez-vous que `CLOUDFLARE_AI_GATEWAY_API_KEY` est disponible pour ce processus (par exemple, dans `~/.openclaw/.env` ou via `env.shellEnv`).
