---
read_when:
  - 定义或重构插件架构
  - 将渠道连接器迁移到插件 SDK/运行时
summary: 计划：为所有消息连接器提供一套统一的插件 SDK + 运行时
title: 插件 SDK 重构
x-i18n:
  generated_at: "2026-02-01T21:36:45Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: d1964e2e47a19ee1d42ddaaa9cf1293c80bb0be463b049dc8468962f35bb6cb0
  source_path: refactor/plugin-sdk.md
  workflow: 15
---

# Plan de refactorisation du SDK + Runtime des plugins

Objectif : chaque connecteur de message est un plugin (intégré ou externe), utilisant une API unifiée et stable.
Les plugins n'importent rien directement de `src/**`. Toutes les dépendances sont obtenues via le SDK ou le runtime.

## Pourquoi maintenant

- Les connecteurs actuels mélangent plusieurs modèles : importations directes de modules principaux, approches de pontage dist uniquement et fonctions d'aide personnalisées.
- Cela rend les mises à niveau fragiles et entrave une interface de plugin externe propre.

## Architecture cible (deux couches)

### 1) SDK des plugins (compile-time, stable, publiable)

Portée : types, fonctions d'aide et outils de configuration. Pas d'état runtime, pas d'effets secondaires.

Contenu (exemples) :

- Types : `ChannelPlugin`, adaptateurs, `ChannelMeta`, `ChannelCapabilities`, `ChannelDirectoryEntry`.
- Fonctions d'aide de configuration : `buildChannelConfigSchema`, `setAccountEnabledInConfigSection`, `deleteAccountFromConfigSection`,
  `applyAccountNameToChannelSection`.
- Fonctions d'aide d'appairage : `PAIRING_APPROVED_MESSAGE`, `formatPairingApproveHint`.
- Fonctions d'aide d'onboarding : `promptChannelAccessConfig`, `addWildcardAllowFrom`, types d'onboarding.
- Fonctions d'aide de paramètres d'outils : `createActionGate`, `readStringParam`, `readNumberParam`, `readReactionParams`, `jsonResult`.
- Fonctions d'aide de liens de documentation : `formatDocsLink`.

Livraison :

- Publié en tant que `openclaw/plugin-sdk` (ou exporté du noyau en tant que `openclaw/plugin-sdk`).
- Utilise le versioning sémantique avec des garanties de stabilité claires.

### 2) Runtime des plugins (couche d'exécution, injection)

Portée : tout ce qui implique le comportement runtime du noyau.
Accessible via `OpenClawPluginApi.runtime`, garantissant que les plugins n'importent jamais `src/**`.

Interface recommandée (minimale mais complète) :

```ts
export type PluginRuntime = {
  channel: {
    text: {
      chunkMarkdownText(text: string, limit: number): string[];
      resolveTextChunkLimit(cfg: OpenClawConfig, channel: string, accountId?: string): number;
      hasControlCommand(text: string, cfg: OpenClawConfig): boolean;
    };
    reply: {
      dispatchReplyWithBufferedBlockDispatcher(params: {
        ctx: unknown;
        cfg: unknown;
        dispatcherOptions: {
          deliver: (payload: {
            text?: string;
            mediaUrls?: string[];
            mediaUrl?: string;
          }) => void | Promise<void>;
          onError?: (err: unknown, info: { kind: string }) => void;
        };
      }): Promise<void>;
      createReplyDispatcherWithTyping?: unknown; // adapter for Teams-style flows
    };
    routing: {
      resolveAgentRoute(params: {
        cfg: unknown;
        channel: string;
        accountId: string;
        peer: { kind: RoutePeerKind; id: string };
      }): { sessionKey: string; accountId: string };
    };
    pairing: {
      buildPairingReply(params: { channel: string; idLine: string; code: string }): string;
      readAllowFromStore(channel: string): Promise<string[]>;
      upsertPairingRequest(params: {
        channel: string;
        id: string;
        meta?: { name?: string };
      }): Promise<{ code: string; created: boolean }>;
    };
    media: {
      fetchRemoteMedia(params: { url: string }): Promise<{ buffer: Buffer; contentType?: string }>;
      saveMediaBuffer(
        buffer: Uint8Array,
        contentType: string | undefined,
        direction: "inbound" | "outbound",
        maxBytes: number,
      ): Promise<{ path: string; contentType?: string }>;
    };
    mentions: {
      buildMentionRegexes(cfg: OpenClawConfig, agentId?: string): RegExp[];
      matchesMentionPatterns(text: string, regexes: RegExp[]): boolean;
    };
    groups: {
      resolveGroupPolicy(
        cfg: OpenClawConfig,
        channel: string,
        accountId: string,
        groupId: string,
      ): {
        allowlistEnabled: boolean;
        allowed: boolean;
        groupConfig?: unknown;
        defaultConfig?: unknown;
      };
      resolveRequireMention(
        cfg: OpenClawConfig,
        channel: string,
        accountId: string,
        groupId: string,
        override?: boolean,
      ): boolean;
    };
    debounce: {
      createInboundDebouncer<T>(opts: {
        debounceMs: number;
        buildKey: (v: T) => string | null;
        shouldDebounce: (v: T) => boolean;
        onFlush: (entries: T[]) => Promise<void>;
        onError?: (err: unknown) => void;
      }): { push: (v: T) => void; flush: () => Promise<void> };
      resolveInboundDebounceMs(cfg: OpenClawConfig, channel: string): number;
    };
    commands: {
      resolveCommandAuthorizedFromAuthorizers(params: {
        useAccessGroups: boolean;
        authorizers: Array<{ configured: boolean; allowed: boolean }>;
      }): boolean;
    };
  };
  logging: {
    shouldLogVerbose(): boolean;
    getChildLogger(name: string): PluginLogger;
  };
  state: {
    resolveStateDir(cfg: OpenClawConfig): string;
  };
};
```

Remarques :

- Le runtime est le seul moyen d'accéder aux comportements du noyau.
- Le SDK est intentionnellement petit et stable.
- Chaque méthode runtime correspond à une implémentation noyau existante (pas de code dupliqué).

## Plan de migration (par étapes, sécurisé)

### Phase 0 : Configuration de base

- Introduire `openclaw/plugin-sdk`.
- Ajouter `api.runtime` avec l'interface ci-dessus à `OpenClawPluginApi`.
- Conserver les importations existantes pendant la transition (ajouter des avertissements de dépréciation).

### Phase 1 : Nettoyage des ponts (faible risque)

- Remplacer `core-bridge.ts` dans chaque extension par `api.runtime`.
- Prioriser la migration de BlueBubbles, Zalo, Zalo Personal (déjà presque terminés).
- Supprimer le code de pontage dupliqué.

### Phase 2 : Plugins avec importations directes légères

- Migrer Matrix vers SDK + runtime.
- Valider la logique d'onboarding, de répertoire et de mentions de groupe.

### Phase 3 : Plugins avec importations directes lourdes

- Migrer Microsoft Teams (plugin utilisant le plus de fonctions d'aide runtime).
- Assurer que la sémantique des réponses/saisie en cours correspond au comportement actuel.

### Phase 4 : Pluginification d'iMessage

- Déplacer iMessage dans `extensions/imessage`.
- Remplacer les appels directs au noyau par `api.runtime`.
- Conserver les clés de configuration, le comportement CLI et la documentation.

### Phase 5 : Application

- Ajouter des règles lint / vérifications CI : interdire les importations de `src/**` depuis `extensions/**`.
- Ajouter des vérifications de compatibilité SDK/version des plugins (runtime + versioning sémantique du SDK).

## Compatibilité et versioning

- SDK : versioning sémantique, publié, changements documentés.
- Runtime : versioning selon la version du noyau. Ajouter `api.runtime.version`.
- Les plugins déclarent la plage de version runtime requise (ex. `openclawRuntime: ">=2026.2.0"`).

## Stratégie de test

- Tests unitaires au niveau adaptateur (valider les fonctions runtime avec les implémentations noyau réelles).
- Tests de référence par plugin : assurer aucune déviation de comportement (routage, appairage, listes blanches, filtrage des mentions).
- Exemple de plugin end-to-end unique en CI (installation + exécution + test de fumée).

## Questions en attente

- Où héberger les types du SDK : package indépendant ou export du noyau ?
- Distribution des types runtime : dans le SDK (types uniquement) ou dans le noyau ?
- Comment exposer les liens de documentation pour les plugins intégrés vs externes ?
- Autoriser les plugins en-repo à importer directement le noyau de manière limitée pendant la transition ?

## Critères de succès

- Tous les connecteurs de canal sont des plugins utilisant SDK + runtime.
- `extensions/**` n'importe plus de `src/**`.
- Le modèle de nouveau connecteur dépend uniquement de SDK + runtime.
- Les plugins externes peuvent être développés et mis à jour sans accès au code source du noyau.

Documentation connexe : [Plugins](/tools/plugin), [Canaux](/channels/index), [Configuration](/gateway/configuration).
