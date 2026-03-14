---
summary: "Utilisation de l'hôte statique Loopback WebChat et de la passerelle WS pour l'interface utilisateur de chat"
read_when:
  - Debugging or configuring WebChat access
title: "WebChat"
---

# WebChat (Interface utilisateur Gateway WebSocket)

Statut : l'interface utilisateur de chat SwiftUI macOS/iOS communique directement avec la passerelle WebSocket.

## Qu'est-ce que c'est

- Une interface utilisateur de chat native pour la passerelle (pas de navigateur intégré et pas de serveur statique local).
- Utilise les mêmes sessions et règles de routage que les autres canaux.
- Routage déterministe : les réponses reviennent toujours à WebChat.

## Démarrage rapide

1. Démarrez la passerelle.
2. Ouvrez l'interface utilisateur WebChat (application macOS/iOS) ou l'onglet chat de l'interface de contrôle.
3. Assurez-vous que l'authentification de la passerelle est configurée (requise par défaut, même sur loopback).

## Fonctionnement (comportement)

- L'interface utilisateur se connecte à la passerelle WebSocket et utilise `chat.history`, `chat.send` et `chat.inject`.
- `chat.history` est limité pour la stabilité : la passerelle peut tronquer les champs de texte longs, omettre les métadonnées lourdes et remplacer les entrées surdimensionnées par `[chat.history omitted: message too large]`.
- `chat.inject` ajoute une note d'assistant directement à la transcription et la diffuse à l'interface utilisateur (pas d'exécution d'agent).
- Les exécutions interrompues peuvent conserver une sortie d'assistant partielle visible dans l'interface utilisateur.
- La passerelle persiste le texte d'assistant partiel interrompu dans l'historique des transcriptions lorsqu'une sortie en mémoire tampon existe, et marque ces entrées avec des métadonnées d'interruption.
- L'historique est toujours récupéré à partir de la passerelle (pas de surveillance de fichier local).
- Si la passerelle est inaccessible, WebChat est en lecture seule.

## Panneau des outils de l'interface de contrôle

- Le panneau Outils `/agents` de l'interface de contrôle récupère un catalogue d'exécution via `tools.catalog` et étiquette chaque outil comme `core` ou `plugin:<id>` (plus `optional` pour les outils de plugin optionnels).
- Si `tools.catalog` n'est pas disponible, le panneau revient à une liste statique intégrée.
- Le panneau modifie la configuration du profil et des remplacements, mais l'accès d'exécution effectif suit toujours la précédence des politiques (`allow`/`deny`, remplacements par agent et fournisseur/canal).

## Utilisation à distance

- Le mode distant tunnelise la passerelle WebSocket via SSH/Tailscale.
- Vous n'avez pas besoin d'exécuter un serveur WebChat séparé.

## Référence de configuration (WebChat)

Configuration complète : [Configuration](/gateway/configuration)

Options de canal :

- Pas de bloc `webchat.*` dédié. WebChat utilise le point de terminaison de la passerelle + les paramètres d'authentification ci-dessous.

Options globales associées :

- `gateway.port`, `gateway.bind` : hôte/port WebSocket.
- `gateway.auth.mode`, `gateway.auth.token`, `gateway.auth.password` : authentification WebSocket (token/password).
- `gateway.auth.mode: "trusted-proxy"` : authentification par proxy inverse pour les clients navigateur (voir [Authentification par proxy de confiance](/gateway/trusted-proxy-auth)).
- `gateway.remote.url`, `gateway.remote.token`, `gateway.remote.password` : cible de passerelle distante.
- `session.*` : stockage de session et valeurs par défaut de clé principale.
