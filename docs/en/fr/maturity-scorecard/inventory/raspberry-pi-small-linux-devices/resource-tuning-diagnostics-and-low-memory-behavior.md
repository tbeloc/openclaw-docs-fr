---
title: "Raspberry Pi / small Linux devices - Performance and Diagnostics Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Raspberry Pi / small Linux devices - Performance and Diagnostics Maturity Note

## Summary

Cette note migre les preuves de maturité archivées pour `Raspberry Pi / small Linux devices` / `Resource Tuning, Diagnostics, and Low-memory Behavior` dans l'inventaire actuel du scorecard process-version-3.

## Category Scope

Inclus dans cette catégorie :

- Swap and low-RAM tuning: Définit la configuration de Swap et low-RAM tuning, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Resource Tuning and Diagnostics.
- USB SSD guidance: Définit les conseils USB SSD, la configuration, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Resource Tuning and Diagnostics.
- Compile cache/no-respawn settings: Définit les paramètres Compile cache/no-respawn, la configuration, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Resource Tuning and Diagnostics.
- OOM/performance troubleshooting: Définit la résolution des problèmes OOM/performance, la configuration, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Resource Tuning and Diagnostics.
- Diagnostics bundles: Définit les bundles Diagnostics, la configuration, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Resource Tuning and Diagnostics.

## Features

- Swap and low-RAM tuning: Définit la configuration de Swap et low-RAM tuning, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Resource Tuning and Diagnostics.
- USB SSD guidance: Définit les conseils USB SSD, la configuration, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Resource Tuning and Diagnostics.
- Compile cache/no-respawn settings: Définit les paramètres Compile cache/no-respawn, la configuration, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Resource Tuning and Diagnostics.
- OOM/performance troubleshooting: Définit la résolution des problèmes OOM/performance, la configuration, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Resource Tuning and Diagnostics.
- Diagnostics bundles: Définit les bundles Diagnostics, la configuration, les identifiants, la configuration et le comportement de vérification de l'opérateur pour Resource Tuning and Diagnostics.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Beta (75%)`
- Positive signals: La documentation Raspberry Pi inclut swap, USB SSD, compile cache, mode no-respawn, systemd drop-ins, conseils sur le modèle cloud, dépannage, persistance et sauvegardes. La source Linux inclut le wrapping OOM score et des conseils d'optimisation au démarrage pour les hôtes ARM/low-memory.
- Negative signals: Les diagnostics et le tuning des ressources sont larges plutôt que spécifiques à Pi, et les résultats d'archive montrent des problèmes répétés de performance Pi et QMD/native dans le monde réel.
- Integration gaps: Les vérifications de mémoire au démarrage et les benchmarks de redémarrage existent, mais il n'y a pas de gate low-memory spécifique au matériel Pi.

## Quality Score

- Score: `Alpha (69%)`
- Gitcrawl reports: limites de ressources adaptatives, surcharge de découverte Raspberry Pi OS arm64, gardes de pression tsgo locales et rapports de saut plugin-loader montrent que les correctifs low-memory sont toujours actifs.
- Discrawl reports: boucles de timeout d'intégration QMD Pi 5 aarch64, latence Pi 5, crash npm install et timeout de poignée de main CLI montrent une douleur récurrente des petits appareils.
- Good qualities: La source contient des atténuations concrètes : ajustement OOM score enfant Linux, indices compile-cache/no-respawn et bundles diagnostics.
- Bad qualities: Le comportement low-memory visible par l'utilisateur reste assez fragile pour que le support recommande toujours des contournements tels que les modèles cloud ou le mode BM25/search.
- Excluded from quality: preuves de test unitaire, intégration, e2e, live, runtime-flow et smoke test manuel.

## Completeness Score

- Score: `Beta (75%)`
- Surface instructions: évaluées par rapport à `references/completeness/raspberry-pi-small-linux-devices.md`.
- Positive signals: les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Swap and low-RAM tuning, USB SSD guidance, Compile cache/no-respawn settings, OOM/performance troubleshooting, Diagnostics bundles.
- Negative signals: la note archivée a précédé le scoring Completeness process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score Coverage archivé.
- Missing capability branches: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Known Gaps

- Aucune cible de performance Pi 2GB ou Pi 4GB n'est appliquée dans CI.
- Le comportement QMD/local embedding sur Pi n'est pas capturé dans un tableau de support small-device net.
- Les vérifications de mémoire au démarrage sont des seuils Linux/darwin génériques, pas des seuils matériel Raspberry Pi.

## Evidence

### Docs

- `docs/install/raspberry-pi.md:77-88` recommande swap pour 2GB ou moins.
- `docs/install/raspberry-pi.md:133-148` recommande USB SSD, `NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache`, et `OPENCLAW_NO_RESPAWN=1`.
- `docs/install/raspberry-pi.md:150-172` donne les systemd drop-ins réduisant la mémoire et le tuning de redémarrage.
- `docs/install/raspberry-pi.md:174-191` dit de ne pas exécuter les LLMs locaux sur un Pi et d'utiliser les modèles API hébergés.
- `docs/install/raspberry-pi.md:212-220` dépanne les OOM kills, les performances lentes, l'échec du démarrage du service et les problèmes binaires ARM.
- `docs/platforms/linux.md:101-135` documente la pression mémoire et le comportement OOM.
- `docs/gateway/health.md:28-34` inclut les diagnostics profonds avec bundles mémoire, liveness, stabilité et redaction.
- `docs/gateway/diagnostics.md:114-155` documente l'enregistreur de stabilité et les avertissements liveness.
- `docs/gateway/diagnostics.md:192-205` documente les snapshots mémoire pré-OOM optionnels.

### Source

- `src/process/linux-oom-score.ts:3-18` explique le wrapping OOM score enfant Linux pour l'opération Gateway longue durée.
- `src/process/linux-oom-score.ts:67-77` applique le wrapper uniquement sur Linux et quand il n'est pas désactivé.
- `src/process/linux-oom-score.ts:98-115` enveloppe le spawn enfant avec `/proc/self/oom_score_adj`.
- `src/commands/doctor-platform-notes.ts:207-269` émet des indices d'optimisation au démarrage ARM/low-memory pour compile cache et `OPENCLAW_NO_RESPAWN`.
- `src/cli/gateway-cli/run-loop.ts:220-253` supporte le fallback no-respawn/in-process restart.

### Integration tests

- `scripts/check-cli-startup-memory.mjs:83-91` définit les limites RSS par défaut pour les vérifications de démarrage Linux/darwin.
- `scripts/check-cli-startup-memory.mjs:96-120` inclut les cas help, status JSON et Gateway status.
- `scripts/bench-gateway-restart.ts:38-46` enregistre RSS dans les snapshots de ressources.
- `package.json:1778` définit la vérification de mémoire au démarrage.

### Unit tests

- `src/process/linux-oom-score.test.ts:13-18` vérifie le wrapping enfant Linux.
- `src/process/linux-oom-score.test.ts:28-40` vérifie le comportement opt-out et no-shell.
- `src/process/linux-oom-score.test.ts:58-70` vérifie le comportement d'environnement renforcé.
- `src/process/supervisor/adapters/pty.test.ts:246-272` vérifie que les spawns PTY Linux sont enveloppés pour OOM score.
- `src/process/supervisor/adapters/child.test.ts:423-437` vérifie que les wrappers enfant suppriment l'environnement shell.

### Gitcrawl queries

Query: `gitcrawl search openclaw/openclaw --json --query "Raspberry Pi low memory OpenClaw"`

Results:

- Returned PR #47706 on adaptive resource limits for ARM/low-memory devices, issue #67288 on Raspberry Pi OS arm64 discovery overhead, PR #71652 on local tsgo pressure guards on Pi, and issue #78196 on plugins skipped by a Pi Gateway.

Query: `gitcrawl search openclaw/openclaw --json --query "Raspberry Pi QMD memory OpenClaw"`

Results:

- Returned storage/performance-adjacent reports but no single focused QMD memory issue in gitcrawl.

### Discrawl queries

Query: `/Users/kevinlin/.local/bin/discrawl search --limit 5 "Raspberry Pi QMD memory OpenClaw"`

Results:

- Found a Pi 5 aarch64 QMD embed timeout loop, node-llama-cpp build churn, timeout mismatch discussion, and workaround guidance to use BM25/search mode.

Query: `/Users/kevinlin/.local/bin/discrawl search --limit 5 "Pi 5 aarch64 OpenClaw gateway"`

Results:

- Found Pi 5 aarch64 server-side latency, Pi500 aarch64 npm install crash, CLI handshake timeout, and high CPU from eager-loaded channel SDKs.
