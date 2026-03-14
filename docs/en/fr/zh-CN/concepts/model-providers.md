---
read_when:
  - Vous avez besoin d'une référence de configuration de modèles classée par fournisseur
  - Vous avez besoin d'exemples de configuration de fournisseurs de modèles ou de commandes d'amorçage CLI
summary: Aperçu des fournisseurs de modèles, avec exemples de configuration et processus CLI
title: Fournisseurs de modèles
x-i18n:
  generated_at: "2026-02-03T07:46:28Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 14f73e5a9f9b7c6f017d59a54633942dba95a3eb50f8848b836cfe0b9f6d7719
  source_path: concepts/model-providers.md
  workflow: 15
---

# Fournisseurs de modèles

Cette page présente les **fournisseurs LLM/modèles** (et non les canaux de chat comme WhatsApp/Telegram).
Pour les règles de sélection de modèles, consultez [/concepts/models](/concepts/models).

## Règles rapides

- Les références de modèles utilisent le format `fournisseur/modèle` (par exemple : `opencode/claude-opus-4-5`).
- Si `agents.defaults.models` est défini, il devient une liste d'autorisation.
- Outils CLI : `openclaw onboard`, `openclaw models list`, `openclaw models set <fournisseur/modèle>`.

## Fournisseurs intégrés (répertoire pi-ai)

OpenClaw est fourni avec le répertoire pi-ai. Ces fournisseurs **ne nécessitent pas** de configuration `models.providers` ; il suffit de définir l'authentification + de sélectionner le modèle.

### OpenAI

- Fournisseur : `openai`
- Authentification : `OPENAI_API_KEY`
- Exemple de modèle : `openai/gpt-5.2`
- CLI : `openclaw onboard --auth-choice openai-api-key`

```json5
{
  agents: { defaults: { model: { primary: "openai/gpt-5.2" } } },
}
```

### Anthropic

- Fournisseur : `anthropic`
- Authentification : `ANTHROPIC_API_KEY` ou `claude setup-token`
- Exemple de modèle : `anthropic/claude-opus-4-5`
- CLI : `openclaw onboard --auth-choice token` (collez setup-token) ou `openclaw models auth paste-token --provider anthropic`

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-5" } } },
}
```

### OpenAI Code (Codex)

- Fournisseur : `openai-codex`
- Authentification : OAuth (ChatGPT)
- Exemple de modèle : `openai-codex/gpt-5.2`
- CLI : `openclaw onboard --auth-choice openai-codex` ou `openclaw models auth login --provider openai-codex`

```json5
{
  agents: { defaults: { model: { primary: "openai-codex/gpt-5.2" } } },
}
```

### OpenCode Zen

- Fournisseur : `opencode`
- Authentification : `OPENCODE_API_KEY` (ou `OPENCODE_ZEN_API_KEY`)
- Exemple de modèle : `opencode/claude-opus-4-5`
- CLI : `openclaw onboard --auth-choice opencode-zen`

```json5
{
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-5" } } },
}
```

### Google Gemini (clé API)

- Fournisseur : `google`
- Authentification : `GEMINI_API_KEY`
- Exemple de modèle : `google/gemini-3-pro-preview`
- CLI : `openclaw onboard --auth-choice gemini-api-key`

### Google Vertex, Antigravity et Gemini CLI

- Fournisseurs : `google-vertex`, `google-antigravity`, `google-gemini-cli`
- Authentification : Vertex utilise gcloud ADC ; Antigravity/Gemini CLI utilisent leurs propres flux d'authentification
- OAuth Antigravity fourni en tant que plugin fourni (`google-antigravity-auth`, désactivé par défaut).
  - Activer : `openclaw plugins enable google-antigravity-auth`
  - Connexion : `openclaw models auth login --provider google-antigravity --set-default`
- OAuth Gemini CLI fourni en tant que plugin fourni (`google-gemini-cli-auth`, désactivé par défaut).
  - Activer : `openclaw plugins enable google-gemini-cli-auth`
  - Connexion : `openclaw models auth login --provider google-gemini-cli --set-default`
  - Remarque : vous **n'avez pas besoin** de coller l'ID client ou la clé secrète dans `openclaw.json`. Le flux de connexion CLI stocke les jetons dans le fichier de configuration d'authentification de l'hôte Gateway.

### Z.AI (GLM)

- Fournisseur : `zai`
- Authentification : `ZAI_API_KEY`
- Exemple de modèle : `zai/glm-4.7`
- CLI : `openclaw onboard --auth-choice zai-api-key`
  - Alias : les spécifications `z.ai/*` et `z-ai/*` sont normalisées en `zai/*`

### Vercel AI Gateway

- Fournisseur : `vercel-ai-gateway`
- Authentification : `AI_GATEWAY_API_KEY`
- Exemple de modèle : `vercel-ai-gateway/anthropic/claude-opus-4.5`
- CLI : `openclaw onboard --auth-choice ai-gateway-api-key`

### Autres fournisseurs intégrés

- OpenRouter : `openrouter` (`OPENROUTER_API_KEY`)
- Exemple de modèle : `openrouter/anthropic/claude-sonnet-4-5`
- xAI : `xai` (`XAI_API_KEY`)
- Groq : `groq` (`GROQ_API_KEY`)
- Cerebras : `cerebras` (`CEREBRAS_API_KEY`)
  - Les modèles GLM sur Cerebras utilisent les ID `zai-glm-4.7` et `zai-glm-4.6`.
  - URL de base compatible OpenAI : `https://api.cerebras.ai/v1`.
- Mistral : `mistral` (`MISTRAL_API_KEY`)
- GitHub Copilot : `github-copilot` (`COPILOT_GITHUB_TOKEN` / `GH_TOKEN` / `GITHUB_TOKEN`)

## Fournisseurs configurés via `models.providers` (personnalisé/URL de base)

Utilisez `models.providers` (ou `models.json`) pour ajouter des fournisseurs **personnalisés** ou des proxies compatibles OpenAI/Anthropic.

### Moonshot AI (Kimi)

Moonshot utilise des points de terminaison compatibles OpenAI, configurez-le donc comme fournisseur personnalisé :

- Fournisseur : `moonshot`
- Authentification : `MOONSHOT_API_KEY`
- Exemple de modèle : `moonshot/kimi-k2.5`

ID de modèle Kimi K2 :

{/_ moonshot-kimi-k2-model-refs:start _/ && null}

- `moonshot/kimi-k2.5`
- `moonshot/kimi-k2-0905-preview`
- `moonshot/kimi-k2-turbo-preview`
- `moonshot/kimi-k2-thinking`
- `moonshot/kimi-k2-thinking-turbo`
  {/_ moonshot-kimi-k2-model-refs:end _/ && null}

```json5
{
  agents: {
    defaults: { model: { primary: "moonshot/kimi-k2.5" } },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [{ id: "kimi-k2.5", name: "Kimi K2.5" }],
      },
    },
  },
}
```

### Kimi Coding

Kimi Coding utilise le point de terminaison compatible Anthropic de Moonshot AI :

- Fournisseur : `kimi-coding`
- Authentification : `KIMI_API_KEY`
- Exemple de modèle : `kimi-coding/k2p5`

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: { model: { primary: "kimi-coding/k2p5" } },
  },
}
```

### Qwen OAuth (niveau gratuit)

Qwen fournit un accès OAuth à Qwen Coder + Vision via un flux de code d'appareil.
Activez le plugin fourni, puis connectez-vous :

```bash
openclaw plugins enable qwen-portal-auth
openclaw models auth login --provider qwen-portal --set-default
```

Références de modèles :

- `qwen-portal/coder-model`
- `qwen-portal/vision-model`

Consultez [/providers/qwen](/providers/qwen) pour les détails de configuration et les remarques.

### Synthetic

Synthetic fournit des modèles compatibles Anthropic via le fournisseur `synthetic` :

- Fournisseur : `synthetic`
- Authentification : `SYNTHETIC_API_KEY`
- Exemple de modèle : `synthetic/hf:MiniMaxAI/MiniMax-M2.1`
- CLI : `openclaw onboard --auth-choice synthetic-api-key`

```json5
{
  agents: {
    defaults: { model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.1" } },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [{ id: "hf:MiniMaxAI/MiniMax-M2.1", name: "MiniMax M2.1" }],
      },
    },
  },
}
```

### MiniMax

MiniMax est configuré via `models.providers` car il utilise un point de terminaison personnalisé :

- MiniMax (compatible Anthropic) : `--auth-choice minimax-api`
- Authentification : `MINIMAX_API_KEY`

Consultez [/providers/minimax](/providers/minimax) pour les détails de configuration, les options de modèles et les fragments de configuration.

### Ollama

Ollama est un runtime LLM local qui fournit une API compatible OpenAI :

- Fournisseur : `ollama`
- Authentification : aucune (serveur local)
- Exemple de modèle : `ollama/llama3.3`
- Installation : https://ollama.ai

```bash
# Installez Ollama, puis téléchargez un modèle :
ollama pull llama3.3
```

```json5
{
  agents: {
    defaults: { model: { primary: "ollama/llama3.3" } },
  },
}
```

La détection automatique se fait lorsqu'Ollama s'exécute localement sur `http://127.0.0.1:11434/v1`. Consultez [/providers/ollama](/providers/ollama) pour les recommandations de modèles et la configuration personnalisée.

### Proxies locaux (LM Studio, vLLM, LiteLLM, etc.)

Exemple (compatible OpenAI) :

```json5
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/minimax-m2.1-gs32" },
      models: { "lmstudio/minimax-m2.1-gs32": { alias: "Minimax" } },
    },
  },
  models: {
    providers: {
      lmstudio: {
        baseUrl: "http://localhost:1234/v1",
        apiKey: "LMSTUDIO_KEY",
        api: "openai-completions",
        models: [
          {
            id: "minimax-m2.1-gs32",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Remarques :

- Pour les fournisseurs personnalisés, `reasoning`, `input`, `cost`, `contextWindow` et `maxTokens` sont facultatifs.
  Lorsqu'ils sont omis, OpenClaw utilise par défaut :
  - `reasoning: false`
  - `input: ["text"]`
  - `cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }`
  - `contextWindow: 200000`
  - `maxTokens: 8192`
- Recommandation : définissez des valeurs explicites correspondant aux limites de votre proxy/modèle.

## Exemples CLI

```bash
openclaw onboard --auth-choice opencode-zen
openclaw models set opencode/claude-opus-4-5
openclaw models list
```

Consultez également : [/gateway/configuration](/gateway/configuration) pour des exemples de configuration complets.
