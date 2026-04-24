---
summary: "Configuration des canaux : contrôle d'accès, appairage, clés par canal sur Slack, Discord, Telegram, WhatsApp, Matrix, iMessage, et plus"
read_when:
  - Configuration d'un plugin de canal (authentification, contrôle d'accès, multi-compte)
  - Dépannage des clés de configuration par canal
  - Audit de la politique DM, de la politique de groupe ou du filtrage des mentions
title: "Configuration — canaux"
---

Clés de configuration par canal sous `channels.*`. Couvre l'accès DM et groupe,
les configurations multi-compte, le filtrage des mentions, et les clés par canal pour Slack, Discord,
Telegram, WhatsApp, Matrix, iMessage, et les autres plugins de canal fournis.

Pour les agents, outils, runtime de passerelle, et autres clés de niveau supérieur, voir
[Référence de configuration](/fr/gateway/configuration-reference).

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
| `open`                | Contourner les listes blanches de groupe (mention-gating s'applique toujours) |
| `disabled`            | Bloquer tous les messages de groupe/salle                 |

<Note>
`channels.defaults.groupPolicy` définit la valeur par défaut lorsque `groupPolicy` d'un fournisseur n'est pas défini.
Les codes d'appairage expirent après 1 heure. Les demandes d'appairage DM en attente sont limitées à **3 par canal**.
Si un bloc de fournisseur est complètement absent (`channels.<provider>` absent), la politique de groupe d'exécution revient à `allowlist` (fail-closed) avec un avertissement au démarrage.
</Note>

### Remplacements de modèle de canal

Utilisez `channels.modelByChannel` pour épingler des ID de canal spécifiques à un modèle. Les valeurs acceptent `provider/model` ou des alias de modèle configurés. Le mappage de canal s'applique lorsqu'une session n'a pas déjà de remplacement de modèle (par exemple, défini via `/model`).

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

### Valeurs par défaut des canaux et battement de cœur

Utilisez `channels.defaults` pour le comportement partagé de politique de groupe et de battement de cœur entre les fournisseurs :

```json5
{
  channels: {
    defaults: {
      groupPolicy: "allowlist", // open | allowlist | disabled
      contextVisibility: "all", // all | allowlist | allowlist_quote
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
- `channels.defaults.contextVisibility` : mode de visibilité du contexte supplémentaire par défaut pour tous les canaux. Valeurs : `all` (défaut, inclure tout le contexte cité/thread/historique), `allowlist` (inclure uniquement le contexte des expéditeurs autorisés), `allowlist_quote` (identique à allowlist mais conserver le contexte de citation/réponse explicite). Remplacement par canal : `channels.<channel>.contextVisibility`.
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
- `channels.whatsapp.defaultAccount` optionnel remplace la sélection du compte par défaut de secours lorsqu'il correspond à un ID de compte configuré.
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
          systemPrompt: "Gardez les réponses brèves.",
          topics: {
            "99": {
              requireMention: false,
              skills: ["search"],
              systemPrompt: "Restez sur le sujet.",
            },
          },
        },
      },
      customCommands: [
        { command: "backup", description: "Sauvegarde Git" },
        { command: "generate", description: "Créer une image" },
      ],
      historyLimit: 50,
      replyToMode: "first", // off | first | all | batched
      linkPreview: true,
      streaming: "partial", // off | partial | block | progress (défaut : off ; opt-in explicite pour éviter les limites de taux d'édition d'aperçu)
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

- Jeton de bot : `channels.telegram.botToken` ou `channels.telegram.tokenFile` (fichier régulier uniquement ; les liens symboliques sont rejetés), avec `TELEGRAM_BOT_TOKEN` comme secours pour le compte par défaut.
- `channels.telegram.defaultAccount` optionnel remplace la sélection du compte par défaut lorsqu'il correspond à un ID de compte configuré.
- Dans les configurations multi-compte (2+ ID de compte), définissez un défaut explicite (`channels.telegram.defaultAccount` ou `channels.telegram.accounts.default`) pour éviter le routage de secours ; `openclaw doctor` avertit lorsque cela est manquant ou invalide.
- `configWrites: false` bloque les écritures de configuration initiées par Telegram (migrations d'ID de supergroupes, `/config set|unset`).
- Les entrées `bindings[]` de niveau supérieur avec `type: "acp"` configurent les liaisons ACP persistantes pour les sujets du forum (utilisez `chatId:topic:topicId` canonique dans `match.peer.id`). La sémantique des champs est partagée dans [ACP Agents](/fr/tools/acp-agents#channel-specific-settings).
- Les aperçus de flux Telegram utilisent `sendMessage` + `editMessageText` (fonctionne dans les chats directs et de groupe).
- Politique de nouvelle tentative : voir [Politique de nouvelle tentative](/fr/concepts/retry).

### Discord

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "your-bot-token",
      mediaMaxMb: 100,
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
      replyToMode: "off", // off | first | all | batched
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
              systemPrompt: "Réponses courtes uniquement.",
            },
          },
        },
      },
      historyLimit: 20,
      textChunkLimit: 2000,
      chunkMode: "length", // length | newline
      streaming: "off", // off | partial | block | progress (progress mappe à partial sur Discord)
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
      execApprovals: {
        enabled: "auto", // true | false | "auto"
        approvers: ["987654321098765432"],
        agentFilter: ["default"],
        sessionFilter: ["discord:"],
        target: "dm", // dm | channel | both
        cleanupAfterResolve: false,
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
- Les entrées `bindings[]` de niveau supérieur avec `type: "acp"` configurent les liaisons ACP persistantes pour les canaux et threads (utilisez l'ID de canal/thread dans `match.peer.id`). La sémantique des champs est partagée dans [ACP Agents](/fr/tools/acp-agents#channel-specific-settings).
- `channels.discord.ui.components.accentColor` définit la couleur d'accent pour les conteneurs Discord components v2.
- `channels.discord.voice` active les conversations de canal vocal Discord et les remplacements optionnels d'auto-join + TTS.
- `channels.discord.voice.daveEncryption` et `channels.discord.voice.decryptionFailureTolerance` passent à `@discordjs/voice` options DAVE (`true` et `24` par défaut).
- OpenClaw tente en outre la récupération de réception vocale en quittant/rejoignant une session vocale après des échecs de déchiffrement répétés.
- `channels.discord.streaming` est la clé de mode de flux canonique. Les valeurs héritées `streamMode` et booléennes `streaming` sont auto-migrées.
- `channels.discord.autoPresence` mappe la disponibilité d'exécution à la présence du bot (sain => en ligne, dégradé => inactif, épuisé => dnd) et permet les remplacements de texte d'état optionnels.
- `channels.discord.dangerouslyAllowNameMatching` réactive la correspondance de nom/tag mutable (mode de compatibilité break-glass).
- `channels.discord.execApprovals` : livraison d'approbation d'exécution native Discord et autorisation d'approbateur.
  - `enabled` : `true`, `false`, ou `"auto"` (défaut). En mode auto, les approbations d'exécution s'activent lorsque les approbateurs peuvent être résolus à partir de `approvers` ou `commands.ownerAllowFrom`.
  - `approvers` : ID d'utilisateur Discord autorisés à approuver les demandes d'exécution. Revient à `commands.ownerAllowFrom` lorsqu'il est omis.
  - `agentFilter` : liste blanche optionnelle d'ID d'agent. Omettez pour transférer les approbations pour tous les agents.
  - `sessionFilter` : modèles de clé de session optionnels (sous-chaîne ou regex).
  - `target` : où envoyer les invites d'approbation. `"dm"` (défaut) envoie aux DM d'approbateur, `"channel"` envoie au canal d'origine, `"both"` envoie aux deux. Lorsque la cible inclut `"channel"`, les boutons ne sont utilisables que par les approbateurs résolus.
  - `cleanupAfterResolve` : lorsque `true`, supprime les DM d'approbation après approbation, refus ou délai d'expiration.

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

- JSON de compte de service : en ligne (`serviceAccount`) ou basé sur fichier (`serviceAccountFile`).
- SecretRef de compte de service est également supporté (`serviceAccountRef`).
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
          systemPrompt: "Réponses courtes uniquement.",
        },
      },
      historyLimit: 50,
      allowBots: false,
      reactionNotifications: "own",
      reactionAllowlist: ["U123"],
      replyToMode: "off", // off | first | all | batched
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
      streaming: {
        mode: "partial", // off | partial | block | progress
        nativeTransport: true, // utiliser l'API de streaming natif Slack lorsque mode=partial
      },
      mediaMaxMb: 20,
      execApprovals: {
        enabled: "auto", // true | false | "auto"
        approvers: ["U123"],
        agentFilter: ["default"],
        sessionFilter: ["slack:"],
        target: "dm", // dm | channel | both
      },
    },
  },
}
```

- **Mode socket** nécessite à la fois `botToken` et `appToken` (`SLACK_BOT_TOKEN` + `SLACK_APP_TOKEN` pour le secours d'env du compte par défaut).
- **Mode HTTP** nécessite `botToken` plus `signingSecret` (à la racine ou par compte).
- `botToken`, `appToken`, `signingSecret`, et `userToken` acceptent les chaînes en texte brut ou les objets SecretRef.
- Les instantanés de compte Slack exposent les champs de source/statut par identifiant tels que `botTokenSource`, `botTokenStatus`, `appTokenStatus`, et, en mode HTTP, `signingSecretStatus`. `configured_unavailable` signifie que le compte est configuré via SecretRef mais le chemin de commande/exécution actuel n'a pas pu résoudre la valeur du secret.
- `configWrites: false` bloque les écritures de configuration initiées par Slack.
- `channels.slack.defaultAccount` optionnel remplace la sélection du compte par défaut lorsqu'il correspond à un ID de compte configuré.
- `channels.slack.streaming.mode` est la clé de mode de flux Slack canonique. `channels.slack.streaming.nativeTransport` contrôle le transport de flux natif Slack. Les valeurs héritées `streamMode`, booléennes `streaming`, et `nativeStreaming` sont auto-migrées.
- Utilisez `user:<id>` (DM) ou `channel:<id>` pour les cibles de livraison.

**Modes de notification de réaction :** `off`, `own` (défaut), `all`, `allowlist` (de `reactionAllowlist`).

**Isolation de session de thread :** `thread.historyScope` est par thread (défaut) ou partagé sur le canal. `thread.inheritParent` copie la transcription du canal parent aux nouveaux threads.

- Le streaming natif Slack plus le statut de thread de style assistant Slack "is typing..." nécessitent une cible de thread de réponse. Les DM de niveau supérieur restent hors thread par défaut, ils utilisent donc `typingReaction` ou la livraison normale au lieu du style d'aperçu de thread.
- `typingReaction` ajoute une réaction temporaire au message Slack entrant pendant qu'une réponse s'exécute, puis la supprime à la fin. Utilisez un code emoji Slack tel que `"hourglass_flowing_sand"`.
- `channels.slack.execApprovals` : livraison d'approbation d'exécution native Slack et autorisation d'approbateur. Même schéma que Discord : `enabled` (`true`/`false`/`"auto"`), `approvers` (ID d'utilisateur Slack), `agentFilter`, `sessionFilter`, et `target` (`"dm"`, `"channel"`, ou `"both"`).

| Groupe d'action | Défaut | Notes                  |
| ------------ | ------- | ---------------------- |
| reactions    | activé | Réagir + lister les réactions |
| messages     | activé | Lire/envoyer/éditer/supprimer  |
| pins         | activé | Épingler/dépingler/lister         |
| memberInfo   | activé | Info membre            |
| emojiList    | activé | Liste emoji personnalisée      |

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
      groups: {
        "*": { requireMention: true },
        "team-channel-id": { requireMention: false },
      },
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
- Les rappels de slash natifs sont authentifiés avec les jetons par commande retournés par Mattermost lors de l'enregistrement de la commande slash. Si l'enregistrement échoue ou qu'aucune commande n'est activée, OpenClaw rejette les rappels avec `Unauthorized: invalid command token.`
- Pour les hôtes de rappel privés/tailnet/internes, Mattermost peut nécessiter que `ServiceSettings.AllowedUntrustedInternalConnections` inclue l'hôte/domaine de rappel. Utilisez les valeurs d'hôte/domaine, pas les URL complètes.
- `channels.mattermost.configWrites` : autoriser ou refuser les écritures de configuration initiées par Mattermost.
- `channels.mattermost.requireMention` : exiger `@mention` avant de répondre dans les canaux.
- `channels.mattermost.groups.<channelId>.requireMention` : remplacement de mention-gating par canal (`"*"` pour défaut).
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

- Chemins de clé principaux couverts ici : `channels.bluebubbles`, `channels.bluebubbles.dmPolicy`.
- `channels.bluebubbles.defaultAccount` optionnel remplace la sélection du compte par défaut lorsqu'il correspond à un ID de compte configuré.
- Les entrées `bindings[]` de niveau supérieur avec `type: "acp"` peuvent lier les conversations BlueBubbles aux sessions ACP persistantes. Utilisez une chaîne de poignée ou de cible BlueBubbles (`chat_id:*`, `chat_guid:*`, `chat_identifier:*`) dans `match.peer.id`. Sémantique des champs partagée : [ACP Agents](/fr/tools/acp-agents#channel-specific-settings).
- La configuration complète du canal BlueBubbles est documentée dans [BlueBubbles](/fr/channels/bluebubbles).

### iMessage

OpenClaw génère `imsg rpc` (JSON-RPC sur stdio). Aucun démon ou port requis.

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
- Les entrées `bindings[]` de niveau supérieur avec `type: "acp"` peuvent lier les conversations iMessage aux sessions ACP persistantes. Utilisez un poignée normalisé ou une cible de chat explicite (`chat_id:*`, `chat_guid:*`, `chat_identifier:*`) dans `match.peer.id`. Sémantique des champs partagée : [ACP Agents](/fr/tools/acp-agents#channel-specific-settings).

<Accordion title="Exemple de wrapper SSH iMessage">

```bash
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"
```

</Accordion>

### Matrix

Matrix est soutenu par plugin et configuré sous `channels.matrix`.

```json5
{
  channels: {
    matrix: {
      enabled: true,
      homeserver: "https://matrix.example.org",
      accessToken: "syt_bot_xxx",
      proxy: "http://127.0.0.1:7890",
      encryption: true,
      initialSyncLimit: 20,
      defaultAccount: "ops",
      accounts: {
        ops: {
          name: "Ops",
          userId: "@ops:example.org",
          accessToken: "syt_ops_xxx",
        },
        alerts: {
          userId: "@alerts:example.org",
          password: "secret",
          proxy: "http://127.0.0.1:7891",
        },
      },
    },
  },
}
```

- L'authentification par jeton utilise `accessToken` ; l'authentification par mot de passe utilise `userId` + `password`.
- `channels.matrix.proxy` achemine le trafic HTTP Matrix via un proxy HTTP(S) explicite. Les comptes nommés peuvent le remplacer avec `channels.matrix.accounts.<id>.proxy`.
- `channels.matrix.network.dangerouslyAllowPrivateNetwork` autorise les serveurs d'accueil privés/internes. `proxy` et cet opt-in réseau sont des contrôles indépendants.
- `channels.matrix.defaultAccount` sélectionne le compte préféré dans les configurations multi-compte.
- `channels.matrix.autoJoin` par défaut à `off`, les salles invitées et les invitations de style DM fraîches sont ignorées jusqu'à ce que vous définissiez `autoJoin: "allowlist"` avec `autoJoinAllowlist` ou `autoJoin: "always"`.
- `channels.matrix.execApprovals` : livraison d'approbation d'exécution native Matrix et autorisation d'approbateur.
  - `enabled` : `true`, `false`, ou `"auto"` (défaut). En mode auto, les approbations d'exécution s'activent lorsque les approbateurs peuvent être résolus à partir de `approvers` ou `commands.ownerAllowFrom`.
  - `approvers` : ID d'utilisateur Matrix (par exemple `@owner:example.org`) autorisés à approuver les demandes d'exécution.
  - `agentFilter` : liste blanche optionnelle d'ID d'agent. Omettez pour transférer les approbations pour tous les agents.
  - `sessionFilter` : modèles de clé de session optionnels (sous-chaîne ou regex).
  - `target` : où envoyer les invites d'approbation. `"dm"` (défaut), `"channel"` (salle d'origine), ou `"both"`.
  - Remplacements par compte : `channels.matrix.accounts.<id>.execApprovals`.
- `channels.matrix.dm.sessionScope` contrôle comment les DM Matrix se regroupent en sessions : `per-user` (défaut) partage par pair routé, tandis que `per-room` isole chaque salle DM.
- Les sondes d'état Matrix et les recherches de répertoire en direct utilisent la même politique de proxy que le trafic d'exécution.
- La configuration complète de Matrix, les règles de ciblage, et les exemples de configuration sont documentés dans [Matrix](/fr/channels/matrix).

### Microsoft Teams

Microsoft Teams est soutenu par plugin et configuré sous `channels.msteams`.

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

- Chemins de clé principaux couverts ici : `channels.msteams`, `channels.msteams.configWrites`.
- La configuration complète de Teams (identifiants, webhook, politique DM/groupe, remplacements par équipe/par canal) est documentée dans [Microsoft Teams](/fr/channels/msteams).

### IRC

IRC est soutenu par plugin et configuré sous `channels.irc`.

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

- Chemins de clé principaux couverts ici : `channels.irc`, `channels.irc.dmPolicy`, `channels.irc.configWrites`, `channels.irc.nickserv.*`.
- `channels.irc.defaultAccount` optionnel remplace la sélection du compte par défaut lorsqu'il correspond à un ID de compte configuré.
- La configuration complète du canal IRC (hôte/port/TLS/canaux/listes blanches/mention gating) est documentée dans [IRC](/fr/channels/irc).

### Multi-compte (tous les canaux)

Exécutez plusieurs comptes par canal (chacun avec son propre `accountId`) :

```json5
{
  channels: {
    telegram: {
      accounts: {
        default: {
          name: "Bot principal",
          botToken: "123456:ABC...",
        },
        alerts: {
          name: "Bot d'alertes",
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
- Si vous ajoutez un compte non-défaut via `openclaw channels add` (ou intégration de canal) tout en restant sur une configuration de canal à compte unique de niveau supérieur, OpenClaw promeut les valeurs de compte unique de niveau supérieur à portée de compte dans la carte de compte de canal en premier afin que le compte d'origine continue de fonctionner. La plupart des canaux les déplacent dans `channels.<channel>.accounts.default` ; Matrix peut préserver une cible nommée/par défaut existante correspondante à la place.
- Les liaisons de canal existantes (pas de `accountId`) continuent de correspondre au compte par défaut ; les liaisons à portée de compte restent optionnelles.
- `openclaw doctor --fix` répare également les formes mixtes en déplaçant les valeurs de compte unique de niveau supérieur à portée de compte dans le compte promu choisi pour ce canal. La plupart des canaux utilisent `accounts.default` ; Matrix peut préserver une cible nommée/par défaut existante correspondante à la place.

### Autres canaux de plugin

De nombreux canaux de plugin sont configurés en tant que `channels.<id>` et documentés dans leurs pages de canal dédiées (par exemple Feishu, Matrix, LINE, Nostr, Zalo, Nextcloud Talk, Synology Chat, et Twitch).
Voir l'index complet des canaux : [Channels](/fr/channels).

### Mention gating de chat de groupe

Les messages de groupe nécessitent par défaut une **mention** (mention de métadonnées ou modèles regex sûrs). S'applique aux chats de groupe WhatsApp, Telegram, Discord, Google Chat, et iMessage.

**Types de mention :**

- **Mentions de métadonnées** : @-mentions natives de la plateforme. Ignorées en mode auto-chat WhatsApp.
- **Modèles de texte** : modèles regex sûrs dans `agents.list[].groupChat.mentionPatterns`. Les modèles invalides et la répétition imbriquée non sûre sont ignorés.
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
    native: "auto", // enregistrer les commandes natives lorsque supporté
    nativeSkills: "auto", // enregistrer les commandes de compétences natives lorsque supporté
    text: true, // analyser /commands dans les messages de chat
    bash: false, // autoriser ! (alias : /bash)
    bashForegroundMs: 2000,
    config: false, // autoriser /config
    mcp: false, // autoriser /mcp
    plugins: false, // autoriser /plugins
    debug: false, // autoriser /debug
    restart: true, // autoriser /restart + outil de redémarrage de passerelle
    ownerAllowFrom: ["discord:123456789012345678"],
    ownerDisplay: "raw", // raw | hash
    ownerDisplaySecret: "${OWNER_ID_HASH_SECRET}",
    allowFrom: {
      "*": ["user1"],
      discord: ["user:123"],
    },
    useAccessGroups: true,
  },
}
```

<Accordion title="Détails des commandes">

- Ce bloc configure les surfaces de commande. Pour le catalogue de commandes intégrées + groupées actuel, voir [Slash Commands](/fr/tools/slash-commands).
- Cette page est une **référence de clé de configuration**, pas le catalogue complet des commandes. Les commandes détenues par canal/plugin telles que QQ Bot `/bot-ping` `/bot-help` `/bot-logs`, LINE `/card`, appairage d'appareil `/pair`, mémoire `/dreaming`, contrôle de téléphone `/phone`, et Talk `/voice` sont documentées dans leurs pages de canal/plugin plus [Slash Commands](/fr/tools/slash-commands).
- Les commandes texte doivent être des **messages autonomes** avec `/` de début.
- `native: "auto"` active les commandes natives pour Discord/Telegram, laisse Slack désactivé.
- `nativeSkills: "auto"` active les commandes de compétences natives pour Discord/Telegram, laisse Slack désactivé.
- Remplacer par canal : `channels.discord.commands.native` (booléen ou `"auto"`). `false` efface les commandes précédemment enregistrées.
- Remplacer l'enregistrement de compétences natives par canal avec `channels.<provider>.commands.nativeSkills`.
- `channels.telegram.customCommands` ajoute des entrées de menu de bot Telegram supplémentaires.
- `bash: true` active `! <cmd>` pour le shell d'hôte. Nécessite `tools.elevated.enabled` et l'expéditeur dans `tools.elevated.allowFrom.<channel>`.
- `config: true` active `/config` (lit/écrit `openclaw.json`). Pour les clients `chat.send` de passerelle, les écritures persistantes `/config set|unset` nécessitent également `operator.admin` ; la lecture seule `/config show` reste disponible pour les clients d'opérateur à portée d'écriture normale.
- `mcp: true` active `/mcp` pour la configuration du serveur MCP géré par OpenClaw sous `mcp.servers`.
- `plugins: true` active `/plugins` pour la découverte de plugin, l'installation, et les contrôles d'activation/désactivation.
- `channels.<provider>.configWrites` contrôle les mutations de configuration par canal (défaut : true).
- Pour les canaux multi-compte, `channels.<provider>.accounts.<id>.configWrites` contrôle également les écritures qui ciblent ce compte (par exemple `/allowlist --config --account <id>` ou `/config set channels.<provider>.accounts.<id>...`).
- `restart: false` désactive `/restart` et les actions d'outil de redémarrage de passerelle. Défaut : `true`.
- `ownerAllowFrom` est la liste blanche de propriétaire explicite pour les commandes/outils réservés au propriétaire. Elle est séparée de `allowFrom`.
- `ownerDisplay: "hash"` hache les ID de propriétaire dans l'invite système. Définissez `ownerDisplaySecret` pour contrôler le hachage.
- `allowFrom` est par fournisseur. Lorsqu'il est défini, c'est la **seule** source d'autorisation (les listes blanches de canal/appairage et `useAccessGroups` sont ignorés).
- `useAccessGroups: false` permet aux commandes de contourner les politiques de groupe d'accès lorsque `allowFrom` n'est pas défini.
- Carte de documentation des commandes :
  - catalogue intégré + groupé : [Slash Commands](/fr/tools/slash-commands)
  - surfaces de commande spécifiques au canal : [Channels](/fr/channels)
  - commandes QQ Bot : [QQ Bot](/fr/channels/qqbot)
  - commandes d'appairage : [Pairing](/fr/channels/pairing)
  - commande de carte LINE : [LINE](/fr/channels/line)
  - mémoire rêvante : [Dreaming](/fr/concepts/dreaming)

</Accordion>

## Connexes

- [Référence de configuration](/fr/gateway/configuration-reference) — clés de niveau supérieur
- [Configuration — agents](/fr/gateway/config-agents)
- [Aperçu des canaux](/fr/channels)
