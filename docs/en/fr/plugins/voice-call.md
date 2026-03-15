---
summary: "Plugin Voice Call : appels sortants + entrants via Twilio/Telnyx/Plivo (installation du plugin + configuration + CLI)"
read_when:
  - You want to place an outbound voice call from OpenClaw
  - You are configuring or developing the voice-call plugin
title: "Plugin Voice Call"
---

# Voice Call (plugin)

Appels vocaux pour OpenClaw via un plugin. Prend en charge les notifications sortantes et
les conversations multi-tours avec des politiques entrantes.

Fournisseurs actuels :

- `twilio` (Programmable Voice + Media Streams)
- `telnyx` (Call Control v2)
- `plivo` (Voice API + XML transfer + GetInput speech)
- `mock` (dev/pas de réseau)

Modèle mental rapide :

- Installer le plugin
- Redémarrer la Gateway
- Configurer sous `plugins.entries.voice-call.config`
- Utiliser `openclaw voicecall ...` ou l'outil `voice_call`

## Où il s'exécute (local vs distant)

Le plugin Voice Call s'exécute **à l'intérieur du processus Gateway**.

Si vous utilisez une Gateway distante, installez/configurez le plugin sur la **machine exécutant la Gateway**, puis redémarrez la Gateway pour le charger.

## Installation

### Option A : installer depuis npm (recommandé)

```bash
openclaw plugins install @openclaw/voice-call
```

Redémarrez la Gateway après.

### Option B : installer depuis un dossier local (dev, sans copie)

```bash
openclaw plugins install ./extensions/voice-call
cd ./extensions/voice-call && pnpm install
```

Redémarrez la Gateway après.

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

          telnyx: {
            apiKey: "...",
            connectionId: "...",
            // Clé publique du webhook Telnyx depuis le Telnyx Mission Control Portal
            // (chaîne Base64 ; peut également être définie via TELNYX_PUBLIC_KEY).
            publicKey: "...",
          },

          plivo: {
            authId: "MAxxxxxxxxxxxxxxxxxxxx",
            authToken: "...",
          },

          // Serveur webhook
          serve: {
            port: 3334,
            path: "/voice/webhook",
          },

          // Sécurité du webhook (recommandé pour les tunnels/proxies)
          webhookSecurity: {
            allowedHosts: ["voice.example.com"],
            trustedProxyIPs: ["100.64.0.1"],
          },

          // Exposition publique (choisir une)
          // publicUrl: "https://example.ngrok.app/voice/webhook",
          // tunnel: { provider: "ngrok" },
          // tailscale: { mode: "funnel", path: "/voice/webhook" }

          outbound: {
            defaultMode: "notify", // notify | conversation
          },

          streaming: {
            enabled: true,
            streamPath: "/voice/stream",
            preStartTimeoutMs: 5000,
            maxPendingConnections: 32,
            maxPendingConnectionsPerIp: 4,
            maxConnections: 128,
          },
        },
      },
    },
  },
}
```

Notes :

- Twilio/Telnyx nécessitent une **URL webhook accessible publiquement**.
- Plivo nécessite une **URL webhook accessible publiquement**.
- `mock` est un fournisseur dev local (pas d'appels réseau).
- Telnyx nécessite `telnyx.publicKey` (ou `TELNYX_PUBLIC_KEY`) sauf si `skipSignatureVerification` est true.
- `skipSignatureVerification` est réservé aux tests locaux uniquement.
- Si vous utilisez le niveau gratuit de ngrok, définissez `publicUrl` sur l'URL ngrok exacte ; la vérification de signature est toujours appliquée.
- `tunnel.allowNgrokFreeTierLoopbackBypass: true` permet les webhooks Twilio avec des signatures invalides **uniquement** quand `tunnel.provider="ngrok"` et `serve.bind` est loopback (agent local ngrok). À utiliser pour le dev local uniquement.
- Les URL du niveau gratuit de ngrok peuvent changer ou ajouter un comportement interstitiel ; si `publicUrl` dérive, les signatures Twilio échoueront. Pour la production, préférez un domaine stable ou un funnel Tailscale.
- Les paramètres par défaut de sécurité du streaming :
  - `streaming.preStartTimeoutMs` ferme les sockets qui n'envoient jamais une trame `start` valide.
  - `streaming.maxPendingConnections` limite les sockets non authentifiés pré-démarrage au total.
  - `streaming.maxPendingConnectionsPerIp` limite les sockets non authentifiés pré-démarrage par IP source.
  - `streaming.maxConnections` limite les sockets de flux média ouverts au total (en attente + actifs).

## Nettoyeur d'appels obsolètes

Utilisez `staleCallReaperSeconds` pour terminer les appels qui ne reçoivent jamais un webhook terminal
(par exemple, les appels en mode notify qui ne se terminent jamais). La valeur par défaut est `0`
(désactivé).

Plages recommandées :

- **Production :** `120`–`300` secondes pour les flux de style notify.
- Gardez cette valeur **supérieure à `maxDurationSeconds`** pour que les appels normaux puissent
  se terminer. Un bon point de départ est `maxDurationSeconds + 30–60` secondes.

Exemple :

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          maxDurationSeconds: 300,
          staleCallReaperSeconds: 360,
        },
      },
    },
  },
}
```

## Sécurité du webhook

Quand un proxy ou un tunnel se trouve devant la Gateway, le plugin reconstruit
l'URL publique pour la vérification de signature. Ces options contrôlent quels en-têtes transférés
sont approuvés.

`webhookSecurity.allowedHosts` met en liste blanche les hôtes des en-têtes de transfert.

`webhookSecurity.trustForwardingHeaders` approuve les en-têtes transférés sans liste blanche.

`webhookSecurity.trustedProxyIPs` approuve uniquement les en-têtes transférés quand l'IP
distante de la requête correspond à la liste.

La protection contre la relecture des webhooks est activée pour Twilio et Plivo. Les requêtes webhook
valides relues sont reconnues mais ignorées pour les effets secondaires.

Les tours de conversation Twilio incluent un jeton par tour dans les rappels `<Gather>`, donc
les rappels de parole obsolètes/relus ne peuvent pas satisfaire un tour de transcription en attente plus récent.

Exemple avec un hôte public stable :

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          publicUrl: "https://voice.example.com/voice/webhook",
          webhookSecurity: {
            allowedHosts: ["voice.example.com"],
          },
        },
      },
    },
  },
}
```

## TTS pour les appels

Voice Call utilise la configuration `messages.tts` du cœur (OpenAI ou ElevenLabs) pour
la parole en streaming sur les appels. Vous pouvez la remplacer sous la configuration du plugin avec la
**même forme** — elle fusionne profondément avec `messages.tts`.

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

Notes :

- **Edge TTS est ignoré pour les appels vocaux** (l'audio téléphonique nécessite PCM ; la sortie Edge n'est pas fiable).
- Le TTS du cœur est utilisé quand le streaming média Twilio est activé ; sinon les appels reviennent aux voix natives du fournisseur.

### Plus d'exemples

Utiliser le TTS du cœur uniquement (pas de remplacement) :

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

Remplacer par ElevenLabs uniquement pour les appels (garder la valeur par défaut du cœur ailleurs) :

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

Remplacer uniquement le modèle OpenAI pour les appels (exemple de fusion profonde) :

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

La politique entrante est désactivée par défaut. Pour activer les appels entrants, définissez :

```json5
{
  inboundPolicy: "allowlist",
  allowFrom: ["+15550001234"],
  inboundGreeting: "Hello! How can I help?",
}
```

`inboundPolicy: "allowlist"` est un filtrage d'ID appelant à faible assurance. Le plugin
normalise la valeur `From` fournie par le fournisseur et la compare à `allowFrom`.
La vérification du webhook authentifie la livraison du fournisseur et l'intégrité de la charge utile, mais
elle ne prouve pas la propriété du numéro d'appelant PSTN/VoIP. Traitez `allowFrom` comme
un filtrage d'ID appelant, pas une identité d'appelant forte.

Les réponses automatiques utilisent le système d'agent. Affinez avec :

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

## Outil d'agent

Nom de l'outil : `voice_call`

Actions :

- `initiate_call` (message, to?, mode?)
- `continue_call` (callId, message)
- `speak_to_user` (callId, message)
- `end_call` (callId)
- `get_status` (callId)

Ce repo inclut un document de compétence correspondant à `skills/voice-call/SKILL.md`.

## RPC Gateway

- `voicecall.initiate` (`to?`, `message`, `mode?`)
- `voicecall.continue` (`callId`, `message`)
- `voicecall.speak` (`callId`, `message`)
- `voicecall.end` (`callId`)
- `voicecall.status` (`callId`)
