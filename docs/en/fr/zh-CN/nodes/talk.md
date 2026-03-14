---
read_when:
  - 在 macOS/iOS/Android 上实现 Talk 模式
  - 更改语音/TTS/中断行为
summary: Talk 模式：使用 ElevenLabs TTS 进行连续语音对话
title: Talk 模式
x-i18n:
  generated_at: "2026-02-03T10:07:59Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: ecbc3701c9e9502970cf13227fedbc9714d13668d8f4f3988fef2a4d68116a42
  source_path: nodes/talk.md
  workflow: 15
---

# Mode Talk

Le mode Talk est une boucle de conversation vocale continue :

1. Écouter la parole
2. Envoyer le texte transcrit au modèle (session principale, chat.send)
3. Attendre la réponse
4. Lire via ElevenLabs (diffusion en continu)

## Comportement (macOS)

- Affiche une **fenêtre flottante persistante** lorsque le mode Talk est activé.
- Transitions de phase **Écoute → Réflexion → Lecture**.
- Après une **brève pause** (fenêtre silencieuse), le texte transcrit actuel est envoyé.
- Les réponses sont **écrites dans WebChat** (comme la dactylographie).
- **Interruption vocale** (activée par défaut) : si l'utilisateur commence à parler pendant que l'assistant lit, nous arrêtons la lecture et enregistrons l'horodatage d'interruption pour l'invite suivante.

## Instructions vocales dans les réponses

L'assistant peut ajouter un **JSON sur une seule ligne** avant la réponse pour contrôler la parole :

```json
{ "voice": "<voice-id>", "once": true }
```

Règles :

- S'applique uniquement à la première ligne non vide.
- Les clés inconnues sont ignorées.
- `once: true` s'applique uniquement à la réponse actuelle.
- Sans `once`, cette voix devient la nouvelle valeur par défaut du mode Talk.
- La ligne JSON est supprimée avant la lecture TTS.

Clés supportées :

- `voice` / `voice_id` / `voiceId`
- `model` / `model_id` / `modelId`
- `speed`, `rate` (WPM), `stability`, `similarity`, `style`, `speakerBoost`
- `seed`, `normalize`, `lang`, `output_format`, `latency_tier`
- `once`

## Configuration (`~/.openclaw/openclaw.json`)

```json5
{
  talk: {
    voiceId: "elevenlabs_voice_id",
    modelId: "eleven_v3",
    outputFormat: "mp3_44100_128",
    apiKey: "elevenlabs_api_key",
    interruptOnSpeech: true,
  },
}
```

Valeurs par défaut :

- `interruptOnSpeech` : true
- `voiceId` : revient à `ELEVENLABS_VOICE_ID` / `SAG_VOICE_ID` (ou utilise la première voix ElevenLabs lorsque la clé API est disponible)
- `modelId` : par défaut `eleven_v3` si non défini
- `apiKey` : revient à `ELEVENLABS_API_KEY` (ou profil shell Gateway si disponible)
- `outputFormat` : par défaut `pcm_44100` sur macOS/iOS, `pcm_24000` sur Android (définir `mp3_*` pour forcer la diffusion MP3)

## Interface macOS

- Basculement de la barre de menus : **Talk**
- Onglet Configuration : groupe **Talk Mode** (ID de voix + commutateur d'interruption)
- Fenêtre flottante :
  - **Écoute** : nuage pulsant avec le niveau du microphone
  - **Réflexion** : animation d'enfoncement
  - **Lecture** : anneaux de rayonnement
  - Cliquer sur le nuage : arrêter la lecture
  - Cliquer sur X : quitter le mode Talk

## Remarques

- Nécessite les permissions de parole + microphone.
- Utilise `chat.send` pour la clé de session `main`.
- TTS utilise l'API de diffusion ElevenLabs avec `ELEVENLABS_API_KEY` et lit de manière incrémentale sur macOS/iOS/Android pour réduire la latence.
- Pour `eleven_v3`, `stability` est validé comme `0.0`, `0.5` ou `1.0` ; les autres modèles acceptent `0..1`.
- `latency_tier` est validé comme `0..4` lors de la configuration.
- Android supporte les formats de sortie `pcm_16000`, `pcm_22050`, `pcm_24000` et `pcm_44100` pour la diffusion AudioTrack à faible latence.
