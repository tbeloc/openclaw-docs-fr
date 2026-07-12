---
summary: "Rechercher dans les transcriptions de sessions passées et rouvrir le contexte correspondant"
title: "Recherche de session"
read_when:
  - You need to find something discussed in an earlier session
  - You want to understand session search privacy or indexing
---

# Recherche de session

`sessions_search` recherche le texte de l'utilisateur et de l'assistant dans vos propres sessions passées. Chaque résultat
inclut une `sessionKey`, un horodatage, un rôle et un court extrait correspondant. Transmettez la
`sessionKey` retournée à `sessions_history` lorsque vous avez besoin de la conversation environnante.

## Visibilité et résultats

La recherche utilise les mêmes règles de visibilité des sessions que `sessions_history`. Les résultats en dehors de l'arborescence
des sessions visibles de l'appelant sont supprimés avant l'application des limites de résultats. Les agents en sandbox restent limités
aux sessions qu'ils ont générées lorsque la visibilité des sessions générées est activée.

Les extraits sont masqués avant d'être retournés au modèle. Les résultats sont également limités par le nombre, la
longueur de l'extrait et la taille totale de la réponse.

## Cycle de vie de l'index

OpenClaw stocke un index de recherche en texte intégral à côté des lignes de transcription dans la base de données SQLite de chaque agent.
Les nouveaux messages de l'utilisateur et de l'assistant sont indexés dans la même transaction qui les persiste, de sorte que
l'index ne prend jamais du retard sur les conversations en direct ; les résultats des outils, les blocs de raisonnement et les images sont exclus.
Seule la branche active de la transcription est consultable.

Les transcriptions antérieures à l'index (par exemple, les sessions importées par `openclaw doctor`) et
les sessions dont la branche active a été annulée sont réindexées par une réconciliation en arrière-plan qui commence
à la prochaine recherche. Une réponse avec `indexing: true` peut donc être incomplète ; réessayez après
la fin de l'indexation. La suppression d'une session supprime ses entrées d'index dans la même transaction.

La recherche utilise actuellement le tokeniseur Unicode de SQLite avec suppression des diacritiques. La tokenisation trigramme
pour la correspondance de sous-chaînes CJK est une amélioration future.

## Recherche de session vs. recherche de mémoire

Utilisez `sessions_search` pour les mots ou phrases exacts des transcriptions de sessions brutes. Utilisez
[`memory_search`](/fr/concepts/memory-search) pour les fichiers de mémoire durable et la récupération sémantique. Le
corpus session-mémoire expérimental est le complément sémantique de cette recherche de transcription exacte.
