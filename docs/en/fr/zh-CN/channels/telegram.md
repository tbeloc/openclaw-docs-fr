# Telegram（Bot API）

Statut : Support des messages privés et des groupes via grammY, prêt pour la production. Long polling par défaut ; webhook optionnel.

## Configuration rapide (démarrage)

1. Créez un bot via **@BotFather** ([lien direct](https://t.me/BotFather)). Confirmez que le nom d'utilisateur est bien `@BotFather`, puis copiez le token.
2. Configurez le token :
   - Variable d'environnement : `TELEGRAM_BOT_TOKEN=...`
   - Ou configuration : `channels.telegram.botToken: "..."`
   - Si les deux sont définis, la configuration a priorité (repli sur variable d'environnement pour le compte par défaut uniquement).
3. Démarrez la Gateway.
4. L'accès aux messages privés utilise par défaut le mode appairage ; l'approbation du code d'appairage est requise au premier contact.

Configuration minimale :

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",
    },
  },
}
```

## Qu'est-ce que c'est

- Un canal Telegram Bot API détenu par la Gateway.
- Routage déterministe : les réponses reviennent à Telegram ; le modèle ne choisit pas le canal.
- Les messages privés partagent la session principale de l'agent ; les groupes restent isolés (`agent:<agentId>:telegram:group:<chatId>`).

## Configuration (chemin rapide)

### 1) Créer un token bot (BotFather)

1. Ouvrez Telegram et discutez avec **@BotFather** ([lien direct](https://t.me/BotFather)). Confirmez que le nom d'utilisateur est bien `@BotFather`.
2. Exécutez `/newbot`, puis suivez les instructions (nom + nom d'utilisateur se terminant par `bot`).
3. Copiez le token et conservez-le en sécurité.

Configuration optionnelle de BotFather :

- `/setjoingroups` — Autoriser/refuser l'ajout du bot aux groupes.
- `/setprivacy` — Contrôler si le bot peut voir tous les messages de groupe.

### 2) Configurer le token (variable d'environnement ou fichier de configuration)

Exemple :

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```

Option de variable d'environnement : `TELEGRAM_BOT_TOKEN=...` (pour le compte par défaut).
Si la variable d'environnement et la configuration sont toutes deux définies, la configuration a priorité.

Support multi-comptes : utilisez `channels.telegram.accounts`, chaque compte ayant son propre token et un `name` optionnel. Voir [`gateway/configuration`](/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) pour les modes partagés.

3. Démarrez la Gateway. Telegram démarre quand le token est résolu avec succès (configuration en priorité, repli sur variable d'environnement).
4. L'accès aux messages privés est par défaut en mode appairage. Le bot approuve le code d'appairage au premier contact.
5. Pour les groupes : ajoutez le bot, décidez du comportement de confidentialité/administrateur (voir ci-dessous), puis configurez `channels.telegram.groups` pour contrôler la porte de mention et la liste d'autorisation.

## Token + Confidentialité + Permissions (côté Telegram)

### Création de token (BotFather)

- `/newbot` crée un bot et retourne un token (gardez-le secret).
- Si le token fuit, révoquez/régénérez via @BotFather et mettez à jour votre configuration.

### Visibilité des messages de groupe (mode confidentialité)

Les bots Telegram ont le **mode confidentialité** activé par défaut, ce qui limite les messages de groupe qu'ils reçoivent.
Si votre bot doit voir *tous* les messages de groupe, vous avez deux options :

- Utilisez `/setprivacy` pour désactiver le mode confidentialité **OU**
- Ajoutez le bot comme **administrateur** du groupe (les bots administrateurs reçoivent tous les messages).

**Remarque :** Quand vous basculez le mode confidentialité, Telegram exige que vous retiriez le bot de chaque groupe et le rajoutiez pour que les modifications prennent effet.

### Permissions de groupe (permissions administrateur)

Le statut d'administrateur est défini dans le groupe (interface Telegram). Les bots administrateurs reçoivent toujours tous les messages de groupe, donc utilisez le statut d'administrateur si vous avez besoin d'une visibilité complète.

## Fonctionnement (comportement)

- Les messages entrants sont normalisés en enveloppe de canal partagée, contenant le contexte de réponse et les espaces réservés de médias.
- Les réponses de groupe nécessitent par défaut une mention (mention native @mention ou `agents.list[].groupChat.mentionPatterns` / `messages.groupChat.mentionPatterns`).
- Couverture multi-agents : définissez les modèles par agent sur `agents.list[].groupChat.mentionPatterns`.
- Les réponses sont toujours routées vers le même chat Telegram.
- Le long polling utilise le runner grammY, traitant chaque chat séquentiellement ; la concurrence globale est limitée par `agents.defaults.maxConcurrent`.
- L'API Telegram Bot ne supporte pas les accusés de réception de lecture ; pas d'option `sendReadReceipts`.

## Streaming de brouillon

OpenClaw peut streamer des réponses partielles dans les messages privés Telegram en utilisant `sendMessageDraft`.

Exigences :

- Activez le mode thread (mode sujet de forum) pour le bot dans @BotFather.
- Limité aux threads de chat privé (Telegram inclut `message_thread_id` dans les messages entrants).
- `channels.telegram.streamMode` n'est pas défini sur `"off"` (par défaut : `"partial"`, `"block"` active les mises à jour de brouillon par chunk).

Le streaming de brouillon est limité aux messages privés ; Telegram ne supporte pas cette fonctionnalité dans les groupes ou canaux.

## Formatage (HTML Telegram)

- Le texte Telegram sortant utilise `parse_mode: "HTML"` (sous-ensemble de balises supportées par Telegram).
- L'entrée de type Markdown est rendue en **HTML sûr pour Telegram** (gras/italique/barré/code/lien) ; les éléments au niveau bloc sont aplatis en texte avec sauts de ligne/puces.
- Le HTML brut du modèle est échappé pour éviter les erreurs d'analyse Telegram.
- Si Telegram rejette la charge HTML, OpenClaw réessaie le même message en texte brut.

## Commandes (natives + personnalisées)

OpenClaw enregistre les commandes natives (comme `/status`, `/reset`, `/model`) dans le menu bot de Telegram au démarrage.
Vous pouvez ajouter des commandes personnalisées au menu via la configuration :

```json5
{
  channels: {
    telegram: {
      customCommands: [
        { command: "backup", description: "Sauvegarde Git" },
        { command: "generate", description: "Créer une image" },
      ],
    },
  },
}
```

## Dépannage

- `setMyCommands failed` dans les logs signifie généralement que le HTTPS/DNS sortant vers `api.telegram.org` est bloqué.
- Si vous voyez `sendMessage` ou `sendChatAction` échouer, vérifiez le routage IPv6 et le DNS.

Plus d'aide : [Dépannage des canaux](/channels/troubleshooting).

Remarques :

- Les commandes personnalisées sont **uniquement des entrées de menu** ; OpenClaw ne les implémente pas à moins que vous les traitiez ailleurs.
- Les noms de commande sont normalisés (suppression du `/` initial, minuscules), doivent correspondre à `a-z`, `0-9`, `_` (1-32 caractères).
- Les commandes personnalisées **ne peuvent pas remplacer les commandes natives**. Les conflits sont ignorés et enregistrés.
- Si `commands.native` est désactivé, seules les commandes personnalisées sont enregistrées (ou aucune si vide).

## Limitations

- Le texte sortant est chunké par `channels.telegram.textChunkLimit` (par défaut 4000).
- Chunking optionnel par saut de ligne : définissez `channels.telegram.chunkMode="newline"` pour diviser par lignes vides (limites de paragraphes) avant le chunking par longueur.
- Le téléchargement/chargement de médias est limité par `channels.telegram.mediaMaxMb` (par défaut 5).
- Les requêtes Telegram Bot API expirent après `channels.telegram.timeoutSeconds` (par défaut 500 via grammY). Définissez une valeur inférieure pour éviter les blocages prolongés.
- Le contexte d'historique de groupe utilise `channels.telegram.historyLimit` (ou `channels.telegram.accounts.*.historyLimit`), repli sur `messages.groupChat.historyLimit`. Définissez `0` pour désactiver (par défaut 50).
- L'historique des messages privés peut être limité avec `channels.telegram.dmHistoryLimit` (tours utilisateur). Remplacement par utilisateur : `channels.telegram.dms["<user_id>"].historyLimit`.

## Modes d'activation de groupe

Par défaut, le bot ne répond aux mentions dans les groupes (`@botname` ou modèles dans `agents.list[].groupChat.mentionPatterns`). Pour changer ce comportement :

### Via configuration (recommandé)

```json5
{
  channels: {
    telegram: {
      groups: {
        "-1001234567890": { requireMention: false }, // Toujours répondre dans ce groupe
      },
    },
  },
}
```

**Important :** Définir `channels.telegram.groups` crée une **liste d'autorisation** - seuls les groupes listés (ou `"*"`) seront acceptés.
Les sujets de forum héritent de la configuration de leur groupe parent (allowFrom, requireMention, skills, prompts), sauf si vous ajoutez des remplacements par sujet sous `channels.telegram.groups.<groupId>.topics.<topicId>`.

Pour autoriser tous les groupes et toujours répondre :

```json5
{
  channels: {
    telegram: {
      groups: {
        "*": { requireMention: false }, // Tous les groupes, toujours répondre
      },
    },
  },
}
```

Pour garder tous les groupes en réponse mention uniquement (comportement par défaut) :

```json5
{
  channels: {
    telegram: {
      groups: {
        "*": { requireMention: true }, // Ou omettez complètement groups
      },
    },
  },
}
```

### Via commande (niveau session)

Dans un groupe, envoyez :

- `/activation always` - Répondre à tous les messages
- `/activation mention` - Nécessite une mention (par défaut)

**Remarque :** Les commandes ne mettent à jour que l'état de la session. Pour conserver le comportement persistant après redémarrage, utilisez la configuration.

### Obtenir l'ID de chat de groupe

Transférez n'importe quel message du groupe à `@userinfobot` ou `@getidsbot` sur Telegram pour voir l'ID de chat (nombre négatif, comme `-1001234567890`).

**Conseil :** Pour obtenir votre propre ID utilisateur, envoyez un message privé à votre bot, il répondra avec votre ID utilisateur (message d'appairage), ou utilisez `/whoami` une fois les commandes activées.

**Remarque de confidentialité :** `@userinfobot` est un bot tiers. Si vous préférez une autre méthode, ajoutez le bot au groupe, envoyez un message, puis utilisez `openclaw logs --follow` pour lire `chat.id`, ou utilisez l'API Bot `getUpdates`.

## Écritures de configuration

Par défaut, Telegram autorise les mises à jour de configuration déclenchées par des événements de canal ou `/config set|unset`.

Cela se produit quand :

- Un groupe est mis à niveau vers un super-groupe, Telegram émet `migrate_to_chat_id` (l'ID de chat change). OpenClaw peut migrer automatiquement `channels.telegram.groups`.
- Vous exécutez `/config set` ou `/config unset` dans un chat Telegram (nécessite `commands.config: true`).

Pour désactiver :

```json5
{
  channels: { telegram: { configWrites: false } },
}
```

## Sujets (super-groupes de forum)

Les sujets de forum Telegram incluent `message_thread_id` dans chaque message. OpenClaw :

- Ajoute `:topic:<threadId>` à la clé de session du groupe Telegram, isolant chaque sujet.
- Envoie les indicateurs de saisie et les réponses avec `message_thread_id`, gardant les réponses dans le sujet.
- Le sujet générique (ID de thread `1`) est spécial : l'envoi de message omet `message_thread_id` (Telegram le rejetterait), mais l'indicateur de saisie l'inclut toujours.
- Expose `MessageThreadId` + `IsForum` dans le contexte de modèle pour le routage/modèles.
- La configuration spécifique au sujet peut être définie sous `channels.telegram.groups.<chatId>.topics.<threadId>` (skills, liste d'autorisation, réponse automatique, invite système, désactivé).
- La configuration du sujet hérite des paramètres du groupe (requireMention, liste d'autorisation, skills, invites, activé), sauf remplacement par sujet.

Les chats privés peuvent inclure `message_thread_id` dans certains cas limites. OpenClaw garde la clé de session des messages privés inchangée, mais l'utilise toujours pour les réponses/streaming de brouillon quand un ID de thread est présent.

## Boutons en ligne

Telegram supporte les claviers en ligne avec boutons de rappel.

```json5
{
  channels: {
    telegram: {
      capabilities: {
        inlineButtons: "allowlist",
      },
    },
  },
}
```

Pour la configuration par compte :

```json5
{
  channels: {
    telegram: {
      accounts: {
        main: {
          capabilities: {
            inlineButtons: "allowlist",
          },
        },
      },
    },
  },
}
```

Portées :

- `off` — Désactiver les boutons en ligne
- `dm` — Messages privés uniquement (cibles de groupe bloquées)
- `group` — Groupes uniquement (cibles de messages privés bloquées)
- `all
