---
summary: "Exécutez OpenClaw via ds4, un serveur OpenAI-compatible local DeepSeek V4 Flash"
read_when:
  - You want to run OpenClaw against antirez/ds4
  - You want a local DeepSeek V4 Flash backend with tool calls
  - You need the OpenClaw config for ds4-server
title: "ds4"
---

[ds4](https://github.com/antirez/ds4) sert DeepSeek V4 Flash à partir d'un backend Metal local avec une API `/v1` compatible OpenAI. OpenClaw se connecte à ds4 via la famille de fournisseurs générique `openai-completions`.

ds4 n'est pas un plugin de fournisseur OpenClaw fourni. Configurez-le sous `models.providers.ds4`, puis sélectionnez `ds4/deepseek-v4-flash`.

- ID du fournisseur : `ds4`
- Plugin : aucun
- API : Chat Completions compatible OpenAI (`openai-completions`)
- URL de base suggérée : `http://127.0.0.1:18000/v1`
- ID du modèle : `deepseek-v4-flash`
- Appels d'outils : supportés via `tools` et `tool_calls` de style OpenAI
- Raisonnement : `thinking` et `reasoning_effort` de style DeepSeek

## Prérequis

- macOS avec support Metal.
- Un checkout ds4 fonctionnel avec `ds4-server` et le fichier GGUF DeepSeek V4 Flash.
- Suffisamment de mémoire pour le contexte que vous choisissez. Les valeurs `--ctx` plus grandes allouent plus de mémoire KV au démarrage du serveur.

<Warning>
Les tours d'agent OpenClaw incluent les schémas d'outils et le contexte de l'espace de travail. Un petit contexte comme `--ctx 4096` peut réussir les tests curl directs mais échouer les exécutions d'agent complètes avec `500 prompt exceeds context`. Utilisez au moins `--ctx 32768` pour les tests de fumée d'agent et d'outils. Utilisez `--ctx 393216` uniquement si vous avez suffisamment de mémoire et souhaitez le comportement ds4 Think Max.
</Warning>

## Démarrage rapide

<Steps>
  <Step title="Démarrer ds4-server">
    Remplacez `<DS4_DIR>` par le chemin de votre checkout ds4.

    ```bash
    <DS4_DIR>/ds4-server \
      --model <DS4_DIR>/ds4flash.gguf \
      --host 127.0.0.1 \
      --port 18000 \
      --ctx 32768 \
      --tokens 128
    ```

  </Step>
  <Step title="Vérifier le point de terminaison compatible OpenAI">
    ```bash
    curl http://127.0.0.1:18000/v1/models
    ```

    La réponse doit inclure `deepseek-v4-flash`.

  </Step>
  <Step title="Ajouter la configuration du fournisseur OpenClaw">
    Ajoutez la configuration de [Configuration complète](#configuration-complète), puis exécutez une vérification de modèle unique :

    ```bash
    openclaw infer model run \
      --local \
      --model ds4/deepseek-v4-flash \
      --thinking off \
      --prompt "Reply with exactly: openclaw-ds4-ok" \
      --json
    ```

  </Step>
</Steps>

## Configuration complète

Utilisez cette configuration quand ds4 est déjà en cours d'exécution sur `127.0.0.1:18000`.

```json5
{
  agents: {
    defaults: {
      model: { primary: "ds4/deepseek-v4-flash" },
      models: {
        "ds4/deepseek-v4-flash": {
          alias: "DS4 local",
        },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      ds4: {
        baseUrl: "http://127.0.0.1:18000/v1",
        apiKey: "ds4-local",
        api: "openai-completions",
        timeoutSeconds: 300,
        models: [
          {
            id: "deepseek-v4-flash",
            name: "DeepSeek V4 Flash (ds4)",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 32768,
            maxTokens: 128,
            compat: {
              supportsUsageInStreaming: true,
              supportsReasoningEffort: true,
              maxTokensField: "max_tokens",
              supportsStrictMode: false,
              thinkingFormat: "deepseek",
              supportedReasoningEfforts: ["low", "medium", "high", "xhigh"],
            },
          },
        ],
      },
    },
  },
}
```

Gardez `contextWindow` aligné avec la valeur `ds4-server --ctx`. Gardez `maxTokens` aligné avec `--tokens` sauf si vous voulez intentionnellement qu'OpenClaw demande moins de sortie que la valeur par défaut du serveur.

## Démarrage à la demande

OpenClaw peut démarrer ds4 uniquement quand un modèle `ds4/...` est sélectionné. Ajoutez `localService` à la même entrée de fournisseur :

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
        models: [
          {
            id: "deepseek-v4-flash",
            name: "DeepSeek V4 Flash (ds4)",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 32768,
            maxTokens: 128,
            compat: {
              supportsUsageInStreaming: true,
              supportsReasoningEffort: true,
              maxTokensField: "max_tokens",
              supportsStrictMode: false,
              thinkingFormat: "deepseek",
              supportedReasoningEfforts: ["low", "medium", "high", "xhigh"],
            },
          },
        ],
      },
    },
  },
}
```

`command` doit être un chemin d'exécutable absolu. La recherche de shell et l'expansion `~` ne sont pas utilisées. Voir [Services de modèles locaux](/fr/gateway/local-model-services) pour chaque champ `localService`.

## Think Max

ds4 applique Think Max uniquement quand les deux conditions sont vraies :

- `ds4-server` démarre avec `--ctx 393216` ou plus.
- La requête utilise `reasoning_effort: "max"` ou le champ d'effort ds4 équivalent.

Si vous exécutez ce grand contexte, mettez à jour à la fois les drapeaux du serveur et les métadonnées du modèle OpenClaw :

```json5
{
  contextWindow: 393216,
  maxTokens: 384000,
  compat: {
    supportsUsageInStreaming: true,
    supportsReasoningEffort: true,
    maxTokensField: "max_tokens",
    supportsStrictMode: false,
    thinkingFormat: "deepseek",
    supportedReasoningEfforts: ["low", "medium", "high", "xhigh", "max"],
  },
}
```

## Test

Commencez par une vérification HTTP directe :

```bash
curl http://127.0.0.1:18000/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"Reply with exactly: ds4-ok"}],"max_tokens":16,"stream":false,"thinking":{"type":"disabled"}}'
```

Ensuite, testez le routage du modèle OpenClaw :

```bash
openclaw infer model run \
  --local \
  --model ds4/deepseek-v4-flash \
  --thinking off \
  --prompt "Reply with exactly: openclaw-ds4-ok" \
  --json
```

Pour un test de fumée complet d'agent et d'appel d'outils, utilisez un contexte d'au moins 32768 :

```bash
openclaw agent \
  --local \
  --session-id ds4-tool-smoke \
  --model ds4/deepseek-v4-flash \
  --thinking off \
  --message "Use the shell command pwd once, then reply exactly: tool-ok <output>" \
  --json \
  --timeout 240
```

Résultat attendu :

- `executionTrace.winnerProvider` est `ds4`
- `executionTrace.winnerModel` est `deepseek-v4-flash`
- `toolSummary.calls` est au moins `1`
- `finalAssistantVisibleText` commence par `tool-ok`

## Dépannage

<AccordionGroup>
  <Accordion title="curl /v1/models ne peut pas se connecter">
    ds4 n'est pas en cours d'exécution ou n'est pas lié à l'hôte et au port dans `baseUrl`. Démarrez `ds4-server`, puis réessayez :

    ```bash
    curl http://127.0.0.1:18000/v1/models
    ```

  </Accordion>

  <Accordion title="500 prompt exceeds context">
    Le `--ctx` configuré est trop petit pour le tour OpenClaw. Augmentez `ds4-server --ctx`, puis mettez à jour `models.providers.ds4.models[].contextWindow` pour correspondre. Les tours d'agent complets avec outils nécessitent beaucoup plus de contexte qu'une requête curl directe à un seul message.
  </Accordion>

  <Accordion title="Think Max ne s'active pas">
    ds4 n'utilise Think Max que quand `--ctx` est au moins `393216` et que la requête demande `reasoning_effort: "max"`. Les contextes plus petits reviennent au raisonnement élevé.
  </Accordion>

  <Accordion title="La première requête est lente">
    ds4 a une phase de résidence Metal froide et de préchauffage du modèle. Utilisez `localService.readyTimeoutMs: 300000` quand OpenClaw démarre le serveur à la demande.
  </Accordion>
</AccordionGroup>

## Connexes

<CardGroup cols={2}>
  <Card title="Services de modèles locaux" href="/fr/gateway/local-model-services" icon="play">
    Démarrez les serveurs de modèles locaux à la demande avant les requêtes de modèles.
  </Card>
  <Card title="Modèles locaux" href="/fr/gateway/local-models" icon="server">
    Choisissez et exploitez les backends de modèles locaux.
  </Card>
  <Card title="Fournisseurs de modèles" href="/fr/concepts/model-providers" icon="layers">
    Configurez les références de fournisseurs, l'authentification et le basculement.
  </Card>
  <Card title="DeepSeek" href="/fr/providers/deepseek" icon="brain">
    Comportement du fournisseur DeepSeek natif et contrôles de réflexion.
  </Card>
</CardGroup>
