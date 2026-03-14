```markdown
---
summary: "Guidance for choosing between heartbeat and cron jobs for automation"
read_when:
  - Deciding how to schedule recurring tasks
  - Setting up background monitoring or notifications
  - Optimizing token usage for periodic checks
title: "Cron vs Heartbeat"
---

# Cron vs Heartbeat : Quand utiliser chacun

Les heartbeats et les cron jobs vous permettent d'exécuter des tâches selon un calendrier. Ce guide vous aide à choisir le bon mécanisme pour votre cas d'usage.

## Guide de décision rapide

| Cas d'usage                             | Recommandé         | Pourquoi                                      |
| ------------------------------------ | ------------------- | ---------------------------------------- |
| Vérifier la boîte de réception toutes les 30 min             | Heartbeat           | Regroupe avec d'autres vérifications, conscient du contexte |
| Envoyer un rapport quotidien à 9h précises       | Cron (isolé)     | Timing exact nécessaire                      |
| Surveiller le calendrier pour les événements à venir | Heartbeat           | Adaptation naturelle pour la sensibilisation périodique       |
| Exécuter une analyse approfondie hebdomadaire             | Cron (isolé)     | Tâche autonome, peut utiliser un modèle différent |
| Me rappeler dans 20 minutes              | Cron (main, `--at`) | One-shot avec timing précis             |
| Vérification de santé du projet en arrière-plan      | Heartbeat           | S'ajoute au cycle existant             |

## Heartbeat : Sensibilisation périodique

Les heartbeats s'exécutent dans la **session principale** à un intervalle régulier (par défaut : 30 min). Ils sont conçus pour que l'agent vérifie les choses et signale tout ce qui est important.

### Quand utiliser heartbeat

- **Plusieurs vérifications périodiques** : Au lieu de 5 cron jobs distincts vérifiant la boîte de réception, le calendrier, la météo, les notifications et l'état du projet, un seul heartbeat peut regrouper tout cela.
- **Décisions conscientes du contexte** : L'agent dispose du contexte complet de la session principale, il peut donc prendre des décisions intelligentes sur ce qui est urgent par rapport à ce qui peut attendre.
- **Continuité conversationnelle** : Les heartbeats partagent la même session, donc l'agent se souvient des conversations récentes et peut faire un suivi naturel.
- **Surveillance à faible surcharge** : Un heartbeat remplace de nombreuses petites tâches de polling.

### Avantages du heartbeat

- **Regroupe plusieurs vérifications** : Un tour d'agent peut examiner la boîte de réception, le calendrier et les notifications ensemble.
- **Réduit les appels API** : Un seul heartbeat est moins cher que 5 cron jobs isolés.
- **Conscient du contexte** : L'agent sait sur quoi vous travaillez et peut prioriser en conséquence.
- **Suppression intelligente** : Si rien ne nécessite d'attention, l'agent répond `HEARTBEAT_OK` et aucun message n'est livré.
- **Timing naturel** : Dérive légèrement en fonction de la charge de la file d'attente, ce qui convient à la plupart des surveillances.

### Exemple de heartbeat : liste de contrôle HEARTBEAT.md

```md
# Liste de contrôle heartbeat

- Vérifier les emails pour les messages urgents
- Examiner le calendrier pour les événements dans les 2 prochaines heures
- Si une tâche en arrière-plan est terminée, résumer les résultats
- Si inactif pendant 8+ heures, envoyer un bref check-in
```

L'agent lit ceci à chaque heartbeat et traite tous les éléments en un seul tour.

### Configuration du heartbeat

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m", // interval
        target: "last", // explicit alert delivery target (default is "none")
        activeHours: { start: "08:00", end: "22:00" }, // optional
      },
    },
  },
}
```

Voir [Heartbeat](/gateway/heartbeat) pour la configuration complète.

## Cron : Planification précise

Les cron jobs s'exécutent à des heures précises et peuvent s'exécuter dans des sessions isolées sans affecter le contexte principal.
Les calendriers récurrents en haut de l'heure sont automatiquement répartis par un décalage déterministe
par job dans une fenêtre de 0-5 minutes.

### Quand utiliser cron

- **Timing exact requis** : « Envoyer ceci à 9h00 chaque lundi » (pas « à peu près à 9h »).
- **Tâches autonomes** : Les tâches qui n'ont pas besoin de contexte conversationnel.
- **Modèle/réflexion différent** : Une analyse lourde qui justifie un modèle plus puissant.
- **Rappels one-shot** : « Me rappeler dans 20 minutes » avec `--at`.
- **Tâches bruyantes/fréquentes** : Les tâches qui encombreraient l'historique de la session principale.
- **Déclencheurs externes** : Les tâches qui doivent s'exécuter indépendamment de l'activité de l'agent.

### Avantages du cron

- **Timing précis** : Expressions cron à 5 ou 6 champs (secondes) avec support des fuseaux horaires.
- **Répartition de charge intégrée** : les calendriers récurrents en haut de l'heure sont décalés jusqu'à 5 minutes par défaut.
- **Contrôle par job** : remplacer le décalage avec `--stagger <duration>` ou forcer le timing exact avec `--exact`.
- **Isolation de session** : S'exécute dans `cron:<jobId>` sans polluer l'historique principal.
- **Remplacements de modèle** : Utiliser un modèle moins cher ou plus puissant par job.
- **Contrôle de livraison** : Les jobs isolés par défaut à `announce` (résumé) ; choisir `none` selon les besoins.
- **Livraison immédiate** : Le mode Announce publie directement sans attendre le heartbeat.
- **Pas de contexte d'agent nécessaire** : S'exécute même si la session principale est inactive ou compactée.
- **Support one-shot** : `--at` pour les timestamps futurs précis.

### Exemple de cron : Briefing matinal quotidien

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

Ceci s'exécute exactement à 7h00 heure de New York, utilise Opus pour la qualité et annonce un résumé directement à WhatsApp.

### Exemple de cron : Rappel one-shot

```bash
openclaw cron add \
  --name "Meeting reminder" \
  --at "20m" \
  --session main \
  --system-event "Reminder: standup meeting starts in 10 minutes." \
  --wake now \
  --delete-after-run
```

Voir [Cron jobs](/automation/cron-jobs) pour la référence CLI complète.

## Organigramme de décision

```
La tâche doit-elle s'exécuter à une heure EXACTE ?
  OUI -> Utiliser cron
  NON  -> Continuer...

La tâche a-t-elle besoin d'isolation de la session principale ?
  OUI -> Utiliser cron (isolé)
  NON  -> Continuer...

Cette tâche peut-elle être regroupée avec d'autres vérifications périodiques ?
  OUI -> Utiliser heartbeat (ajouter à HEARTBEAT.md)
  NON  -> Utiliser cron

Est-ce un rappel one-shot ?
  OUI -> Utiliser cron avec --at
  NON  -> Continuer...

A-t-il besoin d'un modèle différent ou d'un niveau de réflexion différent ?
  OUI -> Utiliser cron (isolé) avec --model/--thinking
  NON  -> Utiliser heartbeat
```

## Combiner les deux

La configuration la plus efficace utilise **les deux** :

1. **Heartbeat** gère la surveillance de routine (boîte de réception, calendrier, notifications) en un seul tour regroupé toutes les 30 minutes.
2. **Cron** gère les calendriers précis (rapports quotidiens, examens hebdomadaires) et les rappels one-shot.

### Exemple : Configuration d'automatisation efficace

**HEARTBEAT.md** (vérifié toutes les 30 min) :

```md
# Liste de contrôle heartbeat

- Analyser la boîte de réception pour les emails urgents
- Vérifier le calendrier pour les événements dans les 2 prochaines heures
- Examiner les tâches en attente
- Vérification légère si calme pendant 8+ heures
```

**Cron jobs** (timing précis) :

```bash
# Briefing matinal quotidien à 7h
openclaw cron add --name "Morning brief" --cron "0 7 * * *" --session isolated --message "..." --announce

# Examen hebdomadaire du projet le lundi à 9h
openclaw cron add --name "Weekly review" --cron "0 9 * * 1" --session isolated --message "..." --model opus

# Rappel one-shot
openclaw cron add --name "Call back" --at "2h" --session main --system-event "Call back the client" --wake now
```

## Lobster : Workflows déterministes avec approbations

Lobster est le runtime de workflow pour les **pipelines d'outils multi-étapes** qui nécessitent une exécution déterministe et des approbations explicites.
Utilisez-le quand la tâche est plus qu'un seul tour d'agent, et vous voulez un workflow reprise avec des points de contrôle humains.

### Quand Lobster convient

- **Automatisation multi-étapes** : Vous avez besoin d'un pipeline fixe d'appels d'outils, pas une invite unique.
- **Portes d'approbation** : Les effets secondaires doivent être en pause jusqu'à approbation, puis reprendre.
- **Exécutions reprenables** : Continuer un workflow en pause sans réexécuter les étapes antérieures.

### Comment il s'associe avec heartbeat et cron

- **Heartbeat/cron** décident _quand_ une exécution se produit.
- **Lobster** définit _quelles étapes_ se produisent une fois l'exécution commencée.

Pour les workflows planifiés, utilisez cron ou heartbeat pour déclencher un tour d'agent qui appelle Lobster.
Pour les workflows ad-hoc, appelez Lobster directement.

### Notes opérationnelles (du code)

- Lobster s'exécute en tant que **sous-processus local** (CLI `lobster`) en mode outil et retourne une **enveloppe JSON**.
- Si l'outil retourne `needs_approval`, vous reprenez avec un `resumeToken` et un drapeau `approve`.
- L'outil est un **plugin optionnel** ; activez-le de manière additive via `tools.alsoAllow: ["lobster"]` (recommandé).
- Lobster s'attend à ce que le CLI `lobster` soit disponible sur `PATH`.

Voir [Lobster](/tools/lobster) pour l'utilisation complète et les exemples.

## Session principale vs session isolée

Heartbeat et cron peuvent tous deux interagir avec la session principale, mais différemment :

|         | Heartbeat                       | Cron (main)              | Cron (isolé)                                 |
| ------- | ------------------------------- | ------------------------ | ----------------------------------------------- |
| Session | Principal                            | Principal (via événement système)  | `cron:<jobId>` ou session personnalisée                |
| Historique | Partagé                          | Partagé                   | Frais à chaque exécution (isolé) / Persistant (personnalisé) |
| Contexte | Complet                            | Complet                   | Aucun (isolé) / Cumulatif (personnalisé)           |
| Modèle   | Modèle de session principale              | Modèle de session principale       | Peut remplacer                                    |
| Sortie  | Livré si pas `HEARTBEAT_OK` | Invite heartbeat + événement | Résumé annoncé (par défaut)                      |

### Quand utiliser cron de session principale

Utilisez `--session main` avec `--system-event` quand vous voulez :

- Le rappel/événement à apparaître dans le contexte de la session principale
- L'agent à le gérer lors du prochain heartbeat avec contexte complet
- Pas d'exécution isolée séparée

```bash
openclaw cron add \
  --name "Check project" \
  --every "4h" \
  --session main \
  --system-event "Time for a project health check" \
  --wake now
```

### Quand utiliser cron isolé

Utilisez `--session isolated` quand vous voulez :

- Une ardoise vierge sans contexte antérieur
- Paramètres de modèle ou de réflexion différents
- Annoncer les résumés directement à un canal
- Un historique qui n'encombre pas la session principale

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

| Mécanisme       | Profil de coût                                            |
| --------------- | ------------------------------------------------------- |
| Heartbeat       | Un tour tous les N minutes ; s'adapte à la taille de HEARTBEAT.md |
| Cron (main)     | Ajoute un événement au prochain heartbeat (pas de tour isolé)         |
| Cron (isolé) | Tour d'agent complet par job ; peut utiliser un modèle moins cher          |

**Conseils** :

- Gardez `HEARTBEAT.md` petit pour minimiser la surcharge de tokens.
- Regroupez les vérifications similaires dans heartbeat au lieu de plusieurs cron jobs.
- Utilisez `target: "none"` sur heartbeat si vous voulez seulement un traitement interne.
- Utilisez cron isolé avec un modèle moins cher pour les tâches de routine.

## Connexes

- [Heartbeat](/gateway/heartbeat) - configuration heartbeat complète
- [Cron jobs](/automation/cron-jobs) - référence CLI et API cron complète
- [System](/cli/system) - événements système + contrôles heartbeat
```
