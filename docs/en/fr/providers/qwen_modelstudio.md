---
title: "Qwen / Model Studio"
summary: "Configuration d'Alibaba Cloud Model Studio (Plan Standard à l'usage et Plan Coding, points de terminaison multi-régions)"
read_when:
  - You want to use Qwen (Alibaba Cloud Model Studio) with OpenClaw
  - You need the API key env var for Model Studio
  - You want to use the Standard (pay-as-you-go) or Coding Plan endpoint
---

# Qwen / Model Studio (Alibaba Cloud)

Le fournisseur Model Studio donne accès aux modèles Alibaba Cloud, notamment Qwen
et aux modèles tiers hébergés sur la plateforme. Deux plans de facturation sont pris en charge :
**Standard** (à l'usage) et **Plan Coding** (abonnement).

- Fournisseur : `modelstudio`
- Authentification : `MODELSTUDIO_API_KEY`
- API : Compatible OpenAI

## Démarrage rapide

### Standard (à l'usage)

```bash
# Point de terminaison Chine
openclaw onboard --auth-choice modelstudio-standard-api-key-cn

# Point de terminaison Global/International
openclaw onboard --auth-choice modelstudio-standard-api-key
```

### Plan Coding (abonnement)

```bash
# Point de terminaison Chine
openclaw onboard --auth-choice modelstudio-api-key-cn

# Point de terminaison Global/International
openclaw onboard --auth-choice modelstudio-api-key
```

Après l'intégration, définissez un modèle par défaut :

```json5
{
  agents: {
    defaults: {
      model: { primary: "modelstudio/qwen3.5-plus" },
    },
  },
}
```

## Types de plans et points de terminaison

| Plan                       | Région | Choix d'authentification          | Point de terminaison                             |
| -------------------------- | ------ | --------------------------------- | ------------------------------------------------ |
| Standard (à l'usage)       | Chine  | `modelstudio-standard-api-key-cn` | `dashscope.aliyuncs.com/compatible-mode/v1`      |
| Standard (à l'usage)       | Global | `modelstudio-standard-api-key`    | `dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| Plan Coding (abonnement)   | Chine  | `modelstudio-api-key-cn`          | `coding.dashscope.aliyuncs.com/v1`               |
| Plan Coding (abonnement)   | Global | `modelstudio-api-key`             | `coding-intl.dashscope.aliyuncs.com/v1`          |

Le fournisseur sélectionne automatiquement le point de terminaison en fonction de votre choix d'authentification. Vous pouvez
le remplacer avec une `baseUrl` personnalisée dans la configuration.

## Obtenir votre clé API

- **Chine** : [bailian.console.aliyun.com](https://bailian.console.aliyun.com/)
- **Global/International** : [modelstudio.console.alibabacloud.com](https://modelstudio.console.alibabacloud.com/)

## Modèles disponibles

- **qwen3.5-plus** (par défaut) — Qwen 3.5 Plus
- **qwen3-coder-plus**, **qwen3-coder-next** — Modèles de codage Qwen
- **GLM-5** — Modèles GLM via Alibaba
- **Kimi K2.5** — Moonshot AI via Alibaba
- **MiniMax-M2.5** — MiniMax via Alibaba

Certains modèles (qwen3.5-plus, kimi-k2.5) prennent en charge l'entrée d'images. Les fenêtres de contexte vont de 200K à 1M tokens.

## Note sur l'environnement

Si la passerelle s'exécute en tant que démon (launchd/systemd), assurez-vous que
`MODELSTUDIO_API_KEY` est disponible pour ce processus (par exemple, dans
`~/.openclaw/.env` ou via `env.shellEnv`).
