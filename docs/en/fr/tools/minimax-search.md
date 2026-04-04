---
summary: "Recherche MiniMax via l'API de recherche du Plan de Codage"
read_when:
  - You want to use MiniMax for web_search
  - You need a MiniMax Coding Plan key
  - You want MiniMax CN/global search host guidance
title: "Recherche MiniMax"
---

# Recherche MiniMax

OpenClaw supporte MiniMax en tant que fournisseur `web_search` via l'API de recherche du Plan de Codage MiniMax. Il retourne des résultats de recherche structurés avec titres, URLs, extraits et requêtes associées.

## Obtenir une clé du Plan de Codage

<Steps>
  <Step title="Créer une clé">
    Créez ou copiez une clé du Plan de Codage MiniMax depuis la
    [Plateforme MiniMax](https://platform.minimax.io/user-center/basic-information/interface-key).
  </Step>
  <Step title="Stocker la clé">
    Définissez `MINIMAX_CODE_PLAN_KEY` dans l'environnement de la Passerelle, ou configurez via :

    ```bash
    openclaw configure --section web
    ```

  </Step>
</Steps>

OpenClaw accepte également `MINIMAX_CODING_API_KEY` comme alias d'env. `MINIMAX_API_KEY`
est toujours lu comme fallback de compatibilité quand il pointe déjà vers un token du plan de codage.

## Configuration

```json5
{
  plugins: {
    entries: {
      minimax: {
        config: {
          webSearch: {
            apiKey: "sk-cp-...", // optionnel si MINIMAX_CODE_PLAN_KEY est défini
            region: "global", // ou "cn"
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "minimax",
      },
    },
  },
}
```

**Alternative d'environnement :** définissez `MINIMAX_CODE_PLAN_KEY` dans l'environnement de la Passerelle.
Pour une installation de passerelle, mettez-le dans `~/.openclaw/.env`.

## Sélection de région

La Recherche MiniMax utilise ces points de terminaison :

- Global : `https://api.minimax.io/v1/coding_plan/search`
- CN : `https://api.minimaxi.com/v1/coding_plan/search`

Si `plugins.entries.minimax.config.webSearch.region` n'est pas défini, OpenClaw résout
la région dans cet ordre :

1. `tools.web.search.minimax.region` / `webSearch.region` appartenant au plugin
2. `MINIMAX_API_HOST`
3. `models.providers.minimax.baseUrl`
4. `models.providers.minimax-portal.baseUrl`

Cela signifie que l'intégration CN ou `MINIMAX_API_HOST=https://api.minimaxi.com/...`
garde automatiquement la Recherche MiniMax sur l'hôte CN aussi.

Même si vous avez authentifié MiniMax via le chemin OAuth `minimax-portal`,
la recherche web s'enregistre toujours avec l'ID de fournisseur `minimax` ; l'URL de base du fournisseur OAuth
n'est utilisée que comme indice de région pour la sélection de l'hôte CN/global.

## Paramètres supportés

La Recherche MiniMax supporte :

- `query`
- `count` (OpenClaw réduit la liste des résultats retournés au nombre demandé)

Les filtres spécifiques au fournisseur ne sont actuellement pas supportés.

## Connexes

- [Aperçu de la Recherche Web](/fr/tools/web) -- tous les fournisseurs et détection automatique
- [MiniMax](/fr/providers/minimax) -- configuration du modèle, image, parole et authentification
