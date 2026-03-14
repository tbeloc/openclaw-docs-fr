```markdown
---
summary: "Dépanner l'appairage des nœuds, les exigences de premier plan, les permissions et les défaillances d'outils"
read_when:
  - Node is connected but camera/canvas/screen/exec tools fail
  - You need the node pairing versus approvals mental model
title: "Dépannage des nœuds"
---

# Dépannage des nœuds

Utilisez cette page lorsqu'un nœud est visible dans le statut mais que les outils du nœud échouent.

## Échelle de commandes

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Ensuite, exécutez les vérifications spécifiques au nœud :

```bash
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
openclaw approvals get --node <idOrNameOrIp>
```

Signaux de bonne santé :

- Le nœud est connecté et appairé pour le rôle `node`.
- `nodes describe` inclut la capacité que vous appelez.
- Les approbations exec affichent le mode/allowlist attendu.

## Exigences de premier plan

`canvas.*`, `camera.*` et `screen.*` sont réservés au premier plan sur les nœuds iOS/Android.

Vérification et correction rapides :

```bash
openclaw nodes describe --node <idOrNameOrIp>
openclaw nodes canvas snapshot --node <idOrNameOrIp>
openclaw logs --follow
```

Si vous voyez `NODE_BACKGROUND_UNAVAILABLE`, mettez l'application du nœud au premier plan et réessayez.

## Matrice des permissions

| Capacité                     | iOS                                     | Android                                      | Application nœud macOS        | Code d'erreur typique          |
| ---------------------------- | --------------------------------------- | -------------------------------------------- | ----------------------------- | ------------------------------ |
| `camera.snap`, `camera.clip` | Caméra (+ micro pour l'audio du clip)   | Caméra (+ micro pour l'audio du clip)        | Caméra (+ micro pour l'audio) | `*_PERMISSION_REQUIRED`        |
| `screen.record`              | Enregistrement d'écran (+ micro optionnel) | Invite de capture d'écran (+ micro optionnel) | Enregistrement d'écran        | `*_PERMISSION_REQUIRED`        |
| `location.get`               | Pendant l'utilisation ou Toujours (selon le mode) | Localisation au premier plan/arrière-plan selon le mode | Permission de localisation | `LOCATION_PERMISSION_REQUIRED` |
| `system.run`                 | n/a (chemin d'accès du nœud hôte)      | n/a (chemin d'accès du nœud hôte)            | Approbations exec requises    | `SYSTEM_RUN_DENIED`            |

## Appairage versus approbations

Ce sont des portes différentes :

1. **Appairage d'appareil** : ce nœud peut-il se connecter à la passerelle ?
2. **Approbations exec** : ce nœud peut-il exécuter une commande shell spécifique ?

Vérifications rapides :

```bash
openclaw devices list
openclaw nodes status
openclaw approvals get --node <idOrNameOrIp>
openclaw approvals allowlist add --node <idOrNameOrIp> "/usr/bin/uname"
```

Si l'appairage est manquant, approuvez d'abord l'appareil du nœud.
Si l'appairage est correct mais que `system.run` échoue, corrigez les approbations exec/allowlist.

## Codes d'erreur courants des nœuds

- `NODE_BACKGROUND_UNAVAILABLE` → l'application est en arrière-plan ; mettez-la au premier plan.
- `CAMERA_DISABLED` → le bouton bascule de la caméra est désactivé dans les paramètres du nœud.
- `*_PERMISSION_REQUIRED` → permission du système d'exploitation manquante/refusée.
- `LOCATION_DISABLED` → le mode de localisation est désactivé.
- `LOCATION_PERMISSION_REQUIRED` → le mode de localisation demandé n'a pas été accordé.
- `LOCATION_BACKGROUND_UNAVAILABLE` → l'application est en arrière-plan mais seule la permission « Pendant l'utilisation » existe.
- `SYSTEM_RUN_DENIED: approval required` → la demande exec nécessite une approbation explicite.
- `SYSTEM_RUN_DENIED: allowlist miss` → commande bloquée par le mode allowlist.
  Sur les hôtes de nœud Windows, les formes de shell-wrapper comme `cmd.exe /c ...` sont traitées comme des absences d'allowlist en
  mode allowlist sauf si elles sont approuvées via le flux de demande.

## Boucle de récupération rapide

```bash
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
openclaw approvals get --node <idOrNameOrIp>
openclaw logs --follow
```

Si vous êtes toujours bloqué :

- Réapprouvez l'appairage de l'appareil.
- Rouvrez l'application du nœud (premier plan).
- Réaccordez les permissions du système d'exploitation.
- Recréez/ajustez la politique d'approbation exec.

Connexes :

- [/nodes/index](/nodes/index)
- [/nodes/camera](/nodes/camera)
- [/nodes/location-command](/nodes/location-command)
- [/tools/exec-approvals](/tools/exec-approvals)
- [/gateway/pairing](/gateway/pairing)
```
