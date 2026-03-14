---
title: Pi 开发工作流程
x-i18n:
  generated_at: "2026-02-03T10:07:59Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 65bd0580dd03df05321ced35a036ce6fb815ce3ddac1d35c9976279adcbf87c0
  source_path: pi-dev.md
  workflow: 15
---

# Flux de travail de développement Pi

Ce guide résume un flux de travail raisonnable pour développer l'intégration Pi dans OpenClaw.

## Vérification des types et linting du code

- Vérification des types et construction : `pnpm build`
- Linting du code : `pnpm lint`
- Vérification du formatage : `pnpm format`
- Vérification complète avant push : `pnpm lint && pnpm build && pnpm test`

## Exécution des tests Pi

Utilisez le script dédié pour exécuter la suite de tests d'intégration Pi :

```bash
scripts/pi/run-tests.sh
```

Pour inclure les tests en direct qui exécutent le comportement réel du fournisseur :

```bash
scripts/pi/run-tests.sh --live
```

Ce script exécute tous les tests unitaires liés à Pi via les modèles glob suivants :

- `src/agents/pi-*.test.ts`
- `src/agents/pi-embedded-*.test.ts`
- `src/agents/pi-tools*.test.ts`
- `src/agents/pi-settings.test.ts`
- `src/agents/pi-tool-definition-adapter.test.ts`
- `src/agents/pi-extensions/*.test.ts`

## Tests manuels

Flux de travail recommandé :

- Exécutez la passerelle en mode développement :
  - `pnpm gateway:dev`
- Déclenchez directement l'agent :
  - `pnpm openclaw agent --message "Hello" --thinking low`
- Utilisez l'interface TUI pour le débogage interactif :
  - `pnpm tui`

Pour le comportement d'appel d'outils, invitez l'exécution d'opérations `read` ou `exec` pour voir le streaming des outils et la gestion des charges utiles.

## Réinitialisation complète

L'état est stocké dans le répertoire d'état OpenClaw. Par défaut, c'est `~/.openclaw`. Si `OPENCLAW_STATE_DIR` est défini, ce répertoire est utilisé.

Pour réinitialiser tout :

- `openclaw.json` pour la configuration
- `credentials/` pour les fichiers de configuration d'authentification et les tokens
- `agents/<agentId>/sessions/` pour l'historique des sessions de l'agent
- `agents/<agentId>/sessions.json` pour l'index des sessions
- `sessions/` s'il existe un ancien chemin
- `workspace/` si vous voulez un espace de travail vierge

Si vous souhaitez uniquement réinitialiser les sessions, supprimez `agents/<agentId>/sessions/` et `agents/<agentId>/sessions.json` pour cet agent. Conservez `credentials/` si vous ne voulez pas vous réauthentifier.

## Références

- https://docs.openclaw.ai/testing
- https://docs.openclaw.ai/start/getting-started
