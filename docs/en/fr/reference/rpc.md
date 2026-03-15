---
summary: "Adaptateurs RPC pour les CLIs externes (signal-cli, imsg hérité) et modèles de passerelle"
read_when:
  - Ajout ou modification d'intégrations CLI externes
  - Débogage des adaptateurs RPC (signal-cli, imsg)
title: "Adaptateurs RPC"
---

# Adaptateurs RPC

OpenClaw intègre les CLIs externes via JSON-RPC. Deux modèles sont utilisés aujourd'hui.

## Modèle A : démon HTTP (signal-cli)

- `signal-cli` s'exécute en tant que démon avec JSON-RPC sur HTTP.
- Le flux d'événements est SSE (`/api/v1/events`).
- Sonde de santé : `/api/v1/check`.
- OpenClaw possède le cycle de vie lorsque `channels.signal.autoStart=true`.

Voir [Signal](/fr/channels/signal) pour la configuration et les points de terminaison.

## Modèle B : processus enfant stdio (hérité : imsg)

> **Note :** Pour les nouvelles configurations iMessage, utilisez [BlueBubbles](/fr/channels/bluebubbles) à la place.

- OpenClaw lance `imsg rpc` en tant que processus enfant (intégration iMessage hérité).
- JSON-RPC est délimité par des sauts de ligne sur stdin/stdout (un objet JSON par ligne).
- Pas de port TCP, pas de démon requis.

Méthodes principales utilisées :

- `watch.subscribe` → notifications (`method: "message"`)
- `watch.unsubscribe`
- `send`
- `chats.list` (sonde/diagnostics)

Voir [iMessage](/fr/channels/imessage) pour la configuration hérité et l'adressage (`chat_id` préféré).

## Directives d'adaptateur

- La passerelle possède le processus (démarrage/arrêt lié au cycle de vie du fournisseur).
- Gardez les clients RPC résilients : délais d'expiration, redémarrage à la sortie.
- Préférez les IDs stables (par exemple, `chat_id`) aux chaînes d'affichage.
