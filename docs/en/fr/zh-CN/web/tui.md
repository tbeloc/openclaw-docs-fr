---
read_when:
  - Vous voulez une introduction conviviale pour les débutants à TUI
  - Vous avez besoin d'une liste complète des fonctionnalités, commandes et raccourcis clavier de TUI
summary: Interface utilisateur terminal (TUI) : se connecter à Gateway depuis n'importe quelle machine
title: TUI
x-i18n:
  generated_at: "2026-02-03T10:13:10Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 4bf5b0037bbb3a166289f2f0a9399489637d4cf26335ae3577af9ea83eee747e
  source_path: web/tui.md
  workflow: 15
---

# TUI (Interface utilisateur terminal)

## Démarrage rapide

1. Démarrez Gateway.

```bash
openclaw gateway
```

2. Ouvrez TUI.

```bash
openclaw tui
```

3. Entrez un message et appuyez sur Entrée.

Gateway distant :

```bash
openclaw tui --url ws://<host>:<port> --token <gateway-token>
```

Si votre Gateway utilise l'authentification par mot de passe, utilisez `--password`.

## Ce que vous voyez

- Barre de titre : URL de connexion, agent actuel, session actuelle.
- Journal de chat : messages utilisateur, réponses de l'assistant, notifications système, cartes d'outils.
- Ligne d'état : état de connexion/exécution (connexion, exécution, streaming, inactif, erreur).
- Pied de page : état de connexion + agent + session + modèle + think/verbose/reasoning + comptage de tokens + état de livraison.
- Entrée : éditeur de texte avec autocomplétion.

## Modèle mental : agents + sessions

- Un agent est un identifiant unique (par exemple `main`, `research`). Gateway expose la liste.
- Les sessions appartiennent à l'agent actuel.
- Les clés de session sont stockées sous la forme `agent:<agentId>:<sessionKey>`.
  - Si vous entrez `/session main`, TUI l'étend à `agent:<currentAgent>:main`.
  - Si vous entrez `/session agent:other:main`, vous basculez explicitement vers cette session d'agent.
- Portée de la session :
  - `per-sender` (par défaut) : plusieurs sessions par agent.
  - `global` : TUI utilise toujours la session `global` (le sélecteur peut être vide).
- L'agent actuel + la session sont toujours visibles dans le pied de page.

## Envoi + Livraison

- Les messages sont envoyés à Gateway ; par défaut, ils ne sont pas livrés au fournisseur.
- Activer la livraison :
  - `/deliver on`
  - ou panneau de paramètres
  - ou démarrer avec `openclaw tui --deliver`

## Sélecteurs + Superpositions

- Sélecteur de modèle : liste les modèles disponibles et définit les remplacements de session.
- Sélecteur d'agent : sélectionnez un agent différent.
- Sélecteur de session : affiche uniquement les sessions de l'agent actuel.
- Paramètres : basculez la livraison, l'expansion de la sortie des outils et la visibilité de la réflexion.

## Raccourcis clavier

- Entrée : envoyer le message
- Échap : interrompre l'exécution active
- Ctrl+C : effacer l'entrée (appuyez deux fois pour quitter)
- Ctrl+D : quitter
- Ctrl+L : sélecteur de modèle
- Ctrl+G : sélecteur d'agent
- Ctrl+P : sélecteur de session
- Ctrl+O : basculer l'expansion de la sortie des outils
- Ctrl+T : basculer la visibilité de la réflexion (recharger l'historique)

## Commandes slash

Noyau :

- `/help`
- `/status`
- `/agent <id>` (ou `/agents`)
- `/session <key>` (ou `/sessions`)
- `/model <provider/model>` (ou `/models`)

Contrôle de session :

- `/think <off|minimal|low|medium|high>`
- `/verbose <on|full|off>`
- `/reasoning <on|off|stream>`
- `/usage <off|tokens|full>`
- `/elevated <on|off|ask|full>` (alias : `/elev`)
- `/activation <mention|always>`
- `/deliver <on|off>`

Cycle de vie de la session :

- `/new` ou `/reset` (réinitialiser la session)
- `/abort` (interrompre l'exécution active)
- `/settings`
- `/exit`

Les autres commandes slash de Gateway (par exemple `/context`) sont transférées à Gateway et affichées en tant que sortie système. Voir [Commandes slash](/tools/slash-commands).

## Commandes shell locales

- Les lignes préfixées par `!` exécutent des commandes shell locales sur l'hôte TUI.
- TUI demande une fois par session pour autoriser l'exécution locale ; refuser désactive `!` dans cette session.
- Les commandes s'exécutent dans le répertoire de travail TUI dans un shell non interactif vierge (pas de `cd`/variables d'environnement persistants).
- Un `!` seul est envoyé en tant que message normal ; les espaces de début ne déclenchent pas l'exécution locale.

## Sortie des outils

- Les appels d'outils s'affichent sous forme de cartes avec paramètres + résultats.
- Ctrl+O bascule entre les vues réduites/développées.
- Lors de l'exécution des outils, les mises à jour partielles sont diffusées en continu vers la même carte.

## Historique + Streaming

- À la connexion, TUI charge l'historique le plus récent (200 messages par défaut).
- Les réponses en streaming se mettent à jour sur place jusqu'à la fin.
- TUI écoute également les événements d'outils d'agent pour des cartes d'outils plus riches.

## Détails de connexion

- TUI s'enregistre auprès de Gateway avec `mode: "tui"`.
- La reconnexion affiche un message système ; les lacunes d'événements s'affichent dans le journal.

## Options

- `--url <url>` : URL WebSocket de Gateway (par défaut configuration ou `ws://127.0.0.1:<port>`)
- `--token <token>` : jeton Gateway (si nécessaire)
- `--password <password>` : mot de passe Gateway (si nécessaire)
- `--session <key>` : clé de session (par défaut : `main`, ou `global` si la portée est globale)
- `--deliver` : livrer les réponses de l'assistant au fournisseur (désactivé par défaut)
- `--thinking <level>` : remplacer le niveau de réflexion envoyé
- `--timeout-ms <ms>` : délai d'expiration de l'agent (millisecondes) (par défaut `agents.defaults.timeoutSeconds`)

## Dépannage

Pas de sortie après l'envoi d'un message :

- Exécutez `/status` dans TUI pour confirmer que Gateway est connecté et en état inactif/occupé.
- Vérifiez les journaux de Gateway : `openclaw logs --follow`.
- Confirmez que l'agent peut s'exécuter : `openclaw status` et `openclaw models status`.
- Si vous vous attendez à ce que le message apparaisse dans un canal de chat, activez la livraison (`/deliver on` ou `--deliver`).
- `--history-limit <n>` : nombre d'entrées d'historique à charger (200 par défaut)

## Dépannage

- `disconnected` : assurez-vous que Gateway est en cours d'exécution et que vos `--url/--token/--password` sont corrects.
- Aucun agent dans le sélecteur : vérifiez `openclaw agents list` et votre configuration de routage.
- Sélecteur de session vide : vous êtes peut-être dans une portée globale ou vous n'avez pas encore de session.
