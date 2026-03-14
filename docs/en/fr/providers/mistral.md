---
summary: "Utiliser les modèles Mistral et la transcription Voxtral avec OpenClaw"
read_when:
  - Vous souhaitez utiliser les modèles Mistral dans OpenClaw
  - Vous avez besoin de l'intégration de la clé API Mistral et des références de modèles
title: "Mistral"
---

# Mistral

OpenClaw supporte Mistral pour le routage des modèles texte/image (`mistral/...`) et
la transcription audio via Voxtral dans la compréhension des médias.
Mistral peut également être utilisé pour les embeddings de mémoire (`memorySearch.provider = "mistral"`).

## Configuration CLI

```bash
openclaw onboard --auth-choice mistral-api-key
# ou non-interactif
openclaw onboard --mistral-api-key "$MISTRAL_API_KEY"
```

## Extrait de configuration (fournisseur LLM)

```json5
{
  env: { MISTRAL_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "mistral/mistral-large-latest" } } },
}
```

## Extrait de configuration (transcription audio avec Voxtral)

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

## Notes

- L'authentification Mistral utilise `MISTRAL_API_KEY`.
- L'URL de base du fournisseur par défaut est `https://api.mistral.ai/v1`.
- Le modèle par défaut de l'intégration est `mistral/mistral-large-latest`.
- Le modèle audio par défaut de compréhension des médias pour Mistral est `voxtral-mini-latest`.
- Le chemin de transcription des médias utilise `/v1/audio/transcriptions`.
- Le chemin des embeddings de mémoire utilise `/v1/embeddings` (modèle par défaut : `mistral-embed`).
