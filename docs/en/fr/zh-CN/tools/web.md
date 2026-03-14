---
read_when:
  - Vous souhaitez activer web_search ou web_fetch
  - Vous devez configurer la clé API Brave Search
  - Vous souhaitez utiliser Perplexity Sonar pour la recherche web
summary: Outils de recherche web + récupération (Brave Search API, Perplexity direct/OpenRouter)
title: Outils Web
x-i18n:
  generated_at: "2026-02-03T10:12:43Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 760b706cc966cb421e370f10f8e76047f8ca9fe0a106d90c05d979976789465a
  source_path: tools/web.md
  workflow: 15
---

# Outils Web

OpenClaw fournit deux outils Web légers :

- `web_search` — Recherchez le web via l'API Brave Search (par défaut) ou Perplexity Sonar (direct ou via OpenRouter).
- `web_fetch` — Récupération HTTP + extraction de lisibilité (HTML → markdown/texte).

Ce ne sont **pas** des outils d'automatisation de navigateur. Pour les sites gourmands en JS ou nécessitant une connexion, utilisez l'[outil navigateur](/tools/browser).

## Fonctionnement

- `web_search` appelle le fournisseur que vous avez configuré et retourne les résultats.
  - **Brave** (par défaut) : retourne des résultats structurés (titre, URL, résumé).
  - **Perplexity** : retourne une réponse synthétisée par IA avec citations de recherche web en temps réel.
- Les résultats sont mis en cache par requête pendant 15 minutes (configurable).
- `web_fetch` effectue une requête HTTP GET ordinaire et extrait le contenu lisible (HTML → markdown/texte). Il **n'exécute pas** JavaScript.
- `web_fetch` est activé par défaut (sauf désactivation explicite).

## Choisir un fournisseur de recherche

| Fournisseur       | Avantages                      | Inconvénients                              | Clé API                                      |
| ----------------- | ------------------------------ | ------------------------------------------ | -------------------------------------------- |
| **Brave** (défaut) | Rapide, résultats structurés, couche gratuite | Résultats de recherche traditionnels | `BRAVE_API_KEY`                              |
| **Perplexity**    | Réponses synthétisées par IA, citations, temps réel | Nécessite accès Perplexity ou OpenRouter | `OPENROUTER_API_KEY` ou `PERPLEXITY_API_KEY` |

Consultez [Configuration Brave Search](/brave-search) et [Perplexity Sonar](/perplexity) pour les détails spécifiques au fournisseur.

Définissez le fournisseur dans la configuration :

```json5
{
  tools: {
    web: {
      search: {
        provider: "brave", // ou "perplexity"
      },
    },
  },
}
```

Exemple : basculer vers Perplexity Sonar (API direct) :

```json5
{
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...",
          baseUrl: "https://api.perplexity.ai",
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

## Obtenir une clé API Brave

1. Créez un compte Brave Search API sur https://brave.com/search/api/
2. Dans le tableau de bord, sélectionnez le plan **Data for Search** (pas "Data for AI") et générez une clé API.
3. Exécutez `openclaw configure --section web` pour stocker la clé dans la configuration (recommandé), ou définissez `BRAVE_API_KEY` dans l'environnement.

Brave offre une couche gratuite et des plans payants ; consultez le portail API Brave pour les limites et tarifs actuels.

### Où définir la clé (recommandé)

**Recommandé :** Exécutez `openclaw configure --section web`. Elle stockera la clé sous `tools.web.search.apiKey` dans `~/.openclaw/openclaw.json`.

**Alternative avec variable d'environnement :** Définissez `BRAVE_API_KEY` dans l'environnement du processus Gateway. Pour les installations Gateway, placez-la dans `~/.openclaw/.env` (ou votre environnement de service). Consultez [Variables d'environnement](/help/faq#how-does-openclaw-load-environment-variables).

## Utiliser Perplexity (direct ou via OpenRouter)

Les modèles Perplexity Sonar disposent d'une recherche web intégrée et retournent des réponses synthétisées par IA avec citations. Vous pouvez les utiliser via OpenRouter (sans carte de crédit - accepte crypto/prépayé).

### Obtenir une clé API OpenRouter

1. Créez un compte sur https://openrouter.ai/
2. Ajoutez des crédits (accepte crypto, prépayé ou carte de crédit)
3. Générez une clé API dans les paramètres du compte

### Configurer la recherche Perplexity

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        provider: "perplexity",
        perplexity: {
          // Clé API (optionnelle si OPENROUTER_API_KEY ou PERPLEXITY_API_KEY est défini)
          apiKey: "sk-or-v1-...",
          // URL de base (par défaut selon la clé si omis)
          baseUrl: "https://openrouter.ai/api/v1",
          // Modèle (par défaut perplexity/sonar-pro)
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

**Alternative avec variable d'environnement :** Définissez `OPENROUTER_API_KEY` ou `PERPLEXITY_API_KEY` dans l'environnement Gateway. Pour les installations Gateway, placez-la dans `~/.openclaw/.env`.

Si l'URL de base n'est pas définie, OpenClaw choisit une valeur par défaut selon la source de la clé API :

- `PERPLEXITY_API_KEY` ou `pplx-...` → `https://api.perplexity.ai`
- `OPENROUTER_API_KEY` ou `sk-or-...` → `https://openrouter.ai/api/v1`
- Format de clé inconnu → OpenRouter (repli sécurisé)

### Modèles Perplexity disponibles

| Modèle                           | Description                  | Meilleur pour |
| -------------------------------- | ---------------------------- | ------------- |
| `perplexity/sonar`               | Q&A rapide avec recherche web | Requêtes rapides |
| `perplexity/sonar-pro` (défaut)  | Raisonnement multi-étapes avec recherche web | Problèmes complexes |
| `perplexity/sonar-reasoning-pro` | Analyse avec chaîne de pensée | Recherche approfondie |

## web_search

Recherchez le web en utilisant le fournisseur configuré.

### Exigences

- `tools.web.search.enabled` ne peut pas être `false` (par défaut : activé)
- Clé API du fournisseur sélectionné :
  - **Brave** : `BRAVE_API_KEY` ou `tools.web.search.apiKey`
  - **Perplexity** : `OPENROUTER_API_KEY`, `PERPLEXITY_API_KEY` ou `tools.web.search.perplexity.apiKey`

### Configuration

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        apiKey: "BRAVE_API_KEY_HERE", // Optionnel si BRAVE_API_KEY est défini
        maxResults: 5,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
      },
    },
  },
}
```

### Paramètres de l'outil

- `query` (obligatoire)
- `count` (1–10 ; par défaut depuis la configuration)
- `country` (optionnel) : code pays à 2 lettres pour les résultats spécifiques à une région (par ex. "DE", "US", "ALL"). Si omis, Brave choisit sa région par défaut.
- `search_lang` (optionnel) : code de langue ISO pour les résultats de recherche (par ex. "de", "en", "fr")
- `ui_lang` (optionnel) : code de langue ISO pour les éléments de l'interface
- `freshness` (optionnel, Brave uniquement) : filtrer par date de découverte (`pd`, `pw`, `pm`, `py` ou `YYYY-MM-DDtoYYYY-MM-DD`)

**Exemples :**

```javascript
// Recherche spécifique à l'Allemagne
await web_search({
  query: "TV online schauen",
  count: 10,
  country: "DE",
  search_lang: "de",
});

// Recherche en français avec interface en français
await web_search({
  query: "actualités",
  country: "FR",
  search_lang: "fr",
  ui_lang: "fr",
});

// Résultats récents (dernière semaine)
await web_search({
  query: "TMBG interview",
  freshness: "pw",
});
```

## web_fetch

Récupérez une URL et extrayez le contenu lisible.

### Exigences

- `tools.web.fetch.enabled` ne peut pas être `false` (par défaut : activé)
- Repli Firecrawl optionnel : définissez `tools.web.fetch.firecrawl.apiKey` ou `FIRECRAWL_API_KEY`.

### Configuration

```json5
{
  tools: {
    web: {
      fetch: {
        enabled: true,
        maxChars: 50000,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
        maxRedirects: 3,
        userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        readability: true,
        firecrawl: {
          enabled: true,
          apiKey: "FIRECRAWL_API_KEY_HERE", // Optionnel si FIRECRAWL_API_KEY est défini
          baseUrl: "https://api.firecrawl.dev",
          onlyMainContent: true,
          maxAgeMs: 86400000, // millisecondes (1 jour)
          timeoutSeconds: 60,
        },
      },
    },
  },
}
```

### Paramètres de l'outil

- `url` (obligatoire, http/https uniquement)
- `extractMode` (`markdown` | `text`)
- `maxChars` (tronquer les pages longues)

Remarques :

- `web_fetch` utilise d'abord Readability (extraction du contenu principal), puis Firecrawl (si configuré). Si les deux échouent, l'outil retourne une erreur.
- Les requêtes Firecrawl utilisent le mode d'évitement des robots et mettent en cache les résultats par défaut.
- `web_fetch` envoie par défaut un User-Agent de type Chrome et `Accept-Language` ; vous pouvez remplacer `userAgent` si nécessaire.
- `web_fetch` bloque les noms d'hôtes privés/internes et revérifie les redirections (limitées avec `maxRedirects`).
- `web_fetch` est un meilleur effort ; certains sites nécessitent l'outil navigateur.
- Consultez [Firecrawl](/tools/firecrawl) pour les détails de configuration des clés et du service.
- Les réponses sont mises en cache (15 minutes par défaut) pour réduire les récupérations répétées.
- Si vous utilisez un fichier de configuration d'outils/liste d'autorisation, ajoutez `web_search`/`web_fetch` ou `group:web`.
- Si la clé Brave est manquante, `web_search` retourne un court conseil de configuration et un lien de documentation.
