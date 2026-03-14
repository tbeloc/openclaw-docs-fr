---
read_when:
  - Vous souhaitez utiliser la transcription vocale Deepgram pour traiter les pièces jointes audio
  - Vous avez besoin d'un exemple de configuration Deepgram rapide
summary: Transcription vocale Deepgram pour recevoir les messages vocaux
title: Deepgram
x-i18n:
  generated_at: "2026-02-01T21:34:47Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 8f19e072f08672116ed1a72578635c0dcebb2b1f0dfcbefa12f80b21a18ad25c
  source_path: providers/deepgram.md
  workflow: 15
---

# Deepgram (Transcription audio)

Deepgram est une API de conversion de la parole en texte. Dans OpenClaw, elle est utilisée via `tools.media.audio` pour **recevoir la transcription des messages audio/vocaux**.

Une fois activée, OpenClaw télécharge le fichier audio vers Deepgram et injecte le texte transcrit dans le pipeline de réponse (bloc `{{Transcript}}` + `[Audio]`). Ce n'est **pas du streaming** ; il utilise le point de terminaison de transcription audio pré-enregistré.

Site web : https://deepgram.com  
Documentation : https://developers.deepgram.com

## Démarrage rapide

1. Configurez votre clé API :

```
DEEPGRAM_API_KEY=dg_...
```

2. Activez le fournisseur :

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

## Options

- `model` : ID du modèle Deepgram (par défaut : `nova-3`)
- `language` : Indice de langue (optionnel)
- `tools.media.audio.providerOptions.deepgram.detect_language` : Activer la détection de langue (optionnel)
- `tools.media.audio.providerOptions.deepgram.punctuate` : Activer la ponctuation (optionnel)
- `tools.media.audio.providerOptions.deepgram.smart_format` : Activer le formatage intelligent (optionnel)

Exemple avec paramètre de langue :

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "deepgram", model: "nova-3", language: "en" }],
      },
    },
  },
}
```

Exemple avec options Deepgram :

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        providerOptions: {
          deepgram: {
            detect_language: true,
            punctuate: true,
            smart_format: true,
          },
        },
        models: [{ provider: "deepgram", model: "nova-3" }],
      },
    },
  },
}
```

## Remarques

- L'authentification suit l'ordre d'authentification standard du fournisseur ; `DEEPGRAM_API_KEY` est le moyen le plus simple.
- Lors de l'utilisation d'un proxy, vous pouvez remplacer le point de terminaison ou les en-têtes de requête via `tools.media.audio.baseUrl` et `tools.media.audio.headers`.
- La sortie suit les mêmes règles audio que les autres fournisseurs (limites de taille, délais d'expiration, injection de texte transcrit).
