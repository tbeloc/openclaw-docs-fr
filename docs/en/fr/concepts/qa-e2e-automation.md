---
summary: "Forme privée d'automatisation QA pour qa-lab, qa-channel, scénarios ensemencés et rapports de protocole"
read_when:
  - Extending qa-lab or qa-channel
  - Adding repo-backed QA scenarios
  - Building higher-realism QA automation around the Gateway dashboard
title: "Automatisation E2E QA"
---

# Automatisation E2E QA

La pile QA privée est destinée à exercer OpenClaw d'une manière plus réaliste,
façonnée par canal, qu'un simple test unitaire ne peut le faire.

Éléments actuels :

- `extensions/qa-channel` : canal de messages synthétique avec surfaces DM, canal, thread,
  réaction, édition et suppression.
- `extensions/qa-lab` : interface de débogage et bus QA pour observer la transcription,
  injecter des messages entrants et exporter un rapport Markdown.
- `qa/` : actifs ensemencés sauvegardés dans le dépôt pour la tâche de lancement et les scénarios QA de base.

L'objectif à long terme est un site QA à deux volets :

- Gauche : tableau de bord Gateway (Interface de contrôle) avec l'agent.
- Droite : QA Lab, affichant la transcription de type Slack et le plan de scénario.

Cela permet à un opérateur ou à une boucle d'automatisation de donner à l'agent une mission QA, d'observer
le comportement réel du canal et d'enregistrer ce qui a fonctionné, échoué ou est resté bloqué.

## Ensemencements sauvegardés dans le dépôt

Les actifs ensemencés se trouvent dans `qa/` :

- `qa/QA_KICKOFF_TASK.md`
- `qa/seed-scenarios.json`

Ceux-ci sont intentionnellement dans git afin que le plan QA soit visible pour les humains et l'agent. La liste de base devrait rester suffisamment large pour couvrir :

- Chat DM et canal
- comportement des threads
- cycle de vie des actions de message
- rappels cron
- rappel de mémoire
- changement de modèle
- transfert de sous-agent
- lecture de dépôt et lecture de documentation
- une petite tâche de construction comme Lobster Invaders

## Rapports

`qa-lab` exporte un rapport de protocole Markdown à partir de la chronologie du bus observée.
Le rapport devrait répondre à :

- Ce qui a fonctionné
- Ce qui a échoué
- Ce qui est resté bloqué
- Quels scénarios de suivi valent la peine d'être ajoutés

## Documentation connexe

- [Testing](/fr/help/testing)
- [QA Channel](/fr/channels/qa-channel)
- [Dashboard](/fr/web/dashboard)
