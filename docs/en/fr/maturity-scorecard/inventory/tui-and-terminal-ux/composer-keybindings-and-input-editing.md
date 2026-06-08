---
title: "TUI - Note de maturité des entrées et commandes"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# TUI - Note de maturité des entrées et commandes

## Résumé

Le chemin d'entrée TUI couvre les messages normaux, les commandes slash, les lignes de shell local, l'historique, la préservation des brouillons lors de soumissions occupées, la coalescence des rafales de collage, l'entrée AltGr/Kitty CSI-u, et les raccourcis clavier documentés. La couverture est large au niveau unitaire et dispose d'une preuve d'entrée typée PTY. La qualité est bêta car la soumission multiligne, les liaisons de touches d'envoi configurables, la convivialité IME et le comportement d'entrée multi-terminal ont toujours des rapports actifs côté utilisateur.

## Portée de la catégorie

Inclus dans cette catégorie :

- Composition de messages : Couvre la composition de messages dans l'éditeur, le gestionnaire de soumission, l'historique d'entrée, le routage slash/shell local, le comportement de soumission occupée, le repli de collage, la déduplication de retour arrière, les raccourcis Ctrl/Esc, la gestion AltGr et les raccourcis clavier documentés.
- Historique d'entrée : Couvre l'historique d'entrée dans l'éditeur, le gestionnaire de soumission, l'historique d'entrée, le routage slash/shell local, le comportement de soumission occupée, le repli de collage, la déduplication de retour arrière, les raccourcis Ctrl/Esc, la gestion AltGr et les raccourcis clavier documentés.
- Raccourcis clavier : Couvre les raccourcis clavier dans l'éditeur, le gestionnaire de soumission, l'historique d'entrée, le routage slash/shell local, le comportement de soumission occupée, le repli de collage, la déduplication de retour arrière, les raccourcis Ctrl/Esc, la gestion AltGr et les raccourcis clavier documentés.
- Gestion du collage et de la soumission occupée : Couvre la gestion du collage et de la soumission occupée dans l'éditeur, le gestionnaire de soumission, l'historique d'entrée, le routage slash/shell local, le comportement de soumission occupée, le repli de collage, la déduplication de retour arrière, les raccourcis Ctrl/Esc, la gestion AltGr et les raccourcis clavier documentés.
- Gestion IME et AltGr : Couvre la gestion IME et AltGr dans l'éditeur, le gestionnaire de soumission, l'historique d'entrée, le routage slash/shell local, le comportement de soumission occupée, le repli de collage, la déduplication de retour arrière, les raccourcis Ctrl/Esc, la gestion AltGr et les raccourcis clavier documentés.
- Commandes Slash : Couvre les commandes Slash dans l'analyse des commandes slash, le transfert de commandes, les commandes locales uniquement, les sélecteurs de modèle/agent/session, la superposition des paramètres, le sélecteur de mode de contexte, la liste de commandes Gateway dynamique, les commandes de patch de session et la documentation des commandes.
- Sélecteurs : Couvre les sélecteurs dans l'analyse des commandes slash, le transfert de commandes, les commandes locales uniquement, les sélecteurs de modèle/agent/session, la superposition des paramètres, le sélecteur de mode de contexte, la liste de commandes Gateway dynamique, les commandes de patch de session et la documentation des commandes.
- Paramètres : Couvre les paramètres dans l'analyse des commandes slash, le transfert de commandes, les commandes locales uniquement, les sélecteurs de modèle/agent/session, la superposition des paramètres, le sélecteur de mode de contexte, la liste de commandes Gateway dynamique, les commandes de patch de session et la documentation des commandes.

## Fonctionnalités

- Composition de messages : Couvre la composition de messages dans l'éditeur, le gestionnaire de soumission, l'historique d'entrée, le routage slash/shell local, le comportement de soumission occupée, le repli de collage, la déduplication de retour arrière, les raccourcis Ctrl/Esc, la gestion AltGr et les raccourcis clavier documentés.
- Historique d'entrée : Couvre l'historique d'entrée dans l'éditeur, le gestionnaire de soumission, l'historique d'entrée, le routage slash/shell local, le comportement de soumission occupée, le repli de collage, la déduplication de retour arrière, les raccourcis Ctrl/Esc, la gestion AltGr et les raccourcis clavier documentés.
- Raccourcis clavier : Couvre les raccourcis clavier dans l'éditeur, le gestionnaire de soumission, l'historique d'entrée, le routage slash/shell local, le comportement de soumission occupée, le repli de collage, la déduplication de retour arrière, les raccourcis Ctrl/Esc, la gestion AltGr et les raccourcis clavier documentés.
- Gestion du collage et de la soumission occupée : Couvre la gestion du collage et de la soumission occupée dans l'éditeur, le gestionnaire de soumission, l'historique d'entrée, le routage slash/shell local, le comportement de soumission occupée, le repli de collage, la déduplication de retour arrière, les raccourcis Ctrl/Esc, la gestion AltGr et les raccourcis clavier documentés.
- Gestion IME et AltGr : Couvre la gestion IME et AltGr dans l'éditeur, le gestionnaire de soumission, l'historique d'entrée, le routage slash/shell local, le comportement de soumission occupée, le repli de collage, la déduplication de retour arrière, les raccourcis Ctrl/Esc, la gestion AltGr et les raccourcis clavier documentés.
- Commandes Slash : Couvre les commandes Slash dans l'analyse des commandes slash, le transfert de commandes, les commandes locales uniquement, les sélecteurs de modèle/agent/session, la superposition des paramètres, le sélecteur de mode de contexte, la liste de commandes Gateway dynamique, les commandes de patch de session et la documentation des commandes.
- Sélecteurs : Couvre les sélecteurs dans l'analyse des commandes slash, le transfert de commandes, les commandes locales uniquement, les sélecteurs de modèle/agent/session, la superposition des paramètres, le sélecteur de mode de contexte, la liste de commandes Gateway dynamique, les commandes de patch de session et la documentation des commandes.
- Paramètres : Couvre les paramètres dans l'analyse des commandes slash, le transfert de commandes, les commandes locales uniquement, les sélecteurs de modèle/agent/session, la superposition des paramètres, le sélecteur de mode de contexte, la liste de commandes Gateway dynamique, les commandes de patch de session et la documentation des commandes.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (76%)`
- Signaux positifs : routage de soumission, historique, préservation des brouillons en état occupé, coalescence de collage, gestionnaires de touches personnalisés, décodage AltGr et entrée typée PTY sont couverts.
- Signaux négatifs : comportement IME multi-terminal, touches d'envoi/nouvelle ligne configurables et variantes réelles de terminal CJK/AltGr ne sont pas prouvées de manière exhaustive.
- Lacunes d'intégration : ajouter des scénarios PTY pour l'entrée multiligne, le comportement Shift+Entrée ou de la touche d'envoi configurée, et au moins un chemin d'encodage de terminal qui a précédemment cassé l'entrée IME/AltGr.

## Score de qualité

- Score : `Bêta (70%)`
- Rapports Gitcrawl : `gitcrawl search issues "Shift Enter newline TUI" -R openclaw/openclaw --state all --json number,title,url,state --limit 8` a retourné l'ouverture `#10118`, qui suit la nouvelle ligne Shift+Entrée, Ctrl+Entrée configurable et le comportement convivial IME.
- Rapports Discrawl : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "Shift Enter newline TUI"` a retourné une discussion selon laquelle le comportement Shift+Entrée principal peut exister via pi-tui, mais les liaisons de touches visibles/configurables et le comportement convivial IME manquent toujours.
- Bonnes qualités : l'éditeur préserve les brouillons lorsqu'il est occupé, reconnaît les raccourcis importants, route `!` uniquement lorsqu'il s'agit du premier caractère brut, et gère plusieurs cas limites de collage/AltGr spécifiques à la plateforme.
- Mauvaises qualités : l'ensemble de raccourcis documenté n'est pas encore configurable, l'ergonomie nouvelle ligne/envoi reste ouverte, et le signal d'archive montre que les utilisateurs considèrent les envois accidentels d'Entrée comme une friction élevée.
- Exclu de la qualité : profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution.

## Score de complétude

- Score : `Bêta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/tui-and-terminal-ux.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la composition de messages, l'historique d'entrée, les raccourcis clavier, la gestion du collage et de la soumission occupée, la gestion IME et AltGr, les commandes Slash, les sélecteurs, les paramètres.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les liaisons de touches d'envoi/nouvelle ligne configurables ne sont pas un contrat utilisateur établi.
- Le comportement d'entrée multi-terminal est toujours largement déduit des fixtures unitaires plutôt que d'une preuve réelle de matrice de terminal.

## Preuves

### Docs

- `docs/web/tui.md:89` répertorie les raccourcis clavier d'Entrée à Ctrl+T.
- `docs/web/tui.md:52` décrit l'entrée comme un éditeur de texte avec autocomplétion.
- `docs/web/tui.md:136` documente le routage du shell local `!` et la règle selon laquelle les espaces de début ne déclenchent pas l'exécution locale.

### Source

- `src/tui/components/custom-editor.ts:42` implémente `CustomEditor` avec des rappels de raccourcis.
- `src/tui/components/custom-editor.ts:55` gère Alt+Entrée, Alt+Haut, Ctrl+L/O/P/G/T, Shift+Tab, Esc, Ctrl+C, Ctrl+D et l'entrée imprimable AltGr.
- `src/tui/tui-submit.ts:3` route les soumissions vers les chemins shell local, commande slash ou envoi de chat.
- `src/tui/tui-submit.ts:55` active la coalescence de rafales de collage spécifique à la plateforme.
- `src/tui/tui.ts:216` déduplique l'entrée de retour arrière rapide.

### Tests d'intégration

- `src/tui/tui-pty-harness.e2e.test.ts:368` pilote la boucle de terminal réelle via l'entrée typée.
- `src/tui/tui-pty-harness.e2e.test.ts:429` vérifie que les messages normaux qui se chevauchent sont bloqués pendant qu'une exécution est occupée.

### Tests unitaires

- `src/tui/tui-input-history.test.ts:4` vérifie que les messages soumis, les commandes slash et les lignes préfixées par bang entrent dans les routes et l'historique corrects.
- `src/tui/tui.submit-handler.test.ts:79` préserve la valeur réelle de l'éditeur après une soumission occupée.
- `src/tui/tui.submit-handler.test.ts:127` couvre la coalescence de collage monolignes rapides.
- `src/tui/components/custom-editor.test.ts:33` insère l'entrée imprimable AltGr allemande Kitty CSI-u.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues "Shift Enter newline TUI" -R openclaw/openclaw --state all --json number,title,url,state --limit 8`

Résultats :

- A retourné l'ouverture `#10118` pour la nouvelle ligne Shift+Entrée et le comportement de touche d'envoi configurable.

### Requêtes Discrawl

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "Shift Enter newline TUI"`

Résultats :

- A retourné une discussion de problème notant les lacunes restantes en matière de configurabilité et de comportement convivial IME.
