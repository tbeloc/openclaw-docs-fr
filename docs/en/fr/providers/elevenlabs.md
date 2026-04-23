---
summary: "Utilisez la synthèse vocale ElevenLabs, Scribe STT et la transcription en temps réel avec OpenClaw"
read_when:
  - You want ElevenLabs text-to-speech in OpenClaw
  - You want ElevenLabs Scribe speech-to-text for audio attachments
  - You want ElevenLabs realtime transcription for Voice Call
title: "ElevenLabs"
---

# ElevenLabs

OpenClaw utilise ElevenLabs pour la synthèse vocale, la reconnaissance vocale par lot avec Scribe v2, et la transcription STT en continu pour Voice Call avec Scribe v2 Realtime.

| Capacité                 | Surface OpenClaw                             | Par défaut               |
| ------------------------ | --------------------------------------------- | ------------------------ |
| Synthèse vocale          | `messages.tts` / `talk`                       | `eleven_multilingual_v2` |
| Reconnaissance vocale par lot | `tools.media.audio`                           | `scribe_v2`              |
| Reconnaissance vocale en continu | Voice Call `streaming.provider: "elevenlabs"` | `scribe_v2_realtime`     |

## Authentification

Définissez `ELEVENLABS_API_KEY` dans l'environnement. `XI_API_KEY` est également accepté pour la compatibilité avec les outils ElevenLabs existants.

```bash
export ELEVENLABS_API_KEY="..."
```

## Synthèse vocale

```json5
{
  messages: {
    tts: {
      providers: {
        elevenlabs: {
          apiKey: "${ELEVENLABS_API_KEY}",
          voiceId: "pMsXgVXv3BLzUgSXRplE",
          modelId: "eleven_multilingual_v2",
        },
      },
    },
  },
}
```

## Reconnaissance vocale

Utilisez Scribe v2 pour les pièces jointes audio entrantes et les courts segments vocaux enregistrés :

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "elevenlabs", model: "scribe_v2" }],
      },
    },
  },
}
```

OpenClaw envoie l'audio multipart à ElevenLabs `/v1/speech-to-text` avec `model_id: "scribe_v2"`. Les indices de langue sont mappés à `language_code` le cas échéant.

## Transcription STT en continu pour Voice Call

Le plugin `elevenlabs` fourni enregistre Scribe v2 Realtime pour la transcription en continu de Voice Call.

| Paramètre       | Chemin de configuration                                                   | Par défaut                                        |
| --------------- | ------------------------------------------------------------------------- | ------------------------------------------------- |
| Clé API         | `plugins.entries.voice-call.config.streaming.providers.elevenlabs.apiKey` | Revient à `ELEVENLABS_API_KEY` / `XI_API_KEY`    |
| Modèle          | `...elevenlabs.modelId`                                                   | `scribe_v2_realtime`                              |
| Format audio    | `...elevenlabs.audioFormat`                                               | `ulaw_8000`                                       |
| Fréquence d'échantillonnage | `...elevenlabs.sampleRate`                                                | `8000`                                            |
| Stratégie de validation | `...elevenlabs.commitStrategy`                                            | `vad`                                             |
| Langue          | `...elevenlabs.languageCode`                                              | (non défini)                                      |

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          streaming: {
            enabled: true,
            provider: "elevenlabs",
            providers: {
              elevenlabs: {
                apiKey: "${ELEVENLABS_API_KEY}",
                audioFormat: "ulaw_8000",
                commitStrategy: "vad",
                languageCode: "en",
              },
            },
          },
        },
      },
    },
  },
}
```

<Note>
Voice Call reçoit les médias Twilio à 8 kHz G.711 u-law. Le fournisseur en temps réel ElevenLabs utilise par défaut `ulaw_8000`, les trames téléphoniques peuvent donc être transférées sans transcodage.
</Note>
