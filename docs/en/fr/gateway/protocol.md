---
summary: "Protocole WebSocket de la passerelle : établissement de connexion, trames, versioning"
read_when:
  - Implementing or updating gateway WS clients
  - Debugging protocol mismatches or connect failures
  - Regenerating protocol schema/models
title: "Protocole de la passerelle"
---

# Protocole de la passerelle (WebSocket)

Le protocole WS de la passerelle est le **plan de contrôle unique + transport de nœud** pour
OpenClaw. Tous les clients (CLI, interface web, application macOS, nœuds iOS/Android, nœuds sans interface) se connectent via WebSocket et déclarent leur **rôle** + **portée** au
moment de l'établissement de connexion.

## Transport

- WebSocket, trames texte avec charges utiles JSON.
- La première trame **doit** être une requête `connect`.

## Établissement de connexion (connect)

Passerelle → Client (défi pré-connexion) :

```json
{
  "type": "event",
  "event": "connect.challenge",
  "payload": { "nonce": "…", "ts": 1737264000000 }
}
```

Client → Passerelle :

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

Passerelle → Client :

```json
{
  "type": "res",
  "id": "…",
  "ok": true,
  "payload": { "type": "hello-ok", "protocol": 3, "policy": { "tickIntervalMs": 15000 } }
}
```

Lorsqu'un jeton d'appareil est émis, `hello-ok` inclut également :

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

## Encadrement

- **Requête** : `{type:"req", id, method, params}`
- **Réponse** : `{type:"res", id, ok, payload|error}`
- **Événement** : `{type:"event", event, payload, seq?, stateVersion?}`

Les méthodes avec effets secondaires nécessitent des **clés d'idempotence** (voir schéma).

## Rôles + portées

### Rôles

- `operator` = client du plan de contrôle (CLI/UI/automatisation).
- `node` = hôte de capacité (caméra/écran/canevas/system.run).

### Portées (opérateur)

Portées courantes :

- `operator.read`
- `operator.write`
- `operator.admin`
- `operator.approvals`
- `operator.pairing`

La portée de la méthode n'est que la première barrière. Certaines commandes slash atteintes via
`chat.send` appliquent des vérifications plus strictes au niveau de la commande. Par exemple, les écritures persistantes
`/config set` et `/config unset` nécessitent `operator.admin`.

### Caps/commandes/permissions (nœud)

Les nœuds déclarent les revendications de capacité au moment de la connexion :

- `caps` : catégories de capacité de haut niveau.
- `commands` : liste blanche de commandes pour l'invocation.
- `permissions` : bascules granulaires (par exemple `screen.record`, `camera.capture`).

La passerelle traite ces éléments comme des **revendications** et applique des listes blanches côté serveur.

## Présence

- `system-presence` retourne des entrées indexées par identité d'appareil.
- Les entrées de présence incluent `deviceId`, `roles` et `scopes` afin que les interfaces utilisateur puissent afficher une seule ligne par appareil
  même lorsqu'il se connecte à la fois en tant qu'**opérateur** et **nœud**.

### Méthodes d'assistance pour les nœuds

- Les nœuds peuvent appeler `skills.bins` pour récupérer la liste actuelle des exécutables de compétences
  pour les vérifications d'auto-autorisation.

### Méthodes d'assistance pour les opérateurs

- Les opérateurs peuvent appeler `tools.catalog` (`operator.read`) pour récupérer le catalogue d'outils d'exécution pour un
  agent. La réponse inclut les outils groupés et les métadonnées de provenance :
  - `source` : `core` ou `plugin`
  - `pluginId` : propriétaire du plugin lorsque `source="plugin"`
  - `optional` : indique si un outil de plugin est optionnel

## Approbations d'exécution

- Lorsqu'une requête d'exécution nécessite une approbation, la passerelle diffuse `exec.approval.requested`.
- Les clients opérateurs résolvent en appelant `exec.approval.resolve` (nécessite la portée `operator.approvals`).
- Pour `host=node`, `exec.approval.request` doit inclure `systemRunPlan` (canonical `argv`/`cwd`/`rawCommand`/métadonnées de session). Les requêtes sans `systemRunPlan` sont rejetées.

## Versioning

- `PROTOCOL_VERSION` se trouve dans `src/gateway/protocol/schema.ts`.
- Les clients envoient `minProtocol` + `maxProtocol` ; le serveur rejette les incompatibilités.
- Les schémas + modèles sont générés à partir des définitions TypeBox :
  - `pnpm protocol:gen`
  - `pnpm protocol:gen:swift`
  - `pnpm protocol:check`

## Authentification

- Si `OPENCLAW_GATEWAY_TOKEN` (ou `--token`) est défini, `connect.params.auth.token`
  doit correspondre ou le socket est fermé.
- Après l'appairage, la passerelle émet un **jeton d'appareil** limité au rôle de connexion + portées. Il est retourné dans `hello-ok.auth.deviceToken` et doit être
  conservé par le client pour les connexions futures.
- Les jetons d'appareil peuvent être renouvelés/révoqués via `device.token.rotate` et
  `device.token.revoke` (nécessite la portée `operator.pairing`).
- Les échecs d'authentification incluent `error.details.code` plus des conseils de récupération :
  - `error.details.canRetryWithDeviceToken` (booléen)
  - `error.details.recommendedNextStep` (`retry_with_device_token`, `update_auth_configuration`, `update_auth_credentials`, `wait_then_retry`, `review_auth_configuration`)
- Comportement du client pour `AUTH_TOKEN_MISMATCH` :
  - Les clients de confiance peuvent tenter une nouvelle tentative limitée avec un jeton par appareil en cache.
  - Si cette nouvelle tentative échoue, les clients doivent arrêter les boucles de reconnexion automatique et afficher les conseils d'action de l'opérateur.

## Identité d'appareil + appairage

- Les nœuds doivent inclure une identité d'appareil stable (`device.id`) dérivée d'une
  empreinte digitale de paire de clés.
- Les passerelles émettent des jetons par appareil + rôle.
- Les approbations d'appairage sont requises pour les nouveaux ID d'appareil sauf si l'auto-approbation locale
  est activée.
- Les connexions **locales** incluent la boucle locale et l'adresse tailnet du propre hôte de la passerelle
  (afin que les liaisons tailnet du même hôte puissent toujours s'auto-approuver).
- Tous les clients WS doivent inclure l'identité `device` lors de `connect` (opérateur + nœud).
  L'interface utilisateur de contrôle peut l'omettre uniquement dans ces modes :
  - `gateway.controlUi.allowInsecureAuth=true` pour la compatibilité HTTP insécurisée localhost uniquement.
  - `gateway.controlUi.dangerouslyDisableDeviceAuth=true` (break-glass, dégradation grave de la sécurité).
- Toutes les connexions doivent signer le nonce `connect.challenge` fourni par le serveur.

### Diagnostics de migration d'authentification d'appareil

Pour les clients hérités qui utilisent toujours le comportement de signature pré-défi, `connect` retourne maintenant
des codes de détail `DEVICE_AUTH_*` sous `error.details.code` avec une `error.details.reason` stable.

Échecs de migration courants :

| Message                     | details.code                     | details.reason           | Signification                                      |
| --------------------------- | -------------------------------- | ------------------------ | -------------------------------------------------- |
| `device nonce required`     | `DEVICE_AUTH_NONCE_REQUIRED`     | `device-nonce-missing`   | Le client a omis `device.nonce` (ou envoyé vide).  |
| `device nonce mismatch`     | `DEVICE_AUTH_NONCE_MISMATCH`     | `device-nonce-mismatch`  | Le client a signé avec un nonce obsolète/incorrect.|
| `device signature invalid`  | `DEVICE_AUTH_SIGNATURE_INVALID`  | `device-signature`       | La charge utile de signature ne correspond pas à la charge utile v2. |
| `device signature expired`  | `DEVICE_AUTH_SIGNATURE_EXPIRED`  | `device-signature-stale` | L'horodatage signé est en dehors de l'écart autorisé. |
| `device identity mismatch`  | `DEVICE_AUTH_DEVICE_ID_MISMATCH` | `device-id-mismatch`     | `device.id` ne correspond pas à l'empreinte digitale de la clé publique. |
| `device public key invalid` | `DEVICE_AUTH_PUBLIC_KEY_INVALID` | `device-public-key`      | Le format/canonicalisation de la clé publique a échoué. |

Cible de migration :

- Attendez toujours `connect.challenge`.
- Signez la charge utile v2 qui inclut le nonce du serveur.
- Envoyez le même nonce dans `connect.params.device.nonce`.
- La charge utile de signature préférée est `v3`, qui lie `platform` et `deviceFamily`
  en plus des champs device/client/role/scopes/token/nonce.
- Les signatures `v2` héritées restent acceptées pour la compatibilité, mais l'épinglage des métadonnées d'appareil appairé
  contrôle toujours la politique de commande à la reconnexion.

## TLS + épinglage

- TLS est pris en charge pour les connexions WS.
- Les clients peuvent éventuellement épingler l'empreinte digitale du certificat de la passerelle (voir la configuration `gateway.tls`
  plus `gateway.remote.tlsFingerprint` ou CLI `--tls-fingerprint`).

## Portée

Ce protocole expose l'**API complète de la passerelle** (statut, canaux, modèles, chat,
agent, sessions, nœuds, approbations, etc.). La surface exacte est définie par les
schémas TypeBox dans `src/gateway/protocol/schema.ts`.
