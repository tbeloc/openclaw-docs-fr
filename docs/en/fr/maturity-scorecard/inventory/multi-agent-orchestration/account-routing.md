---
title: "Orchestration multi-agents - Note de Maturité du Routage de Compte"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Orchestration multi-agents - Note de Maturité du Routage de Compte

## Résumé

La documentation et le code source couvrent le routage par compte et les avertissements de compte par défaut. Les tests couvrent la résolution des routes, les routes de canal de plugin et les défaillances du flux de configuration du docteur.

## Portée de la Catégorie

Cette catégorie couvre la zone de capacité de Routage de Compte définie par la taxonomie pour la surface d'orchestration multi-agents.

## Fonctionnalités

- Configuration multi-compte : Configurez plus d'un compte ou numéro de téléphone.
- Sélection de compte : Choisissez le compte correct pour les routes entrantes et sortantes.
- Comptes par défaut : Utilisez le comportement defaultAccount en toute sécurité.
- Identifiants de compte : Maintenez les identifiants alignés avec l'agent propriétaire et la route.
- Cibles de livraison : Acheminez les réponses via le compte de canal prévu.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (78%)`
- Signaux positifs : La documentation et le code source couvrent le routage par compte et les avertissements de compte par défaut ; Les tests couvrent la résolution des routes, les routes de canal de plugin et les défaillances du flux de configuration du docteur.
- Signaux négatifs : La couverture est principalement automatisée plutôt que basée sur des preuves de canaux réels.
- Lacunes d'intégration : La couverture est principalement automatisée plutôt que basée sur des preuves de canaux réels.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La couverture mesure l'intégration, les preuves e2e, en direct ou de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Stable (84%)`
- Rapports Gitcrawl : La vérification de fraîcheur globale a réussi ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Rapports Discrawl : La vérification de fraîcheur globale a réussi ; aucune recherche Discord spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Bonnes qualités : La documentation et le code source couvrent le routage par compte et les avertissements de compte par défaut.
- Mauvaises qualités : Aucune faiblesse spécifique à la qualité de mise en œuvre n'a été identifiée séparément des autres classes de lacunes dans cette tranche de notation.
- Exclues de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et d'exécution réel a été utilisée uniquement pour la Couverture et non comme entrées de Qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score de Complétude

- Score : `Stable (82%)`
- Instructions de surface : Noté par rapport à `.agents/skills/claw-score/references/completeness/multi-agent-orchestration.md`.
- Signaux positifs : Les preuves archivées de documentation, code source, tests, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Configuration multi-compte, Sélection de compte, Comptes par défaut, Identifiants de compte, Cibles de livraison.
- Signaux négatifs : La couverture est principalement automatisée plutôt que basée sur des preuves de canaux réels.
- Branches de capacité manquantes : La couverture est principalement automatisée plutôt que basée sur des preuves de canaux réels.

Étiquettes de complétude : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La complétude mesure la façon dont cette catégorie fournit complètement l'ensemble de capacités spécifiques à la surface prévu. La rubrique exacte provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes Connues

- La couverture est principalement automatisée plutôt que basée sur des preuves de canaux réels.

## Preuves

### Documentation

- `docs/concepts/multi-agent.md:247`
- `docs/gateway/config-channels.md:751`
- `docs/channels/feishu.md:418`

### Code Source

- `src/routing/account-id.ts:35`
- `src/routing/resolve-route.ts:232`
- `src/commands/doctor/shared/default-account-warnings.ts:68`

### Tests d'intégration

- `src/commands/doctor-config-flow.missing-default-account-bindings.integration.test.ts:8`

### Tests unitaires

- `src/routing/resolve-route.test.ts:566`
- `src/plugin-sdk/channel-route.test.ts:17`

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

- Source du score : `docs/kevinslin/maturity-scorecard/inventory/multi-agent-orchestration/scores.yaml`.
- Source des métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
