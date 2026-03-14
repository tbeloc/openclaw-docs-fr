---
summary: "Transcription Deepgram pour les notes vocales entrantes"
read_when:
  - You want Deepgram speech-to-text for audio attachments
  - You need a quick Deepgram config example
title: "Deepgram"
---

# Deepgram (Transcription audio)

Deepgram est une API de reconnaissance vocale. Dans OpenClaw, elle est utilisée pour la **transcription audio/notes vocales entrantes** via `tools.media.audio`.

Lorsqu'elle est activée, OpenClaw télécharge le fichier audio vers Deepgram et injecte la transcription dans le pipeline de réponse (`{{Transcript}}` + bloc `[Audio]`). Ce n'est **pas du streaming** ; cela utilise le point de terminaison de transcription pré-enregistrée.

Site web : [https://deepgram.com](https://deepgram.com)  
Documentation : [https://developers.deepgram.com](https://developers.deepgram.com)

## Démarrage rapide

1. Définissez votre clé API :

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

- `model`: identifiant du modèle Deepgram (par défaut : `nova-3`)
- `language`: indice de langue (optionnel)
- `tools.media.audio.providerOptions.deepgram.detect_language`: activer la détection de langue (optionnel)
- `tools.media.audio.providerOptions.deepgram.punctuate`: activer la ponctuation (optionnel)
- `tools.media.audio.providerOptions.deepgram.smart_format`: activer le formatage intelligent (optionnel)

Exemple avec langue :

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

## Notes

- L'authentification suit l'ordre d'authentification standard du fournisseur ; `DEEPGRAM_API_KEY` est le chemin le plus simple.
- Remplacez les points de terminaison ou les en-têtes avec `tools.media.audio.baseUrl` et `tools.media.audio.headers` lors de l'utilisation d'un proxy.
- La sortie suit les mêmes règles audio que les autres fournisseurs (limites de taille, délais d'expiration, injection de transcription).
