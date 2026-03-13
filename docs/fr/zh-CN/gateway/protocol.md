---
read_when:
  - 实现或更新 Gateway 网关 WS 客户端
  - 调试协议不匹配或连接失败
  - 重新生成协议模式/模型
summary: Gateway 网关 WebSocket 协议：握手、帧、版本控制
title: Gateway 网关协议
x-i18n:
  generated_at: "2026-02-03T07:48:42Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: bdafac40d53565901b2df450617287664d77fe4ff52681fa00cab9046b2fd850
  source_path: gateway/protocol.md
  workflow: 15
---

# Protocole Gateway (WebSocket)

Le protocole WS Gateway est le **plan de contrôle unique + transport de nœud** d'OpenClaw. Tous les clients (CLI, Web UI, application macOS, nœuds iOS/Android, nœuds headless) se connectent via WebSocket et déclarent leur **rôle** + **portée** lors de la négociation.

## Transport

- WebSocket, avec des trames texte contenant des charges JSON.
- La première trame **doit** être une requête `connect`.

## Négociation (connect)

Gateway → Client (défi avant connexion) :

```json
{
  "type": "event",
  "event": "connect.challenge",
  "payload": { "nonce": "…", "ts": 1737264000000 }
}
```

Client → Gateway :

```json
{
  "type": "req",
  "id": "…",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 3,
    "client": {
      "id": "cli",
      "version": "1.2.3",
      "platform": "macos",
      "mode": "operator"
    },
    "role": "operator",
    "scopes": ["operator.read", "operator.write"],
    "caps": [],
    "commands": [],
    "permissions": {},
    "auth": { "token": "…" },
    "locale": "en-US",
    "userAgent": "openclaw-cli/1.2.3",
    "device": {
      "id": "device_fingerprint",
      "publicKey": "…",
      "signature": "…",
      "signedAt": 1737264000000,
      "nonce": "…"
    }
  }
}
```

Gateway → Client :

```json
{
  "type": "res",
  "id": "…",
  "ok": true,
  "payload": { "type": "hello-ok", "protocol": 3, "policy": { "tickIntervalMs": 15000 } }
}
```

Lors de l'émission d'un jeton d'appareil, `hello-ok` contient également :

```json
{
  "auth": {
    "deviceToken": "…",
    "role": "operator",
    "scopes": ["operator.read", "operator.write"]
  }
}
```

### Exemple de nœud

```json
{
  "type": "req",
  "id": "…",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 3,
    "client": {
      "id": "ios-node",
      "version": "1.2.3",
      "platform": "ios",
      "mode": "node"
    },
    "role": "node",
    "scopes": [],
    "caps": ["camera", "canvas", "screen", "location", "voice"],
    "commands": ["camera.snap", "canvas.navigate", "screen.record", "location.get"],
    "permissions": { "camera.capture": true, "screen.record": false },
    "auth": { "token": "…" },
    "locale": "en-US",
    "userAgent": "openclaw-ios/1.2.3",
    "device": {
      "id": "device_fingerprint",
      "publicKey": "…",
      "signature": "…",
      "signedAt": 1737264000000,
      "nonce": "…"
    }
  }
}
```

## Format des trames

- **Requête** : `{type:"req", id, method, params}`
- **Réponse** : `{type:"res", id, ok, payload|error}`
- **Événement** : `{type:"event", event, payload, seq?, stateVersion?}`

Les méthodes avec effets secondaires nécessitent une **clé d'idempotence** (voir schéma).

## Rôles + Portées

### Rôles

- `operator` = client du plan de contrôle (CLI/UI/automatisation).
- `node` = hôte de capacités (camera/screen/canvas/system.run).

### Portées (operator)

Portées courantes :

- `operator.read`
- `operator.write`
- `operator.admin`
- `operator.approvals`
- `operator.pairing`

### Capacités/Commandes/Permissions (node)

Les nœuds déclarent des capacités lors de la connexion :

- `caps` : catégories de capacités de haut niveau.
- `commands` : liste blanche de commandes pour invoke.
- `permissions` : commutateurs granulaires (par ex. `screen.record`, `camera.capture`).

Gateway traite ces éléments comme des **déclarations** et applique une liste blanche côté serveur.

## Présence en ligne

- `system-presence` retourne des entrées indexées par identité d'appareil.
- Les entrées de présence contiennent `deviceId`, `roles` et `scopes`, permettant à l'UI d'afficher une seule ligne par appareil,
  même s'il est connecté simultanément en tant que **operator** et **node**.

### Méthodes auxiliaires de nœud

- Les nœuds peuvent appeler `skills.bins` pour obtenir la liste actuelle des exécutables de compétences,
  pour les vérifications d'autorisation automatique.

## Approbations Exec

- Lorsqu'une requête exec nécessite une approbation, Gateway diffuse `exec.approval.requested`.
- Les clients opérateur la résolvent en appelant `exec.approval.resolve` (nécessite la portée `operator.approvals`).

## Versioning

- `PROTOCOL_VERSION` est défini dans `src/gateway/protocol/schema.ts`.
- Les clients envoient `minProtocol` + `maxProtocol` ; le serveur rejette les incompatibilités.
- Le schéma + les modèles sont générés à partir des définitions TypeBox :
  - `pnpm protocol:gen`
  - `pnpm protocol:gen:swift`
  - `pnpm protocol:check`

## Authentification

- Si `OPENCLAW_GATEWAY_TOKEN` est défini (ou `--token`), `connect.params.auth.token`
  doit correspondre, sinon le socket sera fermé.
- Après l'appairage, Gateway émet un **jeton d'appareil** limité au rôle de connexion + portées.
  Il est retourné dans `hello-ok.auth.deviceToken` et le client doit le persister pour les connexions futures.
- Les jetons d'appareil peuvent être renouvelés/révoqués via `device.token.rotate` et `device.token.revoke` (nécessite la portée `operator.pairing`).

## Identité d'appareil + Appairage

- Les nœuds doivent inclure une identité d'appareil stable dérivée de l'empreinte de la paire de clés (`device.id`).
- Gateway émet des jetons pour chaque appareil + rôle.
- Les nouveaux ID d'appareil nécessitent une approbation d'appairage, sauf si l'approbation automatique locale est activée.
- Les connexions **locales** incluent loopback et les adresses tailnet du host Gateway lui-même
  (donc la liaison tailnet du même host peut toujours être approuvée automatiquement).
- Tous les clients WS doivent inclure une identité `device` lors de `connect` (operator + node).
  L'UI de contrôle peut l'omettre **uniquement** si `gateway.controlUi.allowInsecureAuth` est activé
  (ou utiliser `gateway.controlUi.dangerouslyDisableDeviceAuth` pour les situations d'urgence).
- Les connexions non-locales doivent signer le nonce `connect.challenge` fourni par le serveur.

## TLS + Épinglage

- Les connexions WS supportent TLS.
- Les clients peuvent optionnellement épingler l'empreinte du certificat Gateway (voir configuration `gateway.tls`
  plus `gateway.remote.tlsFingerprint` ou CLI `--tls-fingerprint`).

## Portée

Ce protocole expose l'**API Gateway complète** (status, channels, models, chat,
agent, sessions, nodes, approvals, etc.). L'interface exacte est définie par le schéma TypeBox dans `src/gateway/protocol/schema.ts`.
