---
summary: "Configuration de Cohere (authentification + sélection du modèle)"
title: "Cohere"
read_when:
  - You want to use Cohere with OpenClaw
  - You need the Cohere API key env var or CLI auth choice
---

[Cohere](https://cohere.com) fournit une inférence compatible avec OpenAI via son API de compatibilité. OpenClaw inclut un plugin fournisseur Cohere intégré avec le catalogue de modèles Command A.

| Property        | Value                                    |
| --------------- | ---------------------------------------- |
| Provider id     | `cohere`                                 |
| Plugin          | bundled, `enabledByDefault: true`        |
| Auth env var    | `COHERE_API_KEY`                         |
| Onboarding flag | `--auth-choice cohere-api-key`           |
| Direct CLI flag | `--cohere-api-key <key>`                 |
| API             | OpenAI-compatible (`openai-completions`) |
| Base URL        | `https://api.cohere.ai/compatibility/v1` |
| Default model   | `cohere/command-a-03-2025`               |

## Commencer

1. Créez une clé API Cohere.
2. Exécutez l'intégration :

```bash
openclaw onboard --non-interactive \
  --auth-choice cohere-api-key \
  --cohere-api-key "$COHERE_API_KEY"
```

3. Confirmez que le catalogue est disponible :

```bash
openclaw models list --provider cohere
```

Le modèle par défaut n'est défini que si aucun modèle principal n'est déjà configuré.

## Configuration basée sur l'environnement uniquement

Mettez `COHERE_API_KEY` à disposition du processus Gateway, puis sélectionnez le modèle intégré :

```json5
{
  agents: {
    defaults: {
      model: { primary: "cohere/command-a-03-2025" },
    },
  },
}
```

<Note>
Si la Gateway s'exécute en tant que daemon ou dans Docker, configurez `COHERE_API_KEY` pour ce service. L'exporter uniquement dans un shell interactif ne le rend pas disponible pour une Gateway déjà en cours d'exécution.
</Note>

## Liens connexes

- [Model providers](/fr/concepts/model-providers)
- [Models CLI](/fr/cli/models)
- [Provider directory](/fr/providers)
