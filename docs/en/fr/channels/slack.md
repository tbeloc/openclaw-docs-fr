---
summary: "Configuration de Slack et comportement à l'exécution (Socket Mode + HTTP Events API)"
read_when:
  - Configuration de Slack ou débogage du mode socket/HTTP de Slack
title: "Slack"
---

# Slack

Statut : prêt pour la production pour les DMs + canaux via les intégrations d'applications Slack. Le mode par défaut est Socket Mode ; le mode HTTP Events API est également supporté.

<CardGroup cols={3}>
  <Card title="Appairage" icon="link" href="/channels/pairing">
    Les DMs Slack utilisent par défaut le mode appairage.
  </Card>
  <Card title="Commandes slash" icon="terminal" href="/tools/slash-commands">
    Comportement des commandes natives et catalogue de commandes.
  </Card>
  <Card title="Dépannage des canaux" icon="wrench" href="/channels/troubleshooting">
    Diagnostics multi-canaux et guides de réparation.
  </Card>
</CardGroup>

## Configuration rapide

<Tabs>
  <Tab title="Socket Mode (par défaut)">
    <Steps>
      <Step title="Créer l'application Slack et les tokens">
        Dans les paramètres de l'application Slack :

        - activez **Socket Mode**
        - créez un **App Token** (`xapp-...`) avec `connections:write`
        - installez l'application et copiez le **Bot Token** (`xoxb-...`)
      </Step>

      <Step title="Configurer OpenClaw">

```json5
{
  channels: {
    slack: {
      enabled: true,
      mode: "socket",
      appToken: "xapp-...",
      botToken: "xoxb-...",
    },
  },
}
```

        Fallback d'environnement (compte par défaut uniquement) :

```bash
SLACK_APP_TOKEN=xapp-...
SLACK_BOT_TOKEN=xoxb-...
```

      </Step>

      <Step title="S'abonner aux événements de l'application">
        S'abonner aux événements du bot pour :

        - `app_mention`
        - `message.channels`, `message.groups`, `message.im`, `message.mpim`
        - `reaction_added`, `reaction_removed`
        - `member_joined_channel`, `member_left_channel`
        - `channel_rename`
        - `pin_added`, `pin_removed`

        Activez également l'onglet **Messages** de la page d'accueil de l'application pour les DMs.
      </Step>

      <Step title="Démarrer la passerelle">

```bash
openclaw gateway
```

      </Step>
    </Steps>

  </Tab>

  <Tab title="Mode HTTP Events API">
    <Steps>
      <Step title="Configurer l'application Slack pour HTTP">

        - définissez le mode sur HTTP (`channels.slack.mode="http"`)
        - copiez le **Signing Secret** de Slack
        - définissez l'URL de webhook Event Subscriptions + Interactivity + Slash command sur le même chemin (par défaut `/slack/events`)

      </Step>

      <Step title="Configurer le mode HTTP d'OpenClaw">

```json5
{
  channels: {
    slack: {
      enabled: true,
      mode: "http",
      botToken: "xoxb-...",
      signingSecret: "your-signing-secret",
      webhookPath: "/slack/events",
    },
  },
}
```

      </Step>

      <Step title="Utiliser des chemins de webhook uniques pour HTTP multi-compte">
        Le mode HTTP par compte est supporté.

        Donnez à chaque compte un `webhookPath` distinct pour que les enregistrements ne se chevauchent pas.
      </Step>
    </Steps>

  </Tab>
</Tabs>

## Modèle de token

- `botToken` + `appToken` sont requis pour Socket Mode.
- Le mode HTTP nécessite `botToken` + `signingSecret`.
- Les tokens de configuration remplacent le fallback d'environnement.
- Le fallback d'environnement `SLACK_BOT_TOKEN` / `SLACK_APP_TOKEN` s'applique uniquement au compte par défaut.
- `userToken` (`xoxp-...`) est configuration uniquement (pas de fallback d'environnement) et utilise par défaut un comportement en lecture seule (`userTokenReadOnly: true`).
- Optionnel : ajoutez `chat:write.customize` si vous souhaitez que les messages sortants utilisent l'identité de l'agent actif (nom d'utilisateur et icône personnalisés). `icon_emoji` utilise la syntaxe `:emoji_name:`.

<Tip>
Pour les lectures d'actions/répertoire, le token utilisateur peut être préféré lorsqu'il est configuré. Pour les écritures, le token bot reste préféré ; les écritures avec token utilisateur ne sont autorisées que lorsque `userTokenReadOnly: false` et que le token bot n'est pas disponible.
</Tip>

## Contrôle d'accès et routage

<Tabs>
  <Tab title="Politique DM">
    `channels.slack.dmPolicy` contrôle l'accès aux DMs (héritage : `channels.slack.dm.policy`) :

    - `pairing` (par défaut)
    - `allowlist`
    - `open` (nécessite que `channels.slack.allowFrom` inclue `"*"` ; héritage : `channels.slack.dm.allowFrom`)
    - `disabled`

    Drapeaux DM :

    - `dm.enabled` (par défaut true)
    - `channels.slack.allowFrom` (préféré)
    - `dm.allowFrom` (héritage)
    - `dm.groupEnabled` (les DMs de groupe sont par défaut false)
    - `dm.groupChannels` (liste d'autorisation MPIM optionnelle)

    Précédence multi-compte :

    - `channels.slack.accounts.default.allowFrom` s'applique uniquement au compte `default`.
    - Les comptes nommés héritent de `channels.slack.allowFrom` lorsque leur propre `allowFrom` n'est pas défini.
    - Les comptes nommés n'héritent pas de `channels.slack.accounts.default.allowFrom`.

    L'appairage dans les DMs utilise `openclaw pairing approve slack <code>`.

  </Tab>

  <Tab title="Politique de canal">
    `channels.slack.groupPolicy` contrôle la gestion des canaux :

    - `open`
    - `allowlist`
    - `disabled`

    La liste d'autorisation des canaux se trouve sous `channels.slack.channels` et doit utiliser des ID de canal stables.

    Note d'exécution : si `channels.slack` est complètement absent (configuration env uniquement), l'exécution revient à `groupPolicy="allowlist"` et enregistre un avertissement (même si `channels.defaults.groupPolicy` est défini).

    Résolution de nom/ID :

    - les entrées de liste d'autorisation de canal et les entrées de liste d'autorisation DM sont résolues au démarrage lorsque l'accès au token le permet
    - les entrées de nom de canal non résolues sont conservées telles que configurées mais ignorées pour le routage par défaut
    - l'autorisation entrante et le routage des canaux sont d'abord basés sur l'ID ; la correspondance directe de nom d'utilisateur/slug nécessite `channels.slack.dangerouslyAllowNameMatching: true`

  </Tab>

  <Tab title="Mentions et utilisateurs de canal">
    Les messages de canal sont contrôlés par mention par défaut.

    Sources de mention :

    - mention explicite de l'application (`<@botId>`)
    - modèles de regex de mention (`agents.list[].groupChat.mentionPatterns`, fallback `messages.groupChat.mentionPatterns`)
    - comportement implicite de réponse au fil du bot

    Contrôles par canal (`channels.slack.channels.<id>` ; noms uniquement via résolution au démarrage ou `dangerouslyAllowNameMatching`) :

    - `requireMention`
    - `users` (liste d'autorisation)
    - `allowBots`
    - `skills`
    - `systemPrompt`
    - `tools`, `toolsBySender`
    - format de clé `toolsBySender` : `id:`, `e164:`, `username:`, `name:`, ou wildcard `"*"`
      (les clés héritées non préfixées correspondent toujours à `id:` uniquement)

  </Tab>
</Tabs>

## Commandes et comportement slash

- Le mode auto de commande native est **désactivé** pour Slack (`commands.native: "auto"` n'active pas les commandes natives Slack).
- Activez les gestionnaires de commandes Slack natives avec `channels.slack.commands.native: true` (ou global `commands.native: true`).
- Lorsque les commandes natives sont activées, enregistrez les commandes slash correspondantes dans Slack (noms `/<command>`), avec une exception :
  - enregistrez `/agentstatus` pour la commande de statut (Slack réserve `/status`)
- Si les commandes natives ne sont pas activées, vous pouvez exécuter une seule commande slash configurée via `channels.slack.slashCommand`.
- Les menus d'arguments natifs adaptent maintenant leur stratégie de rendu :
  - jusqu'à 5 options : blocs de boutons
  - 6-100 options : menu de sélection statique
  - plus de 100 options : sélection externe avec filtrage d'options asynchrone lorsque les gestionnaires d'options d'interactivité sont disponibles
  - si les valeurs d'option codées dépassent les limites de Slack, le flux revient aux boutons
- Pour les charges utiles d'options longues, les menus d'arguments de commande Slash utilisent une boîte de dialogue de confirmation avant de dispatcher une valeur sélectionnée.

Paramètres de commande slash par défaut :

- `enabled: false`
- `name: "openclaw"`
- `sessionPrefix: "slack:slash"`
- `ephemeral: true`

Les sessions Slash utilisent des clés isolées :

- `agent:<agentId>:slack:slash:<userId>`

et routent toujours l'exécution de la commande par rapport à la session de conversation cible (`CommandTargetSessionKey`).

## Threading, sessions et balises de réponse

- Les DMs routent comme `direct` ; les canaux comme `channel` ; les MPIMs comme `group`.
- Avec le `session.dmScope=main` par défaut, les DMs Slack s'effondrent dans la session principale de l'agent.
- Sessions de canal : `agent:<agentId>:slack:channel:<channelId>`.
- Les réponses de fil peuvent créer des suffixes de session de fil (`:thread:<threadTs>`) le cas échéant.
- La valeur par défaut de `channels.slack.thread.historyScope` est `thread` ; la valeur par défaut de `thread.inheritParent` est `false`.
- `channels.slack.thread.initialHistoryLimit` contrôle le nombre de messages de fil existants récupérés au démarrage d'une nouvelle session de fil (par défaut `20` ; définissez `0` pour désactiver).

Contrôles de threading de réponse :

- `channels.slack.replyToMode`: `off|first|all` (par défaut `off`)
- `channels.slack.replyToModeByChatType`: par `direct|group|channel`
- fallback héritage pour les chats directs : `channels.slack.dm.replyToMode`

Les balises de réponse manuelle sont supportées :

- `[[reply_to_current]]`
- `[[reply_to:<id>]]`

Remarque : `replyToMode="off"` désactive **tout** threading de réponse dans Slack, y compris les balises explicites `[[reply_to_*]]`. Cela diffère de Telegram, où les balises explicites sont toujours honorées en mode `"off"`. La différence reflète les modèles de threading de la plateforme : les fils Slack masquent les messages du canal, tandis que les réponses Telegram restent visibles dans le flux de chat principal.

## Médias, chunking et livraison

<AccordionGroup>
  <Accordion title="Pièces jointes entrantes">
    Les pièces jointes de fichier Slack sont téléchargées à partir d'URL privées hébergées par Slack (flux de requête authentifiée par token) et écrites dans le magasin de médias lorsque la récupération réussit et que les limites de taille le permettent.

    Le plafond de taille entrante à l'exécution est par défaut `20MB` sauf s'il est remplacé par `channels.slack.mediaMaxMb`.

  </Accordion>

  <Accordion title="Texte et fichiers sortants">
    - les chunks de texte utilisent `channels.slack.textChunkLimit` (par défaut 4000)
    - `channels.slack.chunkMode="newline"` active le fractionnement paragraphe-d'abord
    - les envois de fichiers utilisent les API de téléchargement Slack et peuvent inclure des réponses de fil (`thread_ts`)
    - le plafond de médias sortants suit `channels.slack.mediaMaxMb` lorsqu'il est configuré ; sinon les envois de canal utilisent les valeurs par défaut de type MIME du pipeline de médias
  </Accordion>

  <Accordion title="Cibles de livraison">
    Cibles explicites préférées :

    - `user:<id>` pour les DMs
    - `channel:<id>` pour les canaux

    Les DMs Slack sont ouverts via les API de conversation Slack lors de l'envoi à des cibles utilisateur.

  </Accordion>
</AccordionGroup>

## Actions et portes

Les actions Slack sont contrôlées par `channels.slack.actions.*`.

Groupes d'actions disponibles dans l'outillage Slack actuel :

| Groupe     | Par défaut |
| ---------- | ---------- |
| messages   | activé     |
| reactions  | activé     |
| pins       | activé     |
| memberInfo | activé     |
| emojiList  | activé     |

## Événements et comportement opérationnel

- Les éditions/suppressions/diffusions de fil de message sont mappées dans les événements système.
- Les événements d'ajout/suppression de réaction sont mappés dans les événements système.
- Les événements de jointure/départ de membre, création/renommage de canal et ajout/suppression de pin sont mappés dans les événements système.
- Les mises à jour du statut du fil d'assistant (pour les indicateurs "en cours de saisie..." dans les fils) utilisent `assistant.threads.setStatus` et nécessitent la portée bot `assistant:write`.
- `channel_id_changed` peut migrer les clés de configuration de canal lorsque `configWrites` est activé.
- Les métadonnées de sujet/objectif du canal sont traitées comme un contexte non fiable et peuvent être injectées dans le contexte de routage.
- Les actions de bloc et les interactions modales émettent des événements système structurés `Slack interaction: ...` avec des champs de charge ut
