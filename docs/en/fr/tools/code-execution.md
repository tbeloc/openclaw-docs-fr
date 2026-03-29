---
summary: "code_execution -- exécuter une analyse Python distante en sandbox avec xAI"
read_when:
  - You want to enable or configure code_execution
  - You want remote analysis without local shell access
  - You want to combine x_search or web_search with remote Python analysis
title: "Code Execution"
---

# Code Execution

`code_execution` exécute une analyse Python distante en sandbox sur l'API Responses de xAI.
Ceci est différent de [`exec`](/fr/tools/exec) local :

- `exec` exécute des commandes shell sur votre machine ou nœud
- `code_execution` exécute Python dans le sandbox distant de xAI

Utilisez `code_execution` pour :

- les calculs
- la tabulation
- les statistiques rapides
- l'analyse de type graphique
- l'analyse des données renvoyées par `x_search` ou `web_search`

Ne l'utilisez **pas** quand vous avez besoin de fichiers locaux, de votre shell, de votre repo ou d'appareils appairés. Utilisez [`exec`](/fr/tools/exec) pour cela.

## Configuration

Vous avez besoin d'une clé API xAI. N'importe lequel de ceux-ci fonctionne :

- `XAI_API_KEY`
- `plugins.entries.xai.config.webSearch.apiKey`

Exemple :

```json5
{
  plugins: {
    entries: {
      xai: {
        config: {
          webSearch: {
            apiKey: "xai-...",
          },
          codeExecution: {
            enabled: true,
            model: "grok-4-1-fast",
            maxTurns: 2,
            timeoutSeconds: 30,
          },
        },
      },
    },
  },
}
```

## Comment l'utiliser

Demandez naturellement et rendez l'intention d'analyse explicite :

```text
Use code_execution to calculate the 7-day moving average for these numbers: ...
```

```text
Use x_search to find posts mentioning OpenClaw this week, then use code_execution to count them by day.
```

```text
Use web_search to gather the latest AI benchmark numbers, then use code_execution to compare percent changes.
```

L'outil prend un seul paramètre `task` en interne, donc l'agent doit envoyer la demande d'analyse complète et toutes les données en ligne dans une seule invite.

## Limites

- Ceci est une exécution distante xAI, pas une exécution de processus local.
- Elle doit être traitée comme une analyse éphémère, pas un notebook persistant.
- Ne supposez pas l'accès aux fichiers locaux ou à votre espace de travail.
- Pour les données X fraîches, utilisez d'abord [`x_search`](/fr/tools/web#x_search).

## Voir aussi

- [Web tools](/fr/tools/web)
- [Exec](/fr/tools/exec)
- [xAI](/fr/providers/xai)
