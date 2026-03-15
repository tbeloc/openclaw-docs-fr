---
summary: "Verrou singleton de passerelle utilisant la liaison d'écoute WebSocket"
read_when:
  - Exécution ou débogage du processus de passerelle
  - Enquête sur l'application de l'instance unique
title: "Verrou de passerelle"
---

# Verrou de passerelle

Dernière mise à jour : 2025-12-11

## Pourquoi

- Assurer qu'une seule instance de passerelle s'exécute par port de base sur le même hôte ; les passerelles supplémentaires doivent utiliser des profils isolés et des ports uniques.
- Survivre aux plantages/SIGKILL sans laisser de fichiers de verrou obsolètes.
- Échouer rapidement avec une erreur claire lorsque le port de contrôle est déjà occupé.

## Mécanisme

- La passerelle lie l'écouteur WebSocket (par défaut `ws://127.0.0.1:18789`) immédiatement au démarrage en utilisant un écouteur TCP exclusif.
- Si la liaison échoue avec `EADDRINUSE`, le démarrage lève `GatewayLockError("another gateway instance is already listening on ws://127.0.0.1:<port>")`.
- Le système d'exploitation libère l'écouteur automatiquement à la sortie de tout processus, y compris les plantages et SIGKILL—aucun fichier de verrou séparé ou étape de nettoyage n'est nécessaire.
- À l'arrêt, la passerelle ferme le serveur WebSocket et le serveur HTTP sous-jacent pour libérer le port rapidement.

## Surface d'erreur

- Si un autre processus détient le port, le démarrage lève `GatewayLockError("another gateway instance is already listening on ws://127.0.0.1:<port>")`.
- Les autres échecs de liaison apparaissent comme `GatewayLockError("failed to bind gateway socket on ws://127.0.0.1:<port>: …")`.

## Notes opérationnelles

- Si le port est occupé par un _autre_ processus, l'erreur est la même ; libérez le port ou choisissez-en un autre avec `openclaw gateway --port <port>`.
- L'application macOS maintient toujours son propre garde PID léger avant de générer la passerelle ; le verrou d'exécution est appliqué par la liaison WebSocket.
