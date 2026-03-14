---
read_when:
  - When changing autoreply execution or concurrency settings
summary: Command queue design for serializing inbound autoreply runs
title: Command Queue
x-i18n:
  generated_at: "2026-02-03T10:05:28Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 2104c24d200fb4f9620e52a19255cd614ababe19d78f3ee42936dc6d0499b73b
  source_path: concepts/queue.md
  workflow: 15
---

# Command Queue (2026-01-16)

We serialize inbound autoreply runs (across all channels) through a small in-process queue to prevent conflicts when multiple agent runs occur, while still allowing safe parallelism across sessions.

## Why It Matters

- Autoreply runs can be expensive (LLM calls) and may conflict when multiple inbound messages arrive nearly simultaneously.
- Serialization avoids contention on shared resources (session files, logs, CLI stdin) and reduces the likelihood of upstream rate limiting.

## How It Works

- A channel-aware FIFO queue drains each channel with a configurable concurrency limit (unconfigured channels default to 1; `main` defaults to 4, `subagent` to 8).
- `runEmbeddedPiAgent` enqueues by **session key** (channel `session:<key>`) to guarantee only one active run per session.
- Each session run is then enqueued to the **global channel** (default `main`), so overall parallelism is bounded by `agents.defaults.maxConcurrent`.
- When verbose logging is enabled, a brief notification is issued if a queued run waits more than ~2 seconds before starting.
- Input indicators still fire immediately upon enqueue (when the channel supports it), so user experience is unaffected while waiting for a turn.

## Queue Modes (by Channel)

Inbound messages can steer the current run, wait for a follow-up turn, or both:

- `steer`: Inject immediately into the current run (cancel pending tool calls after the next tool boundary). Falls back to followup if not streaming.
- `followup`: Enqueue for the next agent turn after the current run ends.
- `collect`: Merge all queued messages into a **single** follow-up turn (default). If messages target different channels/threads, they drain separately to preserve routing.
- `steer-backlog` (aka `steer+backlog`): Steer **now** and also retain the message for a follow-up turn.
- `interrupt` (legacy): Abort the active run for that session, then run the latest message.
- `queue` (legacy alias): Same as `steer`.

steer-backlog means you can get a follow-up response after the steered run, so a streaming interface might look like a duplicate. If you want only one response per inbound message, prefer `collect`/`steer`.
Send `/queue collect` as a standalone command (per session) or set `messages.queue.byChannel.discord: "collect"`.

Defaults (when not set in config):

- All interfaces → `collect`

Configure globally or per-channel via `messages.queue`:

```json5
{
  messages: {
    queue: {
      mode: "collect",
      debounceMs: 1000,
      cap: 20,
      drop: "summarize",
      byChannel: { discord: "collect" },
    },
  },
}
```

## Queue Options

Options apply to `followup`, `collect`, and `steer-backlog` (and when `steer` falls back to followup):

- `debounceMs`: Wait for silence before starting the follow-up turn (prevents "go on, go on").
- `cap`: Maximum queued messages per session.
- `drop`: Overflow policy (`old`, `new`, `summarize`).

summarize keeps a short bullet list of dropped messages and injects it as a synthetic follow-up prompt.
Defaults: `debounceMs: 1000`, `cap: 20`, `drop: summarize`.

## Per-Session Overrides

- Send `/queue <mode>` as a standalone command to store that mode for the current session.
- Options can be combined: `/queue collect debounce:2s cap:25 drop:summarize`
- `/queue default` or `/queue reset` clears the session override.

## Scope and Guarantees

- Applies to autoreply agent runs on all inbound channels using the Gateway reply pipeline (WhatsApp Web, Telegram, Slack, Discord, Signal, iMessage, web chat, etc.).
- The default channel (`main`) is process-scoped for inbound + main heartbeat; set `agents.defaults.maxConcurrent` to allow multiple sessions to run in parallel.
- Additional channels may exist (e.g., `cron`, `subagent`) so background tasks can run in parallel without blocking inbound replies.
- Per-session channels guarantee only one agent run touches a given session at a time.
- No external dependencies or background worker threads; pure TypeScript + promises.

## Troubleshooting

- If a command seems stuck, enable verbose logging and look for "queued for …ms" lines to confirm the queue is draining.
- If you need to see queue depth, enable verbose logging and observe the queue timing lines.
