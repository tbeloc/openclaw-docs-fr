---
title: Sandbox CLI
summary: "Gérer les conteneurs sandbox et inspecter la politique sandbox effective"
read_when: "Vous gérez des conteneurs sandbox ou déboguez le comportement de la politique sandbox/outil."
status: active
---

# Sandbox CLI

Gérez les conteneurs sandbox basés sur Docker pour l'exécution isolée des agents.

## Aperçu

OpenClaw peut exécuter des agents dans des conteneurs Docker isolés pour la sécurité. Les commandes `sandbox` vous aident à gérer ces conteneurs, notamment après des mises à jour ou des modifications de configuration.

## Commandes

### `openclaw sandbox explain`

Inspectez le mode sandbox **effectif** / portée / accès à l'espace de travail, la politique d'outil sandbox et les portes élevées (avec les chemins de clé de configuration de correction).

```bash
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work
openclaw sandbox explain --json
```

### `openclaw sandbox list`

Listez tous les conteneurs sandbox avec leur statut et leur configuration.

```bash
openclaw sandbox list
openclaw sandbox list --browser  # Lister uniquement les conteneurs de navigateur
openclaw sandbox list --json     # Sortie JSON
```

**La sortie inclut :**

- Nom du conteneur et statut (en cours d'exécution/arrêté)
- Image Docker et si elle correspond à la configuration
- Âge (temps écoulé depuis la création)
- Temps d'inactivité (temps écoulé depuis la dernière utilisation)
- Session/agent associé

### `openclaw sandbox recreate`

Supprimez les conteneurs sandbox pour forcer leur recréation avec les images/configurations mises à jour.

```bash
openclaw sandbox recreate --all                # Recréer tous les conteneurs
openclaw sandbox recreate --session main       # Session spécifique
openclaw sandbox recreate --agent mybot        # Agent spécifique
openclaw sandbox recreate --browser            # Uniquement les conteneurs de navigateur
openclaw sandbox recreate --all --force        # Ignorer la confirmation
```

**Options :**

- `--all` : Recréer tous les conteneurs sandbox
- `--session <key>` : Recréer le conteneur pour une session spécifique
- `--agent <id>` : Recréer les conteneurs pour un agent spécifique
- `--browser` : Recréer uniquement les conteneurs de navigateur
- `--force` : Ignorer l'invite de confirmation

**Important :** Les conteneurs sont automatiquement recréés lors de la prochaine utilisation de l'agent.

## Cas d'utilisation

### Après la mise à jour des images Docker

```bash
# Récupérer la nouvelle image
docker pull openclaw-sandbox:latest
docker tag openclaw-sandbox:latest openclaw-sandbox:bookworm-slim

# Mettre à jour la configuration pour utiliser la nouvelle image
# Éditer la configuration : agents.defaults.sandbox.docker.image (ou agents.list[].sandbox.docker.image)

# Recréer les conteneurs
openclaw sandbox recreate --all
```

### Après modification de la configuration sandbox

```bash
# Éditer la configuration : agents.defaults.sandbox.* (ou agents.list[].sandbox.*)

# Recréer pour appliquer la nouvelle configuration
openclaw sandbox recreate --all
```

### Après modification de setupCommand

```bash
openclaw sandbox recreate --all
# ou juste un agent :
openclaw sandbox recreate --agent family
```

### Pour un agent spécifique uniquement

```bash
# Mettre à jour uniquement les conteneurs d'un agent
openclaw sandbox recreate --agent alfred
```

## Pourquoi est-ce nécessaire ?

**Problème :** Lorsque vous mettez à jour les images Docker sandbox ou la configuration :

- Les conteneurs existants continuent de s'exécuter avec les anciens paramètres
- Les conteneurs ne sont purgés qu'après 24 heures d'inactivité
- Les agents régulièrement utilisés conservent indéfiniment les anciens conteneurs en cours d'exécution

**Solution :** Utilisez `openclaw sandbox recreate` pour forcer la suppression des anciens conteneurs. Ils seront recréés automatiquement avec les paramètres actuels lors de la prochaine utilisation.

Conseil : préférez `openclaw sandbox recreate` à la suppression manuelle `docker rm`. Il utilise la dénomination des conteneurs de la Gateway et évite les incompatibilités lorsque les clés de portée/session changent.

## Configuration

Les paramètres sandbox se trouvent dans `~/.openclaw/openclaw.json` sous `agents.defaults.sandbox` (les remplacements par agent se trouvent dans `agents.list[].sandbox`) :

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
          // ... plus d'options Docker
        },
        "prune": {
          "idleHours": 24, // Purge automatique après 24h d'inactivité
          "maxAgeDays": 7, // Purge automatique après 7 jours
        },
      },
    },
  },
}
```

## Voir aussi

- [Documentation Sandbox](/gateway/sandboxing)
- [Configuration Agent](/concepts/agent-workspace)
- [Commande Doctor](/gateway/doctor) - Vérifier la configuration sandbox
