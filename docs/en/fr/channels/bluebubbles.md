---
summary: "iMessage via BlueBubbles macOS server (REST send/receive, typing, reactions, pairing, advanced actions)."
read_when:
  - Setting up BlueBubbles channel
  - Troubleshooting webhook pairing
  - Configuring iMessage on macOS
title: "BlueBubbles"
---

# BlueBubbles (macOS REST)

Statut : plugin fourni qui communique avec le serveur BlueBubbles macOS via HTTP. **Recommandé pour l'intégration iMessage** en raison de son API plus riche et de sa configuration plus facile par rapport au canal imsg hérité.

## Aperçu

- S'exécute sur macOS via l'application d'assistance BlueBubbles ([bluebubbles.app](https://bluebubbles.app)).
- Recommandé/testé : macOS Sequoia (15). macOS Tahoe (26) fonctionne ; l'édition est actuellement cassée sur Tahoe, et les mises à jour d'icônes de groupe peuvent signaler le succès mais ne pas se synchroniser.
- OpenClaw communique avec lui via son API REST (`GET /api/v1/ping`, `POST /message/text`, `POST /chat/:id/*`).
- Les messages entrants arrivent via des webhooks ; les réponses sortantes, les indicateurs de saisie, les accusés de réception et les tapbacks sont des appels REST.
- Les pièces jointes et les autocollants sont ingérés en tant que médias entrants (et présentés à l'agent si possible).
- L'appairage/liste d'autorisation fonctionne de la même manière que les autres canaux (`/channels/pairing` etc) avec `channels.bluebubbles.allowFrom` + codes d'appairage.
- Les réactions sont présentées comme des événements système tout comme Slack/Telegram afin que les agents puissent les « mentionner » avant de répondre.
- Fonctionnalités avancées : édition, annulation d'envoi, threading de réponses, effets de message, gestion de groupe.

## Démarrage rapide

1. Installez le serveur BlueBubbles sur votre Mac (suivez les instructions sur [bluebubbles.app/install](https://bluebubbles.app/install)).
2. Dans la configuration BlueBubbles, activez l'API Web et définissez un mot de passe.
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

4. Pointez les webhooks BlueBubbles vers votre passerelle (exemple : `https://your-gateway-host:3000/bluebubbles-webhook?password=<password>`).
5. Démarrez la passerelle ; elle enregistrera le gestionnaire de webhook et commencera l'appairage.

Note de sécurité :

- Définissez toujours un mot de passe webhook.
- L'authentification webhook est toujours requise. OpenClaw rejette les demandes de webhook BlueBubbles à moins qu'elles n'incluent un mot de passe/guid correspondant à `channels.bluebubbles.password` (par exemple `?password=<password>` ou `x-password`), indépendamment de la topologie de boucle locale/proxy.
- L'authentification par mot de passe est vérifiée avant de lire/analyser les corps de webhook complets.

## Garder Messages.app actif (VM / configurations sans interface)

Certaines configurations de VM macOS / toujours actives peuvent finir par avoir Messages.app qui devient « inactif » (les événements entrants s'arrêtent jusqu'à ce que l'application soit ouverte/mise au premier plan). Une solution simple est de **stimuler Messages toutes les 5 minutes** en utilisant AppleScript + LaunchAgent.

### 1) Enregistrez l'AppleScript

Enregistrez ceci comme :

- `~/Scripts/poke-messages.scpt`

Exemple de script (non interactif ; ne vole pas le focus) :

```applescript
try
  tell application "Messages"
    if not running then
      launch
    end if

    -- Touch the scripting interface to keep the process responsive.
    set _chatCount to (count of chats)
  end tell
on error
  -- Ignore transient failures (first-run prompts, locked session, etc).
end try
```

### 2) Installez un LaunchAgent

Enregistrez ceci comme :

- `~/Library/LaunchAgents/com.user.poke-messages.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.user.poke-messages</string>

    <key>ProgramArguments</key>
    <array>
      <string>/bin/bash</string>
      <string>-lc</string>
      <string>/usr/bin/osascript &quot;$HOME/Scripts/poke-messages.scpt&quot;</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>StartInterval</key>
    <integer>300</integer>

    <key>StandardOutPath</key>
    <string>/tmp/poke-messages.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/poke-messages.err</string>
  </dict>
</plist>
```

Notes :

- Ceci s'exécute **toutes les 300 secondes** et **à la connexion**.
- La première exécution peut déclencher des invites macOS **Automation** (`osascript` → Messages). Approuvez-les dans la même session utilisateur qui exécute le LaunchAgent.

Chargez-le :

```bash
launchctl unload ~/Library/LaunchAgents/com.user.poke-messages.plist 2>/dev/null || true
launchctl load ~/Library/LaunchAgents/com.user.poke-messages.plist
```

## Intégration

BlueBubbles est disponible dans l'assistant de configuration interactif :

```
openclaw onboard
```

L'assistant demande :

- **Server URL** (obligatoire) : adresse du serveur BlueBubbles (par exemple, `http://192.168.1.100:1234`)
- **Password** (obligatoire) : mot de passe API des paramètres du serveur BlueBubbles
- **Webhook path** (optionnel) : par défaut `/bluebubbles-webhook`
- **DM policy** : pairing, allowlist, open, ou disabled
- **Allow list** : numéros de téléphone, e-mails ou cibles de chat

Vous pouvez également ajouter BlueBubbles via CLI :

```
openclaw channels add bluebubbles --http-url http://192.168.1.100:1234 --password <password>
```

## Contrôle d'accès (DMs + groupes)

DMs :

- Par défaut : `channels.bluebubbles.dmPolicy = "pairing"`.
- Les expéditeurs inconnus reçoivent un code d'appairage ; les messages sont ignorés jusqu'à approbation (les codes expirent après 1 heure).
- Approuvez via :
  - `openclaw pairing list bluebubbles`
  - `openclaw pairing approve bluebubbles <CODE>`
- L'appairage est l'échange de jetons par défaut. Détails : [Pairing](/channels/pairing)

Groupes :

- `channels.bluebubbles.groupPolicy = open | allowlist | disabled` (par défaut : `allowlist`).
- `channels.bluebubbles.groupAllowFrom` contrôle qui peut déclencher dans les groupes lorsque `allowlist` est défini.

### Mention gating (groupes)

BlueBubbles prend en charge le mention gating pour les chats de groupe, correspondant au comportement iMessage/WhatsApp :

- Utilise `agents.list[].groupChat.mentionPatterns` (ou `messages.groupChat.mentionPatterns`) pour détecter les mentions.
- Lorsque `requireMention` est activé pour un groupe, l'agent ne répond que lorsqu'il est mentionné.
- Les commandes de contrôle des expéditeurs autorisés contournent le mention gating.

Configuration par groupe :

```json5
{
  channels: {
    bluebubbles: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15555550123"],
      groups: {
        "*": { requireMention: true }, // default for all groups
        "iMessage;-;chat123": { requireMention: false }, // override for specific group
      },
    },
  },
}
```

### Command gating

- Les commandes de contrôle (par exemple, `/config`, `/model`) nécessitent une autorisation.
- Utilise `allowFrom` et `groupAllowFrom` pour déterminer l'autorisation des commandes.
- Les expéditeurs autorisés peuvent exécuter des commandes de contrôle même sans mentionner dans les groupes.

## Indicateurs de saisie + accusés de réception

- **Indicateurs de saisie** : Envoyés automatiquement avant et pendant la génération de réponse.
- **Accusés de réception** : Contrôlés par `channels.bluebubbles.sendReadReceipts` (par défaut : `true`).
- **Indicateurs de saisie** : OpenClaw envoie des événements de début de saisie ; BlueBubbles efface automatiquement la saisie à l'envoi ou au délai d'expiration (l'arrêt manuel via DELETE n'est pas fiable).

```json5
{
  channels: {
    bluebubbles: {
      sendReadReceipts: false, // disable read receipts
    },
  },
}
```

## Actions avancées

BlueBubbles prend en charge les actions de message avancées lorsqu'elles sont activées dans la configuration :

```json5
{
  channels: {
    bluebubbles: {
      actions: {
        reactions: true, // tapbacks (default: true)
        edit: true, // edit sent messages (macOS 13+, broken on macOS 26 Tahoe)
        unsend: true, // unsend messages (macOS 13+)
        reply: true, // reply threading by message GUID
        sendWithEffect: true, // message effects (slam, loud, etc.)
        renameGroup: true, // rename group chats
        setGroupIcon: true, // set group chat icon/photo (flaky on macOS 26 Tahoe)
        addParticipant: true, // add participants to groups
        removeParticipant: true, // remove participants from groups
        leaveGroup: true, // leave group chats
        sendAttachment: true, // send attachments/media
      },
    },
  },
}
```

Actions disponibles :

- **react** : Ajouter/supprimer des réactions tapback (`messageId`, `emoji`, `remove`)
- **edit** : Éditer un message envoyé (`messageId`, `text`)
- **unsend** : Annuler l'envoi d'un message (`messageId`)
- **reply** : Répondre à un message spécifique (`messageId`, `text`, `to`)
- **sendWithEffect** : Envoyer avec effet iMessage (`text`, `to`, `effectId`)
- **renameGroup** : Renommer un chat de groupe (`chatGuid`, `displayName`)
- **setGroupIcon** : Définir l'icône/photo d'un chat de groupe (`chatGuid`, `media`) — instable sur macOS 26 Tahoe (l'API peut signaler le succès mais l'icône ne se synchronise pas).
- **addParticipant** : Ajouter quelqu'un à un groupe (`chatGuid`, `address`)
- **removeParticipant** : Supprimer quelqu'un d'un groupe (`chatGuid`, `address`)
- **leaveGroup** : Quitter un chat de groupe (`chatGuid`)
- **sendAttachment** : Envoyer des médias/fichiers (`to`, `buffer`, `filename`, `asVoice`)
  - Messages vocaux : définissez `asVoice: true` avec audio **MP3** ou **CAF** pour envoyer en tant que message vocal iMessage. BlueBubbles convertit MP3 → CAF lors de l'envoi de messages vocaux.

### IDs de message (court vs complet)

OpenClaw peut afficher des _courts_ IDs de message (par exemple, `1`, `2`) pour économiser les jetons.

- `MessageSid` / `ReplyToId` peuvent être des IDs courts.
- `MessageSidFull` / `ReplyToIdFull` contiennent les IDs complets du fournisseur.
- Les IDs courts sont en mémoire ; ils peuvent expirer au redémarrage ou à l'éviction du cache.
- Les actions acceptent les `messageId` courts ou complets, mais les IDs courts généreront une erreur s'ils ne sont plus disponibles.

Utilisez les IDs complets pour les automations et le stockage durables :

- Modèles : `{{MessageSidFull}}`, `{{ReplyToIdFull}}`
- Contexte : `MessageSidFull` / `ReplyToIdFull` dans les charges utiles entrantes

Voir [Configuration](/gateway/configuration) pour les variables de modèle.

## Block streaming

Contrôlez si les réponses sont envoyées en tant que message unique ou diffusées en blocs :

```json5
{
  channels: {
    bluebubbles: {
      blockStreaming: true, // enable block streaming (off by default)
    },
  },
}
```

## Médias + limites

- Les pièces jointes entrantes sont téléchargées et stockées dans le cache multimédia.
- Limite de médias via `channels.bluebubbles.mediaMaxMb` pour les médias entrants et sortants (par défaut : 8 MB).
- Le texte sortant est divisé en `channels.bluebubbles.textChunkLimit` (par défaut : 4000 caractères).

## Référence de configuration

Configuration complète : [Configuration](/gateway/configuration)

Options du fournisseur :

- `channels.bluebubbles.enabled` : Activer/désactiver le canal.
- `channels.bluebubbles.serverUrl` : URL de base de l'API REST BlueBubbles.
- `channels.bluebubbles.password` : Mot de passe de l'API.
- `channels.bluebubbles.webhookPath` : Chemin du point de terminaison webhook (par défaut : `/bluebubbles-webhook`).
- `channels.bluebubbles.dmPolicy` : `pairing | allowlist | open | disabled` (par défaut : `pairing`).
- `channels.bluebubbles.allowFrom` : Liste blanche des DM (identifiants, e-mails, numéros E.164, `chat_id:*`, `chat_guid:*`).
- `channels.bluebubbles.groupPolicy` : `open | allowlist | disabled` (par défaut : `allowlist`).
- `channels.bluebubbles.groupAllowFrom` : Liste blanche des expéditeurs de groupe.
- `channels.bluebubbles.groups` : Configuration par groupe (`requireMention`, etc.).
- `channels.bluebubbles.sendReadReceipts` : Envoyer les accusés de lecture (par défaut : `true`).
- `channels.bluebubbles.blockStreaming` : Activer le streaming par bloc (par défaut : `false` ; requis pour les réponses en streaming).
- `channels.bluebubbles.textChunkLimit` : Taille des blocs sortants en caractères (par défaut : 4000).
- `channels.bluebubbles.chunkMode` : `length` (par défaut) divise uniquement en cas de dépassement de `textChunkLimit` ; `newline` divise sur les lignes vides (limites de paragraphes) avant la division par longueur.
- `channels.bluebubbles.mediaMaxMb` : Limite des médias entrants/sortants en MB (par défaut : 8).
- `channels.bluebubbles.mediaLocalRoots` : Liste blanche explicite des répertoires locaux absolus autorisés pour les chemins de médias locaux sortants. Les envois de chemins locaux sont refusés par défaut sauf si ceci est configuré. Remplacement par compte : `channels.bluebubbles.accounts.<accountId>.mediaLocalRoots`.
- `channels.bluebubbles.historyLimit` : Nombre maximum de messages de groupe pour le contexte (0 désactive).
- `channels.bluebubbles.dmHistoryLimit` : Limite de l'historique des DM.
- `channels.bluebubbles.actions` : Activer/désactiver des actions spécifiques.
- `channels.bluebubbles.accounts` : Configuration multi-compte.

Options globales associées :

- `agents.list[].groupChat.mentionPatterns` (ou `messages.groupChat.mentionPatterns`).
- `messages.responsePrefix`.

## Adressage / cibles de livraison

Préférez `chat_guid` pour un routage stable :

- `chat_guid:iMessage;-;+15555550123` (préféré pour les groupes)
- `chat_id:123`
- `chat_identifier:...`
- Identifiants directs : `+15555550123`, `user@example.com`
  - Si un identifiant direct n'a pas de chat DM existant, OpenClaw en créera un via `POST /api/v1/chat/new`. Cela nécessite que l'API privée BlueBubbles soit activée.

## Sécurité

- Les requêtes webhook sont authentifiées en comparant les paramètres de requête `guid`/`password` ou les en-têtes par rapport à `channels.bluebubbles.password`. Les requêtes provenant de `localhost` sont également acceptées.
- Gardez le mot de passe de l'API et le point de terminaison webhook secrets (traitez-les comme des identifiants).
- La confiance localhost signifie qu'un proxy inverse sur le même hôte peut contourner involontairement le mot de passe. Si vous proxifiez la passerelle, exigez une authentification au niveau du proxy et configurez `gateway.trustedProxies`. Voir [Sécurité de la passerelle](/gateway/security#reverse-proxy-configuration).
- Activez HTTPS + les règles de pare-feu sur le serveur BlueBubbles si vous l'exposez en dehors de votre LAN.

## Dépannage

- Si les événements de saisie/lecture cessent de fonctionner, vérifiez les journaux webhook BlueBubbles et assurez-vous que le chemin de la passerelle correspond à `channels.bluebubbles.webhookPath`.
- Les codes d'appairage expirent après une heure ; utilisez `openclaw pairing list bluebubbles` et `openclaw pairing approve bluebubbles <code>`.
- Les réactions nécessitent l'API privée BlueBubbles (`POST /api/v1/message/react`) ; assurez-vous que la version du serveur l'expose.
- La modification/l'annulation d'envoi nécessitent macOS 13+ et une version compatible du serveur BlueBubbles. Sur macOS 26 (Tahoe), la modification est actuellement cassée en raison de changements d'API privée.
- Les mises à jour d'icônes de groupe peuvent être instables sur macOS 26 (Tahoe) : l'API peut retourner un succès mais la nouvelle icône ne se synchronise pas.
- OpenClaw masque automatiquement les actions connues comme cassées en fonction de la version macOS du serveur BlueBubbles. Si la modification apparaît toujours sur macOS 26 (Tahoe), désactivez-la manuellement avec `channels.bluebubbles.actions.edit=false`.
- Pour les informations de statut/santé : `openclaw status --all` ou `openclaw status --deep`.

Pour une référence générale du flux de travail des canaux, voir [Canaux](/channels) et le guide [Plugins](/tools/plugin).
