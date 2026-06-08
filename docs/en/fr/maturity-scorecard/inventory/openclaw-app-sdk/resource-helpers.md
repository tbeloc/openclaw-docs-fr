---
title: "OpenClaw App SDK - Note de Maturité des Assistants de Ressources"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# OpenClaw App SDK - Note de Maturité des Assistants de Ressources

## Résumé

La documentation et le code source incluent des concepts d'assistants de ressources typés et une implémentation d'assistant de base. Les tests unitaires et e2e couvrent les méthodes d'assistant sélectionnées.

## Portée de la Catégorie

Cette catégorie couvre la zone de capacité des Assistants de Ressources définie par la taxonomie pour la surface du SDK OpenClaw App.

## Fonctionnalités

- Modèles : Assistants de découverte de modèles typés.
- ToolSpace : Abstraction de découverte et d'invocation d'outils pour les applications externes.
- Artefacts : Résumés d'artefacts, métadonnées de rétention et comportement de téléchargement.
- Tâches : Assistants SDK autour des API de tâches Gateway.
- Environnements : Cycle de vie du fournisseur d'environnement géré et métadonnées.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Alpha (58%)`
- Signaux positifs : La documentation et le code source incluent des concepts d'assistants de ressources typés et une implémentation d'assistant de base ; Les tests unitaires et e2e couvrent les méthodes d'assistant sélectionnées.
- Signaux négatifs : La couverture en direct/runtime pour les flux de travail des assistants est mince ; L'étendue des assistants n'est pas encore au même niveau de maturité que les API client et conversation.
- Lacunes d'intégration : La couverture en direct/runtime pour les flux de travail des assistants est mince ; L'étendue des assistants n'est pas encore au même niveau de maturité que les API client et conversation.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

Les mesures de couverture intègrent l'intégration, e2e, en direct ou des preuves de flux de travail runtime réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : Vérification de fraîcheur globale réussie ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation surface-subagent.
- Rapports Discrawl : Vérification de fraîcheur globale réussie ; aucune recherche Discord spécifique à la catégorie n'a été exécutée dans ce package de notation surface-subagent.
- Bonnes qualités : La documentation et le code source incluent des concepts d'assistants de ressources typés et une implémentation d'assistant de base.
- Mauvaises qualités : L'étendue des assistants n'est pas encore au même niveau de maturité que les API client et conversation.
- Exclus de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et runtime réel a été utilisée uniquement pour la Couverture et non comme entrées de Qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou runtime réel comme entrée de notation.

## Score d'Exhaustivité

- Score : `Beta (70%)`
- Instructions de surface : Noté par rapport à `.agents/skills/claw-score/references/completeness/openclaw-app-sdk.md`.
- Signaux positifs : Les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Modèles, ToolSpace, Artefacts, Tâches, Environnements.
- Signaux négatifs : La couverture en direct/runtime pour les flux de travail des assistants est mince ; L'étendue des assistants n'est pas encore au même niveau de maturité que les API client et conversation.
- Branches de capacité manquantes : La couverture en direct/runtime pour les flux de travail des assistants est mince ; L'étendue des assistants n'est pas encore au même niveau de maturité que les API client et conversation.

Étiquettes d'exhaustivité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

L'exhaustivité mesure la complétude avec laquelle cette catégorie fournit l'ensemble de capacités de surface spécifique prévu. Le barème exact provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes Connues

- La couverture en direct/runtime pour les flux de travail des assistants est mince.
- L'étendue des assistants n'est pas encore au même niveau de maturité que les API client et conversation.

## Preuves

### Docs

- `docs/concepts/openclaw-sdk.md:214-290`
- `docs/reference/openclaw-sdk-api-design.md:217-280`
- `docs/reference/openclaw-sdk-api-design.md:313-345`

### Source

- `packages/sdk/src/client.ts:749-866`
- `packages/sdk/src/client.ts:214-226`
- `packages/sdk/src/types.ts:43-53`
- `packages/sdk/src/types.ts:74-171`

### Tests d'intégration

- `packages/sdk/src/index.e2e.test.ts:467-534`
- `packages/sdk/src/index.e2e.test.ts:662-681`

### Tests unitaires

- `packages/sdk/src/index.test.ts:392-602`

### Commandes de validation de surface

- `gitcrawl doctor --json` : `pass` - La fraîcheur de l'archive a été vérifiée avant la notation.
- `discrawl status --json` : `pass` - La fraîcheur de l'archive Discord a été vérifiée avant la notation.

### Requêtes Gitcrawl

Requête : vérification de fraîcheur globale uniquement.

Résultats :

- `gitcrawl doctor --json` réussi ; les requêtes de problèmes spécifiques à la catégorie n'ont pas été exécutées dans ce package de notation surface-subagent.

### Requêtes Discrawl

Requête : vérification de fraîcheur globale uniquement.

Résultats :

- `discrawl status --json` réussi ; les recherches Discord spécifiques à la catégorie n'ont pas été exécutées dans ce package de notation surface-subagent.

## Provenance d'Audit

- Source de notation : `docs/kevinslin/maturity-scorecard/inventory/openclaw-app-sdk/scores.yaml`.
- Source de métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
