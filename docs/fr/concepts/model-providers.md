---
summary: "Aperçu des fournisseurs de modèles avec exemples de configurations + flux CLI"
read_when:
  - You need a provider-by-provider model setup reference
  - You want example configs or CLI onboarding commands for model providers
title: "Fournisseurs de modèles"
---

# Fournisseurs de modèles

Cette page couvre les **fournisseurs LLM/modèles** (pas les canaux de chat comme WhatsApp/Telegram).
Pour les règles de sélection de modèles, voir [/concepts/models](/concepts/models).

## Règles rapides

- Les références de modèles utilisent `provider/model` (exemple : `opencode/claude-opus-4-6`).
- Si vous définissez `agents.defaults.models`, cela devient la liste d'autorisation.
- Assistants CLI : `openclaw onboard`, `openclaw models list`, `openclaw models set <provider/model>`.

## Rotation des clés API

- Supporte la rotation générique des fournisseurs pour les fournisseurs sélectionnés.
- Configurez plusieurs clés via :
  - `OPENCLAW_LIVE_<PROVIDER>_KEY` (remplacement en direct unique, priorité la plus élevée)
  - `<PROVIDER>_API_KEYS` (liste séparée par des virgules ou des points-virgules)
  - `<PROVIDER>_API_KEY` (clé primaire)
  - `<PROVIDER>_API_KEY_*` (liste numérotée, par exemple `<PROVIDER>_API_KEY_1`)
- Pour les fournisseurs Google, `GOOGLE_API_KEY` est également inclus comme secours.
- L'ordre de sélection des clés préserve la priorité et déduplique les valeurs.
- Les demandes sont réessayées avec la clé suivante uniquement sur les réponses de limite de débit (par exemple `429`, `rate_limit`, `quota`, `resource exhausted`).
- Les défaillances non liées aux limites de débit échouent immédiatement ; aucune rotation de clé n'est tentée.
- Lorsque toutes les clés candidates échouent, l'erreur finale est renvoyée de la dernière tentative.

## Fournisseurs intégrés (catalogue pi-ai)

OpenClaw est livré avec le catalogue pi‑ai. Ces fournisseurs ne nécessitent **pas** de configuration `models.providers` ; définissez simplement l'authentification + choisissez un modèle.

### OpenAI

- Fournisseur : `openai`
- Authentification : `OPENAI_API_KEY`
- Rotation optionnelle : `OPENAI_API_KEYS`, `OPENAI_API_KEY_1`, `OPENAI_API_KEY_2`, plus `OPENCLAW_LIVE_OPENAI_KEY` (remplacement unique)
- Modèles d'exemple : `openai/gpt-5.4`, `openai/gpt-5.4-pro`
- CLI : `openclaw onboard --auth-choice openai-api-key`
- Le transport par défaut est `auto` (WebSocket en premier, secours SSE)
- Remplacez par modèle via `agents.defaults.models["openai/<model>"].params.transport` (`"sse"`, `"websocket"`, ou `"auto"`)
- L'échauffement WebSocket des réponses OpenAI est activé par défaut via `params.openaiWsWarmup` (`true`/`false`)
- Le traitement prioritaire OpenAI peut être activé via `agents.defaults.models["openai/<model>"].params.serviceTier`
- Le mode rapide OpenAI peut être activé par modèle via `agents.defaults.models["<provider>/<model>"].params.fastMode`
- `openai/gpt-5.3-codex-spark` est intentionnellement supprimé dans OpenClaw car l'API OpenAI en direct le rejette ; Spark est traité comme Codex uniquement

```json5
{
  agents: { defaults: { model: { primary: "openai/gpt-5.4" } } },
}
```

### Anthropic

- Fournisseur : `anthropic`
- Authentification : `ANTHROPIC_API_KEY` ou `claude setup-token`
- Rotation optionnelle : `ANTHROPIC_API_KEYS`, `ANTHROPIC_API_KEY_1`, `ANTHROPIC_API_KEY_2`, plus `OPENCLAW_LIVE_ANTHROPIC_KEY` (remplacement unique)
- Modèle d'exemple : `anthropic/claude-opus-4-6`
- CLI : `openclaw onboard --auth-choice token` (collez setup-token) ou `openclaw models auth paste-token --provider anthropic`
- Les modèles de clé API directe supportent le commutateur `/fast` partagé et `params.fastMode` ; OpenClaw le mappe à Anthropic `service_tier` (`auto` vs `standard_only`)
- Note de politique : le support du setup-token est une compatibilité technique ; Anthropic a bloqué certains usages d'abonnement en dehors de Claude Code par le passé. Vérifiez les conditions actuelles d'Anthropic et décidez en fonction de votre tolérance au risque.
- Recommandation : l'authentification par clé API Anthropic est le chemin plus sûr et recommandé par rapport à l'authentification par setup-token d'abonnement.

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

### OpenAI Code (Codex)

- Fournisseur : `openai-codex`
- Authentification : OAuth (ChatGPT)
- Modèle d'exemple : `openai-codex/gpt-5.4`
- CLI : `openclaw onboard --auth-choice openai-codex` ou `openclaw models auth login --provider openai-codex`
- Le transport par défaut est `auto` (WebSocket en premier, secours SSE)
- Remplacez par modèle via `agents.defaults.models["openai-codex/<model>"].params.transport` (`"sse"`, `"websocket"`, ou `"auto"`)
- Partage le même commutateur `/fast` et la configuration `params.fastMode` que `openai/*` direct
- `openai-codex/gpt-5.3-codex-spark` reste disponible lorsque le catalogue OAuth Codex l'expose ; dépendant des droits
- Note de politique : OpenAI Codex OAuth est explicitement supporté pour les outils/flux de travail externes comme OpenClaw.

```json5
{
  agents: { defaults: { model: { primary: "openai-codex/gpt-5.4" } } },
}
```

### OpenCode

- Authentification : `OPENCODE_API_KEY` (ou `OPENCODE_ZEN_API_KEY`)
- Fournisseur de runtime Zen : `opencode`
- Fournisseur de runtime Go : `opencode-go`
- Modèles d'exemple : `opencode/claude-opus-4-6`, `opencode-go/kimi-k2.5`
- CLI : `openclaw onboard --auth-choice opencode-zen` ou `openclaw onboard --auth-choice opencode-go`

```json5
{
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-6" } } },
}
```

### Google Gemini (clé API)

- Fournisseur : `google`
- Authentification : `GEMINI_API_KEY`
- Rotation optionnelle : `GEMINI_API_KEYS`, `GEMINI_API_KEY_1`, `GEMINI_API_KEY_2`, secours `GOOGLE_API_KEY`, et `OPENCLAW_LIVE_GEMINI_KEY` (remplacement unique)
- Modèles d'exemple : `google/gemini-3.1-pro-preview`, `google/gemini-3-flash-preview`
- Compatibilité : la configuration OpenClaw héritée utilisant `google/gemini-3.1-flash-preview` est normalisée en `google/gemini-3-flash-preview`
- CLI : `openclaw onboard --auth-choice gemini-api-key`

### Google Vertex, Antigravity et Gemini CLI

- Fournisseurs : `google-vertex`, `google-antigravity`, `google-gemini-cli`
- Authentification : Vertex utilise gcloud ADC ; Antigravity/Gemini CLI utilisent leurs flux d'authentification respectifs
- Attention : Antigravity et Gemini CLI OAuth dans OpenClaw sont des intégrations non officielles. Certains utilisateurs ont signalé des restrictions de compte Google après avoir utilisé des clients tiers. Consultez les conditions de Google et utilisez un compte non critique si vous choisissez de continuer.
- Antigravity OAuth est livré en tant que plugin fourni (`google-antigravity-auth`, désactivé par défaut).
  - Activer : `openclaw plugins enable google-antigravity-auth`
  - Connexion : `openclaw models auth login --provider google-antigravity --set-default`
- Gemini CLI OAuth est livré en tant que plugin fourni (`google-gemini-cli-auth`, désactivé par défaut).
  - Activer : `openclaw plugins enable google-gemini-cli-auth`
  - Connexion : `openclaw models auth login --provider google-gemini-cli --set-default`
  - Note : vous ne collez **pas** un ID client ou un secret dans `openclaw.json`. Le flux de connexion CLI stocke les jetons dans les profils d'authentification sur l'hôte de la passerelle.

### Z.AI (GLM)

- Fournisseur : `zai`
- Authentification : `ZAI_API_KEY`
- Modèle d'exemple : `zai/glm-5`
- CLI : `openclaw onboard --auth-choice zai-api-key`
  - Alias : `z.ai/*` et `z-ai/*` se normalisent en `zai/*`

### Vercel AI Gateway

- Fournisseur : `vercel-ai-gateway`
- Authentification : `AI_GATEWAY_API_KEY`
- Modèle d'exemple : `vercel-ai-gateway/anthropic/claude-opus-4.6`
- CLI : `openclaw onboard --auth-choice ai-gateway-api-key`

### Kilo Gateway

- Fournisseur : `kilocode`
- Authentification : `KILOCODE_API_KEY`
- Modèle d'exemple : `kilocode/anthropic/claude-opus-4.6`
- CLI : `openclaw onboard --kilocode-api-key <key>`
- URL de base : `https://api.kilo.ai/api/gateway/`
- Le catalogue intégré étendu inclut GLM-5 Free, MiniMax M2.5 Free, GPT-5.2, Gemini 3 Pro Preview, Gemini 3 Flash Preview, Grok Code Fast 1 et Kimi K2.5.

Voir [/providers/kilocode](/providers/kilocode) pour les détails de configuration.

### Autres fournisseurs intégrés

- OpenRouter : `openrouter` (`OPENROUTER_API_KEY`)
- Modèle d'exemple : `openrouter/anthropic/claude-sonnet-4-5`
- Kilo Gateway : `kilocode` (`KILOCODE_API_KEY`)
- Modèle d'exemple : `kilocode/anthropic/claude-opus-4.6`
- xAI : `xai` (`XAI_API_KEY`)
- Mistral : `mistral` (`MISTRAL_API_KEY`)
- Modèle d'exemple : `mistral/mistral-large-latest`
- CLI : `openclaw onboard --auth-choice mistral-api-key`
- Groq : `groq` (`GROQ_API_KEY`)
- Cerebras : `cerebras` (`CEREBRAS_API_KEY`)
  - Les modèles GLM sur Cerebras utilisent les identifiants `zai-glm-4.7` et `zai-glm-4.6`.
  - URL de base compatible OpenAI : `https://api.cerebras.ai/v1`.
- GitHub Copilot : `github-copilot` (`COPILOT_GITHUB_TOKEN` / `GH_TOKEN` / `GITHUB_TOKEN`)
- Hugging Face Inference : `huggingface` (`HUGGINGFACE_HUB_TOKEN` ou `HF_TOKEN`) — routeur compatible OpenAI ; modèle d'exemple : `huggingface/deepseek-ai/DeepSeek-R1` ; CLI : `openclaw onboard --auth-choice huggingface-api-key`. Voir [Hugging Face (Inference)](/providers/huggingface).

## Fournisseurs via `models.providers` (personnalisé/URL de base)

Utilisez `models.providers` (ou `models.json`) pour ajouter des fournisseurs **personnalisés** ou des proxies compatibles OpenAI/Anthropic.

### Moonshot AI (Kimi)

Moonshot utilise des points de terminaison compatibles OpenAI, configurez-le donc en tant que fournisseur personnalisé :

- Fournisseur : `moonshot`
- Authentification : `MOONSHOT_API_KEY`
- Modèle d'exemple : `moonshot/kimi-k2.5`

Identifiants de modèle Kimi K2 :

<!-- markdownlint-disable MD037 -->

{/_ moonshot-kimi-k2-model-refs:start _/ && null}

<!-- markdownlint-enable MD037 -->

- `moonshot/kimi-k2.5`
- `moonshot/kimi-k2-0905-preview`
- `moonshot/kimi-k2-turbo-preview`
- `moonshot/kimi-k2-thinking`
- `moonshot/kimi-k2-thinking-turbo`
  <!-- markdownlint-disable MD037 -->
  {/_ moonshot-kimi-k2-model-refs:end _/ && null}
  <!-- markdownlint-enable MD037 -->

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
- Modèle d'exemple : `kimi-coding/k2p5`

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: { model: { primary: "kimi-coding/k2p5" } },
  },
}
```

### Qwen OAuth (niveau gratuit)

Qwen fournit un accès OAuth à Qwen C
