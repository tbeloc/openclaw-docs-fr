---
title: OpenShell
summary: "Utilisez OpenShell comme backend de sandbox géré pour les agents OpenClaw"
read_when:
  - You want cloud-managed sandboxes instead of local Docker
  - You are setting up the OpenShell plugin
  - You need to choose between mirror and remote workspace modes
---

# OpenShell

OpenShell est un backend de sandbox géré pour OpenClaw. Au lieu d'exécuter des
conteneurs Docker localement, OpenClaw délègue le cycle de vie du sandbox à la CLI `openshell`,
qui provisionne des environnements distants avec exécution de commandes basée sur SSH.

Le plugin OpenShell réutilise le même transport SSH principal et le même pont de système de fichiers
distant que le [backend SSH](/fr/gateway/sandboxing#ssh-backend) générique. Il ajoute
le cycle de vie spécifique à OpenShell (`sandbox create/get/delete`, `sandbox ssh-config`)
et un mode workspace `mirror` optionnel.

## Prérequis

- La CLI `openshell` installée et dans `PATH` (ou définissez un chemin personnalisé via
  `plugins.entries.openshell.config.command`)
- Un compte OpenShell avec accès aux sandboxes
- OpenClaw Gateway en cours d'exécution sur l'hôte

## Démarrage rapide

1. Activez le plugin et définissez le backend de sandbox :

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        backend: "openshell",
        scope: "session",
        workspaceAccess: "rw",
      },
    },
  },
  plugins: {
    entries: {
      openshell: {
        enabled: true,
        config: {
          from: "openclaw",
          mode: "remote",
        },
      },
    },
  },
}
```

2. Redémarrez la Gateway. Au prochain tour d'agent, OpenClaw crée un sandbox OpenShell
   et achemine l'exécution des outils à travers celui-ci.

3. Vérifiez :

```bash
openclaw sandbox list
openclaw sandbox explain
```

## Modes de workspace

C'est la décision la plus importante lors de l'utilisation d'OpenShell.

### `mirror`

Utilisez `plugins.entries.openshell.config.mode: "mirror"` quand vous voulez que le **workspace local reste canonique**.

Comportement :

- Avant `exec`, OpenClaw synchronise le workspace local dans le sandbox OpenShell.
- Après `exec`, OpenClaw synchronise le workspace distant vers le workspace local.
- Les outils de fichiers fonctionnent toujours via le pont de sandbox, mais le workspace local
  reste la source de vérité entre les tours.

Idéal pour :

- Vous modifiez des fichiers localement en dehors d'OpenClaw et voulez que ces modifications soient visibles dans le
  sandbox automatiquement.
- Vous voulez que le sandbox OpenShell se comporte autant que possible comme le backend Docker.
- Vous voulez que le workspace hôte reflète les écritures du sandbox après chaque tour d'exec.

Compromis : coût de synchronisation supplémentaire avant et après chaque exec.

### `remote`

Utilisez `plugins.entries.openshell.config.mode: "remote"` quand vous voulez que le
**workspace OpenShell devienne canonique**.

Comportement :

- Quand le sandbox est créé pour la première fois, OpenClaw amorce le workspace distant à partir
  du workspace local une seule fois.
- Après cela, `exec`, `read`, `write`, `edit`, et `apply_patch` opèrent
  directement sur le workspace OpenShell distant.
- OpenClaw ne synchronise **pas** les modifications distantes vers le workspace local.
- Les lectures de médias au moment du prompt fonctionnent toujours car les outils de fichiers et de médias lisent via
  le pont de sandbox.

Idéal pour :

- Le sandbox doit vivre principalement du côté distant.
- Vous voulez un surcoût de synchronisation inférieur par tour.
- Vous ne voulez pas que les modifications locales de l'hôte écrasent silencieusement l'état du sandbox distant.

Important : si vous modifiez des fichiers sur l'hôte en dehors d'OpenClaw après l'amorçage initial,
le sandbox distant ne voit **pas** ces modifications. Utilisez
`openclaw sandbox recreate` pour ré-amorcer.

### Choisir un mode

|                          | `mirror`                   | `remote`                  |
| ------------------------ | -------------------------- | ------------------------- |
| **Workspace canonique**  | Hôte local                 | OpenShell distant         |
| **Direction de sync**    | Bidirectionnelle (chaque exec) | Amorçage unique           |
| **Surcoût par tour**     | Plus élevé (upload + download) | Plus faible (ops distantes directes) |
| **Modifications locales visibles ?** | Oui, au prochain exec | Non, jusqu'à recreate     |
| **Idéal pour**           | Workflows de développement | Agents longue durée, CI   |

## Référence de configuration

Toute la configuration OpenShell se trouve sous `plugins.entries.openshell.config` :

| Clé                       | Type                     | Par défaut    | Description                                           |
| ------------------------- | ------------------------ | ------------- | ----------------------------------------------------- |
| `mode`                    | `"mirror"` ou `"remote"` | `"mirror"`    | Mode de synchronisation du workspace                  |
| `command`                 | `string`                 | `"openshell"` | Chemin ou nom de la CLI `openshell`                   |
| `from`                    | `string`                 | `"openclaw"`  | Source de sandbox pour la création initiale           |
| `gateway`                 | `string`                 | —             | Nom de la gateway OpenShell (`--gateway`)             |
| `gatewayEndpoint`         | `string`                 | —             | URL du point de terminaison de la gateway OpenShell (`--gateway-endpoint`) |
| `policy`                  | `string`                 | —             | ID de politique OpenShell pour la création de sandbox |
| `providers`               | `string[]`               | `[]`          | Noms de fournisseurs à attacher lors de la création du sandbox |
| `gpu`                     | `boolean`                | `false`       | Demander des ressources GPU                           |
| `autoProviders`           | `boolean`                | `true`        | Passer `--auto-providers` lors de la création du sandbox |
| `remoteWorkspaceDir`      | `string`                 | `"/sandbox"`  | Workspace principal inscriptible à l'intérieur du sandbox |
| `remoteAgentWorkspaceDir` | `string`                 | `"/agent"`    | Chemin de montage du workspace de l'agent (pour accès en lecture seule) |
| `timeoutSeconds`          | `number`                 | `120`         | Délai d'expiration pour les opérations de la CLI `openshell` |

Les paramètres au niveau du sandbox (`mode`, `scope`, `workspaceAccess`) sont configurés sous
`agents.defaults.sandbox` comme avec n'importe quel backend. Voir
[Sandboxing](/fr/gateway/sandboxing) pour la matrice complète.

## Exemples

### Configuration distante minimale

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        backend: "openshell",
      },
    },
  },
  plugins: {
    entries: {
      openshell: {
        enabled: true,
        config: {
          from: "openclaw",
          mode: "remote",
        },
      },
    },
  },
}
```

### Mode mirror avec GPU

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        backend: "openshell",
        scope: "agent",
        workspaceAccess: "rw",
      },
    },
  },
  plugins: {
    entries: {
      openshell: {
        enabled: true,
        config: {
          from: "openclaw",
          mode: "mirror",
          gpu: true,
          providers: ["openai"],
          timeoutSeconds: 180,
        },
      },
    },
  },
}
```

### OpenShell par agent avec gateway personnalisée

```json5
{
  agents: {
    defaults: {
      sandbox: { mode: "off" },
    },
    list: [
      {
        id: "researcher",
        sandbox: {
          mode: "all",
          backend: "openshell",
          scope: "agent",
          workspaceAccess: "rw",
        },
      },
    ],
  },
  plugins: {
    entries: {
      openshell: {
        enabled: true,
        config: {
          from: "openclaw",
          mode: "remote",
          gateway: "lab",
          gatewayEndpoint: "https://lab.example",
          policy: "strict",
        },
      },
    },
  },
}
```

## Gestion du cycle de vie

Les sandboxes OpenShell sont gérés via la CLI de sandbox normale :

```bash
# Lister tous les runtimes de sandbox (Docker + OpenShell)
openclaw sandbox list

# Inspecter la politique effective
openclaw sandbox explain

# Recréer (supprime le workspace distant, ré-amorce à la prochaine utilisation)
openclaw sandbox recreate --all
```

Pour le mode `remote`, **recreate est particulièrement important** : il supprime le
workspace distant canonique pour cette portée. La prochaine utilisation amorce un nouveau workspace distant à partir
du workspace local.

Pour le mode `mirror`, recreate réinitialise principalement l'environnement d'exécution distant car
le workspace local reste canonique.

### Quand recréer

Recréez après avoir modifié l'un de ces éléments :

- `agents.defaults.sandbox.backend`
- `plugins.entries.openshell.config.from`
- `plugins.entries.openshell.config.mode`
- `plugins.entries.openshell.config.policy`

```bash
openclaw sandbox recreate --all
```

## Limitations actuelles

- Le navigateur de sandbox n'est pas supporté sur le backend OpenShell.
- `sandbox.docker.binds` ne s'applique pas à OpenShell.
- Les boutons de runtime spécifiques à Docker sous `sandbox.docker.*` s'appliquent uniquement au backend
  Docker.

## Comment ça marche

1. OpenClaw appelle `openshell sandbox create` (avec les drapeaux `--from`, `--gateway`,
   `--policy`, `--providers`, `--gpu` configurés).
2. OpenClaw appelle `openshell sandbox ssh-config <name>` pour obtenir les détails de connexion SSH
   du sandbox.
3. Core écrit la configuration SSH dans un fichier temporaire et ouvre une session SSH en utilisant le
   même pont de système de fichiers distant que le backend SSH générique.
4. En mode `mirror` : synchronisez local vers distant avant exec, exécutez, synchronisez vers l'arrière après exec.
5. En mode `remote` : amorce une fois à la création, puis opérez directement sur le
   workspace distant.

## Voir aussi

- [Sandboxing](/fr/gateway/sandboxing) -- modes, portées et comparaison des backends
- [Sandbox vs Tool Policy vs Elevated](/fr/gateway/sandbox-vs-tool-policy-vs-elevated) -- débogage des outils bloqués
- [Multi-Agent Sandbox and Tools](/fr/tools/multi-agent-sandbox-tools) -- remplacements par agent
- [Sandbox CLI](/fr/cli/sandbox) -- commandes `openclaw sandbox`
