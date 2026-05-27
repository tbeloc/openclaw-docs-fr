---
summary: "Flux de travail du développeur pour le runtime d'agent OpenClaw : construction, test et validation en direct"
title: "Flux de travail du runtime d'agent OpenClaw"
read_when:
  - Working on OpenClaw agent runtime code or tests
  - Running agent-runtime lint, typecheck, and live test flows
---

Un flux de travail sensé pour travailler sur le runtime d'agent OpenClaw dans OpenClaw.

## Vérification des types et linting

- Portail local par défaut : `pnpm check`
- Portail de construction : `pnpm build` lorsque la modification peut affecter la sortie de construction, l'empaquetage ou les limites de chargement différé/module
- Portail d'atterrissage complet pour les modifications agent-runtime : `pnpm check && pnpm test`

## Exécution des tests du runtime d'agent

Exécutez directement l'ensemble de tests agent-runtime avec Vitest :

```bash
pnpm test \
  "src/agents/agent-*.test.ts" \
  "src/agents/embedded-agent-*.test.ts" \
  "src/agents/agent-tools*.test.ts" \
  "src/agents/agent-settings.test.ts" \
  "src/agents/agent-tool-definition-adapter*.test.ts" \
  "src/agents/agent-hooks/**/*.test.ts"
```

Pour inclure l'exercice du fournisseur en direct :

```bash
OPENCLAW_LIVE_TEST=1 pnpm test src/agents/embedded-agent-runner-extraparams.live.test.ts
```

Cela couvre les principales suites de tests du runtime d'agent :

- `src/agents/agent-*.test.ts`
- `src/agents/embedded-agent-*.test.ts`
- `src/agents/agent-tools*.test.ts`
- `src/agents/agent-settings.test.ts`
- `src/agents/agent-tool-definition-adapter.test.ts`
- `src/agents/agent-hooks/*.test.ts`

## Test manuel

Flux recommandé :

- Exécutez la passerelle en mode développement :
  - `pnpm gateway:dev`
- Déclenchez l'agent directement :
  - `pnpm openclaw agent --message "Hello" --thinking low`
- Utilisez l'interface utilisateur TUI pour le débogage interactif :
  - `pnpm tui`

Pour le comportement des appels d'outils, demandez une action `read` ou `exec` pour pouvoir voir le streaming des outils et la gestion des charges utiles.

## Réinitialisation à zéro

L'état se trouve dans le répertoire d'état OpenClaw. La valeur par défaut est `~/.openclaw`. Si `OPENCLAW_STATE_DIR` est défini, utilisez ce répertoire à la place.

Pour réinitialiser tout :

- `openclaw.json` pour la configuration
- `agents/<agentId>/agent/auth-profiles.json` pour les profils d'authentification du modèle (clés API + OAuth)
- `credentials/` pour l'état du fournisseur/canal qui réside toujours en dehors du magasin de profils d'authentification
- `agents/<agentId>/sessions/` pour l'historique des sessions d'agent
- `agents/<agentId>/sessions/sessions.json` pour l'index des sessions
- `sessions/` si des chemins hérités existent
- `workspace/` si vous voulez un espace de travail vierge

Si vous souhaitez uniquement réinitialiser les sessions, supprimez `agents/<agentId>/sessions/` pour cet agent. Si vous souhaitez conserver l'authentification, laissez `agents/<agentId>/agent/auth-profiles.json` et tout état du fournisseur sous `credentials/` en place.

## Références

- [Testing](/fr/help/testing)
- [Getting Started](/fr/start/getting-started)

## Connexes

- [Architecture du runtime d'agent OpenClaw](/fr/agent-runtime-architecture)
