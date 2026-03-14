---
read_when:
  - Vous souhaitez exécuter un tour d'agent à partir d'un script (avec envoi optionnel de réponse)
summary: "Référence CLI pour `openclaw agent` (envoyer un tour d'agent via la passerelle Gateway)"
title: agent
x-i18n:
  generated_at: "2026-02-03T07:44:38Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: dcf12fb94e207c68645f58235792596d65afecf8216b8f9ab3acb01e03b50a33
  source_path: cli/agent.md
  workflow: 15
---

# `openclaw agent`

Exécuter un tour d'agent via la passerelle Gateway (utiliser `--local` pour une exécution intégrée). Utilisez `--agent <id>` pour spécifier directement un agent configuré.

Contenu connexe :

- Outil d'envoi d'agent : [Agent send](/tools/agent-send)

## Exemples

```bash
openclaw agent --to +15555550123 --message "status update" --deliver
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
```
