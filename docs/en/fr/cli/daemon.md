---
summary: "Référence CLI pour `openclaw daemon` (alias hérité pour la gestion du service de passerelle)"
read_when:
  - Vous utilisez toujours `openclaw daemon ...` dans les scripts
  - Vous avez besoin de commandes de cycle de vie du service (install/start/stop/restart/status)
title: "daemon"
---

# `openclaw daemon`

Alias hérité pour les commandes de gestion du service de passerelle.

`openclaw daemon ...` correspond à la même surface de contrôle de service que les commandes de service `openclaw gateway ...`.

## Utilisation

```bash
openclaw daemon status
openclaw daemon install
openclaw daemon start
openclaw daemon stop
openclaw daemon restart
openclaw daemon uninstall
```

## Sous-commandes

- `status`: afficher l'état d'installation du service et vérifier la santé de la passerelle
- `install`: installer le service (`launchd`/`systemd`/`schtasks`)
- `uninstall`: supprimer le service
- `start`: démarrer le service
- `stop`: arrêter le service
- `restart`: redémarrer le service

## Options communes

- `status`: `--url`, `--token`, `--password`, `--timeout`, `--no-probe`, `--deep`, `--json`
- `install`: `--port`, `--runtime <node|bun>`, `--token`, `--force`, `--json`
- cycle de vie (`uninstall|start|stop|restart`): `--json`

Notes :

- `status` résout les SecretRefs d'authentification configurés pour l'authentification de sonde si possible.
- Sur les installations systemd Linux, les vérifications de dérive de jeton `status` incluent à la fois les sources d'unité `Environment=` et `EnvironmentFile=`.
- Lorsque l'authentification par jeton nécessite un jeton et que `gateway.auth.token` est géré par SecretRef, `install` valide que le SecretRef est résolvable mais ne persiste pas le jeton résolu dans les métadonnées d'environnement du service.
- Si l'authentification par jeton nécessite un jeton et que le SecretRef de jeton configuré n'est pas résolu, l'installation échoue de manière sécurisée.
- Si à la fois `gateway.auth.token` et `gateway.auth.password` sont configurés et que `gateway.auth.mode` n'est pas défini, l'installation est bloquée jusqu'à ce que le mode soit défini explicitement.

## Préférer

Utilisez [`openclaw gateway`](/cli/gateway) pour la documentation et les exemples actuels.
