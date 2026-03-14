---
read_when:
  - Vous souhaitez connaître la liste complète des fonctionnalités supportées par OpenClaw
summary: Fonctionnalités d'OpenClaw en matière de canaux, routage, médias et expérience utilisateur.
title: Fonctionnalités
x-i18n:
  generated_at: "2026-02-04T17:53:22Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 1b6aee0bfda751824cb6b3a99080b4c80c00ffb355a96f9cff1b596d55d15ed4
  source_path: concepts/features.md
  workflow: 15
---

## Points forts

<Columns>
  <Card title="Canaux" icon="message-square">
    Support de WhatsApp, Telegram, Discord et iMessage via une seule passerelle Gateway.
  </Card>
  <Card title="Plugins" icon="plug">
    Ajoutez d'autres plateformes comme Mattermost via des extensions.
  </Card>
  <Card title="Routage" icon="route">
    Routage multi-agents avec support des sessions isolées.
  </Card>
  <Card title="Médias" icon="image">
    Support de l'envoi et de la réception d'images, d'audio et de documents.
  </Card>
  <Card title="Applications et interfaces" icon="monitor">
    Interface de contrôle Web et application compagnon macOS.
  </Card>
  <Card title="Nœuds mobiles" icon="smartphone">
    Nœuds iOS et Android avec support Canvas.
  </Card>
</Columns>

## Liste complète

- Intégration WhatsApp via WhatsApp Web (Baileys)
- Support des bots Telegram (grammY)
- Support des bots Discord (channels.discord.js)
- Support des bots Mattermost (plugin)
- Intégration iMessage via CLI imsg local (macOS)
- Pont d'agents Pi avec support du mode RPC et streaming des outils
- Streaming et traitement par chunks des réponses longues
- Routage multi-agents avec sessions isolées par espace de travail ou expéditeur
- Authentification par abonnement Anthropic et OpenAI via OAuth
- Sessions : les messages privés fusionnés en `main` partagé ; les groupes isolés les uns des autres
- Support des chats de groupe, activés par mention
- Support des médias pour les images, l'audio et les documents
- Hook optionnel de transcription des messages vocaux
- Applications WebChat et barre de menus macOS
- Nœud iOS avec support de l'appairage et de l'interface Canvas
- Nœud Android avec support de l'appairage, Canvas, chat et caméra

<Note>
Les anciens chemins Claude, Codex, Gemini et Opencode ont été supprimés. Pi est le seul chemin d'agent de programmation.
</Note>
