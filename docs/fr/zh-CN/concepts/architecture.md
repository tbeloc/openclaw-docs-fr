---
read_when:
  - 正在开发 Gateway 网关协议、客户端或传输层
summary: WebSocket Gateway 网关架构、组件和客户端流程
title: Gateway 网关架构
x-i18n:
  generated_at: "2026-02-03T07:45:55Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: c636d5d8a5e628067432b30671466309e3d630b106d413f1708765bf2a9399a1
  source_path: concepts/architecture.md
  workflow: 15
---

# Architecture de la passerelle Gateway

Dernière mise à jour : 2026-01-22

## Aperçu

- Une seule **passerelle Gateway** longue durée possède toutes les plateformes de messagerie (WhatsApp via Baileys, Telegram via grammY, Slack, Discord, Signal, iMessage, WebChat).
- Les clients du plan de contrôle (application macOS, CLI, interface Web, automatisation) se connectent à la passerelle Gateway via **WebSocket** sur l'hôte de liaison configuré (par défaut `127.0.0.1:18789`).
- Les **nœuds** (macOS/iOS/Android/appareils sans interface) se connectent également via **WebSocket**, mais déclarent `role: node` avec des capacités/commandes explicites.
- Une passerelle Gateway par hôte ; c'est le seul endroit où une session WhatsApp est ouverte.
- L'**hôte canvas** (par défaut `18793`) fournit du HTML et A2UI modifiables par l'agent.

## Composants et flux

### Passerelle Gateway (démon)

- Maintient les connexions des fournisseurs.
- Expose une API WS typée (requêtes, réponses, événements poussés par le serveur).
- Valide les trames entrantes selon JSON Schema.
- Émet des événements tels que `agent`, `chat`, `presence`, `health`, `heartbeat`, `cron`.

### Clients (application Mac / CLI / administration Web)

- Une connexion WS par client.
- Envoie des requêtes (`health`, `status`, `send`, `agent`, `system-presence`).
- S'abonne aux événements (`tick`, `agent`, `presence`, `shutdown`).

### Nœuds (macOS / iOS / Android / appareils sans interface)

- Se connectent avec `role: node` au **même serveur WS**.
- Fournissent l'identité de l'appareil dans `connect` ; l'appairage est **basé sur l'appareil** (rôle `node`), l'approbation est stockée dans le magasin d'appairage de l'appareil.
- Exposent des commandes telles que `canvas.*`, `camera.*`, `screen.record`, `location.get`.

Détails du protocole :

- [Protocole de la passerelle Gateway](/gateway/protocol)

### WebChat

- Interface statique, utilise l'API WS de la passerelle Gateway pour récupérer l'historique des chats et envoyer des messages.
- Dans les configurations distantes, se connecte via le même tunnel SSH/Tailscale que les autres clients.

## Cycle de vie de la connexion (client unique)

```
Client                    Gateway
  |                          |
  |---- req:connect -------->|
  |<------ res (ok) ---------|   (or res error + close)
  |   (payload=hello-ok carries snapshot: presence + health)
  |                          |
  |<------ event:presence ---|
  |<------ event:tick -------|
  |                          |
  |------- req:agent ------->|
  |<------ res:agent --------|   (ack: {runId,status:"accepted"})
  |<------ event:agent ------|   (streaming)
  |<------ res:agent --------|   (final: {runId,status,summary})
  |                          |
```

## Protocole de ligne (résumé)

- Transport : WebSocket, trames texte avec charge JSON.
- La première trame **doit** être `connect`.
- Après la négociation :
  - Requête : `{type:"req", id, method, params}` → `{type:"res", id, ok, payload|error}`
  - Événement : `{type:"event", event, payload, seq?, stateVersion?}`
- Si `OPENCLAW_GATEWAY_TOKEN` (ou `--token`) est défini, `connect.params.auth.token` doit correspondre, sinon le socket se ferme.
- Les méthodes avec effets secondaires (`send`, `agent`) nécessitent une clé d'idempotence pour les tentatives sûres ; le serveur maintient un cache de déduplication à court terme.
- Les nœuds doivent inclure `role: "node"` dans `connect` ainsi que les capacités/commandes/permissions.

## Appairage + confiance locale

- Tous les clients WS (opérateurs + nœuds) incluent une **identité d'appareil** lors de `connect`.
- Les nouveaux ID d'appareil nécessitent une approbation d'appairage ; la passerelle Gateway émet un **jeton d'appareil** pour les connexions ultérieures.
- Les connexions **locales** (loopback ou adresse tailnet de l'hôte de la passerelle Gateway lui-même) peuvent être approuvées automatiquement pour maintenir une expérience utilisateur fluide sur le même hôte.
- Les connexions **non locales** doivent signer le nonce `connect.challenge` et nécessitent une approbation explicite.
- L'authentification de la passerelle Gateway (`gateway.auth.*`) s'applique toujours à **toutes** les connexions, locales ou distantes.

Détails : [Protocole de la passerelle Gateway](/gateway/protocol), [Appairage](/channels/pairing), [Sécurité](/gateway/security).

## Types de protocole et génération de code

- Les schémas TypeBox définissent le protocole.
- Les schémas JSON sont générés à partir de ces schémas.
- Les modèles Swift sont générés à partir des schémas JSON.

## Accès distant

- Recommandé : Tailscale ou VPN.
- Alternative : Tunnel SSH
  ```bash
  ssh -N -L 18789:127.0.0.1:18789 user@host
  ```
- La même négociation + jeton d'authentification s'appliquent aux connexions tunnelisées.
- TLS + épinglage de certificat optionnel peuvent être activés pour WS dans les configurations distantes.

## Snapshot opérationnel

- Démarrage : `openclaw gateway` (premier plan, journaux vers stdout).
- Vérification de santé : via WS `health` (également inclus dans `hello-ok`).
- Surveillance : utiliser launchd/systemd pour redémarrage automatique.

## Invariants

- Exactement une passerelle Gateway par hôte contrôlant une seule session Baileys.
- La négociation est obligatoire ; toute première trame non-JSON ou non-connect entraîne une fermeture brutale.
- Les événements ne sont pas rejeu ; les clients doivent actualiser en cas de lacune.
