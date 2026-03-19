---
title: "Perplexity (Fournisseur)"
summary: "Configuration du fournisseur de recherche web Perplexity (clé API, modes de recherche, filtrage)"
read_when:
  - Vous souhaitez configurer Perplexity comme fournisseur de recherche web
  - Vous avez besoin de la clé API Perplexity ou de la configuration du proxy OpenRouter
---

# Perplexity (Fournisseur de recherche web)

Le plugin Perplexity fournit des capacités de recherche web via l'API Perplexity
Search ou Perplexity Sonar via OpenRouter.

<Note>
Cette page couvre la configuration du **fournisseur** Perplexity. Pour l'**outil**
Perplexity (comment l'agent l'utilise), voir [Outil Perplexity](/fr/perplexity).
</Note>

- Type : fournisseur de recherche web (pas un fournisseur de modèle)
- Authentification : `PERPLEXITY_API_KEY` (direct) ou `OPENROUTER_API_KEY` (via OpenRouter)
- Chemin de configuration : `tools.web.search.perplexity.apiKey`

## Démarrage rapide

1. Définissez la clé API :

```bash
openclaw config set tools.web.search.perplexity.apiKey "pplx-xxxxxxxxxxxx"
```

2. L'agent utilisera automatiquement Perplexity pour les recherches web une fois configuré.

## Modes de recherche

Le plugin sélectionne automatiquement le transport en fonction du préfixe de la clé API :

| Préfixe de clé | Transport                    | Fonctionnalités                                  |
| -------------- | ---------------------------- | ------------------------------------------------ |
| `pplx-`        | API Perplexity Search native | Résultats structurés, filtres domaine/langue/date |
| `sk-or-`       | OpenRouter (Sonar)           | Réponses synthétisées par IA avec citations      |

## Filtrage de l'API native

Lors de l'utilisation de l'API Perplexity native (clé `pplx-`), les recherches supportent :

- **Pays** : code pays à 2 lettres
- **Langue** : code langue ISO 639-1
- **Plage de dates** : jour, semaine, mois, année
- **Filtres de domaine** : liste blanche/liste noire (max 20 domaines)
- **Budget de contenu** : `max_tokens`, `max_tokens_per_page`

## Note sur l'environnement

Si la Gateway s'exécute en tant que daemon (launchd/systemd), assurez-vous que
`PERPLEXITY_API_KEY` est disponible pour ce processus (par exemple, dans
`~/.openclaw/.env` ou via `env.shellEnv`).
