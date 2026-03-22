---
title: "Aperçu du SDK Plugin"
sidebarTitle: "Aperçu du SDK"
summary: "Comment le SDK plugin OpenClaw est organisé, quels sous-chemins sont stables et comment choisir la bonne importation"
read_when:
  - You are starting a new OpenClaw plugin
  - You need to choose the right plugin-sdk subpath
  - You are replacing deprecated compat imports
---

# Aperçu du SDK Plugin

Le SDK plugin OpenClaw est divisé en **petits sous-chemins publics** sous
`openclaw/plugin-sdk/<subpath>`.

Utilisez l'importation la plus ciblée qui correspond à votre besoin. Cela maintient les dépendances du plugin petites, évite les importations circulaires et clarifie le contrat sur lequel vous dépendez.

## Règles d'abord

- Utilisez des importations ciblées telles que `openclaw/plugin-sdk/plugin-entry`.
- N'importez pas le barrel racine `openclaw/plugin-sdk` dans le nouveau code.
- N'importez pas `openclaw/extension-api` dans le nouveau code.
- N'importez pas `src/**` depuis les packages de plugin.
- À l'intérieur d'un package de plugin, routez les importations internes via des fichiers locaux tels que
  `./api.ts` ou `./runtime-api.ts`, pas via le chemin SDK publié pour ce même plugin.

## Carte du SDK

| Tâche                          | Sous-chemin                                                                                                                                     | Page suivante                                        |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| Définir les modules d'entrée du plugin  | `plugin-sdk/plugin-entry`, `plugin-sdk/core`                                                                                                    | [Points d'entrée du plugin](/fr/plugins/sdk-entrypoints)      |
| Utiliser les helpers runtime injectés | `plugin-sdk/runtime`, `plugin-sdk/runtime-store`                                                                                                | [Runtime du plugin](/fr/plugins/sdk-runtime)               |
| Construire les flux de configuration/setup  | `plugin-sdk/setup`, `plugin-sdk/channel-setup`, `plugin-sdk/secret-input`                                                                       | [Configuration du plugin](/fr/plugins/sdk-setup)                   |
| Construire les plugins de canal        | `plugin-sdk/core`, `plugin-sdk/channel-contract`, `plugin-sdk/channel-actions`, `plugin-sdk/channel-pairing`                                    | [SDK des plugins de canal](/fr/plugins/sdk-channel-plugins)   |
| Construire les plugins de fournisseur       | `plugin-sdk/plugin-entry`, `plugin-sdk/provider-auth`, `plugin-sdk/provider-onboard`, `plugin-sdk/provider-models`, `plugin-sdk/provider-usage` | [SDK des plugins de fournisseur](/fr/plugins/sdk-provider-plugins) |
| Tester le code du plugin             | `plugin-sdk/testing`                                                                                                                            | [Test du SDK Plugin](/fr/plugins/sdk-testing)           |

## Disposition typique du plugin

```text
my-plugin/
├── package.json
├── openclaw.plugin.json
├── index.ts
├── setup-entry.ts
├── api.ts
├── runtime-api.ts
└── src/
    ├── provider.ts
    ├── setup.ts
    └── provider.test.ts
```

```ts
// api.ts
export {
  definePluginEntry,
  type OpenClawPluginApi,
  type ProviderAuthContext,
  type ProviderAuthResult,
} from "openclaw/plugin-sdk/plugin-entry";
```

## Ce qui va où

### Helpers d'entrée

- `plugin-sdk/plugin-entry` est la surface d'entrée par défaut pour les fournisseurs, outils,
  commandes, services, plugins de mémoire et moteurs de contexte.
- `plugin-sdk/core` ajoute des helpers axés sur les canaux tels que
  `defineChannelPluginEntry(...)`.

### Helpers runtime

- Utilisez `api.runtime.*` pour les helpers de confiance en processus qu'OpenClaw injecte au
  moment de l'enregistrement.
- Utilisez `plugin-sdk/runtime-store` quand les modules de plugin ont besoin d'un slot runtime mutable
  qui est initialisé plus tard.

### Helpers de configuration

- `plugin-sdk/setup` contient les helpers partagés de l'assistant de configuration et les
  helpers de patch de configuration.
- `plugin-sdk/channel-setup` contient les adaptateurs de configuration spécifiques aux canaux.
- `plugin-sdk/secret-input` expose les helpers partagés du schéma d'entrée secrète.

### Helpers de canal

- `plugin-sdk/channel-contract` exporte les types de canal purs.
- `plugin-sdk/channel-actions` couvre les helpers partagés du schéma d'outil `message`.
- `plugin-sdk/channel-pairing` couvre les flux d'approbation d'appairage.
- `plugin-sdk/webhook-ingress` couvre les routes webhook appartenant au plugin.

### Helpers de fournisseur

- `plugin-sdk/provider-auth` couvre les flux d'authentification et les helpers d'identifiants.
- `plugin-sdk/provider-onboard` couvre les patches de configuration après l'authentification/configuration.
- `plugin-sdk/provider-models` couvre les helpers de catalogue et de définition de modèle.
- `plugin-sdk/provider-usage` couvre les helpers de snapshot d'utilisation.
- `plugin-sdk/provider-setup` et `plugin-sdk/self-hosted-provider-setup`
  couvrent l'intégration des modèles auto-hébergés et locaux.

## Exemple : mélanger les sous-chemins dans un plugin

```ts
import { definePluginEntry, type OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";
import { createProviderApiKeyAuthMethod } from "openclaw/plugin-sdk/provider-auth";
import { applyProviderConfigWithDefaultModel } from "openclaw/plugin-sdk/provider-onboard";
import { buildSecretInputSchema } from "openclaw/plugin-sdk/secret-input";

export default definePluginEntry({
  id: "example-provider",
  name: "Example Provider",
  description: "Small provider plugin example",
  configSchema: {
    jsonSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        apiKey: { type: "string" },
      },
    },
    safeParse(value) {
      return buildSecretInputSchema().safeParse((value as { apiKey?: unknown })?.apiKey);
    },
  },
  register(api: OpenClawPluginApi) {
    api.registerProvider({
      id: "example",
      label: "Example",
      auth: [
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
      ],
    });
  },
});
```

## Choisir la plus petite couture publique

Si un helper existe sur un sous-chemin ciblé, préférez-le à une surface runtime plus large.

- Préférez `plugin-sdk/provider-auth` à l'accès à des fichiers de fournisseur non liés.
- Préférez `plugin-sdk/channel-contract` pour les types dans les tests et les modules d'aide.
- Préférez `plugin-sdk/runtime-store` aux globals mutables personnalisés.
- Préférez `plugin-sdk/testing` pour les fixtures de test partagées.

## Connexes

- [Construire des plugins](/fr/plugins/building-plugins)
- [Points d'entrée du plugin](/fr/plugins/sdk-entrypoints)
- [Runtime du plugin](/fr/plugins/sdk-runtime)
- [Configuration du plugin](/fr/plugins/sdk-setup)
- [SDK des plugins de canal](/fr/plugins/sdk-channel-plugins)
- [SDK des plugins de fournisseur](/fr/plugins/sdk-provider-plugins)
- [Test du SDK Plugin](/fr/plugins/sdk-testing)
- [Migration du SDK Plugin](/fr/plugins/sdk-migration)
