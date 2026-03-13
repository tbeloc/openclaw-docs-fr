---
read_when:
  - Vous souhaitez utiliser Perplexity Sonar pour la recherche web
  - Vous devez configurer PERPLEXITY_API_KEY ou OpenRouter
summary: Configuration web_search pour Perplexity Sonar
title: Perplexity Sonar
x-i18n:
  generated_at: "2026-02-01T21:19:10Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 264d08e62e3bec854e378dad345ca209d139cd19b0469f3b25f88bb63b73ba00
  source_path: perplexity.md
  workflow: 15
---

# Perplexity Sonar

OpenClaw peut utiliser Perplexity Sonar comme outil `web_search`. Vous pouvez vous connecter via l'API directe de Perplexity ou via OpenRouter.

## Options d'API

### Perplexity (connexion directe)

- URL de base : https://api.perplexity.ai
- Variable d'environnement : `PERPLEXITY_API_KEY`

### OpenRouter (alternative)

- URL de base : https://openrouter.ai/api/v1
- Variable d'environnement : `OPENROUTER_API_KEY`
- Supporte les crédits prépayés/cryptomonnaies.

## Exemple de configuration

```json5
{
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...",
          baseUrl: "https://api.perplexity.ai",
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

## Basculer depuis Brave

```json5
{
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...",
          baseUrl: "https://api.perplexity.ai",
        },
      },
    },
  },
}
```

Si `PERPLEXITY_API_KEY` et `OPENROUTER_API_KEY` sont tous deux définis, veuillez définir `tools.web.search.perplexity.baseUrl` (ou `tools.web.search.perplexity.apiKey`) pour lever l'ambiguïté.

Si l'URL de base n'est pas définie, OpenClaw choisit une valeur par défaut en fonction de la source de la clé API :

- `PERPLEXITY_API_KEY` ou `pplx-...` → Perplexity direct (`https://api.perplexity.ai`)
- `OPENROUTER_API_KEY` ou `sk-or-...` → OpenRouter (`https://openrouter.ai/api/v1`)
- Format de clé inconnu → OpenRouter (secours sécurisé)

## Modèles

- `perplexity/sonar` — Questions-réponses rapides avec recherche web
- `perplexity/sonar-pro` (par défaut) — Raisonnement multi-étapes + recherche web
- `perplexity/sonar-reasoning-pro` — Recherche approfondie

Consultez [Outil Web](/tools/web) pour plus de détails sur la configuration web_search.
