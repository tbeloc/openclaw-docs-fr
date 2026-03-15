---
summary: "Écrire des outils d'agent dans un plugin (schémas, outils optionnels, listes blanches)"
read_when:
  - You want to add a new agent tool in a plugin
  - You need to make a tool opt-in via allowlists
title: "Outils d'agent de plugin"
---

# Outils d'agent de plugin

Les plugins OpenClaw peuvent enregistrer des **outils d'agent** (fonctions JSON‑schema) qui sont exposés
à l'LLM lors des exécutions d'agent. Les outils peuvent être **obligatoires** (toujours disponibles) ou
**optionnels** (opt‑in).

Les outils d'agent sont configurés sous `tools` dans la configuration principale, ou par‑agent sous
`agents.list[].tools`. La politique de liste blanche/liste noire contrôle quels outils l'agent
peut appeler.

## Outil basique

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

## Outil optionnel (opt‑in)

Les outils optionnels ne sont **jamais** activés automatiquement. Les utilisateurs doivent les ajouter à une
liste blanche d'agent.

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

Activez les outils optionnels dans `agents.list[].tools.allow` (ou global `tools.allow`) :

```json5
{
  agents: {
    list: [
      {
        id: "main",
        tools: {
          allow: [
            "workflow_tool", // specific tool name
            "workflow", // plugin id (enables all tools from that plugin)
            "group:plugins", // all plugin tools
          ],
        },
      },
    ],
  },
}
```

Autres paramètres de configuration qui affectent la disponibilité des outils :

- Les listes blanches qui ne nomment que des outils de plugin sont traitées comme des opt-ins de plugin ; les outils principaux restent
  activés sauf si vous incluez également des outils principaux ou des groupes dans la liste blanche.
- `tools.profile` / `agents.list[].tools.profile` (liste blanche de base)
- `tools.byProvider` / `agents.list[].tools.byProvider` (allow/deny spécifique au fournisseur)
- `tools.sandbox.tools.*` (politique d'outil sandbox en cas de sandboxing)

## Règles + conseils

- Les noms d'outils ne doivent **pas** entrer en conflit avec les noms d'outils principaux ; les outils en conflit sont ignorés.
- Les identifiants de plugin utilisés dans les listes blanches ne doivent pas entrer en conflit avec les noms d'outils principaux.
- Préférez `optional: true` pour les outils qui déclenchent des effets secondaires ou qui nécessitent des
  binaires/identifiants supplémentaires.
