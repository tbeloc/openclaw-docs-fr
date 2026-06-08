---
title: "Orchestration multi-agents - Note de Maturité des Voies Spécialisées"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Orchestration multi-agents - Note de Maturité des Voies Spécialisées

## Résumé

La documentation décrit les voies spécialisées parallèles, les sous-agents et les tâches d'automatisation. Le code source implémente la génération de sous-agents, le gestionnaire d'exécution du registre et le comportement de la file d'attente de commandes. Les tests couvrent les limites de profondeur, le cycle de vie et les voies du serveur Gateway.

## Portée de la Catégorie

Cette catégorie couvre la zone de capacité des Voies Spécialisées définie par la taxonomie pour la surface d'orchestration multi-agents.

## Fonctionnalités

- Contrats de voie : Définir la propriété et les limites de charge de travail pour les voies spécialisées.
- Transfert en arrière-plan : Déplacer les travaux lourds vers les sous-agents ou les tâches.
- Contrôles de concurrence : Limiter la concurrence des voies et des sous-agents.
- Contrôles de priorité : Prioriser les travaux urgents ou interactifs par rapport aux travaux en arrière-plan.
- Transfert du coordinateur : Suivre les propriétaires, les demandes en double et les résumés inter-voies.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false` et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0` et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (78%)`
- Signaux positifs : La documentation décrit les voies spécialisées parallèles, les sous-agents et les tâches d'automatisation ; Le code source implémente la génération de sous-agents, le gestionnaire d'exécution du registre et le comportement de la file d'attente de commandes ; Les tests couvrent les limites de profondeur, le cycle de vie et les voies du serveur Gateway.
- Signaux négatifs : L'orchestration opérationnelle des voies est utile mais reste complexe et inégale selon les points d'entrée.
- Lacunes d'intégration : L'orchestration opérationnelle des voies est utile mais reste complexe et inégale selon les points d'entrée.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70` et `Experimental = 0-50`. Aux limites partagées, choisir l'étiquette de maturité supérieure.

Les mesures de couverture intègrent l'intégration, e2e, live ou des preuves de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl : La vérification de fraîcheur globale a réussi ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation surface-sous-agent.
- Rapports Discrawl : La vérification de fraîcheur globale a réussi ; aucune recherche discrawl spécifique à la catégorie n'a été exécutée dans ce package de notation surface-sous-agent.
- Bonnes qualités : La documentation décrit les voies spécialisées parallèles, les sous-agents et les tâches d'automatisation ; Le code source implémente la génération de sous-agents, le gestionnaire d'exécution du registre et le comportement de la file d'attente de commandes.
- Mauvaises qualités : L'orchestration opérationnelle des voies est utile mais reste complexe et inégale selon les points d'entrée.
- Exclus de la qualité : La couverture des tests unitaires, d'intégration, e2e, live et de flux d'exécution réel a été utilisée uniquement pour la Couverture et non comme entrées de Qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70` et `Experimental = 0-50`. Aux limites partagées, choisir l'étiquette de maturité supérieure.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, live ou d'exécution réel comme entrée de notation.

## Score de Complétude

- Score : `Beta (76%)`
- Instructions de surface : Noté par rapport à `.agents/skills/claw-score/references/completeness/multi-agent-orchestration.md`.
- Signaux positifs : Les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les contrats de voie, le transfert en arrière-plan, les contrôles de concurrence, les contrôles de priorité et le transfert du coordinateur.
- Signaux négatifs : L'orchestration opérationnelle des voies est utile mais reste complexe et inégale selon les points d'entrée.
- Branches de capacité manquantes : L'orchestration opérationnelle des voies est utile mais reste complexe et inégale selon les points d'entrée.

Étiquettes de complétude : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70` et `Experimental = 0-50`. Aux limites partagées, choisir l'étiquette de maturité supérieure.

La complétude mesure la façon dont cette catégorie fournit complètement l'ensemble de capacités spécifiques à la surface prévu. La rubrique exacte provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes Connues

- L'orchestration opérationnelle des voies est utile mais reste complexe et inégale selon les points d'entrée.

## Preuves

### Docs

- `docs/concepts/parallel-specialist-lanes.md:12`
- `docs/tools/subagents.md:11`
- `docs/automation/tasks.md:15`

### Source

- `src/agents/subagent-spawn.ts:1044`
- `src/agents/subagent-registry-run-manager.ts:608`
- `src/process/command-queue.ts:326`

### Tests d'intégration

- `src/gateway/server-lanes.test.ts:21`

### Tests unitaires

- `src/agents/subagent-spawn.depth-limits.test.ts:103`
- `src/agents/openclaw-tools.subagents.sessions-spawn.lifecycle.test.ts:214`

### Commandes de validation de surface

- `gitcrawl doctor --json` : `pass` - La fraîcheur de l'archive a été vérifiée avant la notation.
- `discrawl status --json` : `pass` - La fraîcheur de l'archive Discord a été vérifiée avant la notation.

### Requêtes Gitcrawl

Requête : vérification de fraîcheur globale uniquement.

Résultats :

- `gitcrawl doctor --json` réussi ; les requêtes de problèmes spécifiques à la catégorie n'ont pas été exécutées dans ce package de notation surface-sous-agent.

### Requêtes Discrawl

Requête : vérification de fraîcheur globale uniquement.

Résultats :

- `discrawl status --json` réussi ; les recherches Discord spécifiques à la catégorie n'ont pas été exécutées dans ce package de notation surface-sous-agent.

## Provenance de l'Audit

- Source du score : `docs/kevinslin/maturity-scorecard/inventory/multi-agent-orchestration/scores.yaml`.
- Source des métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
