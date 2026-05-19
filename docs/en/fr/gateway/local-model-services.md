---
summary: "Démarrer les serveurs de modèles locaux à la demande avant les requêtes de modèles OpenClaw"
read_when:
  - You want OpenClaw to start a local model server only when its model is selected
  - You run ds4, inferrs, vLLM, llama.cpp, MLX, or another OpenAI-compatible local server
  - You need to control cold start, readiness, and idle shutdown for local providers
title: "Services de modèles locaux"
---

`models.providers.<id>.localService` permet à OpenClaw de démarrer un serveur de modèles local appartenant au fournisseur à la demande. Il s'agit d'une configuration au niveau du fournisseur : lorsque le modèle sélectionné appartient à ce fournisseur, OpenClaw sonde le service, démarre le processus si le point de terminaison est inactif, attend la disponibilité, puis envoie la requête du modèle.

Utilisez-le pour les serveurs locaux qui sont coûteux à maintenir en fonctionnement toute la journée, ou pour les configurations manuelles où la sélection du modèle devrait suffire à activer le backend.

## Fonctionnement

1. Une requête de modèle se résout en un fournisseur configuré.
2. Si ce fournisseur a `localService`, OpenClaw sonde `healthUrl`.
3. Si la sonde réussit, OpenClaw utilise le serveur existant.
4. Si la sonde échoue, OpenClaw démarre `command` avec `args`.
5. OpenClaw interroge la disponibilité jusqu'à l'expiration de `readyTimeoutMs`.
6. La requête du modèle est envoyée via le transport du fournisseur normal.
7. Si OpenClaw a démarré le processus et que `idleStopMs` est positif, le processus est arrêté après que la dernière requête en cours ait été inactive pendant cette durée.

OpenClaw n'installe pas launchd, systemd, Docker ou un daemon pour cela. Le serveur est un processus enfant du processus OpenClaw qui en avait d'abord besoin.

## Forme de la configuration

```json5
{
  models: {
    providers: {
      local: {
        baseUrl: "http://127.0.0.1:8000/v1",
        apiKey: "local-model",
        api: "openai-completions",
        timeoutSeconds: 300,
        localService: {
          command: "/absolute/path/to/server",
          args: ["--host", "127.0.0.1", "--port", "8000"],
          cwd: "/absolute/path/to/working-dir",
          env: { LOCAL_MODEL_CACHE: "/absolute/path/to/cache" },
          healthUrl: "http://127.0.0.1:8000/v1/models",
          readyTimeoutMs: 180000,
          idleStopMs: 0,
        },
        models: [
          {
            id: "my-local-model",
            name: "My Local Model",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 131072,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Champs

- `command`: chemin d'accès exécutable absolu. La recherche de shell n'est pas utilisée.
- `args`: arguments du processus. Aucune expansion de shell, pipes, globbing ou règles de guillemets ne sont appliqués.
- `cwd`: répertoire de travail optionnel pour le processus.
- `env`: variables d'environnement optionnelles fusionnées avec l'environnement du processus OpenClaw.
- `healthUrl`: URL de disponibilité. Si omis, OpenClaw ajoute `/models` à `baseUrl`, donc `http://127.0.0.1:8000/v1` devient `http://127.0.0.1:8000/v1/models`.
- `readyTimeoutMs`: délai d'expiration de la disponibilité au démarrage. Par défaut : `120000`.
- `idleStopMs`: délai d'arrêt inactif pour les processus démarrés par OpenClaw. `0` ou omis maintient le processus actif jusqu'à la sortie d'OpenClaw.

## Exemple Inferrs

Inferrs est un backend `/v1` compatible OpenAI personnalisé, donc la même API de service local fonctionne avec l'entrée du fournisseur `inferrs`.

```json5
{
  agents: {
    defaults: {
      model: { primary: "inferrs/google/gemma-4-E2B-it" },
    },
  },
  models: {
    mode: "merge",
    providers: {
      inferrs: {
        baseUrl: "http://127.0.0.1:8080/v1",
        apiKey: "inferrs-local",
        api: "openai-completions",
        timeoutSeconds: 300,
        localService: {
          command: "/opt/homebrew/bin/inferrs",
          args: [
            "serve",
            "google/gemma-4-E2B-it",
            "--host",
            "127.0.0.1",
            "--port",
            "8080",
            "--device",
            "metal",
          ],
          healthUrl: "http://127.0.0.1:8080/v1/models",
          readyTimeoutMs: 180000,
          idleStopMs: 0,
        },
        models: [
          {
            id: "google/gemma-4-E2B-it",
            name: "Gemma 4 E2B (inferrs)",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 131072,
            maxTokens: 4096,
            compat: {
              requiresStringContent: true,
            },
          },
        ],
      },
    },
  },
}
```

Remplacez `command` par le résultat de `which inferrs` sur la machine exécutant OpenClaw.

## Exemple ds4

Pour la configuration complète, les conseils de dimensionnement du contexte et les commandes de vérification, voir [ds4](/fr/providers/ds4).

```json5
{
  models: {
    providers: {
      ds4: {
        baseUrl: "http://127.0.0.1:18000/v1",
        apiKey: "ds4-local",
        api: "openai-completions",
        timeoutSeconds: 300,
        localService: {
          command: "<DS4_DIR>/ds4-server",
          args: [
            "--model",
            "<DS4_DIR>/ds4flash.gguf",
            "--host",
            "127.0.0.1",
            "--port",
            "18000",
            "--ctx",
            "32768",
            "--tokens",
            "128",
          ],
          cwd: "<DS4_DIR>",
          healthUrl: "http://127.0.0.1:18000/v1/models",
          readyTimeoutMs: 300000,
          idleStopMs: 0,
        },
        models: [],
      },
    },
  },
}
```

## Notes opérationnelles

- Un processus OpenClaw gère l'enfant qu'il a démarré. Un autre processus OpenClaw qui voit la même URL de santé déjà active la réutilisera sans l'adopter.
- Le démarrage est sérialisé par commande de fournisseur et ensemble d'arguments, donc les requêtes concurrentes ne génèrent pas de serveurs en double pour la même configuration.
- Les réponses de streaming actives maintiennent un bail ; l'arrêt inactif attend que la gestion du corps de la réponse soit terminée.
- Utilisez `timeoutSeconds` sur les fournisseurs locaux lents afin que les démarrages à froid et les générations longues ne dépassent pas le délai d'expiration par défaut de la requête du modèle.
- Utilisez un `healthUrl` explicite si votre serveur expose la disponibilité ailleurs qu'à `/v1/models`.

## Connexes

<CardGroup cols={2}>
  <Card title="Local models" href="/fr/gateway/local-models" icon="server">
    Local model setup, provider choices, and safety guidance.
  </Card>
  <Card title="Inferrs" href="/fr/providers/inferrs" icon="cpu">
    Run OpenClaw through the inferrs OpenAI-compatible local server.
  </Card>
</CardGroup>
