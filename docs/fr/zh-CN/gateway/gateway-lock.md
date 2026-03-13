---
read_when:
  - 运行或调试 Gateway 网关进程
  - 调查单实例强制执行
summary: 使用 WebSocket 监听器绑定的 Gateway 网关单例保护
title: Gateway 网关锁
x-i18n:
  generated_at: "2026-02-03T07:47:52Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 15fdfa066d1925da8b4632073a876709f77ca8d40e6828c174a30d953ba4f8e9
  source_path: gateway/gateway-lock.md
  workflow: 15
---

# Verrou Gateway

Dernière mise à jour : 2025-12-11

## Raison

- Assurer qu'une seule instance Gateway s'exécute sur chaque port de base sur le même hôte ; les Gateway supplémentaires doivent utiliser des fichiers de configuration isolés et des ports uniques.
- Ne pas laisser de fichiers de verrou obsolètes après un crash/SIGKILL.
- Échouer rapidement avec un message d'erreur clair lorsque le port de contrôle est déjà occupé.

## Mécanisme

- Gateway se lie immédiatement au démarrage à l'écouteur WebSocket (par défaut `ws://127.0.0.1:18789`) avec un écouteur TCP exclusif.
- Si la liaison échoue en raison de `EADDRINUSE`, le démarrage lève `GatewayLockError("another gateway instance is already listening on ws://127.0.0.1:<port>")`.
- Le système d'exploitation libère automatiquement l'écouteur à la sortie de tout processus (y compris les crashs et SIGKILL) — aucun fichier de verrou séparé ou étape de nettoyage n'est nécessaire.
- À l'arrêt, Gateway ferme le serveur WebSocket et le serveur HTTP sous-jacent pour libérer le port en temps opportun.

## Surface d'erreur

- Si un autre processus détient le port, le démarrage lève `GatewayLockError("another gateway instance is already listening on ws://127.0.0.1:<port>")`.
- Les autres échecs de liaison s'affichent sous la forme `GatewayLockError("failed to bind gateway socket on ws://127.0.0.1:<port>: …")`.

## Notes opérationnelles

- Si le port est occupé par un *autre* processus, l'erreur est identique ; libérez le port ou choisissez un autre port avec `openclaw gateway --port <port>`.
- L'application macOS maintient toujours sa propre protection PID légère avant de démarrer Gateway ; le verrou d'exécution est appliqué par la liaison WebSocket.
