---
title: "Runtime du plugin"
sidebarTitle: "Runtime"
summary: "Comment fonctionne `api.runtime`, quand l'utiliser et comment gérer l'état du runtime du plugin en toute sécurité"
read_when:
  - You need to call runtime helpers from a plugin
  - You are deciding between hooks and injected runtime
  - You need a safe module-level runtime store
---

# Runtime du plugin

Les plugins OpenClaw natifs reçoivent un runtime de confiance via `api.runtime`.

Utilisez-le pour les **opérations détenues par l'hôte** qui doivent rester dans le runtime d'OpenClaw :

- lecture et écriture de la configuration
- assistants/aides de session
- commandes système avec délais d'expiration OpenClaw
- appels de runtime pour les médias, la parole, la génération d'images et la recherche web
- aides détenues par le canal pour les plugins de canal groupés

## Quand utiliser le runtime par rapport aux aides SDK ciblés

- Utilisez les aides SDK ciblés quand un sous-chemin public modélise déjà le travail.
- Utilisez `api.runtime.*` quand l'hôte détient l'opération ou l'état.
- Préférez les hooks pour les intégrations libres qui n'ont pas besoin d'un accès étroit en processus.

## Espaces de noms du runtime

| Espace de noms                   | Ce qu'il couvre                                    |
| -------------------------------- | -------------------------------------------------- |
| `api.runtime.config`             | Charger et persister la configuration OpenClaw    |
| `api.runtime.agent`              | Espace de travail, identité, délais d'expiration, magasin de session |
| `api.runtime.system`             | Événements système, pulsations, exécution de commandes |
| `api.runtime.media`              | Chargement et transformations de fichiers/médias  |
| `api.runtime.tts`                | Synthèse vocale et liste des voix                 |
| `api.runtime.mediaUnderstanding` | Compréhension d'images/audio/vidéo                |
| `api.runtime.imageGeneration`    | Fournisseurs de génération d'images                |
| `api.runtime.webSearch`          | Exécution de recherche web au runtime             |
| `api.runtime.modelAuth`          | Résoudre les identifiants de modèle/fournisseur   |
| `api.runtime.subagent`           | Créer, attendre, inspecter et supprimer des sessions de sous-agent |
| `api.runtime.channel`            | Aides lourdes pour les canaux pour les plugins de canal natifs |

## Exemple : lire et persister la configuration

```ts
import { definePluginEntry, type OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";

export default definePluginEntry({
  id: "talk-settings",
  name: "Talk Settings",
  description: "Example runtime config write",
  register(api: OpenClawPluginApi) {
    api.registerCommand({
      name: "talk-mode",
      description: "Enable talk mode",
      handler: async () => {
        const cfg = api.runtime.config.loadConfig();
        const nextConfig = {
          ...cfg,
          talk: {
            ...cfg.talk,
            enabled: true,
          },
        };
        await api.runtime.config.writeConfigFile(nextConfig);
        return { text: "talk mode enabled" };
      },
    });
  },
});
```

## Exemple : utiliser un service de runtime détenu par OpenClaw

```ts
const cfg = api.runtime.config.loadConfig();
const voices = await api.runtime.tts.listVoices({
  provider: "openai",
  cfg,
});

return {
  text: voices.map((voice) => `${voice.name ?? voice.id}: ${voice.id}`).join("\n"),
};
```

## `createPluginRuntimeStore(...)`

Les modules de plugin ont souvent besoin d'un petit emplacement mutable pour les aides soutenus par le runtime. Utilisez
`plugin-sdk/runtime-store` au lieu d'un `let runtime` non gardé.

```ts
import { defineChannelPluginEntry } from "openclaw/plugin-sdk/core";
import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";
import { channelPlugin } from "./src/channel.js";

const runtimeStore = createPluginRuntimeStore<{
  logger: { info(message: string): void };
}>("Example Channel runtime not initialized");

export function setExampleRuntime(runtime: { logger: { info(message: string): void } }) {
  runtimeStore.setRuntime(runtime);
}

export function getExampleRuntime() {
  return runtimeStore.getRuntime();
}

export default defineChannelPluginEntry({
  id: "example-channel",
  name: "Example Channel",
  description: "Example runtime store usage",
  plugin: channelPlugin,
  setRuntime: setExampleRuntime,
});
```

`createPluginRuntimeStore(...)` vous donne :

- `setRuntime(next)`
- `clearRuntime()`
- `tryGetRuntime()`
- `getRuntime()`

`getRuntime()` lève une exception avec votre message personnalisé si le runtime n'a jamais été défini.

## Note sur le runtime du canal

`api.runtime.channel.*` est l'espace de noms le plus lourd. Il existe pour les plugins de canal natifs
qui ont besoin d'un couplage étroit avec la pile de messagerie OpenClaw.

Préférez les sous-chemins plus étroits tels que :

- `plugin-sdk/channel-pairing`
- `plugin-sdk/channel-actions`
- `plugin-sdk/channel-feedback`
- `plugin-sdk/channel-lifecycle`

Utilisez `api.runtime.channel.*` quand l'opération est clairement détenue par l'hôte et qu'il n'y a
pas de couture publique plus petite.

## Directives de sécurité du runtime

- Ne mettez pas en cache les instantanés de configuration plus longtemps que nécessaire.
- Préférez `createPluginRuntimeStore(...)` pour l'état du module partagé.
- Gardez le code soutenu par le runtime derrière de petits aides locaux.
- Évitez d'accéder aux espaces de noms de runtime dont vous n'avez pas besoin.

## Connexes

- [Aperçu du SDK du plugin](/fr/plugins/sdk-overview)
- [Points d'entrée du plugin](/fr/plugins/sdk-entrypoints)
- [Configuration du plugin](/fr/plugins/sdk-setup)
- [SDK du plugin de canal](/fr/plugins/sdk-channel-plugins)
