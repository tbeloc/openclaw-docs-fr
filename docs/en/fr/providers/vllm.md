---
summary: "Exécuter OpenClaw avec vLLM (serveur local compatible OpenAI)"
read_when:
  - Vous souhaitez exécuter OpenClaw contre un serveur vLLM local
  - Vous souhaitez des points de terminaison /v1 compatibles OpenAI avec vos propres modèles
title: "vLLM"
---

# vLLM

vLLM peut servir des modèles open-source (et certains modèles personnalisés) via une API HTTP **compatible OpenAI**. OpenClaw peut se connecter à vLLM en utilisant l'API `openai-completions`.

OpenClaw peut également **découvrir automatiquement** les modèles disponibles à partir de vLLM lorsque vous acceptez avec `VLLM_API_KEY` (n'importe quelle valeur fonctionne si votre serveur n'applique pas l'authentification) et que vous ne définissez pas d'entrée `models.providers.vllm` explicite.

## Démarrage rapide

1. Démarrez vLLM avec un serveur compatible OpenAI.

Votre URL de base doit exposer les points de terminaison `/v1` (par exemple `/v1/models`, `/v1/chat/completions`). vLLM s'exécute généralement sur :

- `http://127.0.0.1:8000/v1`

2. Acceptez (n'importe quelle valeur fonctionne si aucune authentification n'est configurée) :

```bash
export VLLM_API_KEY="vllm-local"
```

3. Sélectionnez un modèle (remplacez par l'un de vos ID de modèle vLLM) :

```json5
{
  agents: {
    defaults: {
      model: { primary: "vllm/your-model-id" },
    },
  },
}
```

## Découverte de modèles (fournisseur implicite)

Lorsque `VLLM_API_KEY` est défini (ou qu'un profil d'authentification existe) et que vous **ne** définissez **pas** `models.providers.vllm`, OpenClaw interrogera :

- `GET http://127.0.0.1:8000/v1/models`

…et convertira les ID retournés en entrées de modèle.

Si vous définissez `models.providers.vllm` explicitement, la découverte automatique est ignorée et vous devez définir les modèles manuellement.

## Configuration explicite (modèles manuels)

Utilisez la configuration explicite lorsque :

- vLLM s'exécute sur un hôte/port différent.
- Vous souhaitez épingler les valeurs `contextWindow`/`maxTokens`.
- Votre serveur nécessite une clé API réelle (ou vous souhaitez contrôler les en-têtes).

```json5
{
  models: {
    providers: {
      vllm: {
        baseUrl: "http://127.0.0.1:8000/v1",
        apiKey: "${VLLM_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "your-model-id",
            name: "Local vLLM Model",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Dépannage

- Vérifiez que le serveur est accessible :

```bash
curl http://127.0.0.1:8000/v1/models
```

- Si les requêtes échouent avec des erreurs d'authentification, définissez une `VLLM_API_KEY` réelle qui correspond à la configuration de votre serveur, ou configurez le fournisseur explicitement sous `models.providers.vllm`.
