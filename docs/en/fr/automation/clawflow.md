---
summary: "Orchestration de flux ClawFlow pour les tâches en arrière-plan et les exécutions détachées"
read_when:
  - You want a flow to own one or more detached tasks
  - You want to inspect or cancel a background job as a unit
  - You want to understand how flows relate to tasks and background work
title: "ClawFlow"
---

# ClawFlow

ClawFlow est la couche de flux au-dessus des [Tâches en arrière-plan](/fr/automation/tasks). Les tâches continuent à suivre le travail détaché. ClawFlow regroupe ces exécutions de tâches dans un seul travail, conserve le contexte du propriétaire parent et vous donne une surface de contrôle au niveau du flux.

Utilisez ClawFlow lorsque le travail est plus qu'une seule exécution détachée. Un flux peut toujours être une seule tâche, mais il peut aussi coordonner plusieurs tâches dans une simple séquence linéaire.

## TL;DR

- Les tâches sont les enregistrements d'exécution.
- ClawFlow est le wrapper au niveau du travail au-dessus des tâches.
- Un flux conserve un contexte de propriétaire/session unique pour l'ensemble du travail.
- Utilisez `openclaw flows list`, `openclaw flows show` et `openclaw flows cancel` pour inspecter ou gérer les flux.

## Démarrage rapide

```bash
openclaw flows list
openclaw flows show <flow-id-or-owner-session>
openclaw flows cancel <flow-id-or-owner-session>
```

## Comment cela se rapporte aux tâches

Les tâches en arrière-plan font toujours le travail de bas niveau :

- Exécutions ACP
- Exécutions de sous-agents
- Exécutions cron
- Exécutions initiées par CLI

ClawFlow se situe au-dessus de ce registre :

- il conserve les exécutions de tâches associées sous un seul identifiant de flux
- il suit l'état du flux séparément de l'état de la tâche individuelle
- il rend plus facile l'inspection du travail bloqué ou multi-étapes à partir d'un seul endroit

Pour une seule exécution détachée, le flux peut être un flux à une tâche. Pour un travail plus structuré, ClawFlow peut conserver plusieurs exécutions de tâches sous le même travail.

## Substrat d'exécution

ClawFlow est le substrat d'exécution, pas un langage de flux de travail.

Il possède :

- l'identifiant du flux
- la session du propriétaire et le contexte de retour
- l'état d'attente
- les petites sorties persistées
- l'état de fin, d'échec, d'annulation et de blocage

Il ne possède **pas** la ramification ou la logique métier. Mettez cela dans la couche de création qui se situe au-dessus :

- Lobster
- acpx
- Assistants TypeScript simples
- Compétences groupées

En pratique, les couches de création ciblent une petite surface d'exécution :

- `createFlow(...)`
- `runTaskInFlow(...)`
- `setFlowWaiting(...)`
- `setFlowOutput(...)`
- `appendFlowOutput(...)`
- `emitFlowUpdate(...)`
- `resumeFlow(...)`
- `finishFlow(...)`
- `failFlow(...)`

Cela maintient la propriété du flux et le comportement de retour au thread dans le noyau sans forcer un seul DSL au-dessus.

## Modèle de création

La forme prévue est linéaire :

1. Créez un flux pour le travail.
2. Exécutez une tâche détachée sous ce flux.
3. Attendez la tâche enfant ou un événement externe.
4. Reprenez le flux dans l'appelant.
5. Générez la tâche enfant suivante ou terminez.

ClawFlow persiste l'état minimal nécessaire pour reprendre ce travail : l'étape actuelle, la tâche sur laquelle il attend et un petit sac de sortie pour la transmission entre les étapes.

## Surface CLI

La CLI de flux est intentionnellement petite :

- `openclaw flows list` affiche les flux actifs et récents
- `openclaw flows show <lookup>` affiche un flux et ses tâches liées
- `openclaw flows cancel <lookup>` annule le flux et toutes les tâches enfants actives

`flows show` expose également la cible d'attente actuelle et toutes les clés de sortie stockées, ce qui est souvent suffisant pour répondre à « sur quoi ce travail attend-il ? » sans fouiller dans chaque tâche enfant.

Le jeton de recherche accepte soit un identifiant de flux, soit la clé de session du propriétaire.

## Connexes

- [Tâches en arrière-plan](/fr/automation/tasks) — registre de travail détaché
- [CLI : flows](/fr/cli/flows) — commandes d'inspection et de contrôle de flux
- [Travaux Cron](/fr/automation/cron-jobs) — travaux planifiés qui peuvent créer des tâches
