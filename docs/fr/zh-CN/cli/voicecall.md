---
read_when:
  - 使用语音通话插件并想了解 CLI 入口
  - 想要 `voicecall call|continue|status|tail|expose` 的快速示例
summary: 语音通话插件命令的 `openclaw voicecall` CLI 参考
title: voicecall
x-i18n:
  generated_at: "2026-02-01T20:21:37Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: d93aaee6f6f5c9ac468d8d2905cb23f0f2db75809408cb305c055505be9936f2
  source_path: cli/voicecall.md
  workflow: 14
---

# `openclaw voicecall`

`voicecall` est une commande fournie par un plugin. Elle n'apparaît que si le plugin d'appel vocal est installé et activé.

Documentation principale :

- Plugin d'appel vocal : [Appel vocal](/plugins/voice-call)

## Commandes courantes

```bash
openclaw voicecall status --call-id <id>
openclaw voicecall call --to "+15555550123" --message "Hello" --mode notify
openclaw voicecall continue --call-id <id> --message "Any questions?"
openclaw voicecall end --call-id <id>
```

## Exposer un Webhook (Tailscale)

```bash
openclaw voicecall expose --mode serve
openclaw voicecall expose --mode funnel
openclaw voicecall unexpose
```

Conseil de sécurité : n'exposez le point de terminaison webhook que sur les réseaux de confiance. Privilégiez Tailscale Serve plutôt que Funnel autant que possible.
