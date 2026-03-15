---
summary: "Configurer Moonshot K2 vs Kimi Coding (fournisseurs et clés séparés)"
read_when:
  - Vous voulez la configuration Moonshot K2 (Moonshot Open Platform) vs Kimi Coding
  - Vous devez comprendre les points de terminaison, clés et références de modèles séparés
  - Vous voulez une configuration prête à copier/coller pour l'un ou l'autre fournisseur
title: "Moonshot AI"
---

# Moonshot AI (Kimi)

Moonshot fournit l'API Kimi avec des points de terminaison compatibles OpenAI. Configurez le
fournisseur et définissez le modèle par défaut sur `moonshot/kimi-k2.5`, ou utilisez
Kimi Coding avec `kimi-coding/k2p5`.

IDs de modèle Kimi K2 actuels :

[//]: # "moonshot-kimi-k2-ids:start"

- `kimi-k2.5`
- `kimi-k2-0905-preview`
- `kimi-k2-turbo-preview`
- `kimi-k2-thinking`
- `kimi-k2-thinking-turbo`

[//]: # "moonshot-kimi-k2-ids:end"

```bash
openclaw onboard --auth-choice moonshot-api-key
```

Kimi Coding :

```bash
openclaw onboard --auth-choice kimi-code-api-key
```

Remarque : Moonshot et Kimi Coding sont des fournisseurs séparés. Les clés ne sont pas interchangeables, les points de terminaison diffèrent, et les références de modèles diffèrent (Moonshot utilise `moonshot/...`, Kimi Coding utilise `kimi-coding/...`).

## Extrait de configuration (API Moonshot)

```json5
{
  env: { MOONSHOT_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "moonshot/kimi-k2.5" },
      models: {
        // moonshot-kimi-k2-aliases:start
        "moonshot/kimi-k2.5": { alias: "Kimi K2.5" },
        "moonshot/kimi-k2-0905-preview": { alias: "Kimi K2" },
        "moonshot/kimi-k2-turbo-preview": { alias: "Kimi K2 Turbo" },
        "moonshot/kimi-k2-thinking": { alias: "Kimi K2 Thinking" },
        "moonshot/kimi-k2-thinking-turbo": { alias: "Kimi K2 Thinking Turbo" },
        // moonshot-kimi-k2-aliases:end
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [
          // moonshot-kimi-k2-models:start
          {
            id: "kimi-k2.5",
            name: "Kimi K2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-0905-preview",
            name: "Kimi K2 0905 Preview",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-turbo-preview",
            name: "Kimi K2 Turbo",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-thinking",
            name: "Kimi K2 Thinking",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-thinking-turbo",
            name: "Kimi K2 Thinking Turbo",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          // moonshot-kimi-k2-models:end
        ],
      },
    },
  },
}
```

## Kimi Coding

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "kimi-coding/k2p5" },
      models: {
        "kimi-coding/k2p5": { alias: "Kimi K2.5" },
      },
    },
  },
}
```

## Remarques

- Les références de modèles Moonshot utilisent `moonshot/<modelId>`. Les références de modèles Kimi Coding utilisent `kimi-coding/<modelId>`.
- Remplacez les métadonnées de tarification et de contexte dans `models.providers` si nécessaire.
- Si Moonshot publie des limites de contexte différentes pour un modèle, ajustez
  `contextWindow` en conséquence.
- Utilisez `https://api.moonshot.ai/v1` pour le point de terminaison international, et `https://api.moonshot.cn/v1` pour le point de terminaison en Chine.

## Mode de réflexion natif (Moonshot)

Moonshot Kimi supporte la réflexion native binaire :

- `thinking: { type: "enabled" }`
- `thinking: { type: "disabled" }`

Configurez-le par modèle via `agents.defaults.models.<provider/model>.params` :

```json5
{
  agents: {
    defaults: {
      models: {
        "moonshot/kimi-k2.5": {
          params: {
            thinking: { type: "disabled" },
          },
        },
      },
    },
  },
}
```

OpenClaw mappe également les niveaux `/think` d'exécution pour Moonshot :

- `/think off` -> `thinking.type=disabled`
- tout niveau de réflexion non-off -> `thinking.type=enabled`

Lorsque la réflexion Moonshot est activée, `tool_choice` doit être `auto` ou `none`. OpenClaw normalise les valeurs `tool_choice` incompatibles à `auto` pour la compatibilité.
