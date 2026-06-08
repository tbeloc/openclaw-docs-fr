---
title: "TUI - Session Management Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# TUI - Session Management Maturity Note

## Résumé

L'UX de session TUI supporte les clés agent-scoped, la reprise de dernière session, les sélecteurs de session bornés, le chargement d'historique, la correction de session, `/new`, `/reset`, `/abort`, les mises à jour du pied de page token/status, la réconciliation d'utilisateur en attente, et l'actualisation d'historique après les événements finaux. La couverture est stable pour les transitions d'état interne. La qualité est alpha car les rapports actifs montrent que l'actualisation de session, les événements de nouvelle session visibles par hook, l'activité cross-surface, et le comportement d'auto-scroll surprennent encore les utilisateurs.

## Portée de la catégorie

Inclus dans cette catégorie :

- Cycle de vie de session : Couvre le cycle de vie de session sur la résolution de clé de session, la persistance de dernière session sélectionnée, la politique de sélecteur de session, le chargement d'historique, et le comportement associé de cycle de vie de session, d'historique et de reprise.
- Historique : Couvre l'historique sur la résolution de clé de session, la persistance de dernière session sélectionnée, la politique de sélecteur de session, le chargement d'historique, et le comportement associé de cycle de vie de session, d'historique et de reprise.
- Reprise : Couvre la reprise sur la résolution de clé de session, la persistance de dernière session sélectionnée, la politique de sélecteur de session, le chargement d'historique, et le comportement associé de cycle de vie de session, d'historique et de reprise.

## Fonctionnalités

- Cycle de vie de session : Couvre le cycle de vie de session sur la résolution de clé de session, la persistance de dernière session sélectionnée, la politique de sélecteur de session, le chargement d'historique, et le comportement associé de cycle de vie de session, d'historique et de reprise.
- Historique : Couvre l'historique sur la résolution de clé de session, la persistance de dernière session sélectionnée, la politique de sélecteur de session, le chargement d'historique, et le comportement associé de cycle de vie de session, d'historique et de reprise.
- Reprise : Couvre la reprise sur la résolution de clé de session, la persistance de dernière session sélectionnée, la politique de sélecteur de session, le chargement d'historique, et le comportement associé de cycle de vie de session, d'historique et de reprise.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (80%)`
- Signaux positifs : les actions de session, les gestionnaires de commande, les gestionnaires d'événement, la persistance de dernière session, la réessai d'historique Gateway, et les RPC de magasin de session sont bien testés.
- Signaux négatifs : la réinitialisation/actualisation cross-client, le comportement de défilement, et la redémarrage/récupération de session Gateway réelle ne sont pas prouvés de bout en bout depuis un terminal.
- Lacunes d'intégration : ajouter un scénario Gateway PTY qui reprend la dernière session, gère `/new`, reçoit une réinitialisation/changement de session externe, et vérifie l'actualisation d'historique visible.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : `gitcrawl search issues "tui session" -R openclaw/openclaw --state all --json number,title,url,state --limit 10` a retourné `#49918` pour le comportement `/new` visible par hook, `#38966` pour TUI ne s'actualisant pas lors d'une réinitialisation depuis un autre client, `#68970` pour une réponse de battement manquée après redémarrage, `#45388` pour `--session` ne diffusant pas en direct, `#51825` pour aucun indicateur d'activité sur les événements injectés par le système, `#44130` pour le comportement de saut de défilement perturbateur, et `#81781` pour la qualité de titre dérivé.
- Rapports Discrawl : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "tui session"` a retourné une discussion de version/utilisateur sur les chemins soutenus par transcription, les réponses TUI/source, et les sessions TUI intégrées locales.
- Bonnes qualités : les clés de session sont normalisées, bornées, agent-aware, et persistées sous un état scoped ; `/new` isole les sessions avec des clés spécifiques à TUI ; `/reset` utilise la réinitialisation de session backend.
- Mauvaises qualités : l'actualisation de session cross-client et la visibilité d'activité ne sont pas encore assez robustes pour prévenir un état de terminal obsolète ou trompeur dans les rapports d'utilisateurs actifs.
- Exclu de la qualité : la profondeur des tests unitaires, d'intégration, e2e, live, et de flux d'exécution.

## Score de complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/tui-and-terminal-ux.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl, et les preuves Discrawl couvrent la portée de taxonomie pour le cycle de vie de session, l'historique, la reprise.
- Signaux négatifs : la note archivée a précédé le score de complétude de version-3 de processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacune connu utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les événements de réinitialisation/changement de session cross-surface ont besoin d'un comportement de terminal plus clair.
- Le sélecteur de session et le comportement de défilement ont besoin de plus de polissage centré sur l'utilisateur pour les sessions longues.

## Preuves

### Docs

- `docs/web/tui.md:60` explique les agents et sessions, les clés de session agent-scoped, la portée globale, et la reprise de dernière session.
- `docs/web/tui.md:82` documente le sélecteur de session.
- `docs/web/tui.md:123` documente `/new`, `/reset`, `/abort`, les paramètres, et la sortie.
- `docs/cli/sessions.md:19` documente les listes de session bornées et le comportement de `Gateway sessions.list`.

### Source

- `src/tui/tui.ts:149` résout les clés de session TUI brutes en clés globales ou agent-scoped.
- `src/tui/tui-session-actions.ts:73` applique les résultats de portée agent/session backend à l'état TUI.
- `src/tui/tui-session-actions.ts:227` actualise les informations de session à partir de `sessions.list` borné.
- `src/tui/tui-session-actions.ts:297` charge l'historique, rend les messages utilisateur/assistant/outil, et mémorise les clés de session.
- `src/tui/tui-session-actions.ts:378` bascule les sessions et recharge l'historique.
- `src/tui/tui-command-handlers.ts:582` crée des sessions `tui-*` uniques pour `/new` ; `src/tui/tui-command-handlers.ts:600` réinitialise la session actuelle.

### Tests d'intégration

- `src/gateway/server.sessions.store-rpc.test.ts:35` valide la liste de session soutenue par Gateway, la correction, le nettoyage, la réinitialisation, la compaction, la suppression, et les chemins RPC associés.
- `src/tui/tui-pty-harness.e2e.test.ts:381` envoie plusieurs invites dans l'ordre à travers la boucle de terminal.

### Tests unitaires

- `src/tui/tui-session-actions.test.ts:60` vérifie les actualisations de session en file d'attente.
- `src/tui/tui-session-actions.test.ts:549` mémorise les sessions sélectionnées après le chargement d'historique.
- `src/tui/tui-last-session.test.ts:26` persiste la dernière session sous une clé hachée scoped.
- `src/tui/tui-event-handlers.test.ts:692` actualise l'historique après un chat final non-local.
- `src/tui/tui-command-handlers.test.ts:436` couvre `/new` et `/reset`.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues "tui session" -R openclaw/openclaw --state all --json number,title,url,state --limit 10`

Résultats :

- A retourné 10 rapports ouverts, incluant `#49918`, `#38966`, `#68970`, `#45388`, `#51825`, `#44130`, et `#81781`.

### Requêtes Discrawl

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "tui session"`

Résultats :

- A retourné une discussion de version/utilisateur référençant les chemins soutenus par transcription, la relecture CLI/TUI, et la sortie de session TUI intégrée localement.
