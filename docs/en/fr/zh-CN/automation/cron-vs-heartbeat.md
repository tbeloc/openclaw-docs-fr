---
read_when:
  - Décider comment planifier les tâches périodiques
  - Configurer la surveillance en arrière-plan ou les notifications
  - Optimiser l'utilisation des tokens pour les vérifications régulières
summary: Guide pour choisir entre les pulsations et les tâches planifiées pour l'automatisation
title: Comparaison des tâches planifiées et des pulsations
x-i18n:
  generated_at: "2026-02-01T19:38:18Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 5f71a63181baa41b1c307eb7bfac561df7943d4627077dfa2861eb9f76ab086b
  source_path: automation/cron-vs-heartbeat.md
  workflow: 14
---

# Tâches planifiées et pulsations : quand utiliser quelle méthode

Les pulsations et les tâches planifiées peuvent toutes deux exécuter des tâches selon un calendrier. Ce guide vous aide à choisir le mécanisme approprié en fonction de votre cas d'usage.

## Guide de décision rapide

| Cas d'usage                        | Méthode recommandée        | Raison                                     |
| ---------------------------------- | -------------------------- | ------------------------------------------ |
| Vérifier la boîte de réception toutes les 30 min | Pulsation | Peut être traitée par lot avec d'autres vérifications, consciente du contexte |
| Envoyer un rapport tous les jours à 9h du matin | Tâche planifiée (isolée) | Nécessite un timing précis |
| Surveiller les événements à venir dans le calendrier | Pulsation | Naturellement adaptée à la conscience périodique |
| Exécuter une analyse approfondie hebdomadaire | Tâche planifiée (isolée) | Tâche indépendante, peut utiliser un modèle différent |
| Me rappeler dans 20 minutes | Tâche planifiée (session principale, `--at`) | Rappel unique avec timing précis |
| Vérification de santé du projet en arrière-plan | Pulsation | Piggyback sur un cycle existant |

## Pulsations : conscience périodique

Les pulsations s'exécutent dans la **session principale** à intervalles fixes (par défaut : 30 minutes). Elles sont conçues pour permettre à l'agent de vérifier diverses choses et de présenter les informations importantes.

### Quand utiliser les pulsations

- **Plusieurs vérifications périodiques** : Au lieu de configurer 5 tâches planifiées indépendantes pour vérifier la boîte de réception, le calendrier, la météo, les notifications et l'état du projet, utilisez une seule pulsation pour tout traiter par lot.
- **Décisions conscientes du contexte** : L'agent dispose du contexte complet de la session principale, il peut donc juger intelligemment ce qui est urgent et ce qui peut attendre.
- **Continuité de la conversation** : Les pulsations s'exécutent dans la même session, l'agent se souvient donc de la conversation récente et peut faire un suivi naturel.
- **Surveillance à faible surcharge** : Une pulsation remplace plusieurs petites tâches de sondage.

### Avantages des pulsations

- **Traitement par lot de plusieurs vérifications** : Une seule itération d'agent peut examiner simultanément la boîte de réception, le calendrier et les notifications.
- **Réduction des appels API** : Une pulsation est plus économique que 5 tâches planifiées isolées.
- **Conscience du contexte** : L'agent sait ce que vous faites et peut en conséquence établir les priorités.
- **Suppression intelligente** : Si rien ne nécessite d'attention, l'agent répond `HEARTBEAT_OK` sans envoyer de message.
- **Timing naturel** : Peut dériver légèrement en fonction de la charge de la file d'attente, mais c'est acceptable pour la plupart des surveillances.

### Exemple de pulsation : liste de contrôle HEARTBEAT.md

```md
# Heartbeat checklist

- Check email for urgent messages
- Review calendar for events in next 2 hours
- If a background task finished, summarize results
- If idle for 8+ hours, send a brief check-in
```

L'agent lit cette liste à chaque pulsation et traite tous les éléments en une seule itération.

### Configuration des pulsations

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m", // intervalle
        target: "last", // cible de livraison des alertes
        activeHours: { start: "08:00", end: "22:00" }, // optionnel
      },
    },
  },
}
```

Pour la configuration complète, consultez [Pulsations](/gateway/heartbeat).

## Tâches planifiées : planification précise

Les tâches planifiées s'exécutent à des **moments précis** et peuvent s'exécuter dans des sessions isolées sans affecter le contexte de la session principale.

### Quand utiliser les tâches planifiées

- **Timing précis requis** : "Tous les lundis à 9h00" (plutôt que "vers 9h").
- **Tâches indépendantes** : Tâches qui n'ont pas besoin du contexte de conversation.
- **Modèle/niveau de réflexion différent** : Analyse approfondie nécessitant un modèle plus puissant.
- **Rappels uniques** : Utilisez `--at` pour "me rappeler dans 20 minutes".
- **Tâches bruyantes/fréquentes** : Tâches qui encombreraient l'historique de la session principale.
- **Déclencheurs externes** : Tâches qui doivent s'exécuter indépendamment de l'état actif de l'agent.

### Avantages des tâches planifiées

- **Timing précis** : Supporte les expressions cron à 5 champs avec fuseau horaire.
- **Isolation de session** : S'exécute dans `cron:<jobId>`, ne pollue pas l'historique de la session principale.
- **Remplacement de modèle** : Peut utiliser un modèle moins cher ou plus puissant par tâche.
- **Contrôle de livraison** : Les tâches isolées livrent par défaut un résumé `announce`, optionnellement `none` pour exécution interne uniquement.
- **Pas besoin du contexte d'agent** : S'exécute même si la session principale est inactive ou compressée.
- **Support unique** : `--at` pour les horodatages futurs précis.

### Exemple de tâche planifiée : briefing matinal quotidien

```bash
openclaw cron add \
  --name "Morning briefing" \
  --cron "0 7 * * *" \
  --tz "America/New_York" \
  --session isolated \
  --message "Generate today's briefing: weather, calendar, top emails, news summary." \
  --model opus \
  --announce \
  --channel whatsapp \
  --to "+15551234567"
```

Cela s'exécutera précisément à 7h00 heure de New York chaque jour, utilisant Opus pour la qualité, et livrera directement à WhatsApp.

### Exemple de tâche planifiée : rappel unique

```bash
openclaw cron add \
  --name "Meeting reminder" \
  --at "20m" \
  --session main \
  --system-event "Reminder: standup meeting starts in 10 minutes." \
  --wake now \
  --delete-after-run
```

Pour la référence CLI complète, consultez [Tâches planifiées](/automation/cron-jobs).

## Organigramme de décision

```
La tâche doit-elle s'exécuter à un moment précis ?
  Oui -> Utiliser une tâche planifiée
  Non -> Continuer...

La tâche doit-elle être isolée de la session principale ?
  Oui -> Utiliser une tâche planifiée (isolée)
  Non -> Continuer...

Cette tâche peut-elle être traitée par lot avec d'autres vérifications périodiques ?
  Oui -> Utiliser une pulsation (ajouter à HEARTBEAT.md)
  Non -> Utiliser une tâche planifiée

Est-ce un rappel unique ?
  Oui -> Utiliser une tâche planifiée avec --at
  Non -> Continuer...

Un modèle ou niveau de réflexion différent est-il nécessaire ?
  Oui -> Utiliser une tâche planifiée (isolée) avec --model/--thinking
  Non -> Utiliser une pulsation
```

## Utilisation combinée

La configuration la plus efficace est **l'utilisation des deux** :

1. **Pulsations** pour la surveillance régulière (boîte de réception, calendrier, notifications), traitées par lot toutes les 30 minutes.
2. **Tâches planifiées** pour la planification précise (rapports quotidiens, révisions hebdomadaires) et les rappels uniques.

### Exemple : configuration d'automatisation efficace

**HEARTBEAT.md** (vérifiée toutes les 30 minutes) :

```md
# Heartbeat checklist

- Scan inbox for urgent emails
- Check calendar for events in next 2h
- Review any pending tasks
- Light check-in if quiet for 8+ hours
```

**Tâches planifiées** (timing précis) :

```bash
# Briefing matinal tous les jours à 7h
openclaw cron add --name "Morning brief" --cron "0 7 * * *" --session isolated --message "..." --announce

# Révision de projet tous les lundis à 9h
openclaw cron add --name "Weekly review" --cron "0 9 * * 1" --session isolated --message "..." --model opus

# Rappel unique
openclaw cron add --name "Call back" --at "2h" --session main --system-event "Call back the client" --wake now
```

## Lobster : flux de travail déterministe avec approbation

Lobster est un runtime de flux de travail pour les **pipelines d'outils multi-étapes**, idéal pour les scénarios nécessitant une exécution déterministe et une approbation explicite. Utilisez-le quand la tâche n'est pas juste une itération d'agent unique et que vous avez besoin d'un flux de travail récupérable avec des points de contrôle manuels.

### Quand Lobster est approprié

- **Automatisation multi-étapes** : Vous avez besoin d'un pipeline d'appels d'outils fixe, pas une invite unique.
- **Portes d'approbation** : Les effets secondaires doivent être suspendus jusqu'à votre approbation, puis continuer.
- **Exécutions récupérables** : Continuer un flux de travail suspendu sans réexécuter les étapes précédentes.

### Comment cela fonctionne avec les pulsations et les tâches planifiées

- **Pulsations/Tâches planifiées** décident *quand* exécuter.
- **Lobster** définit *quelles étapes* exécuter une fois que l'exécution commence.

Pour les flux de travail planifiés, utilisez une tâche planifiée ou une pulsation pour déclencher une itération d'agent qui appelle Lobster. Pour les flux de travail ad hoc, appelez Lobster directement.

### Notes d'implémentation (du code)

- Lobster s'exécute en mode outil en tant que **sous-processus local** (CLI `lobster`) et retourne une **enveloppe JSON**.
- Si l'outil retourne `needs_approval`, vous devez reprendre en utilisant `resumeToken` et le drapeau `approve`.
- L'outil est **optionnel** ; il est recommandé de l'activer via `tools.alsoAllow: ["lobster"]`.
- Si `lobsterPath` est transmis, il doit être un **chemin absolu**.

Pour l'utilisation complète et les exemples, consultez [Lobster](/tools/lobster).

## Session principale vs session isolée

Les pulsations et les tâches planifiées peuvent toutes deux interagir avec la session principale, mais de manière différente :

|        | Pulsation                | Tâche planifiée (session principale) | Tâche planifiée (isolée) |
| ------ | ------------------------ | ------------------------------------ | ------------------------ |
| Session | Session principale       | Session principale (via événement système) | `cron:<jobId>` |
| Historique | Partagé                  | Partagé                              | Nouveau à chaque exécution |
| Contexte | Complet                  | Complet                              | Aucun (démarrage à zéro) |
| Modèle | Modèle de session principale | Modèle de session principale | Peut être remplacé |
| Sortie | Livré si non `HEARTBEAT_OK` | Événement système + conseil de pulsation | Résumé announce (par défaut) |

### Quand utiliser une tâche planifiée de session principale

Utilisez `--session main` avec `--system-event` quand vous avez besoin de :

- Rappels/événements apparaissant dans le contexte de la session principale
- L'agent les traite à la prochaine pulsation avec contexte complet
- Pas besoin d'une exécution isolée séparée

```bash
openclaw cron add \
  --name "Check project" \
  --every "4h" \
  --session main \
  --system-event "Time for a project health check" \
  --wake now
```

### Quand utiliser une tâche planifiée isolée

Utilisez `--session isolated` quand vous avez besoin de :

- Un environnement vierge sans contexte antérieur
- Paramètres de modèle ou de réflexion différents
- La sortie livrée directement via `announce` résumé (ou `none` pour exécution interne uniquement)
- L'historique ne pollue pas la session principale

```bash
openclaw cron add \
  --name "Deep analysis" \
  --cron "0 6 * * 0" \
  --session isolated \
  --message "Weekly codebase analysis..." \
  --model opus \
  --thinking high \
  --announce
```

## Considérations de coût

| Mécanisme              | Caractéristiques de coût                           |
| ---------------------- | -------------------------------------------------- |
| Pulsation              | Une itération toutes les N minutes ; s'adapte à la taille de HEARTBEAT.md |
| Tâche planifiée (session principale) | Ajoute un événement à la prochaine pulsation (pas d'itération isolée) |
| Tâche planifiée (isolée) | Une itération d'agent complète par tâche ; peut utiliser un modèle moins cher |

**Recommandations** :

- Gardez `HEARTBEAT.md` concis pour réduire les frais de tokens.
- Regroupez les vérifications similaires dans une pulsation plutô
