---
summary: "API de canal d'entrée expérimentale pour l'autorisation des messages entrants"
read_when:
  - Building or migrating a messaging channel plugin
  - Changing DM or group allowlists, route gates, command auth, event auth, or mention activation
  - Reviewing channel ingress redaction or SDK compatibility boundaries
title: "API de canal d'entrée"
sidebarTitle: "Canal d'entrée"
---

# API de canal d'entrée

Le canal d'entrée est la limite de contrôle d'accès expérimentale pour les événements de canal entrants. Utilisez `openclaw/plugin-sdk/channel-ingress-runtime` pour les chemins de réception. Le chemin d'accès `openclaw/plugin-sdk/channel-ingress` plus ancien reste exporté comme façade de compatibilité dépréciée pour les plugins tiers.

Les plugins possèdent les faits de plateforme et les effets secondaires. Le noyau possède la politique générique : listes blanches DM/groupe, entrées DM du magasin d'appairage, portes d'itinéraire, portes de commande, authentification d'événement, activation de mention, diagnostics redactés et admission.

## Résolveur d'exécution

```ts
import {
  defineStableChannelIngressIdentity,
  resolveChannelMessageIngress,
} from "openclaw/plugin-sdk/channel-ingress-runtime";

const identity = defineStableChannelIngressIdentity({
  key: "platform-user-id",
  normalize: normalizePlatformUserId,
  sensitivity: "pii",
});

const result = await resolveChannelMessageIngress({
  channelId: "my-channel",
  accountId,
  identity,
  subject: { stableId: platformUserId },
  conversation: { kind: isGroup ? "group" : "direct", id: conversationId },
  event: { kind: "message", authMode: "inbound", mayPair: !isGroup },
  policy: {
    dmPolicy: config.dmPolicy,
    groupPolicy: config.groupPolicy,
    groupAllowFromFallbackToAllowFrom: true,
  },
  allowFrom: config.allowFrom,
  groupAllowFrom: config.groupAllowFrom,
  accessGroups: cfg.accessGroups,
  route,
  readStoreAllowFrom,
  command: hasControlCommand ? { allowTextCommands: true, hasControlCommand } : undefined,
});
```

Ne précalculez pas les listes blanches effectives, les propriétaires de commandes ou les groupes de commandes. Le résolveur les dérive des listes blanches brutes, des rappels de magasin, des descripteurs d'itinéraire, des groupes d'accès, de la politique et du type de conversation.

## Résultat

Les plugins groupés doivent consommer les projections modernes directement :

- `ingress` : décision de porte ordonnée et admission
- `senderAccess` : autorisation de l'expéditeur/conversation uniquement
- `routeAccess` : projection d'itinéraire et d'expéditeur d'itinéraire
- `commandAccess` : autorisation de commande ; faux quand aucune porte de commande n'a été exécutée
- `activationAccess` : résultat de mention/activation

L'autorisation d'événement reste disponible sur le `ingress.graph` ordonné et le `ingress.reasonCode` décisif ; aucune projection d'événement séparée n'est émise.

Les aides SDK tiers dépréciées peuvent reconstruire les formes plus anciennes en interne. Les nouveaux chemins de réception groupés ne doivent pas traduire les résultats modernes en DTO locaux.

## Groupes d'accès

Les entrées `accessGroup:<name>` restent redactées. Le noyau résout lui-même les groupes `message.senders` statiques et n'appelle `resolveAccessGroupMembership` que pour les groupes dynamiques qui nécessitent une recherche de plateforme. Les groupes manquants, non pris en charge et échoués échouent fermés.

## Modes d'événement

| `authMode`       | Signification                                          |
| ---------------- | ------------------------------------------------------ |
| `inbound`        | portes d'expéditeur entrant normal                     |
| `command`        | portes de commande pour les rappels ou boutons limités |
| `origin-subject` | l'acteur doit correspondre au sujet du message original |
| `route-only`     | portes d'itinéraire uniquement pour les événements de confiance limités à l'itinéraire |
| `none`           | les événements internes appartenant au plugin contournent l'authentification partagée |

Utilisez `mayPair: false` pour les réactions, boutons, rappels et commandes natives.

## Itinéraires et activation

Utilisez des descripteurs d'itinéraire pour la politique de salle, sujet, guilde, fil ou itinéraire imbriqué :

```ts
route: {
  id: "room",
  allowed: roomAllowed,
  enabled: roomEnabled,
  senderPolicy: "replace",
  senderAllowFrom: roomAllowFrom,
  blockReason: "room_sender_not_allowlisted",
}
```

Utilisez `channelIngressRoutes(...)` quand un plugin a plusieurs descripteurs d'itinéraire optionnels ; il filtre les branches désactivées tout en gardant les faits d'itinéraire génériques et ordonnés par la `precedence` de chaque descripteur.

La limitation de mention est une porte d'activation. Un manque de mention retourne `admission: "skip"` afin que le noyau de tour ne traite pas un tour d'observation uniquement. La plupart des canaux doivent laisser l'activation après les portes d'expéditeur et de commande. Les surfaces de chat public qui doivent réduire le bruit du trafic non mentionné avant le bruit de la liste blanche d'expéditeur peuvent opter pour `activation.order: "before-sender"` quand le contournement de commande textuelle est désactivé. Les canaux avec activation implicite, comme les réponses dans les fils de bot, peuvent passer `activation.allowedImplicitMentionKinds` ; la `activationAccess.shouldBypassMention` projetée rapporte alors quand l'activation de commande ou implicite a contourné une mention explicite.

## Redaction

Les valeurs d'expéditeur brutes et les entrées de liste blanche brutes sont l'entrée du résolveur uniquement. Elles ne doivent pas apparaître dans l'état résolu, les décisions, les diagnostics, les instantanés ou les faits de compatibilité. Utilisez les identifiants de sujet opaques, les identifiants d'entrée, les identifiants d'itinéraire et les identifiants de diagnostic.

## Vérification

```bash
pnpm test src/channels/message-access/message-access.test.ts src/plugin-sdk/channel-ingress-runtime.test.ts
pnpm plugin-sdk:api:check
```
