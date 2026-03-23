---
summary: "Recherche web DuckDuckGo -- fournisseur de secours sans clé (expérimental, basé sur HTML)"
read_when:
  - You want a web search provider that requires no API key
  - You want to use DuckDuckGo for web_search
  - You need a zero-config search fallback
title: "Recherche DuckDuckGo"
---

# Recherche DuckDuckGo

OpenClaw supporte DuckDuckGo comme fournisseur `web_search` **sans clé**. Aucune clé API ou compte n'est requis.

<Warning>
  DuckDuckGo est une intégration **expérimentale, non officielle** qui récupère les résultats des pages de recherche non-JavaScript de DuckDuckGo — pas une API officielle. Attendez-vous à des dysfonctionnements occasionnels dus aux pages de défi bot ou aux changements HTML.
</Warning>

## Configuration

Aucune clé API nécessaire — définissez simplement DuckDuckGo comme fournisseur :

<Steps>
  <Step title="Configurer">
    ```bash
    openclaw configure --section web
    # Sélectionnez "duckduckgo" comme fournisseur
    ```
  </Step>
</Steps>

## Config

```json5
{
  tools: {
    web: {
      search: {
        provider: "duckduckgo",
      },
    },
  },
}
```

Paramètres optionnels au niveau du plugin pour la région et SafeSearch :

```json5
{
  plugins: {
    entries: {
      duckduckgo: {
        config: {
          webSearch: {
            region: "us-en", // Code de région DuckDuckGo
            safeSearch: "moderate", // "strict", "moderate", ou "off"
          },
        },
      },
    },
  },
}
```

## Paramètres de l'outil

| Paramètre    | Description                                                |
| ------------ | ---------------------------------------------------------- |
| `query`      | Requête de recherche (obligatoire)                         |
| `count`      | Résultats à retourner (1-10, par défaut : 5)              |
| `region`     | Code de région DuckDuckGo (ex. `us-en`, `uk-en`, `de-de`) |
| `safeSearch` | Niveau SafeSearch : `strict`, `moderate` (par défaut), ou `off` |

La région et SafeSearch peuvent également être définis dans la config du plugin (voir ci-dessus) — les paramètres de l'outil remplacent les valeurs de config par requête.

## Notes

- **Pas de clé API** — fonctionne immédiatement, zéro configuration
- **Expérimental** — récupère les résultats des pages de recherche HTML non-JavaScript de DuckDuckGo, pas une API ou SDK officielle
- **Risque de défi bot** — DuckDuckGo peut servir des CAPTCHAs ou bloquer les requêtes en cas d'utilisation intensive ou automatisée
- **Analyse HTML** — les résultats dépendent de la structure de la page, qui peut changer sans préavis
- **Ordre de détection automatique** — DuckDuckGo est vérifié en dernier (ordre 100) dans la détection automatique, donc tout fournisseur soutenu par une API avec une clé a la priorité
- **SafeSearch par défaut à modéré** quand non configuré

<Tip>
  Pour une utilisation en production, envisagez [Brave Search](/fr/tools/brave-search) (niveau gratuit disponible) ou un autre fournisseur soutenu par une API.
</Tip>

## Connexes

- [Aperçu de la recherche web](/fr/tools/web) -- tous les fournisseurs et détection automatique
- [Brave Search](/fr/tools/brave-search) -- résultats structurés avec niveau gratuit
- [Recherche Exa](/fr/tools/exa-search) -- recherche neuronale avec extraction de contenu
