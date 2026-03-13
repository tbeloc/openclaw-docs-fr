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

- `--dev` : isoler l'état sous `~/.openclaw-dev` et décaler les ports par défaut.
- `--profile <name>` : isoler l'état sous `~/.openclaw-<name>`.
- `--no-color` : désactiver les couleurs ANSI.
- `--update` : raccourci pour `openclaw update` (installations source uniquement).
- `-V`, `--version`, `-v` : afficher la version et quitter.

## Style de sortie

- Les couleurs ANSI et les indicateurs de progression ne s'affichent que dans les sessions TTY.
- Les hyperliens OSC-8 s'affichent sous forme de liens cliquables dans les terminaux pris en charge ; sinon, nous revenons aux URL simples.
- `--json` (et `--plain` où pris en charge) désactive le style pour une sortie propre.
- `--no-color` désactive le style ANSI ; `NO_COLOR=1` est également respecté.
- Les commandes longues affichent un indicateur de progression (OSC 9;4 si pris en charge).

## Palette de couleurs

OpenClaw utilise une palette de homard pour la sortie CLI.

- `accent` (#FF5A2D) : en-têtes, étiquettes, mises en évidence principales.
- `accentBright` (#FF7A3D) : noms de commandes, emphase.
- `accentDim` (#D14A22) : texte de mise en évidence secondaire.
- `info` (#FF8A5B) : valeurs informatives.
- `success` (#2FBF71) : états de succès.
- `warn` (#FFB020) : avertissements, solutions de secours, attention.
- `error` (#E23D2D) : erreurs, défaillances.
- `muted` (#8B7F77) : dé-emphase, métadonnées.

Source de vérité de la palette : `src/terminal/palette.ts` (alias « couture de homard »).

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

Remarque : les plugins peuvent ajouter des commandes de niveau supérieur supplémentaires (par exemple `openclaw voicecall`).

## Sécurité

- `openclaw security audit` — auditer la configuration + l'état local pour les pièges de sécurité courants.
- `openclaw security audit --deep` — sonde Gateway en direct au mieux.
- `openclaw security audit --fix` — resserrer les paramètres par défaut sûrs et chmod l'état/la configuration.

## Secrets

- `openclaw secrets reload` — re-résoudre les références et échanger atomiquement l'instantané d'exécution.
- `openclaw secrets audit` — analyser les résidus en texte brut, les références non résolues et la dérive de précédence.
- `openclaw secrets configure` — assistant interactif pour la configuration du fournisseur + mappage SecretRef + contrôle préalable/application.
- `openclaw secrets apply --from <plan.json>` — appliquer un plan précédemment généré (`--dry-run` pris en charge).

## Plugins

Gérer les extensions et leur configuration :

- `openclaw plugins list` — découvrir les plugins (utiliser `--json` pour la sortie machine).
- `openclaw plugins info <id>` — afficher les détails d'un plugin.
- `openclaw plugins install <path|.tgz|npm-spec>` — installer un plugin (ou ajouter un chemin de plugin à `plugins.load.paths`).
- `openclaw plugins enable <id>` / `disable <id>` — basculer `plugins.entries.<id>.enabled`.
- `openclaw plugins doctor` — signaler les erreurs de chargement de plugin.

La plupart des modifications de plugin nécessitent un redémarrage de la gateway. Voir [/plugin](/tools/plugin).

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
- `/debug` pour les remplacements de configuration d'exécution (mémoire, pas disque ; nécessite `commands.debug: true`).

## Configuration + intégration

### `setup`

Initialiser la configuration + l'espace de travail.

Options :

- `--workspace <dir>` : chemin de l'espace de travail de l'agent (par défaut `~/.openclaw/workspace`).
- `--wizard` : exécuter l'assistant d'intégration.
- `--non-interactive` : exécuter l'assistant sans invites.
- `--mode <local|remote>` : mode assistant.
- `--remote-url <url>` : URL de la Gateway distante.
- `--remote-token <token>` : jeton de la Gateway distante.

L'assistant s'exécute automatiquement lorsque des drapeaux d'assistant sont présents (`--non-interactive`, `--mode`, `--remote-url`, `--remote-token`).

### `onboard`

Assistant interactif pour configurer la gateway, l'espace de travail et les compétences.

Options :

- `--workspace <dir>`
- `--reset` (réinitialiser la configuration + les identifiants + les sessions avant l'assistant)
- `--reset-scope <config|config+creds+sessions|full>` (par défaut `config+creds+sessions` ; utiliser `full` pour supprimer également l'espace de travail)
- `--non-interactive`
- `--mode <local|remote>`
- `--flow <quickstart|advanced|manual>` (manual est un alias pour advanced)
- `--auth-choice <setup-token|token|chutes|openai-codex|openai-api-key|openrouter-api-key|ollama|ai-gateway-api-key|moonshot-api-key|moonshot-api-key-cn|kimi-code-api-key|synthetic-api-key|venice-api-key|gemini-api-key|zai-api-key|mistral-api-key|apiKey|minimax-api|minimax-api-lightning|opencode-zen|opencode-go|custom-api-key|skip>`
- `--token-provider <id>` (non-interactif ; utilisé avec `--auth-choice token`)
- `--token <token>` (non-interactif ; utilisé avec `--auth-choice token`)
- `--token-profile-id <id>` (non-interactif ; par défaut : `<provider>:manual`)
- `--token-expires-in <duration>` (non-interactif ; par exemple `365d`, `12h`)
- `--secret-input-mode <plaintext|ref>` (par défaut `plaintext` ; utiliser `ref` pour stocker les références env du fournisseur par défaut au lieu des clés en texte brut)
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
- `--custom-provider-id <id>` (non-interactif ; id de fournisseur personnalisé optionnel)
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
- `--node-manager <npm|pnpm|bun>` (pnpm recommandé ; bun non recommandé pour le runtime Gateway)
- `--json`

### `configure`

Assistant de configuration interactif (modèles, canaux, compétences, gateway).

### `config`

Assistants de configuration non-interactifs (get/set/unset/file/validate). L'exécution de `openclaw config` sans
sous-commande lance l'assistant.

Sous-commandes :

- `config get <path>` : afficher une valeur de configuration (chemin point/crochet).
- `config set <path> <value>` : définir une valeur (JSON5 ou chaîne brute).
- `config unset <path>` : supprimer une valeur.
- `config file` : afficher le chemin du fichier de configuration actif.
- `config validate` : valider la configuration actuelle par rapport au schéma sans démarrer la gateway.
- `config validate --json` : émettre une sortie JSON lisible par
