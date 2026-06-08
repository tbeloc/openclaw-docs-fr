---
title: "Orchestration multi-agent - Note de maturité d'isolation d'agent"
version: 3
last_refreshed: 2026-06-01
last_refreshed_by: codex
---

# Orchestration multi-agent - Note de maturité d'isolation d'agent

## Résumé

Les docs couvrent l'isolation multi-agent, les sous-agents et les outils sandbox. La source implémente la config de portée, la politique cible et la portabilité des profils d'authentification. Les tests couvrent la génération de sous-agents, la politique d'outils et les limites de session d'agent.

## Portée de la catégorie

Cette catégorie couvre la zone de capacité d'isolation d'agent définie par la taxonomie pour la surface d'orchestration multi-agent.

## Fonctionnalités

- Séparation de l'espace de travail : Gardez chaque espace de travail d'agent et répertoire d'agent distincts.
- Séparation d'état : Séparez les chemins d'état, de config et de session par agent.
- Séparation d'authentification : Gardez l'authentification du fournisseur et du canal limitée à l'agent prévu.
- Séparation de session : Évitez les chevauchements accidentels de transcription et de conversation.
- Profils d'outils : Appliquez la posture d'outils et de sandbox par agent.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false` et `repository_count=2`.
- discrawl : `discrawl status --json` réussi avec `generated_at=2026-06-01T23:01:14Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : Les docs couvrent l'isolation multi-agent, les sous-agents et les outils sandbox ; La source implémente la config de portée, la politique cible et la portabilité des profils d'authentification ; Les tests couvrent la génération de sous-agents, la politique d'outils et les limites de session d'agent.
- Signaux négatifs : L'isolation est large mais s'étend toujours sur plusieurs couches de politique, ce qui réduit la qualité des preuves.
- Lacunes d'intégration : L'isolation est large mais s'étend toujours sur plusieurs couches de politique, ce qui réduit la qualité des preuves.

Étiquettes de couverture : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70` et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

Les mesures de couverture intègrent l'intégration, e2e, live ou des preuves de flux d'exécution réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Beta (78%)`
- Rapports Gitcrawl : Vérification de fraîcheur globale réussie ; aucune requête gitcrawl spécifique à la catégorie n'a été exécutée dans ce package de notation surface-sous-agent.
- Rapports Discrawl : Vérification de fraîcheur globale réussie ; aucune recherche Discord spécifique à la catégorie n'a été exécutée dans ce package de notation surface-sous-agent.
- Bonnes qualités : Les docs couvrent l'isolation multi-agent, les sous-agents et les outils sandbox ; La source implémente la config de portée, la politique cible et la portabilité des profils d'authentification.
- Mauvaises qualités : L'isolation est large mais s'étend toujours sur plusieurs couches de politique, ce qui réduit la qualité des preuves.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, live et d'exécution réel a été utilisée uniquement pour la couverture et non comme entrées de qualité.

Étiquettes de qualité : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70` et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, live ou d'exécution réel comme entrée de notation.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : Noté par rapport à `.agents/skills/claw-score/references/completeness/multi-agent-orchestration.md`.
- Signaux positifs : Les preuves archivées docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la séparation d'espace de travail, la séparation d'état, la séparation d'authentification, la séparation de session et les profils d'outils.
- Signaux négatifs : L'isolation est large mais s'étend toujours sur plusieurs couches de politique, ce qui réduit la qualité des preuves.
- Branches de capacité manquantes : L'isolation est large mais s'étend toujours sur plusieurs couches de politique, ce qui réduit la qualité des preuves.

Étiquettes de complétude : `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`, `Alpha = 50-70` et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La complétude mesure la façon dont cette catégorie fournit complètement l'ensemble de capacités spécifiques à la surface prévu. Le rubrique exact provient du fichier `completeness_instructions` de la taxonomie de la surface de notation.

## Lacunes connues

- L'isolation est large mais s'étend toujours sur plusieurs couches de politique, ce qui réduit la qualité des preuves.

## Preuves

### Docs

- `docs/concepts/multi-agent.md:9`
- `docs/tools/subagents.md:11`
- `docs/tools/multi-agent-sandbox-tools.md:9`

### Source

- `src/agents/agent-scope-config.ts:105`
- `src/agents/subagent-target-policy.ts:47`
- `src/agents/auth-profiles/portability.ts:28`

### Tests d'intégration

- Aucun identifié dans cette tranche de notation.

### Tests unitaires

- `src/agents/subagent-spawn.test.ts:120`
- `src/agents/agent-tools.policy.test.ts:186`
- `src/commands/agent/session.test.ts:87`

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

## Provenance d'audit

- Source de score : `docs/kevinslin/maturity-scorecard/inventory/multi-agent-orchestration/scores.yaml`.
- Source de métadonnées de taxonomie : `.agents/skills/claw-score/taxonomy.yaml`.
- Référence source OpenClaw : `openclaw@29dd7847fd`.
