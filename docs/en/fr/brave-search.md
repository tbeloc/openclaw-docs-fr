---
summary: "Configuration de l'API Brave Search pour web_search"
read_when:
  - You want to use Brave Search for web_search
  - You need a BRAVE_API_KEY or plan details
title: "Brave Search"
---

# API Brave Search

OpenClaw supporte l'API Brave Search en tant que fournisseur `web_search`.

## Obtenir une clé API

1. Créez un compte Brave Search API sur [https://brave.com/search/api/](https://brave.com/search/api/)
2. Dans le tableau de bord, choisissez le plan **Search** et générez une clé API.
3. Stockez la clé dans la configuration ou définissez `BRAVE_API_KEY` dans l'environnement de la Gateway.

## Exemple de configuration

```json5
{
  tools: {
    web: {
      search: {
        provider: "brave",
        apiKey: "BRAVE_API_KEY_HERE",
        maxResults: 5,
        timeoutSeconds: 30,
      },
    },
  },
}
```

## Paramètres de l'outil

| Paramètre     | Description                                                         |
| ------------- | ------------------------------------------------------------------- |
| `query`       | Requête de recherche (obligatoire)                                  |
| `count`       | Nombre de résultats à retourner (1-10, par défaut : 5)              |
| `country`     | Code pays ISO à 2 lettres (ex. : "US", "DE")                        |
| `language`    | Code de langue ISO 639-1 pour les résultats (ex. : "en", "de", "fr") |
| `ui_lang`     | Code de langue ISO pour les éléments de l'interface                 |
| `freshness`   | Filtre temporel : `day` (24h), `week`, `month`, ou `year`           |
| `date_after`  | Uniquement les résultats publiés après cette date (YYYY-MM-DD)      |
| `date_before` | Uniquement les résultats publiés avant cette date (YYYY-MM-DD)      |

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
```

## Notes

- OpenClaw utilise le plan Brave **Search**. Si vous avez un abonnement hérité (par exemple le plan Free original avec 2 000 requêtes/mois), il reste valide mais n'inclut pas les fonctionnalités plus récentes comme LLM Context ou des limites de débit plus élevées.
- Chaque plan Brave inclut **5 $/mois de crédit gratuit** (renouvelable). Le plan Search coûte 5 $ pour 1 000 requêtes, donc le crédit couvre 1 000 requêtes/mois. Définissez votre limite d'utilisation dans le tableau de bord Brave pour éviter les frais inattendus. Consultez le [portail API Brave](https://brave.com/search/api/) pour connaître les plans actuels.
- Le plan Search inclut le point de terminaison LLM Context et les droits d'inférence IA. Le stockage des résultats pour entraîner ou affiner des modèles nécessite un plan avec des droits de stockage explicites. Consultez les [Conditions d'utilisation](https://api-dashboard.search.brave.com/terms-of-service) de Brave.
- Les résultats sont mis en cache pendant 15 minutes par défaut (configurable via `cacheTtlMinutes`).

Consultez [Web tools](/tools/web) pour la configuration complète de web_search.
