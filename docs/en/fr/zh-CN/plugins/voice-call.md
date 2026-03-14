```markdown
---
read_when:
  - Vous souhaitez initier un appel vocal sortant depuis OpenClaw
  - Vous configurez ou développez le plugin voice-call
summary: Plugin Voice Call : appels sortants + entrants via Twilio/Telnyx/Plivo (installation + configuration + CLI)
title: Plugin Voice Call
x-i18n:
  generated_at: "2026-02-03T07:53:40Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: d731c63bf52781cc49262db550d0507d7fc33e5e7ce5d87efaf5d44aedcafef7
  source_path: plugins/voice-call.md
  workflow: 15
---

# Voice Call (Plugin)

Fournissez des appels vocaux à OpenClaw via un plugin. Supporte les notifications sortantes et les conversations multi-tours avec des stratégies entrantes.

Fournisseurs actuels :

- `twilio` (Programmable Voice + Media Streams)
- `telnyx` (Call Control v2)
- `plivo` (Voice API + XML transfer + GetInput speech)
- `mock` (développement/sans réseau)

Modèle mental rapide :

- Installez le plugin
- Redémarrez la passerelle Gateway
- Configurez sous `plugins.entries.voice-call.config`
- Utilisez `openclaw voicecall ...` ou l'outil `voice_call`

## Lieu d'exécution (local vs distant)

Le plugin Voice Call s'exécute **à l'intérieur du processus Gateway**.

Si vous utilisez une passerelle Gateway distante, installez/configurez le plugin sur **la machine exécutant la passerelle Gateway**, puis redémarrez la passerelle Gateway pour le charger.

## Installation

### Option A : Installation depuis npm (recommandé)

```bash
openclaw plugins install @openclaw/voice-call
```

Redémarrez ensuite la passerelle Gateway.

### Option B : Installation depuis un dossier local (développement, sans copie)

```bash
openclaw plugins install ./extensions/voice-call
cd ./extensions/voice-call && pnpm install
```

Redémarrez ensuite la passerelle Gateway.

## Configuration

Définissez la configuration sous `plugins.entries.voice-call.config` :

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        enabled: true,
        config: {
          provider: "twilio", // ou "telnyx" | "plivo" | "mock"
          fromNumber: "+15550001234",
          toNumber: "+15550005678",

          twilio: {
            accountSid: "ACxxxxxxxx",
            authToken: "...",
          },

          plivo: {
            authId: "MAxxxxxxxxxxxxxxxxxxxx",
            authToken: "...",
          },

          // Serveur Webhook
          serve: {
            port: 3334,
            path: "/voice/webhook",
          },

          // Exposition publique (choisissez-en un)
          // publicUrl: "https://example.ngrok.app/voice/webhook",
          // tunnel: { provider: "ngrok" },
          // tailscale: { mode: "funnel", path: "/voice/webhook" }

          outbound: {
            defaultMode: "notify", // notify | conversation
          },

          streaming: {
            enabled: true,
            streamPath: "/voice/stream",
          },
        },
      },
    },
  },
}
```

Points importants :

- Twilio/Telnyx nécessitent une URL webhook **accessible publiquement**.
- Plivo nécessite une URL webhook **accessible publiquement**.
- `mock` est un fournisseur de développement local (sans appels réseau).
- `skipSignatureVerification` est réservé aux tests locaux uniquement.
- Si vous utilisez la version gratuite de ngrok, définissez `publicUrl` sur l'URL ngrok exacte ; la vérification de signature est toujours appliquée.
- `tunnel.allowNgrokFreeTierLoopbackBypass: true` permet les webhooks Twilio avec des signatures invalides, **uniquement si** `tunnel.provider="ngrok"` et `serve.bind` est loopback (proxy local ngrok). Réservé au développement local uniquement.
- Les URL de la version gratuite de ngrok peuvent changer ou ajouter un comportement de page intermédiaire ; si `publicUrl` dérive, la signature Twilio échouera. Pour la production, privilégiez les domaines stables ou Tailscale funnel.

## TTS pour les appels

Voice Call utilise la configuration `messages.tts` du noyau (OpenAI ou ElevenLabs) pour la parole en continu dans les appels. Vous pouvez la remplacer en utilisant la **même structure** sous la configuration du plugin — elle sera fusionnée en profondeur avec `messages.tts`.

```json5
{
  tts: {
    provider: "elevenlabs",
    elevenlabs: {
      voiceId: "pMsXgVXv3BLzUgSXRplE",
      modelId: "eleven_multilingual_v2",
    },
  },
}
```

Points importants :

- **Les appels vocaux ignorent Edge TTS** (l'audio téléphonique nécessite PCM ; la sortie Edge n'est pas fiable).
- Utilisez le TTS du noyau lorsque Twilio Media Streams est activé ; sinon, l'appel revient aux voix natives du fournisseur.

### Autres exemples

Utiliser uniquement le TTS du noyau (sans remplacement) :

```json5
{
  messages: {
    tts: {
      provider: "openai",
      openai: { voice: "alloy" },
    },
  },
}
```

Remplacer uniquement pour les appels par ElevenLabs (garder les valeurs par défaut du noyau ailleurs) :

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          tts: {
            provider: "elevenlabs",
            elevenlabs: {
              apiKey: "elevenlabs_key",
              voiceId: "pMsXgVXv3BLzUgSXRplE",
              modelId: "eleven_multilingual_v2",
            },
          },
        },
      },
    },
  },
}
```

Remplacer uniquement le modèle OpenAI pour les appels (exemple de fusion en profondeur) :

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          tts: {
            openai: {
              model: "gpt-4o-mini-tts",
              voice: "marin",
            },
          },
        },
      },
    },
  },
}
```

## Appels entrants

La stratégie entrante est désactivée par défaut. Pour activer les appels entrants, définissez :

```json5
{
  inboundPolicy: "allowlist",
  allowFrom: ["+15550001234"],
  inboundGreeting: "Hello! How can I help?",
}
```

La réponse automatique utilise le système d'agent. Ajustez via :

- `responseModel`
- `responseSystemPrompt`
- `responseTimeoutMs`

## CLI

```bash
openclaw voicecall call --to "+15555550123" --message "Hello from OpenClaw"
openclaw voicecall continue --call-id <id> --message "Any questions?"
openclaw voicecall speak --call-id <id> --message "One moment"
openclaw voicecall end --call-id <id>
openclaw voicecall status --call-id <id>
openclaw voicecall tail
openclaw voicecall expose --mode funnel
```

## Outil Agent

Nom de l'outil : `voice_call`

Opérations :

- `initiate_call` (message, to?, mode?)
- `continue_call` (callId, message)
- `speak_to_user` (callId, message)
- `end_call` (callId)
- `get_status` (callId)

Ce dépôt fournit une documentation de skill complémentaire dans `skills/voice-call/SKILL.md`.

## RPC Gateway

- `voicecall.initiate` (`to?`, `message`, `mode?`)
- `voicecall.continue` (`callId`, `message`)
- `voicecall.speak` (`callId`, `message`)
- `voicecall.end` (`callId`)
- `voicecall.status` (`callId`)
```
