---
summary: "Plan de refonte du Saint Graal pour un pipeline de streaming d'exécution unifié sur main, subagent et ACP"
owner: "onutc"
status: "draft"
last_updated: "2026-02-25"
title: "Plan de refonte du streaming d'exécution unifié"
---

# Plan de refonte du streaming d'exécution unifié

## Objectif

Fournir un pipeline de streaming partagé pour `main`, `subagent` et `acp` afin que tous les runtimes bénéficient d'un comportement identique en matière de coalescence, chunking, ordre de livraison et récupération après crash.

## Raison d'être

- Le comportement actuel est fragmenté sur plusieurs chemins de mise en forme spécifiques au runtime.
- Les bugs de formatage/coalescence peuvent être corrigés dans un chemin mais persister dans les autres.
- La cohérence de livraison, la suppression des doublons et la sémantique de récupération sont plus difficiles à raisonner.

## Architecture cible

Pipeline unique, adaptateurs spécifiques au runtime :

1. Les adaptateurs de runtime émettent uniquement des événements canoniques.
2. L'assembleur de flux partagé coalescence et finalise les événements texte/outil/statut.
3. Le projecteur de canal partagé applique le chunking/formatage spécifique au canal une seule fois.
4. Le registre de livraison partagé applique la sémantique d'envoi/relecture idempotente.
5. L'adaptateur de canal sortant exécute les envois et enregistre les points de contrôle de livraison.

Contrat d'événement canonique :

- `turn_started`
- `text_delta`
- `block_final`
- `tool_started`
- `tool_finished`
- `status`
- `turn_completed`
- `turn_failed`
- `turn_cancelled`

## Flux de travail

### 1) Contrat de streaming canonique

- Définir un schéma d'événement strict + validation dans le noyau.
- Ajouter des tests de contrat d'adaptateur pour garantir que chaque runtime émet des événements compatibles.
- Rejeter les événements de runtime malformés rapidement et exposer des diagnostics structurés.

### 2) Processeur de flux partagé

- Remplacer la logique de coalescence/projecteur spécifique au runtime par un seul processeur.
- Le processeur gère la mise en buffer des deltas texte, le flush inactif, le fractionnement max-chunk et le flush de fin.
- Déplacer la résolution de configuration ACP/main/subagent dans un seul helper pour éviter la dérive.

### 3) Projection de canal partagée

- Garder les adaptateurs de canal simples : accepter les blocs finalisés et envoyer.
- Déplacer les quirks de chunking spécifiques à Discord au projecteur de canal uniquement.
- Garder le pipeline agnostique au canal avant la projection.

### 4) Registre de livraison + relecture

- Ajouter des IDs de livraison par tour/par chunk.
- Enregistrer les points de contrôle avant et après l'envoi physique.
- Au redémarrage, relire les chunks en attente de manière idempotente et éviter les doublons.

### 5) Migration et basculement

- Phase 1 : mode shadow (le nouveau pipeline calcule la sortie mais l'ancien chemin envoie ; comparer).
- Phase 2 : basculement runtime par runtime (`acp`, puis `subagent`, puis `main` ou inverse selon le risque).
- Phase 3 : supprimer le code de streaming spécifique au runtime hérité.

## Non-objectifs

- Aucune modification du modèle de politique/permissions ACP dans cette refonte.
- Aucune expansion de fonctionnalité spécifique au canal en dehors des correctifs de compatibilité de projection.
- Aucune refonte de transport/backend (le contrat du plugin acpx reste tel quel sauf si nécessaire pour la parité des événements).

## Risques et atténuations

- Risque : régressions comportementales dans les chemins main/subagent existants.
  Atténuation : diffing en mode shadow + tests de contrat d'adaptateur + tests e2e de canal.
- Risque : envois dupliqués lors de la récupération après crash.
  Atténuation : IDs de livraison durables + relecture idempotente dans l'adaptateur de livraison.
- Risque : les adaptateurs de runtime divergent à nouveau.
  Atténuation : suite de tests de contrat partagée obligatoire pour tous les adaptateurs.

## Critères d'acceptation

- Tous les runtimes réussissent les tests de contrat de streaming partagé.
- Discord ACP/main/subagent produisent un comportement d'espacement/chunking équivalent pour les petits deltas.
- La relecture crash/redémarrage n'envoie aucun chunk dupliqué pour le même ID de livraison.
- Le chemin projecteur/coalescence ACP hérité est supprimé.
- La résolution de la configuration de streaming est partagée et indépendante du runtime.
