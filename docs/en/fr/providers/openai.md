---
summary: "Utilisez OpenAI via des clés API ou un abonnement Codex dans OpenClaw"
read_when:
  - You want to use OpenAI models in OpenClaw
  - You want Codex subscription auth instead of API keys
title: "OpenAI"
---

# OpenAI

OpenAI fournit des API de développeur pour les modèles GPT. Codex supporte la **connexion ChatGPT** pour l'accès par abonnement ou la **connexion par clé API** pour l'accès basé sur l'utilisation. Codex cloud nécessite une connexion ChatGPT. OpenAI supporte explicitement l'utilisation OAuth par abonnement dans les outils/workflows externes comme OpenClaw.

## Option A : Clé API OpenAI (Plateforme OpenAI)

**Idéal pour :** l'accès direct à l'API et la facturation à l'usage.
Obtenez votre clé API depuis le tableau de bord OpenAI.

### Configuration CLI

```bash
openclaw onboard --auth-choice openai-api-key
# ou non-interactif
openclaw onboard --openai-api-key "$OPENAI_API_KEY"
```

### Extrait de configuration

```json5
{
  env: { OPENAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "openai/gpt-5.4" } } },
}
```

La documentation actuelle des modèles API d'OpenAI liste `gpt-5.4` et `gpt-5.4-pro` pour l'utilisation directe de l'API OpenAI. OpenClaw transmet les deux via le chemin `openai/*` Responses. OpenClaw supprime intentionnellement la ligne obsolète `openai/gpt-5.3-codex-spark`, car les appels directs à l'API OpenAI la rejettent dans le trafic en direct.

OpenClaw n'expose **pas** `openai/gpt-5.3-codex-spark` sur le chemin direct de l'API OpenAI. `pi-ai` fournit toujours une ligne intégrée pour ce modèle, mais les requêtes directes à l'API OpenAI la rejettent actuellement. Spark est traité comme Codex uniquement dans OpenClaw.

## Option B : Abonnement OpenAI Code (Codex)

**Idéal pour :** utiliser l'accès par abonnement ChatGPT/Codex au lieu d'une clé API.
Codex cloud nécessite une connexion ChatGPT, tandis que la CLI Codex supporte la connexion ChatGPT ou par clé API.

### Configuration CLI (OAuth Codex)

```bash
# Exécutez OAuth Codex dans l'assistant
openclaw onboard --auth-choice openai-codex

# Ou exécutez OAuth directement
openclaw models auth login --provider openai-codex
```

### Extrait de configuration (abonnement Codex)

```json5
{
  agents: { defaults: { model: { primary: "openai-codex/gpt-5.4" } } },
}
```

La documentation actuelle de Codex d'OpenAI liste `gpt-5.4` comme le modèle Codex actuel. OpenClaw le mappe à `openai-codex/gpt-5.4` pour l'utilisation OAuth ChatGPT/Codex.

Si votre compte Codex est autorisé à utiliser Codex Spark, OpenClaw supporte également :

- `openai-codex/gpt-5.3-codex-spark`

OpenClaw traite Codex Spark comme Codex uniquement. Il n'expose pas un chemin direct `openai/gpt-5.3-codex-spark` par clé API.

OpenClaw préserve également `openai-codex/gpt-5.3-codex-spark` quand `pi-ai` le découvre. Traitez-le comme dépendant des droits et expérimental : Codex Spark est séparé de GPT-5.4 `/fast`, et la disponibilité dépend du compte Codex / ChatGPT connecté.

### Transport par défaut

OpenClaw utilise `pi-ai` pour le streaming de modèles. Pour `openai/*` et `openai-codex/*`, le transport par défaut est `"auto"` (WebSocket en premier, puis repli SSE).

Vous pouvez définir `agents.defaults.models.<provider/model>.params.transport` :

- `"sse"` : forcer SSE
- `"websocket"` : forcer WebSocket
- `"auto"` : essayer WebSocket, puis revenir à SSE

Pour `openai/*` (API Responses), OpenClaw active également le préchauffage WebSocket par défaut (`openaiWsWarmup: true`) quand le transport WebSocket est utilisé.

Documentation OpenAI associée :

- [Realtime API with WebSocket](https://platform.openai.com/docs/guides/realtime-websocket)
- [Streaming API responses (SSE)](https://platform.openai.com/docs/guides/streaming-responses)

```json5
{
  agents: {
    defaults: {
      model: { primary: "openai-codex/gpt-5.4" },
      models: {
        "openai-codex/gpt-5.4": {
          params: {
            transport: "auto",
          },
        },
      },
    },
  },
}
```

### Préchauffage WebSocket OpenAI

La documentation OpenAI décrit le préchauffage comme optionnel. OpenClaw l'active par défaut pour `openai/*` afin de réduire la latence du premier tour lors de l'utilisation du transport WebSocket.

### Désactiver le préchauffage

```json5
{
  agents: {
    defaults: {
      models: {
        "openai/gpt-5.4": {
          params: {
            openaiWsWarmup: false,
          },
        },
      },
    },
  },
}
```

### Activer le préchauffage explicitement

```json5
{
  agents: {
    defaults: {
      models: {
        "openai/gpt-5.4": {
          params: {
            openaiWsWarmup: true,
          },
        },
      },
    },
  },
}
```

### Traitement prioritaire OpenAI

L'API OpenAI expose le traitement prioritaire via `service_tier=priority`. Dans OpenClaw, définissez `agents.defaults.models["openai/<model>"].params.serviceTier` pour transmettre ce champ dans les requêtes directes `openai/*` Responses.

```json5
{
  agents: {
    defaults: {
      models: {
        "openai/gpt-5.4": {
          params: {
            serviceTier: "priority",
          },
        },
      },
    },
  },
}
```

Les valeurs supportées sont `auto`, `default`, `flex` et `priority`.

### Mode rapide OpenAI

OpenClaw expose un commutateur de mode rapide partagé pour les sessions `openai/*` et `openai-codex/*` :

- Chat/UI : `/fast status|on|off`
- Config : `agents.defaults.models["<provider>/<model>"].params.fastMode`

Quand le mode rapide est activé, OpenClaw applique un profil OpenAI à faible latence :

- `reasoning.effort = "low"` quand la charge utile ne spécifie pas déjà le raisonnement
- `text.verbosity = "low"` quand la charge utile ne spécifie pas déjà la verbosité
- `service_tier = "priority"` pour les appels directs `openai/*` Responses à `api.openai.com`

Exemple :

```json5
{
  agents: {
    defaults: {
      models: {
        "openai/gpt-5.4": {
          params: {
            fastMode: true,
          },
        },
        "openai-codex/gpt-5.4": {
          params: {
            fastMode: true,
          },
        },
      },
    },
  },
}
```

Les remplacements de session l'emportent sur la configuration. L'effacement du remplacement de session dans l'interface utilisateur Sessions ramène la session à la valeur par défaut configurée.

### Compaction côté serveur OpenAI Responses

Pour les modèles Responses OpenAI directs (`openai/*` utilisant `api: "openai-responses"` avec `baseUrl` sur `api.openai.com`), OpenClaw active maintenant automatiquement les indices de charge utile de compaction côté serveur OpenAI :

- Force `store: true` (sauf si la compatibilité du modèle définit `supportsStore: false`)
- Injecte `context_management: [{ type: "compaction", compact_threshold: ... }]`

Par défaut, `compact_threshold` est `70%` de la `contextWindow` du modèle (ou `80000` quand indisponible).

### Activer la compaction côté serveur explicitement

Utilisez ceci quand vous voulez forcer l'injection `context_management` sur les modèles Responses compatibles (par exemple Azure OpenAI Responses) :

```json5
{
  agents: {
    defaults: {
      models: {
        "azure-openai-responses/gpt-5.4": {
          params: {
            responsesServerCompaction: true,
          },
        },
      },
    },
  },
}
```

### Activer avec un seuil personnalisé

```json5
{
  agents: {
    defaults: {
      models: {
        "openai/gpt-5.4": {
          params: {
            responsesServerCompaction: true,
            responsesCompactThreshold: 120000,
          },
        },
      },
    },
  },
}
```

### Désactiver la compaction côté serveur

```json5
{
  agents: {
    defaults: {
      models: {
        "openai/gpt-5.4": {
          params: {
            responsesServerCompaction: false,
          },
        },
      },
    },
  },
}
```

`responsesServerCompaction` contrôle uniquement l'injection `context_management`. Les modèles Responses OpenAI directs forcent toujours `store: true` sauf si la compatibilité définit `supportsStore: false`.

## Notes

- Les références de modèle utilisent toujours `provider/model` (voir [/concepts/models](/concepts/models)).
- Les détails d'authentification + les règles de réutilisation sont dans [/concepts/oauth](/concepts/oauth).
