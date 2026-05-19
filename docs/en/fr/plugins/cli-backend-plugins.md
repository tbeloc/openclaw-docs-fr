---
summary: "Créer un plugin qui enregistre un backend CLI d'IA local"
title: "Créer des plugins de backend CLI"
sidebarTitle: "Plugins de backend CLI"
read_when:
  - You are building a local AI CLI backend plugin
  - You want to register a backend for model refs such as acme-cli/model
  - You need to map a third-party CLI into OpenClaw's text fallback runner
---

Les plugins de backend CLI permettent à OpenClaw d'appeler une CLI d'IA locale en tant que backend d'inférence textuelle. Le backend apparaît comme un préfixe de fournisseur dans les références de modèle :

```text
acme-cli/acme-large
```

Utilisez un backend CLI quand l'intégration en amont est déjà exposée en tant que commande locale, quand la CLI possède l'état de connexion local, ou quand la CLI est un bon repli si les fournisseurs d'API ne sont pas disponibles.

<Info>
  Si le service en amont expose une API de modèle HTTP normale, écrivez plutôt un
  [plugin de fournisseur](/fr/plugins/sdk-provider-plugins). Si le runtime en amont possède des sessions d'agent complètes, des événements d'outils, une compaction ou un état de tâche en arrière-plan, utilisez un [agent harness](/fr/plugins/sdk-agent-harness).
</Info>

## Ce que le plugin possède

Un plugin de backend CLI a trois contrats :

| Contrat              | Fichier                | Objectif                                                  |
| -------------------- | ---------------------- | --------------------------------------------------------- |
| Entrée du package    | `package.json`         | Pointe OpenClaw vers le module runtime du plugin          |
| Propriété du manifest| `openclaw.plugin.json` | Déclare l'id du backend avant le chargement du runtime    |
| Enregistrement runtime| `index.ts`             | Appelle `api.registerCliBackend(...)` avec les défauts    |

Le manifest est une métadonnée de découverte. Il n'exécute pas la CLI et n'enregistre pas le comportement du runtime. Le comportement du runtime commence quand l'entrée du plugin appelle `api.registerCliBackend(...)`.

## Plugin de backend minimal

<Steps>
  <Step title="Créer les métadonnées du package">
    ```json package.json
    {
      "name": "@acme/openclaw-acme-cli",
      "version": "1.0.0",
      "type": "module",
      "openclaw": {
        "extensions": ["./index.ts"],
        "compat": {
          "pluginApi": ">=2026.3.24-beta.2",
          "minGatewayVersion": "2026.3.24-beta.2"
        },
        "build": {
          "openclawVersion": "2026.3.24-beta.2",
          "pluginSdkVersion": "2026.3.24-beta.2"
        }
      },
      "dependencies": {
        "openclaw": "^2026.3.24"
      },
      "devDependencies": {
        "typescript": "^5.9.0"
      }
    }
    ```

    Les packages publiés doivent livrer les fichiers runtime JavaScript compilés. Si votre entrée source est `./src/index.ts`, ajoutez `openclaw.runtimeExtensions` qui pointe vers le pair JavaScript compilé. Voir [Points d'entrée](/fr/plugins/sdk-entrypoints).

  </Step>

  <Step title="Déclarer la propriété du backend">
    ```json openclaw.plugin.json
    {
      "id": "acme-cli",
      "name": "Acme CLI",
      "description": "Run Acme's local AI CLI through OpenClaw",
      "cliBackends": ["acme-cli"],
      "setup": {
        "cliBackends": ["acme-cli"],
        "requiresRuntime": false
      },
      "activation": {
        "onStartup": false
      },
      "configSchema": {
        "type": "object",
        "additionalProperties": false
      }
    }
    ```

    `cliBackends` est la liste de propriété du runtime. Elle permet à OpenClaw de charger automatiquement le plugin quand la configuration ou la sélection de modèle mentionne `acme-cli/...`.

    `setup.cliBackends` est la surface de configuration descriptor-first. Ajoutez-la quand la découverte de modèle, l'intégration ou le statut doivent reconnaître le backend sans charger le runtime du plugin. Utilisez `requiresRuntime: false` uniquement quand ces descripteurs statiques suffisent pour la configuration.

  </Step>

  <Step title="Enregistrer le backend">
    ```typescript index.ts
    import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
    import {
      CLI_FRESH_WATCHDOG_DEFAULTS,
      CLI_RESUME_WATCHDOG_DEFAULTS,
      type CliBackendPlugin,
    } from "openclaw/plugin-sdk/cli-backend";

    function buildAcmeCliBackend(): CliBackendPlugin {
      return {
        id: "acme-cli",
        liveTest: {
          defaultModelRef: "acme-cli/acme-large",
          defaultImageProbe: false,
          defaultMcpProbe: false,
          docker: {
            npmPackage: "@acme/acme-cli",
            binaryName: "acme",
          },
        },
        config: {
          command: "acme",
          args: ["chat", "--json"],
          output: "json",
          input: "stdin",
          modelArg: "--model",
          sessionArg: "--session",
          sessionMode: "existing",
          sessionIdFields: ["session_id", "conversation_id"],
          systemPromptFileArg: "--system-file",
          systemPromptWhen: "first",
          imageArg: "--image",
          imageMode: "repeat",
          reliability: {
            watchdog: {
              fresh: { ...CLI_FRESH_WATCHDOG_DEFAULTS },
              resume: { ...CLI_RESUME_WATCHDOG_DEFAULTS },
            },
          },
          serialize: true,
        },
      };
    }

    export default definePluginEntry({
      id: "acme-cli",
      name: "Acme CLI",
      description: "Run Acme's local AI CLI through OpenClaw",
      register(api) {
        api.registerCliBackend(buildAcmeCliBackend());
      },
    });
    ```

    L'id du backend doit correspondre à l'entrée `cliBackends` du manifest. La `config` enregistrée n'est que la valeur par défaut ; la configuration utilisateur sous `agents.defaults.cliBackends.acme-cli` est fusionnée par-dessus au runtime.

  </Step>
</Steps>

## Forme de la configuration

`CliBackendConfig` décrit comment OpenClaw doit lancer et analyser la CLI :

| Champ                                     | Utilisation                                             |
| ----------------------------------------- | ------------------------------------------------------- |
| `command`                                 | Nom du binaire ou chemin de commande absolu             |
| `args`                                    | argv de base pour les exécutions fraîches                |
| `resumeArgs`                              | argv alternatif pour les sessions reprises ; supporte `{sessionId}` |
| `output` / `resumeOutput`                 | Analyseur : `json`, `jsonl`, ou `text`                  |
| `input`                                   | Transport du prompt : `arg` ou `stdin`                  |
| `modelArg`                                | Drapeau utilisé avant l'id du modèle                    |
| `modelAliases`                            | Mapper les ids de modèle OpenClaw aux ids natifs de la CLI |
| `sessionArg` / `sessionArgs`              | Comment passer un id de session                         |
| `sessionMode`                             | `always`, `existing`, ou `none`                         |
| `sessionIdFields`                         | Champs JSON que OpenClaw lit depuis la sortie de la CLI |
| `systemPromptArg` / `systemPromptFileArg` | Transport du prompt système                             |
| `systemPromptWhen`                        | `first`, `always`, ou `never`                           |
| `imageArg` / `imageMode`                  | Support du chemin d'image                               |
| `serialize`                               | Garder les exécutions du même backend ordonnées         |
| `reliability.watchdog`                    | Réglage du timeout sans sortie                          |

Préférez la plus petite configuration statique qui correspond à la CLI. Ajoutez des callbacks de plugin uniquement pour le comportement qui appartient vraiment au backend.

## Hooks de backend avancés

`CliBackendPlugin` peut aussi définir :

| Hook                               | Utilisation                                            |
| ---------------------------------- | ------------------------------------------------------ |
| `normalizeConfig(config, context)` | Réécrire la configuration utilisateur héritée après fusion |
| `resolveExecutionArgs(ctx)`        | Ajouter des drapeaux scoped à la requête comme l'effort de réflexion |
| `prepareExecution(ctx)`            | Créer des ponts d'authentification ou de configuration temporaires avant le lancement |
| `transformSystemPrompt(ctx)`       | Appliquer une transformation finale du prompt système spécifique à la CLI |
| `textTransforms`                   | Remplacements bidirectionnels prompt/sortie            |
| `defaultAuthProfileId`             | Préférer un profil d'authentification OpenClaw spécifique |
| `authEpochMode`                    | Décider comment les changements d'authentification invalident les sessions CLI stockées |
| `nativeToolMode`                   | Déclarer si la CLI a des outils natifs toujours activés |
| `bundleMcp` / `bundleMcpMode`      | Opter pour le pont d'outils MCP en boucle fermée d'OpenClaw |

Gardez ces hooks propriétaires du fournisseur. N'ajoutez pas de branches spécifiques à la CLI au cœur quand un hook de backend peut exprimer le comportement.

## Pont d'outils MCP

Les backends CLI ne reçoivent pas les outils OpenClaw par défaut. Si la CLI peut consommer une configuration MCP, optez explicitement :

```typescript
return {
  id: "acme-cli",
  bundleMcp: true,
  bundleMcpMode: "codex-config-overrides",
  config: {
    command: "acme",
    args: ["chat", "--json"],
    output: "json",
  },
};
```

Les modes de pont supportés sont :

| Mode                     | Utilisation                                                      |
| ------------------------ | ---------------------------------------------------------------- |
| `claude-config-file`     | CLIs qui acceptent un fichier de configuration MCP                |
| `codex-config-overrides` | CLIs qui acceptent des remplacements de configuration sur argv    |
| `gemini-system-settings` | CLIs qui lisent les paramètres MCP depuis leur répertoire de paramètres système |

Activez le pont uniquement quand la CLI peut réellement le consommer. Si la CLI a sa propre couche d'outils intégrée qui ne peut pas être désactivée, définissez `nativeToolMode: "always-on"` pour qu'OpenClaw puisse échouer fermé quand un appelant ne nécessite pas d'outils natifs.

## Configuration utilisateur

Les utilisateurs peuvent remplacer n'importe quel défaut du backend :

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "acme-cli": {
          command: "/opt/acme/bin/acme",
          args: ["chat", "--json", "--profile", "work"],
          modelAliases: {
            large: "acme-large-2026",
          },
        },
      },
      model: {
        primary: "openai/gpt-5.5",
        fallbacks: ["acme-cli/large"],
      },
    },
  },
}
```

Documentez le remplacement minimum que les utilisateurs sont susceptibles de nécessiter. Généralement, c'est uniquement `command` quand le binaire est en dehors de `PATH`.

## Vérification

Pour les plugins groupés, ajoutez un test ciblé autour du constructeur et de l'enregistrement de configuration, puis exécutez la voie de test ciblée du plugin :

```bash
pnpm test extensions/acme-cli
```

Pour les plugins locaux ou installés, vérifiez la découverte et une exécution de modèle réelle :

```bash
openclaw plugins inspect acme-cli --runtime --json
openclaw agent --message "reply exactly: backend ok" --model acme-cli/acme-large
```

Si le backend supporte les images ou MCP, ajoutez un smoke test en direct qui prouve ces chemins avec la CLI réelle. Ne vous fiez pas à l'inspection statique pour le comportement du prompt, de l'image, de MCP ou de la reprise de session.

## Liste de contrôle

<Check>`package.json` a `openclaw.extensions` et les entrées de runtime compilées pour les packages publiés</Check>
<Check>`openclaw.plugin.json` déclare `cliBackends` et `activation.onStartup` intentionnel</Check>
<Check>`setup.cliBackends` est présent quand la configuration/découverte de modèle doit voir le backend à froid</Check>
<Check>`api.registerCliBackend(...)` utilise le même id de backend que le manifest</Check>
<Check>Les remplacements utilisateur sous `agents.defaults.cliBackends.<id>` gagnent toujours</Check>
<Check>Les paramètres de session, prompt système, image et analyseur de sortie correspondent au contrat CLI réel</Check>
<Check>Les tests ciblés et au moins un smoke test CLI en direct prouvent le chemin du backend</Check>

## Connexes

- [Backends CLI](/fr/gateway/cli-backends) - configuration utilisateur et comportement à l'exécution
- [Création de plugins](/fr/plugins/building-plugins) - bases des packages et manifestes
- [Aperçu du SDK Plugin](/fr/plugins/sdk-overview) - référence de l'API d'enregistrement
- [Manifeste du plugin](/fr/plugins/manifest) - descripteurs `cliBackends` et setup
- [Agent harness](/fr/plugins/sdk-agent-harness) - runtimes d'agents externes complets
