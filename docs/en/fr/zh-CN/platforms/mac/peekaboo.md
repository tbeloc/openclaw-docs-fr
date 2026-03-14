---
read_when:
  - Hébergement de PeekabooBridge dans OpenClaw.app
  - Intégration de Peekaboo via Swift Package Manager
  - Modification du protocole/chemin de PeekabooBridge
summary: Intégration de PeekabooBridge pour l'automatisation de l'interface utilisateur macOS
title: Peekaboo Bridge
x-i18n:
  generated_at: "2026-02-01T21:32:57Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b5b9ddb9a7c59e153a1d5d23c33616bb1542b5c7dadedc3af340aeee9ba03487
  source_path: platforms/mac/peekaboo.md
  workflow: 15
---

# Peekaboo Bridge (Automatisation de l'interface utilisateur macOS)

OpenClaw peut héberger **PeekabooBridge** en tant qu'agent d'automatisation d'interface utilisateur local et conscient des permissions. Cela permet à la CLI `peekaboo` de piloter l'automatisation de l'interface utilisateur tout en réutilisant les permissions TCC de l'application macOS.

## Qu'est-ce que c'est (et ce que ce n'est pas)

- **Hôte** : OpenClaw.app peut servir d'hôte PeekabooBridge.
- **Client** : Utilise la CLI `peekaboo` (sans interface `openclaw ui ...` séparée).
- **Interface** : La superposition visuelle reste dans Peekaboo.app ; OpenClaw est simplement un hôte proxy léger.

## Activation du pont

Dans l'application macOS :

- Paramètres → **Activer Peekaboo Bridge**

Une fois activé, OpenClaw démarre un serveur de socket UNIX local. S'il est désactivé, l'hôte s'arrête et `peekaboo` bascule vers un autre hôte disponible.

## Ordre de découverte des clients

Le client Peekaboo essaie généralement les hôtes dans cet ordre :

1. Peekaboo.app (expérience utilisateur complète)
2. Claude.app (s'il est installé)
3. OpenClaw.app (proxy léger)

Utilisez `peekaboo bridge status --verbose` pour voir l'hôte actuellement actif et le chemin du socket utilisé. Vous pouvez le remplacer avec :

```bash
export PEEKABOO_BRIDGE_SOCKET=/path/to/bridge.sock
```

## Sécurité et permissions

- Le pont valide la **signature de code de l'appelant** ; applique une liste blanche de TeamID (TeamID de l'hôte Peekaboo + TeamID de l'application OpenClaw).
- Les requêtes expirent après environ 10 secondes.
- Si les permissions requises sont manquantes, le pont retourne un message d'erreur clair au lieu de lancer les paramètres système.

## Comportement des snapshots (automatisation)

Les snapshots sont stockés en mémoire et expirent automatiquement après une courte période. Si une rétention plus longue est nécessaire, recapturez depuis le client.

## Dépannage

- Si `peekaboo` signale « bridge client is not authorized », assurez-vous que le client est correctement signé, ou exécutez l'hôte uniquement en mode **débogage** avec `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1`.
- Si aucun hôte n'est trouvé, ouvrez l'une des applications hôtes (Peekaboo.app ou OpenClaw.app) et confirmez que les permissions ont été accordées.
