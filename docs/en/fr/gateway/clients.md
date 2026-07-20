---
summary: "Construire un opérateur tiers ou un client WebChat pour le protocole Gateway WebSocket"
read_when:
  - Building an operator, dashboard, or WebChat client outside the OpenClaw repository
  - Implementing Gateway reconnect, history, approvals, or device pairing
  - Updating a third-party client for a new Gateway wire version
title: "Construire un client Gateway"
---

Utilisez les packages Gateway publiés pour construire des tableaux de bord d'opérateurs, des clients WebChat et d'autres applications tierces. Ce guide couvre le cycle de vie du client autour du contrat de fil : authentification, capacités, récupération de reconnexion, historique, abonnements et mises à niveau de version.

Pour les formes de trames, la poignée de main, les erreurs et la surface complète des méthodes, consultez la [spécification du protocole Gateway](https://docs.openclaw.ai/gateway/protocol).

## Installer les packages

```bash
npm install @openclaw/gateway-client @openclaw/gateway-protocol
```

<Note>
Ces packages sont livrés avec les trains de version OpenClaw. Lors du déploiement initial, npm peut retourner `E404` jusqu'à ce que la première version OpenClaw contenant des packages soit publiée ; installez-les uniquement après que les pages du registre ci-dessous se résolvent.
</Note>

- [`@openclaw/gateway-protocol`](https://www.npmjs.com/package/@openclaw/gateway-protocol)
  fournit des schémas, des validateurs d'exécution, des types TypeScript, des registres d'identité client et de capacité, des lecteurs d'erreurs structurées et des constantes de version de protocole.
  Son tarball npm inclut également le [`protocol.schema.json`](https://unpkg.com/@openclaw/gateway-protocol/protocol.schema.json)
  généré, contrat lisible par machine.
- [`@openclaw/gateway-client`](https://www.npmjs.com/package/@openclaw/gateway-client)
  est l'implémentation de connexion de référence. Importez la racine du package pour le client Node et `@openclaw/gateway-client/browser` pour le protocole sûr pour le navigateur, les aides d'authentification d'appareil et de reconnexion.

L'entrée Node possède son propre transport WebSocket. Un hôte navigateur fournit un adaptateur WebSocket plus le stockage persistant et les rappels de signature pour l'identité de l'appareil et le jeton de l'appareil.

## Choisir les portées et appairer l'appareil

Un client de chat interactif complet qui rend également les invites d'approbation doit demander `role: "operator"` avec ces portées :

| Portée               | À utiliser pour                                                                                |
| -------------------- | ----------------------------------------------------------------------------------------------- |
| `operator.read`      | `chat.history`, `sessions.list`, `sessions.subscribe`, état du modèle et événements en lecture seule |
| `operator.write`     | `chat.send` et mutations de session ordinaires                                                |
| `operator.approvals` | Énumération, affichage et résolution des approbations exec ou plugin                          |

Ajoutez `operator.questions` uniquement si le client gère les questions interactives,
`operator.pairing` uniquement s'il gère les appareils ou nœuds appairés, et
`operator.admin` uniquement pour les opérations administratives telles que `config.patch`.
La [référence des portées d'opérateur](https://docs.openclaw.ai/gateway/operator-scopes)
définit les règles complètes de méthode et d'approbation.

Ne créez pas de jeton porteur par client en éditant manuellement `openclaw.json`. Configurez l'authentification d'amorçage partagée de Gateway avec `openclaw configure --section gateway` ou les options `openclaw onboard --gateway-auth ...`, puis laissez l'appairage d'appareil créer le jeton client :

1. Persistez une identité d'appareil Ed25519 dans le client.
2. Attendez `connect.challenge`, signez la charge utile d'appareil liée au défi, et envoyez `connect` avec le rôle d'opérateur demandé, les portées et le jeton Gateway partagé ou le mot de passe pour l'authentification d'amorçage.
3. Si Gateway retourne les détails structurés `PAIRING_REQUIRED`, affichez l'ID de demande et mettez en pause ou réessayez selon `error.details.recommendedNextStep`.
4. Sur l'hôte Gateway, examinez la demande avec `openclaw devices list`, puis approuvez cette demande actuelle exacte avec `openclaw devices approve <requestId>`.
5. Reconnectez-vous et persistez `hello-ok.auth.deviceToken` avec le rôle et les portées négociés. Utilisez ce jeton d'appareil pour les connexions ultérieures.

Les mises à niveau de portée ou de rôle créent une nouvelle demande d'appairage en attente. La rotation de jeton ne peut pas étendre le contrat d'appairage approuvé. Consultez la [CLI Devices](https://docs.openclaw.ai/cli/devices) pour les commandes d'approbation, de rotation et de révocation.

## Annoncer les capacités du client

`connect.params.caps` décrit le comportement optionnel que le client peut consommer. Il n'accorde pas d'autorisation. Importez les noms de `GATEWAY_CLIENT_CAPS` au lieu de dupliquer les littéraux de chaîne :

```ts
import { GATEWAY_CLIENT_CAPS } from "@openclaw/gateway-protocol/client-info";

const caps = [GATEWAY_CLIENT_CAPS.TOOL_EVENTS];
```

Le registre actuel contient `approvals`, `exec-approvals`, `inline-widgets`,
`run-tool-bindings`, `session-scoped-events`, `plugin-approvals`,
`task-suggestions`, `terminal-offset-seq`, `tool-events` et `ui-commands`.
Annoncez uniquement les capacités que le client implémente réellement.

<Warning>
`tool-events` contrôle le streaming d'exécution d'outil en direct. Gateway enregistre uniquement les connexions qui annoncent cette capacité comme destinataires des événements d'outil structurés d'une exécution. Sans cela, la connexion ne reçoit aucun événement d'outil en direct et la poignée de main ne signale pas d'erreur.
</Warning>

Les outils d'agent contrôlés par capacité sont une utilisation distincte de la même déclaration. Si un outil d'agent nécessite une capacité client, Gateway omet cet outil à moins que le client d'origine n'ait annoncé chaque capacité requise.

## Récupérer l'état après reconnexion

Traitez chaque reconnexion réussie comme une nouvelle projection sur l'historique durable et l'état d'exécution en mémoire actuel :

1. Rétablissez `sessions.subscribe` et l'abonnement `sessions.messages.subscribe` de la session sélectionnée.
2. Appelez `chat.history` pour le `sessionKey` sélectionné et remplacez les lignes persistantes locales par la projection `messages` retournée.
3. Si `inFlightRun` est présent, adoptez son `runId`, `text` mis en mémoire tampon et `plan` optionnel. Adoptez l'exécution même lorsque `text` est vide.
4. Lisez `sessionInfo.hasActiveRun` et `sessionInfo.activeRunIds`. Préférez l'appartenance exacte à `activeRunIds` lors de la décision si une exécution conservée possède toujours l'interface utilisateur de streaming. Un `hasActiveRun` vrai sans ID listé peut représenter une autre projection d'exécution active.
5. Réconciliez les événements `agent` suivants par `payload.runId` et `payload.seq`.
   Maintenez la séquence la plus élevée acceptée indépendamment pour chaque exécution, ignorez une séquence déjà vue ou inférieure, et traitez un écart vers l'avant comme une raison de recharger l'historique faisant autorité.

La trame d'événement externe a également un `seq` optionnel, qui ordonne les événements sur la connexion WebSocket actuelle. Il se réinitialise avec une nouvelle connexion. Le `seq` à l'intérieur d'une charge utile d'événement `agent` est assigné par exécution et ordonne le cycle de vie, l'assistant, le plan, l'outil et d'autres événements de flux de cette exécution.

## Utiliser les métadonnées d'historique et les ancres stables

Les lignes retournées par `chat.history` peuvent porter une enveloppe de métadonnées `__openclaw` :

- `id` est l'identité de l'entrée de transcription. Utilisez-le pour les demandes d'historique ancrées,
  mais pas comme clé de ligne d'affichage unique.
- `seq` est la séquence d'enregistrement de transcription positive. Un enregistrement stocké peut se projeter en plus d'une ligne d'affichage, donc gardez les frères et sœurs avec le même `id` et la même séquence ensemble.
- `kind` identifie les lignes synthétiques. Une limite de compaction utilise
  `kind: "compaction"` et peut inclure `tokensBefore` et `tokensAfter` lorsqu'un point de contrôle correspondant a enregistré ces métriques.

Paginez vers l'arrière avec les valeurs `hasMore` et `nextOffset` de la réponse. Les décalages numériques décrivent la projection de transcription actuelle, donc ne les persistez pas comme des signets de longue durée à travers la réinitialisation ou la compaction. Persistez `__openclaw.id` à la place.
Pour restaurer autour d'une ligne connue, appelez `chat.history` avec `messageId` et le `sessionId` qui l'a retourné. Gateway peut résoudre cet ancrage à partir de l'historique d'archive réinitialisé ; les réponses ancrées omettent intentionnellement les métadonnées de pagination numériques.

## S'abonner au lieu d'interroger l'utilisation

Chargez le catalogue initial avec `sessions.list`, puis appelez `sessions.subscribe` une fois par connexion. Fusionnez les événements `sessions.changed` par `sessionKey`. Les charges utiles de changement de session peuvent porter `inputTokens`, `outputTokens`, `totalTokens`,
`totalTokensFresh`, `contextTokens`, `estimatedCostUsd` en direct, les paramètres d'utilisation de réponse et l'état d'exécution active.

Certaines notifications de changement sont uniquement des signaux d'invalidation. Si un événement omet les champs de ligne dont votre vue a besoin, actualisez `sessions.list`. N'interrogez pas `usage.cost` ou `sessions.usage` pour maintenir une liste de session en direct actuelle ; réservez ces méthodes pour les rapports agrégés ou détaillés à la demande.

## Remplir les approbations exec

Un client avec `operator.approvals` doit installer son écouteur d'événement dès que `hello-ok` se termine, puis appeler `exec.approval.list` pour remplir les demandes antérieures à la connexion. Réconciliez la liste et les événements `exec.approval.requested` / `exec.approval.resolved` en direct par ID d'approbation afin qu'une transition en conflit avec la demande de liste ne soit ni perdue ni ressuscitée.

## Suivre les versions de protocole

La version de fil actuelle est `4`. Les clients d'opérateur général et WebChat doivent négocier la version actuelle exacte avec `minProtocol: 4` et `maxProtocol: 4`.
Seuls les clients de nœud authentifiés et les sondes légères ont la fenêtre d'acceptation N-1, actuellement protocole `3` à `4`.

Les changements de protocole sont d'abord additifs. `protocol.schema.json` inclut les métadonnées de version de sortie `since` et les métadonnées de portée requises pour les méthodes principales, mais un changement de version de fil est toujours un événement de rupture explicite pour les clients tiers. Épinglez les versions de package que vous testez, mettez à niveau le client et Gateway ensemble lorsque la version de fil change, et consultez le [changelog OpenClaw](https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md) avant chaque mise à niveau.

## Connexes

- [Protocole Gateway](https://docs.openclaw.ai/gateway/protocol)
- [Intégration d'OpenClaw](https://docs.openclaw.ai/gateway/embedding)
- [Référence RPC Gateway](https://docs.openclaw.ai/reference/rpc)
- [Intégrations Gateway pour applications externes](https://docs.openclaw.ai/gateway/external-apps)
