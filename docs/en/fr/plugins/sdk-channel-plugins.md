---
title: "Channel Plugin SDK"
sidebarTitle: "Channel Plugins"
summary: "Contrats et assistants pour les plugins de canal de messagerie natifs, incluant les actions, le routage, l'appairage et la configuration"
read_when:
  - You are building a native channel plugin
  - You need to implement the shared `message` tool for a channel
  - You need pairing, setup, or routing helpers for a channel
---

# Channel Plugin SDK

Les plugins de canal utilisent `defineChannelPluginEntry(...)` depuis
`openclaw/plugin-sdk/core` et implémentent le contrat `ChannelPlugin`.

## Entrée de canal minimale

```ts
import { defineChannelPluginEntry } from "openclaw/plugin-sdk/core";
import { exampleChannelPlugin } from "./src/channel.js";
import { setExampleRuntime } from "./src/runtime.js";

export default defineChannelPluginEntry({
  id: "example-channel",
  name: "Example Channel",
  description: "Example native channel plugin",
  plugin: exampleChannelPlugin,
  setRuntime: setExampleRuntime,
});
```

## Forme de `ChannelPlugin`

Sections importantes du contrat :

- `meta` : documentation, étiquettes et métadonnées du sélecteur
- `capabilities` : réponses, sondages, réactions, fils de discussion, médias et types de chat
- `config` et `configSchema` : résolution de compte et analyse de configuration
- `setup` et `setupWizard` : flux d'intégration/configuration
- `security` : politique de MP et comportement de liste blanche
- `messaging` : analyse de cible et routage de session sortante
- `actions` : découverte et exécution de l'outil `message` partagé
- `pairing`, `threading`, `status`, `lifecycle`, `groups`, `directory`

Pour les types purs, importez depuis `openclaw/plugin-sdk/channel-contract`.

## Outil `message` partagé

Les plugins de canal possèdent leur partie spécifique au canal de l'outil `message` partagé
via `ChannelMessageActionAdapter`.

```ts
import { Type } from "@sinclair/typebox";
import { createMessageToolButtonsSchema } from "openclaw/plugin-sdk/channel-actions";

export const exampleActions = {
  describeMessageTool() {
    return {
      actions: ["send", "edit"],
      capabilities: ["buttons"],
      schema: {
        visibility: "current-channel",
        properties: {
          buttons: createMessageToolButtonsSchema(),
          threadId: Type.String(),
        },
      },
    };
  },
  async handleAction(ctx) {
    if (ctx.action === "send") {
      return {
        content: [{ type: "text", text: `send to ${String(ctx.params.to)}` }],
      };
    }

    return {
      content: [{ type: "text", text: `unsupported action: ${ctx.action}` }],
    };
  },
};
```

Types clés :

- `ChannelMessageActionAdapter`
- `ChannelMessageActionContext`
- `ChannelMessageActionDiscoveryContext`
- `ChannelMessageToolDiscovery`

## Assistants de routage sortant

Quand un plugin de canal a besoin d'un routage sortant personnalisé, implémentez
`messaging.resolveOutboundSessionRoute(...)`.

Utilisez `buildChannelOutboundSessionRoute(...)` depuis `plugin-sdk/core` pour retourner la
charge utile de route standard :

```ts
import { buildChannelOutboundSessionRoute } from "openclaw/plugin-sdk/core";

const messaging = {
  resolveOutboundSessionRoute({ cfg, agentId, accountId, target }) {
    return buildChannelOutboundSessionRoute({
      cfg,
      agentId,
      channel: "example-channel",
      accountId,
      peer: { kind: "direct", id: target },
      chatType: "direct",
      from: accountId ?? "default",
      to: target,
    });
  },
};
```

## Assistants d'appairage

Utilisez `plugin-sdk/channel-pairing` pour les flux d'approbation de MP :

```ts
import { createChannelPairingController } from "openclaw/plugin-sdk/channel-pairing";

const pairing = createChannelPairingController({
  core: runtime,
  channel: "example-channel",
  accountId: "default",
});

const result = pairing.issueChallenge({
  agentId: "assistant",
  requesterId: "user-123",
});
```

Cette surface vous donne également un accès limité aux assistants de stockage d'appairage tels que
les lectures de liste blanche et les mises à jour de demandes.

## Assistants de configuration de canal

Utilisez :

- `plugin-sdk/channel-setup` pour les canaux optionnels ou installables
- `plugin-sdk/setup` pour les adaptateurs de configuration, la politique de MP et les invites de liste blanche
- `plugin-sdk/webhook-ingress` pour les routes webhook appartenant au plugin

## Conseils pour les plugins de canal

- Gardez l'exécution spécifique au transport à l'intérieur du package de canal.
- Utilisez les types `channel-contract` dans les tests et les assistants locaux.
- Gardez `describeMessageTool(...)` et `handleAction(...)` alignés.
- Gardez le routage de session dans `messaging`, pas dans les gestionnaires de commandes ad hoc.
- Préférez les sous-chemins ciblés au couplage large du runtime.

## Connexes

- [Plugin SDK Overview](/fr/plugins/sdk-overview)
- [Plugin Entry Points](/fr/plugins/sdk-entrypoints)
- [Plugin Setup](/fr/plugins/sdk-setup)
- [Plugin Internals](/fr/plugins/architecture)
