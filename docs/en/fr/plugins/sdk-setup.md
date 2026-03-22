---
title: "Configuration du plugin"
sidebarTitle: "Configuration"
summary: "Assistants partagés de l'assistant de configuration pour les plugins de canal, les plugins de fournisseur et les entrées secrètes"
read_when:
  - You are building a setup or onboarding flow
  - You need shared allowlist or DM policy setup helpers
  - You need the shared secret-input schema
---

# Configuration du plugin

OpenClaw expose des assistants de configuration partagés pour que les flux de configuration des plugins se comportent comme les flux intégrés.

Sous-chemins principaux :

- `openclaw/plugin-sdk/setup`
- `openclaw/plugin-sdk/channel-setup`
- `openclaw/plugin-sdk/secret-input`

## Assistants de configuration de canal

Utilisez `plugin-sdk/channel-setup` quand un plugin de canal a besoin de l'adaptateur de configuration standard et des formes de l'assistant de configuration.

### Plugins de canal optionnels

Si un canal est installable mais pas toujours présent, utilisez
`createOptionalChannelSetupSurface(...)` :

```ts
import { createOptionalChannelSetupSurface } from "openclaw/plugin-sdk/channel-setup";

export const optionalExampleSetup = createOptionalChannelSetupSurface({
  channel: "example",
  label: "Example Channel",
  npmSpec: "@openclaw/example-channel",
  docsPath: "/channels/example",
});
```

Cela retourne :

- `setupAdapter`
- `setupWizard`

Les deux surfaces produisent une expérience cohérente « installez d'abord ce plugin ».

## Assistants de configuration partagés

`plugin-sdk/setup` réexporte les primitives de configuration utilisées par les canaux intégrés.

Assistants courants :

- `applySetupAccountConfigPatch(...)`
- `createPatchedAccountSetupAdapter(...)`
- `createEnvPatchedAccountSetupAdapter(...)`
- `createTopLevelChannelDmPolicy(...)`
- `setSetupChannelEnabled(...)`
- `promptResolvedAllowFrom(...)`
- `promptSingleChannelSecretInput(...)`

### Exemple : corriger la configuration du canal lors de la configuration

```ts
import {
  DEFAULT_ACCOUNT_ID,
  createPatchedAccountSetupAdapter,
  setSetupChannelEnabled,
} from "openclaw/plugin-sdk/setup";

export const exampleSetupAdapter = createPatchedAccountSetupAdapter({
  resolveAccountId: ({ accountId }) => accountId ?? DEFAULT_ACCOUNT_ID,
  applyPatch: ({ nextConfig, accountId }) => {
    const resolvedAccountId = accountId ?? DEFAULT_ACCOUNT_ID;
    return setSetupChannelEnabled({
      nextConfig,
      channel: "example",
      accountId: resolvedAccountId,
      enabled: true,
    });
  },
});
```

## Schéma d'entrée secrète

Utilisez `plugin-sdk/secret-input` au lieu de créer votre propre analyseur d'entrée secrète.

```ts
import {
  buildOptionalSecretInputSchema,
  buildSecretInputArraySchema,
  buildSecretInputSchema,
  hasConfiguredSecretInput,
} from "openclaw/plugin-sdk/secret-input";

const ApiKeySchema = buildSecretInputSchema();
const OptionalApiKeySchema = buildOptionalSecretInputSchema();
const ExtraKeysSchema = buildSecretInputArraySchema();

const parsed = OptionalApiKeySchema.safeParse(process.env.EXAMPLE_API_KEY);
if (parsed.success && hasConfiguredSecretInput(parsed.data)) {
  // ...
}
```

## Remarque sur la configuration du fournisseur

Les assistants d'intégration spécifiques au fournisseur se trouvent sur des sous-chemins axés sur le fournisseur :

- `plugin-sdk/provider-auth`
- `plugin-sdk/provider-onboard`
- `plugin-sdk/provider-setup`
- `plugin-sdk/self-hosted-provider-setup`

Voir [SDK du plugin fournisseur](/fr/plugins/sdk-provider-plugins).

## Conseils de configuration

- Gardez les schémas d'entrée de configuration stricts et petits.
- Réutilisez les assistants de liste d'autorisation, de politique DM et d'entrée secrète d'OpenClaw.
- Gardez les modules d'entrée de configuration minces ; déplacez le comportement dans `src/`.
- Liez la documentation à partir des flux de configuration quand les étapes d'installation ou d'authentification sont manuelles.

## Connexes

- [Aperçu du SDK du plugin](/fr/plugins/sdk-overview)
- [Points d'entrée du plugin](/fr/plugins/sdk-entrypoints)
- [SDK du plugin fournisseur](/fr/plugins/sdk-provider-plugins)
- [Manifeste du plugin](/fr/plugins/manifest)
