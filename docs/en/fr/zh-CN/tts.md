---
read_when:
  - Activer la synthèse vocale pour les réponses
  - Configurer un fournisseur TTS ou des limites
  - Utiliser la commande /tts
summary: Synthèse vocale (TTS) pour les réponses sortantes
title: Synthèse vocale
x-i18n:
  generated_at: "2026-02-03T10:13:55Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 070ff0cc8592f64c6c9e4ddaddc7e8fba82f0692ceded6fe833ec9ba5b61e6fb
  source_path: tts.md
  workflow: 15
---

# Synthèse vocale (TTS)

OpenClaw peut convertir les réponses sortantes en audio à l'aide d'ElevenLabs, OpenAI ou Edge TTS. Cela fonctionne partout où OpenClaw peut envoyer de l'audio ; Telegram affiche une bulle de message vocal circulaire.

## Services supportés

- **ElevenLabs** (fournisseur principal ou secondaire)
- **OpenAI** (fournisseur principal ou secondaire ; également utilisé pour les résumés)
- **Edge TTS** (fournisseur principal ou secondaire ; utilise `node-edge-tts`, par défaut sans clé API)

### Remarques sur Edge TTS

Edge TTS utilise le service TTS neuronal en ligne de Microsoft Edge via la bibliothèque `node-edge-tts`. C'est un service hébergé (non local), utilisant les points de terminaison de Microsoft, et ne nécessite pas de clé API. `node-edge-tts` expose les options de configuration vocale et les formats de sortie, mais tous les formats ne sont pas supportés par le service Edge. citeturn2search0

Comme Edge TTS est un service Web public sans SLA ou quota publié, traitez-le comme un service au mieux. Si vous avez besoin de limites garanties et d'un support, utilisez OpenAI ou ElevenLabs. L'API REST Speech de Microsoft documente une limite de 10 minutes d'audio par requête ; Edge TTS n'a pas de limite publiée, supposez donc une limite similaire ou inférieure. citeturn0search3

## Clés optionnelles

Si vous souhaitez utiliser OpenAI ou ElevenLabs :

- `ELEVENLABS_API_KEY` (ou `XI_API_KEY`)
- `OPENAI_API_KEY`

Edge TTS **ne nécessite pas** de clé API. Si aucune clé API n'est trouvée, OpenClaw utilise par défaut Edge TTS (sauf si désactivé via `messages.tts.edge.enabled=false`).

Si plusieurs fournisseurs sont configurés, le fournisseur sélectionné est utilisé en premier, les autres comme options de secours. La synthèse automatique utilise le `summaryModel` configuré (ou `agents.defaults.model.primary`), donc si vous activez la synthèse, ce fournisseur doit également être authentifié.

## Liens des services

- [Guide OpenAI Text-to-Speech](https://platform.openai.com/docs/guides/text-to-speech)
- [Référence API Audio OpenAI](https://platform.openai.com/docs/api-reference/audio)
- [ElevenLabs Text-to-Speech](https://elevenlabs.io/docs/api-reference/text-to-speech)
- [Authentification ElevenLabs](https://elevenlabs.io/docs/api-reference/authentication)
- [node-edge-tts](https://github.com/SchneeHertz/node-edge-tts)
- [Formats de sortie vocale Microsoft](https://learn.microsoft.com/azure/ai-services/speech-service/rest-text-to-speech#audio-outputs)

## Activé par défaut ?

Non. Le TTS automatique est **désactivé** par défaut. Activez-le avec `messages.tts.auto` dans la configuration ou `/tts always` (alias : `/tts on`) par session.

Une fois le TTS activé, Edge TTS **est** activé par défaut et utilisé automatiquement en l'absence de clés API OpenAI ou ElevenLabs.

## Configuration

La configuration TTS se trouve sous `messages.tts` dans `openclaw.json`. Le schéma complet se trouve dans [Configuration de la passerelle](/gateway/configuration).

### Configuration minimale (activation + fournisseur)

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

### OpenAI principal, ElevenLabs secondaire

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

### Edge TTS principal (sans clé API)

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

### Répondre avec de l'audio uniquement après réception d'un message vocal

```json5
{
  messages: {
    tts: {
      auto: "inbound",
    },
  },
}
```

### Désactiver la synthèse automatique pour les réponses longues

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

### Description des champs

- `auto` : Mode TTS automatique (`off`, `always`, `inbound`, `tagged`).
  - `inbound` envoie de l'audio uniquement après réception d'un message vocal.
  - `tagged` envoie de l'audio uniquement si la réponse contient une balise `[[tts]]`.
- `enabled` : Ancien commutateur (doctor le migre vers `auto`).
- `mode` : `"final"` (par défaut) ou `"all"` (inclut les réponses d'outils/chunks).
- `provider` : `"elevenlabs"`, `"openai"` ou `"edge"` (secours automatique).
- Si `provider` **n'est pas défini**, OpenClaw préfère `openai` (s'il a une clé), puis `elevenlabs` (s'il a une clé), sinon `edge`.
- `summaryModel` : Modèle bon marché optionnel pour la synthèse automatique ; par défaut `agents.defaults.model.primary`.
  - Accepte `provider/model` ou un alias de modèle configuré.
- `modelOverrides` : Permet aux modèles d'émettre des instructions TTS (activé par défaut).
- `maxTextLength` : Limite stricte pour l'entrée TTS (caractères). `/tts audio` échoue si dépassé.
- `timeoutMs` : Délai d'expiration de la requête (millisecondes).
- `prefsPath` : Remplace le chemin JSON des préférences locales (fournisseur/limites/synthèse).
- Les valeurs `apiKey` se rabattent sur les variables d'environnement (`ELEVENLABS_API_KEY`/`XI_API_KEY`, `OPENAI_API_KEY`).
- `elevenlabs.baseUrl` : Remplace l'URL de base de l'API ElevenLabs.
- `elevenlabs.voiceSettings` :
  - `stability`, `similarityBoost`, `style` : `0..1`
  - `useSpeakerBoost` : `true|false`
  - `speed` : `0.5..2.0` (1.0 = normal)
- `elevenlabs.applyTextNormalization` : `auto|on|off`
- `elevenlabs.languageCode` : ISO 639-1 à 2 lettres (ex. `en`, `de`)
- `elevenlabs.seed` : Entier `0..4294967295` (déterministe au mieux)
- `edge.enabled` : Permet l'utilisation d'Edge TTS (par défaut `true` ; sans clé API).
- `edge.voice` : Nom de la voix neuronale Edge (ex. `en-US-MichelleNeural`).
- `edge.lang` : Code de langue (ex. `en-US`).
- `edge.outputFormat` : Format de sortie Edge (ex. `audio-24khz-48kbitrate-mono-mp3`).
  - Voir les formats de sortie vocale Microsoft pour les valeurs valides ; tous les formats ne sont pas supportés par Edge.
- `edge.rate` / `edge.pitch` / `edge.volume` : Chaînes de pourcentage (ex. `+10%`, `-5%`).
- `edge.saveSubtitles` : Écrit les sous-titres JSON à côté du fichier audio.
- `edge.proxy` : URL du proxy pour les requêtes Edge TTS.
- `edge.timeoutMs` : Remplacement du délai d'expiration de la requête (millisecondes).

## Remplacements pilotés par le modèle (activés par défaut)

Par défaut, les modèles **peuvent** émettre des instructions TTS pour les réponses individuelles. Lorsque `messages.tts.auto` est `tagged`, ces instructions sont nécessaires pour déclencher l'audio.

Lorsqu'activé, les modèles peuvent émettre des directives `[[tts:...]]` pour remplacer la voix pour une réponse individuelle, plus des blocs optionnels `[[tts:text]]...[[/tts:text]]` pour fournir des étiquettes expressives (rires, indices de chant, etc.) qui ne doivent apparaître que dans l'audio.

Exemple de charge de réponse :

```
Here you go.

[[tts:provider=elevenlabs voiceId=pMsXgVXv3BLzUgSXRplE model=eleven_v3 speed=1.1]]
[[tts:text]](laughs) Read the song once more.[[/tts:text]]
```

Clés d'instruction disponibles (lorsqu'activées) :

- `provider` (`openai` | `elevenlabs` | `edge`)
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

Liste blanche optionnelle (désactiver les remplacements spécifiques tout en gardant les balises activées) :

```json5
{
  messages: {
    tts: {
      modelOverrides: {
        enabled: true,
        allowProvider: false,
        allowSeed: false,
      },
    },
  },
}
```

## Préférences par utilisateur

Les commandes slash écrivent les remplacements locaux dans `prefsPath` (par défaut : `~/.openclaw/settings/tts.json`, remplaçable via `OPENCLAW_TTS_PREFS` ou `messages.tts.prefsPath`).

Champs stockés :

- `enabled`
- `provider`
- `maxLength` (seuil de synthèse ; par défaut 1500 caractères)
- `summarize` (par défaut `true`)

Ceux-ci remplacent `messages.tts.*` pour cet hôte.

## Format de sortie (fixe)

- **Telegram** : Message vocal Opus (ElevenLabs `opus_48000_64`, OpenAI `opus`).
  - 48 kHz / 64 kbps est un bon compromis pour les messages vocaux, requis pour la bulle circulaire.
- **Autres canaux** : MP3 (ElevenLabs `mp3_44100_128`, OpenAI `mp3`).
  - 44,1 kHz / 128 kbps est l'équilibre par défaut pour la clarté vocale.
- **Edge TTS** : Utilise `edge.outputFormat` (par défaut `audio-24khz-48kbitrate-mono-mp3`).
  - `node-edge-tts` accepte `outputFormat`, mais tous les formats ne sont pas disponibles depuis le service Edge. citeturn2search0
  - Les valeurs de format de sortie suivent les formats de sortie vocale Microsoft (y compris Ogg/WebM Opus). citeturn1search0
  - Telegram `sendVoice` accepte OGG/MP3/M4A ; si vous avez besoin de messages vocaux Opus garantis, utilisez OpenAI/ElevenLabs. citeturn1search1
  - Si le format de sortie Edge configuré échoue, OpenClaw réessaie avec MP3.

Les formats OpenAI/ElevenLabs sont fixes ; Telegram s'attend à Opus pour l'expérience utilisateur des messages vocaux.

## Comportement TTS automatique

Lorsqu'activé, OpenClaw :

- Ignore le TTS si la réponse contient déjà des médias ou une directive `MEDIA:`.
- Ignore les réponses très courtes (< 10 caractères).
- Synthétise les réponses longues en utilisant `agents.defaults.model
