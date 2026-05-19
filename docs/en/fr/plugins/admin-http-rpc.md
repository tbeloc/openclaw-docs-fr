---
summary: "Exposer les méthodes du plan de contrôle Gateway sélectionnées via le plugin admin-http-rpc fourni et optionnel"
read_when:
  - Building host tooling that cannot use the Gateway WebSocket RPC client
  - Exposing Gateway admin automation behind a private trusted ingress
  - Auditing the security model for HTTP access to Gateway methods
title: "Plugin Admin HTTP RPC"
---

Le plugin fourni `admin-http-rpc` expose les méthodes du plan de contrôle Gateway sélectionnées sur HTTP pour l'automatisation d'hôte de confiance qui ne peut pas utiliser le client WebSocket RPC Gateway normal.

Le plugin est inclus avec OpenClaw, mais il est désactivé par défaut. Lorsqu'il est désactivé, la route n'est pas enregistrée. Lorsqu'il est activé, il ajoute :

- `POST /api/v1/admin/rpc`
- même écouteur que la Gateway : `http://<gateway-host>:<port>/api/v1/admin/rpc`

Activez-le uniquement pour les outils d'hôte privés, l'automatisation tailnet ou une entrée interne de confiance. N'exposez pas cette route directement à l'Internet public.

## Avant de l'activer

Admin HTTP RPC est une surface de plan de contrôle d'opérateur complet. Tout appelant qui transmet l'authentification HTTP Gateway peut invoquer les méthodes autorisées sur cette page.

Utilisez-le lorsque tous ces éléments sont vrais :

- L'appelant est de confiance pour exploiter la Gateway.
- L'appelant ne peut pas utiliser le client WebSocket RPC.
- La route est accessible uniquement sur loopback, un tailnet ou une entrée interne authentifiée privée.
- Vous avez examiné les méthodes autorisées et elles correspondent à l'automatisation que vous prévoyez d'exécuter.

Utilisez le chemin WebSocket RPC pour les clients OpenClaw et les outils interactifs qui peuvent maintenir une connexion WebSocket Gateway ouverte.

## Activer

Activez le plugin fourni :

<Tabs>
  <Tab title="CLI">
    ```bash
    openclaw plugins enable admin-http-rpc
    openclaw gateway restart
    ```
  </Tab>
  <Tab title="Config">
    ```json5
    {
      plugins: {
        entries: {
          "admin-http-rpc": { enabled: true },
        },
      },
    }
    ```
  </Tab>
</Tabs>

La route est enregistrée lors du démarrage du plugin. Redémarrez la Gateway après avoir modifié la configuration du plugin.

Désactivez-le lorsque vous n'avez plus besoin de la surface HTTP :

```bash
openclaw plugins disable admin-http-rpc
openclaw gateway restart
```

## Vérifier la route

Utilisez `health` comme la plus petite demande sûre :

```bash
curl -sS http://<gateway-host>:<port>/api/v1/admin/rpc \
  -H 'Authorization: Bearer <gateway-token>' \
  -H 'Content-Type: application/json' \
  -d '{"method":"health","params":{}}'
```

Une réponse réussie a `ok: true` :

```json
{
  "id": "generated-request-id",
  "ok": true,
  "payload": {
    "status": "ok"
  }
}
```

Lorsque le plugin est désactivé, la route retourne `404` car elle n'est pas enregistrée.

## Authentification

La route du plugin utilise l'authentification HTTP Gateway.

Chemins d'authentification courants :

- authentification par secret partagé (`gateway.auth.mode="token"` ou `"password"`): `Authorization: Bearer <token-or-password>`
- authentification HTTP porteuse d'identité de confiance (`gateway.auth.mode="trusted-proxy"`): acheminez via le proxy conscient de l'identité configuré et laissez-le injecter les en-têtes d'identité requis
- authentification ouverte d'entrée privée (`gateway.auth.mode="none"`): aucun en-tête d'authentification requis

## Modèle de sécurité

Traitez ce plugin comme une surface d'opérateur Gateway complète.

- L'activation du plugin offre intentionnellement l'accès aux méthodes RPC admin autorisées à `/api/v1/admin/rpc`.
- Le plugin déclare le contrat de manifeste réservé `contracts.gatewayMethodDispatch: ["authenticated-request"]` afin que sa route HTTP authentifiée par Gateway puisse dispatcher les méthodes du plan de contrôle en processus.
- L'authentification par porteur de secret partagé prouve la possession du secret d'opérateur gateway.
- Pour l'authentification `token` et `password`, les en-têtes `x-openclaw-scopes` plus étroits sont ignorés et les valeurs par défaut d'opérateur complet normal sont restaurées.
- Les modes HTTP porteurs d'identité de confiance honorent `x-openclaw-scopes` lorsqu'ils sont présents.
- `gateway.auth.mode="none"` signifie que cette route n'est pas authentifiée si le plugin est activé. Utilisez cela uniquement derrière une entrée privée en laquelle vous avez entièrement confiance.
- Les demandes sont dispatched via les mêmes gestionnaires de méthodes Gateway et vérifications de portée que WebSocket RPC après que l'authentification de la route du plugin réussisse.
- Gardez cette route sur loopback, tailnet ou une entrée interne de confiance. Ne l'exposez pas directement à l'Internet public.
- Les contrats de manifeste de plugin ne sont pas un bac à sable. Ils empêchent l'utilisation accidentelle des assistants SDK réservés ; les plugins de confiance s'exécutent toujours dans le processus Gateway.

Utilisez des gateways séparées lorsque les appelants franchissent les limites de confiance.

## Demande

```http
POST /api/v1/admin/rpc
Authorization: Bearer <gateway-token>
Content-Type: application/json
```

```json
{
  "id": "optional-request-id",
  "method": "health",
  "params": {}
}
```

Champs :

- `id` (string, optionnel) : copié dans la réponse. Un UUID est généré lorsqu'il est omis.
- `method` (string, requis) : nom de méthode Gateway autorisé.
- `params` (any, optionnel) : paramètres spécifiques à la méthode.

La taille maximale par défaut du corps de la demande est de 1 Mo.

## Réponse

Les réponses réussies utilisent la forme Gateway RPC :

```json
{
  "id": "optional-request-id",
  "ok": true,
  "payload": {}
}
```

Les erreurs de méthode Gateway utilisent :

```json
{
  "id": "optional-request-id",
  "ok": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "bad params"
  }
}
```

Le statut HTTP suit l'erreur Gateway si possible. Par exemple, `INVALID_REQUEST` retourne `400` et `UNAVAILABLE` retourne `503`.

## Méthodes autorisées

- discovery: `commands.list`
  Retourne les noms de méthode HTTP RPC autorisés par ce plugin.
- gateway: `health`, `status`, `logs.tail`, `usage.status`, `usage.cost`, `gateway.restart.request`
- config: `config.get`, `config.schema`, `config.schema.lookup`, `config.set`, `config.patch`, `config.apply`
- channels: `channels.status`, `channels.start`, `channels.stop`, `channels.logout`
- web: `web.login.start`, `web.login.wait`
- models: `models.list`, `models.authStatus`
- agents: `agents.list`, `agents.create`, `agents.update`, `agents.delete`
- approvals: `exec.approvals.get`, `exec.approvals.set`, `exec.approvals.node.get`, `exec.approvals.node.set`
- cron: `cron.status`, `cron.list`, `cron.get`, `cron.runs`, `cron.add`, `cron.update`, `cron.remove`, `cron.run`
- devices: `device.pair.list`, `device.pair.approve`, `device.pair.reject`, `device.pair.remove`
- nodes: `node.list`, `node.describe`, `node.pair.list`, `node.pair.approve`, `node.pair.reject`, `node.pair.remove`, `node.rename`
- tasks: `tasks.list`, `tasks.get`, `tasks.cancel`
- diagnostics: `doctor.memory.status`, `update.status`

Les autres méthodes Gateway sont bloquées jusqu'à ce qu'elles soient intentionnellement ajoutées.

## Comparaison WebSocket

Le chemin WebSocket RPC Gateway normal reste l'API du plan de contrôle préférée pour les clients OpenClaw. Utilisez admin HTTP RPC uniquement pour les outils d'hôte qui ont besoin d'une surface HTTP requête/réponse.

Les clients WebSocket à jeton partagé sans identité d'appareil de confiance ne peuvent pas auto-déclarer les portées d'administrateur lors de la connexion. Admin HTTP RPC suit délibérément le modèle d'opérateur HTTP de confiance existant : lorsque le plugin est activé, l'authentification par porteur de secret partagé est traitée comme un accès d'opérateur complet pour cette surface d'administration.

## Dépannage

`404 Not Found`

: Le plugin est désactivé, la Gateway n'a pas redémarré depuis son activation, ou la demande va à un processus Gateway différent.

`401 Unauthorized`

: La demande n'a pas satisfait l'authentification HTTP Gateway. Vérifiez le jeton porteur ou les en-têtes d'identité du proxy de confiance.

`400 INVALID_REQUEST`

: Le corps de la demande n'est pas un JSON valide, le champ `method` est manquant ou la méthode ne figure pas dans la liste d'autorisation du plugin.

`503 UNAVAILABLE`

: Le gestionnaire de méthode Gateway n'est pas disponible. Vérifiez les journaux Gateway et réessayez après que la Gateway ait terminé le démarrage.

## Connexes

- [Operator scopes](/fr/gateway/operator-scopes)
- [Gateway security](/fr/gateway/security)
- [Remote access](/fr/gateway/remote)
- [Plugin manifest](/fr/plugins/manifest#contracts)
- [SDK subpaths](/fr/plugins/sdk-subpaths)
