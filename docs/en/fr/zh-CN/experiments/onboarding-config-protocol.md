# Onboarding + Configuration Protocol

Purpose: Shared onboarding + configuration interface between CLI, macOS app, and Web UI.

## Components

- Wizard engine (shared session + prompts + onboarding state).
- CLI onboarding uses the same wizard flow as UI clients.
- Gateway RPC exposes wizard + configuration schema endpoints.
- macOS onboarding uses wizard step models.
- Web UI renders configuration forms from JSON Schema + UI hints.

## Gateway RPC

- `wizard.start` parameters: `{ mode?: "local"|"remote", workspace?: string }`
- `wizard.next` parameters: `{ sessionId, answer?: { stepId, value? } }`
- `wizard.cancel` parameters: `{ sessionId }`
- `wizard.status` parameters: `{ sessionId }`
- `config.schema` parameters: `{}`

Response (structure)

- Wizard: `{ sessionId, done, step?, status?, error? }`
- Configuration schema: `{ schema, uiHints, version, generatedAt }`

## UI Hints

- `uiHints` keyed by path; optional metadata (label/help/group/order/advanced/sensitive/placeholder).
- Sensitive fields render as password inputs; no redaction layer.
- Unsupported schema nodes fall back to raw JSON editor.

## Notes

- This document is the single source of truth for tracking onboarding/configuration protocol refactoring.
