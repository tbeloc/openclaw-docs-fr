---
summary: "Tâches LLM JSON uniquement pour les workflows (outil de plugin optionnel)"
read_when:
  - Vous voulez une étape LLM JSON uniquement dans les workflows
  - Vous avez besoin d'une sortie LLM validée par schéma pour l'automatisation
title: "Tâche LLM"
---

# Tâche LLM

`llm-task` est un **outil de plugin optionnel** qui exécute une tâche LLM JSON uniquement et
retourne une sortie structurée (optionnellement validée par rapport à JSON Schema).

C'est idéal pour les moteurs de workflow comme Lobster : vous pouvez ajouter une seule étape LLM
sans écrire de code OpenClaw personnalisé pour chaque workflow.

## Activer le plugin

1. Activez le plugin :

```json
{
  "plugins": {
    "entries": {
      "llm-task": { "enabled": true }
    }
  }
}
```

2. Autorisez l'outil (il est enregistré avec `optional: true`) :

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "allow": ["llm-task"] }
      }
    ]
  }
}
```

## Configuration (optionnel)

```json
{
  "plugins": {
    "entries": {
      "llm-task": {
        "enabled": true,
        "config": {
          "defaultProvider": "openai-codex",
          "defaultModel": "gpt-5.4",
          "defaultAuthProfileId": "main",
          "allowedModels": ["openai-codex/gpt-5.4"],
          "maxTokens": 800,
          "timeoutMs": 30000
        }
      }
    }
  }
}
```

`allowedModels` est une liste blanche de chaînes `provider/model`. Si défini, toute demande
en dehors de la liste est rejetée.

## Paramètres de l'outil

- `prompt` (chaîne, obligatoire)
- `input` (quelconque, optionnel)
- `schema` (objet, JSON Schema optionnel)
- `provider` (chaîne, optionnel)
- `model` (chaîne, optionnel)
- `thinking` (chaîne, optionnel)
- `authProfileId` (chaîne, optionnel)
- `temperature` (nombre, optionnel)
- `maxTokens` (nombre, optionnel)
- `timeoutMs` (nombre, optionnel)

`thinking` accepte les présets de raisonnement OpenClaw standard, tels que `low` ou `medium`.

## Sortie

Retourne `details.json` contenant le JSON analysé (et valide par rapport à
`schema` quand fourni).

## Exemple : étape de workflow Lobster

```lobster
openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
  "thinking": "low",
  "input": {
    "subject": "Hello",
    "body": "Can you help?"
  },
  "schema": {
    "type": "object",
    "properties": {
      "intent": { "type": "string" },
      "draft": { "type": "string" }
    },
    "required": ["intent", "draft"],
    "additionalProperties": false
  }
}'
```

## Notes de sécurité

- L'outil est **JSON uniquement** et demande au modèle de produire uniquement du JSON (pas
  de délimiteurs de code, pas de commentaires).
- Aucun outil n'est exposé au modèle pour cette exécution.
- Traitez la sortie comme non fiable sauf si vous validez avec `schema`.
- Placez les approbations avant toute étape ayant des effets secondaires (envoyer, publier, exécuter).
