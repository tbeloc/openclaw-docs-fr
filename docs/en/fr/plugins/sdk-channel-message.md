---
summary: "API du cycle de vie des messages pour les plugins de canal, incluant les envois durables, les reçus, l'aperçu en direct, la politique d'accusé de réception et la migration héritée"
title: "API des messages de canal"
read_when:
  - You are building or refactoring a messaging channel plugin
  - You need durable final reply delivery, receipts, live preview finalization, or receive acknowledgement policy
  - You are migrating from legacy reply pipeline or inbound reply dispatch helpers
---

Les plugins de canal doivent exposer un adaptateur `message` depuis
`openclaw/plugin-sdk/channel-message`. L'adaptateur décrit le cycle de vie natif des messages
que la plateforme supporte :

```text
receive -> route and record -> agent turn -> durable final send
send -> render batch -> platform I/O -> receipt -> lifecycle side effects
live preview -> final edit or fallback -> receipt
```

Core gère la mise en file d'attente, la durabilité, la politique de nouvelle tentative générique, les hooks, les reçus et
l'outil `message` partagé. Le plugin gère les appels natifs d'envoi/édition/suppression, la
normalisation des cibles, le threading de la plateforme, les citations sélectionnées, les drapeaux de notification, l'état du compte
et les effets secondaires spécifiques à la plateforme.

Utilisez cette page avec [Building channel plugins](/fr/plugins/sdk-channel-plugins).

Le sous-chemin `channel-message` est intentionnellement peu coûteux pour les fichiers d'amorçage de plugins chauds
tels que `channel.ts` : il expose les contrats d'adaptateur, les preuves de capacité,
les reçus et les façades de compatibilité sans charger la livraison sortante.
Les assistants de livraison au moment de l'exécution sont disponibles depuis
`openclaw/plugin-sdk/channel-message-runtime` pour les chemins de surveillance/envoi qui
font déjà des E/S de messages asynchrones.

Le nouveau code de canal et d'envoi de plugin doit utiliser les assistants du cycle de vie des messages depuis
`openclaw/plugin-sdk/channel-message-runtime` : `sendDurableMessageBatch`,
`withDurableMessageSendContext` ou `deliverInboundReplyWithMessageSendContext`.
L'assistant plus ancien
`deliverOutboundPayloads(...)` dans `openclaw/plugin-sdk/outbound-runtime`
est un substrat de compatibilité/exécution déprécié pour les internes sortants, la récupération
et les adaptateurs hérités. Ne l'utilisez pas pour les nouveaux chemins d'envoi de canal ou de plugin.

`sendDurableMessageBatch(...)` retourne un résultat de cycle de vie explicite :

- `sent` - au moins un message de plateforme visible a été livré.
- `suppressed` - aucun message de plateforme ne doit être traité comme manquant. Les raisons stables
  incluent `cancelled_by_message_sending_hook`,
  `empty_after_message_sending_hook`, `no_visible_payload`,
  `adapter_returned_no_identity` et l'ancien `no_visible_result`.
- `partial_failed` - au moins un message de plateforme a été livré avant qu'une charge utile ou un effet secondaire ultérieur échoue. Le résultat inclut le préfixe de reçu livré
  plus l'échec.
- `failed` - aucun reçu de plateforme n'a été produit.

Utilisez `payloadOutcomes` quand un lot mélange des charges utiles envoyées, supprimées et échouées.
N'inférez pas l'annulation du hook en vérifiant si l'ancien tableau de livraison directe
est vide.

Les dispatchers de compatibilité qui ont encore besoin du dispatcher de réponse en mémoire tampon doivent
construire les options de préfixe de réponse avec `createChannelMessageReplyPipeline(...)` depuis
`openclaw/plugin-sdk/channel-message`, puis appeler `channel.turn.runPrepared(...)` du runtime. Cela maintient
l'enregistrement de session et l'ordre de dispatch sur le cycle de vie du tour partagé sans ajouter un autre wrapper de tour public.

## Adaptateur minimal

La plupart des nouveaux plugins de canal peuvent commencer avec un petit adaptateur :

```typescript
import {
  defineChannelMessageAdapter,
  createMessageReceiptFromOutboundResults,
} from "openclaw/plugin-sdk/channel-message";

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

Attachez-le ensuite au plugin de canal :

```typescript
export const demoPlugin = createChatChannelPlugin({
  base: {
    id: "demo",
    message: demoMessageAdapter,
    // other channel plugin fields
  },
});
```

Déclarez uniquement les capacités que l'adaptateur préserve vraiment. Chaque capacité déclarée
doit avoir un test de contrat.

## Pont sortant

Si le canal a déjà un adaptateur `outbound` compatible, préférez dériver l'adaptateur
de message au lieu de dupliquer le code d'envoi :

```typescript
import { createChannelMessageAdapterFromOutbound } from "openclaw/plugin-sdk/channel-message";

const demoMessageAdapter = createChannelMessageAdapterFromOutbound({
  id: "demo",
  outbound: demoOutboundAdapter,
});
```

Le pont convertit les anciens résultats d'envoi sortant en valeurs `MessageReceipt`. Le nouveau
code doit passer les reçus de bout en bout et dériver uniquement les identifiants hérités aux bords de compatibilité avec `listMessageReceiptPlatformIds(...)` ou
`resolveMessageReceiptPrimaryId(...)`.
Si aucune politique de réception n'est fournie, `createChannelMessageAdapterFromOutbound(...)`
utilise la politique d'accusé de réception `manual`. Cela rend l'accusé de réception de plateforme appartenant au plugin explicite
sans modifier les canaux qui accusent réception des webhooks,
des sockets ou des décalages de polling en dehors du contexte de réception générique.

## Envois d'outils de message

Le chemin partagé `message(action="send")` doit utiliser le même cycle de vie de livraison principal que les réponses finales. Si un canal a besoin de mise en forme spécifique au fournisseur pour l'envoi de l'outil, implémentez `actions.prepareSendPayload(...)` au lieu d'envoyer depuis
`actions.handleAction(...)`.

`prepareSendPayload(...)` reçoit la `ReplyPayload` principale normalisée plus le
contexte d'action complet. Retournez une charge utile avec des données spécifiques au canal dans
`payload.channelData.<channel>` et laissez core appeler `sendMessage(...)`,
le runtime du cycle de vie des messages, la file d'attente d'écriture anticipée, les hooks d'envoi de messages,
la nouvelle tentative, la récupération et le nettoyage d'ack. Le runtime du cycle de vie peut appeler
`deliverOutboundPayloads(...)` en interne comme substrat de compatibilité, mais les plugins de canal
ne doivent pas l'appeler directement pour le nouveau comportement d'envoi.

Retournez `null` uniquement quand l'envoi ne peut pas être représenté comme une charge utile durable, par
exemple parce qu'il contient une fabrique de composants non sérialisable. Core conservera
le fallback d'action de plugin hérité pour la compatibilité, mais les nouvelles fonctionnalités d'envoi de canal
doivent être exprimables comme données de charge utile durable.

```typescript
export const demoActions: ChannelMessageActionAdapter = {
  describeMessageTool: () => ({ actions: ["send"], capabilities: ["presentation"] }),
  prepareSendPayload: ({ ctx, payload }) => {
    if (ctx.action !== "send") {
      return null;
    }
    return {
      ...payload,
      channelData: {
        ...payload.channelData,
        demo: {
          ...(payload.channelData?.demo as object | undefined),
          nativeCard: ctx.params.card,
        },
      },
    };
  },
};
```

L'adaptateur sortant lit ensuite `payload.channelData.demo` à l'intérieur de `sendPayload`.
Cela maintient le rendu spécifique à la plateforme dans le plugin tandis que core possède toujours
la persistance, la nouvelle tentative, la récupération, les hooks et l'ack.

Les charges utiles `message(action="send")` préparées et la livraison générique de réponse finale utilisent
la livraison principale avec mise en file d'attente au mieux par défaut. La mise en file d'attente durable requise
n'est valide qu'après que core vérifie que le canal peut réconcilier un envoi dont le résultat est
inconnu après un crash. Si l'adaptateur ne peut pas implémenter `reconcileUnknownSend`,
conservez le chemin d'envoi préparé au mieux ; core essaiera toujours la file d'attente d'écriture anticipée,
mais la persistance de la file d'attente ou la récupération de crash incertaine ne fait pas partie du
contrat de livraison requis.

## Capacités finales durables

La livraison finale durable est optionnelle par effet secondaire. Core n'utilisera la livraison durable générique
que lorsque l'adaptateur déclare chaque capacité nécessaire par la charge utile et les options de livraison.

| Capacité               | Déclarer quand                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------ |
| `text`                 | L'adaptateur peut envoyer du texte et retourner un reçu.                             |
| `media`                | Les envois de médias retournent des reçus pour chaque message de plateforme visible. |
| `payload`              | L'adaptateur préserve la sémantique de charge utile de réponse riche, pas seulement le texte et une URL de média. |
| `replyTo`              | Les cibles de réponse natives atteignent la plateforme.                              |
| `thread`               | Les cibles de thread, de sujet ou de thread de canal natifs atteignent la plateforme. |
| `silent`               | La suppression de notification atteint la plateforme.                                |
| `nativeQuote`          | Les métadonnées de citation sélectionnées atteignent la plateforme.                  |
| `messageSendingHooks`  | Les hooks d'envoi de messages principaux peuvent annuler ou réécrire le contenu avant les E/S de plateforme. |
| `batch`                | Les lots rendus multi-parties sont rejouables comme un plan durable.                 |
| `reconcileUnknownSend` | L'adaptateur peut résoudre la récupération `unknown_after_send` sans relecture aveugle. |
| `afterSendSuccess`     | Les effets secondaires locaux du canal après envoi s'exécutent une fois.             |
| `afterCommit`          | Les effets secondaires locaux du canal après commit s'exécutent une fois.            |

La livraison finale au mieux n'exige pas `reconcileUnknownSend` ; elle utilise le cycle de vie partagé
quand l'adaptateur préserve la sémantique visible de la charge utile, et revient aux E/S de plateforme directes
si la persistance de la file d'attente n'est pas disponible. La livraison finale durable requise doit explicitement
exiger `reconcileUnknownSend`. Si l'adaptateur ne peut pas déterminer si un envoi commencé/inconnu a atteint
la plateforme, ne déclarez pas cette capacité ; core rejettera la livraison durable requise
avant la mise en file d'attente.

Quand un appelant a besoin d'une livraison durable, dérivez les exigences au lieu de construire
des cartes à la main :

```typescript
import { deriveDurableFinalDeliveryRequirements } from "openclaw/plugin-sdk/channel-message";

const requiredCapabilities = deriveDurableFinalDeliveryRequirements({
  payload,
  replyToId,
  threadId,
  silent,
  payloadTransport: true,
  extraCapabilities: {
    nativeQuote: hasSelectedQuote(payload),
  },
});
```

`messageSendingHooks` est requis par défaut. Définissez `messageSendingHooks: false`
uniquement pour un chemin qui ne peut intentionnellement pas exécuter les hooks d'envoi de messages globaux.

## Contrat d'envoi durable

Un envoi final durable a une sémantique plus stricte que la livraison héritée gérée par le canal :

- Créer l'intention durable avant les E/S de plateforme.
- Si la livraison durable retourne un résultat traité, ne pas revenir à l'envoi hérité.
- Traiter l'annulation de hook et les résultats sans envoi comme terminaux.
- Traiter `unsupported` comme un résultat pré-intention uniquement.
- Pour la durabilité requise, échouer avant les E/S de plateforme si la file d'attente ne peut pas enregistrer que l'envoi de plateforme a commencé.
- Pour la livraison finale requise et les envois d'outils de message préparés requis, faire un précontrôle `reconcileUnknownSend` ; la récupération doit pouvoir accuser réception d'un message déjà envoyé ou rejouer uniquement après que l'adaptateur prouve que l'envoi original n'a pas eu lieu.
- Pour `best_effort`, les échecs d'écriture en file d'attente peuvent revenir aux E/S de plateforme directes.
- Transférer les signaux d'abandon au chargement des médias et aux envois de plateforme.
- Exécuter les hooks après validation après l'accusé de réception en file d'attente ; le repli direct best-effort les exécute après les E/S de plateforme réussies car il n'y a pas de validation de file d'attente durable.
- Retourner les reçus pour chaque ID de message de plateforme visible.
- Utiliser `reconcileUnknownSend` quand une plateforme peut vérifier si un envoi incertain a déjà atteint l'utilisateur.

Ce contrat évite les envois en double après les plantages et évite de contourner les hooks d'annulation d'envoi de messages.

## Reçus

`MessageReceipt` est le nouvel enregistrement interne de ce que la plateforme a accepté :

```typescript
type MessageReceipt = {
  primaryPlatformMessageId?: string;
  platformMessageIds: string[];
  parts: MessageReceiptPart[];
  threadId?: string;
  replyToId?: string;
  editToken?: string;
  deleteToken?: string;
  sentAt: number;
  raw?: readonly MessageReceiptSourceResult[];
};
```

Utiliser `createMessageReceiptFromOutboundResults(...)` lors de l'adaptation d'un résultat d'envoi existant. Utiliser `createPreviewMessageReceipt(...)` quand un message d'aperçu en direct devient le reçu final. Éviter d'ajouter de nouveaux champs `messageIds` locaux au propriétaire. Le `ChannelDeliveryResult.messageIds` hérité est toujours produit aux limites de compatibilité.

## Aperçu en direct

Les canaux qui diffusent des aperçus de brouillon ou des mises à jour de progression doivent déclarer les capacités en direct :

```typescript
const demoMessageAdapter = defineChannelMessageAdapter({
  id: "demo",
  live: {
    capabilities: {
      draftPreview: true,
      previewFinalization: true,
      progressUpdates: true,
      quietFinalization: true,
    },
    finalizer: {
      capabilities: {
        finalEdit: true,
        normalFallback: true,
        discardPending: true,
        previewReceipt: true,
        retainOnAmbiguousFailure: true,
      },
    },
  },
});
```

Utiliser `defineFinalizableLivePreviewAdapter(...)` et `deliverWithFinalizableLivePreviewAdapter(...)` pour la finalisation à l'exécution. Le finaliseur décide si la réponse finale modifie l'aperçu sur place, envoie un repli normal, abandonne l'état d'aperçu en attente, conserve une modification échouée ambiguë sans dupliquer le message, et retourne le reçu final.

## Politique d'accusé de réception de réception

Les récepteurs entrants qui contrôlent le timing d'accusé de réception de plateforme doivent déclarer la politique de réception :

```typescript
const demoMessageAdapter = defineChannelMessageAdapter({
  id: "demo",
  receive: {
    defaultAckPolicy: "after_agent_dispatch",
    supportedAckPolicies: ["after_receive_record", "after_agent_dispatch"],
  },
});
```

Les adaptateurs qui ne déclarent pas de politique de réception utilisent par défaut :

```typescript
{
  receive: {
    defaultAckPolicy: "manual",
    supportedAckPolicies: ["manual"],
  },
}
```

Utiliser la valeur par défaut quand la plateforme n'a pas d'accusé de réception à différer, reconnaît déjà avant le traitement asynchrone, ou a besoin de sémantique de réponse spécifique au protocole. Déclarer l'une des politiques par étapes uniquement quand le récepteur utilise réellement le contexte de réception pour différer l'accusé de réception de plateforme.

Politiques :

| Politique              | Utiliser quand                                                                                                    |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `after_receive_record` | La plateforme peut être reconnue après que l'événement entrant soit analysé et enregistré.                        |
| `after_agent_dispatch` | La plateforme doit attendre que la distribution de l'agent soit acceptée.                                         |
| `after_durable_send`   | La plateforme doit attendre que la livraison finale ait une décision durable.                                     |
| `manual`               | Le plugin possède l'accusé de réception car la sémantique de plateforme ne correspond pas à une étape générique.  |

Utiliser `createMessageReceiveContext(...)` dans les récepteurs qui différent l'état d'ack, et `shouldAckMessageAfterStage(...)` quand le récepteur doit tester si une étape a satisfait la politique configurée.

## Tests de contrat

Les déclarations de capacité font partie du contrat du plugin. Les soutenir avec des tests :

```typescript
import {
  verifyChannelMessageAdapterCapabilityProofs,
  verifyChannelMessageLiveCapabilityAdapterProofs,
  verifyChannelMessageLiveFinalizerProofs,
  verifyChannelMessageReceiveAckPolicyAdapterProofs,
} from "openclaw/plugin-sdk/channel-message";

it("backs declared message capabilities", async () => {
  await expect(
    verifyChannelMessageAdapterCapabilityProofs({
      adapterName: "demo",
      adapter: demoMessageAdapter,
      proofs: {
        text: async () => {
          const result = await demoMessageAdapter.send!.text!(textCtx);
          expect(result.receipt.platformMessageIds).toContain("msg-1");
        },
        replyTo: async () => {
          await demoMessageAdapter.send!.text!({ ...textCtx, replyToId: "parent-1" });
          expect(sendDemoMessage).toHaveBeenCalledWith(
            expect.objectContaining({
              replyToId: "parent-1",
            }),
          );
        },
        messageSendingHooks: () => {
          expect(demoMessageAdapter.durableFinal!.capabilities!.messageSendingHooks).toBe(true);
        },
      },
    }),
  ).resolves.toContainEqual({ capability: "text", status: "verified" });
});
```

Ajouter les suites de preuves en direct et de réception quand l'adaptateur déclare ces fonctionnalités. Une preuve manquante doit faire échouer le test plutôt que d'élargir silencieusement la surface durable.

## API de compatibilité dépréciées

Ces API restent importables pour la compatibilité tierce. Ne pas les utiliser pour le nouveau code de canal.

| API dépréciée                                | Remplacement                                                                                                       |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `openclaw/plugin-sdk/channel-reply-pipeline` | `openclaw/plugin-sdk/channel-message`                                                                              |
| `createChannelTurnReplyPipeline(...)`        | `createChannelMessageReplyPipeline(...)` pour les distributeurs de compatibilité, ou un adaptateur `message` pour le nouveau code de canal |
| `buildChannelMessageReplyDispatchBase(...)`  | `createChannelMessageReplyPipeline(...)` plus `channel.turn.runPrepared(...)`, ou un adaptateur `message` pour le nouveau code de canal |
| `dispatchChannelMessageReplyWithBase(...)`   | `createChannelMessageReplyPipeline(...)` plus `channel.turn.runPrepared(...)`, ou un adaptateur `message` pour le nouveau code de canal |
| `recordChannelMessageReplyDispatch(...)`     | `createChannelMessageReplyPipeline(...)` plus `channel.turn.runPrepared(...)`, ou un adaptateur `message` pour le nouveau code de canal |
| `deliverOutboundPayloads(...)`               | `sendDurableMessageBatch(...)` ou `deliverInboundReplyWithMessageSendContext(...)` de `channel-message-runtime`    |
| `deliverDurableInboundReplyPayload(...)`     | `deliverInboundReplyWithMessageSendContext(...)` de `openclaw/plugin-sdk/channel-message-runtime`                  |
| `dispatchInboundReplyWithBase(...)`          | `createChannelMessageReplyPipeline(...)` plus `channel.turn.runPrepared(...)`, ou un adaptateur `message` pour le nouveau code de canal |
| `recordInboundSessionAndDispatchReply(...)`  | `createChannelMessageReplyPipeline(...)` plus `channel.turn.runPrepared(...)`, ou un adaptateur `message` pour le nouveau code de canal |
| `resolveChannelSourceReplyDeliveryMode(...)` | `resolveChannelMessageSourceReplyDeliveryMode(...)`                                                                |
| `deliverFinalizableDraftPreview(...)`        | `defineFinalizableLivePreviewAdapter(...)` plus `deliverWithFinalizableLivePreviewAdapter(...)`                    |
| `DraftPreviewFinalizerDraft`                 | `LivePreviewFinalizerDraft`                                                                                        |
| `DraftPreviewFinalizerResult`                | `LivePreviewFinalizerResult`                                                                                       |

Les distributeurs de compatibilité peuvent toujours utiliser `createReplyPrefixContext(...)`, `createReplyPrefixOptions(...)`, et `createTypingCallbacks(...)` via la façade de message. Le nouveau code de cycle de vie doit éviter l'ancien chemin d'accès `channel-reply-pipeline`.

## Liste de contrôle de migration

1. Ajouter `message: defineChannelMessageAdapter(...)` ou `message: createChannelMessageAdapterFromOutbound(...)` au plugin de canal.
2. Retourner `MessageReceipt` des envois de texte, de médias et de charge utile.
3. Déclarer uniquement les capacités soutenues par le comportement natif et les tests.
4. Remplacer les cartes de exigences durables écrites à la main par `deriveDurableFinalDeliveryRequirements(...)`.
5. Déplacer la finalisation d'aperçu via les assistants d'aperçu en direct quand le canal modifie les messages de brouillon sur place.
6. Déclarer la politique d'accusé de réception de réception uniquement quand le récepteur peut vraiment différer l'accusé de réception de plateforme.
7. Conserver les assistants de distribution de réponse hérités uniquement aux limites de compatibilité.
