---
read_when:
  - 你想在 OpenClaw 中使用 Qwen
  - 你想要免费层 OAuth 访问 Qwen Coder
summary: 在 OpenClaw 中使用 Qwen OAuth（免费层）
title: Qwen
x-i18n:
  generated_at: "2026-02-03T07:53:34Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 88b88e224e2fecbb1ca26e24fbccdbe25609be40b38335d0451343a5da53fdd4
  source_path: providers/qwen.md
  workflow: 15
---

# Qwen

Qwen fournit un flux OAuth de niveau gratuit pour les modèles Qwen Coder et Qwen Vision (2 000 requêtes par jour, soumis aux limites de débit de Qwen).

## Activer le plugin

```bash
openclaw plugins enable qwen-portal-auth
```

Redémarrez la passerelle après activation.

## Authentification

```bash
openclaw models auth login --provider qwen-portal --set-default
```

Cela exécute le flux OAuth de code d'appareil Qwen et écrit l'entrée du fournisseur dans votre `models.json` (plus un alias `qwen` pour basculer rapidement).

## ID de modèle

- `qwen-portal/coder-model`
- `qwen-portal/vision-model`

Basculer de modèle :

```bash
openclaw models set qwen-portal/coder-model
```

## Réutiliser la connexion Qwen Code CLI

Si vous êtes déjà connecté avec Qwen Code CLI, OpenClaw synchronisera les identifiants depuis `~/.qwen/oauth_creds.json` lors du chargement du magasin d'authentification. Vous avez toujours besoin d'une entrée `models.providers.qwen-portal` (créez-en une avec la commande de connexion ci-dessus).

## Remarques

- Les jetons s'actualisent automatiquement ; si l'actualisation échoue ou l'accès est révoqué, réexécutez la commande de connexion.
- URL de base par défaut : `https://portal.qwen.ai/v1` (si Qwen fournit un point de terminaison différent, remplacez-le avec `models.providers.qwen-portal.baseUrl`).
- Consultez [Fournisseurs de modèles](/concepts/model-providers) pour les règles au niveau du fournisseur.
