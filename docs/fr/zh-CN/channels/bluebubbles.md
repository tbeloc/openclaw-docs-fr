---
read_when:
  - Configurer le canal BlueBubbles
  - Dépanner les problèmes d'appairage webhook
  - Configurer iMessage sur macOS
summary: Utiliser iMessage via le serveur BlueBubbles macOS (envoi/réception REST, état de saisie, réactions, appairage, opérations avancées).
title: BlueBubbles
x-i18n:
  generated_at: "2026-02-03T10:04:52Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 3aae277a8bec479800a7f6268bfbca912c65a4aadc6e513694057fb873597b69
  source_path: channels/bluebubbles.md
  workflow: 15
---

# BlueBubbles (macOS REST)

Statut : Plugin intégré qui communique avec le serveur BlueBubbles macOS via HTTP. **Recommandé pour l'intégration iMessage** en raison de son API plus riche et de sa configuration plus simple, par rapport au canal imsg hérité.

## Aperçu

- S'exécute via l'application auxiliaire BlueBubbles sur macOS ([bluebubbles.app](https://bluebubbles.app)).
- Version recommandée/testée : macOS Sequoia (15). macOS Tahoe (26) est disponible ; cependant, la fonctionnalité d'édition n'est actuellement pas disponible sur Tahoe, et les mises à jour d'icônes de groupe peuvent afficher un succès mais ne pas se synchroniser réellement.
- OpenClaw communique via son API REST (`GET /api/v1/ping`, `POST /message/text`, `POST /chat/:id/*`).
- Les messages entrants arrivent via webhook ; les réponses sortantes, les indicateurs de saisie, les accusés de lecture et les tapback sont tous des appels REST.
- Les pièces jointes et autocollants sont reçus en tant que médias entrants (et présentés à l'agent si possible).
- L'appairage/liste blanche fonctionne comme pour les autres canaux (`/channels/pairing` etc.), en utilisant `channels.bluebubbles.allowFrom` + code d'appairage.
- Les réactions sont présentées comme des événements système, similaires à Slack/Telegram, et l'agent peut les « mentionner » avant de répondre.
- Fonctionnalités avancées : édition, révocation, threads de réponse, effets de message, gestion de groupe.

## Démarrage rapide

1. Installez le serveur BlueBubbles sur votre Mac (suivez les instructions sur [bluebubbles.app/install](https://bluebubbles.app/install)).
2. Dans la configuration BlueBubbles, activez l'API web et définissez un mot de passe.
3. Exécutez `openclaw onboard` et sélectionnez BlueBubbles, ou configurez manuellement :
   ```json5
   {
     channels: {
       bluebubbles: {
         enabled: true,
         serverUrl: "http://192.168.1.100:1234",
         password: "example-password",
         webhookPath: "/bluebubbles-webhook",
       },
     },
   }
   ```
4. Pointez le webhook BlueBubbles vers votre passerelle Gateway (exemple : `https://your-gateway-host:3000/bluebubbles-webhook?password=<password>`).
5. Démarrez la passerelle Gateway ; elle enregistrera le gestionnaire webhook et commencera l'appairage.

## Onboarding

BlueBubbles est disponible dans l'assistant de configuration interactif :

```
openclaw onboard
```

L'assistant vous demandera :

- **URL du serveur** (obligatoire) : Adresse du serveur BlueBubbles (par exemple `http://192.168.1.100:1234`)
- **Mot de passe** (obligatoire) : Mot de passe API des paramètres du serveur BlueBubbles
- **Chemin du webhook** (optionnel) : Par défaut `/bluebubbles-webhook`
- **Politique de message privé** : Appairage, liste blanche, ouvert ou désactivé
- **Liste blanche** : Numéros de téléphone, adresses e-mail ou cibles de chat

Vous pouvez également ajouter BlueBubbles via CLI :

```
openclaw channels add bluebubbles --http-url http://192.168.1.100:1234 --password <password>
```

## Contrôle d'accès (messages privés + groupes)

Messages privés :

- Par défaut : `channels.bluebubbles.dmPolicy = "pairing"`.
- Les expéditeurs inconnus reçoivent un code d'appairage ; les messages sont ignorés jusqu'à approbation (le code d'appairage expire après 1 heure).
- Approbation :
  - `openclaw pairing list bluebubbles`
  - `openclaw pairing approve bluebubbles <CODE>`
- L'appairage est l'échange de jetons par défaut. Détails : [Appairage](/channels/pairing)

Groupes :

- `channels.bluebubbles.groupPolicy = open | allowlist | disabled` (par défaut : `allowlist`).
- Lorsqu'il est défini sur `allowlist`, `channels.bluebubbles.groupAllowFrom` contrôle qui peut déclencher dans les groupes.

### Mention Gating (Groupes)

BlueBubbles prend en charge le mention gating pour les chats de groupe, cohérent avec le comportement iMessage/WhatsApp :

- Utilisez `agents.list[].groupChat.mentionPatterns` (ou `messages.groupChat.mentionPatterns`) pour détecter les mentions.
- Lorsqu'un groupe a `requireMention` activé, l'agent ne répond que s'il est mentionné.
- Les commandes de contrôle des expéditeurs autorisés contournent le mention gating.

Configuration par groupe :

```json5
{
  channels: {
    bluebubbles: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15555550123"],
      groups: {
        "*": { requireMention: true }, // Défaut pour tous les groupes
        "iMessage;-;chat123": { requireMention: false }, // Remplacement pour un groupe spécifique
      },
    },
  },
}
```

### Command Gating

- Les commandes de contrôle (par exemple `/config`, `/model`) nécessitent une autorisation.
- Utilisez `allowFrom` et `groupAllowFrom` pour déterminer l'autorisation des commandes.
- Les expéditeurs autorisés peuvent exécuter des commandes de contrôle même s'ils ne sont pas mentionnés dans un groupe.

## État de saisie + Accusés de lecture

- **Indicateurs de saisie** : Envoyés automatiquement avant et pendant la génération de réponse.
- **Accusés de lecture** : Contrôlés par `channels.bluebubbles.sendReadReceipts` (par défaut : `true`).
- **Indicateurs de saisie** : OpenClaw envoie un événement de début de saisie ; BlueBubbles efface automatiquement l'état de saisie lors de l'envoi ou du délai d'expiration (l'arrêt manuel via DELETE n'est pas fiable).

```json5
{
  channels: {
    bluebubbles: {
      sendReadReceipts: false, // Désactiver les accusés de lecture
    },
  },
}
```

## Opérations avancées

BlueBubbles prend en charge les opérations de message avancées lorsqu'elles sont activées dans la configuration :

```json5
{
  channels: {
    bluebubbles: {
      actions: {
        reactions: true, // tapback (par défaut : true)
        edit: true, // Éditer les messages envoyés (macOS 13+, non disponible sur macOS 26 Tahoe)
        unsend: true, // Révoquer les messages (macOS 13+)
        reply: true, // Répondre via GUID de message pour les threads
        sendWithEffect: true, // Effets de message (slam, loud, etc.)
        renameGroup: true, // Renommer le chat de groupe
        setGroupIcon: true, // Définir l'icône/photo du groupe (instable sur macOS 26 Tahoe)
        addParticipant: true, // Ajouter un participant au groupe
        removeParticipant: true, // Supprimer un participant du groupe
        leaveGroup: true, // Quitter le chat de groupe
        sendAttachment: true, // Envoyer des pièces jointes/médias
      },
    },
  },
}
```

Opérations disponibles :

- **react** : Ajouter/supprimer une réaction tapback (`messageId`, `emoji`, `remove`)
- **edit** : Éditer un message envoyé (`messageId`, `text`)
- **unsend** : Révoquer un message (`messageId`)
- **reply** : Répondre à un message spécifique (`messageId`, `text`, `to`)
- **sendWithEffect** : Envoyer avec un effet iMessage (`text`, `to`, `effectId`)
- **renameGroup** : Renommer un chat de groupe (`chatGuid`, `displayName`)
- **setGroupIcon** : Définir l'icône/photo du groupe (`chatGuid`, `media`) — instable sur macOS 26 Tahoe (l'API peut retourner un succès mais l'icône ne se synchronise pas).
- **addParticipant** : Ajouter quelqu'un à un groupe (`chatGuid`, `address`)
- **removeParticipant** : Supprimer quelqu'un d'un groupe (`chatGuid`, `address`)
- **leaveGroup** : Quitter un chat de groupe (`chatGuid`)
- **sendAttachment** : Envoyer des médias/fichiers (`to`, `buffer`, `filename`, `asVoice`)
  - Mémos vocaux : Définissez `asVoice: true` avec un audio **MP3** ou **CAF** pour envoyer en tant que message vocal iMessage. BlueBubbles convertit MP3 en CAF lors de l'envoi de mémos vocaux.

### ID de message (format court vs complet)

OpenClaw peut afficher des ID de message *courts* (par exemple `1`, `2`) pour économiser les tokens.

- `MessageSid` / `ReplyToId` peuvent être des ID courts.
- `MessageSidFull` / `ReplyToIdFull` contiennent l'ID complet du fournisseur.
- Les ID courts sont stockés en mémoire ; ils peuvent expirer après un redémarrage ou un vidage du cache.
- Les opérations acceptent les ID courts ou complets `messageId`, mais échoueront si l'ID court n'est plus disponible.

Pour l'automatisation persistante et le stockage, utilisez l'ID complet :

- Modèles : `{{MessageSidFull}}`, `{{ReplyToIdFull}}`
- Contexte : `MessageSidFull` / `ReplyToIdFull` dans la charge utile entrante

Voir [Configuration](/gateway/configuration) pour les variables de modèle.

## Streaming par chunks

Contrôlez si les réponses sont envoyées en tant que message unique ou en streaming par chunks :

```json5
{
  channels: {
    bluebubbles: {
      blockStreaming: true, // Activer le streaming par chunks (désactivé par défaut)
    },
  },
}
```

## Médias + Limites

- Les pièces jointes entrantes sont téléchargées et stockées dans le cache multimédia.
- La limite de médias est définie via `channels.bluebubbles.mediaMaxMb` (par défaut : 8 Mo).
- Le texte sortant est divisé en chunks selon `channels.bluebubbles.textChunkLimit` (par défaut : 4000 caractères).

## Référence de configuration

Configuration complète : [Configuration](/gateway/configuration)

Options du fournisseur :

- `channels.bluebubbles.enabled` : Activer/désactiver le canal.
- `channels.bluebubbles.serverUrl` : URL de base de l'API REST BlueBubbles.
- `channels.bluebubbles.password` : Mot de passe API.
- `channels.bluebubbles.webhookPath` : Chemin du point de terminaison webhook (par défaut : `/bluebubbles-webhook`).
- `channels.bluebubbles.dmPolicy` : `pairing | allowlist | open | disabled` (par défaut : `pairing`).
- `channels.bluebubbles.allowFrom` : Liste blanche des messages privés (handles, e-mails, numéros E.164, `chat_id:*`, `chat_guid:*`).
- `channels.bluebubbles.groupPolicy` : `open | allowlist | disabled` (par défaut : `allowlist`).
- `channels.bluebubbles.groupAllowFrom` : Liste blanche des expéditeurs de groupe.
- `channels.bluebubbles.groups` : Configuration par groupe (`requireMention`, etc.).
- `channels.bluebubbles.sendReadReceipts` : Envoyer les accusés de lecture (par défaut : `true`).
- `channels.bluebubbles.blockStreaming` : Activer le streaming par chunks (par défaut : `false` ; requis pour les réponses en streaming).
- `channels.bluebubbles.textChunkLimit` : Taille des chunks sortants (caractères) (par défaut : 4000).
- `channels.bluebubbles.chunkMode` : `length` (par défaut) divise uniquement si elle dépasse `textChunkLimit` ; `newline` divise d'abord par lignes vides (limites de paragraphes) avant la division par longueur.
- `channels.bluebubbles.mediaMaxMb` : Limite de médias entrants (Mo) (par défaut : 8).
- `channels.bluebubbles.historyLimit` : Nombre maximum de messages de groupe pour le contexte (0 pour désactiver).
- `channels.bluebubbles.dmHistoryLimit` : Limite d'historique des messages privés.
- `channels.bluebubbles.actions` : Activer/désactiver des opérations spécifiques.
- `channels.bluebubbles.accounts` : Configuration multi-comptes.

Options globales connexes :

- `agents.list[].groupChat.mentionPatterns` (ou `messages.groupChat.mentionPatterns`).
- `messages.responsePrefix`.

## Adresses / Cibles de livraison

Préférez `chat_guid` pour un routage stable :

- `chat_guid:iMessage;-;+15555550123` (recommandé pour les groupes)
- `chat_id:123`
- `chat_identifier:...`
- Handle direct : `+15555550123`, `user@example.com`
  - Si le handle direct n'a pas de chat de message privé existant, OpenClaw en créera un via `POST /api/v1/chat/new`. Cela nécessite l'activation de l'API privée BlueBubbles.

## Sécurité

- Les requêtes webhook sont authentifiées en comparant les paramètres de requête `guid`/`password` ou les en-têtes avec `channels.bluebubbles.password
