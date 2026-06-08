---
title: "OpenClaw App SDK - Note de Maturité des Conversations d'Agent"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# OpenClaw App SDK - Note de Maturité des Conversations d'Agent

## Résumé

La documentation couvre la création et la continuation des conversations d'agent. L'implémentation client fournit des assistants pour l'envoi de conversation, l'attente, le streaming et la normalisation. Les tests couvrent le comportement unitaire ainsi que les chemins de conversation e2e soutenus par Gateway.

## Portée de la Catégorie

Cette catégorie couvre la zone de capacité Conversations d'Agent définie par la taxonomie pour la surface OpenClaw App SDK.

## Fonctionnalités

- Handles d'agent : création et recherche d'objets agent côté SDK.
- Exécutions d'agent : chemin d'exécution d'agent avec événements d'exécution en streaming.
- Résultats d'exécution : enveloppe de résultat d'exécution, sémantique d'attente, gestion des délais d'expiration et normalisation des résultats.
- Création de session : création de handle de session réutilisable.
- Envoi de session : interaction de transcription de session à partir d'applications externes.
- Contrôles de session : opérations de patch, d'abandon et de compaction.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (78%)`
- Signaux positifs : La documentation couvre la création et la continuation des conversations d'agent ; l'implémentation client fournit des assistants pour l'envoi de conversation, l'attente, le streaming et la normalisation ; les tests couvrent le comportement unitaire ainsi que les chemins de conversation e2e soutenus par Gateway.
- Signaux négatifs : La couverture est forte pour les chemins principaux mais plus faible pour les scénarios de longue durée et multi-client en direct.
- Lacunes d'intégration : La couverture est forte pour les chemins principaux mais plus faible pour les scénarios de longue durée et multi-client en direct.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Stable (80%)`
- Rapports Gitcrawl : Vérification de fraîcheur globale réussie ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation surface-subagent.
- Rapports Discrawl : Vérification de fraîcheur globale réussie ; aucune recherche Discord spécifique à la catégorie n'a été exécutée dans ce package de notation surface-subagent.
- Bonnes qualités : La documentation couvre la création et la continuation des conversations d'agent ; l'implémentation client fournit des assistants pour l'envoi de conversation, l'attente, le streaming et la normalisation.
- Mauvaises qualités : Aucune faiblesse spécifique à la qualité d'implémentation n'a été identifiée séparément des autres classes de lacunes dans cette tranche de notation.
- Exclues de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et d'exécution réel n'a été utilisée que pour la Couverture et non comme entrées de Qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score de Complétude

- Score : `Stable (84%)`
- Instructions de surface : Noté par rapport à `.agents/skills/claw-score/references/completeness/openclaw-app-sdk.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les handles d'agent, les exécutions d'agent, les résultats d'exécution, la création de session, l'envoi de session, les contrôles de session.
- Signaux négatifs : La couverture est forte pour les chemins principaux mais plus faible pour les scénarios de longue durée et multi-client en direct.
- Branches de capacité manquantes : La couverture est forte pour les chemins principaux mais plus faible pour les scénarios de longue durée et multi-client en direct.

Étiquettes de complétude : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La complétude mesure la façon dont cette catégorie fournit complètement l'ensemble de capacités spécifiques à la surface prévue. La rubrique exacte provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes Connues

- La couverture est forte pour les chemins principaux mais plus faible pour les scénarios de longue durée et multi-client en direct.

## Preuves

### Docs

- `docs/concepts/openclaw-sdk.md:95-151`
- `docs/reference/openclaw-sdk-api-design.md:27-89`
- `docs/gateway/protocol.md:418-442`

### Source

- `packages/sdk/src/client.ts:550-607`
- `packages/sdk/src/client.ts:617-642`
- `packages/sdk/src/client.ts:676-731`
- `packages/sdk/src/types.ts:197-218`
- `packages/sdk/src/types.ts:264-280`

### Tests d'intégration

- `packages/sdk/src/index.e2e.test.ts:378-465`
- `packages/sdk/src/index.e2e.test.ts:566-718`

### Tests unitaires

- `packages/sdk/src/index.test.ts:64-105`
- `packages/sdk/src/index.test.ts:604-683`
- `packages/sdk/src/index.test.ts:1038-1060`

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

## Provenance de l'Audit

- Source du score : `docs/kevinslin/maturity-scorecard/inventory/openclaw-app-sdk/scores.yaml`.
- Source des métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
