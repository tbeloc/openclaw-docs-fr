---
read_when:
  - Travailler avec les réactions emoji dans n'importe quel canal
summary: Sémantique des réactions emoji partagées entre canaux
title: Réactions emoji
x-i18n:
  generated_at: "2026-02-01T21:42:41Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 0f11bff9adb4bd02604f96ebe2573a623702796732b6e17dfeda399cb7be0fa6
  source_path: tools/reactions.md
  workflow: 15
---

# Outil Réactions emoji

Sémantique des réactions emoji partagées entre canaux :

- Lors de l'ajout d'une réaction emoji, `emoji` est obligatoire.
- `emoji=""` supprime la réaction emoji du bot sur le message, le cas échéant.
- `remove: true` supprime l'emoji spécifié, le cas échéant (nécessite de fournir `emoji`).

Spécifications par canal :

- **Discord/Slack** : Un `emoji` vide supprime toutes les réactions emoji du bot sur le message ; `remove: true` supprime uniquement l'emoji spécifié.
- **Google Chat** : Un `emoji` vide supprime la réaction emoji de l'application sur le message ; `remove: true` supprime uniquement l'emoji spécifié.
- **Telegram** : Un `emoji` vide supprime la réaction emoji du bot ; `remove: true` supprime également la réaction emoji, mais la validation de l'outil exige toujours que `emoji` soit non vide.
- **WhatsApp** : Un `emoji` vide supprime la réaction emoji du bot ; `remove: true` est mappé à un emoji vide (nécessite toujours de fournir `emoji`).
- **Signal** : Lorsque `channels.signal.reactionNotifications` est activé, les notifications de réactions emoji reçues déclenchent des événements système.
