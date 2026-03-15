---
summary: "Statut de support du bot Discord, capacités et configuration"
read_when:
  - Working on Discord channel features
title: "Discord"
---

# Discord (Bot API)

Statut : prêt pour les DMs et les canaux de serveur via la passerelle Discord officielle.

<CardGroup cols={3}>
  <Card title="Pairing" icon="link" href="/fr/channels/pairing">
    Les DMs Discord sont par défaut en mode appairage.
  </Card>
  <Card title="Slash commands" icon="terminal" href="/fr/tools/slash-commands">
    Comportement natif des commandes et catalogue de commandes.
  </Card>
  <Card title="Channel troubleshooting" icon="wrench" href="/fr/channels/troubleshooting">
    Diagnostics multi-canaux et flux de réparation.
  </Card>
</CardGroup>

## Configuration rapide

Vous devrez créer une nouvelle application avec un bot, ajouter le bot à votre serveur et l'appairer à OpenClaw. Nous recommandons d'ajouter votre bot à votre propre serveur privé. Si vous n'en avez pas encore, [créez-en un d'abord](https://support.discord.com/hc/en-us/articles/204849977-How-do-I-create-a-server) (choisissez **Create My Own > For me and my friends**).

<Steps>
  <Step title="Créer une application Discord et un bot">
    Allez sur le [Discord Developer Portal](https://discord.com/developers/applications) et cliquez sur **New Application**. Nommez-le quelque chose comme « OpenClaw ».

    Cliquez sur **Bot** dans la barre latérale. Définissez le **Username** sur le nom que vous donnez à votre agent OpenClaw.

  </Step>

  <Step title="Activer les intentions privilégiées">
    Toujours sur la page **Bot**, faites défiler vers le bas jusqu'à **Privileged Gateway Intents** et activez :

    - **Message Content Intent** (requis)
    - **Server Members Intent** (recommandé ; requis pour les listes blanches de rôles et la correspondance nom-à-ID)
    - **Presence Intent** (optionnel ; nécessaire uniquement pour les mises à jour de présence)

  </Step>

  <Step title="Copier votre jeton de bot">
    Remontez sur la page **Bot** et cliquez sur **Reset Token**.

    <Note>
    Malgré le nom, cela génère votre premier jeton — rien n'est en cours de « réinitialisation ».
    </Note>

    Copiez le jeton et enregistrez-le quelque part. C'est votre **Bot Token** et vous en aurez besoin bientôt.

  </Step>

  <Step title="Générer une URL d'invitation et ajouter le bot à votre serveur">
    Cliquez sur **OAuth2** dans la barre latérale. Vous allez générer une URL d'invitation avec les bonnes permissions pour ajouter le bot à votre serveur.

    Faites défiler vers le bas jusqu'à **OAuth2 URL Generator** et activez :

    - `bot`
    - `applications.commands`

    Une section **Bot Permissions** apparaîtra ci-dessous. Activez :

    - View Channels
    - Send Messages
    - Read Message History
    - Embed Links
    - Attach Files
    - Add Reactions (optionnel)

    Copiez l'URL générée en bas, collez-la dans votre navigateur, sélectionnez votre serveur et cliquez sur **Continue** pour vous connecter. Vous devriez maintenant voir votre bot sur le serveur Discord.

  </Step>

  <Step title="Activer le mode développeur et collecter vos ID">
    De retour dans l'application Discord, vous devez activer le mode développeur pour pouvoir copier les ID internes.

    1. Cliquez sur **User Settings** (icône d'engrenage à côté de votre avatar) → **Advanced** → activez **Developer Mode**
    2. Cliquez avec le bouton droit sur l'**icône de votre serveur** dans la barre latérale → **Copy Server ID**
    3. Cliquez avec le bouton droit sur **votre propre avatar** → **Copy User ID**

    Enregistrez votre **Server ID** et **User ID** à côté de votre Bot Token — vous enverrez tous les trois à OpenClaw à l'étape suivante.

  </Step>

  <Step title="Autoriser les DMs des membres du serveur">
    Pour que l'appairage fonctionne, Discord doit autoriser votre bot à vous envoyer des DMs. Cliquez avec le bouton droit sur l'**icône de votre serveur** → **Privacy Settings** → activez **Direct Messages**.

    Cela permet aux membres du serveur (y compris les bots) de vous envoyer des DMs. Gardez cela activé si vous souhaitez utiliser les DMs Discord avec OpenClaw. Si vous prévoyez d'utiliser uniquement les canaux de serveur, vous pouvez désactiver les DMs après l'appairage.

  </Step>

  <Step title="Étape 0 : Définir votre jeton de bot de manière sécurisée (ne l'envoyez pas en chat)">
    Votre jeton de bot Discord est un secret (comme un mot de passe). Définissez-le sur la machine exécutant OpenClaw avant de communiquer avec votre agent.

```bash
openclaw config set channels.discord.token '"YOUR_BOT_TOKEN"' --json
openclaw config set channels.discord.enabled true --json
openclaw gateway
```

    Si OpenClaw s'exécute déjà en tant que service en arrière-plan, utilisez plutôt `openclaw gateway restart`.

  </Step>

  <Step title="Configurer OpenClaw et appairer">

    <Tabs>
      <Tab title="Demander à votre agent">
        Discutez avec votre agent OpenClaw sur n'importe quel canal existant (par exemple Telegram) et dites-lui. Si Discord est votre premier canal, utilisez plutôt l'onglet CLI / config.

        > "I already set my Discord bot token in config. Please finish Discord setup with User ID `<user_id>` and Server ID `<server_id>`."
      </Tab>
      <Tab title="CLI / config">
        Si vous préférez la configuration basée sur des fichiers, définissez :

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

        Secours env pour le compte par défaut :

```bash
DISCORD_BOT_TOKEN=...
```

        Les valeurs SecretRef sont également supportées pour `channels.discord.token` (fournisseurs env/file/exec). Voir [Secrets Management](/fr/gateway/secrets).

      </Tab>
    </Tabs>

  </Step>

  <Step title="Approuver le premier appairage DM">
    Attendez que la passerelle soit en cours d'exécution, puis envoyez un DM à votre bot sur Discord. Il répondra avec un code d'appairage.

    <Tabs>
      <Tab title="Demander à votre agent">
        Envoyez le code d'appairage à votre agent sur votre canal existant :

        > "Approve this Discord pairing code: `<CODE>`"
      </Tab>
      <Tab title="CLI">

```bash
openclaw pairing list discord
openclaw pairing approve discord <CODE>
```

      </Tab>
    </Tabs>

    Les codes d'appairage expirent après 1 heure.

    Vous devriez maintenant pouvoir discuter avec votre agent sur Discord via DM.

  </Step>
</Steps>

<Note>
La résolution des jetons est consciente du compte. Les valeurs de jeton de config l'emportent sur le secours env. `DISCORD_BOT_TOKEN` n'est utilisé que pour le compte par défaut.
Pour les appels sortants avancés (outil de message/actions de canal), un `token` explicite par appel est utilisé pour cet appel. Les paramètres de politique de compte/nouvelle tentative proviennent toujours du compte sélectionné dans l'instantané d'exécution actif.
</Note>

## Recommandé : Configurer un espace de travail de serveur

Une fois que les DMs fonctionnent, vous pouvez configurer votre serveur Discord comme un espace de travail complet où chaque canal obtient sa propre session d'agent avec son propre contexte. Ceci est recommandé pour les serveurs privés où il n'y a que vous et votre bot.

<Steps>
  <Step title="Ajouter votre serveur à la liste blanche de serveur">
    Cela permet à votre agent de répondre dans n'importe quel canal de votre serveur, pas seulement les DMs.

    <Tabs>
      <Tab title="Demander à votre agent">
        > "Add my Discord Server ID `<server_id>` to the guild allowlist"
      </Tab>
      <Tab title="Config">

```json5
{
  channels: {
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        YOUR_SERVER_ID: {
          requireMention: true,
          users: ["YOUR_USER_ID"],
        },
      },
    },
  },
}
```

      </Tab>
    </Tabs>

  </Step>

  <Step title="Autoriser les réponses sans @mention">
    Par défaut, votre agent ne répond dans les canaux de serveur que lorsqu'il est @mentionné. Pour un serveur privé, vous voudrez probablement qu'il réponde à chaque message.

    <Tabs>
      <Tab title="Demander à votre agent">
        > "Allow my agent to respond on this server without having to be @mentioned"
      </Tab>
      <Tab title="Config">
        Définissez `requireMention: false` dans votre configuration de serveur :

```json5
{
  channels: {
    discord: {
      guilds: {
        YOUR_SERVER_ID: {
          requireMention: false,
        },
      },
    },
  },
}
```

      </Tab>
    </Tabs>

  </Step>

  <Step title="Planifier la mémoire dans les canaux de serveur">
    Par défaut, la mémoire à long terme (MEMORY.md) ne se charge que dans les sessions DM. Les canaux de serveur ne chargent pas automatiquement MEMORY.md.

    <Tabs>
      <Tab title="Demander à votre agent">
        > "When I ask questions in Discord channels, use memory_search or memory_get if you need long-term context from MEMORY.md."
      </Tab>
      <Tab title="Manuel">
        Si vous avez besoin d'un contexte partagé dans chaque canal, mettez les instructions stables dans `AGENTS.md` ou `USER.md` (elles sont injectées pour chaque session). Conservez les notes à long terme dans `MEMORY.md` et accédez-y à la demande avec les outils de mémoire.
      </Tab>
    </Tabs>

  </Step>
</Steps>

Créez maintenant quelques canaux sur votre serveur Discord et commencez à discuter. Votre agent peut voir le nom du canal, et chaque canal obtient sa propre session isolée — vous pouvez donc configurer `#coding`, `#home`, `#research`, ou tout ce qui correspond à votre flux de travail.

## Modèle d'exécution

- La passerelle possède la connexion Discord.
- Le routage des réponses est déterministe : les réponses entrantes Discord reviennent à Discord.
- Par défaut (`session.dmScope=main`), les chats directs partagent la session principale de l'agent (`agent:main:main`).
- Les canaux de serveur sont des clés de session isolées (`agent:<agentId>:discord:channel:<channelId>`).
- Les DMs de groupe sont ignorés par défaut (`channels.discord.dm.groupEnabled=false`).
- Les commandes slash natives s'exécutent dans des sessions de commande isolées (`agent:<agentId>:discord:slash:<userId>`), tout en portant `CommandTargetSessionKey` à la session de conversation routée.

## Canaux de forum

Les canaux de forum et de médias Discord n'acceptent que les publications de fil. OpenClaw supporte deux façons de les créer :

- Envoyez un message au parent du forum (`channel:<forumId>`) pour créer automatiquement un fil. Le titre du fil utilise la première ligne non vide de votre message.
- Utilisez `openclaw message thread create` pour créer un fil directement. Ne passez pas `--message-id` pour les canaux de forum.

Exemple : envoyer au parent du forum pour créer un fil

```bash
openclaw message send --channel discord --target channel:<forumId> \
  --message "Topic title\nBody of the post"
```

Exemple : créer un fil de forum explicitement

```bash
openclaw message thread create --channel discord --target channel:<forumId> \
  --thread-name "Topic title" --message "Body of the post"
```

Les parents de forum n'acceptent pas les composants Discord. Si vous avez besoin de composants, envoyez au fil lui-même (`channel:<threadId>`).

## Composants interactifs

OpenClaw prend en charge les conteneurs de composants Discord v2 pour les messages d'agent. Utilisez l'outil de message avec une charge utile `components`. Les résultats d'interaction sont redirigés vers l'agent en tant que messages entrants normaux et suivent les paramètres `replyToMode` Discord existants.

Blocs pris en charge :

- `text`, `section`, `separator`, `actions`, `media-gallery`, `file`
- Les lignes d'action permettent jusqu'à 5 boutons ou un seul menu de sélection
- Types de sélection : `string`, `user`, `role`, `mentionable`, `channel`

Par défaut, les composants sont à usage unique. Définissez `components.reusable=true` pour permettre aux boutons, sélections et formulaires d'être utilisés plusieurs fois jusqu'à leur expiration.

Pour restreindre qui peut cliquer sur un bouton, définissez `allowedUsers` sur ce bouton (ID utilisateur Discord, tags ou `*`). Lorsqu'il est configuré, les utilisateurs non correspondants reçoivent un refus éphémère.

Les commandes slash `/model` et `/models` ouvrent un sélecteur de modèle interactif avec des menus déroulants de fournisseur et de modèle plus une étape Soumettre. La réponse du sélecteur est éphémère et seul l'utilisateur qui l'invoque peut l'utiliser.

Pièces jointes :

- Les blocs `file` doivent pointer vers une référence de pièce jointe (`attachment://<filename>`)
- Fournissez la pièce jointe via `media`/`path`/`filePath` (fichier unique) ; utilisez `media-gallery` pour plusieurs fichiers
- Utilisez `filename` pour remplacer le nom de téléchargement lorsqu'il doit correspondre à la référence de pièce jointe

Formulaires modaux :

- Ajoutez `components.modal` avec jusqu'à 5 champs
- Types de champs : `text`, `checkbox`, `radio`, `select`, `role-select`, `user-select`
- OpenClaw ajoute automatiquement un bouton de déclenchement

Exemple :

```json5
{
  channel: "discord",
  action: "send",
  to: "channel:123456789012345678",
  message: "Optional fallback text",
  components: {
    reusable: true,
    text: "Choose a path",
    blocks: [
      {
        type: "actions",
        buttons: [
          {
            label: "Approve",
            style: "success",
            allowedUsers: ["123456789012345678"],
          },
          { label: "Decline", style: "danger" },
        ],
      },
      {
        type: "actions",
        select: {
          type: "string",
          placeholder: "Pick an option",
          options: [
            { label: "Option A", value: "a" },
            { label: "Option B", value: "b" },
          ],
        },
      },
    ],
    modal: {
      title: "Details",
      triggerLabel: "Open form",
      fields: [
        { type: "text", label: "Requester" },
        {
          type: "select",
          label: "Priority",
          options: [
            { label: "Low", value: "low" },
            { label: "High", value: "high" },
          ],
        },
      ],
    },
  },
}
```

## Contrôle d'accès et routage

<Tabs>
  <Tab title="Politique des MP">
    `channels.discord.dmPolicy` contrôle l'accès aux MP (héritage : `channels.discord.dm.policy`) :

    - `pairing` (par défaut)
    - `allowlist`
    - `open` (nécessite que `channels.discord.allowFrom` inclue `"*"` ; héritage : `channels.discord.dm.allowFrom`)
    - `disabled`

    Si la politique des MP n'est pas ouverte, les utilisateurs inconnus sont bloqués (ou invités à s'appairer en mode `pairing`).

    Précédence multi-compte :

    - `channels.discord.accounts.default.allowFrom` s'applique uniquement au compte `default`.
    - Les comptes nommés héritent de `channels.discord.allowFrom` lorsque leur propre `allowFrom` n'est pas défini.
    - Les comptes nommés n'héritent pas de `channels.discord.accounts.default.allowFrom`.

    Format de destination des MP pour la livraison :

    - `user:<id>`
    - mention `<@id>`

    Les ID numériques nus sont ambigus et rejetés sauf si un type de cible utilisateur/canal explicite est fourni.

  </Tab>

  <Tab title="Politique de guilde">
    La gestion de la guilde est contrôlée par `channels.discord.groupPolicy` :

    - `open`
    - `allowlist`
    - `disabled`

    La ligne de base sécurisée lorsque `channels.discord` existe est `allowlist`.

    Comportement de `allowlist` :

    - la guilde doit correspondre à `channels.discord.guilds` (`id` préféré, slug accepté)
    - listes blanches d'expéditeurs optionnelles : `users` (ID stables recommandés) et `roles` (ID de rôle uniquement) ; si l'un d'eux est configuré, les expéditeurs sont autorisés lorsqu'ils correspondent à `users` OU `roles`
    - la correspondance directe par nom/tag est désactivée par défaut ; activez `channels.discord.dangerouslyAllowNameMatching: true` uniquement comme mode de compatibilité d'urgence
    - les noms/tags sont pris en charge pour `users`, mais les ID sont plus sûrs ; `openclaw security audit` avertit lorsque des entrées de nom/tag sont utilisées
    - si une guilde a `channels` configuré, les canaux non listés sont refusés
    - si une guilde n'a pas de bloc `channels`, tous les canaux de cette guilde autorisée sont autorisés

    Exemple :

```json5
{
  channels: {
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        "123456789012345678": {
          requireMention: true,
          ignoreOtherMentions: true,
          users: ["987654321098765432"],
          roles: ["123456789012345678"],
          channels: {
            general: { allow: true },
            help: { allow: true, requireMention: true },
          },
        },
      },
    },
  },
}
```

    Si vous définissez uniquement `DISCORD_BOT_TOKEN` et ne créez pas de bloc `channels.discord`, le repli à l'exécution est `groupPolicy="allowlist"` (avec un avertissement dans les journaux), même si `channels.defaults.groupPolicy` est `open`.

  </Tab>

  <Tab title="Mentions et MP de groupe">
    Les messages de guilde sont contrôlés par mention par défaut.

    La détection de mention inclut :

    - mention explicite du bot
    - modèles de mention configurés (`agents.list[].groupChat.mentionPatterns`, repli `messages.groupChat.mentionPatterns`)
    - comportement implicite de réponse au bot dans les cas pris en charge

    `requireMention` est configuré par guilde/canal (`channels.discord.guilds...`).
    `ignoreOtherMentions` supprime optionnellement les messages qui mentionnent un autre utilisateur/rôle mais pas le bot (excluant @everyone/@here).

    MP de groupe :

    - par défaut : ignorés (`dm.groupEnabled=false`)
    - liste blanche optionnelle via `dm.groupChannels` (ID de canal ou slugs)

  </Tab>
</Tabs>

### Routage d'agent basé sur les rôles

Utilisez `bindings[].match.roles` pour router les membres de guilde Discord vers différents agents par ID de rôle. Les liaisons basées sur les rôles acceptent uniquement les ID de rôle et sont évaluées après les liaisons de pair ou de pair parent et avant les liaisons uniquement de guilde. Si une liaison définit également d'autres champs de correspondance (par exemple `peer` + `guildId` + `roles`), tous les champs configurés doivent correspondre.

```json5
{
  bindings: [
    {
      agentId: "opus",
      match: {
        channel: "discord",
        guildId: "123456789012345678",
        roles: ["111111111111111111"],
      },
    },
    {
      agentId: "sonnet",
      match: {
        channel: "discord",
        guildId: "123456789012345678",
      },
    },
  ],
}
```

## Configuration du portail des développeurs

<AccordionGroup>
  <Accordion title="Créer une application et un bot">

    1. Portail des développeurs Discord -> **Applications** -> **Nouvelle application**
    2. **Bot** -> **Ajouter un bot**
    3. Copier le jeton du bot

  </Accordion>

  <Accordion title="Intentions privilégiées">
    Dans **Bot -> Privileged Gateway Intents**, activez :

    - Message Content Intent
    - Server Members Intent (recommandé)

    L'intention de présence est optionnelle et uniquement requise si vous souhaitez recevoir des mises à jour de présence. La définition de la présence du bot (`setPresence`) ne nécessite pas d'activer les mises à jour de présence pour les membres.

  </Accordion>

  <Accordion title="Portées OAuth et permissions de base">
    Générateur d'URL OAuth :

    - portées : `bot`, `applications.commands`

    Permissions de base typiques :

    - Afficher les canaux
    - Envoyer des messages
    - Lire l'historique des messages
    - Intégrer des liens
    - Joindre des fichiers
    - Ajouter des réactions (optionnel)

    Évitez `Administrator` sauf si explicitement nécessaire.

  </Accordion>

  <Accordion title="Copier les ID">
    Activez le mode développeur Discord, puis copiez :

    - ID du serveur
    - ID du canal
    - ID utilisateur

    Préférez les ID numériques dans la configuration OpenClaw pour des audits et des sondes fiables.

  </Accordion>
</AccordionGroup>

## Commandes natives et authentification des commandes

- `commands.native` est par défaut `"auto"` et est activé pour Discord.
- Remplacement par canal : `channels.discord.commands.native`.
- `commands.native=false` efface explicitement les commandes natives Discord précédemment enregistrées.
- L'authentification des commandes natives utilise les mêmes listes blanches/politiques Discord que la gestion normale des messages.
- Les commandes peuvent toujours être visibles dans l'interface utilisateur Discord pour les utilisateurs qui ne sont pas autorisés ; l'exécution applique toujours l'authentification OpenClaw et retourne « non autorisé ».

Voir [Commandes slash](/fr/tools/slash-commands) pour le catalogue des commandes et le comportement.

Paramètres de commande slash par défaut :

- `ephemeral: true`

## Détails des fonctionnalités

<AccordionGroup>
  <Accordion title="Balises de réponse et réponses natives">
    Discord supporte les balises de réponse dans la sortie de l'agent :

    - `[[reply_to_current]]`
    - `[[reply_to:<id>]]`

    Contrôlé par `channels.discord.replyToMode` :

    - `off` (par défaut)
    - `first`
    - `all`

    Remarque : `off` désactive le threading de réponse implicite. Les balises explicites `[[reply_to_*]]` sont toujours honorées.

    Les ID de message sont exposés dans le contexte/historique afin que les agents puissent cibler des messages spécifiques.

  </Accordion>

  <Accordion title="Aperçu du flux en direct">
    OpenClaw peut diffuser en continu les réponses brouillon en envoyant un message temporaire et en le modifiant à mesure que le texte arrive.

    - `channels.discord.streaming` contrôle la diffusion d'aperçu (`off` | `partial` | `block` | `progress`, par défaut : `off`).
    - `progress` est accepté pour la cohérence inter-canaux et correspond à `partial` sur Discord.
    - `channels.discord.streamMode` est un alias hérité et est auto-migré.
    - `partial` modifie un seul message d'aperçu à mesure que les jetons arrivent.
    - `block` émet des chunks de taille brouillon (utilisez `draftChunk` pour ajuster la taille et les points d'arrêt).

    Exemple :

```json5
{
  channels: {
    discord: {
      streaming: "partial",
    },
  },
}
```

    Valeurs par défaut du chunking en mode `block` (limité à `channels.discord.textChunkLimit`) :

```json5
{
  channels: {
    discord: {
      streaming: "block",
      draftChunk: {
        minChars: 200,
        maxChars: 800,
        breakPreference: "paragraph",
      },
    },
  },
}
```

    La diffusion d'aperçu est réservée au texte ; les réponses médias reviennent à la livraison normale.

    Remarque : la diffusion d'aperçu est distincte de la diffusion par bloc. Lorsque la diffusion par bloc est explicitement activée pour Discord, OpenClaw ignore le flux d'aperçu pour éviter une double diffusion.

  </Accordion>

  <Accordion title="Historique, contexte et comportement des threads">
    Contexte d'historique de guilde :

    - `channels.discord.historyLimit` par défaut `20`
    - secours : `messages.groupChat.historyLimit`
    - `0` désactive

    Contrôles d'historique DM :

    - `channels.discord.dmHistoryLimit`
    - `channels.discord.dms["<user_id>"].historyLimit`

    Comportement des threads :

    - Les threads Discord sont routés en tant que sessions de canal
    - les métadonnées de thread parent peuvent être utilisées pour la liaison de session parent
    - la configuration du thread hérite de la configuration du canal parent sauf si une entrée spécifique au thread existe

    Les sujets de canal sont injectés en tant que contexte **non fiable** (pas comme invite système).

  </Accordion>

  <Accordion title="Sessions liées aux threads pour les sous-agents">
    Discord peut lier un thread à une cible de session afin que les messages de suivi dans ce thread continuent à être routés vers la même session (y compris les sessions de sous-agent).

    Commandes :

    - `/focus <target>` lier le thread actuel/nouveau à une cible de sous-agent/session
    - `/unfocus` supprimer la liaison du thread actuel
    - `/agents` afficher les exécutions actives et l'état de liaison
    - `/session idle <duration|off>` inspecter/mettre à jour l'auto-unfocus d'inactivité pour les liaisons focalisées
    - `/session max-age <duration|off>` inspecter/mettre à jour l'âge maximum dur pour les liaisons focalisées

    Configuration :

```json5
{
  session: {
    threadBindings: {
      enabled: true,
      idleHours: 24,
      maxAgeHours: 0,
    },
  },
  channels: {
    discord: {
      threadBindings: {
        enabled: true,
        idleHours: 24,
        maxAgeHours: 0,
        spawnSubagentSessions: false, // opt-in
      },
    },
  },
}
```

    Remarques :

    - `session.threadBindings.*` définit les valeurs par défaut globales.
    - `channels.discord.threadBindings.*` remplace le comportement Discord.
    - `spawnSubagentSessions` doit être true pour créer/lier automatiquement des threads pour `sessions_spawn({ thread: true })`.
    - `spawnAcpSessions` doit être true pour créer/lier automatiquement des threads pour ACP (`/acp spawn ... --thread ...` ou `sessions_spawn({ runtime: "acp", thread: true })`).
    - Si les liaisons de thread sont désactivées pour un compte, `/focus` et les opérations de liaison de thread associées ne sont pas disponibles.

    Voir [Sous-agents](/fr/tools/subagents), [Agents ACP](/fr/tools/acp-agents) et [Référence de configuration](/fr/gateway/configuration-reference).

  </Accordion>

  <Accordion title="Liaisons de canal ACP persistantes">
    Pour les espaces de travail ACP stables « toujours actifs », configurez les liaisons ACP typées de niveau supérieur ciblant les conversations Discord.

    Chemin de configuration :

    - `bindings[]` avec `type: "acp"` et `match.channel: "discord"`

    Exemple :

```json5
{
  agents: {
    list: [
      {
        id: "codex",
        runtime: {
          type: "acp",
          acp: {
            agent: "codex",
            backend: "acpx",
            mode: "persistent",
            cwd: "/workspace/openclaw",
          },
        },
      },
    ],
  },
  bindings: [
    {
      type: "acp",
      agentId: "codex",
      match: {
        channel: "discord",
        accountId: "default",
        peer: { kind: "channel", id: "222222222222222222" },
      },
      acp: { label: "codex-main" },
    },
  ],
  channels: {
    discord: {
      guilds: {
        "111111111111111111": {
          channels: {
            "222222222222222222": {
              requireMention: false,
            },
          },
        },
      },
    },
  },
}
```

    Remarques :

    - Les messages de thread peuvent hériter de la liaison ACP du canal parent.
    - Dans un canal ou thread lié, `/new` et `/reset` réinitialisent la même session ACP sur place.
    - Les liaisons de thread temporaires fonctionnent toujours et peuvent remplacer la résolution de cible pendant qu'elles sont actives.

    Voir [Agents ACP](/fr/tools/acp-agents) pour les détails du comportement de liaison.

  </Accordion>

  <Accordion title="Notifications de réaction">
    Mode de notification de réaction par guilde :

    - `off`
    - `own` (par défaut)
    - `all`
    - `allowlist` (utilise `guilds.<id>.users`)

    Les événements de réaction sont transformés en événements système et attachés à la session Discord routée.

  </Accordion>

  <Accordion title="Réactions d'accusé de réception">
    `ackReaction` envoie un emoji d'accusé de réception pendant qu'OpenClaw traite un message entrant.

    Ordre de résolution :

    - `channels.discord.accounts.<accountId>.ackReaction`
    - `channels.discord.ackReaction`
    - `messages.ackReaction`
    - secours emoji d'identité d'agent (`agents.list[].identity.emoji`, sinon "👀")

    Remarques :

    - Discord accepte les emoji unicode ou les noms d'emoji personnalisés.
    - Utilisez `""` pour désactiver la réaction pour un canal ou un compte.

  </Accordion>

  <Accordion title="Écritures de configuration">
    Les écritures de configuration initiées par le canal sont activées par défaut.

    Cela affecte les flux `/config set|unset` (lorsque les fonctionnalités de commande sont activées).

    Désactiver :

```json5
{
  channels: {
    discord: {
      configWrites: false,
    },
  },
}
```

  </Accordion>

  <Accordion title="Proxy de passerelle">
    Routez le trafic WebSocket de la passerelle Discord et les recherches REST de démarrage (ID d'application + résolution de liste d'autorisation) via un proxy HTTP(S) avec `channels.discord.proxy`.

```json5
{
  channels: {
    discord: {
      proxy: "http://proxy.example:8080",
    },
  },
}
```

    Remplacement par compte :

```json5
{
  channels: {
    discord: {
      accounts: {
        primary: {
          proxy: "http://proxy.example:8080",
        },
      },
    },
  },
}
```

  </Accordion>

  <Accordion title="Support de PluralKit">
    Activez la résolution PluralKit pour mapper les messages proxifiés à l'identité du membre du système :

```json5
{
  channels: {
    discord: {
      pluralkit: {
        enabled: true,
        token: "pk_live_...", // optionnel ; nécessaire pour les systèmes privés
      },
    },
  },
}
```

    Remarques :

    - les listes d'autorisation peuvent utiliser `pk:<memberId>`
    - les noms d'affichage des membres sont mis en correspondance par nom/slug uniquement lorsque `channels.discord.dangerouslyAllowNameMatching: true`
    - les recherches utilisent l'ID de message d'origine et sont limitées par fenêtre de temps
    - si la recherche échoue, les messages proxifiés sont traités comme des messages de bot et supprimés sauf si `allowBots=true`

  </Accordion>

  <Accordion title="Configuration de présence">
    Les mises à jour de présence sont appliquées lorsque vous définissez un champ de statut ou d'activité, ou lorsque vous activez la présence automatique.

    Exemple de statut uniquement :

```json5
{
  channels: {
    discord: {
      status: "idle",
    },
  },
}
```

    Exemple d'activité (le statut personnalisé est le type d'activité par défaut) :

```json5
{
  channels: {
    discord: {
      activity: "Focus time",
      activityType: 4,
    },
  },
}
```

    Exemple de diffusion :

```json5
{
  channels: {
    discord: {
      activity: "Live coding",
      activityType: 1,
      activityUrl: "https://twitch.tv/openclaw",
    },
  },
}
```

    Carte des types d'activité :

    - 0 : En train de jouer
    - 1 : Diffusion en continu (nécessite `activityUrl`)
    - 2 : Écoute
    - 3 : Regarder
    - 4 : Personnalisé (utilise le texte d'activité comme état de statut ; l'emoji est optionnel)
    - 5 : En compétition

    Exemple de présence automatique (signal de santé d'exécution) :

```json5
{
  channels: {
    discord: {
      autoPresence: {
        enabled: true,
        intervalMs: 30000,
        minUpdateIntervalMs: 15000,
        exhaustedText: "token exhausted",
      },
    },
  },
}
```

    La présence automatique mappe la disponibilité d'exécution au statut Discord : sain => en ligne, dégradé ou inconnu => inactif, épuisé ou indisponible => ne pas déranger. Remplacements de texte optionnels :

    - `autoPresence.healthyText`
    - `autoPresence.degradedText`
    - `autoPresence.exhaustedText` (supporte l'espace réservé `{reason}`)

  </Accordion>

  <Accordion title="Approbations d'exécution dans Discord">
    Discord supporte les approbations d'exécution basées sur des boutons dans les DM et peut éventuellement publier des invites d'approbation dans le canal d'origine.

    Chemin de configuration :

    - `channels.discord.execApprovals.enabled`
    - `channels.discord.execApprovals.approvers`
    - `channels.discord.execApprovals.target` (`dm` | `channel` | `both`, par défaut : `dm`)
    - `agentFilter`, `sessionFilter`, `cleanupAfterResolve`

    Lorsque `target` est `channel` ou `both`, l'invite d'approbation est visible dans le canal. Seuls les approbateurs configurés peuvent utiliser les boutons ; les autres utilisateurs reçoivent un refus éphémère. Les invites d'approbation incluent le texte de la commande, donc n'activez la livraison de canal que dans les canaux de confiance. Si l'ID de canal ne peut pas être dérivé de la clé de session, OpenClaw revient à la livraison DM.

    L'authentification de la passerelle pour ce gestionnaire utilise le même contrat de résolution d'identifiants partagés que les autres clients de passerelle :

    - authentification locale en priorité env (`OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD` puis `gateway.auth.*`)
    - en mode local, `gateway.remote.*` peut être utilisé comme secours uniquement lorsque `gateway.auth.*` n'est pas défini ; les SecretRefs locales configurées mais non résolues échouent fermées
    - support du mode distant via `gateway.remote.*` le cas échéant
    - les remplacements d'URL sont sûrs pour les remplacements : les remplacements CLI ne réutilisent pas les identifiants implicites, et les remplacements env utilisent uniquement les identifiants env

    Si les approbations échouent avec des ID d'approbation inconnus, vérifiez la liste des approbateurs et l'activation des fonctionnalités.

    Docs connexes : [Approbations d'exécution](/fr/tools/exec-approvals)

  </Accordion>
</AccordionGroup>

## Outils et portes d'action

Les actions de message Discord incluent la messagerie, l'administration des canaux, la modération, la présence et les actions de métadonnées.

Exemples principaux :

- messagerie : `sendMessage`, `readMessages`, `editMessage`, `deleteMessage`, `threadReply`
- réactions : `react`, `reactions`, `emojiList`
- modération : `timeout`, `kick`, `ban`
- présence : `setPresence`

Les portes d'action se trouvent sous `channels.discord.actions.*`.

Comportement par défaut de la porte :

| Groupe d'action                                                                                                                                                             | Par défaut |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- |
| reactions, messages, threads, pins, polls, search, memberInfo, roleInfo, channelInfo, channels, voiceStatus, events, stickers, emojiUploads, stickerUploads, permissions | activé  |
| roles                                                                                                                                                                    | désactivé |
| moderation                                                                                                                                                               | désactivé |
| presence                                                                                                                                                                 | désactivé |

## Interface utilisateur des composants v2

OpenClaw utilise les composants Discord v2 pour les approbations d'exécution et les marqueurs inter-contextes. Les actions de message Discord peuvent également accepter `components` pour une interface utilisateur personnalisée (avancé ; nécessite des instances de composants Carbon), tandis que les `embeds` hérités restent disponibles mais ne sont pas recommandés.

- `channels.discord.ui.components.accentColor` définit la couleur d'accent utilisée par les conteneurs de composants Discord (hexadécimal).
- Définir par compte avec `channels.discord.accounts.<id>.ui.components.accentColor`.
- `embeds` sont ignorés lorsque les composants v2 sont présents.

Exemple :

```json5
{
  channels: {
    discord: {
      ui: {
        components: {
          accentColor: "#5865F2",
        },
      },
    },
  },
}
```

## Canaux vocaux

OpenClaw peut rejoindre les canaux vocaux Discord pour des conversations en temps réel et continues. Ceci est distinct des pièces jointes de messages vocaux.

Exigences :

- Activer les commandes natives (`commands.native` ou `channels.discord.commands.native`).
- Configurer `channels.discord.voice`.
- Le bot a besoin des permissions Connect + Speak dans le canal vocal cible.

Utilisez la commande native Discord uniquement `/vc join|leave|status` pour contrôler les sessions. La commande utilise l'agent par défaut du compte et suit les mêmes règles de liste d'autorisation et de politique de groupe que les autres commandes Discord.

Exemple d'auto-join :

```json5
{
  channels: {
    discord: {
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
    },
  },
}
```

Notes :

- `voice.tts` remplace `messages.tts` pour la lecture vocale uniquement.
- Les tours de transcription vocale dérivant le statut de propriétaire de Discord `allowFrom` (ou `dm.allowFrom`) ; les locuteurs non-propriétaires ne peuvent pas accéder aux outils réservés aux propriétaires (par exemple `gateway` et `cron`).
- La voix est activée par défaut ; définir `channels.discord.voice.enabled=false` pour la désactiver.
- `voice.daveEncryption` et `voice.decryptionFailureTolerance` sont transmis aux options de jointure `@discordjs/voice`.
- Les valeurs par défaut de `@discordjs/voice` sont `daveEncryption=true` et `decryptionFailureTolerance=24` s'ils ne sont pas définis.
- OpenClaw surveille également les échecs de déchiffrement de réception et se récupère automatiquement en quittant/rejoignant le canal vocal après des échecs répétés dans une courte fenêtre.
- Si les journaux de réception affichent à plusieurs reprises `DecryptionFailed(UnencryptedWhenPassthroughDisabled)`, cela peut être le bug de réception en amont `@discordjs/voice` suivi dans [discord.js #11419](https://github.com/discordjs/discord.js/issues/11419).

## Messages vocaux

Les messages vocaux Discord affichent un aperçu de la forme d'onde et nécessitent de l'audio OGG/Opus plus des métadonnées. OpenClaw génère la forme d'onde automatiquement, mais il a besoin de `ffmpeg` et `ffprobe` disponibles sur l'hôte de la passerelle pour inspecter et convertir les fichiers audio.

Exigences et contraintes :

- Fournir un **chemin de fichier local** (les URL sont rejetées).
- Omettre le contenu textuel (Discord ne permet pas le texte + message vocal dans la même charge utile).
- Tout format audio est accepté ; OpenClaw convertit en OGG/Opus si nécessaire.

Exemple :

```bash
message(action="send", channel="discord", target="channel:123", path="/path/to/audio.mp3", asVoice=true)
```

## Dépannage

<AccordionGroup>
  <Accordion title="Intentions non autorisées utilisées ou le bot ne voit aucun message de guilde">

    - activer Message Content Intent
    - activer Server Members Intent lorsque vous dépendez de la résolution utilisateur/membre
    - redémarrer la passerelle après avoir modifié les intentions

  </Accordion>

  <Accordion title="Messages de guilde bloqués de manière inattendue">

    - vérifier `groupPolicy`
    - vérifier la liste d'autorisation de guilde sous `channels.discord.guilds`
    - si la carte `channels` de guilde existe, seuls les canaux listés sont autorisés
    - vérifier le comportement de `requireMention` et les modèles de mention

    Vérifications utiles :

```bash
openclaw doctor
openclaw channels status --probe
openclaw logs --follow
```

  </Accordion>

  <Accordion title="Exiger une mention faux mais toujours bloqué">
    Causes courantes :

    - `groupPolicy="allowlist"` sans liste d'autorisation de guilde/canal correspondante
    - `requireMention` configuré au mauvais endroit (doit être sous `channels.discord.guilds` ou entrée de canal)
    - expéditeur bloqué par la liste d'autorisation `users` de guilde/canal

  </Accordion>

  <Accordion title="Les gestionnaires de longue durée expirent ou dupliquent les réponses">

    Journaux typiques :

    - `Listener DiscordMessageListener timed out after 30000ms for event MESSAGE_CREATE`
    - `Slow listener detected ...`
    - `discord inbound worker timed out after ...`

    Bouton de budget d'écouteur :

    - compte unique : `channels.discord.eventQueue.listenerTimeout`
    - multi-compte : `channels.discord.accounts.<accountId>.eventQueue.listenerTimeout`

    Bouton de délai d'exécution du worker :

    - compte unique : `channels.discord.inboundWorker.runTimeoutMs`
    - multi-compte : `channels.discord.accounts.<accountId>.inboundWorker.runTimeoutMs`
    - par défaut : `1800000` (30 minutes) ; définir `0` pour désactiver

    Ligne de base recommandée :

```json5
{
  channels: {
    discord: {
      accounts: {
        default: {
          eventQueue: {
            listenerTimeout: 120000,
          },
          inboundWorker: {
            runTimeoutMs: 1800000,
          },
        },
      },
    },
  },
}
```

    Utilisez `eventQueue.listenerTimeout` pour la configuration d'écouteur lent et `inboundWorker.runTimeoutMs`
    uniquement si vous souhaitez une soupape de sécurité distincte pour les tours d'agent en file d'attente.

  </Accordion>

  <Accordion title="Incompatibilités d'audit des permissions">
    Les vérifications de permissions `channels status --probe` ne fonctionnent que pour les ID de canal numériques.

    Si vous utilisez des clés slug, la correspondance à l'exécution peut toujours fonctionner, mais la sonde ne peut pas vérifier complètement les permissions.

  </Accordion>

  <Accordion title="Problèmes de DM et d'appairage">

    - DM désactivé : `channels.discord.dm.enabled=false`
    - Politique DM désactivée : `channels.discord.dmPolicy="disabled"` (hérité : `channels.discord.dm.policy`)
    - en attente d'approbation d'appairage en mode `pairing`

  </Accordion>

  <Accordion title="Boucles bot à bot">
    Par défaut, les messages créés par des bots sont ignorés.

    Si vous définissez `channels.discord.allowBots=true`, utilisez des règles de mention strictes et de liste d'autorisation pour éviter le comportement de boucle.
    Préférez `channels.discord.allowBots="mentions"` pour accepter uniquement les messages de bot qui mentionnent le bot.

  </Accordion>

  <Accordion title="Chutes de STT vocales avec DecryptionFailed(...)">

    - garder OpenClaw à jour (`openclaw update`) pour que la logique de récupération de réception vocale Discord soit présente
    - confirmer `channels.discord.voice.daveEncryption=true` (par défaut)
    - commencer par `channels.discord.voice.decryptionFailureTolerance=24` (valeur par défaut en amont) et ajuster uniquement si nécessaire
    - surveiller les journaux pour :
      - `discord voice: DAVE decrypt failures detected`
      - `discord voice: repeated decrypt failures; attempting rejoin`
    - si les échecs persistent après la réunion automatique, collectez les journaux et comparez avec [discord.js #11419](https://github.com/discordjs/discord.js/issues/11419)

  </Accordion>
</AccordionGroup>

## Pointeurs de référence de configuration

Référence principale :

- [Référence de configuration - Discord](/fr/gateway/configuration-reference#discord)

Champs Discord à haut signal :

- démarrage/authentification : `enabled`, `token`, `accounts.*`, `allowBots`
- politique : `groupPolicy`, `dm.*`, `guilds.*`, `guilds.*.channels.*`
- commande : `commands.native`, `commands.useAccessGroups`, `configWrites`, `slashCommand.*`
- file d'attente d'événements : `eventQueue.listenerTimeout` (budget d'écouteur), `eventQueue.maxQueueSize`, `eventQueue.maxConcurrency`
- worker entrant : `inboundWorker.runTimeoutMs`
- réponse/historique : `replyToMode`, `historyLimit`, `dmHistoryLimit`, `dms.*.historyLimit`
- livraison : `textChunkLimit`, `chunkMode`, `maxLinesPerMessage`
- streaming : `streaming` (alias hérité : `streamMode`), `draftChunk`, `blockStreaming`, `blockStreamingCoalesce`
- média/nouvelle tentative : `mediaMaxMb`, `retry`
  - `mediaMaxMb` limite les téléchargements Discord sortants (par défaut : `8MB`)
- actions : `actions.*`
- présence : `activity`, `status`, `activityType`, `activityUrl`
- interface utilisateur : `ui.components.accentColor`
- fonctionnalités : `threadBindings`, `bindings[]` au niveau supérieur (`type: "acp"`), `pluralkit`, `execApprovals`, `intents`, `agentComponents`, `heartbeat`, `responsePrefix`

## Sécurité et opérations

- Traiter les jetons de bot comme des secrets (`DISCORD_BOT_TOKEN` préféré dans les environnements supervisés).
- Accorder les permissions Discord du moindre privilège.
- Si le déploiement/état de la commande est obsolète, redémarrez la passerelle et revérifiez avec `openclaw channels status --probe`.

## Connexes

- [Appairage](/fr/channels/pairing)
- [Routage des canaux](/fr/channels/channel-routing)
- [Routage multi-agent](/fr/concepts/multi-agent)
- [Dépannage](/fr/channels/troubleshooting)
- [Commandes slash](/fr/tools/slash-commands)
