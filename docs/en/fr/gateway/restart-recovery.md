---
summary: "Ce qui survit à un redémarrage ou à un crash de la passerelle : les tours d'agent interrompus reprennent automatiquement, les sous-agents et les tâches de fond se rétablissent, les livraisons en attente s'écoulent"
read_when:
  - You want to know whether restarting the gateway loses in-progress agent work
  - An agent run was interrupted by a restart, crash, or config reload
  - You are debugging automatic session recovery after the gateway comes back up
title: "Restart recovery"
---

Redémarrer la passerelle ne perd pas l'état de l'agent. Les conversations, les transcriptions, les tâches planifiées, les enregistrements de tâches de fond et les messages sortants en attente vivent tous sur le disque, et le travail qui a été interrompu au milieu d'un tour est détecté et repris automatiquement après le redémarrage de la passerelle. Aucune intervention manuelle n'est requise, et il n'y a rien à configurer : la récupération est toujours activée.

Cette page décrit ce qui survit à un redémarrage, comment le travail interrompu est détecté et à quoi ressemble la reprise automatique.

## Ce qui survit à un redémarrage

| État                         | Stockage                                             | Comportement lors du redémarrage                                                 |
| ----------------------------- | --------------------------------------------------- | ----------------------------------------------------------------------- |
| Historique de conversation          | Transcriptions JSONL + magasin de session par agent sur disque | Inchangé ; les sessions continuent à partir de la transcription stockée                 |
| Tour de session principale interrompu | Marqueurs de récupération dans le magasin de session               | Repris automatiquement quelques secondes après le démarrage                       |
| Exécutions de sous-agents                 | SQLite (base de données d'état partagée)                      | Registre restauré au démarrage ; exécutions interrompues reprises                     |
| Tâches de fond              | SQLite (base de données d'état partagée)                      | Réconciliées au démarrage ; exécutions orphelines récupérées ou marquées comme perdues              |
| Livraisons sortantes en attente    | File d'attente de livraison SQLite                               | Drainées après redémarrage ; réponses non livrées sont relancées                  |
| Tâches planifiées (cron)         | Magasin cron SQLite                                   | Les planifications persistent ; le planificateur se réarme au démarrage                        |
| Continuation de redémarrage          | Sentinelle de redémarrage SQLite                             | Suivi ponctuel envoyé à la session qui a demandé le redémarrage |

## Les redémarrages gracieux se drainent d'abord

Un redémarrage demandé (`openclaw gateway restart`, un changement de configuration qui nécessite un redémarrage, ou une mise à jour de la passerelle) ne tue pas immédiatement le travail en cours. La passerelle cesse d'accepter de nouveaux travaux, puis attend que les tours d'agent actifs et les tâches de fond se terminent, jusqu'à un budget de drainage (5 minutes par défaut). La plupart des redémarrages n'interrompent donc rien du tout.

Seul le travail qui ne peut pas se terminer dans le budget de drainage (ou toute exécution interrompue par un redémarrage forcé ou un crash) est abandonné — et avant que cela ne se produise, chaque session affectée est marquée pour récupération.

## Comment le travail interrompu est détecté

Deux mécanismes complémentaires marquent les sessions dont le tour ne s'est pas terminé :

- **À l'arrêt :** pendant le drainage du redémarrage, chaque session avec une exécution active est estampillée avec un marqueur de récupération dans le magasin de session avant que l'exécution ne soit abandonnée.
- **Au démarrage :** la passerelle analyse les magasins de session pour les sessions qui prétendent toujours être en cours d'exécution mais n'ont pas de propriétaire actif dans le nouveau processus. Cela détecte les crashes durs et les arrêts où aucun code d'arrêt n'a été exécuté. Les fichiers de verrouillage de transcription obsolètes sont nettoyés en même temps.

## Reprise automatique

Quelques secondes après le démarrage, la passerelle redépeche chaque session marquée avec un message système synthétique indiquant à l'agent que son tour précédent a été interrompu par un redémarrage et de continuer à partir de la transcription existante. Si une réponse finale avait déjà été produite mais non livrée, son texte est inclus afin que l'agent puisse la livrer au lieu de refaire le travail. La récupération réessaie jusqu'à 3 fois avec backoff exponentiel.

Avant de reprendre, la passerelle vérifie que la queue de transcription est sûre à continuer. Si ce n'est pas le cas (par exemple, le tour s'est terminé sur une approbation en attente obsolète), la session n'est pas aveuglément relancée ; l'agent affiche plutôt un court avis demandant à l'utilisateur de renvoyer la dernière demande.

### Sous-agents

Les exécutions de sous-agents sont persistées dans la base de données d'état SQLite partagée, de sorte que le registre de sous-agents survit au processus. Au démarrage, le registre est restauré et les sessions de sous-agents interrompues sont reprises avec leur contexte de tâche d'origine. Deux soupapes de sécurité s'appliquent :

- Les exécutions interrompues il y a plus de 2 heures sont finalisées au lieu d'être reprises, de sorte qu'une passerelle qui était arrêtée pendant la nuit ne ressuscite pas le travail obsolète.
- Une session qui échoue à se rétablir à plusieurs reprises est marquée comme bloquée afin que la récupération ne puisse pas boucler indéfiniment.

### Tâches de fond

Le [registre des tâches de fond](/fr/automation/tasks) est soutenu par SQLite et réconcilié au démarrage et à intervalles périodiques : les résultats durables enregistrés par les exécutions terminées sont récupérés, et les exécutions dont le processus propriétaire a disparu sont marquées comme perdues après une période de grâce au lieu de rester suspendues indéfiniment.

### Redémarrages demandés par l'agent

Lorsque l'agent lui-même déclenche un redémarrage (en appliquant un changement de configuration, en mettant à jour la passerelle ou une demande de redémarrage explicite), une sentinelle de redémarrage est écrite dans SQLite avant la sortie du processus. Après le démarrage, la passerelle affiche le résultat dans le chat d'origine et envoie un tour de continuation ponctuel afin que l'agent reprenne exactement où il s'était arrêté, sur le même canal et thread.

## Soupapes de sécurité et observabilité

- **Disjoncteur de boucle de crash :** 3 démarrages non propres en 5 minutes déclenchent un disjoncteur qui supprime les services de démarrage automatique au prochain démarrage, de sorte qu'une passerelle qui plante ne s'amplifie pas. Elle se rétablit une fois que la fenêtre de démarrage non propre s'écoule.
- **Métriques :** l'activité de récupération est exportée via [Prometheus](/fr/gateway/prometheus) sous la forme `openclaw_session_recovery_total` et `openclaw_session_recovery_age_seconds`.
- **Journaux :** les décisions de récupération sont enregistrées sous les sous-systèmes `main-session-restart-recovery` et `subagent-interrupted-resume`.

## Ce qui n'est pas repris

- Sessions exclues de la récupération de session principale parce qu'un autre propriétaire les gère déjà : sessions de sous-agents (récupération de sous-agents), sessions cron (le planificateur réexécute selon le calendrier) et sessions gérées par ACP (l'IDE ou le client connecté possède la reprise).
- Sessions dont la queue de transcription ne peut pas être continuée en toute sécurité ; celles-ci reçoivent l'avis de renvoi décrit ci-dessus au lieu d'une réexécution silencieuse.
- Travail qui n'a jamais été admis : les messages arrivant pendant la fenêtre de drainage sont rejetés avec une erreur de redémarrage explicite plutôt que silencieusement mis en attente dans un processus mourant.
