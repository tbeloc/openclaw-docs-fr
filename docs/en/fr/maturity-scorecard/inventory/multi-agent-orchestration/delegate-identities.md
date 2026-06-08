---
title: "Orchestration multi-agents - Note de maturité des identités déléguées"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Orchestration multi-agents - Note de maturité des identités déléguées

## Résumé

La documentation décrit l'architecture des délégués et les attentes en matière de sécurité. Le code source expose la configuration des identités et les commandes CLI d'identité. Les tests couvrent le comportement des commandes d'identité et l'intégration des routes.

## Portée de la catégorie

Cette catégorie couvre la zone de capacité des identités déléguées définie par la taxonomie pour la surface d'orchestration multi-agents.

## Fonctionnalités

- Délégués nommés : Créer des agents avec une identité organisationnelle explicite.
- Modèle d'autorité : Définir le périmètre des actions qu'un délégué peut effectuer au nom d'un utilisateur ou d'une organisation.
- Niveaux de délégation : Prendre en charge les modes lecture seule, brouillon, envoi au nom de, et proactif.
- Délégation d'identité : Configurer la délégation Microsoft 365 ou Google Workspace avec le principe du moindre privilège.
- Assistants organisationnels : Exécuter des modèles de délégation multi-organisations à partir d'une seule passerelle.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (45%)`
- Signaux positifs : La documentation décrit l'architecture des délégués et les attentes en matière de sécurité ; le code source expose la configuration des identités et les commandes CLI d'identité ; les tests couvrent le comportement des commandes d'identité et l'intégration des routes.
- Signaux négatifs : L'identité déléguée reste davantage une politique/runbook qu'un flux de travail produit appliqué de bout en bout ; la couverture est inférieure à Alpha car aucune preuve d'exécution récente et aucun test d'application large n'ont été trouvés.
- Lacunes d'intégration : L'identité déléguée reste davantage une politique/runbook qu'un flux de travail produit appliqué de bout en bout ; la couverture est inférieure à Alpha car aucune preuve d'exécution récente et aucun test d'application large n'ont été trouvés.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Expérimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La couverture mesure l'intégration, les preuves e2e, en direct ou de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : La vérification de fraîcheur globale a réussi ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Rapports Discrawl : La vérification de fraîcheur globale a réussi ; aucune recherche Discord spécifique à la catégorie n'a été exécutée dans ce package de notation de sous-agent de surface.
- Bonnes qualités : La documentation décrit l'architecture des délégués et les attentes en matière de sécurité ; le code source expose la configuration des identités et les commandes CLI d'identité.
- Mauvaises qualités : L'identité déléguée reste davantage une politique/runbook qu'un flux de travail produit appliqué de bout en bout.
- Exclus de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et d'exécution réel a été utilisée uniquement pour la couverture et non comme entrées de qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Expérimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score d'exhaustivité

- Score : `Alpha (62%)`
- Instructions de surface : Noté par rapport à `.agents/skills/claw-score/references/completeness/multi-agent-orchestration.md`.
- Signaux positifs : Les preuves archivées de documentation, code source, tests, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les délégués nommés, le modèle d'autorité, les niveaux de délégation, la délégation d'identité, les assistants organisationnels.
- Signaux négatifs : L'identité déléguée reste davantage une politique/runbook qu'un flux de travail produit appliqué de bout en bout ; la couverture est inférieure à Alpha car aucune preuve d'exécution récente et aucun test d'application large n'ont été trouvés.
- Branches de capacité manquantes : L'identité déléguée reste davantage une politique/runbook qu'un flux de travail produit appliqué de bout en bout ; la couverture est inférieure à Alpha car aucune preuve d'exécution récente et aucun test d'application large n'ont été trouvés.

Étiquettes d'exhaustivité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Expérimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

L'exhaustivité mesure la complétude avec laquelle cette catégorie fournit l'ensemble de capacités spécifiques à la surface prévu. La rubrique exacte provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes connues

- L'identité déléguée reste davantage une politique/runbook qu'un flux de travail produit appliqué de bout en bout.
- La couverture est inférieure à Alpha car aucune preuve d'exécution récente et aucun test d'application large n'ont été trouvés.

## Preuves

### Documentation

- `docs/concepts/delegate-architecture.md:8`
- `docs/concepts/delegate-architecture.md:160`
- `docs/gateway/security/index.md:92`

### Code source

- `src/config/types.agents.ts:79`
- `src/config/zod-schema.core.ts:578`
- `src/commands/agents.commands.identity.ts:64`

### Tests d'intégration

- Aucun identifié dans cette tranche de notation.

### Tests unitaires

- `src/commands/agents.identity.test.ts:72`
- `src/commands/agents.add.test.ts:139`
- `src/routing/resolve-route.test.ts:317`

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

## Provenance d'audit

- Source du score : `docs/kevinslin/maturity-scorecard/inventory/multi-agent-orchestration/scores.yaml`.
- Source des métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
