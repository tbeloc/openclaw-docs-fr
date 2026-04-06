---
title: "Runway"
summary: "Configuration de la génération vidéo Runway dans OpenClaw"
read_when:
  - You want to use Runway video generation in OpenClaw
  - You need the Runway API key/env setup
  - You want to make Runway the default video provider
---

# Runway

OpenClaw est livré avec un fournisseur `runway` intégré pour la génération vidéo hébergée.

- Fournisseur : `runway`
- Authentification : `RUNWAYML_API_SECRET` (canonique ; `RUNWAY_API_KEY` fonctionne aussi)
- API : API de génération vidéo basée sur les tâches Runway

## Démarrage rapide

1. Définissez la clé API :

```bash
openclaw onboard --auth-choice runway-api-key
```

2. Définissez un modèle vidéo par défaut :

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "runway/gen4.5",
      },
    },
  },
}
```

## Génération vidéo

Le fournisseur de génération vidéo `runway` intégré utilise par défaut `runway/gen4.5`.

- Modes : texte vers vidéo, image unique vers vidéo, et vidéo unique vers vidéo
- Exécution : soumission de tâche asynchrone + interrogation via `GET /v1/tasks/{id}`
- Sessions d'agent : `video_generate` démarre une tâche en arrière-plan, et les appels ultérieurs dans la même session retournent désormais le statut de la tâche active au lieu de générer une exécution en double
- Recherche de statut : `video_generate action=status`
- Références d'image/vidéo locales : supportées via les URI de données
- Limitation actuelle vidéo vers vidéo : OpenClaw nécessite actuellement `runway/gen4_aleph` pour les entrées vidéo
- Limitation actuelle texte vers vidéo : OpenClaw expose actuellement `16:9` et `9:16` pour les exécutions texte uniquement

Pour utiliser Runway comme fournisseur vidéo par défaut :

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "runway/gen4.5",
      },
    },
  },
}
```

## Connexes

- [Video Generation](/fr/tools/video-generation)
- [Configuration Reference](/fr/gateway/configuration-reference#agent-defaults)
