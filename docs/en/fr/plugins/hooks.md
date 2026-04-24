---
summary: "Crochets de plugin : intercepter les événements du cycle de vie de l'agent, de l'outil, du message, de la session et de la passerelle"
title: "Crochets de plugin"
read_when:
  - You are building a plugin that needs before_tool_call, before_agent_reply, message hooks, or lifecycle hooks
  - You need to block, rewrite, or require approval for tool calls from a plugin
  - You are deciding between internal hooks and plugin hooks
---

Les crochets de plugin sont des points d'extension en processus pour les plugins OpenClaw. Utilisez-les
quand un plugin doit inspecter ou modifier les exécutions d'agent, les appels d'outil, le flux de messages,
le cycle de vie de la session, le routage des sous-agents, les installations ou le démarrage de la passerelle.

Utilisez plutôt les [crochets internes](/fr/automation/hooks) quand vous voulez un petit
script `HOOK.md` installé par l'opérateur pour les événements de commande et de passerelle tels que
`/new`, `/reset`, `/stop`, `agent:bootstrap`, ou `gateway:startup`.

## Démarrage rapide

Enregistrez les crochets de plugin typés avec `api.on(...)` depuis votre entrée de plugin :

```typescript
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

export default definePluginEntry({
  id: "tool-preflight",
  name: "Tool Preflight",
  register(api) {
    api.on(
      "before_tool_call",
      async (event) => {
        if (event.toolName !== "web_search") {
          return;
        }

        return {
          requireApproval: {
            title: "Run web search",
            description: `Allow search query: ${String(event.params.query ?? "")}`,
            severity: "info",
            timeoutMs: 60_000,
            timeoutBehavior: "deny",
          },
        };
      },
      { priority: 50 },
    );
  },
});
```

Les gestionnaires de crochet s'exécutent séquentiellement par ordre décroissant de `priority`. Les crochets de même priorité
conservent l'ordre d'enregistrement.

## Catalogue des crochets

Les crochets sont groupés par la surface qu'ils étendent. Les noms en **gras** acceptent un
résultat de décision (bloquer, annuler, remplacer ou exiger une approbation) ; tous les autres sont
en observation uniquement.

**Tour d'agent**

- `before_model_resolve` — remplacer le fournisseur ou le modèle avant le chargement des messages de session
- `before_prompt_build` — ajouter du contexte dynamique ou du texte de système-prompt avant l'appel au modèle
- `before_agent_start` — phase combinée de compatibilité uniquement ; préférez les deux crochets ci-dessus
- **`before_agent_reply`** — court-circuiter le tour du modèle avec une réponse synthétique ou le silence
- `agent_end` — observer les messages finaux, l'état de succès et la durée d'exécution

**Observation de conversation**

- `llm_input` — observer l'entrée du fournisseur (système prompt, prompt, historique)
- `llm_output` — observer la sortie du fournisseur

**Outils**

- **`before_tool_call`** — réécrire les paramètres d'outil, bloquer l'exécution ou exiger une approbation
- `after_tool_call` — observer les résultats d'outil, les erreurs et la durée
- **`tool_result_persist`** — réécrire le message d'assistant produit à partir d'un résultat d'outil
- **`before_message_write`** — inspecter ou bloquer une écriture de message en cours (rare)

**Messages et livraison**

- **`inbound_claim`** — réclamer un message entrant avant le routage de l'agent (réponses synthétiques)
- `message_received` — observer le contenu entrant, l'expéditeur, le fil et les métadonnées
- **`message_sending`** — réécrire le contenu sortant ou annuler la livraison
- `message_sent` — observer le succès ou l'échec de la livraison sortante
- **`before_dispatch`** — inspecter ou réécrire une expédition sortante avant le transfert de canal
- **`reply_dispatch`** — participer au pipeline final de réponse-expédition

**Sessions et compaction**

- `session_start` / `session_end` — suivre les limites du cycle de vie de la session
- `before_compaction` / `after_compaction` — observer ou annoter les cycles de compaction
- `before_reset` — observer les événements de réinitialisation de session (`/reset`, réinitialisations programmatiques)

**Sous-agents**

- `subagent_spawning` / `subagent_delivery_target` / `subagent_spawned` / `subagent_ended` — coordonner le routage des sous-agents et la livraison d'achèvement

**Cycle de vie**

- `gateway_start` / `gateway_stop` — démarrer ou arrêter les services appartenant au plugin avec la passerelle
- **`before_install`** — inspecter les analyses d'installation de compétence ou de plugin et bloquer éventuellement

## Politique d'appel d'outil

`before_tool_call` reçoit :

- `event.toolName`
- `event.params`
- `event.runId` optionnel
- `event.toolCallId` optionnel
- des champs de contexte tels que `ctx.agentId`, `ctx.sessionKey`, `ctx.sessionId` et
  `ctx.trace` de diagnostic

Il peut retourner :

```typescript
type BeforeToolCallResult = {
  params?: Record<string, unknown>;
  block?: boolean;
  blockReason?: string;
  requireApproval?: {
    title: string;
    description: string;
    severity?: "info" | "warning" | "critical";
    timeoutMs?: number;
    timeoutBehavior?: "allow" | "deny";
    pluginId?: string;
    onResolution?: (
      decision: "allow-once" | "allow-always" | "deny" | "timeout" | "cancelled",
    ) => Promise<void> | void;
  };
};
```

Règles :

- `block: true` est terminal et ignore les gestionnaires de priorité inférieure.
- `block: false` est traité comme aucune décision.
- `params` réécrit les paramètres d'outil pour l'exécution.
- `requireApproval` met en pause l'exécution de l'agent et demande à l'utilisateur via les approbations de plugin. La commande `/approve` peut approuver les approbations exec et plugin.
- Un `block: true` de priorité inférieure peut toujours bloquer après qu'un crochet de priorité supérieure
  ait demandé une approbation.
- `onResolution` reçoit la décision d'approbation résolue — `allow-once`,
  `allow-always`, `deny`, `timeout`, ou `cancelled`.

## Crochets de prompt et de modèle

Utilisez les crochets spécifiques à la phase pour les nouveaux plugins :

- `before_model_resolve` : reçoit uniquement le prompt actuel et les métadonnées de pièce jointe. Retournez `providerOverride` ou `modelOverride`.
- `before_prompt_build` : reçoit le prompt actuel et les messages de session. Retournez `prependContext`, `systemPrompt`, `prependSystemContext`, ou `appendSystemContext`.

`before_agent_start` reste pour la compatibilité. Préférez les crochets explicites ci-dessus
pour que votre plugin ne dépende pas d'une phase combinée héritée.

Les plugins non regroupés qui ont besoin de `llm_input`, `llm_output`, ou `agent_end` doivent définir :

```json
{
  "plugins": {
    "entries": {
      "my-plugin": {
        "hooks": {
          "allowConversationAccess": true
        }
      }
    }
  }
}
```

Les crochets de mutation de prompt peuvent être désactivés par plugin avec
`plugins.entries.<id>.hooks.allowPromptInjection=false`.

## Crochets de message

Utilisez les crochets de message pour le routage au niveau du canal et la politique de livraison :

- `message_received` : observer le contenu entrant, l'expéditeur, `threadId` et les métadonnées.
- `message_sending` : réécrire `content` ou retourner `{ cancel: true }`.
- `message_sent` : observer le succès ou l'échec final.

Préférez les champs `threadId` et `replyToId` typés avant d'utiliser les métadonnées spécifiques au canal.

Règles de décision :

- `message_sending` avec `cancel: true` est terminal.
- `message_sending` avec `cancel: false` est traité comme aucune décision.
- Le `content` réécrit continue vers les crochets de priorité inférieure sauf si un crochet ultérieur
  annule la livraison.

## Crochets d'installation

`before_install` s'exécute après l'analyse intégrée pour les installations de compétence et de plugin.
Retournez des résultats supplémentaires ou `{ block: true, blockReason }` pour arrêter l'
installation.

`block: true` est terminal. `block: false` est traité comme aucune décision.

## Cycle de vie de la passerelle

Utilisez `gateway_start` pour les services de plugin qui ont besoin d'un état appartenant à la passerelle. Le
contexte expose `ctx.config`, `ctx.workspaceDir` et `ctx.getCron?.()` pour
l'inspection et les mises à jour de cron. Utilisez `gateway_stop` pour nettoyer les
ressources longue durée.

Ne vous fiez pas au crochet interne `gateway:startup` pour les services d'exécution appartenant au plugin.

## Connexes

- [Building plugins](/fr/plugins/building-plugins)
- [Plugin SDK overview](/fr/plugins/sdk-overview)
- [Plugin entry points](/fr/plugins/sdk-entrypoints)
- [Internal hooks](/fr/automation/hooks)
- [Plugin architecture internals](/fr/plugins/architecture-internals)
