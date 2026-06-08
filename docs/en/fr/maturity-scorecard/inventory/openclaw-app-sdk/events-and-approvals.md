---
title: "OpenClaw App SDK - Note de Maturité des Événements et Approbations"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# OpenClaw App SDK - Note de Maturité des Événements et Approbations

## Résumé

La documentation et les types incluent les concepts d'événements et d'approbations. La source client normalise les événements et expose les assistants d'attente/écoute. Les tests couvrent la normalisation des événements, la réception des événements e2e et les portées des méthodes.

## Portée de la Catégorie

Cette catégorie couvre la zone de capacité Événements et Approbations définie par la taxonomie pour la surface OpenClaw App SDK.

## Fonctionnalités

- Flux d'événements : abonnement au flux SDK pour les événements à l'échelle de l'application et par exécution.
- Enveloppe d'événement : enveloppe d'événement stable pour les clients externes.
- Curseurs de relecture : familles d'événements rejouables avec curseurs stables.
- Rappels d'approbation : gestion des approbations de première classe pour les applications externes.
- Questions : gestion des questions aux côtés des flux d'approbation.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (74%)`
- Signaux positifs : La documentation et les types incluent les concepts d'événements et d'approbations ; La source client normalise les événements et expose les assistants d'attente/écoute ; Les tests couvrent la normalisation des événements, la réception des événements e2e et les portées des méthodes.
- Signaux négatifs : Les rappels d'approbation et les questions restent principalement au niveau de la conception plutôt que des flux SDK entièrement ergonomiques ; La complétude est limitée par les lacunes entre les événements de protocole de bas niveau et les API de développeur d'application de première classe.
- Lacunes d'intégration : Les rappels d'approbation et les questions restent principalement au niveau de la conception plutôt que des flux SDK entièrement ergonomiques ; La complétude est limitée par les lacunes entre les événements de protocole de bas niveau et les API de développeur d'application de première classe.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Beta (73%)`
- Rapports Gitcrawl : Vérification de fraîcheur globale réussie ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation du sous-agent de surface.
- Rapports Discrawl : Vérification de fraîcheur globale réussie ; aucune requête discrawl spécifique à la catégorie n'a été exécutée dans ce package de notation du sous-agent de surface.
- Bonnes qualités : La documentation et les types incluent les concepts d'événements et d'approbations ; La source client normalise les événements et expose les assistants d'attente/écoute.
- Mauvaises qualités : Les rappels d'approbation et les questions restent principalement au niveau de la conception plutôt que des flux SDK entièrement ergonomiques ; La complétude est limitée par les lacunes entre les événements de protocole de bas niveau et les API de développeur d'application de première classe.
- Exclus de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel a été utilisée uniquement pour la Couverture et non comme entrées de Qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou de flux d'exécution réel comme entrée de notation.

## Score de Complétude

- Score : `Alpha (58%)`
- Instructions de surface : Noté par rapport à `.agents/skills/claw-score/references/completeness/openclaw-app-sdk.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le flux d'événements, l'enveloppe d'événement, les curseurs de relecture, les rappels d'approbation, les questions.
- Signaux négatifs : Les rappels d'approbation et les questions restent principalement au niveau de la conception plutôt que des flux SDK entièrement ergonomiques ; La complétude est limitée par les lacunes entre les événements de protocole de bas niveau et les API de développeur d'application de première classe.
- Branches de capacité manquantes : Les rappels d'approbation et les questions restent principalement au niveau de la conception plutôt que des flux SDK entièrement ergonomiques ; La complétude est limitée par les lacunes entre les événements de protocole de bas niveau et les API de développeur d'application de première classe.

Étiquettes de complétude : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La complétude mesure la façon dont cette catégorie fournit complètement l'ensemble de capacités de surface spécifique prévu. La rubrique exacte provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes Connues

- Les rappels d'approbation et les questions restent principalement au niveau de la conception plutôt que des flux SDK entièrement ergonomiques.
- La complétude est limitée par les lacunes entre les événements de protocole de bas niveau et les API de développeur d'application de première classe.

## Preuves

### Docs

- `docs/concepts/openclaw-sdk.md:153-212`
- `docs/concepts/openclaw-sdk.md:253-258`
- `docs/reference/openclaw-sdk-api-design.md:91-112`
- `docs/reference/openclaw-sdk-api-design.md:187-215`
- `docs/gateway/protocol.md:469-475`
- `docs/gateway/protocol.md:631-640`

### Source

- `packages/sdk/src/types.ts:220-262`
- `packages/sdk/src/client.ts:373-473`
- `packages/sdk/src/client.ts:518-540`
- `packages/sdk/src/normalize.ts:67-153`
- `packages/sdk/src/client.ts:833-842`

### Tests d'intégration

- `packages/sdk/src/index.e2e.test.ts:380-415`
- `packages/sdk/src/index.e2e.test.ts:503-508`
- `src/gateway/method-scopes.test.ts:293-304`

### Tests unitaires

- `packages/sdk/src/index.test.ts:650-682`
- `packages/sdk/src/index.test.ts:775-780`
- `packages/sdk/src/index.test.ts:984-1035`

### Commandes de validation de surface

- `gitcrawl doctor --json` : `pass` - La fraîcheur de l'archive a été vérifiée avant la notation.
- `discrawl status --json` : `pass` - La fraîcheur de l'archive Discord a été vérifiée avant la notation.

### Requêtes Gitcrawl

Requête : vérification de fraîcheur globale uniquement.

Résultats :

- `gitcrawl doctor --json` réussi ; les requêtes de problèmes spécifiques à la catégorie n'ont pas été exécutées dans ce package de notation du sous-agent de surface.

### Requêtes Discrawl

Requête : vérification de fraîcheur globale uniquement.

Résultats :

- `discrawl status --json` réussi ; les recherches Discord spécifiques à la catégorie n'ont pas été exécutées dans ce package de notation du sous-agent de surface.

## Provenance de l'Audit

- Source du score : `docs/kevinslin/maturity-scorecard/inventory/openclaw-app-sdk/scores.yaml`.
- Source des métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
