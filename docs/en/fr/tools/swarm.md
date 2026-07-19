---
summary: "Orchestrez des sous-agents concurrents à partir de scripts Code Mode avec des résultats structurés, un fan-out limité et une progression en direct"
title: "Swarm"
sidebarTitle: "Swarm"
read_when:
  - You want a Code Mode script to fan out work across several agents
  - You need structured child results, decision gates, or first-completion pipelines
  - You are enabling or tuning tools.swarm limits
  - You want to observe collector children in the session dashboard
---

Swarm est un moyen expérimental et optionnel d'orchestrer de nombreux sous-agents à partir d'un script [Code Mode](/fr/tools/code-mode). Utilisez le flux de contrôle JavaScript ou TypeScript normal tel que `Promise.all`, `while` et `if` pour distribuer le travail, collecter les résultats et prendre des décisions.

Il n'y a pas de DSL de graphe et pas de format de flux de travail séparé. Le programme est l'orchestration. Swarm ajoute des enfants collecteurs attendables, des résultats structurés, une concurrence limitée et un rapport de progression à ce programme.

## Activer Swarm

Le chemin recommandé est **Settings → Labs → Swarm** dans l'interface de contrôle. Le bouton bascule prend effet immédiatement et écrit `tools.swarm.enabled` dans votre configuration.

Vous pouvez également activer Swarm directement dans `openclaw.json` :

```json5
{
  tools: {
    swarm: {
      enabled: true,
      maxConcurrent: 8,
      maxChildrenPerGroup: 50,
      maxTotalPerGroup: 200,
      waitTimeoutSecondsMax: 600,
      defaultAgentId: "",
    },
  },
}
```

Le raccourci booléen active ou désactive la fonctionnalité avec toutes les autres valeurs à leurs valeurs par défaut :

```json5
{
  tools: {
    swarm: true,
  },
}
```

| Champ                   | Défaut | Description                                                                                                                    |
| ----------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `enabled`               | `false` | Expose les options de génération en mode collecteur, `agents_wait` et l'API invité Code Mode `agents.*`.                       |
| `maxConcurrent`         | `8`     | Nombre maximum d'enfants collecteurs s'exécutant simultanément dans un groupe swarm. Les enfants acceptés supplémentaires sont mis en file d'attente dans l'ordre FIFO. |
| `maxChildrenPerGroup`   | `50`    | Nombre maximum d'enfants collecteurs actifs dans un groupe.                                                                    |
| `maxTotalPerGroup`      | `200`   | Nombre maximum d'enfants collecteurs qu'un groupe peut générer au cours de sa durée de vie. C'est le filet de sécurité contre la génération incontrôlée. |
| `waitTimeoutSecondsMax` | `600`   | Délai d'expiration maximal accepté par un appel `agents_wait`. La valeur par défaut de l'appel est de 30 secondes.            |
| `defaultAgentId`        | `""`    | Agent cible utilisé lorsqu'une génération omet `agentId`. Une valeur vide utilise l'agent demandeur. Les listes blanches de sous-agents existantes s'appliquent. |

Les valeurs numériques doivent être des entiers positifs. OpenClaw limite `maxConcurrent` à `1`–`1000`, `maxChildrenPerGroup` à `1`–`10000`, `maxTotalPerGroup` à `1`–`100000` et `waitTimeoutSecondsMax` à `1`–`86400`.

Vous pouvez remplacer Swarm pour un agent configuré avec `agents.list[].tools.swarm`. L'objet par agent fusionne sur l'objet `tools.swarm` de niveau supérieur.

## Exigences

Les globales invitées `agents.run`, `phase` et `log` nécessitent à la fois Swarm et OpenClaw Code Mode :

```json5
{
  tools: {
    codeMode: true,
    swarm: true,
  },
}
```

Code Mode doit également avoir un accès effectif à `sessions_spawn`. Les profils d'outils, la politique d'autorisation/refus, les règles de fournisseur et la politique de bac à sable peuvent supprimer cet outil. Consultez [Activation de Code Mode](/fr/tools/code-mode#activation) et [Sous-agents](/fr/tools/subagents) si un script signale que `sessions_spawn` n'est pas disponible.

Les valeurs `defaultAgentId` et `agentId` par exécution doivent nommer une cible configurée autorisée par la politique `subagents.allowAgents` du demandeur. OpenClaw rejette une cible inconnue ou non autorisée au lieu de revenir à un autre agent.

## Écrire un script Swarm

Lorsque Swarm est activé, Code Mode expose cette API invité :

```typescript
type AgentRunOptions = {
  label?: string;
  model?: string;
  thinking?: string;
  fastMode?: boolean | "auto";
  agentId?: string;
  schema?: Record<string, unknown>;
  phase?: string;
};

agents.run(prompt: string, options?: AgentRunOptions & { schema?: undefined }): Promise<string>;
agents.run<T>(prompt: string, options: AgentRunOptions & { schema: Record<string, unknown> }): Promise<T>;
phase(title: string): void;
log(message: string): void;
```

Sans `schema`, `agents.run()` se résout au texte final de l'enfant. Avec un schéma JSON, il se résout à la valeur soumise via l'outil `structured_output` de l'enfant. Un enfant échoué, tué, expiré ou invalide selon le schéma rejette la promesse avec une `SwarmAgentError`. Lisez les déclarations générées exactes et les idiomes d'orchestration courts à partir de `API.read("agents.d.ts")` dans Code Mode.

Utilisez `label` pour un nom d'enfant reconnaissable dans le tableau de bord et la barre latérale. Utilisez `phase` dans les options pour publier une phase immédiatement avant le démarrage de cet enfant, ou appelez `phase()` lorsque plusieurs enfants appartiennent à la même étape. `log()` publie une courte note de progression. Les appels de progression sont « fire-and-forget » ; ils ne retardent pas le script si l'interface utilisateur n'est pas disponible.

### Distribuer en parallèle avec des résultats structurés

Cet exemple lance un chercheur par sujet, attend tous les résultats, puis demande à un enfant final de synthétiser leurs rapports structurés :

```javascript
const reportSchema = {
  type: "object",
  properties: {
    finding: { type: "string" },
    evidence: { type: "array", items: { type: "string" } },
    confidence: { type: "number" },
  },
  required: ["finding", "evidence", "confidence"],
  additionalProperties: false,
};

const topics = ["authentication", "storage", "recovery"];
phase("Independent review");

const reports = await Promise.all(
  topics.map((topic) =>
    agents.run(`Review the ${topic} path. Return one finding with evidence.`, {
      label: `review-${topic}`,
      thinking: "high",
      fastMode: "auto",
      schema: reportSchema,
    }),
  ),
);

phase("Synthesis");
log(`Collected ${reports.length} independent reports.`);

return await agents.run(
  `Reconcile these reports and explain disagreements:\n${JSON.stringify(reports)}`,
  { label: "synthesis" },
);
```

`Promise.all` est la limite de distribution et de regroupement. OpenClaw démarre jusqu'à `maxConcurrent` enfants pour le groupe et met en file d'attente le reste dans l'ordre de soumission.

### Boucler sur une porte de décision

Utilisez une boucle `while` limitée lorsque chaque passage décide si un autre passage est nécessaire :

```javascript
const gateSchema = {
  type: "object",
  properties: {
    ready: { type: "boolean" },
    reason: { type: "string" },
    nextAction: { type: "string" },
  },
  required: ["ready", "reason", "nextAction"],
  additionalProperties: false,
};

let pass = 0;
let decision = { ready: false, reason: "Not checked", nextAction: "Review" };

while (!decision.ready && pass < 4) {
  pass += 1;
  phase(`Decision pass ${pass}`);
  decision = await agents.run(
    `Check whether the release evidence is complete. Previous decision: ${JSON.stringify(decision)}`,
    {
      label: `release-gate-${pass}`,
      schema: gateSchema,
    },
  );
  log(decision.reason);
}

if (!decision.ready) {
  throw new Error(`Gate still closed after ${pass} passes: ${decision.nextAction}`);
}

return decision;
```

Limitez toujours les boucles de décision. `maxTotalPerGroup` est le filet de sécurité final, pas un substitut à une condition d'arrêt claire.

### Traiter le premier enfant qui se termine

`agents.run()` retourne une promesse ordinaire, donc `Promise.race` peut réagir au premier enfant Code Mode. Pour les harnais qui appellent les outils de niveau inférieur, `agents_wait` fournit la même limite de première exécution : il retourne dès qu'au moins une exécution demandée se termine, ou lorsque le délai d'expiration limité expire. Consultez [Utiliser Swarm à partir d'autres harnais](#use-swarm-from-other-harnesses) pour la boucle de vidage complète.

## Comment se comportent les enfants collecteurs

Les enfants collecteurs sont des sessions de sous-agents isolées ordinaires avec un chemin d'exécution différent. Ils écrivent un résultat collecteur durable pour que le parent l'attende au lieu d'annoncer ou de diriger une réponse dans la session parent.

L'agent cible se résout dans cet ordre :

1. `agentId` sur l'appel de génération ou `agents.run()`.
2. `tools.swarm.defaultAgentId`.
3. L'agent demandeur.

Un agent de travail dédié et léger est utile lorsque les enfants swarm ont besoin d'une surface d'outils plus petite, d'un modèle moins cher ou d'une politique de bac à sable plus stricte. OpenClaw ne fournit pas d'ID d'agent `worker` intégré ; configurez-en un avant de le nommer comme valeur par défaut.

Les approbations des collecteurs échouent fermées. Un enfant n'ouvre jamais une invite d'approbation d'opérateur. Une action d'outil qui nécessiterait une approbation est refusée, et l'enfant peut signaler ce refus dans son résultat afin que le script puisse décider quoi faire ensuite.

Pour la sortie structurée, OpenClaw ajoute un outil `structured_output` synthétique à l'enfant et valide sa charge utile par rapport au schéma JSON fourni. Une charge utile invalide ou manquante reçoit une correction. Si la nouvelle tentative ne valide toujours pas, l'exécution du collecteur conserve le texte brut de l'enfant, laisse `structured` non défini et inclut `schemaError`. Le résultat `agents_wait` de bas niveau expose ces champs pour une logique de récupération explicite.

Swarm applique les trois limites de groupe avant de démarrer plus de travail. Les enfants au-dessus de `maxConcurrent` sont mis en file d'attente FIFO. Une génération qui dépasse `maxChildrenPerGroup` ou `maxTotalPerGroup` est rejetée avec la clé de configuration pertinente dans l'erreur.

## Observer un Swarm

Ouvrez le tableau de bord de la session parent dans l'interface de contrôle pendant qu'un swarm est actif. Le widget Swarm affiche chaque groupe collecteur actif sous la forme d'un point par enfant avec l'état en attente, en cours d'exécution, terminé ou échoué. Les étiquettes apparaissent dans les info-bulles des points, donc les étiquettes courtes et stables rendent les plus grands swarms plus faciles à lire.

La barre latérale de la session conserve l'arborescence parent/enfant normale. Développez la ligne parent pour inspecter un enfant collecteur ou ouvrir sa transcription sans perdre la hiérarchie du swarm.

Les résultats des collecteurs restent attendables jusqu'à ce que leur groupe soit archivé. Après que chaque membre atteigne sa date limite de rétention, OpenClaw archive les enfants du groupe par lot afin que les swarms terminés ne restent pas dans l'arborescence de session active.

## Utiliser Swarm à partir d'autres harnais

Vous pouvez utiliser Swarm sans OpenClaw Code Mode. Ses outils principaux sont
indépendants du harnais : démarrez les enfants collecteurs avec
`sessions_spawn({ collect: true })` et videz-les avec des appels `agents_wait`
bornés.

Codex Code Mode expose automatiquement les outils OpenClaw dynamiques éligibles sous
`tools.*`. Il n'utilise pas l'API guest QuickJS d'OpenClaw et ne nécessite pas
`tools.codeMode`, mais `tools.swarm` doit toujours être activé. Utilisez ce modèle :

```javascript
const tasks = [
  "Check the authentication path.",
  "Check the storage path.",
  "Check the recovery path.",
];

const launches = await Promise.all(
  tasks.map((task, index) =>
    tools.sessions_spawn({
      task,
      collect: true,
      label: `review-${index + 1}`,
    }),
  ),
);

for (const launch of launches) {
  if (launch.status !== "accepted") {
    throw new Error(launch.error ?? "Collector spawn was not accepted.");
  }
}

const pending = new Set(launches.map((launch) => launch.runId));
const completed = [];

while (pending.size > 0) {
  const ids = [...pending].slice(0, 1000);
  const batch = await tools.agents_wait({
    ids,
    timeoutSeconds: 30,
  });

  // Rotate this bounded window behind ids that have not been checked yet.
  for (const runId of ids) {
    if (pending.delete(runId)) pending.add(runId);
  }

  for (const item of batch.completed) {
    pending.delete(item.runId);
    if (item.status !== "done") {
      throw new Error(item.schemaError ?? item.result ?? `${item.runId}: ${item.status}`);
    }
    completed.push(item); // Process each result as soon as it finishes.
  }

  for (const failure of batch.errors ?? []) {
    pending.delete(failure.runId);
    throw new Error(`${failure.runId}: ${failure.error}`);
  }
}

return completed;
```

Chaque appel `agents_wait` accepte 1–1000 identifiants d'exécution. Il retourne :

```typescript
type AgentsWaitResult = {
  completed: Array<{
    runId: string;
    status: "done" | "failed" | "killed" | "timeout";
    result: string;
    structured?: unknown;
    schemaError?: string;
    sessionKey: string;
    label?: string;
    usage?: { inputTokens: number; outputTokens: number };
  }>;
  pending: string[];
  errors?: Array<{
    runId: string;
    error: "not_found" | "not_owner";
  }>;
};
```

L'appel retourne immédiatement quand un enfant demandé est déjà terminé,
quand au moins un enfant en attente se termine, quand aucun identifiant en attente valide ne reste,
ou quand son délai d'expiration expire. Les enregistrements terminés sont idempotents, donc passer un
identifiant d'exécution déjà terminé retourne son résultat à nouveau. Seule la session de génération
ou sa chaîne parente autorisée peut attendre un collecteur.

Il s'agit d'un long polling borné, pas d'une boucle de statut occupée. Continuez à passer uniquement les
identifiants d'exécution restants jusqu'à ce que `pending` soit vide. Le mode collecteur supporte les
sous-agents OpenClaw natifs ; il ne supporte pas le runtime ACP, la liaison de thread, les sessions visibles,
ou le mode session persistant.

## Limites et feuille de route

Swarm v1 exécute des enfants collecteurs ponctuels ; l'API `agents.session()` prévue
ajoutera des workers multi-tours avec état. Les enfants s'exécutent actuellement sur la voie
sub-agent de la Gateway locale ; le placement cloud est prévu comme option de génération explicite.
Les définitions de flux de travail sauvegardées et un DSL de graphe ne font pas partie de la
direction actuelle de Swarm.

## Connexes

- [Code Mode](/fr/tools/code-mode) pour le runtime guest QuickJS et les règles d'activation
- [Sub-agents](/fr/tools/subagents) pour la politique enfant, l'isolation et le comportement de session
- [Outils sandbox multi-agents](/fr/tools/multi-agent-sandbox-tools) pour les restrictions par agent
- [Aperçu des outils](/fr/tools) pour les profils d'outils et le routage de politique
