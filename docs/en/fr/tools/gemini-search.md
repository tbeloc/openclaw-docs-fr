---
summary: "Recherche web Gemini avec grounding Google Search"
read_when:
  - You want to use Gemini for web_search
  - You need a GEMINI_API_KEY
  - You want Google Search grounding
title: "Gemini Search"
---

# Gemini Search

OpenClaw prend en charge les modèles Gemini avec
[grounding Google Search](https://ai.google.dev/gemini-api/docs/grounding) intégré,
qui retourne des réponses synthétisées par l'IA soutenues par les résultats de recherche Google en direct avec
des citations.

## Obtenir une clé API

<Steps>
  <Step title="Créer une clé">
    Allez sur [Google AI Studio](https://aistudio.google.com/apikey) et créez une
    clé API.
  </Step>
  <Step title="Stocker la clé">
    Définissez `GEMINI_API_KEY` dans l'environnement de la passerelle, ou configurez via :

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
      google: {
        config: {
          webSearch: {
            apiKey: "AIza...", // optionnel si GEMINI_API_KEY est défini
            model: "gemini-2.5-flash", // par défaut
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "gemini",
      },
    },
  },
}
```

**Alternative d'environnement :** définissez `GEMINI_API_KEY` dans l'environnement de la passerelle.
Pour une installation de passerelle, mettez-le dans `~/.openclaw/.env`.

## Fonctionnement

Contrairement aux fournisseurs de recherche traditionnels qui retournent une liste de liens et d'extraits,
Gemini utilise le grounding Google Search pour produire des réponses synthétisées par l'IA avec
des citations intégrées. Les résultats incluent à la fois la réponse synthétisée et les URL sources.

- Les URL de citation du grounding Gemini sont automatiquement résolues à partir des URL de redirection Google vers des URL directes.
- La résolution des redirections utilise le chemin de protection SSRF (vérifications HEAD + redirection +
  validation http/https) avant de retourner l'URL de citation finale.
- La résolution des redirections utilise des paramètres par défaut SSRF stricts, donc les redirections vers
  des cibles privées/internes sont bloquées.

## Paramètres pris en charge

La recherche Gemini prend en charge les paramètres standard `query` et `count`.
Les filtres spécifiques au fournisseur comme `country`, `language`, `freshness` et
`domain_filter` ne sont pas pris en charge.

## Sélection du modèle

Le modèle par défaut est `gemini-2.5-flash` (rapide et rentable). Tout modèle Gemini
qui prend en charge le grounding peut être utilisé via
`plugins.entries.google.config.webSearch.model`.

## Connexes

- [Aperçu de la recherche web](/fr/tools/web) -- tous les fournisseurs et détection automatique
- [Brave Search](/fr/tools/brave-search) -- résultats structurés avec extraits
- [Perplexity Search](/fr/tools/perplexity-search) -- résultats structurés + extraction de contenu
