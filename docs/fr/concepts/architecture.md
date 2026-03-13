---
summary: "Architecture de la passerelle WebSocket, composants et flux clients"
read_when:
  - Working on gateway protocol, clients, or transports
title: "Architecture de la passerelle"
---

# Architecture de la passerelle

Dernière mise à jour : 2026-01-22

## Aperçu

- Une seule **Gateway** longue durée possède toutes les surfaces de messagerie (WhatsApp via
  Baileys, Telegram via grammY, Slack, Discord, Signal, iMessage, WebChat).
- Les clients du plan de contrôle (application macOS, CLI, interface web, automations) se connectent à la
  Gateway via **WebSocket** sur l'hôte de liaison configuré (par défaut
  `127.0.0.1:18789`).
- Les **Nodes** (macOS/iOS/Android/headless) se connectent également via **WebSocket**, mais
  déclarent `role: node` avec des capacités/commandes explicites.
- Une Gateway par hôte ; c'est le seul endroit qui ouvre une session WhatsApp.
- L'**hôte canvas** est servi par le serveur HTTP de la Gateway sous :
  - `/__openclaw__/canvas/` (HTML/CSS/JS modifiables par l'agent)
  - `/__openclaw__/a2ui/` (hôte A2UI)
    Il utilise le même port que la Gateway (par défaut `18789`).

## Composants et flux

### Gateway (daemon)

- Maintient les connexions aux fournisseurs.
- Expose une API WS typée (requêtes, réponses, événements push serveur).
- Valide les trames entrantes par rapport à JSON Schema.
- Émet des événements comme `agent`, `chat`, `presence`, `health`, `heartbeat`, `cron`.

### Clients (application mac / CLI / admin web)

- Une connexion WS par client.
- Envoient des requêtes (`health`, `status`, `send`, `agent`, `system-presence`).
- S'abonnent à des événements (`tick`, `agent`, `presence`, `shutdown`).

### Nodes (macOS / iOS / Android / headless)

- Se connectent au **même serveur WS** avec `role: node`.
- Fournissent une identité d'appareil dans `connect` ; l'appairage est **basé sur l'appareil** (rôle `node`) et
  l'approbation réside dans le magasin d'appairage des appareils.
- Exposent des commandes comme `canvas.*`, `camera.*`, `screen.record`, `location.get`.

Détails du protocole :

- [Protocole de la passerelle](/gateway/protocol)

### WebChat

- Interface utilisateur statique qui utilise l'API WS de la Gateway pour l'historique des chats et les envois.
- Dans les configurations distantes, se connecte via le même tunnel SSH/Tailscale que les autres
  clients.

## Cycle de vie de la connexion (client unique)

```mermaid
sequenceDiagram
    participant Client
    participant Gateway

    Client->>Gateway: req:connect
    Gateway-->>Client: res (ok)
    Note right of Gateway: or res error + close
    Note left of Client: payload=hello-ok<br>snapshot: presence + health

    Gateway-->>Client: event:presence
    Gateway-->>Client: event:tick

    Client->>Gateway: req:agent
    Gateway-->>Client: res:agent<br>ack {runId, status:"accepted"}
    Gateway-->>Client: event:agent<br>(streaming)
    Gateway-->>Client: res:agent<br>final {runId, status, summary}
```

## Protocole filaire (résumé)

- Transport : WebSocket, trames texte avec charges JSON.
- La première trame **doit** être `connect`.
- Après la négociation :
  - Requêtes : `{type:"req", id, method, params}` → `{type:"res", id, ok, payload|error}`
  - Événements : `{type:"event", event, payload, seq?, stateVersion?}`
- Si `OPENCLAW_GATEWAY_TOKEN` (ou `--token`) est défini, `connect.params.auth.token`
  doit correspondre ou le socket se ferme.
- Les clés d'idempotence sont requises pour les méthodes avec effets secondaires (`send`, `agent`) pour
  réessayer en toute sécurité ; le serveur maintient un cache de déduplication de courte durée.
- Les Nodes doivent inclure `role: "node"` plus les capacités/commandes/permissions dans `connect`.

## Appairage + confiance locale

- Tous les clients WS (opérateurs + nodes) incluent une **identité d'appareil** sur `connect`.
- Les nouveaux ID d'appareil nécessitent une approbation d'appairage ; la Gateway émet un **jeton d'appareil**
  pour les connexions ultérieures.
- Les connexions **locales** (loopback ou l'adresse tailnet propre de l'hôte de la gateway) peuvent être
  auto-approuvées pour maintenir une UX fluide sur le même hôte.
- Toutes les connexions doivent signer le nonce `connect.challenge`.
- La charge utile de signature `v3` lie également `platform` + `deviceFamily` ; la gateway
  épingle les métadonnées appairées à la reconnexion et nécessite un réappairage pour les changements de métadonnées.
- Les connexions **non-locales** nécessitent toujours une approbation explicite.
- L'authentification de la Gateway (`gateway.auth.*`) s'applique toujours à **toutes** les connexions, locales ou
  distantes.

Détails : [Protocole de la passerelle](/gateway/protocol), [Appairage](/channels/pairing),
[Sécurité](/gateway/security).

## Typage du protocole et génération de code

- Les schémas TypeBox définissent le protocole.
- JSON Schema est généré à partir de ces schémas.
- Les modèles Swift sont générés à partir de JSON Schema.

## Accès distant

- Préféré : Tailscale ou VPN.
- Alternative : Tunnel SSH

  ```bash
  ssh -N -L 18789:127.0.0.1:18789 user@host
  ```

- La même négociation + jeton d'authentification s'appliquent sur le tunnel.
- TLS + épinglage optionnel peuvent être activés pour WS dans les configurations distantes.

## Snapshot des opérations

- Démarrage : `openclaw gateway` (premier plan, journaux vers stdout).
- Santé : `health` via WS (également inclus dans `hello-ok`).
- Supervision : launchd/systemd pour redémarrage automatique.

## Invariants

- Exactement une Gateway contrôle une seule session Baileys par hôte.
- La négociation est obligatoire ; toute première trame non-JSON ou non-connect est une fermeture brutale.
- Les événements ne sont pas relus ; les clients doivent actualiser en cas de lacunes.
