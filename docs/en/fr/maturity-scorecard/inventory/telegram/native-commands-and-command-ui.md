---
title: "Telegram - Native Commands and Command UI Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Telegram - Native Commands and Command UI Maturity Note

## Summary

Les commandes natives Telegram et l'interface utilisateur des commandes sont proches de Stable en termes de couverture. La synchronisation au démarrage enregistre les commandes natives, personnalisées, de plugin et de compétence ; l'authentification des commandes et l'adressage de groupe sont testés ; l'assurance qualité en direct couvre l'aide, les commandes, whoami, status, context, l'authentification répétée et le contrôle d'accès des commandes d'autres bots. La qualité reste Beta en raison du débordement du menu de commandes, de la suppression des alias/menus, des modifications du menu de commandes localisées et de la variation du dispatch des commandes slash.

## Category Scope

- Synchronisation au démarrage native `setMyCommands`, commandes personnalisées, alias natifs, entrées du menu de commandes de plugin et de compétence.
- Normalisation du nom/description de la commande, suppression du budget du menu, gestion des doublons et nettoyage lorsque les commandes natives sont désactivées.
- Commandes intégrées telles que `/help`, `/commands`, `/whoami`, `/status`, `/context`, `/activation`, `/reasoning` et commandes d'appairage d'appareil.
- Autorisation des commandes dans les DM, les groupes et les commandes adressées à d'autres bots.
- Boutons de modèle et assistants d'interface utilisateur de commande.

## Features

- Synchronisation au démarrage native setMyCommands : Synchronisation au démarrage native setMyCommands, commandes personnalisées, alias natifs, plugin
- Normalisation du nom/description de la commande : Normalisation du nom/description de la commande, suppression du budget du menu, doublons
- Commandes intégrées : Commandes intégrées telles que /help, /commands, /whoami, /status et interface utilisateur de commande associée.
- Autorisation des commandes dans les DM : Autorisation des commandes dans les DM, groupes et commandes adressées à d'autres bots
- Boutons de modèle : Boutons de modèle et assistants d'interface utilisateur de commande

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Stable (82%)`
- Positive signals:
  l'assurance qualité en direct inclut plusieurs scénarios de commandes, et l'enregistrement des commandes, la configuration des commandes, l'authentification de groupe, les alias, le support du menu et la livraison des commandes ont tous des tests ciblés.
- Negative signals:
  la preuve en direct ne couvre pas toutes les combinaisons de menu de commandes de plugin/compétence ou toutes les branches de débordement/nettoyage.
- Integration gaps:
  ajouter une preuve en direct pour les grands catalogues de commandes de plugin, le texte du menu de commandes localisé, le nettoyage natif désactivé et la récupération du débordement du menu de commandes.

## Quality Score

- Score: `Beta (76%)`
- Gitcrawl reports:
  #67782, #85493, #68833, #77513, et #81351 montrent un polissage actif du menu de commandes et de la synchronisation des commandes ; #79310/#78347 ont été signalés dans le trafic des responsables comme des problèmes de dispatch de commandes slash ou de plugin.
- Discrawl reports:
  le trafic récent des responsables incluait des corrections de comportement des commandes et les notes de version ont signalé le polissage adjacent aux commandes de saisie/progression/sujet de forum Telegram.
- Good qualities:
  les noms de commandes sont normalisés, les conflits sont ignorés, l'adressage des bots est respecté, l'authentification des commandes est explicite et l'assurance qualité en direct couvre le flux de commande intégrée principal.
- Bad qualities:
  les limites du menu Telegram et les catalogues de commandes de plugin/compétence créent une surface de démarrage à variance élevée pour les opérateurs.
- Excluded from quality:
  la couverture unitaire, la couverture d'intégration, l'étendue de l'assurance qualité en direct et le nombre de tests n'ont pas été utilisés comme entrées de qualité.

## Completeness Score

- Score: `Stable (82%)`
- Surface instructions: evaluated against `references/completeness/telegram.md`.
- Positive signals: les documents archivés, la source, les tests, Gitcrawl et les preuves Discrawl couvrent l'étendue de la taxonomie pour la synchronisation au démarrage native setMyCommands, la normalisation du nom/description de la commande, les commandes intégrées, l'autorisation des commandes dans les DM, les boutons de modèle.
- Negative signals: la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Missing capability branches: see `## Known Gaps` and `## Evidence` below for the recorded missing branches and operator-visible caveats.

## Known Gaps

- Ajouter des diagnostics de budget de menu de commandes générés pour les opérateurs.
- Conserver les combinaisons de menu de commandes localisées/personnalisées/de plugin dans la preuve de version.

## Evidence

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/telegram.md` documents les commandes natives, les commandes personnalisées, le débordement du menu de commandes, les commandes d'appairage d'appareil et le dépannage partiel des commandes.
- `/Users/kevinlin/code/openclaw/docs/channels/telegram.md` documente également le comportement de `/activation` et `/reasoning` pour Telegram.

### Source

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-native-commands.ts`
  et `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-native-command-menu.ts`
  implémentent la gestion des commandes natives et la synchronisation du menu.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/command-config.ts`
  normalise la configuration des commandes personnalisées.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/command-ui.ts` et
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/model-buttons.ts`
  implémentent les assistants d'interface utilisateur de commande.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-native-commands.runtime.ts`
  possède les dépendances d'exécution des commandes à l'exécution.

### Integration tests

- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/telegram/telegram-live.runtime.ts`
  includes `telegram-help-command`, `telegram-commands-command`,
  `telegram-whoami-command`, `telegram-status-command`,
  `telegram-repeated-command-authorization`,
  `telegram-other-bot-command-gating`, and `telegram-context-command`.

### Unit tests

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-native-commands.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-native-command-menu.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot.command-menu.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-native-commands.registry.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-native-commands.group-auth.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/bot-native-commands.skills-allowlist.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/command-ui.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/model-buttons.test.ts`

### Gitcrawl queries

Query:

`gitcrawl search openclaw/openclaw --query "setMyCommands" --json`

Results:

- #67782 PR open: skip delete before non-empty command sync.
- #85493 PR open: keep native aliases out of command menus.
- #68833 PR open: preserve customCommands priority in menu budget trimming.
- #77513 PR open: sync native commands to private and group scopes.

### Discrawl queries

Query:

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram commands"`

Results:

- `maintainers`, 2026-05-29: les corrections incluaient une formulation obsolète spécifique à Telegram pour `/reasoning stream` et des modifications de correspondance de commandes pour `/new` et `/reset`.
- `maintainer-security-ops`, 2026-05-27: l'accès aux commandes/outils a été discuté comme une préoccupation de durcissement inter-canaux.

Query:

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram inline button"`

Results:

- `clawtributors`, 2026-05-13: la PR #81351 a été listée pour les descriptions du menu de commandes Telegram localisées.
