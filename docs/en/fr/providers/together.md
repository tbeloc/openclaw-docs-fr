---
summary: "Configuration de Together AI (authentification + sélection du modèle)"
read_when:
  - Vous voulez utiliser Together AI avec OpenClaw
  - Vous avez besoin de la variable d'environnement de clé API ou du choix d'authentification CLI
---

# Together AI

[Together AI](https://together.ai) fournit un accès aux principaux modèles open-source, notamment Llama, DeepSeek, Kimi, et bien d'autres, via une API unifiée.

- Fournisseur : `together`
- Authentification : `TOGETHER_API_KEY`
- API : Compatible OpenAI

## Démarrage rapide

1. Définissez la clé API (recommandé : la stocker pour la Gateway) :

```bash
openclaw onboard --auth-choice together-api-key
```

2. Définissez un modèle par défaut :

```json5
{
  agents: {
    defaults: {
      model: { primary: "together/moonshotai/Kimi-K2.5" },
    },
  },
}
```

## Exemple non-interactif

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice together-api-key \
  --together-api-key "$TOGETHER_API_KEY"
```

Cela définira `together/moonshotai/Kimi-K2.5` comme modèle par défaut.

## Note sur l'environnement

Si la Gateway s'exécute en tant que daemon (launchd/systemd), assurez-vous que `TOGETHER_API_KEY`
est disponible pour ce processus (par exemple, dans `~/.openclaw/.env` ou via
`env.shellEnv`).

## Modèles disponibles

Together AI fournit un accès à de nombreux modèles open-source populaires :

- **GLM 4.7 Fp8** - Modèle par défaut avec fenêtre de contexte de 200K
- **Llama 3.3 70B Instruct Turbo** - Suivi d'instructions rapide et efficace
- **Llama 4 Scout** - Modèle de vision avec compréhension d'images
- **Llama 4 Maverick** - Vision avancée et raisonnement
- **DeepSeek V3.1** - Modèle puissant de codage et raisonnement
- **DeepSeek R1** - Modèle de raisonnement avancé
- **Kimi K2 Instruct** - Modèle haute performance avec fenêtre de contexte de 262K

Tous les modèles supportent les complétions de chat standard et sont compatibles avec l'API OpenAI.
