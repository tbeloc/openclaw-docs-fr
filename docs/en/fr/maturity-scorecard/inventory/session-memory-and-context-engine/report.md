---
title: "Rapport de maturité du moteur de session, mémoire et contexte"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité du moteur de session, mémoire et contexte

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont arrondis au nombre entier le plus proche.

- Couverture : `Beta (74%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (74%)`
- Fonctionnalités LTS : `6/9`

## Résumé

Ce rapport promeut les preuves de maturité archivées `session-memory-and-context-engine` de `/Users/kevinlin/tmp/maturity/session-memory-and-context-engine` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité de la catégorie proviennent des lignes de score soutenues par les preuves archivées. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                              | LTS | Couverture     | Qualité        | Complétude     | Fonctionnalités à évaluer                                                                            |
| ------------------------------------------------------------------------------------- | --- | -------------- | -------------- | -------------- | ---------------------------------------------------------------------------------------------------- |
| [Gestion des sessions CLI et des transcriptions](cli-session-and-transcript-management.md)     | ✅  | `Beta (74%)`   | `Alpha (68%)`  | `Beta (74%)`   | Session CLI, Gestion des transcriptions                                                              |
| [Gestion des jetons](compaction-pruning-and-token-pressure.md)                          | ✅  | `Beta (78%)`   | `Alpha (60%)`  | `Beta (78%)`   | Compaction, Élagage, Pression des jetons                                                             |
| [Moteur de contexte](context-engine-and-runtime-assembly.md)                              | ✅  | `Beta (72%)`   | `Stable (80%)` | `Beta (72%)`   | Moteur de contexte, Assemblage à l'exécution                                                         |
| [Parité d'historique et de session multi-clients](cross-client-history-and-session-parity.md) | ❌  | `Beta (76%)`   | `Alpha (62%)`  | `Beta (76%)`   | Historique multi-clients, Parité de session                                                          |
| [Diagnostics, maintenance et récupération](diagnostics-maintenance-and-recovery.md)     | ❌  | `Beta (72%)`   | `Alpha (68%)`  | `Beta (72%)`   | Rapports de diagnostic de session, Avertissements de maintenance de session, Récupération de session et de transcription |
| [Invites principales et contexte](instruction-profile-and-context-visibility.md)             | ✅  | `Alpha (68%)`  | `Beta (70%)`   | `Alpha (68%)`  | Profil d'instruction, Visibilité du contexte                                                         |
| [Mémoire](memory-files-tools-and-active-memory.md)                                     | ❌  | `Alpha (66%)`  | `Alpha (58%)`  | `Alpha (66%)`  | Stockage backend de mémoire, Recherche par intégration, Fichiers de mémoire, Outils de recherche et stockage de mémoire, Mémoire active |
| [Routage de session](session-routing-and-conversation-binding.md)                        | ✅  | `Stable (82%)` | `Beta (74%)`   | `Stable (82%)` | Routage de session, Routage de conversation                                                          |
| [Persistance des transcriptions](transcript-persistence-and-durability.md)                    | ✅  | `Beta (78%)`   | `Alpha (58%)`  | `Beta (78%)`   | Persistance des transcriptions, Durabilité                                                           |

## Rubrique de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/exécution
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux d'exécution réel sont des entrées de couverture
  uniquement ; ils ne relèvent ni n'abaissent la qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie livre l'ensemble complet de capacités
  spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme
  une dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Gestion des sessions CLI et des transcriptions

Ancres de recherche : CLI Session, Transcript Management, session, memory, and context engine cli session and transcript management, cli session and transcript management.

Note de catégorie : [CLI Session and Transcript Management](cli-session-and-transcript-management.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (74%)`
- LTS : ✅

Fonctionnalités :

- CLI Session : Couvre CLI Session dans `openclaw sessions`, `openclaw transcripts`, cleanup, show/list/path behavior, TUI session history actions, et Gateway-backed session management commands.
- Transcript Management : Couvre Transcript Management dans `openclaw sessions`, `openclaw transcripts`, cleanup, show/list/path behavior, TUI session history actions, et Gateway-backed session management commands.

Documentation principale :

- `docs/concepts/session.md`
- `docs/reference/session-management-compaction.md`
- `docs/cli/sessions.md`

### 2. Gestion des tokens

Ancres de recherche : Compaction, Pruning, Token Pressure, session, memory, and context engine compaction, pruning, and token pressure, compaction, pruning, and token pressure.

Note de catégorie : [Token Management](compaction-pruning-and-token-pressure.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Alpha (60%)`
- Complétude : `Beta (78%)`
- LTS : ✅

Fonctionnalités :

- Compaction : Couvre Compaction dans manual and automatic compaction, preemptive overflow checks, context-window estimation, session pruning, tool-result trimming, compaction providers, retry/timeout behavior, et compacted transcript checkpoints.
- Pruning : Couvre Pruning dans manual and automatic compaction, preemptive overflow checks, context-window estimation, session pruning, tool-result trimming, compaction providers, retry/timeout behavior, et compacted transcript checkpoints.
- Token Pressure : Couvre Token Pressure dans manual and automatic compaction, preemptive overflow checks, context-window estimation, session pruning, tool-result trimming, compaction providers, retry/timeout behavior, et compacted transcript checkpoints.

Documentation principale :

- `docs/concepts/compaction.md`
- `docs/concepts/context.md`
- `docs/reference/session-management-compaction.md`

### 3. Moteur de contexte

Ancres de recherche : Context Engine, Runtime Assembly, session, memory, and context engine context engine and runtime assembly, context engine and runtime assembly.

Note de catégorie : [Context Engine](context-engine-and-runtime-assembly.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Stable (80%)`
- Complétude : `Beta (72%)`
- LTS : ✅

Fonctionnalités :

- Context Engine : Couvre Context Engine dans context-engine selection, registry, host compatibility, legacy fallback, assemble/ingest/after-turn/compact lifecycle, runtime context projection, et the boundary between OpenClaw context assembly and native harness history.
- Runtime Assembly : Couvre Runtime Assembly dans context-engine selection, registry, host compatibility, legacy fallback, assemble/ingest/after-turn/compact lifecycle, runtime context projection, et the boundary between OpenClaw context assembly and native harness history.

Documentation principale :

- `docs/concepts/context.md`
- `docs/concepts/context-engine.md`
- `docs/plan/codex-context-engine-harness.md`

### 4. Historique multi-clients et parité des sessions

Ancres de recherche : Cross-client History, Session Parity, session, memory, and context engine cross-client history and session parity, cross-client history and session parity.

Note de catégorie : [Cross-client History and Session Parity](cross-client-history-and-session-parity.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Alpha (62%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Cross-client History : Couvre Cross-client History dans `chat.history`, `chat.send`, WebChat display projection, TUI session actions, Android chat/session selection, OpenAI-compatible history mapping, channel history windows, et history visibility across reset/restart.
- Session Parity : Couvre Session Parity dans `chat.history`, `chat.send`, WebChat display projection, TUI session actions, Android chat/session selection, OpenAI-compatible history mapping, channel history windows, et history visibility across reset/restart.

Documentation principale :

- `docs/web/webchat.md`
- `docs/platforms/android.md`
- `docs/channels/channel-routing.md`

### 5. Diagnostics, maintenance et récupération

Ancres de recherche : stuck-session diagnostics, restart recovery, orphaned subagent resume, diagnostic bundles, transcript repair, session maintenance warnings.

Note de catégorie : [Diagnostics, Maintenance, and Recovery](diagnostics-maintenance-and-recovery.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Session diagnostic reports : Couvre stuck-session diagnostics, diagnostic bundles, stability snapshots, et operator visibility into transcript and session health.
- Session maintenance warnings : Couvre restart maintenance warnings, delivery queues, memory/session cleanup signals, et operator-visible maintenance state.
- Session and transcript recovery : Couvre restart recovery, orphaned subagent resume, transcript repair, et safe restoration of session state after failures.

Documentation principale :

- `docs/gateway/diagnostics.md`
- `docs/reference/session-management-compaction.md`
- `docs/diagnostics/flags.md`

### 6. Invites principales et contexte

Ancres de recherche : Instruction Profile, Context Visibility, session, memory, and context engine instruction profile and context visibility, instruction profile and context visibility.

Note de catégorie : [Core Prompts and Context](instruction-profile-and-context-visibility.md)

Décisions de score :

- Couverture : `Alpha (68%)`
- Qualité : `Beta (70%)`
- Complétude : `Alpha (68%)`
- LTS : ✅

Fonctionnalités :

- Instruction Profile : Couvre Instruction Profile dans `AGENTS.md`, `USER.md`, `IDENTITY.md`, `SOUL.md`, project context injection, bootstrap truncation, untrusted supplemental context, context visibility config, et runtime-context leakage prevention.
- Context Visibility : Couvre Context Visibility dans `AGENTS.md`, `USER.md`, `IDENTITY.md`, `SOUL.md`, project context injection, bootstrap truncation, untrusted supplemental context, context visibility config, et runtime-context leakage prevention.

Documentation principale :

- `docs/concepts/context.md`
- `docs/reference/transcript-hygiene.md`
- `docs/channels/discord.md`

### 7. Mémoire

Ancres de recherche : Memory Backend Storage, Embedding Search, Memory Files, memory search, memory get, memory store, Active Memory, root memory files, active memory, memory backend storage and embedding search.

Note de catégorie : [Memory](memory-files-tools-and-active-memory.md)

Décisions de score :

- Couverture : `Alpha (66%)`
- Qualité : `Alpha (58%)`
- Complétude : `Alpha (66%)`
- LTS : ❌

Fonctionnalités :

- Memory Backend Storage : Couvre Memory Backend Storage dans memory backend config, SQLite schema, vector acceleration, embedding provider selection, remote embedding fetch, QMD process/query parsing, session transcript indexing for search, extra paths, et backend security boundaries.
- Embedding Search : Couvre Embedding Search dans memory backend config, SQLite schema, vector acceleration, embedding provider selection, remote embedding fetch, QMD process/query parsing, session transcript indexing for search, extra paths, et backend security boundaries.
- Memory Files : Couvre Memory Files dans root memory files, active memory, memory search/get/store tool exposure, memory prompt sections, memory flush plans, session-memory hook behavior, et memory plugin capability registration visible to agents.
- Memory search and store tools : Couvre memory search/get/store tool exposure, memory prompt sections, memory flush plans, session-memory hook behavior, et memory plugin capability registration visible to agents.
- Active Memory : Couvre Active Memory dans root memory files, active memory, memory search/get/store tool exposure, memory prompt sections, memory flush plans, session-memory hook behavior, et memory plugin capability registration visible to agents.

Documentation principale :

- `docs/reference/memory-config.md`
- `docs/concepts/memory-qmd.md`
- `docs/concepts/memory.md`
- `docs/channels/discord.md`

### 8. Routage des sessions

Ancres de recherche : Session Routing, Conversation Binding, session, memory, and context engine session routing and conversation binding, session routing and conversation binding.

Note de catégorie : [Session Routing](session-routing-and-conversation-binding.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (74%)`
- Complétude : `Stable (82%)`
- LTS : ✅

Fonctionnalités :

- Session Routing : Couvre Session Routing dans `sessionKey` construction, target resolution, conversation bindings, session labels, per-conversation isolation, thread binding, model selection continuity tied to sessions, et agent/workspace store targeting.
- Conversation routing : Couvre Conversation Binding dans `sessionKey` construction, target resolution, conversation bindings, session labels, per-conversation isolation, thread binding, model selection continuity tied to sessions, et agent/workspace store targeting.

Documentation principale :

- `docs/concepts/session.md`
- `docs/channels/channel-routing.md`
- `docs/channels/discord.md`

### 9. Persistance des transcriptions

Ancres de recherche : Transcript Persistence, Durability, session, memory, and context engine transcript persistence and durability, transcript persistence and durability.

Note de catégorie : [Transcript Persistence](transcript-persistence-and-durability.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Alpha (58%)`
- Complétude : `Beta (78%)`
- LTS : ✅

Fonctionnalités :

- Transcript Persistence : Couvre Transcript Persistence dans JSONL session files, transcript append and redaction, session write locks, transcript rotation/archive behavior, disk budget cleanup, provider transcript stores, et restart/repair durability.
- Durability : Couvre Durability dans JSONL session files, transcript append and redaction, session write locks, transcript rotation/archive behavior, disk budget cleanup, provider transcript stores, et restart/repair durability.

Documentation principale :

- `docs/reference/session-management-compaction.md`
- `docs/reference/transcript-hygiene.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base de référence d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche catégorie-agent en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinir les limites de la catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de la catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/session-memory-and-context-engine/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/session-memory-and-context-engine`.
