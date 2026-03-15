---
summary: "Slash commands: text vs native, config, and supported commands"
read_when:
  - Using or configuring chat commands
  - Debugging command routing or permissions
title: "Slash Commands"
---

# Commandes slash

Les commandes sont gérées par la Gateway. La plupart des commandes doivent être envoyées en tant que message **autonome** commençant par `/`.
La commande bash de chat réservée à l'hôte utilise `! <cmd>` (avec `/bash <cmd>` comme alias).

Il existe deux systèmes connexes :

- **Commandes** : messages autonomes `/...`.
- **Directives** : `/think`, `/fast`, `/verbose`, `/reasoning`, `/elevated`, `/exec`, `/model`, `/queue`.
  - Les directives sont supprimées du message avant que le modèle ne le voie.
  - Dans les messages de chat normaux (pas seulement des directives), elles sont traitées comme des « indices intégrés » et ne **persistent pas** les paramètres de session.
  - Dans les messages contenant uniquement des directives (le message ne contient que des directives), elles persistent à la session et répondent par un accusé de réception.
  - Les directives ne s'appliquent que pour les **expéditeurs autorisés**. Si `commands.allowFrom` est défini, c'est la seule liste d'autorisation utilisée ; sinon, l'autorisation provient des listes d'autorisation de canal/appairage plus `commands.useAccessGroups`.
    Les expéditeurs non autorisés voient les directives traitées comme du texte brut.

Il y a aussi quelques **raccourcis intégrés** (expéditeurs autorisés/sur liste blanche uniquement) : `/help`, `/commands`, `/status`, `/whoami` (`/id`).
Ils s'exécutent immédiatement, sont supprimés avant que le modèle ne voie le message, et le texte restant continue par le flux normal.

## Config

```json5
{
  commands: {
    native: "auto",
    nativeSkills: "auto",
    text: true,
    bash: false,
    bashForegroundMs: 2000,
    config: false,
    debug: false,
    restart: false,
    allowFrom: {
      "*": ["user1"],
      discord: ["user:123"],
    },
    useAccessGroups: true,
  },
}
```

- `commands.text` (par défaut `true`) active l'analyse de `/...` dans les messages de chat.
  - Sur les surfaces sans commandes natives (WhatsApp/WebChat/Signal/iMessage/Google Chat/MS Teams), les commandes texte fonctionnent toujours même si vous définissez ceci sur `false`.
- `commands.native` (par défaut `"auto"`) enregistre les commandes natives.
  - Auto : activé pour Discord/Telegram ; désactivé pour Slack (jusqu'à ce que vous ajoutiez des commandes slash) ; ignoré pour les fournisseurs sans support natif.
  - Définissez `channels.discord.commands.native`, `channels.telegram.commands.native`, ou `channels.slack.commands.native` pour remplacer par fournisseur (booléen ou `"auto"`).
  - `false` efface les commandes précédemment enregistrées sur Discord/Telegram au démarrage. Les commandes Slack sont gérées dans l'application Slack et ne sont pas supprimées automatiquement.
- `commands.nativeSkills` (par défaut `"auto"`) enregistre les commandes **skill** nativement lorsqu'elles sont supportées.
  - Auto : activé pour Discord/Telegram ; désactivé pour Slack (Slack nécessite de créer une commande slash par skill).
  - Définissez `channels.discord.commands.nativeSkills`, `channels.telegram.commands.nativeSkills`, ou `channels.slack.commands.nativeSkills` pour remplacer par fournisseur (booléen ou `"auto"`).
- `commands.bash` (par défaut `false`) active `! <cmd>` pour exécuter les commandes shell de l'hôte (`/bash <cmd>` est un alias ; nécessite les listes d'autorisation `tools.elevated`).
- `commands.bashForegroundMs` (par défaut `2000`) contrôle combien de temps bash attend avant de passer en mode arrière-plan (`0` passe immédiatement en arrière-plan).
- `commands.config` (par défaut `false`) active `/config` (lit/écrit `openclaw.json`).
- `commands.debug` (par défaut `false`) active `/debug` (remplacements au runtime uniquement).
- `commands.allowFrom` (optionnel) définit une liste d'autorisation par fournisseur pour l'autorisation des commandes. Lorsqu'elle est configurée, c'est la
  seule source d'autorisation pour les commandes et directives (les listes d'autorisation de canal/appairage et `commands.useAccessGroups`
  sont ignorées). Utilisez `"*"` pour une valeur par défaut globale ; les clés spécifiques au fournisseur la remplacent.
- `commands.useAccessGroups` (par défaut `true`) applique les listes d'autorisation/politiques pour les commandes lorsque `commands.allowFrom` n'est pas défini.

## Liste des commandes

Texte + natif (lorsqu'activé) :

- `/help`
- `/commands`
- `/skill <name> [input]` (exécuter une skill par nom)
- `/status` (afficher l'état actuel ; inclut l'utilisation/quota du fournisseur pour le fournisseur de modèle actuel lorsqu'il est disponible)
- `/allowlist` (lister/ajouter/supprimer les entrées de liste d'autorisation)
- `/approve <id> allow-once|allow-always|deny` (résoudre les invites d'approbation exec)
- `/context [list|detail|json]` (expliquer « context » ; `detail` affiche la taille par fichier + par outil + par skill + invite système)
- `/btw <question>` (poser une question latérale éphémère sur la session actuelle sans modifier le contexte de session futur ; voir [/tools/btw](/fr/tools/btw))
- `/export-session [path]` (alias : `/export`) (exporter la session actuelle en HTML avec l'invite système complète)
- `/whoami` (afficher votre id d'expéditeur ; alias : `/id`)
- `/session idle <duration|off>` (gérer l'auto-unfocus d'inactivité pour les liaisons de thread focalisées)
- `/session max-age <duration|off>` (gérer l'auto-unfocus d'âge maximum dur pour les liaisons de thread focalisées)
- `/subagents list|kill|log|info|send|steer|spawn` (inspecter, contrôler ou générer des exécutions de sous-agent pour la session actuelle)
- `/acp spawn|cancel|steer|close|status|set-mode|set|cwd|permissions|timeout|model|reset-options|doctor|install|sessions` (inspecter et contrôler les sessions de runtime ACP)
- `/agents` (lister les agents liés au thread pour cette session)
- `/focus <target>` (Discord : lier ce thread, ou un nouveau thread, à une cible de session/sous-agent)
- `/unfocus` (Discord : supprimer la liaison de thread actuelle)
- `/kill <id|#|all>` (abandonner immédiatement un ou tous les sous-agents en cours d'exécution pour cette session ; pas de message de confirmation)
- `/steer <id|#> <message>` (diriger un sous-agent en cours d'exécution immédiatement : en cours d'exécution si possible, sinon abandonner le travail actuel et redémarrer sur le message de direction)
- `/tell <id|#> <message>` (alias pour `/steer`)
- `/config show|get|set|unset` (persister la config sur le disque, propriétaire uniquement ; nécessite `commands.config: true`)
- `/debug show|set|unset|reset` (remplacements au runtime, propriétaire uniquement ; nécessite `commands.debug: true`)
- `/usage off|tokens|full|cost` (pied de page d'utilisation par réponse ou résumé de coût local)
- `/tts off|always|inbound|tagged|status|provider|limit|summary|audio` (contrôler TTS ; voir [/tts](/fr/tts))
  - Discord : la commande native est `/voice` (Discord réserve `/tts`) ; le texte `/tts` fonctionne toujours.
- `/stop`
- `/restart`
- `/dock-telegram` (alias : `/dock_telegram`) (basculer les réponses vers Telegram)
- `/dock-discord` (alias : `/dock_discord`) (basculer les réponses vers Discord)
- `/dock-slack` (alias : `/dock_slack`) (basculer les réponses vers Slack)
- `/activation mention|always` (groupes uniquement)
- `/send on|off|inherit` (propriétaire uniquement)
- `/reset` ou `/new [model]` (indice de modèle optionnel ; le reste est transmis)
- `/think <off|minimal|low|medium|high|xhigh>` (choix dynamiques par modèle/fournisseur ; alias : `/thinking`, `/t`)
- `/fast status|on|off` (l'omission de l'argument affiche l'état du mode rapide effectif actuel)
- `/verbose on|full|off` (alias : `/v`)
- `/reasoning on|off|stream` (alias : `/reason` ; lorsqu'il est activé, envoie un message séparé préfixé `Reasoning:` ; `stream` = brouillon Telegram uniquement)
- `/elevated on|off|ask|full` (alias : `/elev` ; `full` ignore les approbations exec)
- `/exec host=<sandbox|gateway|node> security=<deny|allowlist|full> ask=<off|on-miss|always> node=<id>` (envoyer `/exec` pour afficher le courant)
- `/model <name>` (alias : `/models` ; ou `/<alias>` de `agents.defaults.models.*.alias`)
- `/queue <mode>` (plus des options comme `debounce:2s cap:25 drop:summarize` ; envoyer `/queue` pour voir les paramètres actuels)
- `/bash <command>` (hôte uniquement ; alias pour `! <command>` ; nécessite `commands.bash: true` + listes d'autorisation `tools.elevated`)

Texte uniquement :

- `/compact [instructions]` (voir [/concepts/compaction](/fr/concepts/compaction))
- `! <command>` (hôte uniquement ; un à la fois ; utiliser `!poll` + `!stop` pour les travaux de longue durée)
- `!poll` (vérifier la sortie / l'état ; accepte `sessionId` optionnel ; `/bash poll` fonctionne aussi)
- `!stop` (arrêter le travail bash en cours d'exécution ; accepte `sessionId` optionnel ; `/bash stop` fonctionne aussi)

Notes :

- Les commandes acceptent un `:` optionnel entre la commande et les arguments (par exemple `/think: high`, `/send: on`, `/help:`).
- `/new <model>` accepte un alias de modèle, `provider/model`, ou un nom de fournisseur (correspondance floue) ; si aucune correspondance, le texte est traité comme le corps du message.
- Pour une ventilation complète de l'utilisation du fournisseur, utilisez `openclaw status --usage`.
- `/allowlist add|remove` nécessite `commands.config=true` et respecte `configWrites` du canal.
- Dans les canaux multi-comptes, `/allowlist --account <id>` ciblé par config et `/config set channels.<provider>.accounts.<id>...` respectent également `configWrites` du compte cible.
- `/usage` contrôle le pied de page d'utilisation par réponse ; `/usage cost` imprime un résumé de coût local à partir des journaux de session OpenClaw.
- `/restart` est activé par défaut ; définissez `commands.restart: false` pour le désactiver.
- Commande native Discord uniquement : `/vc join|leave|status` contrôle les canaux vocaux (nécessite `channels.discord.voice` et les commandes natives ; non disponible en tant que texte).
- Les commandes de liaison de thread Discord (`/focus`, `/unfocus`, `/agents`, `/session idle`, `/session max-age`) nécessitent que les liaisons de thread effectives soient activées (`session.threadBindings.enabled` et/ou `channels.discord.threadBindings.enabled`).
- Référence de commande ACP et comportement au runtime : [ACP Agents](/fr/tools/acp-agents).
- `/verbose` est destiné au débogage et à une visibilité supplémentaire ; gardez-le **désactivé** en utilisation normale.
- `/fast on|off` persiste un remplacement de session. Utilisez l'option `inherit` de l'interface utilisateur Sessions pour l'effacer et revenir aux valeurs par défaut de la config.
- Les résumés d'échec d'outil sont toujours affichés lorsqu'ils sont pertinents, mais le texte d'échec détaillé n'est inclus que lorsque `/verbose` est `on` ou `full`.
- `/reasoning` (et `/verbose`) sont risqués dans les paramètres de groupe : ils peuvent révéler le raisonnement interne ou la sortie d'outil que vous n'aviez pas l'intention d'exposer. Préférez les laisser désactivés, en particulier dans les chats de groupe.
- **Chemin rapide :** les messages contenant uniquement des commandes des expéditeurs autorisés sont traités immédiatement (contourner la file d'attente + modèle).
- **Gating de mention de groupe :** les messages contenant uniquement des commandes des expéditeurs autorisés contournent les exigences de mention.
- **Raccourcis intégrés (expéditeurs autorisés uniquement) :** certaines commandes fonctionnent également lorsqu'elles sont intégrées dans un message normal et sont supprimées avant que le modèle ne voie le texte restant.
  - Exemple : `hey /status` déclenche une réponse de statut, et le texte restant continue par le flux normal.
- Actuellement : `/help`, `/commands`, `/status`, `/whoami` (`/id`).
- Les messages contenant uniquement des commandes non autorisées sont silencieusement ignorés, et les jetons `/...` intégrés sont traités comme du texte brut.
- **Commandes de skill :** les skills `user-invocable` sont exposées en tant que commandes slash. Les noms sont assainis en `a-z0-9_` (max 32 caractères) ; les collisions obtiennent des suffixes numériques (par exemple `_2`).
  - `/skill <name> [input]` exécute une skill par nom (utile lorsque les limites de commandes natives empêchent les commandes par skill).
  - Par défaut, les commandes de skill sont transmises au modèle en tant que demande normale.
  - Les skills peuvent éventuellement déclarer `command-dispatch: tool` pour router la commande directement vers un outil (déterministe, pas de modèle).
  - Exemple : `/prose` (plugin OpenProse) — voir [OpenProse](/fr/prose).
- **Arguments de commande native :** Discord utilise l'autocomplétion pour les options dynamiques (et les menus de boutons lorsque vous omettez les arguments requis). Telegram et Slack affichent un menu de boutons lorsqu'une commande supporte des choix et que vous omettez l'argument.

## Surfaces d'utilisation (ce qui s'affiche où)

- **Utilisation/quota du fournisseur** (exemple : « Claude 80% restant ») s'affiche dans `/status` pour le fournisseur de modèle actuel lorsque le suivi d'utilisation est activé.
- **Jetons/coût par réponse** est contrôlé par `/usage off|tokens|full` (ajouté aux réponses normales).
- `/model status` concerne les **modèles/authentification/points de terminaison**, pas l'utilisation.

## Sélection de modèle (`/model`)

`/model` est implémenté en tant que directive.

Exemples :

```
/model
/model list
/model 3
/model openai/gpt-5.2
/model opus@anthropic:default
/model status
```

Notes :

- `/model` et `/model list` affichent un sélecteur compact et numéroté (famille de modèles + fournisseurs disponibles).
- Sur Discord, `/model` et `/models` ouvrent un sélecteur interactif avec des listes déroulantes de fournisseur et de modèle plus une étape Submit.
- `/model <#>` sélectionne à partir de ce sélecteur (et préfère le fournisseur actuel lorsque possible).
- `/model status` affiche la vue détaillée, y compris le point de terminaison du fournisseur configuré (`baseUrl`) et le mode API (`api`) lorsqu'ils sont disponibles.

## Remplacements de débogage

`/debug` vous permet de définir des remplacements de configuration **au moment de l'exécution uniquement** (en mémoire, pas sur disque). Réservé au propriétaire. Désactivé par défaut ; activez avec `commands.debug: true`.

Exemples :

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug set channels.whatsapp.allowFrom=["+1555","+4477"]
/debug unset messages.responsePrefix
/debug reset
```

Remarques :

- Les remplacements s'appliquent immédiatement aux nouvelles lectures de configuration, mais n'**écrivent pas** dans `openclaw.json`.
- Utilisez `/debug reset` pour effacer tous les remplacements et revenir à la configuration sur disque.

## Mises à jour de configuration

`/config` écrit dans votre configuration sur disque (`openclaw.json`). Réservé au propriétaire. Désactivé par défaut ; activez avec `commands.config: true`.

Exemples :

```
/config show
/config show messages.responsePrefix
/config get messages.responsePrefix
/config set messages.responsePrefix="[openclaw]"
/config unset messages.responsePrefix
```

Remarques :

- La configuration est validée avant l'écriture ; les modifications invalides sont rejetées.
- Les mises à jour `/config` persistent après les redémarrages.

## Notes de surface

- **Les commandes texte** s'exécutent dans la session de chat normale (les DM partagent `main`, les groupes ont leur propre session).
- **Les commandes natives** utilisent des sessions isolées :
  - Discord : `agent:<agentId>:discord:slash:<userId>`
  - Slack : `agent:<agentId>:slack:slash:<userId>` (préfixe configurable via `channels.slack.slashCommand.sessionPrefix`)
  - Telegram : `telegram:slash:<userId>` (cible la session de chat via `CommandTargetSessionKey`)
- **`/stop`** cible la session de chat active pour pouvoir interrompre l'exécution en cours.
- **Slack :** `channels.slack.slashCommand` est toujours supporté pour une seule commande de style `/openclaw`. Si vous activez `commands.native`, vous devez créer une commande slash Slack par commande intégrée (mêmes noms que `/help`). Les menus d'arguments de commande pour Slack sont livrés sous forme de boutons Block Kit éphémères.
  - Exception Slack native : enregistrez `/agentstatus` (pas `/status`) car Slack réserve `/status`. Le texte `/status` fonctionne toujours dans les messages Slack.

## Questions annexes BTW

`/btw` est une **question annexe** rapide sur la session actuelle.

Contrairement au chat normal :

- elle utilise la session actuelle comme contexte de fond,
- elle s'exécute comme un appel unique **sans outils** séparé,
- elle ne modifie pas le contexte de session futur,
- elle n'est pas écrite dans l'historique des transcriptions,
- elle est livrée comme un résultat annexe en direct au lieu d'un message assistant normal.

Cela rend `/btw` utile quand vous voulez une clarification temporaire tandis que la tâche principale continue.

Exemple :

```text
/btw what are we doing right now?
```

Consultez [BTW Side Questions](/fr/tools/btw) pour les détails complets du comportement et de l'expérience utilisateur client.
