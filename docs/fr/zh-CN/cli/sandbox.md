---
read_when: You are managing sandbox containers or debugging sandbox/tool-policy behavior.
status: active
summary: Gérer les conteneurs de bac à sable et vérifier les politiques de bac à sable en vigueur
title: CLI Bac à sable
x-i18n:
  generated_at: "2026-02-03T07:45:18Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 6e1186f26c77e188206ce5e198ab624d6b38bc7bb7c06e4d2281b6935c39e347
  source_path: cli/sandbox.md
  workflow: 15
---

# CLI Bac à sable

Gérez les conteneurs de bac à sable basés sur Docker pour isoler l'exécution des agents.

## Aperçu

OpenClaw peut exécuter des agents dans des conteneurs Docker isolés pour assurer la sécurité. La commande `sandbox` vous aide à gérer ces conteneurs, en particulier après des mises à jour ou des modifications de configuration.

## Commandes

### `openclaw sandbox explain`

Inspectez le mode/portée/accès à l'espace de travail du bac à sable **en vigueur**, la politique d'outils du bac à sable et les contrôles d'escalade de privilèges (avec les chemins de clés pour corriger la configuration).

```bash
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work
openclaw sandbox explain --json
```

### `openclaw sandbox list`

Listez tous les conteneurs de bac à sable avec leur statut et configuration.

```bash
openclaw sandbox list
openclaw sandbox list --browser  # List only browser containers
openclaw sandbox list --json     # JSON output
```

**La sortie inclut :**

- Nom du conteneur et statut (en cours d'exécution/arrêté)
- Image Docker et si elle correspond à la configuration
- Heure de création
- Temps d'inactivité (depuis la dernière utilisation)
- Session/agent associé

### `openclaw sandbox recreate`

Supprimez les conteneurs de bac à sable pour forcer leur recréation avec l'image/configuration mise à jour.

```bash
openclaw sandbox recreate --all                # Recreate all containers
openclaw sandbox recreate --session main       # Specific session
openclaw sandbox recreate --agent mybot        # Specific agent
openclaw sandbox recreate --browser            # Only browser containers
openclaw sandbox recreate --all --force        # Skip confirmation
```

**Options :**

- `--all` : Recréez tous les conteneurs de bac à sable
- `--session <key>` : Recréez les conteneurs d'une session spécifique
- `--agent <id>` : Recréez les conteneurs d'un agent spécifique
- `--browser` : Recréez uniquement les conteneurs de navigateur
- `--force` : Ignorez l'invite de confirmation

**Important :** Les conteneurs seront automatiquement recréés lors de la prochaine utilisation par l'agent.

## Cas d'utilisation

### Après la mise à jour de l'image Docker

```bash
# Pull new image
docker pull openclaw-sandbox:latest
docker tag openclaw-sandbox:latest openclaw-sandbox:bookworm-slim

# Update config to use new image
# Edit config: agents.defaults.sandbox.docker.image (or agents.list[].sandbox.docker.image)

# Recreate containers
openclaw sandbox recreate --all
```

### Après modification de la configuration du bac à sable

```bash
# Edit config: agents.defaults.sandbox.* (or agents.list[].sandbox.*)

# Recreate to apply new config
openclaw sandbox recreate --all
```

### Après modification de setupCommand

```bash
openclaw sandbox recreate --all
# or just one agent:
openclaw sandbox recreate --agent family
```

### Pour un agent spécifique uniquement

```bash
# Update only one agent's containers
openclaw sandbox recreate --agent alfred
```

## Pourquoi en avez-vous besoin ?

**Problème :** Lorsque vous mettez à jour l'image Docker du bac à sable ou la configuration :

- Les conteneurs existants continuent à s'exécuter avec les anciens paramètres
- Les conteneurs ne sont nettoyés qu'après 24 heures d'inactivité
- Les agents fréquemment utilisés conservent indéfiniment les anciens conteneurs

**Solution :** Utilisez `openclaw sandbox recreate` pour forcer la suppression des anciens conteneurs. Ils seront automatiquement recréés avec les paramètres actuels lors de la prochaine utilisation.

Conseil : Préférez `openclaw sandbox recreate` à `docker rm` manuel. Il utilise les conventions de nommage des conteneurs de la passerelle Gateway, évitant les incompatibilités lors des modifications de clés de portée/session.

## Configuration

Les paramètres du bac à sable se trouvent sous `agents.defaults.sandbox` dans `~/.openclaw/openclaw.json` (les paramètres de remplacement par agent se trouvent dans `agents.list[].sandbox`) :

```jsonc
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "all", // off, non-main, all
        "scope": "agent", // session, agent, shared
        "docker": {
          "image": "openclaw-sandbox:bookworm-slim",
          "containerPrefix": "openclaw-sbx-",
          // ... more Docker options
        },
        "prune": {
          "idleHours": 24, // Auto-prune after 24h idle
          "maxAgeDays": 7, // Auto-prune after 7 days
        },
      },
    },
  },
}
```

## Voir aussi

- [Documentation du bac à sable](/gateway/sandboxing)
- [Configuration des agents](/concepts/agent-workspace)
- [Commande Doctor](/gateway/doctor) - Vérifiez les paramètres du bac à sable
