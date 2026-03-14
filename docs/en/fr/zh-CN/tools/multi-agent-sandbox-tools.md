---
read_when: Vous souhaitez un sandboxing par agent ou des politiques d'autorisation/refus d'outils par agent dans une passerelle multi-agent.
status: active
summary: Sandboxing par agent + restrictions d'outils, priorités et exemples
title: Sandbox et outils multi-agent
x-i18n:
  generated_at: "2026-02-03T07:50:39Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: f602cb6192b84b404cd7b6336562888a239d0fe79514edd51bd73c5b090131ef
  source_path: tools/multi-agent-sandbox-tools.md
  workflow: 15
---

# Configuration de sandbox et outils multi-agent

## Aperçu

Chaque agent dans une configuration multi-agent peut désormais avoir ses propres :

- **Configuration de sandbox** (`agents.list[].sandbox` remplace `agents.defaults.sandbox`)
- **Restrictions d'outils** (`tools.allow` / `tools.deny`, ainsi que `agents.list[].tools`)

Cela vous permet d'exécuter plusieurs agents avec des profils de sécurité différents :

- Assistant personnel avec accès complet
- Agents familiaux/professionnels avec outils limités
- Agents publics exécutés dans une sandbox

`setupCommand` se trouve sous `sandbox.docker` (global ou par agent) et s'exécute une fois lors de la création du conteneur.

L'authentification est par agent : chaque agent lit depuis son propre stockage d'authentification `agentDir` :

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

Les identifiants **ne sont pas** partagés entre les agents. Ne réutilisez jamais `agentDir` entre les agents.
Si vous souhaitez partager des identifiants, copiez `auth-profiles.json` dans le `agentDir` des autres agents.

Pour le comportement de l'isolation de sandbox à l'exécution, consultez [Isolation de sandbox](/gateway/sandboxing).
Pour déboguer « pourquoi ceci a-t-il été bloqué ? », consultez [Sandbox vs politique d'outils vs élévation de privilèges](/gateway/sandbox-vs-tool-policy-vs-elevated) et `openclaw sandbox explain`.

---

## Exemples de configuration

### Exemple 1 : Agent personnel + agent familial limité

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "name": "Personal Assistant",
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "family",
        "name": "Family Bot",
        "workspace": "~/.openclaw/workspace-family",
        "sandbox": {
          "mode": "all",
          "scope": "agent"
        },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit", "apply_patch", "process", "browser"]
        }
      }
    ]
  },
  "bindings": [
    {
      "agentId": "family",
      "match": {
        "provider": "whatsapp",
        "accountId": "*",
        "peer": {
          "kind": "group",
          "id": "120363424282127706@g.us"
        }
      }
    }
  ]
}
```

**Résultat :**

- Agent `main` : s'exécute sur l'hôte, accès complet aux outils
- Agent `family` : s'exécute dans Docker (un conteneur par agent), outils `read` uniquement

---

### Exemple 2 : Agent professionnel avec sandbox partagée

```json
{
  "agents": {
    "list": [
      {
        "id": "personal",
        "workspace": "~/.openclaw/workspace-personal",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "work",
        "workspace": "~/.openclaw/workspace-work",
        "sandbox": {
          "mode": "all",
          "scope": "shared",
          "workspaceRoot": "/tmp/work-sandboxes"
        },
        "tools": {
          "allow": ["read", "write", "apply_patch", "exec"],
          "deny": ["browser", "gateway", "discord"]
        }
      }
    ]
  }
}
```

---

### Exemple 2b : Profil de codage global + agent de messagerie uniquement

```json
{
  "tools": { "profile": "coding" },
  "agents": {
    "list": [
      {
        "id": "support",
        "tools": { "profile": "messaging", "allow": ["slack"] }
      }
    ]
  }
}
```

**Résultat :**

- L'agent par défaut obtient les outils de codage
- L'agent `support` est réservé à la messagerie (+ outils Slack)

---

### Exemple 3 : Modes de sandbox différents par agent

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main", // défaut global
        "scope": "session"
      }
    },
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw/workspace",
        "sandbox": {
          "mode": "off" // remplace : main n'est jamais en sandbox
        }
      },
      {
        "id": "public",
        "workspace": "~/.openclaw/workspace-public",
        "sandbox": {
          "mode": "all", // remplace : public est toujours en sandbox
          "scope": "agent"
        },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit", "apply_patch"]
        }
      }
    ]
  }
}
```

---

## Priorité de configuration

Lorsque la configuration globale (`agents.defaults.*`) et spécifique à l'agent (`agents.list[].*`) existent toutes les deux :

### Configuration de sandbox

Les paramètres spécifiques à l'agent remplacent les paramètres globaux :

```
agents.list[].sandbox.mode > agents.defaults.sandbox.mode
agents.list[].sandbox.scope > agents.defaults.sandbox.scope
agents.list[].sandbox.workspaceRoot > agents.defaults.sandbox.workspaceRoot
agents.list[].sandbox.workspaceAccess > agents.defaults.sandbox.workspaceAccess
agents.list[].sandbox.docker.* > agents.defaults.sandbox.docker.*
agents.list[].sandbox.browser.* > agents.defaults.sandbox.browser.*
agents.list[].sandbox.prune.* > agents.defaults.sandbox.prune.*
```

**Remarques :**

- `agents.list[].sandbox.{docker,browser,prune}.*` remplace `agents.defaults.sandbox.{docker,browser,prune}.*` pour cet agent (ignoré lorsque la portée de sandbox se résout en `"shared"`).

### Restrictions d'outils

L'ordre de filtrage est :

1. **Profil d'outils** (`tools.profile` ou `agents.list[].tools.profile`)
2. **Profil d'outils par fournisseur** (`tools.byProvider[provider].profile` ou `agents.list[].tools.byProvider[provider].profile`)
3. **Politique d'outils globale** (`tools.allow` / `tools.deny`)
4. **Politique d'outils par fournisseur** (`tools.byProvider[provider].allow/deny`)
5. **Politique d'outils spécifique à l'agent** (`agents.list[].tools.allow/deny`)
6. **Politique par fournisseur de l'agent** (`agents.list[].tools.byProvider[provider].allow/deny`)
7. **Politique d'outils de sandbox** (`tools.sandbox.tools` ou `agents.list[].tools.sandbox.tools`)
8. **Politique d'outils des sous-agents** (`tools.subagents.tools`, le cas échéant)

Chaque niveau peut restreindre davantage les outils, mais ne peut pas restaurer les outils refusés par les niveaux précédents.
Si `agents.list[].tools.sandbox.tools` est défini, il remplace `tools.sandbox.tools` pour cet agent.
Si `agents.list[].tools.profile` est défini, il remplace `tools.profile` pour cet agent.
Les clés d'outils par fournisseur acceptent `provider` (par exemple `google-antigravity`) ou `provider/model` (par exemple `openai/gpt-5.2`).

### Groupes d'outils (raccourcis)

Les politiques d'outils (globale, agent, sandbox) supportent les entrées `group:*`, qui se développent en plusieurs outils concrets :

- `group:runtime` : `exec`, `bash`, `process`
- `group:fs` : `read`, `write`, `edit`, `apply_patch`
- `group:sessions` : `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
- `group:memory` : `memory_search`, `memory_get`
- `group:ui` : `browser`, `canvas`
- `group:automation` : `cron`, `gateway`
- `group:messaging` : `message`
- `group:nodes` : `nodes`
- `group:openclaw` : tous les outils OpenClaw intégrés (à l'exclusion des plugins de fournisseur)

### Modes d'élévation de privilèges

`tools.elevated` est la ligne de base globale (basée sur la liste d'autorisation de l'expéditeur). `agents.list[].tools.elevated` peut restreindre davantage l'élévation pour des agents spécifiques (les deux doivent autoriser).

Modes d'atténuation :

- Refuser `exec` pour les agents non fiables (`agents.list[].tools.deny: ["exec"]`)
- Éviter de router vers des agents limités après avoir ajouté l'expéditeur à la liste d'autorisation
- Si vous souhaitez uniquement l'exécution en sandbox, désactiver globalement l'élévation (`tools.elevated.enabled: false`)
- Désactiver l'élévation par agent pour les configurations sensibles (`agents.list[].tools.elevated.enabled: false`)

---

## Migration depuis un agent unique

**Avant (agent unique) :**

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.openclaw/workspace",
      "sandbox": {
        "mode": "non-main"
      }
    }
  },
  "tools": {
    "sandbox": {
      "tools": {
        "allow": ["read", "write", "apply_patch", "exec"],
        "deny": []
      }
    }
  }
}
```

**Après (multi-agent avec profils différents) :**

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      }
    ]
  }
}
```

L'ancienne configuration `agent.*` est migrée par `openclaw doctor` ; préférez `agents.defaults` + `agents.list` à l'avenir.

---

## Exemples de restrictions d'outils

### Agent en lecture seule

```json
{
  "tools": {
    "allow": ["read"],
    "deny": ["exec", "write", "edit", "apply_patch", "process"]
  }
}
```

### Agent d'exécution sécurisée (sans modification de fichiers)

```json
{
  "tools": {
    "allow": ["read", "exec", "process"],
    "deny": ["write", "edit", "apply_patch", "browser", "gateway"]
  }
}
```

### Agent de communication uniquement

```json
{
  "tools": {
    "allow": ["sessions_list", "sessions_send", "sessions_history", "session_status"],
    "deny": ["exec", "write", "edit", "apply_patch", "read", "browser"]
  }
}
```

---

## Pièges courants : « non-main »

`agents.defaults.sandbox.mode: "non-main"` est basé sur `session.mainKey` (par défaut `"main"`),
et non sur l'id de l'agent. Les sessions de groupe/canal obtiennent toujours leur propre clé, donc elles
sont considérées comme non-main et seront mises en sandbox. Si vous souhaitez qu'un agent ne soit jamais
mis en sandbox, définissez `agents.list[].sandbox.mode: "off"`.

---

## Tests

Après avoir configuré le sandbox et les outils multi-agent :

1. **Vérifier la résolution des agents :**

   ```exec
   openclaw agents list --bindings
   ```

2. **Vérifier les conteneurs de sandbox :**

   ```exec
   docker ps --filter "name=openclaw-sbx-"
   ```

3. **Tester les restrictions d'outils :**
   - Envoyer des messages nécessitant des outils limités
   - Vérifier que l'agent ne peut pas utiliser les outils refusés

4. **Surveiller les journaux :**
   ```exec
   tail -f "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/logs/gateway.log" | grep -E "routing|sandbox|tools"
   ```

---

## Dépannage

### L'agent n'est pas mis en sandbox malgré `mode: "all"`

- Vérifier s'il y a un `agents.defaults.sandbox.mode` global qui le remplace
- La configuration spécifique à l'agent a priorité, donc définissez `agents.list[].sandbox.mode: "all"`

### L'outil reste disponible malgré la liste de refus

- Vérifier l'ordre de filtrage des outils : global → agent → sandbox → sous-agents
- Chaque niveau ne peut que restreindre davantage, pas restaurer
- Vérifier via les journaux : `[tools] filtering tools for agent:${agentId}`

### Le conteneur n'est pas isolé par agent

- Définir `scope: "agent"` dans la configuration de sandbox spécifique à l'agent
- La valeur par défaut est `"session"`, ce qui crée un conteneur par session

---

## Voir aussi

- [Routage multi-agent](/concepts/multi-agent)
- [Configuration de sandbox](/gateway/configuration#agentsdefaults-sandbox)
- [Gestion des sessions](/concepts/session)
