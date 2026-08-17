---
summary: "Modes de permission de session, limites de l'espace de travail et examinateurs d'escalade"
read_when:
  - Choosing a permission mode for an agent session
  - Understanding who reviews an exec escalation
  - Comparing session permissions with sandbox and tool policy
title: Modes de permission de session
---

Les modes de permission de session définissent la limite du système de fichiers d'une session et l'examinateur d'escalade exec. La limite est la `sessionRoot` canonique de la session ; le mode détermine ce qui peut se produire à l'intérieur ou à l'extérieur de celle-ci.

| Mode        | Accès au système de fichiers                      | Examinateur d'escalade exec           |
| ----------- | ------------------------------------------------- | ------------------------------------- |
| `read-only` | Lectures sous `sessionRoot` ; outils de mutation omis | Aucun ; exec est refusé                  |
| `guarded`   | Lectures et écritures sous `sessionRoot`              | Un humain après le chemin rapide de la liste d'autorisation |
| `workspace` | Lectures et écritures sous `sessionRoot`              | Examen par LLM, avec secours humain       |
| `full`      | Accès au système de fichiers sans restriction                    | Aucun                                  |

`full` nécessite `operator.admin`. Les autres modes nécessitent `operator.write`.

## Racine de session et valeurs par défaut

La Gateway enregistre `sessionRoot` lors de la création de la session. Un répertoire de travail explicite devient la racine après résolution du chemin canonique. Une session sans répertoire de travail explicite utilise l'espace de travail canonique de l'agent sélectionné.

Les sessions d'arborescence gérées utilisent l'extraction de l'arborescence comme `sessionRoot`. Un répertoire de travail imbriqué reste le `cwd` d'exécution, donc les chemins relatifs commencent là tandis que le confinement du système de fichiers couvre l'ensemble de l'extraction.

Une nouvelle session d'arborescence gérée utilise par défaut `workspace` quand aucun mode n'est spécifié. Les autres sessions sans mode enregistré conservent le comportement existant piloté par la configuration.

## Précédence des politiques et limitation

Un mode de session explicite prend précédence sur les remplacements hérités `execSecurity` et `execAsk` de la session. Quand le mode n'est pas défini, ces champs et la configuration globale ou par agent normale continuent de fonctionner comme avant.

Les planchers de fichiers d'approbation d'hôte, les restrictions de sandbox et la politique d'autorisation/refus d'outils ne peuvent que rendre le résultat effectif plus strict. Un harnais peut également limiter un mode non pris en charge à un tuple de politique compatible plus sûr ; il ne combine pas les champs de tuple en une posture moins restrictive.

Pour les contrôles indépendants de sandbox, de politique d'outils et d'exec élevé, voir [Sandbox vs tool policy vs elevated](/fr/gateway/sandbox-vs-tool-policy-vs-elevated).
