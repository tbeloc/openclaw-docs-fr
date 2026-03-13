---
title: "Architecture d'intégration Pi"
summary: "Architecture de l'intégration de l'agent Pi embarqué d'OpenClaw et cycle de vie de la session"
read_when:
  - Comprendre la conception de l'intégration du SDK Pi dans OpenClaw
  - Modifier le cycle de vie de la session d'agent, les outils ou le câblage des fournisseurs pour Pi
---

# Architecture d'intégration Pi

Ce document décrit comment OpenClaw s'intègre avec [pi-coding-agent](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent) et ses packages associés (`pi-ai`, `pi-agent-core`, `pi-tui`) pour alimenter ses capacités d'agent IA.

## Aperçu

OpenClaw utilise le SDK pi pour intégrer un agent de codage IA dans son architecture de passerelle de messagerie. Au lieu de générer pi en tant que sous-processus ou d'utiliser le mode RPC, OpenClaw importe directement et instancie `AgentSession` de pi via `createAgentSession()`. Cette approche embarquée offre :

- Contrôle total sur le cycle de vie de la session et la gestion des événements
- Injection d'outils personnalisés (messagerie, sandbox, actions spécifiques au canal)
- Personnalisation du message système par canal/contexte
- Persistance de session avec support de branchement/compaction
- Rotation de profil d'authentification multi-compte avec basculement
- Commutation de modèle indépendante du fournisseur

## Dépendances de paquets

```json
{
  "@mariozechner/pi-agent-core": "0.49.3",
  "@mariozechner/pi-ai": "0.49.3",
  "@mariozechner/pi-coding-agent": "0.49.3",
  "@mariozechner/pi-tui": "0.49.3"
}
```

| Paquet            | Objectif                                                                                           |
| ----------------- | -------------------------------------------------------------------------------------------------- |
| `pi-ai`           | Abstractions LLM principales : `Model`, `streamSimple`, types de messages, APIs de fournisseur    |
| `pi-agent-core`   | Boucle d'agent, exécution d'outils, types `AgentMessage`                                          |
| `pi-coding-agent` | SDK haut niveau : `createAgentSession`, `SessionManager`, `AuthStorage`, `ModelRegistry`, outils intégrés |
| `pi-tui`          | Composants d'interface utilisateur terminal (utilisés en mode TUI local d'OpenClaw)               |

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
│   ├── lanes.ts                   # Voies de commande session/globale
│   ├── logger.ts                  # Enregistreur de sous-système
│   ├── model.ts                   # Résolution de modèle via ModelRegistry
│   ├── runs.ts                    # Suivi des exécutions actives, abandon, file d'attente
│   ├── sandbox-info.ts            # Informations sandbox pour le message système
│   ├── session-manager-cache.ts   # Mise en cache de l'instance SessionManager
│   ├── session-manager-init.ts    # Initialisation du fichier de session
│   ├── system-prompt.ts           # Constructeur de message système
│   ├── tool-split.ts              # Diviser les outils en builtIn vs personnalisé
│   ├── types.ts                   # EmbeddedPiAgentMeta, EmbeddedPiRunResult
│   └── utils.ts                   # Mappage ThinkLevel, description d'erreur
├── pi-embedded-subscribe.ts       # Abonnement aux événements de session/dispatch
├── pi-embedded-subscribe.types.ts # SubscribeEmbeddedPiSessionParams
├── pi-embedded-subscribe.handlers.ts # Fabrique de gestionnaire d'événements
├── pi-embedded-subscribe.handlers.lifecycle.ts
├── pi-embedded-subscribe.handlers.types.ts
├── pi-embedded-block-chunker.ts   # Chunking de bloc de réponse en flux
├── pi-embedded-messaging.ts       # Suivi des envois d'outil de messagerie
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
│   ├── context-pruning.ts         # Extension d'élagage de contexte basée sur cache-TTL
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

### 4. Invite

Après la configuration, la session est invitée :

```typescript
await session.prompt(effectivePrompt, { images: imageResult.images });
```

Le SDK gère la boucle d'agent complète : envoi au LLM, exécution des appels d'outils, réponses en flux.

L'injection d'image est locale à l'invite : OpenClaw charge les références d'image de l'invite actuelle et
les transmet via `images` pour ce tour uniquement. Il ne réanalyse pas les tours d'historique plus anciens
pour réinjecter les charges utiles d'image.

## Architecture des outils

### Pipeline d'outils

1. **Outils de base** : `codingTools` de pi (lecture, bash, édition, écriture)
2. **Remplacements personnalisés** : OpenClaw remplace bash par `exec`/`process`, personnalise la lecture/édition/écriture pour sandbox
3. **Outils OpenClaw** : messagerie, navigateur, canvas, sessions, cron, passerelle, etc.
4. **Outils de canal** : Outils d'action spécifiques à Discord/Telegram/Slack/WhatsApp
5. **Filtrage de politique** : Outils filtrés par profil, fournisseur, agent, groupe, politiques sandbox
6. **Normalisation du schéma** : Schémas nettoyés pour les bizarreries Gemini/OpenAI
7. **Enveloppe AbortSignal** : Outils enveloppés pour respecter les signaux d'abandon

### Adaptateur de définition d'outil

`AgentTool` de pi-agent-core a une signature `execute` différente de `ToolDefinition` de pi-coding-agent. L'adaptateur dans `pi-tool-definition-adapter.ts` comble cette lacune :

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

Cela garantit que le filtrage de politique d'OpenClaw, l'intégration sandbox et l'ensemble d'outils étendu restent coh
