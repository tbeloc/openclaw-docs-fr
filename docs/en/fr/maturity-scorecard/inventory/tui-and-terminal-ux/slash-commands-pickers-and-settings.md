---
title: "TUI - Slash Commands, Pickers, and Settings Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# TUI - Slash Commands, Pickers, and Settings Maturity Note

## Résumé

L'UX des commandes TUI est substantielle : model, agent, session, settings, status,
context, thinking, fast, verbose, trace, reasoning, usage, elevated, activation,
delivery, new/reset/abort, exit, et les chemins locaux `/auth` sont implémentés. Il
supporte également les pickers recherchables/filtrables et l'autocomplétion dynamique
des commandes Gateway. La qualité est bêta car la sémantique des commandes locales
par rapport à Gateway, la dispatch des commandes de plugin, les descriptions de
commandes et les lacunes TUI concurrentielles restent des problèmes actifs.

## Portée de la catégorie

Cette catégorie couvre l'analyse des slash commands, le forwarding des commandes, les
commandes locales uniquement, les sélecteurs model/agent/session, l'overlay des
settings, le picker du mode context, la liste dynamique des commandes Gateway, les
commandes de patch de session et la documentation des commandes.

## Fonctionnalités

- Slash Commands: Couvre les Slash Commands dans l'analyse des slash commands, le forwarding des commandes, les commandes locales uniquement, les sélecteurs model/agent/session, l'overlay des settings, le picker du mode context, la liste dynamique des commandes Gateway, les commandes de patch de session et la documentation des commandes.
- Pickers: Couvre les Pickers dans l'analyse des slash commands, le forwarding des commandes, les commandes locales uniquement, les sélecteurs model/agent/session, l'overlay des settings, le picker du mode context, la liste dynamique des commandes Gateway, les commandes de patch de session et la documentation des commandes.
- Settings: Couvre les Settings dans l'analyse des slash commands, le forwarding des commandes, les commandes locales uniquement, les sélecteurs model/agent/session, l'overlay des settings, le picker du mode context, la liste dynamique des commandes Gateway, les commandes de patch de session et la documentation des commandes.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score: `Bêta (78%)`
- Signaux positifs: les gestionnaires de commandes sont testés unitairement pour les pickers, le forwarding, le status, le context, le patching de session, le blocage de l'état occupé, `/auth`, `/new`, `/reset`, le routage d'arrêt et les références de model.
- Signaux négatifs: la dispatch des commandes détenues par les plugins et l'autocomplétion dynamique ont une preuve end-to-end plus mince, et la sémantique des commandes en mode local reste partiellement divergente.
- Lacunes d'intégration: ajouter un scénario PTY qui charge `commands.list`, complète automatiquement une commande de plugin, la dispatch et vérifie que le mode local rejette ou gère les commandes Gateway non supportées de manière prévisible.

## Score de qualité

- Score: `Bêta (72%)`
- Rapports Gitcrawl: `gitcrawl search issues "tui commands" -R openclaw/openclaw --state all --json number,title,url,state --limit 10` a retourné `#71592` pour la fallthrough des commandes locales, `#78347` pour les lacunes de dispatch des slash commands de plugin dans `openclaw agent` et TUI, `#79458` pour les champs i18n de description de commande, et `#86534` pour les lacunes TUI concurrentielles.
- Rapports Discrawl: `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "tui commands"` a retourné une discussion selon laquelle la PR `#83640` connecte l'autocomplétion TUI slash à la liste des commandes Gateway afin que les commandes détenues par les plugins s'affichent.
- Bonnes qualités: l'UX du sélecteur est recherchable/filtrable, les échecs de commande s'affichent sous forme de messages système, et les settings de session/model patchent le backend faisant autorité plutôt que seulement l'état local de l'UI.
- Mauvaises qualités: la découverte et la dispatch des commandes rattrapent encore les commandes détenues par les plugins et le mode local; certaines aides de commande peuvent annoncer un comportement qui n'est pas réellement disponible dans un mode.
- Exclu de la qualité: la profondeur des tests unitaires, d'intégration, e2e, live et du flux d'exécution.

## Score de complétude

- Score: `Bêta (78%)`
- Instructions de surface: évaluées par rapport à `references/completeness/tui-and-terminal-ux.md`.
- Signaux positifs: les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour les Slash Commands, Pickers, Settings.
- Signaux négatifs: la note archivée a précédé le scoring de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connus utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'ensemble des commandes en mode local a besoin d'une table de compatibilité plus stricte.
- La découverte et la dispatch des slash commands de plugin ont besoin d'une preuve complète du flux utilisateur de l'autocomplétion au résultat de la commande.

## Preuves

### Docs

- `docs/web/tui.md:82` documente les pickers model, agent, session et settings.
- `docs/web/tui.md:101` liste les slash commands principaux.
- `docs/web/tui.md:111` liste les contrôles de session tels que thinking, fast, verbose, trace, reasoning, usage, elevated, activation et delivery.
- `docs/web/tui.md:123` liste les commandes du cycle de vie de la session.

### Source

- `src/tui/tui-command-handlers.ts:129` construit le sélecteur de model et patche le model de session.
- `src/tui/tui-command-handlers.ts:165` construit le sélecteur d'agent.
- `src/tui/tui-command-handlers.ts:207` construit le sélecteur de session récente.
- `src/tui/tui-command-handlers.ts:256` construit les settings pour la sortie d'outil et la visibilité du thinking.
- `src/tui/tui-command-handlers.ts:293` dispatche les slash commands et transfère les commandes inconnues via le backend.
- `src/tui/gateway-chat.ts:258` expose `commands.list` pour la découverte dynamique des commandes.

### Tests d'intégration

- `src/tui/tui-pty-harness.e2e.test.ts:368` exerce l'entrée tapée à travers la boucle de terminal réelle.
- `src/tui/tui-pty-harness.e2e.test.ts:397` vérifie qu'une réponse de commande/source d'outil est rendue dans le terminal.

### Tests unitaires

- `src/tui/tui-command-handlers.test.ts:175` couvre l'hydratation du picker de session bornée.
- `src/tui/tui-command-handlers.test.ts:257` ouvre le sélecteur du mode context pour `/context`.
- `src/tui/tui-command-handlers.test.ts:305` transfère `/status` au chemin de commande partagé.
- `src/tui/tui-command-handlers.test.ts:436` crée des sessions TUI uniques pour `/new` et réinitialise les sessions partagées pour `/reset`.
- `src/tui/tui-command-handlers.test.ts:715` utilise des références de model canoniques dans le sélecteur de model.

### Requêtes Gitcrawl

Requête:

`gitcrawl search issues "tui commands" -R openclaw/openclaw --state all --json number,title,url,state --limit 10`

Résultats:

- A retourné 10 rapports ouverts, incluant `#71592`, `#78347`, `#79458`, `#10118`, `#81547`, `#56856`, `#86534` et `#81781`.

### Requêtes Discrawl

Requête:

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "tui commands"`

Résultats:

- A retourné une discussion de la PR `#83640`, qui connecte l'autocomplétion TUI slash à la liste des commandes Gateway pour les commandes détenues par les plugins.
