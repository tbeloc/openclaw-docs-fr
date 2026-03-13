---
summary: "Comment fonctionne le sandboxing OpenClaw : modes, portées, accès à l'espace de travail et images"
title: Sandboxing
read_when: "Vous voulez une explication dédiée du sandboxing ou devez ajuster agents.defaults.sandbox."
status: active
---

# Sandboxing

OpenClaw peut exécuter **des outils à l'intérieur de conteneurs Docker** pour réduire le rayon d'impact.
C'est **optionnel** et contrôlé par la configuration (`agents.defaults.sandbox` ou
`agents.list[].sandbox`). Si le sandboxing est désactivé, les outils s'exécutent sur l'hôte.
La Gateway reste sur l'hôte ; l'exécution des outils s'exécute dans un sandbox isolé
lorsqu'elle est activée.

Ce n'est pas une limite de sécurité parfaite, mais elle limite matériellement l'accès au système de fichiers
et aux processus lorsque le modèle fait quelque chose de stupide.

## Ce qui est sandboxé

- Exécution des outils (`exec`, `read`, `write`, `edit`, `apply_patch`, `process`, etc.).
- Navigateur sandboxé optionnel (`agents.defaults.sandbox.browser`).
  - Par défaut, le navigateur sandbox démarre automatiquement (garantit que CDP est accessible) lorsque l'outil de navigateur en a besoin.
    Configurez via `agents.defaults.sandbox.browser.autoStart` et `agents.defaults.sandbox.browser.autoStartTimeoutMs`.
  - Par défaut, les conteneurs du navigateur sandbox utilisent un réseau Docker dédié (`openclaw-sandbox-browser`) au lieu du réseau global `bridge`.
    Configurez avec `agents.defaults.sandbox.browser.network`.
  - `agents.defaults.sandbox.browser.cdpSourceRange` optionnel restreint l'entrée CDP au bord du conteneur avec une liste blanche CIDR (par exemple `172.21.0.1/32`).
  - L'accès observateur noVNC est protégé par mot de passe par défaut ; OpenClaw émet une URL de jeton de courte durée qui sert une page d'amorçage locale et ouvre noVNC avec le mot de passe dans le fragment d'URL (pas dans les journaux de requête/en-tête).
  - `agents.defaults.sandbox.browser.allowHostControl` permet aux sessions sandboxées de cibler explicitement le navigateur hôte.
  - Les listes blanches optionnelles contrôlent `target: "custom"` : `allowedControlUrls`, `allowedControlHosts`, `allowedControlPorts`.

Non sandboxé :

- Le processus Gateway lui-même.
- Tout outil explicitement autorisé à s'exécuter sur l'hôte (par exemple `tools.elevated`).
  - **L'exécution élevée s'exécute sur l'hôte et contourne le sandboxing.**
  - Si le sandboxing est désactivé, `tools.elevated` ne change pas l'exécution (déjà sur l'hôte). Voir [Mode Élevé](/tools/elevated).

## Modes

`agents.defaults.sandbox.mode` contrôle **quand** le sandboxing est utilisé :

- `"off"` : pas de sandboxing.
- `"non-main"` : sandbox uniquement les sessions **non-main** (par défaut si vous voulez des chats normaux sur l'hôte).
- `"all"` : chaque session s'exécute dans un sandbox.
  Remarque : `"non-main"` est basé sur `session.mainKey` (par défaut `"main"`), pas sur l'ID d'agent.
  Les sessions de groupe/canal utilisent leurs propres clés, elles comptent donc comme non-main et seront sandboxées.

## Portée

`agents.defaults.sandbox.scope` contrôle **combien de conteneurs** sont créés :

- `"session"` (par défaut) : un conteneur par session.
- `"agent"` : un conteneur par agent.
- `"shared"` : un conteneur partagé par toutes les sessions sandboxées.

## Accès à l'espace de travail

`agents.defaults.sandbox.workspaceAccess` contrôle **ce que le sandbox peut voir** :

- `"none"` (par défaut) : les outils voient un espace de travail sandbox sous `~/.openclaw/sandboxes`.
- `"ro"` : monte l'espace de travail de l'agent en lecture seule à `/agent` (désactive `write`/`edit`/`apply_patch`).
- `"rw"` : monte l'espace de travail de l'agent en lecture/écriture à `/workspace`.

Les médias entrants sont copiés dans l'espace de travail sandbox actif (`media/inbound/*`).
Remarque sur les compétences : l'outil `read` est enraciné dans le sandbox. Avec `workspaceAccess: "none"`,
OpenClaw reflète les compétences éligibles dans l'espace de travail sandbox (`.../skills`) pour
qu'elles puissent être lues. Avec `"rw"`, les compétences de l'espace de travail sont lisibles à partir de
`/workspace/skills`.

## Montages de liaison personnalisés

`agents.defaults.sandbox.docker.binds` monte des répertoires hôtes supplémentaires dans le conteneur.
Format : `host:container:mode` (par exemple, `"/home/user/source:/source:rw"`).

Les liaisons globales et par agent sont **fusionnées** (non remplacées). Sous `scope: "shared"`, les liaisons par agent sont ignorées.

`agents.defaults.sandbox.browser.binds` monte des répertoires hôtes supplémentaires dans le conteneur du **navigateur sandbox** uniquement.

- Lorsqu'elle est définie (y compris `[]`), elle remplace `agents.defaults.sandbox.docker.binds` pour le conteneur du navigateur.
- Lorsqu'elle est omise, le conteneur du navigateur revient à `agents.defaults.sandbox.docker.binds` (rétrocompatible).

Exemple (source en lecture seule + un répertoire de données supplémentaire) :

```json5
{
  agents: {
    defaults: {
      sandbox: {
        docker: {
          binds: ["/home/user/source:/source:ro", "/var/data/myapp:/data:ro"],
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

Remarques de sécurité :

- Les liaisons contournent le système de fichiers sandbox : elles exposent les chemins hôtes avec le mode que vous définissez (`:ro` ou `:rw`).
- OpenClaw bloque les sources de liaison dangereuses (par exemple : `docker.sock`, `/etc`, `/proc`, `/sys`, `/dev` et les montages parents qui les exposeraient).
- Les montages sensibles (secrets, clés SSH, identifiants de service) doivent être `:ro` sauf si absolument nécessaire.
- Combinez avec `workspaceAccess: "ro"` si vous n'avez besoin que d'un accès en lecture à l'espace de travail ; les modes de liaison restent indépendants.
- Voir [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated) pour savoir comment les liaisons interagissent avec la politique des outils et l'exécution élevée.

## Images + configuration

Image par défaut : `openclaw-sandbox:bookworm-slim`

Construisez-la une fois :

```bash
scripts/sandbox-setup.sh
```

Remarque : l'image par défaut n'inclut **pas** Node. Si une compétence a besoin de Node (ou
d'autres runtimes), soit créez une image personnalisée, soit installez via
`sandbox.docker.setupCommand` (nécessite une sortie réseau + racine inscriptible +
utilisateur root).

Si vous voulez une image sandbox plus fonctionnelle avec des outils courants (par exemple
`curl`, `jq`, `nodejs`, `python3`, `git`), construisez :

```bash
scripts/sandbox-common-setup.sh
```

Puis définissez `agents.defaults.sandbox.docker.image` sur
`openclaw-sandbox-common:bookworm-slim`.

Image du navigateur sandboxé :

```bash
scripts/sandbox-browser-setup.sh
```

Par défaut, les conteneurs sandbox s'exécutent **sans réseau**.
Remplacez par `agents.defaults.sandbox.docker.network`.

L'image du navigateur sandbox fournie applique également des paramètres de démarrage Chromium conservateurs
pour les charges de travail conteneurisées. Les paramètres de conteneur actuels incluent :

- `--remote-debugging-address=127.0.0.1`
- `--remote-debugging-port=<derived from OPENCLAW_BROWSER_CDP_PORT>`
- `--user-data-dir=${HOME}/.chrome`
- `--no-first-run`
- `--no-default-browser-check`
- `--disable-3d-apis`
- `--disable-gpu`
- `--disable-dev-shm-usage`
- `--disable-background-networking`
- `--disable-extensions`
- `--disable-features=TranslateUI`
- `--disable-breakpad`
- `--disable-crash-reporter`
- `--disable-software-rasterizer`
- `--no-zygote`
- `--metrics-recording-only`
- `--renderer-process-limit=2`
- `--no-sandbox` et `--disable-setuid-sandbox` lorsque `noSandbox` est activé.
- Les trois drapeaux de durcissement graphique (`--disable-3d-apis`,
  `--disable-software-rasterizer`, `--disable-gpu`) sont optionnels et utiles
  lorsque les conteneurs manquent de support GPU. Définissez `OPENCLAW_BROWSER_DISABLE_GRAPHICS_FLAGS=0`
  si votre charge de travail nécessite WebGL ou d'autres fonctionnalités 3D/navigateur.
- `--disable-extensions` est activé par défaut et peut être désactivé avec
  `OPENCLAW_BROWSER_DISABLE_EXTENSIONS=0` pour les flux dépendant des extensions.
- `--renderer-process-limit=2` est contrôlé par
  `OPENCLAW_BROWSER_RENDERER_PROCESS_LIMIT=<N>`, où `0` conserve la valeur par défaut de Chromium.

Si vous avez besoin d'un profil d'exécution différent, utilisez une image de navigateur personnalisée et fournissez
votre propre point d'entrée. Pour les profils Chromium locaux (non-conteneur), utilisez
`browser.extraArgs` pour ajouter des drapeaux de démarrage supplémentaires.

Paramètres de sécurité par défaut :

- `network: "host"` est bloqué.
- `network: "container:<id>"` est bloqué par défaut (risque de contournement de jonction d'espace de noms).
- Remplacement d'urgence : `agents.defaults.sandbox.docker.dangerouslyAllowContainerNamespaceJoin: true`.

Les installations Docker et la gateway conteneurisée se trouvent ici :
[Docker](/install/docker)

Pour les déploiements de gateway Docker, `docker-setup.sh` peut amorcer la configuration du sandbox.
Définissez `OPENCLAW_SANDBOX=1` (ou `true`/`yes`/`on`) pour activer ce chemin. Vous pouvez
remplacer l'emplacement du socket par `OPENCLAW_DOCKER_SOCKET`. Configuration complète et référence env :
[Docker](/install/docker#enable-agent-sandbox-for-docker-gateway-opt-in).

## setupCommand (configuration du conteneur unique)

`setupCommand` s'exécute **une fois** après la création du conteneur sandbox (pas à chaque exécution).
Il s'exécute à l'intérieur du conteneur via `sh -lc`.

Chemins :

- Global : `agents.defaults.sandbox.docker.setupCommand`
- Par agent : `agents.list[].sandbox.docker.setupCommand`

Pièges courants :

- Le `docker.network` par défaut est `"none"` (pas de sortie), donc les installations de paquets échoueront.
- `docker.network: "container:<id>"` nécessite `dangerouslyAllowContainerNamespaceJoin: true` et est réservé aux urgences.
- `readOnlyRoot: true` empêche les écritures ; définissez `readOnlyRoot: false` ou créez une image personnalisée.
- `user` doit être root pour les installations de paquets (omettez `user` ou définissez `user: "0:0"`).
- L'exécution sandbox n'hérite **pas** du `process.env` hôte. Utilisez
  `agents.defaults.sandbox.docker.env` (ou une image personnalisée) pour les clés API de compétences.

## Politique des outils + échappatoires

Les politiques d'autorisation/refus des outils s'appliquent toujours avant les règles de sandbox. Si un outil est refusé
globalement ou par agent, le sandboxing ne le ramène pas.

`tools.elevated` est une échappatoire explicite qui exécute `exec` sur l'hôte.
Les directives `/exec` s'appliquent uniquement aux expéditeurs autorisés et persistent par session ; pour désactiver complètement
`exec`, utilisez la politique de refus des outils (voir [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated)).

Débogage :

- Utilisez `openclaw sandbox explain` pour inspecter le mode sandbox effectif, la politique des outils et les clés de configuration de correction.
- Voir [Sandbox vs Tool Policy vs Elevated](/gateway/sandbox-vs-tool-policy-vs-elevated) pour le modèle mental "pourquoi c'est bloqué ?".
  Gardez-le verrouillé.

## Remplacements multi-agents

Chaque agent peut remplacer sandbox + outils :
`agents.list[].sandbox` et `agents.list[].tools` (plus `agents.list[].tools.sandbox.tools` pour la politique des outils sandbox).
Voir [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools) pour la précédence.

## Exemple d'activation minimale

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

- [Configuration du Sandbox](/gateway/configuration#agentsdefaults-sandbox)
- [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools)
- [Sécurité](/gateway/security)
