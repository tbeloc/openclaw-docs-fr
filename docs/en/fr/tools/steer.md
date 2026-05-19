---
summary: "Diriger une exécution active sans modifier le mode de file d'attente"
read_when:
  - Using /steer or /tell while an agent is already running
  - Comparing /steer with /queue modes
  - Deciding whether to steer the current run, a sub-agent, or an ACP session
title: "Steer"
sidebarTitle: "Steer"
---

`/steer` essaie d'abord d'envoyer des conseils à une exécution déjà active. C'est pour les moments où vous voulez "ajuster cette exécution pendant qu'elle fonctionne encore". Si le runtime actuel ne peut pas accepter de direction, OpenClaw envoie le message comme une invite normale au lieu de l'abandonner.

## Session actuelle

Utilisez `/steer` au niveau supérieur pour cibler l'exécution active de la session actuelle :

```text
/steer prefer the smaller patch and keep the tests focused
/tell summarize before making the next tool call
```

Comportement :

- Cible uniquement l'exécution active de la session actuelle.
- Fonctionne indépendamment du mode `/queue` de la session.
- Démarre un tour normal avec le même message lorsque la session est inactive ou que l'exécution active ne peut pas accepter de direction.
- Utilise le chemin de direction du runtime actif, de sorte que le modèle voit les conseils à la prochaine limite de runtime supportée.

## Steer vs queue

`/queue steer` fait que les messages entrants normaux essaient de diriger l'exécution active lorsqu'ils arrivent pendant qu'une exécution est en cours. `/steer <message>` est une commande explicite qui essaie d'injecter le message de cette commande dans l'exécution active à la prochaine limite de runtime supportée, indépendamment du paramètre `/queue` stocké. Lorsque cette injection n'est pas disponible, le préfixe de commande est supprimé et `<message>` continue comme une invite normale.

Utilisez :

- `/steer <message>` lorsque vous voulez guider l'exécution active maintenant.
- `/queue steer` lorsque vous voulez que les futurs messages normaux dirigent les exécutions actives par défaut.
- `/queue collect` ou `/queue followup` lorsque les futurs messages normaux doivent attendre un tour ultérieur au lieu de diriger l'exécution active.
- `/queue interrupt` lorsque le message le plus récent doit remplacer l'exécution active au lieu de la diriger.

Pour les modes de file d'attente et les limites de direction, voir [Command queue](/fr/concepts/queue) et [Steering queue](/fr/concepts/queue-steering).

## Sous-agents

Utilisez `/subagents steer` lorsque la cible est une exécution enfant :

```text
/subagents steer 2 focus only on the API surface
```

Le `/steer` au niveau supérieur ne sélectionne pas un sous-agent par id ou index de liste. Il cible toujours l'exécution active de la session actuelle. Voir [Sub-agents](/fr/tools/subagents) pour les ids de sous-agents, les étiquettes et les commandes de contrôle.

## Sessions ACP

Utilisez `/acp steer` lorsque la cible est une session de harnais ACP :

```text
/acp steer --session agent:main:acp:codex tighten the repro
```

Voir [ACP agents](/fr/tools/acp-agents) pour la sélection de session ACP et le comportement du runtime.

## Connexes

- [Slash commands](/fr/tools/slash-commands)
- [Command queue](/fr/concepts/queue)
- [Steering queue](/fr/concepts/queue-steering)
- [Sub-agents](/fr/tools/subagents)
