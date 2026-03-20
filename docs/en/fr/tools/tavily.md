---
summary: "Outils de recherche et d'extraction Tavily"
read_when:
  - You want Tavily-backed web search
  - You need a Tavily API key
  - You want Tavily as a web_search provider
  - You want content extraction from URLs
title: "Tavily"
---

# Tavily

OpenClaw peut utiliser **Tavily** de deux façons :

- comme fournisseur `web_search`
- comme outils de plugin explicites : `tavily_search` et `tavily_extract`

Tavily est une API de recherche conçue pour les applications d'IA, renvoyant des résultats structurés
optimisés pour la consommation par LLM. Elle supporte la profondeur de recherche configurable, le filtrage par sujet,
les filtres de domaine, les résumés de réponses générés par IA, et l'extraction de contenu
à partir d'URLs (y compris les pages rendues par JavaScript).

## Obtenir une clé API

1. Créez un compte Tavily sur [tavily.com](https://tavily.com/).
2. Générez une clé API dans le tableau de bord.
3. Stockez-la dans la configuration ou définissez `TAVILY_API_KEY` dans l'environnement de la passerelle.

## Configurer la recherche Tavily

```json5
{
  plugins: {
    entries: {
      tavily: {
        enabled: true,
        config: {
          webSearch: {
            apiKey: "tvly-...", // optionnel si TAVILY_API_KEY est défini
            baseUrl: "https://api.tavily.com",
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "tavily",
      },
    },
  },
}
```

Notes :

- Choisir Tavily lors de l'intégration ou avec `openclaw configure --section web` active
  automatiquement le plugin Tavily fourni.
- Stockez la configuration Tavily sous `plugins.entries.tavily.config.webSearch.*`.
- `web_search` avec Tavily supporte `query` et `count` (jusqu'à 20 résultats).
- Pour les contrôles spécifiques à Tavily comme `search_depth`, `topic`, `include_answer`,
  ou les filtres de domaine, utilisez `tavily_search`.

## Outils du plugin Tavily

### `tavily_search`

Utilisez ceci quand vous voulez des contrôles de recherche spécifiques à Tavily au lieu de
`web_search` générique.

| Paramètre         | Description                                                           |
| ----------------- | --------------------------------------------------------------------- |
| `query`           | Chaîne de requête de recherche (garder moins de 400 caractères)       |
| `search_depth`    | `basic` (par défaut, équilibré) ou `advanced` (plus haute pertinence, plus lent) |
| `topic`           | `general` (par défaut), `news` (mises à jour en temps réel), ou `finance` |
| `max_results`     | Nombre de résultats, 1-20 (par défaut : 5)                            |
| `include_answer`  | Inclure un résumé de réponse généré par IA (par défaut : false)       |
| `time_range`      | Filtrer par récence : `day`, `week`, `month`, ou `year`               |
| `include_domains` | Tableau de domaines pour restreindre les résultats à                  |
| `exclude_domains` | Tableau de domaines à exclure des résultats                           |

**Profondeur de recherche :**

| Profondeur | Vitesse | Pertinence | Meilleur pour                           |
| ---------- | ------- | ---------- | --------------------------------------- |
| `basic`    | Plus rapide | Élevée | Requêtes à usage général (par défaut)   |
| `advanced` | Plus lent | Plus élevée | Précision, faits spécifiques, recherche |

### `tavily_extract`

Utilisez ceci pour extraire du contenu propre d'une ou plusieurs URLs. Gère
les pages rendues par JavaScript et supporte le chunking orienté requête pour
l'extraction ciblée.

| Paramètre           | Description                                                |
| ------------------- | ---------------------------------------------------------- |
| `urls`              | Tableau d'URLs à extraire (1-20 par requête)               |
| `query`             | Reclasser les chunks extraits par pertinence à cette requête |
| `extract_depth`     | `basic` (par défaut, rapide) ou `advanced` (pour pages JS-lourdes) |
| `chunks_per_source` | Chunks par URL, 1-5 (nécessite `query`)                    |
| `include_images`    | Inclure les URLs d'images dans les résultats (par défaut : false) |

**Profondeur d'extraction :**

| Profondeur | Quand l'utiliser                               |
| ---------- | ---------------------------------------------- |
| `basic`    | Pages simples - essayez d'abord ceci           |
| `advanced` | SPAs rendues par JS, contenu dynamique, tableaux |

Conseils :

- Maximum 20 URLs par requête. Divisez les listes plus grandes en plusieurs appels.
- Utilisez `query` + `chunks_per_source` pour obtenir uniquement le contenu pertinent au lieu de pages complètes.
- Essayez d'abord `basic` ; revenez à `advanced` si le contenu est manquant ou incomplet.

## Choisir le bon outil

| Besoin                                 | Outil             |
| ------------------------------------ | ---------------- |
| Recherche web rapide, sans options spéciales | `web_search`     |
| Recherche avec profondeur, sujet, réponses IA | `tavily_search`  |
| Extraire du contenu d'URLs spécifiques   | `tavily_extract` |

Voir [Outils web](/fr/tools/web) pour la configuration complète des outils web et la comparaison des fournisseurs.
