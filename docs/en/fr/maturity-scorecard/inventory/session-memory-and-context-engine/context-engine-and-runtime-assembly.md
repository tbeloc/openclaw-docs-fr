---
title: "Session, memory, and context engine - Context Engine Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Session, memory, and context engine - Context Engine Maturity Note

## Résumé

Le contrat context-engine est de première classe : la documentation décrit les hooks de cycle de vie, le code source définit une interface typée et un registre, et les helpers d'exécution intègrent les moteurs dans les exécutions embarquées et CLI. Les preuves d'archive sont relativement silencieuses concernant la douleur utilisateur actuelle, mais le harnais app-server Codex reste un écart de parité documenté et la sémantique de compaction détenue par le moteur reste facile à mal utiliser.

## Portée de la catégorie

Cette catégorie couvre la sélection du context-engine, le registre, la compatibilité d'hôte, le fallback hérité, le cycle de vie assemble/ingest/after-turn/compact, la projection de contexte d'exécution, et la limite entre l'assemblage de contexte OpenClaw et l'historique du harnais natif.

## Fonctionnalités

- Context Engine : Couvre Context Engine dans la sélection du context-engine, le registre, la compatibilité d'hôte, le fallback hérité, le cycle de vie assemble/ingest/after-turn/compact, la projection de contexte d'exécution, et la limite entre l'assemblage de contexte OpenClaw et l'historique du harnais natif.
- Runtime Assembly : Couvre Runtime Assembly dans la sélection du context-engine, le registre, la compatibilité d'hôte, le fallback hérité, le cycle de vie assemble/ingest/after-turn/compact, la projection de contexte d'exécution, et la limite entre l'assemblage de contexte OpenClaw et l'historique du harnais natif.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (72%)`
- Signaux positifs : la documentation, l'interface, le registre, la compatibilité d'hôte, les helpers de délégation, et les tests de cycle de vie CLI sont présents.
- Signaux négatifs : la couverture actuelle est la plus forte au niveau des helpers unitaires/d'exécution ; moins de scénarios utilisateur complets prouvent les moteurs de plugin sur tous les harnais et les chemins de cycle de vie des sous-agents.
- Lacunes d'intégration : ajouter un scénario de fixture context-engine plugin pour OpenClaw embarqué, CLI runner, projection app-server Codex, `/compact` manuel, et fork/cleanup de sous-agent.

## Score de qualité

- Score : `Stable (80%)`
- Rapports Gitcrawl : la requête de problème context-engine exacte n'a retourné aucun résultat.
- Rapports Discrawl : l'archive Discord enregistre la documentation context-engine, la validation de contrat, et les conseils utilisateur ; le principal risque signalé était les défaillances de contrat opaques avant validation et la parité Codex/harnais.
- Bonnes qualités : le contrat est explicite, la validation fail-fast existe, et la documentation avertit que la compaction no-op sur un moteur actif n'est pas sûre.
- Mauvaises qualités : l'historique de thread natif Codex reste un propriétaire d'état séparé, donc projeter le contexte OpenClaw dans ce harnais est intrinsèquement limité.
- Exclu de la qualité : la profondeur des tests unitaires, d'intégration, e2e, en direct, et de flux d'exécution.

## Score de complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/session-memory-and-context-engine.md`.
- Signaux positifs : les preuves archivées de documentation, code source, test, Gitcrawl, et Discrawl couvrent la portée de taxonomie pour Context Engine, Runtime Assembly.
- Signaux négatifs : la note archivée a précédé la notation de Complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisé pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La parité du cycle de vie context-engine de l'app-server Codex est spécifiée mais pas entièrement documentée comme complète.
- La compaction détenue par le moteur nécessite des choix soigneux de l'opérateur/auteur de plugin.

## Preuves

### Documentation

- `docs/concepts/context.md:166` dit qu'OpenClaw délègue l'assemblage, `/compact`, et les hooks de cycle de vie de sous-agent associés au moteur actif.
- `docs/concepts/context-engine.md:70` énumère les points de cycle de vie ; `docs/concepts/context-engine.md:178` documente l'interface ; `docs/concepts/context-engine.md:254` explique `ownsCompaction`.
- `docs/plan/codex-context-engine-harness.md:16` décrit l'objectif de parité du harnais Codex et `docs/plan/codex-context-engine-harness.md:115` dit que l'app-server Codex reste canonique pour l'état de thread natif.

### Code source

- `src/context-engine/types.ts:230` définit le contrat `ContextEngine`.
- `src/context-engine/registry.ts:374` enregistre les moteurs ; `src/context-engine/registry.ts:527` résout les moteurs actifs ; `src/context-engine/registry.ts:454` valide les méthodes requises.
- `src/context-engine/host-compat.ts:21` définit le support d'hôte embarqué et `src/context-engine/host-compat.ts:34` définit le support d'hôte app-server Codex.
- `src/context-engine/delegate.ts:33` permet aux moteurs non-propriétaires de déléguer la compaction à l'exécution.

### Tests d'intégration

- `src/agents/cli-runner.context-engine.test.ts:145` finalise les tours CLI réussis avec le context-engine actif.
- `src/agents/cli-runner.context-engine.test.ts:256` charge l'historique context-engine non borné séparément de l'historique des hooks.
- `src/agents/embedded-agent-runner/run/attempt.spawn-workspace.context-engine.test.ts` couvre la propagation context-engine dans les espaces de travail générés.

### Tests unitaires

- `src/context-engine/context-engine.test.ts:386` enregistre et résout un moteur simulé.
- `src/context-engine/context-engine.test.ts:415` vérifie `delegateCompactionToRuntime`.
- `src/agents/harness/context-engine-lifecycle.test.ts:50` garde les messages de contexte d'exécution cachés hors des hooks d'assemblage.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues "context engine compact plugins.slots.contextEngine" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats :

- A retourné `[]`.

### Requêtes Discrawl

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "context engine compact plugins.slots.contextEngine"`

Résultats :

- A retourné la documentation context-engine et la discussion de support, un commentaire PR de validation de contrat, et une discussion de `plugins.slots.contextEngine` pour la sélection de contexte dynamique par tour.
