---
summary: "Plateformes de messagerie auxquelles OpenClaw peut se connecter"
read_when:
  - Vous souhaitez choisir un canal de chat pour OpenClaw
  - Vous avez besoin d'un aperçu rapide des plateformes de messagerie prises en charge
title: "Canaux de Chat"
---

# Canaux de Chat

OpenClaw peut vous parler sur n'importe quelle application de chat que vous utilisez déjà. Chaque canal se connecte via la Gateway.
Le texte est pris en charge partout ; les médias et les réactions varient selon le canal.

## Canaux pris en charge

- [BlueBubbles](/fr/channels/bluebubbles) — **Recommandé pour iMessage** ; utilise l'API REST du serveur macOS BlueBubbles avec support complet des fonctionnalités (édition, annulation d'envoi, effets, réactions, gestion de groupe — édition actuellement cassée sur macOS 26 Tahoe).
- [Discord](/fr/channels/discord) — API Discord Bot + Gateway ; prend en charge les serveurs, les canaux et les DM.
- [Feishu](/fr/channels/feishu) — Bot Feishu/Lark via WebSocket (plugin, installé séparément).
- [Google Chat](/fr/channels/googlechat) — Application API Google Chat via webhook HTTP.
- [iMessage (hérité)](/fr/channels/imessage) — Intégration macOS hérité via CLI imsg (déprécié, utilisez BlueBubbles pour les nouvelles installations).
- [IRC](/fr/channels/irc) — Serveurs IRC classiques ; canaux + DM avec contrôles d'appairage/liste blanche.
- [LINE](/fr/channels/line) — Bot API LINE Messaging (plugin, installé séparément).
- [Matrix](/fr/channels/matrix) — Protocole Matrix (plugin, installé séparément).
- [Mattermost](/fr/channels/mattermost) — API Bot + WebSocket ; canaux, groupes, DM (plugin, installé séparément).
- [Microsoft Teams](/fr/channels/msteams) — Bot Framework ; support entreprise (plugin, installé séparément).
- [Nextcloud Talk](/fr/channels/nextcloud-talk) — Chat auto-hébergé via Nextcloud Talk (plugin, installé séparément).
- [Nostr](/fr/channels/nostr) — DM décentralisés via NIP-04 (plugin, installé séparément).
- [Signal](/fr/channels/signal) — signal-cli ; axé sur la confidentialité.
- [Synology Chat](/fr/channels/synology-chat) — Synology NAS Chat via webhooks sortants+entrants (plugin, installé séparément).
- [Slack](/fr/channels/slack) — Bolt SDK ; applications d'espace de travail.
- [Telegram](/fr/channels/telegram) — API Bot via grammY ; prend en charge les groupes.
- [Tlon](/fr/channels/tlon) — Messager basé sur Urbit (plugin, installé séparément).
- [Twitch](/fr/channels/twitch) — Chat Twitch via connexion IRC (plugin, installé séparément).
- [WebChat](/fr/web/webchat) — Interface WebChat Gateway sur WebSocket.
- [WhatsApp](/fr/channels/whatsapp) — Le plus populaire ; utilise Baileys et nécessite un appairage QR.
- [Zalo](/fr/channels/zalo) — API Zalo Bot ; messager populaire au Vietnam (plugin, installé séparément).
- [Zalo Personnel](/fr/channels/zalouser) — Compte personnel Zalo via connexion QR (plugin, installé séparément).

## Notes

- Les canaux peuvent fonctionner simultanément ; configurez plusieurs et OpenClaw acheminera par chat.
- La configuration la plus rapide est généralement **Telegram** (simple jeton bot). WhatsApp nécessite un appairage QR et
  stocke plus d'état sur le disque.
- Le comportement des groupes varie selon le canal ; voir [Groupes](/fr/channels/groups).
- L'appairage DM et les listes blanches sont appliqués pour la sécurité ; voir [Sécurité](/fr/gateway/security).
- Dépannage : [Dépannage des canaux](/fr/channels/troubleshooting).
- Les fournisseurs de modèles sont documentés séparément ; voir [Fournisseurs de Modèles](/fr/providers/models).
