---
summary: "Utilisez l'API unifiée de DeepInfra pour accéder aux modèles open source et frontier les plus populaires dans OpenClaw"
read_when:
  - Vous voulez une seule clé API pour les meilleurs LLMs open source
  - Vous voulez exécuter des modèles via l'API de DeepInfra dans OpenClaw
---

# DeepInfra

DeepInfra fournit une **API unifiée** qui achemine les requêtes vers les modèles open source et frontier les plus populaires derrière un seul
endpoint et une seule clé API. Elle est compatible avec OpenAI, donc la plupart des SDKs OpenAI fonctionnent en changeant l'URL de base.

## Obtenir une clé API

1. Allez sur [https://deepinfra.com/](https://deepinfra.com/)
2. Connectez-vous ou créez un compte
3. Accédez à Dashboard / Keys et générez une nouvelle clé API ou utilisez celle créée automatiquement

## Configuration CLI

```bash
openclaw onboard --deepinfra-api-key <key>
```

Ou définissez la variable d'environnement :

```bash
export DEEPINFRA_API_KEY="<your-deepinfra-api-key>" # pragma: allowlist secret
```

## Extrait de configuration

```json5
{
  env: { DEEPINFRA_API_KEY: "<your-deepinfra-api-key>" }, // pragma: allowlist secret
  agents: {
    defaults: {
      model: { primary: "deepinfra/deepseek-ai/DeepSeek-V3.2" },
    },
  },
}
```

## Surfaces OpenClaw supportées

Le plugin fourni enregistre toutes les surfaces DeepInfra qui correspondent aux contrats de fournisseur OpenClaw actuels :

| Surface                  | Modèle par défaut                  | Configuration/outil OpenClaw                             |
| ------------------------ | ---------------------------------- | -------------------------------------------------------- |
| Chat / fournisseur de modèle | `deepseek-ai/DeepSeek-V3.2`        | `agents.defaults.model`                                  |
| Génération/édition d'images | `black-forest-labs/FLUX-1-schnell` | `image_generate`, `agents.defaults.imageGenerationModel` |
| Compréhension des médias      | `moonshotai/Kimi-K2.5` pour les images  | compréhension d'image entrante                              |
| Reconnaissance vocale           | `openai/whisper-large-v3-turbo`    | transcription audio entrante                              |
| Synthèse vocale           | `hexgrad/Kokoro-82M`               | `messages.tts.provider: "deepinfra"`                     |
| Génération vidéo         | `Pixverse/Pixverse-T2V`            | `video_generate`, `agents.defaults.videoGenerationModel` |
| Embeddings de mémoire        | `BAAI/bge-m3`                      | `agents.defaults.memorySearch.provider: "deepinfra"`     |

DeepInfra expose également le reclassement, la classification, la détection d'objets et d'autres
types de modèles natifs. OpenClaw n'a pas actuellement de contrats de fournisseur de première classe
pour ces catégories, donc ce plugin ne les enregistre pas encore.

## Modèles disponibles

OpenClaw découvre dynamiquement les modèles DeepInfra disponibles au démarrage. Utilisez
`/models deepinfra` pour voir la liste complète des modèles disponibles.

Tout modèle disponible sur [DeepInfra.com](https://deepinfra.com/) peut être utilisé avec le préfixe `deepinfra/` :

```
deepinfra/MiniMaxAI/MiniMax-M2.5
deepinfra/deepseek-ai/DeepSeek-V3.2
deepinfra/moonshotai/Kimi-K2.5
deepinfra/zai-org/GLM-5.1
...et bien d'autres
```

## Notes

- Les références de modèle sont `deepinfra/<provider>/<model>` (par exemple, `deepinfra/Qwen/Qwen3-Max`).
- Modèle par défaut : `deepinfra/deepseek-ai/DeepSeek-V3.2`
- URL de base : `https://api.deepinfra.com/v1/openai`
- La génération vidéo native utilise `https://api.deepinfra.com/v1/inference/<model>`.
