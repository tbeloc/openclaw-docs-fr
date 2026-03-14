---
read_when:
  - Vous souhaitez utiliser Synthetic comme fournisseur de modèles
  - Vous devez configurer la clé API Synthetic ou l'URL de base
summary: Utilisation de l'API compatible Anthropic de Synthetic dans OpenClaw
title: Synthetic
x-i18n:
  generated_at: "2026-02-01T21:35:34Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: f3f6e3eb864661754cbe2276783c5bc96ae01cb85ee4a19c92bed7863a35a4f7
  source_path: providers/synthetic.md
  workflow: 15
---

# Synthetic

Synthetic fournit des points de terminaison compatibles avec Anthropic. OpenClaw l'enregistre en tant que fournisseur `synthetic` et utilise l'API Anthropic Messages.

## Configuration rapide

1. Configurez `SYNTHETIC_API_KEY` (ou exécutez l'assistant suivant).
2. Exécutez l'assistant d'intégration :

```bash
openclaw onboard --auth-choice synthetic-api-key
```

Le modèle par défaut est défini sur :

```
synthetic/hf:MiniMaxAI/MiniMax-M2.1
```

## Exemple de configuration

```json5
{
  env: { SYNTHETIC_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.1" },
      models: { "synthetic/hf:MiniMaxAI/MiniMax-M2.1": { alias: "MiniMax M2.1" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "hf:MiniMaxAI/MiniMax-M2.1",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 192000,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

Remarque : Le client Anthropic d'OpenClaw ajoute automatiquement `/v1` après l'URL de base, utilisez donc `https://api.synthetic.new/anthropic` (et non `/anthropic/v1`). Si Synthetic modifie son URL de base, remplacez `models.providers.synthetic.baseUrl`.

## Catalogue des modèles

Tous les modèles suivants ont un coût de `0` (entrée/sortie/cache).

| ID du modèle                                           | Fenêtre contextuelle | Tokens max | Raisonnement | Entrée       |
| ------------------------------------------------------ | -------------------- | ---------- | ------------ | ------------ |
| `hf:MiniMaxAI/MiniMax-M2.1`                            | 192000               | 65536      | false        | text         |
| `hf:moonshotai/Kimi-K2-Thinking`                       | 256000               | 8192       | true         | text         |
| `hf:zai-org/GLM-4.7`                                   | 198000               | 128000     | false        | text         |
| `hf:deepseek-ai/DeepSeek-R1-0528`                      | 128000               | 8192       | false        | text         |
| `hf:deepseek-ai/DeepSeek-V3-0324`                      | 128000               | 8192       | false        | text         |
| `hf:deepseek-ai/DeepSeek-V3.1`                         | 128000               | 8192       | false        | text         |
| `hf:deepseek-ai/DeepSeek-V3.1-Terminus`                | 128000               | 8192       | false        | text         |
| `hf:deepseek-ai/DeepSeek-V3.2`                         | 159000               | 8192       | false        | text         |
| `hf:meta-llama/Llama-3.3-70B-Instruct`                 | 128000               | 8192       | false        | text         |
| `hf:meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` | 524000               | 8192       | false        | text         |
| `hf:moonshotai/Kimi-K2-Instruct-0905`                  | 256000               | 8192       | false        | text         |
| `hf:openai/gpt-oss-120b`                               | 128000               | 8192       | false        | text         |
| `hf:Qwen/Qwen3-235B-A22B-Instruct-2507`                | 256000               | 8192       | false        | text         |
| `hf:Qwen/Qwen3-Coder-480B-A35B-Instruct`               | 256000               | 8192       | false        | text         |
| `hf:Qwen/Qwen3-VL-235B-A22B-Instruct`                  | 250000               | 8192       | false        | text + image |
| `hf:zai-org/GLM-4.5`                                   | 128000               | 128000     | false        | text         |
| `hf:zai-org/GLM-4.6`                                   | 198000               | 128000     | false        | text         |
| `hf:deepseek-ai/DeepSeek-V3`                           | 128000               | 8192       | false        | text         |
| `hf:Qwen/Qwen3-235B-A22B-Thinking-2507`                | 256000               | 8192       | true         | text         |

## Remarques

- Le format de référence du modèle est `synthetic/<modelId>`.
- Si une liste d'autorisation de modèles est activée (`agents.defaults.models`), ajoutez tous les modèles que vous prévoyez d'utiliser.
- Consultez [Fournisseurs de modèles](/concepts/model-providers) pour connaître les règles des fournisseurs.
