---
read_when:
  - 渠道已连接但消息无法流通
  - 排查渠道配置错误（意图、权限、隐私模式）
summary: 渠道专属故障排除快捷指南（Discord/Telegram/WhatsApp）
title: 渠道故障排除
x-i18n:
  generated_at: "2026-02-01T19:58:09Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 6542ee86b3e50929caeaab127642d135dfbc0d8a44876ec2df0fff15bf57cd63
  source_path: channels/troubleshooting.md
  workflow: 14
---

# Dépannage des canaux

Commencez par exécuter :

```bash
openclaw doctor
openclaw channels status --probe
```

`channels status --probe` affiche des avertissements lors de la détection d'erreurs de configuration courantes des canaux et inclut des vérifications en temps réel minimes (identifiants, autorisations partielles/adhésion).

## Canaux

- Discord : [/channels/discord#troubleshooting](/channels/discord#troubleshooting)
- Telegram : [/channels/telegram#troubleshooting](/channels/telegram#troubleshooting)
- WhatsApp : [/channels/whatsapp#troubleshooting-quick](/channels/whatsapp#troubleshooting-quick)

## Correctif rapide Telegram

- Les journaux affichent `HttpError: Network request for 'sendMessage' failed` ou `sendChatAction` → Vérifiez le DNS IPv6. Si `api.telegram.org` se résout en priorité vers IPv6 et que l'hôte n'a pas de connectivité sortante IPv6, forcez IPv4 ou activez IPv6. Voir [/channels/telegram#troubleshooting](/channels/telegram#troubleshooting).
- Les journaux affichent `setMyCommands failed` → Vérifiez la disponibilité HTTPS sortante et DNS vers `api.telegram.org` (courant dans les environnements VPS ou proxy strictement restreints).
