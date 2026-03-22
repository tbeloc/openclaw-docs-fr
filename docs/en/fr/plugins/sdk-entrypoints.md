---
title: "Points d'entrée des plugins"
sidebarTitle: "Points d'entrée"
summary: "Comment définir les fichiers d'entrée des plugins pour les plugins de fournisseur, outil, canal et configuration"
read_when:
  - You are writing a plugin `index.ts`
  - You need to choose between `definePluginEntry` and `defineChannelPluginEntry`
  - You are adding a separate `setup-entry.ts`
---

# Points d'entrée des plugins

OpenClaw dispose de deux principaux assistants d'entrée :

- `definePluginEntry(...)` pour les plugins généraux
- `defineChannelPluginEntry(...)` pour les canaux de messagerie native

Il y a aussi `defineSetupPluginEntry(...)` pour un module séparé réservé à la configuration.

## `definePluginEntry(...)`

Utilisez ceci pour les fournisseurs, outils, commandes, services, plugins de mémoire et moteurs de contexte.

```ts
import { definePluginEntry, type OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";

export default definePluginEntry({
  id: "example-tools",
  name: "Example Tools",
  description: "Adds a command and a tool",
  register(api: OpenClawPluginApi) {
    api.registerCommand({
      name: "example",
      description: "Show plugin status",
      handler: async () => ({ text: "example ok" }),
    });

    api.registerTool({
      name: "example_lookup",
      description: "Look up Example data",
      parameters: {
        type: "object",
        properties: {
          query: { type: "string" },
        },
        required: ["query"],
      },
      async execute(_callId, params) {
        return {
          content: [{ type: "text", text: `lookup: ${String(params.query)}` }],
        };
      },
    });
  },
});
```

## `defineChannelPluginEntry(...)`

Utilisez ceci pour un plugin qui enregistre un `ChannelPlugin`.

```ts
import { defineChannelPluginEntry } from "openclaw/plugin-sdk/core";
import { channelPlugin } from "./src/channel.js";
import { setRuntime } from "./src/runtime.js";

export default defineChannelPluginEntry({
  id: "example-channel",
  name: "Example Channel",
  description: "Example messaging plugin",
  plugin: channelPlugin,
  setRuntime,
  registerFull(api) {
    api.registerTool({
      name: "example_channel_status",
      description: "Inspect Example Channel state",
      parameters: { type: "object", properties: {} },
      async execute() {
        return { content: [{ type: "text", text: "ok" }] };
      },
    });
  },
});
```

### Pourquoi `registerFull(...)` existe

OpenClaw peut charger les plugins en modes d'enregistrement axés sur la configuration. `registerFull` permet à un plugin de canal de sauter les enregistrements supplémentaires réservés à l'exécution, tels que les outils, tout en enregistrant la capacité du canal elle-même.

Utilisez-le pour :

- les outils d'agent
- les routes réservées à la passerelle
- les commandes réservées à l'exécution

Ne l'utilisez pas pour le `ChannelPlugin` réel ; celui-ci appartient à `plugin: ...`.

## `defineSetupPluginEntry(...)`

Utilisez ceci quand un canal expédie un deuxième module pour les flux de configuration.

```ts
import { defineSetupPluginEntry } from "openclaw/plugin-sdk/core";
import { exampleSetupPlugin } from "./src/channel.setup.js";

export default defineSetupPluginEntry(exampleSetupPlugin);
```

Cela rend la forme du point d'entrée de configuration explicite et correspond au modèle de canal groupé utilisé dans OpenClaw.

## Un plugin, plusieurs capacités

Un seul fichier d'entrée peut enregistrer plusieurs capacités :

```ts
import { definePluginEntry, type OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";

export default definePluginEntry({
  id: "example-hybrid",
  name: "Example Hybrid",
  description: "Provider plus tools",
  register(api: OpenClawPluginApi) {
    api.registerProvider({
      id: "example",
      label: "Example",
      auth: [],
    });

    api.registerTool({
      name: "example_ping",
      description: "Simple health check",
      parameters: { type: "object", properties: {} },
      async execute() {
        return { content: [{ type: "text", text: "pong" }] };
      },
    });
  },
});
```

## Liste de contrôle du fichier d'entrée

- Donnez au plugin un `id` stable.
- Gardez `name` et `description` lisibles par l'homme.
- Mettez le schéma au niveau de l'entrée quand le plugin a une configuration.
- Enregistrez uniquement les capacités publiques à l'intérieur de `register(api)`.
- Gardez les plugins de canal sur `plugin-sdk/core`.
- Gardez les plugins non-canal sur `plugin-sdk/plugin-entry`.

## Connexes

- [Aperçu du SDK des plugins](/fr/plugins/sdk-overview)
- [Runtime du plugin](/fr/plugins/sdk-runtime)
- [SDK des plugins de canal](/fr/plugins/sdk-channel-plugins)
- [SDK des plugins de fournisseur](/fr/plugins/sdk-provider-plugins)
