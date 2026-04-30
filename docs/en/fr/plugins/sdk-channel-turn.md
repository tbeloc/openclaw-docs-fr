---
summary: "runtime.channel.turn -- le noyau de tour entrant partagé que les plugins de canal groupés et tiers utilisent pour enregistrer, dispatcher et finaliser les tours d'agent"
title: "Noyau de tour de canal"
sidebarTitle: "Tour de canal"
read_when:
  - You are building a channel plugin and want the shared inbound turn lifecycle
  - You are migrating a channel monitor off hand-rolled record/dispatch glue
  - You need to understand admission, ingest, classify, preflight, resolve, record, dispatch, and finalize stages
---

Le noyau de tour de canal est la machine d'état entrante partagée qui transforme un événement de plateforme normalisé en un tour d'agent. Les plugins de canal fournissent les faits de plateforme et le rappel de livraison. Le noyau possède l'orchestration : ingestion, classification, préflight, résolution, autorisation, assemblage, enregistrement, dispatch et finalisation.

Utilisez ceci quand votre plugin est sur le chemin chaud des messages entrants. Pour les événements non-message (commandes slash, modales, interactions de bouton, événements de cycle de vie, réactions, état vocal), gardez-les locaux au plugin. Le noyau ne possède que les événements qui peuvent devenir un tour de texte d'agent.

<Info>
  Le noyau est atteint via le runtime du plugin injecté en tant que `runtime.channel.turn.*`. Le type de runtime du plugin est exporté depuis `openclaw/plugin-sdk/core`, donc les plugins natifs tiers peuvent utiliser ces points d'entrée de la même manière que les plugins de canal groupés.
</Info>

## Pourquoi un noyau partagé

Les plugins de canal répètent le même flux entrant : normaliser, router, gater, construire un contexte, enregistrer les métadonnées de session, dispatcher le tour d'agent, finaliser l'état de livraison. Sans un noyau partagé, une modification du gating des mentions, des réponses visibles uniquement pour les outils, des métadonnées de session, de l'historique en attente ou de la finalisation du dispatch doit être appliquée par canal.

Le noyau garde quatre concepts délibérément séparés :

- `ConversationFacts` : d'où provient le message
- `RouteFacts` : quel agent et quelle session doivent le traiter
- `ReplyPlanFacts` : où les réponses visibles doivent aller
- `MessageFacts` : quel corps et quel contexte supplémentaire l'agent doit voir

Les DM Slack, les sujets Telegram, les threads Matrix et les sessions de sujets Feishu font tous cette distinction en pratique. Les traiter comme un seul identifiant cause une dérive au fil du temps.

## Cycle de vie des étapes

Le noyau exécute le même pipeline fixe quel que soit le canal :

1. `ingest` -- l'adaptateur convertit un événement de plateforme brut en `NormalizedTurnInput`
2. `classify` -- l'adaptateur déclare si cet événement peut démarrer un tour d'agent
3. `preflight` -- l'adaptateur fait la déduplication, l'auto-écho, l'hydratation, le débounce, le déchiffrement, le pré-remplissage partiel des faits
4. `resolve` -- l'adaptateur retourne un tour complètement assemblé (route, plan de réponse, message, livraison)
5. `authorize` -- la politique DM, groupe, mention et commande appliquée aux faits assemblés
6. `assemble` -- `FinalizedMsgContext` construit à partir des faits via `buildContext`
7. `record` -- les métadonnées de session entrante et la dernière route sont persistées
8. `dispatch` -- le tour d'agent exécuté via le dispatcher de bloc en buffer
9. `finalize` -- l'adaptateur `onFinalize` s'exécute même en cas d'erreur de dispatch

Chaque étape émet un événement de journal structuré quand un rappel `log` est fourni. Voir [Observabilité](#observability).

## Types d'admission

Le noyau ne lève pas d'exception quand un tour est gaté. Il retourne une `ChannelTurnAdmission` :

| Type          | Quand                                                                                                                                         |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `dispatch`    | Le tour est admis. Le tour d'agent s'exécute et le chemin de réponse visible est exercé.                                                                   |
| `observeOnly` | Le tour s'exécute de bout en bout mais l'adaptateur de livraison n'envoie rien de visible. Utilisé pour les agents observateurs de diffusion et autres flux multi-agents passifs. |
| `handled`     | Un événement de plateforme a été consommé localement (cycle de vie, réaction, bouton, modale). Le noyau saute le dispatch.                                           |
| `drop`        | Chemin de saut. Optionnellement `recordHistory: true` garde le message dans l'historique de groupe en attente pour qu'une future mention ait du contexte.                      |

L'admission peut provenir de `classify` (la classe d'événement a dit qu'elle ne peut pas démarrer un tour), de `preflight` (déduplication, auto-écho, mention manquante avec enregistrement d'historique), ou de `resolveTurn` lui-même.

## Points d'entrée

Le runtime expose trois points d'entrée préférés pour que les adaptateurs puissent s'inscrire au niveau qui correspond au canal.

```typescript
runtime.channel.turn.run(...)             // adapter-driven full pipeline
runtime.channel.turn.runPrepared(...)     // channel owns dispatch; kernel runs record + finalize
runtime.channel.turn.buildContext(...)    // pure facts to FinalizedMsgContext mapping
```

Deux anciens helpers de runtime restent disponibles pour la compatibilité du Plugin SDK :

```typescript
runtime.channel.turn.runResolved(...)      // deprecated compatibility alias; prefer run
runtime.channel.turn.dispatchAssembled(...) // deprecated compatibility alias; prefer run or runPrepared
```

### run

Utilisez quand votre canal peut exprimer son flux entrant comme un `ChannelTurnAdapter<TRaw>`. L'adaptateur a des rappels pour `ingest`, `classify` optionnel, `preflight` optionnel, `resolveTurn` obligatoire, et `onFinalize` optionnel.

```typescript
await runtime.channel.turn.run({
  channel: "tlon",
  accountId,
  raw: platformEvent,
  adapter: {
    ingest(raw) {
      return {
        id: raw.messageId,
        timestamp: raw.timestamp,
        rawText: raw.body,
        textForAgent: raw.body,
      };
    },
    classify(input) {
      return { kind: "message", canStartAgentTurn: input.rawText.length > 0 };
    },
    async preflight(input, eventClass) {
      if (await isDuplicate(input.id)) {
        return { admission: { kind: "drop", reason: "dedupe" } };
      }
      return {};
    },
    resolveTurn(input) {
      return buildAssembledTurn(input);
    },
    onFinalize(result) {
      clearPendingGroupHistory(result);
    },
  },
});
```

`run` est la bonne forme quand le canal a une logique d'adaptateur petite et bénéficie de posséder le cycle de vie via des hooks.

### runPrepared

Utilisez quand le canal a un dispatcher local complexe avec des aperçus, des tentatives, des éditions ou un bootstrap de thread qui doit rester propriété du canal. Le noyau enregistre toujours la session entrante avant le dispatch et expose un `DispatchedChannelTurnResult` uniforme.

```typescript
const { dispatchResult } = await runtime.channel.turn.runPrepared({
  channel: "matrix",
  accountId,
  routeSessionKey,
  storePath,
  ctxPayload,
  recordInboundSession,
  record: {
    onRecordError,
    updateLastRoute,
  },
  onPreDispatchFailure: async (err) => {
    await stopStatusReactions();
  },
  runDispatch: async () => {
    return await runMatrixOwnedDispatcher();
  },
});
```

Les canaux riches (Matrix, Mattermost, Microsoft Teams, Feishu, QQ Bot) utilisent `runPrepared` car leur dispatcher orchestre le comportement spécifique à la plateforme que le noyau ne doit pas apprendre.

### buildContext

Une fonction pure qui mappe les bundles de faits en `FinalizedMsgContext`. Utilisez-la quand votre canal fait rouler à la main une partie du pipeline mais veut une forme de contexte cohérente.

```typescript
const ctxPayload = runtime.channel.turn.buildContext({
  channel: "googlechat",
  accountId,
  messageId,
  timestamp,
  from,
  sender,
  conversation,
  route,
  reply,
  message,
  access,
  media,
  supplemental,
});
```

`buildContext` est aussi utile à l'intérieur des rappels `resolveTurn` lors de l'assemblage d'un tour pour `run`.

<Note>
  Les helpers SDK dépréciés tels que `dispatchInboundReplyWithBase` font toujours un pont via un helper de tour assemblé. Le nouveau code de plugin doit utiliser `run` ou `runPrepared`.
</Note>

## Types de faits

Les faits que le noyau consomme de votre adaptateur sont indépendants de la plateforme. Traduisez les objets de plateforme dans ces formes avant de les transmettre au noyau.

### NormalizedTurnInput

| Champ             | Objectif                                                                      |
| ----------------- | ---------------------------------------------------------------------------- |
| `id`              | ID de message stable utilisé pour la déduplication et les journaux                                   |
| `timestamp`       | Epoch ms optionnel                                                            |
| `rawText`         | Corps tel que reçu de la plateforme                                                    |
| `textForAgent`    | Corps nettoyé optionnel pour l'agent (suppression de mention, suppression d'espace)             |
| `textForCommands` | Corps optionnel utilisé pour l'analyse `/command`                                    |
| `raw`             | Référence de transmission optionnelle pour les rappels d'adaptateur qui ont besoin de l'original |

### ChannelEventClass

| Champ                  | Objectif                                                                 |
| ---------------------- | ----------------------------------------------------------------------- |
| `kind`                 | `message`, `command`, `interaction`, `reaction`, `lifecycle`, `unknown` |
| `canStartAgentTurn`    | Si false, le noyau retourne `{ kind: "handled" }`                       |
| `requiresImmediateAck` | Indice pour les adaptateurs qui doivent ACK avant la distribution                      |

### SenderFacts

| Champ          | Objectif                                                        |
| -------------- | -------------------------------------------------------------- |
| `id`           | ID d'expéditeur stable de la plateforme                                      |
| `name`         | Nom d'affichage                                                   |
| `username`     | Identifiant s'il est distinct de `name`                                 |
| `tag`          | Discriminateur de style Discord ou tag de plateforme                   |
| `roles`        | ID de rôles, utilisés pour la correspondance de liste d'autorisation de rôle de membre              |
| `isBot`        | True quand l'expéditeur est un bot connu (le noyau l'utilise pour supprimer) |
| `isSelf`       | True quand l'expéditeur est l'agent configuré lui-même            |
| `displayLabel` | Étiquette pré-rendue pour le texte d'enveloppe                           |

### ConversationFacts

| Champ             | Objectif                                                              |
| ----------------- | -------------------------------------------------------------------- |
| `kind`            | `direct`, `group`, ou `channel`                                      |
| `id`              | ID de conversation utilisé pour le routage                                     |
| `label`           | Étiquette humaine pour l'enveloppe                                         |
| `spaceId`         | Identifiant d'espace extérieur optionnel (espace de travail Slack, serveur Matrix) |
| `parentId`        | ID de conversation extérieur quand ceci est un fil                          |
| `threadId`        | ID de fil quand ce message est à l'intérieur d'un fil                       |
| `nativeChannelId` | ID de canal natif de la plateforme quand différent de l'ID de routage        |
| `routePeer`       | Pair utilisé pour la recherche `resolveAgentRoute`                             |

### RouteFacts

| Champ                   | Objectif                                                    |
| ----------------------- | ---------------------------------------------------------- |
| `agentId`               | Agent qui devrait gérer ce tour                         |
| `accountId`             | Remplacement optionnel (canaux multi-comptes)                 |
| `routeSessionKey`       | Clé de session utilisée pour le routage                               |
| `dispatchSessionKey`    | Clé de session utilisée à la distribution quand différente de la clé de routage |
| `persistedSessionKey`   | Clé de session écrite dans les métadonnées de session persistées          |
| `parentSessionKey`      | Parent pour les sessions ramifiées/filées                      |
| `modelParentSessionKey` | Parent côté modèle pour les sessions ramifiées                    |
| `mainSessionKey`        | Épingle propriétaire DM principal pour les conversations directes                 |
| `createIfMissing`       | Autoriser l'étape d'enregistrement à créer une ligne de session manquante          |

### ReplyPlanFacts

| Champ                     | Objectif                                                 |
| ------------------------- | ------------------------------------------------------- |
| `to`                      | Cible de réponse logique écrite dans le contexte `To`          |
| `originatingTo`           | Cible de contexte d'origine (`OriginatingTo`)            |
| `nativeChannelId`         | ID de canal natif de la plateforme pour la livraison                 |
| `replyTarget`             | Destination de réponse visible finale si elle diffère de `to` |
| `deliveryTarget`          | Remplacement de livraison de niveau inférieur                           |
| `replyToId`               | ID de message cité/ancré                              |
| `replyToIdFull`           | ID cité de forme complète quand la plateforme en a les deux          |
| `messageThreadId`         | ID de fil au moment de la livraison                              |
| `threadParentId`          | ID de message parent du fil                         |
| `sourceReplyDeliveryMode` | `thread`, `reply`, `channel`, `direct`, ou `none`       |

### AccessFacts

`AccessFacts` porte les booléens dont l'étape d'autorisation a besoin. La correspondance d'identité reste dans le canal : le noyau ne consomme que le résultat.

| Champ      | Objectif                                                                   |
| ---------- | ------------------------------------------------------------------------- |
| `dm`       | Décision d'autorisation/appairage/refus DM et liste `allowFrom`                       |
| `group`    | Politique de groupe, autorisation de routage, autorisation d'expéditeur, liste d'autorisation, exigence de mention   |
| `commands` | Autorisation de commande sur les autorisateurs configurés                      |
| `mentions` | Si la détection de mention est possible et si l'agent a été mentionné |

### MessageFacts

| Champ            | Objectif                                                        |
| ---------------- | -------------------------------------------------------------- |
| `body`           | Corps d'enveloppe final (formaté)                                |
| `rawBody`        | Corps entrant brut                                               |
| `bodyForAgent`   | Corps que l'agent voit                                            |
| `commandBody`    | Corps utilisé pour l'analyse de commande                                  |
| `envelopeFrom`   | Étiquette d'expéditeur pré-rendue pour l'enveloppe                     |
| `senderLabel`    | Remplacement optionnel pour l'expéditeur rendu                      |
| `preview`        | Aperçu court et édité pour les journaux                                |
| `inboundHistory` | Entrées d'historique entrant récentes quand le canal conserve un tampon |

### SupplementalContextFacts

Le contexte supplémentaire couvre la citation, le transfert et le contexte d'amorçage de fil. Le noyau applique la politique `contextVisibility` configurée. L'adaptateur de canal fournit uniquement les faits et les drapeaux `senderAllowed` afin que la politique inter-canaux reste cohérente.

### InboundMediaFacts

Le média est en forme de fait. Le téléchargement de plateforme, l'authentification, la politique SSRF, les règles CDN et le déchiffrement restent locaux au canal. Le noyau mappe les faits dans `MediaPath`, `MediaUrl`, `MediaType`, `MediaPaths`, `MediaUrls`, `MediaTypes`, et `MediaTranscribedIndexes`.

## Contrat d'adaptateur

Pour `run` complet, la forme d'adaptateur est :

```typescript
type ChannelTurnAdapter<TRaw> = {
  ingest(raw: TRaw): Promise<NormalizedTurnInput | null> | NormalizedTurnInput | null;
  classify?(input: NormalizedTurnInput): Promise<ChannelEventClass> | ChannelEventClass;
  preflight?(
    input: NormalizedTurnInput,
    eventClass: ChannelEventClass,
  ): Promise<PreflightFacts | ChannelTurnAdmission | null | undefined>;
  resolveTurn(
    input: NormalizedTurnInput,
    eventClass: ChannelEventClass,
    preflight: PreflightFacts,
  ): Promise<ChannelTurnResolved> | ChannelTurnResolved;
  onFinalize?(result: ChannelTurnResult): Promise<void> | void;
};
```

`resolveTurn` retourne un `ChannelTurnResolved`, qui est un `AssembledChannelTurn` avec un type d'admission optionnel. Retourner `{ admission: { kind: "observeOnly" } }` exécute le tour sans produire de sortie visible. L'adaptateur possède toujours le rappel de livraison ; il devient simplement un no-op pour ce tour.

`onFinalize` s'exécute sur chaque résultat, y compris les erreurs de distribution. Utilisez-le pour effacer l'historique de groupe en attente, supprimer les réactions d'accusé de réception, arrêter les indicateurs d'état et vider l'état local.

## Adaptateur de livraison

Le noyau n'appelle pas la plateforme directement. Le canal remet au noyau un `ChannelTurnDeliveryAdapter` :

```typescript
type ChannelTurnDeliveryAdapter = {
  deliver(payload: ReplyPayload, info: ChannelDeliveryInfo): Promise<ChannelDeliveryResult | void>;
  onError?(err: unknown, info: { kind: string }): void;
};

type ChannelDeliveryResult = {
  messageIds?: string[];
  threadId?: string;
  replyToId?: string;
  visibleReplySent?: boolean;
};
```

`deliver` est appelé une fois par bloc de réponse mis en tampon. Retournez les ID de message de plateforme quand le canal les a afin que le distributeur puisse préserver les ancres de fil et modifier les blocs ultérieurs. Pour les tours en observation seule, retournez `{ visibleReplySent: false }` ou utilisez `createNoopChannelTurnDeliveryAdapter()`.

## Options d'enregistrement

L'étape d'enregistrement enveloppe `recordInboundSession`. La plupart des canaux peuvent utiliser les valeurs par défaut. Remplacez via `record` :

```typescript
record: {
  groupResolution,
  createIfMissing: true,
  updateLastRoute,
  onRecordError: (err) => log.warn("record failed", err),
  trackSessionMetaTask: (task) => pendingTasks.push(task),
}
```

Le distributeur attend l'étape d'enregistrement. Si l'enregistrement lève une exception, le noyau exécute `onPreDispatchFailure` (quand fourni à `runPrepared`) et relève.

## Observabilité

Chaque étape émet un événement structuré quand un rappel `log` est fourni :

```typescript
await runtime.channel.turn.run({
  channel: "twitch",
  accountId,
  raw,
  adapter,
  log: (event) => {
    runtime.log?.debug?.(`turn.${event.stage}:${event.event}`, {
      channel: event.channel,
      accountId: event.accountId,
      messageId: event.messageId,
      sessionKey: event.sessionKey,
      admission: event.admission,
      reason: event.reason,
    });
  },
});
```

Étapes enregistrées : `ingest`, `classify`, `preflight`, `resolve`, `authorize`, `assemble`, `record`, `dispatch`, `finalize`. Évitez de journaliser les corps bruts ; utilisez `MessageFacts.preview` pour les aperçus courts et édités.

## Ce qui reste local au canal

Le noyau possède l'orchestration. Le canal possède toujours :

- Transports de plateforme (passerelle, REST, websocket, interrogation, webhooks)
- Résolution d'identité et correspondance de nom d'affichage
- Commandes natives, commandes slash, autocomplétion, modales, boutons, état vocal
- Rendu de carte, modale et carte adaptative
- Authentification média, règles CDN, média chiffré, transcription
- API d'édition, de réaction, de suppression et de présence
- Remplissage et récupération d'historique côté plateforme
- Flux d'appairage qui nécessitent une vérification spécifique à la plateforme

Si deux canaux commencent à avoir besoin du même assistant pour l'un de ceux-ci, extrayez un assistant SDK partagé au lieu de le pousser dans le noyau.

## Stabilité

`runtime.channel.turn.*` fait partie de la surface d'exécution de plugin publique. Les types de faits (`SenderFacts`, `ConversationFacts`, `RouteFacts`, `ReplyPlanFacts`, `AccessFacts`, `MessageFacts`, `SupplementalContextFacts`, `InboundMediaFacts`) et les formes d'admission (`ChannelTurnAdmission`, `ChannelEventClass`) sont accessibles via `PluginRuntime` depuis `openclaw/plugin-sdk/core`.

Les règles de compatibilité rétroactive s'appliquent : les nouveaux champs de faits sont additifs, les types d'admission ne sont pas renommés, et les noms de points d'entrée restent stables. Les nouveaux besoins de canal qui nécessitent un changement non-additif doivent passer par le processus de migration du SDK de plugin.

## Connexes

- [Création de plugins de canal](/fr/plugins/sdk-channel-plugins) pour le contrat de plugin de canal plus large
- [Assistants d'exécution de plugin](/fr/plugins/sdk-runtime) pour les autres surfaces `runtime.*`
- [Éléments internes du plugin](/fr/plugins/architecture-internals) pour la mécanique du pipeline de chargement et du registre
