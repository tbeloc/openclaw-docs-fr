---
summary: "Outils de recherche web + récupération (fournisseurs Brave, Gemini, Grok, Kimi et Perplexity)"
read_when:
  - You want to enable web_search or web_fetch
  - You need provider API key setup
  - You want to use Gemini with Google Search grounding
title: "Outils Web"
---

# Outils web

OpenClaw propose deux outils web légers :

- `web_search` — Recherchez le web en utilisant l'API Brave Search, Gemini avec Google Search grounding, Grok, Kimi ou l'API Perplexity Search.
- `web_fetch` — Récupération HTTP + extraction lisible (HTML → markdown/texte).

Ce ne sont **pas** des outils d'automatisation de navigateur. Pour les sites lourds en JS ou les connexions, utilisez l'
[outil Browser](/tools/browser).

## Fonctionnement

- `web_search` appelle votre fournisseur configuré et retourne les résultats.
- Les résultats sont mis en cache par requête pendant 15 minutes (configurable).
- `web_fetch` effectue une simple requête HTTP GET et extrait le contenu lisible
  (HTML → markdown/texte). Il n'exécute **pas** JavaScript.
- `web_fetch` est activé par défaut (sauf désactivation explicite).

Consultez [Configuration Brave Search](/brave-search) et [Configuration Perplexity Search](/perplexity) pour les détails spécifiques aux fournisseurs.

## Choisir un fournisseur de recherche

| Fournisseur               | Format des résultats               | Filtres spécifiques au fournisseur             | Notes                                                                          | Clé API                                     |
| ------------------------- | ---------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------- |
| **API Brave Search**      | Résultats structurés avec extraits | `country`, `language`, `ui_lang`, heure       | Supporte le mode Brave `llm-context`                                           | `BRAVE_API_KEY`                             |
| **Gemini**                | Réponses synthétisées par IA + citations | —                                            | Utilise Google Search grounding                                                | `GEMINI_API_KEY`                            |
| **Grok**                  | Réponses synthétisées par IA + citations | —                                            | Utilise les réponses web-grounded de xAI                                       | `XAI_API_KEY`                               |
| **Kimi**                  | Réponses synthétisées par IA + citations | —                                            | Utilise la recherche web Moonshot                                              | `KIMI_API_KEY` / `MOONSHOT_API_KEY`         |
| **API Perplexity Search** | Résultats structurés avec extraits | `country`, `language`, heure, `domain_filter` | Supporte les contrôles d'extraction de contenu ; OpenRouter utilise le chemin de compatibilité Sonar | `PERPLEXITY_API_KEY` / `OPENROUTER_API_KEY` |

### Détection automatique

Le tableau ci-dessus est alphabétique. Si aucun `provider` n'est explicitement défini, la détection automatique à l'exécution vérifie les fournisseurs dans cet ordre :

1. **Brave** — Variable d'environnement `BRAVE_API_KEY` ou configuration `tools.web.search.apiKey`
2. **Gemini** — Variable d'environnement `GEMINI_API_KEY` ou configuration `tools.web.search.gemini.apiKey`
3. **Grok** — Variable d'environnement `XAI_API_KEY` ou configuration `tools.web.search.grok.apiKey`
4. **Kimi** — Variable d'environnement `KIMI_API_KEY` / `MOONSHOT_API_KEY` ou configuration `tools.web.search.kimi.apiKey`
5. **Perplexity** — `PERPLEXITY_API_KEY`, `OPENROUTER_API_KEY`, ou configuration `tools.web.search.perplexity.apiKey`

Si aucune clé n'est trouvée, il revient à Brave (vous obtiendrez une erreur de clé manquante vous invitant à en configurer une).

Comportement de SecretRef à l'exécution :

- Les SecretRefs des outils web sont résolus de manière atomique au démarrage/rechargement de la passerelle.
- En mode auto-détection, OpenClaw résout uniquement la clé du fournisseur sélectionné. Les SecretRefs des fournisseurs non sélectionnés restent inactifs jusqu'à sélection.
- Si le SecretRef du fournisseur sélectionné n'est pas résolu et qu'aucun fallback d'environnement du fournisseur n'existe, le démarrage/rechargement échoue rapidement.

## Configuration de la recherche web

Utilisez `openclaw configure --section web` pour configurer votre clé API et choisir un fournisseur.

### Brave Search

1. Créez un compte Brave Search API sur [brave.com/search/api](https://brave.com/search/api/)
2. Dans le tableau de bord, choisissez le plan **Search** et générez une clé API.
3. Exécutez `openclaw configure --section web` pour stocker la clé dans la configuration, ou définissez `BRAVE_API_KEY` dans votre environnement.

Chaque plan Brave inclut **5 $/mois de crédit gratuit** (renouvelable). Le plan Search
coûte 5 $ pour 1 000 requêtes, donc le crédit couvre 1 000 requêtes/mois. Définissez
votre limite d'utilisation dans le tableau de bord Brave pour éviter les frais inattendus. Consultez le
[portail API Brave](https://brave.com/search/api/) pour les plans et
tarifs actuels.

### Perplexity Search

1. Créez un compte Perplexity sur [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
2. Générez une clé API dans le tableau de bord
3. Exécutez `openclaw configure --section web` pour stocker la clé dans la configuration, ou définissez `PERPLEXITY_API_KEY` dans votre environnement.

Pour la compatibilité héritée Sonar/OpenRouter, définissez `OPENROUTER_API_KEY` à la place, ou configurez `tools.web.search.perplexity.apiKey` avec une clé `sk-or-...`. La définition de `tools.web.search.perplexity.baseUrl` ou `model` fait également revenir Perplexity au chemin de compatibilité chat-completions.

Consultez la [Documentation API Perplexity Search](https://docs.perplexity.ai/guides/search-quickstart) pour plus de détails.

### Où stocker la clé

**Via configuration :** exécutez `openclaw configure --section web`. Elle stocke la clé sous le chemin de configuration spécifique au fournisseur :

- Brave: `tools.web.search.apiKey`
- Gemini: `tools.web.search.gemini.apiKey`
- Grok: `tools.web.search.grok.apiKey`
- Kimi: `tools.web.search.kimi.apiKey`
- Perplexity: `tools.web.search.perplexity.apiKey`

Tous ces champs supportent également les objets SecretRef.

**Via environnement :** définissez les variables d'environnement du fournisseur dans l'environnement du processus Gateway :

- Brave: `BRAVE_API_KEY`
- Gemini: `GEMINI_API_KEY`
- Grok: `XAI_API_KEY`
- Kimi: `KIMI_API_KEY` ou `MOONSHOT_API_KEY`
- Perplexity: `PERPLEXITY_API_KEY` ou `OPENROUTER_API_KEY`

Pour une installation de passerelle, mettez-les dans `~/.openclaw/.env` (ou votre environnement de service). Consultez [Variables d'environnement](/help/faq#how-does-openclaw-load-environment-variables).

### Exemples de configuration

**Brave Search :**

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        provider: "brave",
        apiKey: "YOUR_BRAVE_API_KEY", // optional if BRAVE_API_KEY is set // pragma: allowlist secret
      },
    },
  },
}
```

**Mode Brave LLM Context :**

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        provider: "brave",
        apiKey: "YOUR_BRAVE_API_KEY", // optional if BRAVE_API_KEY is set // pragma: allowlist secret
        brave: {
          mode: "llm-context",
        },
      },
    },
  },
}
```

`llm-context` retourne des chunks de page extraits pour le grounding au lieu des extraits Brave standard.
Dans ce mode, `country` et `language` / `search_lang` fonctionnent toujours, mais `ui_lang`,
`freshness`, `date_after`, et `date_before` sont rejetés.

**Perplexity Search :**

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...", // optional if PERPLEXITY_API_KEY is set
        },
      },
    },
  },
}
```

**Perplexity via OpenRouter / Compatibilité Sonar :**

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        provider: "perplexity",
        perplexity: {
          apiKey: "<openrouter-api-key>", // optional if OPENROUTER_API_KEY is set
          baseUrl: "https://openrouter.ai/api/v1",
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

## Utiliser Gemini (Google Search grounding)

Les modèles Gemini supportent le [Google Search grounding](https://ai.google.dev/gemini-api/docs/grounding) intégré,
qui retourne des réponses synthétisées par IA soutenues par les résultats de recherche Google en direct avec citations.

### Obtenir une clé API Gemini

1. Allez sur [Google AI Studio](https://aistudio.google.com/apikey)
2. Créez une clé API
3. Définissez `GEMINI_API_KEY` dans l'environnement de la passerelle, ou configurez `tools.web.search.gemini.apiKey`

### Configuration de la recherche Gemini

```json5
{
  tools: {
    web: {
      search: {
        provider: "gemini",
        gemini: {
          // Clé API (optionnelle si GEMINI_API_KEY est défini)
          apiKey: "AIza...",
          // Modèle (par défaut "gemini-2.5-flash")
          model: "gemini-2.5-flash",
        },
      },
    },
  },
}
```

**Alternative environnement :** définissez `GEMINI_API_KEY` dans l'environnement de la passerelle.
Pour une installation de passerelle, mettez-le dans `~/.openclaw/.env`.

### Notes

- Les URL de citation du grounding Gemini sont automatiquement résolues à partir des URL de redirection de Google vers les URL directes.
- La résolution de redirection utilise le chemin de protection SSRF (vérifications HEAD + redirection + validation http/https) avant de retourner l'URL de citation finale.
- La résolution de redirection utilise les paramètres SSRF stricts par défaut, donc les redirections vers des cibles privées/internes sont bloquées.
- Le modèle par défaut (`gemini-2.5-flash`) est rapide et rentable.
  N'importe quel modèle Gemini qui supporte le grounding peut être utilisé.

## web_search

Recherchez le web en utilisant votre fournisseur configuré.

### Exigences

- `tools.web.search.enabled` ne doit pas être `false` (par défaut : activé)
- Clé API pour votre fournisseur choisi :
  - **Brave**: `BRAVE_API_KEY` ou `tools.web.search.apiKey`
  - **Gemini**: `GEMINI_API_KEY` ou `tools.web.search.gemini.apiKey`
  - **Grok**: `XAI_API_KEY` ou `tools.web.search.grok.apiKey`
  - **Kimi**: `KIMI_API_KEY`, `MOONSHOT_API_KEY`, ou `tools.web.search.kimi.apiKey`
  - **Perplexity**: `PERPLEXITY_API_KEY`, `OPENROUTER_API_KEY`, ou `tools.web.search.perplexity.apiKey`
- Tous les champs de clé de fournisseur ci-dessus supportent les objets SecretRef.

### Configuration

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        apiKey: "BRAVE_API_KEY_HERE", // optional if BRAVE_API_KEY is set
        maxResults: 5,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
      },
    },
  },
}
```

### Paramètres de l'outil

Tous les paramètres fonctionnent pour Brave et pour l'API Perplexity Search native sauf indication contraire.

Le chemin de compatibilité OpenRouter / Sonar de Perplexity ne supporte que `query` et `freshness`.
Si vous définissez `tools.web.search.perplexity.baseUrl` / `model`, utilisez `OPENROUTER_API_KEY`, ou configurez une clé `sk-or-...`, les filtres spécifiques à l'API Search retournent des erreurs explicites.

| Paramètre             | Description                                           |
| --------------------- | ----------------------------------------------------- |
| `query`               | Requête de recherche (obligatoire)                    |
| `count`               | Résultats à retourner (1-10, par défaut : 5)          |
| `country`             | Code pays ISO à 2 lettres (ex. "US", "DE")            |
| `language`            | Code langue ISO 639-1 (ex. "en", "de")                |
| `freshness`           | Filtre temporel : `day`, `week`, `month`, ou `year`   |
| `date_after`          | Résultats après cette date (YYYY-MM-DD)               |
| `date_before`         | Résultats avant cette date (YYYY-MM-DD)               |
| `ui_lang`             | Code langue UI (Brave uniquement)                     |
| `domain_filter`       | Tableau liste blanche/noire de domaines (Perplexity
