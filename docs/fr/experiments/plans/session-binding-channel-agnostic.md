---
summary: "Architecture de liaison de session agnostique des canaux et portée de livraison de l'itération 1"
read_when:
  - Refactorisation du routage de session agnostique des canaux et des liaisons
  - Enquête sur les livraisons de session dupliquées, obsolètes ou manquantes entre les canaux
owner: "onutc"
status: "in-progress"
last_updated: "2026-02-21"
title: "Plan de liaison de session agnostique des canaux"
---

# Plan de liaison de session agnostique des canaux

## Aperçu

Ce document définit le modèle de liaison de session agnostique des canaux à long terme et la portée concrète pour la prochaine itération de mise en œuvre.

Objectif :

- faire du routage de session lié aux sous-agents une capacité fondamentale
- conserver le comportement spécifique aux canaux dans les adaptateurs
- éviter les régressions dans le comportement normal de Discord

## Raison d'être

Le comportement actuel mélange :

- politique de contenu d'achèvement
- politique de routage de destination
- détails spécifiques à Discord

Cela a causé des cas limites tels que :

- livraison dupliquée du canal principal et du fil lors d'exécutions concurrentes
- utilisation de jetons obsolètes sur les gestionnaires de liaisons réutilisés
- comptabilité d'activité manquante pour les envois de webhook

## Portée de l'itération 1

Cette itération est intentionnellement limitée.

### 1. Ajouter des interfaces de base agnostiques des canaux

Ajouter les types de base et les interfaces de service pour les liaisons et le routage.

Types de base proposés :

```ts
export type BindingTargetKind = "subagent" | "session";
export type BindingStatus = "active" | "ending" | "ended";

export type ConversationRef = {
  channel: string;
  accountId: string;
  conversationId: string;
  parentConversationId?: string;
};

export type SessionBindingRecord = {
  bindingId: string;
  targetSessionKey: string;
  targetKind: BindingTargetKind;
  conversation: ConversationRef;
  status: BindingStatus;
  boundAt: number;
  expiresAt?: number;
  metadata?: Record<string, unknown>;
};
```

Contrat de service de base :

```ts
export interface SessionBindingService {
  bind(input: {
    targetSessionKey: string;
    targetKind: BindingTargetKind;
    conversation: ConversationRef;
    metadata?: Record<string, unknown>;
    ttlMs?: number;
  }): Promise<SessionBindingRecord>;

  listBySession(targetSessionKey: string): SessionBindingRecord[];
  resolveByConversation(ref: ConversationRef): SessionBindingRecord | null;
  touch(bindingId: string, at?: number): void;
  unbind(input: {
    bindingId?: string;
    targetSessionKey?: string;
    reason: string;
  }): Promise<SessionBindingRecord[]>;
}
```

### 2. Ajouter un routeur de livraison de base pour les complétions de sous-agents

Ajouter un chemin de résolution de destination unique pour les événements d'achèvement.

Contrat du routeur :

```ts
export interface BoundDeliveryRouter {
  resolveDestination(input: {
    eventKind: "task_completion";
    targetSessionKey: string;
    requester?: ConversationRef;
    failClosed: boolean;
  }): {
    binding: SessionBindingRecord | null;
    mode: "bound" | "fallback";
    reason: string;
  };
}
```

Pour cette itération :

- seul `task_completion` est routé via ce nouveau chemin
- les chemins existants pour les autres types d'événements restent inchangés

### 3. Garder Discord comme adaptateur

Discord reste la première implémentation d'adaptateur.

Responsabilités de l'adaptateur :

- créer/réutiliser les conversations de fil
- envoyer les messages liés via webhook ou envoi de canal
- valider l'état du fil (archivé/supprimé)
- mapper les métadonnées de l'adaptateur (identité du webhook, identifiants de fil)

### 4. Corriger les problèmes de correction actuellement connus

Requis dans cette itération :

- actualiser l'utilisation du jeton lors de la réutilisation du gestionnaire de liaison de fil existant
- enregistrer l'activité sortante pour les envois Discord basés sur webhook
- arrêter le repli implicite du canal principal lorsqu'une destination de fil liée est sélectionnée pour l'achèvement du mode session

### 5. Préserver les paramètres par défaut de sécurité d'exécution actuels

Aucun changement de comportement pour les utilisateurs avec la génération de session liée au fil désactivée.

Les paramètres par défaut restent :

- `channels.discord.threadBindings.spawnSubagentSessions = false`

Résultat :

- les utilisateurs Discord normaux restent sur le comportement actuel
- le nouveau chemin de base affecte uniquement le routage d'achèvement de session lié où il est activé

## Non inclus dans l'itération 1

Explicitement reporté :

- cibles de liaison ACP (`targetKind: "acp"`)
- nouveaux adaptateurs de canaux au-delà de Discord
- remplacement global de tous les chemins de livraison (`spawn_ack`, futur `subagent_message`)
- modifications au niveau du protocole
- refonte de la migration/versioning du magasin pour toute la persistance des liaisons

Notes sur ACP :

- la conception de l'interface laisse de la place pour ACP
- l'implémentation d'ACP n'est pas commencée dans cette itération

## Invariants de routage

Ces invariants sont obligatoires pour l'itération 1.

- la sélection de destination et la génération de contenu sont des étapes séparées
- si l'achèvement du mode session se résout en une destination liée active, la livraison doit cibler cette destination
- pas de reroutage caché de la destination liée vers le canal principal
- le comportement de repli doit être explicite et observable

## Compatibilité et déploiement

Cible de compatibilité :

- aucune régression pour les utilisateurs avec la génération de session liée au fil désactivée
- aucun changement aux canaux non-Discord dans cette itération

Déploiement :

1. Placer les interfaces et le routeur derrière les portes de fonctionnalités actuelles.
2. Routeur les livraisons d'achèvement Discord en mode lié via le routeur.
3. Conserver le chemin hérité pour les flux non liés.
4. Vérifier avec des tests ciblés et des journaux d'exécution canary.

## Tests requis dans l'itération 1

Couverture unitaire et d'intégration requise :

- la rotation des jetons du gestionnaire utilise le dernier jeton après la réutilisation du gestionnaire
- les envois webhook mettent à jour les horodatages d'activité du canal
- deux sessions liées actives dans le même canal demandeur ne dupliquent pas vers le canal principal
- l'achèvement pour l'exécution du mode session lié se résout uniquement à la destination du fil
- l'indicateur de génération désactivé conserve le comportement hérité inchangé

## Fichiers d'implémentation proposés

Cœur :

- `src/infra/outbound/session-binding-service.ts` (nouveau)
- `src/infra/outbound/bound-delivery-router.ts` (nouveau)
- `src/agents/subagent-announce.ts` (intégration de résolution de destination d'achèvement)

Adaptateur Discord et exécution :

- `src/discord/monitor/thread-bindings.manager.ts`
- `src/discord/monitor/reply-delivery.ts`
- `src/discord/send.outbound.ts`

Tests :

- `src/discord/monitor/provider*.test.ts`
- `src/discord/monitor/reply-delivery.test.ts`
- `src/agents/subagent-announce.format.test.ts`

## Critères de réussite pour l'itération 1

- les interfaces de base existent et sont câblées pour le routage d'achèvement
- les corrections de correction ci-dessus sont fusionnées avec les tests
- aucune livraison d'achèvement dupliquée du canal principal et du fil dans les exécutions liées au mode session
- aucun changement de comportement pour les déploiements avec génération de session liée désactivée
- ACP reste explicitement reporté
