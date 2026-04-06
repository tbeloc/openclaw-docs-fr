---
title: "fal"
summary: "Configuration de la génération d'images et vidéos fal dans OpenClaw"
read_when:
  - You want to use fal image generation in OpenClaw
  - You need the FAL_KEY auth flow
  - You want fal defaults for image_generate or video_generate
---

# fal

OpenClaw est livré avec un fournisseur `fal` intégré pour la génération d'images et vidéos hébergées.

- Fournisseur : `fal`
- Authentification : `FAL_KEY` (canonique ; `FAL_API_KEY` fonctionne également comme solution de secours)
- API : points de terminaison des modèles fal

## Démarrage rapide

1. Définissez la clé API :

```bash
openclaw onboard --auth-choice fal-api-key
```

2. Définissez un modèle d'image par défaut :

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "fal/fal-ai/flux/dev",
      },
    },
  },
}
```

## Génération d'images

Le fournisseur de génération d'images `fal` intégré utilise par défaut
`fal/fal-ai/flux/dev`.

- Génération : jusqu'à 4 images par requête
- Mode édition : activé, 1 image de référence
- Supporte `size`, `aspectRatio` et `resolution`
- Limitation actuelle de l'édition : le point de terminaison d'édition d'image fal ne supporte **pas**
  les remplacements `aspectRatio`

Pour utiliser fal comme fournisseur d'images par défaut :

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "fal/fal-ai/flux/dev",
      },
    },
  },
}
```

## Génération vidéo

Le fournisseur de génération vidéo `fal` intégré utilise par défaut
`fal/fal-ai/minimax/video-01-live`.

- Modes : flux texte-vers-vidéo et flux de référence d'image unique
- Exécution : flux submit/status/result soutenu par une file d'attente pour les tâches longues

Pour utiliser fal comme fournisseur vidéo par défaut :

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "fal/fal-ai/minimax/video-01-live",
      },
    },
  },
}
```

## Connexes

- [Image Generation](/fr/tools/image-generation)
- [Video Generation](/fr/tools/video-generation)
- [Configuration Reference](/fr/gateway/configuration-reference#agent-defaults)
