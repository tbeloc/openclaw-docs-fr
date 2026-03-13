---
read_when:
  - Configurer le support de Signal
  - Déboguer l'envoi/réception de Signal
summary: Support de Signal via signal-cli (JSON-RPC + SSE), configuration et modèle de numéro
title: Signal
x-i18n:
  generated_at: "2026-02-03T07:44:15Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: ca4de8b3685017f54a959e3e2699357ab40b3e4e68574bd7fb5739e4679e7d8a
  source_path: channels/signal.md
  workflow: 15
---

# Signal (signal-cli)

Statut : Intégration CLI externe. La passerelle communique avec `signal-cli` via HTTP JSON-RPC + SSE.

## Configuration rapide (débutants)

1. Utilisez un **numéro Signal distinct** pour le bot (recommandé).
2. Installez `signal-cli` (nécessite Java).
3. Liez l'appareil du bot et démarrez le démon :
   - `signal-cli link -n "OpenClaw"`
4. Configurez OpenClaw et démarrez la passerelle.

Configuration minimale :

```json5
{
  channels: {
    signal: {
      enabled: true,
      account: "+15551234567",
      cliPath: "signal-cli",
      dmPolicy: "pairing",
      allowFrom: ["+15557654321"],
    },
  },
}
```

## Qu'est-ce que c'est

- Canal Signal via `signal-cli` (non libsignal intégré).
- Routage déterministe : les réponses reviennent toujours à Signal.
- Les messages privés partagent la session principale de l'agent ; les groupes sont isolés (`agent:<agentId>:signal:group:<groupId>`).

## Écritures de configuration

Par défaut, Signal autorise les mises à jour de configuration déclenchées par `/config set|unset` (nécessite `commands.config: true`).

Pour désactiver :

```json5
{
  channels: { signal: { configWrites: false } },
}
```

## Modèle de numéro (important)

- La passerelle se connecte à un **appareil Signal** (compte `signal-cli`).
- Si vous exécutez le bot sur votre **compte Signal personnel**, il ignore vos propres messages (protection contre les boucles).
- Pour réaliser « j'envoie un message au bot et il répond », utilisez un **numéro de bot distinct**.

## Configuration (chemin rapide)

1. Installez `signal-cli` (nécessite Java).
2. Liez le compte du bot :
   - `signal-cli link -n "OpenClaw"` puis scannez le code QR dans Signal.
3. Configurez Signal et démarrez la passerelle.

Exemple :

```json5
{
  channels: {
    signal: {
      enabled: true,
      account: "+15551234567",
      cliPath: "signal-cli",
      dmPolicy: "pairing",
      allowFrom: ["+15557654321"],
    },
  },
}
```

Support multi-comptes : utilisez `channels.signal.accounts` pour configurer chaque compte avec un `name` optionnel. Pour le mode partagé, voir [`gateway/configuration`](/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts).

## Mode démon externe (httpUrl)

Si vous souhaitez gérer `signal-cli` vous-même (démarrage à froid JVM lent, initialisation de conteneur ou CPU partagé), exécutez le démon séparément et pointez OpenClaw vers lui :

```json5
{
  channels: {
    signal: {
      httpUrl: "http://127.0.0.1:8080",
      autoStart: false,
    },
  },
}
```

Cela ignore le démarrage automatique et l'attente de démarrage interne à OpenClaw. Pour les démarrages lents lors du démarrage automatique, définissez `channels.signal.startupTimeoutMs`.

## Contrôle d'accès (messages privés + groupes)

Messages privés :

- Par défaut : `channels.signal.dmPolicy = "pairing"`.
- Les expéditeurs inconnus reçoivent un code d'appairage ; les messages sont ignorés avant approbation (le code d'appairage expire après 1 heure).
- Approuvez via :
  - `openclaw pairing list signal`
  - `openclaw pairing approve signal <CODE>`
- L'appairage est l'échange de jetons par défaut pour les messages privés Signal. Détails : [Appairage](/channels/pairing)
- Les expéditeurs avec UUID uniquement (de `sourceUuid`) sont stockés dans `channels.signal.allowFrom` comme `uuid:<id>`.

Groupes :

- `channels.signal.groupPolicy = open | allowlist | disabled`.
- Lorsqu'il est défini sur `allowlist`, `channels.signal.groupAllowFrom` contrôle qui peut déclencher dans les groupes.

## Fonctionnement (comportement)

- `signal-cli` s'exécute en tant que démon ; la passerelle lit les événements via SSE.
- Les messages entrants sont normalisés en enveloppe de canal partagée.
- Les réponses sont toujours routées vers le même numéro ou groupe.

## Médias + limites

- Le texte sortant est fragmenté par `channels.signal.textChunkLimit` (par défaut 4000).
- Fragmentation optionnelle par saut de ligne : définissez `channels.signal.chunkMode="newline"` pour diviser par lignes vides (limites de paragraphes) avant la fragmentation par longueur.
- Les pièces jointes sont supportées (base64 de `signal-cli`).
- Limite de médias par défaut : `channels.signal.mediaMaxMb` (par défaut 8).
- Utilisez `channels.signal.ignoreAttachments` pour ignorer le téléchargement de médias.
- L'historique des groupes utilise `channels.signal.historyLimit` (ou `channels.signal.accounts.*.historyLimit`), avec repli sur `messages.groupChat.historyLimit`. Définissez `0` pour désactiver (par défaut 50).

## Indicateurs de saisie + accusés de lecture

- **Indicateurs de saisie** : OpenClaw envoie des signaux de saisie via `signal-cli sendTyping` et les actualise pendant l'exécution des réponses.
- **Accusés de lecture** : Lorsque `channels.signal.sendReadReceipts` est true, OpenClaw transfère les accusés de lecture pour les messages privés autorisés.
- Signal-cli n'expose pas les accusés de lecture pour les groupes.

## Réactions emoji (outil message)

- Utilisez `message action=react` avec `channel=signal`.
- Cible : E.164 de l'expéditeur ou UUID (utilisez `uuid:<id>` de la sortie d'appairage ; UUID nu fonctionne aussi).
- `messageId` est l'horodatage Signal du message auquel vous réagissez.
- Les réactions emoji de groupe nécessitent `targetAuthor` ou `targetAuthorUuid`.

Exemples :

```
message action=react channel=signal target=uuid:123e4567-e89b-12d3-a456-426614174000 messageId=1737630212345 emoji=🔥
message action=react channel=signal target=+15551234567 messageId=1737630212345 emoji=🔥 remove=true
message action=react channel=signal target=signal:group:<groupId> targetAuthor=uuid:<sender-uuid> messageId=1737630212345 emoji=✅
```

Configuration :

- `channels.signal.actions.reactions` : activer/désactiver les réactions emoji (par défaut true).
- `channels.signal.reactionLevel` : `off | ack | minimal | extensive`.
  - `off`/`ack` désactive les réactions emoji de l'agent (l'outil message `react` génère une erreur).
  - `minimal`/`extensive` active les réactions emoji de l'agent et définit le niveau de guidance.
- Remplacement par compte : `channels.signal.accounts.<id>.actions.reactions`, `channels.signal.accounts.<id>.reactionLevel`.

## Cibles de livraison (CLI/cron)

- Messages privés : `signal:+15551234567` (ou E.164 pur).
- Messages privés UUID : `uuid:<id>` (ou UUID nu).
- Groupes : `signal:group:<groupId>`.
- Noms d'utilisateur : `username:<name>` (si votre compte Signal le supporte).

## Référence de configuration (Signal)

Configuration complète : [Configuration](/gateway/configuration)

Options du fournisseur :

- `channels.signal.enabled` : activer/désactiver le démarrage du canal.
- `channels.signal.account` : E.164 du compte du bot.
- `channels.signal.cliPath` : chemin vers `signal-cli`.
- `channels.signal.httpUrl` : URL complète du démon (remplace host/port).
- `channels.signal.httpHost`, `channels.signal.httpPort` : liaison du démon (par défaut 127.0.0.1:8080).
- `channels.signal.autoStart` : démarrage automatique du démon (par défaut true si `httpUrl` n'est pas défini).
- `channels.signal.startupTimeoutMs` : délai d'attente de démarrage (millisecondes) (max 120000).
- `channels.signal.receiveMode` : `on-start | manual`.
- `channels.signal.ignoreAttachments` : ignorer le téléchargement des pièces jointes.
- `channels.signal.ignoreStories` : ignorer les histoires du démon.
- `channels.signal.sendReadReceipts` : transférer les accusés de lecture.
- `channels.signal.dmPolicy` : `pairing | allowlist | open | disabled` (par défaut : pairing).
- `channels.signal.allowFrom` : liste blanche des messages privés (E.164 ou `uuid:<id>`). `open` nécessite `"*"`. Signal n'a pas de noms d'utilisateur ; utilisez les identifiants téléphone/UUID.
- `channels.signal.groupPolicy` : `open | allowlist | disabled` (par défaut : allowlist).
- `channels.signal.groupAllowFrom` : liste blanche des expéditeurs de groupe.
- `channels.signal.historyLimit` : nombre maximal de messages de groupe à inclure en tant que contexte (0 pour désactiver).
- `channels.signal.dmHistoryLimit` : limite d'historique des messages privés (tours utilisateur). Remplacement par utilisateur : `channels.signal.dms["<phone_or_uuid>"].historyLimit`.
- `channels.signal.textChunkLimit` : taille de fragmentation sortante (caractères).
- `channels.signal.chunkMode` : `length` (par défaut) ou `newline` pour diviser par lignes vides (limites de paragraphes) avant la fragmentation par longueur.
- `channels.signal.mediaMaxMb` : limite de médias entrants/sortants (MB).

Options globales connexes :

- `agents.list[].groupChat.mentionPatterns` (Signal ne supporte pas les mentions natives).
- `messages.groupChat.mentionPatterns` (repli global).
- `messages.responsePrefix`.
