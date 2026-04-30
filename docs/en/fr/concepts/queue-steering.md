---
summary: "Comment les files d'attente de steering actif mettent en file d'attente les messages aux limites d'exécution"
read_when:
  - Explaining how steer behaves while an agent is using tools
  - Changing active-run queue behavior or runtime steering integration
  - Comparing steer, queue, collect, and followup modes
title: "File d'attente de steering"
---

Quand un message arrive alors qu'une exécution de session est déjà en cours de streaming, OpenClaw peut envoyer ce message dans le runtime actif au lieu de démarrer une autre exécution pour la même session. Les modes publics sont neutres par rapport au runtime ; Pi et le harnais natif du serveur d'applications Codex implémentent les détails de livraison différemment.

## Limite d'exécution

Le steering n'interrompt pas un appel d'outil qui est déjà en cours d'exécution. Pi vérifie les messages de steering en file d'attente aux limites du modèle :

1. L'assistant demande des appels d'outil.
2. Pi exécute le lot d'appels d'outil du message assistant actuel.
3. Pi émet l'événement de fin de tour.
4. Pi vide les messages de steering en file d'attente.
5. Pi ajoute ces messages en tant que messages utilisateur avant l'appel LLM suivant.

Cela maintient les résultats des outils appairés avec le message assistant qui les a demandés, puis permet à l'appel du modèle suivant de voir la dernière entrée utilisateur.

Le harnais natif du serveur d'applications Codex expose `turn/steer` au lieu de la file d'attente de steering interne de Pi. OpenClaw adapte les mêmes modes là :

- `steer` met en file d'attente les messages en attente pour la fenêtre de silence configurée, puis envoie une seule demande `turn/steer` avec toutes les entrées utilisateur collectées dans l'ordre d'arrivée.
- `queue` conserve la forme sérialisée héritée en envoyant des demandes `turn/steer` séparées.
- `followup`, `collect`, `steer-backlog`, et `interrupt` restent le comportement de file d'attente détenu par OpenClaw autour du tour Codex actif.

Les tours de révision Codex et de compaction manuelle rejettent le steering du même tour. Quand un runtime ne peut pas accepter le steering, OpenClaw revient à la file d'attente de suivi où ce mode le permet.

## Modes

| Mode            | Comportement d'exécution active                                                                                              | Comportement de suivi ultérieur                                                     |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `steer`         | Injecte tous les messages de steering en file d'attente ensemble à la prochaine limite d'exécution. C'est le mode par défaut. | Revient au suivi uniquement quand le steering n'est pas disponible.                 |
| `queue`         | Steering hérité un à la fois. Pi injecte un message en file d'attente par limite de modèle ; Codex envoie des demandes `turn/steer` séparées. | Revient au suivi uniquement quand le steering n'est pas disponible.                 |
| `steer-backlog` | Même comportement de steering d'exécution active que `steer`.                                                                 | Conserve également le même message pour un tour de suivi ultérieur.                 |
| `followup`      | Ne fait pas de steering de l'exécution actuelle.                                                                             | Exécute les messages en file d'attente plus tard.                                   |
| `collect`       | Ne fait pas de steering de l'exécution actuelle.                                                                             | Fusionne les messages en file d'attente compatibles en un seul tour ultérieur après la fenêtre de debounce. |
| `interrupt`     | Abandonne l'exécution active, puis démarre le message le plus récent.                                                        | Aucun.                                                                              |

## Exemple de rafale

Si quatre utilisateurs envoient des messages pendant que l'agent exécute un appel d'outil :

- `steer` : le runtime actif reçoit les quatre messages dans l'ordre d'arrivée avant sa prochaine décision de modèle. Pi les vide à la prochaine limite de modèle ; Codex les reçoit comme un seul `turn/steer` par lot.
- `queue` : steering sérialisé hérité. Pi injecte un message en file d'attente à la fois ; Codex reçoit des demandes `turn/steer` séparées.
- `collect` : OpenClaw attend que l'exécution active se termine, puis crée un tour de suivi avec les messages en file d'attente compatibles après la fenêtre de debounce.

## Portée

Le steering cible toujours l'exécution de session active actuelle. Il ne crée pas une nouvelle session, ne change pas la politique d'outils de l'exécution active, et ne divise pas les messages par expéditeur. Dans les canaux multi-utilisateurs, les invites entrantes incluent déjà le contexte d'expéditeur et d'itinéraire, donc l'appel du modèle suivant peut voir qui a envoyé chaque message.

Utilisez `collect` quand vous voulez qu'OpenClaw construise un tour de suivi ultérieur qui peut fusionner les messages compatibles et préserver la politique de suppression de la file d'attente de suivi. Utilisez `queue` uniquement quand vous avez besoin du comportement de steering un à la fois plus ancien.

## Debounce

`messages.queue.debounceMs` s'applique à la livraison de suivi, y compris `collect`, `followup`, `steer-backlog`, et `steer` fallback quand le steering d'exécution active n'est pas disponible. Pour Pi, le `steer` actif lui-même n'utilise pas le minuteur de debounce car Pi met naturellement en file d'attente les messages jusqu'à la prochaine limite de modèle. Pour le harnais Codex natif, OpenClaw utilise la même valeur de debounce que la fenêtre de silence avant d'envoyer le `turn/steer` par lot.

## Connexes

- [Command queue](/fr/concepts/queue)
- [Messages](/fr/concepts/messages)
- [Agent loop](/fr/concepts/agent-loop)
