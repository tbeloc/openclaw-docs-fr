---
summary: "Architecture IPC macOS pour l'app OpenClaw, transport du nœud passerelle et PeekabooBridge"
read_when:
  - Editing IPC contracts or menu bar app IPC
title: "macOS IPC"
---

# Architecture IPC macOS OpenClaw

**Modèle actuel :** un socket Unix local connecte le **service hôte nœud** à l'**app macOS** pour les approbations d'exécution + `system.run`. Un CLI de débogage `openclaw-mac` existe pour les vérifications de découverte/connexion ; les actions d'agent transitent toujours par la WebSocket Gateway et `node.invoke`. L'automatisation UI utilise PeekabooBridge.

## Objectifs

- Une seule instance d'app GUI qui gère tout le travail face à TCC (notifications, enregistrement d'écran, micro, parole, AppleScript).
- Une petite surface d'automatisation : commandes Gateway + node, plus PeekabooBridge pour l'automatisation UI.
- Permissions prévisibles : toujours le même ID de bundle signé, lancé par launchd, donc les octrois TCC persistent.

## Fonctionnement

### Transport Gateway + node

- L'app exécute la Gateway (mode local) et s'y connecte en tant que nœud.
- Les actions d'agent sont effectuées via `node.invoke` (par ex. `system.run`, `system.notify`, `canvas.*`).

### IPC service nœud + app

- Un service hôte nœud sans interface se connecte à la WebSocket Gateway.
- Les requêtes `system.run` sont transférées à l'app macOS via un socket Unix local.
- L'app effectue l'exécution en contexte UI, demande une confirmation si nécessaire, et retourne la sortie.

Diagramme (SCI) :

```
Agent -> Gateway -> Node Service (WS)
                      |  IPC (UDS + token + HMAC + TTL)
                      v
                  Mac App (UI + TCC + system.run)
```

### PeekabooBridge (automatisation UI)

- L'automatisation UI utilise un socket UNIX séparé nommé `bridge.sock` et le protocole JSON PeekabooBridge.
- Ordre de préférence d'hôte (côté client) : Peekaboo.app → Claude.app → OpenClaw.app → exécution locale.
- Sécurité : les hôtes bridge nécessitent un TeamID autorisé ; l'échappatoire DEBUG-only même-UID est protégée par `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` (convention Peekaboo).
- Voir : [utilisation de PeekabooBridge](/platforms/mac/peekaboo) pour les détails.

## Flux opérationnels

- Redémarrage/reconstruction : `SIGN_IDENTITY="Apple Development: <Developer Name> (<TEAMID>)" scripts/restart-mac.sh`
  - Tue les instances existantes
  - Build Swift + empaquetage
  - Écrit/amorce/démarre le LaunchAgent
- Instance unique : l'app se ferme rapidement si une autre instance avec le même ID de bundle est en cours d'exécution.

## Notes de durcissement

- Préférer exiger une correspondance TeamID pour toutes les surfaces privilégiées.
- PeekabooBridge : `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` (DEBUG-only) peut autoriser les appelants même-UID pour le développement local.
- Toute communication reste locale uniquement ; aucun socket réseau n'est exposé.
- Les invites TCC proviennent uniquement du bundle d'app GUI ; maintenez l'ID de bundle signé stable entre les reconstructions.
- Durcissement IPC : mode socket `0600`, token, vérifications peer-UID, défi/réponse HMAC, TTL court.
