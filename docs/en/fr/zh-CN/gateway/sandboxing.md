---
read_when: You want a dedicated explanation of sandboxing or need to tune agents.defaults.sandbox.
status: active
summary: Comment fonctionne l'isolation en bac à sable OpenClaw : modes, portée, accès à l'espace de travail et images
title: Isolation en bac à sable
x-i18n:
  generated_at: "2026-02-03T07:49:29Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 184fc53001fc6b2847bbb1963cc9c54475d62f74555a581a262a448a0333a209
  source_path: gateway/sandboxing.md
  workflow: 15
---

# Isolation en bac à sable

OpenClaw peut **exécuter des outils dans des conteneurs Docker** pour réduire la portée des impacts.
C'est **optionnel** et contrôlé par la configuration (`agents.defaults.sandbox` ou `agents.list[].sandbox`). Si l'isolation en bac à sable est désactivée, les outils s'exécutent sur l'hôte.
La passerelle Gateway reste sur l'hôte ; lorsqu'elle est activée, l'exécution des outils s'effectue dans un bac à sable isolé.

Ce n'est pas une limite de sécurité parfaite, mais elle limite substantiellement l'accès au système de fichiers et aux processus lorsque le modèle se comporte mal.

## Ce qui est isolé en bac à sable

- Exécution des outils (`exec`, `read`, `write`, `edit`, `apply_patch`, `process`, etc.).
- Navigateur en bac à sable optionnel (`agents.defaults.sandbox.browser`).
  - Par défaut, le navigateur en bac à sable démarre automatiquement lorsqu'un outil de navigateur en a besoin (en s'assurant que CDP est accessible).
    Configuré via `agents.defaults.sandbox.browser.autoStart` et `agents.defaults.sandbox.browser.autoStartTimeoutMs`.
  - `agents.defaults.sandbox.browser.allowHostControl` permet aux sessions en bac à sable de cibler explicitement le navigateur hôte.
  - Une liste d'autorisation optionnelle limite `target: "custom"` : `allowedControlUrls`, `allowedControlHosts`, `allowedControlPorts`.

Ce qui n'est PAS isolé en bac à sable :

- Le processus Gateway lui-même.
- Tout outil explicitement autorisé à s'exécuter sur l'hôte (par exemple `tools.elevated`).
  - **L'exec avec privilèges élevés s'exécute sur l'hôte et contourne l'isolation en bac à sable.**
  - Si l'isolation en bac à sable est désactivée, `tools.elevated` ne change pas l'exécution (déjà sur l'hôte). Voir [Mode avec privilèges élevés](/tools/elevated).

## Modes

`agents.defaults.sandbox.mode` contrôle **quand** utiliser l'isolation en bac à sable :

- `"off"` : pas d'isolation en bac à sable.
- `"non-main"` : isole en bac à sable uniquement les sessions **non-principales** (c'est la valeur par défaut si vous voulez que le chat ordinaire s'exécute sur l'hôte).
- `"all"` : chaque session s'exécute dans un bac à sable.
  Remarque : `"non-main"` est basé sur `session.mainKey` (par défaut `"main"`), pas sur l'ID de l'agent.
  Les sessions de groupe/canal utilisent leurs propres clés, elles sont donc considérées comme des sessions non-principales et seront isolées en bac à sable.

## Portée

`agents.defaults.sandbox.scope` contrôle **combien de conteneurs** sont créés :

- `"session"` (par défaut) : un conteneur par session.
- `"agent"` : un conteneur par agent.
- `"shared"` : toutes les sessions en bac à sable partagent un conteneur.

## Accès à l'espace de travail

`agents.defaults.sandbox.workspaceAccess` contrôle **ce que le bac à sable peut voir** :

- `"none"` (par défaut) : les outils voient l'espace de travail du bac à sable sous `~/.openclaw/sandboxes`.
- `"ro"` : monte l'espace de travail de l'agent en lecture seule sur `/agent` (désactive `write`/`edit`/`apply_patch`).
- `"rw"` : monte l'espace de travail de l'agent en lecture-écriture sur `/workspace`.

Les médias entrants sont copiés dans l'espace de travail du bac à sable actif (`media/inbound/*`).
Remarque sur les Skills : l'outil `read` utilise le bac à sable comme racine. Avec `workspaceAccess: "none"`, OpenClaw reflète les Skills éligibles dans l'espace de travail du bac à sable (`.../skills`) pour qu'ils puissent être lus. Avec `"rw"`, les Skills de l'espace de travail peuvent être lus depuis `/workspace/skills`.

## Montages de liaison personnalisés

`agents.defaults.sandbox.docker.binds` monte des répertoires hôtes supplémentaires dans le conteneur.
Format : `host:container:mode` (par exemple `"/home/user/source:/source:rw"`).

Les liaisons globales et par agent sont **fusionnées** (pas remplacées). Sous `scope: "shared"`, les liaisons par agent sont ignorées.

Exemple (code source en lecture seule + socket Docker) :

```json5
{
  agents: {
    defaults: {
      sandbox: {
        docker: {
          binds: ["/home/user/source:/source:ro", "/var/run/docker.sock:/var/run/docker.sock"],
        },
      },
    },
    list: [
      {
        id: "build",
        sandbox: {
          docker: {
            binds: ["/mnt/cache:/cache:rw"],
          },
        },
      },
    ],
  },
}
```

Considérations de sécurité :

- Les liaisons contournent le système de fichiers du bac à sable : elles exposent les chemins hôtes dans n'importe quel mode que vous définissez (`:ro` ou `:rw`).
- Les montages sensibles (par exemple `docker.sock`, clés, clés SSH) doivent être `:ro`, sauf si absolument nécessaire.
- Si vous avez besoin uniquement d'un accès en lecture à l'espace de travail, combinez avec `workspaceAccess: "ro"` ; les modes de liaison restent indépendants.
- Voir [Bac à sable vs politique d'outils vs privilèges élevés](/gateway/sandbox-vs-tool-policy-vs-elevated) pour comprendre comment les liaisons interagissent avec les politiques d'outils et l'exec avec privilèges élevés.

## Images + configuration

Image par défaut : `openclaw-sandbox:bookworm-slim`

Construire une fois :

```bash
scripts/sandbox-setup.sh
```

Remarque : l'image par défaut **ne contient pas** Node. Si les Skills ont besoin de Node (ou d'un autre runtime), soit construisez une image personnalisée, soit installez via `sandbox.docker.setupCommand` (nécessite une sortie réseau + racine accessible en écriture + utilisateur root).

Image du navigateur en bac à sable :

```bash
scripts/sandbox-browser-setup.sh
```

Par défaut, les conteneurs en bac à sable s'exécutent **sans réseau**.
Remplacez via `agents.defaults.sandbox.docker.network`.

Installation Docker et Gateway conteneurisée ici :
[Docker](/install/docker)

## setupCommand (configuration unique du conteneur)

`setupCommand` s'exécute **une seule fois** après la création du conteneur en bac à sable (pas à chaque exécution).
Il s'exécute dans le conteneur via `sh -lc`.

Chemins :

- Global : `agents.defaults.sandbox.docker.setupCommand`
- Par agent : `agents.list[].sandbox.docker.setupCommand`

Pièges courants :

- Le `docker.network` par défaut est `"none"` (pas de sortie), donc l'installation de paquets échouera.
- `readOnlyRoot: true` empêche les écritures ; définissez `readOnlyRoot: false` ou construisez une image personnalisée.
- `user` doit être root pour installer des paquets (omettez `user` ou définissez `user: "0:0"`).
- L'exec en bac à sable **n'hérite pas** du `process.env` hôte. Utilisez `agents.defaults.sandbox.docker.env` (ou une image personnalisée) pour définir les clés API des Skills.

## Politique d'outils + canaux d'échappement

Les politiques d'autorisation/refus des outils s'appliquent toujours avant les règles du bac à sable. Si un outil est refusé globalement ou par agent, l'isolation en bac à sable ne le rétablira pas.

`tools.elevated` est un canal d'échappement explicite qui exécute `exec` sur l'hôte.
La directive `/exec` s'applique uniquement aux expéditeurs autorisés et persiste par session ; pour désactiver complètement `exec`, utilisez la politique d'outils pour refuser (voir [Bac à sable vs politique d'outils vs privilèges élevés](/gateway/sandbox-vs-tool-policy-vs-elevated)).

Débogage :

- Utilisez `openclaw sandbox explain` pour vérifier le mode de bac à sable effectif, la politique d'outils et les clés de configuration de correction.
- Voir [Bac à sable vs politique d'outils vs privilèges élevés](/gateway/sandbox-vs-tool-policy-vs-elevated) pour un modèle mental sur "pourquoi c'est bloqué ?".
  Restez verrouillé.

## Remplacements multi-agents

Chaque agent peut remplacer le bac à sable + outils :
`agents.list[].sandbox` et `agents.list[].tools` (plus `agents.list[].tools.sandbox.tools` pour la politique d'outils en bac à sable).
Voir [Bac à sable et outils multi-agents](/tools/multi-agent-sandbox-tools) pour les priorités.

## Exemple minimal activé

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "none",
      },
    },
  },
}
```

## Documentation connexe

- [Configuration du bac à sable](/gateway/configuration#agentsdefaults-sandbox)
- [Bac à sable et outils multi-agents](/tools/multi-agent-sandbox-tools)
- [Sécurité](/gateway/security)
