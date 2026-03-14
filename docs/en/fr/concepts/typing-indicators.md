---
summary: "Quand OpenClaw affiche les indicateurs de saisie et comment les ajuster"
read_when:
  - Changing typing indicator behavior or defaults
title: "Indicateurs de saisie"
---

# Indicateurs de saisie

Les indicateurs de saisie sont envoyés au canal de chat pendant qu'une exécution est active. Utilisez
`agents.defaults.typingMode` pour contrôler **quand** la saisie commence et `typingIntervalSeconds`
pour contrôler **à quelle fréquence** elle s'actualise.

## Valeurs par défaut

Quand `agents.defaults.typingMode` est **non défini**, OpenClaw conserve le comportement hérité :

- **Chats directs** : la saisie commence immédiatement une fois que la boucle du modèle commence.
- **Chats de groupe avec mention** : la saisie commence immédiatement.
- **Chats de groupe sans mention** : la saisie commence uniquement quand le texte du message commence à être diffusé en continu.
- **Exécutions de battement cardiaque** : la saisie est désactivée.

## Modes

Définissez `agents.defaults.typingMode` sur l'une des valeurs suivantes :

- `never` — aucun indicateur de saisie, jamais.
- `instant` — commencer la saisie **dès que la boucle du modèle commence**, même si l'exécution
  retourne ensuite uniquement le jeton de réponse silencieuse.
- `thinking` — commencer la saisie au **premier delta de raisonnement** (nécessite
  `reasoningLevel: "stream"` pour l'exécution).
- `message` — commencer la saisie au **premier delta de texte non silencieux** (ignore
  le jeton silencieux `NO_REPLY`).

Ordre « de la rapidité d'activation » :
`never` → `message` → `thinking` → `instant`

## Configuration

```json5
{
  agent: {
    typingMode: "thinking",
    typingIntervalSeconds: 6,
  },
}
```

Vous pouvez remplacer le mode ou la cadence par session :

```json5
{
  session: {
    typingMode: "message",
    typingIntervalSeconds: 4,
  },
}
```

## Remarques

- Le mode `message` n'affichera pas la saisie pour les réponses silencieuses uniquement (par exemple, le jeton
  `NO_REPLY` utilisé pour supprimer la sortie).
- `thinking` ne s'active que si l'exécution diffuse le raisonnement en continu (`reasoningLevel: "stream"`).
  Si le modèle n'émet pas de deltas de raisonnement, la saisie ne commencera pas.
- Les battements cardiaques n'affichent jamais la saisie, quel que soit le mode.
- `typingIntervalSeconds` contrôle la **cadence d'actualisation**, pas l'heure de début.
  La valeur par défaut est 6 secondes.
