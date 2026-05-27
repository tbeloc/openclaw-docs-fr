---
summary: "API du cycle de vie des messages sortants pour les plugins de canal : adaptateurs, reçus, envois durables, aperçu en direct et assistants de pipeline de réponse"
title: "API sortante du canal"
read_when:
  - You are building or refactoring a messaging channel plugin send path
  - You need durable final reply delivery, receipts, live preview finalization, or receive acknowledgement policy
  - You are migrating from channel-message, channel-message-runtime, or legacy reply dispatch helpers
---

Les plugins de canal doivent exposer le comportement des messages sortants à partir de
`openclaw/plugin-sdk/channel-outbound`. Utilisez
`openclaw/plugin-sdk/channel-inbound` pour l'orchestration de réception/contexte/dispatch.

Core gère la mise en file d'attente, la durabilité, la politique de retry générique, les hooks, les reçus et l'outil `message` partagé. Le plugin gère les appels natifs d'envoi/édition/suppression, la normalisation des cibles, le threading de plateforme, les citations sélectionnées, les drapeaux de notification, l'état du compte et les effets secondaires spécifiques à la plateforme.

## Adaptateur

La plupart des plugins définissent un adaptateur `message` :

```ts
import {
  defineChannelMessageAdapter,
  createMessageReceiptFromOutboundResults,
} from "openclaw/plugin-sdk/channel-outbound";

export const demoMessageAdapter = defineChannelMessageAdapter({
  id: "demo",
  durableFinal: {
    capabilities: {
      text: true,
      replyTo: true,
      thread: true,
      messageSendingHooks: true,
    },
  },
  send: {
    text: async ({ cfg, to, text, accountId, replyToId, threadId, signal }) => {
      const sent = await sendDemoMessage({
        cfg,
        to,
        text,
        accountId: accountId ?? undefined,
        replyToId: replyToId ?? undefined,
        threadId: threadId == null ? undefined : String(threadId),
        signal,
      });

      return {
        receipt: createMessageReceiptFromOutboundResults({
          results: [{ channel: "demo", messageId: sent.id, conversationId: to }],
          kind: "text",
          threadId: threadId == null ? undefined : String(threadId),
          replyToId: replyToId ?? undefined,
        }),
      };
    },
  },
});
```

Déclarez uniquement les capacités que le transport natif préserve réellement. Couvrez chaque capacité d'envoi, de reçu, d'aperçu en direct et de réception déclarée avec les assistants de contrat exportés à partir de ce chemin.

## Adaptateurs Sortants Existants

Si le canal a déjà un adaptateur `outbound` compatible, dérivez l'adaptateur de message au lieu de dupliquer le code d'envoi :

```ts
import { createChannelMessageAdapterFromOutbound } from "openclaw/plugin-sdk/channel-outbound";

export const messageAdapter = createChannelMessageAdapterFromOutbound({
  id: "demo",
  outbound,
  durableFinal: {
    capabilities: {
      text: true,
      media: true,
    },
  },
});
```

## Envois Durables

Les assistants d'envoi runtime vivent également sur `channel-outbound` :

- `sendDurableMessageBatch(...)`
- `withDurableMessageSendContext(...)`
- `deliverInboundReplyWithMessageSendContext(...)`
- assistants de streaming/progression de brouillon tels que `resolveChannelStreamingPreviewChunk(...)`

`sendDurableMessageBatch(...)` retourne un résultat explicite :

- `sent` : au moins un message de plateforme visible a été livré.
- `suppressed` : aucun message de plateforme ne doit être traité comme manquant.
- `partial_failed` : au moins un message de plateforme a été livré avant qu'une charge utile ou un effet secondaire ultérieur échoue.
- `failed` : aucun reçu de plateforme n'a été produit.

Utilisez `payloadOutcomes` quand un lot mélange des charges utiles envoyées, supprimées et échouées.
N'inférez pas l'annulation de hook à partir d'un résultat de livraison directe hérité vide.

## Dispatch de Compatibilité

Le dispatch de réponse entrante doit être assemblé via
`dispatchChannelInboundReply(...)` à partir de `channel-inbound`. Gardez la livraison de plateforme dans l'adaptateur de livraison ; utilisez `channel-outbound` pour les adaptateurs de message, les envois durables, les reçus, l'aperçu en direct et les options de pipeline de réponse.
