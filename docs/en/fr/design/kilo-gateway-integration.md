# Conception de l'intégration du fournisseur Kilo Gateway

## Aperçu

Ce document décrit la conception pour intégrer « Kilo Gateway » en tant que fournisseur de première classe dans OpenClaw, modélisé d'après l'implémentation OpenRouter existante. Kilo Gateway utilise une API de complétions compatible avec OpenAI avec une URL de base différente.

## Décisions de conception

### 1. Dénomination du fournisseur

**Recommandation : `kilocode`**

Justification :

- Correspond à l'exemple de configuration utilisateur fourni (clé de fournisseur `kilocode`)
- Cohérent avec les modèles de dénomination des fournisseurs existants (par exemple, `openrouter`, `opencode`, `moonshot`)
- Court et mémorisable
- Évite la confusion avec les termes génériques « kilo » ou « gateway »

Alternative envisagée : `kilo-gateway` - rejetée car les noms avec tirets sont moins courants dans la base de code et `kilocode` est plus concis.

### 2. Référence de modèle par défaut

**Recommandation : `kilocode/anthropic/claude-opus-4.6`**

Justification :

- Basé sur l'exemple de configuration utilisateur
- Claude Opus 4.5 est un modèle par défaut capable
- La sélection explicite du modèle évite la dépendance à l'acheminement automatique

### 3. Configuration de l'URL de base

**Recommandation : Valeur par défaut codée en dur avec remplacement de configuration**

- **URL de base par défaut :** `https://api.kilo.ai/api/gateway/`
- **Configurable :** Oui, via `models.providers.kilocode.baseUrl`

Cela correspond au modèle utilisé par d'autres fournisseurs comme Moonshot, Venice et Synthetic.

### 4. Analyse des modèles

**Recommandation : Pas de point de terminaison d'analyse de modèles dédié initialement**

Justification :

- Kilo Gateway fait un proxy vers OpenRouter, donc les modèles sont dynamiques
- Les utilisateurs peuvent configurer manuellement les modèles dans leur configuration
- Si Kilo Gateway expose un point de terminaison `/models` à l'avenir, l'analyse peut être ajoutée

### 5. Gestion spéciale

**Recommandation : Hériter du comportement OpenRouter pour les modèles Anthropic**

Puisque Kilo Gateway fait un proxy vers OpenRouter, la même gestion spéciale devrait s'appliquer :

- Éligibilité TTL du cache pour les modèles `anthropic/*`
- Paramètres supplémentaires (cacheControlTtl) pour les modèles `anthropic/*`
- La politique de transcription suit les modèles OpenRouter

## Fichiers à modifier

### Gestion des identifiants de base

#### 1. `src/commands/onboard-auth.credentials.ts`

Ajouter :

```typescript
export const KILOCODE_DEFAULT_MODEL_REF = "kilocode/anthropic/claude-opus-4.6";

export async function setKilocodeApiKey(key: string, agentDir?: string) {
  upsertAuthProfile({
    profileId: "kilocode:default",
    credential: {
      type: "api_key",
      provider: "kilocode",
      key,
    },
    agentDir: resolveAuthAgentDir(agentDir),
  });
}
```

#### 2. `src/agents/model-auth.ts`

Ajouter à `envMap` dans `resolveEnvApiKey()` :

```typescript
const envMap: Record<string, string> = {
  // ... entrées existantes
  kilocode: "KILOCODE_API_KEY",
};
```

#### 3. `src/config/io.ts`

Ajouter à `SHELL_ENV_EXPECTED_KEYS` :

```typescript
const SHELL_ENV_EXPECTED_KEYS = [
  // ... entrées existantes
  "KILOCODE_API_KEY",
];
```

### Application de la configuration

#### 4. `src/commands/onboard-auth.config-core.ts`

Ajouter de nouvelles fonctions :

```typescript
export const KILOCODE_BASE_URL = "https://api.kilo.ai/api/gateway/";

export function applyKilocodeProviderConfig(cfg: OpenClawConfig): OpenClawConfig {
  const models = { ...cfg.agents?.defaults?.models };
  models[KILOCODE_DEFAULT_MODEL_REF] = {
    ...models[KILOCODE_DEFAULT_MODEL_REF],
    alias: models[KILOCODE_DEFAULT_MODEL_REF]?.alias ?? "Kilo Gateway",
  };

  const providers = { ...cfg.models?.providers };
  const existingProvider = providers.kilocode;
  const { apiKey: existingApiKey, ...existingProviderRest } = (existingProvider ?? {}) as Record<
    string,
    unknown
  > as { apiKey?: string };
  const resolvedApiKey = typeof existingApiKey === "string" ? existingApiKey : undefined;
  const normalizedApiKey = resolvedApiKey?.trim();

  providers.kilocode = {
    ...existingProviderRest,
    baseUrl: KILOCODE_BASE_URL,
    api: "openai-completions",
    ...(normalizedApiKey ? { apiKey: normalizedApiKey } : {}),
  };

  return {
    ...cfg,
    agents: {
      ...cfg.agents,
      defaults: {
        ...cfg.agents?.defaults,
        models,
      },
    },
    models: {
      mode: cfg.models?.mode ?? "merge",
      providers,
    },
  };
}

export function applyKilocodeConfig(cfg: OpenClawConfig): OpenClawConfig {
  const next = applyKilocodeProviderConfig(cfg);
  const existingModel = next.agents?.defaults?.model;
  return {
    ...next,
    agents: {
      ...next.agents,
      defaults: {
        ...next.agents?.defaults,
        model: {
          ...(existingModel && "fallbacks" in (existingModel as Record<string, unknown>)
            ? {
                fallbacks: (existingModel as { fallbacks?: string[] }).fallbacks,
              }
            : undefined),
          primary: KILOCODE_DEFAULT_MODEL_REF,
        },
      },
    },
  };
}
```

### Système de choix d'authentification

#### 5. `src/commands/onboard-types.ts`

Ajouter au type `AuthChoice` :

```typescript
export type AuthChoice =
  // ... choix existants
  "kilocode-api-key";
// ...
```

Ajouter à `OnboardOptions` :

```typescript
export type OnboardOptions = {
  // ... options existantes
  kilocodeApiKey?: string;
  // ...
};
```

#### 6. `src/commands/auth-choice-options.ts`

Ajouter à `AuthChoiceGroupId` :

```typescript
export type AuthChoiceGroupId =
  // ... groupes existants
  "kilocode";
// ...
```

Ajouter à `AUTH_CHOICE_GROUP_DEFS` :

```typescript
{
  value: "kilocode",
  label: "Kilo Gateway",
  hint: "Clé API (compatible OpenRouter)",
  choices: ["kilocode-api-key"],
},
```

Ajouter à `buildAuthChoiceOptions()` :

```typescript
options.push({
  value: "kilocode-api-key",
  label: "Clé API Kilo Gateway",
  hint: "Passerelle compatible OpenRouter",
});
```

#### 7. `src/commands/auth-choice.preferred-provider.ts`

Ajouter le mappage :

```typescript
const PREFERRED_PROVIDER_BY_AUTH_CHOICE: Partial<Record<AuthChoice, string>> = {
  // ... mappages existants
  "kilocode-api-key": "kilocode",
};
```

### Application du choix d'authentification

#### 8. `src/commands/auth-choice.apply.api-providers.ts`

Ajouter l'importation :

```typescript
import {
  // ... importations existantes
  applyKilocodeConfig,
  applyKilocodeProviderConfig,
  KILOCODE_DEFAULT_MODEL_REF,
  setKilocodeApiKey,
} from "./onboard-auth.js";
```

Ajouter la gestion pour `kilocode-api-key` :

```typescript
if (authChoice === "kilocode-api-key") {
  const store = ensureAuthProfileStore(params.agentDir, {
    allowKeychainPrompt: false,
  });
  const profileOrder = resolveAuthProfileOrder({
    cfg: nextConfig,
    store,
    provider: "kilocode",
  });
  const existingProfileId = profileOrder.find((profileId) => Boolean(store.profiles[profileId]));
  const existingCred = existingProfileId ? store.profiles[existingProfileId] : undefined;
  let profileId = "kilocode:default";
  let mode: "api_key" | "oauth" | "token" = "api_key";
  let hasCredential = false;

  if (existingProfileId && existingCred?.type) {
    profileId = existingProfileId;
    mode =
      existingCred.type === "oauth" ? "oauth" : existingCred.type === "token" ? "token" : "api_key";
    hasCredential = true;
  }

  if (!hasCredential && params.opts?.token && params.opts?.tokenProvider === "kilocode") {
    await setKilocodeApiKey(normalizeApiKeyInput(params.opts.token), params.agentDir);
    hasCredential = true;
  }

  if (!hasCredential) {
    const envKey = resolveEnvApiKey("kilocode");
    if (envKey) {
      const useExisting = await params.prompter.confirm({
        message: `Utiliser la clé API KILOCODE_API_KEY existante (${envKey.source}, ${formatApiKeyPreview(envKey.apiKey)})?`,
        initialValue: true,
      });
      if (useExisting) {
        await setKilocodeApiKey(envKey.apiKey, params.agentDir);
        hasCredential = true;
      }
    }
  }

  if (!hasCredential) {
    const key = await params.prompter.text({
      message: "Entrez la clé API Kilo Gateway",
      validate: validateApiKeyInput,
    });
    await setKilocodeApiKey(normalizeApiKeyInput(String(key)), params.agentDir);
    hasCredential = true;
  }

  if (hasCredential) {
    nextConfig = applyAuthProfileConfig(nextConfig, {
      profileId,
      provider: "kilocode",
      mode,
    });
  }
  {
    const applied = await applyDefaultModelChoice({
      config: nextConfig,
      setDefaultModel: params.setDefaultModel,
      defaultModel: KILOCODE_DEFAULT_MODEL_REF,
      applyDefaultConfig: applyKilocodeConfig,
      applyProviderConfig: applyKilocodeProviderConfig,
      noteDefault: KILOCODE_DEFAULT_MODEL_REF,
      noteAgentModel,
      prompter: params.prompter,
    });
    nextConfig = applied.config;
    agentModelOverride = applied.agentModelOverride ?? agentModelOverride;
  }
  return { config: nextConfig, agentModelOverride };
}
```

Ajouter également le mappage tokenProvider en haut de la fonction :

```typescript
if (params.opts.tokenProvider === "kilocode") {
  authChoice = "kilocode-api-key";
}
```

### Enregistrement CLI

#### 9. `src/cli/program/register.onboard.ts`

Ajouter l'option CLI :

```typescript
.option("--kilocode-api-key <key>", "Clé API Kilo Gateway")
```

Ajouter au gestionnaire d'action :

```typescript
kilocodeApiKey: opts.kilocodeApiKey as string | undefined,
```

Mettre à jour le texte d'aide du choix d'authentification :

```typescript
.option(
  "--auth-choice <choice>",
  "Auth: setup-token|token|chutes|openai-codex|openai-api-key|openrouter-api-key|kilocode-api-key|ai-gateway-api-key|...",
)
```

### Intégration non-interactive

#### 10. `src/commands/onboard-non-interactive/local/auth-choice.ts`

Ajouter la gestion pour `kilocode-api-key` :

```typescript
if (authChoice === "kilocode-api-key") {
  const resolved = await resolveNonInteractiveApiKey({
    provider: "kilocode",
    cfg: baseConfig,
    flagValue: opts.kilocodeApiKey,
    flagName: "--kilocode-api-key",
    envVar: "KILOCODE_API_KEY",
  });
  await setKilocodeApiKey(resolved.apiKey, agentDir);
  nextConfig = applyAuthProfileConfig(nextConfig, {
    profileId: "kilocode:default",
    provider: "kilocode",
    mode: "api_key",
  });
  // ... appliquer le modèle par défaut
}
```

### Mises à jour des exportations

#### 11. `src/commands/onboard-auth.ts`

Ajouter les exportations :

```typescript
export {
  // ... exportations existantes
  applyKilocodeConfig,
  applyKilocodeProviderConfig,
  KILOCODE_BASE_URL,
} from "./onboard-auth.config-core.js";

export {
  // ... exportations existantes
  KILOCODE_DEFAULT_MODEL_REF,
  setKilocodeApiKey,
} from "./onboard-auth.credentials.js";
```

### Gestion spéciale (Optionnel)

#### 12. `src/agents/pi-embedded-runner/cache-ttl.ts`

Ajouter le support de Kilo Gateway pour les modèles Anthropic :

```typescript
export function isCacheTtlEligibleProvider(provider: string, modelId: string): boolean {
  const normalizedProvider = provider.toLowerCase();
  const normalizedModelId = modelId.toLowerCase();
  if (normalizedProvider === "anthropic") return true;
  if (normalizedProvider === "openrouter" && normalizedModelId.startsWith("anthropic/"))
    return true;
  if (normalizedProvider === "kilocode" && normalizedModelId.startsWith("anthropic/")) return true;
  return false;
}
```

#### 13. `src/agents/transcript-policy.ts`

Ajouter la gestion de Kilo Gateway (similaire à OpenRouter) :

```typescript
const isKilocodeGemini = provider === "kilocode" && modelId.toLowerCase().includes("gemini");

// Inclure dans la vérification needsNonImageSanitize
const needsNonImageSanitize =
  isGoogle || isAnthropic || isMistral || isOpenRouterGemini || isKilocodeGemini;
```

## Structure de configuration

### Exemple de configuration utilisateur

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "kilocode": {
        "baseUrl": "https://api.kilo.ai/api/gateway/",
        "apiKey": "xxxxx",
        "api": "openai-completions",
        "models": [
          {
            "id": "anthropic/claude-opus-4.6",
            "name": "Anthropic: Claude Opus 4.6"
          },
          { "id": "minimax/minimax-m2.5:free", "name": "Minimax: Minimax M2.5" }
        ]
      }
    }
  }
}
```

### Structure du profil d'authentification

```json
{
  "profiles": {
    "kilocode:default": {
      "type": "api_key",
      "provider": "kilocode",
      "key": "xxxxx"
    }
  }
}
```

## Considérations de Test

1. **Tests Unitaires :**
   - Tester que `setKilocodeApiKey()` écrit le profil correct
   - Tester que `applyKilocodeConfig()` définit les valeurs par défaut correctes
   - Tester que `resolveEnvApiKey("kilocode")` retourne la variable d'environnement correcte

2. **Tests d'Intégration :**
   - Tester le flux d'intégration avec `--auth-choice kilocode-api-key`
   - Tester l'intégration non-interactive avec `--kilocode-api-key`
   - Tester la sélection de modèle avec le préfixe `kilocode/`

3. **Tests E2E :**
   - Tester les appels API réels via Kilo Gateway (tests en direct)

## Notes de Migration

- Aucune migration nécessaire pour les utilisateurs existants
- Les nouveaux utilisateurs peuvent immédiatement utiliser le choix d'authentification `kilocode-api-key`
- La configuration manuelle existante avec le fournisseur `kilocode` continuera de fonctionner

## Considérations Futures

1. **Catalogue de Modèles :** Si Kilo Gateway expose un endpoint `/models`, ajouter le support de scan similaire à `scanOpenRouterModels()`

2. **Support OAuth :** Si Kilo Gateway ajoute OAuth, étendre le système d'authentification en conséquence

3. **Limitation de Débit :** Envisager d'ajouter une gestion de limite de débit spécifique à Kilo Gateway si nécessaire

4. **Documentation :** Ajouter la documentation à `docs/providers/kilocode.md` expliquant la configuration et l'utilisation

## Résumé des Modifications

| Fichier                                                     | Type de Modification | Description                                                             |
| ----------------------------------------------------------- | -------------------- | ----------------------------------------------------------------------- |
| `src/commands/onboard-auth.credentials.ts`                  | Ajouter              | `KILOCODE_DEFAULT_MODEL_REF`, `setKilocodeApiKey()`                     |
| `src/agents/model-auth.ts`                                  | Modifier             | Ajouter `kilocode` à `envMap`                                           |
| `src/config/io.ts`                                          | Modifier             | Ajouter `KILOCODE_API_KEY` aux clés d'environnement shell               |
| `src/commands/onboard-auth.config-core.ts`                  | Ajouter              | `applyKilocodeProviderConfig()`, `applyKilocodeConfig()`                |
| `src/commands/onboard-types.ts`                             | Modifier             | Ajouter `kilocode-api-key` à `AuthChoice`, ajouter `kilocodeApiKey` aux options |
| `src/commands/auth-choice-options.ts`                       | Modifier             | Ajouter le groupe `kilocode` et l'option                                |
| `src/commands/auth-choice.preferred-provider.ts`            | Modifier             | Ajouter le mappage `kilocode-api-key`                                   |
| `src/commands/auth-choice.apply.api-providers.ts`           | Modifier             | Ajouter la gestion `kilocode-api-key`                                   |
| `src/cli/program/register.onboard.ts`                       | Modifier             | Ajouter l'option `--kilocode-api-key`                                   |
| `src/commands/onboard-non-interactive/local/auth-choice.ts` | Modifier             | Ajouter la gestion non-interactive                                      |
| `src/commands/onboard-auth.ts`                              | Modifier             | Exporter les nouvelles fonctions                                        |
| `src/agents/pi-embedded-runner/cache-ttl.ts`                | Modifier             | Ajouter le support kilocode                                             |
| `src/agents/transcript-policy.ts`                           | Modifier             | Ajouter la gestion Gemini kilocode                                      |
