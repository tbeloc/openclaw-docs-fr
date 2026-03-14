---
summary: "Compréhension des images/audio/vidéo entrantes (optionnelle) avec fournisseur + fallbacks CLI"
read_when:
  - Designing or refactoring media understanding
  - Tuning inbound audio/video/image preprocessing
title: "Compréhension des médias"
---

# Compréhension des médias (Entrante) — 2026-01-17

OpenClaw peut **résumer les médias entrants** (image/audio/vidéo) avant l'exécution du pipeline de réponse. Il détecte automatiquement quand les outils locaux ou les clés de fournisseur sont disponibles, et peut être désactivé ou personnalisé. Si la compréhension est désactivée, les modèles reçoivent toujours les fichiers/URL d'origine comme d'habitude.

## Objectifs

- Optionnel : pré-digérer les médias entrants en texte court pour un routage plus rapide et une meilleure analyse des commandes.
- Préserver la livraison des médias d'origine au modèle (toujours).
- Supporter les **API de fournisseur** et les **fallbacks CLI**.
- Permettre plusieurs modèles avec fallback ordonné (erreur/taille/timeout).

## Comportement de haut niveau

1. Collecter les pièces jointes entrantes (`MediaPaths`, `MediaUrls`, `MediaTypes`).
2. Pour chaque capacité activée (image/audio/vidéo), sélectionner les pièces jointes selon la politique (par défaut : **première**).
3. Choisir la première entrée de modèle éligible (taille + capacité + authentification).
4. Si un modèle échoue ou le média est trop volumineux, **basculer vers l'entrée suivante**.
5. En cas de succès :
   - `Body` devient un bloc `[Image]`, `[Audio]` ou `[Video]`.
   - Audio définit `{{Transcript}}`; l'analyse des commandes utilise le texte de la légende si présent,
     sinon la transcription.
   - Les légendes sont conservées comme `User text:` à l'intérieur du bloc.

Si la compréhension échoue ou est désactivée, **le flux de réponse continue** avec le corps d'origine + les pièces jointes.

## Aperçu de la configuration

`tools.media` supporte les **modèles partagés** plus les remplacements par capacité :

- `tools.media.models`: liste de modèles partagés (utiliser `capabilities` pour gater).
- `tools.media.image` / `tools.media.audio` / `tools.media.video`:
  - valeurs par défaut (`prompt`, `maxChars`, `maxBytes`, `timeoutSeconds`, `language`)
  - remplacements de fournisseur (`baseUrl`, `headers`, `providerOptions`)
  - Options audio Deepgram via `tools.media.audio.providerOptions.deepgram`
  - contrôles d'écho de transcription audio (`echoTranscript`, par défaut `false`; `echoFormat`)
  - liste de **modèles par capacité** optionnelle (préférée avant les modèles partagés)
  - politique `attachments` (`mode`, `maxAttachments`, `prefer`)
  - `scope` (gating optionnel par canal/chatType/clé de session)
- `tools.media.concurrency`: max d'exécutions de capacité concurrentes (par défaut **2**).

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
        echoTranscript: true,
        echoFormat: '📝 "{transcript}"',
      },
      video: {
        /* remplacements optionnels */
      },
    },
  },
}
```

### Entrées de modèle

Chaque entrée `models[]` peut être **fournisseur** ou **CLI** :

```json5
{
  type: "provider", // par défaut si omis
  provider: "openai",
  model: "gpt-5.2",
  prompt: "Describe the image in <= 500 chars.",
  maxChars: 500,
  maxBytes: 10485760,
  timeoutSeconds: 60,
  capabilities: ["image"], // optionnel, utilisé pour les entrées multi-modales
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

- `{{MediaDir}}` (répertoire contenant le fichier média)
- `{{OutputDir}}` (répertoire de travail créé pour cette exécution)
- `{{OutputBase}}` (chemin de fichier de travail de base, sans extension)

## Valeurs par défaut et limites

Valeurs par défaut recommandées :

- `maxChars`: **500** pour image/vidéo (court, convivial pour les commandes)
- `maxChars`: **non défini** pour audio (transcription complète sauf si vous définissez une limite)
- `maxBytes`:
  - image: **10MB**
  - audio: **20MB**
  - vidéo: **50MB**

Règles :

- Si le média dépasse `maxBytes`, ce modèle est ignoré et le **modèle suivant est essayé**.
- Les fichiers audio plus petits que **1024 octets** sont traités comme vides/corrompus et ignorés avant la transcription du fournisseur/CLI.
- Si le modèle retourne plus que `maxChars`, la sortie est tronquée.
- `prompt` par défaut à simple "Describe the {media}." plus les conseils `maxChars` (image/vidéo uniquement).
- Si `<capability>.enabled: true` mais aucun modèle n'est configuré, OpenClaw essaie le
  **modèle de réponse actif** quand son fournisseur supporte la capacité.

### Détection automatique de la compréhension des médias (par défaut)

Si `tools.media.<capability>.enabled` n'est **pas** défini à `false` et vous n'avez pas
configuré de modèles, OpenClaw détecte automatiquement dans cet ordre et **s'arrête à la première
option fonctionnelle** :

1. **CLIs locales** (audio uniquement; si installées)
   - `sherpa-onnx-offline` (nécessite `SHERPA_ONNX_MODEL_DIR` avec encoder/decoder/joiner/tokens)
   - `whisper-cli` (`whisper-cpp`; utilise `WHISPER_CPP_MODEL` ou le modèle tiny fourni)
   - `whisper` (CLI Python; télécharge les modèles automatiquement)
2. **CLI Gemini** (`gemini`) utilisant `read_many_files`
3. **Clés de fournisseur**
   - Audio: OpenAI → Groq → Deepgram → Google
   - Image: OpenAI → Anthropic → Google → MiniMax
   - Vidéo: Google

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

Remarque : La détection binaire est au mieux sur macOS/Linux/Windows; assurez-vous que la CLI est sur `PATH` (nous développons `~`), ou définissez un modèle CLI explicite avec un chemin de commande complet.

### Support de l'environnement proxy (modèles de fournisseur)

Quand la compréhension des médias **audio** et **vidéo** basée sur le fournisseur est activée, OpenClaw
honore les variables d'environnement proxy sortantes standard pour les appels HTTP du fournisseur :

- `HTTPS_PROXY`
- `HTTP_PROXY`
- `https_proxy`
- `http_proxy`

Si aucune variable d'environnement proxy n'est définie, la compréhension des médias utilise l'accès direct.
Si la valeur du proxy est malformée, OpenClaw enregistre un avertissement et bascule vers l'accès
direct.

## Capacités (optionnel)

Si vous définissez `capabilities`, l'entrée s'exécute uniquement pour ces types de médias. Pour les
listes partagées, OpenClaw peut déduire les valeurs par défaut :

- `openai`, `anthropic`, `minimax`: **image**
- `google` (API Gemini): **image + audio + vidéo**
- `groq`: **audio**
- `deepgram`: **audio**

Pour les entrées CLI, **définissez `capabilities` explicitement** pour éviter les correspondances surprises.
Si vous omettez `capabilities`, l'entrée est éligible pour la liste dans laquelle elle apparaît.

## Matrice de support des fournisseurs (intégrations OpenClaw)

| Capacité | Intégration de fournisseur                       | Remarques                                                 |
| -------- | ------------------------------------------------ | --------------------------------------------------------- |
| Image    | OpenAI / Anthropic / Google / autres via `pi-ai` | Tout modèle capable d'images dans le registre fonctionne. |
| Audio    | OpenAI, Groq, Deepgram, Google, Mistral         | Transcription du fournisseur (Whisper/Deepgram/Gemini/Voxtral). |
| Vidéo    | Google (API Gemini)                             | Compréhension vidéo du fournisseur.                       |

## Conseils de sélection de modèle

- Préférez le modèle de dernière génération le plus puissant disponible pour chaque capacité média quand la qualité et la sécurité importent.
- Pour les agents activés par outils traitant des entrées non fiables, évitez les modèles média plus anciens/plus faibles.
- Gardez au moins un fallback par capacité pour la disponibilité (modèle de qualité + modèle plus rapide/moins cher).
- Les fallbacks CLI (`whisper-cli`, `whisper`, `gemini`) sont utiles quand les API de fournisseur ne sont pas disponibles.
- Remarque `parakeet-mlx`: avec `--output-dir`, OpenClaw lit `<output-dir>/<media-basename>.txt` quand le format de sortie est `txt` (ou non spécifié); les formats non-`txt` reviennent à stdout.

## Politique de pièces jointes

Par capacité `attachments` contrôle quelles pièces jointes sont traitées :

- `mode`: `first` (par défaut) ou `all`
- `maxAttachments`: limiter le nombre traité (par défaut **1**)
- `prefer`: `first`, `last`, `path`, `url`

Quand `mode: "all"`, les sorties sont étiquetées `[Image 1/2]`, `[Audio 2/2]`, etc.

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

### 2) Audio + Vidéo uniquement (image désactivée)

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

### 3) Compréhension d'image optionnelle

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
          { provider: "anthropic", model: "claude-opus-4-6" },
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

### 4) Entrée multi-modale unique (capacités explicites)

```json5
{
  tools: {
    media: {
      image: {
        models: [
          {
            provider: "google",
            model: "gemini-3.1-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
      audio: {
        models: [
          {
            provider: "google",
            model: "gemini-3.1-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
      video: {
        models: [
          {
            provider: "google",
            model: "gemini-3.1-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
    },
  },
}
```

## Sortie de statut

Quand la compréhension des médias s'exécute, `/status` inclut une ligne de résumé courte :

```
📎 Media: image ok
