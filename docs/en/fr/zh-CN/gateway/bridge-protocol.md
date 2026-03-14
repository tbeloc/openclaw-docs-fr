---
read_when:
  - Construire ou déboguer un client de nœud (mode nœud iOS/Android/macOS)
  - Enquêter sur les échecs d'appairage ou d'authentification bridge
  - Auditer les interfaces de nœud exposées par la passerelle Gateway
summary: Protocole Bridge (transport de nœud hérité) : TCP JSONL, appairage, RPC à portée
title: Protocole Bridge
x-i18n:
  generated_at: "2026-02-03T07:47:42Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 789bcf3cbc6841fc293e054b919e63d661b3cc4cd205b2094289f00800127fe2
  source_path: gateway/bridge-protocol.md
  workflow: 15
---

# Protocole Bridge (transport de nœud hérité)

Le protocole Bridge est un transport de nœud **hérité** (TCP JSONL). Les nouveaux clients de nœud doivent utiliser le protocole WebSocket unifié de la passerelle Gateway.

Si vous construisez un opérateur ou un client de nœud, veuillez utiliser le [protocole Gateway](/gateway/protocol).

**Remarque :** Les constructions actuelles d'OpenClaw n'incluent plus l'écouteur TCP bridge ; cette documentation est conservée à titre de référence historique uniquement.
Les anciennes clés de configuration `bridge.*` ne font plus partie du schéma de configuration.

## Pourquoi avons-nous deux protocoles

- **Limites de sécurité** : bridge expose une petite liste d'autorisation plutôt que l'interface API Gateway complète.
- **Appairage + identité du nœud** : l'admission des nœuds est gérée par Gateway et liée à des jetons par nœud.
- **Expérience utilisateur de découverte d'appareils** : les nœuds peuvent découvrir Gateway via Bonjour sur le réseau local, ou se connecter directement via tailnet.
- **WS Loopback** : le plan de contrôle WS complet reste local, sauf via tunnel SSH.

## Transport

- TCP, un objet JSON par ligne (JSONL).
- TLS optionnel (lorsque `bridge.tls.enabled` est true).
- Port d'écoute par défaut hérité `18790` (le bridge TCP n'est pas démarré dans les constructions actuelles).

Lorsque TLS est activé, les enregistrements TXT de découverte d'appareils contiennent `bridgeTls=1` plus `bridgeTlsSha256` afin que les nœuds puissent épingler le certificat.

## Poignée de main + appairage

1. Le client envoie un `hello` avec les métadonnées du nœud + jeton (s'il est déjà appairé).
2. S'il n'est pas appairé, Gateway répond avec une `error` (`NOT_PAIRED`/`UNAUTHORIZED`).
3. Le client envoie une `pair-request`.
4. Gateway attend l'approbation, puis envoie `pair-ok` et `hello-ok`.

`hello-ok` retourne `serverName`, pouvant inclure `canvasHostUrl`.

## Trames

Client → Gateway :

- `req` / `res` : RPC Gateway à portée (chat, sessions, config, health, voicewake, skills.bins)
- `event` : signaux de nœud (transcription vocale, demandes d'agent, abonnements de chat, cycle de vie exec)

Gateway → Client :

- `invoke` / `invoke-res` : commandes de nœud (`canvas.*`, `camera.*`, `screen.record`, `location.get`, `sms.send`)
- `event` : mises à jour de chat pour les sessions abonnées
- `ping` / `pong` : maintien de la connexion

L'application de la liste d'autorisation héritée était située dans `src/gateway/server-bridge.ts` (supprimée).

## Événements du cycle de vie Exec

Les nœuds peuvent émettre des événements `exec.finished` ou `exec.denied` pour exposer l'activité system.run.
Ceux-ci sont mappés aux événements système dans Gateway. (Les nœuds hérités peuvent toujours émettre `exec.started`.)

Champs de charge utile (optionnels sauf indication contraire) :

- `sessionKey` (obligatoire) : session d'agent recevant l'événement système.
- `runId` : identifiant exec unique pour le regroupement.
- `command` : chaîne de commande brute ou formatée.
- `exitCode`, `timedOut`, `success`, `output` : détails d'achèvement (finished uniquement).
- `reason` : raison du refus (denied uniquement).

## Utilisation de Tailnet

- Lier bridge à l'IP tailnet : définissez `bridge.bind: "tailnet"` dans `~/.openclaw/openclaw.json`.
- Les clients se connectent via le nom MagicDNS ou l'IP tailnet.
- Bonjour **ne** traverse **pas** les réseaux ; utilisez le nom d'hôte/port manuel ou DNS‑SD à large bande passante si nécessaire.

## Versioning

Bridge est actuellement **implicitement v1** (pas de négociation min/max). La compatibilité rétroactive est attendue ; ajoutez un champ de version de protocole bridge avant tout changement cassant.
