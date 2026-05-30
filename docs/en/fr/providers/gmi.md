---
summary: "Utilisez l'API compatible OpenAI de GMI Cloud avec OpenClaw"
read_when:
  - You want to run OpenClaw with GMI Cloud models
  - You need the GMI provider id, key, or endpoint
title: "GMI Cloud"
---

GMI Cloud est une plateforme d'inférence hébergée pour les modèles de pointe et open-weight derrière une API compatible OpenAI. Dans OpenClaw, c'est un fournisseur de modèles intégré, ce qui signifie que vous pouvez le sélectionner avec l'identifiant de fournisseur `gmi`, stocker les identifiants via l'authentification de modèle normale, et utiliser des références de modèle comme `gmi/google/gemini-3.1-flash-lite`.

Utilisez GMI quand vous voulez une clé API pour plusieurs familles de modèles hébergés, y compris les routes Google, Anthropic, OpenAI, DeepSeek, Moonshot et Z.AI exposées par le catalogue de GMI. C'est utile comme fournisseur secondaire pour le basculement de modèle, pour comparer les routes hébergées entre les fournisseurs, ou quand GMI a un modèle disponible avant votre fournisseur principal.

Ce fournisseur utilise la sémantique de chat compatible OpenAI. OpenClaw possède l'identifiant de fournisseur, le profil d'authentification, les alias, la graine du catalogue de modèles et l'URL de base ; GMI possède la disponibilité des modèles en direct, la facturation, les limites de débit et toute politique de routage côté fournisseur.

## Configuration

Créez une clé API dans GMI Cloud, puis exécutez :

```bash
openclaw onboard --auth-choice gmi-api-key
```

Ou définissez :

```bash
export GMI_API_KEY="<your-gmi-api-key>" # pragma: allowlist secret
```

## Valeurs par défaut

- Fournisseur : `gmi`
- Alias : `gmi-cloud`, `gmicloud`
- URL de base : `https://api.gmi-serving.com/v1`
- Variable d'environnement : `GMI_API_KEY`
- Modèle par défaut : `gmi/google/gemini-3.1-flash-lite`

## Quand choisir GMI

- Vous voulez un point de terminaison hébergé compatible OpenAI plutôt qu'un serveur de modèle local.
- Vous voulez essayer plusieurs familles de modèles commerciaux et open-weight via un compte de fournisseur.
- Vous voulez un fournisseur de secours avec un routage en amont différent d'OpenRouter, DeepInfra, Together ou les API des fournisseurs directs.
- Vous avez besoin d'identifiants de modèle spécifiques à GMI, de tarification ou de contrôles de compte.

Choisissez plutôt le fournisseur de fournisseur direct quand vous avez besoin de fonctionnalités natives du fournisseur que GMI n'expose pas via sa route compatible OpenAI. Choisissez un fournisseur local tel que Ollama, LM Studio, vLLM ou SGLang quand la localité des données ou le contrôle GPU local est plus important que la commodité hébergée.

## Modèles

Le catalogue intégré amorce les identifiants de route GMI Cloud couramment disponibles, y compris :

- `gmi/zai-org/GLM-5.1-FP8`
- `gmi/deepseek-ai/DeepSeek-V3.2`
- `gmi/moonshotai/Kimi-K2.5`
- `gmi/google/gemini-3.1-flash-lite`
- `gmi/anthropic/claude-sonnet-4.6`
- `gmi/openai/gpt-5.4`

Le catalogue est une graine, pas une promesse que chaque compte peut appeler chaque modèle à tout moment. Utilisez la commande de liste de modèles d'OpenClaw pour voir ce que le fournisseur configuré rapporte dans votre environnement :

```bash
openclaw models list --provider gmi
```

## Dépannage

- `401` ou `403` : vérifiez que `GMI_API_KEY` est défini pour le processus exécutant OpenClaw, ou réexécutez l'intégration pour stocker la clé dans le profil d'authentification du fournisseur.
- Erreurs de modèle inconnu : confirmez que le modèle existe dans votre compte GMI et utilisez la référence complète `gmi/<route-id>` affichée par `openclaw models list --provider gmi`.
- Erreurs de fournisseur intermittentes : essayez une route GMI différente ou configurez GMI comme secours plutôt que comme seul fournisseur de modèle principal.

## Connexes

- [Model providers](/fr/concepts/model-providers)
- [All providers](/fr/providers/index)
