---
read_when:
  - 你想从自己的 GPU 机器提供模型服务
  - 你正在配置 LM Studio 或 OpenAI 兼容代理
  - 你需要最安全的本地模型指南
summary: 在本地 LLM 上运行 OpenClaw（LM Studio、vLLM、LiteLLM、自定义 OpenAI 端点）
title: 本地模型
x-i18n:
  generated_at: "2026-02-03T07:48:15Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: f72b424c3d8986319868dc4c552596bcd599cc79fab5a57c14bf4f0695c39690
  source_path: gateway/local-models.md
  workflow: 15
---

# Modèles locaux

L'exécution locale est possible, mais OpenClaw s'attend à un grand contexte + une défense robuste contre l'injection de prompts. Une petite mémoire GPU tronquera le contexte et compromettra la sécurité. Visez haut : **≥2 Mac Studio entièrement configurés ou configuration GPU équivalente (environ 30 000 $ +)**. Un seul GPU **24 GB** convient uniquement aux prompts plus légers, avec une latence plus élevée. Utilisez **la plus grande variante de modèle complète que vous pouvez exécuter** ; la quantification agressive ou les points de contrôle « petits » augmentent le risque d'injection de prompts (voir [Sécurité](/gateway/security)).

## Recommandé : LM Studio + MiniMax M2.1 (API Responses, taille complète)

La meilleure pile locale actuelle. Chargez MiniMax M2.1 dans LM Studio, activez le serveur local (par défaut `http://127.0.0.1:1234`), et utilisez l'API Responses pour séparer l'inférence du texte final.

```json5
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/minimax-m2.1-gs32" },
      models: {
        "anthropic/claude-opus-4-5": { alias: "Opus" },
        "lmstudio/minimax-m2.1-gs32": { alias: "Minimax" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [
          {
            id: "minimax-m2.1-gs32",
            name: "MiniMax M2.1 GS32",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 196608,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

**Liste de contrôle de configuration**

- Installez LM Studio : https://lmstudio.ai
- Dans LM Studio, téléchargez **la plus grande version MiniMax M2.1 disponible** (évitez les variantes « petites »/fortement quantifiées), démarrez le serveur, confirmez que `http://127.0.0.1:1234/v1/models` l'énumère.
- Gardez le modèle chargé ; le chargement à froid augmente la latence de démarrage.
- Si votre version LM Studio est différente, ajustez `contextWindow`/`maxTokens`.
- Pour WhatsApp, restez avec l'API Responses pour que seul le texte final soit envoyé.

Même lors de l'exécution de modèles locaux, conservez la configuration des modèles hébergés ; utilisez `models.mode: "merge"` pour que les solutions de secours restent disponibles.

### Configuration hybride : hébergé en principal, local en secours

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["lmstudio/minimax-m2.1-gs32", "anthropic/claude-opus-4-5"],
      },
      models: {
        "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
        "lmstudio/minimax-m2.1-gs32": { alias: "MiniMax Local" },
        "anthropic/claude-opus-4-5": { alias: "Opus" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [
          {
            id: "minimax-m2.1-gs32",
            name: "MiniMax M2.1 GS32",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 196608,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

### Local en priorité, hébergé comme filet de sécurité

Inversez l'ordre du principal et des secours ; conservez le même bloc providers et `models.mode: "merge"` pour basculer vers Sonnet ou Opus lorsque votre machine locale est en panne.

### Hébergement régional / routage des données

- Les variantes MiniMax/Kimi/GLM hébergées existent également sur OpenRouter avec des points de terminaison fixes par région (par exemple, hébergement aux États-Unis). Choisissez la variante régionale là-bas pour maintenir le trafic dans la juridiction de votre choix, tout en utilisant `models.mode: "merge"` comme secours Anthropic/OpenAI.
- Purement local reste le chemin de confidentialité le plus fort ; le routage régional hébergé est un compromis lorsque vous avez besoin de fonctionnalités de fournisseur mais que vous souhaitez contrôler le flux de données.

## Autres proxies locaux compatibles OpenAI

vLLM, LiteLLM, OAI-proxy ou une passerelle personnalisée fonctionnent tous tant qu'ils exposent des points de terminaison `/v1` de style OpenAI. Remplacez le bloc provider ci-dessus par votre point de terminaison et votre ID de modèle :

```json5
{
  models: {
    mode: "merge",
    providers: {
      local: {
        baseUrl: "http://127.0.0.1:8000/v1",
        apiKey: "sk-local",
        api: "openai-responses",
        models: [
          {
            id: "my-local-model",
            name: "Local Model",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 120000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Conservez `models.mode: "merge"` pour que les modèles hébergés restent disponibles comme secours.

## Dépannage

- La passerelle peut-elle accéder au proxy ? `curl http://127.0.0.1:1234/v1/models`.
- Le modèle LM Studio est-il déchargé ? Rechargez-le ; le démarrage à froid est une cause courante de « blocage ».
- Erreur de contexte ? Réduisez `contextWindow` ou augmentez les limites du serveur.
- Sécurité : les modèles locaux contournent les filtres côté fournisseur ; gardez la portée de l'agent étroite et activez la compression pour limiter l'impact de l'injection de prompts.
