---
summary: "Référence CLI pour `openclaw proxy`, le proxy de débogage local et l'inspecteur de capture"
read_when:
  - Vous devez capturer le trafic de transport OpenClaw localement pour le débogage
  - Vous souhaitez inspecter les sessions de proxy de débogage, les blobs ou les présets de requête intégrés
title: "proxy"
---

# `openclaw proxy`

Exécutez le proxy de débogage explicite local et inspectez le trafic capturé.

Il s'agit d'une commande de débogage pour l'investigation au niveau du transport. Elle peut démarrer un proxy local, exécuter une commande enfant avec capture activée, lister les sessions de capture, interroger les modèles de trafic courants, lire les blobs capturés et purger les données de capture locales.

## Commandes

```bash
openclaw proxy start [--host <host>] [--port <port>]
openclaw proxy run [--host <host>] [--port <port>] -- <cmd...>
openclaw proxy coverage
openclaw proxy sessions [--limit <count>]
openclaw proxy query --preset <name> [--session <id>]
openclaw proxy blob --id <blobId>
openclaw proxy purge
```

## Présets de requête

`openclaw proxy query --preset <name>` accepte :

- `double-sends`
- `retry-storms`
- `cache-busting`
- `ws-duplicate-frames`
- `missing-ack`
- `error-bursts`

## Notes

- `start` utilise par défaut `127.0.0.1` sauf si `--host` est défini.
- `run` démarre un proxy de débogage local puis exécute la commande après `--`.
- Les captures sont des données de débogage locales ; utilisez `openclaw proxy purge` une fois terminé.
