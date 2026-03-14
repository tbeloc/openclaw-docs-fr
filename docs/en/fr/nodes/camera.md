---
summary: "Capture de caméra (nœuds iOS/Android + app macOS) pour utilisation par agent : photos (jpg) et courts clips vidéo (mp4)"
read_when:
  - Ajout ou modification de la capture de caméra sur les nœuds iOS/Android ou macOS
  - Extension des workflows de fichiers temporaires MEDIA accessibles aux agents
title: "Capture de caméra"
---

# Capture de caméra (agent)

OpenClaw supporte la **capture de caméra** pour les workflows d'agent :

- **Nœud iOS** (appairé via Gateway) : capture une **photo** (`jpg`) ou un **court clip vidéo** (`mp4`, avec audio optionnel) via `node.invoke`.
- **Nœud Android** (appairé via Gateway) : capture une **photo** (`jpg`) ou un **court clip vidéo** (`mp4`, avec audio optionnel) via `node.invoke`.
- **App macOS** (nœud via Gateway) : capture une **photo** (`jpg`) ou un **court clip vidéo** (`mp4`, avec audio optionnel) via `node.invoke`.

Tous les accès à la caméra sont contrôlés par des **paramètres gérés par l'utilisateur**.

## Nœud iOS

### Paramètre utilisateur (activé par défaut)

- Onglet Paramètres iOS → **Caméra** → **Autoriser la caméra** (`camera.enabled`)
  - Par défaut : **activé** (une clé manquante est traitée comme activée).
  - Quand désactivé : les commandes `camera.*` retournent `CAMERA_DISABLED`.

### Commandes (via Gateway `node.invoke`)

- `camera.list`
  - Payload de réponse :
    - `devices` : tableau de `{ id, name, position, deviceType }`

- `camera.snap`
  - Paramètres :
    - `facing` : `front|back` (par défaut : `front`)
    - `maxWidth` : nombre (optionnel ; par défaut `1600` sur le nœud iOS)
    - `quality` : `0..1` (optionnel ; par défaut `0.9`)
    - `format` : actuellement `jpg`
    - `delayMs` : nombre (optionnel ; par défaut `0`)
    - `deviceId` : chaîne (optionnel ; depuis `camera.list`)
  - Payload de réponse :
    - `format: "jpg"`
    - `base64: "<...>"`
    - `width`, `height`
  - Garde de payload : les photos sont recompressées pour maintenir le payload base64 sous 5 MB.

- `camera.clip`
  - Paramètres :
    - `facing` : `front|back` (par défaut : `front`)
    - `durationMs` : nombre (par défaut `3000`, limité à un maximum de `60000`)
    - `includeAudio` : booléen (par défaut `true`)
    - `format` : actuellement `mp4`
    - `deviceId` : chaîne (optionnel ; depuis `camera.list`)
  - Payload de réponse :
    - `format: "mp4"`
    - `base64: "<...>"`
    - `durationMs`
    - `hasAudio`

### Exigence de premier plan

Comme `canvas.*`, le nœud iOS n'autorise les commandes `camera.*` qu'au **premier plan**. Les invocations en arrière-plan retournent `NODE_BACKGROUND_UNAVAILABLE`.

### Assistant CLI (fichiers temporaires + MEDIA)

Le moyen le plus simple d'obtenir des pièces jointes est via l'assistant CLI, qui écrit les médias décodés dans un fichier temporaire et affiche `MEDIA:<path>`.

Exemples :

```bash
openclaw nodes camera snap --node <id>               # par défaut : avant et arrière (2 lignes MEDIA)
openclaw nodes camera snap --node <id> --facing front
openclaw nodes camera clip --node <id> --duration 3000
openclaw nodes camera clip --node <id> --no-audio
```

Notes :

- `nodes camera snap` utilise par défaut les **deux** orientations pour donner à l'agent les deux vues.
- Les fichiers de sortie sont temporaires (dans le répertoire temporaire du système d'exploitation) sauf si vous créez votre propre wrapper.

## Nœud Android

### Paramètre utilisateur Android (activé par défaut)

- Feuille Paramètres Android → **Caméra** → **Autoriser la caméra** (`camera.enabled`)
  - Par défaut : **activé** (une clé manquante est traitée comme activée).
  - Quand désactivé : les commandes `camera.*` retournent `CAMERA_DISABLED`.

### Permissions

- Android nécessite des permissions à l'exécution :
  - `CAMERA` pour `camera.snap` et `camera.clip`.
  - `RECORD_AUDIO` pour `camera.clip` quand `includeAudio=true`.

Si les permissions sont manquantes, l'app demandera si possible ; si refusées, les requêtes `camera.*` échouent avec une erreur `*_PERMISSION_REQUIRED`.

### Exigence de premier plan Android

Comme `canvas.*`, le nœud Android n'autorise les commandes `camera.*` qu'au **premier plan**. Les invocations en arrière-plan retournent `NODE_BACKGROUND_UNAVAILABLE`.

### Commandes Android (via Gateway `node.invoke`)

- `camera.list`
  - Payload de réponse :
    - `devices` : tableau de `{ id, name, position, deviceType }`

### Garde de payload

Les photos sont recompressées pour maintenir le payload base64 sous 5 MB.

## App macOS

### Paramètre utilisateur (désactivé par défaut)

L'app compagnon macOS expose une case à cocher :

- **Paramètres → Général → Autoriser la caméra** (`openclaw.cameraEnabled`)
  - Par défaut : **désactivé**
  - Quand désactivé : les requêtes de caméra retournent "Camera disabled by user".

### Assistant CLI (invocation de nœud)

Utilisez la CLI `openclaw` principale pour invoquer les commandes de caméra sur le nœud macOS.

Exemples :

```bash
openclaw nodes camera list --node <id>            # liste les ids de caméra
openclaw nodes camera snap --node <id>            # affiche MEDIA:<path>
openclaw nodes camera snap --node <id> --max-width 1280
openclaw nodes camera snap --node <id> --delay-ms 2000
openclaw nodes camera snap --node <id> --device-id <id>
openclaw nodes camera clip --node <id> --duration 10s          # affiche MEDIA:<path>
openclaw nodes camera clip --node <id> --duration-ms 3000      # affiche MEDIA:<path> (ancien flag)
openclaw nodes camera clip --node <id> --device-id <id>
openclaw nodes camera clip --node <id> --no-audio
```

Notes :

- `openclaw nodes camera snap` utilise par défaut `maxWidth=1600` sauf si remplacé.
- Sur macOS, `camera.snap` attend `delayMs` (par défaut 2000ms) après le réchauffement/stabilisation de l'exposition avant de capturer.
- Les payloads de photo sont recompressés pour maintenir base64 sous 5 MB.

## Sécurité + limites pratiques

- L'accès à la caméra et au microphone déclenche les invites de permission du système d'exploitation habituelles (et nécessitent des chaînes d'utilisation dans Info.plist).
- Les clips vidéo sont limités (actuellement `<= 60s`) pour éviter les payloads de nœud surdimensionnés (surcharge base64 + limites de messages).

## Vidéo d'écran macOS (niveau OS)

Pour la vidéo d'**écran** (pas de caméra), utilisez l'app compagnon macOS :

```bash
openclaw nodes screen record --node <id> --duration 10s --fps 15   # affiche MEDIA:<path>
```

Notes :

- Nécessite la permission macOS **Screen Recording** (TCC).
