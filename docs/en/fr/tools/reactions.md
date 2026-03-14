---
summary: "Sémantique des réactions partagée entre les canaux"
read_when:
  - Working on reactions in any channel
title: "Réactions"
---

# Outils de réaction

Sémantique des réactions partagée entre les canaux :

- `emoji` est obligatoire lors de l'ajout d'une réaction.
- `emoji=""` supprime la/les réaction(s) du bot si supporté.
- `remove: true` supprime l'emoji spécifié si supporté (nécessite `emoji`).

Notes par canal :

- **Discord/Slack** : un `emoji` vide supprime toutes les réactions du bot sur le message ; `remove: true` supprime uniquement cet emoji.
- **Google Chat** : un `emoji` vide supprime les réactions de l'application sur le message ; `remove: true` supprime uniquement cet emoji.
- **Telegram** : un `emoji` vide supprime les réactions du bot ; `remove: true` supprime également les réactions mais nécessite toujours un `emoji` non vide pour la validation de l'outil.
- **WhatsApp** : un `emoji` vide supprime la réaction du bot ; `remove: true` correspond à un emoji vide (nécessite toujours `emoji`).
- **Zalo Personal (`zalouser`)** : nécessite un `emoji` non vide ; `remove: true` supprime cette réaction emoji spécifique.
- **Signal** : les notifications de réaction entrantes émettent des événements système lorsque `channels.signal.reactionNotifications` est activé.
