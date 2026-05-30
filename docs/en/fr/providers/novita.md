---
summary: "Utilisez l'API compatible OpenAI de NovitaAI avec OpenClaw"
read_when:
  - You want to run OpenClaw with NovitaAI models
  - You need the Novita provider id, key, or endpoint
title: "NovitaAI"
---

NovitaAI est un fournisseur d'infrastructure IA hébergée avec une API de modèle compatible OpenAI. Dans OpenClaw, c'est un fournisseur de modèle intégré, donc l'identifiant du fournisseur est `novita`, les identifiants de modèle ressemblent à `novita/deepseek/deepseek-v3-0324`, et les identifiants d'authentification suivent le flux d'authentification normal des modèles.

Utilisez Novita quand vous voulez un accès hébergé à des modèles open-weight et des routes de modèles tiers sans exécuter votre propre serveur d'inférence. Le catalogue intégré se concentre sur les modèles de chat pratiques pour les tours d'agent, incluant les routes DeepSeek, Moonshot, MiniMax, GLM et Qwen exposées par Novita.

Ce fournisseur utilise le point de terminaison compatible OpenAI de Novita. OpenClaw gère l'enregistrement du fournisseur, l'authentification, les alias, la normalisation des références de modèle et la sélection de l'URL de base ; Novita contrôle la disponibilité des modèles en direct, les permissions de compte, la tarification et les limites de débit.

## Configuration

Créez une clé API sur [novita.ai/settings/key-management](https://novita.ai/settings/key-management), puis exécutez :

```bash
openclaw onboard --auth-choice novita-api-key
```

Ou définissez :

```bash
export NOVITA_API_KEY="<your-novita-api-key>" # pragma: allowlist secret
```

## Valeurs par défaut

- Fournisseur : `novita`
- Alias : `novita-ai`, `novitaai`
- URL de base : `https://api.novita.ai/openai/v1`
- Variable d'environnement : `NOVITA_API_KEY`
- Modèle par défaut : `novita/deepseek/deepseek-v3-0324`

## Quand choisir Novita

- Vous voulez un accès hébergé à des modèles open-weight avec une API compatible OpenAI.
- Vous voulez des routes DeepSeek, Kimi, MiniMax, GLM ou Qwen via un seul compte fournisseur.
- Vous voulez un autre chemin de secours hébergé en plus d'OpenRouter, GMI, DeepInfra ou des API de fournisseurs directs.
- Vous préférez l'hébergement de modèles côté fournisseur à la maintenance d'une infrastructure vLLM, SGLang, LM Studio ou Ollama.

Choisissez un fournisseur de fournisseur direct quand vous avez besoin de paramètres de requête natifs du fournisseur ou de contrats de support. Choisissez un fournisseur local quand le modèle doit s'exécuter sur votre propre matériel ou derrière votre propre limite de réseau.

## Modèles

Le catalogue intégré initialise les identifiants de route NovitaAI couramment disponibles, incluant :

- `novita/moonshotai/kimi-k2.5`
- `novita/minimax/minimax-m2.7`
- `novita/zai-org/glm-5`
- `novita/deepseek/deepseek-v3-0324`
- `novita/deepseek/deepseek-r1-0528`
- `novita/qwen/qwen3-235b-a22b-fp8`

Le catalogue est un point de départ pour la sélection de modèles OpenClaw. Votre compte, votre région ou le catalogue actuel de Novita peuvent ajouter, supprimer ou restreindre des routes. Vérifiez le fournisseur depuis la CLI avant de définir une valeur par défaut de longue durée :

```bash
openclaw models list --provider novita
```

## Dépannage

- `401` ou `403` : vérifiez la clé dans la page de gestion des clés de Novita et réexécutez `openclaw onboard --auth-choice novita-api-key` si le profil stocké est obsolète.
- Erreurs de modèle inconnu : utilisez l'exact `novita/<route-id>` retourné par `openclaw models list --provider novita`.
- Routes lentes ou défaillantes : essayez une autre route de modèle Novita ou définissez Novita comme fournisseur de secours pour les charges de travail qui peuvent tolérer une variance spécifique au fournisseur.

## Connexes

- [Model providers](/fr/concepts/model-providers)
- [All providers](/fr/providers/index)
