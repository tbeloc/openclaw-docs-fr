---
title: "TUI - Note de maturité de la sécurité du rendu et de la sortie"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# TUI - Note de maturité de la sécurité du rendu et de la sortie

## Résumé

L'interface TUI dispose d'un pipeline de rendu riche pour les deltas/finales de l'assistant, la visibilité de la réflexion, les cartes d'appels d'outils, l'expansion de la sortie d'outils, les chiens de garde de streaming, les mises à jour du modèle de secours, les résultats locaux `/btw`, les réponses source et le texte d'erreur désinfecté. La couverture est l'une des parties les plus fortes de l'interface TUI. La qualité est encore en version bêta car les rapports actifs se concentrent autour de l'état du chien de garde de streaming, du streaming en direct via `--session`, des flux Gateway/fournisseur mis en mémoire tampon et des médias en ligne manquants.

## Portée de la catégorie

Inclus dans cette catégorie :

- Rendu des messages en streaming : couvre le rendu des messages en streaming dans le rendu du journal de chat, l'assemblage du flux de l'assistant, la résolution finale/erreur, la visibilité de la réflexion et le comportement connexe du rendu des messages en streaming et des cartes d'outils.
- Cartes d'outils : couvre les cartes d'outils dans le rendu du journal de chat, l'assemblage du flux de l'assistant, la résolution finale/erreur, la visibilité de la réflexion et le comportement connexe du rendu des messages en streaming et des cartes d'outils.
- Primitives de rendu terminal : couvre les primitives de rendu terminal dans les assistants de sortie terminal partagés utilisés par les surfaces CLI/TUI : écriture de flux sécurisée, désinfection de texte, gestion ANSI/OSC, enveloppe de tableau et le comportement connexe des primitives de rendu terminal et de la sécurité de sortie.
- Sécurité de sortie : couvre la sécurité de sortie dans les assistants de sortie terminal partagés utilisés par les surfaces CLI/TUI : écriture de flux sécurisée, désinfection de texte, gestion ANSI/OSC, enveloppe de tableau et le comportement connexe des primitives de rendu terminal et de la sécurité de sortie.

## Fonctionnalités

- Rendu des messages en streaming : couvre le rendu des messages en streaming dans le rendu du journal de chat, l'assemblage du flux de l'assistant, la résolution finale/erreur, la visibilité de la réflexion et le comportement connexe du rendu des messages en streaming et des cartes d'outils.
- Cartes d'outils : couvre les cartes d'outils dans le rendu du journal de chat, l'assemblage du flux de l'assistant, la résolution finale/erreur, la visibilité de la réflexion et le comportement connexe du rendu des messages en streaming et des cartes d'outils.
- Primitives de rendu terminal : couvre les primitives de rendu terminal dans les assistants de sortie terminal partagés utilisés par les surfaces CLI/TUI : écriture de flux sécurisée, désinfection de texte, gestion ANSI/OSC, enveloppe de tableau et le comportement connexe des primitives de rendu terminal et de la sécurité de sortie.
- Sécurité de sortie : couvre la sécurité de sortie dans les assistants de sortie terminal partagés utilisés par les surfaces CLI/TUI : écriture de flux sécurisée, désinfection de texte, gestion ANSI/OSC, enveloppe de tableau et le comportement connexe des primitives de rendu terminal et de la sécurité de sortie.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs : les gestionnaires d'événements et les formateurs disposent de tests unitaires étendus, les tests PTY couvrent les réponses source et les erreurs de fournisseur préservées, et l'assembleur de flux gère la réconciliation delta/finale.
- Signaux négatifs : le comportement complet du streaming Gateway/fournisseur est représenté par des mocks et des tests unitaires spécifiques aux problèmes plutôt que par des preuves terminales de fournisseur en direct récurrentes.
- Lacunes d'intégration : ajouter une preuve PTY Gateway-v4 en direct ou synthétique couvrant les événements delta uniquement, les mises à jour d'outils, les espaces réservés de médias en ligne, le basculement de fournisseur et la reconnexion.

## Score de qualité

- Score : `Bêta (70%)`
- Rapports Gitcrawl : `gitcrawl search issues "tui stream" -R openclaw/openclaw --state all --json number,title,url,state --limit 10` a retourné `#45388` pour `--session` ne pas faire de streaming en direct, `#78360` pour le chien de garde de streaming marquant les exécutions actives silencieuses comme inactives, `#82988` pour les événements d'assistant delta uniquement ignorés par Gateway/TUI intégré, `#57592` pour l'affichage d'image terminal en ligne, `#86050` pour les flux claude-cli mis en mémoire tampon, et `#67052` pour les indicateurs de streaming obsolètes.
- Rapports Discrawl : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "tui stream"` a retourné les notes de version et les discussions utilisateur sur les réponses source, la gestion des transcriptions/sources TUI et un échec de chien de garde TUI intégré local sans streaming.
- Bonnes qualités : les cartes d'outils utilisent des aperçus limités, les contrôles de verbosité des outils exposent la sortie, la réconciliation de texte final gère les fragments malformés et les avis de chien de garde évitent les états silencieusement inactifs.
- Mauvaises qualités : la piste de problèmes actifs montre que la correction du streaming et la sémantique du statut sont toujours le risque de fiabilité TUI le plus visible.
- Exclu de la qualité : profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/tui-and-terminal-ux.md`.
- Signaux positifs : les documents archivés, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour le rendu des messages en streaming, les cartes d'outils, les primitives de rendu terminal et la sécurité de sortie.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le support des images en ligne pour les terminaux modernes est toujours une lacune de fonctionnalité.
- La sémantique du statut de streaming a toujours besoin d'être affinée pour les exécutions actives silencieuses et la mise en mémoire tampon du fournisseur/client.

## Preuves

### Docs

- `docs/web/tui.md:186` documente les cartes d'outils, l'expansion Ctrl+O et les mises à jour partielles d'outils.
- `docs/web/tui.md:198` documente le chargement de l'historique, le streaming en place et les cartes d'outils plus riches.
- `docs/web/tui.md:52` décrit les champs du journal de chat, de la ligne d'état et du pied de page.

### Source

- `src/tui/components/chat-log.ts:18` suit les messages système, utilisateur, assistant, outil, en attente et `/btw`.
- `src/tui/components/chat-log.ts:253` démarre et met à jour les composants d'assistant en streaming.
- `src/tui/components/tool-execution.ts:55` rend les cartes d'outils avec arguments, aperçus, erreurs et sortie développée.
- `src/tui/tui-stream-assembler.ts:103` assemble les deltas de réflexion/contenu et les messages finaux par exécution.
- `src/tui/tui-event-handlers.ts:471` gère les événements delta de chat, arme le chien de garde et met à jour le texte de l'assistant.
- `src/tui/tui-event-handlers.ts:584` gère les événements d'outil d'agent selon les paramètres de sortie verbeux/complets.

### Tests d'intégration

- `src/tui/tui-pty-harness.e2e.test.ts:397` rend les réponses source de l'interface utilisateur interne message-outil uniquement dans le terminal.
- `src/tui/tui-pty-harness.e2e.test.ts:415` préserve les erreurs de limite de compte xAI dans la sortie du terminal.

### Tests unitaires

- `src/tui/tui-event-handlers.test.ts:588` accepte les événements d'outil après la finale du chat pour la même exécution.
- `src/tui/tui-event-handlers.test.ts:1211` couvre le chien de garde de streaming.
- `src/tui/tui-stream-assembler.test.ts` couvre l'assemblage des messages d'assistant en streaming/final.
- `src/tui/tui-formatters.test.ts:11` couvre la préférence de réponse finale, les erreurs de flux malformés, la désinfection ANSI/contrôle, l'extraction de réflexion et la gestion des jetons longs.
- `src/tui/components/chat-log.test.ts` couvre le comportement de rendu du journal de chat.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues "tui stream" -R openclaw/openclaw --state all --json number,title,url,state --limit 10`

Résultats :

- A retourné 10 rapports ouverts, y compris `#45388`, `#78360`, `#82988`, `#57592`, `#86050` et `#67052`.

### Requêtes Discrawl

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "tui stream"`

Résultats :

- A retourné les notes de version et les discussions utilisateur couvrant les réponses source dans WebChat/TUI, la gestion des transcriptions/sources TUI et un échec du chien de garde TUI intégré local sans streaming.
