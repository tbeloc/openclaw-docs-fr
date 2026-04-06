---
title: "Canal QA"
summary: "Plugin de canal synthétique de type Slack pour des scénarios QA OpenClaw déterministes"
read_when:
  - Vous câblez le transport QA synthétique dans une exécution de test locale ou CI
  - Vous avez besoin de la surface de configuration qa-channel fournie
  - Vous itérez sur l'automatisation QA de bout en bout
---

# Canal QA

`qa-channel` est un transport de message synthétique fourni pour l'assurance qualité automatisée d'OpenClaw.

Ce n'est pas un canal de production. Il existe pour exercer la même limite de plugin de canal utilisée par les transports réels tout en gardant l'état déterministe et entièrement inspectable.

## Ce qu'il fait aujourd'hui

- Grammaire cible de type Slack :
  - `dm:<user>`
  - `channel:<room>`
  - `thread:<room>/<thread>`
- Bus synthétique soutenu par HTTP pour :
  - l'injection de messages entrants
  - la capture de transcription sortante
  - la création de threads
  - les réactions
  - les modifications
  - les suppressions
  - les actions de recherche et de lecture
- Exécuteur d'auto-vérification côté hôte fourni qui écrit un rapport Markdown

## Configuration

```json
{
  "channels": {
    "qa-channel": {
      "baseUrl": "http://127.0.0.1:43123",
      "botUserId": "openclaw",
      "botDisplayName": "OpenClaw QA",
      "allowFrom": ["*"],
      "pollTimeoutMs": 1000
    }
  }
}
```

Clés de compte supportées :

- `baseUrl`
- `botUserId`
- `botDisplayName`
- `pollTimeoutMs`
- `allowFrom`
- `defaultTo`
- `actions.messages`
- `actions.reactions`
- `actions.search`
- `actions.threads`

## Exécuteur

Tranche verticale actuelle :

```bash
pnpm qa:e2e
```

Cela passe maintenant par l'extension `qa-lab` fournie. Il démarre le bus QA dans le dépôt, amorce la tranche d'exécution `qa-channel` fournie, exécute une auto-vérification déterministe et écrit un rapport Markdown sous `.artifacts/qa-e2e/`.

Interface de débogage privée :

```bash
pnpm qa:lab:build
pnpm openclaw qa ui
```

Suite QA complète soutenue par le dépôt :

```bash
pnpm openclaw qa suite
```

Cela lance le débogueur QA privé à une URL locale, séparé du bundle Control UI expédié.

## Portée

La portée actuelle est intentionnellement étroite :

- bus + transport de plugin
- grammaire de routage threadé
- actions de message détenues par le canal
- rapports Markdown

Les travaux de suivi ajouteront :

- Orchestration OpenClaw dockerisée
- exécution de matrice fournisseur/modèle
- découverte de scénarios plus riche
- orchestration native OpenClaw ultérieurement
