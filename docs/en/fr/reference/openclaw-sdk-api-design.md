---
summary: "Conception de référence pour l'API SDK OpenClaw publique proposée, taxonomie des événements, artefacts, approbations et structure des paquets"
title: "Conception de l'API SDK OpenClaw"
read_when:
  - You are implementing the proposed public OpenClaw app SDK
  - You need the draft namespace, event, result, artifact, approval, or security contract for the app SDK
  - You are comparing Gateway protocol resources with the high-level OpenClaw SDK wrapper
---

Cette page est la référence détaillée de la conception de l'API pour le [SDK OpenClaw](/fr/concepts/openclaw-sdk) public proposé. Elle est intentionnellement séparée du [SDK plugin](/fr/plugins/sdk-overview).

Le SDK public devrait être construit en deux couches :

1. Un client Gateway généré de bas niveau.
2. Un wrapper ergonomique de haut niveau avec des objets `OpenClaw`, `Agent`, `Session`, `Run`, `Task`, `Artifact`, `Approval` et `Environment`.

## Conception de l'espace de noms

Les espaces de noms de bas niveau doivent suivre de près les ressources Gateway :

```typescript
oc.agents.list();
oc.agents.get("main");
oc.agents.create(...);
oc.agents.update(...);

oc.sessions.list();
oc.sessions.create(...);
oc.sessions.resolve(...);
oc.sessions.send(...);
oc.sessions.messages(...);
oc.sessions.fork(...);
oc.sessions.compact(...);
oc.sessions.abort(...);

oc.runs.create(...);
oc.runs.get(runId);
oc.runs.events(runId, { after });
oc.runs.wait(runId);
oc.runs.cancel(runId);

oc.tasks.list(); // future API: current SDK throws unsupported
oc.tasks.get(taskId); // future API: current SDK throws unsupported
oc.tasks.cancel(taskId); // future API: current SDK throws unsupported
oc.tasks.events(taskId, { after }); // future API

oc.models.list();
oc.models.status(); // Gateway models.authStatus

oc.tools.list();
oc.tools.invoke(...); // future API: current SDK throws unsupported

oc.artifacts.list({ runId }); // future API: current SDK throws unsupported
oc.artifacts.get(artifactId); // future API: current SDK throws unsupported
oc.artifacts.download(artifactId); // future API: current SDK throws unsupported

oc.approvals.list();
oc.approvals.respond(approvalId, ...);

oc.environments.list(); // future API: current SDK throws unsupported
oc.environments.create(...); // future API: current SDK throws unsupported
oc.environments.status(environmentId); // future API: current SDK throws unsupported
oc.environments.delete(environmentId); // future API: current SDK throws unsupported
```

Les wrappers de haut niveau doivent retourner des objets qui rendent les flux courants agréables :

```typescript
const run = await agent.run(inputOrParams);
await run.cancel();
await run.wait();

for await (const event of run.events()) {
  // normalized event stream
}

const artifacts = await run.artifacts.list();
const session = await run.session();
```

## Contrat d'événement

Le SDK public doit exposer des événements versionnés, rejouables et normalisés.

```typescript
type OpenClawEvent = {
  version: 1;
  id: string;
  ts: number;
  type: OpenClawEventType;
  runId?: string;
  sessionId?: string;
  sessionKey?: string;
  taskId?: string;
  agentId?: string;
  data: unknown;
  raw?: unknown;
};
```

`id` est un curseur de relecture. Les consommateurs doivent pouvoir se reconnecter avec `events({ after: id })` et recevoir les événements manqués lorsque la rétention le permet.

Familles d'événements normalisées recommandées :

| Événement             | Signification                                                     |
| --------------------- | ----------------------------------------------------------------- |
| `run.created`         | Exécution acceptée.                                               |
| `run.queued`          | L'exécution attend une voie de session, un runtime ou un environnement. |
| `run.started`         | Le runtime a commencé l'exécution.                                |
| `run.completed`       | L'exécution s'est terminée avec succès.                           |
| `run.failed`          | L'exécution s'est terminée avec une erreur.                       |
| `run.cancelled`       | L'exécution a été annulée.                                        |
| `run.timed_out`       | L'exécution a dépassé son délai d'expiration.                     |
| `assistant.delta`     | Delta de texte de l'assistant.                                    |
| `assistant.message`   | Message complet de l'assistant ou remplacement.                   |
| `thinking.delta`      | Delta de raisonnement ou de plan, lorsque la politique le permet. |
| `tool.call.started`   | L'appel d'outil a commencé.                                       |
| `tool.call.delta`     | Progression en continu de l'appel d'outil ou sortie partielle.    |
| `tool.call.completed` | L'appel d'outil s'est terminé avec succès.                        |
| `tool.call.failed`    | L'appel d'outil a échoué.                                         |
| `approval.requested`  | Une exécution ou un outil nécessite une approbation.              |
| `approval.resolved`   | L'approbation a été accordée, refusée, expirée ou annulée.        |
| `question.requested`  | Le runtime demande une entrée à l'utilisateur ou à l'application hôte. |
| `question.answered`   | L'application hôte a fourni une réponse.                          |
| `artifact.created`    | Nouvel artefact disponible.                                       |
| `artifact.updated`    | L'artefact existant a changé.                                     |
| `session.created`     | Session créée.                                                    |
| `session.updated`     | Les métadonnées de session ont changé.                            |
| `session.compacted`   | La compaction de session s'est produite.                          |
| `task.updated`        | L'état de la tâche de fond a changé.                              |
| `git.branch`          | Le runtime a observé ou modifié l'état de la branche.             |
| `git.diff`            | Le runtime a produit ou modifié un diff.                          |
| `git.pr`              | Le runtime a ouvert, mis à jour ou lié une demande de tirage.     |

Les charges utiles natives du runtime doivent être disponibles via `raw`, mais les applications ne doivent pas avoir à analyser `raw` pour une interface utilisateur normale.

## Contrat de résultat

`Run.wait()` doit retourner une enveloppe de résultat stable :

```typescript
type RunResult = {
  runId: string;
  status: "accepted" | "completed" | "failed" | "cancelled" | "timed_out";
  sessionId?: string;
  sessionKey?: string;
  taskId?: string;
  startedAt?: string | number;
  endedAt?: string | number;
  output?: {
    text?: string;
    messages?: SDKMessage[];
  };
  usage?: {
    inputTokens?: number;
    outputTokens?: number;
    totalTokens?: number;
    costUsd?: number;
  };
  artifacts?: ArtifactSummary[];
  error?: SDKError;
};
```

Le résultat doit être simple et stable. Les valeurs d'horodatage préservent la forme Gateway, donc les exécutions actuelles soutenues par le cycle de vie signalent généralement des nombres en millisecondes d'époque tandis que les adaptateurs peuvent toujours afficher des chaînes ISO. L'interface utilisateur riche, les traces d'outils et les détails natifs du runtime appartiennent aux événements et aux artefacts.

`accepted` est un résultat d'attente non terminal : cela signifie que le délai d'attente Gateway a expiré avant que l'exécution ne produise une fin de cycle de vie ou une erreur. Il ne doit pas être traité comme `timed_out` ; `timed_out` est réservé à une exécution qui a dépassé son propre délai d'expiration du runtime.

## Approbations et questions

Les approbations doivent être de première classe car les agents de codage franchissent constamment les limites de sécurité.

```typescript
run.onApproval(async (request) => {
  if (request.kind === "tool" && request.toolName === "exec") {
    return request.approveOnce({ reason: "CI command allowed by policy" });
  }

  return request.askUser();
});
```

Les événements d'approbation doivent contenir :

- identifiant d'approbation
- identifiant d'exécution et identifiant de session
- type de demande
- résumé de l'action demandée
- nom de l'outil ou action d'environnement
- niveau de risque
- décisions disponibles
- expiration
- si la décision peut être réutilisée

Les questions sont distinctes des approbations. Une question demande à l'utilisateur ou à l'application hôte des informations. Une approbation demande la permission d'effectuer une action.

## Modèle ToolSpace

Les applications doivent comprendre la surface des outils sans importer les éléments internes du plugin.

```typescript
const tools = await run.toolSpace();

for (const tool of tools.list()) {
  console.log(tool.name, tool.source, tool.requiresApproval);
}
```

Le SDK doit exposer :

- métadonnées d'outil normalisées
- source : OpenClaw, MCP, plugin, canal, runtime ou application
- résumé du schéma
- politique d'approbation
- compatibilité du runtime
- si un outil est caché, en lecture seule, capable d'écriture ou capable d'hôte

L'invocation d'outil via le SDK doit être explicite et délimitée. La plupart des applications doivent exécuter des agents, pas appeler des outils arbitraires directement.

## Modèle d'artefact

Les artefacts doivent couvrir plus que des fichiers.

```typescript
type ArtifactSummary = {
  id: string;
  runId?: string;
  sessionId?: string;
  type:
    | "file"
    | "patch"
    | "diff"
    | "log"
    | "media"
    | "screenshot"
    | "trajectory"
    | "pull_request"
    | "workspace";
  title?: string;
  mimeType?: string;
  sizeBytes?: number;
  createdAt: string;
  expiresAt?: string;
};
```

Exemples courants :

- éditions de fichiers et fichiers générés
- lots de correctifs
- diffs VCS
- captures d'écran et sorties médias
- journaux et lots de traces
- liens de demande de tirage
- trajectoires du runtime
- snapshots d'espace de travail d'environnement géré

L'accès aux artefacts doit supporter la rédaction, la rétention et les URL de téléchargement sans supposer que chaque artefact est un fichier local normal.

## Modèle de sécurité

Le SDK d'application doit être explicite sur l'autorité.

Portées de jeton recommandées :

| Portée              | Permet                                              |
| ------------------- | --------------------------------------------------- |
| `agent.read`        | Lister et inspecter les agents.                     |
| `agent.run`         | Démarrer les exécutions.                            |
| `session.read`      | Lire les métadonnées et messages de session.        |
| `session.write`     | Créer, envoyer à, forker, compacter et abandonner les sessions. |
| `task.read`         | Lire l'état de la tâche de fond.                    |
| `task.write`        | Annuler ou modifier la politique de notification des tâches. |
| `approval.respond`  | Approuver ou refuser les demandes.                  |
| `tools.invoke`      | Invoquer les outils exposés directement.            |
| `artifacts.read`    | Lister et télécharger les artefacts.                |
| `environment.write` | Créer ou détruire les environnements gérés.         |
| `admin`             | Opérations administratives.                         |

Valeurs par défaut :

- pas de transmission de secret par défaut
- pas de passage de variable d'environnement sans restriction
- références de secret au lieu de valeurs de secret
- politique de sandbox et de réseau explicite
- rétention d'environnement distant explicite
- approbations pour l'exécution d'hôte sauf si la politique le prouve autrement
- événements de runtime bruts réduits avant de quitter Gateway sauf si l'appelant a une portée de diagnostic plus forte

## Fournisseur d'environnement géré

Les agents gérés doivent être implémentés en tant que fournisseurs d'environnement.

```typescript
type EnvironmentProvider = {
  id: string;
  capabilities: {
    checkout?: boolean;
    sandbox?: boolean;
    networkPolicy?: boolean;
    secrets?: boolean;
    artifacts?: boolean;
    logs?: boolean;
    pullRequests?: boolean;
    longRunning?: boolean;
  };
};
```

La première implémentation n'a pas besoin d'être un SaaS hébergé. Elle peut cibler les hôtes de nœud existants, les espaces de travail éphémères, les exécuteurs de style CI ou les environnements de style Testbox. Le contrat important est :

1. préparer l'espace de travail
2. lier l'environnement sûr et les secrets
3. démarrer l'exécution
4. diffuser les événements
5. collecter les artefacts
6. nettoyer ou conserver selon la politique

Une fois que cela est stable, un service cloud hébergé peut implémenter le même contrat de fournisseur.

## Structure des packages

Packages recommandés :

| Package                 | Objectif                                                      |
| ----------------------- | ------------------------------------------------------------- |
| `@openclaw/sdk`         | SDK public haut niveau et client Gateway généré bas niveau.   |
| `@openclaw/sdk-react`   | Hooks React optionnels pour les tableaux de bord et générateurs d'applications. |
| `@openclaw/sdk-testing` | Assistants de test et serveur Gateway factice pour les intégrations d'applications. |

Le repo contient déjà `openclaw/plugin-sdk/*` pour les plugins. Gardez cet espace de noms
séparé pour éviter de confondre les auteurs de plugins avec les développeurs d'applications.

## Stratégie de client généré

Le client bas niveau doit être généré à partir des schémas de protocole Gateway versionnés,
puis enveloppé par des classes ergonomiques écrites à la main.

Couches :

1. Source de vérité du schéma Gateway.
2. Client TypeScript bas niveau généré.
3. Validateurs d'exécution pour les entrées externes et les charges utiles d'événements.
4. Wrappers haut niveau `OpenClaw`, `Agent`, `Session`, `Run`, `Task` et `Artifact`.
5. Exemples de cookbook et tests d'intégration.

Avantages :

- la dérive de protocole est visible
- les tests peuvent comparer les méthodes générées avec les exports Gateway
- le SDK d'application reste indépendant des éléments internes du SDK de plugin
- les consommateurs bas niveau ont toujours un accès complet au protocole
- les consommateurs haut niveau obtiennent la petite API produit

## Documentation connexe

- [Conception du SDK OpenClaw](/fr/concepts/openclaw-sdk)
- [Référence RPC Gateway](/fr/reference/rpc)
- [Boucle d'agent](/fr/concepts/agent-loop)
- [Runtimes d'agent](/fr/concepts/agent-runtimes)
- [Tâches en arrière-plan](/fr/automation/tasks)
- [Agents ACP](/fr/tools/acp-agents)
- [Aperçu du SDK Plugin](/fr/plugins/sdk-overview)
