---
title: "Slack - Interactive Replies, App Home, and Assistant Events Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Slack - Interactive Replies, App Home, and Assistant Events Maturity Note

## Résumé

Slack supporte App Home, les événements de thread assistant, les actions de bloc, les soumissions de modal, le routage interactif détenu par le plugin, les réponses interactives Slack héritées, et les blocs de présentation partagée plus récents. La couverture est Beta car la couverture source/unité est large et les approbations natives exercent le chemin d'interaction, tandis que la preuve en direct pour App Home, les variantes d'événements assistant, et les modaux détenus par le plugin est plus mince. La qualité est affectée par des problèmes actifs autour du statut du thread d'interaction et des contrôles Slack hérités/dépréciés.

## Portée de la catégorie

Cette catégorie couvre le comportement de publication/ouverture d'App Home, les événements de thread assistant Slack démarrés/contexte modifié, les actions de bloc, les soumissions de modal, les menus d'arguments externes, le routage du gestionnaire interactif du plugin, les contrôles de présentation partagée, les directives héritées de boutons/sélection Slack, et les événements système générés par interaction.

## Fonctionnalités

- Interactive Replies : Couvre les réponses interactives sur le comportement de publication/ouverture d'App Home, les événements de thread assistant Slack démarrés/contexte modifié, les actions de bloc, les soumissions de modal, et le comportement connexe des réponses interactives, app home, et événements assistant.
- App Home : Couvre App Home sur le comportement de publication/ouverture d'App Home, les événements de thread assistant Slack démarrés/contexte modifié, les actions de bloc, les soumissions de modal, et le comportement connexe des réponses interactives, app home, et événements assistant.
- Assistant Events : Couvre les événements assistant sur le comportement de publication/ouverture d'App Home, les événements de thread assistant Slack démarrés/contexte modifié, les actions de bloc, les soumissions de modal, et le comportement connexe des réponses interactives, app home, et événements assistant.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (72%)`
- Signaux positifs : Les tests unitaires couvrent App Home, les événements assistant, les actions de bloc, les interactions, les métadonnées de modal, les réponses interactives, les limites de secours de bloc, et le routage du thread d'interaction ; les scénarios d'approbation en direct exercent les chemins de bouton Slack Block Kit.
- Signaux négatifs : La couverture en direct pour App Home, les threads d'application assistant, les modaux détenus par le plugin, les menus d'options externes, et les contrôles Slack uniquement hérités ne font pas partie de la voie en direct Slack standard.
- Lacunes d'intégration : Ajouter des scénarios en direct pour l'ouverture d'App Home, le contexte modifié du thread assistant, le statut/saisie de l'action de bloc, la soumission/fermeture du modal du plugin, les menus de sélection externes, et le secours de directive hérité.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : `#82886`, `#82895`, `#76185`, `#61374`, `#61502`, et `#12602` montrent le routage du statut d'interaction/thread et la pression des fonctionnalités Block Kit.
- Rapports Discrawl : `Slack interactive reply clicks do not show assistant status/typing` apparaît dans gitcrawl, tandis que la requête discrawl spécifique aux fonctionnalités n'a retourné aucun message d'archive Discord ciblé au-delà des discussions de commande/approbation.
- Bonnes qualités : Les docs distinguent maintenant les directives dépréciées Slack uniquement des contrôles de présentation partagée et expliquent le routage modal du plugin avec des événements système masqués.
- Mauvaises qualités : La surface mélange la syntaxe Slack uniquement ancienne, les contrôles de présentation partagée, les modaux détenus par le plugin, et les événements assistant Slack, ce qui rend les attentes des utilisateurs et l'état du routage difficiles à expliquer.
- Exclu de la qualité : Nombre de tests unitaires, largeur de voie en direct, et profondeur d'intégration.

## Score de complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/slack.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour les réponses interactives, App Home, les événements assistant.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter des scénarios en direct App Home et assistant-thread.
- Ajouter un exemple de modal détenu par le plugin avec vérification en direct de la soumission/fermeture Slack.
- Réduire la dépendance aux directives héritées `[[slack_buttons]]` et `[[slack_select]]` en faveur des contrôles de présentation partagée.

## Preuves

### Docs

- `docs/channels/slack.md` documente les champs de manifeste App Home/assistant, les réponses interactives, les soumissions de modal détenues par le plugin, le routage de rappel Block Kit, et les conseils de dépréciation pour les directives Slack uniquement.
- `docs/channels/slack.md` documente également le comportement de vue par défaut sécurisé d'App Home et le routage du thread assistant.

### Source

- `extensions/slack/src/monitor/events/home.ts`, `assistant.ts`, et `interactions.ts` gèrent App Home, les événements de thread assistant, et les interactions.
- `extensions/slack/src/monitor/events/interactions.block-actions.ts` et `interactions.modal.ts` gèrent les actions de bloc et les modaux.
- `extensions/slack/src/interactive-dispatch.ts`, `interactive-replies.ts`, `shared-interactive.test.ts`, `blocks-input.ts`, `blocks-render.ts`, et `modal-metadata.ts` implémentent le rendu interactif et la distribution du plugin.
- `extensions/slack/src/monitor/message-handler/prepare.ts` restaure le contexte du thread assistant et construit les événements système.

### Tests d'intégration

- `extensions/qa-lab/src/live-transports/slack/slack-live.runtime.ts` inclut des scénarios d'approbation natifs qui vérifient l'interface utilisateur d'approbation Slack Block Kit en attente et résolue.
- Aucun scénario en direct standard App Home, assistant, plugin-modal, ou réponse interactive héritée n'a été trouvé.

### Tests unitaires

- `extensions/slack/src/monitor/events/home.test.ts`, `assistant.test.ts`, `interactions.test.ts`, `message-subtype-handlers.test.ts`, et `system-event-test-harness.ts` couvrent la gestion des événements Slack.
- `extensions/slack/src/interactive-replies.test.ts`, `shared-interactive.test.ts`, `blocks.test.ts`, `actions.blocks.test.ts`, et `message-action-dispatch.test.ts` couvrent le rendu interactif et la distribution.
- `extensions/slack/src/monitor/message-handler/prepare.test.ts` et `prepare-thread-context.test.ts` couvrent l'intégration du contexte assistant/thread.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "slack interactive app home assistant" --json`
- `gitcrawl search openclaw/openclaw --query "Slack" --json`

Résultats :

- La requête d'interaction ciblée n'a retourné aucun résultat.
- La requête Slack large a retourné `#82886` les clics de réponse interactive manquent le statut/saisie de l'assistant, `#82895` préserver le statut du thread d'interaction, `#76185` router les événements d'action de bloc vers les sessions de thread, `#61374` réveiller les sessions pour les actions de bloc interactives, et `#12602` support Slack Block Kit pour les messages d'agent.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Slack interactive replies block actions app home assistant"`

Résultats :

- N'a retourné aucun message ciblé dans l'archive Discord. Les recherches connexes de commande et d'approbation incluent le dépannage de rappel d'interaction pour les boutons d'approbation Slack.
