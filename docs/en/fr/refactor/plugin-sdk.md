---
summary: "Plan: one clean plugin SDK + runtime for all messaging connectors"
read_when:
  - Defining or refactoring the plugin architecture
  - Migrating channel connectors to the plugin SDK/runtime
title: "Plugin SDK Refactor"
---

# Plan de refactorisation du SDK + Runtime des plugins

Objectif : chaque connecteur de messagerie est un plugin (fourni ou externe) utilisant une API stable unique.
Aucun plugin n'importe directement depuis `src/**`. Toutes les dépendances passent par le SDK ou le runtime.

## Pourquoi maintenant

- Les connecteurs actuels mélangent les modèles : imports directs du noyau, ponts dist uniquement et helpers personnalisés.
- Cela rend les mises à jour fragiles et bloque une surface de plugin externe propre.

## Architecture cible (deux couches)

### 1) SDK des plugins (compile-time, stable, publiable)

Portée : types, helpers et utilitaires de configuration. Aucun état runtime, aucun effet secondaire.

Contenu (exemples) :

- Types : `ChannelPlugin`, adaptateurs, `ChannelMeta`, `ChannelCapabilities`, `ChannelDirectoryEntry`.
- Helpers de configuration : `buildChannelConfigSchema`, `setAccountEnabledInConfigSection`, `deleteAccountFromConfigSection`,
  `applyAccountNameToChannelSection`.
- Helpers d'appairage : `PAIRING_APPROVED_MESSAGE`, `formatPairingApproveHint`.
- Helpers d'intégration : `promptChannelAccessConfig`, `addWildcardAllowFrom`, types d'intégration.
- Helpers de paramètres d'outils : `createActionGate`, `readStringParam`, `readNumberParam`, `readReactionParams`, `jsonResult`.
- Helper de lien de documentation : `formatDocsLink`.

Livraison :

- Publier en tant que `openclaw/plugin-sdk` (ou exporter depuis le noyau sous `openclaw/plugin-sdk`).
- Semver avec garanties de stabilité explicites.

### 2) Runtime des plugins (surface d'exécution, injecté)

Portée : tout ce qui touche au comportement du runtime du noyau.
Accédé via `OpenClawPluginApi.runtime` afin que les plugins n'importent jamais `src/**`.

Surface proposée (minimale mais complète) :

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

Notes :

- Le runtime est le seul moyen d'accéder au comportement du noyau.
- Le SDK est intentionnellement petit et stable.
- Chaque méthode du runtime correspond à une implémentation existante du noyau (pas de duplication).

## Plan de migration (par phases, sûr)

### Phase 0 : scaffolding

- Introduire `openclaw/plugin-sdk`.
- Ajouter `api.runtime` à `OpenClawPluginApi` avec la surface ci-dessus.
- Maintenir les imports existants pendant une période de transition (avertissements de dépréciation).

### Phase 1 : nettoyage des ponts (risque faible)

- Remplacer `core-bridge.ts` par extension avec `api.runtime`.
- Migrer BlueBubbles, Zalo, Zalo Personal en premier (déjà proches).
- Supprimer le code de pont dupliqué.

### Phase 2 : plugins légers avec imports directs

- Migrer Matrix vers SDK + runtime.
- Valider la logique d'intégration, de répertoire et de mention de groupe.

### Phase 3 : plugins lourds avec imports directs

- Migrer MS Teams (plus grand ensemble de helpers runtime).
- S'assurer que la sémantique de réponse/saisie correspond au comportement actuel.

### Phase 4 : pluginisation d'iMessage

- Déplacer iMessage dans `extensions/imessage`.
- Remplacer les appels directs du noyau par `api.runtime`.
- Conserver les clés de configuration, le comportement CLI et la documentation.

### Phase 5 : application

- Ajouter une règle lint / vérification CI : aucun import `extensions/**` depuis `src/**`.
- Ajouter des vérifications de compatibilité SDK/version des plugins (runtime + SDK semver).

## Compatibilité et versioning

- SDK : semver, publié, changements documentés.
- Runtime : versionné par version du noyau. Ajouter `api.runtime.version`.
- Les plugins déclarent une plage de runtime requise (par exemple, `openclawRuntime: ">=2026.2.0"`).

## Stratégie de test

- Tests unitaires au niveau de l'adaptateur (fonctions runtime exercées avec implémentation du noyau réelle).
- Tests de référence par plugin : assurer aucune dérive de comportement (routage, appairage, liste d'autorisation, gating de mention).
- Un seul exemple de plugin end-to-end utilisé en CI (installer + exécuter + smoke).

## Questions ouvertes

- Où héberger les types SDK : package séparé ou export du noyau ?
- Distribution des types du runtime : dans le SDK (types uniquement) ou dans le noyau ?
- Comment exposer les liens de documentation pour les plugins fournis vs externes ?
- Autorisons-nous les imports directs du noyau limités pour les plugins dans le repo pendant la transition ?

## Critères de succès

- Tous les connecteurs de canal sont des plugins utilisant SDK + runtime.
- Aucun import `extensions/**` depuis `src/**`.
- Les nouveaux modèles de connecteur dépendent uniquement de SDK + runtime.
- Les plugins externes peuvent être développés et mis à jour sans accès au code source du noyau.

Docs connexes : [Plugins](/tools/plugin), [Channels](/channels/index), [Configuration](/gateway/configuration).
