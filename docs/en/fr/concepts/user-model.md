---
summary: "Stocker les préférences utilisateur durables et les faits de profil en tant qu'entrées USER.md basées sur des directives"
title: "Modèle utilisateur"
read_when:
  - You want stable preferences to guide future sessions
  - You need to update a preference without leaving contradictory history
  - You are deciding whether something belongs in USER.md or MEMORY.md
---

`USER.md` est l'artefact de modèle utilisateur optionnel dans un espace de travail d'agent. Il stocke les préférences stables, le style de communication, les relations et le contexte du projet actif sous forme de directives qui peuvent guider les sessions futures.

OpenClaw charge `USER.md` à côté de `MEMORY.md` au démarrage de la session. Il dispose d'un budget d'amorçage séparé et réduit, et les modifications sont prises en compte lors des tours suivants dans une session longue. Si le fichier est absent, le démarrage se poursuit sans lui.

## Écrire des directives, pas des observations

Chaque entrée comporte une ligne de métadonnées suivie d'une directive impérative :

```md
<!-- observed: 2026-07-27 | status: active -->

- Prefer concise progress updates during implementation work.
```

Utilisez ces règles :

- Commencez par un impératif tel que `Always`, `Never` ou `Prefer`.
- Enregistrez la date à laquelle la préférence a été observée.
- Utilisez uniquement `active` ou `superseded` pour le statut.
- Conservez une seule instruction comportementale par directive.
- Stockez uniquement les détails qui améliorent l'assistance. Ne transformez pas le fichier en dossier.

PrefEval a constaté que le suivi des préférences se dégrade fortement dans les conversations plus longues, même avec la récupération et l'invite ([arXiv:2502.09597](https://arxiv.org/abs/2502.09597)). Reformuler une préférence stable en tant que directive rend le comportement attendu explicite au point où l'agent l'utilise.

## Remplacer sur place

Lorsqu'une préférence change, mettez à jour sa section existante. N'ajoutez pas une deuxième directive active ailleurs dans le fichier.

Avant :

```md
<!-- observed: 2026-05-10 | status: active -->

- Prefer detailed explanations for every code change.
```

Après :

```md
<!-- observed: 2026-05-10 | status: superseded -->

- Prefer detailed explanations for every code change.

<!-- observed: 2026-07-27 | status: active -->

- Prefer concise implementation summaries unless more detail is requested.
```

Conservez l'entrée remplacée à côté de son remplacement afin que la directive actuelle soit sans ambiguïté. HorizonBench rapporte que les systèmes sélectionnent souvent une préférence initialement énoncée après que l'utilisateur l'ait modifiée ([arXiv:2604.17283](https://arxiv.org/abs/2604.17283)) ; un historique contradictoire en ajout seul recrée ce mode de défaillance.

## Choisir le bon fichier

| Information                                                                      | Le stocker dans                                |
| -------------------------------------------------------------------------------- | ---------------------------------------------- |
| Préférence stable ou style de communication                                      | `USER.md`                                      |
| Relation ou fait de projet actif qui change la façon dont l'utilisateur doit être assisté | `USER.md`                                      |
| Fait durable non-profil, décision ou leçon                                       | `MEMORY.md`                                    |
| Observation détaillée ou contexte en cours                                       | `memory/YYYY-MM-DD.md`                         |
| Action future conditionnée par un événement                                      | [Standing intents](/fr/concepts/standing-intents) |
| Action à heure exacte ou récurrente                                              | [Scheduled task](/fr/automation/cron-jobs)        |

## Garder la compacité

`USER.md` dispose intentionnellement d'un budget d'amorçage plus petit que les fichiers généraux de l'espace de travail. Lorsqu'il devient encombré, supprimez les entrées remplacées obsolètes et déplacez les détails du projet qui ne modifient pas le comportement dans la mémoire quotidienne ou `MEMORY.md`.

## Connexes

- [Memory overview](/fr/concepts/memory)
- [Standing intents](/fr/concepts/standing-intents)
- [Agent workspace](/fr/concepts/agent-workspace)
