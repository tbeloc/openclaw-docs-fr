---
title: "Référence de Configuration"
description: "Référence complète champ par champ pour ~/.openclaw/openclaw.json"
summary: "Référence complète pour chaque clé de configuration OpenClaw, les valeurs par défaut et les paramètres de canal"
read_when:
  - You need exact field-level config semantics or defaults
  - You are validating channel, model, gateway, or tool config blocks
---

# Référence de Configuration

Chaque champ disponible dans `~/.openclaw/openclaw.json`. Pour un aperçu orienté tâches, voir [Configuration](/gateway/configuration).

Le format de configuration est **JSON5** (commentaires + virgules finales autorisées). Tous les champs sont optionnels — OpenClaw utilise des valeurs par défaut sûres lorsqu'ils sont omis.

---

## Canaux

Chaque canal démarre automatiquement lorsque sa section de configuration existe (sauf si `enabled: false`).

### Accès DM et groupe

Tous les canaux supportent les politiques DM et les politiques de groupe :

| Politique DM        | Comportement                                                    |
| ------------------- | --------------------------------------------------------------- |
| `pairing` (défaut)  | Les expéditeurs inconnus reçoivent un code d'appairage unique ; le propriétaire doit approuver |
| `allowlist`         | Uniquement les expéditeurs dans `allowFrom` (ou magasin d'appairage autorisé) |
| `open`              | Autoriser tous les DM entrants (nécessite `allowFrom: ["*"]`) |
| `disabled`          | Ignorer tous les DM entrants                                    |

| Politique de groupe   | Comportement                                               |
| --------------------- | ------------------------------------------------------ |
| `allowlist` (défaut)  | Uniquement les groupes correspondant à la liste blanche configurée |
| `open`                | Contourner les listes blanches de groupe (la mention-gating s'applique toujours) |
| `disabled`            | Bloquer tous les messages de groupe/salle                 |

<Note>
`channels.defaults.groupPolicy` définit la politique par défaut lorsque `groupPolicy` d'un fournisseur n'est pas défini.
Les codes d'appairage expirent après 1 heure. Les demandes d'appairage DM en attente sont limitées à **3 par canal**.
Si un bloc de fournisseur est complètement absent (`channels.<provider>` absent), la politique de groupe au moment de l'exécution revient à `allowlist` (fail-closed) avec un avertissement au démarrage.
</Note>

### Remplacements de modèle de canal

Utilisez `channels.modelByChannel` pour épingler des ID de canal spécifiques à un modèle. Les valeurs acceptent `provider/model` ou les alias de modèle configurés. Le mappage de canal s'applique lorsqu'une session n'a pas déjà de remplacement de modèle (par exemple, défini via `/model`).

```json5
{
  channels: {
    modelByChannel: {
      discord: {
        "123456789012345678": "anthropic/claude-opus-4-6",
      },
      slack: {
        C1234567890: "openai/gpt-4.1",
      },
      telegram: {
        "-1001234567890": "openai/gpt-4.1-mini",
        "-1001234567890:topic:99": "anthropic/claude-sonnet-4-6",
      },
    },
  },
}
```

### Valeurs par défaut du canal et battement de cœur

Utilisez `channels.defaults` pour le comportement partagé de la politique de groupe et du battement de cœur entre les fournisseurs :

```json5
{
  channels: {
    defaults: {
      groupPolicy: "allowlist", // open | allowlist | disabled
      heartbeat: {
        showOk: false,
        showAlerts: true,
        useIndicator: true,
      },
    },
  },
}
```

- `channels.defaults.groupPolicy` : politique de groupe de secours lorsque `groupPolicy` au niveau du fournisseur n'est pas défini.
- `channels.defaults.heartbeat.showOk` : inclure les statuts de canal sains dans la sortie du battement de cœur.
- `channels.defaults.heartbeat.showAlerts` : inclure les statuts dégradés/erreur dans la sortie du battement de cœur.
- `channels.defaults.heartbeat.useIndicator` : afficher la sortie du battement de cœur de style indicateur compact.

### WhatsApp

WhatsApp s'exécute via le canal web de la passerelle (Baileys Web). Il démarre automatiquement lorsqu'une session liée existe.

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing", // pairing | allowlist | open | disabled
      allowFrom: ["+15555550123", "+447700900123"],
      textChunkLimit: 4000,
      chunkMode: "length", // length | newline
      mediaMaxMb: 50,
      sendReadReceipts: true, // coches bleues (false en mode auto-chat)
      groups: {
        "*": { requireMention: true },
      },
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
  },
  web: {
    enabled: true,
    heartbeatSeconds: 60,
    reconnect: {
      initialMs: 2000,
      maxMs: 120000,
      factor: 1.4,
      jitter: 0.2,
      maxAttempts: 0,
    },
  },
}
```

<Accordion title="WhatsApp multi-compte">

```json5
{
  channels: {
    whatsapp: {
      accounts: {
        default: {},
        personal: {},
        biz: {
          // authDir: "~/.openclaw/credentials/whatsapp/biz",
        },
      },
    },
  },
}
```

- Les commandes sortantes utilisent par défaut le compte `default` s'il est présent ; sinon le premier ID de compte configuré (trié).
- `channels.whatsapp.defaultAccount` optionnel remplace cette sélection de compte par défaut de secours lorsqu'il correspond à un ID de compte configuré.
- Le répertoire d'authentification Baileys à compte unique hérité est migré par `openclaw doctor` dans `whatsapp/default`.
- Remplacements par compte : `channels.whatsapp.accounts.<id>.sendReadReceipts`, `channels.whatsapp.accounts.<id>.dmPolicy`, `channels.whatsapp.accounts.<id>.allowFrom`.

</Accordion>

### Telegram

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "your-bot-token",
      dmPolicy: "pairing",
      allowFrom: ["tg:123456789"],
      groups: {
        "*": { requireMention: true },
        "-1001234567890": {
          allowFrom: ["@admin"],
          systemPrompt: "Keep answers brief.",
          topics: {
            "99": {
              requireMention: false,
              skills: ["search"],
              systemPrompt: "Stay on topic.",
            },
          },
        },
      },
      customCommands: [
        { command: "backup", description: "Git backup" },
        { command: "generate", description: "Create an image" },
      ],
      historyLimit: 50,
      replyToMode: "first", // off | first | all
      linkPreview: true,
      streaming: "partial", // off | partial | block | progress (défaut : off)
      actions: { reactions: true, sendMessage: true },
      reactionNotifications: "own", // off | own | all
      mediaMaxMb: 100,
      retry: {
        attempts: 3,
        minDelayMs: 400,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
      network: {
        autoSelectFamily: true,
        dnsResultOrder: "ipv4first",
      },
      proxy: "socks5://localhost:9050",
      webhookUrl: "https://example.com/telegram-webhook",
      webhookSecret: "secret",
      webhookPath: "/telegram-webhook",
    },
  },
}
```

- Jeton du bot : `channels.telegram.botToken` ou `channels.telegram.tokenFile` (fichier régulier uniquement ; les liens symboliques sont rejetés), avec `TELEGRAM_BOT_TOKEN` comme secours pour le compte par défaut.
- `channels.telegram.defaultAccount` optionnel remplace la sélection du compte par défaut lorsqu'il correspond à un ID de compte configuré.
- Dans les configurations multi-compte (2+ ID de compte), définissez un défaut explicite (`channels.telegram.defaultAccount` ou `channels.telegram.accounts.default`) pour éviter le routage de secours ; `openclaw doctor` avertit lorsque cela est manquant ou invalide.
- `configWrites: false` bloque les écritures de configuration initiées par Telegram (migrations d'ID de supergroupes, `/config set|unset`).
- Les entrées `bindings[]` de niveau supérieur avec `type: "acp"` configurent les liaisons ACP persistantes pour les sujets du forum (utilisez `chatId:topic:topicId` canonique dans `match.peer.id`). La sémantique des champs est partagée dans [ACP Agents](/tools/acp-agents#channel-specific-settings).
- Les aperçus de flux Telegram utilisent `sendMessage` + `editMessageText` (fonctionne dans les chats directs et de groupe).
- Politique de nouvelle tentative : voir [Politique de nouvelle tentative](/concepts/retry).

### Discord

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "your-bot-token",
      mediaMaxMb: 8,
      allowBots: false,
      actions: {
        reactions: true,
        stickers: true,
        polls: true,
        permissions: true,
        messages: true,
        threads: true,
        pins: true,
        search: true,
        memberInfo: true,
        roleInfo: true,
        roles: false,
        channelInfo: true,
        voiceStatus: true,
        events: true,
        moderation: false,
      },
      replyToMode: "off", // off | first | all
      dmPolicy: "pairing",
      allowFrom: ["1234567890", "123456789012345678"],
      dm: { enabled: true, groupEnabled: false, groupChannels: ["openclaw-dm"] },
      guilds: {
        "123456789012345678": {
          slug: "friends-of-openclaw",
          requireMention: false,
          ignoreOtherMentions: true,
          reactionNotifications: "own",
          users: ["987654321098765432"],
          channels: {
            general: { allow: true },
            help: {
              allow: true,
              requireMention: true,
              users: ["987654321098765432"],
              skills: ["docs"],
              systemPrompt: "Short answers only.",
            },
          },
        },
      },
      historyLimit: 20,
      textChunkLimit: 2000,
      chunkMode: "length", // length | newline
      streaming: "off", // off | partial | block | progress (progress correspond à partial sur Discord)
      maxLinesPerMessage: 17,
      ui: {
        components: {
          accentColor: "#5865F2",
        },
      },
      threadBindings: {
        enabled: true,
        idleHours: 24,
        maxAgeHours: 0,
        spawnSubagentSessions: false, // opt-in pour sessions_spawn({ thread: true })
      },
      voice: {
        enabled: true,
        autoJoin: [
          {
            guildId: "123456789012345678",
            channelId: "234567890123456789",
          },
        ],
        daveEncryption: true,
        decryptionFailureTolerance: 24,
        tts: {
          provider: "openai",
          openai: { voice: "alloy" },
        },
      },
      retry: {
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}
```

- Jeton : `channels.discord.token`, avec `DISCORD_BOT_TOKEN` comme secours pour le compte par défaut.
- Les appels sortants directs qui fournissent un `token` Discord explicite utilisent ce jeton pour l'appel ; les paramètres de nouvelle tentative/politique du compte proviennent toujours du compte sélectionné dans l'instantané d'exécution actif.
- `channels.discord.defaultAccount` optionnel remplace la sélection du compte par défaut lorsqu'il correspond à un ID de compte configuré.
- Utilisez `user:<id>` (DM) ou `channel:<id>` (canal de guilde) pour les cibles de livraison ; les ID numériques nus sont rejetés.
- Les slugs de guilde sont en minuscules avec les espaces remplacés par `-` ; les clés de canal utilisent le nom slugifié (pas de `#`). Préférez les ID de guilde.
- Les messages créés par des bots sont ignorés par défaut. `allowBots: true` les active ; utilisez `allowBots: "mentions"` pour accepter uniquement les messages de bot qui mentionnent le bot (les messages propres sont toujours filtrés).
- `channels.discord.guilds.<id>.ignoreOtherMentions` (et les remplacements de canal) supprime les messages qui mentionnent un autre utilisateur ou rôle mais pas le bot (à l'exclusion de @everyone/@here).
- `maxLinesPerMessage` (défaut 17) divise les messages hauts même lorsqu'ils sont sous 2000 caractères.
- `channels.discord.threadBindings` contrôle le routage lié aux threads Discord :
  - `enabled` : remplacement Discord pour les fonctionnalités de session liée aux threads (`/focus`, `/unfocus`, `/agents`, `/session idle`, `/session max-age`, et livraison/routage lié)
  - `idleHours` : remplacement Discord pour l'auto-unfocus d'inactivité en heures (`0` désactive)
  - `maxAgeHours` : remplacement Discord pour l'âge maximum dur en heures (`0` désactive)
  - `spawnSubagentSessions` : commutateur opt-in pour la création/liaison automatique de threads `sessions_spawn({ thread: true })`
- Les entrées `bindings[]` de niveau supérieur avec `type: "acp"` configurent les liaisons ACP persistantes pour les canaux et threads (utilisez l'ID de canal/thread dans `match.peer.id`). La sémantique des champs est partagée dans [ACP Agents](/tools/acp-agents#channel-specific-settings).
- `channels.discord.ui.components.accentColor` définit la couleur d'accent pour les conteneurs Discord components v2.
- `channels.discord.voice` active les conversations de canal vocal Discord et les remplacements optionnels d'auto-join + TTS.
- `channels.discord.voice.daveEncryption` et `channels.discord.voice.decryptionFailureTolerance` passent à travers les options DAVE de `@discordjs/voice` (`true` et `24` par défaut).
- OpenClaw tente en outre la récupération de réception vocale en quittant/rejoignant une session vocale après des échecs de déchiffrement répétés.
- `channels.discord.streaming` est la clé du mode de flux canonique. Les valeurs `streamMode` héritées et `streaming` booléennes sont auto-migrées.
- `channels.discord.autoPresence` mappe la disponibilité au moment de l'exécution à la présence du bot (sain => en ligne, dégradé => inactif, épuisé => dnd) et permet les remplacements de texte d'état optionnels.
- `channels.discord.dangerouslyAllowNameMatching` réactive la correspondance de nom/tag mutable (mode de compatibilité break-glass).

**Modes de notification de réaction :** `off` (aucun), `own` (messages du bot, défaut), `all` (tous les messages), `allowlist` (de `guilds.<id>.users` sur tous les messages).

### Google Chat

```json5
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountFile: "/path/to/service-account.json",
      audienceType: "app-url", // app-url | project-number
      audience: "https://gateway.example.com/googlechat",
      webhookPath: "/googlechat",
      botUser: "users/1234567890",
      dm: {
        enabled: true,
        policy: "pairing",
        allowFrom: ["users/1234567890"],
      },
      groupPolicy: "allowlist",
      groups: {
        "spaces/AAAA": { allow: true, requireMention: true },
      },
      actions: { reactions: true },
      typingIndicator: "message",
      mediaMaxMb: 20,
    },
  },
}
```

- JSON du compte de service : en ligne (`serviceAccount`) ou basé sur fichier (`serviceAccountFile`).
- SecretRef du compte de service est également supporté (`serviceAccountRef`).
- Secours d'env : `GOOGLE_CHAT_SERVICE_ACCOUNT` ou `GOOGLE_CHAT_SERVICE_ACCOUNT_FILE`.
- Utilisez `spaces/<spaceId>` ou `users/<userId>` pour les cibles de livraison.
- `channels.googlechat.dangerouslyAllowNameMatching` réactive la correspondance de principal d'email mutable (mode de compatibilité break-glass).

### Slack

```json5
{
  channels: {
    slack: {
      enabled: true,
      botToken: "xoxb-...",
      appToken: "xapp-...",
      dmPolicy: "pairing",
      allowFrom: ["U123", "U456", "*"],
      dm: { enabled: true, groupEnabled: false, groupChannels: ["G123"] },
      channels: {
        C123: { allow: true, requireMention: true, allowBots: false },
        "#general": {
          allow: true,
          requireMention: true,
          allowBots: false,
          users: ["U123"],
          skills: ["docs"],
          systemPrompt: "Short answers only.",
        },
      },
      historyLimit: 50,
      allowBots: false,
      reactionNotifications: "own",
      reactionAllowlist: ["U123"],
      replyToMode: "off", // off | first | all
      thread: {
        historyScope: "thread", // thread | channel
        inheritParent: false,
      },
      actions: {
        reactions: true,
        messages: true,
        pins: true,
        memberInfo: true,
        emojiList: true,
      },
      slashCommand: {
        enabled: true,
        name: "openclaw",
        sessionPrefix: "slack:slash",
        ephemeral: true,
      },
      typingReaction: "hourglass_flowing_sand",
      textChunkLimit: 4000,
      chunkMode: "length",
      streaming: "partial", // off | partial | block | progress (mode aperçu)
      nativeStreaming: true, // utiliser l'API de streaming natif Slack lorsque streaming=partial
      mediaMaxMb: 20,
    },
  },
}
```

- **Mode socket** nécessite à la fois `botToken` et `appToken` (`SLACK_BOT_TOKEN` + `SLACK_APP_TOKEN` pour le secours d'env du compte par défaut).
- **Mode HTTP** nécessite `botToken` plus `signingSecret` (à la racine ou par compte).
- `configWrites: false` bloque les écritures de configuration initiées par Slack.
- `channels.slack.defaultAccount` optionnel remplace la sélection du compte par défaut lorsqu'il correspond à un ID de compte configuré.
- `channels.slack.streaming` est la clé du mode de flux canonique. Les valeurs `streamMode` héritées et `streaming` booléennes sont auto-migrées.
- Utilisez `user:<id>` (DM) ou `channel:<id>` pour les cibles de livraison.

**Modes de notification de réaction :** `off`, `own` (défaut), `all`, `allowlist` (de `reactionAllowlist`).

**Isolation de session de thread :** `thread.historyScope` est par thread (défaut) ou partagé sur le canal. `thread.inheritParent` copie la transcription du canal parent vers les nouveaux threads.

- `typingReaction` ajoute une réaction temporaire au message Slack entrant pendant qu'une réponse s'exécute, puis la supprime à la fin. Utilisez un code emoji Slack tel que `"hourglass_flowing_sand"`.

| Groupe d'action | Défaut  | Notes                  |
| --------------- | ------- | ---------------------- |
| reactions       | activé  | Réagir + lister les réactions |
| messages        | activé  | Lire/envoyer/modifier/supprimer |
| pins            | activé  | Épingler/dépingler/lister |
| memberInfo      | activé  | Info membre            |
| emojiList       | activé  | Liste emoji personnalisée |

### Mattermost

Mattermost est livré en tant que plugin : `openclaw plugins install @openclaw/mattermost`.

```json5
{
  channels: {
    mattermost: {
      enabled: true,
      botToken: "mm-token",
      baseUrl: "https://chat.example.com",
      dmPolicy: "pairing",
      chatmode: "oncall", // oncall | onmessage | onchar
      oncharPrefixes: [">", "!"],
      commands: {
        native: true, // opt-in
        nativeSkills: true,
        callbackPath: "/api/channels/mattermost/command",
        // URL explicite optionnelle pour les déploiements reverse-proxy/publics
        callbackUrl: "https://gateway.example.com/api/channels/mattermost/command",
      },
      textChunkLimit: 4000,
      chunkMode: "length",
    },
  },
}
```

Modes de chat : `oncall` (répondre sur @-mention, défaut), `onmessage` (chaque message), `onchar` (messages commençant par le préfixe de déclenchement).

Lorsque les commandes natives Mattermost sont activées :

- `commands.callbackPath` doit être un chemin (par exemple `/api/channels/mattermost/command`), pas une URL complète.
- `commands.callbackUrl` doit se résoudre au point de terminaison de la passerelle OpenClaw et être accessible depuis le serveur Mattermost.
- Pour les hôtes de rappel privés/tailnet/internes, Mattermost peut nécessiter
  `ServiceSettings.AllowedUntrustedInternalConnections` pour inclure l'hôte/domaine de rappel.
  Utilisez les valeurs d'hôte/domaine, pas les URL complètes.
- `channels.mattermost.configWrites` : autoriser ou refuser les écritures de configuration initiées par Mattermost.
- `channels.mattermost.requireMention` : exiger `@mention` avant de répondre dans les canaux.
- `channels.mattermost.defaultAccount` optionnel remplace la sélection du compte par défaut lorsqu'il correspond à un ID de compte configuré.

### Signal

```json5
{
  channels: {
    signal: {
      enabled: true,
      account: "+15555550123", // liaison de compte optionnelle
      dmPolicy: "pairing",
      allowFrom: ["+15551234567", "uuid:123e4567-e89b-12d3-a456-426614174000"],
      configWrites: true,
      reactionNotifications: "own", // off | own | all | allowlist
      reactionAllowlist: ["+15551234567", "uuid:123e4567-e89b-12d3-a456-426614174000"],
      historyLimit: 50,
    },
  },
}
```

**Modes de notification de réaction :** `off`, `own` (défaut), `all`, `allowlist` (de `reactionAllowlist`).

- `channels.signal.account` : épingler le démarrage du canal à une identité de compte Signal spécifique.
- `channels.signal.configWrites` : autoriser ou refuser les écritures de configuration initiées par Signal.
- `channels.signal.defaultAccount` optionnel remplace la sélection du compte par défaut lorsqu'il correspond à un ID de compte configuré.

### BlueBubbles

BlueBubbles est le chemin iMessage recommandé (soutenu par plugin, configuré sous `channels.bluebubbles`).

```json5
{
  channels: {
    bluebubbles: {
      enabled: true,
      dmPolicy: "pairing",
      // serverUrl, password, webhookPath, contrôles de groupe, et actions avancées :
      // voir /channels/bluebubbles
    },
  },
}
```

- Chemins de clés principaux couverts ici : `channels.bluebubbles`, `channels.bluebubbles.dmPolicy`.
- `channels.bluebubbles.defaultAccount` optionnel remplace la sélection du compte par défaut lorsqu'il correspond à un ID de compte configuré.
- La configuration complète du canal BlueBubbles est documentée dans [BlueBubbles](/channels/bluebubbles).

### iMessage

OpenClaw lance `imsg rpc` (JSON-RPC sur stdio). Aucun démon ou port requis.

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "imsg",
      dbPath: "~/Library/Messages/chat.db",
      remoteHost: "user@gateway-host",
      dmPolicy: "pairing",
      allowFrom: ["+15555550123", "user@example.com", "chat_id:123"],
      historyLimit: 50,
      includeAttachments: false,
      attachmentRoots: ["/Users/*/Library/Messages/Attachments"],
      remoteAttachmentRoots: ["/Users/*/Library/Messages/Attachments"],
      mediaMaxMb: 16,
      service: "auto",
      region: "US",
    },
  },
}
```

- `channels.imessage.defaultAccount` optionnel remplace la sélection du compte par défaut lorsqu'il correspond à un ID de compte configuré.

- Nécessite l'accès complet au disque à la base de données Messages.
- Préférez les cibles `chat_id:<id>`. Utilisez `imsg chats --limit 20` pour lister les chats.
- `cliPath` peut pointer vers un wrapper SSH ; définissez `remoteHost` (`host` ou `user@host`) pour la récupération de pièces jointes SCP.
- `attachmentRoots` et `remoteAttachmentRoots` limitent les chemins de pièces jointes entrantes (défaut : `/Users/*/Library/Messages/Attachments`).
- SCP utilise la vérification stricte de la clé d'hôte, assurez-vous donc que la clé d'hôte de relais existe déjà dans `~/.ssh/known_hosts`.
- `channels.imessage.configWrites` : autoriser ou refuser les écritures de configuration initiées par iMessage.

<Accordion title="Exemple de wrapper SSH iMessage">

```bash
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"
```

</Accordion>

### Microsoft Teams

Microsoft Teams est soutenu par extension et configuré sous `channels.msteams`.

```json5
{
  channels: {
    msteams: {
      enabled: true,
      configWrites: true,
      // appId, appPassword, tenantId, webhook, politiques d'équipe/canal :
      // voir /channels/msteams
    },
  },
}
```

- Chemins de clés principaux couverts ici : `channels.msteams`, `channels.msteams.configWrites`.
- La configuration complète de Teams (identifiants, webhook, politique DM/groupe, remplacements par équipe/par canal) est documentée dans [Microsoft Teams](/channels/msteams).

### IRC

IRC est soutenu par extension et configuré sous `channels.irc`.

```json5
{
  channels: {
    irc: {
      enabled: true,
      dmPolicy: "pairing",
      configWrites: true,
      nickserv: {
        enabled: true,
        service: "NickServ",
        password: "${IRC_NICKSERV_PASSWORD}",
        register: false,
        registerEmail: "bot@example.com",
      },
    },
  },
}
```

- Chemins de clés principaux couverts ici : `channels.irc`, `channels.irc.dmPolicy`, `channels.irc.configWrites`, `channels.irc.nickserv.*`.
- `channels.irc.defaultAccount` optionnel remplace la sélection du compte par défaut lorsqu'il correspond à un ID de compte configuré.
- La configuration complète du canal IRC (hôte/port/TLS/canaux/listes blanches/mention gating) est documentée dans [IRC](/channels/irc).

### Multi-compte (tous les canaux)

Exécutez plusieurs comptes par canal (chacun avec son propre `accountId`) :

```json5
{
  channels: {
    telegram: {
      accounts: {
        default: {
          name: "Primary bot",
          botToken: "123456:ABC...",
        },
        alerts: {
          name: "Alerts bot",
          botToken: "987654:XYZ...",
        },
      },
    },
  },
}
```

- `default` est utilisé lorsque `accountId` est omis (CLI + routage).
- Les jetons d'env s'appliquent uniquement au compte **par défaut**.
- Les paramètres de canal de base s'appliquent à tous les comptes sauf s'ils sont remplacés par compte.
- Utilisez `bindings[].match.accountId` pour router chaque compte vers un agent différent.
- Si vous ajoutez un compte non-défaut via `openclaw channels add` (ou l'intégration de canal) tout en étant toujours sur une configuration de canal à compte unique au niveau supérieur, OpenClaw déplace les valeurs à compte unique au niveau supérieur dans `channels.<channel>.accounts.default` en premier afin que le compte d'origine continue de fonctionner.
- Les liaisons de canal existantes (pas de `accountId`) continuent de correspondre au compte par défaut ; les liaisons à compte unique restent optionnelles.
- `openclaw doctor --fix` répare également les formes mixtes en déplaçant les valeurs à compte unique au niveau supérieur dans `accounts.default` lorsque des comptes nommés existent mais que `default` est manquant.

### Autres canaux d'extension

De nombreux canaux d'extension sont configurés comme `channels.<id>` et documentés dans leurs pages de canal dédiées (par exemple Feishu, Matrix, LINE, Nostr, Zalo, Nextcloud Talk, Synology Chat et Twitch).
Voir l'index complet des canaux : [Canaux](/channels).

### Mention gating de chat de groupe

Les messages de groupe nécessitent par défaut une **mention** (mention de métadonnées ou modèles regex). S'applique aux chats de groupe WhatsApp, Telegram, Discord, Google Chat et iMessage.

**Types de mention :**

- **Mentions de métadonnées** : @-mentions natives de la plateforme. Ignorées en mode auto-chat WhatsApp.
- **Modèles de texte** : Modèles regex dans `agents.list[].groupChat.mentionPatterns`. Toujours vérifiés.
- Le mention gating n'est appliqué que lorsque la détection est possible (mentions natives ou au moins un modèle).

```json5
{
  messages: {
    groupChat: { historyLimit: 50 },
  },
  agents: {
    list: [{ id: "main", groupChat: { mentionPatterns: ["@openclaw", "openclaw"] } }],
  },
}
```

`messages.groupChat.historyLimit` définit la valeur par défaut globale. Les canaux peuvent remplacer avec `channels.<channel>.historyLimit` (ou par compte). Définissez `0` pour désactiver.

#### Limites d'historique DM

```json5
{
  channels: {
    telegram: {
      dmHistoryLimit: 30,
      dms: {
        "123456789": { historyLimit: 50 },
      },
    },
  },
}
```

Résolution : remplacement par DM → défaut du fournisseur → pas de limite (tous conservés).

Supporté : `telegram`, `whatsapp`, `discord`, `slack`, `signal`, `imessage`, `msteams`.

#### Mode auto-chat

Incluez votre propre numéro dans `allowFrom` pour activer le mode auto-chat (ignore les @-mentions natives, répond uniquement aux modèles de texte) :

```json5
{
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: { mentionPatterns: ["reisponde", "@openclaw"] },
      },
    ],
  },
}
```

### Commandes (gestion des commandes de chat)

```json5
{
  commands: {
    native: "auto", // enregistrer les commandes natives lorsqu'elles sont supportées
    text: true, // analyser /commands dans les messages de chat
    bash: false, // autoriser ! (alias : /bash)
    bashForegroundMs: 2000,
    config: false, // autoriser /config
    debug: false, // autoriser /debug
    restart: false, // autoriser /restart + outil de redémarrage de passerelle
    allowFrom: {
      "*": ["user1"],
      discord: ["user:123"],
    },
    useAccessGroups: true,
  },
}
```

<Accordion title="Détails des commandes">

- Les commandes texte doivent être des messages **autonomes** avec un `/` initial.
- `native: "auto"` active les commandes natives pour Discord/Telegram, laisse Slack désactivé.
- Remplacer par canal : `channels.discord.commands.native` (bool ou `"auto"`). `false` efface les commandes précédemment enregistrées.
- `channels.telegram.customCommands` ajoute des entrées de menu de bot Telegram supplémentaires.
- `bash: true` active `! <cmd>` pour le shell d'hôte. Nécessite `tools.elevated.enabled` et l'expéditeur dans `tools.elevated.allowFrom.<channel>`.
- `config: true` active `/config` (lit/écrit `openclaw.json`). Pour les clients `chat.send` de passerelle, les écritures persistantes `/config set|unset` nécessitent également `operator.admin` ; la lecture seule `/config show` reste disponible pour les clients opérateur à portée d'écriture normale.
- `channels.<provider>.configWrites` contrôle les mutations de configuration par canal (défaut : true).
- Pour les canaux multi-compte, `channels.<provider>.accounts.<id>.configWrites` contrôle également les écritures qui ciblent ce compte (par exemple `/allowlist --config --account <id>` ou `/config set channels.<provider>.accounts.<id>...`).
- `allowFrom` est par fournisseur. Lorsqu'il est défini, c'est la **seule** source d'autorisation (les listes blanches de canal/appairage et `useAccessGroups` sont ignorés).
- `useAccessGroups: false` permet aux commandes de contourner les politiques de groupe d'accès lorsque `allowFrom` n'est pas défini.

</Accordion>

## Valeurs par défaut des agents

### `agents.defaults.workspace`

Valeur par défaut : `~/.openclaw/workspace`.

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

### `agents.defaults.repoRoot`

Racine du référentiel optionnelle affichée dans la ligne Runtime de l'invite système. Si non définie, OpenClaw détecte automatiquement en remontant à partir de l'espace de travail.

```json5
{
  agents: { defaults: { repoRoot: "~/Projects/openclaw" } },
}
```

### `agents.defaults.skipBootstrap`

Désactive la création automatique des fichiers d'amorçage de l'espace de travail (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOTSTRAP.md`).

```json5
{
  agents: { defaults: { skipBootstrap: true } },
}
```

### `agents.defaults.bootstrapMaxChars`

Nombre maximum de caractères par fichier d'amorçage de l'espace de travail avant troncature. Valeur par défaut : `20000`.

```json5
{
  agents: { defaults: { bootstrapMaxChars: 20000 } },
}
```

### `agents.defaults.bootstrapTotalMaxChars`

Nombre maximum total de caractères injectés dans tous les fichiers d'amorçage de l'espace de travail. Valeur par défaut : `150000`.

```json5
{
  agents: { defaults: { bootstrapTotalMaxChars: 150000 } },
}
```

### `agents.defaults.bootstrapPromptTruncationWarning`

Contrôle le texte d'avertissement visible par l'agent lorsque le contexte d'amorçage est tronqué.
Valeur par défaut : `"once"`.

- `"off"` : ne jamais injecter de texte d'avertissement dans l'invite système.
- `"once"` : injecter l'avertissement une fois par signature de troncature unique (recommandé).
- `"always"` : injecter l'avertissement à chaque exécution lorsqu'une troncature existe.

```json5
{
  agents: { defaults: { bootstrapPromptTruncationWarning: "once" } }, // off | once | always
}
```

### `agents.defaults.imageMaxDimensionPx`

Taille maximale en pixels pour le côté le plus long de l'image dans les blocs d'image de transcription/outil avant les appels au fournisseur.
Valeur par défaut : `1200`.

Les valeurs plus basses réduisent généralement l'utilisation des jetons de vision et la taille de la charge utile de la requête pour les exécutions riches en captures d'écran.
Les valeurs plus élevées préservent plus de détails visuels.

```json5
{
  agents: { defaults: { imageMaxDimensionPx: 1200 } },
}
```

### `agents.defaults.userTimezone`

Fuseau horaire pour le contexte de l'invite système (pas les horodatages des messages). Revient au fuseau horaire de l'hôte.

```json5
{
  agents: { defaults: { userTimezone: "America/Chicago" } },
}
```

### `agents.defaults.timeFormat`

Format d'heure dans l'invite système. Valeur par défaut : `auto` (préférence du système d'exploitation).

```json5
{
  agents: { defaults: { timeFormat: "auto" } }, // auto | 12 | 24
}
```

### `agents.defaults.model`

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "opus" },
        "minimax/MiniMax-M2.5": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["minimax/MiniMax-M2.5"],
      },
      imageModel: {
        primary: "openrouter/qwen/qwen-2.5-vl-72b-instruct:free",
        fallbacks: ["openrouter/google/gemini-2.0-flash-vision:free"],
      },
      pdfModel: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["openai/gpt-5-mini"],
      },
      pdfMaxBytesMb: 10,
      pdfMaxPages: 20,
      thinkingDefault: "low",
      verboseDefault: "off",
      elevatedDefault: "on",
      timeoutSeconds: 600,
      mediaMaxMb: 5,
      contextTokens: 200000,
      maxConcurrent: 3,
    },
  },
}
```

- `model` : accepte soit une chaîne (`"provider/model"`) soit un objet (`{ primary, fallbacks }`).
  - La forme chaîne définit uniquement le modèle principal.
  - La forme objet définit le modèle principal plus les modèles de basculement ordonnés.
- `imageModel` : accepte soit une chaîne (`"provider/model"`) soit un objet (`{ primary, fallbacks }`).
  - Utilisé par le chemin d'outil `image` comme configuration de modèle de vision.
  - Également utilisé comme routage de secours lorsque le modèle sélectionné/par défaut ne peut pas accepter d'entrée d'image.
- `pdfModel` : accepte soit une chaîne (`"provider/model"`) soit un objet (`{ primary, fallbacks }`).
  - Utilisé par l'outil `pdf` pour le routage des modèles.
  - S'il est omis, l'outil PDF revient à `imageModel`, puis aux valeurs par défaut du fournisseur au mieux.
- `pdfMaxBytesMb` : limite de taille PDF par défaut pour l'outil `pdf` lorsque `maxBytesMb` n'est pas passé au moment de l'appel.
- `pdfMaxPages` : nombre maximum de pages par défaut considérées par le mode de secours d'extraction dans l'outil `pdf`.
- `model.primary` : format `provider/model` (par exemple `anthropic/claude-opus-4-6`). Si vous omettez le fournisseur, OpenClaw suppose `anthropic` (déprécié).
- `models` : le catalogue de modèles configuré et la liste d'autorisation pour `/model`. Chaque entrée peut inclure `alias` (raccourci) et `params` (spécifique au fournisseur, par exemple `temperature`, `maxTokens`, `cacheRetention`, `context1m`).
- `params` fusion de précédence (config) : `agents.defaults.models["provider/model"].params` est la base, puis `agents.list[].params` (correspondant à l'id de l'agent) remplace par clé.
- Les rédacteurs de config qui mutent ces champs (par exemple `/models set`, `/models set-image` et les commandes d'ajout/suppression de secours) enregistrent la forme d'objet canonique et préservent les listes de secours existantes si possible.
- `maxConcurrent` : nombre maximum d'exécutions d'agents parallèles entre les sessions (chaque session reste sérialisée). Valeur par défaut : 1.

**Raccourcis d'alias intégrés** (s'appliquent uniquement lorsque le modèle est dans `agents.defaults.models`) :

| Alias               | Modèle                                 |
| ------------------- | -------------------------------------- |
| `opus`              | `anthropic/claude-opus-4-6`            |
| `sonnet`            | `anthropic/claude-sonnet-4-6`          |
| `gpt`               | `openai/gpt-5.4`                       |
| `gpt-mini`          | `openai/gpt-5-mini`                    |
| `gemini`            | `google/gemini-3.1-pro-preview`        |
| `gemini-flash`      | `google/gemini-3-flash-preview`        |
| `gemini-flash-lite` | `google/gemini-3.1-flash-lite-preview` |

Vos alias configurés l'emportent toujours sur les valeurs par défaut.

Les modèles Z.AI GLM-4.x activent automatiquement le mode de réflexion sauf si vous définissez `--thinking off` ou `agents.defaults.models["zai/<model>"].params.thinking` vous-même.
Les modèles Z.AI activent `tool_stream` par défaut pour le streaming des appels d'outils. Définissez `agents.defaults.models["zai/<model>"].params.tool_stream` sur `false` pour le désactiver.
Les modèles Anthropic Claude 4.6 utilisent par défaut la réflexion `adaptive` lorsqu'aucun niveau de réflexion explicite n'est défini.

### `agents.defaults.cliBackends`

Backends CLI optionnels pour les exécutions de secours texte uniquement (pas d'appels d'outils). Utile comme sauvegarde lorsque les fournisseurs d'API échouent.

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
        "my-cli": {
          command: "my-cli",
          args: ["--json"],
          output: "json",
          modelArg: "--model",
          sessionArg: "--session",
          sessionMode: "existing",
          systemPromptArg: "--system",
          systemPromptWhen: "first",
          imageArg: "--image",
          imageMode: "repeat",
        },
      },
    },
  },
}
```

- Les backends CLI sont texte en premier ; les outils sont toujours désactivés.
- Sessions supportées lorsque `sessionArg` est défini.
- Passage d'image supporté lorsque `imageArg` accepte les chemins de fichiers.

### `agents.defaults.heartbeat`

Exécutions de battement de cœur périodiques.

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m", // 0m désactive
        model: "openai/gpt-5.2-mini",
        includeReasoning: false,
        lightContext: false, // par défaut : false ; true conserve uniquement HEARTBEAT.md des fichiers d'amorçage de l'espace de travail
        session: "main",
        to: "+15555550123",
        directPolicy: "allow", // allow (par défaut) | block
        target: "none", // par défaut : none | options : last | whatsapp | telegram | discord | ...
        prompt: "Read HEARTBEAT.md if it exists...",
        ackMaxChars: 300,
        suppressToolErrorWarnings: false,
      },
    },
  },
}
```

- `every` : chaîne de durée (ms/s/m/h). Valeur par défaut : `30m`.
- `suppressToolErrorWarnings` : lorsque true, supprime les charges utiles d'avertissement d'erreur d'outil lors des exécutions de battement de cœur.
- `directPolicy` : politique de livraison directe/DM. `allow` (par défaut) permet la livraison à cible directe. `block` supprime la livraison à cible directe et émet `reason=dm-blocked`.
- `lightContext` : lorsque true, les exécutions de battement de cœur utilisent un contexte d'amorçage léger et conservent uniquement `HEARTBEAT.md` des fichiers d'amorçage de l'espace de travail.
- Par agent : définissez `agents.list[].heartbeat`. Lorsqu'un agent définit `heartbeat`, **seuls ces agents** exécutent les battements de cœur.
- Les battements de cœur exécutent des tours d'agent complets — les intervalles plus courts consomment plus de jetons.

### `agents.defaults.compaction`

```json5
{
  agents: {
    defaults: {
      compaction: {
        mode: "safeguard", // default | safeguard
        reserveTokensFloor: 24000,
        identifierPolicy: "strict", // strict | off | custom
        identifierInstructions: "Preserve deployment IDs, ticket IDs, and host:port pairs exactly.", // utilisé lorsque identifierPolicy=custom
        postCompactionSections: ["Session Startup", "Red Lines"], // [] désactive la réinjection
        model: "openrouter/anthropic/claude-sonnet-4-5", // override optionnel de modèle de compaction uniquement
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 6000,
          systemPrompt: "Session nearing compaction. Store durable memories now.",
          prompt: "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store.",
        },
      },
    },
  },
}
```

- `mode` : `default` ou `safeguard` (résumé par chunks pour les longs historiques). Voir [Compaction](/concepts/compaction).
- `identifierPolicy` : `strict` (par défaut), `off` ou `custom`. `strict` ajoute des conseils intégrés de rétention d'identifiant opaque lors de la résumé de compaction.
- `identifierInstructions` : texte optionnel de préservation d'identifiant personnalisé utilisé lorsque `identifierPolicy=custom`.
- `postCompactionSections` : noms de sections H2/H3 optionnels de AGENTS.md à réinjecter après compaction. Par défaut `["Session Startup", "Red Lines"]` ; définissez `[]` pour désactiver la réinjection. Lorsque non défini ou explicitement défini sur cette paire par défaut, les anciens titres `Every Session`/`Safety` sont également acceptés comme secours hérité.
- `model` : override optionnel `provider/model-id` pour la résumé de compaction uniquement. Utilisez ceci lorsque la session principale doit conserver un modèle mais les résumés de compaction doivent s'exécuter sur un autre ; lorsque non défini, la compaction utilise le modèle principal de la session.
- `memoryFlush` : tour agentic silencieux avant la compaction automatique pour stocker les mémoires durables. Ignoré lorsque l'espace de travail est en lecture seule.

### `agents.defaults.contextPruning`

Élague les **anciens résultats d'outils** du contexte en mémoire avant d'envoyer au LLM. Ne modifie **pas** l'historique de la session sur le disque.

```json5
{
  agents: {
    defaults: {
      contextPruning: {
        mode: "cache-ttl", // off | cache-ttl
        ttl: "1h", // durée (ms/s/m/h), unité par défaut : minutes
        keepLastAssistants: 3,
        softTrimRatio: 0.3,
        hardClearRatio: 0.5,
        minPrunableToolChars: 50000,
        softTrim: { maxChars: 4000, headChars: 1500, tailChars: 1500 },
        hardClear: { enabled: true, placeholder: "[Old tool result content cleared]" },
        tools: { deny: ["browser", "canvas"] },
      },
    },
  },
}
```

<Accordion title="Comportement du mode cache-ttl">

- `mode: "cache-ttl"` active les passages d'élagage.
- `ttl` contrôle la fréquence à laquelle l'élagage peut s'exécuter à nouveau (après le dernier accès au cache).
- L'élagage réduit d'abord les résultats d'outils surdimensionnés, puis efface les résultats d'outils plus anciens si nécessaire.

**Réduction progressive** conserve le début + la fin et insère `...` au milieu.

**Effacement complet** remplace le résultat d'outil entier par l'espace réservé.

Notes :

- Les blocs d'image ne sont jamais réduits/effacés.
- Les ratios sont basés sur les caractères (approximatifs), pas les comptes de jetons exacts.
- Si moins de `keepLastAssistants` messages d'assistant existent, l'élagage est ignoré.

</Accordion>

Voir [Session Pruning](/concepts/session-pruning) pour les détails du comportement.

### Streaming par blocs

```json5
{
  agents: {
    defaults: {
      blockStreamingDefault: "off", // on | off
      blockStreamingBreak: "text_end", // text_end | message_end
      blockStreamingChunk: { minChars: 800, maxChars: 1200 },
      blockStreamingCoalesce: { idleMs: 1000 },
      humanDelay: { mode: "natural" }, // off | natural | custom (utiliser minMs/maxMs)
    },
  },
}
```

- Les canaux non-Telegram nécessitent un `*.blockStreaming: true` explicite pour activer les réponses par blocs.
- Overrides de canal : `channels.<channel>.blockStreamingCoalesce` (et variantes par compte). Signal/Slack/Discord/Google Chat utilisent par défaut `minChars: 1500`.
- `humanDelay` : pause aléatoire entre les réponses par blocs. `natural` = 800–2500ms. Override par agent : `agents.list[].humanDelay`.

Voir [Streaming](/concepts/streaming) pour les détails du comportement + chunking.

### Indicateurs de saisie

```json5
{
  agents: {
    defaults: {
      typingMode: "instant", // never | instant | thinking | message
      typingIntervalSeconds: 6,
    },
  },
}
```

- Valeurs par défaut : `instant` pour les chats directs/mentions, `message` pour les chats de groupe non mentionnés.
- Overrides par session : `session.typingMode`, `session.typingIntervalSeconds`.

Voir [Typing Indicators](/concepts/typing-indicators).

### `agents.defaults.sandbox`

Sandboxing **Docker** optionnel pour l'agent intégré. Voir [Sandboxing](/gateway/sandboxing) pour le guide complet.

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // off | non-main | all
        scope: "agent", // session | agent | shared
        workspaceAccess: "none", // none | ro | rw
        workspaceRoot: "~/.openclaw/sandboxes",
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          containerPrefix: "openclaw-sbx-",
          workdir: "/workspace",
          readOnlyRoot: true,
          tmpfs: ["/tmp", "/var/tmp", "/run"],
          network: "none",
          user: "1000:1000",
          capDrop: ["ALL"],
          env: { LANG: "C.UTF-8" },
          setupCommand: "apt-get update && apt-get install -y git curl jq",
          pidsLimit: 256,
          memory: "1g",
          memorySwap: "2g",
          cpus: 1,
          ulimits: {
            nofile: { soft: 1024, hard: 2048 },
            nproc: 256,
          },
          seccompProfile: "/path/to/seccomp.json",
          apparmorProfile: "openclaw-sandbox",
          dns: ["1.1.1.1", "8.8.8.8"],
          extraHosts: ["internal.service:10.0.0.5"],
          binds: ["/home/user/source:/source:rw"],
        },
        browser: {
          enabled: false,
          image: "openclaw-sandbox-browser:bookworm-slim",
          network: "openclaw-sandbox-browser",
          cdpPort: 9222,
          cdpSourceRange: "172.21.0.1/32",
          vncPort: 5900,
          noVncPort: 6080,
          headless: false,
          enableNoVnc: true,
          allowHostControl: false,
          autoStart: true,
          autoStartTimeoutMs: 12000,
        },
        prune: {
          idleHours: 24,
          maxAgeDays: 7,
        },
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        allow: [
          "exec",
          "process",
          "read",
          "write",
          "edit",
          "apply_patch",
          "sessions_list",
          "sessions_history",
          "sessions_send",
          "sessions_spawn",
          "session_status",
        ],
        deny: ["browser", "canvas", "nodes", "cron", "discord", "gateway"],
      },
    },
  },
}
```

<Accordion title="Détails du sandbox">

**Accès à l'espace de travail :**

- `none` : espace de travail sandbox par portée sous `~/.openclaw/sandboxes`
- `ro` : espace de travail sandbox à `/workspace`, espace de travail de l'agent monté en lecture seule à `/agent`
- `rw` : espace de travail de l'agent monté en lecture/écriture à `/workspace`

**Portée :**

- `session` : conteneur + espace de travail par session
- `agent` : un conteneur + espace de travail par agent (par défaut)
- `shared` : conteneur et espace de travail partagés (pas d'isolation entre sessions)

**`setupCommand`** s'exécute une fois après la création du conteneur (via `sh -lc`). Nécessite l'accès réseau sortant, la racine inscriptible, l'utilisateur root.

**Les conteneurs utilisent par défaut `network: "none"`** — définissez sur `"bridge"` (ou un réseau bridge personnalisé) si l'agent a besoin d'accès sortant.
`"host"` est bloqué. `"container:<id>"` est bloqué par défaut sauf si vous définissez explicitement
`sandbox.docker.dangerouslyAllowContainerNamespaceJoin: true` (break-glass).

**Les pièces jointes entrantes** sont mises en scène dans `media/inbound/*` dans l'espace de travail actif.

**`docker.binds`** monte des répertoires hôtes supplémentaires ; les binds globaux et par agent sont fusionnés.

**Navigateur sandboxé** (`sandbox.browser.enabled`) : Chromium + CDP dans un conteneur. URL noVNC injectée dans l'invite système. Ne nécessite pas `browser.enabled` dans `openclaw.json`.
L'accès observateur noVNC utilise l'authentification VNC par défaut et OpenClaw émet une URL de jeton de courte durée (au lieu d'exposer le mot de passe dans l'URL partagée).

- `allowHostControl: false` (par défaut) bloque les sessions sandboxées de cibler le navigateur hôte.
- `network` utilise par défaut `openclaw-sandbox-browser` (réseau bridge dédié). Définissez sur `bridge` uniquement lorsque vous voulez explicitement la connectivité bridge globale.
- `cdpSourceRange` restreint optionnellement l'entrée CDP au bord du conteneur à une plage CIDR (par exemple `172.21.0.1/32`).
- `sandbox.browser.binds` monte des répertoires hôtes supplémentaires uniquement dans le conteneur du navigateur sandboxé. Lorsqu'il est défini (y compris `[]`), il remplace `docker.binds` pour le conteneur du navigateur.
- Les valeurs par défaut de lancement sont définies dans `scripts/sandbox-browser-entrypoint.sh` et ajustées pour les hôtes de conteneur :
  - `--remote-debugging-address=127.0.0.1`
  - `--remote-debugging-port=<dérivé de OPENCLAW_BROWSER_CDP_PORT>`
  - `--user-data-dir=${HOME}/.chrome`
  - `--no-first-run`
  - `--no-default-browser-check`
  - `--disable-3d-apis`
  - `--disable-gpu`
  - `--disable-software-rasterizer`
  - `--disable-dev-shm-usage`
  - `--disable-background-networking`
  - `--disable-features=TranslateUI`
  - `--disable-breakpad`
  - `--disable-crash-reporter`
  - `--renderer-process-limit=2`
  - `--no-zygote`
  - `--metrics-recording-only`
  - `--disable-extensions` (activé par défaut)
  - `--disable-3d-apis`, `--disable-software-rasterizer` et `--disable-gpu` sont
    activés par défaut et peuvent être désactivés avec
    `OPENCLAW_BROWSER_DISABLE_GRAPHICS_FLAGS=0` si l'utilisation de WebGL/3D l'exige.
  - `OPENCLAW_BROWSER_DISABLE_EXTENSIONS=0` réactive les extensions si votre flux de travail
    en dépend.
  - `--renderer-process-limit=2` peut être modifié avec
    `OPENCLAW_BROWSER_RENDERER_PROCESS_LIMIT=<N>` ; définissez `0` pour utiliser la
    limite de processus par défaut de Chromium.
  - plus `--no-sandbox` et `--disable-setuid-sandbox` lorsque `noSandbox` est activé.
  - Les valeurs par défaut sont la ligne de base de l'image du conteneur ; utilisez une image de navigateur personnalisée avec un point d'entrée personnalisé pour modifier les valeurs par défaut du conteneur.

</Accordion>

Construire les images :

```bash
scripts/sandbox-setup.sh           # image sandbox principale
scripts/sandbox-browser-setup.sh   # image navigateur optionnelle
```

### `agents.list` (overrides par agent)

```json5
{
  agents: {
    list: [
      {
        id: "main",
        default: true,
        name: "Main Agent",
        workspace: "~/.openclaw/workspace",
        agentDir: "~/.openclaw/agents/main/agent",
        model: "anthropic/claude-opus-4-6", // ou { primary, fallbacks }
        params: { cacheRetention: "none" }, // remplace les params defaults.models correspondants par clé
        identity: {
          name: "Samantha",
          theme: "helpful sloth",
          emoji: "🦥",
          avatar: "avatars/samantha.png",
        },
        groupChat: { mentionPatterns: ["@openclaw"] },
        sandbox: { mode: "off" },
        runtime: {
          type: "acp",
          acp: {
            agent: "codex",
            backend: "acpx",
            mode: "persistent",
            cwd: "/workspace/openclaw",
          },
        },
        subagents: { allowAgents: ["*"] },
        tools: {
          profile: "coding",
          allow: ["browser"],
          deny: ["canvas"],
          elevated: { enabled: true },
        },
      },
    ],
  },
}
```

- `id` : id d'agent stable (requis).
- `default` : lorsque plusieurs sont définis, le premier gagne (avertissement enregistré). Si aucun n'est défini, la première entrée de liste est par défaut.
- `model` : la forme chaîne remplace uniquement `primary` ; la forme objet `{ primary, fallbacks }` remplace les deux (`[]` désactive les secours globaux). Les tâches cron qui remplacent uniquement `primary` héritent toujours des secours par défaut sauf si vous définissez `fallbacks: []`.
- `params` : params de flux par agent fusionnés sur l'entrée de modèle sélectionnée dans `agents.defaults.models`. Utilisez ceci pour les overrides spécifiques à l'agent comme `cacheRetention`, `temperature` ou `maxTokens` sans dupliquer le catalogue de modèles entier.
- `runtime` : descripteur de runtime optionnel par agent. Utilisez `type: "acp"` avec les valeurs par défaut `runtime.acp` (`agent`, `backend`, `mode`, `cwd`) lorsque l'agent doit utiliser par défaut les sessions du harnais ACP.
- `identity.avatar` : chemin relatif à l'espace de travail, URL `http(s)` ou URI `data:`.
- `identity` dérive les valeurs par défaut : `ackReaction` de `emoji`, `mentionPatterns` de `name`/`emoji`.
- `subagents.allowAgents` : liste d'autorisation des ids d'agent pour `sessions_spawn` (`["*"]` = n'importe lequel ; par défaut : même agent uniquement).
- Garde d'héritage sandbox : si la session du demandeur est sandboxée, `sessions_spawn` rejette les cibles qui s'exécuteraient sans sandbox.

---

## Routage multi-agent

Exécutez plusieurs agents isolés dans une seule Gateway. Voir [Multi-Agent](/concepts/multi-agent).

```json5
{
  agents: {
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
}
```

### Champs de correspondance de liaison

- `type` (optionnel) : `route` pour le routage normal (le type manquant par défaut à route), `acp` pour les liaisons de conversation ACP persistantes.
- `match.channel` (requis)
- `match.accountId` (optionnel ; `*` = tout compte ; omis = compte par défaut)
- `match.peer` (optionnel ; `{ kind: direct|group|channel, id }`)
- `match.guildId` / `match.teamId` (optionnel ; spécifique au canal)
- `acp` (optionnel ; uniquement pour `type: "acp"`) : `{ mode, label, cwd, backend }`

**Ordre de correspondance déterministe :**

1. `match.peer`
2. `match.guildId`
3. `match.teamId`
4. `match.accountId` (exact, sans peer/guild/team)
5. `match.accountId: "*"` (à l'échelle du canal)
6. Agent par défaut

Dans chaque niveau, la première entrée `bindings` correspondante gagne.

Pour les entrées `type: "acp"`, OpenClaw résout par identité de conversation exacte (`match.channel` + compte + `match.peer.id`) et n'utilise pas l'ordre de niveau de liaison de route ci-dessus.

### Profils d'accès par agent

<Accordion title="Accès complet (pas de sandbox)">

```json5
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: { mode: "off" },
      },
    ],
  },
}
```

</Accordion>

<Accordion title="Outils et espace de travail en lecture seule">

```json5
{
  agents: {
    list: [
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: { mode: "all", scope: "agent", workspaceAccess: "ro" },
        tools: {
          allow: [
            "read",
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
          ],
          deny: ["write", "edit", "apply_patch", "exec", "process", "browser"],
        },
      },
    ],
  },
}
```

</Accordion>

<Accordion title="Pas d'accès au système de fichiers (messagerie uniquement)">

```json5
{
  agents: {
    list: [
      {
        id: "public",
        workspace: "~/.openclaw/workspace-public",
        sandbox: { mode: "all", scope: "agent", workspaceAccess: "none" },
        tools: {
          allow: [
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
            "whatsapp",
            "telegram",
            "slack",
            "discord",
            "gateway",
          ],
          deny: [
            "read",
            "write",
            "edit",
            "apply_patch",
            "exec",
            "process",
            "browser",
            "canvas",
            "nodes",
            "cron",
            "gateway",
            "image",
          ],
        },
      },
    ],
  },
}
```

</Accordion>

Voir [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools) pour les détails de précédence.

---

## Session

```json5
{
  session: {
    scope: "per-sender",
    dmScope: "main", // main | per-peer | per-channel-peer | per-account-channel-peer
    identityLinks: {
      alice: ["telegram:123456789", "discord:987654321012345678"],
    },
    reset: {
      mode: "daily", // daily | idle
      atHour: 4,
      idleMinutes: 60,
    },
    resetByType: {
      thread: { mode: "daily", atHour: 4 },
      direct: { mode: "idle", idleMinutes: 240 },
      group: { mode: "idle", idleMinutes: 120 },
    },
    resetTriggers: ["/new", "/reset"],
    store: "~/.openclaw/agents/{agentId}/sessions/sessions.json",
    parentForkMaxTokens: 100000, // skip parent-thread fork above this token count (0 disables)
    maintenance: {
      mode: "warn", // warn | enforce
      pruneAfter: "30d",
      maxEntries: 500,
      rotateBytes: "10mb",
      resetArchiveRetention: "30d", // duration or false
      maxDiskBytes: "500mb", // optional hard budget
      highWaterBytes: "400mb", // optional cleanup target
    },
    threadBindings: {
      enabled: true,
      idleHours: 24, // default inactivity auto-unfocus in hours (`0` disables)
      maxAgeHours: 0, // default hard max age in hours (`0` disables)
    },
    mainKey: "main", // legacy (runtime always uses "main")
    agentToAgent: { maxPingPongTurns: 5 },
    sendPolicy: {
      rules: [{ action: "deny", match: { channel: "discord", chatType: "group" } }],
      default: "allow",
    },
  },
}
```

<Accordion title="Détails des champs de session">

- **`dmScope`** : comment les DM sont regroupés.
  - `main` : tous les DM partagent la session principale.
  - `per-peer` : isoler par ID d'expéditeur sur les canaux.
  - `per-channel-peer` : isoler par canal + expéditeur (recommandé pour les boîtes de réception multi-utilisateurs).
  - `per-account-channel-peer` : isoler par compte + canal + expéditeur (recommandé pour multi-compte).
- **`identityLinks`** : mapper les ID canoniques aux pairs préfixés par fournisseur pour le partage de session inter-canaux.
- **`reset`** : politique de réinitialisation principale. `daily` réinitialise à `atHour` heure locale ; `idle` réinitialise après `idleMinutes`. Lorsque les deux sont configurés, celui qui expire en premier gagne.
- **`resetByType`** : remplacements par type (`direct`, `group`, `thread`). L'alias hérité `dm` accepté pour `direct`.
- **`parentForkMaxTokens`** : max `totalTokens` de session parent autorisé lors de la création d'une session de thread forké (par défaut `100000`).
  - Si `totalTokens` parent est au-dessus de cette valeur, OpenClaw démarre une nouvelle session de thread au lieu d'hériter de l'historique de transcription parent.
  - Définissez `0` pour désactiver cette protection et toujours autoriser le forking parent.
- **`mainKey`** : champ hérité. Le runtime utilise maintenant toujours `"main"` pour le bucket de chat direct principal.
- **`sendPolicy`** : correspondance par `channel`, `chatType` (`direct|group|channel`, avec alias hérité `dm`), `keyPrefix`, ou `rawKeyPrefix`. Le premier refus gagne.
- **`maintenance`** : nettoyage du magasin de session + contrôles de rétention.
  - `mode` : `warn` émet uniquement des avertissements ; `enforce` applique le nettoyage.
  - `pruneAfter` : seuil d'âge pour les entrées obsolètes (par défaut `30d`).
  - `maxEntries` : nombre maximum d'entrées dans `sessions.json` (par défaut `500`).
  - `rotateBytes` : faire pivoter `sessions.json` lorsqu'il dépasse cette taille (par défaut `10mb`).
  - `resetArchiveRetention` : rétention pour les archives de transcription `*.reset.<timestamp>`. Par défaut à `pruneAfter` ; définissez `false` pour désactiver.
  - `maxDiskBytes` : budget disque optionnel du répertoire des sessions. En mode `warn`, il enregistre les avertissements ; en mode `enforce`, il supprime d'abord les artefacts/sessions les plus anciens.
  - `highWaterBytes` : cible optionnelle après nettoyage du budget. Par défaut à `80%` de `maxDiskBytes`.
- **`threadBindings`** : valeurs par défaut globales pour les fonctionnalités de session liées aux threads.
  - `enabled` : commutateur par défaut maître (les fournisseurs peuvent remplacer ; Discord utilise `channels.discord.threadBindings.enabled`)
  - `idleHours` : défaut d'inactivité auto-unfocus en heures (`0` désactive ; les fournisseurs peuvent remplacer)
  - `maxAgeHours` : âge maximum par défaut en heures (`0` désactive ; les fournisseurs peuvent remplacer)

</Accordion>

---

## Messages

```json5
{
  messages: {
    responsePrefix: "🦞", // or "auto"
    ackReaction: "👀",
    ackReactionScope: "group-mentions", // group-mentions | group-all | direct | all
    removeAckAfterReply: false,
    queue: {
      mode: "collect", // steer | followup | collect | steer-backlog | steer+backlog | queue | interrupt
      debounceMs: 1000,
      cap: 20,
      drop: "summarize", // old | new | summarize
      byChannel: {
        whatsapp: "collect",
        telegram: "collect",
      },
    },
    inbound: {
      debounceMs: 2000, // 0 disables
      byChannel: {
        whatsapp: 5000,
        slack: 1500,
      },
    },
  },
}
```

### Préfixe de réponse

Remplacements par canal/compte : `channels.<channel>.responsePrefix`, `channels.<channel>.accounts.<id>.responsePrefix`.

Résolution (le plus spécifique gagne) : compte → canal → global. `""` désactive et arrête la cascade. `"auto"` dérive `[{identity.name}]`.

**Variables de modèle :**

| Variable          | Description            | Exemple                     |
| ----------------- | ---------------------- | --------------------------- |
| `{model}`         | Nom court du modèle    | `claude-opus-4-6`           |
| `{modelFull}`     | Identifiant complet du modèle | `anthropic/claude-opus-4-6` |
| `{provider}`      | Nom du fournisseur     | `anthropic`                 |
| `{thinkingLevel}` | Niveau de réflexion actuel | `high`, `low`, `off`        |
| `{identity.name}` | Nom d'identité de l'agent | (identique à `"auto"`)      |

Les variables sont insensibles à la casse. `{think}` est un alias pour `{thinkingLevel}`.

### Réaction d'accusé de réception

- Par défaut à `identity.emoji` de l'agent actif, sinon `"👀"`. Définissez `""` pour désactiver.
- Remplacements par canal : `channels.<channel>.ackReaction`, `channels.<channel>.accounts.<id>.ackReaction`.
- Ordre de résolution : compte → canal → `messages.ackReaction` → fallback d'identité.
- Portée : `group-mentions` (par défaut), `group-all`, `direct`, `all`.
- `removeAckAfterReply` : supprime l'accusé de réception après la réponse (Slack/Discord/Telegram/Google Chat uniquement).

### Débounce entrant

Regroupe les messages texte rapides du même expéditeur en un seul tour d'agent. Les médias/pièces jointes se vident immédiatement. Les commandes de contrôle contournent le débounce.

### TTS (synthèse vocale)

```json5
{
  messages: {
    tts: {
      auto: "always", // off | always | inbound | tagged
      mode: "final", // final | all
      provider: "elevenlabs",
      summaryModel: "openai/gpt-4.1-mini",
      modelOverrides: { enabled: true },
      maxTextLength: 4000,
      timeoutMs: 30000,
      prefsPath: "~/.openclaw/settings/tts.json",
      elevenlabs: {
        apiKey: "elevenlabs_api_key",
        baseUrl: "https://api.elevenlabs.io",
        voiceId: "voice_id",
        modelId: "eleven_multilingual_v2",
        seed: 42,
        applyTextNormalization: "auto",
        languageCode: "en",
        voiceSettings: {
          stability: 0.5,
          similarityBoost: 0.75,
          style: 0.0,
          useSpeakerBoost: true,
          speed: 1.0,
        },
      },
      openai: {
        apiKey: "openai_api_key",
        baseUrl: "https://api.openai.com/v1",
        model: "gpt-4o-mini-tts",
        voice: "alloy",
      },
    },
  },
}
```

- `auto` contrôle le TTS automatique. `/tts off|always|inbound|tagged` remplace par session.
- `summaryModel` remplace `agents.defaults.model.primary` pour le résumé automatique.
- `modelOverrides` est activé par défaut ; `modelOverrides.allowProvider` par défaut à `false` (opt-in).
- Les clés API reviennent à `ELEVENLABS_API_KEY`/`XI_API_KEY` et `OPENAI_API_KEY`.
- `openai.baseUrl` remplace le point de terminaison OpenAI TTS. L'ordre de résolution est config, puis `OPENAI_TTS_BASE_URL`, puis `https://api.openai.com/v1`.
- Lorsque `openai.baseUrl` pointe vers un point de terminaison non-OpenAI, OpenClaw le traite comme un serveur TTS compatible OpenAI et assouplit la validation du modèle/voix.

---

## Talk

Valeurs par défaut pour le mode Talk (macOS/iOS/Android).

```json5
{
  talk: {
    voiceId: "elevenlabs_voice_id",
    voiceAliases: {
      Clawd: "EXAVITQu4vr4xnSDxMaL",
      Roger: "CwhRBWXzGAHq8TQ4Fs17",
    },
    modelId: "eleven_v3",
    outputFormat: "mp3_44100_128",
    apiKey: "elevenlabs_api_key",
    silenceTimeoutMs: 1500,
    interruptOnSpeech: true,
  },
}
```

- Les ID de voix reviennent à `ELEVENLABS_VOICE_ID` ou `SAG_VOICE_ID`.
- `apiKey` et `providers.*.apiKey` acceptent les chaînes en texte brut ou les objets SecretRef.
- Le fallback `ELEVENLABS_API_KEY` s'applique uniquement lorsqu'aucune clé API Talk n'est configurée.
- `voiceAliases` permet aux directives Talk d'utiliser des noms conviviaux.
- `silenceTimeoutMs` contrôle combien de temps le mode Talk attend après le silence de l'utilisateur avant d'envoyer la transcription. Non défini conserve la fenêtre de pause par défaut de la plateforme (`700 ms sur macOS et Android, 900 ms sur iOS`).

## Outils

### Profils d'outils

`tools.profile` définit une liste d'autorisation de base avant `tools.allow`/`tools.deny` :

L'intégration locale par défaut définit les nouvelles configurations locales sur `tools.profile: "coding"` lorsqu'elles ne sont pas définies (les profils explicites existants sont conservés).

| Profil      | Inclut                                                                                    |
| ----------- | ----------------------------------------------------------------------------------------- |
| `minimal`   | `session_status` uniquement                                                               |
| `coding`    | `group:fs`, `group:runtime`, `group:sessions`, `group:memory`, `image`                    |
| `messaging` | `group:messaging`, `sessions_list`, `sessions_history`, `sessions_send`, `session_status` |
| `full`      | Aucune restriction (identique à non défini)                                               |

### Groupes d'outils

| Groupe             | Outils                                                                                   |
| ------------------ | ---------------------------------------------------------------------------------------- |
| `group:runtime`    | `exec`, `process` (`bash` est accepté comme alias pour `exec`)                            |
| `group:fs`         | `read`, `write`, `edit`, `apply_patch`                                                   |
| `group:sessions`   | `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status` |
| `group:memory`     | `memory_search`, `memory_get`                                                            |
| `group:web`        | `web_search`, `web_fetch`                                                                |
| `group:ui`         | `browser`, `canvas`                                                                      |
| `group:automation` | `cron`, `gateway`                                                                        |
| `group:messaging`  | `message`                                                                                |
| `group:nodes`      | `nodes`                                                                                  |
| `group:openclaw`   | Tous les outils intégrés (exclut les plugins de fournisseur)                             |

### `tools.allow` / `tools.deny`

Politique d'autorisation/refus d'outils globale (le refus l'emporte). Insensible à la casse, supporte les caractères génériques `*`. Appliqué même lorsque le bac à sable Docker est désactivé.

```json5
{
  tools: { deny: ["browser", "canvas"] },
}
```

### `tools.byProvider`

Restreindre davantage les outils pour des fournisseurs ou modèles spécifiques. Ordre : profil de base → profil de fournisseur → allow/deny.

```json5
{
  tools: {
    profile: "coding",
    byProvider: {
      "google-antigravity": { profile: "minimal" },
      "openai/gpt-5.2": { allow: ["group:fs", "sessions_list"] },
    },
  },
}
```

### `tools.elevated`

Contrôle l'accès exec élevé (hôte) :

```json5
{
  tools: {
    elevated: {
      enabled: true,
      allowFrom: {
        whatsapp: ["+15555550123"],
        discord: ["1234567890123", "987654321098765432"],
      },
    },
  },
}
```

- Le remplacement par agent (`agents.list[].tools.elevated`) ne peut que restreindre davantage.
- `/elevated on|off|ask|full` stocke l'état par session ; les directives en ligne s'appliquent à un seul message.
- L'exec élevé s'exécute sur l'hôte, contourne le bac à sable.

### `tools.exec`

```json5
{
  tools: {
    exec: {
      backgroundMs: 10000,
      timeoutSec: 1800,
      cleanupMs: 1800000,
      notifyOnExit: true,
      notifyOnExitEmptySuccess: false,
      applyPatch: {
        enabled: false,
        allowModels: ["gpt-5.2"],
      },
    },
  },
}
```

### `tools.loopDetection`

Les vérifications de sécurité des boucles d'outils sont **désactivées par défaut**. Définissez `enabled: true` pour activer la détection.
Les paramètres peuvent être définis globalement dans `tools.loopDetection` et remplacés par agent à `agents.list[].tools.loopDetection`.

```json5
{
  tools: {
    loopDetection: {
      enabled: true,
      historySize: 30,
      warningThreshold: 10,
      criticalThreshold: 20,
      globalCircuitBreakerThreshold: 30,
      detectors: {
        genericRepeat: true,
        knownPollNoProgress: true,
        pingPong: true,
      },
    },
  },
}
```

- `historySize` : historique maximal des appels d'outils conservé pour l'analyse des boucles.
- `warningThreshold` : seuil de motif sans progression répétée pour les avertissements.
- `criticalThreshold` : seuil de répétition plus élevé pour bloquer les boucles critiques.
- `globalCircuitBreakerThreshold` : seuil d'arrêt dur pour toute exécution sans progression.
- `detectors.genericRepeat` : avertir sur les appels répétés du même outil/mêmes arguments.
- `detectors.knownPollNoProgress` : avertir/bloquer sur les outils d'interrogation connus (`process.poll`, `command_status`, etc.).
- `detectors.pingPong` : avertir/bloquer sur les motifs de paires alternées sans progression.
- Si `warningThreshold >= criticalThreshold` ou `criticalThreshold >= globalCircuitBreakerThreshold`, la validation échoue.

### `tools.web`

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        apiKey: "brave_api_key", // ou BRAVE_API_KEY env
        maxResults: 5,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
      },
      fetch: {
        enabled: true,
        maxChars: 50000,
        maxCharsCap: 50000,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
        userAgent: "custom-ua",
      },
    },
  },
}
```

### `tools.media`

Configure la compréhension des médias entrants (image/audio/vidéo) :

```json5
{
  tools: {
    media: {
      concurrency: 2,
      audio: {
        enabled: true,
        maxBytes: 20971520,
        scope: {
          default: "deny",
          rules: [{ action: "allow", match: { chatType: "direct" } }],
        },
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          { type: "cli", command: "whisper", args: ["--model", "base", "{{MediaPath}}"] },
        ],
      },
      video: {
        enabled: true,
        maxBytes: 52428800,
        models: [{ provider: "google", model: "gemini-3-flash-preview" }],
      },
    },
  },
}
```

<Accordion title="Champs d'entrée du modèle média">

**Entrée de fournisseur** (`type: "provider"` ou omis) :

- `provider` : identifiant du fournisseur API (`openai`, `anthropic`, `google`/`gemini`, `groq`, etc.)
- `model` : remplacement de l'identifiant du modèle
- `profile` / `preferredProfile` : sélection du profil `auth-profiles.json`

**Entrée CLI** (`type: "cli"`) :

- `command` : exécutable à exécuter
- `args` : arguments modélisés (supporte `{{MediaPath}}`, `{{Prompt}}`, `{{MaxChars}}`, etc.)

**Champs communs :**

- `capabilities` : liste optionnelle (`image`, `audio`, `video`). Valeurs par défaut : `openai`/`anthropic`/`minimax` → image, `google` → image+audio+vidéo, `groq` → audio.
- `prompt`, `maxChars`, `maxBytes`, `timeoutSeconds`, `language` : remplacements par entrée.
- Les défaillances reviennent à l'entrée suivante.

L'authentification du fournisseur suit l'ordre standard : `auth-profiles.json` → variables env → `models.providers.*.apiKey`.

</Accordion>

### `tools.agentToAgent`

```json5
{
  tools: {
    agentToAgent: {
      enabled: false,
      allow: ["home", "work"],
    },
  },
}
```

### `tools.sessions`

Contrôle les sessions qui peuvent être ciblées par les outils de session (`sessions_list`, `sessions_history`, `sessions_send`).

Par défaut : `tree` (session actuelle + sessions générées par celle-ci, comme les sous-agents).

```json5
{
  tools: {
    sessions: {
      // "self" | "tree" | "agent" | "all"
      visibility: "tree",
    },
  },
}
```

Notes :

- `self` : uniquement la clé de session actuelle.
- `tree` : session actuelle + sessions générées par la session actuelle (sous-agents).
- `agent` : toute session appartenant à l'identifiant d'agent actuel (peut inclure d'autres utilisateurs si vous exécutez des sessions par expéditeur sous le même identifiant d'agent).
- `all` : toute session. Le ciblage entre agents nécessite toujours `tools.agentToAgent`.
- Serrage du bac à sable : lorsque la session actuelle est en bac à sable et `agents.defaults.sandbox.sessionToolsVisibility="spawned"`, la visibilité est forcée à `tree` même si `tools.sessions.visibility="all"`.

### `tools.sessions_spawn`

Contrôle le support des pièces jointes en ligne pour `sessions_spawn`.

```json5
{
  tools: {
    sessions_spawn: {
      attachments: {
        enabled: false, // opt-in : définissez true pour autoriser les pièces jointes de fichiers en ligne
        maxTotalBytes: 5242880, // 5 Mo au total sur tous les fichiers
        maxFiles: 50,
        maxFileBytes: 1048576, // 1 Mo par fichier
        retainOnSessionKeep: false, // conserver les pièces jointes lorsque cleanup="keep"
      },
    },
  },
}
```

Notes :

- Les pièces jointes ne sont supportées que pour `runtime: "subagent"`. Le runtime ACP les rejette.
- Les fichiers sont matérialisés dans l'espace de travail enfant à `.openclaw/attachments/<uuid>/` avec un `.manifest.json`.
- Le contenu des pièces jointes est automatiquement supprimé de la persistance des transcriptions.
- Les entrées Base64 sont validées avec des vérifications strictes d'alphabet/remplissage et une garde de taille avant décodage.
- Les permissions des fichiers sont `0700` pour les répertoires et `0600` pour les fichiers.
- Le nettoyage suit la politique `cleanup` : `delete` supprime toujours les pièces jointes ; `keep` les conserve uniquement lorsque `retainOnSessionKeep: true`.

### `tools.subagents`

```json5
{
  agents: {
    defaults: {
      subagents: {
        model: "minimax/MiniMax-M2.5",
        maxConcurrent: 1,
        runTimeoutSeconds: 900,
        archiveAfterMinutes: 60,
      },
    },
  },
}
```

- `model` : modèle par défaut pour les sous-agents générés. S'il est omis, les sous-agents héritent du modèle de l'appelant.
- `runTimeoutSeconds` : délai d'expiration par défaut (secondes) pour `sessions_spawn` lorsque l'appel d'outil omet `runTimeoutSeconds`. `0` signifie pas de délai d'expiration.
- Politique d'outils par sous-agent : `tools.subagents.tools.allow` / `tools.subagents.tools.deny`.

## Fournisseurs personnalisés et URLs de base

OpenClaw utilise le catalogue de modèles pi-coding-agent. Ajoutez des fournisseurs personnalisés via `models.providers` dans la config ou `~/.openclaw/agents/<agentId>/agent/models.json`.

```json5
{
  models: {
    mode: "merge", // merge (default) | replace
    providers: {
      "custom-proxy": {
        baseUrl: "http://localhost:4000/v1",
        apiKey: "LITELLM_KEY",
        api: "openai-completions", // openai-completions | openai-responses | anthropic-messages | google-generative-ai
        models: [
          {
            id: "llama-3.1-8b",
            name: "Llama 3.1 8B",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            maxTokens: 32000,
          },
        ],
      },
    },
  },
}
```

- Utilisez `authHeader: true` + `headers` pour les besoins d'authentification personnalisés.
- Remplacez la racine de la config de l'agent avec `OPENCLAW_AGENT_DIR` (ou `PI_CODING_AGENT_DIR`).
- Ordre de fusion pour les IDs de fournisseur correspondants :
  - Les valeurs `baseUrl` non vides dans `models.json` de l'agent gagnent.
  - Les valeurs `apiKey` non vides de l'agent gagnent uniquement lorsque ce fournisseur n'est pas géré par SecretRef dans le contexte de config/profil d'authentification actuel.
  - Les valeurs `apiKey` du fournisseur gérées par SecretRef sont actualisées à partir des marqueurs source (`ENV_VAR_NAME` pour les références env, `secretref-managed` pour les références fichier/exec) au lieu de persister les secrets résolus.
  - Les valeurs d'en-tête du fournisseur gérées par SecretRef sont actualisées à partir des marqueurs source (`secretref-env:ENV_VAR_NAME` pour les références env, `secretref-managed` pour les références fichier/exec).
  - Les `apiKey`/`baseUrl` vides ou manquants de l'agent reviennent à `models.providers` dans la config.
  - Les `contextWindow`/`maxTokens` de modèle correspondants utilisent la valeur la plus élevée entre la config explicite et les valeurs du catalogue implicite.
  - Utilisez `models.mode: "replace"` lorsque vous voulez que la config réécrive complètement `models.json`.
  - La persistance des marqueurs est source-autoritaire : les marqueurs sont écrits à partir de l'instantané de config source actif (pré-résolution), pas à partir des valeurs de secret runtime résolues.

### Détails des champs du fournisseur

- `models.mode` : comportement du catalogue du fournisseur (`merge` ou `replace`).
- `models.providers` : carte de fournisseur personnalisé indexée par ID de fournisseur.
- `models.providers.*.api` : adaptateur de requête (`openai-completions`, `openai-responses`, `anthropic-messages`, `google-generative-ai`, etc).
- `models.providers.*.apiKey` : identifiant du fournisseur (préférez la substitution SecretRef/env).
- `models.providers.*.auth` : stratégie d'authentification (`api-key`, `token`, `oauth`, `aws-sdk`).
- `models.providers.*.injectNumCtxForOpenAICompat` : pour Ollama + `openai-completions`, injectez `options.num_ctx` dans les requêtes (défaut : `true`).
- `models.providers.*.authHeader` : forcez le transport des identifiants dans l'en-tête `Authorization` si nécessaire.
- `models.providers.*.baseUrl` : URL de base de l'API en amont.
- `models.providers.*.headers` : en-têtes statiques supplémentaires pour le routage proxy/tenant.
- `models.providers.*.models` : entrées du catalogue de modèles explicites du fournisseur.
- `models.providers.*.models.*.compat.supportsDeveloperRole` : indice de compatibilité optionnel. Pour `api: "openai-completions"` avec un `baseUrl` non vide et non natif (hôte pas `api.openai.com`), OpenClaw force ceci à `false` à l'exécution. Un `baseUrl` vide/omis conserve le comportement OpenAI par défaut.
- `models.bedrockDiscovery` : racine des paramètres de découverte automatique Bedrock.
- `models.bedrockDiscovery.enabled` : activez/désactivez l'interrogation de découverte.
- `models.bedrockDiscovery.region` : région AWS pour la découverte.
- `models.bedrockDiscovery.providerFilter` : filtre d'ID de fournisseur optionnel pour la découverte ciblée.
- `models.bedrockDiscovery.refreshInterval` : intervalle d'interrogation pour l'actualisation de la découverte.
- `models.bedrockDiscovery.defaultContextWindow` : fenêtre de contexte de secours pour les modèles découverts.
- `models.bedrockDiscovery.defaultMaxTokens` : jetons de sortie max de secours pour les modèles découverts.

### Exemples de fournisseurs

<Accordion title="Cerebras (GLM 4.6 / 4.7)">

```json5
{
  env: { CEREBRAS_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: {
        primary: "cerebras/zai-glm-4.7",
        fallbacks: ["cerebras/zai-glm-4.6"],
      },
      models: {
        "cerebras/zai-glm-4.7": { alias: "GLM 4.7 (Cerebras)" },
        "cerebras/zai-glm-4.6": { alias: "GLM 4.6 (Cerebras)" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      cerebras: {
        baseUrl: "https://api.cerebras.ai/v1",
        apiKey: "${CEREBRAS_API_KEY}",
        api: "openai-completions",
        models: [
          { id: "zai-glm-4.7", name: "GLM 4.7 (Cerebras)" },
          { id: "zai-glm-4.6", name: "GLM 4.6 (Cerebras)" },
        ],
      },
    },
  },
}
```

Utilisez `cerebras/zai-glm-4.7` pour Cerebras ; `zai/glm-4.7` pour Z.AI direct.

</Accordion>

<Accordion title="OpenCode">

```json5
{
  agents: {
    defaults: {
      model: { primary: "opencode/claude-opus-4-6" },
      models: { "opencode/claude-opus-4-6": { alias: "Opus" } },
    },
  },
}
```

Définissez `OPENCODE_API_KEY` (ou `OPENCODE_ZEN_API_KEY`). Utilisez les références `opencode/...` pour le catalogue Zen ou `opencode-go/...` pour le catalogue Go. Raccourci : `openclaw onboard --auth-choice opencode-zen` ou `openclaw onboard --auth-choice opencode-go`.

</Accordion>

<Accordion title="Z.AI (GLM-4.7)">

```json5
{
  agents: {
    defaults: {
      model: { primary: "zai/glm-4.7" },
      models: { "zai/glm-4.7": {} },
    },
  },
}
```

Définissez `ZAI_API_KEY`. Les alias `z.ai/*` et `z-ai/*` sont acceptés. Raccourci : `openclaw onboard --auth-choice zai-api-key`.

- Point de terminaison général : `https://api.z.ai/api/paas/v4`
- Point de terminaison de codage (par défaut) : `https://api.z.ai/api/coding/paas/v4`
- Pour le point de terminaison général, définissez un fournisseur personnalisé avec le remplacement d'URL de base.

</Accordion>

<Accordion title="Moonshot AI (Kimi)">

```json5
{
  env: { MOONSHOT_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "moonshot/kimi-k2.5" },
      models: { "moonshot/kimi-k2.5": { alias: "Kimi K2.5" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "kimi-k2.5",
            name: "Kimi K2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Pour le point de terminaison China : `baseUrl: "https://api.moonshot.cn/v1"` ou `openclaw onboard --auth-choice moonshot-api-key-cn`.

</Accordion>

<Accordion title="Kimi Coding">

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "kimi-coding/k2p5" },
      models: { "kimi-coding/k2p5": { alias: "Kimi K2.5" } },
    },
  },
}
```

Compatible avec Anthropic, fournisseur intégré. Raccourci : `openclaw onboard --auth-choice kimi-code-api-key`.

</Accordion>

<Accordion title="Synthetic (compatible Anthropic)">

```json5
{
  env: { SYNTHETIC_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.5" },
      models: { "synthetic/hf:MiniMaxAI/MiniMax-M2.5": { alias: "MiniMax M2.5" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "hf:MiniMaxAI/MiniMax-M2.5",
            name: "MiniMax M2.5",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 192000,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

L'URL de base doit omettre `/v1` (le client Anthropic l'ajoute). Raccourci : `openclaw onboard --auth-choice synthetic-api-key`.

</Accordion>

<Accordion title="MiniMax M2.5 (direct)">

```json5
{
  agents: {
    defaults: {
      model: { primary: "minimax/MiniMax-M2.5" },
      models: {
        "minimax/MiniMax-M2.5": { alias: "Minimax" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      minimax: {
        baseUrl: "https://api.minimax.io/anthropic",
        apiKey: "${MINIMAX_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "MiniMax-M2.5",
            name: "MiniMax M2.5",
            reasoning: true,
            input: ["text"],
            cost: { input: 15, output: 60, cacheRead: 2, cacheWrite: 10 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Définissez `MINIMAX_API_KEY`. Raccourci : `openclaw onboard --auth-choice minimax-api`.

</Accordion>

<Accordion title="Modèles locaux (LM Studio)">

Voir [Local Models](/gateway/local-models). TL;DR : exécutez MiniMax M2.5 via l'API LM Studio Responses sur du matériel sérieux ; conservez les modèles hébergés fusionnés pour la solution de secours.

</Accordion>

---

## Compétences

```json5
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills"],
    },
    install: {
      preferBrew: true,
      nodeManager: "npm", // npm | pnpm | yarn
    },
    entries: {
      "nano-banana-pro": {
        apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" }, // or plaintext string
        env: { GEMINI_API_KEY: "GEMINI_KEY_HERE" },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

- `allowBundled` : liste d'autorisation optionnelle pour les compétences groupées uniquement (les compétences gérées/workspace ne sont pas affectées).
- `entries.<skillKey>.enabled: false` désactive une compétence même si elle est groupée/installée.
- `entries.<skillKey>.apiKey` : commodité pour les compétences déclarant une variable env principale (chaîne en texte brut ou objet SecretRef).

---

## Plugins

```json5
{
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    deny: [],
    load: {
      paths: ["~/Projects/oss/voice-call-extension"],
    },
    entries: {
      "voice-call": {
        enabled: true,
        hooks: {
          allowPromptInjection: false,
        },
        config: { provider: "twilio" },
      },
    },
  },
}
```

- Chargés à partir de `~/.openclaw/extensions`, `<workspace>/.openclaw/extensions`, plus `plugins.load.paths`.
- **Les modifications de config nécessitent un redémarrage de la passerelle.**
- `allow` : liste d'autorisation optionnelle (seuls les plugins listés se chargent). `deny` gagne.
- `plugins.entries.<id>.apiKey` : champ de commodité de clé API au niveau du plugin (lorsqu'il est supporté par le plugin).
- `plugins.entries.<id>.env` : carte de variables env au niveau du plugin.
- `plugins.entries.<id>.hooks.allowPromptInjection` : lorsque `false`, le noyau bloque `before_prompt_build` et ignore les champs mutant le prompt de `before_agent_start` hérité, tout en préservant `modelOverride` et `providerOverride` hérités.
- `plugins.entries.<id>.config` : objet de config défini par le plugin (validé par le schéma du plugin).
- `plugins.slots.memory` : choisissez l'ID du plugin de mémoire actif, ou `"none"` pour désactiver les plugins de mémoire.
- `plugins.slots.contextEngine` : choisissez l'ID du plugin de moteur de contexte actif ; par défaut `"legacy"` sauf si vous installez et sélectionnez un autre moteur.
- `plugins.installs` : métadonnées d'installation gérées par CLI utilisées par `openclaw plugins update`.
  - Inclut `source`, `spec`, `sourcePath`, `installPath`, `version`, `resolvedName`, `resolvedVersion`, `resolvedSpec`, `integrity`, `shasum`, `resolvedAt`, `installedAt`.
  - Traitez `plugins.installs.*` comme un état géré ; préférez les commandes CLI aux modifications manuelles.

Voir [Plugins](/tools/plugin).

## Navigateur

```json5
{
  browser: {
    enabled: true,
    evaluateEnabled: true,
    defaultProfile: "user",
    ssrfPolicy: {
      dangerouslyAllowPrivateNetwork: true, // mode réseau de confiance par défaut
      // allowPrivateNetwork: true, // alias hérité
      // hostnameAllowlist: ["*.example.com", "example.com"],
      // allowedHostnames: ["localhost"],
    },
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC" },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
    },
    color: "#FF4500",
    // headless: false,
    // noSandbox: false,
    // extraArgs: [],
    // relayBindHost: "0.0.0.0", // uniquement quand le relais d'extension doit être accessible entre espaces de noms (par exemple WSL2)
    // executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    // attachOnly: false,
  },
}
```

- `evaluateEnabled: false` désactive `act:evaluate` et `wait --fn`.
- `ssrfPolicy.dangerouslyAllowPrivateNetwork` est défini par défaut à `true` quand non spécifié (modèle réseau de confiance).
- Définissez `ssrfPolicy.dangerouslyAllowPrivateNetwork: false` pour une navigation navigateur stricte publique uniquement.
- `ssrfPolicy.allowPrivateNetwork` reste supporté comme alias hérité.
- En mode strict, utilisez `ssrfPolicy.hostnameAllowlist` et `ssrfPolicy.allowedHostnames` pour les exceptions explicites.
- Les profils distants sont en mode attachement uniquement (démarrage/arrêt/réinitialisation désactivés).
- Ordre de détection automatique : navigateur par défaut si basé sur Chromium → Chrome → Brave → Edge → Chromium → Chrome Canary.
- Service de contrôle : loopback uniquement (port dérivé de `gateway.port`, par défaut `18791`).
- `extraArgs` ajoute des drapeaux de lancement supplémentaires au démarrage local de Chromium (par exemple `--disable-gpu`, dimensionnement de fenêtre, ou drapeaux de débogage).
- `relayBindHost` change où le relais d'extension Chrome écoute. Laissez non défini pour un accès loopback uniquement ; définissez une adresse de liaison explicite non-loopback comme `0.0.0.0` uniquement quand le relais doit traverser une limite d'espace de noms (par exemple WSL2) et le réseau hôte est déjà de confiance.

---

## Interface utilisateur

```json5
{
  ui: {
    seamColor: "#FF4500",
    assistant: {
      name: "OpenClaw",
      avatar: "CB", // emoji, texte court, URL d'image, ou data URI
    },
  },
}
```

- `seamColor` : couleur d'accent pour le chrome de l'interface utilisateur de l'application native (teinte de bulle du mode Talk, etc.).
- `assistant` : remplacement du contrôle d'identité de l'interface utilisateur. Revient à l'identité de l'agent actif.

---

## Passerelle

```json5
{
  gateway: {
    mode: "local", // local | remote
    port: 18789,
    bind: "loopback",
    auth: {
      mode: "token", // none | token | password | trusted-proxy
      token: "your-token",
      // password: "your-password", // ou OPENCLAW_GATEWAY_PASSWORD
      // trustedProxy: { userHeader: "x-forwarded-user" }, // pour mode=trusted-proxy ; voir /gateway/trusted-proxy-auth
      allowTailscale: true,
      rateLimit: {
        maxAttempts: 10,
        windowMs: 60000,
        lockoutMs: 300000,
        exemptLoopback: true,
      },
    },
    tailscale: {
      mode: "off", // off | serve | funnel
      resetOnExit: false,
    },
    controlUi: {
      enabled: true,
      basePath: "/openclaw",
      // root: "dist/control-ui",
      // allowedOrigins: ["https://control.example.com"], // requis pour Control UI non-loopback
      // dangerouslyAllowHostHeaderOriginFallback: false, // mode de secours d'origine d'en-tête Host dangereux
      // allowInsecureAuth: false,
      // dangerouslyDisableDeviceAuth: false,
    },
    remote: {
      url: "ws://gateway.tailnet:18789",
      transport: "ssh", // ssh | direct
      token: "your-token",
      // password: "your-password",
    },
    trustedProxies: ["10.0.0.1"],
    // Optionnel. Faux par défaut.
    allowRealIpFallback: false,
    tools: {
      // Refus HTTP supplémentaires pour /tools/invoke
      deny: ["browser"],
      // Supprimer les outils de la liste de refus HTTP par défaut
      allow: ["gateway"],
    },
    push: {
      apns: {
        relay: {
          baseUrl: "https://relay.example.com",
          timeoutMs: 10000,
        },
      },
    },
  },
}
```

<Accordion title="Détails des champs de la passerelle">

- `mode` : `local` (exécuter la passerelle) ou `remote` (se connecter à une passerelle distante). La passerelle refuse de démarrer sauf si `local`.
- `port` : port multiplexé unique pour WS + HTTP. Précédence : `--port` > `OPENCLAW_GATEWAY_PORT` > `gateway.port` > `18789`.
- `bind` : `auto`, `loopback` (par défaut), `lan` (`0.0.0.0`), `tailnet` (IP Tailscale uniquement), ou `custom`.
- **Alias de liaison hérités** : utilisez les valeurs de mode de liaison dans `gateway.bind` (`auto`, `loopback`, `lan`, `tailnet`, `custom`), pas les alias d'hôte (`0.0.0.0`, `127.0.0.1`, `localhost`, `::`, `::1`).
- **Note Docker** : la liaison `loopback` par défaut écoute sur `127.0.0.1` à l'intérieur du conteneur. Avec la mise en réseau Docker bridge (`-p 18789:18789`), le trafic arrive sur `eth0`, donc la passerelle est inaccessible. Utilisez `--network host`, ou définissez `bind: "lan"` (ou `bind: "custom"` avec `customBindHost: "0.0.0.0"`) pour écouter sur toutes les interfaces.
- **Auth** : requis par défaut. Les liaisons non-loopback nécessitent un jeton/mot de passe partagé. L'assistant d'intégration génère un jeton par défaut.
- Si à la fois `gateway.auth.token` et `gateway.auth.password` sont configurés (y compris SecretRefs), définissez `gateway.auth.mode` explicitement à `token` ou `password`. Les flux de démarrage et d'installation/réparation de service échouent quand les deux sont configurés et le mode n'est pas défini.
- `gateway.auth.mode: "none"` : mode explicite sans authentification. À utiliser uniquement pour les configurations loopback locales de confiance ; ceci n'est intentionnellement pas proposé par les invites d'intégration.
- `gateway.auth.mode: "trusted-proxy"` : déléguer l'authentification à un proxy inverse conscient de l'identité et faire confiance aux en-têtes d'identité de `gateway.trustedProxies` (voir [Authentification par proxy de confiance](/gateway/trusted-proxy-auth)).
- `gateway.auth.allowTailscale` : quand `true`, les en-têtes d'identité Tailscale Serve peuvent satisfaire l'authentification Control UI/WebSocket (vérifiée via `tailscale whois`) ; les points de terminaison API HTTP nécessitent toujours une authentification par jeton/mot de passe. Ce flux sans jeton suppose que l'hôte de la passerelle est de confiance. Par défaut `true` quand `tailscale.mode = "serve"`.
- `gateway.auth.rateLimit` : limiteur optionnel d'authentification échouée. S'applique par IP client et par portée d'authentification (secret partagé et jeton d'appareil sont suivis indépendamment). Les tentatives bloquées retournent `429` + `Retry-After`.
  - `gateway.auth.rateLimit.exemptLoopback` est par défaut `true` ; définissez `false` quand vous voulez intentionnellement que le trafic localhost soit aussi limité en débit (pour les configurations de test ou les déploiements de proxy stricts).
- Les tentatives d'authentification WS d'origine navigateur sont toujours limitées avec exemption loopback désactivée (défense en profondeur contre les attaques par force brute localhost basées sur navigateur).
- `tailscale.mode` : `serve` (tailnet uniquement, liaison loopback) ou `funnel` (public, nécessite authentification).
- `controlUi.allowedOrigins` : liste d'autorisation explicite d'origine navigateur pour les connexions WebSocket de la passerelle. Requis quand les clients navigateur sont attendus d'origines non-loopback.
- `controlUi.dangerouslyAllowHostHeaderOriginFallback` : mode dangereux qui active le secours d'origine d'en-tête Host pour les déploiements qui s'appuient intentionnellement sur la politique d'origine d'en-tête Host.
- `remote.transport` : `ssh` (par défaut) ou `direct` (ws/wss). Pour `direct`, `remote.url` doit être `ws://` ou `wss://`.
- `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` : remplacement de verre brisé côté client qui permet le texte brut `ws://` aux IPs de réseau privé de confiance ; le défaut reste loopback uniquement pour le texte brut.
- `gateway.remote.token` / `.password` sont des champs d'identifiants de client distant. Ils ne configurent pas l'authentification de la passerelle par eux-mêmes.
- `gateway.push.apns.relay.baseUrl` : URL HTTPS de base pour le relais APNs externe utilisé par les builds iOS officiels/TestFlight après qu'ils publient les enregistrements soutenus par relais à la passerelle. Cette URL doit correspondre à l'URL du relais compilée dans la build iOS.
- `gateway.push.apns.relay.timeoutMs` : délai d'expiration d'envoi passerelle-vers-relais en millisecondes. Par défaut `10000`.
- Les enregistrements soutenus par relais sont délégués à une identité de passerelle spécifique. L'application iOS appairée récupère `gateway.identity.get`, inclut cette identité dans l'enregistrement du relais, et transfère une subvention d'envoi à portée d'enregistrement à la passerelle. Une autre passerelle ne peut pas réutiliser cet enregistrement stocké.
- `OPENCLAW_APNS_RELAY_BASE_URL` / `OPENCLAW_APNS_RELAY_TIMEOUT_MS` : remplacements env temporaires pour la configuration du relais ci-dessus.
- `OPENCLAW_APNS_RELAY_ALLOW_HTTP=true` : trappe d'échappatoire de développement uniquement pour les URL de relais HTTP loopback. Les URL de relais de production doivent rester sur HTTPS.
- Les chemins d'appel de passerelle locale peuvent utiliser `gateway.remote.*` comme secours uniquement quand `gateway.auth.*` n'est pas défini.
- Si `gateway.auth.token` / `gateway.auth.password` est explicitement configuré via SecretRef et non résolu, la résolution échoue fermée (pas de secours distant masquant).
- `trustedProxies` : IPs de proxy inverse qui terminent TLS. Listez uniquement les proxies que vous contrôlez.
- `allowRealIpFallback` : quand `true`, la passerelle accepte `X-Real-IP` si `X-Forwarded-For` est manquant. Par défaut `false` pour un comportement d'échec fermé.
- `gateway.tools.deny` : noms d'outils supplémentaires bloqués pour HTTP `POST /tools/invoke` (étend la liste de refus par défaut).
- `gateway.tools.allow` : supprimer les noms d'outils de la liste de refus HTTP par défaut.

</Accordion>

### Points de terminaison compatibles OpenAI

- Chat Completions : désactivé par défaut. Activez avec `gateway.http.endpoints.chatCompletions.enabled: true`.
- API Responses : `gateway.http.endpoints.responses.enabled`.
- Durcissement d'entrée URL Responses :
  - `gateway.http.endpoints.responses.maxUrlParts`
  - `gateway.http.endpoints.responses.files.urlAllowlist`
  - `gateway.http.endpoints.responses.images.urlAllowlist`
- En-tête de durcissement de réponse optionnel :
  - `gateway.http.securityHeaders.strictTransportSecurity` (définissez uniquement pour les origines HTTPS que vous contrôlez ; voir [Authentification par proxy de confiance](/gateway/trusted-proxy-auth#tls-termination-and-hsts))

### Isolation multi-instance

Exécutez plusieurs passerelles sur un hôte avec des ports et des répertoires d'état uniques :

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json \
OPENCLAW_STATE_DIR=~/.openclaw-a \
openclaw gateway --port 19001
```

Drapeaux de commodité : `--dev` (utilise `~/.openclaw-dev` + port `19001`), `--profile <name>` (utilise `~/.openclaw-<name>`).

Voir [Plusieurs passerelles](/gateway/multiple-gateways).

---

## Hooks

```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
    maxBodyBytes: 262144,
    defaultSessionKey: "hook:ingress",
    allowRequestSessionKey: false,
    allowedSessionKeyPrefixes: ["hook:"],
    allowedAgentIds: ["hooks", "main"],
    presets: ["gmail"],
    transformsDir: "~/.openclaw/hooks/transforms",
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        agentId: "hooks",
        wakeMode: "now",
        name: "Gmail",
        sessionKey: "hook:gmail:{{messages[0].id}}",
        messageTemplate: "From: {{messages[0].from}}\nSubject: {{messages[0].subject}}\n{{messages[0].snippet}}",
        deliver: true,
        channel: "last",
        model: "openai/gpt-5.2-mini",
      },
    ],
  },
}
```

Authentification : `Authorization: Bearer <token>` ou `x-openclaw-token: <token>`.

**Points de terminaison :**

- `POST /hooks/wake` → `{ text, mode?: "now"|"next-heartbeat" }`
- `POST /hooks/agent` → `{ message, name?, agentId?, sessionKey?, wakeMode?, deliver?, channel?, to?, model?, thinking?, timeoutSeconds? }`
  - `sessionKey` de la charge utile de la requête n'est accepté que lorsque `hooks.allowRequestSessionKey=true` (par défaut : `false`).
- `POST /hooks/<name>` → résolu via `hooks.mappings`

<Accordion title="Détails du mappage">

- `match.path` correspond au sous-chemin après `/hooks` (par exemple `/hooks/gmail` → `gmail`).
- `match.source` correspond à un champ de charge utile pour les chemins génériques.
- Les modèles comme `{{messages[0].subject}}` lisent à partir de la charge utile.
- `transform` peut pointer vers un module JS/TS retournant une action hook.
  - `transform.module` doit être un chemin relatif et rester dans `hooks.transformsDir` (les chemins absolus et la traversée sont rejetés).
- `agentId` achemine vers un agent spécifique ; les ID inconnus reviennent par défaut.
- `allowedAgentIds` : restreint l'acheminement explicite (`*` ou omis = autoriser tous, `[]` = refuser tous).
- `defaultSessionKey` : clé de session fixe optionnelle pour les exécutions d'agent hook sans `sessionKey` explicite.
- `allowRequestSessionKey` : autoriser les appelants `/hooks/agent` à définir `sessionKey` (par défaut : `false`).
- `allowedSessionKeyPrefixes` : liste d'autorisation de préfixe optionnelle pour les valeurs `sessionKey` explicites (requête + mappage), par exemple `["hook:"]`.
- `deliver: true` envoie la réponse finale à un canal ; `channel` par défaut à `last`.
- `model` remplace le LLM pour cette exécution hook (doit être autorisé si le catalogue de modèles est défini).

</Accordion>

### Intégration Gmail

```json5
{
  hooks: {
    gmail: {
      account: "openclaw@gmail.com",
      topic: "projects/<project-id>/topics/gog-gmail-watch",
      subscription: "gog-gmail-watch-push",
      pushToken: "shared-push-token",
      hookUrl: "http://127.0.0.1:18789/hooks/gmail",
      includeBody: true,
      maxBytes: 20000,
      renewEveryMinutes: 720,
      serve: { bind: "127.0.0.1", port: 8788, path: "/" },
      tailscale: { mode: "funnel", path: "/gmail-pubsub" },
      model: "openrouter/meta-llama/llama-3.3-70b-instruct:free",
      thinking: "off",
    },
  },
}
```

- La passerelle démarre automatiquement `gog gmail watch serve` au démarrage lorsqu'elle est configurée. Définissez `OPENCLAW_SKIP_GMAIL_WATCHER=1` pour désactiver.
- N'exécutez pas un `gog gmail watch serve` séparé aux côtés de la passerelle.

---

## Hôte Canvas

```json5
{
  canvasHost: {
    root: "~/.openclaw/workspace/canvas",
    liveReload: true,
    // enabled: false, // ou OPENCLAW_SKIP_CANVAS_HOST=1
  },
}
```

- Sert HTML/CSS/JS modifiables par agent et A2UI sur HTTP sous le port de la passerelle :
  - `http://<gateway-host>:<gateway.port>/__openclaw__/canvas/`
  - `http://<gateway-host>:<gateway.port>/__openclaw__/a2ui/`
- Accès local uniquement : conservez `gateway.bind: "loopback"` (par défaut).
- Liaisons non-loopback : les routes canvas nécessitent l'authentification de la passerelle (jeton/mot de passe/proxy de confiance), comme les autres surfaces HTTP de la passerelle.
- Les WebViews de nœud n'envoient généralement pas d'en-têtes d'authentification ; après l'appairage et la connexion d'un nœud, la passerelle annonce les URL de capacité limitées au nœud pour l'accès canvas/A2UI.
- Les URL de capacité sont liées à la session WS du nœud actif et expirent rapidement. Le secours basé sur l'IP n'est pas utilisé.
- Injecte le client de rechargement en direct dans le HTML servi.
- Crée automatiquement un `index.html` de démarrage lorsqu'il est vide.
- Sert également A2UI à `/__openclaw__/a2ui/`.
- Les modifications nécessitent un redémarrage de la passerelle.
- Désactivez le rechargement en direct pour les grands répertoires ou les erreurs `EMFILE`.

---

## Découverte

### mDNS (Bonjour)

```json5
{
  discovery: {
    mdns: {
      mode: "minimal", // minimal | full | off
    },
  },
}
```

- `minimal` (par défaut) : omettez `cliPath` + `sshPort` des enregistrements TXT.
- `full` : incluez `cliPath` + `sshPort`.
- Le nom d'hôte par défaut est `openclaw`. Remplacez par `OPENCLAW_MDNS_HOSTNAME`.

### Zone large (DNS-SD)

```json5
{
  discovery: {
    wideArea: { enabled: true },
  },
}
```

Écrit une zone DNS-SD unicast sous `~/.openclaw/dns/`. Pour la découverte inter-réseaux, associez-la à un serveur DNS (CoreDNS recommandé) + DNS fractionné Tailscale.

Configuration : `openclaw dns setup --apply`.

---

## Environnement

### `env` (variables d'environnement en ligne)

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

- Les variables d'environnement en ligne ne sont appliquées que si l'environnement du processus manque la clé.
- Fichiers `.env` : `.env` du répertoire courant + `~/.openclaw/.env` (aucun ne remplace les variables existantes).
- `shellEnv` : importe les clés attendues manquantes de votre profil de shell de connexion.
- Voir [Environnement](/help/environment) pour la précédence complète.

### Substitution de variable d'environnement

Référencez les variables d'environnement dans n'importe quelle chaîne de configuration avec `${VAR_NAME}` :

```json5
{
  gateway: {
    auth: { token: "${OPENCLAW_GATEWAY_TOKEN}" },
  },
}
```

- Seuls les noms en majuscules correspondent : `[A-Z_][A-Z0-9_]*`.
- Les variables manquantes/vides lèvent une erreur au chargement de la configuration.
- Échappez avec `$${VAR}` pour un `${VAR}` littéral.
- Fonctionne avec `$include`.

---

## Secrets

Les références de secrets sont additives : les valeurs en texte brut fonctionnent toujours.

### `SecretRef`

Utilisez une forme d'objet :

```json5
{ source: "env" | "file" | "exec", provider: "default", id: "..." }
```

Validation :

- Modèle `provider` : `^[a-z][a-z0-9_-]{0,63}$`
- Modèle d'ID `source: "env"` : `^[A-Z][A-Z0-9_]{0,127}$`
- ID `source: "file"` : pointeur JSON absolu (par exemple `"/providers/openai/apiKey"`)
- Modèle d'ID `source: "exec"` : `^[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}$`
- Les ID `source: "exec"` ne doivent pas contenir de segments de chemin délimités par des points ou des points-points (par exemple `a/../b` est rejeté)

### Surface de credentials supportée

- Matrice canonique : [Surface de credentials SecretRef](/reference/secretref-credential-surface)
- `secrets apply` cible les chemins de credentials `openclaw.json` supportés.
- Les références `auth-profiles.json` sont incluses dans la résolution d'exécution et la couverture d'audit.

### Configuration des fournisseurs de secrets

```json5
{
  secrets: {
    providers: {
      default: { source: "env" }, // fournisseur env explicite optionnel
      filemain: {
        source: "file",
        path: "~/.openclaw/secrets.json",
        mode: "json",
        timeoutMs: 5000,
      },
      vault: {
        source: "exec",
        command: "/usr/local/bin/openclaw-vault-resolver",
        passEnv: ["PATH", "VAULT_ADDR"],
      },
    },
    defaults: {
      env: "default",
      file: "filemain",
      exec: "vault",
    },
  },
}
```

Notes :

- Le fournisseur `file` supporte `mode: "json"` et `mode: "singleValue"` (l'ID doit être `"value"` en mode singleValue).
- Le fournisseur `exec` nécessite un chemin `command` absolu et utilise des charges utiles de protocole sur stdin/stdout.
- Par défaut, les chemins de commande symlink sont rejetés. Définissez `allowSymlinkCommand: true` pour autoriser les chemins symlink tout en validant le chemin cible résolu.
- Si `trustedDirs` est configuré, la vérification du répertoire de confiance s'applique au chemin cible résolu.
- L'environnement enfant `exec` est minimal par défaut ; transmettez les variables requises explicitement avec `passEnv`.
- Les références de secrets sont résolues au moment de l'activation dans un snapshot en mémoire, puis les chemins de requête lisent uniquement le snapshot.
- Le filtrage de surface active s'applique lors de l'activation : les références non résolues sur les surfaces activées échouent au démarrage/rechargement, tandis que les surfaces inactives sont ignorées avec des diagnostics.

---

## Stockage d'authentification

```json5
{
  auth: {
    profiles: {
      "anthropic:me@example.com": { provider: "anthropic", mode: "oauth", email: "me@example.com" },
      "anthropic:work": { provider: "anthropic", mode: "api_key" },
    },
    order: {
      anthropic: ["anthropic:me@example.com", "anthropic:work"],
    },
  },
}
```

- Les profils par agent sont stockés à `<agentDir>/auth-profiles.json`.
- `auth-profiles.json` supporte les références au niveau des valeurs (`keyRef` pour `api_key`, `tokenRef` pour `token`).
- Les credentials d'exécution statiques proviennent de snapshots résolus en mémoire ; les entrées `auth.json` statiques héritées sont supprimées lorsqu'elles sont découvertes.
- Importations OAuth héritées de `~/.openclaw/credentials/oauth.json`.
- Voir [OAuth](/concepts/oauth).
- Comportement d'exécution des secrets et outillage `audit/configure/apply` : [Gestion des secrets](/gateway/secrets).

---

## Journalisation

```json5
{
  logging: {
    level: "info",
    file: "/tmp/openclaw/openclaw.log",
    consoleLevel: "info",
    consoleStyle: "pretty", // pretty | compact | json
    redactSensitive: "tools", // off | tools
    redactPatterns: ["\\bTOKEN\\b\\s*[=:]\\s*([\"']?)([^\\s\"']+)\\1"],
  },
}
```

- Fichier journal par défaut : `/tmp/openclaw/openclaw-YYYY-MM-DD.log`.
- Définissez `logging.file` pour un chemin stable.
- `consoleLevel` augmente à `debug` lorsque `--verbose`.

---

## CLI

```json5
{
  cli: {
    banner: {
      taglineMode: "off", // random | default | off
    },
  },
}
```

- `cli.banner.taglineMode` contrôle le style de la ligne d'accroche de la bannière :
  - `"random"` (par défaut) : lignes d'accroche amusantes/saisonnières en rotation.
  - `"default"` : ligne d'accroche neutre fixe (`All your chats, one OpenClaw.`).
  - `"off"` : pas de texte de ligne d'accroche (titre/version de la bannière toujours affichés).
- Pour masquer la bannière entière (pas seulement les lignes d'accroche), définissez l'env `OPENCLAW_HIDE_BANNER=1`.

---

## Assistant

Métadonnées écrites par les assistants CLI (`onboard`, `configure`, `doctor`) :

```json5
{
  wizard: {
    lastRunAt: "2026-01-01T00:00:00.000Z",
    lastRunVersion: "2026.1.4",
    lastRunCommit: "abc1234",
    lastRunCommand: "configure",
    lastRunMode: "local",
  },
}
```

---

## Identité

```json5
{
  agents: {
    list: [
      {
        id: "main",
        identity: {
          name: "Samantha",
          theme: "helpful sloth",
          emoji: "🦥",
          avatar: "avatars/samantha.png",
        },
      },
    ],
  },
}
```

Écrit par l'assistant d'intégration macOS. Dérive les valeurs par défaut :

- `messages.ackReaction` de `identity.emoji` (revient à 👀)
- `mentionPatterns` de `identity.name`/`identity.emoji`
- `avatar` accepte : chemin relatif à l'espace de travail, URL `http(s)`, ou URI `data:`

---

## Pont (hérité, supprimé)

Les builds actuels n'incluent plus le pont TCP. Les nœuds se connectent via la WebSocket de la passerelle. Les clés `bridge.*` ne font plus partie du schéma de configuration (la validation échoue jusqu'à suppression ; `openclaw doctor --fix` peut supprimer les clés inconnues).

<Accordion title="Configuration de pont hérité (référence historique)">

```json
{
  "bridge": {
    "enabled": true,
    "port": 18790,
    "bind": "tailnet",
    "tls": {
      "enabled": true,
      "autoGenerate": true
    }
  }
}
```

</Accordion>

## Cron

```json5
{
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
    webhook: "https://example.invalid/legacy", // deprecated fallback for stored notify:true jobs
    webhookToken: "replace-with-dedicated-token", // optional bearer token for outbound webhook auth
    sessionRetention: "24h", // duration string or false
    runLog: {
      maxBytes: "2mb", // default 2_000_000 bytes
      keepLines: 2000, // default 2000
    },
  },
}
```

- `sessionRetention` : durée de conservation des sessions de cron isolées complétées avant suppression de `sessions.json`. Contrôle également le nettoyage des transcriptions de cron supprimées archivées. Par défaut : `24h` ; définissez `false` pour désactiver.
- `runLog.maxBytes` : taille maximale par fichier journal d'exécution (`cron/runs/<jobId>.jsonl`) avant suppression. Par défaut : `2_000_000` octets.
- `runLog.keepLines` : lignes les plus récentes conservées lors du déclenchement de la suppression du journal d'exécution. Par défaut : `2000`.
- `webhookToken` : jeton porteur utilisé pour la livraison du webhook cron POST (`delivery.mode = "webhook"`), si omis, aucun en-tête d'authentification n'est envoyé.
- `webhook` : URL webhook héritée dépréciée (http/https) utilisée uniquement pour les tâches stockées qui ont toujours `notify: true`.

Voir [Tâches Cron](/automation/cron-jobs).

---

## Variables de modèle de média

Espaces réservés de modèle développés dans `tools.media.models[].args` :

| Variable           | Description                                       |
| ------------------ | ------------------------------------------------- |
| `{{Body}}`         | Corps complet du message entrant                  |
| `{{RawBody}}`      | Corps brut (sans wrappers d'historique/expéditeur)|
| `{{BodyStripped}}` | Corps avec mentions de groupe supprimées          |
| `{{From}}`         | Identifiant de l'expéditeur                       |
| `{{To}}`           | Identifiant de destination                        |
| `{{MessageSid}}`   | ID de message du canal                            |
| `{{SessionId}}`    | UUID de session actuelle                          |
| `{{IsNewSession}}` | `"true"` lors de la création d'une nouvelle session|
| `{{MediaUrl}}`     | Pseudo-URL de média entrant                       |
| `{{MediaPath}}`    | Chemin de média local                             |
| `{{MediaType}}`    | Type de média (image/audio/document/…)            |
| `{{Transcript}}`   | Transcription audio                               |
| `{{Prompt}}`       | Invite de média résolue pour les entrées CLI      |
| `{{MaxChars}}`     | Caractères de sortie max résolus pour les entrées CLI|
| `{{ChatType}}`     | `"direct"` ou `"group"`                           |
| `{{GroupSubject}}` | Sujet du groupe (meilleur effort)                 |
| `{{GroupMembers}}` | Aperçu des membres du groupe (meilleur effort)    |
| `{{SenderName}}`   | Nom d'affichage de l'expéditeur (meilleur effort) |
| `{{SenderE164}}`   | Numéro de téléphone de l'expéditeur (meilleur effort)|
| `{{Provider}}`     | Indice de fournisseur (whatsapp, telegram, discord, etc.)|

---

## Inclusions de configuration (`$include`)

Divisez la configuration en plusieurs fichiers :

```json5
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789 },
  agents: { $include: "./agents.json5" },
  broadcast: {
    $include: ["./clients/mueller.json5", "./clients/schmidt.json5"],
  },
}
```

**Comportement de fusion :**

- Fichier unique : remplace l'objet contenant.
- Tableau de fichiers : fusionné en profondeur dans l'ordre (les versions ultérieures remplacent les versions antérieures).
- Clés sœurs : fusionnées après les inclusions (remplacent les valeurs incluses).
- Inclusions imbriquées : jusqu'à 10 niveaux de profondeur.
- Chemins : résolus par rapport au fichier incluant, mais doivent rester dans le répertoire de configuration de niveau supérieur (`dirname` de `openclaw.json`). Les formes absolues/`../` sont autorisées uniquement si elles se résolvent toujours dans cette limite.
- Erreurs : messages clairs pour les fichiers manquants, les erreurs d'analyse et les inclusions circulaires.

---

_Connexe : [Configuration](/gateway/configuration) · [Exemples de configuration](/gateway/configuration-examples) · [Doctor](/gateway/doctor)_
