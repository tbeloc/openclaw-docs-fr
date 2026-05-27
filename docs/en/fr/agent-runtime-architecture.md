---
title: "Architecture du runtime d'agent"
summary: "Comment OpenClaw exécute le runtime d'agent intégré, les fournisseurs, les sessions, les outils et les extensions."
---

OpenClaw possède directement le runtime d'agent intégré. Le code du runtime se trouve sous `src/agents/`, les assistants modèle/fournisseur se trouvent sous `src/llm/`, et les contrats orientés plugin sont exposés via les barils `openclaw/plugin-sdk/*`.

## Disposition du Runtime

- `src/agents/embedded-agent-runner/`: boucle de tentative d'agent intégré, adaptateurs de flux de fournisseur, compaction, sélection de modèle et câblage de session.
- `src/agents/sessions/`: persistance de session, chargement d'extension, découverte de ressources, compétences, invites, thèmes et renderers d'outils soutenus par TUI.
- `packages/agent-core/`: noyau d'agent réutilisable, types de harnais de bas niveau, messages, assistants de compaction, modèles d'invite et contrats d'outil/session.
- `src/agents/runtime/`: façade OpenClaw pour `@openclaw/agent-core` plus utilitaires de proxy locaux.
- `src/agents/agent-tools*.ts`: définitions d'outils appartenant à OpenClaw, schémas, politique, adaptateurs de hooks avant/après et support d'édition d'hôte.
- `src/agents/agent-hooks/`: hooks de runtime intégrés tels que les protections de compaction et l'élagage de contexte.
- `src/llm/`: registre modèle/fournisseur, assistants de transport et implémentations de flux spécifiques au fournisseur.

## Limites

Le code principal appelle le runtime intégré via les modules OpenClaw et les barils SDK, et non via les anciens packages d'agent externes. Les plugins utilisent les points d'entrée documentés `openclaw/plugin-sdk/*` et n'importent pas les éléments internes `src/**`.

`@earendil-works/pi-tui` reste une dépendance TUI tierce. Il est utilisé comme kit d'outils de composants de terminal par le TUI local et les renderers de session ; l'internaliser serait un effort de vendoring distinct.

## Manifestes

Les packages de ressources déclarent les ressources OpenClaw dans les métadonnées du package :

```json
{
  "openclaw": {
    "extensions": ["extensions/index.ts"],
    "skills": ["skills/*.md"],
    "prompts": ["prompts/*.md"],
    "themes": ["themes/*.json"]
  }
}
```

Le gestionnaire de packages découvre également les répertoires conventionnels `extensions/`, `skills/`, `prompts/` et `themes/`.

## Sélection du Runtime

L'ID de runtime intégré par défaut est `openclaw`. Les harnais de plugin peuvent enregistrer des ID de runtime supplémentaires. `auto` sélectionne un harnais de plugin de support lorsqu'il existe et utilise sinon le runtime OpenClaw intégré.

## Connexes

- [Flux de travail du runtime d'agent OpenClaw](/fr/openclaw-agent-runtime)
- [Runtimes d'agent](/fr/concepts/agent-runtimes)
