---
summary: "Recherche web SearXNG -- fournisseur de méta-recherche auto-hébergé, sans clé"
read_when:
  - You want a self-hosted web search provider
  - You want to use SearXNG for web_search
  - You need a privacy-focused or air-gapped search option
title: "Recherche SearXNG"
---

# Recherche SearXNG

OpenClaw supporte [SearXNG](https://docs.searxng.org/) comme fournisseur `web_search` **auto-hébergé, sans clé**. SearXNG est un moteur de méta-recherche open-source qui agrège les résultats de Google, Bing, DuckDuckGo et d'autres sources.

Avantages :

- **Gratuit et illimité** -- aucune clé API ou abonnement commercial requis
- **Confidentialité / air-gap** -- les requêtes ne quittent jamais votre réseau
- **Fonctionne partout** -- aucune restriction régionale sur les API de recherche commerciales

## Configuration

<Steps>
  <Step title="Exécuter une instance SearXNG">
    ```bash
    docker run -d -p 8888:8080 searxng/searxng
    ```

    Ou utilisez n'importe quel déploiement SearXNG existant auquel vous avez accès. Consultez la
    [documentation SearXNG](https://docs.searxng.org/) pour la configuration en production.

  </Step>
  <Step title="Configurer">
    ```bash
    openclaw configure --section web
    # Sélectionnez "searxng" comme fournisseur
    ```

    Ou définissez la variable d'environnement et laissez la détection automatique la trouver :

    ```bash
    export SEARXNG_BASE_URL="http://localhost:8888"
    ```

  </Step>
</Steps>

## Config

```json5
{
  tools: {
    web: {
      search: {
        provider: "searxng",
      },
    },
  },
}
```

Paramètres au niveau du plugin pour l'instance SearXNG :

```json5
{
  plugins: {
    entries: {
      searxng: {
        config: {
          webSearch: {
            baseUrl: "http://localhost:8888",
            categories: "general,news", // optionnel
            language: "en", // optionnel
          },
        },
      },
    },
  },
}
```

Le champ `baseUrl` accepte également les objets SecretRef.

## Variable d'environnement

Définissez `SEARXNG_BASE_URL` comme alternative à la configuration :

```bash
export SEARXNG_BASE_URL="http://localhost:8888"
```

Lorsque `SEARXNG_BASE_URL` est défini et qu'aucun fournisseur explicite n'est configuré, la détection automatique
choisit SearXNG automatiquement (avec la priorité la plus basse -- tout fournisseur basé sur une API avec une
clé gagne en premier).

## Référence de configuration du plugin

| Champ        | Description                                                        |
| ------------ | ------------------------------------------------------------------ |
| `baseUrl`    | URL de base de votre instance SearXNG (requis)                     |
| `categories` | Catégories séparées par des virgules telles que `general`, `news`, ou `science` |
| `language`   | Code de langue pour les résultats tels que `en`, `de`, ou `fr`     |

## Notes

- **API JSON** -- utilise le point de terminaison natif `format=json` de SearXNG, pas le scraping HTML
- **Pas de clé API** -- fonctionne avec n'importe quelle instance SearXNG prête à l'emploi
- **Ordre de détection automatique** -- SearXNG est vérifié en dernier (ordre 200) dans la détection automatique,
  donc tout fournisseur basé sur une API avec une clé a priorité sur SearXNG, et SearXNG se situe
  derrière DuckDuckGo (ordre 100) également
- **Auto-hébergé** -- vous contrôlez l'instance, les requêtes et les moteurs de recherche en amont
- **Catégories** par défaut à `general` lorsqu'elles ne sont pas configurées

<Tip>
  Pour que l'API JSON de SearXNG fonctionne, assurez-vous que votre instance SearXNG a le format `json`
  activé dans son `settings.yml` sous `search.formats`.
</Tip>

## Connexes

- [Aperçu de la recherche web](/fr/tools/web) -- tous les fournisseurs et détection automatique
- [Recherche DuckDuckGo](/fr/tools/duckduckgo-search) -- un autre secours sans clé
- [Recherche Brave](/fr/tools/brave-search) -- résultats structurés avec niveau gratuit
