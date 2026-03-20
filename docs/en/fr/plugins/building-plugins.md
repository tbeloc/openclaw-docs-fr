---
title: "Créer des plugins"
sidebarTitle: "Créer des plugins"
summary: "Guide étape par étape pour créer des plugins OpenClaw avec n'importe quelle combinaison de capacités"
read_when:
  - You want to create a new OpenClaw plugin
  - You need to understand the plugin SDK import patterns
  - You are adding a new channel, provider, tool, or other capability to OpenClaw
---

# Créer des plugins

Les plugins étendent OpenClaw avec de nouvelles capacités : canaux, fournisseurs de modèles, synthèse vocale,
génération d'images, recherche web, outils d'agent, ou n'importe quelle combinaison. Un seul plugin
peut enregistrer plusieurs capacités.

OpenClaw encourage le **développement de plugins externes**. Vous n'avez pas besoin d'ajouter votre
plugin au référentiel OpenClaw. Publiez votre plugin sur npm, et les utilisateurs l'installent
avec `openclaw plugins install <npm-spec>`. OpenClaw maintient également un ensemble de
plugins principaux dans le référentiel, mais le système de plugins est conçu pour une propriété
et une distribution indépendantes.

## Prérequis

- Node >= 22 et un gestionnaire de paquets (npm ou pnpm)
- Familiarité avec TypeScript (ESM)
- Pour les plugins dans le référentiel : référentiel OpenClaw cloné et `pnpm install` effectué

## Capacités des plugins

Un plugin peut enregistrer une ou plusieurs capacités. La capacité que vous enregistrez
détermine ce que votre plugin fournit à OpenClaw :

| Capacité            | Méthode d'enregistrement                      | Ce qu'elle ajoute                    |
| ------------------- | --------------------------------------------- | ------------------------------------ |
| Inférence textuelle  | `api.registerProvider(...)`                   | Fournisseur de modèle (LLM)          |
| Canal / messagerie   | `api.registerChannel(...)`                    | Canal de chat (ex. Slack, IRC)       |
| Synthèse vocale      | `api.registerSpeechProvider(...)`             | Synthèse vocale / STT                |
| Compréhension média  | `api.registerMediaUnderstandingProvider(...)` | Analyse image/audio/vidéo            |
| Génération d'images  | `api.registerImageGenerationProvider(...)`    | Génération d'images                  |
| Recherche web        | `api.registerWebSearchProvider(...)`          | Fournisseur de recherche web         |
| Outils d'agent       | `api.registerTool(...)`                       | Outils appelables par l'agent        |

Un plugin qui enregistre zéro capacité mais fournit des hooks ou des services est un
plugin **hook-only**. Ce modèle est toujours supporté.

## Structure du plugin

Les plugins suivent cette disposition (qu'ils soient dans le référentiel ou autonomes) :

```
my-plugin/
├── package.json          # Métadonnées npm + configuration openclaw
├── openclaw.plugin.json  # Manifeste du plugin
├── index.ts              # Point d'entrée
├── setup-entry.ts        # Assistant de configuration (optionnel)
├── api.ts                # Exports publics (optionnel)
├── runtime-api.ts        # Exports internes (optionnel)
└── src/
    ├── provider.ts       # Implémentation de capacité
    ├── runtime.ts        # Câblage d'exécution
    └── *.test.ts         # Tests colocalisés
```

## Créer un plugin

<Steps>
  <Step title="Créer le paquet">
    Créez `package.json` avec le bloc de métadonnées `openclaw`. La structure
    dépend des capacités que votre plugin fournit.

    **Exemple de plugin de canal :**

    ```json
    {
      "name": "@myorg/openclaw-my-channel",
      "version": "1.0.0",
      "type": "module",
      "openclaw": {
        "extensions": ["./index.ts"],
        "channel": {
          "id": "my-channel",
          "label": "My Channel",
          "blurb": "Short description of the channel."
        }
      }
    }
    ```

    **Exemple de plugin fournisseur :**

    ```json
    {
      "name": "@myorg/openclaw-my-provider",
      "version": "1.0.0",
      "type": "module",
      "openclaw": {
        "extensions": ["./index.ts"],
        "providers": ["my-provider"]
      }
    }
    ```

    Le champ `openclaw` indique au système de plugins ce que votre plugin fournit.
    Un plugin peut déclarer à la fois `channel` et `providers` s'il fournit plusieurs
    capacités.

  </Step>

  <Step title="Définir le point d'entrée">
    Le point d'entrée enregistre vos capacités avec l'API du plugin.

    **Plugin de canal :**

    ```typescript
    import { defineChannelPluginEntry } from "openclaw/plugin-sdk/core";

    export default defineChannelPluginEntry({
      id: "my-channel",
      name: "My Channel",
      description: "Connects OpenClaw to My Channel",
      plugin: {
        // Implémentation de l'adaptateur de canal
      },
    });
    ```

    **Plugin fournisseur :**

    ```typescript
    import { definePluginEntry } from "openclaw/plugin-sdk/core";

    export default definePluginEntry({
      id: "my-provider",
      name: "My Provider",
      register(api) {
        api.registerProvider({
          // Implémentation du fournisseur
        });
      },
    });
    ```

    **Plugin multi-capacité** (fournisseur + outil) :

    ```typescript
    import { definePluginEntry } from "openclaw/plugin-sdk/core";

    export default definePluginEntry({
      id: "my-plugin",
      name: "My Plugin",
      register(api) {
        api.registerProvider({ /* ... */ });
        api.registerTool({ /* ... */ });
        api.registerImageGenerationProvider({ /* ... */ });
      },
    });
    ```

    Utilisez `defineChannelPluginEntry` pour les plugins de canal et `definePluginEntry`
    pour tout le reste. Un seul plugin peut enregistrer autant de capacités que nécessaire.

  </Step>

  <Step title="Importer depuis des chemins SDK ciblés">
    Importez toujours depuis des chemins spécifiques `openclaw/plugin-sdk/\<subpath\>`. L'ancien
    import monolithique est déprécié (voir [Migration SDK](/fr/plugins/sdk-migration)).

    ```typescript
    // Correct : chemins ciblés
    import { definePluginEntry } from "openclaw/plugin-sdk/core";
    import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";
    import { buildOauthProviderAuthResult } from "openclaw/plugin-sdk/provider-oauth";

    // Incorrect : racine monolithique (le linter rejettera ceci)
    import { ... } from "openclaw/plugin-sdk";
    ```

    <Accordion title="Référence des chemins courants">
      | Chemin | Objectif |
      | --- | --- |
      | `plugin-sdk/core` | Définitions d'entrée de plugin et types de base |
      | `plugin-sdk/channel-setup` | Adaptateurs d'assistant de configuration |
      | `plugin-sdk/channel-pairing` | Primitives d'appairage DM |
      | `plugin-sdk/channel-reply-pipeline` | Câblage de préfixe de réponse + saisie |
      | `plugin-sdk/channel-config-schema` | Constructeurs de schéma de configuration |
      | `plugin-sdk/channel-policy` | Aides de politique groupe/DM |
      | `plugin-sdk/secret-input` | Analyse/aides d'entrée secrète |
      | `plugin-sdk/webhook-ingress` | Aides de requête/cible webhook |
      | `plugin-sdk/runtime-store` | Stockage persistant du plugin |
      | `plugin-sdk/allow-from` | Résolution de liste blanche |
      | `plugin-sdk/reply-payload` | Types de réponse de message |
      | `plugin-sdk/provider-oauth` | Aides de connexion OAuth + PKCE |
      | `plugin-sdk/provider-onboard` | Correctifs de configuration d'intégration du fournisseur |
      | `plugin-sdk/testing` | Utilitaires de test |
    </Accordion>

    Utilisez le chemin le plus étroit qui correspond à la tâche.

  </Step>

  <Step title="Utiliser des modules locaux pour les imports internes">
    Dans votre plugin, créez des fichiers de module locaux pour le partage de code interne
    au lieu de réimporter via le SDK du plugin :

    ```typescript
    // api.ts — exports publics pour ce plugin
    export { MyConfig } from "./src/config.js";
    export { MyRuntime } from "./src/runtime.js";

    // runtime-api.ts — exports internes uniquement
    export { internalHelper } from "./src/helpers.js";
    ```

    <Warning>
      N'importez jamais votre propre plugin via son chemin SDK publié depuis les fichiers
      de production. Routez les imports internes via des fichiers locaux comme `./api.ts`
      ou `./runtime-api.ts`. Le chemin SDK est réservé aux consommateurs externes uniquement.
    </Warning>

  </Step>

  <Step title="Ajouter un manifeste de plugin">
    Créez `openclaw.plugin.json` à la racine de votre plugin :

    ```json
    {
      "id": "my-plugin",
      "kind": "provider",
      "name": "My Plugin",
      "description": "Adds My Provider to OpenClaw"
    }
    ```

    Pour les plugins de canal, définissez `"kind": "channel"` et ajoutez `"channels": ["my-channel"]`.

    Voir [Manifeste du plugin](/fr/plugins/manifest) pour le schéma complet.

  </Step>

  <Step title="Tester votre plugin">
    **Plugins externes :** exécutez votre propre suite de tests contre les contrats du SDK du plugin.

    **Plugins dans le référentiel :** OpenClaw exécute des tests de contrat contre tous les plugins enregistrés :

    ```bash
    pnpm test:contracts:channels   # plugins de canal
    pnpm test:contracts:plugins    # plugins fournisseur
    ```

    Pour les tests unitaires, importez les aides de test depuis la surface de test :

    ```typescript
    import { createTestRuntime } from "openclaw/plugin-sdk/testing";
    ```

  </Step>

  <Step title="Publier et installer">
    **Plugins externes :** publiez sur npm, puis installez :

    ```bash
    npm publish
    openclaw plugins install @myorg/openclaw-my-plugin
    ```

    **Plugins dans le référentiel :** placez le plugin sous `extensions/` et il est
    automatiquement découvert lors de la compilation.

    Les utilisateurs peuvent parcourir et installer des plugins communautaires avec :

    ```bash
    openclaw plugins search <query>
    openclaw plugins install <npm-spec>
    ```

  </Step>
</Steps>

## Application du linting (plugins dans le référentiel)

Trois scripts appliquent les limites du SDK pour les plugins du référentiel OpenClaw :

1. **Pas d'imports de racine monolithique** — la racine `openclaw/plugin-sdk` est rejetée
2. **Pas d'imports directs src/** — les plugins ne peuvent pas importer `../../src/` directement
3. **Pas d'auto-imports** — les plugins ne peuvent pas importer leur propre chemin `plugin-sdk/\<name\>`

Exécutez `pnpm check` pour vérifier toutes les limites avant de valider.

Les plugins externes ne sont pas soumis à ces règles de linting, mais suivre les mêmes
modèles est fortement recommandé.

## Liste de contrôle pré-soumission

<Check>**package.json** a les métadonnées `openclaw` correctes</Check>
<Check>Le point d'entrée utilise `defineChannelPluginEntry` ou `definePluginEntry`</Check>
<Check>Tous les imports utilisent des chemins `plugin-sdk/\<subpath\>` ciblés</Check>
<Check>Les imports internes utilisent des modules locaux, pas d'auto-imports SDK</Check>
<Check>Le manifeste `openclaw.plugin.json` est présent et valide</Check>
<Check>Les tests passent</Check>
<Check>`pnpm check` passe (plugins dans le référentiel)</Check>

## Connexes

- [Migration SDK du plugin](/fr/plugins/sdk-migration) — migration depuis l'import compat déprécié
- [Architecture du plugin](/fr/plugins/architecture) — internals et modèle de capacité
- [Manifeste du plugin](/fr/plugins/manifest) — schéma manifeste complet
- [Outils d'agent du plugin](/fr/plugins/agent-tools) — ajouter des outils d'agent dans un plugin
- [Plugins communautaires](/fr/plugins/community) — listing et barre de qualité
