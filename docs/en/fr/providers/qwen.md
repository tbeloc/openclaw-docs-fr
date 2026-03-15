---
summary: "Utiliser Qwen OAuth (niveau gratuit) dans OpenClaw"
read_when:
  - Vous voulez utiliser Qwen avec OpenClaw
  - Vous voulez un accès OAuth au niveau gratuit pour Qwen Coder
title: "Qwen"
---

# Qwen

Qwen fournit un flux OAuth au niveau gratuit pour les modèles Qwen Coder et Qwen Vision
(2 000 requêtes/jour, soumis aux limites de débit de Qwen).

## Activer le plugin

```bash
openclaw plugins enable qwen-portal-auth
```

Redémarrez la Gateway après activation.

## S'authentifier

```bash
openclaw models auth login --provider qwen-portal --set-default
```

Cela exécute le flux OAuth de code d'appareil Qwen et écrit une entrée de fournisseur dans votre
`models.json` (plus un alias `qwen` pour basculer rapidement).

## ID de modèles

- `qwen-portal/coder-model`
- `qwen-portal/vision-model`

Basculez les modèles avec :

```bash
openclaw models set qwen-portal/coder-model
```

## Réutiliser la connexion CLI Qwen Code

Si vous vous êtes déjà connecté avec la CLI Qwen Code, OpenClaw synchronisera les identifiants
depuis `~/.qwen/oauth_creds.json` lors du chargement du magasin d'authentification. Vous avez toujours besoin d'une
entrée `models.providers.qwen-portal` (utilisez la commande de connexion ci-dessus pour en créer une).

## Remarques

- Les jetons se rafraîchissent automatiquement ; réexécutez la commande de connexion si le rafraîchissement échoue ou si l'accès est révoqué.
- URL de base par défaut : `https://portal.qwen.ai/v1` (remplacez par
  `models.providers.qwen-portal.baseUrl` si Qwen fournit un point de terminaison différent).
- Voir [Fournisseurs de modèles](/fr/concepts/model-providers) pour les règles au niveau du fournisseur.
