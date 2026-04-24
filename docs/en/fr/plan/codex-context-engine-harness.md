---
title: "Port du moteur de contexte Codex Harness"
summary: "Spécification pour faire honorer au harnais bundlé du serveur d'application Codex les plugins du moteur de contexte OpenClaw"
read_when:
  - Vous câblez le comportement du cycle de vie du moteur de contexte dans le harnais Codex
  - Vous avez besoin que lossless-claw ou un autre plugin de moteur de contexte fonctionne avec les sessions de harnais embarqué codex/*
  - Vous comparez le comportement du contexte PI embarqué et du serveur d'application Codex
---

# Port du moteur de contexte Codex Harness

## Statut

Spécification d'implémentation en brouillon.

## Objectif

Faire en sorte que le harnais bundlé du serveur d'application Codex honore le même contrat de cycle de vie du moteur de contexte OpenClaw que les tours PI embarqués honorent déjà.

Une session utilisant `agents.defaults.embeddedHarness.runtime: "codex"` ou un modèle `codex/*` devrait toujours laisser le plugin de moteur de contexte sélectionné, tel que `lossless-claw`, contrôler l'assemblage du contexte, l'ingestion post-tour, la maintenance et la politique de compaction au niveau OpenClaw dans la mesure où la limite du serveur d'application Codex le permet.

## Non-objectifs

- Ne pas réimplémenter les internals du serveur d'application Codex.
- Ne pas faire en sorte que la compaction de thread native Codex produise un résumé lossless-claw.
- Ne pas exiger que les modèles non-Codex utilisent le harnais Codex.
- Ne pas modifier le comportement de la session ACP/acpx. Cette spécification concerne uniquement le chemin du harnais d'agent embarqué non-ACP.
- Ne pas faire en sorte que les plugins tiers enregistrent les usines d'extension du serveur d'application Codex ; la limite de confiance du plugin bundlé existant reste inchangée.

## Architecture actuelle

La boucle d'exécution embarquée résout le moteur de contexte configuré une fois par exécution avant de sélectionner un harnais de bas niveau concret :

- `src/agents/pi-embedded-runner/run.ts`
  - initialise les plugins du moteur de contexte
  - appelle `resolveContextEngine(params.config)`
  - transmet `contextEngine` et `contextTokenBudget` dans `runEmbeddedAttemptWithBackend(...)`

`runEmbeddedAttemptWithBackend(...)` délègue au harnais d'agent sélectionné :

- `src/agents/pi-embedded-runner/run/backend.ts`
- `src/agents/harness/selection.ts`

Le harnais du serveur d'application Codex est enregistré par le plugin Codex bundlé :

- `extensions/codex/index.ts`
- `extensions/codex/harness.ts`

L'implémentation du harnais Codex reçoit les mêmes `EmbeddedRunAttemptParams` que les tentatives soutenues par PI :

- `extensions/codex/src/app-server/run-attempt.ts`

Cela signifie que le point d'accroche requis se trouve dans le code contrôlé par OpenClaw. La limite externe est le protocole du serveur d'application Codex lui-même : OpenClaw peut contrôler ce qu'il envoie à `thread/start`, `thread/resume` et `turn/start`, et peut observer les notifications, mais il ne peut pas modifier le magasin de thread interne de Codex ou le compacteur natif.

## Lacune actuelle

Les tentatives PI embarquées appellent directement le cycle de vie du moteur de contexte :

- bootstrap/maintenance avant la tentative
- assemblage avant l'appel du modèle
- afterTurn ou ingest après la tentative
- maintenance après un tour réussi
- compaction du moteur de contexte pour les moteurs qui possèdent la compaction

Code PI pertinent :

- `src/agents/pi-embedded-runner/run/attempt.ts`
- `src/agents/pi-embedded-runner/run/attempt.context-engine-helpers.ts`
- `src/agents/pi-embedded-runner/context-engine-maintenance.ts`

Les tentatives du serveur d'application Codex exécutent actuellement des hooks de harnais d'agent générique et reflètent la transcription, mais n'appellent pas `params.contextEngine.bootstrap`, `params.contextEngine.assemble`, `params.contextEngine.afterTurn`, `params.contextEngine.ingestBatch`, `params.contextEngine.ingest` ou `params.contextEngine.maintain`.

Code Codex pertinent :

- `extensions/codex/src/app-server/run-attempt.ts`
- `extensions/codex/src/app-server/thread-lifecycle.ts`
- `extensions/codex/src/app-server/event-projector.ts`
- `extensions/codex/src/app-server/compact.ts`

## Comportement souhaité

Pour les tours du harnais Codex, OpenClaw devrait préserver ce cycle de vie :

1. Lire la transcription de la session OpenClaw reflétée.
2. Bootstrapper le moteur de contexte actif quand un fichier de session précédent existe.
3. Exécuter la maintenance du bootstrap quand disponible.
4. Assembler le contexte en utilisant le moteur de contexte actif.
5. Convertir le contexte assemblé en entrées compatibles avec Codex.
6. Démarrer ou reprendre le thread Codex avec des instructions de développeur qui incluent tout `systemPromptAddition` du moteur de contexte.
7. Démarrer le tour Codex avec l'invite orientée utilisateur assemblée.
8. Refléter le résultat Codex dans la transcription OpenClaw.
9. Appeler `afterTurn` si implémenté, sinon `ingestBatch`/`ingest`, en utilisant l'instantané de transcription reflété.
10. Exécuter la maintenance du tour après les tours réussis non-abandonnés.
11. Préserver les signaux de compaction natifs Codex et les hooks de compaction OpenClaw.

## Contraintes de conception

### Le serveur d'application Codex reste canonique pour l'état du thread natif

Codex possède son thread natif et tout historique étendu interne. OpenClaw ne devrait pas essayer de muter l'historique interne du serveur d'application sauf par les appels de protocole supportés.

Le miroir de transcription d'OpenClaw reste la source pour les fonctionnalités OpenClaw :

- historique de chat
- recherche
- comptabilité `/new` et `/reset`
- commutation future de modèle ou de harnais
- état du plugin du moteur de contexte

### L'assemblage du moteur de contexte doit être projeté dans les entrées Codex

L'interface du moteur de contexte retourne `AgentMessage[]` OpenClaw, pas un patch de thread Codex. Le serveur d'application Codex `turn/start` accepte une entrée utilisateur actuelle, tandis que `thread/start` et `thread/resume` acceptent des instructions de développeur.

Par conséquent, l'implémentation a besoin d'une couche de projection. La première version sûre devrait éviter de prétendre pouvoir remplacer l'historique interne de Codex. Elle devrait injecter le contexte assemblé comme matériel d'invite/instruction de développeur déterministe autour du tour actuel.

### La stabilité du cache d'invite est importante

Pour les moteurs comme lossless-claw, le contexte assemblé devrait être déterministe pour les entrées inchangées. N'ajoutez pas d'horodatages, d'identifiants aléatoires ou d'ordonnancement non-déterministe au texte de contexte généré.

### La sémantique de secours PI ne change pas

La sélection du harnais reste telle quelle :

- `runtime: "pi"` force PI
- `runtime: "codex"` sélectionne le harnais Codex enregistré
- `runtime: "auto"` laisse les harnais de plugin réclamer les fournisseurs supportés
- `fallback: "none"` désactive le secours PI quand aucun harnais de plugin ne correspond

Ce travail change ce qui se passe après la sélection du harnais Codex.

## Plan de mise en œuvre

### 1. Exporter ou relocaliser les assistants réutilisables du moteur de contexte

Aujourd'hui, les assistants de cycle de vie réutilisables se trouvent sous le runner PI :

- `src/agents/pi-embedded-runner/run/attempt.context-engine-helpers.ts`
- `src/agents/pi-embedded-runner/run/attempt.prompt-helpers.ts`
- `src/agents/pi-embedded-runner/context-engine-maintenance.ts`

Codex ne devrait pas importer à partir d'un chemin d'implémentation dont le nom implique PI si nous
pouvons l'éviter.

Créer un module neutre pour le harnais, par exemple :

- `src/agents/harness/context-engine-lifecycle.ts`

Déplacer ou réexporter :

- `runAttemptContextEngineBootstrap`
- `assembleAttemptContextEngine`
- `finalizeAttemptContextEngineTurn`
- `buildAfterTurnRuntimeContext`
- `buildAfterTurnRuntimeContextFromUsage`
- un petit wrapper autour de `runContextEngineMaintenance`

Garder les imports PI fonctionnels soit en réexportant à partir des anciens fichiers, soit en mettant à jour les sites d'appel PI dans la même PR.

Les noms d'assistants neutres ne doivent pas mentionner PI.

Noms suggérés :

- `bootstrapHarnessContextEngine`
- `assembleHarnessContextEngine`
- `finalizeHarnessContextEngineTurn`
- `buildHarnessContextEngineRuntimeContext`
- `runHarnessContextEngineMaintenance`

### 2. Ajouter un assistant de projection de contexte Codex

Ajouter un nouveau module :

- `extensions/codex/src/app-server/context-engine-projection.ts`

Responsabilités :

- Accepter le `AgentMessage[]` assemblé, l'historique en miroir original et l'invite actuelle.
- Déterminer quel contexte appartient aux instructions du développeur par rapport à l'entrée utilisateur actuelle.
- Préserver l'invite utilisateur actuelle comme demande actionnable finale.
- Rendre les messages antérieurs dans un format stable et explicite.
- Éviter les métadonnées volatiles.

API proposée :

```ts
export type CodexContextProjection = {
  developerInstructionAddition?: string;
  promptText: string;
  assembledMessages: AgentMessage[];
  prePromptMessageCount: number;
};

export function projectContextEngineAssemblyForCodex(params: {
  assembledMessages: AgentMessage[];
  originalHistoryMessages: AgentMessage[];
  prompt: string;
  systemPromptAddition?: string;
}): CodexContextProjection;
```

Projection recommandée en premier :

- Mettre `systemPromptAddition` dans les instructions du développeur.
- Mettre le contexte de la transcription assemblée avant l'invite actuelle dans `promptText`.
- L'étiqueter clairement comme contexte assemblé OpenClaw.
- Garder l'invite actuelle en dernier.
- Exclure l'invite utilisateur actuelle dupliquée si elle apparaît déjà à la fin.

Exemple de forme d'invite :

```text
Contexte assemblé OpenClaw pour ce tour :

<conversation_context>
[user]
...

[assistant]
...
</conversation_context>

Demande utilisateur actuelle :
...
```

C'est moins élégant que la chirurgie d'historique native de Codex, mais c'est implémentable
à l'intérieur d'OpenClaw et préserve la sémantique du moteur de contexte.

Amélioration future : si le serveur d'application Codex expose un protocole pour remplacer ou
compléter l'historique des threads, remplacer cette couche de projection pour utiliser cette API.

### 3. Câbler l'amorçage avant le démarrage du thread Codex

Dans `extensions/codex/src/app-server/run-attempt.ts` :

- Lire l'historique de session en miroir comme aujourd'hui.
- Déterminer si le fichier de session existait avant cette exécution. Préférer un assistant
  qui vérifie `fs.stat(params.sessionFile)` avant les écritures en miroir.
- Ouvrir un `SessionManager` ou utiliser un adaptateur de gestionnaire de session étroit si l'assistant
  l'exige.
- Appeler l'assistant d'amorçage neutre quand `params.contextEngine` existe.

Pseudo-flux :

```ts
const hadSessionFile = await fileExists(params.sessionFile);
const sessionManager = SessionManager.open(params.sessionFile);
const historyMessages = sessionManager.buildSessionContext().messages;

await bootstrapHarnessContextEngine({
  hadSessionFile,
  contextEngine: params.contextEngine,
  sessionId: params.sessionId,
  sessionKey: sandboxSessionKey,
  sessionFile: params.sessionFile,
  sessionManager,
  runtimeContext: buildHarnessContextEngineRuntimeContext(...),
  runMaintenance: runHarnessContextEngineMaintenance,
  warn,
});
```

Utiliser la même convention `sessionKey` que le pont d'outil Codex et le miroir de transcription. Aujourd'hui, Codex calcule `sandboxSessionKey` à partir de `params.sessionKey` ou
`params.sessionId` ; utiliser cela de manière cohérente sauf s'il y a une raison de préserver
`params.sessionKey` brut.

### 4. Câbler l'assemblage avant `thread/start` / `thread/resume` et `turn/start`

Dans `runCodexAppServerAttempt` :

1. Construire d'abord les outils dynamiques, afin que le moteur de contexte voie les noms d'outils réellement disponibles.
2. Lire l'historique de session en miroir.
3. Exécuter l'assemblage du moteur de contexte `assemble(...)` quand `params.contextEngine` existe.
4. Projeter le résultat assemblé dans :
   - ajout d'instruction du développeur
   - texte d'invite pour `turn/start`

L'appel de hook existant :

```ts
resolveAgentHarnessBeforePromptBuildResult({
  prompt: params.prompt,
  developerInstructions: buildDeveloperInstructions(params),
  messages: historyMessages,
  ctx: hookContext,
});
```

devrait devenir conscient du contexte :

1. calculer les instructions du développeur de base avec `buildDeveloperInstructions(params)`
2. appliquer l'assemblage/projection du moteur de contexte
3. exécuter `before_prompt_build` avec l'invite/les instructions du développeur projetées

Cet ordre permet aux hooks d'invite génériques de voir la même invite que Codex recevra. Si
nous avons besoin d'une parité PI stricte, exécuter l'assemblage du moteur de contexte avant la composition des hooks,
car PI applique le `systemPromptAddition` du moteur de contexte à l'invite système finale
après son pipeline d'invite. L'invariant important est que le moteur de contexte et les hooks obtiennent tous deux un ordre
déterministe et documenté.

Ordre recommandé pour la première implémentation :

1. `buildDeveloperInstructions(params)`
2. moteur de contexte `assemble()`
3. ajouter/préfixer `systemPromptAddition` aux instructions du développeur
4. projeter les messages assemblés dans le texte d'invite
5. `resolveAgentHarnessBeforePromptBuildResult(...)`
6. passer les instructions du développeur finales à `startOrResumeThread(...)`
7. passer le texte d'invite final à `buildTurnStartParams(...)`

La spécification doit être codée dans les tests afin que les modifications futures ne la réordonnent pas
accidentellement.

### 5. Préserver le formatage stable du cache d'invite

L'assistant de projection doit produire une sortie stable en octets pour des entrées identiques :

- ordre de message stable
- étiquettes de rôle stables
- pas d'horodatages générés
- pas de fuite d'ordre de clés d'objet
- pas de délimiteurs aléatoires
- pas d'ids par exécution

Utiliser des délimiteurs fixes et des sections explicites.

### 6. Câbler post-tour après la mise en miroir de la transcription

Le `CodexAppServerEventProjector` de Codex construit un `messagesSnapshot` local pour le
tour actuel. `mirrorTranscriptBestEffort(...)` écrit cet instantané dans le miroir de transcription OpenClaw.

Après la réussite ou l'échec de la mise en miroir, appeler le finaliseur du moteur de contexte avec le
meilleur instantané de message disponible :

- Préférer le contexte de session en miroir complet après l'écriture, car `afterTurn`
  s'attend à l'instantané de session, pas seulement au tour actuel.
- Revenir à `historyMessages + result.messagesSnapshot` si le fichier de session
  ne peut pas être rouvert.

Pseudo-flux :

```ts
const prePromptMessageCount = historyMessages.length;
await mirrorTranscriptBestEffort(...);
const finalMessages = readMirroredSessionHistoryMessages(params.sessionFile)
  ?? [...historyMessages, ...result.messagesSnapshot];

await finalizeHarnessContextEngineTurn({
  contextEngine: params.contextEngine,
  promptError: Boolean(finalPromptError),
  aborted: finalAborted,
  yieldAborted,
  sessionIdUsed: params.sessionId,
  sessionKey: sandboxSessionKey,
  sessionFile: params.sessionFile,
  messagesSnapshot: finalMessages,
  prePromptMessageCount,
  tokenBudget: params.contextTokenBudget,
  runtimeContext: buildHarnessContextEngineRuntimeContextFromUsage({
    attempt: params,
    workspaceDir: effectiveWorkspace,
    agentDir,
    tokenBudget: params.contextTokenBudget,
    lastCallUsage: result.attemptUsage,
    promptCache: result.promptCache,
  }),
  runMaintenance: runHarnessContextEngineMaintenance,
  sessionManager,
  warn,
});
```

Si la mise en miroir échoue, appeler quand même `afterTurn` avec l'instantané de secours, mais enregistrer
que le moteur de contexte ingère à partir de données de tour de secours.

### 7. Normaliser l'utilisation et le contexte d'exécution du cache d'invite

Les résultats de Codex incluent l'utilisation normalisée à partir des notifications de jetons du serveur d'application quand disponible. Passer cette utilisation dans le contexte d'exécution du moteur de contexte.

Si le serveur d'application Codex expose éventuellement les détails de lecture/écriture du cache, les mapper dans
`ContextEnginePromptCacheInfo`. Jusqu'à présent, omettre `promptCache` plutôt que
d'inventer des zéros.

### 8. Politique de compaction

Il y a deux systèmes de compaction :

1. Moteur de contexte OpenClaw `compact()`
2. Thread natif Codex app-server `/compact/start`

Ne pas les confluer silencieusement.

#### `/compact` et compaction OpenClaw explicite

Quand le moteur de contexte sélectionné a `info.ownsCompaction === true`, la compaction OpenClaw explicite
devrait préférer le résultat `compact()` du moteur de contexte pour le miroir de transcription OpenClaw et l'état du plugin.

Quand le harnais Codex sélectionné a une liaison de thread native, nous pouvons également
demander la compaction native Codex pour garder le thread du serveur d'application sain, mais cela
doit être signalé comme une action backend séparée dans les détails.

Comportement recommandé :

- Si `contextEngine.info.ownsCompaction === true` :
  - appeler d'abord le moteur de contexte `compact()`
  - puis appeler au mieux la compaction native Codex quand une liaison de thread existe
  - retourner le résultat du moteur de contexte comme résultat principal
  - inclure l'état de compaction native Codex dans `details.codexNativeCompaction`
- Si le moteur de contexte actif ne possède pas la compaction :
  - préserver le comportement de compaction native Codex actuel

Cela nécessite probablement de modifier `extensions/codex/src/app-server/compact.ts` ou
de l'envelopper à partir du chemin de compaction générique, selon où
`maybeCompactAgentHarnessSession(...)` est invoqué.

#### Événements de contextCompaction natifs Codex en cours de tour

Codex peut émettre des événements d'élément `contextCompaction` pendant un tour. Garder l'émission de hook de compaction avant/après actuelle dans `event-projector.ts`, mais ne pas traiter
cela comme une compaction du moteur de contexte complétée.

Pour les moteurs qui possèdent la compaction, émettre un diagnostic explicite quand Codex effectue quand même
la compaction native :

- nom du flux/événement : le flux `compaction` existant est acceptable
- détails : `{ backend: "codex-app-server", ownsCompaction: true }`

Cela rend la division auditable.

### 9. Comportement de réinitialisation de session et de liaison

Le `reset(...)` du harnais Codex existant efface la liaison du serveur d'application Codex du
fichier de session OpenClaw. Préserver ce comportement.

Aussi s'assurer que le nettoyage de l'état du moteur de contexte continue de se produire via les chemins de cycle de vie de session OpenClaw existants. Ne pas ajouter de nettoyage spécifique à Codex sauf si le
cycle de vie du moteur de contexte manque actuellement les événements de réinitialisation/suppression pour tous les harnais.

### 10. Gestion des erreurs

Suivre la sémantique PI :

- les échecs d'amorçage avertissent et continuent
- les échecs d'assemblage avertissent et reviennent aux messages de pipeline non assemblés/invite
- les échecs afterTurn/ingest avertissent et marquent la finalisation post-tour comme non réussie
- la maintenance s'exécute uniquement après les tours réussis, non abandonnés, non-yield
- les erreurs de compaction ne doivent pas être réessayées comme des invites fraîches

Ajouts spécifiques à Codex :

- Si la projection de contexte échoue, avertir et revenir à l'invite originale.
- Si la mise en miroir de transcription échoue, tenter quand même la finalisation du moteur de contexte avec des messages de secours.
- Si la compaction native Codex échoue après la réussite de la compaction du moteur de contexte,
  ne pas échouer la compaction OpenClaw entière quand le moteur de contexte est principal.

## Plan de test

### Tests unitaires

Ajouter des tests sous `extensions/codex/src/app-server`:

1. `run-attempt.context-engine.test.ts`
   - Codex appelle `bootstrap` quand un fichier de session existe.
   - Codex appelle `assemble` avec les messages en miroir, le budget de tokens, les noms d'outils,
     le mode citations, l'ID du modèle et le prompt.
   - `systemPromptAddition` est inclus dans les instructions du développeur.
   - Les messages assemblés sont projetés dans le prompt avant la requête actuelle.
   - Codex appelle `afterTurn` après le mirroring de la transcription.
   - Sans `afterTurn`, Codex appelle `ingestBatch` ou `ingest` par message.
   - La maintenance des tours s'exécute après les tours réussis.
   - La maintenance des tours ne s'exécute pas en cas d'erreur de prompt, d'abandon ou d'abandon de rendement.

2. `context-engine-projection.test.ts`
   - sortie stable pour des entrées identiques
   - pas de prompt actuel dupliqué quand l'historique assemblé l'inclut
   - gère l'historique vide
   - préserve l'ordre des rôles
   - inclut l'ajout de prompt système uniquement dans les instructions du développeur

3. `compact.context-engine.test.ts`
   - le résultat principal du moteur de contexte propriétaire gagne
   - Le statut de compaction natif Codex apparaît dans les détails quand aussi tenté
   - L'échec natif Codex ne fait pas échouer la compaction du moteur de contexte propriétaire
   - le moteur de contexte non-propriétaire préserve le comportement de compaction natif actuel

### Tests existants à mettre à jour

- `extensions/codex/src/app-server/run-attempt.test.ts` s'il existe, sinon
  les tests de run app-server Codex les plus proches.
- `extensions/codex/src/app-server/event-projector.test.ts` uniquement si les détails d'événement de compaction changent.
- `src/agents/harness/selection.test.ts` ne devrait pas nécessiter de modifications sauf si le comportement de configuration change;
  il devrait rester stable.
- Les tests du moteur de contexte PI devraient continuer à passer sans modification.

### Tests d'intégration / tests en direct

Ajouter ou étendre les tests de fumée du harnais Codex en direct:

- configurer `plugins.slots.contextEngine` sur un moteur de test
- configurer `agents.defaults.model` sur un modèle `codex/*`
- configurer `agents.defaults.embeddedHarness.runtime = "codex"`
- affirmer que le moteur de test a observé:
  - bootstrap
  - assemble
  - afterTurn ou ingest
  - maintenance

Éviter de nécessiter lossless-claw dans les tests du noyau OpenClaw. Utiliser un petit plugin de moteur de contexte factice dans le dépôt.

## Observabilité

Ajouter des logs de débogage autour des appels du cycle de vie du moteur de contexte Codex:

- `codex context engine bootstrap started/completed/failed`
- `codex context engine assemble applied`
- `codex context engine finalize completed/failed`
- `codex context engine maintenance skipped` avec raison
- `codex native compaction completed alongside context-engine compaction`

Éviter de logger les prompts complets ou le contenu de la transcription.

Ajouter des champs structurés où utile:

- `sessionId`
- `sessionKey` masqué ou omis selon la pratique de logging existante
- `engineId`
- `threadId`
- `turnId`
- `assembledMessageCount`
- `estimatedTokens`
- `hasSystemPromptAddition`

## Migration / compatibilité

Cela devrait être rétro-compatible:

- Si aucun moteur de contexte n'est configuré, le comportement du moteur de contexte hérité devrait
  être équivalent au comportement actuel du harnais Codex.
- Si l'`assemble` du moteur de contexte échoue, Codex devrait continuer avec le chemin de prompt original.
- Les liaisons de thread Codex existantes devraient rester valides.
- L'empreinte digitale d'outil dynamique ne devrait pas inclure la sortie du moteur de contexte; sinon
  chaque changement de contexte pourrait forcer un nouveau thread Codex. Seul le catalogue d'outils
  devrait affecter l'empreinte digitale d'outil dynamique.

## Questions ouvertes

1. Le contexte assemblé devrait-il être injecté entièrement dans le prompt utilisateur, entièrement
   dans les instructions du développeur, ou divisé?

   Recommandation: divisé. Mettre `systemPromptAddition` dans les instructions du développeur;
   mettre le contexte de transcription assemblé dans le wrapper de prompt utilisateur. Cela correspond mieux
   au protocole Codex actuel sans muter l'historique de thread natif.

2. La compaction natif Codex devrait-elle être désactivée quand un moteur de contexte possède
   la compaction?

   Recommandation: non, pas initialement. La compaction natif Codex peut toujours être
   nécessaire pour garder le thread app-server actif. Mais elle doit être rapportée comme
   compaction Codex natif, pas comme compaction du moteur de contexte.

3. `before_prompt_build` devrait-il s'exécuter avant ou après l'assemblage du moteur de contexte?

   Recommandation: après la projection du moteur de contexte pour Codex, afin que les hooks du harnais générique
   voient le prompt/les instructions du développeur réels que Codex recevra. Si la parité PI nécessite
   le contraire, encoder l'ordre choisi dans les tests et le documenter ici.

4. L'app-server Codex peut-il accepter un futur remplacement de contexte/historique structuré?

   Inconnu. Si c'est le cas, remplacer la couche de projection de texte par ce protocole et
   garder les appels du cycle de vie inchangés.

## Critères d'acceptation

- Un tour de harnais intégré `codex/*` invoque le cycle de vie d'assemblage du moteur de contexte sélectionné.
- Une `systemPromptAddition` du moteur de contexte affecte les instructions du développeur Codex.
- Le contexte assemblé affecte l'entrée du tour Codex de manière déterministe.
- Les tours Codex réussis appellent `afterTurn` ou le fallback ingest.
- Les tours Codex réussis exécutent la maintenance des tours du moteur de contexte.
- Les tours échoués/abandonnés/abandon de rendement ne exécutent pas la maintenance des tours.
- La compaction possédée par le moteur de contexte reste principale pour l'état OpenClaw/plugin.
- La compaction natif Codex reste auditable comme comportement Codex natif.
- Le comportement existant du moteur de contexte PI est inchangé.
- Le comportement existant du harnais Codex est inchangé quand aucun moteur de contexte non-hérité
  n'est sélectionné ou quand l'assemblage échoue.
