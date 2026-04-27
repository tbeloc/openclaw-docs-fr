---
summary: "Aperçu du bot YuanBao, fonctionnalités et configuration"
read_when:
  - You want to connect a YuanBao bot
  - You are configuring the YuanBao channel
title: YuanBao
---

# YuanBao

YuanBao est la plateforme d'assistant IA de Tencent qui prend en charge l'intégration de bots via la messagerie instantanée. Les bots peuvent interagir avec les utilisateurs via des messages directs et des chats de groupe.

**Statut :** prêt pour la production pour les DM de bot + chats de groupe. WebSocket est le seul mode de connexion pris en charge.

---

## Démarrage rapide

> **Nécessite OpenClaw 2026.4.10 ou supérieur.** Exécutez `openclaw --version` pour vérifier. Mettez à jour avec `openclaw update`.

<Steps>
  <Step title="Ajouter le canal YuanBao avec vos identifiants">
  ```bash
  openclaw channels add --channel yuanbao --token "appKey:appSecret"
  ```
  La valeur `--token` utilise le format `appKey:appSecret` séparé par deux points. Vous pouvez obtenir ces identifiants à partir de l'APP YuanBao en créant un robot dans les paramètres de votre application.
  </Step>

  <Step title="Une fois la configuration terminée, redémarrez la passerelle pour appliquer les modifications">
  ```bash
  openclaw gateway restart
  ```
  </Step>
</Steps>

### Configuration interactive (alternative)

Vous pouvez également utiliser l'assistant interactif :

```bash
openclaw channels login --channel yuanbao
```

Suivez les invites pour entrer votre ID d'application et votre secret d'application.

---

## Contrôle d'accès

### Messages directs

Configurez `dmPolicy` pour contrôler qui peut envoyer des DM au bot :

- `"pairing"` — les utilisateurs inconnus reçoivent un code d'appairage ; approuvez via CLI
- `"allowlist"` — seuls les utilisateurs listés dans `allowFrom` peuvent discuter
- `"open"` — autoriser tous les utilisateurs (par défaut)
- `"disabled"` — désactiver tous les DM

**Approuver une demande d'appairage :**

```bash
openclaw pairing list yuanbao
openclaw pairing approve yuanbao <CODE>
```

### Chats de groupe

**Exigence de mention** (`channels.yuanbao.requireMention`) :

- `true` — exiger @mention (par défaut)
- `false` — répondre sans @mention

Répondre au message du bot dans un chat de groupe est traité comme une mention implicite.

---

## Exemples de configuration

### Configuration de base avec politique de DM ouverte

```json5
{
  channels: {
    yuanbao: {
      appKey: "your_app_key",
      appSecret: "your_app_secret",
      dm: {
        policy: "open",
      },
    },
  },
}
```

### Restreindre les DM à des utilisateurs spécifiques

```json5
{
  channels: {
    yuanbao: {
      appKey: "your_app_key",
      appSecret: "your_app_secret",
      dm: {
        policy: "allowlist",
        allowFrom: ["user_id_1", "user_id_2"],
      },
    },
  },
}
```

### Désactiver l'exigence de @mention dans les groupes

```json5
{
  channels: {
    yuanbao: {
      requireMention: false,
    },
  },
}
```

### Optimiser la livraison des messages sortants

```json5
{
  channels: {
    yuanbao: {
      // Envoyer chaque bloc immédiatement sans mise en buffer
      outboundQueueStrategy: "immediate",
    },
  },
}
```

### Ajuster la stratégie de fusion de texte

```json5
{
  channels: {
    yuanbao: {
      outboundQueueStrategy: "merge-text",
      minChars: 2800, // mettre en buffer jusqu'à ce nombre de caractères
      maxChars: 3000, // forcer la division au-dessus de cette limite
      idleMs: 5000, // vider automatiquement après délai d'inactivité (ms)
    },
  },
}
```

---

## Commandes courantes

| Commande   | Description                      |
| ---------- | -------------------------------- |
| `/help`    | Afficher les commandes disponibles |
| `/status`  | Afficher l'état du bot           |
| `/new`     | Démarrer une nouvelle session    |
| `/stop`    | Arrêter l'exécution actuelle     |
| `/restart` | Redémarrer OpenClaw              |
| `/compact` | Compacter le contexte de session |

> YuanBao prend en charge les menus de commandes slash natifs. Les commandes sont synchronisées automatiquement avec la plateforme au démarrage de la passerelle.

---

## Dépannage

### Le bot ne répond pas dans les chats de groupe

1. Assurez-vous que le bot est ajouté au groupe
2. Assurez-vous que vous @mentionnez le bot (requis par défaut)
3. Vérifiez les journaux : `openclaw logs --follow`

### Le bot ne reçoit pas les messages

1. Assurez-vous que le bot est créé et approuvé dans l'APP YuanBao
2. Assurez-vous que `appKey` et `appSecret` sont correctement configurés
3. Assurez-vous que la passerelle est en cours d'exécution : `openclaw gateway status`
4. Vérifiez les journaux : `openclaw logs --follow`

### Le bot envoie des réponses vides ou de secours

1. Vérifiez si le modèle IA retourne un contenu valide
2. La réponse de secours par défaut est : "暂时无法解答，你可以换个问题问问我哦"
3. Personnalisez-la via `channels.yuanbao.fallbackReply`

### Secret d'application divulgué

1. Réinitialisez le secret d'application dans l'APP YuanBao
2. Mettez à jour la valeur dans votre configuration
3. Redémarrez la passerelle : `openclaw gateway restart`

---

## Configuration avancée

### Comptes multiples

```json5
{
  channels: {
    yuanbao: {
      defaultAccount: "main",
      accounts: {
        main: {
          appKey: "key_xxx",
          appSecret: "secret_xxx",
          name: "Primary bot",
        },
        backup: {
          appKey: "key_yyy",
          appSecret: "secret_yyy",
          name: "Backup bot",
          enabled: false,
        },
      },
    },
  },
}
```

`defaultAccount` contrôle quel compte est utilisé lorsque les API sortantes ne spécifient pas d'`accountId`.

### Limites de messages

- `maxChars` — nombre maximum de caractères par message (par défaut : `3000` caractères)
- `mediaMaxMb` — limite de téléchargement/chargement de médias (par défaut : `20` MB)
- `overflowPolicy` — comportement lorsque le message dépasse la limite : `"split"` (par défaut) ou `"stop"`

### Streaming

YuanBao prend en charge la sortie de streaming au niveau des blocs. Lorsqu'elle est activée, le bot envoie le texte par chunks au fur et à mesure qu'il le génère.

```json5
{
  channels: {
    yuanbao: {
      disableBlockStreaming: false, // streaming de bloc activé (par défaut)
    },
  },
}
```

Définissez `disableBlockStreaming: true` pour envoyer la réponse complète en un seul message.

### Contexte d'historique de chat de groupe

Contrôlez le nombre de messages historiques inclus dans le contexte IA pour les chats de groupe :

```json5
{
  channels: {
    yuanbao: {
      historyLimit: 100, // par défaut : 100, définissez 0 pour désactiver
    },
  },
}
```

### Mode réponse

Contrôlez comment le bot cite les messages lors de la réponse dans les chats de groupe :

```json5
{
  channels: {
    yuanbao: {
      replyToMode: "first", // "off" | "first" | "all" (par défaut : "first")
    },
  },
}
```

| Valeur    | Comportement                                                 |
| --------- | ------------------------------------------------------------ |
| `"off"`   | Pas de citation de réponse                                   |
| `"first"` | Citer uniquement la première réponse par message entrant (par défaut) |
| `"all"`   | Citer chaque réponse                                         |

### Injection d'indice Markdown

Par défaut, le bot injecte des instructions dans l'invite système pour empêcher le modèle IA d'envelopper la réponse entière dans des blocs de code markdown.

```json5
{
  channels: {
    yuanbao: {
      markdownHintEnabled: true, // par défaut : true
    },
  },
}
```

### Mode débogage

Activez la sortie de journal non désinfectée pour des ID de bot spécifiques :

```json5
{
  channels: {
    yuanbao: {
      debugBotIds: ["bot_user_id_1", "bot_user_id_2"],
    },
  },
}
```

### Routage multi-agent

Utilisez `bindings` pour router les DM ou groupes YuanBao vers différents agents.

```json5
{
  agents: {
    list: [
      { id: "main" },
      { id: "agent-a", workspace: "/home/user/agent-a" },
      { id: "agent-b", workspace: "/home/user/agent-b" },
    ],
  },
  bindings: [
    {
      agentId: "agent-a",
      match: {
        channel: "yuanbao",
        peer: { kind: "direct", id: "user_xxx" },
      },
    },
    {
      agentId: "agent-b",
      match: {
        channel: "yuanbao",
        peer: { kind: "group", id: "group_zzz" },
      },
    },
  ],
}
```

Champs de routage :

- `match.channel`: `"yuanbao"`
- `match.peer.kind`: `"direct"` (DM) ou `"group"` (chat de groupe)
- `match.peer.id`: ID utilisateur ou code de groupe

---

## Référence de configuration

Configuration complète : [Configuration de la passerelle](/fr/gateway/configuration)

| Paramètre                                  | Description                                       | Par défaut                             |
| ------------------------------------------ | ------------------------------------------------- | -------------------------------------- |
| `channels.yuanbao.enabled`                 | Activer/désactiver le canal                       | `true`                                 |
| `channels.yuanbao.defaultAccount`          | Compte par défaut pour le routage sortant         | `default`                              |
| `channels.yuanbao.accounts.<id>.appKey`    | Clé d'application (utilisée pour la signature et la génération de ticket) | —                                      |
| `channels.yuanbao.accounts.<id>.appSecret` | Secret d'application (utilisé pour la signature)  | —                                      |
| `channels.yuanbao.accounts.<id>.token`     | Jeton pré-signé (ignore la signature automatique de ticket) | —                                      |
| `channels.yuanbao.accounts.<id>.name`      | Nom d'affichage du compte                         | —                                      |
| `channels.yuanbao.accounts.<id>.enabled`   | Activer/désactiver un compte spécifique           | `true`                                 |
| `channels.yuanbao.dm.policy`               | Politique de DM                                   | `open`                                 |
| `channels.yuanbao.dm.allowFrom`            | Liste blanche de DM (liste d'ID utilisateur)      | —                                      |
| `channels.yuanbao.requireMention`          | Exiger @mention dans les groupes                  | `true`                                 |
| `channels.yuanbao.overflowPolicy`          | Gestion des longs messages (`split` ou `stop`)    | `split`                                |
| `channels.yuanbao.replyToMode`             | Stratégie de réponse de groupe (`off`, `first`, `all`) | `first`                                |
| `channels.yuanbao.outboundQueueStrategy`   | Stratégie sortante (`merge-text` ou `immediate`)  | `merge-text`                           |
| `channels.yuanbao.minChars`                | Fusion-texte : caractères min pour déclencher l'envoi | `2800`                                 |
| `channels.yuanbao.maxChars`                | Fusion-texte : caractères max par message         | `3000`                                 |
| `channels.yuanbao.idleMs`                  | Fusion-texte : délai d'inactivité avant vidage automatique (ms) | `5000`                                 |
| `channels.yuanbao.mediaMaxMb`              | Limite de taille des médias (MB)                  | `20`                                   |
| `channels.yuanbao.historyLimit`            | Entrées de contexte d'historique de chat de groupe | `100`                                  |
| `channels.yuanbao.disableBlockStreaming`   | Désactiver la sortie de streaming au niveau des blocs | `false`                                |
| `channels.yuanbao.fallbackReply`           | Réponse de secours lorsque l'IA ne retourne aucun contenu | `暂时无法解答，你可以换个问题问问我哦` |
| `channels.yuanbao.markdownHintEnabled`     | Injecter des instructions anti-enveloppe markdown | `true`                                 |
| `channels.yuanbao.debugBotIds`             | Liste blanche de débogage des ID de bot (journaux non désinfectés) | `[]`                                   |

---

## Types de messages pris en charge

### Recevoir

- ✅ Texte
- ✅ Images
- ✅ Fichiers
- ✅ Audio / Voix
- ✅ Vidéo
- ✅ Autocollants / Emoji personnalisé
- ✅ Éléments personnalisés (cartes de lien, etc.)

### Envoyer

- ✅ Texte (avec support markdown)
- ✅ Images
- ✅ Fichiers
- ✅ Audio
- ✅ Vidéo
- ✅ Autocollants

### Threads et réponses

- ✅ Réponses avec citation (configurable via `replyToMode`)
- ❌ Réponses de thread (non pris en charge par la plateforme)

---

## Connexes

- [Aperçu des canaux](/fr/channels) — tous les canaux pris en charge
- [Appairage](/fr/channels/pairing) — authentification DM et flux d'appairage
- [Groupes](/fr/channels/groups) — comportement du chat de groupe et gating de mention
- [Routage de canal](/fr/channels/channel-routing) — routage de session pour les messages
- [Sécurité](/fr/gateway/security) — modèle d'accès et renforcement
