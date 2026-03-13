---
read_when:
  - 你想为 OpenClaw 选择一个聊天渠道
  - 你需要快速了解支持的消息平台
summary: OpenClaw 可连接的消息平台
title: 聊天渠道
x-i18n:
  generated_at: "2026-02-03T07:43:27Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 2632863def6dee97e0fa8b931762f0969174fd4fb22303a00dcd46527fe4a141
  source_path: channels/index.md
  workflow: 15
---

# Canaux de chat

OpenClaw peut communiquer avec vous sur n'importe quelle application de chat que vous utilisez déjà. Chaque canal se connecte via une passerelle Gateway.
Tous les canaux supportent le texte ; le support des médias et des réactions emoji varie selon le canal.

## Canaux supportés

- [BlueBubbles](/channels/bluebubbles) — **Recommandé pour iMessage** ; utilise l'API REST du serveur macOS BlueBubbles, fonctionnalités complètes (édition, suppression, effets, réactions, gestion de groupe — l'édition n'est actuellement pas disponible sur macOS 26 Tahoe).
- [Discord](/channels/discord) — API Discord Bot + Gateway ; support des serveurs, canaux et messages directs.
- [飞书](/channels/feishu) — Bot 飞书 (Lark) (plugin, installation séparée requise).
- [Google Chat](/channels/googlechat) — Application API Google Chat via webhook HTTP.
- [iMessage (hérité)](/channels/imessage) — Intégration macOS hérité via imsg CLI (déprécié, utilisez BlueBubbles pour les nouvelles configurations).
- [LINE](/channels/line) — Bot API LINE Messaging (plugin, installation séparée requise).
- [Matrix](/channels/matrix) — Protocole Matrix (plugin, installation séparée requise).
- [Mattermost](/channels/mattermost) — API Bot + WebSocket ; canaux, groupes, messages directs (plugin, installation séparée requise).
- [Microsoft Teams](/channels/msteams) — Bot Framework ; support entreprise (plugin, installation séparée requise).
- [Nextcloud Talk](/channels/nextcloud-talk) — Chat auto-hébergé via Nextcloud Talk (plugin, installation séparée requise).
- [Nostr](/channels/nostr) — Messages privés décentralisés via NIP-04 (plugin, installation séparée requise).
- [Signal](/channels/signal) — signal-cli ; axé sur la confidentialité.
- [Slack](/channels/slack) — Bolt SDK ; application d'espace de travail.
- [Telegram](/channels/telegram) — API Bot via grammY ; support des groupes.
- [Tlon](/channels/tlon) — Application de messagerie basée sur Urbit (plugin, installation séparée requise).
- [Twitch](/channels/twitch) — Chat Twitch connecté via IRC (plugin, installation séparée requise).
- [WebChat](/web/webchat) — Interface WebChat Gateway basée sur WebSocket.
- [WhatsApp](/channels/whatsapp) — Le plus populaire ; utilise Baileys, appairage par code QR requis.
- [Zalo](/channels/zalo) — API Bot Zalo ; application de messagerie populaire au Vietnam (plugin, installation séparée requise).
- [Zalo Personnel](/channels/zalouser) — Compte personnel Zalo avec connexion par code QR (plugin, installation séparée requise).

## Remarques

- Les canaux peuvent s'exécuter simultanément ; après configuration de plusieurs canaux, OpenClaw achemine par conversation.
- La configuration la plus rapide est généralement **Telegram** (simple jeton bot). WhatsApp nécessite un appairage par code QR et
  stocke plus d'état sur le disque.
- Le comportement des groupes varie selon le canal ; voir [Groupes](/channels/groups).
- Pour la sécurité, l'appairage des messages directs et les listes d'autorisation sont appliqués ; voir [Sécurité](/gateway/security).
- Mécanisme interne Telegram : [Documentation grammY](/channels/grammy).
- Dépannage : [Dépannage des canaux](/channels/troubleshooting).
- Les fournisseurs de modèles sont documentés séparément ; voir [Fournisseurs de modèles](/providers/models).
