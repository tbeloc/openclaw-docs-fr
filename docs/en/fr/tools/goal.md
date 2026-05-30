---
doc-schema-version: 1
summary: "Objectifs de session : objectifs durables par session, contrôles /goal, outils de modèle d'objectif, budgets de jetons et statut TUI"
read_when:
  - You want OpenClaw to keep one objective visible across a long session
  - You need to pause, resume, block, complete, or clear a session goal
  - You want to understand the get_goal, create_goal, and update_goal tools
  - You want to see how goals appear in the TUI
title: "Objectif"
---

# Objectif

Un **objectif** est un objectif durable attaché à la session OpenClaw actuelle.
Il donne à l'agent et à l'opérateur une cible commune pour les travaux de longue durée,
sans transformer cette cible en tâche de fond, rappel, travail cron ou
ordre permanent.

Les objectifs sont un état de session. Ils se déplacent avec la clé de session, survivent aux
redémarrages de processus, s'affichent dans `/goal`, sont disponibles pour le modèle via les outils
d'objectif et apparaissent dans le pied de page TUI lorsque la session active en a un.

## Démarrage rapide

Définir un objectif :

```text
/goal start get CI green for PR 87469 and push the fix
```

Le vérifier :

```text
/goal
```

Le mettre en pause lorsque le travail attend intentionnellement :

```text
/goal pause waiting for CI
```

Le reprendre :

```text
/goal resume
```

Le marquer comme terminé :

```text
/goal complete pushed and verified
```

L'effacer :

```text
/goal clear
```

## À quoi servent les objectifs

Utilisez un objectif lorsqu'une session a un résultat concret qui doit rester visible
sur plusieurs tours :

- Une fermeture de PR : corriger, vérifier, examen automatique, pousser et ouvrir ou mettre à jour la PR.
- Une exécution de débogage : reproduire le bogue, identifier la surface propriétaire, corriger et prouver
  la correction.
- Un passage de documentation : lire la documentation pertinente, écrire la nouvelle page, la lier de manière croisée et
  vérifier que la documentation se construit.
- Une tâche de maintenance : inspecter l'état actuel, apporter des modifications délimitées, exécuter les
  vérifications appropriées et signaler ce qui a changé.

Un objectif n'est pas une file d'attente de tâches. Utilisez [Task Flow](/fr/automation/taskflow),
[tâches](/fr/automation/tasks), [travaux cron](/fr/automation/cron-jobs) ou
[ordres permanents](/fr/automation/standing-orders) lorsque le travail doit s'exécuter de manière détachée,
se répéter selon un calendrier, se diviser en sous-travaux gérés ou persister en tant que politique.

## Référence des commandes

`/goal` sans arguments affiche le résumé de l'objectif actuel :

```text
Goal
Status: active
Objective: get CI green for PR 87469 and push the fix
Tokens used: 12k
Token budget: 12k/50k

Commands: /goal pause, /goal complete, /goal clear
```

Commandes :

- `/goal` ou `/goal status` affiche l'objectif actuel.
- `/goal start <objective>` crée un nouvel objectif pour la session actuelle.
- `/goal set <objective>` et `/goal create <objective>` sont des alias pour
  `start`.
- `/goal pause [note]` met en pause un objectif actif.
- `/goal resume [note]` reprend un objectif en pause, bloqué, limité en utilisation ou
  limité en budget.
- `/goal complete [note]` marque l'objectif comme atteint.
- `/goal done [note]` est un alias pour `complete`.
- `/goal block [note]` marque l'objectif comme bloqué.
- `/goal blocked [note]` est un alias pour `block`.
- `/goal clear` supprime l'objectif de la session.

Un seul objectif peut exister sur une session à la fois. Démarrer un deuxième objectif échoue
jusqu'à ce que l'objectif actuel soit effacé.

## Statuts

Les objectifs utilisent un petit ensemble de statuts :

- `active` : la session poursuit l'objectif.
- `paused` : l'opérateur a mis en pause l'objectif ; `/goal resume` le rend actif à nouveau.
- `blocked` : l'agent ou l'opérateur a signalé un vrai bloqueur ; `/goal resume`
  le rend actif à nouveau lorsque de nouvelles informations ou un nouvel état sont disponibles.
- `budget_limited` : le budget de jetons configuré a été atteint ; `/goal resume`
  redémarre la poursuite du même objectif.
- `usage_limited` : réservé pour les états d'arrêt de limite d'utilisation ; `/goal resume`
  redémarre la poursuite lorsque c'est autorisé.
- `complete` : l'objectif a été atteint. Les objectifs terminés sont terminaux ; utilisez
  `/goal clear` avant de démarrer un autre objectif.

`/new` et `/reset` effacent l'objectif de session actuel car ils démarrent intentionnellement
un contexte de session frais.

## Budgets de jetons

Les objectifs peuvent avoir un budget de jetons positif optionnel. Le budget est stocké avec l'
objectif et mesuré à partir du nombre de jetons frais de la session au moment de la création. Si la
session actuelle n'a que des jetons d'utilisation obsolètes ou inconnus lorsque l'objectif démarre,
OpenClaw attend le prochain instantané de jeton de session frais et l'utilise comme
ligne de base, de sorte que les jetons dépensés avant l'existence de l'objectif ne sont pas facturés à l'objectif.

Lorsque l'utilisation des jetons atteint le budget, l'objectif passe à `budget_limited`. Cela
ne supprime pas l'objectif ni n'efface l'objectif. Cela indique à l'opérateur et à l'
agent que l'objectif n'est plus activement poursuivi jusqu'à ce qu'il soit repris ou
effacé.

Les budgets de jetons sont une barrière de sécurité pour les objectifs de session, pas un plafond de facturation. Le quota du fournisseur,
la génération de rapports de coûts et le comportement de la fenêtre de contexte utilisent toujours les
contrôles d'utilisation et de modèle OpenClaw normaux.

## Outils de modèle

OpenClaw expose trois outils d'objectif principaux aux harnais d'agent :

- `get_goal` : lire l'objectif de session actuel, y compris le statut, l'objectif, l'utilisation des jetons
  et le budget de jetons.
- `create_goal` : créer un objectif uniquement lorsque l'utilisateur, le système ou les instructions du développeur
  en demandent explicitement un. Cela échoue si la session a déjà un
  objectif.
- `update_goal` : marquer l'objectif comme `complete` ou `blocked`.

Le modèle ne peut pas mettre silencieusement en pause, reprendre, effacer ou remplacer un objectif. Ce sont des
contrôles d'opérateur/session via les commandes `/goal` et de réinitialisation. Cela empêche l'
agent de déplacer silencieusement la cible tout en préservant un chemin propre pour l'
agent de signaler la réussite ou un vrai bloqueur.

L'outil `update_goal` ne doit marquer un objectif comme `complete` que lorsque l'objectif est
réellement atteint. Il ne doit marquer un objectif comme `blocked` que lorsque la même condition de blocage
s'est répétée et que l'agent ne peut pas faire de progrès significatifs sans
nouvelle entrée utilisateur ou changement d'état externe.

## TUI

Le TUI garde l'objectif de la session active visible dans le pied de page à côté de l'
agent, de la session, du modèle, des contrôles d'exécution et des compteurs de jetons.

Exemples de pied de page :

- `Pursuing goal (12k/50k)` pour un objectif actif avec un budget de jetons.
- `Goal paused (/goal resume)` pour un objectif en pause.
- `Goal blocked (/goal resume)` pour un objectif bloqué.
- `Goal hit usage limits (/goal resume)` pour un objectif limité en utilisation.
- `Goal unmet (50k/50k)` pour un objectif limité en budget.
- `Goal achieved (42k)` pour un objectif terminé.

Le pied de page est intentionnellement compact. Utilisez `/goal` pour l'objectif complet, la note,
le budget de jetons et les commandes disponibles.

## Comportement des canaux

La commande `/goal` fonctionne dans les sessions OpenClaw compatibles avec les commandes, y compris le TUI et les surfaces de chat
qui permettent les commandes texte. L'état de l'objectif est attaché à la clé de session, pas au transport. Si deux surfaces utilisent la même session, elles voient le même objectif.

L'état de l'objectif n'est pas une directive de livraison. Il ne force pas les réponses via un
canal, ne change pas le comportement de la file d'attente, n'approuve pas les outils ou ne planifie pas le travail.

## Dépannage

`Goal error: goal already exists` signifie que la session a déjà un objectif. Utilisez
`/goal` pour l'inspecter, `/goal complete` s'il est terminé, ou `/goal clear` avant
de démarrer un objectif différent.

`Goal error: goal not found` signifie que la session n'a pas encore d'objectif. Démarrez-en un avec
`/goal start <objective>`.

`Goal error: goal is already complete` signifie que l'objectif est terminal. Effacez-le
avant de démarrer ou de reprendre un autre objectif.

Si l'utilisation des jetons ressemble à `0` ou est obsolète, la session active peut ne pas avoir d'
instantané de jeton frais pour le moment. L'utilisation s'actualise à mesure qu'OpenClaw enregistre l'utilisation de la session et les
totaux dérivés de la transcription.

## Connexes

- [Commandes slash](/fr/tools/slash-commands)
- [TUI](/fr/web/tui)
- [Outil de session](/fr/concepts/session-tool)
- [Compaction](/fr/concepts/compaction)
- [Task Flow](/fr/automation/taskflow)
- [Ordres permanents](/fr/automation/standing-orders)
