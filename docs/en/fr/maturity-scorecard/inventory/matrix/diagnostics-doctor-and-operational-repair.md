---
title: "Matrix - Diagnostics, Doctor, and Operational Repair Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Matrix - Diagnostics, Doctor, and Operational Repair Maturity Note

## Summary

Les diagnostics et réparations Matrix sont pratiques et basés sur les sources. Le chemin doctor
détecte les installations de plugins obsolètes, les alias de configuration hérités, la politique DM hérité, la migration d'état hérité, la migration d'état chiffré hérité, et les snapshots de migration.
Les sondes d'exécution, la recherche de répertoire, l'intégration de migration au démarrage, les commandes de statut, et les diagnostics d'exécution Matrix QA ajoutent plus de visibilité opérationnelle.
La couverture et la qualité sont toutes deux en version bêta car la surface de l'outil est large et utile,
mais les preuves d'archive montrent que les opérateurs atteignent toujours les flux de réparation à partir des problèmes Matrix actifs.

## Category Scope

- Avertissements Matrix doctor, normalisation de la configuration, nettoyage de la configuration de plugin obsolète,
  réparation doctor, migration d'état hérité, migration d'état chiffré hérité, et
  snapshots de sauvegarde.
- Sonde/statut Matrix, recherche de répertoire en direct, diagnostics CLI, résumés d'exécution QA, et intégration de migration au démarrage.
- Hors de portée : assistant de configuration, routage normal des messages, livraison sortante, et
  E2EE en interne sauf où la réparation/statut les expose.

## Features

- Avertissements Matrix doctor : avertissements Matrix doctor, normalisation de la configuration, et nettoyage de la configuration de plugin obsolète.
- Sonde/statut Matrix : sonde/statut Matrix, recherche de répertoire en direct, diagnostics CLI, et statut d'exécution QA.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Beta (74%)`
- Positive signals:
  - Les docs couvrent les snapshots de migration, les avertissements de migration, les conseils de récupération,
    les vérifications de dépannage, la résolution de cible, les références de configuration, et les docs connexes.
  - La source implémente les avertissements/réparations doctor, le nettoyage du chemin de plugin obsolète, la normalisation de la configuration hérité, les snapshots de migration, la sonde, et la recherche de répertoire en direct.
  - Les tests unitaires couvrent les aperçus doctor, les changements de réparation, la configuration de plugin obsolète,
    la normalisation de la configuration hérité, la recherche de répertoire, la sonde, la maintenance au démarrage, et le comportement du répertoire de canal.
  - Les preuves d'intégration couvrent le câblage de migration Matrix au démarrage de la passerelle et les diagnostics d'exécution QA.
- Negative signals:
  - Les diagnostics sont larges mais réactifs ; ils ne prouvent pas que les chemins d'exécution sous-jacents sont stables.
  - Les requêtes spécifiques aux diagnostics Discrawl et gitcrawl ont retourné peu de signal direct, donc les preuves d'archive sont principalement des incidents Matrix larges.
- Integration gaps:
  - Ajouter un scénario de réparation d'opérateur qui exécute doctor avant et après une migration Matrix et capture les avertissements, changements, et statut exacts.
  - Ajouter des artefacts de diagnostics en direct pour les défaillances de préparation Matrix.
  - Ajouter une voie QA pour le comportement de recherche de répertoire et de sonde par rapport à un vrai serveur d'accueil.

Coverage labels:

- `Lovable`: 95-100
- `Stable`: 80-95
- `Beta`: 70-80
- `Alpha`: 50-70
- `Experimental`: 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct, ou les preuves de flux d'exécution réel dans le composant. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Quality Score

- Score: `Beta (74%)`
- Gitcrawl reports:
  - Query `gitcrawl --json search openclaw/openclaw --query "Matrix doctor status migration repair"` returned open PR #87141, a broad plugin hardening PR whose snippet referenced doctor migration/doc changes.
  - Broad query `gitcrawl --json search openclaw/openclaw --query "Matrix"` returned open Matrix runtime, routing, media, and E2EE issues that would likely rely on diagnostics and repair flows.
- Discrawl reports:
  - Query `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix doctor status migration repair"` returned no hits.
  - Broad query `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"` returned release chatter and scorecard discussion.
- Good qualities:
  - La réparation doctor crée ou réutilise un snapshot de migration Matrix avant d'appliquer
    les mises à niveau Matrix.
  - La migration de configuration hérité est explicite, consciente du chemin, et préserve les politiques plus sûres
    quand c'est possible.
  - La sonde échoue avec des erreurs concrètes d'authentification manquante et d'exécution.
  - La recherche de répertoire utilise les chemins de client HTTP Matrix renforcés et gère les identifiants Matrix directs sans appels réseau inutiles.
- Bad qualities:
  - Les diagnostics sont répartis entre doctor, CLI, sonde, répertoire, maintenance au démarrage, exécution QA, et docs.
  - Certaines réparations nécessitent une mutation d'état, donc l'échec du snapshot doit bloquer la réparation.
  - Les incidents Matrix actifs montrent que les diagnostics doivent rester alignés avec les modes de défaillance d'exécution en évolution rapide.
- Excluded from quality:
  - Je n'ai pas augmenté ou diminué la qualité en raison de la couverture des tests unitaires, d'intégration, e2e, en direct, ou d'exécution réel.

Quality labels:

- `Lovable`: 95-100
- `Stable`: 80-95
- `Beta`: 70-80
- `Alpha`: 50-70
- `Experimental`: 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct, ou d'exécution réel comme entrée de notation.

## Completeness Score

- Score: `Beta (74%)`
- Surface instructions: evaluated against `references/completeness/matrix.md`.
- Positive signals: archived docs, source, test, Gitcrawl, and Discrawl evidence cover the taxonomy scope for Matrix doctor warnings, Matrix probe/status.
- Negative signals: the archived note predated process-version-3 Completeness scoring, so this score is initialized from the same evidence breadth and known-gap record used for the archived Coverage score.
- Missing capability branches: see `## Known Gaps` and `## Evidence` below for the recorded missing branches and operator-visible caveats.

## Known Gaps

- Ajouter une transcription de réparation actuelle montrant les avertissements doctor avant la réparation,
  création/réutilisation du snapshot de migration, configuration post-réparation, et résultat de statut.
- Lier les classes d'incidents Matrix actifs à des commandes de diagnostics spécifiques.
- Ajouter des preuves de répertoire/sonde en direct pour compléter les tests source et unitaires.

## Evidence

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/matrix-migration.md:21`
  documents automatic migration snapshots.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix-migration.md:146`
  documents common messages and recovery guidance.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix-migration.md:340`
  documents troubleshooting checks and related docs.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:812` documents
  target resolution.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:831` documents config
  reference, access, reply behavior, reaction settings, tooling, and approvals.

### Source

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/doctor.ts:50` formats
  Matrix legacy state previews.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/doctor.ts:62` formats
  legacy encrypted-state migration previews.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/doctor.ts:83`
  collects stale plugin install path warnings.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/doctor.ts:131`
  applies Matrix doctor repair and creates migration snapshots.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/doctor.ts:207` runs
  Matrix doctor config sequence.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/doctor-contract.ts:121`
  declares legacy Matrix config rules.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/doctor-contract.ts:166`
  normalizes compatibility config.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/probe.ts:25`
  probes Matrix auth and homeserver reachability.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/directory-live.ts:105`
  lists Matrix directory peers live.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/directory-live.ts:181`
  lists Matrix directory groups live.

### Integration tests

- `/Users/kevinlin/code/openclaw/src/gateway/server.startup-matrix-migration.integration.test.ts:4`
  covers gateway startup channel maintenance wiring.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/runtime.test.ts:342`
  records default and per-scenario Matrix config snapshots in summaries.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/runtime.test.ts:449`
  preserves negative-scenario artifacts in the Matrix summary.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/runtime.test.ts:494`
  keeps failing Matrix scenario details and timings complete in summary and
  report output.
- `/Users/kevinlin/code/openclaw/extensions/qa-matrix/src/runners/contract/scenario-runtime-cli.test.ts:24`
  redacts secret CLI arguments in diagnostic command text.

### Unit tests

- `/Users/kevinlin/code/openclaw/extensions/matrix/src/doctor.test.ts:64`
  formats state and crypto previews.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/doctor.test.ts:98`
  warns on stale plugin paths and cleans them.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/doctor.test.ts:125`
  surfaces sequence warnings and repair changes.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/doctor.test.ts:166`
  normalizes legacy Matrix room allow aliases.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/doctor.test.ts:260`
  migrates legacy trusted DM policy with allowFrom to allowlist.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/directory-live.test.ts:72`
  passes dispatcher policy through to live directory client.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/directory-live.test.ts:156`
  resolves prefixed room aliases through the hardened Matrix HTTP client.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/matrix/probe.test.ts`
  covers Matrix probe behavior.
- `/Users/kevinlin/code/openclaw/extensions/matrix/src/startup-maintenance.test.ts`
  covers startup maintenance behavior.

### Gitcrawl queries

- `gitcrawl --json search openclaw/openclaw --query "Matrix doctor status migration repair"`
  returned open PR #87141 with a snippet referencing doctor migration/doc
  changes.
- `gitcrawl --json search openclaw/openclaw --query "Matrix"` returned broad
  Matrix issues that diagnostics and repair flows must support.

### Discrawl queries

- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix doctor status migration repair"`
  returned no hits.
- `/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 10 "Matrix openclaw"`
  returned release chatter and scorecard discussion.
