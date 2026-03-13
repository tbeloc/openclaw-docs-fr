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
| `allowlist` (défaut)  | Uniquement les groupes correspondant à la liste d'autorisation configurée |
| `open`                | Contourner les listes d'autorisation de groupe (la limitation de mention s'applique toujours) |
| `disabled`            | Bloquer tous les messages de groupe/salle                |

<Note>
`channels.defaults.groupPolicy` définit la valeur par défaut lorsque la `groupPolicy` d'un fournisseur n'est pas définie.
Les codes d'appairage expirent après 1 heure. Les demandes d'appairage DM en attente sont limitées à **3 par canal**.
Si un bloc de fournisseur est complètement absent (`channels.<provider>` absent), la politique de groupe d'exécution revient à `allowlist` (fermeture sûre) avec un avertissement au démarrage.
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

### Valeurs par défaut de canal et battement de cœur

Utilisez `channels.defaults` pour le comportement partagé de politique de groupe et de battement de cœur entre les fournisseurs :

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

- `channels.defaults.groupPolicy` : politique de groupe de secours lorsque la `groupPolicy` au niveau du fournisseur n'est pas définie.
- `channels.defaults.heartbeat.showOk` : inclure les statuts de canal sains dans la sortie du battement de cœur.
- `channels.defaults.heartbeat.showAlerts` : inclure les statuts dégradés/erreur dans la sortie du battement de cœur.
- `channels.defaults.heartbeat.useIndicator` : rendre la sortie du battement de cœur de style indicateur compact.

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
      streaming: "partial", // off | partial | block | progress (défaut: off)
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
- `configWrites: false` bloque les écritures de configuration initiées par Telegram (migrations d'ID de supergroupe, `/config set|unset`).
- Les entrées `bindings[]` de niveau supérieur avec `type: "acp"` configurent les liaisons ACP persistantes pour les sujets du forum (utilisez `chatId:topic:topicId` canonique dans `match.peer.id`). La sémantique des champs est partagée dans [Agents ACP](/tools/acp-agents#channel-specific-settings).
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
- `channels.discord.guilds.<id>.ignoreOtherMentions` (et les remplacements de canal) supprime les messages qui mentionnent un autre utilisateur ou rôle mais pas le bot (excluant @everyone/@here).
- `maxLinesPerMessage` (défaut 17) divise les messages hauts même lorsqu'ils sont sous 2000 caractères.
- `channels.discord.threadBindings` contrôle le routage lié aux threads Discord :
  - `enabled` : remplacement Discord pour les fonctionnalités de session liée aux threads (`/focus`, `/unfocus`, `/agents`, `/session idle`, `/session max-age` et livraison/routage lié)
  - `idleHours` : remplacement Discord pour l'auto-unfocus d'inactivité en heures (`0` désactive)
  - `maxAgeHours` : remplacement Discord pour l'âge maximum dur en heures (`0` désactive)
  - `spawnSubagentSessions` : commutateur opt-in pour la création/liaison automatique de threads `sessions_spawn({ thread: true })`
- Les entrées `bindings[]` de niveau supérieur avec `type: "acp"` configurent les liaisons ACP persistantes pour les canaux et threads (utilisez l'ID de canal/thread dans `match.peer.id`). La sémantique des champs est partagée dans [Agents ACP](/tools/acp-agents#channel-specific-settings).
- `channels.discord.ui.components.accentColor` définit la couleur d'accent pour les conteneurs de composants Discord v2.
- `channels.discord.voice` active les conversations de canal vocal Discord et les remplacements optionnels d'auto-join + TTS.
- `channels.discord.voice.dave
