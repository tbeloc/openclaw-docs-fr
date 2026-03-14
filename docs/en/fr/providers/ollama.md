---
summary: "Exécuter OpenClaw avec Ollama (modèles cloud et locaux)"
read_when:
  - You want to run OpenClaw with cloud or local models via Ollama
  - You need Ollama setup and configuration guidance
title: "Ollama"
---

# Ollama

Ollama est un runtime LLM local qui facilite l'exécution de modèles open-source sur votre machine. OpenClaw s'intègre à l'API native d'Ollama (`/api/chat`), supporte le streaming et l'appel d'outils, et peut découvrir automatiquement les modèles Ollama locaux lorsque vous optez pour `OLLAMA_API_KEY` (ou un profil d'authentification) et ne définissez pas d'entrée explicite `models.providers.ollama`.

<Warning>
**Utilisateurs d'Ollama distant** : N'utilisez pas l'URL compatible OpenAI `/v1` (`http://host:11434/v1`) avec OpenClaw. Cela casse l'appel d'outils et les modèles peuvent afficher le JSON brut des outils en tant que texte brut. Utilisez plutôt l'URL native de l'API Ollama : `baseUrl: "http://host:11434"` (sans `/v1`).
</Warning>

## Démarrage rapide

### Assistant d'intégration (recommandé)

Le moyen le plus rapide de configurer Ollama est via l'assistant d'intégration :

```bash
openclaw onboard
```

Sélectionnez **Ollama** dans la liste des fournisseurs. L'assistant va :

1. Demander l'URL de base d'Ollama où votre instance peut être atteinte (par défaut `http://127.0.0.1:11434`).
2. Vous laisser choisir entre **Cloud + Local** (modèles cloud et locaux) ou **Local** (modèles locaux uniquement).
3. Ouvrir un flux de connexion au navigateur si vous choisissez **Cloud + Local** et n'êtes pas connecté à ollama.com.
4. Découvrir les modèles disponibles et suggérer des valeurs par défaut.
5. Télécharger automatiquement le modèle sélectionné s'il n'est pas disponible localement.

Le mode non-interactif est également supporté :

```bash
openclaw onboard --non-interactive \
  --auth-choice ollama \
  --accept-risk
```

Spécifiez optionnellement une URL de base personnalisée ou un modèle :

```bash
openclaw onboard --non-interactive \
  --auth-choice ollama \
  --custom-base-url "http://ollama-host:11434" \
  --custom-model-id "qwen3.5:27b" \
  --accept-risk
```

### Configuration manuelle

1. Installez Ollama : [https://ollama.com/download](https://ollama.com/download)

2. Téléchargez un modèle local si vous voulez l'inférence locale :

```bash
ollama pull glm-4.7-flash
# ou
ollama pull gpt-oss:20b
# ou
ollama pull llama3.3
```

3. Si vous voulez aussi des modèles cloud, connectez-vous :

```bash
ollama signin
```

4. Exécutez l'intégration et choisissez `Ollama` :

```bash
openclaw onboard
```

- `Local` : modèles locaux uniquement
- `Cloud + Local` : modèles locaux plus modèles cloud
- Les modèles cloud tels que `kimi-k2.5:cloud`, `minimax-m2.5:cloud`, et `glm-5:cloud` ne nécessitent **pas** un `ollama pull` local

OpenClaw suggère actuellement :

- défaut local : `glm-4.7-flash`
- défauts cloud : `kimi-k2.5:cloud`, `minimax-m2.5:cloud`, `glm-5:cloud`

5. Si vous préférez la configuration manuelle, activez Ollama pour OpenClaw directement (n'importe quelle valeur fonctionne ; Ollama ne nécessite pas une vraie clé) :

```bash
# Définir la variable d'environnement
export OLLAMA_API_KEY="ollama-local"

# Ou configurer dans votre fichier de configuration
openclaw config set models.providers.ollama.apiKey "ollama-local"
```

6. Inspectez ou changez les modèles :

```bash
openclaw models list
openclaw models set ollama/glm-4.7-flash
```

7. Ou définissez la valeur par défaut dans la configuration :

```json5
{
  agents: {
    defaults: {
      model: { primary: "ollama/glm-4.7-flash" },
    },
  },
}
```

## Découverte de modèles (fournisseur implicite)

Lorsque vous définissez `OLLAMA_API_KEY` (ou un profil d'authentification) et que vous **ne** définissez **pas** `models.providers.ollama`, OpenClaw découvre les modèles à partir de l'instance Ollama locale à `http://127.0.0.1:11434` :

- Interroge `/api/tags`
- Utilise les recherches `/api/show` au mieux pour lire `contextWindow` quand disponible
- Marque `reasoning` avec une heuristique de nom de modèle (`r1`, `reasoning`, `think`)
- Définit `maxTokens` à la limite de jetons max par défaut d'Ollama utilisée par OpenClaw
- Définit tous les coûts à `0`

Cela évite les entrées de modèles manuelles tout en gardant le catalogue aligné avec l'instance Ollama locale.

Pour voir quels modèles sont disponibles :

```bash
ollama list
openclaw models list
```

Pour ajouter un nouveau modèle, téléchargez-le simplement avec Ollama :

```bash
ollama pull mistral
```

Le nouveau modèle sera automatiquement découvert et disponible à l'utilisation.

Si vous définissez `models.providers.ollama` explicitement, la découverte automatique est ignorée et vous devez définir les modèles manuellement (voir ci-dessous).

## Configuration

### Configuration de base (découverte implicite)

Le moyen le plus simple d'activer Ollama est via une variable d'environnement :

```bash
export OLLAMA_API_KEY="ollama-local"
```

### Configuration explicite (modèles manuels)

Utilisez la configuration explicite quand :

- Ollama s'exécute sur un autre hôte/port.
- Vous voulez forcer des fenêtres de contexte spécifiques ou des listes de modèles.
- Vous voulez des définitions de modèles entièrement manuelles.

```json5
{
  models: {
    providers: {
      ollama: {
        baseUrl: "http://ollama-host:11434",
        apiKey: "ollama-local",
        api: "ollama",
        models: [
          {
            id: "gpt-oss:20b",
            name: "GPT-OSS 20B",
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

Si `OLLAMA_API_KEY` est défini, vous pouvez omettre `apiKey` dans l'entrée du fournisseur et OpenClaw le remplira pour les vérifications de disponibilité.

### URL de base personnalisée (configuration explicite)

Si Ollama s'exécute sur un hôte ou un port différent (la configuration explicite désactive la découverte automatique, donc définissez les modèles manuellement) :

```json5
{
  models: {
    providers: {
      ollama: {
        apiKey: "ollama-local",
        baseUrl: "http://ollama-host:11434", // Pas de /v1 - utilisez l'URL native de l'API Ollama
        api: "ollama", // Définir explicitement pour garantir le comportement natif d'appel d'outils
      },
    },
  },
}
```

<Warning>
N'ajoutez pas `/v1` à l'URL. Le chemin `/v1` utilise le mode compatible OpenAI, où l'appel d'outils n'est pas fiable. Utilisez l'URL Ollama de base sans suffixe de chemin.
</Warning>

### Sélection de modèle

Une fois configuré, tous vos modèles Ollama sont disponibles :

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "ollama/gpt-oss:20b",
        fallbacks: ["ollama/llama3.3", "ollama/qwen2.5-coder:32b"],
      },
    },
  },
}
```

## Modèles cloud

Les modèles cloud vous permettent d'exécuter des modèles hébergés dans le cloud (par exemple `kimi-k2.5:cloud`, `minimax-m2.5:cloud`, `glm-5:cloud`) aux côtés de vos modèles locaux.

Pour utiliser les modèles cloud, sélectionnez le mode **Cloud + Local** lors de l'intégration. L'assistant vérifie si vous êtes connecté et ouvre un flux de connexion au navigateur si nécessaire. Si l'authentification ne peut pas être vérifiée, l'assistant revient aux défauts de modèles locaux.

Vous pouvez également vous connecter directement à [ollama.com/signin](https://ollama.com/signin).

## Avancé

### Modèles de raisonnement

OpenClaw traite les modèles avec des noms tels que `deepseek-r1`, `reasoning`, ou `think` comme capables de raisonnement par défaut :

```bash
ollama pull deepseek-r1:32b
```

### Coûts des modèles

Ollama est gratuit et s'exécute localement, donc tous les coûts des modèles sont définis à $0.

### Configuration du streaming

L'intégration Ollama d'OpenClaw utilise l'**API native d'Ollama** (`/api/chat`) par défaut, qui supporte complètement le streaming et l'appel d'outils simultanément. Aucune configuration spéciale n'est nécessaire.

#### Mode compatible OpenAI hérité

<Warning>
**L'appel d'outils n'est pas fiable en mode compatible OpenAI.** Utilisez ce mode uniquement si vous avez besoin du format OpenAI pour un proxy et ne dépendez pas du comportement natif d'appel d'outils.
</Warning>

Si vous avez besoin d'utiliser le point de terminaison compatible OpenAI à la place (par exemple, derrière un proxy qui ne supporte que le format OpenAI), définissez `api: "openai-completions"` explicitement :

```json5
{
  models: {
    providers: {
      ollama: {
        baseUrl: "http://ollama-host:11434/v1",
        api: "openai-completions",
        injectNumCtxForOpenAICompat: true, // défaut : true
        apiKey: "ollama-local",
        models: [...]
      }
    }
  }
}
```

Ce mode peut ne pas supporter le streaming + appel d'outils simultanément. Vous devrez peut-être désactiver le streaming avec `params: { streaming: false }` dans la configuration du modèle.

Quand `api: "openai-completions"` est utilisé avec Ollama, OpenClaw injecte `options.num_ctx` par défaut pour qu'Ollama ne revienne pas silencieusement à une fenêtre de contexte de 4096. Si votre proxy/upstream rejette les champs `options` inconnus, désactivez ce comportement :

```json5
{
  models: {
    providers: {
      ollama: {
        baseUrl: "http://ollama-host:11434/v1",
        api: "openai-completions",
        injectNumCtxForOpenAICompat: false,
        apiKey: "ollama-local",
        models: [...]
      }
    }
  }
}
```

### Fenêtres de contexte

Pour les modèles découverts automatiquement, OpenClaw utilise la fenêtre de contexte rapportée par Ollama quand disponible, sinon il revient à la fenêtre de contexte Ollama par défaut utilisée par OpenClaw. Vous pouvez remplacer `contextWindow` et `maxTokens` dans la configuration explicite du fournisseur.

## Dépannage

### Ollama non détecté

Assurez-vous qu'Ollama s'exécute et que vous avez défini `OLLAMA_API_KEY` (ou un profil d'authentification), et que vous **n'avez pas** défini d'entrée explicite `models.providers.ollama` :

```bash
ollama serve
```

Et que l'API est accessible :

```bash
curl http://localhost:11434/api/tags
```

### Aucun modèle disponible

Si votre modèle n'est pas listé, soit :

- Téléchargez le modèle localement, soit
- Définissez le modèle explicitement dans `models.providers.ollama`.

Pour ajouter des modèles :

```bash
ollama list  # Voir ce qui est installé
ollama pull glm-4.7-flash
ollama pull gpt-oss:20b
ollama pull llama3.3     # Ou un autre modèle
```

### Connexion refusée

Vérifiez qu'Ollama s'exécute sur le port correct :

```bash
# Vérifier si Ollama s'exécute
ps aux | grep ollama

# Ou redémarrer Ollama
ollama serve
```

## Voir aussi

- [Model Providers](/concepts/model-providers) - Aperçu de tous les fournisseurs
- [Model Selection](/concepts/models) - Comment choisir les modèles
- [Configuration](/gateway/configuration) - Référence de configuration complète
