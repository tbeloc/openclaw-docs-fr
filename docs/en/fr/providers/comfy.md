---
title: "ComfyUI"
summary: "Configuration de génération d'images, vidéos et musique avec flux ComfyUI dans OpenClaw"
read_when:
  - You want to use local ComfyUI workflows with OpenClaw
  - You want to use Comfy Cloud with image, video, or music workflows
  - You need the bundled comfy plugin config keys
---

# ComfyUI

OpenClaw est livré avec un plugin `comfy` intégré pour les exécutions ComfyUI pilotées par flux.

- Provider: `comfy`
- Models: `comfy/workflow`
- Shared surfaces: `image_generate`, `video_generate`, `music_generate`
- Auth: aucune pour ComfyUI local; `COMFY_API_KEY` ou `COMFY_CLOUD_API_KEY` pour Comfy Cloud
- API: ComfyUI `/prompt` / `/history` / `/view` et Comfy Cloud `/api/*`

## Ce qu'il supporte

- Génération d'images à partir d'un flux JSON
- Édition d'images avec 1 image de référence téléchargée
- Génération de vidéos à partir d'un flux JSON
- Génération de vidéos avec 1 image de référence téléchargée
- Génération de musique ou audio via l'outil partagé `music_generate`
- Téléchargement de sortie à partir d'un nœud configuré ou de tous les nœuds de sortie correspondants

Le plugin intégré est piloté par flux, donc OpenClaw ne tente pas de mapper les
contrôles génériques `size`, `aspectRatio`, `resolution`, `durationSeconds` ou
de style TTS sur votre graphique.

## Disposition de la configuration

Comfy supporte les paramètres de connexion partagés au niveau supérieur plus les
sections de flux par capacité:

```json5
{
  models: {
    providers: {
      comfy: {
        mode: "local",
        baseUrl: "http://127.0.0.1:8188",
        image: {
          workflowPath: "./workflows/flux-api.json",
          promptNodeId: "6",
          outputNodeId: "9",
        },
        video: {
          workflowPath: "./workflows/video-api.json",
          promptNodeId: "12",
          outputNodeId: "21",
        },
        music: {
          workflowPath: "./workflows/music-api.json",
          promptNodeId: "3",
          outputNodeId: "18",
        },
      },
    },
  },
}
```

Clés partagées:

- `mode`: `local` ou `cloud`
- `baseUrl`: par défaut `http://127.0.0.1:8188` pour local ou `https://cloud.comfy.org` pour cloud
- `apiKey`: alternative de clé en ligne optionnelle aux variables d'environnement
- `allowPrivateNetwork`: autoriser une `baseUrl` privée/LAN en mode cloud

Clés par capacité sous `image`, `video` ou `music`:

- `workflow` ou `workflowPath`: requis
- `promptNodeId`: requis
- `promptInputName`: par défaut `text`
- `outputNodeId`: optionnel
- `pollIntervalMs`: optionnel
- `timeoutMs`: optionnel

Les sections image et vidéo supportent également:

- `inputImageNodeId`: requis quand vous passez une image de référence
- `inputImageInputName`: par défaut `image`

## Compatibilité rétroactive

La configuration d'image au niveau supérieur existante fonctionne toujours:

```json5
{
  models: {
    providers: {
      comfy: {
        workflowPath: "./workflows/flux-api.json",
        promptNodeId: "6",
        outputNodeId: "9",
      },
    },
  },
}
```

OpenClaw traite cette forme héritée comme la configuration du flux d'image.

## Flux d'image

Définissez le modèle d'image par défaut:

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "comfy/workflow",
      },
    },
  },
}
```

Exemple d'édition avec image de référence:

```json5
{
  models: {
    providers: {
      comfy: {
        image: {
          workflowPath: "./workflows/edit-api.json",
          promptNodeId: "6",
          inputImageNodeId: "7",
          inputImageInputName: "image",
          outputNodeId: "9",
        },
      },
    },
  },
}
```

## Flux vidéo

Définissez le modèle vidéo par défaut:

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "comfy/workflow",
      },
    },
  },
}
```

Les flux vidéo Comfy supportent actuellement la conversion texte-vers-vidéo et
image-vers-vidéo via le graphique configuré. OpenClaw ne transmet pas les vidéos
d'entrée aux flux ComfyUI.

## Flux musicaux

Le plugin intégré enregistre un fournisseur de génération musicale pour les
sorties audio ou musicales définies par flux, exposées via l'outil partagé
`music_generate`:

```text
/tool music_generate prompt="Warm ambient synth loop with soft tape texture"
```

Utilisez la section de configuration `music` pour pointer vers votre flux JSON
audio et nœud de sortie.

## Comfy Cloud

Utilisez `mode: "cloud"` plus l'un de:

- `COMFY_API_KEY`
- `COMFY_CLOUD_API_KEY`
- `models.providers.comfy.apiKey`

Le mode cloud utilise toujours les mêmes sections de flux `image`, `video` et
`music`.

## Tests en direct

Une couverture en direct optionnelle existe pour le plugin intégré:

```bash
OPENCLAW_LIVE_TEST=1 COMFY_LIVE_TEST=1 pnpm test:live -- extensions/comfy/comfy.live.test.ts
```

Le test en direct ignore les cas d'image, vidéo ou musique individuels sauf si
la section de flux Comfy correspondante est configurée.

## Connexes

- [Image Generation](/fr/tools/image-generation)
- [Video Generation](/fr/tools/video-generation)
- [Music Generation](/fr/tools/music-generation)
- [Provider Directory](/fr/providers/index)
- [Configuration Reference](/fr/gateway/configuration-reference#agent-defaults)
