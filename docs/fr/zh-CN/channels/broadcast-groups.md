---
read_when:
  - Configurer les groupes de diffusion
  - Déboguer les réponses multi-agents dans WhatsApp
status: experimental
summary: Diffuser des messages WhatsApp à plusieurs agents
title: Groupes de diffusion
x-i18n:
  generated_at: "2026-02-03T07:43:43Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: eaeb4035912c49413e012177cf0bd28b348130d30d3317674418dca728229b70
  source_path: channels/broadcast-groups.md
  workflow: 15
---

# Groupes de diffusion

**Statut :** Fonctionnalité expérimentale  
**Version :** Ajoutée dans la version 2026.1.9

## Aperçu

Les groupes de diffusion permettent à plusieurs agents de traiter et de répondre simultanément au même message. Cela vous permet de créer une équipe d'agents professionnels travaillant en collaboration dans un seul groupe WhatsApp ou un message privé — en utilisant tous le même numéro de téléphone.

Portée actuelle : **WhatsApp uniquement** (canal web).

Les groupes de diffusion sont évalués après la liste blanche des canaux et les règles d'activation des groupes. Dans un groupe WhatsApp, cela signifie que la diffusion se produit lorsque OpenClaw répond normalement (par exemple : lorsqu'il est mentionné, selon votre configuration de groupe).

## Cas d'usage

### 1. Équipe d'agents professionnels

Déployez plusieurs agents avec des responsabilités atomisées et ciblées :

```
Group: "Development Team"
Agents:
  - CodeReviewer (reviews code snippets)
  - DocumentationBot (generates docs)
  - SecurityAuditor (checks for vulnerabilities)
  - TestGenerator (suggests test cases)
```

Chaque agent traite le même message et fournit sa perspective professionnelle.

### 2. Support multilingue

```
Group: "International Support"
Agents:
  - Agent_EN (responds in English)
  - Agent_DE (responds in German)
  - Agent_ES (responds in Spanish)
```

### 3. Flux de travail d'assurance qualité

```
Group: "Customer Support"
Agents:
  - SupportAgent (provides answer)
  - QAAgent (reviews quality, only responds if issues found)
```

### 4. Automatisation des tâches

```
Group: "Project Management"
Agents:
  - TaskTracker (updates task database)
  - TimeLogger (logs time spent)
  - ReportGenerator (creates summaries)
```

## Configuration

### Configuration de base

Ajoutez une section `broadcast` au niveau supérieur (au même niveau que `bindings`). Les clés sont les ID de pair WhatsApp :

- Groupes de chat : JID du groupe (par exemple `120363403215116621@g.us`)
- Messages privés : Numéro de téléphone au format E.164 (par exemple `+15551234567`)

```json
{
  "broadcast": {
    "120363403215116621@g.us": ["alfred", "baerbel", "assistant3"]
  }
}
```

**Résultat :** Lorsque OpenClaw répond dans ce chat, les trois agents s'exécutent.

### Stratégies de traitement

Contrôlez comment les agents traitent les messages :

#### Parallèle (par défaut)

Tous les agents traitent simultanément :

```json
{
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": ["alfred", "baerbel"]
  }
}
```

#### Séquentiel

Les agents traitent dans l'ordre (chacun attend que le précédent se termine) :

```json
{
  "broadcast": {
    "strategy": "sequential",
    "120363403215116621@g.us": ["alfred", "baerbel"]
  }
}
```

### Exemple complet

```json
{
  "agents": {
    "list": [
      {
        "id": "code-reviewer",
        "name": "Code Reviewer",
        "workspace": "/path/to/code-reviewer",
        "sandbox": { "mode": "all" }
      },
      {
        "id": "security-auditor",
        "name": "Security Auditor",
        "workspace": "/path/to/security-auditor",
        "sandbox": { "mode": "all" }
      },
      {
        "id": "docs-generator",
        "name": "Documentation Generator",
        "workspace": "/path/to/docs-generator",
        "sandbox": { "mode": "all" }
      }
    ]
  },
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": ["code-reviewer", "security-auditor", "docs-generator"],
    "120363424282127706@g.us": ["support-en", "support-de"],
    "+15555550123": ["assistant", "logger"]
  }
}
```

## Fonctionnement

### Flux des messages

1. **Réception du message** dans un groupe WhatsApp
2. **Vérification de la diffusion** : Le système vérifie si l'ID de pair est dans `broadcast`
3. **S'il est dans la liste de diffusion** :
   - Tous les agents listés traitent le message
   - Chaque agent a sa propre clé de session et un contexte isolé
   - Les agents traitent en parallèle (par défaut) ou séquentiellement
4. **S'il n'est pas dans la liste de diffusion** :
   - Le routage normal s'applique (première liaison correspondante)

Remarque : Les groupes de diffusion ne contournent pas la liste blanche des canaux ou les règles d'activation des groupes (mentions/commandes, etc.). Ils changent seulement *quels agents s'exécutent* lorsque le message remplit les conditions de traitement.

### Isolation des sessions

Chaque agent dans un groupe de diffusion maintient une isolation complète :

- **Clés de session** (`agent:alfred:whatsapp:group:120363...` vs `agent:baerbel:whatsapp:group:120363...`)
- **Historique de conversation** (les agents ne voient pas les messages des autres agents)
- **Espaces de travail** (bacs à sable indépendants si configurés)
- **Accès aux outils** (listes d'autorisation/refus différentes)
- **Mémoire/contexte** (IDENTITY.md, SOUL.md, etc. indépendants)
- **Tampon de contexte de groupe** (messages de groupe récents pour le contexte) partagé par pair, donc tous les agents de diffusion voient le même contexte lorsqu'ils sont déclenchés

Cela permet à chaque agent d'avoir :

- Des personnalités différentes
- Des accès aux outils différents (par exemple lecture seule vs lecture-écriture)
- Des modèles différents (par exemple opus vs sonnet)
- Des Skills installés différents

### Exemple : Sessions isolées

Dans le groupe `120363403215116621@g.us`, avec les agents `["alfred", "baerbel"]` :

**Contexte d'Alfred :**

```
Session: agent:alfred:whatsapp:group:120363403215116621@g.us
History: [user message, alfred's previous responses]
Workspace: /Users/pascal/openclaw-alfred/
Tools: read, write, exec
```

**Contexte de Bärbel :**

```
Session: agent:baerbel:whatsapp:group:120363403215116621@g.us
History: [user message, baerbel's previous responses]
Workspace: /Users/pascal/openclaw-baerbel/
Tools: read only
```

## Bonnes pratiques

### 1. Gardez les agents ciblés

Concevez chaque agent avec une responsabilité unique et claire :

```json
{
  "broadcast": {
    "DEV_GROUP": ["formatter", "linter", "tester"]
  }
}
```

✅ **Bonne pratique :** Chaque agent a une seule tâche  
❌ **Mauvaise pratique :** Un agent générique "dev-helper"

### 2. Utilisez des noms descriptifs

Clarifiez la fonction de chaque agent :

```json
{
  "agents": {
    "security-scanner": { "name": "Security Scanner" },
    "code-formatter": { "name": "Code Formatter" },
    "test-generator": { "name": "Test Generator" }
  }
}
```

### 3. Configurez des accès aux outils différents

Donnez aux agents uniquement les outils dont ils ont besoin :

```json
{
  "agents": {
    "reviewer": {
      "tools": { "allow": ["read", "exec"] } // Read-only
    },
    "fixer": {
      "tools": { "allow": ["read", "write", "edit", "exec"] } // Read-write
    }
  }
}
```

### 4. Surveillez les performances

Avec plusieurs agents, considérez :

- Utilisez `"strategy": "parallel"` (par défaut) pour plus de vitesse
- Limitez les groupes de diffusion à 5-10 agents
- Utilisez des modèles plus rapides pour les agents plus simples

### 5. Gérez les défaillances avec élégance

Les agents échouent indépendamment. L'erreur d'un agent ne bloque pas les autres :

```
Message → [Agent A ✓, Agent B ✗ error, Agent C ✓]
Result: Agent A and C respond, Agent B logs error
```

## Compatibilité

### Fournisseurs

Les groupes de diffusion supportent actuellement :

- ✅ WhatsApp (implémenté)
- 🚧 Telegram (planifié)
- 🚧 Discord (planifié)
- 🚧 Slack (planifié)

### Routage

Les groupes de diffusion fonctionnent avec le routage existant :

```json
{
  "bindings": [
    {
      "match": { "channel": "whatsapp", "peer": { "kind": "group", "id": "GROUP_A" } },
      "agentId": "alfred"
    }
  ],
  "broadcast": {
    "GROUP_B": ["agent1", "agent2"]
  }
}
```

- `GROUP_A` : Seul alfred répond (routage normal)
- `GROUP_B` : agent1 et agent2 répondent tous les deux (diffusion)

**Priorité :** `broadcast` a priorité sur `bindings`.

## Dépannage

### Les agents ne répondent pas

**Vérifiez :**

1. L'ID de l'agent existe dans `agents.list`
2. Le format de l'ID de pair est correct (par exemple `120363403215116621@g.us`)
3. L'agent n'est pas dans une liste de refus

**Débogage :**

```bash
tail -f ~/.openclaw/logs/gateway.log | grep broadcast
```

### Un seul agent répond

**Raison :** L'ID de pair peut être dans `bindings` mais pas dans `broadcast`.

**Correction :** Ajoutez à la configuration de diffusion ou supprimez des liaisons.

### Problèmes de performance

**Si c'est lent avec beaucoup d'agents :**

- Réduisez le nombre d'agents par groupe
- Utilisez des modèles plus légers (sonnet au lieu d'opus)
- Vérifiez les temps de démarrage du bac à sable

## Exemples

### Exemple 1 : Équipe d'examen de code

```json
{
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": [
      "code-formatter",
      "security-scanner",
      "test-coverage",
      "docs-checker"
    ]
  },
  "agents": {
    "list": [
      {
        "id": "code-formatter",
        "workspace": "~/agents/formatter",
        "tools": { "allow": ["read", "write"] }
      },
      {
        "id": "security-scanner",
        "workspace": "~/agents/security",
        "tools": { "allow": ["read", "exec"] }
      },
      {
        "id": "test-coverage",
        "workspace": "~/agents/testing",
        "tools": { "allow": ["read", "exec"] }
      },
      { "id": "docs-checker", "workspace": "~/agents/docs", "tools": { "allow": ["read"] } }
    ]
  }
}
```

**L'utilisateur envoie :** Un extrait de code  
**Réponses :**

- code-formatter : "Indentation corrigée et ajout de conseils de type"
- security-scanner : "⚠️ Injection SQL possible à la ligne 12"
- test-coverage : "Couverture à 45%, tests manquants pour les cas d'erreur"
- docs-checker : "Docstring manquante pour la fonction `process_data`"

### Exemple 2 : Support multilingue

```json
{
  "broadcast": {
    "strategy": "sequential",
    "+15555550123": ["detect-language", "translator-en", "translator-de"]
  },
  "agents": {
    "list": [
      { "id": "detect-language", "workspace": "~/agents/lang-detect" },
      { "id": "translator-en", "workspace": "~/agents/translate-en" },
      { "id": "translator-de", "workspace": "~/agents/translate-de" }
    ]
  }
}
```

## Référence API

### Schéma de configuration

```typescript
interface OpenClawConfig {
  broadcast?: {
    strategy?: "parallel" | "sequential";
    [peerId: string]: string[];
  };
}
```

### Champs

- `strategy` (optionnel) : Comment traiter les agents
  - `"parallel"` (par défaut) : Tous les agents traitent simultanément
  - `"sequential"` : Les agents traitent dans l'ordre du tableau
- `[peerId]` : JID du groupe WhatsApp, numéro E.164 ou autre ID de pair
  - Valeur : Tableau d'ID d'agents qui doivent traiter le message

## Limitations

1. **Nombre maximum d'agents :** Pas de limite stricte, mais plus de 10 agents peut être lent
2. **Contexte partagé :** Les agents ne voient pas les réponses les uns des autres (par conception)
3. **Ordre des messages :** Les réponses parallèles peuvent arriver dans n'importe quel ordre
4. **Limites de débit :** Tous les agents comptent dans les limites de débit WhatsApp

## Améliorations futures

Fonctionnalités prévues :

- [ ] Mode de contexte partagé (les agents peuvent voir les réponses les uns des autres)
- [ ] Coordination d'agents (les agents peuvent se signaler mutuellement)
- [ ] Sélection dynamique d'agents (choisir les agents en fonction du contenu du message)
- [ ] Priorité des agents (certains agents répondent avant d'autres)

## Voir aussi

- [Configuration multi-agents](/tools/multi-agent-sandbox-tools)
- [Configuration du rout
