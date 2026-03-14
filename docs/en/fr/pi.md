---
title: "Architecture d'intégration Pi"
summary: "Architecture de l'intégration de l'agent Pi embarqué d'OpenClaw et cycle de vie de la session"
read_when:
  - Comprendre la conception de l'intégration du SDK Pi dans OpenClaw
  - Modifier le cycle de vie de la session de l'agent, les outils ou le câblage des fournisseurs pour Pi
---

# Architecture d'intégration Pi

Ce document décrit comment OpenClaw s'intègre avec [pi-coding-agent](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent) et ses packages associés (`pi-ai`, `pi-agent-core`, `pi-tui`) pour alimenter ses capacités d'agent IA.

## Aperçu

OpenClaw utilise le SDK pi pour intégrer un agent de codage IA dans son architecture de passerelle de messagerie. Au lieu de générer pi en tant que sous-processus ou d'utiliser le mode RPC, OpenClaw importe directement et instancie `AgentSession` de pi via `createAgentSession()`. Cette approche embarquée offre :

- Contrôle total sur le cycle de vie de la session et la gestion des événements
- Injection d'outils personnalisés (messagerie, sandbox, actions spécifiques aux canaux)
- Personnalisation du message système par canal/contexte
- Persistance de session avec support de branchement/compaction
- Rotation de profil d'authentification multi-compte avec basculement
- Commutation de modèle indépendante du fournisseur

## Dépendances des packages

```json
{
  "@mariozechner/pi-agent-core": "0.49.3",
  "@mariozechner/pi-ai": "0.49.3",
  "@mariozechner/pi-coding-agent": "0.49.3",
  "@mariozechner/pi-tui": "0.49.3"
}
```

| Package           | Objectif                                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------------------ |
| `pi-ai`           | Abstractions LLM principales : `Model`, `streamSimple`, types de messages, APIs de fournisseur                           |
| `pi-agent-core`   | Boucle d'agent, exécution d'outils, types `AgentMessage`                                                       |
| `pi-coding-agent` | SDK de haut niveau : `createAgentSession`, `SessionManager`, `AuthStorage`, `ModelRegistry`, outils intégrés |
| `pi-tui`          | Composants d'interface utilisateur terminal (utilisés en mode TUI local d'OpenClaw)                                             |

## Structure des fichiers

```
src/agents/
├── pi-embedded-runner.ts          # Réexporte depuis pi-embedded-runner/
├── pi-embedded-runner/
│   ├── run.ts                     # Point d'entrée principal : runEmbeddedPiAgent()
│   ├── run/
│   │   ├── attempt.ts             # Logique d'une seule tentative avec configuration de session
│   │   ├── params.ts              # Type RunEmbeddedPiAgentParams
│   │   ├── payloads.ts            # Construire les charges utiles de réponse à partir des résultats d'exécution
│   │   ├── images.ts              # Injection d'image de modèle de vision
│   │   └── types.ts               # EmbeddedRunAttemptResult
│   ├── abort.ts                   # Détection d'erreur d'abandon
│   ├── cache-ttl.ts               # Suivi TTL du cache pour l'élagage du contexte
│   ├── compact.ts                 # Logique de compaction manuelle/automatique
│   ├── extensions.ts              # Charger les extensions pi pour les exécutions embarquées
│   ├── extra-params.ts            # Paramètres de flux spécifiques au fournisseur
│   ├── google.ts                  # Corrections d'ordre de tour Google/Gemini
│   ├── history.ts                 # Limitation de l'historique (DM vs groupe)
│   ├── lanes.ts                   # Voies de commande de session/globales
│   ├── logger.ts                  # Enregistreur de sous-système
│   ├── model.ts                   # Résolution de modèle via ModelRegistry
│   ├── runs.ts                    # Suivi des exécutions actives, abandon, file d'attente
│   ├── sandbox-info.ts            # Informations sandbox pour le message système
│   ├── session-manager-cache.ts   # Mise en cache de l'instance SessionManager
│   ├── session-manager-init.ts    # Initialisation du fichier de session
│   ├── system-prompt.ts           # Générateur de message système
│   ├── tool-split.ts              # Diviser les outils en builtIn vs personnalisés
│   ├── types.ts                   # EmbeddedPiAgentMeta, EmbeddedPiRunResult
│   └── utils.ts                   # Mappage ThinkLevel, description d'erreur
├── pi-embedded-subscribe.ts       # Abonnement aux événements de session/dispatch
├── pi-embedded-subscribe.types.ts # SubscribeEmbeddedPiSessionParams
├── pi-embedded-subscribe.handlers.ts # Fabrique de gestionnaire d'événements
├── pi-embedded-subscribe.handlers.lifecycle.ts
├── pi-embedded-subscribe.handlers.types.ts
├── pi-embedded-block-chunker.ts   # Chunking de bloc de réponse en flux
├── pi-embedded-messaging.ts       # Suivi des envois d'outils de messagerie
├── pi-embedded-helpers.ts         # Classification d'erreur, validation de tour
├── pi-embedded-helpers/           # Modules d'aide
├── pi-embedded-utils.ts           # Utilitaires de formatage
├── pi-tools.ts                    # createOpenClawCodingTools()
├── pi-tools.abort.ts              # Enveloppe AbortSignal pour les outils
├── pi-tools.policy.ts             # Politique de liste blanche/noire d'outils
├── pi-tools.read.ts               # Personnalisations d'outil de lecture
├── pi-tools.schema.ts             # Normalisation du schéma d'outil
├── pi-tools.types.ts              # Alias de type AnyAgentTool
├── pi-tool-definition-adapter.ts  # Adaptateur AgentTool -> ToolDefinition
├── pi-settings.ts                 # Remplacements de paramètres
├── pi-extensions/                 # Extensions pi personnalisées
│   ├── compaction-safeguard.ts    # Extension de sauvegarde
│   ├── compaction-safeguard-runtime.ts
│   ├── context-pruning.ts         # Extension d'élagage de contexte Cache-TTL
│   └── context-pruning/
├── model-auth.ts                  # Résolution du profil d'authentification
├── auth-profiles.ts               # Magasin de profils, refroidissement, basculement
├── model-selection.ts             # Résolution du modèle par défaut
├── models-config.ts               # Génération models.json
├── model-catalog.ts               # Cache du catalogue de modèles
├── context-window-guard.ts        # Validation de la fenêtre de contexte
├── failover-error.ts              # Classe FailoverError
├── defaults.ts                    # DEFAULT_PROVIDER, DEFAULT_MODEL
├── system-prompt.ts               # buildAgentSystemPrompt()
├── system-prompt-params.ts        # Résolution des paramètres du message système
├── system-prompt-report.ts        # Génération de rapport de débogage
├── tool-summaries.ts              # Résumés de description d'outil
├── tool-policy.ts                 # Résolution de la politique d'outil
├── transcript-policy.ts           # Politique de validation de transcription
├── skills.ts                      # Construction de snapshot/prompt de compétence
├── skills/                        # Sous-système de compétences
├── sandbox.ts                     # Résolution du contexte sandbox
├── sandbox/                       # Sous-système sandbox
├── channel-tools.ts               # Injection d'outil spécifique au canal
├── openclaw-tools.ts              # Outils spécifiques à OpenClaw
├── bash-tools.ts                  # Outils exec/process
├── apply-patch.ts                 # Outil apply_patch (OpenAI)
├── tools/                         # Implémentations d'outils individuels
│   ├── browser-tool.ts
│   ├── canvas-tool.ts
│   ├── cron-tool.ts
│   ├── discord-actions*.ts
│   ├── gateway-tool.ts
│   ├── image-tool.ts
│   ├── message-tool.ts
│   ├── nodes-tool.ts
│   ├── session*.ts
│   ├── slack-actions.ts
│   ├── telegram-actions.ts
│   ├── web-*.ts
│   └── whatsapp-actions.ts
└── ...
```

## Flux d'intégration principal

### 1. Exécution d'un agent embarqué

Le point d'entrée principal est `runEmbeddedPiAgent()` dans `pi-embedded-runner/run.ts` :

```typescript
import { runEmbeddedPiAgent } from "./agents/pi-embedded-runner.js";

const result = await runEmbeddedPiAgent({
  sessionId: "user-123",
  sessionKey: "main:whatsapp:+1234567890",
  sessionFile: "/path/to/session.jsonl",
  workspaceDir: "/path/to/workspace",
  config: openclawConfig,
  prompt: "Hello, how are you?",
  provider: "anthropic",
  model: "claude-sonnet-4-20250514",
  timeoutMs: 120_000,
  runId: "run-abc",
  onBlockReply: async (payload) => {
    await sendToChannel(payload.text, payload.mediaUrls);
  },
});
```

### 2. Création de session

À l'intérieur de `runEmbeddedAttempt()` (appelé par `runEmbeddedPiAgent()`), le SDK pi est utilisé :

```typescript
import {
  createAgentSession,
  DefaultResourceLoader,
  SessionManager,
  SettingsManager,
} from "@mariozechner/pi-coding-agent";

const resourceLoader = new DefaultResourceLoader({
  cwd: resolvedWorkspace,
  agentDir,
  settingsManager,
  additionalExtensionPaths,
});
await resourceLoader.reload();

const { session } = await createAgentSession({
  cwd: resolvedWorkspace,
  agentDir,
  authStorage: params.authStorage,
  modelRegistry: params.modelRegistry,
  model: params.model,
  thinkingLevel: mapThinkingLevel(params.thinkLevel),
  tools: builtInTools,
  customTools: allCustomTools,
  sessionManager,
  settingsManager,
  resourceLoader,
});

applySystemPromptOverrideToSession(session, systemPromptOverride);
```

### 3. Abonnement aux événements

`subscribeEmbeddedPiSession()` s'abonne aux événements `AgentSession` de pi :

```typescript
const subscription = subscribeEmbeddedPiSession({
  session: activeSession,
  runId: params.runId,
  verboseLevel: params.verboseLevel,
  reasoningMode: params.reasoningLevel,
  toolResultFormat: params.toolResultFormat,
  onToolResult: params.onToolResult,
  onReasoningStream: params.onReasoningStream,
  onBlockReply: params.onBlockReply,
  onPartialReply: params.onPartialReply,
  onAgentEvent: params.onAgentEvent,
});
```

Les événements gérés incluent :

- `message_start` / `message_end` / `message_update` (texte/réflexion en flux)
- `tool_execution_start` / `tool_execution_update` / `tool_execution_end`
- `turn_start` / `turn_end`
- `agent_start` / `agent_end`
- `auto_compaction_start` / `auto_compaction_end`

### 4. Invitation

Après la configuration, la session est invitée :

```typescript
await session.prompt(effectivePrompt, { images: imageResult.images });
```

Le SDK gère la boucle complète de l'agent : envoi au LLM, exécution des appels d'outils, réponses en flux.

L'injection d'image est locale à l'invitation : OpenClaw charge les références d'image de l'invitation actuelle et
les transmet via `images` pour ce tour uniquement. Il ne réanalyse pas les tours d'historique plus anciens
pour réinjecter les charges utiles d'image.

## Architecture des outils

### Pipeline d'outils

1. **Outils de base** : `codingTools` de pi (read, bash, edit, write)
2. **Remplacements personnalisés** : OpenClaw remplace bash par `exec`/`process`, personnalise read/edit/write pour sandbox
3. **Outils OpenClaw** : messagerie, navigateur, canvas, sessions, cron, passerelle, etc.
4. **Outils de canal** : Outils d'action spécifiques à Discord/Telegram/Slack/WhatsApp
5. **Filtrage de politique** : Outils filtrés par profil, fournisseur, agent, groupe, politiques sandbox
6. **Normalisation du schéma** : Schémas nettoyés pour les particularités de Gemini/OpenAI
7. **Enveloppe AbortSignal** : Outils enveloppés pour respecter les signaux d'abandon

### Adaptateur de définition d'outil

`AgentTool` de pi-agent-core a une signature `execute` différente de `ToolDefinition` de pi-coding-agent. L'adaptateur dans `pi-tool-definition-adapter.ts` fait le pont :

```typescript
export function toToolDefinitions(tools: AnyAgentTool[]): ToolDefinition[] {
  return tools.map((tool) => ({
    name: tool.name,
    label: tool.label ?? name,
    description: tool.description ?? "",
    parameters: tool.parameters,
    execute: async (toolCallId, params, onUpdate, _ctx, signal) => {
      // La signature pi-coding-agent diffère de pi-agent-core
      return await tool.execute(toolCallId, params, signal, onUpdate);
    },
  }));
}
```

### Stratégie de division d'outils

`splitSdkTools()` transmet tous les outils via `customTools` :

```typescript
export function splitSdkTools(options: { tools: AnyAgentTool[]; sandboxEnabled: boolean }) {
  return {
    builtInTools: [], // Vide. Nous remplaçons tout
    customTools: toToolDefinitions(options.tools),
  };
}
```

Cela garantit que le filtrage de politique d'OpenClaw, l'intégration sandbox et l'ensemble d'outils étendu restent cohérents entre les fournisseurs.

## Construction du Prompt Système

Le prompt système est construit dans `buildAgentSystemPrompt()` (`system-prompt.ts`). Il assemble un prompt complet avec des sections incluant Tooling, Tool Call Style, Safety guardrails, OpenClaw CLI reference, Skills, Docs, Workspace, Sandbox, Messaging, Reply Tags, Voice, Silent Replies, Heartbeats, Runtime metadata, plus Memory et Reactions quand activés, et contenu optionnel de fichiers de contexte et prompt système supplémentaire. Les sections sont réduites pour le mode prompt minimal utilisé par les subagents.

Le prompt est appliqué après la création de session via `applySystemPromptOverrideToSession()`:

```typescript
const systemPromptOverride = createSystemPromptOverride(appendPrompt);
applySystemPromptOverrideToSession(session, systemPromptOverride);
```

## Gestion des Sessions

### Fichiers de Session

Les sessions sont des fichiers JSONL avec structure arborescente (liaison id/parentId). Le `SessionManager` de Pi gère la persistance:

```typescript
const sessionManager = SessionManager.open(params.sessionFile);
```

OpenClaw l'enveloppe avec `guardSessionManager()` pour la sécurité des résultats d'outils.

### Mise en Cache des Sessions

`session-manager-cache.ts` met en cache les instances de SessionManager pour éviter l'analyse répétée de fichiers:

```typescript
await prewarmSessionFile(params.sessionFile);
sessionManager = SessionManager.open(params.sessionFile);
trackSessionManagerAccess(params.sessionFile);
```

### Limitation de l'Historique

`limitHistoryTurns()` réduit l'historique de conversation en fonction du type de canal (DM vs groupe).

### Compaction

La compaction automatique se déclenche au débordement de contexte. `compactEmbeddedPiSessionDirect()` gère la compaction manuelle:

```typescript
const compactResult = await compactEmbeddedPiSessionDirect({
  sessionId, sessionFile, provider, model, ...
});
```

## Authentification et Résolution de Modèle

### Profils d'Authentification

OpenClaw maintient un magasin de profils d'authentification avec plusieurs clés API par fournisseur:

```typescript
const authStore = ensureAuthProfileStore(agentDir, { allowKeychainPrompt: false });
const profileOrder = resolveAuthProfileOrder({ cfg, store: authStore, provider, preferredProfile });
```

Les profils tournent en cas d'échec avec suivi du délai d'attente:

```typescript
await markAuthProfileFailure({ store, profileId, reason, cfg, agentDir });
const rotated = await advanceAuthProfile();
```

### Résolution de Modèle

```typescript
import { resolveModel } from "./pi-embedded-runner/model.js";

const { model, error, authStorage, modelRegistry } = resolveModel(
  provider,
  modelId,
  agentDir,
  config,
);

// Utilise le ModelRegistry et AuthStorage de pi
authStorage.setRuntimeApiKey(model.provider, apiKeyInfo.apiKey);
```

### Basculement

`FailoverError` déclenche le basculement de modèle quand configuré:

```typescript
if (fallbackConfigured && isFailoverErrorMessage(errorText)) {
  throw new FailoverError(errorText, {
    reason: promptFailoverReason ?? "unknown",
    provider,
    model: modelId,
    profileId,
    status: resolveFailoverStatus(promptFailoverReason),
  });
}
```

## Extensions Pi

OpenClaw charge des extensions pi personnalisées pour un comportement spécialisé:

### Sauvegarde de Compaction

`src/agents/pi-extensions/compaction-safeguard.ts` ajoute des garde-fous à la compaction, incluant la budgétisation adaptative des tokens plus les résumés d'échecs d'outils et d'opérations de fichiers:

```typescript
if (resolveCompactionMode(params.cfg) === "safeguard") {
  setCompactionSafeguardRuntime(params.sessionManager, { maxHistoryShare });
  paths.push(resolvePiExtensionPath("compaction-safeguard"));
}
```

### Élagage de Contexte

`src/agents/pi-extensions/context-pruning.ts` implémente l'élagage de contexte basé sur le cache-TTL:

```typescript
if (cfg?.agents?.defaults?.contextPruning?.mode === "cache-ttl") {
  setContextPruningRuntime(params.sessionManager, {
    settings,
    contextWindowTokens,
    isToolPrunable,
    lastCacheTouchAt,
  });
  paths.push(resolvePiExtensionPath("context-pruning"));
}
```

## Streaming et Réponses en Bloc

### Chunking de Bloc

`EmbeddedBlockChunker` gère le streaming de texte en blocs de réponse discrets:

```typescript
const blockChunker = blockChunking ? new EmbeddedBlockChunker(blockChunking) : null;
```

### Suppression des Balises Thinking/Final

La sortie en streaming est traitée pour supprimer les blocs `<think>`/`<thinking>` et extraire le contenu `<final>`:

```typescript
const stripBlockTags = (text: string, state: { thinking: boolean; final: boolean }) => {
  // Supprime le contenu <think>...</think>
  // Si enforceFinalTag, retourne uniquement le contenu <final>...</final>
};
```

### Directives de Réponse

Les directives de réponse comme `[[media:url]]`, `[[voice]]`, `[[reply:id]]` sont analysées et extraites:

```typescript
const { text: cleanedText, mediaUrls, audioAsVoice, replyToId } = consumeReplyDirectives(chunk);
```

## Gestion des Erreurs

### Classification des Erreurs

`pi-embedded-helpers.ts` classe les erreurs pour un traitement approprié:

```typescript
isContextOverflowError(errorText)     // Contexte trop volumineux
isCompactionFailureError(errorText)   // Échec de compaction
isAuthAssistantError(lastAssistant)   // Échec d'authentification
isRateLimitAssistantError(...)        // Limité en débit
isFailoverAssistantError(...)         // Doit basculer
classifyFailoverReason(errorText)     // "auth" | "rate_limit" | "quota" | "timeout" | ...
```

### Fallback du Niveau de Thinking

Si un niveau de thinking n'est pas supporté, il bascule:

```typescript
const fallbackThinking = pickFallbackThinkingLevel({
  message: errorText,
  attempted: attemptedThinking,
});
if (fallbackThinking) {
  thinkLevel = fallbackThinking;
  continue;
}
```

## Intégration Sandbox

Quand le mode sandbox est activé, les outils et chemins sont contraints:

```typescript
const sandbox = await resolveSandboxContext({
  config: params.config,
  sessionKey: sandboxSessionKey,
  workspaceDir: resolvedWorkspace,
});

if (sandboxRoot) {
  // Utilise les outils read/edit/write en sandbox
  // Exec s'exécute dans un conteneur
  // Browser utilise l'URL du pont
}
```

## Gestion Spécifique aux Fournisseurs

### Anthropic

- Suppression de la chaîne magique de refus
- Validation des tours pour les rôles consécutifs
- Compatibilité des paramètres Claude Code

### Google/Gemini

- Corrections de l'ordre des tours (`applyGoogleTurnOrderingFix`)
- Sanitisation du schéma d'outils (`sanitizeToolsForGoogle`)
- Sanitisation de l'historique de session (`sanitizeSessionHistory`)

### OpenAI

- Outil `apply_patch` pour les modèles Codex
- Gestion de la rétrogradation du niveau de thinking

## Intégration TUI

OpenClaw a également un mode TUI local qui utilise directement les composants pi-tui:

```typescript
// src/tui/tui.ts
import { ... } from "@mariozechner/pi-tui";
```

Cela fournit l'expérience interactive du terminal similaire au mode natif de pi.

## Différences Clés avec Pi CLI

| Aspect          | Pi CLI                  | OpenClaw Embedded                                                                              |
| --------------- | ----------------------- | ---------------------------------------------------------------------------------------------- |
| Invocation      | Commande `pi` / RPC     | SDK via `createAgentSession()`                                                                 |
| Outils          | Outils de codage par défaut | Suite d'outils OpenClaw personnalisée                                                          |
| Prompt système  | AGENTS.md + prompts     | Dynamique par canal/contexte                                                                   |
| Stockage de session | `~/.pi/agent/sessions/` | `~/.openclaw/agents/<agentId>/sessions/` (ou `$OPENCLAW_STATE_DIR/agents/<agentId>/sessions/`) |
| Authentification | Identifiant unique      | Multi-profil avec rotation                                                                     |
| Extensions      | Chargées depuis le disque | Programmatique + chemins disque                                                                |
| Gestion d'événements | Rendu TUI           | Basée sur les callbacks (onBlockReply, etc.)                                                   |

## Considérations Futures

Domaines pour une refonte potentielle:

1. **Alignement de signature d'outils**: Adaptation actuelle entre les signatures pi-agent-core et pi-coding-agent
2. **Enveloppe du gestionnaire de session**: `guardSessionManager` ajoute la sécurité mais augmente la complexité
3. **Chargement d'extensions**: Pourrait utiliser plus directement le `ResourceLoader` de pi
4. **Complexité du gestionnaire de streaming**: `subscribeEmbeddedPiSession` a grandi
5. **Quirks des fournisseurs**: Nombreux chemins de code spécifiques aux fournisseurs que pi pourrait potentiellement gérer

## Tests

La couverture d'intégration Pi s'étend sur ces suites:

- `src/agents/pi-*.test.ts`
- `src/agents/pi-auth-json.test.ts`
- `src/agents/pi-embedded-*.test.ts`
- `src/agents/pi-embedded-helpers*.test.ts`
- `src/agents/pi-embedded-runner*.test.ts`
- `src/agents/pi-embedded-runner/**/*.test.ts`
- `src/agents/pi-embedded-subscribe*.test.ts`
- `src/agents/pi-tools*.test.ts`
- `src/agents/pi-tool-definition-adapter*.test.ts`
- `src/agents/pi-settings.test.ts`
- `src/agents/pi-extensions/**/*.test.ts`

Live/opt-in:

- `src/agents/pi-embedded-runner-extraparams.live.test.ts` (activez `OPENCLAW_LIVE_TEST=1`)

Pour les commandes d'exécution actuelles, voir [Pi Development Workflow](/pi-dev).
