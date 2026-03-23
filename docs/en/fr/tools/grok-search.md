---
summary: "Recherche web Grok via réponses web-grounded xAI"
read_when:
  - You want to use Grok for web_search
  - You need an XAI_API_KEY for web search
title: "Recherche Grok"
---

# Recherche Grok

OpenClaw supporte Grok en tant que fournisseur `web_search`, utilisant les réponses web-grounded xAI pour produire des réponses synthétisées par IA soutenues par des résultats de recherche en direct avec citations.

## Obtenir une clé API

<Steps>
  <Step title="Créer une clé">
    Obtenez une clé API depuis [xAI](https://console.x.ai/).
  </Step>
  <Step title="Stocker la clé">
    Définissez `XAI_API_KEY` dans l'environnement Gateway, ou configurez via :

    ```bash
    openclaw configure --section web
    ```

  </Step>
</Steps>

## Configuration

```json5
{
  plugins: {
    entries: {
      xai: {
        config: {
          webSearch: {
            apiKey: "xai-...", // optional if XAI_API_KEY is set
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "grok",
      },
    },
  },
}
```

**Alternative environnement :** définissez `XAI_API_KEY` dans l'environnement Gateway.
Pour une installation gateway, placez-le dans `~/.openclaw/.env`.

## Fonctionnement

Grok utilise les réponses web-grounded xAI pour synthétiser des réponses avec des citations intégrées, similaire à l'approche de grounding Google Search de Gemini.

## Paramètres supportés

La recherche Grok supporte les paramètres standard `query` et `count`.
Les filtres spécifiques au fournisseur ne sont actuellement pas supportés.

## Liens connexes

- [Aperçu de la recherche web](/fr/tools/web) -- tous les fournisseurs et détection automatique
- [Recherche Gemini](/fr/tools/gemini-search) -- réponses synthétisées par IA via grounding Google
