---
title: "Slack - Native Approvals, Actions, and Security-sensitive Ops Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Slack - Native Approvals, Actions, and Security-sensitive Ops Maturity Note

## Résumé

Slack dispose d'une surface d'approbation et d'action native substantielle : boutons d'approbation exec/plugin, routage des approbateurs, livraison origine/DM/canal, `/approve` dans le même chat, actions de lecture/édition/suppression/épinglage/réaction/membre/emoji, sélection de jetons pour les lectures/écritures et portes d'action. La couverture est Beta car des scénarios d'approbation native en direct existent, mais de nombreux groupes d'actions Slack ne sont pas contrôlés en direct. La qualité reste Beta car les archives montrent une confusion de rappel d'approbation, des pièges de `/approve` de secours et des risques d'autorisation de cible non résolus pour les DM sortants.

## Portée de la catégorie

Cette catégorie couvre les approbations exec et plugin natives de Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation, le comportement de secours d'approbation, les actions de message Slack, les opérations de lecture/téléchargement/édition/suppression/épinglage/réaction/info-membre/liste-emoji, les portes d'action et la politique de jeton/jeton utilisateur.

## Fonctionnalités

- Approbations natives : couvre les approbations natives dans les approbations exec et plugin natives de Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation et le comportement d'approbations, d'actions et d'opérations sensibles à la sécurité natives associées.
- Actions : couvre les actions dans les approbations exec et plugin natives de Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation et le comportement d'approbations, d'actions et d'opérations sensibles à la sécurité natives associées.
- Opérations sensibles à la sécurité : couvre les opérations sensibles à la sécurité dans les approbations exec et plugin natives de Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation et le comportement d'approbations, d'actions et d'opérations sensibles à la sécurité natives associées.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (75%)`
- Signaux positifs : des scénarios d'approbation exec et plugin en direct existent ; la source et les tests couvrent les abonnements d'approbation, le rendu, l'authentification, les cibles d'origine, les filtres de compte, la suppression de secours de plugin et de nombreuses portes d'exécution d'action.
- Signaux négatifs : la preuve en direct est plus mince pour les actions destructrices, les limites de portée de lecture/téléchargement, les opérations de réaction/épinglage, les actions de membre/emoji et le routage d'approbation entre comptes.
- Lacunes d'intégration : ajouter des scénarios d'action en direct pour lecture/édition/suppression/épinglage/réaction/téléchargement-fichier, tentatives d'action non autorisées, cibles d'approbation entre comptes et gestion des défaillances de clic de bouton Slack.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : `#81901`, `#76185`, `#82240`, `#78793`, `#86983` et `#7234` indiquent le contexte d'approbation, le threading d'interaction, la charge utile d'approbation de plugin, le texte de secours, l'autorisation DM sortante et les préoccupations de granularité de porte d'action.
- Rapports Discrawl : un fil de support d'approbations Slack montre des utilisateurs confondant `capabilities.interactiveReplies` avec `execApprovals`, s'attendant à ce que `/approve` nu fonctionne en mode commande unique et ayant besoin de vérifications de plomberie de rappel.
- Bonnes qualités : le code d'approbation distingue les approbateurs exec par rapport aux plugin, supprime le secours générique uniquement lorsque la livraison native peut le gérer et documente le comportement de secours manuel.
- Mauvaises qualités : l'UX d'approbation a plusieurs commutateurs portant des noms similaires, le secours manuel Slack diffère entre `/openclaw /approve` et `/approve` natif, et les groupes d'actions mélangent toujours les lectures sûres avec les opérations destructrices derrière une activation grossière.
- Exclu de la qualité : nombre de tests unitaires, largeur de voie en direct et profondeur d'intégration.

## Score de complétude

- Score : `Beta (75%)`
- Instructions de surface : évaluées par rapport à `references/completeness/slack.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour les approbations natives, les actions et les opérations sensibles à la sécurité.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter des diagnostics d'opérateur qui expliquent pourquoi un clic sur un bouton d'approbation n'a pas atteint la porte.
- Diviser les portes d'action plus granuleirement pour les opérations Slack destructrices par rapport à la lecture seule.
- Ajouter une liste d'autorisation DM sortante ou une autorisation de cible avant que les agents puissent initier des DM utilisateur Slack arbitraires.

## Preuves

### Docs

- `docs/channels/slack.md` documente les actions et les portes, les approbations natives, le routage d'approbation exec/plugin, le `/approve` dans le même chat, les chemins de configuration des approbateurs, le comportement auto du client natif et les avertissements de secours d'approbation Slack.
- `docs/tools/exec-approvals.md` et `docs/tools/exec-approvals-advanced.md` sont des références d'approbation partagées liées.

### Source

- `extensions/slack/src/approval-native.ts`, `approval-auth.ts`, `approval-handler.runtime.ts`, `exec-approvals.ts` et `approval-native-gates.ts` implémentent les approbations natives Slack et l'authentification.
- `extensions/slack/src/action-runtime.ts`, `actions.ts`, `channel-actions.ts`, `message-actions.ts` et `message-action-dispatch.ts` implémentent les actions Slack et la distribution d'actions.
- `extensions/slack/src/channel.ts` expose les capacités d'action et la sélection de jetons à la surface du plugin de canal partagé.

### Tests d'intégration

- `extensions/qa-lab/src/live-transports/slack/slack-live.runtime.ts` inclut `slack-approval-exec-native` et `slack-approval-plugin-native`.
- `extensions/qa-lab/src/live-transports/slack/slack-live.runtime.test.ts` vérifie la sélection de scénario d'approbation native, la configuration d'approbation, l'extraction de valeur de bouton, la preuve de point de contrôle et la rédaction.

### Tests unitaires

- `extensions/slack/src/approval-native.test.ts`, `approval-auth.test.ts`, `approval-handler.runtime.test.ts` et `exec-approvals.test.ts` couvrent le routage et le rendu d'approbation native.
- `extensions/slack/src/action-runtime.test.ts` couvre les réactions, le téléchargement de fichier, le téléchargement de fichier, l'édition, la lecture, l'épinglage, la sélection de jeton et le rejet de liste d'autorisation.
- `extensions/slack/src/actions.read.test.ts`, `actions.reactions.test.ts`, `actions.download-file.test.ts`, `message-tools.test.ts` et `message-action-dispatch.test.ts` couvrent les détails d'action.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "slack approval" --json`
- `gitcrawl search openclaw/openclaw --query "slack actions reactions pins read delete" --json`

Résultats :

- La recherche d'approbation a retourné `#81901`, `#76185`, `#82240`, `#78793` et les problèmes d'approbation médiatisés par canal associés.
- La recherche d'action a retourné `#7234`, notant que Slack a déjà des commutateurs séparés pour les réactions, les épingles, les infos de membre et la liste d'emoji tandis que les portes d'action Discord restent moins granuleuses.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Slack approvals execApprovals approve buttons"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Slack actions reactions pins read delete"`

Résultats :

- La requête d'approbation a retourné un fil de support où les boutons d'approbation Slack ont été rendus mais ne se sont pas propagés, avec des conseils sur `execApprovals`, `/openclaw /approve`, les commandes natives et la plomberie de rappel.
- La requête d'action a retourné une sortie de capacité listant le support Slack pour direct/canal/thread, réactions, médias, commandes natives, envoi/diffusion/réaction/lecture/édition/suppression/téléchargement-fichier/épinglage/info-membre/liste-emoji.
