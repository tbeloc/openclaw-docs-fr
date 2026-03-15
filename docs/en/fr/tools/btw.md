---
summary: "Questions éphémères avec /btw"
read_when:
  - You want to ask a quick side question about the current session
  - You are implementing or debugging BTW behavior across clients
title: "Questions latérales BTW"
---

# Questions latérales BTW

`/btw` vous permet de poser une question latérale rapide sur la **session actuelle** sans
transformer cette question en historique de conversation normal.

Il est modélisé d'après le comportement `/btw` de Claude Code, mais adapté à
l'architecture Gateway et multi-canal d'OpenClaw.

## Ce qu'il fait

Quand vous envoyez :

```text
/btw what changed?
```

OpenClaw :

1. crée un instantané du contexte de session actuel,
2. exécute un appel de modèle **sans outils** séparé,
3. répond uniquement à la question latérale,
4. laisse la tâche principale intacte,
5. **n'écrit pas** la question ou la réponse BTW dans l'historique de session,
6. émet la réponse comme un **résultat latéral en direct** plutôt qu'un message assistant normal.

Le modèle mental important est :

- même contexte de session
- requête latérale séparée et unique
- pas d'appels d'outils
- pas de pollution de contexte futur
- pas de persistance de transcription

## Ce qu'il ne fait pas

`/btw` **ne** :

- crée pas une nouvelle session durable,
- ne continue pas la tâche principale inachevée,
- ne lance pas d'outils ou de boucles d'outils d'agent,
- n'écrit pas les données de question/réponse BTW dans l'historique de transcription,
- n'apparaît pas dans `chat.history`,
- ne survit pas à un rechargement.

C'est intentionnellement **éphémère**.

## Fonctionnement du contexte

BTW utilise la session actuelle comme **contexte d'arrière-plan uniquement**.

Si la tâche principale est actuellement active, OpenClaw crée un instantané de l'état du message actuel
et inclut l'invite principale en cours comme contexte d'arrière-plan, tout en
indiquant explicitement au modèle :

- répondre uniquement à la question latérale,
- ne pas reprendre ou compléter la tâche principale inachevée,
- ne pas émettre d'appels d'outils ou de pseudo-appels d'outils.

Cela maintient BTW isolé de la tâche principale tout en le rendant conscient de ce que
la session concerne.

## Modèle de livraison

BTW **n'est pas** livré comme un message de transcription assistant normal.

Au niveau du protocole Gateway :

- le chat assistant normal utilise l'événement `chat`
- BTW utilise l'événement `chat.side_result`

Cette séparation est intentionnelle. Si BTW réutilisait le chemin d'événement `chat` normal,
les clients le traiteraient comme un historique de conversation régulier.

Parce que BTW utilise un événement en direct séparé et n'est pas rejoué à partir de
`chat.history`, il disparaît après rechargement.

## Comportement de surface

### TUI

Dans TUI, BTW est rendu en ligne dans la vue de session actuelle, mais il reste
éphémère :

- visuellement distinct d'une réponse assistant normale
- peut être fermé avec `Entrée` ou `Échap`
- n'est pas rejoué au rechargement

### Canaux externes

Sur des canaux comme Telegram, WhatsApp et Discord, BTW est livré comme une
réponse unique clairement étiquetée car ces surfaces n'ont pas de concept de superposition éphémère locale.

La réponse est toujours traitée comme un résultat latéral, pas un historique de session normal.

### Interface de contrôle / web

La Gateway émet correctement BTW comme `chat.side_result`, et BTW n'est pas inclus
dans `chat.history`, donc le contrat de persistance est déjà correct pour le web.

L'interface de contrôle actuelle a toujours besoin d'un consommateur `chat.side_result` dédié pour
rendre BTW en direct dans le navigateur. Jusqu'à ce que ce support côté client arrive, BTW est une
fonctionnalité au niveau de la Gateway avec un comportement TUI et de canal externe complet, mais pas encore
une UX de navigateur complète.

## Quand utiliser BTW

Utilisez `/btw` quand vous voulez :

- une clarification rapide sur le travail actuel,
- une réponse factuelle latérale pendant qu'une longue tâche est toujours en cours,
- une réponse temporaire qui ne devrait pas devenir partie du contexte de travail futur de la session.

Exemples :

```text
/btw what file are we editing?
/btw what does this error mean?
/btw summarize the current task in one sentence
/btw what is 17 * 19?
```

## Quand ne pas utiliser BTW

N'utilisez pas `/btw` quand vous voulez que la réponse devienne partie du
contexte de travail futur de la session.

Dans ce cas, posez la question normalement dans la session principale au lieu d'utiliser BTW.

## Connexes

- [Commandes slash](/fr/tools/slash-commands)
- [Niveaux de réflexion](/fr/tools/thinking)
- [Session](/fr/concepts/session)
