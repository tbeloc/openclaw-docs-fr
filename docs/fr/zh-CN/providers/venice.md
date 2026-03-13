```markdown
---
read_when:
  - Vous souhaitez utiliser un service d'inférence respectueux de la vie privée dans OpenClaw
  - Vous avez besoin de conseils de configuration pour Venice AI
summary: Utiliser les modèles respectueux de la vie privée de Venice AI dans OpenClaw
title: Venice AI
x-i18n:
  generated_at: "2026-02-01T21:36:03Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 2453a6ec3a715c24c460f902dec1755edcad40328de2ef895e35a614a25624cf
  source_path: providers/venice.md
  workflow: 15
---

# Venice AI (Sélection Venice)

**Venice** est notre configuration d'inférence Venice respectueuse de la vie privée, avec accès optionnel anonymisé aux modèles propriétaires.

Venice AI fournit un service d'inférence IA respectueux de la vie privée, supportant les modèles sans censure et permettant l'accès anonymisé aux modèles propriétaires populaires via son proxy anonyme. Toute inférence est privée par défaut — vos données ne sont pas utilisées pour l'entraînement et ne sont pas enregistrées.

## Pourquoi utiliser Venice dans OpenClaw

- **Inférence privée** pour les modèles open source (sans enregistrement).
- Utilisez des **modèles sans censure** si nécessaire.
- **Accès anonymisé** aux modèles propriétaires (Opus/GPT/Gemini) quand la qualité compte.
- Compatible avec les points de terminaison OpenAI `/v1`.

## Modes de confidentialité

Venice offre deux niveaux de confidentialité — comprendre cela est clé pour choisir votre modèle :

| Mode | Description | Modèles |
| --- | --- | --- |
| **Privé** | Complètement privé. Les invites/réponses ne sont **jamais stockées ou enregistrées**. Traitement éphémère. | Llama, Qwen, DeepSeek, Venice Uncensored, etc. |
| **Anonymisé** | Acheminé via le proxy Venice avec métadonnées supprimées. Les fournisseurs sous-jacents (OpenAI, Anthropic) reçoivent des requêtes anonymisées. | Claude, GPT, Gemini, Grok, Kimi, MiniMax |

## Capacités

- **Respectueux de la vie privée** : Modes « privé » (complètement privé) et « anonymisé » (proxy) au choix
- **Modèles sans censure** : Accès à des modèles sans restrictions de contenu
- **Accès aux modèles populaires** : Utilisez Claude, GPT-5.2, Gemini, Grok via le proxy anonyme Venice
- **Compatible avec l'API OpenAI** : Point de terminaison `/v1` standard, facile à intégrer
- **Streaming** : ✅ Supporté par tous les modèles
- **Appels de fonction** : ✅ Supporté par certains modèles (vérifiez les capacités du modèle)
- **Vision** : ✅ Supporté par les modèles avec capacités visuelles
- **Pas de limite de débit stricte** : Une limitation d'équité peut être déclenchée en cas d'utilisation extrême

## Configuration

### 1. Obtenir une clé API

1. Inscrivez-vous sur [venice.ai](https://venice.ai)
2. Allez à **Settings → API Keys → Create new key**
3. Copiez votre clé API (format : `vapi_xxxxxxxxxxxx`)

### 2. Configurer OpenClaw

**Option A : Variable d'environnement**

```bash
export VENICE_API_KEY="vapi_xxxxxxxxxxxx"
```

**Option B : Configuration interactive (recommandée)**

```bash
openclaw onboard --auth-choice venice-api-key
```

Cela va :

1. Vous demander votre clé API (ou utiliser la `VENICE_API_KEY` existante)
2. Afficher tous les modèles Venice disponibles
3. Vous laisser choisir le modèle par défaut
4. Configurer automatiquement le fournisseur

**Option C : Non-interactive**

```bash
openclaw onboard --non-interactive \
  --auth-choice venice-api-key \
  --venice-api-key "vapi_xxxxxxxxxxxx"
```

### 3. Vérifier la configuration

```bash
openclaw chat --model venice/llama-3.3-70b "Hello, are you working?"
```

## Sélection du modèle

Une fois configuré, OpenClaw affichera tous les modèles Venice disponibles. Choisissez selon vos besoins :

- **Par défaut (notre recommandation)** : `venice/llama-3.3-70b`, privé et équilibré en performance.
- **Meilleure qualité globale** : `venice/claude-opus-45`, pour les tâches complexes (Opus reste le plus puissant).
- **Confidentialité** : Choisissez un modèle « privé » pour une inférence complètement privée.
- **Capacités** : Choisissez un modèle « anonymisé » pour accéder à Claude, GPT, Gemini via le proxy Venice.

Changez le modèle par défaut à tout moment :

```bash
openclaw models set venice/claude-opus-45
openclaw models set venice/llama-3.3-70b
```

Listez tous les modèles disponibles :

```bash
openclaw models list | grep venice
```

## Configuration via `openclaw configure`

1. Exécutez `openclaw configure`
2. Sélectionnez **Model/auth**
3. Sélectionnez **Venice AI**

## Quel modèle utiliser ?

| Cas d'usage | Modèle recommandé | Raison |
| --- | --- | --- |
| **Conversation générale** | `llama-3.3-70b` | Bonnes performances globales, complètement privé |
| **Meilleure qualité globale** | `claude-opus-45` | Opus reste le plus puissant pour les tâches complexes |
| **Confidentialité + Qualité Claude** | `claude-opus-45` | Meilleure capacité d'inférence via proxy anonyme |
| **Programmation** | `qwen3-coder-480b-a35b-instruct` | Optimisé pour le code, contexte 262k |
| **Tâches visuelles** | `qwen3-vl-235b-a22b` | Meilleur modèle visuel privé |
| **Sans censure** | `venice-uncensored` | Pas de restrictions de contenu |
| **Rapide + Faible coût** | `qwen3-4b` | Léger, capacités décentes |
| **Raisonnement complexe** | `deepseek-v3.2` | Fortes capacités de raisonnement, privé |

## Modèles disponibles (25 au total)

### Modèles privés (15) — Complètement privés, sans enregistrement

| ID du modèle | Nom | Contexte (tokens) | Caractéristiques |
| --- | --- | --- | --- |
| `llama-3.3-70b` | Llama 3.3 70B | 131k | Général |
| `llama-3.2-3b` | Llama 3.2 3B | 131k | Rapide, léger |
| `hermes-3-llama-3.1-405b` | Hermes 3 Llama 3.1 405B | 131k | Tâches complexes |
| `qwen3-235b-a22b-thinking-2507` | Qwen3 235B Thinking | 131k | Raisonnement |
| `qwen3-235b-a22b-instruct-2507` | Qwen3 235B Instruct | 131k | Général |
| `qwen3-coder-480b-a35b-instruct` | Qwen3 Coder 480B | 262k | Programmation |
| `qwen3-next-80b` | Qwen3 Next 80B | 262k | Général |
| `qwen3-vl-235b-a22b` | Qwen3 VL 235B | 262k | Vision |
| `qwen3-4b` | Venice Small (Qwen3 4B) | 32k | Rapide, raisonnement |
| `deepseek-v3.2` | DeepSeek V3.2 | 163k | Raisonnement |
| `venice-uncensored` | Venice Uncensored | 32k | Sans censure |
| `mistral-31-24b` | Venice Medium (Mistral) | 131k | Vision |
| `google-gemma-3-27b-it` | Gemma 3 27B Instruct | 202k | Vision |
| `openai-gpt-oss-120b` | OpenAI GPT OSS 120B | 131k | Général |
| `zai-org-glm-4.7` | GLM 4.7 | 202k | Raisonnement, multilingue |

### Modèles anonymisés (10) — Via proxy Venice

| ID du modèle | Modèle original | Contexte (tokens) | Caractéristiques |
| --- | --- | --- | --- |
| `claude-opus-45` | Claude Opus 4.5 | 202k | Raisonnement, vision |
| `claude-sonnet-45` | Claude Sonnet 4.5 | 202k | Raisonnement, vision |
| `openai-gpt-52` | GPT-5.2 | 262k | Raisonnement |
| `openai-gpt-52-codex` | GPT-5.2 Codex | 262k | Raisonnement, vision |
| `gemini-3-pro-preview` | Gemini 3 Pro | 202k | Raisonnement, vision |
| `gemini-3-flash-preview` | Gemini 3 Flash | 262k | Raisonnement, vision |
| `grok-41-fast` | Grok 4.1 Fast | 262k | Raisonnement, vision |
| `grok-code-fast-1` | Grok Code Fast 1 | 262k | Raisonnement, programmation |
| `kimi-k2-thinking` | Kimi K2 Thinking | 262k | Raisonnement |
| `minimax-m21` | MiniMax M2.1 | 202k | Raisonnement |

## Découverte de modèles

Quand `VENICE_API_KEY` est configurée, OpenClaw découvre automatiquement les modèles depuis l'API Venice. Si l'API est inaccessible, il revient à un répertoire statique.

Le point de terminaison `/models` est public (lister les modèles ne nécessite pas d'authentification), mais l'inférence nécessite une clé API valide.

## Support du streaming et des outils

| Fonctionnalité | Support |
| --- | --- |
| **Streaming** | ✅ Tous les modèles |
| **Appels de fonction** | ✅ La plupart des modèles (vérifiez `supportsFunctionCalling` dans l'API) |
| **Vision/Images** | ✅ Modèles marqués avec la caractéristique « Vision » |
| **Mode JSON** | ✅ Supporté via `response_format` |

## Tarification

Venice utilise un système de crédits. Consultez [venice.ai/pricing](https://venice.ai/pricing) pour les tarifs actuels :

- **Modèles privés** : Généralement moins chers
- **Modèles anonymisés** : Similaire à la tarification API directe + frais Venice mineurs

## Comparaison : Venice vs API directe

| Aspect | Venice (anonymisé) | API directe |
| --- | --- | --- |
| **Confidentialité** | Métadonnées supprimées, anonymisé | Associé à votre compte |
| **Latence** | +10-50ms (proxy) | Connexion directe |
| **Fonctionnalités** | Plupart des fonctionnalités supportées | Fonctionnalités complètes |
| **Facturation** | Crédits Venice | Facturation du fournisseur |

## Exemples d'utilisation

```bash
# Utiliser le modèle privé par défaut
openclaw chat --model venice/llama-3.3-70b

# Utiliser Claude via Venice (anonymisé)
openclaw chat --model venice/claude-opus-45

# Utiliser un modèle sans censure
openclaw chat --model venice/venice-uncensored

# Utiliser un modèle visuel pour les images
openclaw chat --model venice/qwen3-vl-235b-a22b

# Utiliser un modèle de programmation
openclaw chat --model venice/qwen3-coder-480b-a35b-instruct
```

## Dépannage

### Clé API non reconnue

```bash
echo $VENICE_API_KEY
openclaw models list | grep venice
```

Assurez-vous que la clé commence par `vapi_`.

### Modèle non disponible

Le répertoire de modèles Venice se met à jour dynamiquement. Exécutez `openclaw models list` pour voir les modèles actuellement disponibles. Certains modèles peuvent être temporairement hors ligne.

### Problèmes de connexion

L'API Venice est à `https://api.venice.ai/api/v1`. Assurez-vous que votre réseau autorise les connexions HTTPS.

## Exemple de fichier de configuration

```json5
{
  env: { VENICE_API_KEY: "vapi_..." },
  agents: { defaults: { model: { primary: "venice/llama-3.3-70b" } } },
  models: {
    mode: "merge",
    providers: {
      venice: {
        baseUrl: "https://api.venice.ai/api/v1",
        apiKey: "${VENICE_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "llama-3.3-70b",
            name: "Llama 3.3 70B",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 131072,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Liens

- [Venice AI](https://venice.ai)
- [Documentation API](https://docs.venice.ai)
- [Tarification](https://venice.ai/pricing)
- [Page de statut](https://status.venice.ai)
```
