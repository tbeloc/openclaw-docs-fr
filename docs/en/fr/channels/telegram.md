---
summary: "Statut de support du bot Telegram, capacités et configuration"
read_when:
  - Working on Telegram features or webhooks
title: "Telegram"
---

# Telegram (Bot API)

Statut : prêt pour la production pour les DM de bot + groupes via grammY. Le long polling est le mode par défaut ; le mode webhook est optionnel.

<CardGroup cols={3}>
  <Card title="Appairage" icon="link" href="/channels/pairing">
    La politique DM par défaut pour Telegram est l'appairage.
  </Card>
  <Card title="Dépannage des canaux" icon="wrench" href="/channels/troubleshooting">
    Diagnostics multi-canaux et playbooks de réparation.
  </Card>
  <Card title="Configuration de la passerelle" icon="settings" href="/gateway/configuration">
    Modèles et exemples de configuration de canal complets.
  </Card>
</CardGroup>

## Configuration rapide

<Steps>
  <Step title="Créer le jeton du bot dans BotFather">
    Ouvrez Telegram et discutez avec **@BotFather** (confirmez que le handle est exactement `@BotFather`).

    Exécutez `/newbot`, suivez les invites et enregistrez le jeton.

  </Step>

  <Step title="Configurer le jeton et la politique DM">

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

    Fallback env : `TELEGRAM_BOT_TOKEN=...` (compte par défaut uniquement).
    Telegram n'utilise **pas** `openclaw channels login telegram` ; configurez le jeton dans config/env, puis démarrez la passerelle.

  </Step>

  <Step title="Démarrer la passerelle et approuver le premier DM">

```bash
openclaw gateway
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

    Les codes d'appairage expirent après 1 heure.

  </Step>

  <Step title="Ajouter le bot à un groupe">
    Ajoutez le bot à votre groupe, puis définissez `channels.telegram.groups` et `groupPolicy` pour correspondre à votre modèle d'accès.
  </Step>
</Steps>

<Note>
L'ordre de résolution des jetons est conscient du compte. En pratique, les valeurs de config l'emportent sur le fallback env, et `TELEGRAM_BOT_TOKEN` s'applique uniquement au compte par défaut.
</Note>

## Paramètres côté Telegram

<AccordionGroup>
  <Accordion title="Mode de confidentialité et visibilité des groupes">
    Les bots Telegram sont par défaut en **Mode de confidentialité**, ce qui limite les messages de groupe qu'ils reçoivent.

    Si le bot doit voir tous les messages du groupe, soit :

    - désactiver le mode de confidentialité via `/setprivacy`, soit
    - faire du bot un administrateur du groupe.

    Lors du basculement du mode de confidentialité, supprimez et rajoutez le bot dans chaque groupe pour que Telegram applique la modification.

  </Accordion>

  <Accordion title="Permissions de groupe">
    Le statut d'administrateur est contrôlé dans les paramètres du groupe Telegram.

    Les bots administrateurs reçoivent tous les messages du groupe, ce qui est utile pour un comportement de groupe toujours actif.

  </Accordion>

  <Accordion title="Bascules BotFather utiles">

    - `/setjoingroups` pour autoriser/refuser les ajouts de groupe
    - `/setprivacy` pour le comportement de visibilité du groupe

  </Accordion>
</AccordionGroup>

## Contrôle d'accès et activation

<Tabs>
  <Tab title="Politique DM">
    `channels.telegram.dmPolicy` contrôle l'accès aux messages directs :

    - `pairing` (par défaut)
    - `allowlist` (nécessite au moins un ID d'expéditeur dans `allowFrom`)
    - `open` (nécessite que `allowFrom` inclue `"*"`)
    - `disabled`

    `channels.telegram.allowFrom` accepte les ID d'utilisateur Telegram numériques. Les préfixes `telegram:` / `tg:` sont acceptés et normalisés.
    `dmPolicy: "allowlist"` avec `allowFrom` vide bloque tous les DM et est rejeté par la validation de la configuration.
    L'assistant d'intégration accepte l'entrée `@username` et la résout en ID numériques.
    Si vous avez effectué une mise à niveau et que votre configuration contient des entrées de liste d'autorisation `@username`, exécutez `openclaw doctor --fix` pour les résoudre (meilleur effort ; nécessite un jeton de bot Telegram).
    Si vous aviez précédemment compté sur les fichiers de liste d'autorisation du magasin d'appairage, `openclaw doctor --fix` peut récupérer les entrées dans `channels.telegram.allowFrom` dans les flux de liste d'autorisation (par exemple lorsque `dmPolicy: "allowlist"` n'a pas encore d'ID explicites).

    Pour les bots à propriétaire unique, préférez `dmPolicy: "allowlist"` avec des ID `allowFrom` numériques explicites pour maintenir la politique d'accès durable dans la configuration (au lieu de dépendre des approbations d'appairage précédentes).

    ### Trouver votre ID d'utilisateur Telegram

    Plus sûr (pas de bot tiers) :

    1. Envoyez un DM à votre bot.
    2. Exécutez `openclaw logs --follow`.
    3. Lisez `from.id`.

    Méthode officielle de l'API Bot :

```bash
curl "https://api.telegram.org/bot<bot_token>/getUpdates"
```

    Méthode tierce (moins privée) : `@userinfobot` ou `@getidsbot`.

  </Tab>

  <Tab title="Politique de groupe et listes d'autorisation">
    Deux contrôles s'appliquent ensemble :

    1. **Quels groupes sont autorisés** (`channels.telegram.groups`)
       - pas de configuration `groups` :
         - avec `groupPolicy: "open"` : n'importe quel groupe peut passer les vérifications d'ID de groupe
         - avec `groupPolicy: "allowlist"` (par défaut) : les groupes sont bloqués jusqu'à ce que vous ajoutiez des entrées `groups` (ou `"*"`)
       - `groups` configuré : agit comme liste d'autorisation (ID explicites ou `"*"`)

    2. **Quels expéditeurs sont autorisés dans les groupes** (`channels.telegram.groupPolicy`)
       - `open`
       - `allowlist` (par défaut)
       - `disabled`

    `groupAllowFrom` est utilisé pour le filtrage des expéditeurs de groupe. S'il n'est pas défini, Telegram revient à `allowFrom`.
    Les entrées `groupAllowFrom` doivent être des ID d'utilisateur Telegram numériques (les préfixes `telegram:` / `tg:` sont normalisés).
    Ne mettez pas les ID de chat de groupe ou de supergroupe Telegram dans `groupAllowFrom`. Les ID de chat négatifs appartiennent à `channels.telegram.groups`.
    Les entrées non numériques sont ignorées pour l'autorisation de l'expéditeur.
    Limite de sécurité (`2026.2.25+`) : l'authentification de l'expéditeur du groupe n'hérite **pas** des approbations du magasin d'appairage DM.
    L'appairage reste DM uniquement. Pour les groupes, définissez `groupAllowFrom` ou `allowFrom` par groupe/par sujet.
    Note d'exécution : si `channels.telegram` est complètement absent, l'exécution par défaut est `groupPolicy="allowlist"` fermé à moins que `channels.defaults.groupPolicy` soit explicitement défini.

    Exemple : autoriser n'importe quel membre dans un groupe spécifique :

```json5
{
  channels: {
    telegram: {
      groups: {
        "-1001234567890": {
          groupPolicy: "open",
          requireMention: false,
        },
      },
    },
  },
}
```

    Exemple : autoriser uniquement des utilisateurs spécifiques dans un groupe spécifique :

```json5
{
  channels: {
    telegram: {
      groups: {
        "-1001234567890": {
          requireMention: true,
          allowFrom: ["8734062810", "745123456"],
        },
      },
    },
  },
}
```

    <Warning>
      Erreur courante : `groupAllowFrom` n'est pas une liste d'autorisation de groupe Telegram.

      - Mettez les ID de chat de groupe ou de supergroupe Telegram négatifs comme `-1001234567890` sous `channels.telegram.groups`.
      - Mettez les ID d'utilisateur Telegram comme `8734062810` sous `groupAllowFrom` lorsque vous voulez limiter les personnes d'un groupe autorisé qui peuvent déclencher le bot.
      - Utilisez `groupAllowFrom: ["*"]` uniquement lorsque vous voulez que n'importe quel membre d'un groupe autorisé puisse parler au bot.
    </Warning>

  </Tab>

  <Tab title="Comportement de mention">
    Les réponses de groupe nécessitent une mention par défaut.

    La mention peut provenir de :

    - mention native `@botusername`, ou
    - modèles de mention dans :
      - `agents.list[].groupChat.mentionPatterns`
      - `messages.groupChat.mentionPatterns`

    Bascules de commande au niveau de la session :

    - `/activation always`
    - `/activation mention`

    Celles-ci mettent à jour l'état de la session uniquement. Utilisez la configuration pour la persistance.

    Exemple de configuration persistante :

```json5
{
  channels: {
    telegram: {
      groups: {
        "*": { requireMention: false },
      },
    },
  },
}
```

    Obtenir l'ID du chat de groupe :

    - transférer un message de groupe à `@userinfobot` / `@getidsbot`
    - ou lire `chat.id` à partir de `openclaw logs --follow`
    - ou inspecter l'API Bot `getUpdates`

  </Tab>
</Tabs>

## Comportement à l'exécution

- Telegram est détenu par le processus de passerelle.
- Le routage est déterministe : les réponses entrantes Telegram reviennent à Telegram (le modèle ne choisit pas les canaux).
- Les messages entrants se normalisent dans l'enveloppe de canal partagée avec les métadonnées de réponse et les espaces réservés de média.
- Les sessions de groupe sont isolées par ID de groupe. Les sujets du forum ajoutent `:topic:<threadId>` pour garder les sujets isolés.
- Les messages DM peuvent porter `message_thread_id` ; OpenClaw les achemine avec des clés de session conscientes des threads et préserve l'ID de thread pour les réponses.
- Le long polling utilise le runner grammY avec séquençage par chat/par thread. La concurrence globale du sink du runner utilise `agents.defaults.maxConcurrent`.
- L'API Bot Telegram n'a pas de support de reçu de lecture (`sendReadReceipts` ne s'applique pas).

## Référence des fonctionnalités

<AccordionGroup>
  <Accordion title="Aperçu du flux en direct (éditions de messages)">
    OpenClaw peut diffuser en continu des réponses partielles en temps réel :

    - chats directs : message d'aperçu + `editMessageText`
    - groupes/sujets : message d'aperçu + `editMessageText`

    Condition requise :

    - `channels.telegram.streaming` est `off | partial | block | progress` (par défaut : `partial`)
    - `progress` correspond à `partial` sur Telegram (compatibilité avec la dénomination inter-canaux)
    - les valeurs héritées `channels.telegram.streamMode` et booléennes `streaming` sont automatiquement mappées

    Pour les réponses texte uniquement :

    - DM : OpenClaw conserve le même message d'aperçu et effectue une édition finale sur place (pas de deuxième message)
    - groupe/sujet : OpenClaw conserve le même message d'aperçu et effectue une édition finale sur place (pas de deuxième message)

    Pour les réponses complexes (par exemple les charges utiles multimédias), OpenClaw revient à la livraison finale normale, puis nettoie le message d'aperçu.

    La diffusion d'aperçu est distincte de la diffusion de bloc. Lorsque la diffusion de bloc est explicitement activée pour Telegram, OpenClaw ignore le flux d'aperçu pour éviter la double diffusion.

    Si le transport de brouillon natif n'est pas disponible/rejeté, OpenClaw revient automatiquement à `sendMessage` + `editMessageText`.

    Flux de raisonnement spécifique à Telegram :

    - `/reasoning stream` envoie le raisonnement à l'aperçu en direct pendant la génération
    - la réponse finale est envoyée sans texte de raisonnement

  </Accordion>

  <Accordion title="Formatage et secours HTML">
    Le texte sortant utilise Telegram `parse_mode: "HTML"`.

    - Le texte de type Markdown est rendu en HTML sûr pour Telegram.
    - Le HTML brut du modèle est échappé pour réduire les défaillances d'analyse de Telegram.
    - Si Telegram rejette le HTML analysé, OpenClaw réessaie en texte brut.

    Les aperçus de lien sont activés par défaut et peuvent être désactivés avec `channels.telegram.linkPreview: false`.

  </Accordion>

  <Accordion title="Commandes natives et commandes personnalisées">
    L'enregistrement du menu de commandes Telegram est géré au démarrage avec `setMyCommands`.

    Valeurs par défaut des commandes natives :

    - `commands.native: "auto"` active les commandes natives pour Telegram

    Ajouter des entrées de menu de commandes personnalisées :

```json5
{
  channels: {
    telegram: {
      customCommands: [
        { command: "backup", description: "Git backup" },
        { command: "generate", description: "Create an image" },
      ],
    },
  },
}
```

    Règles :

    - les noms sont normalisés (suppression du `/` initial, minuscules)
    - modèle valide : `a-z`, `0-9`, `_`, longueur `1..32`
    - les commandes personnalisées ne peuvent pas remplacer les commandes natives
    - les conflits/doublons sont ignorés et enregistrés

    Notes :

    - les commandes personnalisées sont des entrées de menu uniquement ; elles n'implémentent pas automatiquement le comportement
    - les commandes de plugin/compétence peuvent toujours fonctionner lorsqu'elles sont tapées même si elles ne sont pas affichées dans le menu Telegram

    Si les commandes natives sont désactivées, les éléments intégrés sont supprimés. Les commandes personnalisées/plugin peuvent toujours s'enregistrer si configurées.

    Défaillances de configuration courantes :

    - `setMyCommands failed` avec `BOT_COMMANDS_TOO_MUCH` signifie que le menu Telegram a toujours débordé après la réduction ; réduisez les commandes de plugin/compétence/personnalisées ou désactivez `channels.telegram.commands.native`.
    - `setMyCommands failed` avec des erreurs réseau/fetch signifie généralement que le DNS/HTTPS sortant vers `api.telegram.org` est bloqué.

    ### Commandes d'appairage d'appareils (plugin `device-pair`)

    Lorsque le plugin `device-pair` est installé :

    1. `/pair` génère un code de configuration
    2. collez le code dans l'application iOS
    3. `/pair approve` approuve la dernière demande en attente

    Plus de détails : [Appairage](/channels/pairing#pair-via-telegram-recommended-for-ios).

  </Accordion>

  <Accordion title="Boutons en ligne">
    Configurer la portée du clavier en ligne :

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

    Remplacement par compte :

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

    - `off`
    - `dm`
    - `group`
    - `all`
    - `allowlist` (par défaut)

    L'héritage `capabilities: ["inlineButtons"]` correspond à `inlineButtons: "all"`.

    Exemple d'action de message :

```json5
{
  action: "send",
  channel: "telegram",
  to: "123456789",
  message: "Choose an option:",
  buttons: [
    [
      { text: "Yes", callback_data: "yes" },
      { text: "No", callback_data: "no" },
    ],
    [{ text: "Cancel", callback_data: "cancel" }],
  ],
}
```

    Les clics de rappel sont transmis à l'agent sous forme de texte :
    `callback_data: <value>`

  </Accordion>

  <Accordion title="Actions de messages Telegram pour les agents et l'automatisation">
    Les actions d'outils Telegram incluent :

    - `sendMessage` (`to`, `content`, `mediaUrl` optionnel, `replyToMessageId`, `messageThreadId`)
    - `react` (`chatId`, `messageId`, `emoji`)
    - `deleteMessage` (`chatId`, `messageId`)
    - `editMessage` (`chatId`, `messageId`, `content`)
    - `createForumTopic` (`chatId`, `name`, `iconColor` optionnel, `iconCustomEmojiId`)

    Les actions de messages de canal exposent des alias ergonomiques (`send`, `react`, `delete`, `edit`, `sticker`, `sticker-search`, `topic-create`).

    Contrôles de limitation :

    - `channels.telegram.actions.sendMessage`
    - `channels.telegram.actions.deleteMessage`
    - `channels.telegram.actions.reactions`
    - `channels.telegram.actions.sticker` (par défaut : désactivé)

    Note : `edit` et `topic-create` sont actuellement activés par défaut et n'ont pas de basculements `channels.telegram.actions.*` séparés.
    Les envois à l'exécution utilisent l'instantané de configuration/secrets actif (démarrage/rechargement), donc les chemins d'action n'effectuent pas de re-résolution SecretRef ad-hoc par envoi.

    Sémantique de suppression de réaction : [/tools/reactions](/tools/reactions)

  </Accordion>

  <Accordion title="Balises de threading de réponse">
    Telegram prend en charge les balises de threading de réponse explicites dans la sortie générée :

    - `[[reply_to_current]]` répond au message déclencheur
    - `[[reply_to:<id>]]` répond à un ID de message Telegram spécifique

    `channels.telegram.replyToMode` contrôle la gestion :

    - `off` (par défaut)
    - `first`
    - `all`

    Note : `off` désactive le threading de réponse implicite. Les balises explicites `[[reply_to_*]]` sont toujours honorées.

  </Accordion>

  <Accordion title="Sujets de forum et comportement des threads">
    Supergroups de forum :

    - les clés de session de sujet ajoutent `:topic:<threadId>`
    - les réponses et la saisie ciblent le thread de sujet
    - chemin de configuration de sujet :
      `channels.telegram.groups.<chatId>.topics.<threadId>`

    Sujet général (`threadId=1`) cas spécial :

    - les envois de messages omettent `message_thread_id` (Telegram rejette `sendMessage(...thread_id=1)`)
    - les actions de saisie incluent toujours `message_thread_id`

    Héritage de sujet : les entrées de sujet héritent des paramètres de groupe sauf s'ils sont remplacés (`requireMention`, `allowFrom`, `skills`, `systemPrompt`, `enabled`, `groupPolicy`).
    `agentId` est spécifique au sujet et n'hérite pas des valeurs par défaut du groupe.

    **Routage d'agent par sujet** : Chaque sujet peut router vers un agent différent en définissant `agentId` dans la configuration du sujet. Cela donne à chaque sujet son propre espace de travail isolé, sa mémoire et sa session. Exemple :

    ```json5
    {
      channels: {
        telegram: {
          groups: {
            "-1001234567890": {
              topics: {
                "1": { agentId: "main" },      // General topic → main agent
                "3": { agentId: "zu" },        // Dev topic → zu agent
                "5": { agentId: "coder" }      // Code review → coder agent
              }
            }
          }
        }
      }
    }
    ```

    Chaque sujet a alors sa propre clé de session : `agent:zu:telegram:group:-1001234567890:topic:3`

    **Liaison de sujet ACP persistante** : Les sujets de forum peuvent épingler les sessions du harnais ACP via les liaisons ACP typées de niveau supérieur :

    - `bindings[]` avec `type: "acp"` et `match.channel: "telegram"`

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
            channel: "telegram",
            accountId: "default",
            peer: { kind: "group", id: "-1001234567890:topic:42" },
          },
        },
      ],
      channels: {
        telegram: {
          groups: {
            "-1001234567890": {
              topics: {
                "42": {
                  requireMention: false,
                },
              },
            },
          },
        },
      },
    }
    ```

    Ceci est actuellement limité aux sujets de forum dans les groupes et supergroups.

    **Génération ACP liée au thread à partir du chat** :

    - `/acp spawn <agent> --thread here|auto` peut lier le sujet Telegram actuel à une nouvelle session ACP.
    - Les messages de sujet de suivi routent directement vers la session ACP liée (pas de `/acp steer` requis).
    - OpenClaw épingle le message de confirmation de génération dans le sujet après une liaison réussie.
    - Nécessite `channels.telegram.threadBindings.spawnAcpSessions=true`.

    Le contexte du modèle inclut :

    - `MessageThreadId`
    - `IsForum`

    Comportement des threads DM :

    - les chats privés avec `message_thread_id` conservent le routage DM mais utilisent des clés de session/cibles de réponse conscientes des threads.

  </Accordion>

  <Accordion title="Audio, vidéo et autocollants">
    ### Messages audio

    Telegram distingue les notes vocales des fichiers audio.

    - par défaut : comportement de fichier audio
    - balise `[[audio_as_voice]]` dans la réponse de l'agent pour forcer l'envoi de note vocale

    Exemple d'action de message :

```json5
{
  action: "send",
  channel: "telegram",
  to: "123456789",
  media: "https://example.com/voice.ogg",
  asVoice: true,
}
```

    ### Messages vidéo

    Telegram distingue les fichiers vidéo des notes vidéo.

    Exemple d'action de message :

```json5
{
  action: "send",
  channel: "telegram",
  to: "123456789",
  media: "https://example.com/video.mp4",
  asVideoNote: true,
}
```

    Les notes vidéo ne supportent pas les légendes ; le texte du message fourni est envoyé séparément.

    ### Autocollants

    Gestion des autocollants entrants :

    - WEBP statique : téléchargé et traité (espace réservé `<media:sticker>`)
    - TGS animé : ignoré
    - WEBM vidéo : ignoré

    Champs de contexte d'autocollant :

    - `Sticker.emoji`
    - `Sticker.setName`
    - `Sticker.fileId`
    - `Sticker.fileUniqueId`
    - `Sticker.cachedDescription`

    Fichier de cache d'autocollant :

    - `~/.openclaw/telegram/sticker-cache.json`

    Les autocollants sont décrits une fois (si possible) et mis en cache pour réduire les appels de vision répétés.

    Activer les actions d'autocollant :

```json5
{
  channels: {
    telegram: {
      actions: {
        sticker: true,
      },
    },
  },
}
```

    Action d'envoi d'autocollant :

```json5
{
  action: "sticker",
  channel: "telegram",
  to: "123456789",
  fileId: "CAACAgIAAxkBAAI...",
}
```

    Rechercher les autocollants en cache :

```json5
{
  action: "sticker-search",
  channel: "telegram",
  query: "cat waving",
  limit: 5,
}
```

  </Accordion>

  <Accordion title="Notifications de réaction">
    Les réactions Telegram arrivent sous forme de mises à jour `message_reaction` (séparées des charges utiles de message).

    Lorsqu'elle est activée, OpenClaw met en file d'attente les événements système comme :

    - `Telegram reaction added: 👍 by Alice (@alice) on msg 42`

    Configuration :

    - `channels.telegram.reactionNotifications` : `off | own | all` (par défaut : `own`)
    - `channels.telegram.reactionLevel` : `off | ack | minimal | extensive` (par défaut : `minimal`)

    Notes :

    - `own` signifie les réactions de l'utilisateur aux messages envoyés par le bot uniquement (meilleur effort via le cache des messages envoyés).
    - Les événements de réaction respectent toujours les contrôles d'accès Telegram (`dmPolicy`, `allowFrom`, `groupPolicy`, `groupAllowFrom`) ; les expéditeurs non autorisés sont supprimés.
    - Telegram ne fournit pas les ID de thread dans les mises à jour de réaction.
      - les groupes non-forum routent vers la session de chat de groupe
      - les groupes de forum routent vers la session de sujet général du groupe (`:topic:1`), pas le sujet d'origine exact

    `allowed_updates` pour l'interrogation/webhook incluent automatiquement `message_reaction`.

  </Accordion>

  <Accordion title="Réactions d'accusé de réception">
    `ackReaction` envoie un emoji d'accusé de réception pendant qu'OpenClaw traite un message entrant.

    Ordre de résolution :

    - `channels.telegram.accounts.<accountId>.ackReaction`
    - `channels.telegram.ackReaction`
    - `messages.ackReaction`
    - secours d'emoji d'identité d'agent (`agents.list[].identity.emoji`, sinon "👀")

    Notes :

    - Telegram s'attend à un emoji unicode (par exemple "👀").
    - Utilisez `""` pour désactiver la réaction pour un canal ou un compte.

  </Accordion>

  <Accordion title="Écritures de configuration à partir d'événements et de commandes Telegram">
    Les écritures de configuration de canal sont activées par défaut (`configWrites !== false`).

    Les écritures déclenchées par Telegram incluent :

    - événements de migration de groupe (`migrate_to_chat_id`) pour mettre à jour `channels.telegram.groups`
    - `/config set` et `/config unset` (nécessite l'activation de la commande)

    Désactiver :

```json5
{
  channels: {
    telegram: {
      configWrites: false,
    },
  },
}
```

  </Accordion>

  <Accordion title="Interrogation longue vs webhook">
    Par défaut : interrogation longue.

    Mode webhook :

    - définir `channels.telegram.webhookUrl`
    - définir `channels.telegram.webhookSecret` (requis lorsque l'URL du webhook est définie)
    - `channels.telegram.webhookPath` optionnel (par défaut `/telegram-webhook`)
    - `channels.telegram.webhookHost` optionnel (par défaut `127.0.0.1`)
    - `channels.telegram.webhookPort` optionnel (par défaut `8787`)

    L'écouteur local par défaut pour le mode webhook se lie à `127.0.0.1:8787`.

    Si votre point de terminaison public diffère, placez un proxy inverse devant et pointez `webhookUrl` vers l'URL publique.
    Définissez `webhookHost` (par exemple `0.0.0.0`) lorsque vous avez besoin intentionnellement d'une entrée externe.

  </Accordion>

  <Accordion title="Limites, nouvelle tentative et cibles CLI">
    - `channels.telegram.textChunkLimit` par défaut est 4000.
    - `channels.telegram.chunkMode="newline"` préfère les limites de paragraphe (lignes vides) avant la division de longueur.
    - `channels.telegram.mediaMaxMb` (par défaut 100) limite la taille des médias Telegram entrants et sortants.
    - `channels.telegram.timeoutSeconds` remplace le délai d'expiration du client API Telegram (si non défini, la valeur par défaut de grammY s'applique).
    - l'historique du contexte de groupe utilise `channels.telegram.historyLimit` ou `messages.groupChat.historyLimit` (par défaut 50) ; `0` désactive.
    - Contrôles d'historique DM :
      - `channels.telegram.dmHistoryLimit`
      - `channels.telegram.dms["<user_id>"].historyLimit`
    - la configuration `channels.telegram.retry` s'applique aux assistants d'envoi Telegram (CLI/outils/actions) pour les erreurs API sortantes récupérables.

    La cible d'envoi CLI peut être un ID de chat numérique ou un nom d'utilisateur :

```bash
openclaw message send --channel telegram --target 123456789 --message "hi"
openclaw message send --channel telegram --target @name --message "hi"
```

    Les sondages Telegram utilisent `openclaw message poll` et supportent les sujets de forum :

```bash
openclaw message poll --channel telegram --target 123456789 \
  --poll-question "Ship it?" --poll-option "Yes" --poll-option "No"
openclaw message poll --channel telegram --target -1001234567890:topic:42 \
  --poll-question "Pick a time" --poll-option "10am" --poll-option "2pm" \
  --poll-duration-seconds 300 --poll-public
```

    Drapeaux de sondage spécifiques à Telegram :

    - `--poll-duration-seconds` (5-600)
    - `--poll-anonymous`
    - `--poll-public`
    - `--thread-id` pour les sujets de forum (ou utilisez une cible `:topic:`)

    Limitation d'action :

    - `channels.telegram.actions.sendMessage=false` désactive les messages Telegram sortants, y compris les sondages
    - `channels.telegram.actions.poll=false` désactive la création de sondage Telegram tout en laissant les envois réguliers activés

  </Accordion>

  <Accordion title="Approbations d'exécution dans Telegram">
    Telegram prend en charge les approbations d'exécution dans les DM des approbateurs et peut éventuellement publier des invites d'approbation dans le chat ou le sujet d'origine.

    Chemin de configuration :

    - `channels.telegram.execApprovals.enabled`
    - `channels.telegram.execApprovals.approvers`
    - `channels.telegram.execApprovals.target` (`dm` | `channel` | `both`, par défaut : `dm`)
    - `agentFilter`, `sessionFilter`

    Les approbateurs doivent être des ID d'utilisateur Telegram numériques. Lorsque `enabled` est faux ou `approvers` est vide, Telegram n'agit pas en tant que client d'approbation d'exécution. Les demandes d'approbation reviennent à d'autres itinéraires d'approbation configurés ou à la politique de secours d'approbation d'exécution.

    Règles de livraison :

    - `target: "dm"` envoie les invites d'approbation uniquement aux DM des approbateurs configurés
    - `target: "channel"` renvoie l'invite au chat/sujet Telegram d'origine
    - `target: "both"` envoie aux DM des approbateurs et au chat/sujet d'origine

    Seuls les approbateurs configurés peuvent approuver ou refuser. Les non-approbateurs ne peuvent pas utiliser `/approve` et ne peuvent pas utiliser les boutons d'approbation Telegram.

    La livraison de canal affiche le texte de la commande dans le chat, donc n'activez `channel` ou `both` que dans les groupes/sujets de confiance. Lorsque l'invite arrive dans un sujet de forum, OpenClaw préserve le sujet à la fois pour l'invite d'approbation et le suivi post-approbation.

    Les boutons d'approbation en ligne dépendent également de `channels.telegram.capabilities.inlineButtons` permettant la surface cible (`dm`, `group`, ou `all`).

    Documentation connexe : [Approbations d'exécution](/tools/exec-approvals)

  </Accordion>
</AccordionGroup>

## Dépannage

<AccordionGroup>
  <Accordion title="Le bot ne répond pas aux messages de groupe sans mention">

    - Si `requireMention=false`, le mode de confidentialité Telegram doit permettre une visibilité complète.
      - BotFather : `/setprivacy` -> Désactiver
      - puis supprimer et réajouter le bot au groupe
    - `openclaw channels status` avertit lorsque la configuration s'attend à des messages de groupe sans mention.
    - `openclaw channels status --probe` peut vérifier les ID de groupe numériques explicites ; le caractère générique `"*"` ne peut pas être sondé pour l'adhésion.
    - test de session rapide : `/activation always`.

  </Accordion>

  <Accordion title="Le bot ne voit pas du tout les messages de groupe">

    - quand `channels.telegram.groups` existe, le groupe doit être listé (ou inclure `"*"`)
    - vérifier l'adhésion du bot au groupe
    - consulter les journaux : `openclaw logs --follow` pour les raisons d'omission

  </Accordion>

  <Accordion title="Les commandes fonctionnent partiellement ou pas du tout">

    - autoriser votre identité d'expéditeur (appairage et/ou `allowFrom` numérique)
    - l'autorisation des commandes s'applique toujours même lorsque la politique de groupe est `open`
    - `setMyCommands failed` avec `BOT_COMMANDS_TOO_MUCH` signifie que le menu natif a trop d'entrées ; réduire les commandes de plugin/compétence/personnalisées ou désactiver les menus natifs
    - `setMyCommands failed` avec des erreurs réseau/fetch indique généralement des problèmes de réachabilité DNS/HTTPS vers `api.telegram.org`

  </Accordion>

  <Accordion title="Instabilité du polling ou du réseau">

    - Node 22+ + fetch/proxy personnalisé peut déclencher un comportement d'abandon immédiat si les types AbortSignal ne correspondent pas.
    - Certains hôtes résolvent `api.telegram.org` en IPv6 en premier ; une sortie IPv6 cassée peut causer des défaillances intermittentes de l'API Telegram.
    - Si les journaux incluent `TypeError: fetch failed` ou `Network request for 'getUpdates' failed!`, OpenClaw réessaie maintenant ces erreurs réseau comme récupérables.
    - Sur les hôtes VPS avec sortie/TLS directe instable, acheminez les appels de l'API Telegram via `channels.telegram.proxy` :

```yaml
channels:
  telegram:
    proxy: socks5://<user>:<password>@proxy-host:1080
```

    - Node 22+ utilise par défaut `autoSelectFamily=true` (sauf WSL2) et `dnsResultOrder=ipv4first`.
    - Si votre hôte est WSL2 ou fonctionne explicitement mieux avec un comportement IPv4 uniquement, forcez la sélection de famille :

```yaml
channels:
  telegram:
    network:
      autoSelectFamily: false
```

    - Remplacements d'environnement (temporaires) :
      - `OPENCLAW_TELEGRAM_DISABLE_AUTO_SELECT_FAMILY=1`
      - `OPENCLAW_TELEGRAM_ENABLE_AUTO_SELECT_FAMILY=1`
      - `OPENCLAW_TELEGRAM_DNS_RESULT_ORDER=ipv4first`
    - Valider les réponses DNS :

```bash
dig +short api.telegram.org A
dig +short api.telegram.org AAAA
```

  </Accordion>
</AccordionGroup>

Plus d'aide : [Dépannage des canaux](/channels/troubleshooting).

## Pointeurs de référence de configuration Telegram

Référence principale :

- `channels.telegram.enabled` : activer/désactiver le démarrage du canal.
- `channels.telegram.botToken` : jeton du bot (BotFather).
- `channels.telegram.tokenFile` : lire le jeton à partir d'un chemin de fichier régulier. Les liens symboliques sont rejetés.
- `channels.telegram.dmPolicy` : `pairing | allowlist | open | disabled` (par défaut : pairing).
- `channels.telegram.allowFrom` : liste blanche des MP (ID utilisateur Telegram numériques). `allowlist` nécessite au moins un ID d'expéditeur. `open` nécessite `"*"`. `openclaw doctor --fix` peut résoudre les entrées `@username` héritées en ID et peut récupérer les entrées de liste blanche à partir des fichiers de magasin d'appairage dans les flux de migration de liste blanche.
- `channels.telegram.actions.poll` : activer ou désactiver la création de sondage Telegram (par défaut : activé ; nécessite toujours `sendMessage`).
- `channels.telegram.defaultTo` : cible Telegram par défaut utilisée par la CLI `--deliver` quand aucun `--reply-to` explicite n'est fourni.
- `channels.telegram.groupPolicy` : `open | allowlist | disabled` (par défaut : allowlist).
- `channels.telegram.groupAllowFrom` : liste blanche des expéditeurs de groupe (ID utilisateur Telegram numériques). `openclaw doctor --fix` peut résoudre les entrées `@username` héritées en ID. Les entrées non numériques sont ignorées au moment de l'authentification. L'authentification de groupe n'utilise pas la solution de secours du magasin d'appairage MP (`2026.2.25+`).
- Précédence multi-compte :
  - Quand deux ou plusieurs ID de compte sont configurés, définissez `channels.telegram.defaultAccount` (ou incluez `channels.telegram.accounts.default`) pour rendre le routage par défaut explicite.
  - Si aucun n'est défini, OpenClaw revient au premier ID de compte normalisé et `openclaw doctor` avertit.
  - `channels.telegram.accounts.default.allowFrom` et `channels.telegram.accounts.default.groupAllowFrom` s'appliquent uniquement au compte `default`.
  - Les comptes nommés héritent de `channels.telegram.allowFrom` et `channels.telegram.groupAllowFrom` quand les valeurs au niveau du compte ne sont pas définies.
  - Les comptes nommés n'héritent pas de `channels.telegram.accounts.default.allowFrom` / `groupAllowFrom`.
- `channels.telegram.groups` : valeurs par défaut par groupe + liste blanche (utilisez `"*"` pour les valeurs par défaut globales).
  - `channels.telegram.groups.<id>.groupPolicy` : remplacement par groupe pour groupPolicy (`open | allowlist | disabled`).
  - `channels.telegram.groups.<id>.requireMention` : valeur par défaut de la mention gating.
  - `channels.telegram.groups.<id>.skills` : filtre de compétence (omis = toutes les compétences, vide = aucune).
  - `channels.telegram.groups.<id>.allowFrom` : remplacement de la liste blanche des expéditeurs par groupe.
  - `channels.telegram.groups.<id>.systemPrompt` : invite système supplémentaire pour le groupe.
  - `channels.telegram.groups.<id>.enabled` : désactiver le groupe quand `false`.
  - `channels.telegram.groups.<id>.topics.<threadId>.*` : remplacements par sujet (champs de groupe + `agentId` spécifique au sujet).
  - `channels.telegram.groups.<id>.topics.<threadId>.agentId` : acheminer ce sujet vers un agent spécifique (remplace le routage au niveau du groupe et de la liaison).
- `channels.telegram.groups.<id>.topics.<threadId>.groupPolicy` : remplacement par sujet pour groupPolicy (`open | allowlist | disabled`).
- `channels.telegram.groups.<id>.topics.<threadId>.requireMention` : remplacement par sujet de la mention gating.
- `bindings[]` de haut niveau avec `type: "acp"` et ID de sujet canonique `chatId:topic:topicId` dans `match.peer.id` : champs de liaison de sujet ACP persistants (voir [Agents ACP](/tools/acp-agents#channel-specific-settings)).
- `channels.telegram.direct.<id>.topics.<threadId>.agentId` : acheminer les sujets MP vers un agent spécifique (même comportement que les sujets de forum).
- `channels.telegram.execApprovals.enabled` : activer Telegram comme client d'approbation d'exécution basé sur le chat pour ce compte.
- `channels.telegram.execApprovals.approvers` : ID utilisateur Telegram autorisés à approuver ou refuser les demandes d'exécution. Requis quand les approbations d'exécution sont activées.
- `channels.telegram.execApprovals.target` : `dm | channel | both` (par défaut : `dm`). `channel` et `both` préservent le sujet Telegram d'origine le cas échéant.
- `channels.telegram.execApprovals.agentFilter` : filtre d'ID d'agent optionnel pour les invites d'approbation transférées.
- `channels.telegram.execApprovals.sessionFilter` : filtre de clé de session optionnel (sous-chaîne ou regex) pour les invites d'approbation transférées.
- `channels.telegram.accounts.<account>.execApprovals` : remplacement par compte pour le routage d'approbation d'exécution Telegram et l'autorisation des approbateurs.
- `channels.telegram.capabilities.inlineButtons` : `off | dm | group | all | allowlist` (par défaut : allowlist).
- `channels.telegram.accounts.<account>.capabilities.inlineButtons` : remplacement par compte.
- `channels.telegram.commands.nativeSkills` : activer/désactiver les commandes de compétences natives Telegram.
- `channels.telegram.replyToMode` : `off | first | all` (par défaut : `off`).
- `channels.telegram.textChunkLimit` : taille du bloc sortant (caractères).
- `channels.telegram.chunkMode` : `length` (par défaut) ou `newline` pour diviser sur les lignes vides (limites de paragraphe) avant le chunking de longueur.
- `channels.telegram.linkPreview` : basculer les aperçus de lien pour les messages sortants (par défaut : true).
- `channels.telegram.streaming` : `off | partial | block | progress` (aperçu de flux en direct ; par défaut : `partial` ; `progress` correspond à `partial` ; `block` est le mode de compatibilité d'aperçu hérité). Le streaming d'aperçu Telegram utilise un seul message d'aperçu qui est édité sur place.
- `channels.telegram.mediaMaxMb` : limite de média Telegram entrante/sortante (MB, par défaut : 100).
- `channels.telegram.retry` : politique de retry pour les assistants d'envoi Telegram (CLI/outils/actions) sur les erreurs API sortantes récupérables (tentatives, minDelayMs, maxDelayMs, jitter).
- `channels.telegram.network.autoSelectFamily` : remplacer Node autoSelectFamily (true=activer, false=désactiver). Activé par défaut sur Node 22+, WSL2 étant désactivé par défaut.
- `channels.telegram.network.dnsResultOrder` : remplacer l'ordre des résultats DNS (`ipv4first` ou `verbatim`). Par défaut `ipv4first` sur Node 22+.
- `channels.telegram.proxy` : URL proxy pour les appels de l'API Bot (SOCKS/HTTP).
- `channels.telegram.webhookUrl` : activer le mode webhook (nécessite `channels.telegram.webhookSecret`).
- `channels.telegram.webhookSecret` : secret webhook (requis quand webhookUrl est défini).
- `channels.telegram.webhookPath` : chemin webhook local (par défaut `/telegram-webhook`).
- `channels.telegram.webhookHost` : hôte de liaison webhook local (par défaut `127.0.0.1`).
- `channels.telegram.webhookPort` : port de liaison webhook local (par défaut `8787`).
- `channels.telegram.actions.reactions` : gating des réactions d'outil Telegram.
- `channels.telegram.actions.sendMessage` : gating des envois de message d'outil Telegram.
- `channels.telegram.actions.deleteMessage` : gating des suppressions de message d'outil Telegram.
- `channels.telegram.actions.sticker` : gating des actions d'autocollant Telegram — envoyer et rechercher (par défaut : false).
- `channels.telegram.reactionNotifications` : `off | own | all` — contrôler quelles réactions déclenchent les événements système (par défaut : `own` quand non défini).
- `channels.telegram.reactionLevel` : `off | ack | minimal | extensive` — contrôler la capacité de réaction de l'agent (par défaut : `minimal` quand non défini).

- [Référence de configuration - Telegram](/gateway/configuration-reference#telegram)

Champs Telegram spécifiques à haut signal :

- démarrage/authentification : `enabled`, `botToken`, `tokenFile`, `accounts.*` (`tokenFile` doit pointer vers un fichier régulier ; les liens symboliques sont rejetés)
- contrôle d'accès : `dmPolicy`, `allowFrom`, `groupPolicy`, `groupAllowFrom`, `groups`, `groups.*.topics.*`, `bindings[]` de haut niveau (`type: "acp"`)
- approbations d'exécution : `execApprovals`, `accounts.*.execApprovals`
- commande/menu : `commands.native`, `commands.nativeSkills`, `customCommands`
- threading/réponses : `replyToMode`
- streaming : `streaming` (aperçu), `blockStreaming`
- formatage/livraison : `textChunkLimit`, `chunkMode`, `linkPreview`, `responsePrefix`
- média/réseau : `mediaMaxMb`, `timeoutSeconds`, `retry`, `network.autoSelectFamily`, `proxy`
- webhook : `webhookUrl`, `webhookSecret`, `webhookPath`, `webhookHost`
- actions/capacités : `capabilities.inlineButtons`, `actions.sendMessage|editMessage|deleteMessage|reactions|sticker`
- réactions : `reactionNotifications`, `reactionLevel`
- écritures/historique : `configWrites`, `historyLimit`, `dmHistoryLimit`, `dms.*.historyLimit`

## Connexes

- [Appairage](/channels/pairing)
- [Routage des canaux](/channels/channel-routing)
- [Routage multi-agent](/concepts/multi-agent)
- [Dépannage](/channels/troubleshooting)
