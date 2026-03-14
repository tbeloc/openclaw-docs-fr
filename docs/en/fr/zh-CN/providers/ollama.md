---
read_when:
  - Vous souhaitez exécuter OpenClaw avec des modèles locaux via Ollama
  - Vous avez besoin de conseils d'installation et de configuration d'Ollama
summary: Exécuter OpenClaw via Ollama (runtime LLM local)
title: Ollama
x-i18n:
  generated_at: "2026-02-01T21:35:22Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 157080ad90f449f622260a5f5bd293f79c15800527d36b15596e8ca232e3c957
  source_path: providers/ollama.md
  workflow: 15
---

# Ollama

Ollama est un runtime LLM local qui permet d'exécuter facilement des modèles open source sur votre machine. OpenClaw s'intègre via l'API compatible OpenAI d'Ollama et peut **découvrir automatiquement les modèles supportant l'appel d'outils** lorsque vous l'activez via `OLLAMA_API_KEY` (ou la configuration d'authentification) et qu'aucune entrée explicite `models.providers.ollama` n'est définie.

## Démarrage rapide

1. Installez Ollama : https://ollama.ai

2. Téléchargez un modèle :

```bash
ollama pull llama3.3
# ou
ollama pull qwen2.5-coder:32b
# ou
ollama pull deepseek-r1:32b
```

3. Activez Ollama pour OpenClaw (n'importe quelle valeur fonctionne ; Ollama ne nécessite pas de clé réelle) :

```bash
# Définir la variable d'environnement
export OLLAMA_API_KEY="ollama-local"

# Ou définir dans le fichier de configuration
openclaw config set models.providers.ollama.apiKey "ollama-local"
```

4. Utilisez les modèles Ollama :

```json5
{
  agents: {
    defaults: {
      model: { primary: "ollama/llama3.3" },
    },
  },
}
```

## Découverte de modèles (fournisseur implicite)

Lorsque vous avez défini `OLLAMA_API_KEY` (ou la configuration d'authentification) et que vous **n'avez pas** défini `models.providers.ollama`, OpenClaw découvre les modèles à partir de votre instance Ollama locale `http://127.0.0.1:11434` :

- Interroge `/api/tags` et `/api/show`
- Conserve uniquement les modèles qui rapportent la capacité `tools`
- Marque comme `reasoning` lorsque le modèle rapporte `thinking`
- Lit `contextWindow` depuis `model_info["<arch>.context_length"]` quand disponible
- Définit `maxTokens` à 10 fois la fenêtre de contexte
- Tous les coûts sont définis à `0`

Cela permet d'utiliser les modèles sans configuration manuelle, tout en gardant le répertoire aligné avec les capacités d'Ollama.

Consultez les modèles disponibles :

```bash
ollama list
openclaw models list
```

Pour ajouter un nouveau modèle, téléchargez-le simplement via Ollama :

```bash
ollama pull mistral
```

Le nouveau modèle sera automatiquement découvert et disponible à l'utilisation.

Si vous définissez explicitement `models.providers.ollama`, la découverte automatique sera ignorée et vous devrez définir manuellement les modèles (voir ci-dessous).

## Configuration

### Configuration de base (découverte implicite)

Le moyen le plus simple d'activer Ollama est via une variable d'environnement :

```bash
export OLLAMA_API_KEY="ollama-local"
```

### Configuration explicite (modèles manuels)

Utilisez la configuration explicite dans les cas suivants :

- Ollama s'exécute sur un autre hôte/port.
- Vous souhaitez forcer la spécification de la fenêtre de contexte ou de la liste des modèles.
- Vous souhaitez inclure des modèles qui ne rapportent pas le support des outils.

```json5
{
  models: {
    providers: {
      ollama: {
        // Utilisez l'adresse d'hôte avec /v1 pour la compatibilité avec l'API OpenAI
        baseUrl: "http://ollama-host:11434/v1",
        apiKey: "ollama-local",
        api: "openai-completions",
        models: [
          {
            id: "llama3.3",
            name: "Llama 3.3",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 8192,
            maxTokens: 8192 * 10
          }
        ]
      }
    }
  }
}
```

Si `OLLAMA_API_KEY` est défini, vous pouvez omettre `apiKey` dans l'entrée du fournisseur, et OpenClaw le remplira automatiquement pour les vérifications de disponibilité.

### URL de base personnalisée (configuration explicite)

Si Ollama s'exécute sur un hôte ou un port différent (la configuration explicite désactive la découverte automatique, donc les modèles doivent être définis manuellement) :

```json5
{
  models: {
    providers: {
      ollama: {
        apiKey: "ollama-local",
        baseUrl: "http://ollama-host:11434/v1",
      },
    },
  },
}
```

### Sélection de modèles

Une fois configurés, tous les modèles Ollama sont disponibles :

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "ollama/llama3.3",
        fallbacks: ["ollama/qwen2.5-coder:32b"],
      },
    },
  },
}
```

## Utilisation avancée

### Modèles de raisonnement

Lorsqu'Ollama rapporte `thinking` dans `/api/show`, OpenClaw marque le modèle comme ayant des capacités de raisonnement :

```bash
ollama pull deepseek-r1:32b
```

### Coûts des modèles

Ollama est gratuit et s'exécute localement, donc tous les coûts des modèles sont définis à $0.

### Fenêtre de contexte

Pour les modèles découverts automatiquement, OpenClaw utilise la fenêtre de contexte rapportée par Ollama (si disponible), sinon par défaut à `8192`. Vous pouvez remplacer `contextWindow` et `maxTokens` dans la configuration explicite du fournisseur.

## Dépannage

### Ollama n'est pas détecté

Assurez-vous qu'Ollama est en cours d'exécution, que vous avez défini `OLLAMA_API_KEY` (ou la configuration d'authentification), et qu'aucune entrée explicite `models.providers.ollama` n'est définie :

```bash
ollama serve
```

Confirmez également que l'API est accessible :

```bash
curl http://localhost:11434/api/tags
```

### Aucun modèle disponible

OpenClaw découvre automatiquement uniquement les modèles qui rapportent le support des outils. Si votre modèle n'est pas listé, vous pouvez :

- Télécharger un modèle qui supporte l'appel d'outils, ou
- Définir explicitement le modèle dans `models.providers.ollama`.

Ajouter un modèle :

```bash
ollama list  # Voir les modèles installés
ollama pull llama3.3  # Télécharger un modèle
```

### Connexion refusée

Vérifiez qu'Ollama s'exécute sur le bon port :

```bash
# Vérifier si Ollama est en cours d'exécution
ps aux | grep ollama

# Ou redémarrer Ollama
ollama serve
```

## Voir aussi

- [Fournisseurs de modèles](/concepts/model-providers) - Aperçu de tous les fournisseurs
- [Sélection de modèles](/concepts/models) - Comment choisir un modèle
- [Configuration](/gateway/configuration) - Référence de configuration complète
