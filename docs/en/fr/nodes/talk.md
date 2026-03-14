---
summary: "Mode Talk : conversations vocales continues avec TTS ElevenLabs"
read_when:
  - Implementing Talk mode on macOS/iOS/Android
  - Changing voice/TTS/interrupt behavior
title: "Mode Talk"
---

# Mode Talk

Le mode Talk est une boucle de conversation vocale continue :

1. Écouter la parole
2. Envoyer la transcription au modèle (session principale, chat.send)
3. Attendre la réponse
4. La prononcer via ElevenLabs (lecture en streaming)

## Comportement (macOS)

- **Superposition toujours active** pendant que le mode Talk est activé.
- **Écoute → Réflexion → Parole** transitions de phase.
- Sur une **courte pause** (fenêtre de silence), la transcription actuelle est envoyée.
- Les réponses sont **écrites dans WebChat** (comme lors de la saisie).
- **Interruption à la parole** (activée par défaut) : si l'utilisateur commence à parler pendant que l'assistant parle, nous arrêtons la lecture et notons l'horodatage de l'interruption pour l'invite suivante.

## Directives vocales dans les réponses

L'assistant peut préfixer sa réponse avec une **seule ligne JSON** pour contrôler la voix :

```json
{ "voice": "<voice-id>", "once": true }
```

Règles :

- Première ligne non vide uniquement.
- Les clés inconnues sont ignorées.
- `once: true` s'applique à la réponse actuelle uniquement.
- Sans `once`, la voix devient la nouvelle valeur par défaut pour le mode Talk.
- La ligne JSON est supprimée avant la lecture TTS.

Clés supportées :

- `voice` / `voice_id` / `voiceId`
- `model` / `model_id` / `modelId`
- `speed`, `rate` (WPM), `stability`, `similarity`, `style`, `speakerBoost`
- `seed`, `normalize`, `lang`, `output_format`, `latency_tier`
- `once`

## Config (`~/.openclaw/openclaw.json`)

```json5
{
  talk: {
    voiceId: "elevenlabs_voice_id",
    modelId: "eleven_v3",
    outputFormat: "mp3_44100_128",
    apiKey: "elevenlabs_api_key",
    silenceTimeoutMs: 1500,
    interruptOnSpeech: true,
  },
}
```

Valeurs par défaut :

- `interruptOnSpeech`: true
- `silenceTimeoutMs`: lorsque non défini, Talk conserve la fenêtre de pause par défaut de la plateforme avant d'envoyer la transcription (`700 ms sur macOS et Android, 900 ms sur iOS`)
- `voiceId`: revient à `ELEVENLABS_VOICE_ID` / `SAG_VOICE_ID` (ou première voix ElevenLabs quand la clé API est disponible)
- `modelId`: par défaut `eleven_v3` lorsque non défini
- `apiKey`: revient à `ELEVENLABS_API_KEY` (ou profil shell de passerelle si disponible)
- `outputFormat`: par défaut `pcm_44100` sur macOS/iOS et `pcm_24000` sur Android (définir `mp3_*` pour forcer le streaming MP3)

## Interface macOS

- Bascule de la barre de menu : **Talk**
- Onglet Config : groupe **Talk Mode** (ID de voix + bascule d'interruption)
- Superposition :
  - **Écoute** : le nuage pulse avec le niveau du micro
  - **Réflexion** : animation d'enfoncement
  - **Parole** : anneaux rayonnants
  - Cliquer sur le nuage : arrêter la parole
  - Cliquer sur X : quitter le mode Talk

## Notes

- Nécessite les permissions Speech + Microphone.
- Utilise `chat.send` contre la clé de session `main`.
- TTS utilise l'API de streaming ElevenLabs avec `ELEVENLABS_API_KEY` et lecture incrémentale sur macOS/iOS/Android pour une latence plus faible.
- `stability` pour `eleven_v3` est validé à `0.0`, `0.5`, ou `1.0` ; les autres modèles acceptent `0..1`.
- `latency_tier` est validé à `0..4` lorsqu'il est défini.
- Android supporte les formats de sortie `pcm_16000`, `pcm_22050`, `pcm_24000`, et `pcm_44100` pour le streaming AudioTrack à faible latence.
