---
title: "Agent Runtime - External Runtimes and Subagents Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Agent Runtime - External Runtimes and Subagents Maturity Note

## Summary

OpenClaw traite les runtimes externes comme un mode d'exécution de première classe : les docs séparent les fournisseurs des runtimes, expliquent la propriété Codex/OpenClaw/ACP/harness externe, documentent les alias Claude CLI et Gemini CLI, et décrivent l'authentification des subagents, la livraison, le nettoyage et la récupération. Source relie les transcriptions et événements CLI via `runCliAgent`, et les tests couvrent les aperçus CLI, les sessions subagent, le nettoyage du cycle de vie et les limites de remplacement du runtime. La qualité est Alpha car les archives montrent des problèmes récurrents autour de `claude-cli`, la livraison ACP/subagent, les paramètres backend non supportés, les artefacts de trajectoire et la propagation d'authentification à partir des sessions principales.

## Category Scope

Cette catégorie couvre l'exécution visible par l'opérateur en dehors du chemin du fournisseur intégré par défaut : choisir des harnesses externes, utiliser les alias de runtime CLI, exécuter les tours de subagent et récupérer des problèmes de nettoyage, timeout ou liveness dans ces runtimes externes.

## Features

- External harness selection : Choisir les harnesses Codex app-server, ACP et autres runtimes externes.
- CLI runtime aliases : Alias de runtime et chemins d'exécution basés sur CLI tels que Claude CLI et Gemini CLI.
- Subagent turns : Générer, livrer et annoncer le travail des subagents en dehors du chemin intégré par défaut.
- Runtime recovery : Comportement de nettoyage, timeout et liveness pour les runtimes externes et les subagents.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Beta (78%)`

La couverture est bonne pour les workflows Codex/CLI/subagent, mais les harnesses externes et ACP ont moins de preuves uniformes que le runtime intégré.

## Quality Score

- Score: `Alpha (66%)`

L'exécution CLI/subagent est fonctionnelle mais opérationnellement fragile où l'authentification spécifique au backend, les limites de permission des outils, les paramètres non supportés et la livraison des résultats varient selon le runtime.

## Completeness Score

- Score: `Beta (78%)`
- Surface instructions: evaluated against `references/completeness/agent-runtime-and-provider-execution.md`.
- Positive signals: archived docs, source, test, Gitcrawl, and Discrawl evidence cover the taxonomy scope for External harness selection, CLI runtime aliases, Subagent turns, Runtime recovery.
- Negative signals: the archived note predated process-version-3 Completeness scoring, so this score is initialized from the same evidence breadth and known-gap record used for the archived Coverage score.
- Missing capability branches: see `## Known Gaps` and `## Evidence` below for the recorded missing branches and operator-visible caveats.

## Known Gaps

- Le comportement du runtime externe change avec les outils CLI en amont et nécessite plus de preuves version par version.
- L'UX des subagents et la sémantique du cycle de vie sont bien testées mais produisent toujours des rapports de terrain autour de la livraison, du routage des comptes et de la parité.
- Certains artefacts CLI et diagnostics, tels que les trajectoires pures `claude-cli`, ont des rapports de lacunes actifs.

## Evidence

### Docs

- `/Users/kevinlin/code/openclaw/docs/concepts/agent-runtimes.md` documents runtimes versus providers/model/channel, embedded harnesses versus CLI backends, Codex surfaces, runtime decision tree, ownership split, runtime selection, fail-closed explicit runtimes, CLI backend aliases, Claude CLI, OpenAI default to Codex harness, and compatibility contract.
- `/Users/kevinlin/code/openclaw/docs/providers/anthropic.md` documents Claude CLI setup, same-host requirement, canonical Anthropic refs with `agentRuntime.id: "claude-cli"`, legacy refs, and thinking defaults.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md` documents Gemini CLI OAuth setup, plugin capabilities, legacy aliases, and capability expectations.
- `/Users/kevinlin/code/openclaw/docs/tools/subagents.md` documents subagent auth, announce behavior, delivery routing, sessions_history sanitation, subagent tool policy, concurrency, liveness, and recovery.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/cli-runner.ts` persists approved CLI user turn transcripts, finalizes CLI context engine turns, invokes `before_agent_reply`, and runs CLI agent turns.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.ts` resolves CLI runtime execution providers, handles runtime overrides, bridges CLI assistant events into previews, forwards runtime plan/approval/command/patch events, and enforces live switch retry caps.
- `/Users/kevinlin/code/openclaw/src/agents/agent-tools.ts` applies subagent/inherited tool policy and configures tool execution boundaries used by spawned runtime sessions.

### Integration tests

- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.subagents.sessions-spawn.lifecycle.test.ts` covers `sessions_spawn` lifecycle behavior, cleanup, enough gateway request time, MCP cleanup, delete via `agent.wait`, timeout handling, account routing, and announce behavior.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.test.ts` covers forwarding static extra prompts to CLI backends, prepared CLI user turns at the persistence boundary, no CLI session reuse for room-event turns, CLI assistant event previews, reasoning previews, CLI runtime override boundaries, and Codex app-server telemetry.

### Unit tests

- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.test.ts` includes focused tests for runtime override resolution, CLI preview bridging, external error formatting, gateway restart recovery copy, and live model switch retry caps.
- `/Users/kevinlin/code/openclaw/src/agents/agent-tools.message-provider-policy.test.ts` covers provider-policy behavior that affects external runtime tool surfaces.

### Gitcrawl queries

- `gitcrawl --json search issues -R openclaw/openclaw "claude-cli codex cli harness subagent sessions_spawn"` returned #73097 on PI harness ignoring `cliBackends` configuration and splitting subagent execution from chat path.
- `gitcrawl --json search issues -R openclaw/openclaw "openai-codex Anthropic Google provider tool call"` returned #80667 on `trajectory.jsonl` never being written for pure `claude-cli` sessions and #78196 on extension plugin loader behavior.
- `gitcrawl --json search issues -R openclaw/openclaw "local model provider context timeout Ollama"` returned #81214 on an OpenClaw subagent regression and #87642 on exposing subagent-control `waitForRun` timeout for slow local LLMs.

### Discrawl queries

- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "sessions_spawn claude-cli"` returned Apr-May 2026 discussions about ACP runtime failures with Claude Opus settings, Claude CLI tool availability, tool permission boundaries/sandboxing, ACP/sub-agent relay UX, and subagent/ACP result delivery regressions.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "tool call streaming"` returned Claude CLI/WebChat tool visibility concerns and app-server watchdog discussions that affect external runtime delivery.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "No API key found provider openai-codex"` returned related Codex OAuth profile propagation and rebuild-recognition reports that affect external runtime/subagent sessions.
