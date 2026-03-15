---
summary: "Intégrer les agents de codage ACP via un plan de contrôle ACP de première classe dans les runtimes core et plugin-backed (acpx en premier)"
owner: "onutc"
status: "draft"
last_updated: "2026-02-25"
title: "Agents ACP liés aux threads"
---

# Agents ACP liés aux threads

## Aperçu

Ce plan définit comment OpenClaw devrait supporter les agents de codage ACP dans les canaux compatibles avec les threads (Discord en premier) avec un cycle de vie et une récupération au niveau de la production.

Document connexe :

- [Plan de refactorisation du streaming unifié ACP](/fr/experiments/plans/acp-unified-streaming-refactor)

Expérience utilisateur cible :

- un utilisateur crée ou concentre une session ACP dans un thread
- les messages de l'utilisateur dans ce thread sont acheminés vers la session ACP liée
- la sortie de l'agent est diffusée en continu vers le même persona de thread
- la session peut être persistante ou ponctuelle avec des contrôles de nettoyage explicites

## Résumé des décisions

La recommandation à long terme est une architecture hybride :

- Le core OpenClaw possède les préoccupations du plan de contrôle ACP
  - identité et métadonnées de session
  - décisions de liaison et d'acheminement des threads
  - invariants de livraison et suppression des doublons
  - sémantique de nettoyage du cycle de vie et récupération
- Le backend runtime ACP est enfichable
  - le premier backend est un service plugin soutenu par acpx
  - le runtime gère le transport ACP, la mise en file d'attente, l'annulation, la reconnexion

OpenClaw ne devrait pas réimplémenter les éléments internes du transport ACP dans le core.
OpenClaw ne devrait pas dépendre d'un chemin d'interception pur plugin uniquement pour l'acheminement.

## Architecture nord-étoile (le graal)

Traiter ACP comme un plan de contrôle de première classe dans OpenClaw, avec des adaptateurs runtime enfichables.

Invariants non négociables :

- chaque liaison de thread ACP référence un enregistrement de session ACP valide
- chaque session ACP a un état de cycle de vie explicite (`creating`, `idle`, `running`, `cancelling`, `closed`, `error`)
- chaque exécution ACP a un état d'exécution explicite (`queued`, `running`, `completed`, `failed`, `cancelled`)
- spawn, bind et enqueue initial sont atomiques
- les tentatives de commande sont idempotentes (pas d'exécutions dupliquées ou de sorties Discord dupliquées)
- la sortie du canal du thread lié est une projection des événements d'exécution ACP, jamais des effets secondaires ad-hoc

Modèle de propriété à long terme :

- `AcpSessionManager` est le seul écrivain et orchestrateur ACP
- le gestionnaire vit d'abord dans le processus gateway ; peut être déplacé vers un sidecar dédié plus tard derrière la même interface
- par clé de session ACP, le gestionnaire possède un acteur en mémoire (exécution de commande sérialisée)
- les adaptateurs (`acpx`, futurs backends) sont uniquement des implémentations de transport/runtime

Modèle de persistance à long terme :

- déplacer l'état du plan de contrôle ACP vers un magasin SQLite dédié (mode WAL) sous le répertoire d'état OpenClaw
- garder `SessionEntry.acp` comme projection de compatibilité pendant la migration, pas comme source de vérité
- stocker les événements ACP en ajout uniquement pour supporter la relecture, la récupération après crash et la livraison déterministe

### Stratégie de livraison (pont vers le graal)

- pont à court terme
  - garder les mécaniques de liaison de thread actuels et la surface de configuration ACP existante
  - corriger les bugs d'écart de métadonnées et acheminer les tours ACP via une seule branche ACP core
  - ajouter des clés d'idempotence et des vérifications d'acheminement fail-closed immédiatement
- basculement à long terme
  - déplacer la source de vérité ACP vers la DB du plan de contrôle + acteurs
  - rendre la livraison du thread lié purement basée sur la projection d'événements
  - supprimer le comportement de secours hérité qui dépend des métadonnées de session-entry opportunistes

## Pourquoi pas plugin uniquement

Les hooks de plugin actuels ne sont pas suffisants pour l'acheminement de session ACP de bout en bout sans modifications du core.

- l'acheminement entrant de la liaison de thread se résout à une clé de session dans le dispatch core en premier
- les hooks de message sont fire-and-forget et ne peuvent pas court-circuiter le chemin de réponse principal
- les commandes de plugin sont bonnes pour les opérations de contrôle mais pas pour remplacer le flux de dispatch par tour du core

Résultat :

- le runtime ACP peut être enfichable
- la branche d'acheminement ACP doit exister dans le core

## Fondation existante à réutiliser

Déjà implémenté et devrait rester canonique :

- la cible de liaison de thread supporte `subagent` et `acp`
- l'override d'acheminement de thread entrant se résout par liaison avant le dispatch normal
- identité de thread sortant via webhook dans la livraison de réponse
- flux `/focus` et `/unfocus` avec compatibilité cible ACP
- magasin de liaison persistant avec restauration au démarrage
- sémantique de débind du cycle de vie sur archive, suppression, unfocus, reset et delete

Ce plan étend cette fondation plutôt que de la remplacer.

## Architecture

### Modèle de limite

Core (doit être dans le core OpenClaw) :

- branche de dispatch en mode session ACP dans le pipeline de réponse
- arbitrage de livraison pour éviter la duplication parent plus thread
- persistance du plan de contrôle ACP (avec projection de compatibilité `SessionEntry.acp` pendant la migration)
- sémantique de débind du cycle de vie et détachement runtime liés au reset/delete de session

Backend de plugin (implémentation acpx) :

- supervision du worker runtime ACP
- invocation du processus acpx et analyse des événements
- gestionnaires de commandes ACP (`/acp ...`) et UX opérateur
- défauts de configuration spécifiques au backend et diagnostics

### Modèle de propriété du runtime

- un processus gateway possède l'état d'orchestration ACP
- l'exécution ACP s'exécute dans des processus enfants supervisés via le backend acpx
- la stratégie de processus est longue durée par clé de session ACP active, pas par message

Cela évite le coût de démarrage à chaque invite et maintient les sémantiques d'annulation et de reconnexion fiables.

### Contrat runtime core

Ajouter un contrat runtime ACP core afin que le code d'acheminement ne dépende pas des détails CLI et puisse basculer les backends sans modifier la logique de dispatch :

```ts
export type AcpRuntimePromptMode = "prompt" | "steer";

export type AcpRuntimeHandle = {
  sessionKey: string;
  backend: string;
  runtimeSessionName: string;
};

export type AcpRuntimeEvent =
  | { type: "text_delta"; stream: "output" | "thought"; text: string }
  | { type: "tool_call"; name: string; argumentsText: string }
  | { type: "done"; usage?: Record<string, number> }
  | { type: "error"; code: string; message: string; retryable?: boolean };

export interface AcpRuntime {
  ensureSession(input: {
    sessionKey: string;
    agent: string;
    mode: "persistent" | "oneshot";
    cwd?: string;
    env?: Record<string, string>;
    idempotencyKey: string;
  }): Promise<AcpRuntimeHandle>;

  submit(input: {
    handle: AcpRuntimeHandle;
    text: string;
    mode: AcpRuntimePromptMode;
    idempotencyKey: string;
  }): Promise<{ runtimeRunId: string }>;

  stream(input: {
    handle: AcpRuntimeHandle;
    runtimeRunId: string;
    onEvent: (event: AcpRuntimeEvent) => Promise<void> | void;
    signal?: AbortSignal;
  }): Promise<void>;

  cancel(input: {
    handle: AcpRuntimeHandle;
    runtimeRunId?: string;
    reason?: string;
    idempotencyKey: string;
  }): Promise<void>;

  close(input: { handle: AcpRuntimeHandle; reason: string; idempotencyKey: string }): Promise<void>;

  health?(): Promise<{ ok: boolean; details?: string }>;
}
```

Détail d'implémentation :

- premier backend : `AcpxRuntime` livré en tant que service de plugin
- le core résout le runtime via le registre et échoue avec une erreur d'opérateur explicite quand aucun backend runtime ACP n'est disponible

### Modèle de données du plan de contrôle et persistance

La source de vérité à long terme est une base de données SQLite ACP dédiée (mode WAL), pour les mises à jour transactionnelles et la récupération sûre après crash :

- `acp_sessions`
  - `session_key` (pk), `backend`, `agent`, `mode`, `cwd`, `state`, `created_at`, `updated_at`, `last_error`
- `acp_runs`
  - `run_id` (pk), `session_key` (fk), `state`, `requester_message_id`, `idempotency_key`, `started_at`, `ended_at`, `error_code`, `error_message`
- `acp_bindings`
  - `binding_key` (pk), `thread_id`, `channel_id`, `account_id`, `session_key` (fk), `expires_at`, `bound_at`
- `acp_events`
  - `event_id` (pk), `run_id` (fk), `seq`, `kind`, `payload_json`, `created_at`
- `acp_delivery_checkpoint`
  - `run_id` (pk/fk), `last_event_seq`, `last_discord_message_id`, `updated_at`
- `acp_idempotency`
  - `scope`, `idempotency_key`, `result_json`, `created_at`, unique `(scope, idempotency_key)`

```ts
export type AcpSessionMeta = {
  backend: string;
  agent: string;
  runtimeSessionName: string;
  mode: "persistent" | "oneshot";
  cwd?: string;
  state: "idle" | "running" | "error";
  lastActivityAt: number;
  lastError?: string;
};
```

Règles de stockage :

- garder `SessionEntry.acp` comme projection de compatibilité pendant la migration
- les identifiants de processus et les sockets restent en mémoire uniquement
- l'état du cycle de vie durable et l'état d'exécution vivent dans la DB ACP, pas dans le JSON de session générique
- si le propriétaire du runtime meurt, la gateway réhydrate à partir de la DB ACP et reprend à partir des points de contrôle

### Acheminement et livraison

Entrant :

- garder la recherche de liaison de thread actuelle comme première étape d'acheminement
- si la cible de liaison est une session ACP, acheminer vers la branche runtime ACP au lieu de `getReplyFromConfig`
- la commande `/acp steer` explicite utilise `mode: "steer"`

Sortant :

- le flux d'événements ACP est normalisé en chunks de réponse OpenClaw
- la cible de livraison est résolue via le chemin de destination lié existant
- quand un thread lié est actif pour ce tour de session, la complétion du canal parent est supprimée

Politique de streaming :

- diffuser la sortie partielle avec fenêtre de coalescence
- intervalle minimum configurable et octets de chunk max pour rester sous les limites de débit Discord
- le message final est toujours émis à la complétion ou à l'échec

### Machines d'état et limites de transaction

Machine d'état de session :

- `creating -> idle -> running -> idle`
- `running -> cancelling -> idle | error`
- `idle -> closed`
- `error -> idle | closed`

Machine d'état d'exécution :

- `queued -> running -> completed`
- `running -> failed | cancelled`
- `queued -> cancelled`

Limites de transaction requises :

- transaction de spawn
  - créer une ligne de session ACP
  - créer/mettre à jour une ligne de liaison de thread ACP
  - enqueuer une ligne d'exécution initiale
- transaction de fermeture
  - marquer la session fermée
  - supprimer/expirer les lignes de liaison
  - écrire l'événement de fermeture final
- transaction d'annulation
  - marquer l'exécution cible annulation/annulée avec clé d'idempotence

Aucun succès partiel n'est autorisé à travers ces limites.

### Modèle d'acteur par session

`AcpSessionManager` exécute un acteur par clé de session ACP :

- la boîte aux lettres de l'acteur sérialise les effets secondaires `submit`, `cancel`, `close` et `stream`
- l'acteur possède l'hydratation du handle runtime et le cycle de vie du processus de l'adaptateur runtime pour cette session
- l'acteur écrit les événements d'exécution dans l'ordre (`seq`) avant toute livraison Discord
- l'acteur met à jour les points de contrôle de livraison après un envoi sortant réussi

Cela supprime les courses entre tours et empêche la sortie de thread dupliquée ou désordonnée.

### Idempotence et projection de livraison

Toutes les actions ACP externes doivent porter des clés d'idempotence :

- clé d'idempotence de spawn
- clé d'idempotence de prompt/steer
- clé d'idempotence d'annulation
- clé d'idempotence de fermeture

Règles de livraison :

- les messages Discord sont dérivés de `acp_events` plus `acp_delivery_checkpoint`
- les tentatives reprennent à partir du point de contrôle sans renvoyer les chunks déjà livrés
- l'émission de réponse finale est exactement une fois par exécution à partir de la logique de projection

### Récupération et auto-guérison

Au démarrage de la gateway :

- charger les sessions ACP non-terminales (`creating`, `idle`, `running`, `cancelling`, `error`)
- recréer les acteurs paresseusement au premier événement entrant ou avec enthousiasme sous un plafond configuré
- réconcilier toute exécution `running` manquant les battements de cœur et marquer `failed` ou récupérer via l'adaptateur

Au message de thread Discord entrant :

- si la liaison existe mais que la session ACP est manquante, échouer fermé avec un message de liaison obsolète explicite
- optionnellement auto-débind la liaison obsolète après validation sûre pour l'opérateur
- ne jamais acheminer silencieusement les liaisons ACP obsolètes vers le chemin LLM normal

### Cycle de vie et sécurité

Opérations supportées :

- annuler l'exécution actuelle : `/acp cancel`
- débind le thread : `/unfocus`
- fermer la session ACP : `/acp close`
- fermer automatiquement les sessions inactives par TTL effectif

Politique TTL :

- le TTL effectif est le minimum de
  - TTL global/session
  - TTL de liaison de thread Discord
  - TTL du propriétaire du runtime ACP

Contrôles de sécurité :

- liste blanche des agents ACP par nom
- restreindre les racines d'espace de travail pour les sessions ACP
- passthrough de liste blanche env
- sessions ACP concurrentes max par compte et globalement
- backoff de redémarrage borné pour les crashes runtime

## Surface de configuration

Clés principales :

- `acp.enabled`
- `acp.dispatch.enabled` (commutateur d'arrêt du routage ACP indépendant)
- `acp.backend` (par défaut `acpx`)
- `acp.defaultAgent`
- `acp.allowedAgents[]`
- `acp.maxConcurrentSessions`
- `acp.stream.coalesceIdleMs`
- `acp.stream.maxChunkChars`
- `acp.runtime.ttlMinutes`
- `acp.controlPlane.store` (`sqlite` par défaut)
- `acp.controlPlane.storePath`
- `acp.controlPlane.recovery.eagerActors`
- `acp.controlPlane.recovery.reconcileRunningAfterMs`
- `acp.controlPlane.checkpoint.flushEveryEvents`
- `acp.controlPlane.checkpoint.flushEveryMs`
- `acp.idempotency.ttlHours`
- `channels.discord.threadBindings.spawnAcpSessions`

Clés du plugin/backend (section du plugin acpx) :

- remplacements de commande/chemin du backend
- liste blanche des variables d'environnement du backend
- présets du backend par agent
- délais de démarrage/arrêt du backend
- exécutions maximales en vol par session du backend

## Spécification de mise en œuvre

### Modules du plan de contrôle (nouveaux)

Ajouter des modules dédiés du plan de contrôle ACP dans le noyau :

- `src/acp/control-plane/manager.ts`
  - possède les acteurs ACP, les transitions de cycle de vie, la sérialisation des commandes
- `src/acp/control-plane/store.ts`
  - gestion du schéma SQLite, transactions, assistants de requête
- `src/acp/control-plane/events.ts`
  - définitions d'événements ACP typés et sérialisation
- `src/acp/control-plane/checkpoint.ts`
  - points de contrôle de livraison durable et curseurs de relecture
- `src/acp/control-plane/idempotency.ts`
  - réservation de clé d'idempotence et relecture de réponse
- `src/acp/control-plane/recovery.ts`
  - réconciliation au démarrage et plan de réhydratation des acteurs

Modules de pont de compatibilité :

- `src/acp/runtime/session-meta.ts`
  - reste temporairement pour la projection dans `SessionEntry.acp`
  - doit cesser d'être la source de vérité après le basculement de migration

### Invariants requis (doivent être appliqués dans le code)

- la création de session ACP et la liaison de thread sont atomiques (transaction unique)
- il y a au maximum une exécution active par acteur de session ACP à la fois
- la séquence d'événements `seq` est strictement croissante par exécution
- le point de contrôle de livraison n'avance jamais au-delà du dernier événement validé
- la relecture d'idempotence retourne la charge utile de succès précédente pour les clés de commande en double
- les métadonnées ACP obsolètes/manquantes ne peuvent pas être acheminées vers le chemin de réponse normal non-ACP

### Points de contact du noyau

Fichiers principaux à modifier :

- `src/auto-reply/reply/dispatch-from-config.ts`
  - la branche ACP appelle `AcpSessionManager.submit` et la projection de livraison d'événements
  - supprimer le secours ACP direct qui contourne les invariants du plan de contrôle
- `src/auto-reply/reply/inbound-context.ts` (ou limite de contexte normalisée la plus proche)
  - exposer les clés de routage normalisées et les graines d'idempotence pour le plan de contrôle ACP
- `src/config/sessions/types.ts`
  - garder `SessionEntry.acp` comme champ de compatibilité de projection uniquement
- `src/gateway/server-methods/sessions.ts`
  - la réinitialisation/suppression/archivage doit appeler le chemin de transaction de fermeture/déliaison du gestionnaire ACP
- `src/infra/outbound/bound-delivery-router.ts`
  - appliquer le comportement de destination fermé en cas d'échec pour les tours de session liée ACP
- `src/discord/monitor/thread-bindings.ts`
  - ajouter des assistants de validation de liaison obsolète ACP câblés aux recherches du plan de contrôle
- `src/auto-reply/reply/commands-acp.ts`
  - acheminer spawn/cancel/close/steer via les API du gestionnaire ACP
- `src/agents/acp-spawn.ts`
  - arrêter les écritures de métadonnées ad hoc ; appeler la transaction de spawn du gestionnaire ACP
- `src/plugin-sdk/**` et pont d'exécution du plugin
  - exposer l'enregistrement du backend ACP et la sémantique de santé de manière propre

Fichiers principaux explicitement non remplacés :

- `src/discord/monitor/message-handler.preflight.ts`
  - garder le comportement de remplacement de liaison de thread comme le résolveur de clé de session canonique

### API du registre d'exécution ACP

Ajouter un module de registre principal :

- `src/acp/runtime/registry.ts`

API requise :

```ts
export type AcpRuntimeBackend = {
  id: string;
  runtime: AcpRuntime;
  healthy?: () => boolean;
};

export function registerAcpRuntimeBackend(backend: AcpRuntimeBackend): void;
export function unregisterAcpRuntimeBackend(id: string): void;
export function getAcpRuntimeBackend(id?: string): AcpRuntimeBackend | null;
export function requireAcpRuntimeBackend(id?: string): AcpRuntimeBackend;
```

Comportement :

- `requireAcpRuntimeBackend` lève une erreur de backend ACP manquant typée lorsqu'elle n'est pas disponible
- le service du plugin enregistre le backend au `start` et le désenregistre au `stop`
- les recherches d'exécution sont en lecture seule et locales au processus

### Contrat du plugin d'exécution acpx (détail de mise en œuvre)

Pour le premier backend de production (`extensions/acpx`), OpenClaw et acpx sont
connectés avec un contrat de commande strict :

- id du backend : `acpx`
- id du service du plugin : `acpx-runtime`
- encodage du handle d'exécution : `runtimeSessionName = acpx:v1:<base64url(json)>`
- champs de charge utile encodés :
  - `name` (session nommée acpx ; utilise `sessionKey` OpenClaw)
  - `agent` (commande d'agent acpx)
  - `cwd` (racine de l'espace de travail de la session)
  - `mode` (`persistent | oneshot`)

Mappage des commandes :

- assurer la session :
  - `acpx --format json --json-strict --cwd <cwd> <agent> sessions ensure --name <name>`
- tour d'invite :
  - `acpx --format json --json-strict --cwd <cwd> <agent> prompt --session <name> --file -`
- annuler :
  - `acpx --format json --json-strict --cwd <cwd> <agent> cancel --session <name>`
- fermer :
  - `acpx --format json --json-strict --cwd <cwd> <agent> sessions close <name>`

Streaming :

- OpenClaw consomme les événements ndjson de `acpx --format json --json-strict`
- `text` => `text_delta/output`
- `thought` => `text_delta/thought`
- `tool_call` => `tool_call`
- `done` => `done`
- `error` => `error`

### Patch du schéma de session

Patch `SessionEntry` dans `src/config/sessions/types.ts` :

```ts
type SessionAcpMeta = {
  backend: string;
  agent: string;
  runtimeSessionName: string;
  mode: "persistent" | "oneshot";
  cwd?: string;
  state: "idle" | "running" | "error";
  lastActivityAt: number;
  lastError?: string;
};
```

Champ persistant :

- `SessionEntry.acp?: SessionAcpMeta`

Règles de migration :

- phase A : double écriture (projection `acp` + source de vérité SQLite ACP)
- phase B : lecture primaire depuis SQLite ACP, lecture de secours depuis `SessionEntry.acp` hérité
- phase C : commande de migration remplit les lignes ACP manquantes à partir des entrées héritées valides
- phase D : supprimer la lecture de secours et garder la projection optionnelle pour l'UX uniquement
- les champs hérités (`cliSessionIds`, `claudeCliSessionId`) restent inchangés

### Contrat d'erreur

Ajouter des codes d'erreur ACP stables et des messages destinés à l'utilisateur :

- `ACP_BACKEND_MISSING`
  - message : `ACP runtime backend is not configured. Install and enable the acpx runtime plugin.`
- `ACP_BACKEND_UNAVAILABLE`
  - message : `ACP runtime backend is currently unavailable. Try again in a moment.`
- `ACP_SESSION_INIT_FAILED`
  - message : `Could not initialize ACP session runtime.`
- `ACP_TURN_FAILED`
  - message : `ACP turn failed before completion.`

Règles :

- retourner un message sûr et actionnable pour l'utilisateur dans le thread
- enregistrer l'erreur détaillée du backend/système uniquement dans les journaux d'exécution
- ne jamais revenir silencieusement au chemin LLM normal lorsque le routage ACP a été explicitement sélectionné

### Arbitrage de livraison en double

Règle de routage unique pour les tours liés ACP :

- si une liaison de thread active existe pour la session ACP cible et le contexte du demandeur, livrer uniquement à ce thread lié
- ne pas envoyer également au canal parent pour le même tour
- si la sélection de destination liée est ambiguë, échouer fermé avec une erreur explicite (pas de secours implicite au parent)
- si aucune liaison active n'existe, utiliser le comportement de destination de session normal

### Observabilité et préparation opérationnelle

Métriques requises :

- nombre de succès/échecs de spawn ACP par backend et code d'erreur
- percentiles de latence d'exécution ACP (attente en file d'attente, temps de tour d'exécution, temps de projection de livraison)
- nombre de redémarrages d'acteur ACP et raison du redémarrage
- nombre de détections de liaison obsolète
- taux de succès de relecture d'idempotence
- compteurs de relance de livraison Discord et de limite de débit

Journaux requis :

- journaux structurés clés par `sessionKey`, `runId`, `backend`, `threadId`, `idempotencyKey`
- journaux de transition d'état explicites pour les machines d'état de session et d'exécution
- journaux de commande d'adaptateur avec arguments sûrs pour la rédaction et résumé de sortie

Diagnostics requis :

- `/acp sessions` inclut l'état, l'exécution active, la dernière erreur et l'état de liaison
- `/acp doctor` (ou équivalent) valide l'enregistrement du backend, la santé du magasin et les liaisons obsolètes

### Précédence de configuration et valeurs effectives

Précédence d'activation ACP :

- remplacement de compte : `channels.discord.accounts.<id>.threadBindings.spawnAcpSessions`
- remplacement de canal : `channels.discord.threadBindings.spawnAcpSessions`
- portail ACP global : `acp.enabled`
- portail de dispatch : `acp.dispatch.enabled`
- disponibilité du backend : backend enregistré pour `acp.backend`

Comportement d'activation automatique :

- lorsque ACP est configuré (`acp.enabled=true`, `acp.dispatch.enabled=true`, ou
  `acp.backend=acpx`), l'activation automatique du plugin marque `plugins.entries.acpx.enabled=true`
  sauf s'il est sur liste noire ou explicitement désactivé

Valeur TTL effective :

- `min(session ttl, discord thread binding ttl, acp runtime ttl)`

### Carte de test

Tests unitaires :

- `src/acp/runtime/registry.test.ts` (nouveau)
- `src/auto-reply/reply/dispatch-from-config.acp.test.ts` (nouveau)
- `src/infra/outbound/bound-delivery-router.test.ts` (étendre les cas d'échec fermé ACP)
- `src/config/sessions/types.test.ts` ou tests de magasin de session les plus proches (persistance des métadonnées ACP)

Tests d'intégration :

- `src/discord/monitor/reply-delivery.test.ts` (comportement de destination de livraison ACP lié)
- `src/discord/monitor/message-handler.preflight*.test.ts` (continuité du routage de clé de session ACP lié)
- tests d'exécution du plugin acpx dans le package backend (enregistrement du service/démarrage/arrêt + normalisation d'événement)

Tests e2e de la passerelle :

- `src/gateway/server.sessions.gateway-server-sessions-a.e2e.test.ts` (étendre la couverture du cycle de vie de réinitialisation/suppression ACP)
- e2e de tour de thread ACP pour spawn, message, stream, cancel, unfocus, récupération de redémarrage

### Garde de déploiement

Ajouter un commutateur d'arrêt de dispatch ACP indépendant :

- `acp.dispatch.enabled` par défaut `false` pour la première version
- lorsque désactivé :
  - les commandes de contrôle spawn/focus ACP peuvent toujours lier les sessions
  - le chemin de dispatch ACP ne s'active pas
  - l'utilisateur reçoit un message explicite indiquant que le dispatch ACP est désactivé par la politique
- après validation du canari, la valeur par défaut peut être basculée à `true` dans une version ultérieure

## Plan de commande et UX

### Nouvelles commandes

- `/acp spawn <agent-id> [--mode persistent|oneshot] [--thread auto|here|off]`
- `/acp cancel [session]`
- `/acp steer <instruction>`
- `/acp close [session]`
- `/acp sessions`

### Compatibilité des commandes existantes

- `/focus <sessionKey>` continue de supporter les cibles ACP
- `/unfocus` conserve la sémantique actuelle
- `/session idle` et `/session max-age` remplacent l'ancien remplacement TTL

## Déploiement par phases

### Phase 0 ADR et gel du schéma

- livrer l'ADR pour la propriété du plan de contrôle ACP et les limites des adaptateurs
- geler le schéma DB (`acp_sessions`, `acp_runs`, `acp_bindings`, `acp_events`, `acp_delivery_checkpoint`, `acp_idempotency`)
- définir les codes d'erreur ACP stables, le contrat d'événement et les gardes de transition d'état

### Phase 1 Fondation du plan de contrôle dans le noyau

- implémenter `AcpSessionManager` et le runtime d'acteur par session
- implémenter le magasin ACP SQLite et les assistants de transaction
- implémenter le magasin d'idempotence et les assistants de relecture
- implémenter les modules d'ajout d'événement et de point de contrôle de livraison
- connecter les API spawn/cancel/close au gestionnaire avec garanties transactionnelles

### Phase 2 Intégration du routage principal et du cycle de vie

- router les tours ACP liés aux threads du pipeline de dispatch vers le gestionnaire ACP
- appliquer le routage fail-closed lorsque les invariants de liaison/session ACP échouent
- intégrer le cycle de vie reset/delete/archive/unfocus avec les transactions ACP close/unbind
- ajouter la détection de liaison obsolète et la politique d'auto-unbind optionnelle

### Phase 3 Adaptateur/plugin backend acpx

- implémenter l'adaptateur `acpx` par rapport au contrat runtime (`ensureSession`, `submit`, `stream`, `cancel`, `close`)
- ajouter les vérifications de santé du backend et l'enregistrement du démarrage/arrêt
- normaliser les événements ndjson acpx en événements runtime ACP
- appliquer les délais d'expiration du backend, la supervision des processus et la politique de redémarrage/backoff

### Phase 4 Projection de livraison et UX de canal (Discord en premier)

- implémenter la projection de canal pilotée par événement avec reprise de point de contrôle (Discord en premier)
- fusionner les chunks de streaming avec une politique de vidage consciente du débit limite
- garantir exactement un message de fin par exécution
- livrer `/acp spawn`, `/acp cancel`, `/acp steer`, `/acp close`, `/acp sessions`

### Phase 5 Migration et basculement

- introduire la double écriture vers la projection `SessionEntry.acp` plus la source de vérité ACP SQLite
- ajouter l'utilitaire de migration pour les lignes de métadonnées ACP héritées
- basculer le chemin de lecture vers ACP SQLite primaire
- supprimer le routage de secours hérité qui dépend de `SessionEntry.acp` manquant

### Phase 6 Durcissement, SLO et limites d'échelle

- appliquer les limites de concurrence (global/compte/session), les politiques de file d'attente et les budgets de délai d'expiration
- ajouter la télémétrie complète, les tableaux de bord et les seuils d'alerte
- test de chaos pour la récupération après panne et la suppression des livraisons en double
- publier le runbook pour la panne du backend, la corruption de DB et la correction des liaisons obsolètes

### Liste de contrôle d'implémentation complète

- modules et tests du plan de contrôle principal
- migrations DB et plan de restauration
- intégration de l'API du gestionnaire ACP dans le dispatch et les commandes
- interface d'enregistrement d'adaptateur dans le pont du runtime du plugin
- implémentation et tests de l'adaptateur acpx
- logique de projection de livraison de canal capable de threads avec relecture de point de contrôle (Discord en premier)
- hooks de cycle de vie pour reset/delete/archive/unfocus
- détecteur de liaison obsolète et diagnostics orientés opérateur
- tests de validation de configuration et de précédence pour toutes les nouvelles clés ACP
- docs opérationnels et runbook de dépannage

## Plan de test

Tests unitaires :

- limites de transaction DB ACP (atomicité spawn/bind/enqueue, cancel, close)
- gardes de transition de machine d'état ACP pour les sessions et les exécutions
- sémantique de réservation/relecture d'idempotence dans toutes les commandes ACP
- sérialisation d'acteur par session et ordre de file d'attente
- analyseur d'événement acpx et fusionneur de chunks
- politique de redémarrage et de backoff du superviseur runtime
- précédence de configuration et calcul TTL effectif
- sélection de branche de routage ACP principal et comportement fail-closed lorsque le backend/session est invalide

Tests d'intégration :

- processus d'adaptateur ACP factice pour le streaming déterministe et le comportement d'annulation
- intégration du gestionnaire ACP + dispatch avec persistance transactionnelle
- routage entrant lié aux threads vers la clé de session ACP
- la livraison sortante liée aux threads supprime la duplication du canal parent
- la relecture du point de contrôle récupère après l'échec de la livraison et reprend à partir du dernier événement
- enregistrement du service de plugin et arrêt du runtime backend ACP

Tests e2e de passerelle :

- spawn ACP avec thread, échanger des invites multi-tours, unfocus
- redémarrage de passerelle avec DB ACP persisté et liaisons, puis continuer la même session
- les sessions ACP concurrentes dans plusieurs threads n'ont pas de diaphonie
- les tentatives de commande en double (même clé d'idempotence) ne créent pas d'exécutions ou de réponses en double
- le scénario de liaison obsolète produit une erreur explicite et un comportement de nettoyage automatique optionnel

## Risques et atténuations

- Livraisons en double pendant la transition
  - Atténuation : résolveur de destination unique et point de contrôle d'événement idempotent
- Agitation du processus runtime sous charge
  - Atténuation : propriétaires par session longue durée + plafonds de concurrence + backoff
- Plugin absent ou mal configuré
  - Atténuation : erreur explicite orientée opérateur et routage ACP fail-closed (pas de secours implicite vers le chemin de session normal)
- Confusion de configuration entre la sous-agent et les portes ACP
  - Atténuation : clés ACP explicites et retour de commande qui inclut la source de politique effective
- Corruption du magasin du plan de contrôle ou bogues de migration
  - Atténuation : mode WAL, hooks de sauvegarde/restauration, tests de fumée de migration et diagnostics de secours en lecture seule
- Blocages d'acteur ou famine de boîte aux lettres
  - Atténuation : minuteurs de surveillance, sondes de santé d'acteur et profondeur de boîte aux lettres bornée avec télémétrie de rejet

## Liste de contrôle d'acceptation

- la spawn de session ACP peut créer ou lier un thread dans un adaptateur de canal pris en charge (actuellement Discord)
- tous les messages de thread sont routés vers la session ACP liée uniquement
- les sorties ACP apparaissent dans la même identité de thread avec streaming ou lots
- pas de sortie en double dans le canal parent pour les tours liés
- spawn+bind+enqueue initial sont atomiques dans le magasin persistant
- les tentatives de commande ACP sont idempotentes et ne dupliquent pas les exécutions ou les sorties
- cancel, close, unfocus, archive, reset et delete effectuent un nettoyage déterministe
- le redémarrage après panne préserve le mappage et reprend la continuité multi-tours
- les sessions ACP liées aux threads concurrentes fonctionnent indépendamment
- l'absence d'état du backend ACP produit une erreur claire et exploitable
- les liaisons obsolètes sont détectées et exposées explicitement (avec nettoyage automatique sûr optionnel)
- les métriques et diagnostics du plan de contrôle sont disponibles pour les opérateurs
- la couverture unitaire, d'intégration et e2e nouvelle réussit

## Addendum : refactorisations ciblées pour l'implémentation actuelle (statut)

Ce sont des suites non bloquantes pour maintenir le chemin ACP maintenable après l'atterrissage de l'ensemble de fonctionnalités actuel.

### 1) Centraliser l'évaluation de la politique de dispatch ACP (complété)

- implémenté via les assistants de politique ACP partagés dans `src/acp/policy.ts`
- le dispatch, les gestionnaires de cycle de vie des commandes ACP et le chemin de spawn ACP consomment maintenant la logique de politique partagée

### 2) Diviser le gestionnaire de commandes ACP par domaine de sous-commande (complété)

- `src/auto-reply/reply/commands-acp.ts` est maintenant un routeur mince
- le comportement de sous-commande est divisé en :
  - `src/auto-reply/reply/commands-acp/lifecycle.ts`
  - `src/auto-reply/reply/commands-acp/runtime-options.ts`
  - `src/auto-reply/reply/commands-acp/diagnostics.ts`
  - assistants partagés dans `src/auto-reply/reply/commands-acp/shared.ts`

### 3) Diviser le gestionnaire de session ACP par responsabilité (complété)

- le gestionnaire est divisé en :
  - `src/acp/control-plane/manager.ts` (façade publique + singleton)
  - `src/acp/control-plane/manager.core.ts` (implémentation du gestionnaire)
  - `src/acp/control-plane/manager.types.ts` (types/dépendances du gestionnaire)
  - `src/acp/control-plane/manager.utils.ts` (normalisation + fonctions d'assistance)

### 4) Nettoyage optionnel de l'adaptateur runtime acpx

- `extensions/acpx/src/runtime.ts` peut être divisé en :
- exécution/supervision du processus
- analyse/normalisation d'événement ndjson
- surface de l'API runtime (`submit`, `cancel`, `close`, etc.)
- améliore la testabilité et facilite l'audit du comportement du backend
