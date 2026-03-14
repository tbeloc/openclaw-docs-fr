# Agents Thread Bound ACP

## Aperçu

Ce plan définit comment OpenClaw devrait supporter les agents de codage ACP dans les canaux compatibles avec les threads (Discord en premier) avec un cycle de vie et une récupération au niveau de la production.

Document connexe :

- [Unified Runtime Streaming Refactor Plan](/experiments/plans/acp-unified-streaming-refactor)

Expérience utilisateur cible :

- un utilisateur crée ou concentre une session ACP dans un thread
- les messages de l'utilisateur dans ce thread sont acheminés vers la session ACP liée
- la sortie de l'agent est diffusée en continu vers le même persona de thread
- la session peut être persistante ou ponctuelle avec des contrôles de nettoyage explicites

## Résumé des décisions

La recommandation à long terme est une architecture hybride :

- Le cœur d'OpenClaw possède les préoccupations du plan de contrôle ACP
  - identité et métadonnées de session
  - décisions de liaison et d'acheminement des threads
  - invariants de livraison et suppression des doublons
  - sémantique de nettoyage du cycle de vie et récupération
- Le backend d'exécution ACP est enfichable
  - le premier backend est un service de plugin soutenu par acpx
  - le runtime gère le transport ACP, la mise en file d'attente, l'annulation, la reconnexion

OpenClaw ne devrait pas réimplémenter les éléments internes du transport ACP dans le cœur.
OpenClaw ne devrait pas dépendre d'un chemin d'interception pur plugin uniquement pour l'acheminement.

## Architecture nord-étoile (saint graal)

Traiter ACP comme un plan de contrôle de première classe dans OpenClaw, avec des adaptateurs d'exécution enfichables.

Invariants non négociables :

- chaque liaison de thread ACP référence un enregistrement de session ACP valide
- chaque session ACP a un état de cycle de vie explicite (`creating`, `idle`, `running`, `cancelling`, `closed`, `error`)
- chaque exécution ACP a un état d'exécution explicite (`queued`, `running`, `completed`, `failed`, `cancelled`)
- spawn, bind et enqueue initial sont atomiques
- les tentatives de commande sont idempotentes (pas d'exécutions dupliquées ou de sorties Discord dupliquées)
- la sortie du canal de thread lié est une projection des événements d'exécution ACP, jamais des effets secondaires ad hoc

Modèle de propriété à long terme :

- `AcpSessionManager` est le seul écrivain et orchestrateur ACP
- le gestionnaire vit d'abord dans le processus de passerelle ; peut être déplacé vers un sidecar dédié plus tard derrière la même interface
- par clé de session ACP, le gestionnaire possède un acteur en mémoire (exécution de commande sérialisée)
- les adaptateurs (`acpx`, futurs backends) sont uniquement des implémentations de transport/runtime

Modèle de persistance à long terme :

- déplacer l'état du plan de contrôle ACP vers un magasin SQLite dédié (mode WAL) sous le répertoire d'état d'OpenClaw
- garder `SessionEntry.acp` comme projection de compatibilité pendant la migration, pas source de vérité
- stocker les événements ACP en ajout uniquement pour supporter la relecture, la récupération après sinistre et la livraison déterministe

### Stratégie de livraison (pont vers le saint graal)

- pont à court terme
  - garder les mécaniques de liaison de thread actuelles et la surface de configuration ACP existante
  - corriger les bugs d'écart de métadonnées et acheminer les tours ACP via une seule branche ACP principale
  - ajouter immédiatement les clés d'idempotence et les vérifications d'acheminement fail-closed
- basculement à long terme
  - déplacer la source de vérité ACP vers la base de données du plan de contrôle + acteurs
  - rendre la livraison de thread lié purement basée sur la projection d'événements
  - supprimer le comportement de secours hérité qui dépend des métadonnées de session-entry opportunistes

## Pourquoi pas pur plugin uniquement

Les crochets de plugin actuels ne sont pas suffisants pour l'acheminement de session ACP de bout en bout sans modifications du cœur.

- l'acheminement entrant de la liaison de thread se résout à une clé de session dans la distribution du cœur en premier
- les crochets de message sont fire-and-forget et ne peuvent pas court-circuiter le chemin de réponse principal
- les commandes de plugin sont bonnes pour les opérations de contrôle mais pas pour remplacer le flux de distribution par tour du cœur

Résultat :

- le runtime ACP peut être enfichable
- la branche d'acheminement ACP doit exister dans le cœur

## Fondation existante à réutiliser

Déjà implémenté et devrait rester canonique :

- la cible de liaison de thread supporte `subagent` et `acp`
- l'override d'acheminement de thread entrant se résout par liaison avant la distribution normale
- identité de thread sortant via webhook dans la livraison de réponse
- flux `/focus` et `/unfocus` avec compatibilité de cible ACP
- magasin de liaison persistant avec restauration au démarrage
- débindage du cycle de vie sur archive, suppression, unfocus, réinitialisation et suppression

Ce plan étend cette fondation plutôt que de la remplacer.

## Architecture

### Modèle de limite

Cœur (doit être dans le cœur d'OpenClaw) :

- branche de distribution en mode session ACP dans le pipeline de réponse
- arbitrage de livraison pour éviter la duplication parent plus thread
- persistance du plan de contrôle ACP (avec projection de compatibilité `SessionEntry.acp` pendant la migration)
- sémantique de débindage du cycle de vie et détachement du runtime liés à la réinitialisation/suppression de session

Backend de plugin (implémentation acpx) :

- supervision du worker d'exécution ACP
- invocation du processus acpx et analyse des événements
- gestionnaires de commandes ACP (`/acp ...`) et UX d'opérateur
- valeurs par défaut de configuration spécifiques au backend et diagnostics

### Modèle de propriété du runtime

- un processus de passerelle possède l'état d'orchestration ACP
- l'exécution ACP s'exécute dans des processus enfants supervisés via le backend acpx
- la stratégie de processus est longue durée par clé de session ACP active, pas par message

Cela évite le coût de démarrage à chaque invite et maintient les sémantiques d'annulation et de reconnexion fiables.

### Contrat d'exécution du cœur

Ajouter un contrat d'exécution ACP du cœur afin que le code d'acheminement ne dépende pas des détails CLI et puisse basculer les backends sans modifier la logique de distribution :

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
- le cœur résout le runtime via le registre et échoue avec une erreur d'opérateur explicite quand aucun backend d'exécution ACP n'est disponible

### Modèle de données du plan de contrôle et persistance

La source de vérité à long terme est une base de données SQLite ACP dédiée (mode WAL), pour les mises à jour transactionnelles et la récupération sûre après sinistre :

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
- l'état du cycle de vie durable et l'état d'exécution vivent dans la base de données ACP, pas dans le JSON de session générique
- si le propriétaire du runtime meurt, la passerelle se réhydrate à partir de la base de données ACP et reprend à partir des points de contrôle

### Acheminement et livraison

Entrant :

- garder la recherche de liaison de thread actuelle comme première étape d'acheminement
- si la cible de liaison liée est une session ACP, acheminer vers la branche d'exécution ACP au lieu de `getReplyFromConfig`
- la commande explicite `/acp steer` utilise `mode: "steer"`

Sortant :

- le flux d'événements ACP est normalisé en chunks de réponse OpenClaw
- la cible de livraison est résolue via le chemin de destination lié existant
- quand un thread lié est actif pour ce tour de session, la fin du canal parent est supprimée

Politique de diffusion en continu :

- diffuser la sortie partielle avec fenêtre de coalescence
- intervalle minimum configurable et octets de chunk maximum pour rester sous les limites de débit Discord
- le message final est toujours émis à la fin ou en cas d'échec

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

Aucun succès partiel n'est autorisé sur ces limites.

### Modèle d'acteur par session

`AcpSessionManager` exécute un acteur par clé de session ACP :

- la boîte aux lettres d'acteur sérialise les effets secondaires `submit`, `cancel`, `close` et `stream`
- l'acteur possède l'hydratation du handle d'exécution et le cycle de vie du processus d'adaptateur d'exécution pour cette session
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

Au démarrage de la passerelle :

- charger les sessions ACP non terminales (`creating`, `idle`, `running`, `cancelling`, `error`)
- recréer les acteurs paresseusement au premier événement entrant ou avec impatience sous un plafond configuré
- réconcilier toute exécution `running` manquant les battements de cœur et marquer `failed` ou
