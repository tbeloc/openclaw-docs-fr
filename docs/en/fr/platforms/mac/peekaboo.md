---
summary: "Intégration de PeekabooBridge pour l'automatisation de l'interface utilisateur macOS"
read_when:
  - Hosting PeekabooBridge in OpenClaw.app
  - Integrating Peekaboo via Swift Package Manager
  - Changing PeekabooBridge protocol/paths
title: "Peekaboo Bridge"
---

# Peekaboo Bridge (automatisation de l'interface utilisateur macOS)

OpenClaw peut héberger **PeekabooBridge** en tant que courtier d'automatisation d'interface utilisateur local et conscient des permissions. Cela permet à la CLI `peekaboo` de piloter l'automatisation de l'interface utilisateur tout en réutilisant les permissions TCC de l'application macOS.

## Ce que c'est (et ce que ce n'est pas)

- **Hôte** : OpenClaw.app peut agir comme hôte PeekabooBridge.
- **Client** : utilisez la CLI `peekaboo` (pas de surface `openclaw ui ...` distincte).
- **Interface utilisateur** : les superpositions visuelles restent dans Peekaboo.app ; OpenClaw est un hôte courtier léger.

## Activer le bridge

Dans l'application macOS :

- Paramètres → **Enable Peekaboo Bridge**

Lorsqu'il est activé, OpenClaw démarre un serveur de socket UNIX local. S'il est désactivé, l'hôte est arrêté et `peekaboo` basculera vers d'autres hôtes disponibles.

## Ordre de découverte des clients

Les clients Peekaboo essaient généralement les hôtes dans cet ordre :

1. Peekaboo.app (expérience complète)
2. Claude.app (s'il est installé)
3. OpenClaw.app (courtier léger)

Utilisez `peekaboo bridge status --verbose` pour voir quel hôte est actif et quel chemin de socket est utilisé. Vous pouvez remplacer avec :

```bash
export PEEKABOO_BRIDGE_SOCKET=/path/to/bridge.sock
```

## Sécurité et permissions

- Le bridge valide les **signatures de code de l'appelant** ; une liste blanche de TeamID est appliquée (TeamID de l'hôte Peekaboo + TeamID de l'application OpenClaw).
- Les demandes expirent après environ 10 secondes.
- Si les permissions requises sont manquantes, le bridge retourne un message d'erreur clair au lieu de lancer les Paramètres Système.

## Comportement des snapshots (automatisation)

Les snapshots sont stockés en mémoire et expirent automatiquement après une courte période. Si vous avez besoin d'une rétention plus longue, recapturez à partir du client.

## Dépannage

- Si `peekaboo` signale « bridge client is not authorized », assurez-vous que le client est correctement signé ou exécutez l'hôte avec `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` en mode **debug** uniquement.
- Si aucun hôte n'est trouvé, ouvrez l'une des applications hôtes (Peekaboo.app ou OpenClaw.app) et confirmez que les permissions sont accordées.
