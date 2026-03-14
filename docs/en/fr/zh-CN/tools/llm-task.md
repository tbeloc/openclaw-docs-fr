---
read_when:
  - Vous devez ajouter une étape LLM en JSON pur à votre flux de travail
  - Vous avez besoin d'une sortie LLM validée par schéma pour l'automatisation
summary: Tâche LLM en JSON pur pour les flux de travail (outil de plugin optionnel)
title: Tâche LLM
x-i18n:
  generated_at: "2026-02-01T21:42:34Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: d81b74fcfd5491a9edb4bfadb47d404067020990b1f6d6d8fed652fbc860f646
  source_path: tools/llm-task.md
  workflow: 15
---

# Tâche LLM

`llm-task` est un **outil de plugin optionnel** permettant d'exécuter des tâches LLM en JSON pur et de retourner une sortie structurée (avec validation optionnelle selon un schéma JSON).

C'est parfait pour les moteurs de flux de travail comme Lobster : vous pouvez ajouter une étape LLM unique sans avoir à écrire du code OpenClaw personnalisé pour chaque flux de travail.

## Activation du plugin

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

2. Ajoutez l'outil à la liste d'autorisation (il est enregistré avec `optional: true`) :

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

## Configuration (optionnelle)

```json
{
  "plugins": {
    "entries": {
      "llm-task": {
        "enabled": true,
        "config": {
          "defaultProvider": "openai-codex",
          "defaultModel": "gpt-5.2",
          "defaultAuthProfileId": "main",
          "allowedModels": ["openai-codex/gpt-5.2"],
          "maxTokens": 800,
          "timeoutMs": 30000
        }
      }
    }
  }
}
```

`allowedModels` est une liste d'autorisation de chaînes `provider/model`. Si défini, toute demande ne figurant pas dans la liste sera rejetée.

## Paramètres de l'outil

- `prompt` (chaîne, obligatoire)
- `input` (tout type, optionnel)
- `schema` (objet, schéma JSON optionnel)
- `provider` (chaîne, optionnel)
- `model` (chaîne, optionnel)
- `authProfileId` (chaîne, optionnel)
- `temperature` (nombre, optionnel)
- `maxTokens` (nombre, optionnel)
- `timeoutMs` (nombre, optionnel)

## Sortie

Retourne `details.json` contenant le JSON analysé (validé selon le `schema` s'il est fourni).

## Exemple : étape de flux de travail Lobster

```lobster
openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
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

## Considérations de sécurité

- Cet outil utilise le **mode JSON pur**, indiquant au modèle de produire uniquement du JSON (sans délimiteurs de code, sans commentaires explicatifs).
- Aucun outil n'est exposé au modèle lors de cette exécution.
- Traitez la sortie comme non fiable sauf si elle est validée avec `schema`.
- Mettez en place un processus d'approbation avant toute étape avec effets secondaires (envoi, publication, exécution).
