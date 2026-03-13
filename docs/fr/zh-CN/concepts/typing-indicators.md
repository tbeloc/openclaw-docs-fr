---
read_when:
  - Modifier le comportement ou les paramètres par défaut de l'indicateur de saisie
summary: Quand OpenClaw affiche les indicateurs de saisie et comment les ajuster
title: Indicateurs de saisie
x-i18n:
  generated_at: "2026-02-01T20:24:47Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 8ee82d02829c4ff58462be8bf5bb52f23f519aeda816c2fd8a583e7a317a2e98
  source_path: concepts/typing-indicators.md
  workflow: 14
---

# Indicateurs de saisie

Pendant l'exécution active, les indicateurs de saisie sont envoyés au canal de chat. Utilisez
`agents.defaults.typingMode` pour contrôler **quand** les indicateurs de saisie commencent à s'afficher, et utilisez `typingIntervalSeconds`
pour contrôler la **fréquence de rafraîchissement**.

## Comportement par défaut

Quand `agents.defaults.typingMode` **n'est pas défini**, OpenClaw conserve le comportement hérité :

- **Messages privés** : l'indicateur de saisie s'affiche immédiatement après le début de la boucle du modèle.
- **Mentionné dans un groupe** : l'indicateur de saisie s'affiche immédiatement.
- **Non mentionné dans un groupe** : l'indicateur de saisie s'affiche uniquement quand le texte du message commence à être diffusé en continu.
- **Exécutions de battement cardiaque** : l'indicateur de saisie est désactivé.

## Modes

Définissez `agents.defaults.typingMode` sur l'une des valeurs suivantes :

- `never` — ne jamais afficher l'indicateur de saisie.
- `instant` — afficher l'indicateur de saisie **immédiatement après le début de la boucle du modèle**, même si l'exécution retourne finalement uniquement un jeton de réponse silencieuse.
- `thinking` — commencer à afficher l'indicateur de saisie au **premier incrément de raisonnement** (nécessite `reasoningLevel: "stream"`
  défini lors de l'exécution).
- `message` — commencer à afficher l'indicateur de saisie au **premier incrément de texte non silencieux** (ignore
  les jetons silencieux `NO_REPLY`).

L'ordre de déclenchement du plus tard au plus tôt :
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

Le mode ou la fréquence de rafraîchissement peuvent être remplacés par session :

```json5
{
  session: {
    typingMode: "message",
    typingIntervalSeconds: 4,
  },
}
```

## Remarques

- Le mode `message` n'affiche pas l'indicateur de saisie pour les réponses purement silencieuses (par exemple, le jeton `NO_REPLY`
  utilisé pour supprimer la sortie).
- `thinking` ne se déclenche que quand l'exécution diffuse le raisonnement en continu (`reasoningLevel: "stream"`).
  Si le modèle ne produit pas d'incrément de raisonnement, l'indicateur de saisie ne s'affiche pas.
- Quel que soit le mode utilisé, les exécutions de battement cardiaque n'affichent jamais l'indicateur de saisie.
- `typingIntervalSeconds` contrôle la **fréquence de rafraîchissement**, et non le moment du démarrage.
  La valeur par défaut est 6 secondes.
