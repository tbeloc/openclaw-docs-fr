---
read_when:
  - Utiliser ou configurer les commandes de chat
  - Déboguer le routage des commandes ou les permissions
summary: Commandes slash : texte vs natif, configuration et commandes supportées
title: Commandes slash
x-i18n:
  generated_at: "2026-02-03T10:12:40Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: ca0deebf89518e8c62828fbb9bf4621c5fff8ab86ccb22e37da61a28f9a7886a
  source_path: tools/slash-commands.md
  workflow: 15
---

# Commandes slash

Les commandes sont traitées par la passerelle Gateway. La plupart des commandes doivent être envoyées en tant que messages **indépendants** commençant par `/`.
Seules les commandes bash du host utilisent `! <cmd>` (`/bash <cmd>` est un alias).

Il y a deux systèmes connexes :

- **Commandes** : messages indépendants `/...`.
- **Directives** : `/think`, `/verbose`, `/reasoning`, `/elevated`, `/exec`, `/model`, `/queue`.
  - Les directives sont supprimées avant que le modèle ne voie le message.
  - Dans les messages de chat normaux (pas seulement des messages de directive), elles sont traitées comme des « invites en ligne » et **ne** persistent **pas** les paramètres de session.
  - Dans les messages contenant uniquement des directives (le message ne contient que des directives), elles persistent dans la session et répondent avec une confirmation.
  - Les directives ne fonctionnent que pour les **expéditeurs autorisés** (liste blanche de canal/appairage plus `commands.useAccessGroups`).
    Les directives des expéditeurs non autorisés sont traitées comme du texte brut.

Il y a aussi des **raccourcis en ligne** (liste blanche/expéditeurs autorisés uniquement) : `/help`, `/commands`, `/status`, `/whoami` (`/id`).
Ils s'exécutent immédiatement, sont supprimés avant que le modèle ne voie le message, et le texte restant continue via le processus normal.

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
    useAccessGroups: true,
  },
}
```

- `commands.text` (par défaut `true`) active l'analyse des `/...` dans les messages de chat.
  - Sur les plateformes sans commandes natives (WhatsApp/WebChat/Signal/iMessage/Google Chat/MS Teams), les commandes texte fonctionnent même si vous définissez ceci sur `false`.
- `commands.native` (par défaut `"auto"`) enregistre les commandes natives.
  - Auto : activé sur Discord/Telegram ; désactivé sur Slack (jusqu'à ce que vous ajoutiez des commandes slash) ; ignoré sur les fournisseurs qui ne supportent pas les commandes natives.
  - Définissez `channels.discord.commands.native`, `channels.telegram.commands.native` ou `channels.slack.commands.native` pour remplacer par fournisseur (booléen ou `"auto"`).
  - `false` efface les commandes précédemment enregistrées sur Discord/Telegram au démarrage. Les commandes Slack sont gérées dans l'application Slack et ne sont pas supprimées automatiquement.
- `commands.nativeSkills` (par défaut `"auto"`) enregistre nativement les commandes **Skill** lorsqu'elles sont supportées.
  - Auto : activé sur Discord/Telegram ; désactivé sur Slack (Slack nécessite de créer une commande slash pour chaque Skill).
  - Définissez `channels.discord.commands.nativeSkills`, `channels.telegram.commands.nativeSkills` ou `channels.slack.commands.nativeSkills` pour remplacer par fournisseur (booléen ou `"auto"`).
- `commands.bash` (par défaut `false`) active `! <cmd>` pour exécuter les commandes shell du host (`/bash <cmd>` est un alias ; nécessite une liste blanche `tools.elevated`).
- `commands.bashForegroundMs` (par défaut `2000`) contrôle combien de temps attendre avant de basculer bash en mode arrière-plan (`0` pour arrière-plan immédiat).
- `commands.config` (par défaut `false`) active `/config` (lecture/écriture de `openclaw.json`).
- `commands.debug` (par défaut `false`) active `/debug` (remplacements d'exécution uniquement).
- `commands.useAccessGroups` (par défaut `true`) applique la liste blanche/les politiques aux commandes.

## Liste des commandes

Texte + natif (lorsqu'activé) :

- `/help`
- `/commands`
- `/skill <name> [input]` (exécuter une Skill par nom)
- `/status` (afficher l'état actuel ; inclut l'utilisation/quota du fournisseur du fournisseur de modèle actuel lorsqu'il est disponible)
- `/allowlist` (lister/ajouter/supprimer les entrées de la liste blanche)
- `/approve <id> allow-once|allow-always|deny` (résoudre les invites d'approbation exec)
- `/context [list|detail|json]` (expliquer le « contexte » ; `detail` affiche la taille de chaque fichier + chaque outil + chaque Skill + invite système)
- `/whoami` (afficher votre ID d'expéditeur ; alias : `/id`)
- `/subagents list|kill|log|info|send|steer|spawn` (vérifier, contrôler ou créer les exécutions de sous-agents de la session actuelle)
- `/config show|get|set|unset` (persister la configuration sur le disque, propriétaire uniquement ; nécessite `commands.config: true`)
- `/debug show|set|unset|reset` (remplacements d'exécution, propriétaire uniquement ; nécessite `commands.debug: true`)
- `/usage off|tokens|full|cost` (pied de page d'utilisation par réponse ou résumé de coût local)
- `/tts off|always|inbound|tagged|status|provider|limit|summary|audio` (contrôler TTS ; voir [/tts](/tts))
  - Discord : la commande native est `/voice` (Discord a réservé `/tts`) ; le texte `/tts` fonctionne toujours.
- `/stop`
- `/restart`
- `/dock-telegram` (alias : `/dock_telegram`) (basculer les réponses vers Telegram)
- `/dock-discord` (alias : `/dock_discord`) (basculer les réponses vers Discord)
- `/dock-slack` (alias : `/dock_slack`) (basculer les réponses vers Slack)
- `/activation mention|always` (groupes uniquement)
- `/send on|off|inherit` (propriétaire uniquement)
- `/reset` ou `/new [model]` (modèle optionnel ; le reste est transmis)
- `/think <off|minimal|low|medium|high|xhigh>` (sélection dynamique par modèle/fournisseur ; alias : `/thinking`, `/t`)
- `/verbose on|full|off` (alias : `/v`)
- `/reasoning on|off|stream` (alias : `/reason` ; lorsqu'activé, envoie un message séparé avec le préfixe `Reasoning:` ; `stream` = brouillons Telegram uniquement)
- `/elevated on|off|ask|full` (alias : `/elev` ; `full` ignore l'approbation exec)
- `/exec host=<sandbox|gateway|node> security=<deny|allowlist|full> ask=<off|on-miss|always> node=<id>` (envoyer `/exec` pour afficher les paramètres actuels)
- `/model <name>` (alias : `/models` ; ou `/<alias>` depuis `agents.defaults.models.*.alias`)
- `/queue <mode>` (plus les options comme `debounce:2s cap:25 drop:summarize` ; envoyer `/queue` pour voir les paramètres actuels)
- `/bash <command>` (host uniquement ; alias de `! <command>` ; nécessite `commands.bash: true` + liste blanche `tools.elevated`)

Texte uniquement :

- `/compact [instructions]` (voir [/concepts/compaction](/concepts/compaction))
- `! <command>` (host uniquement ; un à la fois ; utilisez `!poll` + `!stop` pour les tâches longues)
- `!poll` (vérifier la sortie/l'état ; accepte un `sessionId` optionnel ; `/bash poll` est aussi disponible)
- `!stop` (arrêter la tâche bash en cours d'exécution ; accepte un `sessionId` optionnel ; `/bash stop` est aussi disponible)

Remarques :

- Les commandes acceptent un `:` optionnel entre la commande et les arguments (par exemple `/think: high`, `/send: on`, `/help:`).
- `/new <model>` accepte un alias de modèle, `provider/model` ou un nom de fournisseur (correspondance floue) ; si aucune correspondance, le texte est traité comme le corps du message.
- Pour obtenir une ventilation complète de l'utilisation du fournisseur, utilisez `openclaw status --usage`.
- `/allowlist add|remove` nécessite `commands.config=true` et respecte le canal `configWrites`.
- `/usage` contrôle le pied de page d'utilisation par réponse ; `/usage cost` imprime un résumé de coût local à partir du journal de session OpenClaw.
- `/restart` est désactivé par défaut ; définissez `commands.restart: true` pour l'activer.
- `/verbose` est pour le débogage et la visibilité supplémentaire ; gardez-le **désactivé** lors d'une utilisation normale.
- `/reasoning` (et `/verbose`) sont risqués dans les paramètres de groupe : ils peuvent exposer le raisonnement interne ou la sortie d'outils que vous n'aviez pas l'intention de rendre publics. Il est préférable de les garder désactivés, surtout dans les chats de groupe.
- **Chemin rapide :** les messages contenant uniquement des commandes des expéditeurs de la liste blanche sont traités immédiatement (contournement de la file d'attente + modèle).
- **Contrôle de mention de groupe :** les messages contenant uniquement des commandes des expéditeurs de la liste blanche contournent les exigences de mention.
- **Raccourcis en ligne (expéditeurs de liste blanche uniquement) :** certaines commandes fonctionnent aussi lorsqu'elles sont intégrées dans des messages normaux et sont supprimées avant que le modèle ne voie le texte restant.
  - Exemple : `hey /status` déclenche une réponse de statut, le texte restant continue via le processus normal.
- Actuellement : `/help`, `/commands`, `/status`, `/whoami` (`/id`).
- Les messages contenant uniquement des commandes non autorisés sont silencieusement ignorés, les jetons `/...` en ligne sont traités comme du texte brut.
- **Commandes Skill :** les Skills `user-invocable` sont exposées en tant que commandes slash. Les noms sont nettoyés en `a-z0-9_` (max 32 caractères) ; les conflits reçoivent des suffixes numériques (par exemple `_2`).
  - `/skill <name> [input]` exécute une Skill par nom (utile lorsque les limites de commandes natives empêchent une commande par Skill).
  - Par défaut, les commandes Skill sont transmises au modèle en tant que requête normale.
  - Les Skills peuvent optionnellement déclarer `command-dispatch: tool` pour router la commande directement vers l'outil (déterministe, sans modèle).
  - Exemple : `/prose` (plugin OpenProse) — voir [OpenProse](/prose).
- **Paramètres de commande native :** Discord utilise l'autocomplétion pour les options dynamiques (et un menu de boutons lorsque vous omettez les paramètres requis). Telegram et Slack affichent un menu de boutons lorsque la commande supporte les choix et que vous omettez les paramètres.

## Affichage de l'utilisation (ce qui s'affiche où)

- **Utilisation/quota du fournisseur** (exemple : « Claude 80% left ») s'affiche dans `/status` lorsque le suivi de l'utilisation est activé, pour le fournisseur de modèle actuel.
- **Jetons/coût par réponse** contrôlés par `/usage off|tokens|full` (ajoutés aux réponses normales).
- `/model status` concerne le **modèle/authentification/endpoint**, pas l'utilisation.

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

Remarques :

- `/model` et `/model list` affichent un sélecteur numéroté compact (familles de modèles + fournisseurs disponibles).
- `/model <#>` sélectionne à partir de ce sélecteur (et préfère le fournisseur actuel si possible).
- `/model status` affiche une vue détaillée, y compris les endpoints du fournisseur configurés lorsqu'ils sont disponibles (`baseUrl`) et le schéma API (`api`).

## Remplacements de débogage

`/debug` vous permet de définir des remplacements de configuration **d'exécution uniquement** (mémoire, n'écrit pas sur le disque). Propriétaire uniquement. Désactivé par défaut ; utilisez `commands.debug: true` pour l'activer.

Exemples :

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug set channels.whatsapp.allowFrom=["+1555","+4477"]
/debug unset messages.responsePrefix
/debug reset
```

Remarques :

- Les remplacements sont appliqués immédiatement aux nouvelles lectures de configuration, mais **ne** s'écrivent **pas** dans `openclaw.json`.
- Utilisez `/debug reset` pour effacer tous les remplacements et revenir à la configuration sur le disque.

## Mises à jour de configuration

`/config` écrit votre configuration sur le disque (`openclaw.json`). Propriétaire uniquement. Désactivé par défaut ; utilisez `commands.config: true` pour l'activer.

Exemples :

```
/config show
/config show messages.responsePrefix
/config get messages.responsePrefix
/config set messages.responsePrefix="[openclaw]"
/config unset messages.responsePrefix
```

Remarques :

- La configuration est validée avant d'être écrite ; les modifications invalides sont rejetées.
- Les mises à jour `/config` persistent après un redémarrage.

## Remarques spécifiques à la platef
