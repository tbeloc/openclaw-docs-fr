---
read_when:
  - Mise à jour du schéma de protocole ou génération de code
summary: Schéma TypeBox comme source unique de vérité pour le protocole Gateway
title: TypeBox
x-i18n:
  generated_at: "2026-02-03T07:47:23Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 233800f4f5fabe8ed0e1b3d8aded2eca27252e08c9b0b24ea9c6293e9282c918
  source_path: concepts/typebox.md
  workflow: 15
---

# TypeBox comme source de vérité du protocole

Dernière mise à jour : 2026-01-10

TypeBox est une bibliothèque de schémas orientée TypeScript. Nous l'utilisons pour définir le **protocole WebSocket Gateway** (poignée de main, requête/réponse, événements serveur). Ces schémas pilotent la **validation à l'exécution**, l'**export JSON Schema** et la **génération de code Swift** pour l'application macOS. Une source unique de vérité ; tout le reste est généré.

Si vous souhaitez comprendre le contexte du protocole à un niveau plus élevé, commencez par [l'architecture Gateway](/concepts/architecture).

## Modèle mental (30 secondes)

Chaque message Gateway WS est l'un de ces trois types de trames :

- **Request** : `{ type: "req", id, method, params }`
- **Response** : `{ type: "res", id, ok, payload | error }`
- **Event** : `{ type: "event", event, payload, seq?, stateVersion? }`

La première trame **doit** être une requête `connect`. Après cela, le client peut appeler des méthodes (par exemple `health`, `send`, `chat.send`) et s'abonner à des événements (par exemple `presence`, `tick`, `agent`).

Flux de connexion (minimal) :

```
Client                    Gateway
  |---- req:connect -------->|
  |<---- res:hello-ok --------|
  |<---- event:tick ----------|
  |---- req:health ---------->|
  |<---- res:health ----------|
```

Méthodes + événements courants :

| Catégorie | Exemples                                                  | Description                      |
| --------- | --------------------------------------------------------- | -------------------------------- |
| Cœur      | `connect`, `health`, `status`                             | `connect` doit être le premier   |
| Messages  | `send`, `poll`, `agent`, `agent.wait`                     | Ceux avec effets nécessitent `idempotencyKey` |
| Chat      | `chat.history`, `chat.send`, `chat.abort`, `chat.inject`  | Utilisés par WebChat            |
| Sessions  | `sessions.list`, `sessions.patch`, `sessions.delete`      | Gestion des sessions            |
| Nœud      | `node.list`, `node.invoke`, `node.pair.*`                 | Gateway WS + opérations de nœud |
| Événements | `tick`, `presence`, `agent`, `chat`, `health`, `shutdown` | Poussée serveur                 |

La liste faisant autorité se trouve dans `src/gateway/server.ts` (`METHODS`, `EVENTS`).

## Où se trouvent les schémas

- Source : `src/gateway/protocol/schema.ts`
- Validateur à l'exécution (AJV) : `src/gateway/protocol/index.ts`
- Poignée de main serveur + distribution des méthodes : `src/gateway/server.ts`
- Client nœud : `src/gateway/client.ts`
- JSON Schema généré : `dist/protocol.schema.json`
- Modèles Swift générés : `apps/macos/Sources/OpenClawProtocol/GatewayModels.swift`

## Flux actuel

- `pnpm protocol:gen`
  - Écrit JSON Schema (draft‑07) dans `dist/protocol.schema.json`
- `pnpm protocol:gen:swift`
  - Génère les modèles Gateway Swift
- `pnpm protocol:check`
  - Exécute les deux générateurs et vérifie que les sorties sont validées

## Comment les schémas sont utilisés à l'exécution

- **Côté serveur** : Chaque trame entrante est validée avec AJV. La poignée de main n'accepte que les requêtes `connect` dont les paramètres correspondent à `ConnectParams`.
- **Côté client** : Le client JS valide les trames d'événement et de réponse avant utilisation.
- **Surface des méthodes** : Gateway annonce les `methods` et `events` supportés dans `hello-ok`.

## Exemples de trames

Connect (premier message) :

```json
{
  "type": "req",
  "id": "c1",
  "method": "connect",
  "params": {
    "minProtocol": 2,
    "maxProtocol": 2,
    "client": {
      "id": "openclaw-macos",
      "displayName": "macos",
      "version": "1.0.0",
      "platform": "macos 15.1",
      "mode": "ui",
      "instanceId": "A1B2"
    }
  }
}
```

Réponse Hello-ok :

```json
{
  "type": "res",
  "id": "c1",
  "ok": true,
  "payload": {
    "type": "hello-ok",
    "protocol": 2,
    "server": { "version": "dev", "connId": "ws-1" },
    "features": { "methods": ["health"], "events": ["tick"] },
    "snapshot": {
      "presence": [],
      "health": {},
      "stateVersion": { "presence": 0, "health": 0 },
      "uptimeMs": 0
    },
    "policy": { "maxPayload": 1048576, "maxBufferedBytes": 1048576, "tickIntervalMs": 30000 }
  }
}
```

Requête + réponse :

```json
{ "type": "req", "id": "r1", "method": "health" }
```

```json
{ "type": "res", "id": "r1", "ok": true, "payload": { "ok": true } }
```

Événement :

```json
{ "type": "event", "event": "tick", "payload": { "ts": 1730000000 }, "seq": 12 }
```

## Client minimal (Node.js)

Flux minimal viable : connect + health.

```ts
import { WebSocket } from "ws";

const ws = new WebSocket("ws://127.0.0.1:18789");

ws.on("open", () => {
  ws.send(
    JSON.stringify({
      type: "req",
      id: "c1",
      method: "connect",
      params: {
        minProtocol: 3,
        maxProtocol: 3,
        client: {
          id: "cli",
          displayName: "example",
          version: "dev",
          platform: "node",
          mode: "cli",
        },
      },
    }),
  );
});

ws.on("message", (data) => {
  const msg = JSON.parse(String(data));
  if (msg.type === "res" && msg.id === "c1" && msg.ok) {
    ws.send(JSON.stringify({ type: "req", id: "h1", method: "health" }));
  }
  if (msg.type === "res" && msg.id === "h1") {
    console.log("health:", msg.payload);
    ws.close();
  }
});
```

## Exemple pratique : ajouter une méthode de bout en bout

Exemple : ajouter une nouvelle requête `system.echo` qui retourne `{ ok: true, text }`.

1. **Schéma (source de vérité)**

Ajouter à `src/gateway/protocol/schema.ts` :

```ts
export const SystemEchoParamsSchema = Type.Object(
  { text: NonEmptyString },
  { additionalProperties: false },
);

export const SystemEchoResultSchema = Type.Object(
  { ok: Type.Boolean(), text: NonEmptyString },
  { additionalProperties: false },
);
```

Ajouter les deux à `ProtocolSchemas` et exporter les types :

```ts
  SystemEchoParams: SystemEchoParamsSchema,
  SystemEchoResult: SystemEchoResultSchema,
```

```ts
export type SystemEchoParams = Static<typeof SystemEchoParamsSchema>;
export type SystemEchoResult = Static<typeof SystemEchoResultSchema>;
```

2. **Validation**

Dans `src/gateway/protocol/index.ts`, exporter un validateur AJV :

```ts
export const validateSystemEchoParams = ajv.compile<SystemEchoParams>(SystemEchoParamsSchema);
```

3. **Comportement du serveur**

Ajouter un gestionnaire dans `src/gateway/server-methods/system.ts` :

```ts
export const systemHandlers: GatewayRequestHandlers = {
  "system.echo": ({ params, respond }) => {
    const text = String(params.text ?? "");
    respond(true, { ok: true, text });
  },
};
```

Enregistrer dans `src/gateway/server-methods.ts` (les `systemHandlers` sont déjà fusionnés), puis ajouter `"system.echo"` à `METHODS` dans `src/gateway/server.ts`.

4. **Régénérer**

```bash
pnpm protocol:check
```

5. **Tester + documenter**

Ajouter un test serveur dans `src/gateway/server.*.test.ts` et documenter la méthode.

## Comportement de la génération de code Swift

Le générateur Swift produit :

- Une énumération `GatewayFrame` avec les cas `req`, `res`, `event` et `unknown`
- Des structures/énumérations de payload fortement typées
- Les valeurs `ErrorCode` et `GATEWAY_PROTOCOL_VERSION`

Les types de trames inconnus sont conservés comme payload brut pour la compatibilité ascendante.

## Versioning + compatibilité

- `PROTOCOL_VERSION` dans `src/gateway/protocol/schema.ts`.
- Les clients envoient `minProtocol` + `maxProtocol` ; le serveur rejette les non-correspondances.
- Les modèles Swift conservent les types de trames inconnus pour éviter de casser les anciens clients.

## Motifs et conventions de schéma

- La plupart des objets utilisent `additionalProperties: false` pour des payloads stricts.
- `NonEmptyString` est la valeur par défaut pour les ID et les noms de méthodes/événements.
- Le `GatewayFrame` de niveau supérieur utilise un **discriminateur** sur `type`.
- Les méthodes avec effets secondaires nécessitent généralement une `idempotencyKey` dans les paramètres (exemples : `send`, `poll`, `agent`, `chat.send`).

## JSON schema en direct

Le JSON Schema généré se trouve dans `dist/protocol.schema.json` du dépôt. Le fichier brut publié est généralement disponible à :

- https://raw.githubusercontent.com/openclaw/openclaw/main/dist/protocol.schema.json

## Quand vous modifiez le schéma

1. Mettez à jour le schéma TypeBox.
2. Exécutez `pnpm protocol:check`.
3. Validez le schéma régénéré + les modèles Swift.
