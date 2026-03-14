---
read_when:
  - 你想快速诊断渠道健康状况 + 最近的会话接收者
  - 你想获取可粘贴的"all"状态用于调试
summary: "`openclaw status` 的 CLI 参考（诊断、探测、使用量快照）"
title: status
x-i18n:
  generated_at: "2026-02-03T07:45:21Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 2bbf5579c48034fc15c2cbd5506c50456230b17e4a74c06318968c590d8f1501
  source_path: cli/status.md
  workflow: 15
---

# `openclaw status`

Diagnostics des canaux + sessions.

```bash
openclaw status
openclaw status --all
openclaw status --deep
openclaw status --usage
```

Remarques :

- `--deep` exécute des sondes en temps réel (WhatsApp Web + Telegram + Discord + Google Chat + Slack + Signal).
- Lorsque plusieurs agents sont configurés, la sortie contient le stockage des sessions pour chaque agent.
- L'aperçu contient l'état d'installation/exécution de la passerelle Gateway + du service hôte de nœud (si disponible).
- L'aperçu contient le canal de mise à jour + git SHA (pour les extraits de code source).
- Les informations de mise à jour s'affichent dans l'aperçu ; s'il y a une mise à jour disponible, status affichera une invite pour exécuter `openclaw update` (voir [Mise à jour](/install/updating)).
