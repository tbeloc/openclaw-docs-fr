---
summary: "Fenêtre de contexte + compaction : comment OpenClaw maintient les sessions dans les limites du modèle"
read_when:
  - Vous voulez comprendre la compaction automatique et /compact
  - Vous déboguez des sessions longues qui atteignent les limites de contexte
title: "Compaction"
---

# Fenêtre de contexte et compaction

Chaque modèle a une **fenêtre de contexte** (nombre maximum de tokens qu'il peut voir). Les chats de longue durée accumulent des messages et des résultats d'outils ; une fois la fenêtre serrée, OpenClaw **compacte** l'historique ancien pour rester dans les limites.

## Qu'est-ce que la compaction

La compaction **résume la conversation plus ancienne** en une entrée de résumé compact et conserve les messages récents intacts. Le résumé est stocké dans l'historique de la session, donc les futures requêtes utilisent :

- Le résumé de compaction
- Les messages récents après le point de compaction

La compaction **persiste** dans l'historique JSONL de la session.

## Configuration

Utilisez le paramètre `agents.defaults.compaction` dans votre `openclaw.json` pour configurer le comportement de compaction (mode, tokens cibles, etc.).
La compaction de résumé préserve les identifiants opaques par défaut (`identifierPolicy: "strict"`). Vous pouvez remplacer cela par `identifierPolicy: "off"` ou fournir du texte personnalisé avec `identifierPolicy: "custom"` et `identifierInstructions`.

Vous pouvez optionnellement spécifier un modèle différent pour la résumé de compaction via `agents.defaults.compaction.model`. Ceci est utile lorsque votre modèle principal est un modèle local ou petit et que vous souhaitez que les résumés de compaction soient produits par un modèle plus capable. Le remplacement accepte n'importe quelle chaîne `provider/model-id` :

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "model": "openrouter/anthropic/claude-sonnet-4-5"
      }
    }
  }
}
```

Cela fonctionne également avec les modèles locaux, par exemple un deuxième modèle Ollama dédié à la résumé ou un spécialiste de compaction affiné :

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "model": "ollama/llama3.1:8b"
      }
    }
  }
}
```

Lorsqu'il n'est pas défini, la compaction utilise le modèle principal de l'agent.

## Compaction automatique (activée par défaut)

Lorsqu'une session approche ou dépasse la fenêtre de contexte du modèle, OpenClaw déclenche une compaction automatique et peut réessayer la requête d'origine en utilisant le contexte compacté.

Vous verrez :

- `🧹 Auto-compaction complete` en mode verbeux
- `/status` affichant `🧹 Compactions: <count>`

Avant la compaction, OpenClaw peut exécuter un tour de **vidage de mémoire silencieux** pour stocker des notes durables sur le disque. Voir [Memory](/concepts/memory) pour les détails et la configuration.

## Compaction manuelle

Utilisez `/compact` (optionnellement avec des instructions) pour forcer un passage de compaction :

```
/compact Focus on decisions and open questions
```

## Source de la fenêtre de contexte

La fenêtre de contexte est spécifique au modèle. OpenClaw utilise la définition du modèle du catalogue de fournisseurs configuré pour déterminer les limites.

## Compaction vs élagage

- **Compaction** : résume et **persiste** dans JSONL.
- **Élagage de session** : supprime les anciens **résultats d'outils** uniquement, **en mémoire**, par requête.

Voir [/concepts/session-pruning](/concepts/session-pruning) pour les détails d'élagage.

## Compaction côté serveur OpenAI

OpenClaw supporte également les indices de compaction côté serveur OpenAI Responses pour les modèles OpenAI directs compatibles. Ceci est séparé de la compaction OpenClaw locale et peut s'exécuter en parallèle.

- Compaction locale : OpenClaw résume et persiste dans la session JSONL.
- Compaction côté serveur : OpenAI compacte le contexte du côté du fournisseur lorsque `store` + `context_management` sont activés.

Voir [OpenAI provider](/providers/openai) pour les paramètres de modèle et les remplacements.

## Conseils

- Utilisez `/compact` lorsque les sessions semblent obsolètes ou que le contexte est gonflé.
- Les grandes sorties d'outils sont déjà tronquées ; l'élagage peut réduire davantage l'accumulation de résultats d'outils.
- Si vous avez besoin d'une ardoise vierge, `/new` ou `/reset` démarre un nouvel identifiant de session.
