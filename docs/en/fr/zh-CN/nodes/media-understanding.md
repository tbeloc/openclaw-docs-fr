---
read_when:
  - Concevoir ou restructurer la compréhension des médias
  - Affiner le prétraitement des médias entrants (audio/vidéo/images)
summary: Compréhension des médias entrants (image/audio/vidéo) (optionnel), avec fournisseur + secours CLI
title: Compréhension des médias
x-i18n:
  generated_at: "2026-02-03T07:51:40Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: f6c575662b7fcbf0b62c46e3fdfa4cdb7cfd455513097e4a2cdec8a34cbdbd48
  source_path: nodes/media-understanding.md
  workflow: 15
---

# Compréhension des médias (entrants) — 2026-01-17

OpenClaw peut **résumer les médias entrants** (images/audio/vidéo) avant l'exécution du flux de réponse. Il détecte automatiquement si les outils locaux ou les clés de fournisseur sont disponibles, et peut être désactivé ou personnalisé. Si la compréhension est désactivée, le modèle reçoit toujours les fichiers/URL bruts comme d'habitude.

## Objectifs

- Optionnel : pré-digérer les médias entrants en texte court pour un routage plus rapide + une meilleure analyse des commandes.
- Conserver la transmission des médias originaux au modèle (toujours).
- Prendre en charge les **API de fournisseur** et les **secours CLI**.
- Permettre plusieurs modèles et basculer en ordre (erreurs/taille/délais d'expiration).

## Comportement de haut niveau

1. Collecter les pièces jointes entrantes (`MediaPaths`, `MediaUrls`, `MediaTypes`).
2. Pour chaque capacité activée (image/audio/vidéo), sélectionner les pièces jointes selon la stratégie (par défaut : **première**).
3. Sélectionner la première entrée de modèle admissible (taille + capacité + authentification).
4. Si le modèle échoue ou le média est trop volumineux, **basculer vers l'entrée suivante**.
5. En cas de succès :
   - `Body` devient un bloc `[Image]`, `[Audio]` ou `[Video]`.
   - L'audio définit `{{Transcript}}`; l'analyse des commandes utilise le texte du titre s'il existe, sinon la transcription.
   - Le titre est conservé en tant que `User text:` dans le bloc.

Si la compréhension échoue ou est désactivée, **le flux de réponse continue** avec le corps original + les pièces jointes.

## Aperçu de la configuration

`tools.media` prend en charge les **modèles partagés** plus les remplacements par capacité :

- `tools.media.models` : liste de modèles partagés (utiliser `capabilities` pour qualifier).
- `tools.media.image` / `tools.media.audio` / `tools.media.video` :
  - Valeurs par défaut (`prompt`, `maxChars`, `maxBytes`, `timeoutSeconds`, `language`)
  - Remplacements de fournisseur (`baseUrl`, `headers`, `providerOptions`)
  - Configurer les options audio Deepgram via `tools.media.audio.providerOptions.deepgram`
  - Liste optionnelle de **modèles par capacité** (prioritaire sur les modèles partagés)
  - Stratégie `attachments` (`mode`, `maxAttachments`, `prefer`)
  - `scope` (qualification optionnelle par canal/type de chat/clé de session)
- `tools.media.concurrency` : nombre maximal d'exécutions de capacités concurrentes (par défaut **2**).

```json5
{
  tools: {
    media: {
      models: [
        /* liste partagée */
      ],
      image: {
        /* remplacements optionnels */
      },
      audio: {
        /* remplacements optionnels */
      },
      video: {
        /* remplacements optionnels */
      },
    },
  },
}
```

### Entrées de modèle

Chaque entrée `models[]` peut être un **fournisseur** ou une **CLI** :

```json5
{
  type: "provider", // par défaut si omis
  provider: "openai",
  model: "gpt-5.2",
  prompt: "Describe the image in <= 500 chars.",
  maxChars: 500,
  maxBytes: 10485760,
  timeoutSeconds: 60,
  capabilities: ["image"], // optionnel, pour les entrées multimodales
  profile: "vision-profile",
  preferredProfile: "vision-fallback",
}
```

```json5
{
  type: "cli",
  command: "gemini",
  args: [
    "-m",
    "gemini-3-flash",
    "--allowed-tools",
    "read_file",
    "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
  ],
  maxChars: 500,
  maxBytes: 52428800,
  timeoutSeconds: 120,
  capabilities: ["video", "image"],
}
```

Les modèles CLI peuvent également utiliser :

- `{{MediaDir}}` (répertoire contenant les fichiers médias)
- `{{OutputDir}}` (répertoire temporaire créé pour cette exécution)
- `{{OutputBase}}` (chemin de base du fichier temporaire, sans extension)

## Valeurs par défaut et limites

Valeurs par défaut recommandées :

- `maxChars` : **500** pour image/vidéo (court, adapté aux commandes)
- `maxChars` : **non défini** pour audio (transcription complète, sauf si vous définissez une limite)
- `maxBytes` :
  - Image : **10 Mo**
  - Audio : **20 Mo**
  - Vidéo : **50 Mo**

Règles :

- Si le média dépasse `maxBytes`, ce modèle est ignoré, **essayer le modèle suivant**.
- Si le modèle retourne plus que `maxChars`, la sortie est tronquée.
- `prompt` par défaut est un simple "Describe the {media}." plus les conseils `maxChars` (images/vidéo uniquement).
- Si `<capability>.enabled: true` mais aucun modèle configuré, OpenClaw essaie le **modèle de réponse actif** lorsque le fournisseur prend en charge la capacité.

### Détection automatique de la compréhension des médias (par défaut)

Si `tools.media.<capability>.enabled` n'est **pas** défini sur `false` et que vous n'avez pas configuré de modèles, OpenClaw détecte automatiquement et **s'arrête à la première option disponible** dans cet ordre :

1. **CLI local** (audio uniquement ; si installé)
   - `sherpa-onnx-offline` (nécessite `SHERPA_ONNX_MODEL_DIR` avec encoder/decoder/joiner/tokens)
   - `whisper-cli` (`whisper-cpp` ; utilise `WHISPER_CPP_MODEL` ou le modèle tiny fourni)
   - `whisper` (CLI Python ; télécharge automatiquement le modèle)
2. **CLI Gemini** (`gemini`) utilisant `read_many_files`
3. **Clés de fournisseur**
   - Audio : OpenAI → Groq → Deepgram → Google
   - Image : OpenAI → Anthropic → Google → MiniMax
   - Vidéo : Google

Pour désactiver la détection automatique, définissez :

```json5
{
  tools: {
    media: {
      audio: {
        enabled: false,
      },
    },
  },
}
```

Remarque : la détection de binaires est au mieux sur macOS/Linux/Windows ; assurez-vous que la CLI est dans `PATH` (nous développons `~`), ou définissez un modèle CLI explicite avec le chemin complet de la commande.

## Capacités (optionnel)

Si vous définissez `capabilities`, cette entrée s'exécute uniquement pour ces types de médias. Pour une liste partagée, OpenClaw peut déduire les valeurs par défaut :

- `openai`, `anthropic`, `minimax` : **image**
- `google` (API Gemini) : **image + audio + vidéo**
- `groq` : **audio**
- `deepgram` : **audio**

Pour les entrées CLI, **définissez explicitement `capabilities`** pour éviter les correspondances accidentelles. Si vous omettez `capabilities`, cette entrée est admissible pour toutes les listes dans lesquelles elle apparaît.

## Matrice de support des fournisseurs (intégrations OpenClaw)

| Capacité | Intégrations de fournisseur                    | Description                                    |
| -------- | ---------------------------------------------- | ---------------------------------------------- |
| Image    | OpenAI / Anthropic / Google / autres via `pi-ai` | Tout modèle supportant les images dans le registre est disponible. |
| Audio    | OpenAI, Groq, Deepgram, Google                 | Transcription du fournisseur (Whisper/Deepgram/Gemini). |
| Vidéo    | Google (API Gemini)                            | Compréhension vidéo du fournisseur.             |

## Fournisseurs recommandés

**Image**

- Privilégier votre modèle actif s'il supporte les images.
- Bonnes valeurs par défaut : `openai/gpt-5.2`, `anthropic/claude-opus-4-5`, `google/gemini-3-pro-preview`.

**Audio**

- `openai/gpt-4o-mini-transcribe`, `groq/whisper-large-v3-turbo` ou `deepgram/nova-3`.
- Secours CLI : `whisper-cli` (whisper-cpp) ou `whisper`.
- Configuration Deepgram : [Deepgram (transcription audio)](/providers/deepgram).

**Vidéo**

- `google/gemini-3-flash-preview` (rapide), `google/gemini-3-pro-preview` (plus riche).
- Secours CLI : CLI `gemini` (supporte l'utilisation de `read_file` pour vidéo/audio).

## Stratégie des pièces jointes

`attachments` par capacité contrôle quelles pièces jointes traiter :

- `mode` : `first` (par défaut) ou `all`
- `maxAttachments` : limite le nombre traité (par défaut **1**)
- `prefer` : `first`, `last`, `path`, `url`

Quand `mode: "all"`, la sortie est marquée `[Image 1/2]`, `[Audio 2/2]`, etc.

## Exemples de configuration

### 1) Liste de modèles partagés + remplacements

```json5
{
  tools: {
    media: {
      models: [
        { provider: "openai", model: "gpt-5.2", capabilities: ["image"] },
        {
          provider: "google",
          model: "gemini-3-flash-preview",
          capabilities: ["image", "audio", "video"],
        },
        {
          type: "cli",
          command: "gemini",
          args: [
            "-m",
            "gemini-3-flash",
            "--allowed-tools",
            "read_file",
            "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
          ],
          capabilities: ["image", "video"],
        },
      ],
      audio: {
        attachments: { mode: "all", maxAttachments: 2 },
      },
      video: {
        maxChars: 500,
      },
    },
  },
}
```

### 2) Audio + vidéo uniquement (image désactivée)

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          {
            type: "cli",
            command: "whisper",
            args: ["--model", "base", "{{MediaPath}}"],
          },
        ],
      },
      video: {
        enabled: true,
        maxChars: 500,
        models: [
          { provider: "google", model: "gemini-3-flash-preview" },
          {
            type: "cli",
            command: "gemini",
            args: [
              "-m",
              "gemini-3-flash",
              "--allowed-tools",
              "read_file",
              "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
            ],
          },
        ],
      },
    },
  },
}
```

### 3) Compréhension optionnelle des images

```json5
{
  tools: {
    media: {
      image: {
        enabled: true,
        maxBytes: 10485760,
        maxChars: 500,
        models: [
          { provider: "openai", model: "gpt-5.2" },
          { provider: "anthropic", model: "claude-opus-4-5" },
          {
            type: "cli",
            command: "gemini",
            args: [
              "-m",
              "gemini-3-flash",
              "--allowed-tools",
              "read_file",
              "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
            ],
          },
        ],
      },
    },
  },
}
```

### 4) Entrée unique multimodale (capacités explicites)

```json5
{
  tools: {
    media: {
      image: {
        models: [
          {
            provider: "google",
            model: "gemini-3-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
      audio: {
        models: [
          {
            provider: "google",
            model: "gemini-3-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
      video: {
        models: [
          {
            provider: "google",
            model: "gemini-3-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
    },
  },
}
```

## Sortie d'état

Quand la compréhension des médias s'exécute, `/status` contient une ligne de résumé court :

```
📎 Media: image ok (openai/gpt-5.2) · audio skipped (maxBytes)
```

Cela affiche le résultat par capacité et le fournisseur/modèle sélectionné le cas échéant.

## Remarques

- La compréhension est **au mieux**. Les erreurs n'empêchent pas la réponse.
- Les pièces jointes sont toujours transmises au modèle, même si la compréhension est désactivée.
- Utiliser `scope` pour limiter où la compréhension s'exécute (par exemple, messages privés uniquement).
