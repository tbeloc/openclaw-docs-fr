---
title: "OpenClaw App SDK - Note de Maturité d'Accès à la Passerelle"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# OpenClaw App SDK - Note de Maturité d'Accès à la Passerelle

## Résumé

La documentation couvre la configuration de l'URL de la passerelle/authentification, les attentes de connexion au protocole et le comportement des points de terminaison. La source de transport inclut la configuration de WebSocket et la gestion des requêtes. Les tests E2E exercent le comportement du SDK soutenu par la passerelle et les défaillances de connexion.

## Portée de la Catégorie

Cette catégorie couvre la zone de capacité d'Accès à la Passerelle définie par la taxonomie pour la surface du SDK OpenClaw App.

## Fonctionnalités

- Connexion à la passerelle : construction du SDK pour les connexions explicites à la passerelle.
- Configuration d'URL et de jeton : entrées d'URL, de jeton et d'authentification pour les clients externes.
- Passerelle automatique : comportement de découverte automatique de la passerelle pour les environnements pris en charge.
- Transport personnalisé : injection de transport pour les environnements clients non par défaut.
- Portées et rédaction : portées de jeton, valeurs par défaut de transfert de secret et limites de rédaction.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false` et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0` et `share.needs_update=true`.

## Score de Couverture

- Score : `Bêta (78%)`
- Signaux positifs : La documentation couvre la configuration de l'URL de la passerelle/authentification, les attentes de connexion au protocole et le comportement des points de terminaison ; la source de transport inclut la configuration de WebSocket et la gestion des requêtes ; les tests E2E exercent le comportement du SDK soutenu par la passerelle et les défaillances de connexion.
- Signaux négatifs : `gateway: "auto"` reste incomplet ; l'ergonomie d'accès et la découverte sont plus minces que le transport sous-jacent.
- Lacunes d'intégration : `gateway: "auto"` reste incomplet ; l'ergonomie d'accès et la découverte sont plus minces que le transport sous-jacent.

Étiquettes de couverture : `Adorable = 95-100`, `Stable = 80-95`, `Bêta = 70-80`, `Alpha = 50-70` et `Expérimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

Les mesures de couverture intègrent l'intégration, e2e, en direct ou des preuves de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Bêta (74%)`
- Rapports Gitcrawl : vérification de fraîcheur globale réussie ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Rapports Discrawl : vérification de fraîcheur globale réussie ; aucune recherche discrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Bonnes qualités : La documentation couvre la configuration de l'URL de la passerelle/authentification, les attentes de connexion au protocole et le comportement des points de terminaison ; la source de transport inclut la configuration de WebSocket et la gestion des requêtes.
- Mauvaises qualités : `gateway: "auto"` reste incomplet ; l'ergonomie d'accès et la découverte sont plus minces que le transport sous-jacent.
- Exclus de la qualité : la couverture des tests unitaires, d'intégration, e2e, en direct et d'exécution réel a été utilisée uniquement pour la Couverture et non comme entrées de Qualité.

Étiquettes de qualité : `Adorable = 95-100`, `Stable = 80-95`, `Bêta = 70-80`, `Alpha = 50-70` et `Expérimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score de Complétude

- Score : `Alpha (64%)`
- Instructions de surface : noté par rapport à `.agents/skills/claw-score/references/completeness/openclaw-app-sdk.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la connexion à la passerelle, la configuration d'URL et de jeton, la passerelle automatique, le transport personnalisé, les portées et la rédaction.
- Signaux négatifs : `gateway: "auto"` reste incomplet ; l'ergonomie d'accès et la découverte sont plus minces que le transport sous-jacent.
- Branches de capacité manquantes : `gateway: "auto"` reste incomplet ; l'ergonomie d'accès et la découverte sont plus minces que le transport sous-jacent.

Étiquettes de complétude : `Adorable = 95-100`, `Stable = 80-95`, `Bêta = 70-80`, `Alpha = 50-70` et `Expérimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La complétude mesure la plénitude avec laquelle cette catégorie fournit l'ensemble de capacités spécifiques à la surface prévu. Le barème exact provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes Connues

- `gateway: "auto"` reste incomplet.
- L'ergonomie d'accès et la découverte sont plus minces que le transport sous-jacent.

## Preuves

### Docs

- `docs/concepts/openclaw-sdk.md:60-93`
- `docs/reference/openclaw-sdk-api-design.md:282-311`
- `docs/gateway/protocol.md:45-90`
- `docs/gateway/protocol.md:223-245`

### Source

- `packages/sdk/src/client.ts:35-52`
- `packages/sdk/src/client.ts:323-331`
- `packages/sdk/src/transport.ts:21-55`
- `packages/sdk/src/transport.ts:69-148`

### Tests d'intégration

- `packages/sdk/src/index.e2e.test.ts:378-385`
- `packages/sdk/src/index.e2e.test.ts:569-629`
- `packages/sdk/src/index.e2e.test.ts:662-718`
- `packages/gateway-client/src/client.watchdog.test.ts:482`

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

- Source de score : `docs/kevinslin/maturity-scorecard/inventory/openclaw-app-sdk/scores.yaml`.
- Source de métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
