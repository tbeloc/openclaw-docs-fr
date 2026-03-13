---
title: "Flux de travail de développement Pi"
summary: "Flux de travail développeur pour l'intégration Pi : construction, test et validation en direct"
read_when:
  - Working on Pi integration code or tests
  - Running Pi-specific lint, typecheck, and live test flows
---

# Flux de travail de développement Pi

Ce guide résume un flux de travail cohérent pour travailler sur l'intégration pi dans OpenClaw.

## Vérification des types et linting

- Vérifier les types et construire : `pnpm build`
- Linting : `pnpm lint`
- Vérification du formatage : `pnpm format`
- Vérification complète avant de pousser : `pnpm lint && pnpm build && pnpm test`

## Exécution des tests Pi

Exécutez l'ensemble de tests axé sur Pi directement avec Vitest :

```bash
pnpm test -- \
  "src/agents/pi-*.test.ts" \
  "src/agents/pi-embedded-*.test.ts" \
  "src/agents/pi-tools*.test.ts" \
  "src/agents/pi-settings.test.ts" \
  "src/agents/pi-tool-definition-adapter*.test.ts" \
  "src/agents/pi-extensions/**/*.test.ts"
```

Pour inclure l'exercice du fournisseur en direct :

```bash
OPENCLAW_LIVE_TEST=1 pnpm test -- src/agents/pi-embedded-runner-extraparams.live.test.ts
```

Cela couvre les principales suites d'unités Pi :

- `src/agents/pi-*.test.ts`
- `src/agents/pi-embedded-*.test.ts`
- `src/agents/pi-tools*.test.ts`
- `src/agents/pi-settings.test.ts`
- `src/agents/pi-tool-definition-adapter.test.ts`
- `src/agents/pi-extensions/*.test.ts`

## Tests manuels

Flux recommandé :

- Exécutez la passerelle en mode développement :
  - `pnpm gateway:dev`
- Déclenchez l'agent directement :
  - `pnpm openclaw agent --message "Hello" --thinking low`
- Utilisez l'interface TUI pour le débogage interactif :
  - `pnpm tui`

Pour le comportement des appels d'outils, demandez une action `read` ou `exec` pour voir le streaming des outils et la gestion des charges utiles.

## Réinitialisation complète

L'état se trouve dans le répertoire d'état OpenClaw. La valeur par défaut est `~/.openclaw`. Si `OPENCLAW_STATE_DIR` est défini, utilisez ce répertoire à la place.

Pour réinitialiser tout :

- `openclaw.json` pour la configuration
- `credentials/` pour les profils d'authentification et les jetons
- `agents/<agentId>/sessions/` pour l'historique des sessions de l'agent
- `agents/<agentId>/sessions.json` pour l'index des sessions
- `sessions/` si des chemins hérités existent
- `workspace/` si vous voulez un espace de travail vierge

Si vous souhaitez uniquement réinitialiser les sessions, supprimez `agents/<agentId>/sessions/` et `agents/<agentId>/sessions.json` pour cet agent. Conservez `credentials/` si vous ne voulez pas vous réauthentifier.

## Références

- [https://docs.openclaw.ai/testing](https://docs.openclaw.ai/testing)
- [https://docs.openclaw.ai/start/getting-started](https://docs.openclaw.ai/start/getting-started)
