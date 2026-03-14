---
summary: "Statut de support du bot Discord, capacités et configuration"
read_when:
  - Working on Discord channel features
title: "Discord"
---

# Discord (Bot API)

Statut : prêt pour les DMs et les canaux de serveur via la passerelle Discord officielle.

<CardGroup cols={3}>
  <Card title="Appairage" icon="link" href="/channels/pairing">
    Les DMs Discord sont par défaut en mode appairage.
  </Card>
  <Card title="Commandes slash" icon="terminal" href="/tools/slash-commands">
    Comportement natif des commandes et catalogue des commandes.
  </Card>
  <Card title="Dépannage des canaux" icon="wrench" href="/channels/troubleshooting">
    Diagnostics multi-canaux et flux de réparation.
  </Card>
</CardGroup>

## Configuration rapide

Vous devez créer une nouvelle application avec un bot, ajouter le bot à votre serveur et l'appairer à OpenClaw. Nous recommandons d'ajouter votre bot à votre propre serveur privé. Si vous n'en avez pas encore, [créez-en un d'abord](https://support.discord.com/hc/en-us/articles/204849977-How-do-I-create-a-server) (choisissez **Create My Own > For me and my friends**).

<Steps>
  <Step title="Créer une application Discord et un bot">
    Allez sur le [Portail des développeurs Discord](https://discord.com/developers/applications) et cliquez sur **New Application**. Nommez-la quelque chose comme « OpenClaw ».

    Cliquez sur **Bot** dans la barre latérale. Définissez le **Username** sur le nom que vous donnez à votre agent OpenClaw.

  </Step>

  <Step title="Activer les intentions privilégiées">
    Toujours sur la page **Bot**, faites défiler vers le bas jusqu'à **Privileged Gateway Intents** et activez :

    - **Message Content Intent** (obligatoire)
    - **Server Members Intent** (recommandé ; obligatoire pour les listes blanches de rôles et la correspondance nom-à-ID)
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

    Copiez l'URL générée en bas, collez-la dans votre navigateur, sélectionnez votre serveur et cliquez sur **Continue** pour vous connecter. Vous devriez maintenant voir votre bot dans le serveur Discord.

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

        > « J'ai déjà défini mon jeton de bot Discord dans la config. Veuillez terminer la configuration de Discord avec l'ID utilisateur `<user_id>` et l'ID serveur `<server_id>`. »
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

        Les valeurs SecretRef sont également supportées pour `channels.discord.token` (fournisseurs env/file/exec). Voir [Gestion des secrets](/gateway/secrets).

      </Tab>
    </Tabs>

  </Step>

  <Step title="Approuver le premier appairage DM">
    Attendez que la passerelle soit en cours d'exécution, puis envoyez un DM à votre bot dans Discord. Il répondra avec un code d'appairage.

    <Tabs>
      <Tab title="Demander à votre agent">
        Envoyez le code d'appairage à votre agent sur votre canal existant :

        > « Approuvez ce code d'appairage Discord : `<CODE>` »
      </Tab>
      <Tab title="CLI">

```bash
openclaw pairing list discord
openclaw pairing approve discord <CODE>
```

      </Tab>
    </Tabs>

    Les codes d'appairage expirent après 1 heure.

    Vous devriez maintenant pouvoir discuter avec votre agent dans Discord via DM.

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
        > « Ajoutez mon ID de serveur Discord `<server_id>` à la liste blanche de serveur »
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
        > « Autorisez mon agent à répondre sur ce serveur sans avoir besoin d'être @mentionné »
      </Tab>
      <Tab title="Config">
        Définissez `requireMention: false` dans votre config de serveur :

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
        > « Quand je pose des questions dans les canaux Discord, utilisez memory_search ou memory_get si vous avez besoin d'un contexte à long terme de MEMORY.md. »
      </Tab>
      <Tab title="Manuel">
        Si vous avez besoin d'un contexte partagé dans chaque canal, mettez les instructions stables dans `AGENTS.md` ou `USER.md` (elles sont injectées pour chaque session). Gardez les notes à long terme dans `MEMORY.md` et accédez-y à la demande avec les outils de mémoire.
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

OpenClaw supporte les conteneurs de composants Discord v2 pour les messages d'agent. Utilisez l'outil de message avec une charge utile `components`. Les résultats d'interaction sont routés vers l'agent en tant que messages entrants normaux et suivent les paramètres `replyToMode` Discord existants.

Blocs supportés :

- `text`, `section`, `separator`, `actions`, `media-gallery`, `file`
- Les lignes d'action permettent jusqu'à 5 boutons ou un seul menu de sélection
- Types de sélection : `string`, `user`, `role`, `mentionable`, `channel`

Par défaut, les composants sont à usage unique. Définissez `components.reusable=true` pour permettre aux boutons, sélections et formulaires d'être utilisés plusieurs fois jusqu'à expiration.

Pour restreindre qui peut cliquer sur un bouton, définissez `allowedUsers` sur ce bouton (ID utilisateur Discord, tags ou `*`). Lorsqu'il est configuré, les utilisateurs non correspondants reçoivent un refus éphémère.

Les commandes slash `/model` et `/models` ouvrent un sélecteur de modèle interactif avec des menus déroulants de fournisseur et de modèle plus une étape Soumettre. La réponse du sélecteur est éphémère et seul l'utilisateur invoquant peut l'utiliser.

Pièces jointes de fichiers :

- Les blocs `file` doivent pointer vers une référence de pièce jointe (`attachment://<filename>`)
- Fournissez la pièce jointe via `media`/`path
