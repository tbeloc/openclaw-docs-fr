---
title: "SDK du plugin fournisseur"
sidebarTitle: "Plugins fournisseurs"
summary: "Contrats et sous-chemins d'aide pour les plugins de fournisseur de modèles, incluant l'authentification, l'intégration, les catalogues et l'utilisation"
read_when:
  - You are building a model provider plugin
  - You need auth helpers for API keys or OAuth
  - You need onboarding config patches or catalog helpers
---

# SDK du plugin fournisseur

Les plugins fournisseurs utilisent `definePluginEntry(...)` et appellent `api.registerProvider(...)`
avec une définition `ProviderPlugin`.

## Entrée fournisseur minimale

```ts
import { definePluginEntry, type OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";

export default definePluginEntry({
  id: "example-provider",
  name: "Example Provider",
  description: "Example text-inference provider plugin",
  register(api: OpenClawPluginApi) {
    api.registerProvider({
      id: "example",
      label: "Example",
      auth: [],
    });
  },
});
```

## Sous-chemins fournisseur

| Sous-chemin                             | À utiliser pour                                |
| --------------------------------------- | ---------------------------------------------- |
| `plugin-sdk/provider-auth`              | Clé API, OAuth, profil d'authentification et aides PKCE |
| `plugin-sdk/provider-onboard`           | Correctifs de configuration après configuration/authentification |
| `plugin-sdk/provider-models`            | Définition de modèle et aides de catalogue    |
| `plugin-sdk/provider-setup`             | Flux de configuration partagés locaux/auto-hébergés |
| `plugin-sdk/self-hosted-provider-setup` | Fournisseurs auto-hébergés compatibles OpenAI |
| `plugin-sdk/provider-usage`             | Aides de récupération d'instantané d'utilisation |

## Authentification par clé API

`createProviderApiKeyAuthMethod(...)` est l'aide standard pour les fournisseurs
avec clé API :

```ts
import { createProviderApiKeyAuthMethod } from "openclaw/plugin-sdk/provider-auth";
import { applyProviderConfigWithDefaultModel } from "openclaw/plugin-sdk/provider-onboard";

const auth = [
  createProviderApiKeyAuthMethod({
    providerId: "example",
    methodId: "api-key",
    label: "Example API key",
    optionKey: "exampleApiKey",
    flagName: "--example-api-key",
    envVar: "EXAMPLE_API_KEY",
    promptMessage: "Enter Example API key",
    profileId: "example:default",
    defaultModel: "example/default",
    applyConfig: (cfg) =>
      applyProviderConfigWithDefaultModel(cfg, "example", {
        id: "default",
        name: "Default",
      }),
  }),
];
```

## Authentification OAuth

`buildOauthProviderAuthResult(...)` construit la charge utile de résultat d'authentification standard pour
les fournisseurs de style OAuth :

```ts
import { buildOauthProviderAuthResult } from "openclaw/plugin-sdk/provider-auth";

async function runOAuthLogin() {
  return buildOauthProviderAuthResult({
    providerId: "example-portal",
    defaultModel: "example-portal/default",
    access: "access-token",
    refresh: "refresh-token",
    email: "user@example.com",
    notes: ["Tokens auto-refresh when the provider supports refresh tokens."],
  });
}
```

## Crochets de catalogue et de découverte

Les plugins fournisseurs implémentent généralement soit `catalog`, soit l'alias hérité `discovery`.
`catalog` est préféré.

```ts
api.registerProvider({
  id: "example",
  label: "Example",
  auth,
  catalog: {
    order: "simple",
    async run(ctx) {
      const apiKey = ctx.resolveProviderApiKey("example").apiKey;
      if (!apiKey) {
        return null;
      }
      return {
        provider: {
          api: "openai",
          baseUrl: "https://api.example.com/v1",
          apiKey,
          models: [
            {
              id: "default",
              name: "Default",
              input: ["text"],
            },
          ],
        },
      };
    },
  },
});
```

## Correctifs de configuration d'intégration

`plugin-sdk/provider-onboard` maintient les écritures de configuration post-authentification cohérentes.

Aides courantes :

- `applyProviderConfigWithDefaultModel(...)`
- `applyProviderConfigWithDefaultModels(...)`
- `applyProviderConfigWithModelCatalog(...)`
- `applyAgentDefaultModelPrimary(...)`
- `ensureModelAllowlistEntry(...)`

## Configuration de modèle auto-hébergé et local

Utilisez `plugin-sdk/provider-setup` ou
`plugin-sdk/self-hosted-provider-setup` lorsque le fournisseur est un backend de style OpenAI, Ollama, SGLang ou vLLM.

Exemples des surfaces de configuration partagées :

- `promptAndConfigureOllama(...)`
- `configureOllamaNonInteractive(...)`
- `promptAndConfigureOpenAICompatibleSelfHostedProvider(...)`
- `discoverOpenAICompatibleSelfHostedProvider(...)`

Ces aides maintiennent le comportement de configuration aligné avec les flux de fournisseur intégrés.

## Instantanés d'utilisation

Si le fournisseur possède des points de terminaison de quota ou d'utilisation, utilisez `resolveUsageAuth(...)` et
`fetchUsageSnapshot(...)`.

`plugin-sdk/provider-usage` inclut des aides de récupération partagées telles que :

- `fetchClaudeUsage(...)`
- `fetchCodexUsage(...)`
- `fetchGeminiUsage(...)`
- `fetchMinimaxUsage(...)`
- `fetchZaiUsage(...)`

## Conseils fournisseur

- Gardez la logique d'authentification dans `provider-auth`.
- Gardez la mutation de configuration dans `provider-onboard`.
- Gardez les aides de catalogue/modèle dans `provider-models`.
- Gardez la logique d'utilisation dans `provider-usage`.
- Utilisez `catalog`, pas `discovery`, dans les nouveaux plugins.

## Connexes

- [Aperçu du SDK du plugin](/fr/plugins/sdk-overview)
- [Points d'entrée du plugin](/fr/plugins/sdk-entrypoints)
- [Configuration du plugin](/fr/plugins/sdk-setup)
- [Éléments internes du plugin](/fr/plugins/architecture#provider-runtime-hooks)
