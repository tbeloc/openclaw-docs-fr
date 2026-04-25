---
summary: "SenseAudio conversion par lot de la parole en texte pour les notes vocales entrantes"
read_when:
  - You want SenseAudio speech-to-text for audio attachments
  - You need the SenseAudio API key env var or audio config path
title: "SenseAudio"
---

# SenseAudio

SenseAudio peut transcrire les pièces jointes audio/notes vocales entrantes via
le pipeline partagé `tools.media.audio` d'OpenClaw. OpenClaw envoie du contenu
audio multipart au point de terminaison de transcription compatible OpenAI et
injecte le texte retourné en tant que `{{Transcript}}` plus un bloc `[Audio]`.

| Détail        | Valeur                                           |
| ------------- | ------------------------------------------------ |
| Site web      | [senseaudio.cn](https://senseaudio.cn)           |
| Documentation | [senseaudio.cn/docs](https://senseaudio.cn/docs) |
| Authentification | `SENSEAUDIO_API_KEY`                          |
| Modèle par défaut | `senseaudio-asr-pro-1.5-260319`              |
| URL par défaut | `https://api.senseaudio.cn/v1`                   |

## Démarrage

<Steps>
  <Step title="Définissez votre clé API">
    ```bash
    export SENSEAUDIO_API_KEY="..."
    ```
  </Step>
  <Step title="Activez le fournisseur audio">
    ```json5
    {
      tools: {
        media: {
          audio: {
            enabled: true,
            models: [{ provider: "senseaudio", model: "senseaudio-asr-pro-1.5-260319" }],
          },
        },
      },
    }
    ```
  </Step>
  <Step title="Envoyez une note vocale">
    Envoyez un message audio via n'importe quel canal connecté. OpenClaw télécharge
    l'audio vers SenseAudio et utilise la transcription dans le pipeline de réponse.
  </Step>
</Steps>

## Options

| Option     | Chemin                                | Description                         |
| ---------- | ------------------------------------- | ----------------------------------- |
| `model`    | `tools.media.audio.models[].model`    | ID du modèle ASR SenseAudio         |
| `language` | `tools.media.audio.models[].language` | Indice de langue optionnel          |
| `prompt`   | `tools.media.audio.prompt`            | Invite de transcription optionnelle |
| `baseUrl`  | `tools.media.audio.baseUrl` ou modèle | Remplacer la base compatible OpenAI |
| `headers`  | `tools.media.audio.request.headers`   | En-têtes de requête supplémentaires |

<Note>
SenseAudio est uniquement STT par lot dans OpenClaw. La transcription en temps
réel des appels vocaux continue d'utiliser des fournisseurs avec support STT
en continu.
</Note>
