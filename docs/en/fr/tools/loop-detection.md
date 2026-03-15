---
title: "Détection de boucles d'outils"
description: "Configurez des garde-fous optionnels pour prévenir les boucles d'appels d'outils répétitives ou bloquées"
summary: "Comment activer et ajuster les garde-fous qui détectent les boucles d'appels d'outils répétitives"
read_when:
  - A user reports agents getting stuck repeating tool calls
  - You need to tune repetitive-call protection
  - You are editing agent tool/runtime policies
---

# Détection de boucles d'outils

OpenClaw peut empêcher les agents de rester bloqués dans des motifs d'appels d'outils répétés.
Le garde-fou est **désactivé par défaut**.

Activez-le uniquement où nécessaire, car il peut bloquer les appels répétés légitimes avec des paramètres stricts.

## Pourquoi cela existe

- Détecter les séquences répétitives qui ne font pas de progrès.
- Détecter les boucles sans résultat à haute fréquence (même outil, mêmes entrées, erreurs répétées).
- Détecter des motifs d'appels répétés spécifiques pour les outils d'interrogation connus.

## Bloc de configuration

Valeurs par défaut globales :

```json5
{
  tools: {
    loopDetection: {
      enabled: false,
      historySize: 30,
      warningThreshold: 10,
      criticalThreshold: 20,
      globalCircuitBreakerThreshold: 30,
      detectors: {
        genericRepeat: true,
        knownPollNoProgress: true,
        pingPong: true,
      },
    },
  },
}
```

Remplacement par agent (optionnel) :

```json5
{
  agents: {
    list: [
      {
        id: "safe-runner",
        tools: {
          loopDetection: {
            enabled: true,
            warningThreshold: 8,
            criticalThreshold: 16,
          },
        },
      },
    ],
  },
}
```

### Comportement des champs

- `enabled` : Interrupteur principal. `false` signifie qu'aucune détection de boucle n'est effectuée.
- `historySize` : nombre d'appels d'outils récents conservés pour l'analyse.
- `warningThreshold` : seuil avant de classer un motif comme avertissement uniquement.
- `criticalThreshold` : seuil pour bloquer les motifs de boucles répétitives.
- `globalCircuitBreakerThreshold` : seuil du disjoncteur global sans progrès.
- `detectors.genericRepeat` : détecte les motifs d'outil identique + paramètres identiques répétés.
- `detectors.knownPollNoProgress` : détecte les motifs d'interrogation connus sans changement d'état.
- `detectors.pingPong` : détecte les motifs alternés ping-pong.

## Configuration recommandée

- Commencez avec `enabled: true`, valeurs par défaut inchangées.
- Gardez les seuils ordonnés comme `warningThreshold < criticalThreshold < globalCircuitBreakerThreshold`.
- Si des faux positifs se produisent :
  - augmentez `warningThreshold` et/ou `criticalThreshold`
  - (optionnellement) augmentez `globalCircuitBreakerThreshold`
  - désactivez uniquement le détecteur causant des problèmes
  - réduisez `historySize` pour un contexte historique moins strict

## Journaux et comportement attendu

Lorsqu'une boucle est détectée, OpenClaw signale un événement de boucle et bloque ou atténue le prochain cycle d'outil selon la gravité.
Cela protège les utilisateurs contre les dépenses de jetons incontrôlées et les blocages tout en préservant l'accès normal aux outils.

- Préférez d'abord l'avertissement et la suppression temporaire.
- Escaladez uniquement lorsque des preuves répétées s'accumulent.

## Notes

- `tools.loopDetection` est fusionné avec les remplacements au niveau de l'agent.
- La configuration par agent remplace ou étend complètement les valeurs globales.
- Si aucune configuration n'existe, les garde-fous restent désactivés.
