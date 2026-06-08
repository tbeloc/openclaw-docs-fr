---
title: "TUI - Primitives de rendu terminal et note de maturité de sécurité de sortie"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# TUI - Primitives de rendu terminal et note de maturité de sécurité de sortie

## Résumé

OpenClaw dispose d'une large boîte à outils terminal partagée : suppression ANSI, texte sûr sur une seule ligne, écritures de flux sûres pour les tuyaux cassés, invites stylisées, enveloppe de tableau, rendu QR terminal, progression OSC, liens OSC8, secours emoji décoratifs et thèmes spécifiques à TUI. C'est une infrastructure d'implémentation solide, mais c'est une couche de support plutôt qu'un flux de travail utilisateur entièrement documenté. La couverture est bêta car la plupart des preuves sont au niveau unitaire et dispersées dans les fonctionnalités CLI.

## Portée de la catégorie

Cette catégorie couvre les aides de sortie terminal partagées utilisées par les surfaces CLI/TUI : écriture de flux sûre, assainissement du texte, gestion ANSI/OSC, enveloppe de tableau, stylisation des invites, sortie QR, progression OSC, liens terminal, secours emoji décoratifs et contrôles de thème/lisibilité terminal.

## Fonctionnalités

- Primitives de rendu terminal : couvre les primitives de rendu terminal dans les aides de sortie terminal partagées utilisées par les surfaces CLI/TUI : écriture de flux sûre, assainissement du texte, gestion ANSI/OSC, enveloppe de tableau et primitives de rendu terminal et comportement de sécurité de sortie connexes.
- Sécurité de sortie : couvre la sécurité de sortie dans les aides de sortie terminal partagées utilisées par les surfaces CLI/TUI : écriture de flux sûre, assainissement du texte, gestion ANSI/OSC, enveloppe de tableau et primitives de rendu terminal et comportement de sécurité de sortie connexes.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (76%)`
- Signaux positifs : les aides terminal ont des tests unitaires directs pour la gestion ANSI/OSC, les graphèmes larges, l'enveloppe de tableau, les écritures de flux, le rendu QR, la progression OSC, les emoji décoratifs et le formatage TUI.
- Signaux négatifs : il y a peu de preuves au niveau du flux de travail que ces primitives se composent correctement sur install/onboard/status/logs/QR/TUI sur macOS, Linux, Windows Terminal et les terminaux dumb/non-TTY.
- Lacunes d'intégration : ajouter une couverture de fumée terminal multiplateforme pour la sortie table/log/status/QR en modes TTY et non-TTY.

## Score de qualité

- Score : `Bêta (78%)`
- Rapports Gitcrawl : `gitcrawl search issues "terminal output" -R openclaw/openclaw --state all --json number,title,url,state --limit 10` a retourné des rapports adjacents TUI/sortie incluant `#49763` pour un gel du spinner de chargement lors de la mise en file d'attente, `#79859` pour un mode de statut silencieux compatible avec l'enregistrement et `#74385` pour un mode terminal Hatch lent.
- Rapports Discrawl : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "terminal output"` a retourné une discussion d'opérateur adjacente sur la complétion terminal et la gestion de sortie, mais aucune défaillance de primitive partagée directe.
- Bonnes qualités : les aides de sortie assainissent les séquences de contrôle, gèrent les tuyaux cassés, préservent les jetons sûrs pour la copie, adaptent les bordures sur les terminaux Windows et supportent les capacités terminales QR et OSC.
- Mauvaises qualités : les primitives ne sont pas présentées comme un contrat d'opérateur cohésif, et certains problèmes de sortie terminal visibles par l'utilisateur restent aux couches supérieures.
- Exclu de la qualité : profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution.

## Score de complétude

- Score : `Bêta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/tui-and-terminal-ux.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour les primitives de rendu terminal et la sécurité de sortie.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le comportement du mode terminal non-TTY et multiplateforme n'est pas noté comme un flux de travail cohérent.
- La détection des capacités terminal est forte dans les aides, mais les docs exposent principalement le comportement de commande résultant plutôt que le modèle de capacité.

## Preuves

### Docs

- `docs/web/tui.md:192` documente les contrôles de couleur terminal et `OPENCLAW_THEME`.
- `docs/cli/qr.md:30` documente `--no-ascii` et `--json` pour la sortie QR.
- `docs/cli/logs.md:24` documente les modes de sortie de journal JSON/plain/no-color.
- `docs/cli/completion.md:11` documente la génération et l'installation de la complétion shell.

### Source

- `src/terminal/stream-writer.ts:18` implémente les écritures de flux sûres avec gestion des tuyaux cassés.
- `src/terminal/safe-text.ts:6` supprime les caractères ANSI et de contrôle pour le rendu terminal/journal sur une seule ligne.
- `src/terminal/table.ts:23` choisit les bordures Unicode ou ASCII en fonction de la plateforme et de l'environnement terminal.
- `src/terminal/table.ts:67` enveloppe les cellules de tableau sans diviser les séquences ANSI SGR ou OSC8.
- `src/media/qr-terminal.ts:47` rend la sortie QR terminal, y compris le mode QR compact.
- `src/terminal/osc-progress.ts:12` détecte le support de progression OSC et assainit les étiquettes de progression.

### Tests d'intégration

- `src/tui/tui-pty-harness.e2e.test.ts:415` vérifie que le texte d'erreur du fournisseur est préservé dans la sortie terminal.
- `src/tui/tui-pty-local.e2e.test.ts:249` prouve la sortie TUI locale via un PTY avec `OPENCLAW_THEME=dark`.

### Tests unitaires

- `src/terminal/ansi.test.ts:4` supprime les séquences ANSI et OSC8 et mesure les graphèmes larges.
- `src/terminal/table.test.ts:232` conserve les bordures Unicode sur les terminaux Windows modernes.
- `src/terminal/stream-writer.test.ts` couvre les écritures sûres pour les tuyaux cassés.
- `src/terminal/osc-progress.test.ts:4` couvre la détection du support terminal et les séquences de progression OSC assainies.
- `src/media/qr-terminal.test.ts:28` délègue le rendu terminal à qrcode ; `src/media/qr-terminal.render.test.ts:71` rend la sortie QR compacte.
- `src/tui/tui-formatters.test.ts:310` couvre l'assainissement du texte rendable TUI.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues "terminal output" -R openclaw/openclaw --state all --json number,title,url,state --limit 10`

Résultats :

- Rapports ouverts adjacents à la sortie retournés incluant `#49763`, `#79859` et `#74385`.

Requête :

`gitcrawl search issues "terminal qr ansi table" -R openclaw/openclaw --state all --json number,title,url,state --limit 8`

Résultats :

- Retourné 0 rapports de primitive terminal partagée directe.

### Requêtes Discrawl

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "terminal output"`

Résultats :

- Discussion d'opérateur adjacente retournée sur la complétion terminal et la gestion de sortie, mais aucune défaillance de primitive terminal directe.
