---
read_when:
  - Vous souhaitez utiliser le modèle Xiaomi MiMo dans OpenClaw
  - Vous devez configurer XIAOMI_API_KEY
summary: Utiliser Xiaomi MiMo (mimo-v2-flash) dans OpenClaw
title: Xiaomi MiMo
x-i18n:
  generated_at: "2026-02-01T21:36:15Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 366fd2297b2caf8c5ad944d7f1b6d233b248fe43aedd22a28352ae7f370d2435
  source_path: providers/xiaomi.md
  workflow: 15
---

# Xiaomi MiMo

Xiaomi MiMo est une plateforme API pour le modèle **MiMo**. Elle fournit une API REST compatible avec les formats OpenAI et Anthropic, et utilise une clé API pour l'authentification. Créez votre clé API dans la [console Xiaomi MiMo](https://platform.xiaomimimo.com/#/console/api-keys). OpenClaw utilise le fournisseur `xiaomi` avec la clé API Xiaomi MiMo.

## Aperçu des modèles

- **mimo-v2-flash** : fenêtre de contexte de 262144 tokens, compatible avec l'API Anthropic Messages.
- URL de base : `https://api.xiaomimimo.com/anthropic`
- Méthode d'autorisation : `Bearer $XIAOMI_API_KEY`

## Configuration CLI

```bash
openclaw onboard --auth-choice xiaomi-api-key
# ou non-interactif
openclaw onboard --auth-choice xiaomi-api-key --xiaomi-api-key "$XIAOMI_API_KEY"
```

## Extrait de configuration

```json5
{
  env: { XIAOMI_API_KEY: "your-key" },
  agents: { defaults: { model: { primary: "xiaomi/mimo-v2-flash" } } },
  models: {
    mode: "merge",
    providers: {
      xiaomi: {
        baseUrl: "https://api.xiaomimimo.com/anthropic",
        api: "anthropic-messages",
        apiKey: "XIAOMI_API_KEY",
        models: [
          {
            id: "mimo-v2-flash",
            name: "Xiaomi MiMo V2 Flash",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Remarques

- Référence du modèle : `xiaomi/mimo-v2-flash`.
- Ce fournisseur est automatiquement injecté lorsque `XIAOMI_API_KEY` est défini (ou qu'un fichier de configuration d'authentification existe).
- Pour les règles des fournisseurs, consultez [/concepts/model-providers](/concepts/model-providers).
