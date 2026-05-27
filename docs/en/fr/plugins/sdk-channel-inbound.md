---
summary: "Assistants inbound pour les plugins de canal : construction de contexte, orchestration du runner partagé, enregistrement de session et dispatch de réponse préparée"
title: "API inbound de canal"
read_when:
  - Vous construisez ou refactorisez un chemin de réception de plugin de canal de messagerie
  - Vous avez besoin de construction de contexte inbound partagé, d'enregistrement de session ou de dispatch de réponse préparée
  - Vous migrez les anciens assistants de tour de canal vers les API inbound/message
---

Les plugins de canal doivent modéliser les chemins de réception avec les noms inbound et message :

```text
événement de plateforme -> faits/contexte inbound -> réponse d'agent -> livraison de message
```

Utilisez `openclaw/plugin-sdk/channel-inbound` pour la normalisation d'événement inbound,
le formatage, les racines et l'orchestration. Utilisez
`openclaw/plugin-sdk/channel-outbound` pour l'envoi natif,
la réception, la livraison durable et le comportement d'aperçu en direct.

## Assistants principaux

```ts
import {
  buildChannelInboundEventContext,
  runChannelInboundEvent,
  dispatchChannelInboundReply,
} from "openclaw/plugin-sdk/channel-inbound";
```

- `buildChannelInboundEventContext(...)` : projette les faits de canal normalisés dans
  le contexte de prompt/session.
- `runChannelInboundEvent(...)` : exécute l'ingestion, la classification, la vérification préalable, la résolution,
  l'enregistrement, le dispatch et la finalisation pour un événement de plateforme inbound.
- `dispatchChannelInboundReply(...)` : enregistre et dispatche une réponse inbound déjà assemblée
  avec un adaptateur de livraison.

Le runtime du plugin injecté expose les mêmes assistants de haut niveau sous
`runtime.channel.inbound.*` pour les canaux groupés/natifs qui reçoivent déjà l'objet
runtime.

```ts
await runtime.channel.inbound.run({
  channel: "demo",
  accountId,
  raw: platformEvent,
  adapter: {
    ingest: normalizePlatformEvent,
    resolveTurn: resolveInboundReply,
  },
});
```

Les dispatchers de compatibilité doivent assembler les entrées `dispatchChannelInboundReply(...)` 
et conserver la livraison de plateforme dans l'adaptateur de livraison. Les nouveaux chemins d'envoi doivent
préférer les adaptateurs de message et les assistants de message durable.

## Migration

Les anciens alias de runtime `runtime.channel.turn.*` ont été supprimés. Utilisez :

- `runtime.channel.inbound.run(...)` pour les événements inbound bruts.
- `runtime.channel.inbound.dispatchReply(...)` pour les contextes de réponse assemblés.
- `runtime.channel.inbound.buildContext(...)` pour les charges utiles de contexte inbound.
- `runtime.channel.inbound.runPreparedReply(...)` uniquement pour les chemins de dispatch préparés appartenant au canal qui assemblent déjà leur propre fermeture de dispatch.

Le nouveau code de plugin ne doit pas introduire d'API de canal nommées `turn`. Conservez le vocabulaire de tour de modèle ou
d'agent à l'intérieur du code d'agent/fournisseur ; les plugins de canal utilisent les termes inbound,
message, livraison et réponse.
