---
read_when:
  - Modification de la façon dont les transcriptions audio ou le traitement des médias sont effectués
summary: Comment les messages audio/vocaux entrants sont téléchargés, transcrits et injectés dans les réponses
title: Audio et messages vocaux
x-i18n:
  generated_at: "2026-02-01T21:17:35Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b926c47989ab0d1ee1fb8ae6372c51d27515b53d6fefe211a85856d372f14569
  source_path: nodes/audio.md
  workflow: 15
---

# Audio / Messages vocaux — 2026-01-17

## Fonctionnalités prises en charge

- **Compréhension des médias (audio)** : Si la compréhension audio est activée (ou détection automatique), OpenClaw :
  1. Localise la première pièce jointe audio (chemin local ou URL) et la télécharge si nécessaire.
  2. Applique la limite `maxBytes` avant d'envoyer à chaque entrée de modèle.
  3. Exécute séquentiellement la première entrée de modèle correspondante (fournisseur ou CLI).
  4. En cas d'échec ou de saut (taille/délai d'attente), essaie l'entrée suivante.
  5. Une fois réussi, remplace le `Body` par un bloc `[Audio]` et définit `{{Transcript}}`.
- **Analyse des commandes** : Lors d'une transcription réussie, `CommandBody`/`RawBody` est défini au texte transcrit, les commandes slash restent donc valides.
- **Journalisation détaillée** : En mode `--verbose`, nous enregistrons les exécutions de transcription et les remplacements de corps.

## Détection automatique (par défaut)

Si vous **n'avez pas configuré de modèle** et que `tools.media.audio.enabled` **n'est pas** défini à `false`, OpenClaw détecte automatiquement dans cet ordre et s'arrête à la première option disponible :

1. **CLI local** (si installé)
   - `sherpa-onnx-offline` (nécessite `SHERPA_ONNX_MODEL_DIR` contenant encoder/decoder/joiner/tokens)
   - `whisper-cli` (depuis `whisper-cpp` ; utilise `WHISPER_CPP_MODEL` ou le modèle tiny intégré)
   - `whisper` (CLI Python ; télécharge automatiquement le modèle)
2. **CLI Gemini** (`gemini`) utilisant `read_many_files`
3. **Clés de fournisseur** (OpenAI → Groq → Deepgram → Google)

Pour désactiver la détection automatique, définissez `tools.media.audio.enabled: false`.
Pour personnaliser, définissez `tools.media.audio.models`.
Remarque : La détection binaire fonctionne au mieux sur macOS/Linux/Windows ; assurez-vous que le CLI est dans `PATH` (nous développons `~`), ou définissez un modèle CLI explicite via le chemin de commande complet.

## Exemples de configuration

### Fournisseur + Secours CLI (OpenAI + Whisper CLI)

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

### Fournisseur uniquement + Contrôle de portée

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

## Remarques et limitations

- L'authentification du fournisseur suit l'ordre d'authentification standard du modèle (fichier de configuration d'authentification, variables d'environnement, `models.providers.*.apiKey`).
- Lors de l'utilisation de `provider: "deepgram"`, Deepgram lit `DEEPGRAM_API_KEY`.
- Détails de configuration Deepgram : [Deepgram (transcription audio)](/providers/deepgram).
- Les fournisseurs audio peuvent remplacer `baseUrl`, `headers` et `providerOptions` via `tools.media.audio`.
- La limite de taille par défaut est 20 Mo (`tools.media.audio.maxBytes`). Les audios trop volumineux ignorent ce modèle et essaient l'entrée suivante.
- Le `maxChars` par défaut pour l'audio **n'est pas défini** (texte transcrit complet). Définissez `tools.media.audio.maxChars` ou `maxChars` par entrée pour tronquer la sortie.
- La détection automatique OpenAI utilise par défaut `gpt-4o-mini-transcribe` ; définissez `model: "gpt-4o-transcribe"` pour une meilleure précision.
- Utilisez `tools.media.audio.attachments` pour traiter plusieurs messages vocaux (`mode: "all"` + `maxAttachments`).
- Le texte transcrit est disponible dans les modèles via `{{Transcript}}`.
- La sortie standard CLI a une limite (5 Mo) ; gardez la sortie CLI concise.

## Pièges courants

- Les règles de portée utilisent la première correspondance. `chatType` est normalisé en `direct`, `group` ou `room`.
- Assurez-vous que votre CLI se termine avec le code de sortie 0 et produit du texte brut ; les formats JSON nécessitent une conversion via `jq -r .text`.
- Maintenez des délais d'attente raisonnables (`timeoutSeconds`, 60 secondes par défaut) pour éviter de bloquer la file d'attente des réponses.
