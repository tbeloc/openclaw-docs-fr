---
summary: "Surfaces de suivi d'utilisation et exigences d'authentification"
read_when:
  - You are wiring provider usage/quota surfaces
  - You need to explain usage tracking behavior or auth requirements
title: "Suivi d'utilisation"
---

# Suivi d'utilisation

## Qu'est-ce que c'est

- Récupère l'utilisation/quota du fournisseur directement à partir de ses points de terminaison d'utilisation.
- Pas de coûts estimés ; uniquement les fenêtres signalées par le fournisseur.

## Où cela s'affiche

- `/status` dans les chats : carte de statut riche en emoji avec jetons de session + coût estimé (clé API uniquement). L'utilisation du fournisseur s'affiche pour le **fournisseur de modèle actuel** lorsqu'elle est disponible.
- `/usage off|tokens|full` dans les chats : pied de page d'utilisation par réponse (OAuth affiche uniquement les jetons).
- `/usage cost` dans les chats : résumé des coûts locaux agrégé à partir des journaux de session OpenClaw.
- CLI : `openclaw status --usage` affiche une ventilation complète par fournisseur.
- CLI : `openclaw channels list` affiche le même snapshot d'utilisation aux côtés de la configuration du fournisseur (utilisez `--no-usage` pour ignorer).
- Barre de menu macOS : section « Utilisation » sous Contexte (uniquement si disponible).

## Fournisseurs + authentification

- **Anthropic (Claude)** : jetons OAuth dans les profils d'authentification.
- **GitHub Copilot** : jetons OAuth dans les profils d'authentification.
- **Gemini CLI** : jetons OAuth dans les profils d'authentification.
- **Antigravity** : jetons OAuth dans les profils d'authentification.
- **OpenAI Codex** : jetons OAuth dans les profils d'authentification (accountId utilisé si présent).
- **MiniMax** : clé API (clé de plan de codage ; `MINIMAX_CODE_PLAN_KEY` ou `MINIMAX_API_KEY`) ; utilise la fenêtre de plan de codage de 5 heures.
- **z.ai** : clé API via env/config/magasin d'authentification.

L'utilisation est masquée s'il n'existe pas d'authentification OAuth/API correspondante.
