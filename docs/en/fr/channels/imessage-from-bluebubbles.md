---
summary: "Migrez les anciennes configurations BlueBubbles vers le plugin iMessage fourni sans perdre l'appairage, les listes d'autorisation ou les liaisons de groupe."
read_when:
  - Planning a move from BlueBubbles to the bundled iMessage plugin
  - Translating BlueBubbles config keys to iMessage equivalents
  - Verifying imsg before enabling the iMessage plugin
title: "Provenant de BlueBubbles"
---

Le plugin `imessage` fourni atteint désormais la même surface d'API privée que BlueBubbles (`react`, `edit`, `unsend`, `reply`, `sendWithEffect`, gestion de groupe, pièces jointes) en pilotant [`steipete/imsg`](https://github.com/steipete/imsg) via JSON-RPC. Si vous exécutez déjà un Mac avec `imsg` installé, vous pouvez abandonner le serveur BlueBubbles et laisser le plugin communiquer directement avec Messages.app.

Le support BlueBubbles a été supprimé. OpenClaw supporte iMessage via `imsg` uniquement. Ce guide est destiné à la migration des anciennes configurations `channels.bluebubbles` vers `channels.imessage` ; il n'existe pas d'autre chemin de migration supporté.

<Note>
Pour l'annonce courte et le résumé de l'opérateur, voir [Suppression de BlueBubbles et le chemin iMessage imsg](/fr/announcements/bluebubbles-imessage).
</Note>

## Liste de contrôle de migration

Utilisez cette liste de contrôle lorsque vous connaissez déjà votre ancienne configuration BlueBubbles et que vous voulez le chemin le plus court et sûr :

1. Vérifiez `imsg` directement sur le Mac qui exécute Messages.app (`imsg chats`, `imsg history`, `imsg send`, et `imsg rpc --help`).
2. Copiez les clés de comportement de `channels.bluebubbles` vers `channels.imessage` : `dmPolicy`, `allowFrom`, `groupPolicy`, `groupAllowFrom`, `groups`, `includeAttachments`, `attachmentRoots`, `mediaMaxMb`, `textChunkLimit`, `coalesceSameSenderDms`, et `actions`.
3. Supprimez les clés de transport qui n'existent plus : `serverUrl`, `password`, les URL de webhook, et la configuration du serveur BlueBubbles.
4. Si la Gateway n'est pas exécutée sur le Mac Messages, définissez `channels.imessage.cliPath` sur un wrapper SSH et définissez `remoteHost` pour les récupérations de pièces jointes distantes.
5. Avec la Gateway arrêtée, activez `channels.imessage`, puis exécutez `openclaw channels status --probe --channel imessage`.
6. Testez un DM, un groupe autorisé, les pièces jointes si activées, et chaque action d'API privée que vous vous attendez à ce que l'agent utilise.
7. Supprimez le serveur BlueBubbles et l'ancienne configuration `channels.bluebubbles` après vérification du chemin iMessage.

## Quand cette migration a du sens

- Vous exécutez déjà `imsg` sur le même Mac (ou un accessible via SSH) où Messages.app est connecté.
- Vous voulez une pièce mobile de moins — pas de serveur BlueBubbles séparé, pas de point de terminaison REST à authentifier, pas de plomberie webhook. Un seul binaire CLI au lieu d'un serveur + application client + assistant.
- Vous êtes sur une [version macOS / `imsg` supportée](/fr/channels/imessage#requirements-and-permissions-macos) où la sonde d'API privée rapporte `available: true`.

## Ce que fait imsg

`imsg` est un CLI macOS local pour Messages. OpenClaw démarre `imsg rpc` en tant que processus enfant et communique via JSON-RPC sur stdin/stdout. Il n'y a pas de serveur HTTP, d'URL webhook, de daemon en arrière-plan, d'agent de lancement ou de port à exposer.

- Les lectures proviennent de `~/Library/Messages/chat.db` en utilisant un handle SQLite en lecture seule.
- Les messages entrants en direct proviennent de `imsg watch` / `watch.subscribe`, qui suit les événements du système de fichiers `chat.db` avec un fallback de polling.
- Les envois utilisent l'automatisation Messages.app pour les envois de texte et de fichiers normaux.
- Les actions avancées utilisent `imsg launch` pour injecter l'assistant `imsg` dans Messages.app. C'est ce qui déverrouille les accusés de réception, les indicateurs de saisie, les envois enrichis, l'édition, l'annulation, la réponse en fil, les tapbacks et la gestion de groupe.
- Les builds Linux peuvent inspecter un `chat.db` copié, mais ne peuvent pas envoyer, regarder la base de données Mac en direct ou piloter Messages.app. Pour OpenClaw iMessage, exécutez `imsg` sur le Mac connecté ou via un wrapper SSH vers ce Mac.

## Avant de commencer

1. Installez `imsg` sur le Mac qui exécute Messages.app :

   ```bash
   brew install steipete/tap/imsg
   imsg --version
   imsg chats --limit 3
   ```

   Si `imsg chats` échoue avec `unable to open database file`, une sortie vide ou `authorization denied`, accordez l'accès complet au disque au terminal, à l'éditeur, au processus Node, au service Gateway ou au processus parent SSH qui lance `imsg`, puis rouvrez ce processus parent.

2. Vérifiez les surfaces de lecture, de surveillance, d'envoi et RPC avant de modifier la configuration OpenClaw :

   ```bash
   imsg chats --limit 10 --json | jq -s
   imsg history --chat-id 42 --limit 10 --attachments --json | jq -s
   imsg watch --chat-id 42 --reactions --json
   imsg send --chat-id 42 --text "OpenClaw imsg test"
   imsg rpc --help
   ```

   Remplacez `42` par un vrai chat id de `imsg chats`. L'envoi nécessite la permission Automation pour Messages.app. Si OpenClaw s'exécutera via SSH, exécutez ces commandes via le même wrapper SSH ou contexte utilisateur qu'OpenClaw utilisera.

3. Activez le pont d'API privée lorsque vous avez besoin d'actions avancées :

   ```bash
   imsg launch
   imsg status --json
   ```

   `imsg launch` nécessite que SIP soit désactivé. L'envoi basique, l'historique et la surveillance fonctionnent sans `imsg launch` ; les actions avancées ne le font pas.

4. Après avoir ajouté une configuration `channels.imessage` activée, vérifiez le pont via OpenClaw :

   ```bash
   openclaw channels status --probe
   ```

   Vous voulez `imessage.privateApi.available: true`. S'il rapporte `false`, corrigez d'abord cela — voir [Détection de capacité](/fr/channels/imessage#private-api-actions). `channels status --probe` ne sonde que les comptes configurés et activés.

5. Créez un snapshot de votre configuration :

   ```bash
   cp ~/.openclaw/openclaw.json5 ~/.openclaw/openclaw.json5.bak
   ```

## Traduction de la configuration

iMessage et BlueBubbles partagent beaucoup de configuration au niveau des canaux. Les clés qui changent sont principalement le transport (serveur REST vs CLI local). Les clés de comportement (`dmPolicy`, `groupPolicy`, `allowFrom`, etc.) conservent la même signification.

| BlueBubbles                                                | iMessage intégré                          | Notes                                                                                                                                                                                                                                                                                                                                        |
| ---------------------------------------------------------- | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `channels.bluebubbles.enabled`                             | `channels.imessage.enabled`               | Même sémantique.                                                                                                                                                                                                                                                                                                                              |
| `channels.bluebubbles.serverUrl`                           | _(supprimé)_                               | Pas de serveur REST — le plugin lance `imsg rpc` sur stdio.                                                                                                                                                                                                                                                                                    |
| `channels.bluebubbles.password`                            | _(supprimé)_                               | Aucune authentification webhook nécessaire.                                                                                                                                                                                                                                                                                                            |
| _(implicite)_                                               | `channels.imessage.cliPath`               | Chemin vers `imsg` (par défaut `imsg`) ; utilisez un script wrapper pour SSH.                                                                                                                                                                                                                                                               |
| _(implicite)_                                               | `channels.imessage.dbPath`                | Remplacement optionnel de `chat.db` de Messages.app ; détection automatique si omis.                                                                                                                                                                                                                                                        |
| _(implicite)_                                               | `channels.imessage.remoteHost`            | `host` ou `user@host` — nécessaire uniquement si `cliPath` est un wrapper SSH et vous voulez des récupérations d'attachements SCP.                                                                                                                                                                                                                                    |
| `channels.bluebubbles.dmPolicy`                            | `channels.imessage.dmPolicy`              | Mêmes valeurs (`pairing` / `allowlist` / `open` / `disabled`).                                                                                                                                                                                                                                                                                 |
| `channels.bluebubbles.allowFrom`                           | `channels.imessage.allowFrom`             | Les approbations d'appairage sont transférées par handle, pas par token.                                                                                                                                                                                                                                                                                                        |
| `channels.bluebubbles.groupPolicy`                         | `channels.imessage.groupPolicy`           | Mêmes valeurs (`allowlist` / `open` / `disabled`).                                                                                                                                                                                                                                                                                             |
| `channels.bluebubbles.groupAllowFrom`                      | `channels.imessage.groupAllowFrom`        | Identique.                                                                                                                                                                                                                                                                                                                                        |
| `channels.bluebubbles.groups`                              | `channels.imessage.groups`                | **Copiez ceci textuellement, y compris toute entrée wildcard `groups: { "*": { ... } }`.** Les paramètres par groupe `requireMention`, `tools`, `toolsBySender` sont transférés. Avec `groupPolicy: "allowlist"`, un bloc `groups` vide ou manquant supprime silencieusement chaque message de groupe — voir « Group registry footgun » ci-dessous.                                               |
| `channels.bluebubbles.sendReadReceipts`                    | `channels.imessage.sendReadReceipts`      | Par défaut `true`. Avec le plugin intégré, ceci ne s'active que lorsque la sonde d'API privée est active.                                                                                                                                                                                                                                                    |
| `channels.bluebubbles.includeAttachments`                  | `channels.imessage.includeAttachments`    | Même forme, **désactivé par défaut**. Si vous aviez des pièces jointes qui circulaient sur BlueBubbles, vous devez réactiver ceci explicitement sur le bloc iMessage — cela ne se transfère pas implicitement, et les photos/médias entrants seront silencieusement supprimés sans ligne de log `Inbound message` jusqu'à ce que vous le fassiez.                                                             |
| `channels.bluebubbles.attachmentRoots`                     | `channels.imessage.attachmentRoots`       | Racines locales ; mêmes règles wildcard.                                                                                                                                                                                                                                                                                                            |
| _(N/A)_                                                    | `channels.imessage.remoteAttachmentRoots` | Utilisé uniquement lorsque `remoteHost` est défini pour les récupérations SCP.                                                                                                                                                                                                                                                                                                          |
| `channels.bluebubbles.mediaMaxMb`                          | `channels.imessage.mediaMaxMb`            | Par défaut 16 Mo sur iMessage (BlueBubbles par défaut était 8 Mo). Définissez explicitement si vous voulez conserver le plafond inférieur.                                                                                                                                                                                                                                  |
| `channels.bluebubbles.textChunkLimit`                      | `channels.imessage.textChunkLimit`        | Par défaut 4000 sur les deux.                                                                                                                                                                                                                                                                                                                        |
| `channels.bluebubbles.coalesceSameSenderDms`               | `channels.imessage.coalesceSameSenderDms` | Même opt-in. DM uniquement — les chats de groupe conservent une dispatch instantanée par message sur les deux canaux. Élargit le débounce entrant par défaut à 2500 ms lorsqu'il est activé sans un `messages.inbound.byChannel.imessage` explicite. Voir [documentation iMessage § Coalescing split-send DMs](/fr/channels/imessage#coalescing-split-send-dms-command--url-in-one-composition). |
| `channels.bluebubbles.enrichGroupParticipantsFromContacts` | _(N/A)_                                   | iMessage lit déjà les noms d'affichage des expéditeurs depuis `chat.db`.                                                                                                                                                                                                                                                                                                  |
| `channels.bluebubbles.actions.*`                           | `channels.imessage.actions.*`             | Bascules par action : `reactions`, `edit`, `unsend`, `reply`, `sendWithEffect`, `renameGroup`, `setGroupIcon`, `addParticipant`, `removeParticipant`, `leaveGroup`, `sendAttachment`.                                                                                                                                                          |

Les configurations multi-comptes (`channels.bluebubbles.accounts.*`) se traduisent un-à-un en `channels.imessage.accounts.*`.

## Piège du registre de groupe

Le plugin iMessage fourni exécute **deux** portes de liste blanche de groupe séparées dos à dos. Les deux doivent passer pour qu'un message de groupe atteigne l'agent :

1. **Liste blanche expéditeur / cible de chat** (`channels.imessage.groupAllowFrom`) — vérifiée par `isAllowedIMessageSender`. Correspond aux messages entrants par handle d'expéditeur, `chat_guid`, `chat_identifier`, ou `chat_id`. Même forme que BlueBubbles.
2. **Registre de groupe** (`channels.imessage.groups`) — vérifiée par `resolveChannelGroupPolicy` de `inbound-processing.ts:199`. Avec `groupPolicy: "allowlist"`, cette porte nécessite soit :
   - une entrée de caractère générique `groups: { "*": { ... } }` (définit `allowAll = true`), soit
   - une entrée explicite par `chat_id` sous `groups`.

Si la porte 1 passe mais la porte 2 échoue, le message est supprimé. Le plugin émet deux signaux de niveau `warn` pour que ce ne soit plus silencieux au niveau de journalisation par défaut :

- Un `warn` de démarrage unique par compte lorsque `groupPolicy: "allowlist"` est défini mais `channels.imessage.groups` est vide (pas de caractère générique `"*"`, pas d'entrées par `chat_id`) — déclenché avant l'arrivée de messages.
- Un `warn` unique par `chat_id` la première fois qu'un groupe spécifique est supprimé à l'exécution, nommant le chat_id et la clé exacte à ajouter à `groups` pour l'autoriser.

Les DM continuent de fonctionner car ils empruntent un chemin de code différent.

C'est le mode d'échec de migration BlueBubbles → iMessage fourni le plus courant : les opérateurs copient `groupAllowFrom` et `groupPolicy` mais ignorent le bloc `groups`, car `groups: { "*": { "requireMention": true } }` de BlueBubbles ressemble à un paramètre de mention sans rapport. C'est en fait critique pour la porte du registre.

La configuration minimale pour maintenir le flux des messages de groupe après `groupPolicy: "allowlist"` :

```json5
{
  channels: {
    imessage: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15555550123", "chat_guid:any;-;..."],
      groups: {
        "*": { requireMention: true },
      },
    },
  },
}
```

`requireMention: true` sous `*` est inoffensif quand aucun motif de mention n'est configuré : l'exécution définit `canDetectMention = false` et court-circuite la suppression de mention à `inbound-processing.ts:512`. Avec des motifs de mention configurés (`agents.list[].groupChat.mentionPatterns`), cela fonctionne comme prévu.

Si la passerelle enregistre `imessage: dropping group message from chat_id=<id>` ou la ligne de démarrage `imessage: groupPolicy="allowlist" but channels.imessage.groups is empty`, la porte 2 supprime — ajoutez le bloc `groups`.

## Étape par étape

1. Ajoutez un bloc iMessage à côté du bloc BlueBubbles existant. Gardez-le désactivé tant que la passerelle achemine toujours le trafic BlueBubbles :

   ```json5
   {
     channels: {
       bluebubbles: {
         enabled: true,
         // ... config existante ...
       },
       imessage: {
         enabled: false,
         cliPath: "/opt/homebrew/bin/imsg",
         dmPolicy: "pairing",
         allowFrom: ["+15555550123"], // copié de bluebubbles.allowFrom
         groupPolicy: "allowlist",
         groupAllowFrom: [], // copié de bluebubbles.groupAllowFrom
         groups: { "*": { requireMention: true } }, // copié de bluebubbles.groups — supprime silencieusement les groupes s'il manque, voir « Piège du registre de groupe » ci-dessus
         actions: {
           reactions: true,
           edit: true,
           unsend: true,
           reply: true,
           sendWithEffect: true,
           sendAttachment: true,
         },
       },
     },
   }
   ```

2. **Testez avant que le trafic ne compte** — arrêtez la passerelle, activez temporairement le bloc iMessage, et confirmez qu'iMessage signale un état sain depuis la CLI :

   ```bash
   openclaw gateway stop
   # éditer config : channels.imessage.enabled = true
   openclaw channels status --probe --channel imessage   # attendez imessage.privateApi.available: true
   ```

   `channels status --probe` teste uniquement les comptes configurés et activés. Ne redémarrez pas la passerelle avec BlueBubbles et iMessage activés à moins que vous ne vouliez intentionnellement que les deux moniteurs de canal s'exécutent. Si vous ne basculez pas immédiatement, définissez `channels.imessage.enabled` sur `false` avant de redémarrer la passerelle. Utilisez les commandes `imsg` directes dans [Avant de commencer](#avant-de-commencer) pour valider le Mac avant d'activer le trafic OpenClaw.

3. **Basculez.** Une fois que le compte iMessage activé signale un état sain, supprimez la config BlueBubbles et gardez iMessage activé :

   ```json5
   {
     channels: {
       imessage: { enabled: true /* ... */ },
     },
   }
   ```

   Redémarrez la passerelle. Le trafic iMessage entrant circule maintenant via le plugin fourni.

4. **Vérifiez les DM.** Envoyez un message direct à l'agent ; confirmez que la réponse arrive.

5. **Vérifiez les groupes séparément.** Les DM et les groupes empruntent des chemins de code différents — le succès des DM ne prouve pas que les groupes sont acheminés. Envoyez un message à l'agent dans un chat de groupe appairé et confirmez que la réponse arrive. Si le groupe devient silencieux (pas de réponse d'agent, pas d'erreur), vérifiez le journal de la passerelle pour `imessage: dropping group message from chat_id=<id>` ou la ligne de démarrage `imessage: groupPolicy="allowlist" but channels.imessage.groups is empty` — les deux se déclenchent au niveau de journalisation par défaut. Si l'un ou l'autre apparaît, votre bloc `groups` manque ou est vide — voir « Piège du registre de groupe » ci-dessus.

6. **Vérifiez la surface d'action** — à partir d'un DM appairé, demandez à l'agent de réagir, modifier, annuler, répondre, envoyer une photo, et (dans un groupe) renommer le groupe / ajouter ou supprimer un participant. Chaque action doit arriver nativement dans Messages.app. Si l'une d'elles lève « iMessage `<action>` requires the imsg private API bridge », exécutez `imsg launch` à nouveau et actualisez `channels status --probe`.

7. **Supprimez le serveur et la config BlueBubbles** une fois que les DM iMessage, les groupes et les actions sont vérifiés. OpenClaw n'utilisera pas `channels.bluebubbles`.

## Parité d'action en un coup d'œil

| Action                                                     | BlueBubbles hérité                  | iMessage fourni                                                                                                        |
| ---------------------------------------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Envoyer du texte / secours SMS                             | ✅                                  | ✅                                                                                                                      |
| Envoyer des médias (photo, vidéo, fichier, voix)           | ✅                                  | ✅                                                                                                                      |
| Réponse filetée (`reply_to_guid`)                          | ✅                                  | ✅ (ferme [#51892](https://github.com/openclaw/openclaw/issues/51892))                                                 |
| Tapback (`react`)                                          | ✅                                  | ✅                                                                                                                      |
| Modifier / annuler (destinataires macOS 13+)               | ✅                                  | ✅                                                                                                                      |
| Envoyer avec effet d'écran                                 | ✅                                  | ✅ (ferme une partie de [#9394](https://github.com/openclaw/openclaw/issues/9394))                                           |
| Texte riche gras / italique / souligné / barré             | ✅                                  | ✅ (formatage typed-run via attributedBody)                                                                            |
| Renommer le groupe / définir l'icône du groupe             | ✅                                  | ✅                                                                                                                      |
| Ajouter / supprimer un participant, quitter le groupe      | ✅                                  | ✅                                                                                                                      |
| Accusés de réception et indicateur de saisie               | ✅                                  | ✅ (conditionné par sonde d'API privée)                                                                                         |
| Coalescence DM du même expéditeur                          | ✅                                  | ✅ (DM uniquement ; opt-in via `channels.imessage.coalesceSameSenderDms`)                                                      |
| Rattrapage des messages entrants reçus pendant l'arrêt de la passerelle | ✅ (relecture webhook + récupération d'historique) | ✅ (opt-in via `channels.imessage.catchup.enabled`; ferme [#78649](https://github.com/openclaw/openclaw/issues/78649)) |

Le rattrapage iMessage est maintenant disponible en tant que fonctionnalité opt-in sur le plugin fourni. Au démarrage de la passerelle, si `channels.imessage.catchup.enabled` est `true`, la passerelle exécute un passage `chats.list` + `messages.history` par chat contre le même client JSON-RPC utilisé par `imsg watch`, relit chaque ligne entrante manquée via le chemin de dispatch en direct (listes blanches, politique de groupe, déboucleur, cache d'écho), et persiste un curseur par compte pour que les démarrages ultérieurs reprennent là où ils se sont arrêtés. Voir [Rattrapage après un arrêt de la passerelle](/fr/channels/imessage#rattrapage-après-un-arrêt-de-la-passerelle) pour l'ajustement.

## Appairage, sessions et liaisons ACP

- **Les approbations d'appairage** sont transférées par handle. Vous n'avez pas besoin de réapprouver les expéditeurs connus — `channels.imessage.allowFrom` reconnaît les mêmes chaînes `+15555550123` / `user@example.com` que BlueBubbles utilisait.
- **Les sessions** restent limitées par agent + chat. Les DM s'effondrent dans la session principale de l'agent sous `session.dmScope=main` par défaut ; les sessions de groupe restent isolées par `chat_id`. Les clés de session diffèrent (`agent:<id>:imessage:group:<chat_id>` par rapport à l'équivalent BlueBubbles) — l'ancien historique de conversation sous les clés de session BlueBubbles ne se transfère pas dans les sessions iMessage.
- **Les liaisons ACP** référençant `match.channel: "bluebubbles"` doivent être mises à jour vers `"imessage"`. Les formes `match.peer.id` (`chat_id:`, `chat_guid:`, `chat_identifier:`, handle nu) sont identiques.

## Pas de canal de retour

Il n'y a pas de runtime BlueBubbles pris en charge pour revenir. Si la vérification iMessage échoue, définissez `channels.imessage.enabled: false`, redémarrez la passerelle, corrigez le bloqueur `imsg`, et réessayez le basculement.

Le cache de réponse se trouve à `~/.openclaw/state/imessage/reply-cache.jsonl` (mode `0600`, répertoire parent `0700`). Il est sûr de supprimer si vous voulez une ardoise vierge.

## Connexes

- [Suppression de BlueBubbles et le chemin iMessage imsg](/fr/announcements/bluebubbles-imessage) — annonce courte et résumé de l'opérateur.
- [iMessage](/fr/channels/imessage) — référence complète du canal iMessage, y compris la configuration `imsg launch` et la détection de capacité.
- `/channels/bluebubbles` — URL héritée qui redirige vers ce guide de migration.
- [Appairage](/fr/channels/pairing) — authentification DM et flux d'appairage.
- [Routage des canaux](/fr/channels/channel-routing) — comment la passerelle choisit un canal pour les réponses sortantes.
