---
title: "Signal - Note de Maturité des Contrôles Natifs et des Approbations"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Signal - Note de Maturité des Contrôles Natifs et des Approbations

## Résumé

Cette note migre les preuves de maturité archivées pour `Signal` / `Routage des Approbations et Résolution des Réactions` dans l'inventaire actuel du scorecard de la version 3 du processus.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Contrôles Natifs et Approbations`
- Fusionnée à partir de : `Approbations Natives`, `Livraison des Messages et Actions`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Routage des approbations natives : Définit l'autorisation du routage des approbations natives, les limites de confiance et de sécurité, et les contrôles des opérateurs pour le Routage des Approbations et la Résolution des Réactions.
- Réponses d'approbation des réactions : Définit l'autorisation des réponses d'approbation des réactions, les limites de confiance et de sécurité, et les contrôles des opérateurs pour le Routage des Approbations et la Résolution des Réactions.
- Ciblage des approbateurs : Définit l'autorisation du ciblage des approbateurs, les limites de confiance et de sécurité, et les contrôles des opérateurs pour le Routage des Approbations et la Résolution des Réactions.
- Cibles de livraison de texte : Couvre le routage des cibles de livraison de texte, la liaison de session, l'historique et le contexte de conversation pour la Livraison Sortante, les Médias, les Reçus et la Saisie.
- Livraison et limites des médias : Couvre le routage de la livraison et des limites des médias, la liaison de session, l'historique et le contexte de conversation pour la Livraison Sortante, les Médias, les Reçus et la Saisie.
- Saisie et reçus de lecture : Couvre le routage de la saisie et des reçus de lecture, la liaison de session, l'historique et le contexte de conversation pour la Livraison Sortante, les Médias, les Reçus et la Saisie.
- Sortie stylisée/fragmentée : Couvre le routage de la sortie stylisée/fragmentée, la liaison de session, l'historique et le contexte de conversation pour la Livraison Sortante, les Médias, les Reçus et la Saisie.
- Découverte des actions de réaction : Couvre le routage de la découverte des actions de réaction, la liaison de session, l'historique et le contexte de conversation pour l'Outil de Message de Réactions.
- Ajouter/supprimer des réactions : Couvre le routage de l'ajout/suppression de réactions, la liaison de session, l'historique et le contexte de conversation pour l'Outil de Message de Réactions.
- Ciblage des réactions de groupe : Couvre le routage du ciblage des réactions de groupe, la liaison de session, l'historique et le contexte de conversation pour l'Outil de Message de Réactions.
- Outil de Message de Réactions : Portée des preuves pour l'Outil de Message de Réactions

## Fonctionnalités

- Routage des approbations natives : Définit l'autorisation du routage des approbations natives, les limites de confiance et de sécurité, et les contrôles des opérateurs pour le Routage des Approbations et la Résolution des Réactions.
- Réponses d'approbation des réactions : Définit l'autorisation des réponses d'approbation des réactions, les limites de confiance et de sécurité, et les contrôles des opérateurs pour le Routage des Approbations et la Résolution des Réactions.
- Ciblage des approbateurs : Définit l'autorisation du ciblage des approbateurs, les limites de confiance et de sécurité, et les contrôles des opérateurs pour le Routage des Approbations et la Résolution des Réactions.

## Fraîcheur des Archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Alpha (65%)`

La couverture est Alpha car la documentation, le code source et les tests couvrent le routage des approbations natives et la liaison des réactions, mais aucune exécution d'approbation Signal en direct n'a été trouvée.

## Score de Qualité

- Score : `Beta (70%)`

La qualité est Beta car le routage des sessions et des cibles ont des vérifications de source explicites et une persistance, mais les approbations de groupe dépendent du routage explicite des approbateurs et des métadonnées de cible exactes. Exclus de la qualité : les preuves de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution ; celles-ci affectent uniquement la Couverture.

## Score de Complétude

- Score : `Alpha (65%)`
- Instructions de surface : évaluées par rapport à `references/completeness/signal.md`.
- Signaux positifs : la documentation archivée, le code source, les tests, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le routage des approbations natives, les réponses d'approbation des réactions, le ciblage des approbateurs.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Documentation

- `docs/channels/signal.md` lignes 309-322 documentent les réactions d'approbation, la configuration des routes et le comportement de secours.
- `docs/channels/signal.md` lignes 324-329 documentent les cibles de livraison utilisées par le routage des approbations.
- `docs/channels/signal.md` lignes 286-307 documentent les primitives de réaction sur lesquelles les invites d'approbation s'appuient.

### Code Source

- `extensions/signal/src/approval-native.ts` vérifie l'admissibilité des approbations, le compte d'origine, le mode de route, les approbateurs explicites et les capacités de livraison ; il supprime également les invites d'exécution locale uniquement lorsque les routes Signal configurées peuvent les gérer.
- `extensions/signal/src/approval-handler.runtime.ts` crée l'adaptateur d'exécution natif et prépare les cibles d'approbation spécifiques à Signal.
- `extensions/signal/src/approval-reactions.ts` stocke les liaisons d'invites délimitées, construit les indices de réaction, ajoute les métadonnées d'admissibilité, enregistre les cibles d'approbation sortantes et résout les réponses de réaction.
- `extensions/signal/src/channel.ts` câble la capacité d'approbation dans le canal Signal.

### Tests d'intégration

- `extensions/signal/src/approval-handler.runtime.test.ts` exerce la préparation des cibles d'exécution et la livraison en attente via l'adaptateur d'approbation Signal.
- Aucune transcription d'invite d'approbation Signal en direct, d'approbation de réaction ou de secours n'a été trouvée dans `qa/`, `test/` ou `tests`.

### Tests unitaires

- `extensions/signal/src/approval-native.test.ts` couvre la disponibilité seule sans activer les approbations, la livraison d'exécution en mode session pour les origines correspondantes, les approbateurs explicites pour les approbations d'origine de groupe, les portes d'exécution/plugin indépendantes, le rejet d'origine non-Signal, la disponibilité de la configuration du mode cible et le secours manuel sans liaisons/approbateurs de réaction.
- `extensions/signal/src/approval-reactions.test.ts` couvre les indices de réaction, l'évitement des indices en double, l'enregistrement des invites d'approbation sortantes en mode cible, le secours de route cible désactivée, le comportement de cible toujours autorisée et la résolution de cible enregistrée.

### Requêtes Gitcrawl

- Requête : `Signal approval reactions`
  - Résultats : les résultats d'archive ont montré l'historique du développement des réactions d'approbation mais aucune transcription de succès d'approbation Signal en direct.
- Requête : `Signal approvals explicit approvers group`
  - Résultats : aucun échec actuel ciblé n'a été retourné au-delà de l'exigence d'approbateur explicite visible dans le code source.

### Requêtes Discrawl

- Requête : `Signal approval reactions`
  - Résultats : aucune transcription d'opérateur affichée n'a prouvé la gestion des approbations Signal en direct.
- Requête : `Signal approvals explicit approvers group`
  - Résultats : aucun rapport d'opérateur affiché n'a modifié l'évaluation basée sur le code source.
