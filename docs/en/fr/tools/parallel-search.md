---
summary: "Parallel Search -- Extraits denses optimisés pour LLM provenant de sources web"
read_when:
  - You want to use Parallel for web_search
  - You need a PARALLEL_API_KEY
  - You want dense excerpts ranked for LLM context efficiency
title: "Recherche Parallel"
---

OpenClaw supporte [Parallel](https://parallel.ai/) en tant que fournisseur `web_search`.
Parallel retourne des extraits denses classés et optimisés pour LLM provenant d'un index web
conçu spécifiquement pour les agents IA.

## Obtenir une clé API

<Steps>
  <Step title="Créer un compte">
    Inscrivez-vous sur [platform.parallel.ai](https://platform.parallel.ai) et
    générez une clé API depuis votre tableau de bord.
  </Step>
  <Step title="Stocker la clé">
    Définissez `PARALLEL_API_KEY` dans l'environnement Gateway, ou configurez via :

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
      parallel: {
        config: {
          webSearch: {
            apiKey: "par-...", // optionnel si PARALLEL_API_KEY est défini
            baseUrl: "https://api.parallel.ai", // optionnel ; OpenClaw ajoute /v1/search
          },
        },
      },
    },
  },
  tools: {
    web: {
      search: {
        provider: "parallel",
      },
    },
  },
}
```

**Alternative environnement :** définissez `PARALLEL_API_KEY` dans l'environnement Gateway.
Pour une installation gateway, placez-le dans `~/.openclaw/.env`.

## Remplacement de l'URL de base

Définissez `plugins.entries.parallel.config.webSearch.baseUrl` lorsque les requêtes Parallel
doivent passer par un proxy compatible ou un endpoint Parallel alternatif (par
exemple, la Cloudflare AI Gateway). OpenClaw normalise les hôtes simples en
ajoutant `https://` au début et ajoute `/v1/search` sauf si le chemin se termine déjà
là. L'endpoint résolu est inclus dans la clé de cache de recherche, donc les résultats
provenant de différents endpoints Parallel ne sont pas partagés.

## Paramètres de l'outil

OpenClaw expose la forme de recherche native de Parallel afin que le modèle puisse remplir à la fois
l'objectif en langage naturel et quelques requêtes de mots-clés courts — l'appairage que
Parallel [recommande](https://docs.parallel.ai/search/best-practices) pour
les meilleurs résultats.

<ParamField path="objective" type="string" required>
Description en langage naturel de la question ou de l'objectif sous-jacent (max 5000
caractères). Doit être autonome.
</ParamField>

<ParamField path="search_queries" type="string[]" required>
Requêtes de recherche par mots-clés concises, 3-6 mots chacune (1-5 entrées, max 200 caractères
chacune). Fournissez 2-3 requêtes diversifiées pour les meilleurs résultats.
</ParamField>

<ParamField path="count" type="number">
Résultats à retourner (1-40).
</ParamField>

<ParamField path="session_id" type="string">
ID de session Parallel optionnel (max 1000 caractères). Passez le `sessionId` d'un
résultat Parallel précédent lors de recherches de suivi qui font partie de la même tâche
afin que Parallel puisse regrouper les appels connexes et améliorer les résultats ultérieurs.
</ParamField>

<ParamField path="client_model" type="string">
Identifiant optionnel du modèle effectuant l'appel (par ex. `claude-opus-4-7`,
`gpt-5.5`). Permet à Parallel d'adapter les paramètres par défaut aux
capacités de votre modèle. Passez le slug de modèle actif exact ; ne raccourcissez pas vers un
alias de famille.
</ParamField>

## Notes

- Parallel classe et compresse les résultats en fonction de l'utilité du raisonnement LLM, et non
  des clics humains ; attendez-vous à des extraits denses dans chaque résultat plutôt qu'à
  du contenu de page complète
- Les extraits de résultats reviennent sous forme de tableau `excerpts` et sont également fusionnés dans
  le champ `description` pour la compatibilité avec le contrat générique `web_search`
- Parallel retourne un `session_id` à chaque réponse ; OpenClaw le surface en tant que
  `sessionId` dans la charge utile de l'outil afin que les appelants puissent regrouper les recherches de suivi
- `searchId`, `warnings`, et `usage` de Parallel sont transmis lorsqu'ils sont
  présents
- OpenClaw transmet toujours un nombre de résultats résolu à Parallel en tant que
  `advanced_settings.max_results`. L'argument `count` de l'appelant gagne, puis le
  paramètre de niveau supérieur `tools.web.search.maxResults`, sinon la
  valeur par défaut générique `web_search` d'OpenClaw (5). Cela maintient le volume de résultats cohérent
  lors du changement entre fournisseurs ; Parallel seul utilise par défaut 10
- Les résultats sont mis en cache pendant 15 minutes par défaut (configurable via
  `cacheTtlMinutes`)

## Connexes

- [Aperçu de Web Search](/fr/tools/web) -- tous les fournisseurs et détection automatique
- [Recherche Exa](/fr/tools/exa-search) -- recherche neuronale avec extraction de contenu
- [Recherche Perplexity](/fr/tools/perplexity-search) -- résultats structurés avec filtrage de domaine
