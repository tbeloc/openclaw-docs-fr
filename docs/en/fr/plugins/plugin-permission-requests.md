---
summary: "Demander aux utilisateurs d'approuver les appels d'outils de plugin et les invites de permissions détenues par le plugin"
title: "Demandes de permissions de plugin"
sidebarTitle: "Demandes de permissions"
read_when:
  - You need a plugin hook or tool to ask before a side effect runs
  - You need to configure where plugin approval prompts are delivered
  - You are deciding between optional tools, exec approvals, and plugin approvals
---

Les demandes de permissions de plugin permettent au code du plugin de suspendre un appel d'outil ou une opération détenue par le plugin jusqu'à ce qu'un utilisateur l'approuve ou la refuse. Elles utilisent le flux `plugin.approval.*` de la Gateway et les mêmes surfaces d'interface d'approbation qui gèrent les boutons d'approbation de chat et les commandes `/approve`.

Utilisez les demandes de permissions de plugin pour les permissions de plugin/application. Elles ne remplacent pas les approbations exec de l'hôte, les listes blanches d'outils optionnels ou l'examen des permissions natif de Codex.

## Choisir la bonne barrière

Choisissez la barrière qui correspond au point de décision dont vous avez besoin :

| Barrière                         | À utiliser quand                                                         | Ce qu'elle contrôle                                                                                               |
| -------------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| Outils optionnels                | Un outil ne doit pas être visible pour le modèle jusqu'à ce que l'utilisateur l'active. | Exposition de l'outil via `tools.allow`.                                                                         |
| Demandes de permissions de plugin | Un hook de plugin ou une opération détenue par le plugin doit demander avant qu'une action s'exécute. | Approbation à l'exécution via `plugin.approval.*`.                                                               |
| Approbations exec                | Une commande hôte ou un outil de type shell a besoin de l'approbation de l'opérateur. | Politique exec de l'hôte et listes blanches exec durables.                                                       |
| Demandes de permissions natives Codex | Codex demande avant les actions natives de shell, fichier, MCP ou app-server. | Gestion de l'approbation du hook natif ou app-server de Codex, acheminée via les approbations de plugin quand OpenClaw possède l'invite. |
| Élicitations d'approbation MCP   | Un serveur MCP Codex demande l'approbation pour un appel d'outil.        | Réponses d'approbation MCP acheminées via les approbations de plugin OpenClaw.                                    |

Les outils optionnels sont une barrière au moment de la découverte. Les demandes de permissions de plugin sont une barrière par appel. Utilisez les deux quand un outil sensible doit nécessiter un opt-in explicite avant que le modèle puisse le voir et une approbation avant que l'action s'exécute.

## Demander une approbation avant un appel d'outil

La plupart des invites créées par le plugin doivent commencer dans un hook `before_tool_call`. Le hook s'exécute après que le modèle sélectionne un outil et avant qu'OpenClaw l'exécute :

```typescript
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

export default definePluginEntry({
  id: "deploy-policy",
  name: "Deploy Policy",
  register(api) {
    api.on("before_tool_call", async (event) => {
      if (event.toolName !== "deploy_service") {
        return;
      }

      const environment =
        typeof event.params.environment === "string" ? event.params.environment : "unknown";

      return {
        requireApproval: {
          title: "Deploy service",
          description: `Deploy service to ${environment}.`,
          severity: environment === "production" ? "critical" : "warning",
          allowedDecisions:
            environment === "production"
              ? ["allow-once", "deny"]
              : ["allow-once", "allow-always", "deny"],
          timeoutMs: 120_000,
          timeoutBehavior: "deny",
          onResolution(decision) {
            console.log(`deploy approval resolved: ${decision}`);
          },
        },
      };
    });
  },
});
```

Rédigez le texte de l'invite pour la personne qui approuvera l'action :

- Gardez `title` court et axé sur l'action. La Gateway accepte jusqu'à 80 caractères.
- Gardez `description` spécifique et délimitée. La Gateway accepte jusqu'à 256 caractères.
- Incluez l'action, la cible et le risque. N'incluez pas les secrets, les jetons ou les charges utiles privées qui ne doivent pas apparaître dans les surfaces d'approbation de chat.
- Utilisez `severity: "critical"` uniquement pour les actions où une mauvaise décision pourrait causer des dommages en production ou une perte de données.
- Utilisez `allowedDecisions: ["allow-once", "deny"]` quand la confiance persistante n'est pas sûre pour cette action.

## Comportement de la décision

OpenClaw crée une approbation en attente avec un ID `plugin:`, la livre aux surfaces d'approbation disponibles et attend une décision.

| Décision          | Résultat                                                                  |
| ----------------- | ------------------------------------------------------------------------- |
| `allow-once`      | L'appel actuel continue.                                                  |
| `allow-always`    | L'appel actuel continue et la décision est transmise au plugin.           |
| `deny`            | L'appel est bloqué avec un résultat d'outil refusé.                       |
| Délai d'expiration | L'appel est bloqué sauf si `timeoutBehavior` est `"allow"`.               |
| Annulation        | L'appel est bloqué quand l'exécution est interrompue.                     |
| Aucune route d'approbation | L'appel est bloqué car aucune surface d'approbation connectée ne peut le résoudre. |

`allow-always` n'est durable que si le plugin demandeur ou le runtime implémente cette persistance. Pour les hooks `before_tool_call.requireApproval` ordinaires, OpenClaw traite `allow-once` et `allow-always` comme des décisions d'approbation pour l'appel actuel et transmet la valeur résolue à `onResolution`. Si votre plugin offre `allow-always`, documentez et implémentez exactement quels appels futurs il approuve.

Si le hook retourne également `params`, OpenClaw applique ces modifications de paramètres uniquement après que l'approbation réussisse. Un hook de priorité inférieure peut toujours bloquer après qu'un hook de priorité supérieure ait demandé une approbation.

`allowedDecisions` limite les boutons et les commandes affichés à l'utilisateur. La Gateway rejette une tentative de résolution pour toute décision que la demande n'a pas offerte.

## Acheminer les invites d'approbation

Les invites d'approbation peuvent se résoudre dans les surfaces d'interface utilisateur locales ou dans les canaux de chat qui supportent la gestion des approbations. Pour transférer les invites d'approbation de plugin vers des cibles de chat explicites, configurez `approvals.plugin` :

```json5
{
  approvals: {
    plugin: {
      enabled: true,
      mode: "targets",
      agentFilter: ["main"],
      targets: [{ channel: "slack", to: "U12345678" }],
    },
  },
}
```

`approvals.plugin` est indépendant de `approvals.exec`. L'activation du transfert d'approbation exec n'achemine pas les invites d'approbation de plugin, et l'activation du transfert d'approbation de plugin ne change pas la politique exec de l'hôte.

Quand une invite inclut du texte d'approbation manuel, résolvez-la avec l'une des décisions offertes :

```text
/approve <id> allow-once
/approve <id> allow-always
/approve <id> deny
```

Voir [Approbations exec avancées](/fr/tools/exec-approvals-advanced#plugin-approval-forwarding) pour le modèle de transfert complet, le comportement d'approbation dans le même chat, la livraison de canal natif et les règles d'approbateur spécifiques au canal.

## Permissions natives Codex

Les invites de permissions natives Codex peuvent également voyager via les approbations de plugin, mais elles ont une propriété différente des hooks créés par le plugin.

- Les demandes d'approbation app-server de Codex s'acheminent via OpenClaw après l'examen de Codex.
- Le relais de hook natif `permission_request` peut demander via `plugin.approval.request` quand ce relais est activé.
- Les élicitations d'approbation d'outil MCP s'acheminent via les approbations de plugin quand Codex marque `_meta.codex_approval_kind` comme `"mcp_tool_call"`.

Voir [Runtime du harnais Codex](/fr/plugins/codex-harness-runtime#native-permissions-and-mcp-elicitations) pour le comportement spécifique à Codex et les règles de secours.

## Dépannage

**L'outil dit que les approbations de plugin ne sont pas disponibles.** Aucune interface d'approbation ou route d'approbation configurée n'a accepté la demande. Connectez un client capable d'approbation, utilisez un canal qui supporte `/approve` dans le même chat, ou configurez `approvals.plugin`.

**`allow-always` apparaît mais l'appel suivant demande à nouveau.** Le flux d'approbation de plugin générique ne persiste pas automatiquement la confiance pour les hooks arbitraires. Persistez la confiance détenue par le plugin dans votre plugin après `onResolution("allow-always")`, ou offrez uniquement `allow-once` et `deny`.

**`/approve` rejette la décision.** La demande a restreint `allowedDecisions`. Utilisez l'une des décisions imprimées dans l'invite.

**Une invite Slack, Discord, Telegram ou Matrix s'achemine différemment des approbations exec.** Les approbations de plugin et les approbations exec utilisent une configuration séparée et peuvent utiliser des vérifications d'autorisation différentes. Vérifiez `approvals.plugin` et le support d'approbation de plugin du canal au lieu de vérifier uniquement `approvals.exec`.

## Connexes

- [Hooks de plugin](/fr/plugins/hooks#tool-call-policy)
- [Construire des plugins](/fr/plugins/building-plugins#registering-agent-tools)
- [Approbations exec avancées](/fr/tools/exec-approvals-advanced#plugin-approval-forwarding)
- [Protocole Gateway](/fr/gateway/protocol)
- [Runtime du harnais Codex](/fr/plugins/codex-harness-runtime#native-permissions-and-mcp-elicitations)
