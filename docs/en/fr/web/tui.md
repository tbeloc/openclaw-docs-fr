---
summary: "Interface utilisateur de terminal (TUI) : se connecter à la Gateway depuis n'importe quelle machine"
read_when:
  - You want a beginner-friendly walkthrough of the TUI
  - You need the complete list of TUI features, commands, and shortcuts
title: "TUI"
---

# TUI (Interface utilisateur de terminal)

## Démarrage rapide

1. Démarrez la Gateway.

```bash
openclaw gateway
```

2. Ouvrez la TUI.

```bash
openclaw tui
```

3. Tapez un message et appuyez sur Entrée.

Gateway distante :

```bash
openclaw tui --url ws://<host>:<port> --token <gateway-token>
```

Utilisez `--password` si votre Gateway utilise l'authentification par mot de passe.

## Ce que vous voyez

- En-tête : URL de connexion, agent actuel, session actuelle.
- Journal de chat : messages utilisateur, réponses de l'assistant, avis système, cartes d'outils.
- Ligne d'état : état de connexion/exécution (connexion, exécution, streaming, inactif, erreur).
- Pied de page : état de connexion + agent + session + modèle + think/fast/verbose/reasoning + compteurs de jetons + livraison.
- Entrée : éditeur de texte avec autocomplétion.

## Modèle mental : agents + sessions

- Les agents sont des slugs uniques (par exemple `main`, `research`). La Gateway expose la liste.
- Les sessions appartiennent à l'agent actuel.
- Les clés de session sont stockées sous la forme `agent:<agentId>:<sessionKey>`.
  - Si vous tapez `/session main`, la TUI l'étend à `agent:<currentAgent>:main`.
  - Si vous tapez `/session agent:other:main`, vous basculez explicitement vers cette session d'agent.
- Portée de la session :
  - `per-sender` (par défaut) : chaque agent a plusieurs sessions.
  - `global` : la TUI utilise toujours la session `global` (le sélecteur peut être vide).
- L'agent actuel + la session sont toujours visibles dans le pied de page.

## Envoi + livraison

- Les messages sont envoyés à la Gateway ; la livraison aux fournisseurs est désactivée par défaut.
- Activez la livraison :
  - `/deliver on`
  - ou le panneau Paramètres
  - ou démarrez avec `openclaw tui --deliver`

## Sélecteurs + superpositions

- Sélecteur de modèle : liste les modèles disponibles et définit le remplacement de session.
- Sélecteur d'agent : choisissez un agent différent.
- Sélecteur de session : affiche uniquement les sessions de l'agent actuel.
- Paramètres : basculez la livraison, l'expansion de la sortie d'outil et la visibilité de la réflexion.

## Raccourcis clavier

- Entrée : envoyer le message
- Échap : abandonner l'exécution active
- Ctrl+C : effacer l'entrée (appuyez deux fois pour quitter)
- Ctrl+D : quitter
- Ctrl+L : sélecteur de modèle
- Ctrl+G : sélecteur d'agent
- Ctrl+P : sélecteur de session
- Ctrl+O : basculer l'expansion de la sortie d'outil
- Ctrl+T : basculer la visibilité de la réflexion (recharge l'historique)

## Commandes slash

Cœur :

- `/help`
- `/status`
- `/agent <id>` (ou `/agents`)
- `/session <key>` (ou `/sessions`)
- `/model <provider/model>` (ou `/models`)

Contrôles de session :

- `/think <off|minimal|low|medium|high>`
- `/fast <status|on|off>`
- `/verbose <on|full|off>`
- `/reasoning <on|off|stream>`
- `/usage <off|tokens|full>`
- `/elevated <on|off|ask|full>` (alias : `/elev`)
- `/activation <mention|always>`
- `/deliver <on|off>`

Cycle de vie de la session :

- `/new` ou `/reset` (réinitialiser la session)
- `/abort` (abandonner l'exécution active)
- `/settings`
- `/exit`

Les autres commandes slash de Gateway (par exemple, `/context`) sont transmises à la Gateway et affichées comme sortie système. Voir [Commandes slash](/tools/slash-commands).

## Commandes shell locales

- Préfixez une ligne avec `!` pour exécuter une commande shell locale sur l'hôte TUI.
- La TUI demande une fois par session pour autoriser l'exécution locale ; refuser maintient `!` désactivé pour la session.
- Les commandes s'exécutent dans un shell frais et non interactif dans le répertoire de travail TUI (pas de `cd`/env persistant).
- Les commandes shell locales reçoivent `OPENCLAW_SHELL=tui-local` dans leur environnement.
- Un seul `!` est envoyé comme message normal ; les espaces de début ne déclenchent pas l'exécution locale.

## Sortie d'outil

- Les appels d'outil s'affichent sous forme de cartes avec args + résultats.
- Ctrl+O bascule entre les vues réduites/développées.
- Pendant que les outils s'exécutent, les mises à jour partielles se diffusent dans la même carte.

## Couleurs du terminal

- La TUI conserve le texte du corps de l'assistant dans la couleur de premier plan par défaut de votre terminal afin que les terminaux sombres et clairs restent lisibles.
- Si votre terminal utilise un fond clair et la détection automatique est incorrecte, définissez `OPENCLAW_THEME=light` avant de lancer `openclaw tui`.
- Pour forcer la palette sombre d'origine à la place, définissez `OPENCLAW_THEME=dark`.

## Historique + streaming

- À la connexion, la TUI charge l'historique le plus récent (200 messages par défaut).
- Les réponses en streaming se mettent à jour sur place jusqu'à finalisation.
- La TUI écoute également les événements d'outil d'agent pour des cartes d'outil plus riches.

## Détails de connexion

- La TUI s'enregistre auprès de la Gateway en tant que `mode: "tui"`.
- Les reconnexions affichent un message système ; les lacunes d'événements sont signalées dans le journal.

## Options

- `--url <url>` : URL WebSocket de la Gateway (par défaut config ou `ws://127.0.0.1:<port>`)
- `--token <token>` : jeton de Gateway (si requis)
- `--password <password>` : mot de passe de Gateway (si requis)
- `--session <key>` : clé de session (par défaut : `main`, ou `global` quand la portée est globale)
- `--deliver` : livrer les réponses de l'assistant au fournisseur (désactivé par défaut)
- `--thinking <level>` : niveau de réflexion de remplacement pour les envois
- `--timeout-ms <ms>` : délai d'expiration de l'agent en ms (par défaut `agents.defaults.timeoutSeconds`)

Remarque : lorsque vous définissez `--url`, la TUI ne revient pas à la config ou aux identifiants d'environnement.
Passez `--token` ou `--password` explicitement. Les identifiants explicites manquants sont une erreur.

## Dépannage

Pas de sortie après l'envoi d'un message :

- Exécutez `/status` dans la TUI pour confirmer que la Gateway est connectée et inactif/occupé.
- Vérifiez les journaux de Gateway : `openclaw logs --follow`.
- Confirmez que l'agent peut s'exécuter : `openclaw status` et `openclaw models status`.
- Si vous attendez des messages dans un canal de chat, activez la livraison (`/deliver on` ou `--deliver`).
- `--history-limit <n>` : entrées d'historique à charger (200 par défaut)

## Dépannage de la connexion

- `disconnected` : assurez-vous que la Gateway est en cours d'exécution et que vos `--url/--token/--password` sont corrects.
- Aucun agent dans le sélecteur : vérifiez `openclaw agents list` et votre configuration de routage.
- Sélecteur de session vide : vous pourriez être dans la portée globale ou n'avoir aucune session pour le moment.
