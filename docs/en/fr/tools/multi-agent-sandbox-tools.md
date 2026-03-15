---
summary: "Bac à sable par agent + restrictions d'outils, précédence et exemples"
title: Configuration Multi-Agent Sandbox & Tools
read_when: "Vous souhaitez un bac à sable par agent ou des politiques d'autorisation/refus d'outils par agent dans une passerelle multi-agent."
status: active
---

# Configuration Multi-Agent Sandbox & Tools

## Aperçu

Chaque agent dans une configuration multi-agent peut maintenant avoir :

- **Configuration du bac à sable** (`agents.list[].sandbox` remplace `agents.defaults.sandbox`)
- **Restrictions d'outils** (`tools.allow` / `tools.deny`, plus `agents.list[].tools`)

Cela vous permet d'exécuter plusieurs agents avec des profils de sécurité différents :

- Assistant personnel avec accès complet
- Agents familiaux/professionnels avec outils restreints
- Agents accessibles au public dans des bacs à sable

`setupCommand` doit être placé sous `sandbox.docker` (global ou par agent) et s'exécute une seule fois
lors de la création du conteneur.

L'authentification est par agent : chaque agent lit depuis son propre magasin d'authentification `agentDir` à :

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

Les identifiants **ne sont pas** partagés entre les agents. Ne réutilisez jamais `agentDir` entre les agents.
Si vous souhaitez partager des identifiants, copiez `auth-profiles.json` dans le `agentDir` de l'autre agent.

Pour savoir comment le bac à sable se comporte à l'exécution, consultez [Sandboxing](/fr/gateway/sandboxing).
Pour déboguer « pourquoi ceci est-il bloqué ? », consultez [Sandbox vs Tool Policy vs Elevated](/fr/gateway/sandbox-vs-tool-policy-vs-elevated) et `openclaw sandbox explain`.

---

## Exemples de Configuration

### Exemple 1 : Agent Personnel + Agent Familial Restreint

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

- Agent `main` : S'exécute sur l'hôte, accès complet aux outils
- Agent `family` : S'exécute dans Docker (un conteneur par agent), seul l'outil `read` est disponible

---

### Exemple 2 : Agent Professionnel avec Bac à Sable Partagé

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

- Les agents par défaut obtiennent les outils de codage
- L'agent `support` est réservé à la messagerie (+ outil Slack)

---

### Exemple 3 : Modes de Bac à Sable Différents par Agent

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main", // Défaut global
        "scope": "session"
      }
    },
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw/workspace",
        "sandbox": {
          "mode": "off" // Remplace : main jamais en bac à sable
        }
      },
      {
        "id": "public",
        "workspace": "~/.openclaw/workspace-public",
        "sandbox": {
          "mode": "all", // Remplace : public toujours en bac à sable
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

## Précédence de Configuration

Quand les configurations globales (`agents.defaults.*`) et spécifiques à l'agent (`agents.list[].*`) existent toutes les deux :

### Configuration du Bac à Sable

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

**Notes :**

- `agents.list[].sandbox.{docker,browser,prune}.*` remplace `agents.defaults.sandbox.{docker,browser,prune}.*` pour cet agent (ignoré quand la portée du bac à sable se résout en `"shared"`).

### Restrictions d'Outils

L'ordre de filtrage est :

1. **Profil d'outil** (`tools.profile` ou `agents.list[].tools.profile`)
2. **Profil d'outil par fournisseur** (`tools.byProvider[provider].profile` ou `agents.list[].tools.byProvider[provider].profile`)
3. **Politique d'outil globale** (`tools.allow` / `tools.deny`)
4. **Politique d'outil par fournisseur** (`tools.byProvider[provider].allow/deny`)
5. **Politique d'outil spécifique à l'agent** (`agents.list[].tools.allow/deny`)
6. **Politique de fournisseur par agent** (`agents.list[].tools.byProvider[provider].allow/deny`)
7. **Politique d'outil du bac à sable** (`tools.sandbox.tools` ou `agents.list[].tools.sandbox.tools`)
8. **Politique d'outil du sous-agent** (`tools.subagents.tools`, le cas échéant)

Chaque niveau peut restreindre davantage les outils, mais ne peut pas réaccorder les outils refusés aux niveaux antérieurs.
Si `agents.list[].tools.sandbox.tools` est défini, il remplace `tools.sandbox.tools` pour cet agent.
Si `agents.list[].tools.profile` est défini, il remplace `tools.profile` pour cet agent.
Les clés d'outil par fournisseur acceptent soit `provider` (par ex. `google-antigravity`) soit `provider/model` (par ex. `openai/gpt-5.2`).

### Groupes d'outils (raccourcis)

Les politiques d'outils (global, agent, bac à sable) supportent les entrées `group:*` qui se développent en plusieurs outils concrets :

- `group:runtime`: `exec`, `bash`, `process`
- `group:fs`: `read`, `write`, `edit`, `apply_patch`
- `group:sessions`: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
- `group:memory`: `memory_search`, `memory_get`
- `group:ui`: `browser`, `canvas`
- `group:automation`: `cron`, `gateway`
- `group:messaging`: `message`
- `group:nodes`: `nodes`
- `group:openclaw`: tous les outils OpenClaw intégrés (exclut les plugins de fournisseur)

### Mode Élevé

`tools.elevated` est la ligne de base globale (liste d'autorisation basée sur l'expéditeur). `agents.list[].tools.elevated` peut restreindre davantage le mode élevé pour des agents spécifiques (les deux doivent autoriser).

Modèles d'atténuation :

- Refuser `exec` pour les agents non fiables (`agents.list[].tools.deny: ["exec"]`)
- Éviter d'autoriser les expéditeurs qui acheminent vers des agents restreints
- Désactiver le mode élevé globalement (`tools.elevated.enabled: false`) si vous souhaitez uniquement l'exécution en bac à sable
- Désactiver le mode élevé par agent (`agents.list[].tools.elevated.enabled: false`) pour les profils sensibles

---

## Migration depuis un Agent Unique

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

Les configurations `agent.*` héritées sont migrées par `openclaw doctor` ; préférez `agents.defaults` + `agents.list` à l'avenir.

---

## Exemples de Restriction d'Outils

### Agent en Lecture Seule

```json
{
  "tools": {
    "allow": ["read"],
    "deny": ["exec", "write", "edit", "apply_patch", "process"]
  }
}
```

### Agent d'Exécution Sûr (pas de modifications de fichiers)

```json
{
  "tools": {
    "allow": ["read", "exec", "process"],
    "deny": ["write", "edit", "apply_patch", "browser", "gateway"]
  }
}
```

### Agent de Communication Uniquement

```json
{
  "tools": {
    "sessions": { "visibility": "tree" },
    "allow": ["sessions_list", "sessions_send", "sessions_history", "session_status"],
    "deny": ["exec", "write", "edit", "apply_patch", "read", "browser"]
  }
}
```

---

## Piège Courant : « non-main »

`agents.defaults.sandbox.mode: "non-main"` est basé sur `session.mainKey` (par défaut `"main"`),
pas sur l'ID de l'agent. Les sessions de groupe/canal obtiennent toujours leurs propres clés, donc elles
sont traitées comme non-main et seront mises en bac à sable. Si vous souhaitez qu'un agent ne soit jamais
mis en bac à sable, définissez `agents.list[].sandbox.mode: "off"`.

---

## Test

Après avoir configuré le bac à sable et les outils multi-agent :

1. **Vérifier la résolution de l'agent :**

   ```exec
   openclaw agents list --bindings
   ```

2. **Vérifier les conteneurs du bac à sable :**

   ```exec
   docker ps --filter "name=openclaw-sbx-"
   ```

3. **Tester les restrictions d'outils :**
   - Envoyer un message nécessitant des outils restreints
   - Vérifier que l'agent ne peut pas utiliser les outils refusés

4. **Surveiller les journaux :**

   ```exec
   tail -f "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/logs/gateway.log" | grep -E "routing|sandbox|tools"
   ```

---

## Dépannage

### Agent non mis en bac à sable malgré `mode: "all"`

- Vérifier s'il y a une `agents.defaults.sandbox.mode` globale qui la remplace
- La configuration spécifique à l'agent a la priorité, donc définissez `agents.list[].sandbox.mode: "all"`

### Outils toujours disponibles malgré la liste de refus

- Vérifier l'ordre de filtrage des outils : global → agent → bac à sable → sous-agent
- Chaque niveau ne peut que restreindre davantage, pas réaccorder
- Vérifier avec les journaux : `[tools] filtering tools for agent:${agentId}`

### Conteneur non isolé par agent

- Définir `scope: "agent"` dans la configuration du bac à sable spécifique à l'agent
- La valeur par défaut est `"session"` qui crée un conteneur par session

---

## Voir Aussi

- [Routage Multi-Agent](/fr/concepts/multi-agent)
- [Configuration du Bac à Sable](/fr/gateway/configuration#agentsdefaults-sandbox)
- [Gestion des Sessions](/fr/concepts/session)
