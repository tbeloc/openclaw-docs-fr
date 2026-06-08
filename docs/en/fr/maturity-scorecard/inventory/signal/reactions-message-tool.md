---
title: "Signal - Reactions Message Tool Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Signal - Reactions Message Tool Maturity Note

## Résumé

Cette note migre les preuves de maturité archivées pour `Signal` / `Reactions Message Tool` dans l'inventaire de scorecard actuel process-version-3.

## Portée de la catégorie

Cette catégorie évalue la zone de capacité Signal représentée par ces fonctionnalités de taxonomie :

- Reactions Message Tool : Portée des preuves pour Reactions Message Tool.

## Fonctionnalités

- Reaction action discovery : Couvre le routage de découverte d'action de réaction, la liaison de session, l'historique et le contexte de conversation pour Reactions Message Tool.
- Add/remove reactions : Couvre le routage d'ajout/suppression de réactions, la liaison de session, l'historique et le contexte de conversation pour Reactions Message Tool.
- Group reaction targeting : Couvre le ciblage de réaction de groupe, la liaison de session, l'historique et le contexte de conversation pour Reactions Message Tool.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (70%)`

La couverture est Beta car la documentation, le code source et les tests unitaires couvrent la découverte d'action de réaction, les appels d'ajout/suppression et la validation des métadonnées de groupe, mais aucune preuve de réaction Signal en direct n'a été trouvée.

## Score de qualité

- Score : `Beta (72%)`

La qualité est Beta car le gating et la validation des réactions sont explicites, le principal risque source étant les cibles de groupe sensibles aux métadonnées plutôt qu'une ambiguïté de conception générale. Exclus de la qualité : preuves de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution ; ceux-ci affectent uniquement la couverture.

## Score de complétude

- Score : `Beta (70%)`
- Instructions de surface : évaluées par rapport à `references/completeness/signal.md`.
- Signaux positifs : la documentation archivée, le code source, les tests et les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la découverte d'action de réaction, l'ajout/suppression de réactions, le ciblage de réaction de groupe.
- Signaux négatifs : la note archivée a précédé le scoring de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Documentation

- `docs/channels/signal.md` lignes 286-307 documentent les réactions Signal, l'outil de message, la configuration d'activation, la sélection de compte, `reactionLevel` et les exigences de `targetAuthor` de groupe.
- `docs/channels/signal.md` lignes 324-329 documentent les formulaires cibles utilisés par les appels de réaction.

### Code source

- `extensions/signal/src/message-actions.ts` décrit les outils de message disponibles en fonction des comptes configurés et des portes d'action, valide les ID de cible/message, gère le fallback de message actuel et expose les actions d'ajout/suppression de réaction.
- `extensions/signal/src/send-reactions.ts` normalise les destinataires, nécessite un timestamp/emoji/auteur cible le cas échéant, et mappe les appels d'ajout/suppression aux RPC de réaction Signal.
- `extensions/signal/src/channel.ts` câble les actions de message Signal dans la surface de canal.
- `src/config/types.signal.ts` définit `actions.reactions` et `reactionLevel`.

### Tests d'intégration

- Aucune exécution de réaction d'ajout/suppression en direct n'a été trouvée dans `qa/`, `test/` ou `tests`.
- Les tests de contrat de canal Signal couvrent le câblage de contexte mais pas la livraison de réaction réelle.

### Tests unitaires

- `extensions/signal/src/message-actions.test.ts` couvre la découverte d'action par comptes configurés et portes de réaction, comportement d'action désactivée, mappage de cible directe, cibles UUID, `targetAuthor` de groupe, fallback de message actuel et entrées invalides.
- `extensions/signal/src/client-container.test.ts` couvre le mappage RPC de réaction de conteneur.
- `extensions/signal/src/approval-reactions.test.ts` couvre un chemin de réaction d'approbation séparé et un comportement de liaison de cible.

### Requêtes Gitcrawl

- Requête : `Signal reactions targetAuthor`
  - Résultats : aucune défaillance actuelle ciblée n'a été trouvée pour l'outil de réaction de message général.
- Requête : `Signal message actions reactions`
  - Résultats : résultats d'archive plus larges centrés sur les réactions d'approbation et le routage de réaction plutôt que sur l'action de message orientée utilisateur.

### Requêtes Discrawl

- Requête : `Signal reactions targetAuthor`
  - Résultats : aucune transcription d'opérateur affichée n'a prouvé le succès ou l'échec de la réaction en direct.
- Requête : `Signal message actions reactions`
  - Résultats : aucun rapport utilisateur/opérateur spécifique à Signal affiché n'a modifié l'évaluation basée sur le code source.
