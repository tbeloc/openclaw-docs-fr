---
title: "Microsoft Teams - Native Controls and Approvals Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Microsoft Teams - Native Controls and Approvals Maturity Note

## Résumé

Teams expose une large surface d'actions de messages : téléchargement de fichiers, sondages, lecture/recherche,
modification/suppression, épingles, réactions, informations sur les membres, gestion de groupe, authentification d'approbation et
retours d'information. La couverture reste Alpha car ces actions sont principalement soutenues par des sources et des tests unitaires. La qualité reste Alpha car les permissions Graph, le routage cible,
les invocations de cartes et la livraison native des approbations Teams nécessitent une preuve réelle sur plusieurs locataires dans les états
de chat, canal, équipe et consentement administrateur.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Native Controls and Approvals`
- Fusionnée à partir de : `Message Actions and Approvals`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Découverte d'actions de message : Couvre la découverte d'actions de message sur la découverte d'outils de message, téléchargement de fichiers, sondages, lecture/recherche et comportements d'actions et d'approbations connexes.
- Sondages et réactions : Couvre les sondages et réactions sur la découverte d'outils de message, téléchargement de fichiers, sondages, lecture/recherche et comportements d'actions et d'approbations connexes.
- Lecture, modification, suppression et épingle : Couvre la lecture, modification, suppression et épingle sur la découverte d'outils de message, téléchargement de fichiers, sondages, lecture/recherche et comportements d'actions et d'approbations connexes.
- Cartes d'approbation natives : Couvre les cartes d'approbation natives sur la découverte d'outils de message, téléchargement de fichiers, sondages, lecture/recherche et comportements d'actions et d'approbations connexes.
- Retours d'information et actions de groupe : Couvre les retours d'information et actions de groupe sur la découverte d'outils de message, téléchargement de fichiers, sondages, lecture/recherche et comportements d'actions et d'approbations connexes.

## Fonctionnalités

- Découverte d'actions de message : Couvre la découverte d'actions de message sur la découverte d'outils de message, téléchargement de fichiers, sondages, lecture/recherche et comportements d'actions et d'approbations connexes.
- Sondages et réactions : Couvre les sondages et réactions sur la découverte d'outils de message, téléchargement de fichiers, sondages, lecture/recherche et comportements d'actions et d'approbations connexes.
- Lecture, modification, suppression et épingle : Couvre la lecture, modification, suppression et épingle sur la découverte d'outils de message, téléchargement de fichiers, sondages, lecture/recherche et comportements d'actions et d'approbations connexes.
- Cartes d'approbation natives : Couvre les cartes d'approbation natives sur la découverte d'outils de message, téléchargement de fichiers, sondages, lecture/recherche et comportements d'actions et d'approbations connexes.
- Retours d'information et actions de groupe : Couvre les retours d'information et actions de groupe sur la découverte d'outils de message, téléchargement de fichiers, sondages, lecture/recherche et comportements d'actions et d'approbations connexes.

## Fraîcheur des archives

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (64%)`
- Signaux positifs : Les tests source et unitaires couvrent la découverte d'actions, le repli cible, le téléchargement de fichiers, les sondages, les réactions, la liste/info des canaux, l'épingle/dépingle,
  les cartes de présentation, l'authentification d'approbation et les adaptateurs d'exécution de gestion de groupe.
- Signaux négatifs : Aucun scénario d'action, réaction, sondage, approbation ou gestion de groupe Teams en direct n'a été trouvé.
- Lacunes d'intégration : Preuve de locataire réelle manquante pour les états de permission Graph refusée,
  les invocations d'actions de cartes, la livraison native d'approbations, les votes de sondages, les réactions
  et les opérations d'adhésion à un groupe.

## Score de qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl : La recherche de problèmes `msteams approval feedback poll adaptive card OAuth SSO`
  a retourné `[]` ; les requêtes plus larges ont retourné `#66327` cartes d'approbation interactives et `#76262` migration du SDK Teams avec corrections de cartes/retours d'information.
- Rapports Discrawl : La requête d'approbation/sondage/retour d'information ciblée n'a retourné aucune ligne ;
  la recherche large `msteams` incluait une discussion de migration sur les boutons de cartes adaptatives, les retours d'information et les corrections d'édition/suppression.
- Bonnes qualités : Les actions de message sont annoncées de manière centralisée, la résolution cible
  est explicite, l'authentification d'approbation normalise les utilisateurs Teams stables, les votes de sondages valident
  les ID de conversation et les adaptateurs d'exécution Graph séparent les opérations privilégiées.
- Mauvaises qualités : Les actions sont sensibles aux permissions Graph, la livraison d'approbation n'est
  pas prouvée comme un scénario Teams natif, les invocations de cartes sont sensibles à la sécurité
  et le comportement réel de l'interface utilisateur Teams n'est pas représenté par une preuve de scénario durable.
- Exclu de la qualité : Largeur des tests unitaires d'actions, profondeur des tests de cartes et manque de tests de locataires en direct.

## Score de complétude

- Score : `Alpha (64%)`
- Instructions de surface : évaluées par rapport à `references/completeness/microsoft-teams.md`.
- Signaux positifs : Les archives de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la découverte d'actions de message, les sondages et réactions, la lecture, modification, suppression et épingle, les cartes d'approbation natives, les retours d'information et actions de groupe.
- Signaux négatifs : la note archivée a précédé le scoring de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter des scénarios en direct pour les sondages, réactions, livraison native d'approbations, retours d'information,
  épingle/dépingle, édition/suppression, recherche/lecture, téléchargement de fichiers et gestion de groupe.
- Ajouter une preuve de scénario de permission refusée et consentement partiel pour chaque groupe d'actions soutenu par Graph.
- Ajouter une preuve de flux d'approbation de carte d'approbation et de repli dans un locataire Teams réel.

## Preuve

### Documentation

- `docs/channels/msteams.md` documente les sondages, cartes de présentation, actions de message,
  formats cibles, exigences Graph/informations sur les membres et téléchargement de fichiers.
- `docs/tools/exec-approvals-advanced.md` mentionne Microsoft Teams parmi les surfaces d'approbation de chat livrables.

### Source

- `extensions/msteams/src/channel.ts` annonce les actions incluant
  `upload-file`, `poll`, lecture/recherche/édition/suppression/épingle/réactions, liste/info des canaux, gestion de groupe et `member-info`, et achemine la gestion des actions.
- `extensions/msteams/src/channel.runtime.ts` exporte les adaptateurs d'exécution pour
  les messages Graph, les équipes Graph, les membres Graph, la gestion de groupe, sortant, sonde,
  et les fonctions d'envoi/carte.
- `extensions/msteams/src/polls.ts` construit les cartes de sondage et enregistre les votes.
- `extensions/msteams/src/monitor.ts` gère les actions de cartes de sondage et les actions de cartes génériques.
- `extensions/msteams/src/approval-auth.ts` implémente l'authentification d'approbation Teams ;
  ce n'est pas la même chose qu'une preuve durable de livraison d'approbation native.
- `extensions/msteams/src/feedback-invoke.ts`,
  `feedback-reflection.ts` et `feedback-reflection-store.ts` implémentent
  les retours d'information et la réflexion.
- `extensions/msteams/src/graph-messages.ts` et
  `graph-group-management.ts` implémentent les actions soutenues par Graph.

### Tests d'intégration

- Aucun scénario d'action/réaction/sondage/approbation/gestion de groupe Teams en direct n'a
  été trouvé par `rg`.

### Tests unitaires

- `extensions/msteams/src/channel.actions.test.ts` couvre la découverte d'actions,
  le repli cible, le téléchargement de fichiers, les informations sur les membres, la liste/info des canaux, l'épingle/dépingle,
  les réactions et les ID de canaux natifs.
- `extensions/msteams/src/polls.test.ts` couvre les cartes de sondage et la sélection de votes.
- `extensions/msteams/src/monitor-handler.adaptive-card.test.ts` et
  `monitor.lifecycle.test.ts` couvrent la gestion des invocations de cartes.
- `extensions/msteams/src/channel.test.ts` couvre l'exposition de la capacité d'approbation.
- `extensions/msteams/src/graph-messages.actions.test.ts`,
  `graph-messages.read.test.ts`, `graph-messages.search.test.ts`,
  `graph-group-management.test.ts` et `feedback-reflection.test.ts` couvrent
  le comportement Graph/action simulé.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "msteams Teams approval feedback poll adaptive card OAuth SSO" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10`
- `gitcrawl search openclaw/openclaw --query "msteams adaptive card approvals feedback poll action" --json --limit 10`
- `gitcrawl search openclaw/openclaw --query "msteams Microsoft Teams" --json --limit 10`

Résultats :

- Les recherches de problèmes et de mots-clés d'actions ciblées ont retourné `[]`.
- La recherche large a retourné `#66327`, cartes d'approbation interactives, et `#76262`,
  migration du SDK Teams avec extraits de cartes adaptatives/retours d'information.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "msteams approval poll feedback reaction Adaptive Card"`

Résultats :

- La requête ciblée n'a retourné aucune ligne.
