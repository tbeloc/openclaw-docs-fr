---
title: "OpenClaw App SDK - Note de Maturité de Compatibilité"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# OpenClaw App SDK - Note de Maturité de Compatibilité

## Résumé

La documentation identifie la compatibilité des packages/runtimes et les attentes de conception. Le code source contient des exports de packages versionnés et une gestion de la compatibilité des transports. Les tests couvrent la consommation de packages et le comportement du SDK soutenu par Gateway.

## Portée de la Catégorie

Cette catégorie couvre la zone de capacité Compatibilité définie par la taxonomie pour la surface OpenClaw App SDK.

## Fonctionnalités

- Client généré : Génération de client à partir des schémas Gateway.
- Wrappers ergonomiques : Wrappers écrits à la main superposés sur les contrats de transport générés.
- Appels non supportés : Erreurs explicites pour les mutations d'environnement non supportées et les surcharges futures par exécution.
- Alignement des schémas : Le comportement du SDK reste aligné avec les schémas Gateway.
- Contrat de package public : La publication de package et les attentes de client réutilisable sont suivies explicitement.

## Fraîcheur des Archives

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (76%)`
- Signaux positifs : La documentation identifie la compatibilité des packages/runtimes et les attentes de conception ; Le code source contient des exports de packages versionnés et une gestion de la compatibilité des transports ; Les tests couvrent la consommation de packages et le comportement du SDK soutenu par Gateway.
- Signaux négatifs : Le chemin du client généré est de conception uniquement ; Les packages compagnons manquants et le statut de package privé réduisent l'exhaustivité.
- Lacunes d'intégration : Le chemin du client généré est de conception uniquement ; Les packages compagnons manquants et le statut de package privé réduisent l'exhaustivité.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La couverture mesure l'intégration, e2e, live, ou les preuves de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : La vérification de fraîcheur globale a réussi ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Rapports Discrawl : La vérification de fraîcheur globale a réussi ; aucune recherche discrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Bonnes qualités : La documentation identifie la compatibilité des packages/runtimes et les attentes de conception ; Le code source contient des exports de packages versionnés et une gestion de la compatibilité des transports.
- Mauvaises qualités : Le chemin du client généré est de conception uniquement ; Les packages compagnons manquants et le statut de package privé réduisent l'exhaustivité.
- Exclus de la qualité : La couverture des tests unitaires, d'intégration, e2e, live et d'exécution réel a été utilisée uniquement pour la Couverture et non comme entrées de Qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, live ou d'exécution réel comme entrée de notation.

## Score d'Exhaustivité

- Score : `Alpha (62%)`
- Instructions de surface : Noté par rapport à `.agents/skills/claw-score/references/completeness/openclaw-app-sdk.md`.
- Signaux positifs : Les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Client généré, Wrappers ergonomiques, Appels non supportés, Alignement des schémas, Contrat de package public.
- Signaux négatifs : Le chemin du client généré est de conception uniquement ; Les packages compagnons manquants et le statut de package privé réduisent l'exhaustivité.
- Branches de capacité manquantes : Le chemin du client généré est de conception uniquement ; Les packages compagnons manquants et le statut de package privé réduisent l'exhaustivité.

Étiquettes d'exhaustivité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

L'exhaustivité mesure la complétude avec laquelle cette catégorie fournit l'ensemble de capacités de surface spécifique prévu. Le barème exact provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes Connues

- Le chemin du client généré est de conception uniquement.
- Les packages compagnons manquants et le statut de package privé réduisent l'exhaustivité.

## Preuves

### Docs

- `docs/concepts/openclaw-sdk.md:24-45`
- `docs/concepts/openclaw-sdk.md:275-290`
- `docs/reference/openclaw-sdk-api-design.md:347-363`

### Source

- `packages/sdk/src/client.ts:162-200`
- `packages/sdk/src/client.ts:303-333`
- `packages/sdk/src/client.ts:846-866`
- `packages/sdk/src/transport.ts:69-148`
- `packages/sdk/package.json:1-23`

### Tests d'intégration

- `packages/sdk/src/index.e2e.test.ts:378-425`
- `packages/sdk/src/index.e2e.test.ts:566-718`
- `packages/sdk/src/package.e2e.test.ts:208-273`

### Tests unitaires

- `packages/sdk/src/index.test.ts:326-359`
- `packages/sdk/src/index.test.ts:456-466`

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
