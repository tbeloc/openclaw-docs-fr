---
summary: "Protocole Bridge (nœuds hérités) : TCP JSONL, appairage, RPC limité"
read_when:
  - Building or debugging node clients (iOS/Android/macOS node mode)
  - Investigating pairing or bridge auth failures
  - Auditing the node surface exposed by the gateway
title: "Protocole Bridge"
---

# Protocole Bridge (transport de nœud hérité)

Le protocole Bridge est un **transport de nœud hérité** (TCP JSONL). Les nouveaux clients de nœud
doivent utiliser le protocole Gateway WebSocket unifié à la place.

Si vous créez un opérateur ou un client de nœud, utilisez le
[protocole Gateway](/gateway/protocol).

**Remarque :** Les builds OpenClaw actuels ne livrent plus l'écouteur TCP bridge ; ce document est conservé à titre historique.
Les clés de configuration `bridge.*` héritées ne font plus partie du schéma de configuration.

## Pourquoi nous avons les deux

- **Limite de sécurité** : le bridge expose une petite liste d'autorisation au lieu de
  la surface API gateway complète.
- **Appairage + identité du nœud** : l'admission des nœuds est gérée par la gateway et liée
  à un jeton par nœud.
- **UX de découverte** : les nœuds peuvent découvrir les gateways via Bonjour sur LAN, ou se connecter
  directement via un tailnet.
- **WS en boucle locale** : le plan de contrôle WS complet reste local sauf s'il est tunnelisé via SSH.

## Transport

- TCP, un objet JSON par ligne (JSONL).
- TLS optionnel (quand `bridge.tls.enabled` est true).
- Le port d'écoute par défaut hérité était `18790` (les builds actuels ne démarrent pas de TCP bridge).

Quand TLS est activé, les enregistrements TXT de découverte incluent `bridgeTls=1` plus
`bridgeTlsSha256` comme indice non-secret. Notez que les enregistrements TXT Bonjour/mDNS sont
non authentifiés ; les clients ne doivent pas traiter l'empreinte annoncée comme une
épingle faisant autorité sans intention utilisateur explicite ou autre vérification hors bande.

## Poignée de main + appairage

1. Le client envoie `hello` avec les métadonnées du nœud + jeton (s'il est déjà appairé).
2. S'il n'est pas appairé, la gateway répond `error` (`NOT_PAIRED`/`UNAUTHORIZED`).
3. Le client envoie `pair-request`.
4. La gateway attend l'approbation, puis envoie `pair-ok` et `hello-ok`.

`hello-ok` retourne `serverName` et peut inclure `canvasHostUrl`.

## Trames

Client → Gateway :

- `req` / `res` : RPC limité de la gateway (chat, sessions, config, health, voicewake, skills.bins)
- `event` : signaux du nœud (transcription vocale, demande d'agent, souscription au chat, cycle de vie exec)

Gateway → Client :

- `invoke` / `invoke-res` : commandes du nœud (`canvas.*`, `camera.*`, `screen.record`,
  `location.get`, `sms.send`)
- `event` : mises à jour du chat pour les sessions souscrites
- `ping` / `pong` : maintien de la connexion

L'application de la liste d'autorisation héritée vivait dans `src/gateway/server-bridge.ts` (supprimée).

## Événements du cycle de vie exec

Les nœuds peuvent émettre des événements `exec.finished` ou `exec.denied` pour exposer l'activité system.run.
Ceux-ci sont mappés aux événements système dans la gateway. (Les nœuds hérités peuvent toujours émettre `exec.started`.)

Champs de charge utile (tous optionnels sauf indication contraire) :

- `sessionKey` (requis) : session d'agent pour recevoir l'événement système.
- `runId` : identifiant exec unique pour le regroupement.
- `command` : chaîne de commande brute ou formatée.
- `exitCode`, `timedOut`, `success`, `output` : détails d'achèvement (finished uniquement).
- `reason` : raison du refus (denied uniquement).

## Utilisation du tailnet

- Lier le bridge à une IP tailnet : `bridge.bind: "tailnet"` dans
  `~/.openclaw/openclaw.json`.
- Les clients se connectent via le nom MagicDNS ou l'IP tailnet.
- Bonjour **ne traverse pas** les réseaux ; utilisez l'hôte/port manuel ou DNS‑SD large
  quand nécessaire.

## Versioning

Bridge est actuellement **implicitement v1** (pas de négociation min/max). La compatibilité rétroactive
est attendue ; ajoutez un champ de version de protocole bridge avant tout changement cassant.
