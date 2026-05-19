---
summary: "Le support BlueBubbles a été supprimé d'OpenClaw. Utilisez le plugin iMessage fourni avec imsg pour les nouvelles configurations iMessage et les configurations migrées."
read_when:
  - You used the old BlueBubbles channel and need to move to iMessage
  - You are choosing the supported OpenClaw iMessage setup
  - You need a short explanation of the BlueBubbles removal
title: "Suppression de BlueBubbles et le chemin iMessage imsg"
---

# Suppression de BlueBubbles et le chemin iMessage imsg

OpenClaw ne fournit plus le canal BlueBubbles. Le support iMessage s'exécute désormais via le plugin `imessage` fourni, qui démarre [`imsg`](https://github.com/steipete/imsg) localement ou via un wrapper SSH et communique en JSON-RPC sur stdin/stdout.

Si votre configuration contient toujours `channels.bluebubbles`, migrez-la vers `channels.imessage`. L'URL de documentation héritée `/channels/bluebubbles` redirige vers [Coming from BlueBubbles](/fr/channels/imessage-from-bluebubbles), qui contient le tableau complet de traduction de configuration et la liste de contrôle de basculement.

## Ce qui a changé

- Il n'y a pas de serveur HTTP BlueBubbles, de route webhook, de mot de passe REST ou d'exécution du plugin BlueBubbles dans le chemin iMessage OpenClaw pris en charge.
- OpenClaw lit et surveille les Messages via `imsg` sur le Mac où Messages.app est connecté.
- L'envoi, la réception, l'historique et les médias de base utilisent les surfaces `imsg` normales et les permissions macOS.
- Les actions avancées telles que les réponses en fil, les tapbacks, l'édition, l'annulation d'envoi, les effets, les accusés de réception, les indicateurs de saisie et la gestion de groupe nécessitent `imsg launch` avec le pont API privé disponible.
- Les passerelles Linux et Windows peuvent toujours utiliser iMessage en définissant `channels.imessage.cliPath` sur un wrapper SSH qui exécute `imsg` sur le Mac connecté.

## Que faire

1. Installez et vérifiez `imsg` sur le Mac Messages :

   ```bash
   brew install steipete/tap/imsg
   imsg --version
   imsg chats --limit 3
   imsg rpc --help
   ```

2. Accordez les permissions d'accès complet au disque et d'automatisation au contexte de processus qui exécute `imsg` et OpenClaw.

3. Traduisez l'ancienne configuration :

   ```json5
   {
     channels: {
       imessage: {
         enabled: true,
         cliPath: "/opt/homebrew/bin/imsg",
         dmPolicy: "pairing",
         allowFrom: ["+15555550123"],
         groupPolicy: "allowlist",
         groupAllowFrom: ["+15555550123"],
         groups: {
           "*": { requireMention: true },
         },
         includeAttachments: true,
       },
     },
   }
   ```

4. Redémarrez la passerelle et vérifiez :

   ```bash
   openclaw channels status --probe
   ```

5. Testez les DM, les groupes, les pièces jointes et toutes les actions API privées dont vous dépendez avant de supprimer votre ancien serveur BlueBubbles.

## Notes de migration

- `channels.bluebubbles.serverUrl` et `channels.bluebubbles.password` n'ont pas d'équivalent iMessage.
- `channels.bluebubbles.allowFrom`, `groupAllowFrom`, `groups`, `includeAttachments`, les racines de pièces jointes, les limites de taille de média, le chunking et les bascules d'action ont des équivalents iMessage.
- `channels.imessage.includeAttachments` est toujours désactivé par défaut. Définissez-le explicitement si vous attendez que les photos, mémos vocaux, vidéos ou fichiers entrants atteignent l'agent.
- Avec `groupPolicy: "allowlist"`, copiez l'ancien bloc `groups`, y compris toute entrée de caractère générique `"*"`. Les listes d'autorisation des expéditeurs de groupe et le registre de groupe sont des portes séparées.
- Les liaisons ACP qui correspondaient à `channel: "bluebubbles"` doivent être modifiées en `channel: "imessage"`.
- Les anciennes clés de session BlueBubbles ne deviennent pas des clés de session iMessage. Les approbations d'appairage sont transférées par handle, mais l'historique des conversations sous les clés de session BlueBubbles ne l'est pas.

## Voir aussi

- [Coming from BlueBubbles](/fr/channels/imessage-from-bluebubbles)
- [iMessage](/fr/channels/imessage)
- [Configuration reference - iMessage](/fr/gateway/config-channels#imessage)
