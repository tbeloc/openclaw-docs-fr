---
summary: "Mémoire de suivi déduite pour les vérifications qui ne sont pas des rappels exacts"
title: "Engagements déduits"
sidebarTitle: "Engagements"
read_when:
  - You want OpenClaw to remember natural follow-ups
  - You want to understand how inferred check-ins differ from reminders
  - You want to review or dismiss follow-up commitments
---

Les engagements sont des mémoires de suivi à courte durée de vie. Lorsqu'ils sont activés, OpenClaw peut remarquer qu'une conversation a créé une opportunité de suivi futur et se souvenir de la ramener plus tard.

Exemples :

- Vous mentionnez un entretien demain. OpenClaw peut faire un suivi après.
- Vous dites que vous êtes épuisé. OpenClaw peut vous demander plus tard si vous avez dormi.
- L'agent dit qu'il fera un suivi après un changement. OpenClaw peut suivre cette boucle ouverte.

Les engagements ne sont pas des faits durables comme `MEMORY.md`, et ce ne sont pas des rappels exacts. Ils se situent entre la mémoire et l'automatisation : OpenClaw se souvient d'une obligation liée à la conversation, puis heartbeat la livre quand elle est due.

## Activer les engagements

Les engagements sont désactivés par défaut. Activez-les dans la configuration :

```bash
openclaw config set commitments.enabled true
openclaw config set commitments.maxPerDay 3
```

Équivalent `openclaw.json` :

```json
{
  "commitments": {
    "enabled": true,
    "maxPerDay": 3
  }
}
```

`commitments.maxPerDay` limite le nombre de suivis déduits qui peuvent être livrés par session d'agent sur un jour glissant. La valeur par défaut est `3`.

## Fonctionnement

Après une réponse d'agent, OpenClaw peut exécuter une passe d'extraction cachée en arrière-plan dans un contexte séparé. Cette passe ne recherche que les engagements de suivi déduits. Elle n'écrit pas dans la conversation visible et ne demande pas à l'agent principal de raisonner sur l'extraction.

Lorsqu'elle trouve un candidat à haute confiance, OpenClaw stocke un engagement avec :

- l'identifiant de l'agent
- la clé de session
- le canal d'origine et la cible de livraison
- une fenêtre d'échéance
- un court suivi suggéré
- suffisamment de contexte source pour que heartbeat décide de l'envoyer

La livraison se fait via heartbeat. Lorsqu'un engagement devient dû, heartbeat ajoute l'engagement au tour heartbeat pour le même agent et la même portée de canal. Le modèle peut envoyer une vérification naturelle ou répondre `HEARTBEAT_OK` pour le rejeter.

OpenClaw ne livre jamais un engagement déduit immédiatement après l'avoir écrit. Le délai d'échéance est limité à au moins un intervalle heartbeat après la création de l'engagement, de sorte que le suivi ne peut pas revenir au même moment où il a été déduit.

## Portée

Les engagements sont limités au contexte exact de l'agent et du canal où ils ont été créés. Un suivi déduit lors d'une conversation avec un agent dans Discord n'est pas livré par un autre agent, un autre canal ou une session non liée.

Cette portée fait partie de la fonctionnalité. Les vérifications naturelles doivent donner l'impression que la même conversation continue, et non comme un système de rappel global.

## Engagements vs rappels

| Besoin                                          | Utiliser                                 |
| ----------------------------------------------- | ---------------------------------------- |
| « Rappelle-moi à 15h »                          | [Tâches planifiées](/fr/automation/cron-jobs) |
| « Ping-moi dans 20 minutes »                    | [Tâches planifiées](/fr/automation/cron-jobs) |
| « Exécute ce rapport tous les jours de semaine » | [Tâches planifiées](/fr/automation/cron-jobs) |
| « J'ai un entretien demain »                    | Engagements                              |
| « J'ai été réveillé toute la nuit »             | Engagements                              |
| « Fais un suivi si je ne réponds pas à ce fil » | Engagements                              |

Les demandes exactes de l'utilisateur appartiennent déjà au chemin du planificateur. Les engagements ne concernent que les suivis déduits : les moments où l'utilisateur n'a pas demandé de rappel, mais la conversation a clairement créé une vérification future utile.

## Gérer les engagements

Utilisez la CLI pour inspecter et effacer les engagements stockés :

```bash
openclaw commitments
openclaw commitments --all
openclaw commitments --agent main
openclaw commitments --status snoozed
openclaw commitments dismiss cm_abc123
```

Voir [`openclaw commitments`](/fr/cli/commitments) pour la référence de commande.

## Confidentialité et coût

L'extraction d'engagement utilise une passe LLM, donc l'activer ajoute une utilisation de modèle en arrière-plan après les tours éligibles. La passe est cachée de la conversation visible par l'utilisateur, mais elle peut lire l'échange récent nécessaire pour décider si un suivi existe.

Les engagements stockés sont l'état local d'OpenClaw. C'est une mémoire opérationnelle, pas une mémoire à long terme. Désactivez la fonctionnalité avec :

```bash
openclaw config set commitments.enabled false
```

## Dépannage

Si les suivis attendus n'apparaissent pas :

- Confirmez que `commitments.enabled` est `true`.
- Vérifiez `openclaw commitments --all` pour les enregistrements en attente, rejetés, reportés ou expirés.
- Assurez-vous que heartbeat s'exécute pour l'agent.
- Vérifiez si `commitments.maxPerDay` a déjà été atteint pour cette session d'agent.
- Rappelez-vous que les rappels exacts sont ignorés par l'extraction d'engagement et doivent apparaître sous [tâches planifiées](/fr/automation/cron-jobs) à la place.

## Connexes

- [Aperçu de la mémoire](/fr/concepts/memory)
- [Mémoire active](/fr/concepts/active-memory)
- [Heartbeat](/fr/gateway/heartbeat)
- [Tâches planifiées](/fr/automation/cron-jobs)
- [`openclaw commitments`](/fr/cli/commitments)
- [Référence de configuration](/fr/gateway/configuration-reference#commitments)
