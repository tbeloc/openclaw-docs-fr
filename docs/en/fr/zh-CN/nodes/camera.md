---
read_when:
  - Ajouter ou modifier la capture de caméra sur un nœud iOS ou macOS
  - Étendre le flux de travail des fichiers temporaires MEDIA accessibles aux agents
summary: Capture de caméra pour les agents (nœud iOS + application macOS) : photos (jpg) et courts clips vidéo (mp4)
title: Capture de caméra
x-i18n:
  generated_at: "2026-02-03T07:50:55Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b4d5f5ecbab6f70597cf1e1f9cc5f7f54681253bd747442db16cc681203b5813
  source_path: nodes/camera.md
  workflow: 15
---

# Capture de caméra (Agents)

OpenClaw prend en charge la **capture de caméra** pour les flux de travail des agents :

- **Nœud iOS** (appairé via Gateway) : capture de **photos** (`jpg`) ou de **courts clips vidéo** (`mp4`, audio optionnel) via `node.invoke`.
- **Nœud Android** (appairé via Gateway) : capture de **photos** (`jpg`) ou de **courts clips vidéo** (`mp4`, audio optionnel) via `node.invoke`.
- **Application macOS** (nœud via Gateway) : capture de **photos** (`jpg`) ou de **courts clips vidéo** (`mp4`, audio optionnel) via `node.invoke`.

Tous les accès à la caméra sont limités par les **paramètres contrôlés par l'utilisateur**.

## Nœud iOS

### Paramètres utilisateur (activés par défaut)

- Onglet Paramètres iOS → **Caméra** → **Autoriser la caméra** (`camera.enabled`)
  - Par défaut : **Activé** (considéré comme activé si la clé est absente).
  - Lorsque désactivé : les commandes `camera.*` retournent `CAMERA_DISABLED`.

### Commandes (via Gateway `node.invoke`)

- `camera.list`
  - Charge utile de réponse :
    - `devices` : tableau de `{ id, name, position, deviceType }`

- `camera.snap`
  - Paramètres :
    - `facing` : `front|back` (par défaut : `front`)
    - `maxWidth` : nombre (optionnel ; par défaut `1600` pour le nœud iOS)
    - `quality` : `0..1` (optionnel ; par défaut `0.9`)
    - `format` : actuellement `jpg`
    - `delayMs` : nombre (optionnel ; par défaut `0`)
    - `deviceId` : chaîne (optionnel ; provenant de `camera.list`)
  - Charge utile de réponse :
    - `format: "jpg"`
    - `base64: "<...>"`
    - `width`, `height`
  - Protection de la charge utile : les photos sont recompressées pour maintenir la charge utile base64 en dessous de 5 MB.

- `camera.clip`
  - Paramètres :
    - `facing` : `front|back` (par défaut : `front`)
    - `durationMs` : nombre (par défaut `3000`, maximum `60000`)
    - `includeAudio` : booléen (par défaut `true`)
    - `format` : actuellement `mp4`
    - `deviceId` : chaîne (optionnel ; provenant de `camera.list`)
  - Charge utile de réponse :
    - `format: "mp4"`
    - `base64: "<...>"`
    - `durationMs`
    - `hasAudio`

### Exigence de premier plan

Comme pour `canvas.*`, le nœud iOS n'autorise l'exécution des commandes `camera.*` qu'en **premier plan**. Les appels en arrière-plan retournent `NODE_BACKGROUND_UNAVAILABLE`.

### Outil CLI auxiliaire (fichiers temporaires + MEDIA)

Le moyen le plus simple d'obtenir les pièces jointes est d'utiliser l'outil CLI auxiliaire, qui écrit les médias décodés dans un fichier temporaire et affiche `MEDIA:<path>`.

Exemple :

```bash
openclaw nodes camera snap --node <id>               # par défaut : avant et arrière (2 lignes MEDIA)
openclaw nodes camera snap --node <id> --facing front
openclaw nodes camera clip --node <id> --duration 3000
openclaw nodes camera clip --node <id> --no-audio
```

Remarques :

- `nodes camera snap` capture par défaut **deux** orientations pour fournir à l'agent deux perspectives.
- Les fichiers de sortie sont temporaires (dans le répertoire temporaire du système d'exploitation), sauf si vous créez votre propre wrapper.

## Nœud Android

### Paramètres utilisateur (activés par défaut)

- Page Paramètres Android → **Caméra** → **Autoriser la caméra** (`camera.enabled`)
  - Par défaut : **Activé** (considéré comme activé si la clé est absente).
  - Lorsque désactivé : les commandes `camera.*` retournent `CAMERA_DISABLED`.

### Permissions

- Android nécessite des permissions à l'exécution :
  - `CAMERA` pour `camera.snap` et `camera.clip`.
  - `RECORD_AUDIO` pour `camera.clip` lorsque `includeAudio=true`.

Si les permissions sont manquantes, l'application les demande si possible ; si elles sont refusées, les requêtes `camera.*` échouent et retournent une erreur `*_PERMISSION_REQUIRED`.

### Exigence de premier plan

Comme pour `canvas.*`, le nœud Android n'autorise l'exécution des commandes `camera.*` qu'en **premier plan**. Les appels en arrière-plan retournent `NODE_BACKGROUND_UNAVAILABLE`.

### Protection de la charge utile

Les photos sont recompressées pour maintenir la charge utile base64 en dessous de 5 MB.

## Application macOS

### Paramètres utilisateur (désactivés par défaut)

L'application compagnon macOS expose une case à cocher :

- **Paramètres → Général → Autoriser la caméra** (`openclaw.cameraEnabled`)
  - Par défaut : **Désactivé**
  - Lorsque désactivé : les requêtes de caméra retournent « L'utilisateur a désactivé la caméra ».

### Outil CLI auxiliaire (invocation de nœud)

Utilisez le CLI `openclaw` principal pour invoquer les commandes de caméra sur un nœud macOS.

Exemple :

```bash
openclaw nodes camera list --node <id>            # lister les identifiants de caméra
openclaw nodes camera snap --node <id>            # affiche MEDIA:<path>
openclaw nodes camera snap --node <id> --max-width 1280
openclaw nodes camera snap --node <id> --delay-ms 2000
openclaw nodes camera snap --node <id> --device-id <id>
openclaw nodes camera clip --node <id> --duration 10s          # affiche MEDIA:<path>
openclaw nodes camera clip --node <id> --duration-ms 3000      # affiche MEDIA:<path> (drapeau hérité)
openclaw nodes camera clip --node <id> --device-id <id>
openclaw nodes camera clip --node <id> --no-audio
```

Remarques :

- `openclaw nodes camera snap` utilise par défaut `maxWidth=1600`, sauf s'il est remplacé.
- Sur macOS, `camera.snap` attend `delayMs` (par défaut 2000ms) après le préchauffage/stabilisation de l'exposition avant de capturer.
- La charge utile de la photo est recompressée pour maintenir base64 en dessous de 5 MB.

## Sécurité + Limitations pratiques

- L'accès à la caméra et au microphone déclenche les invites de permission du système d'exploitation habituelles (et nécessite des chaînes de description d'utilisation dans Info.plist).
- Les clips vidéo ont une limite supérieure (actuellement `<= 60s`) pour éviter des charges utiles de nœud trop volumineuses (surcharge base64 + limites de messages).

## Vidéo d'écran macOS (niveau du système d'exploitation)

Pour les vidéos d'*écran* (non-caméra), utilisez l'application compagnon macOS :

```bash
openclaw nodes screen record --node <id> --duration 10s --fps 15   # affiche MEDIA:<path>
```

Remarques :

- Nécessite la permission macOS **Enregistrement d'écran** (TCC).
