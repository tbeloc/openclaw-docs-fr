---
summary: "Configuration de la génération vidéo PixVerse dans OpenClaw"
title: "PixVerse"
read_when:
  - You want to use PixVerse video generation in OpenClaw
  - You need the PixVerse API key/env setup
  - You want to make PixVerse the default video provider
---

OpenClaw fournit `pixverse` comme plugin externe officiel pour la génération vidéo PixVerse hébergée. Le plugin enregistre le fournisseur `pixverse` par rapport au contrat `videoGenerationProviders`.

| Property           | Value                                                                |
| ------------------ | -------------------------------------------------------------------- |
| Provider id        | `pixverse`                                                           |
| Plugin package     | `@openclaw/pixverse-provider`                                        |
| Auth env var       | `PIXVERSE_API_KEY`                                                   |
| Onboarding flag    | `--auth-choice pixverse-api-key`                                     |
| Direct CLI flag    | `--pixverse-api-key <key>`                                           |
| API                | PixVerse Platform API v2 (`video_id` submission plus result polling) |
| Default model      | `pixverse/v6`                                                        |
| Default API region | International                                                        |

## Commencer

<Steps>
  <Step title="Installer le plugin">
    ```bash
    openclaw plugins install @openclaw/pixverse-provider
    openclaw gateway restart
    ```
  </Step>
  <Step title="Définir la clé API">
    ```bash
    openclaw onboard --auth-choice pixverse-api-key
    ```

    L'assistant demande s'il faut utiliser le point de terminaison International
    (`https://app-api.pixverse.ai/openapi/v2`) ou le point de terminaison CN
    (`https://app-api.pixverseai.cn/openapi/v2`) avant d'écrire `region` et
    `baseUrl` dans la configuration du fournisseur.

  </Step>
  <Step title="Définir PixVerse comme fournisseur vidéo par défaut">
    ```bash
    openclaw config set agents.defaults.videoGenerationModel.primary "pixverse/v6"
    ```
  </Step>
  <Step title="Générer une vidéo">
    Demandez à l'agent de générer une vidéo. PixVerse sera utilisé automatiquement.
  </Step>
</Steps>

## Modes et modèles pris en charge

Le fournisseur expose les modèles de génération PixVerse via l'outil vidéo partagé d'OpenClaw.

| Mode           | Models               | Reference input         |
| -------------- | -------------------- | ----------------------- |
| Text-to-video  | `v6` (default), `c1` | None                    |
| Image-to-video | `v6` (default), `c1` | 1 local or remote image |

Les références d'images locales sont téléchargées vers PixVerse avant la demande image-to-video. Les URL d'images distantes sont transmises via le point de terminaison de téléchargement d'images PixVerse en tant que `image_url`.

| Option          | Supported values                                                            |
| --------------- | --------------------------------------------------------------------------- |
| Duration        | 1-15 seconds                                                                |
| Resolution      | `360P`, `540P`, `720P`, `1080P`                                             |
| Aspect ratio    | `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, `2:3`, `3:2`, `21:9` for text-to-video |
| Generated audio | `audio: true`                                                               |

<Note>
La génération de modèle d'image PixVerse n'est pas encore exposée via `image_generate`. Cette API est pilotée par template-id, tandis que le contrat de génération d'images partagées d'OpenClaw n'a pas actuellement d'option de sac typée spécifique à PixVerse.
</Note>

## Options du fournisseur

Le fournisseur vidéo accepte ces clés optionnelles spécifiques au fournisseur :

| Option                               | Type   | Effect                            |
| ------------------------------------ | ------ | --------------------------------- |
| `seed`                               | number | Deterministic seed when supported |
| `negativePrompt` / `negative_prompt` | string | Negative prompt                   |
| `quality`                            | string | PixVerse quality such as `720p`   |
| `motionMode` / `motion_mode`         | string | Image-to-video motion mode        |
| `cameraMovement` / `camera_movement` | string | PixVerse camera movement preset   |
| `templateId` / `template_id`         | number | Activated PixVerse template id    |

## Configuration

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "pixverse/v6",
      },
    },
  },
}
```

## Configuration avancée

<AccordionGroup>
  <Accordion title="Région API">
    OpenClaw utilise par défaut l'API PixVerse internationale. Définissez `models.providers.pixverse.region`
    manuellement lorsque votre clé appartient à une région de plateforme PixVerse spécifique, ou utilisez
    `openclaw onboard --auth-choice pixverse-api-key` pour en choisir une dans l'assistant de configuration :

    | Region value    | PixVerse API base URL                         |
    | --------------- | --------------------------------------------- |
    | `international` | `https://app-api.pixverse.ai/openapi/v2`      |
    | `cn`            | `https://app-api.pixverseai.cn/openapi/v2`    |

    ```json5
    {
      models: {
        providers: {
          pixverse: {
            region: "cn", // "international" or "cn"
            baseUrl: "https://app-api.pixverseai.cn/openapi/v2",
            models: [],
          },
        },
      },
    }
    ```

  </Accordion>

  <Accordion title="URL de base personnalisée">
    Définissez `models.providers.pixverse.baseUrl` uniquement lors du routage via un proxy compatible de confiance.
    `baseUrl` a la priorité sur `region`.

    ```json5
    {
      models: {
        providers: {
          pixverse: {
            baseUrl: "https://app-api.pixverse.ai/openapi/v2",
          },
        },
      },
    }
    ```

  </Accordion>

  <Accordion title="Interrogation des tâches">
    PixVerse retourne un `video_id` de la demande de génération. OpenClaw interroge
    `/openapi/v2/video/result/{video_id}` jusqu'à ce que la tâche réussisse, échoue,
    ou expire.
  </Accordion>
</AccordionGroup>

## Connexes

<CardGroup cols={2}>
  <Card title="Video generation" href="/fr/tools/video-generation" icon="video">
    Shared tool parameters, provider selection, and async behavior.
  </Card>
  <Card title="Configuration reference" href="/fr/gateway/config-agents#agent-defaults" icon="gear">
    Agent default settings including video generation model.
  </Card>
</CardGroup>
