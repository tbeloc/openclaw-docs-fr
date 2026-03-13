---
read_when:
  - Vous souhaitez utiliser Brave Search pour web_search
  - Vous avez besoin de BRAVE_API_KEY ou des détails du plan
summary: Configuration de l'API Brave Search pour web_search
title: Brave Search
x-i18n:
  generated_at: "2026-02-03T07:43:09Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: cdcb037b092b8a10609f02acf062b4164cb826ac22bdb3fb2909c842a1405341
  source_path: brave-search.md
  workflow: 15
---

# API Brave Search

OpenClaw utilise Brave Search comme fournisseur par défaut pour `web_search`.

## Obtenir une clé API

1. Créez un compte Brave Search API sur https://brave.com/search/api/
2. Dans le tableau de bord, sélectionnez le plan **Data for Search** et générez une clé API.
3. Stockez la clé dans votre configuration (recommandé), ou définissez `BRAVE_API_KEY` dans l'environnement de la passerelle Gateway.

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

## Remarques importantes

- Le plan Data for AI n'est **pas** compatible avec `web_search`.
- Brave propose un niveau gratuit et des plans payants ; consultez le portail API Brave pour connaître les limites actuelles.

Consultez [Web Tools](/tools/web) pour la configuration complète de web_search.
