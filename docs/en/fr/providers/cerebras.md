---
summary: "Configuration de Cerebras (authentification + sélection du modèle)"
title: "Cerebras"
read_when:
  - You want to use Cerebras with OpenClaw
  - You need the Cerebras API key env var or CLI auth choice
---

[Cerebras](https://www.cerebras.ai) fournit une inférence haute vitesse compatible avec OpenAI.

| Propriété | Valeur                       |
| --------- | ---------------------------- |
| Provider  | `cerebras`                   |
| Auth      | `CEREBRAS_API_KEY`           |
| API       | Compatible OpenAI            |
| Base URL  | `https://api.cerebras.ai/v1` |

## Démarrage

<Steps>
  <Step title="Obtenir une clé API">
    Créez une clé API dans la [Console Cloud Cerebras](https://cloud.cerebras.ai).
  </Step>
  <Step title="Exécuter l'intégration">
    ```bash
    openclaw onboard --auth-choice cerebras-api-key
    ```
  </Step>
  <Step title="Vérifier que les modèles sont disponibles">
    ```bash
    openclaw models list --provider cerebras
    ```
  </Step>
</Steps>

### Configuration non-interactive

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice cerebras-api-key \
  --cerebras-api-key "$CEREBRAS_API_KEY"
```

## Catalogue intégré

OpenClaw inclut un catalogue Cerebras statique pour le point de terminaison public compatible OpenAI :

| Référence du modèle                       | Nom                  | Notes                                           |
| ----------------------------------------- | -------------------- | ----------------------------------------------- |
| `cerebras/zai-glm-4.7`                    | Z.ai GLM 4.7         | Modèle par défaut ; modèle de raisonnement en aperçu |
| `cerebras/gpt-oss-120b`                   | GPT OSS 120B         | Modèle de raisonnement en production             |
| `cerebras/qwen-3-235b-a22b-instruct-2507` | Qwen 3 235B Instruct | Modèle sans raisonnement en aperçu              |
| `cerebras/llama3.1-8b`                    | Llama 3.1 8B         | Modèle axé sur la vitesse en production         |

<Warning>
Cerebras marque `zai-glm-4.7` et `qwen-3-235b-a22b-instruct-2507` comme des modèles en aperçu, et `llama3.1-8b` / `qwen-3-235b-a22b-instruct-2507` sont documentés pour une dépréciation le 27 mai 2026. Consultez la page des modèles supportés de Cerebras avant de les utiliser en production.
</Warning>

## Configuration manuelle

Le plugin fourni signifie généralement que vous n'avez besoin que de la clé API. Utilisez la configuration explicite `models.providers.cerebras` lorsque vous souhaitez remplacer les métadonnées du modèle :

```json5
{
  env: { CEREBRAS_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "cerebras/zai-glm-4.7" },
    },
  },
  models: {
    mode: "merge",
    providers: {
      cerebras: {
        baseUrl: "https://api.cerebras.ai/v1",
        apiKey: "${CEREBRAS_API_KEY}",
        api: "openai-completions",
        models: [
          { id: "zai-glm-4.7", name: "Z.ai GLM 4.7" },
          { id: "gpt-oss-120b", name: "GPT OSS 120B" },
        ],
      },
    },
  },
}
```

<Note>
Si la passerelle s'exécute en tant que démon (launchd/systemd), assurez-vous que `CEREBRAS_API_KEY`
est disponible pour ce processus, par exemple dans `~/.openclaw/.env` ou via
`env.shellEnv`.
</Note>
