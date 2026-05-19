---
summary: "Mode code OpenClaw : une surface d'outil exec/wait opt-in soutenue par QuickJS-WASI et un catalogue d'outils caché à portée d'exécution"
title: "Mode code"
sidebarTitle: "Mode code"
read_when:
  - You want to enable OpenClaw code mode for an agent run
  - You need to explain why code mode is different from Codex Code mode
  - You are reviewing the exec/wait contract, QuickJS-WASI sandbox, TypeScript transform, or hidden tool-catalog bridge
---

Le mode code est une fonctionnalité expérimentale du runtime d'agent OpenClaw. Il est désactivé par défaut. Lorsque vous l'activez, OpenClaw change ce que le modèle voit pour une exécution : au lieu d'exposer directement chaque schéma d'outil activé, le modèle ne voit que `exec` et `wait`.

Cette page documente le mode code OpenClaw. Ce n'est pas le mode code Codex. Le mode code Codex fait partie de l'harnais de codage Codex et possède son propre espace de travail de projet, runtime, outils et sémantique d'exécution. Le mode code Codex et la recherche d'outils dynamiques native à Codex sont des surfaces d'harnais stables Codex. Le mode code OpenClaw est un adaptateur de surface d'outil expérimental appartenant à OpenClaw pour les exécutions OpenClaw génériques. Il utilise `quickjs-wasi`, un catalogue d'outils OpenClaw caché, et l'exécuteur d'outils OpenClaw normal.

## Qu'est-ce que c'est ?

Le mode code OpenClaw permet au modèle d'écrire un petit programme JavaScript ou TypeScript au lieu de choisir directement dans une longue liste d'outils.

Lorsque le mode code est actif :

- La liste d'outils visible par le modèle est exactement `exec` et `wait`.
- `exec` évalue le JavaScript ou TypeScript généré par le modèle dans un worker QuickJS-WASI contraint.
- Les outils OpenClaw normaux sont cachés à l'invite du modèle et exposés à l'intérieur du programme invité via `ALL_TOOLS` et `tools`.
- Le code invité peut rechercher le catalogue caché, décrire un outil et appeler un outil via le même chemin d'exécution OpenClaw utilisé par les tours d'agent normaux.
- `wait` reprend une exécution en mode code suspendue lorsque les appels d'outils imbriqués sont toujours en attente.

La distinction importante : le mode code change la surface d'orchestration visible par le modèle. Il ne remplace pas les outils OpenClaw, les outils de plugin, les outils MCP, l'authentification, la politique d'approbation, le comportement des canaux ou la sélection du modèle.

## Pourquoi c'est bien ?

Le mode code rend les grands catalogues d'outils plus faciles à utiliser pour les modèles.

- Surface d'invite plus petite : les fournisseurs reçoivent deux outils de contrôle au lieu de dizaines ou de centaines de schémas d'outils complets.
- Meilleure orchestration : le modèle peut utiliser des boucles, des jointures, de petites transformations, une logique conditionnelle et des appels d'outils imbriqués parallèles à l'intérieur d'une seule cellule de code.
- Neutre vis-à-vis du fournisseur : cela fonctionne pour les outils OpenClaw, plugin, MCP et client sans dépendre de l'exécution de code native du fournisseur.
- La politique existante reste en vigueur : les appels d'outils imbriqués passent toujours par la politique OpenClaw, les approbations, les hooks, le contexte de session et les chemins d'audit.
- Mode d'échec clair : lorsque le mode code est explicitement activé et que le runtime n'est pas disponible, OpenClaw échoue de manière fermée au lieu de revenir à une exposition d'outils directe large.

Le mode code est particulièrement utile pour les agents avec un grand catalogue d'outils activés ou pour les workflows où le modèle doit à plusieurs reprises rechercher, combiner et appeler des outils avant de produire une réponse.

## Comment l'activer

Ajoutez `tools.codeMode.enabled: true` à la configuration de l'agent ou du runtime :

```json5
{
  tools: {
    codeMode: {
      enabled: true,
    },
  },
}
```

La notation abrégée est également acceptée :

```json5
{
  tools: {
    codeMode: true,
  },
}
```

Le mode code reste désactivé lorsque `tools.codeMode` est omis, `false`, ou un objet sans `enabled: true`.

Utilisez des limites explicites lorsque vous voulez des limites plus strictes :

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

Pour confirmer la forme de la charge utile du modèle lors du débogage, exécutez la passerelle avec la journalisation ciblée :

```bash
OPENCLAW_DEBUG_CODE_MODE=1 \
OPENCLAW_DEBUG_MODEL_TRANSPORT=1 \
OPENCLAW_DEBUG_MODEL_PAYLOAD=tools \
openclaw gateway
```

Avec le mode code actif, les noms d'outils visibles par le modèle enregistrés doivent être `exec` et `wait`. Si vous avez besoin de la charge utile du fournisseur expurgée, ajoutez `OPENCLAW_DEBUG_MODEL_PAYLOAD=full-redacted` pour une courte session de débogage.

## Visite technique

Le reste de cette page décrit le contrat du runtime et les détails d'implémentation. Elle est destinée aux responsables de la maintenance, aux auteurs de plugins déboguant l'exposition des outils et aux opérateurs validant les déploiements à haut risque.

## État du runtime

- Runtime : [`quickjs-wasi`](https://github.com/vercel-labs/quickjs-wasi).
- État par défaut : désactivé.
- Stabilité : surface OpenClaw expérimentale ; le mode code Codex est une surface d'harnais stable Codex séparée.
- Surface cible : exécutions d'agent OpenClaw génériques.
- Posture de sécurité : le code du modèle est hostile.
- Promesse visible par l'utilisateur : l'activation du mode code ne revient jamais silencieusement à une exposition d'outils directe large.

## Portée

Le mode code possède la forme d'orchestration visible par le modèle pour une exécution préparée. Il ne possède pas la sélection du modèle, le comportement des canaux, l'authentification, la politique des outils ou les implémentations des outils.

Dans la portée :

- définitions d'outils `exec` et `wait` visibles par le modèle
- construction du catalogue d'outils caché
- exécution d'invité JavaScript et TypeScript
- runtime du worker QuickJS-WASI
- callbacks d'hôte pour la recherche de catalogue, la description de schéma et l'appel d'outil
- état reprise pour les programmes invités suspendus
- limites de sortie, délai d'attente, mémoire, appel en attente et snapshot
- télémétrie et projection de trajectoire pour les appels d'outils imbriqués

Hors de la portée :

- exécution de code distant native du fournisseur
- sémantique d'exécution de shell
- modification de l'autorisation d'outil existante
- scripts persistants créés par l'utilisateur
- accès au gestionnaire de paquets, fichiers, réseau ou modules dans le code invité
- réutilisation directe des éléments internes du mode code Codex

Les outils appartenant au fournisseur, tels que les sandboxes Python distants, restent des outils séparés. Voir [Exécution de code](/fr/tools/code-execution).

## Termes

**Mode code** est le mode runtime OpenClaw qui cache les outils de modèle normaux et expose uniquement `exec` et `wait`.

**Runtime invité** est la VM JavaScript QuickJS-WASI qui évalue le code du modèle.

**Pont d'hôte** est la surface de callback étroite compatible JSON du code invité vers OpenClaw.

**Catalogue** est la liste à portée d'exécution des outils effectifs après la politique d'outil normale, la résolution de plugin, MCP et outil client.

**Appel d'outil imbriqué** est un appel d'outil effectué à partir du code invité via le pont d'hôte.

**Snapshot** est l'état de VM QuickJS-WASI sérialisé enregistré pour que `wait` puisse continuer une exécution en mode code suspendue.

## Configuration

`tools.codeMode.enabled` est la porte d'activation. La définition d'autres champs du mode code n'active pas la fonctionnalité.

Champs pris en charge :

- `enabled` : booléen. Par défaut `false`. Active le mode code uniquement lorsque `true`.
- `runtime` : `"quickjs-wasi"`. Seul runtime pris en charge.
- `mode` : `"only"`. Expose `exec` et `wait`, cache les outils de modèle normaux.
- `languages` : tableau de `"javascript"` et `"typescript"`. Par défaut inclut les deux.
- `timeoutMs` : limite de temps mur pour un `exec` ou `wait`. Par défaut `10000`. Serrage du runtime : `100` à `60000`.
- `memoryLimitBytes` : limite du tas QuickJS. Par défaut `67108864`. Serrage du runtime : `1048576` à `1073741824`.
- `maxOutputBytes` : limite pour le texte retourné, JSON et journaux. Par défaut `65536`. Serrage du runtime : `1024` à `10485760`.
- `maxSnapshotBytes` : limite pour les snapshots de VM sérialisés. Par défaut `10485760`. Serrage du runtime : `1024` à `268435456`.
- `maxPendingToolCalls` : limite pour les appels d'outils imbriqués concurrents. Par défaut `16`. Serrage du runtime : `1` à `128`.
- `snapshotTtlSeconds` : durée pendant laquelle une VM suspendue peut être reprise. Par défaut `900`. Serrage du runtime : `1` à `86400`.
- `searchDefaultLimit` : nombre de résultats de recherche de catalogue caché par défaut. Par défaut `8`. Le runtime serre cela à `maxSearchLimit`.
- `maxSearchLimit` : nombre maximum de résultats de recherche de catalogue caché. Par défaut `50`. Serrage du runtime : `1` à `50`.

Si le mode code est activé mais que QuickJS-WASI ne peut pas être chargé, OpenClaw échoue de manière fermée pour cette exécution. Il n'expose pas silencieusement les outils normaux comme solution de secours.

## Activation

Le mode code est évalué après que la politique d'outil effective soit connue et avant que la demande de modèle finale soit assemblée.

Ordre d'activation :

1. Résolvez l'agent, le modèle, le fournisseur, le sandbox, le canal, l'expéditeur et la politique d'exécution.
2. Construisez la liste d'outils OpenClaw effective.
3. Ajoutez les outils de plugin, MCP et client éligibles.
4. Appliquez la politique d'autorisation et de refus.
5. Si `tools.codeMode.enabled` est false, continuez avec l'exposition d'outils normale.
6. Si activé et que les outils sont actifs pour l'exécution, enregistrez les outils effectifs dans le catalogue du mode code.
7. Supprimez tous les outils normaux de la liste d'outils visible par le modèle.
8. Ajoutez le mode code `exec` et `wait`.

Les exécutions qui intentionnellement n'ont pas d'outils, telles que les appels de modèle bruts, `disableTools`, ou une liste d'autorisation vide, n'activent pas la surface du mode code même si la configuration contient `tools.codeMode.enabled: true`.

Le catalogue du mode code est à portée d'exécution. Il ne doit pas fuir les outils d'un autre agent, session, expéditeur ou exécution.

## Outils visibles par le modèle

Lorsque le mode code est actif, le modèle voit exactement ces outils de niveau supérieur :

- `exec`
- `wait`

Tous les autres outils activés sont cachés à la liste d'outils visible par le modèle et enregistrés dans le catalogue du mode code.

Le modèle doit utiliser `exec` pour l'orchestration d'outils, la jointure de données, les boucles, les appels imbriqués parallèles et les transformations structurées. Le modèle doit utiliser `wait` uniquement lorsque `exec` retourne un résultat `waiting` reprise.

## `exec`

`exec` démarre une cellule du mode code et retourne un résultat. Le code d'entrée est généré par le modèle et doit être traité comme hostile.

Entrée :

```typescript
type CodeModeExecInput = {
  code: string;
  language?: "javascript" | "typescript";
};
```

Règles d'entrée :

- `code` est requis et doit être non vide.
- `language` par défaut à `"javascript"`.
- Si `language` est `"typescript"`, OpenClaw transpile avant l'évaluation.
- `exec` rejette les modèles `import`, `require`, import dynamique et chargeur de module en v1.
- `exec` n'expose pas l'implémentation `exec` de shell normale de manière récursive.

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

`exec` retourne `waiting` lorsque la VM QuickJS se suspend avec un état reprise. Le résultat inclut un `runId` pour `wait`.

`exec` retourne `completed` uniquement lorsque la VM invitée n'a pas de travail en attente et que la valeur finale est compatible JSON après l'exécution de l'adaptateur de sortie OpenClaw.

## `wait`

`wait` reprend une VM en mode code suspendue.

Entrée :

```typescript
type CodeModeWaitInput = {
  runId: string;
};
```

La sortie est la même union `CodeModeResult` retournée par `exec`.

`wait` existe parce que les outils OpenClaw imbriqués peuvent être lents, interactifs, soumis à approbation ou diffuser des mises à jour partielles. Le modèle ne devrait pas avoir besoin de garder un long appel `exec` ouvert pendant que l'hôte attend un travail externe.

La capture d'écran et la restauration de QuickJS-WASI constituent le mécanisme de reprise v1 :

1. `exec` évalue le code jusqu'à l'achèvement, l'échec ou la suspension.
2. En cas de suspension, OpenClaw capture l'état de la VM QuickJS et enregistre le travail d'hôte en attente.
3. Lorsque le travail en attente se règle, `wait` restaure la capture d'écran de la VM.
4. OpenClaw réenregistre les rappels d'hôte par des noms stables.
5. OpenClaw livre les résultats des outils imbriqués dans la VM restaurée.
6. OpenClaw vide les tâches en attente de QuickJS.
7. `wait` retourne `completed`, `failed` ou un autre résultat `waiting`.

Les captures d'écran sont l'état d'exécution, pas des artefacts utilisateur. Elles sont limitées en taille, expirées et limitées à l'exécution et à la session qui les ont créées.

`wait` échoue quand :

- `runId` est inconnu.
- la capture d'écran a expiré.
- l'exécution ou la session parente a été interrompue.
- l'appelant n'est pas dans la même portée d'exécution/session.
- la restauration de QuickJS-WASI échoue.
- la restauration dépasserait les limites configurées.

## API d'exécution invité

L'exécution invité expose une petite API globale :

```typescript
declare const ALL_TOOLS: ToolCatalogEntry[];
declare const tools: ToolCatalog;

declare function text(value: unknown): void;
declare function json(value: unknown): void;
declare function yield_control(reason?: string): Promise<void>;
```

`ALL_TOOLS` est des métadonnées compactes pour le catalogue limité à l'exécution. Il ne contient pas de schémas complets par défaut.

```typescript
type ToolCatalogEntry = {
  id: string;
  name: string;
  label?: string;
  description: string;
  source: "openclaw" | "plugin" | "mcp" | "client";
  sourceName?: string;
};
```

Le schéma complet est chargé uniquement à la demande :

```typescript
type ToolCatalogEntryWithSchema = ToolCatalogEntry & {
  parameters: unknown;
};
```

Assistants de catalogue :

```typescript
type ToolCatalog = {
  search(query: string, options?: { limit?: number }): Promise<ToolCatalogEntry[]>;
  describe(id: string): Promise<ToolCatalogEntryWithSchema>;
  call(id: string, input?: unknown): Promise<unknown>;
  [safeToolName: string]: unknown;
};
```

Les fonctions d'outil de commodité sont installées uniquement pour les noms sûrs sans ambiguïté :

```typescript
const files = await tools.search("read local file");
const fileRead = await tools.describe(files[0].id);
const content = await tools.call(fileRead.id, { path: "README.md" });

// Si le catalogue caché a une entrée `web_search` sans ambiguïté :
const hits = await tools.web_search({ query: "OpenClaw code mode" });
```

L'exécution invité ne doit pas exposer directement les objets hôtes. Les entrées et sorties traversent le pont en tant que valeurs compatibles JSON avec des limites de taille explicites.

## API de sortie

`text(value)` ajoute une sortie lisible par l'homme au tableau `output`.

`json(value)` ajoute un élément de sortie structuré après sérialisation compatible JSON.

La valeur retournée finale du code invité devient `value` dans un résultat `completed`.

Élément de sortie :

```typescript
type CodeModeOutput = { type: "text"; text: string } | { type: "json"; value: unknown };
```

Règles de sortie :

- l'ordre de sortie correspond aux appels invités
- la sortie est limitée par `maxOutputBytes`
- les valeurs non sérialisables sont converties en chaînes simples ou erreurs
- les valeurs binaires ne sont pas prises en charge en v1
- les images et fichiers circulent via les outils OpenClaw ordinaires, pas via le pont en mode code

## Catalogue d'outils

Le catalogue caché inclut les outils après filtrage de politique efficace :

1. Outils principaux OpenClaw.
2. Outils de plugin groupés.
3. Outils de plugin externes.
4. Outils MCP.
5. Outils fournis par le client pour l'exécution actuelle.

Les identifiants de catalogue sont stables dans une exécution et déterministes entre les ensembles d'outils équivalents si possible.

Forme d'identifiant recommandée :

```text
<source>:<owner>:<tool-name>
```

Exemples :

```text
openclaw:core:message
plugin:browser:browser_request
mcp:github:create_issue
client:app:select_file
```

Le catalogue omet les outils de contrôle en mode code :

- `exec`
- `wait`
- `tool_search_code`
- `tool_search`
- `tool_describe`
- `tool_call`

Cela prévient la récursion et maintient le contrat orienté modèle étroit.

## Interaction de recherche d'outils

Le mode code remplace la surface du modèle PI Tool Search pour les exécutions où il est actif.

Quand `tools.codeMode.enabled` est vrai et que le mode code s'active :

- OpenClaw n'expose pas `tool_search_code`, `tool_search`, `tool_describe` ou `tool_call` en tant qu'outils visibles par le modèle.
- La même idée de catalogage se déplace à l'intérieur de l'exécution invité.
- L'exécution invité reçoit des métadonnées compactes `ALL_TOOLS` et des assistants de recherche, description et appel.
- Les appels imbriqués se distribuent via le même chemin d'exécuteur OpenClaw que Tool Search utilise.

La page [Tool Search](/fr/tools/tool-search) existante décrit le pont de catalogue compact PI. Le mode code est l'alternative OpenClaw générique pour les exécutions qui peuvent utiliser `exec` et `wait`.

## Noms d'outils et collisions

L'outil `exec` visible par le modèle est l'outil en mode code. Si l'outil shell `exec` OpenClaw normal est activé, il est caché au modèle et catalogué comme tout autre outil.

À l'intérieur de l'exécution invité :

- `tools.call("openclaw:core:exec", input)` peut appeler l'outil shell exec si la politique le permet.
- `tools.exec(...)` est installé uniquement si l'entrée du catalogue d'outils shell exec a un nom sûr sans ambiguïté.
- l'outil `exec` en mode code n'est jamais récursivement disponible via `tools`.

Si deux outils se normalisent au même nom de commodité sûr, OpenClaw omet la fonction de commodité et nécessite `tools.call(id, input)`.

## Exécution d'outils imbriqués

Chaque appel d'outil imbriqué traverse le pont d'hôte et rentre dans OpenClaw.

L'exécution imbriquée préserve :

- identifiant d'agent actif
- identifiant de session et clé de session
- contexte d'expéditeur et de canal
- politique de bac à sable
- politique d'approbation
- crochets de plugin `before_tool_call`
- signal d'abandon
- mises à jour en continu où disponibles
- événements de trajectoire et d'audit

Les appels imbriqués se projettent dans la transcription en tant qu'appels d'outils réels afin que les bundles de support puissent montrer ce qui s'est passé. La projection identifie l'appel d'outil en mode code parent et l'identifiant d'outil imbriqué.

Les appels d'outils imbriqués parallèles sont autorisés jusqu'à `maxPendingToolCalls`.

## État d'exécution

Chaque exécution en mode code a une machine d'état :

- `running` : la VM exécute ou les appels imbriqués sont en vol.
- `waiting` : la capture d'écran de la VM existe et peut être reprise avec `wait`.
- `completed` : valeur finale retournée ; capture d'écran supprimée.
- `failed` : erreur retournée ; capture d'écran supprimée.
- `expired` : capture d'écran ou état en attente dépassé la rétention ; impossible de reprendre.
- `aborted` : exécution/session parente annulée ; capture d'écran supprimée.

L'état est limité par l'exécution d'agent, la session et l'identifiant d'appel d'outil. Un appel `wait` d'une exécution ou session différente échoue.

Le stockage de capture d'écran est limité :

- octets de capture d'écran maximum par exécution
- captures d'écran en direct maximum par processus
- TTL de capture d'écran
- nettoyage à la fin de l'exécution
- nettoyage à l'arrêt de la passerelle où la persistance n'est pas prise en charge

## Exécution QuickJS-WASI

OpenClaw charge `quickjs-wasi` en tant que dépendance directe dans le package propriétaire. L'exécution ne repose pas sur une copie transitive installée pour proxy, PAC ou d'autres dépendances non liées.

Responsabilités d'exécution :

- compiler ou charger le module WebAssembly QuickJS-WASI
- créer une VM isolée par exécution en mode code ou reprise
- enregistrer les rappels d'hôte par des noms stables
- définir les limites de mémoire et d'interruption
- évaluer JavaScript
- vider les tâches en attente
- capturer l'état de la VM suspendue
- restaurer les captures d'écran pour `wait`
- disposer des poignées de VM et des captures d'écran après les états terminaux

L'exécution s'exécute en dehors de la boucle d'événements principale d'OpenClaw dans un worker. Une boucle infinie invitée ne doit pas bloquer indéfiniment le processus Gateway.

## TypeScript

La prise en charge de TypeScript est une transformation source uniquement :

- entrée acceptée : une chaîne de code TypeScript
- sortie : chaîne JavaScript évaluée par QuickJS-WASI
- pas de vérification de type
- pas de résolution de module
- pas d'`import` ou `require` en v1
- les diagnostics sont retournés en tant que résultats `failed`

Le compilateur TypeScript est chargé paresseusement uniquement pour les cellules TypeScript. Les cellules JavaScript simples et le mode code désactivé ne chargent pas le compilateur.

La transformation doit préserver les numéros de ligne utiles si possible.

## Limite de sécurité

Le code du modèle est hostile. L'exécution utilise la défense en profondeur :

- exécuter QuickJS-WASI en dehors de la boucle d'événements principale
- charger `quickjs-wasi` en tant que dépendance directe, pas via Codex ou un package transitif
- pas de système de fichiers, réseau, sous-processus, importation de module, variables d'environnement ou objets globaux hôtes dans l'invité
- utiliser les limites de mémoire et d'interruption de QuickJS
- appliquer le délai d'expiration du processus parent
- appliquer les limites de sortie, capture d'écran, journal et appel en attente
- sérialiser les valeurs du pont d'hôte via un adaptateur JSON étroit
- convertir les erreurs d'hôte en erreurs invitées simples, jamais des objets du domaine d'hôte
- supprimer les captures d'écran en cas de délai d'expiration, abandon, fin de session ou expiration
- rejeter l'accès récursif à `exec`, `wait` et les outils de contrôle Tool Search
- empêcher les collisions de noms de commodité d'ombrager les assistants de catalogue

Le bac à sable est une couche de sécurité. Les opérateurs peuvent toujours avoir besoin de durcissement au niveau du système d'exploitation pour les déploiements à haut risque.

## Codes d'erreur

```typescript
type CodeModeErrorCode =
  | "runtime_unavailable"
  | "invalid_config"
  | "invalid_input"
  | "unsupported_language"
  | "typescript_transform_failed"
  | "module_access_denied"
  | "timeout"
  | "memory_limit_exceeded"
  | "output_limit_exceeded"
  | "snapshot_limit_exceeded"
  | "snapshot_expired"
  | "snapshot_restore_failed"
  | "too_many_pending_tool_calls"
  | "nested_tool_failed"
  | "aborted"
  | "internal_error";
```

Les erreurs retournées à l'invité sont des données simples. Les instances `Error` d'hôte, les objets de pile, les prototypes et les fonctions d'hôte ne traversent pas dans QuickJS.

## Télémétrie

Le mode code rapporte :

- noms d'outils visibles envoyés au modèle
- taille du catalogue caché et répartition des sources
- comptages `exec` et `wait`
- comptages de recherche, description et appel imbriqués
- identifiants d'outils imbriqués appelés
- délai d'expiration, mémoire, capture d'écran et défaillances de limite de sortie
- événements du cycle de vie de la capture d'écran

La télémétrie ne doit pas inclure de secrets, de valeurs d'environnement brutes ou d'entrées d'outils non rédactées au-delà de la politique de trajectoire OpenClaw existante.

## Débogage

Utilisez la journalisation ciblée du transport de modèle quand le mode code se comporte différemment d'une exécution d'outil normale :

```bash
OPENCLAW_DEBUG_CODE_MODE=1 \
OPENCLAW_DEBUG_MODEL_TRANSPORT=1 \
OPENCLAW_DEBUG_MODEL_PAYLOAD=tools \
OPENCLAW_DEBUG_SSE=events \
openclaw gateway
```

Pour le débogage de forme de charge utile, utilisez `OPENCLAW_DEBUG_MODEL_PAYLOAD=full-redacted`. Cela enregistre une capture d'écran JSON rédactée et limitée de la demande du modèle ; elle ne doit être utilisée que lors du débogage car les invites et le texte du message peuvent toujours apparaître.

Pour le débogage de flux, utilisez `OPENCLAW_DEBUG_SSE=peek` pour enregistrer les cinq premiers événements SSE rédactés. Le mode code échoue également fermé si la charge utile du fournisseur final ne contient pas exactement `exec` et `wait` après l'activation de la surface en mode code.

## Disposition de mise en œuvre

Unités de mise en œuvre :

- contrat de configuration : `tools.codeMode`
- générateur de catalogue : outils efficaces pour les entrées compactes et la carte d'identifiants
- adaptateur de surface de modèle : remplacer les outils visibles par `exec` et `wait`
- adaptateur d'exécution QuickJS-WASI : charger, évaluer, capturer, restaurer, disposer
- superviseur de worker : délai d'expiration, abandon, isolation de panne
- adaptateur de pont : rappels sûrs JSON et livraison de résultats
- adaptateur de transformation TypeScript
- magasin de capture d'écran : TTL, limites de taille, portée d'exécution/session
- projection de trajectoire pour les appels d'outils imbriqués
- compteurs de télémétrie et diagnostics

La mise en œuvre réutilise les concepts de catalogue et d'exécuteur de Tool Search, mais n'utilise pas l'enfant `node:vm` comme bac à sable.

## Liste de contrôle de validation

La couverture du mode code doit prouver :

- la configuration désactivée laisse l'exposition des outils existants inchangée
- la configuration d'objet sans `enabled: true` laisse le mode code désactivé
- la configuration activée expose uniquement `exec` et `wait` au modèle quand les outils sont
  actifs pour l'exécution
- les exécutions sans outil brutes, `disableTools`, et les listes d'autorisation vides ne déclenchent pas l'application
  de la charge utile du mode code
- tous les outils effectifs apparaissent dans `ALL_TOOLS`
- les outils refusés n'apparaissent pas dans `ALL_TOOLS`
- `tools.search`, `tools.describe`, et `tools.call` fonctionnent pour les outils OpenClaw
- Les outils de contrôle Tool Search sont masqués à la fois de la surface du modèle et du catalogue
  caché
- les appels imbriqués préservent le comportement d'approbation et de hook
- l'`exec` shell est masqué du modèle mais appelable par id de catalogue quand autorisé
- l'`exec` et `wait` du mode code récursif ne sont pas appelables depuis le code invité
- l'entrée TypeScript est transformée et évaluée sans charger TypeScript sur les
  chemins désactivés ou JavaScript uniquement
- `import`, `require`, l'accès au système de fichiers, réseau et environnement échouent
- les boucles infinies expirent et ne peuvent pas bloquer la Gateway
- les défaillances du plafond de mémoire terminent la VM invitée
- les plafonds de sortie et d'instantané sont appliqués pour les appels complétés et suspendus
- `wait` reprend un instantané suspendu et retourne la valeur finale
- les valeurs `runId` expirées, abandonnées, de mauvaise session et inconnues échouent
- la relecture et la persistance de la transcription préservent les appels de contrôle du mode code
- la transcription et la télémétrie affichent clairement les appels d'outils imbriqués

## Plan de test E2E

Exécutez ces tests en tant que tests d'intégration ou de bout en bout lors de la modification du runtime :

1. Démarrez une Gateway avec `tools.codeMode.enabled: false`.
2. Envoyez un tour d'agent avec un petit ensemble d'outils directs.
3. Affirmez que les outils visibles du modèle sont inchangés.
4. Redémarrez avec `tools.codeMode.enabled: true`.
5. Envoyez un tour d'agent avec OpenClaw, plugin, MCP, et outils de test client.
6. Affirmez que la liste des outils visibles du modèle est exactement `exec`, `wait`.
7. Dans `exec`, lisez `ALL_TOOLS` et affirmez que les outils de test effectifs sont présents.
8. Dans `exec`, appelez `tools.search`, `tools.describe`, et `tools.call`.
9. Affirmez que les outils refusés sont absents et ne peuvent pas être appelés par id deviné.
10. Démarrez un appel d'outil imbriqué qui se résout après que `exec` retourne `waiting`.
11. Appelez `wait` et affirmez que la VM restaurée reçoit le résultat de l'outil.
12. Affirmez que la réponse finale contient la sortie produite après la restauration.
13. Affirmez que le délai d'expiration, l'abandon et l'expiration de l'instantané nettoient l'état du runtime.
14. Exportez la trajectoire et affirmez que les appels imbriqués sont visibles sous l'appel
    du mode code parent.

Les modifications de documentation uniquement sur cette page doivent toujours exécuter `pnpm check:docs`.

## Connexes

- [Tool Search](/fr/tools/tool-search)
- [Runtimes d'agent](/fr/concepts/agent-runtimes)
- [Outil Exec](/fr/tools/exec)
- [Exécution de code](/fr/tools/code-execution)
