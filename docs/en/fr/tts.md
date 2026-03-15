---
summary: "Synthèse vocale (TTS) pour les réponses sortantes"
read_when:
  - Enabling text-to-speech for replies
  - Configuring TTS providers or limits
  - Using /tts commands
title: "Synthèse vocale"
---

# Synthèse vocale (TTS)

OpenClaw peut convertir les réponses sortantes en audio en utilisant ElevenLabs, OpenAI ou Edge TTS.
Cela fonctionne partout où OpenClaw peut envoyer de l'audio ; Telegram reçoit une bulle de note vocale arrondie.

## Services supportés

- **ElevenLabs** (fournisseur principal ou de secours)
- **OpenAI** (fournisseur principal ou de secours ; également utilisé pour les résumés)
- **Edge TTS** (fournisseur principal ou de secours ; utilise `node-edge-tts`, par défaut quand aucune clé API)

### Notes sur Edge TTS

Edge TTS utilise le service de synthèse vocale neuronale en ligne de Microsoft Edge via la
bibliothèque `node-edge-tts`. C'est un service hébergé (pas local), utilise les points de terminaison de Microsoft, et
ne nécessite pas de clé API. `node-edge-tts` expose les options de configuration vocale et
les formats de sortie, mais pas toutes les options sont supportées par le service Edge. citeturn2search0

Comme Edge TTS est un service web public sans SLA ou quota publié, traitez-le
comme un service au mieux. Si vous avez besoin de limites garanties et d'assistance, utilisez OpenAI ou ElevenLabs.
L'API REST Speech de Microsoft documente une limite de 10 minutes d'audio par requête ; Edge TTS
ne publie pas de limites, donc supposez des limites similaires ou inférieures. citeturn0search3

## Clés optionnelles

Si vous voulez OpenAI ou ElevenLabs :

- `ELEVENLABS_API_KEY` (ou `XI_API_KEY`)
- `OPENAI_API_KEY`

Edge TTS ne **nécessite pas** de clé API. Si aucune clé API n'est trouvée, OpenClaw utilise par défaut
Edge TTS (sauf s'il est désactivé via `messages.tts.edge.enabled=false`).

Si plusieurs fournisseurs sont configurés, le fournisseur sélectionné est utilisé en premier et les autres sont des options de secours.
Le résumé automatique utilise le `summaryModel` configuré (ou `agents.defaults.model.primary`),
donc ce fournisseur doit également être authentifié si vous activez les résumés.

## Liens de service

- [Guide OpenAI Text-to-Speech](https://platform.openai.com/docs/guides/text-to-speech)
- [Référence API OpenAI Audio](https://platform.openai.com/docs/api-reference/audio)
- [ElevenLabs Text to Speech](https://elevenlabs.io/docs/api-reference/text-to-speech)
- [Authentification ElevenLabs](https://elevenlabs.io/docs/api-reference/authentication)
- [node-edge-tts](https://github.com/SchneeHertz/node-edge-tts)
- [Formats de sortie Microsoft Speech](https://learn.microsoft.com/azure/ai-services/speech-service/rest-text-to-speech#audio-outputs)

## Est-ce activé par défaut ?

Non. La TTS automatique est **désactivée** par défaut. Activez-la dans la config avec
`messages.tts.auto` ou par session avec `/tts always` (alias : `/tts on`).

Edge TTS **est** activé par défaut une fois que TTS est activé, et est utilisé automatiquement
quand aucune clé API OpenAI ou ElevenLabs n'est disponible.

## Config

La config TTS se trouve sous `messages.tts` dans `openclaw.json`.
Le schéma complet est dans [Configuration de la passerelle](/fr/gateway/configuration).

### Config minimale (activation + fournisseur)

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "elevenlabs",
    },
  },
}
```

### OpenAI principal avec ElevenLabs en secours

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "openai",
      summaryModel: "openai/gpt-4.1-mini",
      modelOverrides: {
        enabled: true,
      },
      openai: {
        apiKey: "openai_api_key",
        baseUrl: "https://api.openai.com/v1",
        model: "gpt-4o-mini-tts",
        voice: "alloy",
      },
      elevenlabs: {
        apiKey: "elevenlabs_api_key",
        baseUrl: "https://api.elevenlabs.io",
        voiceId: "voice_id",
        modelId: "eleven_multilingual_v2",
        seed: 42,
        applyTextNormalization: "auto",
        languageCode: "en",
        voiceSettings: {
          stability: 0.5,
          similarityBoost: 0.75,
          style: 0.0,
          useSpeakerBoost: true,
          speed: 1.0,
        },
      },
    },
  },
}
```

### Edge TTS principal (pas de clé API)

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "edge",
      edge: {
        enabled: true,
        voice: "en-US-MichelleNeural",
        lang: "en-US",
        outputFormat: "audio-24khz-48kbitrate-mono-mp3",
        rate: "+10%",
        pitch: "-5%",
      },
    },
  },
}
```

### Désactiver Edge TTS

```json5
{
  messages: {
    tts: {
      edge: {
        enabled: false,
      },
    },
  },
}
```

### Limites personnalisées + chemin des préférences

```json5
{
  messages: {
    tts: {
      auto: "always",
      maxTextLength: 4000,
      timeoutMs: 30000,
      prefsPath: "~/.openclaw/settings/tts.json",
    },
  },
}
```

### Répondre avec audio uniquement après une note vocale entrante

```json5
{
  messages: {
    tts: {
      auto: "inbound",
    },
  },
}
```

### Désactiver le résumé automatique pour les réponses longues

```json5
{
  messages: {
    tts: {
      auto: "always",
    },
  },
}
```

Puis exécutez :

```
/tts summary off
```

### Notes sur les champs

- `auto`: mode TTS automatique (`off`, `always`, `inbound`, `tagged`).
  - `inbound` envoie uniquement l'audio après une note vocale entrante.
  - `tagged` envoie uniquement l'audio quand la réponse inclut des balises `[[tts]]`.
- `enabled`: bascule héritée (le docteur migre ceci vers `auto`).
- `mode`: `"final"` (par défaut) ou `"all"` (inclut les réponses d'outil/bloc).
- `provider`: `"elevenlabs"`, `"openai"`, ou `"edge"` (le secours est automatique).
- Si `provider` est **non défini**, OpenClaw préfère `openai` (si clé), puis `elevenlabs` (si clé),
  sinon `edge`.
- `summaryModel`: modèle bon marché optionnel pour le résumé automatique ; par défaut `agents.defaults.model.primary`.
  - Accepte `provider/model` ou un alias de modèle configuré.
- `modelOverrides`: permettre au modèle d'émettre des directives TTS (activé par défaut).
  - `allowProvider` par défaut à `false` (le changement de fournisseur est opt-in).
- `maxTextLength`: limite stricte pour l'entrée TTS (caractères). `/tts audio` échoue si dépassée.
- `timeoutMs`: délai d'expiration de la requête (ms).
- `prefsPath`: remplacer le chemin JSON des préférences locales (fournisseur/limite/résumé).
- Les valeurs `apiKey` se replient sur les variables d'environnement (`ELEVENLABS_API_KEY`/`XI_API_KEY`, `OPENAI_API_KEY`).
- `elevenlabs.baseUrl`: remplacer l'URL de base de l'API ElevenLabs.
- `openai.baseUrl`: remplacer le point de terminaison OpenAI TTS.
  - Ordre de résolution : `messages.tts.openai.baseUrl` -> `OPENAI_TTS_BASE_URL` -> `https://api.openai.com/v1`
  - Les valeurs non par défaut sont traitées comme des points de terminaison TTS compatibles OpenAI, donc les noms de modèle et de voix personnalisés sont acceptés.
- `elevenlabs.voiceSettings`:
  - `stability`, `similarityBoost`, `style`: `0..1`
  - `useSpeakerBoost`: `true|false`
  - `speed`: `0.5..2.0` (1.0 = normal)
- `elevenlabs.applyTextNormalization`: `auto|on|off`
- `elevenlabs.languageCode`: ISO 639-1 à 2 lettres (par ex. `en`, `de`)
- `elevenlabs.seed`: entier `0..4294967295` (déterminisme au mieux)
- `edge.enabled`: autoriser l'utilisation d'Edge TTS (par défaut `true` ; pas de clé API).
- `edge.voice`: nom de voix neuronale Edge (par ex. `en-US-MichelleNeural`).
- `edge.lang`: code de langue (par ex. `en-US`).
- `edge.outputFormat`: format de sortie Edge (par ex. `audio-24khz-48kbitrate-mono-mp3`).
  - Voir les formats de sortie Microsoft Speech pour les valeurs valides ; pas tous les formats sont supportés par Edge.
- `edge.rate` / `edge.pitch` / `edge.volume`: chaînes de pourcentage (par ex. `+10%`, `-5%`).
- `edge.saveSubtitles`: écrire les sous-titres JSON à côté du fichier audio.
- `edge.proxy`: URL du proxy pour les requêtes Edge TTS.
- `edge.timeoutMs`: remplacement du délai d'expiration de la requête (ms).

## Remplacements pilotés par le modèle (activé par défaut)

Par défaut, le modèle **peut** émettre des directives TTS pour une seule réponse.
Quand `messages.tts.auto` est `tagged`, ces directives sont requises pour déclencher l'audio.

Quand activé, le modèle peut émettre des directives `[[tts:...]]` pour remplacer la voix
pour une seule réponse, plus un bloc optionnel `[[tts:text]]...[[/tts:text]]` pour
fournir des balises expressives (rires, indices de chant, etc) qui ne doivent apparaître que dans
l'audio.

Les directives `provider=...` sont ignorées sauf si `modelOverrides.allowProvider: true`.

Exemple de charge utile de réponse :

```
Here you go.

[[tts:voiceId=pMsXgVXv3BLzUgSXRplE model=eleven_v3 speed=1.1]]
[[tts:text]](laughs) Read the song once more.[[/tts:text]]
```

Clés de directive disponibles (quand activé) :

- `provider` (`openai` | `elevenlabs` | `edge`, nécessite `allowProvider: true`)
- `voice` (voix OpenAI) ou `voiceId` (ElevenLabs)
- `model` (modèle OpenAI TTS ou ID de modèle ElevenLabs)
- `stability`, `similarityBoost`, `style`, `speed`, `useSpeakerBoost`
- `applyTextNormalization` (`auto|on|off`)
- `languageCode` (ISO 639-1)
- `seed`

Désactiver tous les remplacements de modèle :

```json5
{
  messages: {
    tts: {
      modelOverrides: {
        enabled: false,
      },
    },
  },
}
```

Liste blanche optionnelle (activer le changement de fournisseur tout en gardant les autres paramètres configurables) :

```json5
{
  messages: {
    tts: {
      modelOverrides: {
        enabled: true,
        allowProvider: true,
        allowSeed: false,
      },
    },
  },
}
```

## Préférences par utilisateur

Les commandes slash écrivent les remplacements locaux dans `prefsPath` (par défaut :
`~/.openclaw/settings/tts.json`, remplacer avec `OPENCLAW_TTS_PREFS` ou
`messages.tts.prefsPath`).

Champs stockés :

- `enabled`
- `provider`
- `maxLength` (seuil de résumé ; par défaut 1500 caractères)
- `summarize` (par défaut `true`)

Ceux-ci remplacent `messages.tts.*` pour cet hôte.

## Formats de sortie (fixes)

- **Telegram**: Note vocale Opus (`opus_48000_64` d'ElevenLabs, `opus` d'OpenAI).
  - 48kHz / 64kbps est un bon compromis pour les notes vocales et requis pour la bulle arrondie.
- **Autres canaux**: MP3 (`mp3_44100_128` d'ElevenLabs, `mp3` d'OpenAI).
  - 44.1kHz / 128kbps est l'équilibre par défaut pour la clarté vocale.
- **Edge TTS**: utilise `edge.outputFormat` (par défaut `audio-24khz-48kbitrate-mono-mp3`).
  - `node-edge-tts` accepte un `outputFormat`, mais pas tous les formats sont disponibles
    depuis le service Edge. citeturn2search0
  - Les valeurs de format de sortie suivent les formats de sortie Microsoft Speech (y compris Ogg/WebM Opus). citeturn1search0
  - Telegram `sendVoice` accepte OGG/MP3/M4A ; utilisez OpenAI/ElevenLabs si vous avez besoin
    de notes vocales Opus garanties. citeturn1search1
  - Si le format de sortie Edge configuré échoue, OpenClaw réessaie avec MP3.

Les formats OpenAI/ElevenLabs sont fixes ; Telegram s'attend à Opus pour l'UX des notes vocales.

## Comportement de la TTS automatique

Quand activée, OpenClaw :

- ignore la TTS si la réponse contient déjà des médias ou une directive `MEDIA:`.
- ignore les réponses très courtes (< 10 caractères).
- résume les réponses longues quand activé en utilisant `agents.defaults.model.primary` (ou `summaryModel`).
- attache l'audio généré à la réponse.

Si la réponse dépasse `maxLength` et que le résumé est désactivé (ou pas de clé API pour le
modèle de résumé), l'audio
est ignoré et la réponse textuelle normale est envoyée.

## Diagramme de flux

```
Reply -> TTS enabled?
  no  -> send text
  yes -> has media / MEDIA: / short?
          yes -> send text
          no  -> length > limit?
                   no  -> TTS -> attach audio
                   yes -> summary enabled?
                            no  -> send text
                            yes -> summarize (summaryModel or agents.defaults.model.primary)
                                      -> TTS -> attach audio
```

## Utilisation des commandes slash

Il y a une seule commande : `/tts`.
Voir [Commandes slash](/fr/tools/slash-commands) pour les détails d'activation.

Note Discord : `/tts` est une commande Discord intégrée, donc OpenClaw enregistre
`/voice` comme commande native là-bas. Le texte `/tts ...` fonctionne toujours.

```
/tts off
/tts always
/tts inbound
/tts tagged
/tts status
/tts provider openai
/tts limit 2000
/tts summary off
/tts audio Hello from OpenClaw
```

Notes :

- Les commandes nécessitent un expéditeur autorisé (les règles de liste blanche/propriétaire s'appliquent toujours).
- `commands.text` ou l'enregistrement de commande native doit être activé.
- `off|always|inbound|tagged` sont des bascules par session (`/tts on` est un alias pour `/tts always`).
- `limit` et `summary` sont stockés dans les préférences locales, pas dans la config principale.
- `/tts audio` génère une réponse audio unique (ne bascule pas la TTS).

## Outil d'agent

L'outil `tts` convertit le texte en parole et retourne un chemin `MEDIA:`. Quand le
résultat est compatible Telegram, l'outil inclut `[[audio_as_voice]]` donc
Telegram envoie une bulle vocale.

## Gateway RPC

Méthodes Gateway :

- `tts.status`
- `tts.enable`
- `tts.disable`
- `tts.convert`
- `tts.setProvider`
- `tts.providers`
