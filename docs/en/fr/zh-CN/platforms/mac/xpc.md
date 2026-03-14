---
read_when:
  - Édition de contrats IPC ou applications de barre de menus IPC
summary: Architecture macOS IPC d'OpenClaw, transmission du nœud Gateway et PeekabooBridge
title: macOS IPC
x-i18n:
  generated_at: "2026-02-03T07:52:57Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: d0211c334a4a59b71afb29dd7b024778172e529fa618985632d3d11d795ced92
  source_path: platforms/mac/xpc.md
  workflow: 15
---

# Architecture macOS IPC d'OpenClaw

**Modèle actuel :** Une socket Unix locale connecte le **service hôte nœud** à l'**application macOS**, pour l'approbation exec + `system.run`. Il existe un CLI de débogage `openclaw-mac` pour la découverte/vérification de connexion ; les opérations d'agent transitent toujours par Gateway WebSocket et `node.invoke`. L'automatisation UI utilise PeekabooBridge.

## Objectifs

- Une seule instance d'application GUI possède tous les travaux orientés TCC (notifications, enregistrement d'écran, microphone, voix, AppleScript).
- Interface d'automatisation minimaliste : Gateway + commandes nœud, plus PeekabooBridge pour l'automatisation UI.
- Permissions prévisibles : toujours le même bundle ID signé, lancé par launchd, donc les autorisations TCC restent valides.

## Fonctionnement

### Transmission Gateway + Nœud

- L'application exécute Gateway (mode local) et se connecte à elle en tant que nœud.
- Les opérations d'agent s'exécutent via `node.invoke` (par exemple `system.run`, `system.notify`, `canvas.*`).

### Service Nœud + IPC Application

- Un service hôte nœud sans interface se connecte à Gateway WebSocket.
- Les requêtes `system.run` sont transférées via socket Unix locale à l'application macOS.
- L'application exécute exec dans le contexte UI, invite si nécessaire, et retourne la sortie.

Diagramme (SCI) :

```
Agent -> Gateway -> Node Service (WS)
                      |  IPC (UDS + token + HMAC + TTL)
                      v
                  Mac App (UI + TCC + system.run)
```

### PeekabooBridge (Automatisation UI)

- L'automatisation UI utilise une socket UNIX séparée nommée `bridge.sock` et le protocole JSON PeekabooBridge.
- Ordre de préférence hôte (côté client) : Peekaboo.app → Claude.app → OpenClaw.app → exécution locale.
- Sécurité : l'hôte bridge nécessite un TeamID autorisé ; le canal d'échappement même UID DEBUG uniquement est protégé par `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` (convention Peekaboo).
- Voir : [Utilisation de PeekabooBridge](/platforms/mac/peekaboo) pour plus de détails.

## Flux opérationnel

- Redémarrage/reconstruction : `SIGN_IDENTITY="Apple Development: <Developer Name> (<TEAMID>)" scripts/restart-mac.sh`
  - Terminer les instances existantes
  - Construction Swift + empaquetage
  - Écrire/amorcer/lancer LaunchAgent
- Instance unique : si une autre instance avec le même bundle ID s'exécute, l'application se termine tôt.

## Considérations de durcissement

- Exiger la correspondance TeamID pour toutes les interfaces privilégiées en priorité.
- PeekabooBridge : `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` (DEBUG uniquement) peut permettre aux appelants même UID pour le développement local.
- Toutes les communications restent locales ; ne pas exposer les sockets réseau.
- Les invites TCC proviennent uniquement du bundle d'application GUI ; maintenir le bundle ID signé stable lors de la reconstruction.
- Durcissement IPC : mode socket `0600`, token, vérification UID pair, défi/réponse HMAC, TTL court.
