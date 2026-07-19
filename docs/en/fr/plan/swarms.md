# Swarms — fan-out et orchestration d'agents en mode code

Status: spec d'implémentation (v1 en cours). Ce document est le spec de build figé.
Il sera réécrit en docs orientées utilisateur (`docs/tools/swarm.md`) une fois la
fonctionnalité livrée et testée. Feature-gated derrière `tools.swarm` (désactivé par défaut);
`main` reste livrable à chaque point.

## 1. Quoi et pourquoi

Un **swarm** est un ensemble de sous-agents orchestrés de manière déterministe à partir d'un
script en mode code : fan out N lecteurs, vérifier les résultats de manière adversariale,
synthétiser via un prioritaire avec état, boucler sur des portes de décision. Le flux de contrôle
(`Promise.all`, `while`, `if`) _est_ l'orchestration — il n'y a délibérément **pas de DSL graphique,
pas de nouveau mode, pas de nouvelle surface d'outil de haut niveau**.

Le mode code OpenClaw (QuickJS-WASI, snapshot/resume, bridge requests) est le substrat.
Un appel bridge parqué survit au snapshot VM, au redémarrage de la gateway, et reprend
exactement où il s'est arrêté — plus robuste que les designs basés sur journal-replay,
sans contraintes de déterminisme sur les scripts.

Nommage : le nom produit/docs est **Swarm**. Les identifiants de code restent littéraux :
API guest `agents.*`, config `tools.swarm`, colonnes de groupe `swarm`.

## 2. Décisions (mainteneur, 2026-07-17)

- Coût : caps de config appliqués ; budget de tokens par swarm optionnel. Pas de budget obligatoire.
- Approbations : les enfants s'exécutent **fail-closed / non-interactif**. Les actions
  nécessitant une approbation sont refusées ; le refus est rapporté dans le résultat de l'enfant ;
  le script décide. Pas de spam de prompt opérateur à partir du fan-out.
- v1 est scripts ad-hoc écrits par modèle uniquement. Workflows sauvegardés/nommés, entrée CLI/cron :
  plus tard (le mode code headless existe déjà pour cron).
- Identité enfant : agent worker dédié par défaut via config `tools.swarm.defaultAgentId`
  (validé contre la liste d'autorisation de cible de sous-agent existante) ; override
  `agentId` par spawn. Le core ne livre aucun id d'agent bundlé ; les docs recommandent
  une config `worker` légère.
- Pas de changements source Codex. Le harnais Codex utilise l'idiome spawn/wait (§8).

## 3. Aperçu de l'architecture

```
script mode-code (VM QuickJS, gateway)          script Codex V8 (processus codex)
  agents.run(...) ── appel bridge parqué         tools.sessions_spawn / tools.agents_wait
        │                                                │ item/tool/call RPC (≤600s chacun)
        ▼                                                ▼
             CORE (harness-agnostic, ce repo)
  sessions_spawn {collect:true, outputSchema, fastMode, groupId}
  agents_wait {ids, timeoutSeconds}
        │
  registre de sous-agent (SQLite) : enregistrements de complétion du collecteur, id de groupe swarm
        │
  enfants = sessions de sous-agent ordinaires (lane-capped, approbations fail-closed)
        │
  sessions.changed SSE ──► Points Control UI / sidebar / message de statut de canal
```

Un propriétaire canonique unique de la sémantique spawn/complete/settle (outils core + registre).
Deux transports d'attente : QuickJS parque un appel bridge indéfiniment (snapshot) ;
Codex interroge `agents_wait` dans des RPCs bornées.

## 4. Porte de config (v1)

Nouveau `tools.swarm` (global + override par agent, même pattern de fusion que
`tools.codeMode`) :

```jsonc
"tools": {
  "swarm": {
    "enabled": false,            // porte maître, OFF par défaut
    "maxConcurrent": 8,          // enfants s'exécutant à la fois (cap de lane swarm)
    "maxChildrenPerGroup": 50,   // enfants vivants par groupe swarm
    "maxTotalPerGroup": 200,     // nombre de spawn à vie par groupe (backstop runaway)
    "waitTimeoutSecondsMax": 600,
    "defaultAgentId": ""         // optionnel ; id d'agent enfant quand spawn omet agentId
  }
}
```

- Zod : union `boolean | strict object` comme `CodeModeSchema`
  (`src/config/zod-schema.agent-runtime.ts`) ; `swarm: true` → `{enabled: true}`.
- Types dans `src/config/types.tools.ts` (à la fois par agent et top-level `tools`),
  labels dans `schema.labels.ts`, aide dans `schema.help.runtime.ts`.
- Helper de résolution `resolveSwarmConfig(cfg, agentId)` miroir de
  `resolveCodeModeConfig` (`src/agents/code-mode.ts:215`), clamping tous les nombres.
- Effets de porte quand désactivée : outil `agents_wait` absent des catalogues ;
  params `collect`/`outputSchema`/`fastMode`/`groupId` sur `sessions_spawn`
  rejetés avec une erreur claire nommant la clé de config. Pas d'autre changement de comportement.
- `defaultAgentId` est validé via `resolveSubagentAllowedTargetIds`
  (`src/agents/subagent-target-policy.ts`) ; id inconnu → erreur de spawn, pas de fallback.

## 5. Core : spawn en mode collecteur + `agents_wait` (v1)

### 5.1 Ajouts `sessions_spawn` (tous gated sur swarm activé)

- `collect: boolean` — quand true, l'exécution enfant est enregistrée avec
  `expectsCompletionMessage: false` et un **enregistrement de complétion du collecteur**
  au lieu de livraison announce/steering. L'outil retourne `{ runId, sessionKey }`
  immédiatement. Pas de liaison canal/thread.
- `outputSchema: object` — JSON Schema. L'enfant obtient un outil synthétique
  `structured_output` ajouté à sa surface d'outil ; un addendum de system-prompt
  l'instruit d'appeler exactement une fois avec son résultat final. En cas d'échec
  de validation, l'enfant obtient une tentative de nudge retry ; après cela,
  l'enregistrement de complétion porte `structured: undefined` plus le texte brut
  et une `schemaError`.
- `fastMode: true | "auto" | false` — enfilé dans le patch de session enfant
  aux côtés du modèle/thinking via `resolveSubagentModelAndThinkingPlan`
  (`src/agents/subagent-spawn-plan.ts`), utilisant l'axe `FastMode` existant
  (`src/shared/fast-mode.ts`). Omis = hériter.
- `groupId: string` — timbre de groupe swarm. Par défaut
  `swarm:<requesterSessionKey>:<runId-of-requesting-run>`. Persisté sur l'enregistrement
  du registre et la ligne de session enfant. Utilisé pour les caps, listing, archive batch,
  et les points.
- `label: string` existe déjà — surfaces dans les points et `subagents list`.
- Id d'agent enfant : `params.agentId` → sinon `tools.swarm.defaultAgentId` → sinon
  agent demandeur (comportement existant).

### 5.2 Les approbations échouent fermées

Les enfants du collecteur s'exécutent avec un contexte d'approbation non-interactif : tout appel
d'outil qui nécessiterait une approbation d'opérateur se résout comme un refus structuré
(`approval_required`) visible à l'enfant, qui est censé rapporter le blocage dans son résultat.
Implémentation : réutiliser la plomberie de politique d'approbation d'outil/exec existante
avec un resolver `deny` forcé pour les exécutions enfant en mode collecteur.
Aucun événement d'approbation n'est émis vers les surfaces opérateur à partir des enfants du collecteur.

### 5.3 Outil `agents_wait` (nouveau, gated)

```
agents_wait({ ids: string[], timeoutSeconds?: number })
→ {
    completed: [{ runId, status: "done"|"failed"|"killed"|"timeout",
                  result: string, structured?: unknown, schemaError?: string,
                  sessionKey, label?, usage?: {inputTokens, outputTokens} }],
    pending: string[]
  }
```

- Retourne dès que **au moins un** id se complète (sémantique first-completion / race,
  active les pipelines), ou sur timeout avec `completed: []`.
- `timeoutSeconds` par défaut 30, clampé à `waitTimeoutSecondsMax`.
- Idempotent : les ids déjà complétés retournent leurs enregistrements à nouveau
  (les enregistrements sont conservés jusqu'à l'archive du groupe). Id inconnu → entrée
  d'erreur par id, pas un throw.
- Propriété : seule la session qui a spawné une exécution (ou sa chaîne parente) peut
  l'attendre — même règle de propriété que `wait` en mode code (`code-mode.ts:1684`).
- Registre : les enregistrements de complétion vivent dans le store SQLite du registre
  de sous-agent existant (`subagent-registry.store.sqlite.ts`) — nouveaux champs,
  pas de nouveau store, pas de bump de version de schéma (colonnes additives uniquement ; voir contrainte §9).

### 5.4 Application des caps

- `maxConcurrent` : les enfants du collecteur s'exécutent sur la lane de sous-agent existante
  mais comptés par groupe swarm ; les spawns au-delà du cap mettent en queue FIFO
  (côté host, dans le chemin spawn — retourne runId immédiatement, l'exécution commence
  quand un slot se libère).
- `maxChildrenPerGroup` / `maxTotalPerGroup` : spawn rejette avec une erreur typée
  une fois dépassée ; le texte d'erreur nomme la clé de config.
- Profondeur : les enfants du collecteur conservent la sémantique `DEFAULT_SUBAGENT_MAX_SPAWN_DEPTH`
  (les enfants sont des feuilles sauf si l'imbrication est explicitement configurée).

## 6. Contrat de test (v1, lane A)

- Unité : résolution/clamping de config ; rejets de porte quand désactivée ; defaulting de groupId ;
  application des caps (queue + reject) ; sémantique race d'attente ; idempotence d'attente ;
  refus de propriété ; validation de structured-output + nudge retry + chemin schemaError ;
  plomberie fastMode dans patch de session ; validation defaultAgentId.
- Intégration (vitest, mock model runtime) : spawn 3 enfants du collecteur, attendre
  en boucle, assert l'ordre first-completion et le drain final ; simulation de gateway-restart :
  rechargement du registre → l'attente se résout à partir de la complétion persistée.
- Tous les tests colocalisés `*.test.ts` ; pas d'appels de modèle en direct.

## 7. Surface guest QuickJS (lane B, après core)

- Globals guest installées dans `CONTROLLER_SOURCE`
  (`src/agents/code-mode.worker.ts:190-374`), noms réservés ajoutés dans
  `code-mode-namespaces.ts` :
  - `agents.run(prompt, opts) → Promise<result|structured>` — sucre :
    spawn du collecteur + attente parquée sur une méthode bridge dédiée (`agentWait`)
    que l'host règle à la complétion (pas de polling ; snapshot-safe).
  - `agents.session(system, opts) → Promise<handle>` ;
    `handle.send(input, opts) → Promise<...>` ; `handle.close()`. (v1.1 —
    livré après run() ; utilise `mode:"session"` + enregistrements du collecteur par tour.)
  - `phase(title)`, `log(message)` — notifications bridge fire-and-forget →
    événements de progression swarm.
- Méthodes bridge ajoutées à `CodeModeBridgeMethod` (`code-mode.ts:91`) :
  `agentSpawn`, `agentWait`, `swarmNote`. `agentSpawn`/`agentWait` sont
  **par construction** replay-safe : clé d'idempotence `(codeModeRunId, bridgeId)`
  stockée sur l'enregistrement du registre ; le redémarrage règle à nouveau à partir
  des complétions persistées et ne double-spawn jamais.
- Les appels bridge `agentWait` en attente prolongent le TTL de snapshot de l'exécution
  (l'ensemble des agents en attente est le signal ; pas de flag).
- `API.read("agents.d.ts")` fichier virtuel documente la surface typée + les idiomes
  fan-out / gate / cycle (`createCodeModeApiVirtualFiles`,
  `code-mode-namespaces.ts:876`).

## 8. Projection du harnais Codex (lane ultérieure)

- `sessions_spawn` (avec nouveaux params) et `agents_wait` circulent via le bridge
  d'outil dynamique existant ; à l'intérieur des scripts mode-code Codex, ils apparaissent
  comme `tools.*` automatiquement (vérifié : `codex-rs/code-mode/src/runtime/globals.rs:14-65`,
  `codex-rs/core/src/tools/spec_plan.rs:448-507`).
- `agents_wait` obtient la classe de timeout d'outil dynamique long (cap 600s ;
  `extensions/codex/src/app-server/dynamic-tool-execution.ts:37-39`) et est
  marquée timeout/replay-safe.
- Clé de groupe pour parents Codex : `swarm:<parentSessionKey>:<turnId>`.
- Les sous-agents `spawn_agent` natifs Codex coexistent ; leurs lignes task-mirror
  alimentent la même surface de progression.

## 9. Persistance et rétention

- Pas de nouveaux stores. Les enregistrements du registre étendent les tables SQLite
  du registre de sous-agent existant ; les enfants sont des lignes `sessions` ordinaires.
  Colonnes additives uniquement — **tout changement nécessitant un bump de version
  de schéma SQLite a besoin d'une approbation explicite du mainteneur d'abord**
  (politique du repo).
- Id de groupe swarm sur l'enregistrement du registre + métadonnées de session enfant.
- Rétention : les enregistrements du collecteur complétés survivent jusqu'à **l'archive du groupe** :
  quand l'exécution parente se termine (ou le TTL expire), les enfants du groupe s'archiven
  en batch (étendre le balayage `DEFAULT_SUBAGENT_ARCHIVE_AFTER_MINUTES` existant
  pour opérer par groupe).

## 10. Surface de progression (« les points ») — lane ultérieure

- Implicite, piloté par le harnais. Dérivé du SSE `sessions.changed` existant +
  registre ; les notes `phase`/`log` ajoutent de la sémantique. Pas de rendu piloté par agent.
- Control UI : renderer `swarm` dans la famille de widgets de l'espace de travail
  (`ui/src/lib/workspace/widgets/`) — grille de points groupée par phase, ligne narrateur,
  statut/label/modèle par point ; arbre enfant de la sidebar inchangé.
- Canaux : un message de statut édité throttled par groupe (suivre
  `docs/concepts/streaming.md` ; jamais de messages par enfant).

## 11. Page Labs (Control UI, voie indépendante)

Paramètres → **Labs** : bascules de fonctionnalités expérimentales, premières entrées **Code Mode**
et **Swarm**. Chaque ligne : nom, description d'une ligne, lien de documentation, bascule câblée
via le RPC `config.patch` existant (RFC 7396 merge-patch — définir
`tools.codeMode.enabled` / `tools.swarm.enabled`), plus un indice « redémarrage requis » le cas échéant. Découvrable, mais le texte rend le statut expérimental clair. i18n : toutes les chaînes via le pipeline normal `en.ts` + synchronisation.

## 12. Placement (ultérieurement)

- Option `placement` au lancement : `"local"` (par défaut) | `"cloud:<profile>"` via
  la distribution d'environnement worker existante (`sessions.dispatch`) ; placement en pool
  ultérieurement si les enfants sandbox SSH de boîte partagée s'avèrent insuffisants.
- La VM Orchestrator reste toujours sur la passerelle ; settle/dots/budget sont
  indépendants du placement.

## 13. Non-objectifs

- Pas de DSL graphique — le flux de contrôle est le graphe (délibéré, documenté).
- Pas de modifications de source Codex ; pas de réutilisation des internals Code Mode de Codex.
- Pas de workflows enregistrés/nommés en v1 ; pas de point d'entrée CLI.
- Pas de bulle d'approbation d'opérateur par enfant.
- Pas d'approvisionnement cloud 1:1 à l'échelle du fan-out.
- Pas de shims de compatibilité runtime en état stable ; swarm est une nouvelle surface, contrôlée.

## 14. Phases de construction / découpage des PR

1. **Voie A (cœur)** : §4 config + §5 spawn/wait/caps/approvals + §6 tests.
2. **Voie C (page Labs)** : §11 — indépendante, peut atterrir en premier.
3. **Voie B (surface QuickJS)** : §7 — après l'atterrissage des contrats A.
4. Renderer Dots (§10), projection Codex (§8), `agents.session` (§7 v1.1),
   placement (§12), réécriture de la documentation utilisateur — PR de suivi dans cet ordre.

Chaque PR : CI vert, `$autoreview` propre, contrôlé par défaut, main livrable.
