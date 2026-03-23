---
summary: "Recherche web Kimi via recherche web Moonshot"
read_when:
  - Vous voulez utiliser Kimi pour web_search
  - Vous avez besoin d'une KIMI_API_KEY ou MOONSHOT_API_KEY
title: "Recherche Kimi"
---

# Recherche Kimi

OpenClaw supporte Kimi en tant que fournisseur `web_search`, utilisant la recherche web Moonshot
pour produire des réponses synthétisées par IA avec citations.

## Obtenir une clé API

<Steps>
  <Step title="Créer une clé">
    Obtenez une clé API auprès de [Moonshot AI](https://platform.moonshot.cn/).
  </Step>
  <Step title="Stocker la clé">
    Définissez `KIMI_API_KEY` ou `MOONSHOT_API_KEY` dans l'environnement de la passerelle, ou
    configurez via :

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
      moonshot: {
        config: {
          webSearch: {
            apiKey: "sk-...", // optionnel si KIMI_API_KEY ou MOONSHOT_API_KEY est défini
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "kimi",
      },
    },
  },
}
```

**Alternative environnement :** définissez `KIMI_API_KEY` ou `MOONSHOT_API_KEY` dans l'environnement de la
passerelle. Pour une installation de passerelle, mettez-le dans `~/.openclaw/.env`.

## Fonctionnement

Kimi utilise la recherche web Moonshot pour synthétiser des réponses avec des citations intégrées,
similaire à l'approche de réponse ancrée de Gemini et Grok.

## Paramètres supportés

La recherche Kimi supporte les paramètres standard `query` et `count`.
Les filtres spécifiques au fournisseur ne sont actuellement pas supportés.

## Connexes

- [Aperçu de la recherche web](/fr/tools/web) -- tous les fournisseurs et détection automatique
- [Recherche Gemini](/fr/tools/gemini-search) -- réponses synthétisées par IA via ancrage Google
- [Recherche Grok](/fr/tools/grok-search) -- réponses synthétisées par IA via ancrage xAI
