# Enquête sur la duplication d'achèvement d'exécution asynchrone

## Portée

- Session : `agent:main:telegram:group:-1003774691294:topic:1`
- Symptôme : le même achèvement d'exécution asynchrone pour la session/exécution `keen-nexus` a été enregistré deux fois dans LCM en tant que tours utilisateur.
- Objectif : déterminer s'il s'agit très probablement d'une injection de session dupliquée ou d'une simple tentative de livraison sortante.

## Conclusion

Il s'agit très probablement d'une **injection de session dupliquée**, et non d'une simple tentative de livraison sortante.

L'écart le plus important du côté de la passerelle se trouve dans le **chemin d'achèvement d'exécution du nœud** :

1. Un achèvement d'exécution côté nœud émet `exec.finished` avec le `runId` complet.
2. La passerelle `server-node-events` convertit cela en événement système et demande un battement de cœur.
3. Le battement de cœur injecte le bloc d'événement système drainé dans l'invite de l'agent.
4. Le runner intégré persiste cette invite en tant que nouveau tour utilisateur dans la transcription de session.

Si le même `exec.finished` atteint la passerelle deux fois pour le même `runId` pour une raison quelconque (relecture, doublon de reconnexion, renvoi en amont, producteur dupliqué), OpenClaw n'a actuellement **aucune vérification d'idempotence clé par `runId`/`contextKey`** sur ce chemin. La deuxième copie deviendra un deuxième message utilisateur avec le même contenu.

## Chemin de code exact

### 1. Producteur : événement d'achèvement d'exécution du nœud

- `src/node-host/invoke.ts:340-360`
  - `sendExecFinishedEvent(...)` émet `node.event` avec l'événement `exec.finished`.
  - La charge utile inclut `sessionKey` et le `runId` complet.

### 2. Ingestion d'événement de la passerelle

- `src/gateway/server-node-events.ts:574-640`
  - Gère `exec.finished`.
  - Construit le texte :
    - `Exec finished (node=..., id=<runId>, code ...)`
  - L'enfile via :
    - `enqueueSystemEvent(text, { sessionKey, contextKey: runId ? \`exec:${runId}\` : "exec", trusted: false })`
  - Demande immédiatement un réveil :
    - `requestHeartbeatNow(scopedHeartbeatWakeOptions(sessionKey, { reason: "exec-event" }))`

### 3. Faiblesse de la déduplication d'événement système

- `src/infra/system-events.ts:90-115`
  - `enqueueSystemEvent(...)` supprime uniquement les **doublons de texte consécutifs** :
    - `if (entry.lastText === cleaned) return false`
  - Il stocke `contextKey`, mais **n'utilise pas** `contextKey` pour l'idempotence.
  - Après drainage, la suppression des doublons se réinitialise.

Cela signifie qu'un `exec.finished` relu avec le même `runId` peut être accepté à nouveau plus tard, même si le code avait déjà un candidat d'idempotence stable (`exec:<runId>`).

### 4. La gestion du réveil n'est pas le principal duplicateur

- `src/infra/heartbeat-wake.ts:79-117`
  - Les réveils sont fusionnés par `(agentId, sessionKey)`.
  - Les demandes de réveil dupliquées pour la même cible s'effondrent en une seule entrée de réveil en attente.

Cela rend la **gestion des réveils dupliqués seule** une explication plus faible que l'ingestion d'événement dupliquée.

### 5. Le battement de cœur consomme l'événement et le transforme en entrée d'invite

- `src/infra/heartbeat-runner.ts:535-574`
  - Le contrôle préalable examine les événements système en attente et classe les exécutions d'événement exec.
- `src/auto-reply/reply/session-system-events.ts:86-90`
  - `drainFormattedSystemEvents(...)` draine la file d'attente pour la session.
- `src/auto-reply/reply/get-reply-run.ts:400-427`
  - Le bloc d'événement système drainé est ajouté au début du corps de l'invite de l'agent.

### 6. Point d'injection de transcription

- `src/agents/pi-embedded-runner/run/attempt.ts:2000-2017`
  - `activeSession.prompt(effectivePrompt)` soumet l'invite complète à la session PI intégrée.
  - C'est le point où l'invite dérivée de l'achèvement devient un tour utilisateur persistant.

Donc une fois que le même événement système est reconstruit dans l'invite deux fois, les messages utilisateur LCM dupliqués sont attendus.

## Pourquoi la simple tentative de livraison sortante est moins probable

Il existe un vrai chemin d'échec sortant dans le runner de battement de cœur :

- `src/infra/heartbeat-runner.ts:1194-1242`
  - La réponse est générée en premier.
  - La livraison sortante se fait plus tard via `deliverOutboundPayloads(...)`.
  - L'échec là retourne `{ status: "failed" }`.

Cependant, pour la même entrée de file d'attente d'événement système, cela seul **n'est pas suffisant** pour expliquer les tours utilisateur dupliqués :

- `src/auto-reply/reply/session-system-events.ts:86-90`
  - La file d'attente d'événement système est déjà drainée avant la livraison sortante.

Donc une tentative d'envoi de canal par elle-même ne recréerait pas le même événement en file d'attente. Elle pourrait expliquer une livraison externe manquante/échouée, mais pas par elle-même un deuxième message utilisateur de session identique.

## Possibilité secondaire, de confiance inférieure

Il y a une boucle de tentative de course complète dans le runner d'agent :

- `src/auto-reply/reply/agent-runner-execution.ts:741-1473`
  - Certains échecs transitoires peuvent réessayer la course entière et renvoyer le même `commandBody`.

Cela peut dupliquer une invite utilisateur persistante **dans la même exécution de réponse** si l'invite a déjà été ajoutée avant que la condition de tentative ne se déclenche.

Je classe cela plus bas que l'ingestion dupliquée de `exec.finished` parce que :

- l'écart observé était d'environ 51 secondes, ce qui ressemble plus à un deuxième réveil/tour qu'à une tentative en processus ;
- le rapport mentionne déjà des échecs d'envoi de message répétés, ce qui pointe plus vers un tour ultérieur séparé qu'une tentative immédiate de modèle/runtime.

## Hypothèse de cause première

Hypothèse de plus haute confiance :

- L'achèvement de `keen-nexus` est passé par le **chemin d'événement d'exécution du nœud**.
- Le même `exec.finished` a été livré à `server-node-events` deux fois.
- La passerelle a accepté les deux parce que `enqueueSystemEvent(...)` ne déduplique pas par `contextKey` / `runId`.
- Chaque événement accepté a déclenché un battement de cœur et a été injecté en tant que tour utilisateur dans la transcription PI.

## Correctif chirurgical minuscule proposé

Si un correctif est souhaité, le plus petit changement de haute valeur est :

- faire en sorte que l'idempotence d'événement exec/système honore `contextKey` pour un horizon court, au moins pour les répétitions exactes `(sessionKey, contextKey, text)` ;
- ou ajouter une déduplication dédiée dans `server-node-events` pour `exec.finished` clé par `(sessionKey, runId, event kind)`.

Cela bloquerait directement les doublons `exec.finished` relus avant qu'ils ne deviennent des tours de session.
