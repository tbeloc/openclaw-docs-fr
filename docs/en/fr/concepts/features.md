---
summary: "Capacités d'OpenClaw sur les canaux, le routage, les médias et l'UX."
read_when:
  - Vous voulez une liste complète de ce qu'OpenClaw supporte
title: "Fonctionnalités"
---

## Points forts

<Columns>
  <Card title="Canaux" icon="message-square">
    WhatsApp, Telegram, Discord et iMessage avec une seule passerelle.
  </Card>
  <Card title="Plugins" icon="plug">
    Ajoutez Mattermost et plus avec des extensions.
  </Card>
  <Card title="Routage" icon="route">
    Routage multi-agent avec sessions isolées.
  </Card>
  <Card title="Médias" icon="image">
    Images, audio et documents en entrée et sortie.
  </Card>
  <Card title="Applications et interface utilisateur" icon="monitor">
    Interface de contrôle Web et application compagnon macOS.
  </Card>
  <Card title="Nœuds mobiles" icon="smartphone">
    Nœuds iOS et Android avec appairage, voix/chat et commandes riches d'appareil.
  </Card>
</Columns>

## Liste complète

- Intégration WhatsApp via WhatsApp Web (Baileys)
- Support des bots Telegram (grammY)
- Support des bots Discord (channels.discord.js)
- Support des bots Mattermost (plugin)
- Intégration iMessage via CLI imsg local (macOS)
- Pont d'agent pour Pi en mode RPC avec streaming d'outils
- Streaming et chunking pour les réponses longues
- Routage multi-agent pour les sessions isolées par espace de travail ou expéditeur
- Authentification par abonnement pour Anthropic et OpenAI via OAuth
- Sessions : les chats directs se regroupent dans `main` partagé ; les groupes sont isolés
- Support des chats de groupe avec activation basée sur les mentions
- Support des médias pour les images, l'audio et les documents
- Hook optionnel de transcription des notes vocales
- Application WebChat et barre de menu macOS
- Nœud iOS avec appairage, Canvas, caméra, enregistrement d'écran, localisation et fonctionnalités vocales
- Nœud Android avec appairage, onglet Connect, sessions de chat, onglet voix, Canvas/caméra, ainsi que commandes d'appareil, notifications, contacts/calendrier, mouvement, photos et SMS

<Note>
Les chemins hérités Claude, Codex, Gemini et Opencode ont été supprimés. Pi est le seul
chemin d'agent de codage.
</Note>
