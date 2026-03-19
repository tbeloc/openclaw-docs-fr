---
title: "Volcengine (Doubao)"
summary: "Configuration de Volcano Engine (modèles Doubao, points de terminaison généraux + codage)"
read_when:
  - Vous souhaitez utiliser Volcano Engine ou les modèles Doubao avec OpenClaw
  - Vous avez besoin de la configuration de la clé API Volcengine
---

# Volcengine (Doubao)

Le fournisseur Volcengine donne accès aux modèles Doubao et aux modèles tiers
hébergés sur Volcano Engine, avec des points de terminaison séparés pour les
charges de travail générales et de codage.

- Fournisseurs : `volcengine` (général) + `volcengine-plan` (codage)
- Authentification : `VOLCANO_ENGINE_API_KEY`
- API : Compatible OpenAI

## Démarrage rapide

1. Définissez la clé API :

```bash
openclaw onboard --auth-choice volcengine-api-key
```

2. Définissez un modèle par défaut :

```json5
{
  agents: {
    defaults: {
      model: { primary: "volcengine-plan/ark-code-latest" },
    },
  },
}
```

## Exemple non-interactif

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice volcengine-api-key \
  --volcengine-api-key "$VOLCANO_ENGINE_API_KEY"
```

## Fournisseurs et points de terminaison

| Fournisseur       | Point de terminaison                      | Cas d'usage    |
| ----------------- | ----------------------------------------- | -------------- |
| `volcengine`      | `ark.cn-beijing.volces.com/api/v3`        | Modèles généraux |
| `volcengine-plan` | `ark.cn-beijing.volces.com/api/coding/v3` | Modèles de codage |

Les deux fournisseurs sont configurés à partir d'une seule clé API. La
configuration enregistre les deux automatiquement.

## Modèles disponibles

- **doubao-seed-1-8** - Doubao Seed 1.8 (général, par défaut)
- **doubao-seed-code-preview** - Modèle de codage Doubao
- **ark-code-latest** - Valeur par défaut du plan de codage
- **Kimi K2.5** - Moonshot AI via Volcano Engine
- **GLM-4.7** - GLM via Volcano Engine
- **DeepSeek V3.2** - DeepSeek via Volcano Engine

La plupart des modèles supportent l'entrée texte + image. Les fenêtres de
contexte vont de 128K à 256K tokens.

## Note sur l'environnement

Si la passerelle s'exécute en tant que démon (launchd/systemd), assurez-vous
que `VOLCANO_ENGINE_API_KEY` est disponible pour ce processus (par exemple,
dans `~/.openclaw/.env` ou via `env.shellEnv`).
