---
title: "TUI - Note de Maturité de l'Exécution de Shell Local"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# TUI - Note de Maturité de l'Exécution de Shell Local

## Résumé

La fonctionnalité de shell local est utile et intentionnellement contrôlée : un `!` initial déclenche une invite d'approbation une fois par session, les commandes s'exécutent sur l'hôte TUI avec `OPENCLAW_SHELL=tui-local`, la sortie est plafonnée, et les sessions refusées restent désactivées. L'UX dispose de documentation claire et d'une couverture unitaire, mais peu de preuve PTY réelle et la limite de sécurité est à haut risque car elle utilise intentionnellement un shell sur la machine de l'opérateur.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Routage des commandes Bang : Couvre le routage des commandes Bang sur le routage `!`, l'invite d'approbation d'exécution locale, l'overlay Oui/Non, l'exécution de commande, la capture et le plafonnement de sortie, le rendu de sortie/erreur, le marqueur d'environnement, la gestion du répertoire courant, et la documentation qui distingue l'exécution sur l'hôte local de l'exécution Gateway.
- Invite d'approbation : Couvre l'invite d'approbation sur le routage `!`, l'invite d'approbation d'exécution locale, l'overlay Oui/Non, l'exécution de commande, la capture et le plafonnement de sortie, le rendu de sortie/erreur, le marqueur d'environnement, la gestion du répertoire courant, et la documentation qui distingue l'exécution sur l'hôte local de l'exécution Gateway.
- Affichage de la sortie de commande : Couvre l'affichage de la sortie de commande sur le routage `!`, l'invite d'approbation d'exécution locale, l'overlay Oui/Non, l'exécution de commande, la capture et le plafonnement de sortie, le rendu de sortie/erreur, le marqueur d'environnement, la gestion du répertoire courant, et la documentation qui distingue l'exécution sur l'hôte local de l'exécution Gateway.
- Marqueur d'environnement d'exécution : Couvre le marqueur d'environnement d'exécution sur le routage `!`, l'invite d'approbation d'exécution locale, l'overlay Oui/Non, l'exécution de commande, la capture et le plafonnement de sortie, le rendu de sortie/erreur, le marqueur d'environnement, la gestion du répertoire courant, et la documentation qui distingue l'exécution sur l'hôte local de l'exécution Gateway.

## Fonctionnalités

- Routage des commandes Bang : Couvre le routage des commandes Bang sur le routage `!`, l'invite d'approbation d'exécution locale, l'overlay Oui/Non, l'exécution de commande, la capture et le plafonnement de sortie, le rendu de sortie/erreur, le marqueur d'environnement, la gestion du répertoire courant, et la documentation qui distingue l'exécution sur l'hôte local de l'exécution Gateway.
- Invite d'approbation : Couvre l'invite d'approbation sur le routage `!`, l'invite d'approbation d'exécution locale, l'overlay Oui/Non, l'exécution de commande, la capture et le plafonnement de sortie, le rendu de sortie/erreur, le marqueur d'environnement, la gestion du répertoire courant, et la documentation qui distingue l'exécution sur l'hôte local de l'exécution Gateway.
- Affichage de la sortie de commande : Couvre l'affichage de la sortie de commande sur le routage `!`, l'invite d'approbation d'exécution locale, l'overlay Oui/Non, l'exécution de commande, la capture et le plafonnement de sortie, le rendu de sortie/erreur, le marqueur d'environnement, la gestion du répertoire courant, et la documentation qui distingue l'exécution sur l'hôte local de l'exécution Gateway.
- Marqueur d'environnement d'exécution : Couvre le marqueur d'environnement d'exécution sur le routage `!`, l'invite d'approbation d'exécution locale, l'overlay Oui/Non, l'exécution de commande, la capture et le plafonnement de sortie, le rendu de sortie/erreur, le marqueur d'environnement, la gestion du répertoire courant, et la documentation qui distingue l'exécution sur l'hôte local de l'exécution Gateway.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (70%)`
- Signaux positifs : le routage de soumission et l'approbation/exécution du shell local disposent de tests unitaires ciblés, et la documentation est précise sur le comportement de l'hôte local.
- Signaux négatifs : aucun scénario PTY/e2e ne vérifie l'overlay d'approbation, une commande réelle, le plafonnement de stdout/stderr, et le comportement de refus ensemble.
- Lacunes d'intégration : ajouter un test de fumée de shell local PTY qui refuse une fois, réessaie, approuve, exécute une commande inoffensive, vérifie `OPENCLAW_SHELL=tui-local`, et vérifie le plafonnement de sortie.

## Score de Qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : `gitcrawl search issues "TUI local shell" -R openclaw/openclaw --state all --json number,title,url,state --limit 8` n'a retourné aucun défaut direct de shell local, mais a retourné `#86632` où le mode intégré local a échoué une demande de données en direct qu'un autre agent capable de shell/curl a gérée. Une recherche plus large `gitcrawl search issues "local shell" ...` a retourné des rapports d'environnement de shell et de transport local en dehors du chemin TUI.
- Rapports Discrawl : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "TUI local shell"` a retourné une discussion TUI locale sans rapports de défaut direct de shell local.
- Bonnes qualités : l'exécution locale est explicite, contrôlée, limitée à la session, visiblement étiquetée, et plafonnée ; l'espace blanc initial et un `!` seul ne s'exécutent pas accidentellement.
- Mauvaises qualités : la fonctionnalité utilise `shell: true` par conception, donc le texte d'approbation et la gestion de sortie portent la plupart du fardeau de sécurité ; une supervision de commande plus riche n'est pas présente.
- Exclu de la qualité : profondeur des tests unitaires, d'intégration, e2e, en direct, et de flux d'exécution.

## Score de Complétude

- Score : `Beta (70%)`
- Instructions de surface : évaluées par rapport à `references/completeness/tui-and-terminal-ux.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le routage des commandes Bang, l'invite d'approbation, l'affichage de la sortie de commande, le marqueur d'environnement d'exécution.
- Signaux négatifs : la note archivée a précédé le score de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Il n'existe aucun scénario de terminal réel prouvant l'overlay d'approbation et le chemin d'exécution ensemble.
- La sortie est capturée après la fermeture de la commande plutôt que diffusée en continu en tant que processus interactif.

## Preuves

### Documentation

- `docs/web/tui.md:136` documente les commandes de shell local `!`.
- `docs/web/tui.md:138` indique que le TUI demande une approbation une fois par session et les sessions désactivées gardent l'exécution locale désactivée.
- `docs/web/tui.md:140` indique que les commandes s'exécutent dans un nouveau shell non interactif dans le répertoire de travail TUI.
- `docs/web/tui.md:141` documente `OPENCLAW_SHELL=tui-local`.
- `docs/cli/tui.md:76` utilise des commandes de shell local dans la boucle de réparation de configuration.

### Source

- `src/tui/tui-submit.ts:24` achemine uniquement les lignes `!` initiales brutes vers le shell local et traite un `!` seul comme un message normal.
- `src/tui/tui-local-shell.ts:27` crée le runner de shell local.
- `src/tui/tui-local-shell.ts:36` implémente l'invite d'approbation une fois par session.
- `src/tui/tui-local-shell.ts:81` exécute une ligne de shell local, plafonne la sortie, étiquette la sortie comme `[local]`, et signale la sortie.
- `src/tui/tui-local-shell.ts:108` génère avec `shell: true`, le répertoire de travail TUI, et `OPENCLAW_SHELL=tui-local`.

### Tests d'intégration

- Aucun test PTY/e2e dédié au shell local trouvé. `src/tui/tui-pty-harness.e2e.test.ts:368` couvre l'entrée tapée à travers la boucle TUI, mais pas l'overlay d'approbation ou l'exécution du shell.

### Tests unitaires

- `src/tui/tui.submit-handler.test.ts:13` achemine les lignes `!` vers le gestionnaire bang.
- `src/tui/tui.submit-handler.test.ts:24` traite un `!` seul comme un message normal.
- `src/tui/tui.submit-handler.test.ts:34` garde l'espace blanc initial `!` comme un message normal.
- `src/tui/tui-local-shell.test.ts:64` enregistre le refus sans re-demander.
- `src/tui/tui-local-shell.test.ts:81` définit `OPENCLAW_SHELL` lors de l'exécution de commandes locales.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues "TUI local shell" -R openclaw/openclaw --state all --json number,title,url,state --limit 8`

Résultats :

- A retourné des rapports ouverts adjacents au TUI/mode local incluant `#86632`, mais aucun défaut direct d'approbation/exécution de shell local.

### Requêtes Discrawl

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "TUI local shell"`

Résultats :

- A retourné une discussion TUI locale sans rapports de défaut direct d'approbation/exécution de shell local.
