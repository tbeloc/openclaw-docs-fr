---
title: "Model Studio"
summary: "Configuration d'Alibaba Cloud Model Studio (Plan de codage, points de terminaison multi-régions)"
read_when:
  - You want to use Alibaba Cloud Model Studio with OpenClaw
  - You need the API key env var for Model Studio
---

# Model Studio (Alibaba Cloud)

Le fournisseur Model Studio donne accès aux modèles du Plan de codage d'Alibaba Cloud,
y compris Qwen et les modèles tiers hébergés sur la plateforme.

- Fournisseur : `modelstudio`
- Authentification : `MODELSTUDIO_API_KEY`
- API : Compatible OpenAI

## Démarrage rapide

1. Définissez la clé API :

```bash
openclaw onboard --auth-choice modelstudio-api-key
```

2. Définissez un modèle par défaut :

```json5
{
  agents: {
    defaults: {
      model: { primary: "modelstudio/qwen3.5-plus" },
    },
  },
}
```

## Points de terminaison régionaux

Model Studio dispose de deux points de terminaison selon la région :

| Région     | Point de terminaison                 |
| ---------- | ------------------------------------ |
| Chine (CN) | `coding.dashscope.aliyuncs.com`      |
| Global     | `coding-intl.dashscope.aliyuncs.com` |

Le fournisseur sélectionne automatiquement en fonction du choix d'authentification (`modelstudio-api-key` pour
global, `modelstudio-api-key-cn` pour la Chine). Vous pouvez remplacer par une
`baseUrl` personnalisée dans la configuration.

## Modèles disponibles

- **qwen3.5-plus** (par défaut) - Qwen 3.5 Plus
- **qwen3-max** - Qwen 3 Max
- Série **qwen3-coder** - Modèles de codage Qwen
- **GLM-5**, **GLM-4.7** - Modèles GLM via Alibaba
- **Kimi K2.5** - Moonshot AI via Alibaba
- **MiniMax-M2.5** - MiniMax via Alibaba

La plupart des modèles supportent l'entrée d'images. Les fenêtres de contexte vont de 200K à 1M tokens.

## Note sur l'environnement

Si la passerelle s'exécute en tant que démon (launchd/systemd), assurez-vous que
`MODELSTUDIO_API_KEY` est disponible pour ce processus (par exemple, dans
`~/.openclaw/.env` ou via `env.shellEnv`).
