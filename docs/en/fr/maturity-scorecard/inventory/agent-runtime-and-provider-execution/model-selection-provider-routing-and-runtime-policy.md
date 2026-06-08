---
title: "Agent Runtime - Model and Runtime Selection Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Agent Runtime - Model and Runtime Selection Maturity Note

## Summary

La sélection de modèle et le routage des fournisseurs sont parmi les parties les plus matures de cette surface. La documentation explique les références de modèle, les valeurs par défaut configurées, les références strictes sélectionnées par l'utilisateur, les secours des fournisseurs, les secours des profils d'authentification, `/model`, les remplacements d'exécution et la politique de réflexion/contexte. La source centralise la plupart de l'état dans `createModelSelectionState`, et les tests couvrent le comportement de liste/ensemble de modèles ainsi que le routage de secours/nouvelle tentative. La qualité est Beta en raison des preuves d'archive montrant une dérive récente autour des routes OAuth Codex, des références `openai-codex` obsolètes et de l'état de secours par session/fournisseur.

## Category Scope

Cette catégorie couvre la sélection d'un modèle/fournisseur/exécution pour un tour d'agent, en respectant les choix de l'utilisateur et de la configuration, en résolvant les paramètres de réflexion/contexte, en gérant les remplacements de fournisseur d'exécution et en préservant ou en effaçant l'état de route invalide.

## Features

- Model reference selection: Sélection de la référence de modèle pour un tour d'agent à partir des valeurs par défaut de l'utilisateur ou configurées.
- Provider and runtime overrides: Gestion de la sélection du fournisseur et des remplacements d'exécution pour un tour.
- Thinking and context settings: Résolution des paramètres de réflexion et de contexte dans le cadre de la sélection de modèle.
- Invalid route recovery: Préservation ou effacement de l'état de route invalide lorsque les sélections dérivent ou échouent.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Stable (84%)`

La couverture est solide dans la documentation des modèles, la documentation des commandes CLI, la documentation des fournisseurs, la source et les tests e2e pour la normalisation de la liste/ensemble de modèles et des secours.

## Quality Score

- Score: `Beta (72%)`

Le comportement de routage est explicite et défensif, mais la qualité est réduite par la réparation de route visible par l'opérateur récente, les références d'authentification/fournisseur obsolètes et les rapports de collage de secours.

## Completeness Score

- Score: `Stable (84%)`
- Surface instructions: evaluated against `references/completeness/agent-runtime-and-provider-execution.md`.
- Positive signals: archived docs, source, test, Gitcrawl, and Discrawl evidence cover the taxonomy scope for Model reference selection, Provider and runtime overrides, Thinking and context settings, Invalid route recovery.
- Negative signals: the archived note predated process-version-3 Completeness scoring, so this score is initialized from the same evidence breadth and known-gap record used for the archived Coverage score.
- Missing capability branches: see `## Known Gaps` and `## Evidence` below for the recorded missing branches and operator-visible caveats.

## Known Gaps

- La récupération d'opérateur pour les références de fournisseur/exécution obsolètes est répartie entre le comportement du docteur, la documentation du fournisseur et la copie d'erreur.
- La politique d'exécution est solide pour les fournisseurs courants, mais les rapports de terrain montrent une dérive de route lorsque OAuth Codex, les ID de fournisseur personnalisés et les profils de secours interagissent.
- Le système a besoin d'une preuve de scénario récurrente au niveau de la version pour le comportement de réparation de route et de réinitialisation de secours.

## Evidence

### Docs

- `/Users/kevinlin/code/openclaw/docs/concepts/models.md` documents model refs versus runtime, selection order, provider/auth fallbacks, configured defaults, auto fallback selections, strict user session selections, model allowlists, local/GGUF refs, `/model` switching, live switching, and strict selected refs.
- `/Users/kevinlin/code/openclaw/docs/cli/models.md` documents `models list`, `models set`, status/probe options, catalog/auth columns, provider catalog responsiveness, ref parsing/fallback, auth profiles, login, paste-api-key, and OpenAI API versus ChatGPT/OAuth routing.
- `/Users/kevinlin/code/openclaw/docs/providers/openai.md` documents OpenAI/Codex route distinctions, naming map, GPT-5.5/Codex app-server repair notes, capability tables, and the default OpenAI agent route summary.
- `/Users/kevinlin/code/openclaw/docs/concepts/agent-runtimes.md` documents runtime selection, fail-closed explicit runtimes, CLI backend aliases, and OpenAI defaulting to the Codex harness.

### Source

- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/model-selection.ts` implements provider/model initialization, allowlists, catalog visibility policy, direct stored override handling, stale legacy `openai-codex` override clearing, auth profile override validation, thinking/reasoning resolution, and context token resolution.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.ts` applies fallback candidate auth profiles, live model switches, runtime config, runtime provider resolution, and retry state.
- `/Users/kevinlin/code/openclaw/src/agents/configured-provider-fallback.ts` defines configured fallback behavior for provider selection.

### Integration tests

- `/Users/kevinlin/code/openclaw/src/commands/models.set.e2e.test.ts` covers model setting and fallback normalization.
- `/Users/kevinlin/code/openclaw/src/commands/models.list.e2e.test.ts` covers model list/status, catalog/auth/local/provider behavior, and provider visibility.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.test.ts` covers fallback rechecks, stale queued probe dropping after user model switches, preserving and re-persisting fallback origins, CLI runtime override boundaries, model capacity errors, live model switch restarts, and retry-loop caps.

### Unit tests

- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/agent-runner-execution.test.ts` includes focused tests for provider/model fallback retry state, auth profile preservation, dropping `authProfileId` when fallback switches providers, and same-provider auth profile fallback.
- `/Users/kevinlin/code/openclaw/src/commands/models.auth.provider-resolution.test.ts` covers auth-provider resolution behavior for model commands.

### Gitcrawl queries

- `gitcrawl --json search issues -R openclaw/openclaw "models list model selection fallback auth profile provider"` returned #59168 on using `provider/name` as the internal model key, #83954 on Pro-plan paths for `gpt-5.5-pro` and retired Spark via Codex CLI/app-server, and #70055 on disabling external CLI sync for auth profiles via config.
- `gitcrawl --json search issues -R openclaw/openclaw "No API key found provider openai-codex auth profile"` returned stale route and Codex OAuth issues including #86470 on doctor rewriting `openai-codex/*` to `openai/*`, #83223 on migrated routes still looking up `openai-codex` auth before fallback, and #86820 on compaction falling back to direct OpenAI API.
- `gitcrawl --json search issues -R openclaw/openclaw "rate limit fallback usage limit openai-codex"` returned #85103 on provider-wide quota fallback not triggering, #87467 on auto rate-limit fallback staying pinned after primary recovery, #79604 on rotating auth profiles before provider fallback, and #79611 on active-memory plugin failover.

### Discrawl queries

- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "models list provider routing fallback"` returned a May 16 beta announcement emphasizing Codex app-server reliability, progress timeouts, compaction handling, tool policy enforcement, OAuth fallback, local/custom providers, and guidance on Ollama provider pressure, vision routing, CLI crashes, and per-turn model routing with `before_model_resolve`.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "openai-codex provider routing"` returned maintainer notes around OpenAI OAuth/Codex routing, `openai-codex` being load-bearing in auth profile resolution, compaction routing, context config, auth order, and stale persisted route state.
- `/Users/kevinlin/.local/bin/discrawl search --limit 10 "model fallback decision"` returned recent discussions about openai-codex timeouts, fallback decisions, No API key fallback decisions, OpenRouter timeouts, and session repair loops.
