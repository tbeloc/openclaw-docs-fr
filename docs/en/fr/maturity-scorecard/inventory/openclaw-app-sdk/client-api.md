---
title: "OpenClaw App SDK - Note de Maturité de l'API Client"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# OpenClaw App SDK - Note de Maturité de l'API Client

## Résumé

La documentation et la conception de l'API décrivent la forme du client, les exports, les assistants d'événements et l'utilisation du package. La source expose une API client typée et des assistants de haut niveau. Les tests E2E et les tests de consommateurs de packages exercent l'importation du SDK et les appels client.

## Portée de la Catégorie

Cette catégorie couvre la zone de capacité de l'API Client définie par la taxonomie pour la surface du SDK OpenClaw App.

## Fonctionnalités

- Points d'entrée du SDK : Imports de packages publics et objets assistants pour les applications externes.
- Disposition des espaces de noms : Espaces de noms de haut niveau et de bas niveau tels que les agents et les sessions.
- Division des packages : Limites entre le SDK principal, les assistants React et le package de test.
- Limite application/plugin : Distinction claire entre les intégrations d'applications externes et la création de plugins en processus.

## Fraîcheur des Archives

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (86%)`
- Signaux positifs : La documentation et la conception de l'API décrivent la forme du client, les exports, les assistants d'événements et l'utilisation du package ; La source expose une API client typée et des assistants de haut niveau ; Les tests E2E et les tests de consommateurs de packages exercent l'importation du SDK et les appels client.
- Signaux négatifs : Le package reste privé/0.0.0-private ; Certaines couches de commodité conçues ne sont pas encore implémentées.
- Lacunes d'intégration : Le package reste privé/0.0.0-private ; Certaines couches de commodité conçues ne sont pas encore implémentées.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité la plus élevée.

Les mesures de couverture intègrent des preuves d'intégration, e2e, en direct ou de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Stable (82%)`
- Rapports Gitcrawl : Vérification de fraîcheur globale réussie ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Rapports Discrawl : Vérification de fraîcheur globale réussie ; aucune recherche discrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Bonnes qualités : La documentation et la conception de l'API décrivent la forme du client, les exports, les assistants d'événements et l'utilisation du package ; La source expose une API client typée et des assistants de haut niveau.
- Mauvaises qualités : Le package reste privé/0.0.0-private ; Certaines couches de commodité conçues ne sont pas encore implémentées.
- Exclus de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et d'exécution réel a été utilisée uniquement pour la Couverture et non comme entrées de Qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité la plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score d'Exhaustivité

- Score : `Beta (78%)`
- Instructions de surface : Noté par rapport à `.agents/skills/claw-score/references/completeness/openclaw-app-sdk.md`.
- Signaux positifs : Les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les points d'entrée du SDK, la disposition des espaces de noms, la division des packages, la limite application/plugin.
- Signaux négatifs : Le package reste privé/0.0.0-private ; Certaines couches de commodité conçues ne sont pas encore implémentées.
- Branches de capacité manquantes : Le package reste privé/0.0.0-private ; Certaines couches de commodité conçues ne sont pas encore implémentées.

Étiquettes d'exhaustivité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité la plus élevée.

L'exhaustivité mesure la complétude avec laquelle cette catégorie fournit l'ensemble de capacités de surface spécifique prévu. La rubrique exacte provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes Connues

- Le package reste privé/0.0.0-private.
- Certaines couches de commodité conçues ne sont pas encore implémentées.

## Preuves

### Documentation

- `docs/concepts/openclaw-sdk.md:11-58`
- `docs/concepts/openclaw-sdk.md:292-312`
- `docs/reference/openclaw-sdk-api-design.md:27-89`
- `docs/reference/openclaw-sdk-api-design.md:347-355`

### Source

- `packages/sdk/package.json:1-23`
- `packages/sdk/src/index.ts:1-56`
- `packages/sdk/src/client.ts:303-340`
- `packages/sdk/src/client.ts:544-731`

### Tests d'intégration

- `packages/sdk/src/index.e2e.test.ts:378-425`
- `packages/sdk/src/index.e2e.test.ts:427-534`
- `packages/sdk/src/package.e2e.test.ts:208-273`

### Tests unitaires

- Aucun identifié dans cette tranche de notation.

### Commandes de validation de surface

- `gitcrawl doctor --json` : `pass` - La fraîcheur de l'archive a été vérifiée avant la notation.
- `discrawl status --json` : `pass` - La fraîcheur de l'archive Discord a été vérifiée avant la notation.

### Requêtes Gitcrawl

Requête : vérification de fraîcheur globale uniquement.

Résultats :

- `gitcrawl doctor --json` réussi ; les requêtes de problèmes spécifiques à la catégorie n'ont pas été exécutées dans ce package de notation de sous-agent de surface.

### Requêtes Discrawl

Requête : vérification de fraîcheur globale uniquement.

Résultats :

- `discrawl status --json` réussi ; les recherches Discord spécifiques à la catégorie n'ont pas été exécutées dans ce package de notation de sous-agent de surface.

## Provenance de l'Audit

- Source du score : `docs/kevinslin/maturity-scorecard/inventory/openclaw-app-sdk/scores.yaml`.
- Source des métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
