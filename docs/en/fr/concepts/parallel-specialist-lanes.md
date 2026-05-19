---
summary: "Exécutez des agents spécialisés en parallèle sans surcharger la capacité partagée du modèle et des outils"
title: "Voies spécialisées parallèles"
sidebarTitle: "Voies spécialisées"
read_when:
  - You route group chats to dedicated agents
  - You want parallel work without one long task blocking every chat
  - You are designing a multi-agent operations setup
status: active
---

Les voies spécialisées parallèles permettent à une Gateway d'acheminer différents chats ou salons vers différents agents, tout en maintenant une expérience utilisateur rapide. L'astuce consiste à traiter le parallélisme comme un problème de conception de ressources rares, et non simplement comme « plus d'agents ».

## Principes fondamentaux

Une voie spécialisée n'améliore le débit que si elle réduit la contention sur les vrais goulots d'étranglement :

- **Verrous de session** : une seule exécution doit muter une session donnée à la fois.
- **Capacité globale du modèle** : tous les chats visibles partagent toujours les limites du fournisseur.
- **Capacité des outils** : le travail shell, navigateur, réseau et référentiel peut être plus lent que le tour du modèle lui-même.
- **Budget de contexte** : les longs transcriptions rendent chaque tour futur plus lent et moins ciblé.
- **Ambiguïté de propriété** : les agents en double faisant le même travail gaspillent la capacité.

OpenClaw sérialise déjà les exécutions par session et limite le parallélisme global via la [file d'attente des commandes](/fr/concepts/queue). Les voies spécialisées ajoutent une politique par-dessus : quel agent possède quel travail, ce qui reste dans le chat et ce qui devient du travail en arrière-plan.

## Déploiement recommandé

### Phase 1 : contrats de voie + travail lourd en arrière-plan

Donnez à chaque voie un contrat écrit dans son espace de travail et son invite système :

- **Objectif** : le travail que cette voie possède.
- **Non-objectifs** : le travail qu'elle devrait déléguer au lieu de tenter.
- **Budget de chat** : les réponses rapides restent dans le chat ; les tâches longues doivent être brièvement reconnues, puis exécutées dans un sous-agent ou une tâche en arrière-plan.
- **Règle de délégation** : quand une autre voie possède le travail, indiquez où il devrait aller et fournissez un résumé de délégation compact.
- **Règle de risque d'outil** : préférez la plus petite surface d'outil qui peut faire le travail.

C'est la phase la moins chère et elle corrige la plupart des obstructions : un travail de codage ne transforme plus la voie de recherche en mélasse, et chaque chat garde son propre contexte propre.

### Phase 2 : contrôles de priorité et de concurrence

Ajustez la file d'attente et la capacité du modèle autour de la valeur commerciale de chaque voie :

```json5
{
  agents: {
    defaults: {
      maxConcurrent: 4,
      subagents: { maxConcurrent: 8, delegationMode: "prefer" },
    },
  },
  messages: {
    queue: {
      mode: "collect",
      debounceMs: 1000,
      cap: 20,
      drop: "summarize",
    },
  },
}
```

Utilisez les chats directs/personnels et les agents de production-ops pour le travail hautement prioritaire. Laissez la recherche, la rédaction et le codage par lot passer à des tâches en arrière-plan quand le système est occupé.

### Phase 3 : coordinateur / contrôleur de trafic

Ajoutez un petit motif de coordinateur une fois que plusieurs voies sont actives :

- Suivez les tâches de voie actives et les propriétaires.
- Détectez les demandes en double entre les groupes.
- Acheminez les résumés de délégation entre les voies.
- Surfacez uniquement les bloqueurs, les résultats complétés et les décisions que l'humain doit prendre.

Ne commencez pas ici. Un coordinateur sans contrats de voie coordonne simplement le chaos.

## Modèle de contrat de voie minimal

```md
# Contrat de voie

## Possède

- <travail dont cette voie est responsable>

## Ne possède pas

- <travail à déléguer>

## Budget de chat

- Répondez directement aux questions rapides.
- Pour le travail multi-étapes, lent ou lourd en outils : reconnaître brièvement, générer/mettre en arrière-plan le travail, puis retourner le résultat une fois terminé.

## Délégation

Si une autre voie possède la demande, répondez avec :

- voie cible
- objectif
- contexte pertinent
- action suivante exacte

## Posture d'outil

Utilisez la plus petite surface d'outil qui peut accomplir la tâche. Évitez le travail shell ou réseau large à moins que cette voie ne le possède explicitement.
```

## Connexes

- [Routage multi-agent](/fr/concepts/multi-agent)
- [File d'attente des commandes](/fr/concepts/queue)
- [Sous-agents](/fr/tools/subagents)
