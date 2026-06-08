---
title: "Orchestration multi-agents - Note de maturité de configuration d'agent"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Orchestration multi-agents - Note de maturité de configuration d'agent

## Résumé

La CLI, l'assistant et la documentation/source Gateway couvrent la création et la suppression d'agents. Les tests exercent le comportement d'ajout/suppression et de mutation Gateway.

## Portée de la catégorie

Cette catégorie couvre la zone de capacité de configuration d'agent définie par la taxonomie pour la surface d'orchestration multi-agents.

## Fonctionnalités

- Ajouter des agents : Créer des agents nommés supplémentaires à partir de la CLI ou des flux d'intégration.
- Liste d'agents et suppression : Inspecter et supprimer les agents configurés.
- Fichiers d'identité : Définir et maintenir les métadonnées d'identité de l'agent.
- Configuration non-interactive : Créer des agents de script avec des options de modèle et de route.
- Agent unique par défaut : Préserver la topologie main-agent par défaut.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : La CLI, l'assistant et la documentation/source Gateway couvrent la création et la suppression d'agents ; Les tests exercent le comportement d'ajout/suppression et de mutation Gateway.
- Signaux négatifs : Une preuve fraîche de configuration multi-agents en direct n'a pas été produite dans cette tranche de notation.
- Lacunes d'intégration : Une preuve fraîche de configuration multi-agents en direct n'a pas été produite dans cette tranche de notation.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

Les mesures de couverture intègrent l'intégration, e2e, en direct ou des preuves de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Stable (82%)`
- Rapports Gitcrawl : La vérification de fraîcheur globale a réussi ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation surface-subagent.
- Rapports Discrawl : La vérification de fraîcheur globale a réussi ; aucune recherche discrawl spécifique à la catégorie n'a été exécutée dans ce package de notation surface-subagent.
- Bonnes qualités : La CLI, l'assistant et la documentation/source Gateway couvrent la création et la suppression d'agents.
- Mauvaises qualités : Aucune faiblesse spécifique à la qualité de mise en œuvre n'a été identifiée séparément des autres classes de lacunes dans cette tranche de notation.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et d'exécution réel a été utilisée uniquement pour la couverture et non comme entrées de qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score d'exhaustivité

- Score : `Stable (84%)`
- Instructions de surface : Noté par rapport à `.agents/skills/claw-score/references/completeness/multi-agent-orchestration.md`.
- Signaux positifs : Les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Ajouter des agents, Liste d'agents et suppression, Fichiers d'identité, Configuration non-interactive, Agent unique par défaut.
- Signaux négatifs : Une preuve fraîche de configuration multi-agents en direct n'a pas été produite dans cette tranche de notation.
- Branches de capacité manquantes : Une preuve fraîche de configuration multi-agents en direct n'a pas été produite dans cette tranche de notation.

Étiquettes d'exhaustivité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.

L'exhaustivité mesure la complétude avec laquelle cette catégorie fournit l'ensemble de capacités spécifiques à la surface prévu. Le rubrique exact provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes connues

- Une preuve fraîche de configuration multi-agents en direct n'a pas été produite dans cette tranche de notation.

## Preuves

### Docs

- `docs/cli/agents.md:20`
- `docs/start/wizard.md:111`
- `docs/start/wizard-cli-automation.md:202`

### Source

- `src/commands/agents.commands.add.ts:121`
- `src/commands/agents.commands.delete.ts:83`
- `src/gateway/server-methods/agents.ts:507`

### Tests d'intégration

- `src/gateway/server-methods/agents-mutate.test.ts:527`

### Tests unitaires

- `src/commands/agents.add.test.ts:98`
- `src/commands/agents.delete.test.ts:117`

### Commandes de validation de surface

- `gitcrawl doctor --json` : `pass` - La fraîcheur des archives a été vérifiée avant la notation.
- `discrawl status --json` : `pass` - La fraîcheur des archives Discord a été vérifiée avant la notation.

### Requêtes Gitcrawl

Requête : vérification de fraîcheur globale uniquement.

Résultats :

- `gitcrawl doctor --json` réussi ; les requêtes de problèmes spécifiques à la catégorie n'ont pas été exécutées dans ce package de notation surface-subagent.

### Requêtes Discrawl

Requête : vérification de fraîcheur globale uniquement.

Résultats :

- `discrawl status --json` réussi ; les recherches Discord spécifiques à la catégorie n'ont pas été exécutées dans ce package de notation surface-subagent.

## Provenance d'audit

- Source du score : `docs/kevinslin/maturity-scorecard/inventory/multi-agent-orchestration/scores.yaml`.
- Source des métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
