---
summary: "Utilisez OpenClaw Code Mode pour découvrir, appeler et combiner de grands catalogues d'outils dans des workflows JavaScript ou TypeScript compacts"
title: "Code Mode"
sidebarTitle: "Code Mode"
read_when:
  - You want to enable OpenClaw code mode for an agent run
  - You need to explain why Code Mode is different from Codex Code Mode
  - You are reviewing the compact tool contract, QuickJS-WASI sandbox, TypeScript transform, or hidden tool-catalog bridge
  - You are adding or reviewing an internal code-mode namespace registry integration
---

Code mode est une fonctionnalité expérimentale et optionnelle du runtime d'agent OpenClaw. Lorsqu'elle est activée, le modèle ne voit plus tous les schémas d'outils activés ; à la place, il voit `exec`, `wait` et tout outil direct uniquement dont le résultat structuré ne peut pas traverser le pont JSON uniquement. Le modèle écrit un petit programme JavaScript ou TypeScript qui recherche, décrit et appelle le catalogue d'outils caché.

Cette page documente OpenClaw code mode, pas Codex Code Mode. Les deux fonctionnalités partagent un nom et les mêmes noms d'outils de contrôle (`exec`, `wait`), mais ce sont des implémentations distinctes :

- Codex Code Mode s'exécute dans le harnais de codage Codex. Son outil `exec` est un outil à grammaire libre : le modèle écrit du code JavaScript brut (optionnellement préfixé par une ligne pragma `// @exec: {...}` pour les options d'exécution), exécuté dans le runtime Code Mode V8 en processus de Codex.
- OpenClaw code mode s'exécute dans le runtime d'agent OpenClaw générique et est désactivé sauf si `tools.codeMode.enabled: true` est configuré. Son outil `exec` prend une charge utile JSON `{ code, language }`, exécutée dans un worker QuickJS-WASI.

Les deux sont des surfaces d'exécution JavaScript, pas des surfaces de commandes shell. Traitez-les comme des fonctionnalités indépendantes, différemment implémentées, qui exposent simplement des outils `exec`/`wait` identiquement nommés.

## Ce qu'il fait

- La liste des outils visibles par le modèle devient `exec`, `wait`, plus tout outil direct uniquement comme `computer` ou le chargeur `image` de vision native dont le résultat d'image ne peut pas survivre au pont guest.
- `exec` évalue le JavaScript ou TypeScript généré par le modèle dans un worker QuickJS-WASI isolé.
- Chaque outil compatible avec le catalogue activé (cœur OpenClaw, plugin, MCP, client) est caché en tant qu'outil de modèle autonome et exposé dans le programme guest via `ALL_TOOLS` et `tools`.
- La description `exec` porte un index rapide borné des identifiants de catalogue OpenClaw/plugin exacts, des indices d'entrée compacts et des indices de sortie déclarés compacts lorsqu'un outil de confiance fournit un schéma de sortie. Il omet les descriptions, les schémas complets, les entrées MCP et les entrées de débordement ; la recherche de catalogue côté guest reste le recours.
- Le code guest recherche le catalogue caché, décrit le schéma d'un outil et appelle un outil via le même chemin d'exécution utilisé par les tours d'agent normaux (la politique, les approbations, les hooks, la télémétrie s'appliquent tous).
- Les outils MCP sont regroupés sous l'espace de noms `MCP` ; en code mode c'est la seule façon prise en charge de les appeler.
- `wait` reprend une exécution code-mode suspendue lorsque des appels d'outils imbriqués sont toujours en attente.

Code mode change uniquement la surface d'orchestration visible par le modèle. Il ne remplace pas les outils, les outils de plugin, les outils MCP, l'authentification, la politique d'approbation, le comportement du canal ou la sélection du modèle.

## Pourquoi l'utiliser

- Surface de prompt plus petite : les fournisseurs obtiennent deux outils de contrôle, un index d'outils natifs borné et seulement les quelques outils directs requis au lieu de dizaines ou de centaines de schémas d'outils complets.
- Meilleure orchestration : le modèle peut utiliser des boucles, des jointures, de petites transformations, une logique conditionnelle et des appels d'outils imbriqués parallèles dans une seule cellule de code.
- Moins de tours de modèle : un contrat de sortie déclaré permet au modèle d'appeler et de transformer un résultat d'outil en un seul `exec` ; les sorties inconnues restent brutes en premier.
- Neutre du fournisseur : fonctionne pour les outils OpenClaw, plugin, MCP et client sans dépendre de l'exécution de code natif du fournisseur.
- Échoue fermé : si code mode est activé mais que le runtime QuickJS-WASI n'est pas disponible, l'exécution échoue au lieu de revenir silencieusement à une exposition d'outils directs large.

Très utile pour les agents avec un grand catalogue d'outils activés, ou les workflows où le modèle doit rechercher, combiner et appeler plusieurs outils avant de répondre.

Conservez l'exposition d'outils directs pour un petit catalogue ou un modèle qui n'écrit pas de manière fiable de courts programmes. Utilisez [Tool Search](/fr/tools/tool-search) lorsque vous voulez un catalogue compact mais préférez les contrôles de recherche/description/appel structurés au lieu du guest QuickJS-WASI.

## Démarrage rapide

### Activer Code Mode

```json5
{
  tools: {
    codeMode: {
      enabled: true,
    },
  },
}
```

Raccourci :

```json5
{
  tools: {
    codeMode: true,
  },
}
```

Code mode reste désactivé lorsque `tools.codeMode` est omis, `false` ou un objet sans `enabled: true`.

Si vous utilisez des agents en sandbox avec des serveurs MCP configurés, autorisez également le plugin MCP fourni dans la politique d'outils en sandbox, par exemple `tools.sandbox.tools.alsoAllow: ["bundle-mcp"]`. Voir [Configuration - tools and custom providers](/fr/gateway/config-tools#mcp-and-plugin-tools-inside-sandbox-tool-policy).

Définissez des limites explicites pour des bornes plus strictes :

```json5
{
  tools: {
    codeMode: {
      enabled: true,
      timeoutMs: 10000,
      memoryLimitBytes: 67108864,
      maxOutputBytes: 65536,
      maxSnapshotBytes: 10485760,
      maxPendingToolCalls: 16,
      snapshotTtlSeconds: 900,
      searchDefaultLimit: 8,
      maxSearchLimit: 50,
    },
  },
}
```

### Ce que fait le modèle

Pour un outil avec une sortie déclarée comme `Array<{ id: string; paid: boolean; tons: number }>`, un programme guest peut le sélectionner, l'appeler et le transformer :

```javascript
const [shipmentTool] = await tools.search("list shipments");
const shipments = await tools.callValue(shipmentTool.id, {});
return shipments.filter((shipment) => !shipment.paid && shipment.tons > 10);
```

Lorsqu'une ligne d'index rapide se termine par `-> ?`, la forme de sortie est inconnue. Le premier `exec` doit retourner `await tools.callValue(...)` inchangé. Un `exec` ultérieur peut transformer la valeur observée. Cela coûte un tour de modèle supplémentaire, mais empêche le modèle de deviner les noms de champs.

### Vérifier la surface active

Pour confirmer la forme de la charge utile du modèle lors du débogage, exécutez la Gateway avec la journalisation ciblée :

```bash
OPENCLAW_DEBUG_CODE_MODE=1 \
OPENCLAW_DEBUG_MODEL_TRANSPORT=1 \
OPENCLAW_DEBUG_MODEL_PAYLOAD=tools \
openclaw gateway
```

Avec code mode actif, les noms d'outils visibles par le modèle enregistrés doivent être `exec` et `wait`. Pour la charge utile du fournisseur complète masquée, ajoutez `OPENCLAW_DEBUG_MODEL_PAYLOAD=full-redacted` pour une courte session de débogage.

## Visite technique

Le reste de cette page couvre le contrat runtime et les détails d'implémentation, pour les responsables de la maintenance, les auteurs de plugins déboguant l'exposition des outils et les opérateurs validant les déploiements à haut risque.

## Statut du runtime

|                     |                                                                                             |
| ------------------- | ------------------------------------------------------------------------------------------- |
| Runtime             | [`quickjs-wasi`](https://github.com/vercel-labs/quickjs-wasi)                               |
| État par défaut     | désactivé                                                                                   |
| Stabilité           | surface OpenClaw expérimentale (Codex Code Mode est une surface de harnais Codex stable et distincte) |
| Surface cible       | exécutions d'agent OpenClaw générique                                                      |
| Posture de sécurité | le code du modèle est hostile                                                              |
| Promesse visible par l'utilisateur | l'activation de code mode ne revient jamais silencieusement à une exposition d'outils directs large |

## Portée

Code mode possède la forme d'orchestration visible par le modèle pour une exécution préparée. Il ne possède pas la sélection du modèle, le comportement du canal, l'authentification, la politique d'outils ou les implémentations d'outils.

Dans la portée : définitions d'outils de contrôle/directs visibles par le modèle, construction de catalogue d'outils caché, exécution guest JavaScript/TypeScript, runtime worker QuickJS-WASI, callbacks d'hôte pour recherche/description/appel, état reprendre pour les programmes guest suspendus, limites de sortie/timeout/mémoire/appels en attente/snapshot et télémétrie/projection de trajectoire pour les appels d'outils imbriqués.

Hors de portée : exécution de code distant native du fournisseur, sémantique d'exécution de shell, modification de l'autorisation d'outils existante, scripts persistants créés par l'utilisateur, accès au gestionnaire de packages/fichiers/réseau/modules dans le code guest et réutilisation directe des internals de Codex Code Mode.

Les outils appartenant au fournisseur tels que les sandboxes Python distants sont des outils distincts. Voir [Code execution](/fr/tools/code-execution).

## Termes

- **Code mode** : le mode runtime OpenClaw qui cache les outils de modèle compatibles avec le catalogue et expose `exec`, `wait`, plus les outils directs requis.
- **Guest runtime** : la VM JavaScript QuickJS-WASI qui évalue le code du modèle.
- **Host bridge** : la surface de callback étroite compatible JSON du code guest vers OpenClaw.
- **Catalog** : la liste des outils effectifs scoped à l'exécution après la politique d'outils normale, la résolution de plugin, MCP et client-tool.
- **Nested tool call** : un appel d'outil effectué à partir du code guest via le host bridge.
- **Snapshot** : état VM QuickJS-WASI sérialisé sauvegardé pour que `wait` puisse continuer une exécution code-mode suspendue.

## Configuration

`tools.codeMode.enabled` est la porte d'activation ; définir d'autres champs n'active pas la fonctionnalité en soi.

| Champ                 | Par défaut                     | Limite                                          |
| --------------------- | ------------------------------ | ----------------------------------------------- |
| `enabled`             | `false`                        | booléen ; seul `true` active code mode          |
| `runtime`             | `"quickjs-wasi"`               | seule valeur prise en charge                    |
| `mode`                | `"only"`                       | expose les outils de contrôle/directs, catalogue le reste |
| `languages`           | `["javascript", "typescript"]` | tout sous-ensemble des deux                     |
| `timeoutMs`           | `10000`                        | `100`-`60000`                                   |
| `memoryLimitBytes`    | `67108864`                     | `1048576`-`1073741824`                          |
| `maxOutputBytes`      | `65536`                        | `1024`-`10485760`                               |
| `maxSnapshotBytes`    | `10485760`                     | `1024`-`268435456`                              |
| `maxPendingToolCalls` | `16`                           | `1`-`128`                                       |
| `snapshotTtlSeconds`  | `900`                          | `1`-`86400`                                     |
| `searchDefaultLimit`  | `8`                            | limité à `maxSearchLimit`                       |
| `maxSearchLimit`      | `50`                           | `1`-`50`                                        |

Si code mode est activé mais que QuickJS-WASI ne peut pas se charger, OpenClaw échoue fermé pour cette exécution ; il n'expose pas silencieusement les outils normaux comme recours.

## Activation

Le mode code est évalué après que la politique d'outil effective soit connue et avant que la demande finale du modèle soit assemblée :

1. Résoudre l'agent, le modèle, le fournisseur, le sandbox, le canal, l'expéditeur et la politique d'exécution.
2. Construire la liste effective des outils OpenClaw, en ajoutant les outils de plugin, MCP et client éligibles.
3. Appliquer la politique d'autorisation/refus.
4. Si `tools.codeMode.enabled` est false, continuer avec l'exposition normale des outils.
5. Si activé et que des outils sont actifs pour l'exécution, conserver les outils directs requis et enregistrer tous les outils effectifs éligibles du catalogue dans le catalogue du mode code.
6. Supprimer les outils catalogués de la liste visible du modèle ; ajouter `exec` et `wait` aux côtés des outils directs conservés.

Les exécutions qui n'ont intentionnellement aucun outil (appels de modèle bruts, `disableTools: true`, ou une liste `tools.allow` vide) n'activent pas la surface du mode code même lorsque `tools.codeMode.enabled: true` est configuré. Le mode code et la recherche d'outils OpenClaw s'excluent mutuellement pour une exécution ; si le mode code s'active, la compaction de la recherche d'outils ne se fait pas.

Le catalogue du mode code est limité à l'exécution et ne doit pas divulguer les outils d'un autre agent, session, expéditeur ou exécution.

## Outils visibles du modèle

Lorsque le mode code est actif, le modèle voit `exec`, `wait` et tout outil direct requis. Tous les autres outils activés sont masqués de la liste des outils visible au modèle et enregistrés dans le catalogue du mode code.

Utilisez `exec` pour l'orchestration des outils, la jointure de données, les boucles, les appels imbriqués parallèles et les transformations structurées. Utilisez `wait` uniquement lorsque `exec` retourne un résultat `waiting` reprendre.

## `exec`

`exec` démarre une cellule du mode code et retourne un résultat. Le code d'entrée est généré par le modèle et doit être traité comme hostile.

Entrée :

```typescript
type CodeModeExecInput = {
  code?: string;
  command?: string;
  language?: "javascript" | "typescript";
};
```

Règles :

- L'un de `code` ou `command` doit être non vide.
- `code` est le champ visible au modèle documenté.
- `command` est accepté comme alias compatible avec exec pour les politiques de hook et les réécritures de confiance (l'outil shell exec OpenClaw normal utilise également un champ `command`) ; lorsque les deux sont présents, les valeurs doivent correspondre.
- `language` par défaut à `"javascript"` ; le schéma l'expose comme une énumération de chaîne plate (`"javascript" | "typescript"`), pas une union `oneOf`/`anyOf`, car certains fournisseurs rejettent ces formes.
- Si `language` est `"typescript"`, OpenClaw transpile avant l'évaluation.
- `exec` rejette `import`, `require`, l'importation dynamique et les modèles de chargeur de module.
- `exec` n'expose jamais l'implémentation shell `exec` normale de manière récursive.
- Les événements de hook `exec` du mode code externe portent `toolKind: "code_mode_exec"` et `toolInputKind: "javascript" | "typescript"` (lorsqu'ils sont connus), afin que les politiques puissent distinguer les cellules du mode code des appels `exec` de style shell qui partagent le même nom d'outil.

Résultat :

```typescript
type CodeModeResult = CodeModeCompletedResult | CodeModeWaitingResult | CodeModeFailedResult;

type CodeModeCompletedResult = {
  status: "completed";
  value: unknown;
  output?: CodeModeOutput[];
  telemetry: CodeModeTelemetry;
};

type CodeModeWaitingResult = {
  status: "waiting";
  runId: string;
  reason: "pending_tools" | "yield";
  pendingToolCalls?: CodeModePendingToolCall[];
  output?: CodeModeOutput[];
  telemetry: CodeModeTelemetry;
};

type CodeModeFailedResult = {
  status: "failed";
  error: string;
  code?: CodeModeErrorCode;
  output?: CodeModeOutput[];
  telemetry: CodeModeTelemetry;
};
```

`exec` retourne `waiting` lorsque l'invité se suspend avec un état reprendre qui a encore besoin d'une continuation visible du modèle — un `yield_control(...)` explicite, ou un appel d'outil bridge qui n'a pas été résolu avant la date limite d'exec. Le résultat inclut un `runId` pour `wait`. Les appels d'outils bridge — `tools.search`/`describe`/`call` et les appels d'espace de noms, y compris les appels d'espace de noms MCP — sont auto-vidés dans le même appel `exec`/`wait` tandis qu'ils se résolvent avant la date limite, afin qu'un bloc de code compact qui attend plusieurs outils s'exécute jusqu'à la fin en un seul tour de modèle au lieu de forcer un appel d'outil de modèle par await. Les exécutions sûres pour le redémarrage ne s'auto-vident jamais ; leur travail en attente passe toujours par les vérifications sûres pour la relecture.

`exec` retourne `completed` uniquement lorsque la VM invitée n'a aucun travail en attente et que la valeur finale est compatible JSON après l'exécution de l'adaptateur de sortie d'OpenClaw.

## `wait`

`wait` continue une VM du mode code suspendue.

Entrée :

```typescript
type CodeModeWaitInput = {
  runId: string;
};
```

La sortie est la même union `CodeModeResult` retournée par `exec`.

`wait` existe parce que les outils OpenClaw imbriqués peuvent être lents, interactifs, contrôlés par approbation ou diffuser des mises à jour partielles ; le modèle ne devrait pas avoir besoin de garder un long appel `exec` ouvert pendant que l'hôte attend un travail externe.

La capture/restauration de snapshot QuickJS-WASI est le mécanisme de reprise :

1. `exec` évalue le code jusqu'à la fin, l'échec ou la suspension.
2. En cas de suspension, OpenClaw capture un snapshot de la VM QuickJS et enregistre le travail d'hôte en attente.
3. Lorsque le travail en attente se règle, `wait` restaure le snapshot de la VM et réenregistre les rappels d'hôte par des noms stables.
4. OpenClaw livre les résultats des outils imbriqués dans la VM restaurée et vide les travaux en attente de QuickJS.
5. `wait` retourne `completed`, `failed` ou un autre résultat `waiting`.

Les snapshots sont l'état d'exécution, pas des artefacts utilisateur : ils vivent uniquement dans une carte en mémoire (pas d'écriture en base de données ou sur disque), sont limités en taille, expirent et sont limités à l'exécution et à la session qui les ont créés.

`wait` échoue (en tant que résultat `failed`) lorsque :

- `runId` est inconnu ou son snapshot a déjà expiré.
- l'appelant n'est pas dans la même portée d'exécution/session que l'exécution suspendue.
- un `wait` est déjà en cours pour ce `runId`.
- la restauration QuickJS-WASI échoue.
- la reprise dépasserait `maxOutputBytes` ou `maxSnapshotBytes`.

## API du runtime invité

```typescript
declare const ALL_TOOLS: ToolCatalogEntry[];
declare const tools: ToolCatalog;
declare const MCP: Record<string, unknown>;
declare const namespaces: Record<string, unknown>;

declare function text(value: unknown): void;
declare function json(value: unknown): void;
declare function yield_control(reason?: string): Promise<void>;
```

`ALL_TOOLS` est des métadonnées compactes pour le catalogue limité à l'exécution ; il ne contient pas de schémas complets par défaut. La description `exec` visible au modèle inclut également un sous-ensemble borné et déterministe d'identifiants OpenClaw/plugin exacts, d'indices d'entrée compacts et d'indices de sortie déclarés de confiance. Les descriptions restent différées afin que la prose de catalogue malveillante ne puisse pas orienter le modèle. Lorsque cet index omet un outil, lisez `ALL_TOOLS` ou appelez `tools.search(...)` à l'intérieur du programme invité.

La flèche dans chaque ligne d'index rapide décrit la valeur `tools.callValue(...)`. `-> Array<{ id: string }>` est un indice de sortie déclaré ; `-> ?` est une sortie inconnue. Les sorties inconnues restent brutes en premier : retournez la valeur inchangée, observez-la, puis filtrez ou mappez-la dans un `exec` ultérieur au lieu de deviner les noms de champs.

```typescript
type ToolCatalogEntry = {
  id: string;
  name: string;
  label?: string;
  description: string;
  source: "openclaw" | "mcp" | "client";
  sourceName?: string;
  input: string;
  output?: string;
};
```

`input` est une signature de style TypeScript bornée pour le cas courant. Utilisez `tools.describe(...)` lorsque le schéma complet exact est toujours nécessaire. Les entrées MCP et client distantes utilisent `input: "unknown"` afin que leurs schémas non fiables restent différés jusqu'à `describe`. `output` est présent uniquement pour un indice compact complet dérivé d'un `outputSchema` OpenClaw core ou plugin de confiance. Les revendications de schéma de sortie MCP et client ne sont pas promues dans cet indice de catalogue de confiance.

Les outils de plugin utilisent `source: "openclaw"` avec `sourceName` défini sur l'identifiant du plugin propriétaire ; il n'y a pas de valeur `"plugin"` source distincte. `source: "mcp"` est utilisé uniquement pour les entrées MCP dans les métadonnées `sourceName`/`mcp` (et est filtré de `ALL_TOOLS`/`tools.*`, voir ci-dessous).

Le schéma complet est chargé uniquement à la demande :

```typescript
type ToolCatalogEntryWithSchema = ToolCatalogEntry & {
  parameters: unknown;
  outputSchema?: unknown;
};
```

Assistants du catalogue :

```typescript
type ToolCatalog = {
  search(query: string, options?: { limit?: number }): Promise<ToolCatalogEntry[]>;
  describe(id: string): Promise<ToolCatalogEntryWithSchema>;
  callValue(id: string, input?: unknown): Promise<unknown>;
  call(id: string, input?: unknown): Promise<unknown>;
  [safeToolName: string]: unknown;
};
```

Les fonctions d'outil de commodité sont installées uniquement pour les noms sûrs sans ambiguïté :

```typescript
const files = await tools.search("read local file");
const fileRead = await tools.describe(files[0].id);
const content = await tools.callValue(fileRead.id, { path: "README.md" });

// If the hidden catalog has an unambiguous `web_search` entry:
const hits = await tools.web_search({ query: "OpenClaw code mode" });
```

`tools.callValue(...)` retourne directement la valeur `details` JSON d'un outil normal. `tools.call(...)` préserve l'enveloppe brute `{ tool, result }` pour les appelants qui ont besoin de blocs de contenu ou d'autres métadonnées de résultat.

## Contrats de sortie déclarés

Les outils OpenClaw peuvent déclarer `outputSchema` pour la valeur structurée placée dans
`AgentToolResult.details`. Ceci est utile pour le Mode Code et la Recherche d'Outils ; ce n'est pas
un schéma de réponse d'outil natif du fournisseur et ne change pas l'exposition directe des outils.

Pour un outil créé avec `defineToolPlugin`, déclarez le schéma à côté de
`parameters` :

```typescript
import { Type } from "typebox";
import { defineToolPlugin } from "openclaw/plugin-sdk/tool-plugin";

const Shipment = Type.Object(
  {
    id: Type.String(),
    paid: Type.Boolean(),
    tons: Type.Number(),
  },
  { additionalProperties: false },
);

export default defineToolPlugin({
  id: "shipping",
  name: "Shipping",
  description: "Shipment tools.",
  tools: (tool) => [
    tool({
      name: "shipping_list",
      description: "List shipments.",
      parameters: Type.Object({}),
      outputSchema: Type.Array(Shipment),
      execute: async () => loadShipments(),
    }),
  ],
});
```

Pour `api.registerTool(...)` ou un outil factory, mettez la même propriété `outputSchema`
sur l'objet `AnyAgentTool` retourné.

Les règles du contrat sont strictes :

- Décrivez la valeur `details` exacte compatible JSON, pas les blocs `content` rendus
  ou une enveloppe de fournisseur.
- Incluez chaque variante de succès ou d'erreur sans lancer d'exception. Omettez `outputSchema` quand
  l'outil n'a pas de résultat structuré stable.
- Fermez les couches d'objets avec `{ additionalProperties: false }` pour un indice d'indexation rapide complet. Les schémas
  ouverts, surdimensionnés ou partiels restent
  disponibles via `tools.describe(...)` mais ne permettent pas l'utilisation de champs en un seul tour.
- OpenClaw compile le schéma avant d'exécuter l'outil, puis valide le `details` final
  après les hooks d'outil normaux et avant qu'un appel de catalogue ne retourne. Un
  schéma invalide ne peut pas exécuter l'outil ; une non-correspondance échoue sans imprimer la
  valeur.
- Les indices compacts sont déterministes et bornés. `tools.describe(...)` expose
  le schéma complet de confiance quand l'indice compact est insuffisant.
- Le code du plugin installé est déjà du code local de confiance. Le MCP distant et les
  métadonnées du client restent non fiables et ne peuvent pas opter pour ces indices d'indexation rapide.

Voir [Plugins d'outils](/fr/plugins/tool-plugins#output-contracts) pour les détails de création de plugins.

Les entrées du catalogue MCP ne sont pas appelables via `tools.callValue(...)`,
`tools.call(...)`, ou les fonctions de commodité en mode code ; elles sont exposées
uniquement via l'espace de noms `MCP` généré. Les fichiers de déclaration de style TypeScript
sont disponibles via la surface de fichier virtuel en lecture seule `API`, afin que les agents puissent
inspecter les signatures MCP sans ajouter les schémas MCP à l'invite :

```typescript
const files = await API.list("mcp");
const githubApi = await API.read("mcp/github.d.ts");

const issue = await MCP.github.createIssue({
  owner: "openclaw",
  repo: "openclaw",
  title: "Investigate gateway logs",
});

const snapshot = await MCP.chromeDevtools.takeSnapshot({ output: "markdown" });
const resource = await MCP.docs.resources.read({ uri: "memo://one" });
const prompt = await MCP.docs.prompts.get({
  name: "brief",
  arguments: { topic: "release" },
});
```

`API.read("mcp/<server>.d.ts")` retourne des déclarations compactes déduites des
métadonnées d'outil MCP :

```typescript
type McpToolResult = {
  content?: unknown[];
  structuredContent?: unknown;
  isError?: boolean;
  [key: string]: unknown;
};

declare namespace MCP.github {
  /** Return this TypeScript-style API header. */
  function $api(toolName?: string, options?: { schema?: boolean }): Promise<McpApiHeader>;

  /**
   * Create a GitHub issue.
   * @param owner Repository owner
   * @param repo Repository name
   * @param title Issue title
   */
  function createIssue(input: {
    owner: string;
    repo: string;
    title: string;
    body?: string;
  }): Promise<McpToolResult>;
}
```

Les fichiers de déclaration sont virtuels, non écrits sous le répertoire de l'espace de travail ou d'état.
Pour chaque appel `exec` en mode code, OpenClaw construit le catalogue d'outils limité à l'exécution,
conserve les entrées MCP visibles, rend `mcp/index.d.ts` plus un
`mcp/<server>.d.ts` par serveur visible, et injecte cette petite table en lecture seule
dans le worker QuickJS. Le code invité voit uniquement l'objet `API` :
`API.list(prefix?)` retourne les métadonnées de fichier et `API.read(path)` retourne le
contenu de déclaration sélectionné. Les chemins inconnus et les segments `.`/`..` sont
rejetés.

Cela garde les grands schémas MCP hors de l'invite du modèle : l'agent apprend que l'API
virtuelle existe à partir de la description de l'outil `exec`, lit uniquement le fichier de déclaration nécessaire,
puis appelle `MCP.<server>.<tool>()` avec un argument objet unique.
`MCP.<server>.$api()` reste disponible comme solution de secours en ligne pour une
réponse de schéma d'outil unique à l'intérieur du programme.

Le runtime invité ne voit jamais les objets hôte directement. Les entrées et sorties traversent
le pont en tant que valeurs compatibles JSON avec des limites de taille explicites.

## Espaces de noms internes

Les espaces de noms internes donnent au mode code une API de domaine concise sans ajouter plus d'outils visibles par le modèle. Une intégration détenue par un chargeur enregistre un espace de noms tel que `Issues` ou `Calendar` ; le code invité appelle ensuite cet espace de noms à l'intérieur du programme QuickJS tandis que le modèle voit toujours la surface de contrôle/direct compacte.

Les espaces de noms sont internes pour l'instant. Il n'y a pas d'API d'espace de noms SDK public :
les espaces de noms de plugins externes ont besoin d'un contrat détenu par le chargeur afin que l'identité du plugin, les manifestes installés, l'état d'authentification et les descripteurs de catalogue en cache ne dérivent pas des outils de plugin qui soutiennent l'espace de noms. Le mode code principal ne possède que le bac à sable, la sérialisation, le contrôle du catalogue et la distribution de pont.

Le code invité peut utiliser soit le global direct, soit la carte `namespaces` :

```javascript
const open = await Issues.list({ state: "open" });
const alsoOpen = await namespaces.Issues.list({ state: "open" });
return { count: open.length, alsoCount: alsoOpen.length };
```

### Cycle de vie du registre

Le registre d'espace de noms est local au processus et indexé par l'ID d'espace de noms :

1. Un chargeur de confiance appelle `registerCodeModeNamespaceForPlugin(pluginId, registration)`.
2. Le mode code crée le `ToolSearchRuntime` caché pour l'exécution et lit son catalogue limité à l'exécution.
3. `createCodeModeNamespaceRuntime(ctx, catalog)` conserve uniquement les enregistrements dont tous les `requiredToolNames` sont visibles et appartiennent au même `pluginId`.
4. Chaque espace de noms visible appelle `createScope(ctx)` pour l'exécution actuelle, recevant le contexte d'exécution tel que `agentId`, `sessionKey`, `sessionId`, `runId`, la configuration et l'état d'abandon.
5. Les données de portée sont sérialisées dans un descripteur simple et injectées dans QuickJS en tant que globals directs et `namespaces.<globalName>`.
6. Les appels invités suspendent via le pont de travail, résolvent le chemin d'espace de noms sur l'hôte, mappent l'appel à un outil de catalogue détenu par un plugin déclaré et exécutent cet outil via `ToolSearchRuntime.callExactId`.
7. Les appels de pont d'espace de noms prêts sont automatiquement vidés à l'intérieur de l'appel `exec`/`wait` actif ; si le travail d'espace de noms est toujours en attente au délai d'expiration ou si l'invité cède explicitement, `wait` reprend le même runtime d'espace de noms plus tard.
8. L'annulation du plugin ou la désinstallation appelle `clearCodeModeNamespacesForPlugin(pluginId)` afin que les globals obsolètes ne survivent pas à un chargement de plugin échoué.

Les appels d'espace de noms sont des appels d'outil de catalogue : ils utilisent les mêmes crochets de politique, approbations, gestion d'abandon, télémétrie, projection de transcription et comportement de suspension/reprise que `tools.call(...)`.

### Forme d'enregistrement

Enregistrez les espaces de noms à partir de l'intégration qui possède les outils de support. Gardez la portée petite et exposez uniquement les verbes de domaine qui correspondent aux outils de catalogue déclarés.

```typescript
import {
  createCodeModeNamespaceTool,
  registerCodeModeNamespaceForPlugin,
} from "../agents/code-mode-namespaces.js";

const pluginId = "github";

registerCodeModeNamespaceForPlugin(pluginId, {
  id: "github-issues",
  globalName: "Issues",
  description: "GitHub issue helpers for the current repository.",
  requiredToolNames: ["github_list_issues", "github_update_issue"],
  prompt: "Use Issues.list(params) and Issues.update(number, patch).",
  createScope: (ctx) => ({
    repository: ctx.config,
    list: createCodeModeNamespaceTool("github_list_issues", ([params]) => params ?? {}),
    update: createCodeModeNamespaceTool("github_update_issue", ([number, patch]) => ({
      number,
      patch,
    })),
  }),
});
```

`createCodeModeNamespaceTool(toolName, inputMapper)` marque un membre de portée comme une fonction d'espace de noms appelable. Le `inputMapper` optionnel reçoit les arguments invités et retourne l'objet d'entrée pour l'outil de catalogue de support ; sans lui, le premier argument invité est utilisé, ou `{}` lorsqu'il est omis.

Les fonctions d'hôte brutes sont rejetées avant l'exécution du code invité :

```typescript
createScope: () => ({
  // Wrong: this bypasses the catalog tool lifecycle and will be rejected.
  list: async () => githubClient.listIssues(),
});
```

### Propriété et visibilité

La propriété d'espace de noms est liée au `pluginId` de l'appelant d'enregistrement.
`requiredToolNames` est à la fois une porte de visibilité et une vérification de propriété :

- chaque outil requis doit exister dans le catalogue d'exécution
- chaque outil requis doit avoir `sourceName === pluginId`
- l'espace de noms est caché lorsqu'un outil requis est absent ou appartient à un autre plugin
- chaque chemin appelable ne peut cibler que un outil nommé dans `requiredToolNames`

Cela empêche un autre plugin d'exposer un espace de noms en enregistrant un outil de même nom, et maintient les espaces de noms alignés avec la politique d'agent ordinaire : si l'exécution ne peut pas voir les outils de support, elle ne peut pas voir l'espace de noms.

Par exemple, un espace de noms GitHub devrait vivre derrière un plugin détenu par GitHub qui possède l'authentification GitHub, les clients REST/GraphQL, les limites de débit, les approbations d'écriture et les tests. Le mode code principal ne devrait pas intégrer les API spécifiques à GitHub, la gestion des jetons ou la politique du fournisseur.

### Règles de sérialisation de portée

`createScope(ctx)` peut retourner un objet simple contenant des valeurs compatibles JSON, des tableaux, des objets imbriqués et des marqueurs d'appel `createCodeModeNamespaceTool(...)`. Les objets hôtes n'entrent jamais directement dans QuickJS.

Le sérialiseur rejette :

- les fonctions brutes
- les graphes d'objets circulaires
- les segments de chemin non sûrs : `__proto__`, `constructor`, `prototype`, les clés vides ou les clés contenant le séparateur de chemin interne
- les valeurs `globalName` qui ne sont pas des identifiants JavaScript
- les collisions `globalName` avec les globals de mode code intégrés tels que `tools`, `namespaces`, `text`, `json`, `yield_control`, `MCP`, `API`, `ALL_TOOLS` ou `__openclaw*`

Les valeurs qui ne peuvent pas être sérialisées en JSON sont converties en valeurs de secours sûres pour JSON avant de traverser le pont. Les données binaires, les poignées, les sockets, les clients et les instances de classe doivent rester derrière les outils de catalogue ordinaires.

### Invites

La `description` d'espace de noms et l'`prompt` optionnel sont ajoutés au schéma `exec` visible par le modèle uniquement lorsque l'espace de noms est visible pour cette exécution. Utilisez-les pour enseigner la plus petite surface utile :

```typescript
{
  description: "Fiction production service helpers.",
  prompt:
    "Use Fictions.riskAudit(), Fictions.promoteIfReady(id, status), and Fictions.unpaidOver(amount).",
}
```

Gardez les invites sur le contrat d'espace de noms, pas sur la configuration d'authentification, l'historique d'implémentation ou le comportement de plugin non lié.

### Nettoyage

Les espaces de noms sont des enregistrements locaux au processus. Supprimez-les lorsque le plugin propriétaire est désactivé, désinstallé ou annulé :

```typescript
clearCodeModeNamespacesForPlugin(pluginId);
```

Le nettoyage du mode code est détenu par le plugin ; effacez les enregistrements d'espace de noms du plugin lorsque son cycle de vie se termine au lieu de conserver des poignées de démontage par espace de noms. Les tests peuvent appeler `clearCodeModeNamespacesForTest()` pour éviter les fuites d'enregistrements entre les cas.

### Liste de contrôle de test

Les modifications d'espace de noms doivent couvrir la limite de sécurité et le comportement invité :

- le texte d'invite d'espace de noms n'apparaît que lorsque les outils de support sont visibles
- les outils de même nom d'un autre `sourceName` n'exposent pas l'espace de noms
- les fonctions de portée brutes sont rejetées
- les ID d'espace de noms forgés et les chemins forgés sont rejetés
- les chemins appelables ne peuvent pas cibler les outils non déclarés
- les objets imbriqués et les références partagées se sérialisent correctement
- les appels d'espace de noms s'exécutent via les outils de catalogue et retournent les détails sûrs pour JSON
- les défaillances peuvent être capturées par le code invité
- les appels d'espace de noms suspendus reprennent via `wait`
- l'annulation du plugin efface les enregistrements d'espace de noms propriétaires

Les espaces de noms complètent le catalogue générique `tools.search`/`tools.call` : utilisez le catalogue pour les outils OpenClaw, plugin et client arbitraires activés ; utilisez `MCP` pour les outils MCP ; utilisez d'autres espaces de noms pour les API de domaine détenues par le plugin, documentées, où le code concis est plus fiable que les recherches de schéma répétées.

## API de sortie

- `text(value)` ajoute une sortie lisible par l'homme au tableau `output`.
- `json(value)` ajoute un élément de sortie structuré après sérialisation compatible JSON.
- La valeur retournée finale du code invité devient `value` dans un résultat `completed`.

```typescript
type CodeModeOutput = { type: "text"; text: string } | { type: "json"; value: unknown };
```

Règles : l'ordre de sortie correspond aux appels invités ; la sortie est limitée par `maxOutputBytes` ; les valeurs non sérialisables sont converties en chaînes simples ou erreurs ; les valeurs binaires ne sont pas prises en charge. Les images et les fichiers se déplacent via les outils OpenClaw ordinaires, pas via le pont du mode code.

## Catalogue d'outils

Le catalogue caché inclut les outils après le filtrage de politique effectif, dans cet ordre : outils principaux OpenClaw, outils de plugin groupés, outils de plugin externes, outils MCP, puis outils fournis par le client pour l'exécution actuelle.

Les ID de catalogue sont stables dans une exécution et déterministes entre les ensembles d'outils équivalents si possible. Forme réelle :

```text
<source>:<owner>:<tool-name>
```

où `<source>` est `openclaw`, `mcp` ou `client` (les outils de plugin utilisent `openclaw` avec l'ID de plugin comme `<owner>` ; les outils principaux utilisent `openclaw:core:*`). Exemples :

```text
openclaw:core:message
openclaw:browser:browser_request
mcp:github:create_issue
client:app:select_file
```

Le catalogue omet les outils de contrôle du mode code (`exec`, `wait`, `tool_search_code`, `tool_search`, `tool_describe`, `tool_call`) et les outils directs uniquement. Les contrôles ne doivent pas se récurser via le catalogue ; les outils directs uniquement restent visibles par le modèle car leurs résultats structurés ne peuvent pas traverser le pont QuickJS.

Les entrées MCP restent dans le catalogue limité à l'exécution afin que la politique, les approbations, les crochets, la télémétrie, la projection de transcription et les ID d'outils exacts restent partagés avec l'exécution d'outil normale. Les vues `ALL_TOOLS`, `tools.search(...)`, `tools.describe(...)`, `tools.callValue(...)` et `tools.call(...)` visibles par l'invité omettent les entrées MCP. L'espace de noms `MCP.<server>.<tool>({ ...input })` généré se résout à l'ID de catalogue exact et se distribue via le même chemin d'exécuteur.

## Interaction de recherche d'outils

Le mode code remplace la surface du modèle OpenClaw Tool Search pour les exécutions où il est actif.

Lorsque `tools.codeMode.enabled` est vrai et que le mode code s'active :

- OpenClaw n'expose pas `tool_search_code`, `tool_search`, `tool_describe` ou `tool_call` en tant qu'outils visibles par le modèle.
- La même idée de catalogage se déplace à l'intérieur du runtime invité.
- Le runtime invité reçoit les métadonnées compactes `ALL_TOOLS` et les assistants de recherche/description/appel pour les outils non-MCP.
- Les appels MCP utilisent l'espace de noms `MCP` généré et ses en-têtes `$api()` au lieu de `tools.call(...)`.
- Les appels imbriqués se distribuent via le même chemin d'exécuteur OpenClaw que Tool Search utilise.

Voir [Tool Search](/fr/tools/tool-search) pour le pont de catalogue compact OpenClaw que le mode code remplace pour les exécutions actives.

## Noms d'outils et collisions

L'outil `exec` visible par le modèle est l'outil du mode code. Si l'outil shell `exec` OpenClaw normal est activé, il est caché du modèle et catalogué comme n'importe quel autre outil.

À l'intérieur du runtime invité :

- `tools.call("openclaw:core:exec", input)` peut appeler l'outil shell exec si la politique le permet.
- `tools.exec(...)` est installé uniquement si l'entrée du catalogue shell exec a un nom sûr et sans ambiguïté.
- l'outil `exec` du mode code n'est jamais récursivement disponible via `tools`.

Si deux outils se normalisent au même nom de commodité sûr, OpenClaw omet la fonction de commodité et nécessite `tools.call(id, input)`.

## Exécution d'outil imbriquée

Chaque appel d'outil imbriqué traverse le pont d'hôte et rentre dans OpenClaw, préservant : l'ID d'agent actif, l'ID et la clé de session, le contexte d'expéditeur et de canal, la politique de bac à sable, la politique d'approbation, les crochets `before_tool_call` du plugin, le signal d'abandon, les mises à jour en continu si disponibles et les événements de trajectoire/audit.

Les appels imbriqués se projettent dans la transcription en tant qu'appels d'outils réels afin que les bundles de support montrent ce qui s'est passé, la projection identifiant l'appel d'outil du mode code parent et l'ID d'outil imbriqué.

Les appels d'outils imbriqués parallèles sont autorisés jusqu'à `maxPendingToolCalls`.

## Cycle de vie des exécutions et snapshots

Chaque exécution en mode code est suivie dans une carte en mémoire indexée par `runId` (non persistée sur disque ou base de données). `exec`/`wait` retournent l'un des trois statuts de résultat : `completed`, `waiting`, ou `failed`.

- Un résultat `waiting` stocke le snapshot QuickJS, les demandes de bridge en attente, et les métadonnées de portée (id d'exécution d'agent, id/clé de session) jusqu'à ce que `wait` le reprenne ou qu'il expire.
- L'expiration, la mauvaise session, la mauvaise exécution, et les valeurs `runId` inconnues/déjà en cours de reprise ne produisent pas de statut terminal distinct ; elles apparaissent comme un résultat `failed` (`code: "invalid_input"`) avec un message tel que `code mode run is unavailable or expired.` ou `code mode run belongs to a different session.`.
- Le snapshot d'une exécution est supprimé de la carte dès qu'il se termine en `completed` ou `failed`, ou est supprimé à l'arrêt de la Gateway (rien ne survit à un redémarrage : c'est un état d'exécution transitoire).
- Pour les travaux en lecture seule, `exec` peut définir `restartSafe: true`. OpenClaw rejette alors les appels de catalogue avec effets secondaires et les espaces de noms de plugin avant l'exécution et marque les résultats suspendus comme sûrs pour la relecture. Si un redémarrage interrompt `wait`, la [récupération au redémarrage](/fr/gateway/restart-recovery) reconstruit le tour à partir de la transcription au lieu de restaurer le snapshot local au processus. Le tour de récupération lui-même reste limité aux outils principaux audités en lecture seule et aux outils de plugin explicitement sûrs pour la relecture.
- OpenClaw limite le nombre d'exécutions suspendues concurrentes par processus (64) et rejette les nouvelles suspensions au-delà de cette limite avec `too many suspended code mode runs.`.

Le stockage des snapshots est limité par `maxSnapshotBytes` par exécution, la limite d'exécutions suspendues par processus ci-dessus, et `snapshotTtlSeconds`.

## Runtime QuickJS-WASI

OpenClaw charge `quickjs-wasi` comme dépendance directe dans le paquet propriétaire ; il ne s'appuie pas sur une copie transitive installée pour une dépendance non liée.

Responsabilités du runtime : compiler/charger le module WebAssembly QuickJS-WASI ; créer une VM isolée par exécution en mode code ou reprise ; enregistrer les callbacks hôte par noms stables ; définir les limites de mémoire et d'interruption ; évaluer JavaScript ; vider les tâches en attente ; créer un snapshot de l'état de la VM suspendue ; restaurer les snapshots pour `wait` ; libérer les handles de VM et les snapshots après les états terminaux.

Le runtime s'exécute dans un thread worker Node.js, en dehors de la boucle d'événements principale d'OpenClaw. Une boucle infinie invitée ne doit pas bloquer indéfiniment le processus Gateway ; le gestionnaire d'interruption du worker applique le délai d'expiration en temps réel indépendamment du code invité coopérant.

## TypeScript

Le support de TypeScript est une transformation de source uniquement : l'entrée acceptée est une chaîne de code TypeScript ; la sortie est une chaîne JavaScript évaluée par QuickJS-WASI. Il n'y a pas de vérification de type, pas de résolution de module, et pas de `import`/`require`. Les diagnostics sont retournés comme des résultats `failed`.

Le compilateur TypeScript est chargé paresseusement uniquement pour les cellules TypeScript ; les cellules JavaScript simples et le mode code désactivé ne le chargent jamais.

## Limite de sécurité

Le code du modèle est hostile. Le runtime utilise la défense en profondeur :

- exécute QuickJS-WASI en dehors de la boucle d'événements principale, dans un thread worker
- charge `quickjs-wasi` comme dépendance directe, pas via Codex ou un paquet transitif
- pas de système de fichiers, réseau, sous-processus, importation de module, variables d'environnement, ou objets globaux hôte dans l'invité
- utilise les limites de mémoire et d'interruption QuickJS plus un délai d'expiration en temps réel du processus parent
- applique les limites de sortie, snapshot, journal et appels en attente
- sérialise les valeurs de bridge hôte via un adaptateur JSON étroit
- convertit les erreurs hôte en erreurs invitées simples, jamais des objets du domaine hôte
- supprime les snapshots en cas de délai d'expiration, abandon, fin de session ou expiration
- rejette l'accès récursif à `exec`, `wait`, et les outils de contrôle Tool Search
- empêche les collisions de noms de commodité d'ombrager les assistants de catalogue

Le sandbox est une couche de sécurité ; les opérateurs peuvent toujours avoir besoin de renforcement au niveau du système d'exploitation pour les déploiements à haut risque.

## Codes d'erreur

```typescript
type CodeModeErrorCode =
  | "invalid_input"
  | "runtime_unavailable"
  | "timeout"
  | "output_limit_exceeded"
  | "snapshot_limit_exceeded"
  | "internal_error";
```

`invalid_input` couvre les mauvais arguments `exec`/`wait`, les langages désactivés, l'accès au module rejeté, les échecs de transformation TypeScript, les valeurs `runId` inconnues/expirées/de mauvaise portée, et trop d'exécutions suspendues. `runtime_unavailable` couvre un worker QuickJS qui échoue au démarrage ou se termine avec un code non nul.

Les erreurs retournées à l'invité sont des données simples ; les instances `Error` hôte, les objets de pile, les prototypes, et les fonctions hôte ne traversent pas dans QuickJS.

## Télémétrie

Le champ `telemetry` de chaque résultat rapporte : la taille du catalogue caché et une ventilation des sources (comptages `openclaw`/`mcp`/`client`), les comptages cumulatifs de recherche/description/appel pour le catalogue de l'exécution, et les noms d'outils visibles par le modèle (`exec`, `wait`, et outils directs retenus).

La télémétrie ne doit pas inclure de secrets, de valeurs d'environnement brutes, ou d'entrées d'outils non rédactées au-delà de la politique de trajectoire OpenClaw existante.

## Débogage

Utilisez la journalisation ciblée du transport du modèle lorsque le mode code se comporte différemment d'une exécution d'outil normale :

```bash
OPENCLAW_DEBUG_CODE_MODE=1 \
OPENCLAW_DEBUG_MODEL_TRANSPORT=1 \
OPENCLAW_DEBUG_MODEL_PAYLOAD=tools \
OPENCLAW_DEBUG_SSE=events \
openclaw gateway
```

Pour le débogage de la forme de la charge utile, utilisez `OPENCLAW_DEBUG_MODEL_PAYLOAD=full-redacted`. Cela enregistre un snapshot JSON réduit et limité de la demande du modèle ; utilisez-le uniquement lors du débogage, car les invites et le texte du message peuvent toujours apparaître.

Pour le débogage du flux, utilisez `OPENCLAW_DEBUG_SSE=peek` pour enregistrer les cinq premiers événements SSE rédactés. Le mode code échoue également de manière fermée si la charge utile du fournisseur final ne contient pas exactement un `exec`, un `wait`, et uniquement les outils directs approuvés après l'activation de la surface du mode code.

## Disposition de l'implémentation

- contrat de configuration : `tools.codeMode`
- constructeur de catalogue : outils effectifs pour les entrées compactes et la carte d'id
- adaptateur de surface de modèle : remplacer les outils visibles par les outils de contrôle/directs
- adaptateur de runtime QuickJS-WASI : charger, évaluer, créer un snapshot, restaurer, libérer
- superviseur de worker : délai d'expiration, abandon, isolation des plantages
- adaptateur de bridge : callbacks hôte sûrs pour JSON et livraison de résultats
- adaptateur de transformation TypeScript
- magasin de snapshots : TTL, limites de taille, portée d'exécution/session
- projection de trajectoire pour les appels d'outils imbriqués
- compteurs de télémétrie et diagnostics

L'implémentation réutilise les concepts de catalogue et d'exécuteur de Tool Search, mais n'utilise pas un enfant `node:vm` comme sandbox.

## Liste de contrôle de validation

La couverture du mode code doit prouver :

- la configuration désactivée laisse l'exposition d'outils existante inchangée
- la configuration d'objet sans `enabled: true` laisse le mode code désactivé
- la configuration activée expose `exec`, `wait`, et uniquement les outils directs requis au modèle lorsque les outils sont actifs pour l'exécution
- les exécutions sans outil brutes, `disableTools`, et les listes d'autorisation vides ne déclenchent pas l'application de charge utile du mode code
- tous les outils effectifs non-MCP éligibles au catalogue apparaissent dans `ALL_TOOLS`
- les outils directs restent visibles par le modèle et n'apparaissent pas dans `ALL_TOOLS`
- les outils refusés n'apparaissent pas dans `ALL_TOOLS`
- `tools.search`, `tools.describe`, `tools.callValue`, et `tools.call` fonctionnent pour les outils OpenClaw
- `API.list("mcp")` et `API.read("mcp/<server>.d.ts")` exposent les déclarations MCP de style TypeScript sans appel de bridge/outil
- l'espace de noms MCP `$api()` reste disponible comme secours en ligne pour les schémas
- les appels d'espace de noms MCP fonctionnent pour les outils MCP visibles avec une entrée d'objet unique, tandis que les entrées de catalogue MCP directes sont absentes de `tools.*`
- les outils de contrôle Tool Search sont cachés à la fois de la surface du modèle et du catalogue caché
- les appels imbriqués préservent l'approbation et le comportement des hooks
- le shell `exec` est caché du modèle mais appelable par id de catalogue lorsqu'autorisé
- le mode code récursif `exec` et `wait` ne sont pas appelables à partir du code invité
- l'entrée TypeScript est transformée et évaluée sans charger TypeScript sur les chemins désactivés ou JavaScript uniquement
- `import`, `require`, l'accès au système de fichiers, réseau, et environnement échouent
- les boucles infinies expirent et ne peuvent pas bloquer la Gateway
- les défaillances de limite de mémoire terminent la VM invitée
- les limites de sortie et de snapshot sont appliquées pour les appels complétés et suspendus
- `wait` reprend un snapshot suspendu et retourne la valeur finale
- les valeurs `runId` expirées, abandonnées, de mauvaise session, et inconnues échouent
- la relecture de transcription et la persistance préservent les appels de contrôle du mode code
- la transcription et la télémétrie montrent clairement les appels d'outils imbriqués

## Plan de test E2E

Exécutez-les comme tests d'intégration ou de bout en bout lors de la modification du runtime :

1. Démarrez une Gateway avec `tools.codeMode.enabled: false`.
2. Envoyez un tour d'agent avec un petit ensemble d'outils directs.
3. Affirmez que les outils visibles par le modèle sont inchangés.
4. Redémarrez avec `tools.codeMode.enabled: true`.
5. Envoyez un tour d'agent avec des outils de test OpenClaw, plugin, MCP, et client.
6. Affirmez que la liste des outils visibles par le modèle est `exec`, `wait`, plus uniquement les outils directs configurés.
7. Dans `exec`, lisez `ALL_TOOLS` et affirmez que les outils de test effectifs éligibles au catalogue sont présents tandis que les outils directs sont absents.
8. Dans `exec`, appelez les outils OpenClaw/plugin/client via `tools.search`, `tools.describe`, et `tools.callValue` (ou `tools.call` brut).
9. Dans `exec`, appelez `API.list("mcp")` et `API.read("mcp/<server>.d.ts")` et affirmez que les fichiers de déclaration décrivent les outils MCP visibles.
10. Dans `exec`, appelez les outils MCP via `MCP.<server>.<tool>({ ...input })` et affirmez que les entrées de catalogue MCP directes sont absentes de `ALL_TOOLS` et `tools.*`.
11. Affirmez que les outils refusés sont absents et ne peuvent pas être appelés par id deviné.
12. Démarrez un appel d'outil imbriqué qui se résout après que `exec` retourne `waiting`.
13. Appelez `wait` et affirmez que la VM restaurée reçoit le résultat de l'outil.
14. Affirmez que la réponse finale contient la sortie produite après la restauration.
15. Affirmez que le délai d'expiration, l'abandon, et l'expiration du snapshot nettoient l'état du runtime.
16. Exportez la trajectoire et affirmez que les appels imbriqués sont visibles sous l'appel du mode code parent.

Les modifications de documentation uniquement sur cette page doivent toujours exécuter `pnpm check:docs`.

## Connexes

- [Tool Search](/fr/tools/tool-search)
- [Runtimes d'agent](/fr/concepts/agent-runtimes)
- [Outil Exec](/fr/tools/exec)
- [Exécution de code](/fr/tools/code-execution)
