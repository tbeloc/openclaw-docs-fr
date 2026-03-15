---
summary: "Configuration de Slack et comportement à l'exécution (Socket Mode + HTTP Events API)"
read_when:
  - Setting up Slack or debugging Slack socket/HTTP mode
title: "Slack"
---

# Slack

Statut : prêt pour la production pour les DMs + canaux via les intégrations d'applications Slack. Le mode par défaut est Socket Mode ; le mode HTTP Events API est également supporté.

<CardGroup cols={3}>
  <Card title="Appairage" icon="link" href="/fr/channels/pairing">
    Les DMs Slack sont par défaut en mode appairage.
  </Card>
  <Card title="Commandes slash" icon="terminal" href="/fr/tools/slash-commands">
    Comportement des commandes natives et catalogue de commandes.
  </Card>
  <Card title="Dépannage des canaux" icon="wrench" href="/fr/channels/troubleshooting">
    Diagnostics multi-canaux et playbooks de réparation.
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

        Activez également l'onglet **Messages** de l'App Home pour les DMs.
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
        - définissez Event Subscriptions + Interactivity + Slash command Request URL sur le même chemin webhook (par défaut `/slack/events`)

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

      <Step title="Utiliser des chemins webhook uniques pour HTTP multi-compte">
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
- `userToken` (`xoxp-...`) est configuration uniquement (pas de fallback d'environnement) et par défaut en lecture seule (`userTokenReadOnly: true`).
- Optionnel : ajoutez `chat:write.customize` si vous voulez que les messages sortants utilisent l'identité de l'agent actif (custom `username` et icône). `icon_emoji` utilise la syntaxe `:emoji_name:`.

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

    La liste d'autorisation des canaux se trouve sous `channels.slack.channels` et doit utiliser des IDs de canal stables.

    Note d'exécution : si `channels.slack` est complètement absent (configuration env uniquement), l'exécution revient à `groupPolicy="allowlist"` et enregistre un avertissement (même si `channels.defaults.groupPolicy` est défini).

    Résolution nom/ID :

    - les entrées de liste d'autorisation de canal et les entrées de liste d'autorisation DM sont résolues au démarrage lorsque l'accès au token le permet
    - les entrées de nom de canal non résolues sont conservées telles que configurées mais ignorées pour le routage par défaut
    - l'autorisation entrante et le routage de canal sont d'abord basés sur l'ID par défaut ; la correspondance directe nom d'utilisateur/slug nécessite `channels.slack.dangerouslyAllowNameMatching: true`

  </Tab>

  <Tab title="Mentions et utilisateurs de canal">
    Les messages de canal sont gérés par mention par défaut.

    Sources de mention :

    - mention explicite de l'application (`<@botId>`)
    - modèles de regex de mention (`agents.list[].groupChat.mentionPatterns`, fallback `messages.groupChat.mentionPatterns`)
    - comportement implicite de réponse au thread du bot

    Contrôles par canal (`channels.slack.channels.<id>` ; noms uniquement via résolution au démarrage ou `dangerouslyAllowNameMatching`) :

    - `requireMention`
    - `users` (liste d'autorisation)
    - `allowBots`
    - `skills`
    - `systemPrompt`
    - `tools`, `toolsBySender`
    - format de clé `toolsBySender` : `id:`, `e164:`, `username:`, `name:`, ou wildcard `"*"`
      (les clés héritées non préfixées mappent toujours à `id:` uniquement)

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
  - si les valeurs d'option encodées dépassent les limites de Slack, le flux revient aux boutons
- Pour les charges utiles d'options longues, les menus d'arguments de commande Slash utilisent une boîte de dialogue de confirmation avant de dispatcher une valeur sélectionnée.

## Réponses interactives

Slack peut afficher les contrôles de réponse interactive créés par l'agent, mais cette fonctionnalité est désactivée par défaut.

Activez-la globalement :

```json5
{
  channels: {
    slack: {
      capabilities: {
        interactiveReplies: true,
      },
    },
  },
}
```

Ou activez-la pour un seul compte Slack :

```json5
{
  channels: {
    slack: {
      accounts: {
        ops: {
          capabilities: {
            interactiveReplies: true,
          },
        },
      },
    },
  },
}
```

Lorsqu'elle est activée, les agents peuvent émettre des directives de réponse spécifiques à Slack :

- `[[slack_buttons: Approve:approve, Reject:reject]]`
- `[[slack_select: Choose a target | Canary:canary, Production:production]]`

Ces directives se compilent en Slack Block Kit et acheminent les clics ou sélections via le chemin d'événement d'interaction Slack existant.

Notes :

- Ceci est une interface utilisateur spécifique à Slack. Les autres canaux ne traduisent pas les directives Slack Block Kit dans leurs propres systèmes de boutons.
- Les valeurs de rappel interactif sont des tokens opaques générés par OpenClaw, pas des valeurs brutes créées par l'agent.
- Si les blocs interactifs générés dépasseraient les limites de Slack Block Kit, OpenClaw revient à la réponse texte d'origine au lieu d'envoyer une charge utile de blocs invalide.

Paramètres de commande slash par défaut :

- `enabled: false`
- `name: "openclaw"`
- `sessionPrefix: "slack:slash"`
- `ephemeral: true`

Les sessions Slash utilisent des clés isolées :

- `agent:<agentId>:slack:slash:<userId>`

et acheminent toujours l'exécution de commande contre la session de conversation cible (`CommandTargetSessionKey`).

## Threading, sessions et tags de réponse

- Les DMs acheminent comme `direct` ; les canaux comme `channel` ; les MPIMs comme `group`.
- Avec le `session.dmScope=main` par défaut, les DMs Slack s'effondrent dans la session principale de l'agent.
- Sessions de canal : `agent:<agentId>:slack:channel:<channelId>`.
- Les réponses de thread peuvent créer des suffixes de session de thread (`:thread:<threadTs>`) le cas échéant.
- La valeur par défaut de `channels.slack.thread.historyScope` est `thread` ; la valeur par défaut de `thread.inheritParent` est `false`.
- `channels.slack.thread.initialHistoryLimit` contrôle le nombre de messages de thread existants récupérés au démarrage d'une nouvelle session de thread (par défaut `20` ; définissez `0` pour désactiver).

Contrôles de threading de réponse :

- `channels.slack.replyToMode`: `off|first|all` (par défaut `off`)
- `channels.slack.replyToModeByChatType`: par `direct|group|channel`
- fallback héritage pour les chats directs : `channels.slack.dm.replyToMode`

Les tags de réponse manuels sont supportés :

- `[[reply_to_current]]`
- `[[reply_to:<id>]]`

Note : `replyToMode="off"` désactive **tout** threading de réponse dans Slack, y compris les tags explicites `[[reply_to_*]]`. Ceci diffère de Telegram, où les tags explicites sont toujours honorés en mode `"off"`. La différence reflète les modèles de threading de la plateforme : les threads Slack masquent les messages du canal, tandis que les réponses Telegram restent visibles dans le flux de chat principal.

## Médias, chunking et livraison

<AccordionGroup>
  <Accordion title="Pièces jointes entrantes">
    Les pièces jointes de fichier Slack sont téléchargées à partir d'URLs privées hébergées par Slack (flux de requête authentifié par token) et écrites dans le magasin de médias lorsque la récupération réussit et que les limites de taille le permettent.

    Le plafond de taille entrante à l'exécution est par défaut `20MB` sauf s'il est remplacé par `channels.slack.mediaMaxMb`.

  </Accordion>

  <Accordion title="Texte et fichiers sortants">
    - les chunks de texte utilisent `channels.slack.textChunkLimit` (par défaut 4000)
    - `channels.slack.chunkMode="newline"` active le fractionnement paragraphe-d'abord
    - les envois de fichier utilisent les APIs de téléchargement Slack et peuvent inclure des réponses de thread (`thread_ts`)
    - le plafond de médias sortants suit `channels.slack.mediaMaxMb` lorsqu'il est configuré ; sinon les envois de canal utilisent les valeurs par défaut de type MIME du pipeline de médias
  </Accordion>

  <Accordion title="Cibles de livraison">
    Cibles explicites préférées :

    - `user:<id>` pour les DMs
    - `channel:<id>` pour les canaux

    Les DMs Slack sont ouverts via les APIs de conversation Slack lors de l'envoi vers des cibles utilisateur.

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

- Les modifications/suppressions de messages/diffusions de threads sont mappées dans des événements système.
- Les événements d'ajout/suppression de réactions sont mappés dans des événements système.
- Les événements de jointure/départ de membres, création/renommage de canal et ajout/suppression d'épingle sont mappés dans des événements système.
- Les mises à jour du statut du thread assistant (pour les indicateurs "en train de taper..." dans les threads) utilisent `assistant.threads.setStatus` et nécessitent la portée bot `assistant:write`.
- `channel_id_changed` peut migrer les clés de configuration de canal lorsque `configWrites` est activé.
- Les métadonnées de sujet/objectif de canal sont traitées comme un contexte non fiable et peuvent être injectées dans le contexte de routage.
- Les actions de bloc et les interactions modales émettent des événements système structurés `Slack interaction: ...` avec des champs de charge utile enrichis :
  - actions de bloc : valeurs sélectionnées, étiquettes, valeurs du sélecteur et métadonnées `workflow_*`
  - événements `view_submission` et `view_closed` modaux avec métadonnées de canal routées et entrées de formulaire

## Réactions d'accusé de réception

`ackReaction` envoie un emoji d'accusé de réception tandis qu'OpenClaw traite un message entrant.

Ordre de résolution :

- `channels.slack.accounts.<accountId>.ackReaction`
- `channels.slack.ackReaction`
- `messages.ackReaction`
- emoji d'identité d'agent par défaut (`agents.list[].identity.emoji`, sinon "👀")

Remarques :

- Slack attend des codes courts (par exemple `"eyes"`).
- Utilisez `""` pour désactiver la réaction pour le compte Slack ou globalement.

## Réaction de saisie de secours

`typingReaction` ajoute une réaction temporaire au message Slack entrant tandis qu'OpenClaw traite une réponse, puis la supprime lorsque l'exécution se termine. C'est un bon secours lorsque la saisie native de l'assistant Slack n'est pas disponible, en particulier dans les DM.

Ordre de résolution :

- `channels.slack.accounts.<accountId>.typingReaction`
- `channels.slack.typingReaction`

Remarques :

- Slack attend des codes courts (par exemple `"hourglass_flowing_sand"`).
- La réaction est au mieux et le nettoyage est tenté automatiquement après la réponse ou le chemin d'échec se termine.

## Manifeste et liste de contrôle des portées

<AccordionGroup>
  <Accordion title="Exemple de manifeste d'application Slack">

```json
{
  "display_information": {
    "name": "OpenClaw",
    "description": "Slack connector for OpenClaw"
  },
  "features": {
    "bot_user": {
      "display_name": "OpenClaw",
      "always_online": false
    },
    "app_home": {
      "messages_tab_enabled": true,
      "messages_tab_read_only_enabled": false
    },
    "slash_commands": [
      {
        "command": "/openclaw",
        "description": "Send a message to OpenClaw",
        "should_escape": false
      }
    ]
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "chat:write",
        "channels:history",
        "channels:read",
        "groups:history",
        "im:history",
        "im:read",
        "im:write",
        "mpim:history",
        "mpim:read",
        "mpim:write",
        "users:read",
        "app_mentions:read",
        "assistant:write",
        "reactions:read",
        "reactions:write",
        "pins:read",
        "pins:write",
        "emoji:read",
        "commands",
        "files:read",
        "files:write"
      ]
    }
  },
  "settings": {
    "socket_mode_enabled": true,
    "event_subscriptions": {
      "bot_events": [
        "app_mention",
        "message.channels",
        "message.groups",
        "message.im",
        "message.mpim",
        "reaction_added",
        "reaction_removed",
        "member_joined_channel",
        "member_left_channel",
        "channel_rename",
        "pin_added",
        "pin_removed"
      ]
    }
  }
}
```

  </Accordion>

  <Accordion title="Portées de jeton utilisateur optionnelles (opérations de lecture)">
    Si vous configurez `channels.slack.userToken`, les portées de lecture typiques sont :

    - `channels:history`, `groups:history`, `im:history`, `mpim:history`
    - `channels:read`, `groups:read`, `im:read`, `mpim:read`
    - `users:read`
    - `reactions:read`
    - `pins:read`
    - `emoji:read`
    - `search:read` (si vous dépendez des lectures de recherche Slack)

  </Accordion>
</AccordionGroup>

## Dépannage

<AccordionGroup>
  <Accordion title="Pas de réponses dans les canaux">
    Vérifiez, dans l'ordre :

    - `groupPolicy`
    - liste blanche de canal (`channels.slack.channels`)
    - `requireMention`
    - liste blanche `users` par canal

    Commandes utiles :

```bash
openclaw channels status --probe
openclaw logs --follow
openclaw doctor
```

  </Accordion>

  <Accordion title="Messages DM ignorés">
    Vérifiez :

    - `channels.slack.dm.enabled`
    - `channels.slack.dmPolicy` (ou `channels.slack.dm.policy` hérité)
    - approbations d'appairage / entrées de liste blanche

```bash
openclaw pairing list slack
```

  </Accordion>

  <Accordion title="Mode Socket non connecté">
    Validez les jetons bot + app et l'activation du mode Socket dans les paramètres de l'application Slack.
  </Accordion>

  <Accordion title="Mode HTTP ne recevant pas d'événements">
    Validez :

    - secret de signature
    - chemin webhook
    - URL de requête Slack (Événements + Interactivité + Commandes slash)
    - `webhookPath` unique par compte HTTP

  </Accordion>

  <Accordion title="Commandes natives/slash ne se déclenchant pas">
    Vérifiez si vous aviez l'intention :

    - mode de commande native (`channels.slack.commands.native: true`) avec commandes slash correspondantes enregistrées dans Slack
    - ou mode de commande slash unique (`channels.slack.slashCommand.enabled: true`)

    Vérifiez également `commands.useAccessGroups` et les listes blanches de canal/utilisateur.

  </Accordion>
</AccordionGroup>

## Diffusion en continu de texte

OpenClaw prend en charge la diffusion en continu de texte native Slack via l'API Agents and AI Apps.

`channels.slack.streaming` contrôle le comportement d'aperçu en direct :

- `off` : désactiver la diffusion en continu d'aperçu.
- `partial` (par défaut) : remplacer le texte d'aperçu par la dernière sortie partielle.
- `block` : ajouter les mises à jour d'aperçu fragmentées.
- `progress` : afficher le texte d'état de progression pendant la génération, puis envoyer le texte final.

`channels.slack.nativeStreaming` contrôle l'API de diffusion en continu native de Slack (`chat.startStream` / `chat.appendStream` / `chat.stopStream`) lorsque `streaming` est `partial` (par défaut : `true`).

Désactiver la diffusion en continu native Slack (conserver le comportement d'aperçu brouillon) :

```yaml
channels:
  slack:
    streaming: partial
    nativeStreaming: false
```

Clés héritées :

- `channels.slack.streamMode` (`replace | status_final | append`) est automatiquement migré vers `channels.slack.streaming`.
- booléen `channels.slack.streaming` est automatiquement migré vers `channels.slack.nativeStreaming`.

### Exigences

1. Activez **Agents and AI Apps** dans les paramètres de votre application Slack.
2. Assurez-vous que l'application a la portée `assistant:write`.
3. Un thread de réponse doit être disponible pour ce message. La sélection du thread suit toujours `replyToMode`.

### Comportement

- Le premier bloc de texte démarre un flux (`chat.startStream`).
- Les blocs de texte ultérieurs s'ajoutent au même flux (`chat.appendStream`).
- La fin de la réponse finalise le flux (`chat.stopStream`).
- Les médias et les charges utiles non textuelles reviennent à la livraison normale.
- Si la diffusion en continu échoue au milieu de la réponse, OpenClaw revient à la livraison normale pour les charges utiles restantes.

## Pointeurs de référence de configuration

Référence principale :

- [Référence de configuration - Slack](/fr/gateway/configuration-reference#slack)

  Champs Slack à haut signal :
  - mode/auth : `mode`, `botToken`, `appToken`, `signingSecret`, `webhookPath`, `accounts.*`
  - accès DM : `dm.enabled`, `dmPolicy`, `allowFrom` (hérité : `dm.policy`, `dm.allowFrom`), `dm.groupEnabled`, `dm.groupChannels`
  - basculement de compatibilité : `dangerouslyAllowNameMatching` (verre de secours ; garder désactivé sauf si nécessaire)
  - accès au canal : `groupPolicy`, `channels.*`, `channels.*.users`, `channels.*.requireMention`
  - threading/historique : `replyToMode`, `replyToModeByChatType`, `thread.*`, `historyLimit`, `dmHistoryLimit`, `dms.*.historyLimit`
  - livraison : `textChunkLimit`, `chunkMode`, `mediaMaxMb`, `streaming`, `nativeStreaming`
  - ops/fonctionnalités : `configWrites`, `commands.native`, `slashCommand.*`, `actions.*`, `userToken`, `userTokenReadOnly`

## Connexes

- [Appairage](/fr/channels/pairing)
- [Routage de canal](/fr/channels/channel-routing)
- [Dépannage](/fr/channels/troubleshooting)
- [Configuration](/fr/gateway/configuration)
- [Commandes slash](/fr/tools/slash-commands)
