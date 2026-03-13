---
read_when:
  - Vous souhaitez comprendre la configuration de Moonshot K2 (plateforme ouverte Moonshot) et Kimi Coding
  - Vous devez connaître les points de terminaison, clés et références de modèles indépendants
  - Vous souhaitez obtenir une configuration prête à copier-coller pour l'un ou l'autre fournisseur
summary: Configurer Moonshot K2 et Kimi Coding (fournisseurs et clés indépendants)
title: Moonshot AI
x-i18n:
  generated_at: "2026-02-01T21:35:13Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 2de81b1a37a0e6e61e0e142fcd36760ecd00834e107dc9b5e38bbf971b27e18e
  source_path: providers/moonshot.md
  workflow: 15
---

# Moonshot AI (Kimi)

Moonshot fournit l'API Kimi compatible avec les points de terminaison OpenAI. Configurez le fournisseur et définissez le modèle par défaut sur `moonshot/kimi-k2.5`, ou utilisez `kimi-coding/k2p5` pour Kimi Coding.

IDs de modèle Kimi K2 actuels :
{/_ moonshot-kimi-k2-ids:start _/}

- `kimi-k2.5`
- `kimi-k2-0905-preview`
- `kimi-k2-turbo-preview`
- `kimi-k2-thinking`
- `kimi-k2-thinking-turbo`
  {/_ moonshot-kimi-k2-ids:end _/}

```bash
openclaw onboard --auth-choice moonshot-api-key
```

Kimi Coding :

```bash
openclaw onboard --auth-choice kimi-code-api-key
```

Remarque : Moonshot et Kimi Coding sont des fournisseurs indépendants. Les clés ne sont pas interchangeables, les points de terminaison sont différents, et les références de modèles aussi (Moonshot utilise `moonshot/...`, Kimi Coding utilise `kimi-coding/...`).

## Fragment de configuration (API Moonshot)

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
- Vous pouvez remplacer les métadonnées de tarification et de contexte dans `models.providers` si nécessaire.
- Si Moonshot publie des limites de contexte différentes pour un modèle, ajustez `contextWindow` en conséquence.
- Pour utiliser le point de terminaison chinois, utilisez `https://api.moonshot.cn/v1`.
