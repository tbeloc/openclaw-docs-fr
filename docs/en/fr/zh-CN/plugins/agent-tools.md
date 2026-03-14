---
read_when:
  - 你想在插件中添加新的智能体工具
  - 你需要通过允许列表使工具可选启用
summary: 在插件中编写智能体工具（模式、可选工具、允许列表）
title: 插件智能体工具
x-i18n:
  generated_at: "2026-02-03T07:53:22Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 4479462e9d8b17b664bf6b5f424f2efc8e7bedeaabfdb6a93126e051e635c659
  source_path: plugins/agent-tools.md
  workflow: 15
---

# Outils d'agent de plugin

Les plugins OpenClaw peuvent enregistrer des **outils d'agent** (fonctions de schéma JSON) qui sont exposés au LLM pendant l'exécution de l'agent. Les outils peuvent être **obligatoires** (toujours disponibles) ou **optionnels** (activation sélective).

Les outils d'agent sont configurés sous `tools` dans la configuration principale, ou sous `agents.list[].tools` pour chaque agent. Les stratégies de liste d'autorisation/liste de refus contrôlent quels outils un agent peut appeler.

## Outil de base

```ts
import { Type } from "@sinclair/typebox";

export default function (api) {
  api.registerTool({
    name: "my_tool",
    description: "Do a thing",
    parameters: Type.Object({
      input: Type.String(),
    }),
    async execute(_id, params) {
      return { content: [{ type: "text", text: params.input }] };
    },
  });
}
```

## Outils optionnels (activation sélective)

Les outils optionnels ne sont **jamais** activés automatiquement. Les utilisateurs doivent les ajouter à la liste d'autorisation de l'agent.

```ts
export default function (api) {
  api.registerTool(
    {
      name: "workflow_tool",
      description: "Run a local workflow",
      parameters: {
        type: "object",
        properties: {
          pipeline: { type: "string" },
        },
        required: ["pipeline"],
      },
      async execute(_id, params) {
        return { content: [{ type: "text", text: params.pipeline }] };
      },
    },
    { optional: true },
  );
}
```

Activez les outils optionnels dans `agents.list[].tools.allow` (ou `tools.allow` global) :

```json5
{
  agents: {
    list: [
      {
        id: "main",
        tools: {
          allow: [
            "workflow_tool", // nom d'outil spécifique
            "workflow", // id du plugin (active tous les outils de ce plugin)
            "group:plugins", // tous les outils de plugin
          ],
        },
      },
    ],
  },
}
```

Autres options de configuration affectant la disponibilité des outils :

- Une liste d'autorisation contenant uniquement des noms d'outils de plugin est considérée comme une activation sélective du plugin ; les outils principaux restent activés, sauf si vous incluez également les outils principaux ou les groupes dans la liste d'autorisation.
- `tools.profile` / `agents.list[].tools.profile` (liste d'autorisation de base)
- `tools.byProvider` / `agents.list[].tools.byProvider` (autorisation/refus spécifique au fournisseur)
- `tools.sandbox.tools.*` (stratégie d'outils sandbox lors de l'isolation sandbox)

## Règles + conseils

- Les noms d'outils **ne peuvent pas** entrer en conflit avec les noms d'outils principaux ; les outils en conflit sont ignorés.
- Les id de plugin utilisés dans la liste d'autorisation ne peuvent pas entrer en conflit avec les noms d'outils principaux.
- Pour les outils qui déclenchent des effets secondaires ou qui nécessitent des fichiers binaires/identifiants supplémentaires, privilégiez `optional: true`.
