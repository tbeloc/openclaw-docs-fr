---
summary: "Comment les notes audio/vocales entrantes sont téléchargées, transcrites et injectées dans les réponses"
read_when:
  - Changing audio transcription or media handling
title: "Audio et Notes Vocales"
---

# Audio / Notes Vocales — 2026-01-17

## Ce qui fonctionne

- **Compréhension des médias (audio)** : Si la compréhension audio est activée (ou détectée automatiquement), OpenClaw :
  1. Localise la première pièce jointe audio (chemin local ou URL) et la télécharge si nécessaire.
  2. Applique `maxBytes` avant d'envoyer à chaque entrée de modèle.
  3. Exécute la première entrée de modèle éligible dans l'ordre (fournisseur ou CLI).
  4. En cas d'échec ou de saut (taille/délai d'attente), il essaie l'entrée suivante.
  5. En cas de succès, il remplace `Body` par un bloc `[Audio]` et définit `{{Transcript}}`.
- **Analyse des commandes** : Lorsque la transcription réussit, `CommandBody`/`RawBody` sont définis sur la transcription afin que les commandes slash fonctionnent toujours.
- **Journalisation détaillée** : En `--verbose`, nous enregistrons quand la transcription s'exécute et quand elle remplace le corps.

## Détection automatique (par défaut)

Si vous **ne configurez pas de modèles** et que `tools.media.audio.enabled` **n'est pas** défini sur `false`,
OpenClaw détecte automatiquement dans cet ordre et s'arrête à la première option fonctionnelle :

1. **CLIs locales** (si installées)
   - `sherpa-onnx-offline` (nécessite `SHERPA_ONNX_MODEL_DIR` avec encodeur/décodeur/joiner/tokens)
   - `whisper-cli` (de `whisper-cpp` ; utilise `WHISPER_CPP_MODEL` ou le modèle tiny fourni)
   - `whisper` (CLI Python ; télécharge automatiquement les modèles)
2. **CLI Gemini** (`gemini`) utilisant `read_many_files`
3. **Clés de fournisseur** (OpenAI → Groq → Deepgram → Google)

Pour désactiver la détection automatique, définissez `tools.media.audio.enabled: false`.
Pour personnaliser, définissez `tools.media.audio.models`.
Remarque : La détection binaire est au mieux un effort sur macOS/Linux/Windows ; assurez-vous que la CLI est sur `PATH` (nous développons `~`), ou définissez un modèle CLI explicite avec un chemin de commande complet.

## Exemples de configuration

### Fournisseur + secours CLI (OpenAI + Whisper CLI)

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        maxBytes: 20971520,
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          {
            type: "cli",
            command: "whisper",
            args: ["--model", "base", "{{MediaPath}}"],
            timeoutSeconds: 45,
          },
        ],
      },
    },
  },
}
```

### Fournisseur uniquement avec contrôle de portée

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        scope: {
          default: "allow",
          rules: [{ action: "deny", match: { chatType: "group" } }],
        },
        models: [{ provider: "openai", model: "gpt-4o-mini-transcribe" }],
      },
    },
  },
}
```

### Fournisseur uniquement (Deepgram)

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "deepgram", model: "nova-3" }],
      },
    },
  },
}
```

### Fournisseur uniquement (Mistral Voxtral)

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "mistral", model: "voxtral-mini-latest" }],
      },
    },
  },
}
```

### Répéter la transcription au chat (opt-in)

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        echoTranscript: true, // default is false
        echoFormat: '📝 "{transcript}"', // optional, supports {transcript}
        models: [{ provider: "openai", model: "gpt-4o-mini-transcribe" }],
      },
    },
  },
}
```

## Notes et limites

- L'authentification du fournisseur suit l'ordre d'authentification du modèle standard (profils d'authentification, variables d'environnement, `models.providers.*.apiKey`).
- Deepgram récupère `DEEPGRAM_API_KEY` lorsque `provider: "deepgram"` est utilisé.
- Détails de configuration Deepgram : [Deepgram (transcription audio)](/providers/deepgram).
- Détails de configuration Mistral : [Mistral](/providers/mistral).
- Les fournisseurs audio peuvent remplacer `baseUrl`, `headers` et `providerOptions` via `tools.media.audio`.
- La limite de taille par défaut est 20 Mo (`tools.media.audio.maxBytes`). L'audio surdimensionné est ignoré pour ce modèle et l'entrée suivante est essayée.
- Les fichiers audio minuscules/vides en dessous de 1024 octets sont ignorés avant la transcription du fournisseur/CLI.
- `maxChars` par défaut pour l'audio est **non défini** (transcription complète). Définissez `tools.media.audio.maxChars` ou `maxChars` par entrée pour réduire la sortie.
- La valeur par défaut automatique d'OpenAI est `gpt-4o-mini-transcribe` ; définissez `model: "gpt-4o-transcribe"` pour une meilleure précision.
- Utilisez `tools.media.audio.attachments` pour traiter plusieurs notes vocales (`mode: "all"` + `maxAttachments`).
- La transcription est disponible pour les modèles sous la forme `{{Transcript}}`.
- `tools.media.audio.echoTranscript` est désactivé par défaut ; activez-le pour envoyer une confirmation de transcription au chat d'origine avant le traitement de l'agent.
- `tools.media.audio.echoFormat` personnalise le texte d'écho (espace réservé : `{transcript}`).
- La sortie CLI est limitée (5 Mo) ; gardez la sortie CLI concise.

### Support de l'environnement proxy

La transcription audio basée sur le fournisseur respecte les variables d'environnement proxy sortantes standard :

- `HTTPS_PROXY`
- `HTTP_PROXY`
- `https_proxy`
- `http_proxy`

Si aucune variable d'environnement proxy n'est définie, la sortie directe est utilisée. Si la configuration du proxy est malformée, OpenClaw enregistre un avertissement et revient à la récupération directe.

## Détection de mention dans les groupes

Lorsque `requireMention: true` est défini pour un chat de groupe, OpenClaw transcrit maintenant l'audio **avant** de vérifier les mentions. Cela permet aux notes vocales d'être traitées même si elles contiennent des mentions.

**Comment cela fonctionne :**

1. Si un message vocal n'a pas de corps de texte et que le groupe nécessite des mentions, OpenClaw effectue une transcription « préalable ».
2. La transcription est vérifiée pour les modèles de mention (par exemple, `@BotName`, déclencheurs emoji).
3. Si une mention est trouvée, le message procède à travers le pipeline de réponse complet.
4. La transcription est utilisée pour la détection de mention afin que les notes vocales puissent passer la porte de mention.

**Comportement de secours :**

- Si la transcription échoue lors du préalable (délai d'attente, erreur API, etc.), le message est traité en fonction de la détection de mention textuelle uniquement.
- Cela garantit que les messages mixtes (texte + audio) ne sont jamais incorrectement supprimés.

**Opt-out par groupe/sujet Telegram :**

- Définissez `channels.telegram.groups.<chatId>.disableAudioPreflight: true` pour ignorer les vérifications de mention de transcription préalable pour ce groupe.
- Définissez `channels.telegram.groups.<chatId>.topics.<threadId>.disableAudioPreflight` pour remplacer par sujet (`true` pour ignorer, `false` pour forcer l'activation).
- La valeur par défaut est `false` (préalable activé lorsque les conditions de mention-gated correspondent).

**Exemple :** Un utilisateur envoie une note vocale disant « Hey @Claude, quel est le temps ? » dans un groupe Telegram avec `requireMention: true`. La note vocale est transcrite, la mention est détectée et l'agent répond.

## Pièges

- Les règles de portée utilisent le premier match gagne. `chatType` est normalisé en `direct`, `group` ou `room`.
- Assurez-vous que votre CLI se termine avec 0 et imprime du texte brut ; JSON doit être massé via `jq -r .text`.
- Pour `parakeet-mlx`, si vous passez `--output-dir`, OpenClaw lit `<output-dir>/<media-basename>.txt` lorsque `--output-format` est `txt` (ou omis) ; les formats de sortie non-`txt` reviennent à l'analyse stdout.
- Gardez les délais d'attente raisonnables (`timeoutSeconds`, par défaut 60s) pour éviter de bloquer la file d'attente de réponse.
- La transcription préalable ne traite que la **première** pièce jointe audio pour la détection de mention. L'audio supplémentaire est traité pendant la phase de compréhension des médias principale.
