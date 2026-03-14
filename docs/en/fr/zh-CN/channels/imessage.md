---
read_when:
  - Configurer le support iMessage
  - Déboguer l'envoi/réception iMessage
summary: Implémentation du support iMessage, configuration et routage chat_id via imsg (JSON-RPC basé sur stdio)
title: iMessage
x-i18n:
  generated_at: "2026-02-03T07:44:18Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: bc19756a42ead80a0845f18c4830c3f1f40948f69b2b016a4026598cfb8fef0d
  source_path: channels/imessage.md
  workflow: 15
---

# iMessage (imsg)

Statut : Intégration CLI externe. La passerelle génère `imsg rpc` (JSON-RPC basé sur stdio).

## Configuration rapide (débutants)

1. Assurez-vous d'être connecté à Messages sur ce Mac.
2. Installez `imsg` :
   - `brew install steipete/tap/imsg`
3. Configurez `channels.imessage.cliPath` et `channels.imessage.dbPath` pour OpenClaw.
4. Démarrez la passerelle et approuvez toutes les invites macOS (Automatisation + Accès disque complet).

Configuration minimale :

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "/usr/local/bin/imsg",
      dbPath: "/Users/<you>/Library/Messages/chat.db",
    },
  },
}
```

## Présentation

- Canal iMessage basé sur `imsg` sur macOS.
- Routage déterministe : les réponses reviennent toujours à iMessage.
- Les messages privés partagent la session principale de l'agent ; les groupes sont isolés (`agent:<agentId>:imessage:group:<chat_id>`).
- Si une session multi-participants arrive avec `is_group=false`, vous pouvez toujours l'isoler par `chat_id` en utilisant `channels.imessage.groups` (voir "Sessions de type groupe" ci-dessous).

## Écritures de configuration

Par défaut, iMessage autorise les mises à jour de configuration déclenchées par `/config set|unset` (nécessite `commands.config: true`).

Pour désactiver :

```json5
{
  channels: { imessage: { configWrites: false } },
}
```

## Exigences

- macOS avec Messages connecté.
- Accès disque complet pour OpenClaw + `imsg` (pour accéder à la base de données Messages).
- Permissions d'automatisation requises pour l'envoi.
- `channels.imessage.cliPath` peut pointer vers n'importe quelle commande qui proxie stdin/stdout (par exemple, un script wrapper qui se connecte via SSH à un autre Mac et exécute `imsg rpc`).

## Configuration (chemin rapide)

1. Assurez-vous d'être connecté à Messages sur ce Mac.
2. Configurez iMessage et démarrez la passerelle.

### Utilisateur macOS bot dédié (pour une identité isolée)

Si vous souhaitez que le bot envoie depuis une **identité iMessage indépendante** (et garder votre Messages personnel propre), utilisez un Apple ID dédié + un utilisateur macOS dédié.

1. Créez un Apple ID dédié (par exemple : `my-cool-bot@icloud.com`).
   - Apple peut nécessiter un numéro de téléphone pour la vérification / 2FA.
2. Créez un utilisateur macOS (par exemple : `openclawhome`) et connectez-vous.
3. Ouvrez Messages dans cet utilisateur macOS et connectez-vous à iMessage avec l'Apple ID du bot.
4. Activez la connexion à distance (Paramètres système → Général → Partage → Connexion à distance).
5. Installez `imsg` :
   - `brew install steipete/tap/imsg`
6. Configurez SSH pour que `ssh <bot-macos-user>@localhost true` fonctionne sans mot de passe.
7. Pointez `channels.imessage.accounts.bot.cliPath` vers un script wrapper SSH qui exécute `imsg` en tant qu'utilisateur bot.

Note sur la première exécution : l'envoi/réception peut nécessiter une approbation GUI dans l'*utilisateur macOS bot* (Automatisation + Accès disque complet). Si `imsg rpc` semble bloqué ou se ferme, connectez-vous à cet utilisateur (le partage d'écran est utile), exécutez une fois `imsg chats --limit 1` / `imsg send ...`, approuvez les invites, puis réessayez.

Exemple de script wrapper (`chmod +x`). Remplacez `<bot-macos-user>` par votre nom d'utilisateur macOS réel :

```bash
#!/usr/bin/env bash
set -euo pipefail

# Run an interactive SSH once first to accept host keys:
#   ssh <bot-macos-user>@localhost true
exec /usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=5 -T <bot-macos-user>@localhost \
  "/usr/local/bin/imsg" "$@"
```

Exemple de configuration :

```json5
{
  channels: {
    imessage: {
      enabled: true,
      accounts: {
        bot: {
          name: "Bot",
          enabled: true,
          cliPath: "/path/to/imsg-bot",
          dbPath: "/Users/<bot-macos-user>/Library/Messages/chat.db",
        },
      },
    },
  },
}
```

Pour une configuration à compte unique, utilisez les options plates (`channels.imessage.cliPath`, `channels.imessage.dbPath`) au lieu de la carte `accounts`.

### Variante distante/SSH (optionnel)

Si vous souhaitez utiliser iMessage sur un autre Mac, définissez `channels.imessage.cliPath` sur un script wrapper qui exécute `imsg` sur l'hôte macOS distant via SSH. OpenClaw n'a besoin que de stdio.

Exemple de script wrapper :

```bash
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"
```

**Pièces jointes distantes :** Lorsque `cliPath` pointe vers un hôte distant via SSH, les chemins des pièces jointes dans la base de données Messages font référence à des fichiers sur la machine distante. OpenClaw peut récupérer automatiquement ces fichiers via SCP en définissant `channels.imessage.remoteHost` :

```json5
{
  channels: {
    imessage: {
      cliPath: "~/imsg-ssh", // SSH wrapper to remote Mac
      remoteHost: "user@gateway-host", // for SCP file transfer
      includeAttachments: true,
    },
  },
}
```

Si `remoteHost` n'est pas défini, OpenClaw tentera de détecter automatiquement en analysant la commande SSH dans le script wrapper. Il est recommandé de configurer explicitement pour une meilleure fiabilité.

#### Connexion à un Mac distant via Tailscale (exemple)

Si la passerelle s'exécute sur un hôte Linux/VM mais iMessage doit s'exécuter sur un Mac, Tailscale est le moyen le plus simple de créer un pont : la passerelle communique avec le Mac via le tailnet, exécute `imsg` via SSH et récupère les pièces jointes via SCP.

Architecture :

```
┌──────────────────────────────┐          SSH (imsg rpc)          ┌──────────────────────────┐
│ Gateway host (Linux/VM)      │──────────────────────────────────▶│ Mac with Messages + imsg │
│ - openclaw gateway           │          SCP (attachments)        │ - Messages signed in     │
│ - channels.imessage.cliPath  │◀──────────────────────────────────│ - Remote Login enabled   │
└──────────────────────────────┘                                   └──────────────────────────┘
              ▲
              │ Tailscale tailnet (hostname or 100.x.y.z)
              ▼
        user@gateway-host
```

Exemple de configuration spécifique (nom d'hôte Tailscale) :

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "~/.openclaw/scripts/imsg-ssh",
      remoteHost: "bot@mac-mini.tailnet-1234.ts.net",
      includeAttachments: true,
      dbPath: "/Users/bot/Library/Messages/chat.db",
    },
  },
}
```

Exemple de script wrapper (`~/.openclaw/scripts/imsg-ssh`) :

```bash
#!/usr/bin/env bash
exec ssh -T bot@mac-mini.tailnet-1234.ts.net imsg "$@"
```

Remarques :

- Assurez-vous que le Mac est connecté à Messages et que la connexion à distance est activée.
- Utilisez des clés SSH pour que `ssh bot@mac-mini.tailnet-1234.ts.net` fonctionne sans invite.
- `remoteHost` doit correspondre à la cible SSH pour que SCP puisse récupérer les pièces jointes.

Support multi-comptes : Utilisez `channels.imessage.accounts` pour configurer chaque compte avec un `name` optionnel. Voir [`gateway/configuration`](/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) pour les modèles partagés. Ne soumettez pas `~/.openclaw/openclaw.json` (il contient généralement des jetons).

## Contrôle d'accès (messages privés + groupes)

Messages privés :

- Par défaut : `channels.imessage.dmPolicy = "pairing"`.
- Les expéditeurs inconnus reçoivent un code d'appairage ; les messages sont ignorés jusqu'à approbation (le code d'appairage expire après 1 heure).
- Pour approuver :
  - `openclaw pairing list imessage`
  - `openclaw pairing approve imessage <CODE>`
- L'appairage est l'échange de jetons par défaut pour les messages privés iMessage. Détails : [Appairage](/channels/pairing)

Groupes :

- `channels.imessage.groupPolicy = open | allowlist | disabled`.
- Lorsque défini sur `allowlist`, `channels.imessage.groupAllowFrom` contrôle qui peut déclencher dans les groupes.
- La détection des mentions utilise `agents.list[].groupChat.mentionPatterns` (ou `messages.groupChat.mentionPatterns`), car iMessage n'a pas de métadonnées de mention natives.
- Remplacement multi-agents : définissez les modèles par agent sur `agents.list[].groupChat.mentionPatterns`.

## Fonctionnement (comportement)

- `imsg` diffuse les événements de message ; la passerelle les normalise en enveloppes de canal partagées.
- Les réponses sont toujours routées vers le même ID de chat ou handle.

## Sessions de type groupe (`is_group=false`)

Certaines sessions iMessage peuvent avoir plusieurs participants, mais arrivent toujours avec `is_group=false` en fonction de la façon dont Messages stocke les identifiants de chat.

Si vous configurez explicitement un `chat_id` sous `channels.imessage.groups`, OpenClaw traitera cette session comme un "groupe" pour :

- Isolation de session (clé de session indépendante `agent:<agentId>:imessage:group:<chat_id>`)
- Comportement de liste d'autorisation de groupe / détection de mentions

Exemple :

```json5
{
  channels: {
    imessage: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15555550123"],
      groups: {
        "42": { requireMention: false },
      },
    },
  },
}
```

C'est utile lorsque vous souhaitez utiliser une personnalité/un modèle isolé pour une session spécifique (voir [Routage multi-agents](/concepts/multi-agent)). Pour l'isolation du système de fichiers, voir [Sandboxing](/gateway/sandboxing).

## Médias + limites

- Ingestion optionnelle des pièces jointes via `channels.imessage.includeAttachments`.
- Limite de médias définie via `channels.imessage.mediaMaxMb`.

## Limitations

- Le texte sortant est fragmenté selon `channels.imessage.textChunkLimit` (par défaut 4000).
- Fragmentation optionnelle par saut de ligne : définissez `channels.imessage.chunkMode="newline"` pour diviser par lignes vides (limites de paragraphes) avant la fragmentation par longueur.
- Les téléchargements de médias sont limités par `channels.imessage.mediaMaxMb` (par défaut 16).

## Adressage / cibles de livraison

Préférez `chat_id` pour un routage stable :

- `chat_id:123` (recommandé)
- `chat_guid:...`
- `chat_identifier:...`
- Handle direct : `imessage:+1555` / `sms:+1555` / `user@example.com`

Lister les chats :

```
imsg chats --limit 20
```

## Référence de configuration (iMessage)

Configuration complète : [Configuration](/gateway/configuration)

Options du fournisseur :

- `channels.imessage.enabled` : Activer/désactiver le démarrage du canal.
- `channels.imessage.cliPath` : Chemin vers `imsg`.
- `channels.imessage.dbPath` : Chemin de la base de données Messages.
- `channels.imessage.remoteHost` : Hôte SSH pour le transfert de pièces jointes SCP lorsque `cliPath` pointe vers un Mac distant (par exemple `user@gateway-host`). Détection automatique à partir du script wrapper SSH si non défini.
- `channels.imessage.service` : `imessage | sms | auto`.
- `channels.imessage.region` : Région SMS.
- `channels.imessage.dmPolicy` : `pairing | allowlist | open | disabled` (par défaut : pairing).
- `channels.imessage.allowFrom` : Liste d'autorisation des messages privés (handle, email, numéro E.164 ou `chat_id:*`). `open` nécessite `"*"`. iMessage n'a pas de noms d'utilisateur ; utilisez handle ou cible de chat.
- `channels.imessage.groupPolicy` : `open | allowlist | disabled` (par défaut : allowlist).
- `channels.imessage.groupAllowFrom` : Liste d'autorisation des expéditeurs de groupe.
- `channels.imessage.historyLimit` / `channels.imessage.accounts.*.historyLimit` : Nombre maximal de messages de groupe à inclure comme contexte (0 pour désactiver).
- `channels.imessage.dmHistoryLimit` : Limite d'historique des messages privés (
