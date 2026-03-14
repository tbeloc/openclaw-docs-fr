---
read_when:
  - Ajout ou modification de commandes CLI ou d'options
  - Rédaction de documentation pour une nouvelle interface de commande
summary: Référence CLI des commandes, sous-commandes et options OpenClaw `openclaw`
title: Référence CLI
x-i18n:
  generated_at: "2026-02-03T07:47:54Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a73923763d7b89d4b183f569d543927ffbfd1f3e02f9e66639913f6daf226850
  source_path: cli/index.md
  workflow: 15
---

# Référence CLI

Cette page décrit le comportement actuel de la CLI. Si une commande change, veuillez mettre à jour cette documentation.

## Pages de commandes

- [`setup`](/cli/setup)
- [`onboard`](/cli/onboard)
- [`configure`](/cli/configure)
- [`config`](/cli/config)
- [`doctor`](/cli/doctor)
- [`dashboard`](/cli/dashboard)
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
- [`plugins`](/cli/plugins) (commandes de plugins)
- [`channels`](/cli/channels)
- [`security`](/cli/security)
- [`skills`](/cli/skills)
- [`voicecall`](/cli/voicecall) (plugin ; si installé)

## Drapeaux globaux

- `--dev` : isole l'état sous `~/.openclaw-dev` et ajuste les ports par défaut.
- `--profile <name>` : isole l'état sous `~/.openclaw-<name>`.
- `--no-color` : désactive les couleurs ANSI.
- `--update` : raccourci pour `openclaw update` (installations à partir de la source uniquement).
- `-V`, `--version`, `-v` : affiche la version et quitte.

## Style de sortie

- Les couleurs ANSI et les indicateurs de progression ne s'affichent que dans les sessions TTY.
- Les hyperliens OSC-8 s'affichent sous forme de liens cliquables dans les terminaux supportés ; sinon, ils reviennent à des URL simples.
- `--json` (et `--plain` où supporté) désactive le style pour une sortie propre.
- `--no-color` désactive le style ANSI ; `NO_COLOR=1` est également supporté.
- Les commandes longues affichent des indicateurs de progression (utilisant OSC 9;4 si supporté).

## Palette de couleurs

OpenClaw utilise la palette de homard dans la sortie CLI.

- `accent` (#FF5A2D) : titres, étiquettes, mises en évidence principales.
- `accentBright` (#FF7A3D) : noms de commandes, emphase.
- `accentDim` (#D14A22) : texte de mise en évidence secondaire.
- `info` (#FF8A5B) : valeurs informatives.
- `success` (#2FBF71) : état de succès.
- `warn` (#FFB020) : avertissements, replis, remarques.
- `error` (#E23D2D) : erreurs, échecs.
- `muted` (#8B7F77) : affaibli, métadonnées.

Source d'autorité de la palette : `src/terminal/palette.ts` (alias "lobster seam").

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
  doctor
  security
    audit
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
  docs
  dns
    setup
  tui
```

Remarque : les plugins peuvent ajouter des commandes de niveau supérieur supplémentaires (par exemple `openclaw voicecall`).

## Sécurité

- `openclaw security audit` — audite la configuration + les failles de sécurité courantes dans l'état local.
- `openclaw security audit --deep` — effectue des sondages Gateway en temps réel au mieux.
- `openclaw security audit --fix` — renforce les paramètres de sécurité par défaut et chmod l'état/la configuration.

## Plugins

Gérez les extensions et leurs configurations :

- `openclaw plugins list` — découvrez les plugins (utilisez `--json` pour une sortie lisible par machine).
- `openclaw plugins info <id>` — affiche les détails du plugin.
- `openclaw plugins install <path|.tgz|npm-spec>` — installe un plugin (ou ajoute le chemin du plugin à `plugins.load.paths`).
- `openclaw plugins enable <id>` / `disable <id>` — bascule `plugins.entries.<id>.enabled`.
- `openclaw plugins doctor` — signale les erreurs de chargement des plugins.

La plupart des modifications de plugins nécessitent un redémarrage du Gateway. Voir [/plugin](/tools/plugin).

## Mémoire

Effectuez une recherche vectorielle sur `MEMORY.md` + `memory/*.md` :

- `openclaw memory status` — affiche les statistiques d'indexation.
- `openclaw memory index` — réindexe les fichiers de mémoire.
- `openclaw memory search "<query>"` — effectue une recherche sémantique sur la mémoire.

## Commandes slash de chat

Les messages de chat supportent les commandes `/...` (texte et natif). Voir [/tools/slash-commands](/tools/slash-commands).

Points forts :

- `/status` pour un diagnostic rapide.
- `/config` pour les modifications de configuration persistantes.
- `/debug` pour les remplacements de configuration au moment de l'exécution uniquement (en mémoire, non écrit sur disque ; nécessite `commands.debug: true`).

## Configuration + Intégration

### `setup`

Initialise la configuration + l'espace de travail.

Options :

- `--workspace <dir>` : chemin de l'espace de travail de l'agent (par défaut `~/.openclaw/workspace`).
- `--wizard` : exécute l'assistant d'intégration.
- `--non-interactive` : exécute l'assistant sans invites.
- `--mode <local|remote>` : mode assistant.
- `--remote-url <url>` : URL du Gateway distant.
- `--remote-token <token>` : jeton du Gateway distant.

L'assistant s'exécute automatiquement lorsque des drapeaux d'assistant sont présents (`--non-interactive`, `--mode`, `--remote-url`, `--remote-token`).

### `onboard`

Assistant interactif pour configurer le Gateway, l'espace de travail et les Skills.

Options :

- `--workspace <dir>`
- `--reset` (réinitialise la configuration + les identifiants + les sessions + l'espace de travail avant l'assistant)
- `--non-interactive`
- `--mode <local|remote>`
- `--flow <quickstart|advanced|manual>` (manual est un alias pour advanced)
- `--auth-choice <setup-token|token|chutes|openai-codex|openai-api-key|openrouter-api-key|ai-gateway-api-key|moonshot-api-key|kimi-code-api-key|synthetic-api-key|venice-api-key|gemini-api-key|zai-api-key|apiKey|minimax-api|minimax-api-lightning|opencode-zen|skip>`
- `--token-provider <id>` (non-interactif ; utilisé avec `--auth-choice token`)
- `--token <token>` (non-interactif ; utilisé avec `--auth-choice token`)
- `--token-profile-id <id>` (non-interactif ; par défaut : `<provider>:manual`)
- `--token-expires-in <duration>` (non-interactif ; par exemple `365d`, `12h`)
- `--anthropic-api-key <key>`
- `--openai-api-key <key>`
- `--openrouter-api-key <key>`
- `--ai-gateway-api-key <key>`
- `--moonshot-api-key <key>`
- `--kimi-code-api-key <key>`
- `--gemini-api-key <key>`
- `--zai-api-key <key>`
- `--minimax-api-key <key>`
- `--opencode-zen-api-key <key>`
- `--gateway-port <port>`
- `--gateway-bind <loopback|lan|tailnet|auto|custom>`
- `--gateway-auth <token|password>`
- `--gateway-token <token>`
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
- `--node-manager <npm|pnpm|bun>` (pnpm recommandé ; bun non recommandé pour le runtime Gateway)
- `--json`

### `configure`

Assistant de configuration interactif (modèles, canaux, Skills, Gateway).

### `config`

Outil de configuration non-interactif (get/set/unset). Exécuter `openclaw config` sans sous-commande lance l'assistant.

Sous-commandes :

- `config get <path>` : affiche la valeur de configuration (chemin point/crochet).
- `config set <path> <value>` : définit la valeur (JSON5 ou chaîne brute).
- `config unset <path>` : supprime la valeur.

### `doctor`

Vérification de santé + correctifs rapides (configuration + Gateway + services hérités).

Options :

- `--no-workspace-suggestions` : désactive les suggestions de mémoire de l'espace de travail.
- `--yes` : accepte les valeurs par défaut sans invite (mode sans tête).
- `--non-interactive` : ignore les invites ; applique uniquement les migrations de sécurité.
- `--deep` : analyse les services système pour trouver les installations Gateway supplémentaires.

## Outils de canaux

### `channels`

Gérez les comptes de canaux de chat (WhatsApp/Telegram/Discord/Google Chat/Slack/Mattermost (plugin)/Signal/iMessage/MS Teams).

Sous-commandes :

- `channels list` : affiche les canaux configurés et les profils d'authentification.
- `channels status` : vérifie la disponibilité du Gateway et la santé des canaux (`--probe` exécute des vérifications supplémentaires ; utilisez `openclaw health` ou `openclaw status --deep` pour les sondages de santé du Gateway).
- Conseil : `channels status` affiche des avertissements avec des corrections suggérées lorsqu'il détecte des erreurs de configuration courantes (puis pointe vers `openclaw doctor`).
- `channels logs` : affiche les journaux de canaux récents du fichier journal du Gateway.
- `channels add` : utilise un assistant de configuration lorsqu'aucun drapeau n'est passé ; les drapeaux basculent en mode non-interactif.
- `channels remove` : désactivé par défaut ; passez `--delete` pour supprimer sans invite l'entrée de configuration.
- `channels login` : connexion de canal interactif (WhatsApp Web uniquement).
- `channels logout` : déconnexion de la session de canal (si supporté).

Options générales :

- `--channel <name>` : `whatsapp|telegram|discord|googlechat|slack|mattermost|signal|imessage|msteams`
- `--account <id>` : id du compte de canal (par défaut `default`)
- `--name <label>` : nom d'affichage du compte

Options de `channels login` :

- `--channel <channel>` (par défaut `whatsapp` ; supporte `whatsapp`/`web`)
- `--account <id>`
- `--verbose`

Options de `channels logout` :

- `--channel <channel>` (par défaut `whatsapp`)
- `--account <id>`

Options de `channels list` :

- `--no-usage` : ignore les instantanés d'utilisation/quota du fournisseur de modèles (OAuth/API supportés uniquement).
- `--json` : sortie
