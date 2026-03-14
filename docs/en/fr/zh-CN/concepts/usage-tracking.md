---
read_when:
  - 你正在对接提供商使用量/配额界面
  - 你需要解释使用量跟踪行为或认证要求
summary: 使用量跟踪界面及凭据要求
title: 使用量跟踪
x-i18n:
  generated_at: "2026-02-01T20:24:46Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 6f6ed2a70329b2a6206c327aa749a84fbfe979762caca5f0e7fb556f91631cbb
  source_path: concepts/usage-tracking.md
  workflow: 14
---

# Suivi de l'utilisation

## Aperçu des fonctionnalités

- Récupère directement les données d'utilisation/quota à partir du point de terminaison d'utilisation du fournisseur.
- Ne fournit pas d'estimation des coûts ; affiche uniquement les données de la fenêtre de temps rapportées par le fournisseur.

## Emplacements d'affichage

- `/status` dans le chat : carte de statut enrichie d'emojis contenant le nombre de tokens de session et les coûts estimés (clé API uniquement). Affiche l'utilisation du **fournisseur de modèle actuel** lorsqu'elle est disponible.
- `/usage off|tokens|full` dans le chat : pied de page d'utilisation pour chaque réponse (OAuth affiche uniquement le nombre de tokens).
- `/usage cost` dans le chat : résumé des coûts locaux agrégés à partir des journaux de session OpenClaw.
- CLI : `openclaw status --usage` imprime les informations détaillées complètes catégorisées par fournisseur.
- CLI : `openclaw channels list` imprime le même snapshot d'utilisation à côté des configurations de fournisseur (utilisez `--no-usage` pour ignorer).
- Barre de menus macOS : section "Utilisation" sous le menu contextuel (affichée uniquement si disponible).

## Fournisseurs et identifiants

- **Anthropic (Claude)** : jeton OAuth dans la configuration d'authentification.
- **GitHub Copilot** : jeton OAuth dans la configuration d'authentification.
- **Gemini CLI** : jeton OAuth dans la configuration d'authentification.
- **Antigravity** : jeton OAuth dans la configuration d'authentification.
- **OpenAI Codex** : jeton OAuth dans la configuration d'authentification (utilise accountId si présent).
- **MiniMax** : clé API (clé de plan de programmation ; `MINIMAX_CODE_PLAN_KEY` ou `MINIMAX_API_KEY`) ; utilise une fenêtre de temps de plan de programmation de 5 heures.
- **z.ai** : clé API fournie via variable d'environnement/configuration/stockage d'authentification.

Si aucune identifiant OAuth/API correspondant n'est trouvé, les informations d'utilisation seront masquées.
