---
title: "Orchestration multi-agent - Note de maturité du routage de conversation"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Orchestration multi-agent - Note de maturité du routage de conversation

## Résumé

La documentation et le code source couvrent la résolution des routes de canal, les correspondances configurées et le comportement de livraison. Les tests incluent les tests unitaires de routage, l'intégration Matrix bind et la couverture live Gateway bind.

## Portée de la catégorie

Cette catégorie couvre la zone de capacité de routage de conversation définie par la taxonomie pour la surface d'orchestration multi-agent.

## Fonctionnalités

- Sélection d'agent : Résoudre les messages entrants vers l'agent correct.
- Précédence des routes : Appliquer l'ordre de correspondance déterministe et le bris d'égalité.
- Secours par défaut : Revenir à l'agent par défaut configuré.
- Remplacements de pairs : Router des pairs ou des groupes spécifiques vers un agent choisi.
- Exemples multi-canaux : Réutiliser les modèles de routage sur Discord, Telegram, WhatsApp et canaux similaires.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : La documentation et le code source couvrent la résolution des routes de canal, les correspondances configurées et le comportement de livraison ; Les tests incluent les tests unitaires de routage, l'intégration Matrix bind et la couverture live Gateway bind.
- Signaux négatifs : La preuve complète du routage multi-canal en direct reste limitée.
- Lacunes d'intégration : La preuve complète du routage multi-canal en direct reste limitée.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Stable (84%)`
- Rapports Gitcrawl : La vérification de fraîcheur globale a réussi ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Rapports Discrawl : La vérification de fraîcheur globale a réussi ; aucune recherche discrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Bonnes qualités : La documentation et le code source couvrent la résolution des routes de canal, les correspondances configurées et le comportement de livraison.
- Mauvaises qualités : Aucune faiblesse spécifique à la qualité de mise en œuvre n'a été identifiée séparément des autres classes de lacunes dans cette tranche de notation.
- Exclu de la qualité : Les tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel ont été utilisés uniquement pour la couverture et non comme entrées de qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score d'exhaustivité

- Score : `Stable (86%)`
- Instructions de surface : Noté par rapport à `.agents/skills/claw-score/references/completeness/multi-agent-orchestration.md`.
- Signaux positifs : Les preuves archivées de documentation, code source, tests, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la sélection d'agent, la précédence des routes, le secours par défaut, les remplacements de pairs, les exemples multi-canaux.
- Signaux négatifs : La preuve complète du routage multi-canal en direct reste limitée.
- Branches de capacité manquantes : La preuve complète du routage multi-canal en direct reste limitée.

Étiquettes d'exhaustivité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

L'exhaustivité mesure la complétude avec laquelle cette catégorie fournit l'ensemble de capacités spécifiques à la surface prévu. La rubrique exacte provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes connues

- La preuve complète du routage multi-canal en direct reste limitée.

## Preuves

### Documentation

- `docs/concepts/multi-agent.md:210`
- `docs/channels/channel-routing.md:75`
- `docs/cli/agents.md:34`

### Code source

- `src/routing/resolve-route.ts:610`
- `src/channels/plugins/configured-binding-match.ts:17`
- `src/channels/plugins/binding-routing.ts:69`

### Tests d'intégration

- `src/commands/agents.bind.matrix.integration.test.ts:21`
- `src/gateway/gateway-codex-bind.live.test.ts:466`

### Tests unitaires

- `src/routing/resolve-route.test.ts:101`

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

## Provenance de l'audit

- Source du score : `docs/kevinslin/maturity-scorecard/inventory/multi-agent-orchestration/scores.yaml`.
- Source des métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
