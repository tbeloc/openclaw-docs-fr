---
summary: "Configuration DeepSeek (authentification + sélection du modèle)"
read_when:
  - You want to use DeepSeek with OpenClaw
  - You need the API key env var or CLI auth choice
---

# DeepSeek

[DeepSeek](https://www.deepseek.com) fournit des modèles d'IA puissants avec une API compatible OpenAI.

- Provider: `deepseek`
- Auth: `DEEPSEEK_API_KEY`
- API: Compatible OpenAI

## Démarrage rapide

Définissez la clé API (recommandé : la stocker pour la Gateway) :

```bash
openclaw onboard --auth-choice deepseek-api-key
```

Cela vous demandera votre clé API et définira `deepseek/deepseek-chat` comme modèle par défaut.

## Exemple non-interactif

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice deepseek-api-key \
  --deepseek-api-key "$DEEPSEEK_API_KEY" \
  --skip-health \
  --accept-risk
```

## Note sur l'environnement

Si la Gateway s'exécute en tant que daemon (launchd/systemd), assurez-vous que `DEEPSEEK_API_KEY`
est disponible pour ce processus (par exemple, dans `~/.openclaw/.env` ou via
`env.shellEnv`).

## Modèles disponibles

| Model ID            | Name                     | Type      | Context |
| ------------------- | ------------------------ | --------- | ------- |
| `deepseek-chat`     | DeepSeek Chat (V3.2)     | General   | 128K    |
| `deepseek-reasoner` | DeepSeek Reasoner (V3.2) | Reasoning | 128K    |

- **deepseek-chat** correspond à DeepSeek-V3.2 en mode non-thinking.
- **deepseek-reasoner** correspond à DeepSeek-V3.2 en mode thinking avec raisonnement en chaîne de pensée.

Obtenez votre clé API sur [platform.deepseek.com](https://platform.deepseek.com/api_keys).
