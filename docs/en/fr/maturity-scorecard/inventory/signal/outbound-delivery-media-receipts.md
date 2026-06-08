---
title: "Signal - Note de Maturité Media et Contenu Enrichi"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Signal - Note de Maturité Media et Contenu Enrichi

## Résumé

Cette note migre les preuves de maturité archivées pour `Signal` / `Outbound Delivery, Media, Receipts, and Typing` dans l'inventaire de scorecard actuel process-version-3.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Media and Rich Content`
- Fusionnée à partir de : `Message Delivery and Actions`
- Report de score : minimum conservateur des scores de la catégorie source fusionnée.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Cibles de livraison de texte : Couvre le routage des cibles de livraison de texte, la liaison de session, l'historique et le contexte de conversation pour Outbound Delivery, Media, Receipts, and Typing.
- Livraison et limites des médias : Couvre le routage de la livraison et des limites des médias, la liaison de session, l'historique et le contexte de conversation pour Outbound Delivery, Media, Receipts, and Typing.
- Indicateurs de saisie et accusés de lecture : Couvre le routage des indicateurs de saisie et des accusés de lecture, la liaison de session, l'historique et le contexte de conversation pour Outbound Delivery, Media, Receipts, and Typing.
- Sortie stylisée/fragmentée : Couvre le routage de la sortie stylisée/fragmentée, la liaison de session, l'historique et le contexte de conversation pour Outbound Delivery, Media, Receipts, and Typing.
- Découverte d'action de réaction : Couvre le routage de la découverte d'action de réaction, la liaison de session, l'historique et le contexte de conversation pour Reactions Message Tool.
- Ajouter/supprimer des réactions : Couvre le routage de l'ajout/suppression de réactions, la liaison de session, l'historique et le contexte de conversation pour Reactions Message Tool.
- Ciblage de réaction de groupe : Couvre le routage du ciblage de réaction de groupe, la liaison de session, l'historique et le contexte de conversation pour Reactions Message Tool.

## Fonctionnalités

- Cibles de livraison de texte : Couvre le routage des cibles de livraison de texte, la liaison de session, l'historique et le contexte de conversation pour Outbound Delivery, Media, Receipts, and Typing.
- Livraison et limites des médias : Couvre le routage de la livraison et des limites des médias, la liaison de session, l'historique et le contexte de conversation pour Outbound Delivery, Media, Receipts, and Typing.
- Indicateurs de saisie et accusés de lecture : Couvre le routage des indicateurs de saisie et des accusés de lecture, la liaison de session, l'historique et le contexte de conversation pour Outbound Delivery, Media, Receipts, and Typing.
- Sortie stylisée/fragmentée : Couvre le routage de la sortie stylisée/fragmentée, la liaison de session, l'historique et le contexte de conversation pour Outbound Delivery, Media, Receipts, and Typing.
- Découverte d'action de réaction : Couvre le routage de la découverte d'action de réaction, la liaison de session, l'historique et le contexte de conversation pour Reactions Message Tool.
- Ajouter/supprimer des réactions : Couvre le routage de l'ajout/suppression de réactions, la liaison de session, l'historique et le contexte de conversation pour Reactions Message Tool.
- Ciblage de réaction de groupe : Couvre le routage du ciblage de réaction de groupe, la liaison de session, l'historique et le contexte de conversation pour Reactions Message Tool.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (72%)`

La couverture est Beta car la documentation, le code source et les tests couvrent le texte, les médias, la fragmentation, les accusés de livraison, la saisie et les accusés de lecture, mais la preuve de livraison Signal en direct est absente.

## Score de Qualité

- Score : `Alpha (68%)`

La qualité est Alpha car le chemin d'envoi est structuré, mais l'historique de l'opérateur montre toujours un support d'aperçu de lien manquant et un comportement de saisie visible par l'utilisateur peu fiable. Exclus de la qualité : preuves de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution ; ceux-ci affectent uniquement la couverture.

## Score de Complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/signal.md`.
- Signaux positifs : la documentation archivée, le code source, les tests, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les cibles de livraison de texte, la livraison et les limites des médias, les indicateurs de saisie et les accusés de lecture, la sortie stylisée/fragmentée, la découverte d'action de réaction, l'ajout/suppression de réactions, le ciblage de réaction de groupe.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Documentation

- `docs/channels/signal.md` lignes 263-278 documentent le comportement de réception/envoi normalisé, les limites des médias, les espaces réservés aux pièces jointes et la capture d'historique.
- `docs/channels/signal.md` lignes 280-284 documentent la saisie et les accusés de lecture.
- `docs/channels/signal.md` lignes 324-329 documentent les cibles de livraison pour les envois directs et de groupe.
- `docs/channels/signal.md` lignes 346-363 incluent les commandes de dépannage sortantes.

### Code Source

- `extensions/signal/src/send.ts` résout le compte et la cible, applique les indices de réaction d'approbation, applique les plafonds de médias, résout les pièces jointes, convertit le markdown, envoie les messages, enregistre les cibles de réaction et expose les assistants de saisie/accusé de lecture.
- `extensions/signal/src/format.ts` convertit le markdown en texte Signal et fragmente les messages stylisés sans diviser l'état de formatage.
- `extensions/signal/src/channel.ts` implémente des adaptateurs finaux durables pour le texte et les médias et formate les fragments sortants en utilisant les limites configurées.
- `extensions/signal/src/monitor/event-handler.ts` récupère les pièces jointes, construit les espaces réservés et envoie les accusés de lecture après les messages entrants acceptés.

### Tests d'intégration

- `extensions/signal/src/inbound-context.contract.test.ts` et les tests d'exécution d'approbation exercent les contrats de contexte et de routage internes.
- Aucune transcription d'envoi direct en direct, d'envoi de groupe, d'envoi de médias, de saisie, d'accusé de lecture ou d'accusé de livraison n'a été trouvée dans `qa/`, `test/` ou `tests`.

### Tests unitaires

- `extensions/signal/src/send.test.ts` couvre les horodatages de réception de texte, les accusés de réception de médias de groupe et l'évitement des ID de plateforme inventés lorsque Signal ne retourne pas d'horodatage.
- `extensions/signal/src/format.chunking.test.ts` couvre la fragmentation de base, la préservation du style entre les fragments et la gestion du rognage/style.
- `extensions/signal/src/core.test.ts` couvre la fragmentation sortante et le comportement de l'adaptateur texte/médias durable.
- `extensions/signal/src/monitor.tool-result.pairs-uuid-only-senders-uuid-allowlist-entry.test.ts` couvre les plafonds de réponse de pièces jointes de `mediaMaxMb`.
- `extensions/signal/src/monitor/event-handler.inbound-context.test.ts` couvre le comportement de saisie et d'accusé de lecture pour les messages directs autorisés.

### Requêtes Gitcrawl

- Requête : `Signal typing indicator official clients`
  - Résultats : le problème ouvert `#84120` signale que la saisie est envoyée avec succès mais les clients officiels n'affichent pas l'indicateur.
- Requête : `Signal linkPreview config`
  - Résultats : le problème ouvert `#24118` suit la configuration `channels.signal.linkPreview` manquante et le pass-through du chemin d'envoi.
- Requête : `Signal live tool-call progress`
  - Résultats : le problème ouvert `#77202` suit le comportement de progression du tool-call en direct.
- Requête : `Signal voice notes MediaPath transcription`
  - Résultats : le problème `#48614` a été fermé/corrigé pour le chemin de médias de note vocale et la population du type de médias.

### Requêtes Discrawl

- Requête : `Signal linkPreview config`
  - Résultats : le contenu du miroir GitHub Discord pour le problème `#24118` indique que la lacune reste ouverte.
- Requête : `Signal typing indicator official clients`
  - Résultats : aucune transcription d'opérateur affichée n'a montré une visibilité de saisie fiable dans les clients officiels.
- Requête : `Signal voice notes MediaPath transcription`
  - Résultats : le contenu du miroir Discord a signalé le problème `#48614` fermé avec le commit `537a8e25ed`, donc ce problème spécifique de chemin de médias a été traité comme corrigé.
