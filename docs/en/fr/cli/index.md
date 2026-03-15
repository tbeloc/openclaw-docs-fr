---
summary: "Référence CLI OpenClaw pour les commandes `openclaw`, sous-commandes et options"
read_when:
  - Adding or modifying CLI commands or options
  - Documenting new command surfaces
title: "Référence CLI"
---

# Référence CLI

Cette page décrit le comportement CLI actuel. Si les commandes changent, mettez à jour ce document.

## Pages de commandes

- [`setup`](/cli/setup)
- [`onboard`](/cli/onboard)
- [`configure`](/cli/configure)
- [`config`](/cli/config)
- [`completion`](/cli/completion)
- [`doctor`](/cli/doctor)
- [`dashboard`](/cli/dashboard)
- [`backup`](/cli/backup)
- [`reset`](/cli/reset)
- [`uninstall`](/cli/uninstall)
- [`update`](/cli/update)
- [`message`](/cli/message)
- [`agent`](/cli/agent)
- [`agents`](/cli/agents)
- [`acp`](/cli/acp)
- [`status`](/cli/status)
- [`health`](/cli/health)
- [`sessions`](/cli/sessions)
- [`gateway`](/cli/gateway)
- [`logs`](/cli/logs)
- [`system`](/cli/system)
- [`models`](/cli/models)
- [`memory`](/cli/memory)
- [`directory`](/cli/directory)
- [`nodes`](/cli/nodes)
- [`devices`](/cli/devices)
- [`node`](/cli/node)
- [`approvals`](/cli/approvals)
- [`sandbox`](/cli/sandbox)
- [`tui`](/cli/tui)
- [`browser`](/cli/browser)
- [`cron`](/cli/cron)
- [`dns`](/cli/dns)
- [`docs`](/cli/docs)
- [`hooks`](/cli/hooks)
- [`webhooks`](/cli/webhooks)
- [`pairing`](/cli/pairing)
- [`qr`](/cli/qr)
- [`plugins`](/cli/plugins) (commandes de plugin)
- [`channels`](/cli/channels)
- [`security`](/cli/security)
- [`secrets`](/cli/secrets)
- [`skills`](/cli/skills)
- [`daemon`](/cli/daemon) (alias hérité pour les commandes de service gateway)
- [`clawbot`](/cli/clawbot) (alias d'espace de noms hérité)
- [`voicecall`](/cli/voicecall) (plugin ; si installé)

## Drapeaux globaux

- `--dev`: isoler l'état sous `~/.openclaw-dev` et décaler les ports par défaut.
- `--profile <name>`: isoler l'état sous `~/.openclaw-<name>`.
- `--no-color`: désactiver les couleurs ANSI.
- `--update`: raccourci pour `openclaw update` (installations source uniquement).
- `-V`, `--version`, `-v`: afficher la version et quitter.

## Style de sortie

- Les couleurs ANSI et les indicateurs de progression ne s'affichent que dans les sessions TTY.
- Les hyperliens OSC-8 s'affichent sous forme de liens cliquables dans les terminaux pris en charge ; sinon, nous revenons aux URL simples.
- `--json` (et `--plain` le cas échéant) désactive le style pour une sortie propre.
- `--no-color` désactive le style ANSI ; `NO_COLOR=1` est également respecté.
- Les commandes longues affichent un indicateur de progression (OSC 9;4 le cas échéant).

## Palette de couleurs

OpenClaw utilise une palette de homard pour la sortie CLI.

- `accent` (#FF5A2D): en-têtes, étiquettes, mises en évidence principales.
- `accentBright` (#FF7A3D): noms de commandes, emphase.
- `accentDim` (#D14A22): texte de mise en évidence secondaire.
- `info` (#FF8A5B): valeurs informatives.
- `success` (#2FBF71): états de succès.
- `warn` (#FFB020): avertissements, solutions de secours, attention.
- `error` (#E23D2D): erreurs, défaillances.
- `muted` (#8B7F77): dé-emphase, métadonnées.

Source de vérité de la palette : `src/terminal/palette.ts` (alias « lobster seam »).

## Arborescence des commandes

```
openclaw [--dev] [--profile <name>] <command>
  setup
  onboard
  configure
  config
    get
    set
    unset
  completion
  doctor
  dashboard
  backup
    create
    verify
  security
    audit
  secrets
    reload
    migrate
  reset
  uninstall
  update
  channels
    list
    status
    logs
    add
    remove
    login
    logout
  directory
  skills
    list
    info
    check
  plugins
    list
    info
    install
    enable
    disable
    doctor
  memory
    status
    index
    search
  message
  agent
  agents
    list
    add
    delete
  acp
  status
  health
  sessions
  gateway
    call
    health
    status
    probe
    discover
    install
    uninstall
    start
    stop
    restart
    run
  daemon
    status
    install
    uninstall
    start
    stop
    restart
  logs
  system
    event
    heartbeat last|enable|disable
    presence
  models
    list
    status
    set
    set-image
    aliases list|add|remove
    fallbacks list|add|remove|clear
    image-fallbacks list|add|remove|clear
    scan
    auth add|setup-token|paste-token
    auth order get|set|clear
  sandbox
    list
    recreate
    explain
  cron
    status
    list
    add
    edit
    rm
    enable
    disable
    runs
    run
  nodes
  devices
  node
    run
    status
    install
    uninstall
    start
    stop
    restart
  approvals
    get
    set
    allowlist add|remove
  browser
    status
    start
    stop
    reset-profile
    tabs
    open
    focus
    close
    profiles
    create-profile
    delete-profile
    screenshot
    snapshot
    navigate
    resize
    click
    type
    press
    hover
    drag
    select
    upload
    fill
    dialog
    wait
    evaluate
    console
    pdf
  hooks
    list
    info
    check
    enable
    disable
    install
    update
  webhooks
    gmail setup|run
  pairing
    list
    approve
  qr
  clawbot
    qr
  docs
  dns
    setup
  tui
```

Remarque : les plugins peuvent ajouter des commandes supplémentaires au niveau supérieur (par exemple `openclaw voicecall`).

## Sécurité

- `openclaw security audit` — auditer la configuration + l'état local pour les pièges de sécurité courants.
- `openclaw security audit --deep` — sonde Gateway en direct au mieux.
- `openclaw security audit --fix` — renforcer les paramètres par défaut sûrs et chmod l'état/la configuration.

## Secrets

- `openclaw secrets reload` — re-résoudre les références et échanger atomiquement l'instantané d'exécution.
- `openclaw secrets audit` — analyser les résidus en texte brut, les références non résolues et la dérive de précédence.
- `openclaw secrets configure` — assistant interactif pour la configuration du fournisseur + mappage SecretRef + contrôle préalable/application.
- `openclaw secrets apply --from <plan.json>` — appliquer un plan précédemment généré (`--dry-run` pris en charge).

## Plugins

Gérer les extensions et leur configuration :

- `openclaw plugins list` — découvrir les plugins (utilisez `--json` pour la sortie machine).
- `openclaw plugins info <id>` — afficher les détails d'un plugin.
- `openclaw plugins install <path|.tgz|npm-spec>` — installer un plugin (ou ajouter un chemin de plugin à `plugins.load.paths`).
- `openclaw plugins enable <id>` / `disable <id>` — basculer `plugins.entries.<id>.enabled`.
- `openclaw plugins doctor` — signaler les erreurs de chargement des plugins.

La plupart des modifications de plugins nécessitent un redémarrage de la gateway. Voir [/plugin](/tools/plugin).

## Mémoire

Recherche vectorielle sur `MEMORY.md` + `memory/*.md` :

- `openclaw memory status` — afficher les statistiques d'index.
- `openclaw memory index` — réindexer les fichiers de mémoire.
- `openclaw memory search "<query>"` (ou `--query "<query>"`) — recherche sémantique sur la mémoire.

## Commandes slash de chat

Les messages de chat prennent en charge les commandes `/...` (texte et natif). Voir [/tools/slash-commands](/tools/slash-commands).

Points forts :

- `/status` pour les diagnostics rapides.
- `/config` pour les modifications de configuration persistantes.
- `/debug` pour les remplacements de configuration d'exécution uniquement (mémoire, pas disque ; nécessite `commands.debug: true`).

## Configuration + intégration

### `setup`

Initialiser la configuration + l'espace de travail.

Options :

- `--workspace <dir>`: chemin de l'espace de travail de l'agent (par défaut `~/.openclaw/workspace`).
- `--wizard`: exécuter l'assistant d'intégration.
- `--non-interactive`: exécuter l'assistant sans invites.
- `--mode <local|remote>`: mode assistant.
- `--remote-url <url>`: URL de la Gateway distante.
- `--remote-token <token>`: jeton de la Gateway distante.

L'assistant s'exécute automatiquement lorsque des drapeaux d'assistant sont présents (`--non-interactive`, `--mode`, `--remote-url`, `--remote-token`).

### `onboard`

Assistant interactif pour configurer la gateway, l'espace de travail et les compétences.

Options :

- `--workspace <dir>`
- `--reset` (réinitialiser la configuration + les identifiants + les sessions avant l'assistant)
- `--reset-scope <config|config+creds+sessions|full>` (par défaut `config+creds+sessions` ; utilisez `full` pour supprimer également l'espace de travail)
- `--non-interactive`
- `--mode <local|remote>`
- `--flow <quickstart|advanced|manual>` (manual est un alias pour advanced)
- `--auth-choice <setup-token|token|chutes|openai-codex|openai-api-key|openrouter-api-key|ollama|ai-gateway-api-key|moonshot-api-key|moonshot-api-key-cn|kimi-code-api-key|synthetic-api-key|venice-api-key|gemini-api-key|zai-api-key|mistral-api-key|apiKey|minimax-api|minimax-api-lightning|opencode-zen|opencode-go|custom-api-key|skip>`
- `--token-provider <id>` (non-interactif ; utilisé avec `--auth-choice token`)
- `--token <token>` (non-interactif ; utilisé avec `--auth-choice token`)
- `--token-profile-id <id>` (non-interactif ; par défaut : `<provider>:manual`)
- `--token-expires-in <duration>` (non-interactif ; par exemple `365d`, `12h`)
- `--secret-input-mode <plaintext|ref>` (par défaut `plaintext` ; utilisez `ref` pour stocker les références env par défaut du fournisseur au lieu des clés en texte brut)
- `--anthropic-api-key <key>`
- `--openai-api-key <key>`
- `--mistral-api-key <key>`
- `--openrouter-api-key <key>`
- `--ai-gateway-api-key <key>`
- `--moonshot-api-key <key>`
- `--kimi-code-api-key <key>`
- `--gemini-api-key <key>`
- `--zai-api-key <key>`
- `--minimax-api-key <key>`
- `--opencode-zen-api-key <key>`
- `--opencode-go-api-key <key>`
- `--custom-base-url <url>` (non-interactif ; utilisé avec `--auth-choice custom-api-key` ou `--auth-choice ollama`)
- `--custom-model-id <id>` (non-interactif ; utilisé avec `--auth-choice custom-api-key` ou `--auth-choice ollama`)
- `--custom-api-key <key>` (non-interactif ; optionnel ; utilisé avec `--auth-choice custom-api-key` ; revient à `CUSTOM_API_KEY` s'il est omis)
- `--custom-provider-id <id>` (non-interactif ; ID de fournisseur personnalisé optionnel)
- `--custom-compatibility <openai|anthropic>` (non-interactif ; optionnel ; par défaut `openai`)
- `--gateway-port <port>`
- `--gateway-bind <loopback|lan|tailnet|auto|custom>`
- `--gateway-auth <token|password>`
- `--gateway-token <token>`
- `--gateway-token-ref-env <name>` (non-interactif ; stocker `gateway.auth.token` comme SecretRef env ; nécessite que cette variable env soit définie ; ne peut pas être combiné avec `--gateway-token`)
- `--gateway-password <password>`
- `--remote-url <url>`
- `--remote-token <token>`
- `--tailscale <off|serve|funnel>`
- `--tailscale-reset-on-exit`
- `--install-daemon`
- `--no-install-daemon` (alias : `--skip-daemon`)
- `--daemon-runtime <node|bun>`
- `--skip-channels`
- `--skip-skills`
- `--skip-health`
- `--skip-ui`
- `--node-manager <npm|pnpm|bun>` (pnpm recommandé ; bun non recommandé pour l'exécution de Gateway)
- `--json`

### `configure`

Assistant de configuration interactif (modèles, canaux, compétences, gateway).

### `config`

Assistants de configuration non-interactifs (get/set/unset/file/validate). L'exécution de `openclaw config` sans sous-commande lance l'assistant.

Sous-commandes :

- `config get <path>`: afficher une valeur de configuration (chemin point/crochet).
- `config set <path> <value>`: définir une valeur (JSON5 ou chaîne brute).
- `config unset <path>`: supprimer une valeur.
- `config file`: afficher le chemin du fichier de configuration actif.
- `config validate`: valider la configuration actuelle par rapport au schéma sans démarrer la gateway.
- `config validate --json`: émettre une sortie JSON lisible par machine.

### `doctor`

Vérifications de santé + correctifs rapides (configuration + gateway + services hérités).

Options :

- `--no-workspace-suggestions`: désactiver les conseils de mémoire de l'espace de travail.
- `--yes`: accepter les valeurs par défaut sans demander (sans tête).
- `--non-interactive`: ignorer les invites ; appliquer uniquement les migrations sûres.
- `--deep`: analyser les services système pour les installations de gateway supplémentaires.

## Assistants de canal

### `channels`

Gérer les comptes de canal de chat (WhatsApp/Telegram/Discord/Google Chat/Slack/Mattermost (plugin)/Signal/iMessage/MS Teams).

Sous-commandes :

- `channels list` : afficher les canaux configurés et les profils d'authentification.
- `channels status` : vérifier la disponibilité de la passerelle et la santé du canal (`--probe` exécute des vérifications supplémentaires ; utilisez `openclaw health` ou `openclaw status --deep` pour les sondes de santé de la passerelle).
- Conseil : `channels status` affiche les avertissements avec les corrections suggérées lorsqu'il peut détecter les erreurs de configuration courantes (puis vous renvoie à `openclaw doctor`).
- `channels logs` : afficher les journaux de canal récents du fichier journal de la passerelle.
- `channels add` : configuration de style assistant lorsqu'aucun drapeau n'est transmis ; les drapeaux passent au mode non interactif.
  - Lors de l'ajout d'un compte non par défaut à un canal utilisant toujours la configuration de niveau supérieur à compte unique, OpenClaw déplace les valeurs délimitées par compte dans `channels.<channel>.accounts.default` avant d'écrire le nouveau compte.
  - `channels add` non interactif ne crée/met à niveau pas automatiquement les liaisons ; les liaisons réservées au canal continuent de correspondre au compte par défaut.
- `channels remove` : désactiver par défaut ; passez `--delete` pour supprimer les entrées de configuration sans invites.
- `channels login` : connexion interactive au canal (WhatsApp Web uniquement).
- `channels logout` : se déconnecter d'une session de canal (si pris en charge).

Options courantes :

- `--channel <name>` : `whatsapp|telegram|discord|googlechat|slack|mattermost|signal|imessage|msteams`
- `--account <id>` : identifiant du compte de canal (par défaut `default`)
- `--name <label>` : nom d'affichage du compte

Options de `channels login` :

- `--channel <channel>` (par défaut `whatsapp` ; prend en charge `whatsapp`/`web`)
- `--account <id>`
- `--verbose`

Options de `channels logout` :

- `--channel <channel>` (par défaut `whatsapp`)
- `--account <id>`

Options de `channels list` :

- `--no-usage` : ignorer les instantanés d'utilisation/quota du fournisseur de modèles (OAuth/API uniquement).
- `--json` : sortie JSON (inclut l'utilisation sauf si `--no-usage` est défini).

Options de `channels logs` :

- `--channel <name|all>` (par défaut `all`)
- `--lines <n>` (par défaut `200`)
- `--json`

Plus de détails : [/concepts/oauth](/concepts/oauth)

Exemples :

```bash
openclaw channels add --channel telegram --account alerts --name "Alerts Bot" --token $TELEGRAM_BOT_TOKEN
openclaw channels add --channel discord --account work --name "Work Bot" --token $DISCORD_BOT_TOKEN
openclaw channels remove --channel discord --account work --delete
openclaw channels status --probe
openclaw status --deep
```

### `skills`

Lister et inspecter les compétences disponibles ainsi que les informations de disponibilité.

Sous-commandes :

- `skills list` : lister les compétences (par défaut quand aucune sous-commande).
- `skills info <name>` : afficher les détails d'une compétence.
- `skills check` : résumé des compétences prêtes par rapport aux exigences manquantes.

Options :

- `--eligible` : afficher uniquement les compétences prêtes.
- `--json` : sortie JSON (sans style).
- `-v`, `--verbose` : inclure les détails des exigences manquantes.

Conseil : utilisez `npx clawhub` pour rechercher, installer et synchroniser les compétences.

### `pairing`

Approuver les demandes d'appairage DM sur les canaux.

Sous-commandes :

- `pairing list [channel] [--channel <channel>] [--account <id>] [--json]`
- `pairing approve <channel> <code> [--account <id>] [--notify]`
- `pairing approve --channel <channel> [--account <id>] <code> [--notify]`

### `devices`

Gérer les entrées d'appairage des appareils de la passerelle et les jetons d'appareil par rôle.

Sous-commandes :

- `devices list [--json]`
- `devices approve [requestId] [--latest]`
- `devices reject <requestId>`
- `devices remove <deviceId>`
- `devices clear --yes [--pending]`
- `devices rotate --device <id> --role <role> [--scope <scope...>]`
- `devices revoke --device <id> --role <role>`

### `webhooks gmail`

Configuration et exécution du hook Gmail Pub/Sub. Voir [/automation/gmail-pubsub](/automation/gmail-pubsub).

Sous-commandes :

- `webhooks gmail setup` (nécessite `--account <email>` ; prend en charge `--project`, `--topic`, `--subscription`, `--label`, `--hook-url`, `--hook-token`, `--push-token`, `--bind`, `--port`, `--path`, `--include-body`, `--max-bytes`, `--renew-minutes`, `--tailscale`, `--tailscale-path`, `--tailscale-target`, `--push-endpoint`, `--json`)
- `webhooks gmail run` (remplacements d'exécution pour les mêmes drapeaux)

### `dns setup`

Assistant DNS de découverte à grande distance (CoreDNS + Tailscale). Voir [/gateway/discovery](/gateway/discovery).

Options :

- `--apply` : installer/mettre à jour la configuration CoreDNS (nécessite sudo ; macOS uniquement).

## Messagerie + agent

### `message`

Messagerie sortante unifiée + actions de canal.

Voir : [/cli/message](/cli/message)

Sous-commandes :

- `message send|poll|react|reactions|read|edit|delete|pin|unpin|pins|permissions|search|timeout|kick|ban`
- `message thread <create|list|reply>`
- `message emoji <list|upload>`
- `message sticker <send|upload>`
- `message role <info|add|remove>`
- `message channel <info|list>`
- `message member info`
- `message voice status`
- `message event <list|create>`

Exemples :

- `openclaw message send --target +15555550123 --message "Hi"`
- `openclaw message poll --channel discord --target channel:123 --poll-question "Snack?" --poll-option Pizza --poll-option Sushi`

### `agent`

Exécuter un tour d'agent via la passerelle (ou `--local` intégré).

Requis :

- `--message <text>`

Options :

- `--to <dest>` (pour la clé de session et la livraison optionnelle)
- `--session-id <id>`
- `--thinking <off|minimal|low|medium|high|xhigh>` (modèles GPT-5.2 + Codex uniquement)
- `--verbose <on|full|off>`
- `--channel <whatsapp|telegram|discord|slack|mattermost|signal|imessage|msteams>`
- `--local`
- `--deliver`
- `--json`
- `--timeout <seconds>`

### `agents`

Gérer les agents isolés (espaces de travail + authentification + routage).

#### `agents list`

Lister les agents configurés.

Options :

- `--json`
- `--bindings`

#### `agents add [name]`

Ajouter un nouvel agent isolé. Exécute l'assistant guidé sauf si des drapeaux (ou `--non-interactive`) sont transmis ; `--workspace` est requis en mode non interactif.

Options :

- `--workspace <dir>`
- `--model <id>`
- `--agent-dir <dir>`
- `--bind <channel[:accountId]>` (répétable)
- `--non-interactive`
- `--json`

Les spécifications de liaison utilisent `channel[:accountId]`. Lorsque `accountId` est omis, OpenClaw peut résoudre la portée du compte via les valeurs par défaut du canal/les hooks de plugin ; sinon, c'est une liaison de canal sans portée de compte explicite.

#### `agents bindings`

Lister les liaisons de routage.

Options :

- `--agent <id>`
- `--json`

#### `agents bind`

Ajouter des liaisons de routage pour un agent.

Options :

- `--agent <id>`
- `--bind <channel[:accountId]>` (répétable)
- `--json`

#### `agents unbind`

Supprimer les liaisons de routage pour un agent.

Options :

- `--agent <id>`
- `--bind <channel[:accountId]>` (répétable)
- `--all`
- `--json`

#### `agents delete <id>`

Supprimer un agent et nettoyer son espace de travail + état.

Options :

- `--force`
- `--json`

### `acp`

Exécuter le pont ACP qui connecte les IDE à la passerelle.

Voir [`acp`](/cli/acp) pour les options et exemples complets.

### `status`

Afficher la santé de la session liée et les destinataires récents.

Options :

- `--json`
- `--all` (diagnostic complet ; lecture seule, collable)
- `--deep` (sonder les canaux)
- `--usage` (afficher l'utilisation/quota du fournisseur de modèles)
- `--timeout <ms>`
- `--verbose`
- `--debug` (alias pour `--verbose`)

Remarques :

- L'aperçu inclut l'état du service de la passerelle + nœud hôte lorsqu'il est disponible.

### Suivi de l'utilisation

OpenClaw peut afficher l'utilisation/quota du fournisseur lorsque les identifiants OAuth/API sont disponibles.

Surfaces :

- `/status` (ajoute une ligne d'utilisation du fournisseur courte lorsqu'elle est disponible)
- `openclaw status --usage` (affiche la répartition complète du fournisseur)
- Barre de menu macOS (section Utilisation sous Contexte)

Remarques :

- Les données proviennent directement des points de terminaison d'utilisation du fournisseur (pas d'estimations).
- Fournisseurs : Anthropic, GitHub Copilot, OpenAI Codex OAuth, plus Gemini CLI/Antigravity lorsque ces plugins de fournisseur sont activés.
- Si aucune information d'identification correspondante n'existe, l'utilisation est masquée.
- Détails : voir [Suivi de l'utilisation](/concepts/usage-tracking).

### `health`

Récupérer la santé de la passerelle en cours d'exécution.

Options :

- `--json`
- `--timeout <ms>`
- `--verbose`

### `sessions`

Lister les sessions de conversation stockées.

Options :

- `--json`
- `--verbose`
- `--store <path>`
- `--active <minutes>`

## Réinitialisation / Désinstallation

### `reset`

Réinitialiser la configuration/état local (garde la CLI installée).

Options :

- `--scope <config|config+creds+sessions|full>`
- `--yes`
- `--non-interactive`
- `--dry-run`

Remarques :

- `--non-interactive` nécessite `--scope` et `--yes`.

### `uninstall`

Désinstaller le service de passerelle + données locales (la CLI reste).

Options :

- `--service`
- `--state`
- `--workspace`
- `--app`
- `--all`
- `--yes`
- `--non-interactive`
- `--dry-run`

Remarques :

- `--non-interactive` nécessite `--yes` et des portées explicites (ou `--all`).

## Passerelle

### `gateway`

Exécuter la passerelle WebSocket.

Options :

- `--port <port>`
- `--bind <loopback|tailnet|lan|auto|custom>`
- `--token <token>`
- `--auth <token|password>`
- `--password <password>`
- `--password-file <path>`
- `--tailscale <off|serve|funnel>`
- `--tailscale-reset-on-exit`
- `--allow-unconfigured`
- `--dev`
- `--reset` (réinitialiser la configuration dev + identifiants + sessions + espace de travail)
- `--force` (tuer l'écouteur existant sur le port)
- `--verbose`
- `--claude-cli-logs`
- `--ws-log <auto|full|compact>`
- `--compact` (alias pour `--ws-log compact`)
- `--raw-stream`
- `--raw-stream-path <path>`

### `gateway service`

Gérer le service de passerelle (launchd/systemd/schtasks).

Sous-commandes :

- `gateway status` (sonde le RPC de la passerelle par défaut)
- `gateway install` (installation du service)
- `gateway uninstall`
- `gateway start`
- `gateway stop`
- `gateway restart`

Remarques :

- `gateway status` sonde le RPC de la passerelle par défaut en utilisant le port/la configuration résolue du service (remplacer avec `--url/--token/--password`).
- `gateway status` prend en charge `--no-probe`, `--deep`, `--require-rpc` et `--json` pour les scripts.
- `gateway status` affiche également les services de passerelle hérités ou supplémentaires lorsqu'il peut les détecter (`--deep` ajoute des analyses au niveau du système). Les services OpenClaw nommés par profil sont traités comme de première classe et ne sont pas signalés comme « supplémentaires ».
- `gateway status` affiche le chemin de configuration que la CLI utilise par rapport à la configuration que le service utilise probablement (env du service), plus l'URL cible de sonde résolue.
- Sur les installations systemd Linux, les vérifications de dérive de jeton d'état incluent à la fois les sources d'unité `Environment=` et `EnvironmentFile=`.
- `gateway install|uninstall|start|stop|restart` prennent en charge `--json` pour les scripts (la sortie par défaut reste conviviale).
- `gateway install` utilise par défaut le runtime Node ; bun n'est **pas recommandé** (bugs WhatsApp/Telegram).
- Options de `gateway install` : `--port`, `--runtime`, `--token`, `--force`, `--json`.

### `logs`

Suivre les journaux de fichier de la passerelle via RPC.

Remarques :

- Les sessions TTY affichent une vue structurée et colorisée ; les non-TTY reviennent au texte brut.
- `--json` émet du JSON délimité par des lignes (un événement de journal par ligne).

Exemples :

```bash
openclaw logs --follow
openclaw logs --limit 200
openclaw logs --plain
openclaw logs --json
openclaw logs --no-color
```

### `gateway <subcommand>`

Assistants CLI de la passerelle (utilisez `--url`, `--token`, `--password`, `--timeout`, `--expect-final` pour les sous-commandes RPC).
Lorsque vous passez `--url`, la CLI n'applique pas automatiquement les identifiants de configuration ou d'environnement.
Incluez `--token` ou `--password` explicitement. Les identifiants explicites manquants sont une erreur.

Sous-commandes :

- `gateway call <method> [--params <json>]`
- `gateway health`
- `gateway status`
- `gateway probe`
- `gateway discover`
- `gateway install|uninstall|start|stop|restart`
- `gateway run`

RPC courants :

- `config.apply` (valider + écrire la configuration + redémarrer + réveiller)
- `config.patch` (fusionner une mise à jour partielle + redémarrer + réveiller)
- `update.run` (exécuter la mise à jour + redémarrer + réveiller)

Conseil : lors de l'appel de `config.set`/`config.apply`/`config.patch` directement, passez `baseHash` de
`config.get` si une configuration existe déjà.

## Modèles

Voir [/concepts/models](/concepts/models) pour le comportement de secours et la stratégie d'analyse.

Configuration du jeton Anthropic (supportée) :

```bash
claude setup-token
openclaw models auth setup-token --provider anthropic
openclaw models status
```

Note de politique : il s'agit d'une compatibilité technique. Anthropic a bloqué certains usages d'abonnement en dehors de Claude Code par le passé ; vérifiez les conditions actuelles d'Anthropic avant de vous fier à setup-token en production.

### `models` (racine)

`openclaw models` est un alias pour `models status`.

Options racine :

- `--status-json` (alias pour `models status --json`)
- `--status-plain` (alias pour `models status --plain`)

### `models list`

Options :

- `--all`
- `--local`
- `--provider <name>`
- `--json`
- `--plain`

### `models status`

Options :

- `--json`
- `--plain`
- `--check` (sortie 1=expiré/manquant, 2=expiration imminente)
- `--probe` (sonde en direct des profils d'authentification configurés)
- `--probe-provider <name>`
- `--probe-profile <id>` (répéter ou séparé par des virgules)
- `--probe-timeout <ms>`
- `--probe-concurrency <n>`
- `--probe-max-tokens <n>`

Inclut toujours l'aperçu de l'authentification et l'état d'expiration OAuth pour les profils du magasin d'authentification.
`--probe` exécute des requêtes en direct (peut consommer des jetons et déclencher des limites de débit).

### `models set <model>`

Définir `agents.defaults.model.primary`.

### `models set-image <model>`

Définir `agents.defaults.imageModel.primary`.

### `models aliases list|add|remove`

Options :

- `list` : `--json`, `--plain`
- `add <alias> <model>`
- `remove <alias>`

### `models fallbacks list|add|remove|clear`

Options :

- `list` : `--json`, `--plain`
- `add <model>`
- `remove <model>`
- `clear`

### `models image-fallbacks list|add|remove|clear`

Options :

- `list` : `--json`, `--plain`
- `add <model>`
- `remove <model>`
- `clear`

### `models scan`

Options :

- `--min-params <b>`
- `--max-age-days <days>`
- `--provider <name>`
- `--max-candidates <n>`
- `--timeout <ms>`
- `--concurrency <n>`
- `--no-probe`
- `--yes`
- `--no-input`
- `--set-default`
- `--set-image`
- `--json`

### `models auth add|setup-token|paste-token`

Options :

- `add` : assistant d'authentification interactif
- `setup-token` : `--provider <name>` (par défaut `anthropic`), `--yes`
- `paste-token` : `--provider <name>`, `--profile-id <id>`, `--expires-in <duration>`

### `models auth order get|set|clear`

Options :

- `get` : `--provider <name>`, `--agent <id>`, `--json`
- `set` : `--provider <name>`, `--agent <id>`, `<profileIds...>`
- `clear` : `--provider <name>`, `--agent <id>`

## Système

### `system event`

Mettre en file d'attente un événement système et déclencher optionnellement un battement de cœur (Gateway RPC).

Requis :

- `--text <text>`

Options :

- `--mode <now|next-heartbeat>`
- `--json`
- `--url`, `--token`, `--timeout`, `--expect-final`

### `system heartbeat last|enable|disable`

Contrôles de battement de cœur (Gateway RPC).

Options :

- `--json`
- `--url`, `--token`, `--timeout`, `--expect-final`

### `system presence`

Lister les entrées de présence système (Gateway RPC).

Options :

- `--json`
- `--url`, `--token`, `--timeout`, `--expect-final`

## Cron

Gérer les tâches planifiées (Gateway RPC). Voir [/automation/cron-jobs](/automation/cron-jobs).

Sous-commandes :

- `cron status [--json]`
- `cron list [--all] [--json]` (sortie tableau par défaut ; utilisez `--json` pour le format brut)
- `cron add` (alias : `create` ; nécessite `--name` et exactement l'un de `--at` | `--every` | `--cron`, et exactement une charge utile de `--system-event` | `--message`)
- `cron edit <id>` (champs de correctif)
- `cron rm <id>` (alias : `remove`, `delete`)
- `cron enable <id>`
- `cron disable <id>`
- `cron runs --id <id> [--limit <n>]`
- `cron run <id> [--force]`

Toutes les commandes `cron` acceptent `--url`, `--token`, `--timeout`, `--expect-final`.

## Hôte de nœud

`node` exécute un **hôte de nœud sans interface** ou le gère en tant que service en arrière-plan. Voir
[`openclaw node`](/cli/node).

Sous-commandes :

- `node run --host <gateway-host> --port 18789`
- `node status`
- `node install [--host <gateway-host>] [--port <port>] [--tls] [--tls-fingerprint <sha256>] [--node-id <id>] [--display-name <name>] [--runtime <node|bun>] [--force]`
- `node uninstall`
- `node stop`
- `node restart`

Notes d'authentification :

- `node` résout l'authentification de la passerelle à partir de l'env/config (pas de drapeaux `--token`/`--password`) : `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD`, puis `gateway.auth.*`. En mode local, l'hôte de nœud ignore intentionnellement `gateway.remote.*` ; en `gateway.mode=remote`, `gateway.remote.*` participe selon les règles de précédence distante.
- Les variables d'env héritées `CLAWDBOT_GATEWAY_*` sont intentionnellement ignorées pour la résolution d'authentification de l'hôte de nœud.

## Nœuds

`nodes` communique avec la passerelle et cible les nœuds appairés. Voir [/nodes](/nodes).

Options communes :

- `--url`, `--token`, `--timeout`, `--json`

Sous-commandes :

- `nodes status [--connected] [--last-connected <duration>]`
- `nodes describe --node <id|name|ip>`
- `nodes list [--connected] [--last-connected <duration>]`
- `nodes pending`
- `nodes approve <requestId>`
- `nodes reject <requestId>`
- `nodes rename --node <id|name|ip> --name <displayName>`
- `nodes invoke --node <id|name|ip> --command <command> [--params <json>] [--invoke-timeout <ms>] [--idempotency-key <key>]`
- `nodes run --node <id|name|ip> [--cwd <path>] [--env KEY=VAL] [--command-timeout <ms>] [--needs-screen-recording] [--invoke-timeout <ms>] <command...>` (nœud mac ou hôte de nœud sans interface)
- `nodes notify --node <id|name|ip> [--title <text>] [--body <text>] [--sound <name>] [--priority <passive|active|timeSensitive>] [--delivery <system|overlay|auto>] [--invoke-timeout <ms>]` (mac uniquement)

Caméra :

- `nodes camera list --node <id|name|ip>`
- `nodes camera snap --node <id|name|ip> [--facing front|back|both] [--device-id <id>] [--max-width <px>] [--quality <0-1>] [--delay-ms <ms>] [--invoke-timeout <ms>]`
- `nodes camera clip --node <id|name|ip> [--facing front|back] [--device-id <id>] [--duration <ms|10s|1m>] [--no-audio] [--invoke-timeout <ms>]`

Canevas + écran :

- `nodes canvas snapshot --node <id|name|ip> [--format png|jpg|jpeg] [--max-width <px>] [--quality <0-1>] [--invoke-timeout <ms>]`
- `nodes canvas present --node <id|name|ip> [--target <urlOrPath>] [--x <px>] [--y <px>] [--width <px>] [--height <px>] [--invoke-timeout <ms>]`
- `nodes canvas hide --node <id|name|ip> [--invoke-timeout <ms>]`
- `nodes canvas navigate <url> --node <id|name|ip> [--invoke-timeout <ms>]`
- `nodes canvas eval [<js>] --node <id|name|ip> [--js <code>] [--invoke-timeout <ms>]`
- `nodes canvas a2ui push --node <id|name|ip> (--jsonl <path> | --text <text>) [--invoke-timeout <ms>]`
- `nodes canvas a2ui reset --node <id|name|ip> [--invoke-timeout <ms>]`
- `nodes screen record --node <id|name|ip> [--screen <index>] [--duration <ms|10s>] [--fps <n>] [--no-audio] [--out <path>] [--invoke-timeout <ms>]`

Localisation :

- `nodes location get --node <id|name|ip> [--max-age <ms>] [--accuracy <coarse|balanced|precise>] [--location-timeout <ms>] [--invoke-timeout <ms>]`

## Navigateur

CLI de contrôle du navigateur (Chrome/Brave/Edge/Chromium dédié). Voir [`openclaw browser`](/cli/browser) et l'[outil Navigateur](/tools/browser).

Options communes :

- `--url`, `--token`, `--timeout`, `--json`
- `--browser-profile <name>`

Gérer :

- `browser status`
- `browser start`
- `browser stop`
- `browser reset-profile`
- `browser tabs`
- `browser open <url>`
- `browser focus <targetId>`
- `browser close [targetId]`
- `browser profiles`
- `browser create-profile --name <name> [--color <hex>] [--cdp-url <url>]`
- `browser delete-profile --name <name>`

Inspecter :

- `browser screenshot [targetId] [--full-page] [--ref <ref>] [--element <selector>] [--type png|jpeg]`
- `browser snapshot [--format aria|ai] [--target-id <id>] [--limit <n>] [--interactive] [--compact] [--depth <n>] [--selector <sel>] [--out <path>]`

Actions :

- `browser navigate <url> [--target-id <id>]`
- `browser resize <width> <height> [--target-id <id>]`
- `browser click <ref> [--double] [--button <left|right|middle>] [--modifiers <csv>] [--target-id <id>]`
- `browser type <ref> <text> [--submit] [--slowly] [--target-id <id>]`
- `browser press <key> [--target-id <id>]`
- `browser hover <ref> [--target-id <id>]`
- `browser drag <startRef> <endRef> [--target-id <id>]`
- `browser select <ref> <values...> [--target-id <id>]`
- `browser upload <paths...> [--ref <ref>] [--input-ref <ref>] [--element <selector>] [--target-id <id>] [--timeout-ms <ms>]`
- `browser fill [--fields <json>] [--fields-file <path>] [--target-id <id>]`
- `browser dialog --accept|--dismiss [--prompt <text>] [--target-id <id>] [--timeout-ms <ms>]`
- `browser wait [--time <ms>] [--text <value>] [--text-gone <value>] [--target-id <id>]`
- `browser evaluate --fn <code> [--ref <ref>] [--target-id <id>]`
- `browser console [--level <error|warn|info>] [--target-id <id>]`
- `browser pdf [--target-id <id>]`

## Recherche de documentation

### `docs [query...]`

Rechercher dans l'index de documentation en direct.

## TUI

### `tui`

Ouvrir l'interface utilisateur du terminal connectée à la passerelle.

Options :

- `--url <url>`
- `--token <token>`
- `--password <password>`
- `--session <key>`
- `--deliver`
- `--thinking <level>`
- `--message <text>`
- `--timeout-ms <ms>` (par défaut `agents.defaults.timeoutSeconds`)
- `--history-limit <n>`
