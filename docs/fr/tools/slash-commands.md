---
summary: "Commandes slash : texte vs natif, configuration et commandes supportées"
read_when:
  - Using or configuring chat commands
  - Debugging command routing or permissions
title: "Commandes slash"
---

# Commandes slash

Les commandes sont gérées par la Gateway. La plupart des commandes doivent être envoyées comme un message **autonome** commençant par `/`.
La commande bash de chat réservée à l'hôte utilise `! <cmd>` (avec `/bash <cmd>` comme alias).

Il existe deux systèmes connexes :

- **Commandes** : messages autonomes `/...`.
- **Directives** : `/think`, `/fast`, `/verbose`, `/reasoning`, `/elevated`, `/exec`, `/model`, `/queue`.
  - Les directives sont supprimées du message avant que le modèle ne le voie.
  - Dans les messages de chat normaux (pas seulement des directives), elles sont traitées comme des « indices en ligne » et ne **persistent pas** les paramètres de session.
  - Dans les messages contenant uniquement des directives (le message ne contient que des directives), elles persistent dans la session et répondent par un accusé de réception.
  - Les directives ne s'appliquent que pour les **expéditeurs autorisés**. Si `commands.allowFrom` est défini, c'est la seule liste d'autorisation utilisée ; sinon l'autorisation provient des listes d'autorisation de canal/appairage plus `commands.useAccessGroups`.
    Les expéditeurs non autorisés voient les directives traitées comme du texte brut.

Il y a aussi quelques **raccourcis en ligne** (expéditeurs autorisés/sur liste blanche uniquement) : `/help`, `/commands`, `/status`, `/whoami` (`/id`).
Ils s'exécutent immédiatement, sont supprimés avant que le modèle ne voie le message, et le texte restant continue dans le flux normal.

## Configuration

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
- `commands.nativeSkills` (par défaut `"auto"`) enregistre les commandes de **compétence** nativement quand supporté.
  - Auto : activé pour Discord/Telegram ; désactivé pour Slack (Slack nécessite de créer une commande slash par compétence).
  - Définissez `channels.discord.commands.nativeSkills`, `channels.telegram.commands.nativeSkills`, ou `channels.slack.commands.nativeSkills` pour remplacer par fournisseur (booléen ou `"auto"`).
- `commands.bash` (par défaut `false`) active `! <cmd>` pour exécuter les commandes shell de l'hôte (`/bash <cmd>` est un alias ; nécessite les listes d'autorisation `tools.elevated`).
- `commands.bashForegroundMs` (par défaut `2000`) contrôle combien de temps bash attend avant de passer en mode arrière-plan (`0` passe immédiatement en arrière-plan).
- `commands.config` (par défaut `false`) active `/config` (lit/écrit `openclaw.json`).
- `commands.debug` (par défaut `false`) active `/debug` (remplacements au moment de l'exécution uniquement).
- `commands.allowFrom` (optionnel) définit une liste d'autorisation par fournisseur pour l'autorisation des commandes. Quand configuré, c'est la seule source d'autorisation pour les commandes et directives (les listes d'autorisation de canal/appairage et `commands.useAccessGroups` sont ignorées). Utilisez `"*"` pour une valeur par défaut globale ; les clés spécifiques au fournisseur la remplacent.
- `commands.useAccessGroups` (par défaut `true`) applique les listes d'autorisation/politiques pour les commandes quand `commands.allowFrom` n'est pas défini.

## Liste des commandes

Texte + natif (quand activé) :

- `/help`
- `/commands`
- `/skill <name> [input]` (exécuter une compétence par nom)
- `/status` (afficher l'état actuel ; inclut l'utilisation/quota du fournisseur pour le fournisseur de modèle actuel quand disponible)
- `/allowlist` (lister/ajouter/supprimer les entrées de liste d'autorisation)
- `/approve <id> allow-once|allow-always|deny` (résoudre les invites d'approbation exec)
- `/context [list|detail|json]` (expliquer « contexte » ; `detail` affiche la taille par fichier + par outil + par compétence + invite système)
- `/export-session [path]` (alias : `/export`) (exporter la session actuelle en HTML avec l'invite système complète)
- `/whoami` (afficher votre ID d'expéditeur ; alias : `/id`)
- `/session idle <duration|off>` (gérer le dé-focus automatique d'inactivité pour les liaisons de fil focalisées)
- `/session max-age <duration|off>` (gérer le dé-focus automatique d'âge maximal pour les liaisons de fil focalisées)
- `/subagents list|kill|log|info|send|steer|spawn` (inspecter, contrôler ou générer des exécutions de sous-agent pour la session actuelle)
- `/acp spawn|cancel|steer|close|status|set-mode|set|cwd|permissions|timeout|model|reset-options|doctor|install|sessions` (inspecter et contrôler les sessions d'exécution ACP)
- `/agents` (lister les agents liés au fil pour cette session)
- `/focus <target>` (Discord : lier ce fil, ou un nouveau fil, à une cible de session/sous-agent)
- `/unfocus` (Discord : supprimer la liaison de fil actuelle)
- `/kill <id|#|all>` (abandonner immédiatement un ou tous les sous-agents en cours d'exécution pour cette session ; pas de message de confirmation)
- `/steer <id|#> <message>` (diriger un sous-agent en cours d'exécution immédiatement : en cours d'exécution si possible, sinon abandonner le travail actuel et redémarrer sur le message de direction)
- `/tell <id|#> <message>` (alias pour `/steer`)
- `/config show|get|set|unset` (persister la configuration sur le disque, propriétaire uniquement ; nécessite `commands.config: true`)
- `/debug show|set|unset|reset` (remplacements au moment de l'exécution, propriétaire uniquement ; nécessite `commands.debug: true`)
- `/usage off|tokens|full|cost` (pied de page d'utilisation par réponse ou résumé de coût local)
- `/tts off|always|inbound|tagged|status|provider|limit|summary|audio` (contrôler TTS ; voir [/tts](/tts))
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
- `/fast status|on|off` (omettre l'argument affiche l'état du mode rapide effectif actuel)
- `/verbose on|full|off` (alias : `/v`)
- `/reasoning on|off|stream` (alias : `/reason` ; quand activé, envoie un message séparé préfixé `Reasoning:` ; `stream` = Telegram uniquement)
- `/elevated on|off|ask|full` (alias : `/elev` ; `full` ignore les approbations exec)
- `/exec host=<sandbox|gateway|node> security=<deny|allowlist|full> ask=<off|on-miss|always> node=<id>` (envoyer `/exec` pour afficher le courant)
- `/model <name>` (alias : `/models` ; ou `/<alias>` de `agents.defaults.models.*.alias`)
- `/queue <mode>` (plus d'options comme `debounce:2s cap:25 drop:summarize` ; envoyer `/queue` pour voir les paramètres actuels)
- `/bash <command>` (hôte uniquement ; alias pour `! <command>` ; nécessite `commands.bash: true` + listes d'autorisation `tools.elevated`)

Texte uniquement :

- `/compact [instructions]` (voir [/concepts/compaction](/concepts/compaction))
- `! <command>` (hôte uniquement ; un à la fois ; utiliser `!poll` + `!stop` pour les tâches longues)
- `!poll` (vérifier la sortie / l'état ; accepte `sessionId` optionnel ; `/bash poll` fonctionne aussi)
- `!stop` (arrêter la tâche bash en cours d'exécution ; accepte `sessionId` optionnel ; `/bash stop` fonctionne aussi)

Notes :

- Les commandes acceptent un `:` optionnel entre la commande et les arguments (par ex. `/think: high`, `/send: on`, `/help:`).
- `/new <model>` accepte un alias de modèle, `provider/model`, ou un nom de fournisseur (correspondance floue) ; si aucune correspondance, le texte est traité comme le corps du message.
- Pour une ventilation complète de l'utilisation du fournisseur, utilisez `openclaw status --usage`.
- `/allowlist add|remove` nécessite `commands.config=true` et respecte `configWrites` du canal.
- Dans les canaux multi-comptes, `/allowlist --account <id>` ciblé par configuration et `/config set channels.<provider>.accounts.<id>...` respectent également `configWrites` du compte cible.
- `/usage` contrôle le pied de page d'utilisation par réponse ; `/usage cost` imprime un résumé de coût local à partir des journaux de session OpenClaw.
- `/restart` est activé par défaut ; définissez `commands.restart: false` pour le désactiver.
- Commande native Discord uniquement : `/vc join|leave|status` contrôle les canaux vocaux (nécessite `channels.discord.voice` et les commandes natives ; non disponible en texte).
- Les commandes de liaison de fil Discord (`/focus`, `/unfocus`, `/agents`, `/session idle`, `/session max-age`) nécessitent que les liaisons de fil effectives soient activées (`session.threadBindings.enabled` et/ou `channels.discord.threadBindings.enabled`).
- Référence de commande ACP et comportement au moment de l'exécution : [ACP Agents](/tools/acp-agents).
- `/verbose` est destiné au débogage et à une visibilité supplémentaire ; gardez-le **désactivé** en utilisation normale.
- `/fast on|off` persiste un remplacement de session. Utilisez l'option `inherit` de l'interface utilisateur Sessions pour l'effacer et revenir aux valeurs par défaut de configuration.
- Les résumés d'échec d'outil sont toujours affichés quand pertinent, mais le texte d'échec détaillé n'est inclus que quand `/verbose` est `on` ou `full`.
- `/reasoning` (et `/verbose`) sont risqués dans les paramètres de groupe : ils peuvent révéler le raisonnement interne ou la sortie d'outil que vous n'aviez pas l'intention d'exposer. Préférez les laisser désactivés, surtout dans les chats de groupe.
- **Chemin rapide :** les messages contenant uniquement des commandes des expéditeurs autorisés sont traités immédiatement (contourner la file d'attente + modèle).
- **Gating de mention de groupe :** les messages contenant uniquement des commandes des expéditeurs autorisés contournent les exigences de mention.
- **Raccourcis en ligne (expéditeurs autorisés uniquement) :** certaines commandes fonctionnent également quand elles sont intégrées dans un message normal et sont supprimées avant que le modèle ne voie le texte restant.
  - Exemple : `hey /status` déclenche une réponse de statut, et le texte restant continue dans le flux normal.
- Actuellement : `/help`, `/commands`, `/status`, `/whoami` (`/id`).
- Les messages contenant uniquement des commandes non autorisées sont silencieusement ignorés, et les jetons `/...` en ligne sont traités comme du texte brut.
- **Commandes de compétence :** les compétences `user-invocable` sont exposées comme des commandes slash. Les noms sont assainis en `a-z0-9_` (max 32 caractères) ; les collisions obtiennent des suffixes numériques (par ex. `_2`).
  - `/skill <name> [input]` exécute une compétence par nom (utile quand les limites de commandes natives empêchent les commandes par compétence).
  - Par défaut, les commandes de compétence sont transmises au modèle comme une demande normale.
  - Les compétences peuvent optionnellement déclarer `command-dispatch: tool` pour router la commande directement vers un outil (déterministe, pas de modèle).
  - Exemple : `/prose` (plugin OpenProse) — voir [OpenProse](/prose).
- **Arguments de commande native :** Discord utilise l'autocomplétion pour les options dynamiques (et les menus de bou
