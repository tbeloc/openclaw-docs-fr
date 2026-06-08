---
title: "Session, memory, and context engine - Token Management Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Session, memory, and context engine - Token Management Maturity Note

## Résumé

OpenClaw dispose d'une implémentation large de compaction et d'élagage : résumés sémantiques,
estimation des jetons pré-prompt, récupération de débordement, troncature des résultats d'outils, élagage
du contexte, hooks de fournisseur, et `sessions.compact` manuel. La couverture est relativement
forte pour les chemins algorithmiques à haut risque, mais les rapports actifs montrent que
le débordement, les mathématiques des jetons de réserve, la direction de l'utilisateur, et la compaction
détenue par le moteur restent des points faibles visibles par l'opérateur.

## Portée de la catégorie

Cette catégorie couvre la compaction manuelle et automatique, les vérifications de débordement préemptives,
l'estimation de la fenêtre de contexte, l'élagage des sessions, la réduction des résultats d'outils,
les fournisseurs de compaction, le comportement de retry/timeout, et les points de contrôle de transcription compactée.

## Fonctionnalités

- Compaction : Couvre la Compaction sur la compaction manuelle et automatique, les vérifications de débordement préemptives, l'estimation de la fenêtre de contexte, l'élagage des sessions, la réduction des résultats d'outils, les fournisseurs de compaction, le comportement de retry/timeout, et les points de contrôle de transcription compactée.
- Élagage : Couvre l'Élagage sur la compaction manuelle et automatique, les vérifications de débordement préemptives, l'estimation de la fenêtre de contexte, l'élagage des sessions, la réduction des résultats d'outils, les fournisseurs de compaction, le comportement de retry/timeout, et les points de contrôle de transcription compactée.
- Pression des jetons : Couvre la Pression des jetons sur la compaction manuelle et automatique, les vérifications de débordement préemptives, l'estimation de la fenêtre de contexte, l'élagage des sessions, la réduction des résultats d'outils, les fournisseurs de compaction, le comportement de retry/timeout, et les points de contrôle de transcription compactée.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : la préparation de la compaction, la sélection des points de coupure, les résumés de branche, les décisions de débordement préemptif, la retry à l'exécution, la compaction manuelle de Gateway, et l'élagage du contexte ont tous une couverture de test ciblée.
- Signaux négatifs : les scénarios complets de session utilisateur longue durée sur le basculement de fournisseur, la compaction détenue par le moteur de contexte, et la livraison de canal ne sont pas également représentés.
- Lacunes d'intégration : ajouter un smoke test de version qui conduit une vraie session longue à travers la précheck, la compaction sémantique, la retry, la restauration du point de contrôle, et l'affichage WebChat/historique.

## Score de qualité

- Score : `Alpha (60%)`
- Rapports Gitcrawl : les problèmes ouverts couvrent la mort silencieuse de débordement préemptif, la compaction dirigée par l'utilisateur, les zones mortes de jetons de réserve, et le comportement de basculement conscient du contexte.
- Rapports Discrawl : les résultats de l'archive Discord incluent des commentaires d'examen sur la compaction détenue par le moteur étant contournée, les erreurs de débordement masquées, et les corrections de serrage des jetons de réserve.
- Bonnes qualités : le code a des estimations explicites de pression de jetons, des routes de basculement, des gardes de timeout, et des résumés persistants.
- Mauvaises qualités : la récupération de débordement reste complexe et a produit des rapports de masquage, zone morte, et défaillance silencieuse visibles par l'utilisateur.
- Exclu de la qualité : la profondeur des tests unitaires, d'intégration, e2e, en direct, et de flux d'exécution.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/session-memory-and-context-engine.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour Compaction, Élagage, Pression des jetons.
- Signaux négatifs : la note archivée a précédé le score de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les causes profondes du débordement de contexte peuvent toujours être difficiles à identifier pour les opérateurs.
- La compaction détenue par le moteur et la récupération de débordement intégrée ont besoin de limites de comportement très claires.

## Preuves

### Docs

- `docs/concepts/compaction.md:11` explique le remplacement de résumé et la persistance de la transcription.
- `docs/concepts/context.md:156` dit que la compaction persiste les résumés tandis que l'élagage n'affecte que l'assemblage du prompt.
- `docs/reference/session-management-compaction.md:242` documente les entrées de compaction persistées ; `docs/reference/session-management-compaction.md:272` documente les déclencheurs de compaction automatique et la récupération de débordement.

### Source

- `packages/agent-core/src/harness/compaction/compaction.ts:226` décide s'il faut compacter ; `packages/agent-core/src/harness/compaction/compaction.ts:616` prépare la compaction ; `packages/agent-core/src/harness/compaction/compaction.ts:712` exécute la compaction.
- `src/agents/embedded-agent-runner/run/preemptive-compaction.ts:242` décide les routes de compaction pré-prompt.
- `src/agents/embedded-agent-runner/run/compaction-retry-aggregate-timeout.ts:1` limite l'attente de retry.
- `src/agents/agent-hooks/context-pruning/pruner.ts:287` élague les messages de contexte.

### Tests d'intégration

- `src/gateway/server.sessions.compaction.test.ts:277` exécute `sessions.compact` manuel via Gateway RPC.
- `src/agents/embedded-agent-runner/run.overflow-compaction.test.ts:1739` vérifie le routage de retry de compaction déclenché par débordement.
- `src/infra/heartbeat-runner.transcript-prune.test.ts:88` couvre le comportement d'élagage de transcription de heartbeat.

### Tests unitaires

- `src/agents/embedded-agent-runner/run/preemptive-compaction.test.ts:102` demande une compaction préemptive quand le budget de réserve est dépassé.
- `src/agents/embedded-agent-runner/run/preemptive-compaction.test.ts:357` route la troncature directe des résultats d'outils quand les queues d'outils peuvent absorber le débordement.
- `src/plugins/compaction-provider.test.ts` couvre le comportement du registre de fournisseur.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues "compaction context overflow preemptive compaction" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats :

- Retourné ouvert `#84536` mort silencieuse de débordement préemptif, `#65502` basculement conscient du contexte, `#84571` compaction dirigée par l'utilisateur, et `#66830` zone morte de jetons de réserve.

### Requêtes Discrawl

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "compaction context overflow preemptive compaction"`

Résultats :

- Retourné discussion d'archive d'estimation pré-envoi implémentée, erreurs de débordement masquées, risque d'examen de compaction détenue par le moteur, serrage de jetons de réserve, et assemblage du moteur de contexte pendant la compaction.
