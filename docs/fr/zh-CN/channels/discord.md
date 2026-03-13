# Discord（Bot API）

Statut : Pris en charge pour la communication par message privé et canal textuel serveur via la passerelle officielle Discord Bot.

## Configuration rapide (débutants)

1. Créez un bot Discord et copiez le jeton du bot.
2. Activez **Message Content Intent** dans les paramètres de l'application Discord (et **Server Members Intent** si vous prévoyez d'utiliser une liste d'autorisation ou une recherche par nom).
3. Configurez le jeton pour OpenClaw :
   - Variable d'environnement : `DISCORD_BOT_TOKEN=...`
   - Ou configuration : `channels.discord.token: "..."`
   - Si les deux sont définis, la configuration a priorité (la variable d'environnement est un repli pour le compte par défaut uniquement).
4. Invitez le bot à votre serveur avec les permissions de message (ou créez un serveur privé si vous souhaitez utiliser uniquement les messages privés).
5. Démarrez la passerelle Gateway.
6. L'accès aux messages privés utilise par défaut le mode d'appairage ; l'approbation d'un code d'appairage est requise au premier contact.

Configuration minimale :

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "YOUR_BOT_TOKEN",
    },
  },
}
```

## Objectifs

- Discuter avec OpenClaw via les messages privés Discord ou les canaux serveur.
- Les chats directs sont fusionnés dans la session principale de l'agent (par défaut `agent:main:main`) ; les canaux serveur restent isolés en tant que `agent:<agentId>:discord:channel:<channelId>` (le nom d'affichage utilise `discord:<guildSlug>#<channelSlug>`).
- Les messages privés de groupe sont ignorés par défaut ; activez-les via `channels.discord.dm.groupEnabled`, avec restriction optionnelle via `channels.discord.dm.groupChannels`.
- Maintenir le routage déterministe : les réponses reviennent toujours au canal source du message.

## Fonctionnement

1. Créez une application Discord → Bot, activez les intentions dont vous avez besoin (messages privés + messages serveur + contenu des messages), et obtenez le jeton du bot.
2. Invitez le bot à votre serveur avec les permissions requises pour lire/envoyer des messages où vous souhaitez l'utiliser.
3. Configurez OpenClaw avec `channels.discord.token` (ou utilisez `DISCORD_BOT_TOKEN` comme repli).
4. Exécutez la passerelle Gateway ; elle démarre automatiquement le canal Discord lorsque le jeton est disponible (configuration en priorité, repli sur variable d'environnement) et que `channels.discord.enabled` n'est pas `false`.
   - Si vous préférez utiliser une variable d'environnement, définissez `DISCORD_BOT_TOKEN` (le bloc de configuration est optionnel).
5. Chats directs : utilisez `user:<id>` (ou mentionnez `<@id>`) lors de l'envoi ; toutes les conversations entrent dans la session partagée `main`. Les ID numériques seuls sont ambigus et seront rejetés.
6. Canaux serveur : utilisez `channel:<channelId>` lors de l'envoi. La mention est requise par défaut, configurable par serveur ou par canal.
7. Chats directs : protégés par défaut via `channels.discord.dm.policy` (par défaut : `"pairing"`). Les expéditeurs inconnus reçoivent un code d'appairage (expire après 1 heure) ; approuvez-le via `openclaw pairing approve discord <code>`.
   - Pour conserver l'ancien comportement "ouvert à tous" : définissez `channels.discord.dm.policy="open"` et `channels.discord.dm.allowFrom=["*"]`.
   - Pour utiliser une liste d'autorisation codée en dur : définissez `channels.discord.dm.policy="allowlist"` et listez les expéditeurs dans `channels.discord.dm.allowFrom`.
   - Pour ignorer tous les messages privés : définissez `channels.discord.dm.enabled=false` ou `channels.discord.dm.policy="disabled"`.
8. Les messages privés de groupe sont ignorés par défaut ; activez-les via `channels.discord.dm.groupEnabled`, avec restriction optionnelle via `channels.discord.dm.groupChannels`.
9. Règles serveur optionnelles : définissez `channels.discord.guilds`, avec des clés par ID serveur (préféré) ou slug, et incluez les règles pour chaque canal.
10. Commandes natives optionnelles : `commands.native` est par défaut `"auto"` (activé pour Discord/Telegram, désactivé pour Slack). Remplacez avec `channels.discord.commands.native: true|false|"auto"` ; `false` efface les commandes précédemment enregistrées. Les commandes texte sont contrôlées par `commands.text`, doivent être envoyées comme des messages `/...` distincts. Utilisez `commands.useAccessGroups: false` pour ignorer la vérification des groupes d'accès pour les commandes.
    - Liste complète des commandes + configuration : [Commandes slash](/tools/slash-commands)
11. Historique de contexte serveur optionnel : définissez `channels.discord.historyLimit` (par défaut 20, repli sur `messages.groupChat.historyLimit`) pour inclure les N derniers messages serveur comme contexte lors de la mention de réponses. Définissez `0` pour désactiver.
12. Réactions emoji : les agents peuvent déclencher des réactions emoji via l'outil `discord` (contrôlé par `channels.discord.actions.*`).
    - Sémantique de suppression des réactions emoji : voir [/tools/reactions](/tools/reactions).
    - L'outil `discord` n'est exposé que lorsque le canal actuel est Discord.
13. Les commandes natives utilisent des clés de session isolées (`agent:<agentId>:discord:slash:<userId>`) plutôt que la session partagée `main`.

Remarque : la résolution nom → ID utilise la recherche de membres serveur, nécessitant Server Members Intent ; si le bot ne peut pas rechercher les membres, utilisez des ID ou des mentions `<@id>`.
Remarque : les slugs sont en minuscules, les espaces remplacés par `-`. Le slug du nom de canal n'inclut pas le `#` initial.
Remarque : les lignes de contexte serveur `[from:]` incluent `author.tag` + `id` pour faciliter les réponses mentionnables.

## Écritures de configuration

Par défaut, les écritures de configuration déclenchées par `/config set|unset` sont autorisées pour Discord (nécessite `commands.config: true`).

Pour désactiver :

```json5
{
  channels: { discord: { configWrites: false } },
}
```

## Comment créer votre propre bot

Ceci est la configuration du "Portail des développeurs Discord" pour exécuter OpenClaw dans les canaux serveur (comme `#help`).

### 1) Créer une application Discord + utilisateur bot

1. Portail des développeurs Discord → **Applications** → **New Application**
2. Dans votre application :
   - **Bot** → **Add Bot**
   - Copiez **Bot Token** (c'est ce que vous mettez dans `DISCORD_BOT_TOKEN`)

### 2) Activer les intentions de passerelle requises par OpenClaw

Discord bloque les "intentions privilégiées" à moins que vous ne les activiez explicitement.

Dans **Bot** → **Privileged Gateway Intents**, activez :

- **Message Content Intent** (nécessaire pour lire le texte des messages sur la plupart des serveurs ; sans cela, vous verrez "Used disallowed intents" ou le bot se connectera mais ne répondra pas aux messages)
- **Server Members Intent** (recommandé ; certaines recherches de membres/utilisateurs et correspondances de liste d'autorisation dans les serveurs en ont besoin)

Vous n'avez généralement **pas besoin** de **Presence Intent**.

### 3) Générer une URL d'invitation (Générateur d'URL OAuth2)

Dans votre application : **OAuth2** → **URL Generator**

**Scopes**

- ✅ `bot`
- ✅ `applications.commands` (requis pour les commandes natives)

**Permissions du bot** (base minimale)

- ✅ View Channels
- ✅ Send Messages
- ✅ Read Message History
- ✅ Embed Links
- ✅ Attach Files
- ✅ Add Reactions (optionnel mais recommandé)
- ✅ Use External Emojis / Stickers (optionnel ; uniquement si nécessaire)

Évitez **Administrator** à moins que vous ne déboguiez et que vous fassiez entièrement confiance au bot.

Copiez l'URL générée, ouvrez-la, sélectionnez votre serveur, puis installez le bot.

### 4) Obtenir les ID (serveur/utilisateur/canal)

Discord utilise des ID numériques partout ; la configuration OpenClaw privilégie les ID.

1. Discord (bureau/web) → **Paramètres utilisateur** → **Avancé** → Activez **Mode développeur**
2. Clic droit sur :
   - Nom du serveur → **Copier l'ID du serveur** (ID serveur)
   - Canal (par exemple `#help`) → **Copier l'ID du canal**
   - Votre utilisateur → **Copier l'ID utilisateur**

### 5) Configurer OpenClaw

#### Jeton

Définissez le jeton du bot via une variable d'environnement (recommandé sur serveur) :

- `DISCORD_BOT_TOKEN=...`

Ou via la configuration :

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "YOUR_BOT_TOKEN",
    },
  },
}
```

Support multi-comptes : utilisez `channels.discord.accounts`, chaque compte ayant son propre jeton et un `name` optionnel. Voir [`gateway/configuration`](/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) pour le modèle générique.

#### Liste d'autorisation + routage des canaux

Exemple "un serveur, seulement moi, seulement #help" :

```json5
{
  channels: {
    discord: {
      enabled: true,
      dm: { enabled: false },
      guilds: {
        YOUR_GUILD_ID: {
          users: ["YOUR_USER_ID"],
          requireMention: true,
          channels: {
            help: { allow: true, requireMention: true },
          },
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

Remarques :

- `requireMention: true` signifie que le bot ne répond que s'il est mentionné (recommandé pour les canaux partagés).
- `agents.list[].groupChat.mentionPatterns` (ou `messages.groupChat.mentionPatterns`) compte également comme une mention pour les messages serveur.
- Surcharge multi-agents : définissez les modèles par agent sur `agents.list[].groupChat.mentionPatterns`.
- Si `channels` existe, tout canal non listé est rejeté par défaut.
- Utilisez une entrée de canal `"*"` pour appliquer les valeurs par défaut à tous les canaux ; les entrées de canal explicites remplacent le joker.
- Les fils héritent de la configuration du canal parent (liste d'autorisation, `requireMention`, Skills, invite système, etc.), sauf si vous ajoutez explicitement l'ID du canal de fil.
- Les messages envoyés par le bot sont ignorés par défaut ; définissez `channels.discord.allowBots=true` pour les autoriser (vos propres messages sont toujours filtrés).
- Avertissement : si vous autorisez les réponses à d'autres bots (`channels.discord.allowBots=true`), utilisez `requireMention`, les listes d'autorisation `channels.discord.guilds.*.channels.<id>.users` et/ou définissez des garde-fous explicites dans `AGENTS.md` et `SOUL.md` pour éviter les boucles de réponse entre bots.

### 6) Vérifier que cela fonctionne

1. Démarrez la passerelle Gateway.
2. Envoyez dans votre canal serveur : `@Krill hello` (ou le nom de votre bot).
3. Si pas de réponse : consultez **Dépannage** ci-dessous.

### Dépannage

- D'abord : exécutez `openclaw doctor` et `openclaw channels status --probe` (avertissements exploitables + audit rapide).
- **"Used disallowed intents"** : activez **Message Content Intent** dans le portail des développeurs (et possiblement **Server Members Intent**), puis redémarrez la passerelle Gateway.
- **Le bot se connecte mais ne répond jamais dans les canaux serveur** :
  - **Message Content Intent** manquant, ou
  - Le bot manque de permissions de canal (View/Send/Read History), ou
  - Votre configuration nécessite une mention mais vous ne l'avez pas mentionné, ou
  - Votre liste d'autorisation serveur/canal rejette le canal/utilisateur.
- **`requireMention: false` mais toujours pas de réponse** :
- `channels.discord.groupPolicy` est par défaut **allowlist** ; définissez-le sur `"open"` ou ajoutez une entrée serveur sous `channels.discord.guilds` (optionnellement listez les canaux sous `channels.discord.guilds.<id>.channels` pour restreindre).
  - Si vous avez seulement défini `DISCORD_BOT_TOKEN` et n'avez jamais créé la section `channels.discord`, le runtime définira par défaut `groupPolicy` sur `open`. Ajoutez `channels.discord.groupPolicy`, `channels.defaults.groupPolicy` ou des listes d'autorisation serveur/canal pour le verrouiller.
- `requireMention` doit être sous `channels.discord.guilds` (ou un canal spécifique). Le `channels.discord.requireMention` de haut niveau est ignoré.
- **Audit des permissions** (`channels status --probe`) ne vérifie que les ID de canal numériques. Si vous utilisez slug/nom comme clés `channels.discord.guilds.*.channels`, l'audit ne peut pas vérifier les permissions.
- **Les messages privés ne fonctionnent pas** : `channels.discord.dm.enabled=false`, `channels.discord.dm.policy="disabled"`, ou vous n'avez pas encore été approuvé (`channels.discord.dm.policy="pairing"`).
- **Approbation d'exécution dans Discord** : Discord prend en charge l'**interface utilisateur des boutons** pour l'approbation d'exécution dans les messages privés (Autoriser une fois / Toujours autoriser / Refuser). `/approve <id> ...` est uniquement pour les approbations transférées, ne parse pas les invites de bouton Discord. Si vous
