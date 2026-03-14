---
summary: "Perplexity Search API et compatibilité Sonar/OpenRouter pour web_search"
read_when:
  - You want to use Perplexity Search for web search
  - You need PERPLEXITY_API_KEY or OPENROUTER_API_KEY setup
title: "Perplexity Search"
---

# API Perplexity Search

OpenClaw supporte l'API Perplexity Search en tant que fournisseur `web_search`.
Elle retourne des résultats structurés avec les champs `title`, `url` et `snippet`.

Pour la compatibilité, OpenClaw supporte également les configurations héritées Perplexity Sonar/OpenRouter.
Si vous utilisez `OPENROUTER_API_KEY`, une clé `sk-or-...` dans `tools.web.search.perplexity.apiKey`, ou si vous définissez `tools.web.search.perplexity.baseUrl` / `model`, le fournisseur bascule vers le chemin chat-completions et retourne des réponses synthétisées par IA avec citations au lieu des résultats structurés de l'API Search.

## Obtenir une clé API Perplexity

1. Créez un compte Perplexity sur <https://www.perplexity.ai/settings/api>
2. Générez une clé API dans le tableau de bord
3. Stockez la clé dans la configuration ou définissez `PERPLEXITY_API_KEY` dans l'environnement de la Gateway.

## Compatibilité OpenRouter

Si vous utilisiez déjà OpenRouter pour Perplexity Sonar, conservez `provider: "perplexity"` et définissez `OPENROUTER_API_KEY` dans l'environnement de la Gateway, ou stockez une clé `sk-or-...` dans `tools.web.search.perplexity.apiKey`.

Contrôles hérités optionnels :

- `tools.web.search.perplexity.baseUrl`
- `tools.web.search.perplexity.model`

## Exemples de configuration

### API Perplexity Search native

```json5
{
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...",
        },
      },
    },
  },
}
```

### Compatibilité OpenRouter / Sonar

```json5
{
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "<openrouter-api-key>",
          baseUrl: "https://openrouter.ai/api/v1",
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

## Où définir la clé

**Via la configuration :** exécutez `openclaw configure --section web`. Elle stocke la clé dans
`~/.openclaw/openclaw.json` sous `tools.web.search.perplexity.apiKey`.
Ce champ accepte également les objets SecretRef.

**Via l'environnement :** définissez `PERPLEXITY_API_KEY` ou `OPENROUTER_API_KEY`
dans l'environnement du processus Gateway. Pour une installation de gateway, mettez-la dans
`~/.openclaw/.env` (ou votre environnement de service). Voir [Variables d'environnement](/help/faq#how-does-openclaw-load-environment-variables).

Si `provider: "perplexity"` est configuré et que la SecretRef de la clé Perplexity n'est pas résolue sans secours d'environnement, le démarrage/rechargement échoue rapidement.

## Paramètres de l'outil

Ces paramètres s'appliquent au chemin natif de l'API Perplexity Search.

| Paramètre             | Description                                                    |
| --------------------- | -------------------------------------------------------------- |
| `query`               | Requête de recherche (obligatoire)                             |
| `count`               | Nombre de résultats à retourner (1-10, par défaut : 5)         |
| `country`             | Code pays ISO à 2 lettres (ex. : "US", "DE")                  |
| `language`            | Code de langue ISO 639-1 (ex. : "en", "de", "fr")             |
| `freshness`           | Filtre temporel : `day` (24h), `week`, `month` ou `year`       |
| `date_after`          | Uniquement les résultats publiés après cette date (YYYY-MM-DD) |
| `date_before`         | Uniquement les résultats publiés avant cette date (YYYY-MM-DD) |
| `domain_filter`       | Liste blanche/noire de domaines (max 20)                       |
| `max_tokens`          | Budget de contenu total (par défaut : 25000, max : 1000000)    |
| `max_tokens_per_page` | Limite de tokens par page (par défaut : 2048)                  |

Pour le chemin de compatibilité Sonar/OpenRouter hérité, seuls `query` et `freshness` sont supportés.
Les filtres spécifiques à l'API Search tels que `country`, `language`, `date_after`, `date_before`, `domain_filter`, `max_tokens` et `max_tokens_per_page` retournent des erreurs explicites.

**Exemples :**

```javascript
// Recherche spécifique à un pays et une langue
await web_search({
  query: "renewable energy",
  country: "DE",
  language: "de",
});

// Résultats récents (semaine passée)
await web_search({
  query: "AI news",
  freshness: "week",
});

// Recherche par plage de dates
await web_search({
  query: "AI developments",
  date_after: "2024-01-01",
  date_before: "2024-06-30",
});

// Filtrage de domaines (liste blanche)
await web_search({
  query: "climate research",
  domain_filter: ["nature.com", "science.org", ".edu"],
});

// Filtrage de domaines (liste noire - préfixe avec -)
await web_search({
  query: "product reviews",
  domain_filter: ["-reddit.com", "-pinterest.com"],
});

// Extraction de contenu plus importante
await web_search({
  query: "detailed AI research",
  max_tokens: 50000,
  max_tokens_per_page: 4096,
});
```

### Règles de filtre de domaine

- Maximum 20 domaines par filtre
- Impossible de mélanger liste blanche et liste noire dans la même requête
- Utilisez le préfixe `-` pour les entrées de liste noire (ex. : `["-reddit.com"]`)

## Notes

- L'API Perplexity Search retourne des résultats de recherche web structurés (`title`, `url`, `snippet`)
- OpenRouter ou `baseUrl` / `model` explicite bascule Perplexity vers Sonar chat completions pour la compatibilité
- Les résultats sont mis en cache pendant 15 minutes par défaut (configurable via `cacheTtlMinutes`)

Voir [Outils Web](/tools/web) pour la configuration complète de web_search.
Voir [Documentation de l'API Perplexity Search](https://docs.perplexity.ai/docs/search/quickstart) pour plus de détails.
