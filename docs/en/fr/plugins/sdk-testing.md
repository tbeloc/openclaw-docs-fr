---
title: "Tests du SDK Plugin"
sidebarTitle: "Tests"
summary: "Comment tester le code des plugins avec les assistants de test publics et les petits doublures de test locales"
read_when:
  - You are writing tests for a plugin
  - You need fixtures for Windows command shims or shared routing failures
  - You want to know what the public testing surface includes
---

# Tests du SDK Plugin

OpenClaw maintient intentionnellement la surface de test publique réduite.

Utilisez `openclaw/plugin-sdk/testing` pour les assistants suffisamment stables pour être supportés
par les auteurs de plugins, et construisez de petites doublures locales au plugin pour tout le reste.

## Assistants de test publics

Les assistants actuels incluent :

- `createWindowsCmdShimFixture(...)`
- `installCommonResolveTargetErrorCases(...)`
- `shouldAckReaction(...)`
- `removeAckReactionAfterReply(...)`

La surface de test réexporte également certains types partagés :

- `OpenClawConfig`
- `PluginRuntime`
- `RuntimeEnv`
- `ChannelAccountSnapshot`
- `ChannelGatewayContext`

## Exemple : fixture de shim de commande Windows

```ts
import { createWindowsCmdShimFixture } from "openclaw/plugin-sdk/testing";
import { describe, expect, it } from "vitest";

describe("example CLI integration", () => {
  it("creates a command shim", async () => {
    await createWindowsCmdShimFixture({
      shimPath: "/tmp/example.cmd",
      scriptPath: "/tmp/example.js",
      shimLine: 'node "%~dp0\\example.js" %*',
    });

    expect(true).toBe(true);
  });
});
```

## Exemple : échecs de résolution de cible partagés

```ts
import { installCommonResolveTargetErrorCases } from "openclaw/plugin-sdk/testing";

installCommonResolveTargetErrorCases({
  implicitAllowFrom: ["user-1"],
  resolveTarget({ to, mode, allowFrom }) {
    if (!to?.trim()) {
      return { ok: false, error: new Error("missing target") };
    }
    if (mode === "implicit" && allowFrom.length > 0 && to === "invalid-target") {
      return { ok: false, error: new Error("invalid target") };
    }
    return { ok: true, to };
  },
});
```

## Doublures de runtime

Il n'y a pas d'export `createTestRuntime()` fourre-tout sur le SDK public aujourd'hui.
À la place :

- utilisez les assistants de test publics où ils conviennent
- utilisez `plugin-sdk/runtime` pour les petits adaptateurs de runtime
- construisez de minuscules doublures de runtime locales au plugin pour le reste

Exemple :

```ts
import { createLoggerBackedRuntime } from "openclaw/plugin-sdk/runtime";

const logs: string[] = [];

const runtime = createLoggerBackedRuntime({
  logger: {
    info(message) {
      logs.push(`info:${message}`);
    },
    error(message) {
      logs.push(`error:${message}`);
    },
  },
});
```

## Conseils de test

- Préférez les tests unitaires ciblés aux grands harnais de bout en bout.
- Importez les types purs à partir de chemins SDK ciblés dans les tests.
- Gardez les doublures de test locales au plugin petites et explicites.
- Évitez de dépendre des internes de test OpenClaw non exportés.

## Connexes

- [Building Plugins](/fr/plugins/building-plugins)
- [Plugin SDK Overview](/fr/plugins/sdk-overview)
- [Plugin Runtime](/fr/plugins/sdk-runtime)
