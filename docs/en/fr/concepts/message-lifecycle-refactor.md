---
summary: "Plan de conception pour le cycle de vie unifié de réception, d'envoi, d'aperçu, de modification et de diffusion en continu des messages durables"
read_when:
  - Refactoring channel send or receive behavior
  - Changing channel turn, reply dispatch, outbound queue, preview streaming, or plugin SDK message APIs
  - Designing a new channel plugin that needs durable sends, receipts, previews, edits, or retries
title: "Message lifecycle refactor"
---

Cette page est la conception cible pour remplacer les helpers dispersés de tour de canal, de dispatch de réponse, de diffusion en continu d'aperçu et de livraison sortante par un cycle de vie de message durable unifié.

La version courte :

- Les primitives principales doivent être **receive** et **send**, pas **reply**.
- Une réponse n'est qu'une relation sur un message sortant.
- Un tour est une commodité de traitement entrant, pas le propriétaire de la livraison.
- L'envoi doit être basé sur le contexte : `begin`, render, preview ou stream, envoi final, commit, fail.
- La réception doit aussi être basée sur le contexte : normaliser, dédupliquer, router, enregistrer, dispatcher, ack de plateforme, fail.
- Le SDK de plugin public devrait se réduire à une petite surface de message de canal.

## Problèmes

La pile de canal actuelle a grandi à partir de plusieurs besoins locaux valides :

- Les adaptateurs entrants simples utilisent `runtime.channel.turn.run`.
- Les adaptateurs riches utilisent `runtime.channel.turn.runPrepared`.
- Les helpers hérités utilisent `dispatchInboundReplyWithBase`, `recordInboundSessionAndDispatchReply`, les helpers de charge utile de réponse, le chunking de réponse, les références de réponse et les helpers de runtime sortant.
- La diffusion en continu d'aperçu vit dans les dispatchers spécifiques au canal.
- La durabilité de la livraison finale est ajoutée autour des chemins de charge utile de réponse existants.

Cette forme corrige les bugs locaux, mais elle laisse OpenClaw avec trop de concepts publics et trop d'endroits où la sémantique de livraison peut dériver.

Le problème de fiabilité qui a exposé ceci est :

```text
Telegram polling update acked
  -> assistant final text exists
  -> process restarts before sendMessage succeeds
  -> final response is lost
```

L'invariant cible est plus large que Telegram : une fois que le cœur décide qu'un message sortant visible devrait exister, l'intention doit être durable avant que l'envoi de plateforme ne soit tenté, et la réception de plateforme doit être validée après le succès. Cela donne à OpenClaw une récupération au moins une fois. Le comportement exactement une fois n'existe que pour les adaptateurs qui peuvent prouver l'idempotence native ou réconcilier une tentative inconnue après envoi par rapport à l'état de la plateforme avant la relecture.

C'est l'état final de cette refonte, pas une description de chaque chemin actuel. Pendant la migration, les helpers sortants existants peuvent toujours tomber sur un envoi direct lorsque les écritures de file d'attente durables échouent au mieux. La refonte est complète uniquement lorsque les envois finaux durables échouent fermés ou optent explicitement pour une politique non durable documentée.

## Objectifs

- Un cycle de vie principal pour tous les chemins de réception et d'envoi de messages de canal.
- Envois finaux durables par défaut dans le nouveau cycle de vie des messages après qu'un adaptateur déclare un comportement sûr pour la relecture.
- Sémantique partagée d'aperçu, de modification, de flux, de finalisation, de nouvelle tentative, de récupération et de réception.
- Une petite surface SDK de plugin que les plugins tiers peuvent apprendre et maintenir.
- Compatibilité pour les appelants `channel.turn` existants pendant la migration.
- Points d'extension clairs pour les nouvelles capacités de canal.
- Aucune branche spécifique à la plateforme dans le cœur.
- Aucun message de canal delta de jeton. La diffusion en continu de canal reste l'aperçu de message, la modification, l'ajout ou la livraison de bloc complété.
- Métadonnées d'origine OpenClaw structurées pour la sortie opérationnelle/système afin que les défaillances de passerelle visibles ne réentrent pas dans les salles partagées activées par bot en tant que nouvelles invites.

## Non-objectifs

- Ne pas supprimer `runtime.channel.turn.*` dans la première phase.
- Ne pas forcer chaque canal dans le même comportement de transport natif.
- Ne pas enseigner au cœur les sujets Telegram, les flux natifs Slack, les rédactions Matrix, les cartes Feishu, la voix QQ ou les activités Teams.
- Ne pas publier tous les helpers de migration interne en tant qu'API SDK stable.
- Ne pas relire les opérations de plateforme complétées non-idempotentes.

## Modèle de référence

Vercel Chat a un bon modèle mental public :

- `Chat`
- `Thread`
- `Channel`
- `Message`
- méthodes d'adaptateur telles que `postMessage`, `editMessage`, `deleteMessage`, `stream`, `startTyping` et les récupérations d'historique
- un adaptateur d'état pour la dédupe, les verrous, les files d'attente et la persistance

OpenClaw devrait emprunter le vocabulaire, pas copier la surface.

Ce qu'OpenClaw a besoin au-delà de ce modèle :

- Intentions d'envoi sortant durable avant les appels de transport direct.
- Contextes d'envoi explicites avec begin, commit et fail.
- Contextes de réception qui connaissent la politique d'ack de plateforme.
- Reçus qui survivent au redémarrage et peuvent conduire les modifications, les suppressions, la récupération et la suppression des doublons.
- Un SDK public plus petit. Les plugins groupés peuvent utiliser les helpers de runtime interne, mais les plugins tiers devraient voir une API de message cohérente.
- Comportement spécifique à l'agent : sessions, transcriptions, diffusion en continu de bloc, progression des outils, approbations, directives médias, réponses silencieuses et historique de mention de groupe.

Les promesses de style `thread.post()` ne suffisent pas pour OpenClaw. Elles cachent la limite de transaction qui décide si un envoi est récupérable.

## Modèle principal

Le nouveau domaine devrait vivre sous un espace de noms principal interne tel que `src/channels/message/*`.

Il a quatre concepts :

```typescript
core.messages.receive(...)
core.messages.send(...)
core.messages.live(...)
core.messages.state(...)
```

`receive` possède le cycle de vie entrant.

`send` possède le cycle de vie sortant.

`live` possède l'aperçu, la modification, la progression et l'état du flux.

`state` possède le stockage d'intention durable, les reçus, l'idempotence, la récupération, les verrous et la dédupe.

## Termes de message

### Message

Un message normalisé est neutre par rapport à la plateforme :

```typescript
type ChannelMessage = {
  id: string;
  channel: string;
  accountId?: string;
  direction: "inbound" | "outbound";
  target: MessageTarget;
  sender?: MessageActor;
  body?: MessageBody;
  attachments?: MessageAttachment[];
  relation?: MessageRelation;
  origin?: MessageOrigin;
  timestamp?: number;
  raw?: unknown;
};
```

### Target

La cible décrit où le message vit :

```typescript
type MessageTarget = {
  kind: "direct" | "group" | "channel" | "thread";
  id: string;
  label?: string;
  spaceId?: string;
  parentId?: string;
  threadId?: string;
  nativeChannelId?: string;
};
```

### Relation

La réponse est une relation, pas une racine API :

```typescript
type MessageRelation =
  | {
      kind: "reply";
      inboundMessageId?: string;
      replyToId?: string;
      threadId?: string;
      quote?: MessageQuote;
    }
  | {
      kind: "followup";
      sessionKey?: string;
      previousMessageId?: string;
    }
  | {
      kind: "broadcast";
      reason?: string;
    }
  | {
      kind: "system";
      reason:
        | "approval"
        | "task"
        | "hook"
        | "cron"
        | "subagent"
        | "message_tool"
        | "cli"
        | "control_ui"
        | "automation"
        | "error";
    };
```

Cela permet au même chemin d'envoi de gérer les réponses normales, les notifications cron, les invites d'approbation, les complétions de tâches, les envois d'outils de message, les envois CLI ou Control UI, les résultats de sous-agent et les envois d'automatisation.

### Origin

L'origine décrit qui a produit un message et comment OpenClaw devrait traiter les échos de ce message. C'est séparé de la relation : un message peut être une réponse à un utilisateur et être toujours une sortie opérationnelle d'origine OpenClaw.

```typescript
type MessageOrigin =
  | {
      source: "openclaw";
      schemaVersion: 1;
      kind: "gateway_failure";
      code: "agent_failed_before_reply" | "missing_api_key" | "model_login_expired";
      echoPolicy: "drop_bot_room_echo";
    }
  | {
      source: "user" | "external_bot" | "platform" | "unknown";
    };
```

Le cœur possède le sens de la sortie d'origine OpenClaw. Les canaux possèdent comment cette origine est codée dans leur transport.

Le premier usage requis est la sortie d'échec de passerelle. Les humains devraient toujours voir des messages tels que « Agent failed before reply » ou « Missing API key », mais la sortie opérationnelle OpenClaw balisée ne doit pas être acceptée comme entrée créée par bot dans les salles partagées lorsque `allowBots` est activé.

### Receipt

Les reçus sont de première classe :

```typescript
type MessageReceipt = {
  primaryPlatformMessageId?: string;
  platformMessageIds: string[];
  parts: MessageReceiptPart[];
  threadId?: string;
  replyToId?: string;
  editToken?: string;
  deleteToken?: string;
  url?: string;
  sentAt: number;
  raw?: unknown;
};

type MessageReceiptPart = {
  platformMessageId: string;
  kind: "text" | "media" | "voice" | "card" | "preview" | "unknown";
  index: number;
  threadId?: string;
  replyToId?: string;
  editToken?: string;
  deleteToken?: string;
  url?: string;
  raw?: unknown;
};
```

Les reçus sont le pont entre l'intention durable et la modification future, la suppression, la finalisation d'aperçu, la suppression des doublons et la récupération.

Un reçu peut décrire un message de plateforme ou une livraison multi-parties. Le texte fragmenté, le média plus texte, la voix plus texte et les replis de carte doivent préserver tous les identifiants de plateforme tout en exposant un identifiant principal pour le threading et les modifications ultérieures.

## Recevoir le contexte

La réception ne doit pas être un simple appel d'aide. Le noyau a besoin d'un contexte qui connaît
la déduplication, le routage, l'enregistrement de session et la politique d'accusé de réception de la plateforme.

```typescript
type MessageReceiveContext = {
  id: string;
  channel: string;
  accountId?: string;
  input: ChannelMessage;
  ack: ReceiveAckController;
  route: MessageRouteController;
  session: MessageSessionController;
  log: MessageLifecycleLogger;

  dedupe(): Promise<ReceiveDedupeResult>;
  resolve(): Promise<ResolvedInboundMessage>;
  record(resolved: ResolvedInboundMessage): Promise<RecordResult>;
  dispatch(recorded: RecordResult): Promise<DispatchResult>;
  commit(result: DispatchResult): Promise<void>;
  fail(error: unknown): Promise<void>;
};
```

Flux de réception :

```text
événement de plateforme
  -> début du contexte de réception
  -> normalisation
  -> classification
  -> déduplication et porte d'auto-écho
  -> routage et autorisation
  -> enregistrement des métadonnées de session entrante
  -> dispatch de l'exécution de l'agent
  -> les envois sortants durables se font via le contexte d'envoi
  -> commit de la réception
  -> accusé de réception de la plateforme quand la politique le permet
```

L'accusé de réception n'est pas une seule chose. Le contrat de réception doit garder ces signaux séparés :

- **Accusé de réception du transport :** indique à la plateforme webhook ou socket qu'OpenClaw a accepté
  l'enveloppe d'événement. Certaines plateformes l'exigent avant le dispatch.
- **Accusé de réception du décalage d'interrogation :** avance un curseur pour que le même événement ne soit pas récupéré
  à nouveau. Cela ne doit pas avancer au-delà du travail qui ne peut pas être récupéré.
- **Accusé de réception du dossier entrant :** confirme qu'OpenClaw a persisté suffisamment de métadonnées entrantes pour
  dédupliquer et router une rélivraison.
- **Reçu visible par l'utilisateur :** comportement optionnel de lecture/statut/saisie ; jamais une
  limite de durabilité.

`ReceiveAckPolicy` contrôle uniquement l'accusé de réception du transport ou de l'interrogation. Il ne doit
pas être réutilisé pour les reçus de lecture ou les réactions de statut.

Avant l'autorisation du bot, la réception doit appliquer la politique d'écho OpenClaw partagée
quand le canal peut décoder les métadonnées d'origine du message :

```typescript
function shouldDropOpenClawEcho(params: {
  origin?: MessageOrigin;
  isBotAuthor: boolean;
  isRoomish: boolean;
}): boolean {
  return (
    params.isBotAuthor &&
    params.isRoomish &&
    params.origin?.source === "openclaw" &&
    params.origin.kind === "gateway_failure" &&
    params.origin.echoPolicy === "drop_bot_room_echo"
  );
}
```

Cette suppression est basée sur les balises, pas sur le texte. Un message de salle créé par un bot avec
le même texte d'échec de passerelle visible mais sans métadonnées d'origine OpenClaw
passe par l'autorisation `allowBots` normale.

La politique d'accusé de réception est explicite :

```typescript
type ReceiveAckPolicy =
  | { kind: "immediate"; reason: "webhook-timeout" | "platform-contract" }
  | { kind: "after-record" }
  | { kind: "after-durable-send" }
  | { kind: "manual" };
```

L'interrogation Telegram utilise maintenant la politique d'accusé de réception du contexte de réception pour son repère de redémarrage persistant. Le suivi observe toujours les mises à jour grammY à mesure qu'elles entrent dans la chaîne de middleware, mais OpenClaw persiste uniquement l'ID de mise à jour complétée sûre après un dispatch réussi, laissant les mises à jour échouées ou inférieures en attente rejouables après un redémarrage. Le décalage de récupération `getUpdates` en amont de Telegram est toujours contrôlé par la bibliothèque d'interrogation, donc la coupure plus profonde restante est une source d'interrogation entièrement durable si nous avons besoin d'une rélivraison au niveau de la plateforme au-delà du repère de redémarrage d'OpenClaw. Les plateformes webhook peuvent avoir besoin d'un accusé de réception HTTP immédiat, mais elles ont toujours besoin de déduplication entrante et d'intentions d'envoi sortant durable car les webhooks peuvent rélivrer.

## Contexte d'envoi

L'envoi est également basé sur le contexte :

```typescript
type MessageSendContext = {
  id: string;
  channel: string;
  accountId?: string;
  message: ChannelMessage;
  intent: DurableSendIntent;
  attempt: number;
  signal: AbortSignal;
  previousReceipt?: MessageReceipt;
  preview?: LiveMessageState;
  log: MessageLifecycleLogger;

  render(): Promise<RenderedMessageBatch>;
  previewUpdate(rendered: RenderedMessageBatch): Promise<LiveMessageState>;
  send(rendered: RenderedMessageBatch): Promise<MessageReceipt>;
  edit(receipt: MessageReceipt, rendered: RenderedMessageBatch): Promise<MessageReceipt>;
  delete(receipt: MessageReceipt): Promise<void>;
  commit(receipt: MessageReceipt): Promise<void>;
  fail(error: unknown): Promise<void>;
};
```

Orchestration préférée :

```typescript
await core.messages.withSendContext(message, async (ctx) => {
  const rendered = await ctx.render();

  if (ctx.preview?.canFinalizeInPlace) {
    return await ctx.edit(ctx.preview.receipt, rendered);
  }

  return await ctx.send(rendered);
});
```

L'aide se développe en :

```text
début de l'intention durable
  -> rendu
  -> travail optionnel d'aperçu/édition/flux
  -> marquer l'envoi
  -> envoi de plateforme final ou édition finale
  -> marquer le commit avec le reçu brut
  -> commit du reçu
  -> accusé de réception de l'intention durable
  -> échec de l'intention durable en cas d'échec classifié
```

L'intention doit exister avant les E/S de transport. Un redémarrage après le début mais avant
le commit est récupérable.

La limite dangereuse est après le succès de la plateforme et avant le commit du reçu. Si un
processus meurt là, OpenClaw ne peut pas savoir si le message de plateforme existe
à moins que l'adaptateur ne fournisse l'idempotence native ou un chemin de réconciliation de reçu.
Ces tentatives doivent reprendre dans `unknown_after_send`, pas rejouer aveuglément. Les canaux
sans réconciliation peuvent choisir une relecture au moins une fois uniquement si les messages visibles en double
sont un compromis acceptable et documenté pour ce canal et cette relation.
Le pont de réconciliation SDK actuel exige que l'adaptateur déclare
`reconcileUnknownSend`, puis demande à `durableFinal.reconcileUnknownSend` de
classifier une entrée inconnue comme `sent`, `not_sent`, ou `unresolved` ; seul `not_sent`
permet la relecture, et les entrées non résolues restent terminales ou ne réessaient que la
vérification de réconciliation.

La politique de durabilité doit être explicite :

```typescript
type MessageDurabilityPolicy = "required" | "best_effort" | "disabled";
```

`required` signifie que le noyau doit échouer fermé quand il ne peut pas écrire l'intention durable.
`best_effort` peut passer quand la persistance n'est pas disponible. `disabled` conserve
l'ancien comportement d'envoi direct. Pendant la migration, les wrappers hérités et les aides de compatibilité publique par défaut à `disabled` ; ils ne doivent pas déduire `required` du
fait qu'un canal a un adaptateur sortant générique.

Les contextes d'envoi possèdent également les effets post-envoi locaux au canal. Une migration n'est pas sûre
si la livraison durable contourne le comportement local qui était précédemment attaché au
chemin d'envoi direct du canal. Les exemples incluent les caches de suppression d'auto-écho,
les marqueurs de participation aux threads, les ancres d'édition natives, le rendu de signature de modèle,
et les gardes de duplication spécifiques à la plateforme. Ces effets doivent soit se déplacer dans l'adaptateur
d'envoi, l'adaptateur de rendu, ou un hook de contexte d'envoi nommé avant que ce
canal puisse activer la livraison générique finale durable.

Les aides d'envoi doivent retourner les reçus jusqu'à leur appelant. Les wrappers durables
ne peuvent pas avaler les ID de message ou remplacer un résultat de livraison de canal par
`undefined` ; les dispatchers mis en mémoire tampon utilisent ces ID pour les ancres de thread, les éditions ultérieures,
la finalisation d'aperçu et la suppression de duplication.

Les envois de secours opèrent sur des lots, pas sur des charges utiles uniques. Les réécritures de réponse silencieuse,
le secours média, le secours de carte et la projection de chunk peuvent tous produire plus d'un
message livrable, donc un contexte d'envoi doit soit livrer le lot projeté entier soit
documenter explicitement pourquoi une seule charge utile est valide.

```typescript
type RenderedMessageBatch = {
  units: RenderedMessageUnit[];
  atomicity: "all_or_retry_remaining" | "best_effort_parts";
  idempotencyKey: string;
};

type RenderedMessageUnit = {
  index: number;
  kind: "text" | "media" | "voice" | "card" | "preview" | "unknown";
  payload: unknown;
  required: boolean;
};
```

Quand un tel secours est durable, le lot projeté entier doit être représenté par
une intention d'envoi durable ou un autre plan de lot atomique. Enregistrer chaque charge utile
une par une n'est pas suffisant : un crash entre les charges utiles peut laisser un secours visible partiel
sans dossier durable pour les charges utiles restantes. La récupération doit savoir
quelles unités ont déjà des reçus et soit rejouer uniquement les unités manquantes soit marquer
le lot `unknown_after_send` jusqu'à ce que l'adaptateur le réconcilie.

## Contexte en direct

Le comportement d'aperçu, d'édition, de progression et de flux doit être un cycle de vie opt-in.

```typescript
type MessageLiveAdapter = {
  begin?(ctx: MessageSendContext): Promise<LiveMessageState>;
  update?(
    ctx: MessageSendContext,
    state: LiveMessageState,
    update: LiveMessageUpdate,
  ): Promise<LiveMessageState>;
  finalize?(
    ctx: MessageSendContext,
    state: LiveMessageState,
    final: RenderedMessageBatch,
  ): Promise<MessageReceipt>;
  cancel?(
    ctx: MessageSendContext,
    state: LiveMessageState,
    reason: LiveCancelReason,
  ): Promise<void>;
};
```

L'état en direct est suffisamment durable pour récupérer ou supprimer les doublons :

```typescript
type LiveMessageState = {
  mode: "partial" | "block" | "progress" | "native";
  receipt?: MessageReceipt;
  visibleSince?: number;
  canFinalizeInPlace: boolean;
  lastRenderedHash?: string;
  staleAfterMs?: number;
};
```

Cela devrait couvrir le comportement actuel :

- Envoi Telegram plus aperçu d'édition, avec final frais après l'âge d'aperçu obsolète.
- Envoi Discord plus aperçu d'édition, annulation sur média/erreur/réponse explicite.
- Flux natif Slack ou aperçu de brouillon selon la forme du thread.
- Finalisation du brouillon de publication Mattermost.
- Finalisation d'événement de brouillon Matrix ou rédaction en cas de non-concordance.
- Flux de progression natif Teams.
- Flux QQ Bot ou secours accumulé.

## Adapter surface

La cible du SDK public devrait être un seul sous-chemin :

```typescript
import { defineChannelMessageAdapter } from "openclaw/plugin-sdk/channel-message";
```

Forme cible :

```typescript
type ChannelMessageAdapter = {
  receive?: MessageReceiveAdapter;
  send: MessageSendAdapter;
  live?: MessageLiveAdapter;
  origin?: MessageOriginAdapter;
  render?: MessageRenderAdapter;
  capabilities: MessageCapabilities;
};
```

Adaptateur d'envoi :

```typescript
type MessageSendAdapter = {
  send(ctx: MessageSendContext, rendered: RenderedMessageBatch): Promise<MessageReceipt>;
  edit?(
    ctx: MessageSendContext,
    receipt: MessageReceipt,
    rendered: RenderedMessageBatch,
  ): Promise<MessageReceipt>;
  delete?(ctx: MessageSendContext, receipt: MessageReceipt): Promise<void>;
  classifyError?(ctx: MessageSendContext, error: unknown): DeliveryFailureKind;
  reconcileUnknownSend?(ctx: MessageSendContext): Promise<MessageReceipt | null>;
  afterSendSuccess?(ctx: MessageSendContext, receipt: MessageReceipt): Promise<void>;
  afterCommit?(ctx: MessageSendContext, receipt: MessageReceipt): Promise<void>;
};
```

Adaptateur de réception :

```typescript
type MessageReceiveAdapter<TRaw = unknown> = {
  normalize(raw: TRaw, ctx: MessageNormalizeContext): Promise<ChannelMessage>;
  classify?(message: ChannelMessage): Promise<MessageEventClass>;
  preflight?(message: ChannelMessage, event: MessageEventClass): Promise<MessagePreflightResult>;
  ackPolicy?(message: ChannelMessage, event: MessageEventClass): ReceiveAckPolicy;
};
```

Avant l'autorisation de préflight, le noyau doit exécuter le prédicat d'écho OpenClaw partagé
chaque fois que `origin.decode` retourne des métadonnées d'origine OpenClaw. L'adaptateur de réception
fournit des faits de plateforme tels que l'auteur du bot et la forme de la salle ; le noyau possède la décision
de suppression et l'ordre afin que les canaux ne réimplémentent pas les filtres de texte.

Adaptateur d'origine :

```typescript
type MessageOriginAdapter<TRaw = unknown, TNative = unknown> = {
  encode?(origin: MessageOrigin): TNative | undefined;
  decode?(raw: TRaw): MessageOrigin | undefined;
};
```

Le noyau définit `MessageOrigin`. Les canaux ne font que le traduire vers et depuis les métadonnées
de transport natif. Slack le mappe à `chat.postMessage({ metadata })` et
aux `message.metadata` entrants ; Matrix peut le mapper à du contenu d'événement supplémentaire ; les canaux
sans métadonnées natives peuvent utiliser un registre de reçus/sortants lorsque c'est la
meilleure approximation disponible.

Capacités :

```typescript
type MessageCapabilities = {
  text: { maxLength?: number; chunking?: boolean };
  attachments?: {
    upload: boolean;
    remoteUrl: boolean;
    voice?: boolean;
  };
  threads?: {
    reply: boolean;
    topic?: boolean;
    nativeThread?: boolean;
  };
  live?: {
    edit: boolean;
    delete: boolean;
    nativeStream?: boolean;
    progress?: boolean;
  };
  delivery?: {
    idempotencyKey?: boolean;
    retryAfter?: boolean;
    receiptRequired?: boolean;
  };
};
```

## Réduction du SDK public

La nouvelle surface publique devrait absorber ou déprécier ces domaines conceptuels :

- `reply-runtime`
- `reply-dispatch-runtime`
- `reply-reference`
- `reply-chunking`
- `reply-payload`
- `inbound-reply-dispatch`
- `channel-reply-pipeline`
- la plupart des utilisations publiques de `outbound-runtime`
- les aides du cycle de vie du flux de brouillon ad hoc

Les sous-chemins de compatibilité peuvent rester comme des wrappers, mais les nouveaux plugins tiers
ne devraient pas en avoir besoin.

Les plugins groupés peuvent conserver les importations d'aides internes via des sous-chemins d'exécution réservés
pendant la migration. La documentation publique devrait orienter les auteurs de plugins vers
`plugin-sdk/channel-message` une fois qu'il existe.

## Relation avec le tour de canal

`runtime.channel.turn.*` devrait rester pendant la migration.

Il devrait devenir un adaptateur de compatibilité :

```text
channel.turn.run
  -> messages.receive context
  -> session dispatch
  -> messages.send context for visible output
```

`channel.turn.runPrepared` devrait également rester initialement :

```text
channel-owned dispatcher
  -> messages.receive record/finalize bridge
  -> messages.live for preview/progress
  -> messages.send for final delivery
```

Une fois que tous les plugins groupés et les chemins de compatibilité tiers connus sont bridgés,
`channel.turn` peut être déprécié. Il ne devrait pas être supprimé jusqu'à ce qu'il y ait un
chemin de migration SDK publié et des tests de contrat prouvant que les anciens plugins fonctionnent toujours
ou échouent avec une erreur de version claire.

## Garde-fous de compatibilité

Pendant la migration, la livraison durable générique est opt-in pour tout canal dont
le rappel de livraison existant a des effets secondaires au-delà de « envoyer cette charge utile ».

Les points d'entrée hérités ne sont pas durables par défaut :

- `channel.turn.run` et `dispatchAssembledChannelTurn` utilisent le rappel de livraison du canal sauf si
  ce canal fournit explicitement un objet de politique/options durable audité.
- `channel.turn.runPrepared` reste propriété du canal jusqu'à ce que le répartiteur préparé
  appelle explicitement le contexte d'envoi.
- Les aides de compatibilité publiques telles que `recordInboundSessionAndDispatchReply`,
  `dispatchInboundReplyWithBase`, et les aides de DM directs n'injectent jamais de livraison durable générique
  avant le rappel `deliver` ou `reply` fourni par l'appelant.

Pour les types de pont de migration, `durable: undefined` signifie « non durable ». Le
chemin durable est activé uniquement par une valeur de politique/options explicite. `durable:
false` peut rester comme une orthographe de compatibilité, mais l'implémentation ne devrait pas
exiger que chaque canal non migré l'ajoute.

Le code du pont actuel doit garder la décision de durabilité explicite :

- La livraison finale durable retourne un statut discriminé. `handled_visible` et
  `handled_no_send` sont terminaux ; `unsupported` et `not_applicable` peuvent revenir à
  la livraison propriété du canal ; `failed` propage l'échec d'envoi.
- La livraison finale durable générique est contrôlée par les capacités de l'adaptateur telles que
  la livraison silencieuse, la préservation de la cible de réponse, la préservation de la citation native, et
  les crochets d'envoi de messages. L'absence de parité devrait choisir la livraison propriété du canal,
  pas un envoi générique qui change le comportement visible par l'utilisateur.
- Les envois durables soutenus par une file d'attente exposent une référence d'intention de livraison. Les champs
  de session `pendingFinalDelivery*` existants peuvent porter l'id d'intention pendant la
  transition ; l'état final est un magasin `MessageSendIntent` au lieu du texte de réponse gelé
  plus les champs de contexte ad hoc.

N'activez pas le chemin durable générique pour un canal que si tous ces éléments sont
vrais :

- L'adaptateur d'envoi générique exécute le même rendu et le même comportement de transport que
  le chemin direct ancien.
- Les effets secondaires post-envoi locaux sont préservés via le contexte d'envoi.
- L'adaptateur retourne des reçus ou des résultats de livraison avec tous les identifiants de messages de plateforme.
- Les chemins du répartiteur préparé appellent soit le nouveau contexte d'envoi, soit restent documentés
  comme en dehors de la garantie durable.
- La livraison de secours gère chaque charge utile projetée, pas seulement la première.
- La livraison durable de secours enregistre le tableau de charge utile projeté entier comme une
  intention ou un plan de lot rejouable.

Aléas de migration concrets à préserver :

- La livraison du moniteur iMessage enregistre les messages envoyés dans un cache d'écho après un
  envoi réussi. Les envois finaux durables doivent toujours remplir ce cache, sinon
  OpenClaw peut réingérer ses propres réponses finales comme des messages utilisateur entrants.
- Tlon ajoute une signature de modèle optionnelle et enregistre les threads auxquels il a participé
  après les réponses de groupe. La livraison durable générique ne doit pas contourner ces effets ;
  soit les déplacer dans les adaptateurs de rendu/envoi/finalisation de Tlon, soit garder Tlon sur le
  chemin propriété du canal.
- Discord et d'autres répartiteurs préparés possèdent déjà la livraison directe et le comportement d'aperçu.
  Ils ne sont pas couverts par une garantie durable de tour assemblé jusqu'à ce que
  leurs répartiteurs préparés acheminent explicitement les finales via le contexte d'envoi.
- La livraison de secours silencieuse de Telegram doit livrer le tableau de charge utile projeté complet.
  Un raccourci de charge utile unique peut supprimer les charges utiles de secours supplémentaires après
  la projection.
- LINE, Zalo, Nostr, et d'autres chemins assemblés/aides existants peuvent
  avoir la gestion des jetons de réponse, le proxying des médias, les caches de messages envoyés, le nettoyage du chargement/statut,
  ou les cibles de rappel uniquement. Ils restent sur la livraison propriété du canal jusqu'à ce que
  ces sémantiques soient représentées par l'adaptateur d'envoi et vérifiées par les tests.
- Les aides de DM directs peuvent avoir un rappel de réponse qui est la seule cible de transport correcte.
  La sortie générique ne doit pas deviner à partir de `OriginatingTo` ou `To` et ignorer
  ce rappel.
- La sortie d'échec de la passerelle OpenClaw doit rester visible aux humains, mais les échos de salle
  marqués comme créés par bot doivent être supprimés avant l'autorisation `allowBots`.
  Les canaux ne doivent pas implémenter cela avec des filtres de préfixe de texte visible sauf comme
  un court arrêt d'urgence ; le contrat durable est des métadonnées d'origine structurées.

## Stockage interne

La file d'attente durable devrait stocker les intentions d'envoi de messages, pas les charges utiles de réponse.

```typescript
type DurableSendIntent = {
  id: string;
  idempotencyKey: string;
  channel: string;
  accountId?: string;
  message: ChannelMessage;
  batch?: RenderedMessageBatch;
  liveState?: LiveMessageState;
  status:
    | "pending"
    | "sending"
    | "committing"
    | "unknown_after_send"
    | "sent"
    | "failed"
    | "cancelled";
  attempt: number;
  nextAttemptAt?: number;
  receipt?: MessageReceipt;
  partialReceipt?: MessageReceipt;
  failure?: DeliveryFailure;
  createdAt: number;
  updatedAt: number;
};
```

Boucle de récupération :

```text
load pending or sending intents
  -> acquire idempotency lock
  -> skip if receipt already committed
  -> reconstruct send context
  -> render if needed
  -> reconcile unknown_after_send if needed
  -> call adapter send/edit/finalize
  -> commit receipt, mark unknown_after_send, or schedule retry
```

La file d'attente devrait conserver suffisamment d'identité pour rejouer via le même compte,
le même fil, la même cible, la même politique de formatage, et les mêmes règles de médias après redémarrage.

## Classes d'échec

Les adaptateurs de canal classent les échecs de transport en catégories fermées :

```typescript
type DeliveryFailureKind =
  | "transient"
  | "rate_limit"
  | "auth"
  | "permission"
  | "not_found"
  | "invalid_payload"
  | "conflict"
  | "cancelled"
  | "unknown";
```

Politique du noyau :

- Réessayer `transient` et `rate_limit`.
- Ne pas réessayer `invalid_payload` sauf si un repli de rendu existe.
- Ne pas réessayer `auth` ou `permission` jusqu'à ce que la configuration change.
- Pour `not_found`, laisser la finalisation en direct revenir de l'édition à un envoi frais lorsque
  le canal déclare que c'est sûr.
- Pour `conflict`, utiliser les règles de reçu/idempotence pour décider si le message
  existe déjà.
- Toute erreur après que l'adaptateur peut avoir complété les E/S de plateforme mais avant la validation du reçu
  devient `unknown_after_send` sauf si l'adaptateur peut prouver que l'opération de plateforme n'a pas eu lieu.

## Mappage des canaux

| Canal           | Migration cible                                                                                                                                                                                                                                                                                                                                                |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Telegram        | Recevoir la politique d'accusé de réception plus les envois finaux durables. L'adaptateur en direct possède l'envoi plus l'aperçu de modification, l'envoi final d'aperçu obsolète, les sujets, l'omission d'aperçu de citation-réponse, le secours médias et la gestion du délai de nouvelle tentative.                                                                                                                                                                   |
| Discord         | L'adaptateur d'envoi encapsule la livraison de charge utile durable existante. L'adaptateur en direct possède la modification du brouillon, le brouillon de progression, l'annulation d'aperçu média/erreur, la préservation de la cible de réponse et les reçus d'ID de message. Auditer les échos d'échec de passerelle créés par bot dans les salons partagés ; utiliser un registre sortant ou un équivalent natif équivalent si Discord ne peut pas transporter les métadonnées d'origine sur les messages normaux. |
| Slack           | L'adaptateur d'envoi gère les publications de chat normales. L'adaptateur en direct choisit le flux natif lorsque la forme du fil le supporte, sinon l'aperçu du brouillon. Les reçus préservent les horodatages des fils. L'adaptateur d'origine mappe les échecs de passerelle OpenClaw aux métadonnées `chat.postMessage.metadata` de Slack et supprime les échos de salle balisés par bot avant l'autorisation `allowBots`.                                  |
| WhatsApp        | L'adaptateur d'envoi possède l'envoi texte/média avec des intentions finales durables. L'adaptateur de réception gère la mention de groupe et l'identité de l'expéditeur. Le direct peut rester absent jusqu'à ce que WhatsApp ait un transport modifiable.                                                                                                                                                                        |
| Matrix          | L'adaptateur en direct possède les modifications d'événement de brouillon, la finalisation, la suppression, les contraintes de média chiffré et le secours de non-correspondance de cible de réponse. L'adaptateur de réception possède l'hydratation d'événement chiffré et la déduplication. L'adaptateur d'origine doit encoder l'origine d'échec de passerelle OpenClaw dans le contenu d'événement Matrix et supprimer les échos de salle de bot configurés avant la gestion `allowBots`.              |
| Mattermost      | L'adaptateur en direct possède un brouillon de publication, le pliage de progression/outil, la finalisation en place et le secours d'envoi frais.                                                                                                                                                                                                                                                       |
| Microsoft Teams | L'adaptateur en direct possède le comportement de flux de bloc et de progression natif. L'adaptateur d'envoi possède les activités et les reçus de pièce jointe/carte.                                                                                                                                                                                                                                        |
| Feishu          | L'adaptateur de rendu possède le rendu texte/carte/brut. L'adaptateur en direct possède les cartes en continu et la suppression finale en double. L'adaptateur d'envoi possède les commentaires, les sessions de sujet, les médias et la suppression vocale.                                                                                                                                                                      |
| QQ Bot          | L'adaptateur en direct possède la diffusion en continu C2C, le délai d'expiration de l'accumulateur et l'envoi final de secours. L'adaptateur de rendu possède les balises média et le texte en tant que voix.                                                                                                                                                                                                                                               |
| Signal          | Adaptateur de réception et d'envoi simple. Pas d'adaptateur en direct sauf si signal-cli ajoute un support de modification fiable.                                                                                                                                                                                                                                                                |
| iMessage        | Adaptateur de réception et d'envoi simple. L'envoi iMessage doit préserver le remplissage du cache d'écho du moniteur avant que les finales durables puissent contourner la livraison du moniteur.                                                                                                                                                                                                                 |
| Google Chat     | Adaptateur de réception et d'envoi simple avec relation de fil mappée aux espaces et aux ID de fil. Auditer le comportement de salle `allowBots=true` pour les échos d'échec de passerelle OpenClaw balisés.                                                                                                                                                                                        |
| LINE            | Adaptateur de réception et d'envoi simple avec contraintes de jeton de réponse modélisées comme capacité cible/relation.                                                                                                                                                                                                                                                           |
| Nextcloud Talk  | Pont de réception SDK plus adaptateur d'envoi.                                                                                                                                                                                                                                                                                                                          |
| IRC             | Adaptateur de réception et d'envoi simple, pas de reçus de modification durable.                                                                                                                                                                                                                                                                                                    |
| Nostr           | Adaptateur de réception et d'envoi pour les messages directs chiffrés ; les reçus sont des ID d'événement.                                                                                                                                                                                                                                                                                           |
| Canal QA        | Adaptateur de test de contrat pour le comportement de réception, d'envoi, en direct, de nouvelle tentative et de récupération.                                                                                                                                                                                                                                                                                   |
| Synology Chat   | Adaptateur de réception et d'envoi simple.                                                                                                                                                                                                                                                                                                              |
| Tlon            | L'adaptateur d'envoi doit préserver le rendu de signature de modèle et le suivi de fil participé avant que la livraison finale durable générique soit activée.                                                                                                                                                                                                                        |
| Twitch          | Adaptateur de réception et d'envoi simple avec classification de limite de débit.                                                                                                                                                                                                                                                                                                                              |
| Zalo            | Adaptateur de réception et d'envoi simple.                                                                                                                                                                                                                                                                                                              |
| Zalo Personnel  | Adaptateur de réception et d'envoi simple.                                                                                                                                                                                                                                                                                              |

## Plan de migration

### Phase 1 : Domaine de message interne

- Ajouter les types `src/channels/message/*` pour les messages, les cibles, les relations,
  les origines, les reçus, les capacités, les intentions durables, le contexte de réception,
  le contexte d'envoi, le contexte en direct et les classes d'échec.
- Ajouter `origin?: MessageOrigin` au type de charge utile du pont de migration utilisé par
  la livraison de réponse actuelle, puis déplacer ce champ vers `ChannelMessage` et les
  types de message rendus à mesure que la refonte remplace les charges utiles de réponse.
- Garder ceci en interne jusqu'à ce que les adaptateurs et les tests prouvent la forme.
- Ajouter des tests unitaires purs pour les transitions d'état et la sérialisation.

### Phase 2 : Noyau d'envoi durable

- Déplacer la file d'attente sortante existante de la durabilité de la charge utile de réponse
  vers les intentions d'envoi de message durable.
- Laisser une intention d'envoi durable porter un tableau de charge utile projeté ou un plan
  de lot, pas seulement une charge utile de réponse.
- Préserver le comportement actuel de récupération de file d'attente par conversion de compatibilité.
- Faire en sorte que `deliverOutboundPayloads` appelle `messages.send`.
- Faire de la durabilité d'envoi final la valeur par défaut et échouer fermé lorsque l'intention
  durable ne peut pas être écrite dans le nouveau cycle de vie du message, après que l'adaptateur
  déclare la sécurité de relecture. Les chemins de compatibilité du tour de canal et du SDK
  existants restent en envoi direct par défaut pendant cette phase.
- Enregistrer les reçus de manière cohérente.
- Retourner les reçus et les résultats de livraison à l'appelant du répartiteur d'origine au lieu
  de traiter l'envoi durable comme un effet secondaire terminal.
- Persister l'origine du message par le biais des intentions d'envoi de message durable afin que
  la récupération, la relecture et les envois fragmentés préservent la provenance opérationnelle
  d'OpenClaw.

### Phase 3 : Pont de tour de canal

- Réimplémenter `channel.turn.run` et `dispatchAssembledChannelTurn` au-dessus de
  `messages.receive` et `messages.send`.
- Garder les types de faits actuels stables.
- Garder le comportement hérité par défaut. Un tour de canal assemblé devient durable
  uniquement lorsque son adaptateur s'inscrit explicitement avec une politique de durabilité
  sûre pour la relecture.
- Garder `durable: false` comme échappatoire de compatibilité pour les chemins qui finalisent
  les modifications natives et ne peuvent pas encore rejouer en toute sécurité, mais ne pas
  compter sur les marqueurs `false` pour protéger les canaux non migrés.
- Durabilité d'assemblage par défaut uniquement dans le nouveau cycle de vie du message, après
  que le mappage de canal prouve que le chemin d'envoi générique préserve la sémantique de
  livraison de canal ancienne.

### Phase 4 : Pont du répartiteur préparé

- Remplacer `deliverDurableInboundReplyPayload` par un pont de contexte d'envoi.
- Garder l'ancien assistant comme wrapper.
- Porter Telegram, WhatsApp, Slack, Signal, iMessage et Discord en premier car ils ont déjà
  un travail durable final ou des chemins d'envoi plus simples.
- Traiter chaque répartiteur préparé comme non couvert jusqu'à ce qu'il s'inscrive explicitement
  au contexte d'envoi. La documentation et les entrées du journal des modifications doivent dire
  « tours de canal assemblés » ou nommer les chemins de canal migrés plutôt que de prétendre
  que toutes les réponses finales automatiques.
- Garder le comportement de `recordInboundSessionAndDispatchReply`, les assistants DM directs
  et les assistants de compatibilité publique similaires préservant le comportement. Ils peuvent
  exposer un opt-in de contexte d'envoi explicite plus tard, mais ne doivent pas tenter
  automatiquement une livraison durable générique avant le rappel de livraison détenu par
  l'appelant.

### Phase 5 : Cycle de vie en direct unifié

- Construire `messages.live` avec deux adaptateurs de preuve :
  - Telegram pour l'envoi plus l'édition plus l'envoi final obsolète.
  - Matrix pour la finalisation de brouillon plus le repli de rédaction.
- Ensuite, migrer Discord, Slack, Mattermost, Teams, QQ Bot et Feishu.
- Supprimer le code de finalisation d'aperçu dupliqué uniquement après que chaque canal ait
  des tests de parité.

### Phase 6 : SDK public

- Ajouter `openclaw/plugin-sdk/channel-message`.
- Le documenter comme l'API de plugin de canal préférée.
- Mettre à jour les exportations de package, l'inventaire des points d'entrée, les lignes de
  base d'API générées et la documentation du SDK de plugin.
- Inclure `MessageOrigin`, les crochets d'encodage/décodage d'origine et le prédicat partagé
  `shouldDropOpenClawEcho` dans la surface du SDK de message de canal.
- Garder les wrappers de compatibilité pour les anciens sous-chemins.
- Marquer les assistants SDK nommés par réponse comme dépréciés dans la documentation après
  la migration des plugins fournis.

### Phase 7 : Tous les expéditeurs

Déplacer tous les producteurs sortants non-réponse vers `messages.send` :

- notifications cron et heartbeat
- complétions de tâche
- résultats de hook
- invites d'approbation et résultats d'approbation
- envois d'outil de message
- annonces de complétude de sous-agent
- envois CLI ou Control UI explicites
- chemins d'automatisation/diffusion

C'est là que le modèle cesse d'être « réponses d'agent » et devient « OpenClaw envoie
des messages ».

### Phase 8 : Déprécier le tour

- Garder `channel.turn` comme wrapper pour au moins une fenêtre de compatibilité.
- Publier les notes de migration.
- Exécuter les tests de compatibilité du SDK de plugin par rapport aux anciens imports.
- Supprimer ou masquer les anciens assistants internes uniquement après qu'aucun plugin fourni
  n'en ait besoin et que les contrats tiers aient un remplacement stable.

## Plan de test

Tests unitaires :

- Sérialisation et récupération d'intention d'envoi durable.
- Réutilisation de clé d'idempotence et suppression de doublon.
- Engagement de reçu et saut de relecture.
- Récupération `unknown_after_send` qui se réconcilie avant la relecture lorsqu'un adaptateur
  supporte la réconciliation.
- Politique de classification d'échec.
- Séquençage de politique d'ack de réception.
- Mappage de relation pour les envois de réponse, suivi, système et diffusion.
- Usine d'origine d'échec de passerelle et prédicat `shouldDropOpenClawEcho`.
- Préservation d'origine par le biais de la normalisation de charge utile, du fragmentage,
  de la sérialisation de file d'attente durable et de la récupération.

Tests d'intégration :

- `channel.turn.run` l'adaptateur simple enregistre et envoie toujours.
- La livraison d'événement assemblé hérité ne devient pas durable à moins que le canal
  s'inscrive explicitement.
- `channel.turn.runPrepared` le pont enregistre et finalise toujours.
- Les assistants de compatibilité publique appellent les rappels de livraison détenus par
  l'appelant par défaut et ne font pas d'envoi générique avant ces rappels.
- La livraison de repli durable rejoue le tableau de charge utile projeté entier après
  redémarrage et ne peut pas laisser les charges utiles ultérieures non enregistrées après
  un crash précoce.
- La livraison d'événement assemblé durable retourne les identifiants de message de plateforme
  au répartiteur mis en mémoire tampon.
- Les crochets de livraison personnalisés retournent toujours les identifiants de message de
  plateforme lorsque la livraison durable est désactivée ou indisponible.
- La réponse finale survit au redémarrage entre la complétude de l'assistant et l'envoi de
  plateforme.
- Le brouillon d'aperçu se finalise sur place lorsqu'il est autorisé.
- Le brouillon d'aperçu est annulé ou rédacté lorsqu'une incompatibilité média/erreur/cible
  de réponse nécessite une livraison normale.
- Le streaming de bloc et le streaming d'aperçu ne livrent pas tous les deux le même texte.
- Le média diffusé en continu tôt n'est pas dupliqué dans la livraison finale.

Tests de canal :

- Réponse de sujet Telegram avec ack d'interrogation retardé jusqu'au repère de filigrane
  complété en toute sécurité du contexte de réception.
- Récupération d'interrogation Telegram pour les mises à jour acceptées mais non livrées
  couvertes par le modèle de décalage complété en toute sécurité persisté.
- L'aperçu obsolète Telegram envoie un final frais et nettoie l'aperçu.
- Le repli silencieux Telegram envoie chaque charge utile de repli projetée.
- La durabilité du repli silencieux Telegram enregistre le tableau de repli projeté complet
  de manière atomique, pas une intention durable à charge utile unique par itération de boucle.
- Annulation d'aperçu Discord sur média/erreur/réponse explicite.
- Les finales du répartiteur préparé Discord acheminent par le biais du contexte d'envoi avant
  que les documents ou le journal des modifications ne revendiquent la durabilité de réponse
  finale Discord.
- Les envois finaux durables iMessage remplissent le cache d'écho de message envoyé du moniteur.
- Les chemins de livraison hérités LINE, Zalo et Nostr ne sont pas contournés par l'envoi
  durable générique jusqu'à ce que leurs tests de parité d'adaptateur existent.
- La livraison de rappel DM direct/Nostr reste autoritaire sauf si elle est explicitement
  migrée vers une cible de message complète et un adaptateur d'envoi sûr pour la relecture.
- Les messages d'échec de passerelle OpenClaw Slack balisés restent visibles sortants, les
  échos de salle de bot balisés se déposent avant `allowBots`, et les messages de bot non
  balisés avec le même texte visible suivent toujours l'autorisation de bot normale.
- Repli de flux natif Slack vers aperçu de brouillon dans les DM de niveau supérieur.
- Finalisation d'aperçu Matrix et repli de rédaction.
- Les échos de salle d'échec de passerelle OpenClaw balisés Matrix à partir de comptes de bot
  configurés se déposent avant la gestion de `allowBots`.
- Les cascades d'échec de passerelle Discord et Google Chat de salle partagée auditent les
  modes `allowBots` avant de revendiquer une protection générique là.
- Finalisation de brouillon Mattermost et repli d'envoi frais.
- Finalisation de progrès natif Teams.
- Suppression finale en double Feishu.
- Repli de délai d'expiration d'accumulateur QQ Bot.
- Les envois finaux durables Tlon préservent le rendu de signature de modèle et le suivi de
  thread participé.
- WhatsApp, Signal, iMessage, Google Chat, LINE, IRC, Nostr, Nextcloud Talk, Synology Chat,
  Tlon, Twitch, Zalo et envois finaux durables simples Zalo Personal.

Validation :

- Fichiers Vitest ciblés pendant le développement.
- `pnpm check:changed` dans Testbox pour la surface complète modifiée.
- `pnpm check` plus large dans Testbox avant d'atterrir la refonte complète ou après les
  modifications d'exportation/SDK publiques.
- Fumée en direct ou qa-channel pour au moins un canal capable d'édition et un canal
  d'envoi simple uniquement avant de supprimer les wrappers de compatibilité.

## Questions ouvertes

- Si Telegram devrait éventuellement remplacer la source du runner grammY par une source
  d'interrogation entièrement durable qui peut contrôler la relivraison au niveau de la
  plateforme, pas seulement le repère de redémarrage persisté d'OpenClaw.
- Si l'état d'aperçu en direct durable doit être stocké dans le même enregistrement de file
  d'attente que l'intention d'envoi final ou dans un magasin d'état en direct frère.
- Combien de temps les wrappers de compatibilité restent documentés après l'expédition de
  `plugin-sdk/channel-message`.
- Si les plugins tiers doivent implémenter les adaptateurs de réception directement ou
  uniquement fournir les crochets de normalisation/envoi/en direct par le biais de
  `defineChannelMessageAdapter`.
- Quels champs de reçu sont sûrs à exposer dans le SDK public par rapport à l'état d'exécution
  interne.
- Si les effets secondaires tels que les caches d'auto-écho et les marqueurs de thread participé
  doivent être modélisés comme des crochets de contexte d'envoi, des étapes de finalisation
  détenues par l'adaptateur ou des abonnés de reçu.
- Quels canaux ont des métadonnées d'origine natives, lesquels ont besoin de registres sortants
  persistés et lesquels ne peuvent pas offrir une suppression d'écho inter-bot fiable.

## Critères d'acceptation

- Chaque canal de message fourni envoie la sortie visible finale par le biais de
  `messages.send`.
- Chaque canal de message entrant entre par le biais de `messages.receive` ou d'un wrapper
  de compatibilité documenté.
- Chaque canal d'aperçu/édition/flux utilise `messages.live` pour l'état de brouillon et
  la finalisation.
- `channel.turn` n'est qu'un wrapper.
- Les assistants SDK nommés par réponse sont des exportations de compatibilité, pas le chemin
  recommandé.
- La récupération durable peut rejouer les envois finaux en attente après redémarrage sans
  perdre la réponse finale ou dupliquer les envois déjà validés ; les envois dont le résultat
  de plateforme est inconnu sont réconciliés avant la relecture ou documentés comme au moins
  une fois pour cet adaptateur.
- Les envois finaux durables échouent fermés lorsque l'intention durable ne peut pas être
  écrite, sauf si un appelant a explicitement sélectionné un mode non durable documenté.
- Les assistants de compatibilité du tour de canal hérité et du SDK par défaut à la livraison
  détenue par le canal direct ; l'envoi durable générique est uniquement un opt-in explicite.
- Les reçus préservent tous les identifiants de message de plateforme pour les livraisons
  multi-parties et un identifiant principal pour la commodité de threading/édition.
- Les wrappers durables préservent les effets secondaires locaux du canal avant de remplacer
  les rappels de livraison directs.
- Les répartiteurs préparés ne sont pas comptés comme durables jusqu'à ce que leur chemin de
  livraison final utilise explicitement le contexte d'envoi.
- La livraison de repli gère chaque charge utile projetée.
- La livraison de repli durable enregistre chaque charge utile projetée dans une intention ou
  un plan de lot rejouable.
- La sortie d'échec de passerelle originaire d'OpenClaw est visible pour les humains mais les
  échos de salle balisés bot-authored sont déposés avant l'autorisation de bot sur les canaux
  qui déclarent le support du contrat d'origine.
- La documentation explique l'envoi, la réception, le direct, l'état, les reçus, les relations,
  la politique d'échec, la migration et la couverture de test.

## Connexes

- [Messages](/fr/concepts/messages)
- [Streaming et fragmentage](/fr/concepts/streaming)
- [Brouillons de progrès](/fr/concepts/progress-drafts)
- [Politique de relance](/fr/concepts/retry)
- [Noyau du tour de canal](/fr/plugins/sdk-channel-turn)
