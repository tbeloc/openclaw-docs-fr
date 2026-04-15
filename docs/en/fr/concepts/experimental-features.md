---
title: "Fonctionnalités expérimentales"
summary: "Ce que signifient les drapeaux expérimentaux dans OpenClaw et lesquels sont actuellement documentés"
read_when:
  - You see an `.experimental` config key and want to know whether it is stable
  - You want to try preview runtime features without confusing them with normal defaults
  - You want one place to find the currently documented experimental flags
---

# Fonctionnalités expérimentales

Les fonctionnalités expérimentales dans OpenClaw sont des **surfaces d'aperçu opt-in**. Elles
sont derrière des drapeaux explicites car elles ont encore besoin d'une utilisation réelle avant de
mériter une valeur par défaut stable ou un contrat public durable.

Traitez-les différemment de la configuration normale :

- Gardez-les **désactivées par défaut** sauf si la documentation associée vous dit d'en essayer une.
- Attendez-vous à ce que la **forme et le comportement changent** plus rapidement que la configuration stable.
- Préférez d'abord le chemin stable quand il en existe déjà un.
- Si vous déployez OpenClaw largement, testez les drapeaux expérimentaux dans un environnement plus petit
  avant de les intégrer dans une ligne de base partagée.

## Drapeaux actuellement documentés

| Surface                  | Clé                                                       | À utiliser quand                                                                                                    | Plus d'infos                                                                                          |
| ------------------------ | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Runtime de modèle local      | `agents.defaults.experimental.localModelLean`             | Un backend local plus petit ou plus strict a du mal avec la surface d'outils par défaut complète d'OpenClaw                             | [Local Models](/fr/gateway/local-models)                                                         |
| Recherche en mémoire            | `agents.defaults.memorySearch.experimental.sessionMemory` | Vous voulez que `memory_search` indexe les transcriptions de sessions antérieures et acceptez le coût supplémentaire de stockage/indexation         | [Memory configuration reference](/fr/reference/memory-config#session-memory-search-experimental) |
| Outil de planification structuré | `tools.experimental.planTool`                             | Vous voulez que l'outil structuré `update_plan` soit exposé pour le suivi du travail multi-étapes dans les runtimes et interfaces compatibles | [Gateway configuration reference](/fr/gateway/configuration-reference#toolsexperimental)         |

## Mode lean de modèle local

`agents.defaults.experimental.localModelLean: true` est une soupape de décompression
pour les configurations de modèles locaux plus faibles. Il réduit les outils par défaut lourds comme
`browser`, `cron`, et `message` afin que la forme du prompt soit plus petite et moins fragile
pour les backends à petit contexte ou plus stricts compatibles avec OpenAI.

Ce n'est intentionnellement **pas** le chemin normal. Si votre backend gère le runtime complet
proprement, laissez ceci désactivé.

## Expérimental ne signifie pas caché

Si une fonctionnalité est expérimentale, OpenClaw devrait le dire clairement dans la documentation et dans
le chemin de configuration lui-même. Ce qu'il ne devrait **pas** faire, c'est contrebander un comportement d'aperçu dans un bouton stable et prétendre que c'est normal. C'est comme ça que les surfaces de configuration deviennent désordonnées.
