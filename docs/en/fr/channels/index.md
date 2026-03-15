---
summary: "Plateformes de messagerie auxquelles OpenClaw peut se connecter"
read_when:
  - You want to choose a chat channel for OpenClaw
  - You need a quick overview of supported messaging platforms
title: "Canaux de Chat"
---

# Canaux de Chat

OpenClaw peut vous parler sur n'importe quelle application de chat que vous utilisez déjà. Chaque canal se connecte via la Gateway.
Le texte est supporté partout ; les médias et les réactions varient selon le canal.

## Canaux supportés

- [BlueBubbles](/channels/bluebubbles) — **Recommandé pour iMessage** ; utilise l'API REST du serveur macOS BlueBubbles avec support complet des fonctionnalités (édition, annulation d'envoi, effets, réactions, gestion de groupe — édition actuellement cassée sur macOS 26 Tahoe).
- [Discord](/channels/discord) — API Discord Bot + Gateway ; supporte les serveurs, les canaux et les DMs.
- [Feishu](/channels/feishu) — Bot Feishu/Lark via WebSocket (plugin, installé séparément).
- [Google Chat](/channels/googlechat) — Application API Google Chat via webhook HTTP.
- [iMessage (legacy)](/channels/imessage) — Intégration macOS legacy via CLI imsg (dépréciée, utilisez BlueBubbles pour les nouvelles installations).
- [IRC](/channels/irc) — Serveurs IRC classiques ; canaux + DMs avec contrôles d'appairage/liste blanche.
- [LINE](/channels/line) — Bot LINE Messaging API (plugin, installé séparément).
- [Matrix](/channels/matrix) — Protocole Matrix (plugin, installé séparément).
- [Mattermost](/channels/mattermost) — API Bot + WebSocket ; canaux, groupes, DMs (plugin, installé séparément).
- [Microsoft Teams](/channels/msteams) — Bot Framework ; support entreprise (plugin, installé séparément).
- [Nextcloud Talk](/channels/nextcloud-talk) — Chat auto-hébergé via Nextcloud Talk (plugin, installé séparément).
- [Nostr](/channels/nostr) — DMs décentralisés via NIP-04 (plugin, installé séparément).
- [Signal](/channels/signal) — signal-cli ; axé sur la confidentialité.
- [Synology Chat](/channels/synology-chat) — Synology NAS Chat via webhooks sortants+entrants (plugin, installé séparément).
- [Slack](/channels/slack) — Bolt SDK ; applications d'espace de travail.
- [Telegram](/channels/telegram) — API Bot via grammY ; supporte les groupes.
- [Tlon](/channels/tlon) — Messager basé sur Urbit (plugin, installé séparément).
- [Twitch](/channels/twitch) — Chat Twitch via connexion IRC (plugin, installé séparément).
- [WebChat](/web/webchat) — Interface WebChat Gateway sur WebSocket.
- [WhatsApp](/channels/whatsapp) — Le plus populaire ; utilise Baileys et nécessite un appairage QR.
- [Zalo](/channels/zalo) — API Zalo Bot ; messager populaire au Vietnam (plugin, installé séparément).
- [Zalo Personal](/channels/zalouser) — Compte personnel Zalo via connexion QR (plugin, installé séparément).

## Notes

- Les canaux peuvent fonctionner simultanément ; configurez plusieurs et OpenClaw acheminera par chat.
- La configuration la plus rapide est généralement **Telegram** (simple jeton bot). WhatsApp nécessite un appairage QR et
  stocke plus d'état sur le disque.
- Le comportement des groupes varie selon le canal ; voir [Groupes](/channels/groups).
- L'appairage DM et les listes blanches sont appliqués pour la sécurité ; voir [Sécurité](/gateway/security).
- Dépannage : [Dépannage des canaux](/channels/troubleshooting).
- Les fournisseurs de modèles sont documentés séparément ; voir [Fournisseurs de Modèles](/providers/models).
