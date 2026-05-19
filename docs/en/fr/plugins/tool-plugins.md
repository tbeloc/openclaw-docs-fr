---
summary: "Créez des outils d'agent typés simples avec defineToolPlugin et openclaw plugins init/build/validate"
title: "Plugins d'outils"
sidebarTitle: "Plugins d'outils"
read_when:
  - You want to build a simple OpenClaw plugin that only adds agent tools
  - You want to use defineToolPlugin instead of hand-writing plugin manifest metadata
  - You need to scaffold, generate, validate, test, or publish a tool-only plugin
---

Les plugins d'outils ajoutent des outils appelables par agent à OpenClaw sans ajouter de canal,
fournisseur de modèle, hook, service ou backend de configuration. Utilisez `defineToolPlugin` quand le
plugin possède une liste fixe d'outils et que vous voulez qu'OpenClaw génère les métadonnées du manifeste
qui gardent ces outils découvrables sans charger le code d'exécution.

Le flux recommandé est :

1. Générez un package avec `openclaw plugins init`.
2. Écrivez les outils avec `defineToolPlugin`.
3. Générez JavaScript.
4. Générez les métadonnées `openclaw.plugin.json` et `package.json` avec
   `openclaw plugins build`.
5. Validez les métadonnées générées avant de publier ou d'installer.

Pour les plugins de fournisseur, canal, hook, service ou à capacités mixtes, commencez par
[Building plugins](/fr/plugins/building-plugins), [Channel Plugins](/fr/plugins/sdk-channel-plugins),
ou [Provider Plugins](/fr/plugins/sdk-provider-plugins) à la place.

## Exigences

- Node >= 22.
- Package TypeScript ESM en sortie.
- `typebox` pour les schémas de configuration et de paramètres d'outils.
- `openclaw >=2026.5.17`, la première version d'OpenClaw qui exporte
  `openclaw/plugin-sdk/tool-plugin`.
- Une racine de package qui peut livrer `dist/`, `openclaw.plugin.json`, et
  `package.json`.

Le plugin généré importe `typebox` à l'exécution, donc gardez `typebox` dans
`dependencies`, pas seulement `devDependencies`.

## Démarrage rapide

Créez un nouveau package de plugin :

```bash
openclaw plugins init stock-quotes --name "Stock Quotes"
cd stock-quotes
npm install
npm run plugin:build
npm run plugin:validate
npm test
```

L'échafaudage crée :

- `src/index.ts` : une entrée `defineToolPlugin` avec un outil `echo`.
- `src/index.test.ts` : un petit test de métadonnées.
- `tsconfig.json` : sortie TypeScript NodeNext vers `dist/`.
- `package.json` : scripts, dépendances d'exécution, et
  `openclaw.extensions: ["./dist/index.js"]`.
- `openclaw.plugin.json` : métadonnées du manifeste généré pour l'outil initial.

Sortie de validation attendue :

```text
Plugin stock-quotes is valid.
```

## Écrivez un outil

`defineToolPlugin` prend l'identité du plugin, un schéma de configuration optionnel, et une
liste statique d'outils. Les types de paramètres et de configuration sont déduits des
schémas TypeBox.

```typescript
import { Type } from "typebox";
import { defineToolPlugin } from "openclaw/plugin-sdk/tool-plugin";

export default defineToolPlugin({
  id: "stock-quotes",
  name: "Stock Quotes",
  description: "Fetch stock quote snapshots.",
  configSchema: Type.Object({
    apiKey: Type.Optional(Type.String({ description: "Quote API key." })),
    baseUrl: Type.Optional(Type.String({ description: "Quote API base URL." })),
  }),
  tools: (tool) => [
    tool({
      name: "stock_quote",
      label: "Stock Quote",
      description: "Fetch a stock quote snapshot.",
      parameters: Type.Object({
        symbol: Type.String({ description: "Ticker symbol, for example OPEN." }),
      }),
      async execute({ symbol }, config, context) {
        context.signal?.throwIfAborted();
        return {
          symbol: symbol.toUpperCase(),
          configured: Boolean(config.apiKey),
          baseUrl: config.baseUrl ?? "https://api.example.com",
        };
      },
    }),
  ],
});
```

Les noms d'outils sont l'API stable. Choisissez des noms qui sont uniques, en minuscules, et
suffisamment spécifiques pour éviter les collisions avec les outils principaux ou d'autres plugins.

## Outils optionnels et d'usine

Définissez `optional: true` quand les utilisateurs doivent explicitement autoriser l'outil avant qu'il
soit envoyé à un modèle :

```typescript
tool({
  name: "workflow_run",
  description: "Run an external workflow.",
  parameters: Type.Object({ goal: Type.String() }),
  optional: true,
  execute: ({ goal }) => ({ queued: true, goal }),
});
```

`openclaw plugins build` écrit l'entrée du manifeste `toolMetadata.<tool>.optional` correspondante,
donc OpenClaw peut découvrir l'outil sans charger le code d'exécution du plugin.

Utilisez `factory` quand un outil a besoin du contexte d'outil d'exécution avant de pouvoir
être créé. L'usine garde les métadonnées statiques tout en permettant à l'outil de se désactiver pour une
exécution spécifique, d'inspecter l'état du sandbox, ou de lier des aides d'exécution.

```typescript
tool({
  name: "local_workflow",
  description: "Run a local workflow outside sandboxed sessions.",
  parameters: Type.Object({ goal: Type.String() }),
  optional: true,
  factory({ api, toolContext }) {
    if (toolContext.sandboxed) {
      return null;
    }
    return createLocalWorkflowTool(api);
  },
});
```

Les usines sont toujours pour les noms d'outils fixes. Utilisez `definePluginEntry` directement quand
le plugin calcule les noms d'outils dynamiquement ou combine les outils avec des hooks,
services, fournisseurs, commandes ou d'autres surfaces d'exécution.

## Valeurs de retour

`defineToolPlugin` enveloppe les valeurs de retour simples dans le format de résultat d'outil OpenClaw :

- Retournez une chaîne quand le modèle doit voir ce texte exact.
- Retournez une valeur compatible JSON quand vous voulez que le modèle voie du JSON formaté
  et qu'OpenClaw garde la valeur originale dans `details`.

```typescript
tool({
  name: "echo_text",
  description: "Echo input text.",
  parameters: Type.Object({
    input: Type.String(),
  }),
  execute: ({ input }) => input,
});
```

```typescript
tool({
  name: "echo_json",
  description: "Echo input as structured JSON.",
  parameters: Type.Object({
    input: Type.String(),
  }),
  execute: ({ input }) => ({ input, length: input.length }),
});
```

Utilisez un outil d'usine quand vous avez besoin de retourner un `AgentToolResult` personnalisé ou de réutiliser
une implémentation `api.registerTool` existante. Utilisez `definePluginEntry` à la place de
`defineToolPlugin` quand vous avez besoin d'outils entièrement dynamiques ou de capacités de plugin mixtes.

## Configuration

`configSchema` est optionnel. Si vous l'omettez, OpenClaw utilise un schéma d'objet vide strict
et le manifeste généré inclut toujours `configSchema`.

```typescript
export default defineToolPlugin({
  id: "no-config-tools",
  name: "No Config Tools",
  description: "Adds tools that do not need configuration.",
  tools: () => [],
});
```

Quand vous incluez `configSchema`, le deuxième argument `execute` est typé à partir du
schéma :

```typescript
const configSchema = Type.Object({
  apiKey: Type.String(),
});

export default defineToolPlugin({
  id: "configured-tools",
  name: "Configured Tools",
  description: "Adds configured tools.",
  configSchema,
  tools: (tool) => [
    tool({
      name: "configured_ping",
      description: "Check whether configuration is available.",
      parameters: Type.Object({}),
      execute: (_params, config) => ({ hasKey: config.apiKey.length > 0 }),
    }),
  ],
});
```

OpenClaw lit la configuration du plugin à partir de l'entrée du plugin dans la configuration de la Gateway. Ne
codez pas en dur les secrets dans la source ou dans les exemples de docs. Utilisez la configuration, les variables
d'environnement, ou les SecretRefs selon le modèle de sécurité du plugin.

## Métadonnées générées

OpenClaw découvre les plugins installés à partir de métadonnées froides. Il doit pouvoir lire
le manifeste du plugin avant d'importer le code d'exécution du plugin. `defineToolPlugin`
expose donc des métadonnées statiques, et `openclaw plugins build` écrit ces
métadonnées dans le package.

Exécutez le générateur après avoir modifié l'id du plugin, le nom, la description, le schéma de configuration,
l'activation, ou les noms d'outils :

```bash
npm run build
openclaw plugins build --entry ./dist/index.js
```

Pour un plugin à un outil, le manifeste généré ressemble à ceci :

```json
{
  "id": "stock-quotes",
  "name": "Stock Quotes",
  "description": "Fetch stock quote snapshots.",
  "version": "0.1.0",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  },
  "activation": {
    "onStartup": true
  },
  "contracts": {
    "tools": ["stock_quote"]
  }
}
```

`contracts.tools` est le contrat de découverte important. Il dit à OpenClaw quel
plugin possède chaque outil sans charger chaque exécution de plugin installée. Si le
manifeste est obsolète, l'outil peut être manquant de la découverte ou le mauvais plugin
peut être blâmé pour une erreur d'enregistrement.

## Métadonnées du package

Pour le flux simple de plugin d'outil, `openclaw plugins build` aligne
`package.json` à l'entrée d'exécution unique sélectionnée :

```json
{
  "type": "module",
  "files": ["dist", "openclaw.plugin.json", "README.md"],
  "dependencies": {
    "typebox": "^1.1.38"
  },
  "peerDependencies": {
    "openclaw": ">=2026.5.17"
  },
  "openclaw": {
    "extensions": ["./dist/index.js"]
  }
}
```

Utilisez JavaScript construit comme `./dist/index.js` pour les packages installés. Les entrées source
sont utiles dans le développement d'espace de travail, mais les packages publiés ne doivent pas
dépendre du chargement d'exécution TypeScript.

## Validez en CI

Utilisez `plugins build --check` pour échouer CI quand les métadonnées générées sont obsolètes sans
réécrire les fichiers :

```bash
npm run build
openclaw plugins build --entry ./dist/index.js --check
openclaw plugins validate --entry ./dist/index.js
npm test
```

`plugins validate` vérifie que :

- `openclaw.plugin.json` existe et passe le chargeur de manifeste normal.
- L'entrée actuelle exporte les métadonnées `defineToolPlugin`.
- Les champs du manifeste généré correspondent aux métadonnées d'entrée.
- `contracts.tools` correspond aux noms d'outils déclarés.
- `package.json` pointe `openclaw.extensions` vers l'entrée d'exécution sélectionnée.

## Installez et inspectez localement

À partir d'une extraction OpenClaw séparée ou d'une CLI installée, installez le chemin du package :

```bash
openclaw plugins install ./stock-quotes
openclaw plugins inspect stock-quotes --runtime
```

Pour un test de package, emballez d'abord et installez le tarball :

```bash
npm pack
openclaw plugins install npm-pack:./openclaw-plugin-stock-quotes-0.1.0.tgz
openclaw plugins inspect stock-quotes --runtime --json
```

Après l'installation, démarrez ou redémarrez la Gateway et demandez à l'agent d'utiliser l'
outil. Si vous déboguez la visibilité des outils, inspectez l'exécution du plugin et le
catalogue d'outils effectif avant de modifier le code.

## Publier

Publiez via ClawHub quand le package est prêt :

```bash
clawhub package publish your-org/stock-quotes --dry-run
clawhub package publish your-org/stock-quotes
```

Installez avec un localisateur ClawHub explicite :

```bash
openclaw plugins install clawhub:your-org/stock-quotes
```

Les spécifications de packages npm simples restent prises en charge pendant la transition de lancement, mais ClawHub
est la surface de découverte et de distribution préférée pour les plugins OpenClaw.

## Dépannage

### `plugin entry not found: ./dist/index.js`

Le fichier d'entrée sélectionné n'existe pas. Exécutez `npm run build`, puis réexécutez
`openclaw plugins build --entry ./dist/index.js` ou
`openclaw plugins validate --entry ./dist/index.js`.

### `plugin entry does not expose defineToolPlugin metadata`

L'entrée n'a pas exporté une valeur créée par `defineToolPlugin`. Vérifiez que
l'export par défaut du module est le résultat de `defineToolPlugin(...)`, ou passez l'entrée correcte avec `--entry`.

### `openclaw.plugin.json generated metadata is stale`

Le manifeste ne correspond plus aux métadonnées d'entrée. Exécutez :

```bash
npm run build
openclaw plugins build --entry ./dist/index.js
```

Validez les modifications apportées à `openclaw.plugin.json` et `package.json`.

### `package.json openclaw.extensions must include ./dist/index.js`

Les métadonnées du package pointent vers une entrée runtime différente. Exécutez
`openclaw plugins build --entry ./dist/index.js` pour que le générateur aligne
les métadonnées du package avec l'entrée que vous avez l'intention de livrer.

### `Cannot find package 'typebox'`

Le plugin compilé importe `typebox` au moment de l'exécution. Conservez `typebox` dans
`dependencies`, réinstallez les dépendances du package, recompilez et réexécutez la validation.

### L'outil n'apparaît pas après l'installation

Vérifiez ces points dans l'ordre :

1. `openclaw plugins inspect <plugin-id> --runtime`
2. `openclaw plugins validate --root <plugin-root> --entry ./dist/index.js`
3. `openclaw.plugin.json` contient `contracts.tools` avec les noms d'outils attendus.
4. `package.json` contient `openclaw.extensions: ["./dist/index.js"]`.
5. La passerelle a été redémarrée ou rechargée après l'installation du plugin.

## Voir aussi

- [Créer des plugins](/fr/plugins/building-plugins)
- [Points d'entrée des plugins](/fr/plugins/sdk-entrypoints)
- [Sous-chemins du SDK des plugins](/fr/plugins/sdk-subpaths)
- [Manifeste des plugins](/fr/plugins/manifest)
- [CLI des plugins](/fr/cli/plugins)
- [Publication sur ClawHub](/fr/clawhub/publishing)
