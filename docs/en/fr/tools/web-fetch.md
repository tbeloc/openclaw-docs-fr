---
summary: "outil web_fetch -- Récupération HTTP avec extraction de contenu lisible"
read_when:
  - You want to fetch a URL and extract readable content
  - You need to configure web_fetch or its Firecrawl fallback
  - You want to understand web_fetch limits and caching
title: "Web Fetch"
sidebarTitle: "Web Fetch"
---

# Web Fetch

L'outil `web_fetch` effectue une simple requête HTTP GET et extrait le contenu lisible
(HTML en markdown ou texte). Il n'exécute **pas** JavaScript.

Pour les sites lourds en JS ou les pages protégées par connexion, utilisez plutôt le
[Web Browser](/fr/tools/browser).

## Démarrage rapide

`web_fetch` est **activé par défaut** -- aucune configuration nécessaire. L'agent peut
l'appeler immédiatement :

```javascript
await web_fetch({ url: "https://example.com/article" });
```

## Paramètres de l'outil

| Paramètre     | Type     | Description                              |
| ------------- | -------- | ---------------------------------------- |
| `url`         | `string` | URL à récupérer (obligatoire, http/https uniquement) |
| `extractMode` | `string` | `"markdown"` (par défaut) ou `"text"`       |
| `maxChars`    | `number` | Tronquer la sortie à ce nombre de caractères       |

## Fonctionnement

<Steps>
  <Step title="Récupération">
    Envoie une requête HTTP GET avec un User-Agent de type Chrome et un en-tête
    `Accept-Language`. Bloque les noms d'hôte privés/internes et revérifie les redirections.
  </Step>
  <Step title="Extraction">
    Exécute Readability (extraction du contenu principal) sur la réponse HTML.
  </Step>
  <Step title="Secours (optionnel)">
    Si Readability échoue et que Firecrawl est configuré, réessaie via l'API
    Firecrawl avec le mode de contournement de bot.
  </Step>
  <Step title="Cache">
    Les résultats sont mis en cache pendant 15 minutes (configurable) pour réduire les
    récupérations répétées de la même URL.
  </Step>
</Steps>

## Configuration

```json5
{
  tools: {
    web: {
      fetch: {
        enabled: true, // par défaut : true
        maxChars: 50000, // max caractères de sortie
        maxCharsCap: 50000, // limite stricte pour le paramètre maxChars
        maxResponseBytes: 2000000, // taille max de téléchargement avant troncature
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
        maxRedirects: 3,
        readability: true, // utiliser l'extraction Readability
        userAgent: "Mozilla/5.0 ...", // remplacer User-Agent
      },
    },
  },
}
```

## Secours Firecrawl

Si l'extraction Readability échoue, `web_fetch` peut basculer vers
[Firecrawl](/fr/tools/firecrawl) pour le contournement de bot et une meilleure extraction :

```json5
{
  tools: {
    web: {
      fetch: {
        firecrawl: {
          enabled: true,
          apiKey: "fc-...", // optionnel si FIRECRAWL_API_KEY est défini
          baseUrl: "https://api.firecrawl.dev",
          onlyMainContent: true,
          maxAgeMs: 86400000, // durée du cache (1 jour)
          timeoutSeconds: 60,
        },
      },
    },
  },
}
```

`tools.web.fetch.firecrawl.apiKey` supporte les objets SecretRef.

<Note>
  Si Firecrawl est activé et que sa SecretRef n'est pas résolue sans secours
  à la variable d'environnement `FIRECRAWL_API_KEY`, le démarrage de la passerelle échoue rapidement.
</Note>

## Limites et sécurité

- `maxChars` est limité à `tools.web.fetch.maxCharsCap`
- Le corps de la réponse est plafonné à `maxResponseBytes` avant l'analyse ; les réponses surdimensionnées
  sont tronquées avec un avertissement
- Les noms d'hôte privés/internes sont bloqués
- Les redirections sont vérifiées et limitées par `maxRedirects`
- `web_fetch` est au mieux effort -- certains sites nécessitent le [Web Browser](/fr/tools/browser)

## Profils d'outils

Si vous utilisez des profils d'outils ou des listes d'autorisation, ajoutez `web_fetch` ou `group:web` :

```json5
{
  tools: {
    allow: ["web_fetch"],
    // ou : allow: ["group:web"]  (inclut web_fetch et web_search)
  },
}
```

## Connexes

- [Web Search](/fr/tools/web) -- rechercher le web avec plusieurs fournisseurs
- [Web Browser](/fr/tools/browser) -- automatisation complète du navigateur pour les sites lourds en JS
- [Firecrawl](/fr/tools/firecrawl) -- outils de recherche et scraping Firecrawl
