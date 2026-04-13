---
summary: "Exécuter OpenClaw avec LM Studio"
read_when:
  - You want to run OpenClaw with open source models via LM Studio
  - You want to set up and configure LM Studio
title: "LM Studio"
---

# LM Studio

LM Studio est une application conviviale mais puissante pour exécuter des modèles open-weight sur votre propre matériel. Elle vous permet d'exécuter des modèles llama.cpp (GGUF) ou MLX (Apple Silicon). Elle est disponible en tant qu'application GUI ou daemon sans interface (`llmster`). Pour la documentation produit et de configuration, consultez [lmstudio.ai](https://lmstudio.ai/).

## Démarrage rapide

1. Installez LM Studio (bureau) ou `llmster` (sans interface), puis démarrez le serveur local :

```bash
curl -fsSL https://lmstudio.ai/install.sh | bash
```

2. Démarrez le serveur

Assurez-vous de démarrer l'application de bureau ou d'exécuter le daemon à l'aide de la commande suivante :

```bash
lms daemon up
```

```bash
lms server start --port 1234
```

Si vous utilisez l'application, assurez-vous que JIT est activé pour une expérience fluide. En savoir plus dans le [guide LM Studio JIT et TTL](https://lmstudio.ai/docs/developer/core/ttl-and-auto-evict).

3. OpenClaw nécessite une valeur de token LM Studio. Définissez `LM_API_TOKEN` :

```bash
export LM_API_TOKEN="your-lm-studio-api-token"
```

Si l'authentification LM Studio est désactivée, utilisez n'importe quelle valeur de token non vide :

```bash
export LM_API_TOKEN="placeholder-key"
```

Pour plus de détails sur la configuration de l'authentification LM Studio, consultez [LM Studio Authentication](https://lmstudio.ai/docs/developer/core/authentication).

4. Exécutez l'intégration et choisissez `LM Studio` :

```bash
openclaw onboard
```

5. Lors de l'intégration, utilisez l'invite `Default model` pour sélectionner votre modèle LM Studio.

Vous pouvez également le définir ou le modifier ultérieurement :

```bash
openclaw models set lmstudio/qwen/qwen3.5-9b
```

Les clés de modèle LM Studio suivent un format `author/model-name` (par exemple `qwen/qwen3.5-9b`). Les références de modèle OpenClaw ajoutent le nom du fournisseur : `lmstudio/qwen/qwen3.5-9b`. Vous pouvez trouver la clé exacte d'un modèle en exécutant `curl http://localhost:1234/api/v1/models` et en regardant le champ `key`.

## Intégration non interactive

Utilisez l'intégration non interactive lorsque vous souhaitez automatiser la configuration (CI, provisionnement, bootstrap à distance) :

```bash
openclaw onboard \
  --non-interactive \
  --accept-risk \
  --auth-choice lmstudio
```

Ou spécifiez l'URL de base ou le modèle avec la clé API :

```bash
openclaw onboard \
  --non-interactive \
  --accept-risk \
  --auth-choice lmstudio \
  --custom-base-url http://localhost:1234/v1 \
  --lmstudio-api-key "$LM_API_TOKEN" \
  --custom-model-id qwen/qwen3.5-9b
```

`--custom-model-id` prend la clé de modèle telle que retournée par LM Studio (par exemple `qwen/qwen3.5-9b`), sans le préfixe du fournisseur `lmstudio/`.

L'intégration non interactive nécessite `--lmstudio-api-key` (ou `LM_API_TOKEN` dans l'environnement).
Pour les serveurs LM Studio non authentifiés, n'importe quelle valeur de token non vide fonctionne.

`--custom-api-key` reste supporté pour la compatibilité, mais `--lmstudio-api-key` est préféré pour LM Studio.

Cela écrit `models.providers.lmstudio`, définit le modèle par défaut sur
`lmstudio/<custom-model-id>`, et écrit le profil d'authentification `lmstudio:default`.

La configuration interactive peut demander une longueur de contexte de chargement préférée optionnelle et l'applique à tous les modèles LM Studio découverts qu'elle enregistre dans la configuration.

## Configuration

### Configuration explicite

```json5
{
  models: {
    providers: {
      lmstudio: {
        baseUrl: "http://localhost:1234/v1",
        apiKey: "${LM_API_TOKEN}",
        api: "openai-completions",
        models: [
          {
            id: "qwen/qwen3-coder-next",
            name: "Qwen 3 Coder Next",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Dépannage

### LM Studio non détecté

Assurez-vous que LM Studio est en cours d'exécution et que vous avez défini `LM_API_TOKEN` (pour les serveurs non authentifiés, n'importe quelle valeur de token non vide fonctionne) :

```bash
# Démarrez via l'application de bureau, ou sans interface :
lms server start --port 1234
```

Vérifiez que l'API est accessible :

```bash
curl http://localhost:1234/api/v1/models
```

### Erreurs d'authentification (HTTP 401)

Si la configuration signale HTTP 401, vérifiez votre clé API :

- Vérifiez que `LM_API_TOKEN` correspond à la clé configurée dans LM Studio.
- Pour plus de détails sur la configuration de l'authentification LM Studio, consultez [LM Studio Authentication](https://lmstudio.ai/docs/developer/core/authentication).
- Si votre serveur ne nécessite pas d'authentification, utilisez n'importe quelle valeur de token non vide pour `LM_API_TOKEN`.

### Chargement de modèle juste-à-temps

LM Studio supporte le chargement de modèle juste-à-temps (JIT), où les modèles sont chargés à la première demande. Assurez-vous que cela est activé pour éviter les erreurs « Model not loaded ».
