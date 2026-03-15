---
summary: "Utilisez l'API compatible OpenAI de NVIDIA dans OpenClaw"
read_when:
  - You want to use NVIDIA models in OpenClaw
  - You need NVIDIA_API_KEY setup
title: "NVIDIA"
---

# NVIDIA

NVIDIA fournit une API compatible OpenAI à `https://integrate.api.nvidia.com/v1` pour les modèles Nemotron et NeMo. Authentifiez-vous avec une clé API de [NVIDIA NGC](https://catalog.ngc.nvidia.com/).

## Configuration CLI

Exportez la clé une fois, puis exécutez l'intégration et définissez un modèle NVIDIA :

```bash
export NVIDIA_API_KEY="nvapi-..."
openclaw onboard --auth-choice skip
openclaw models set nvidia/nvidia/llama-3.1-nemotron-70b-instruct
```

Si vous passez toujours `--token`, rappelez-vous qu'il se retrouve dans l'historique du shell et la sortie de `ps` ; préférez la variable d'environnement si possible.

## Extrait de configuration

```json5
{
  env: { NVIDIA_API_KEY: "nvapi-..." },
  models: {
    providers: {
      nvidia: {
        baseUrl: "https://integrate.api.nvidia.com/v1",
        api: "openai-completions",
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "nvidia/nvidia/llama-3.1-nemotron-70b-instruct" },
    },
  },
}
```

## IDs de modèles

- `nvidia/llama-3.1-nemotron-70b-instruct` (par défaut)
- `meta/llama-3.3-70b-instruct`
- `nvidia/mistral-nemo-minitron-8b-8k-instruct`

## Notes

- Point de terminaison `/v1` compatible OpenAI ; utilisez une clé API de NVIDIA NGC.
- Le fournisseur s'active automatiquement lorsque `NVIDIA_API_KEY` est défini ; utilise les paramètres par défaut statiques (fenêtre de contexte de 131 072 jetons, 4 096 jetons maximum).
