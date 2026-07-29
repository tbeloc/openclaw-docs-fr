---
summary: "Connectez les serveurs MCP à OpenClaw à partir des Paramètres, de la CLI ou de la config"
title: "Connecter les serveurs MCP"
read_when:
  - Adding an MCP server for OpenClaw agents
  - Choosing between Settings and `openclaw mcp`
  - Troubleshooting MCP transport, OAuth, or tool discovery
---

Le Model Context Protocol (MCP) est la façon dont un agent emprunte des outils à un autre programme : un serveur MCP expose des outils, des ressources et des invites, et OpenClaw s'y connecte et met ces outils à disposition de vos agents. Les définitions de serveur se trouvent sous `mcp.servers` dans la config, et les outils qu'ils exposent passent par les mêmes contrôles de profil d'outil et de politique d'outil que tout le reste — connecter un serveur ne contourne pas votre politique.

<Note>
Ce guide concerne la connexion de serveurs MCP tiers **à OpenClaw**. Pour l'inverse — exposer les conversations de canal OpenClaw à un autre client MCP — utilisez [`openclaw mcp serve`](/fr/cli/mcp#openclaw-as-an-mcp-server).
</Note>

## Ajouter un serveur à partir des Paramètres

1. Ouvrez l'interface de contrôle et allez à **Paramètres → MCP**.
2. Sous **Serveurs configurés**, sélectionnez **Ajouter un serveur**.
3. Donnez-lui un nom unique et choisissez un transport : **Streamable HTTP**, **SSE**, ou **Stdio**.
4. Pour les transports HTTP, entrez l'URL `http://` ou `https://` du serveur. Pour stdio, entrez la commande suivie de ses arguments.
5. Sélectionnez **Ajouter un serveur**.

Cela écrit la nouvelle entrée `mcp.servers` via la Gateway. Pour tout ce qui dépasse les bases — en-têtes, valeurs d'environnement, métadonnées OAuth, paramètres TLS, délais d'expiration, indices d'appels d'outils parallèles, filtres d'outils — utilisez l'éditeur de config délimité plus bas sur la page. Les lignes de serveur vous permettent également d'activer, désactiver ou supprimer une définition.

Une fois le serveur enregistré, vérifiez qu'il répond réellement :

```bash
openclaw mcp doctor <name> --probe
```

Enregistrer une définition ne prouve rien sur la disponibilité — la sonde le fait. Notez que les processus Gateway ou agent déjà en cours d'exécution peuvent avoir besoin d'un redémarrage ou d'un rechargement à l'exécution avant de récupérer la nouvelle définition.

## Ajouter un serveur à partir de la CLI

Un serveur stdio local :

```bash
openclaw mcp add local-tools \
  --command node \
  --arg ./dist/mcp-server.js \
  --cwd /srv/openclaw-tools
openclaw mcp doctor local-tools --probe
```

Un serveur Streamable HTTP distant, exposant seulement certains de ses outils :

```bash
openclaw mcp add docs \
  --url https://mcp.example.com/mcp \
  --transport streamable-http \
  --include 'search,read_*'
openclaw mcp doctor docs --probe
```

Compagnons utiles : `openclaw mcp status --verbose` pour un résumé config uniquement, `openclaw mcp probe <name>` pour les capacités en direct, et `openclaw mcp login <name>` quand un serveur HTTP utilise OAuth. La [référence CLI MCP](/fr/cli/mcp) documente chaque commande, drapeau et forme de sortie, plus le pont `mcp serve` séparé.

## Configurer un serveur directement

Le même serveur `docs`, écrit directement dans la config :

```json5
{
  mcp: {
    servers: {
      docs: {
        url: "https://mcp.example.com/mcp",
        transport: "streamable-http",
        enabled: true,
        connectionTimeoutMs: 5000,
        requestTimeoutMs: 20000,
        toolFilter: {
          include: ["search", "read_*"],
        },
      },
    },
  },
}
```

Un serveur activé a besoin soit d'une commande (stdio) soit d'une URL (SSE ou Streamable HTTP). Définir `enabled: false` garde la définition sans la connecter. Gardez les identifiants en dehors des littéraux de config — stockez les en-têtes sensibles et les valeurs d'environnement via les mécanismes de secret supportés.

## Dépannage

### Le serveur apparaît dans les Paramètres mais n'expose aucun outil

Exécutez `openclaw mcp doctor <name> --probe`. Doctor valide d'abord la définition enregistrée, puis ouvre une connexion en direct et rapporte les outils et autres capacités que le serveur annonce. S'il se connecte mais que les outils attendus manquent, vérifiez `toolFilter.include` et `toolFilter.exclude`.

### Un serveur stdio ne démarre pas

Confirmez que la `command` se résout dans l'environnement du processus Gateway et que `cwd` existe. Les arguments appartiennent à `args`, et un `transport: "stdio"` explicite nécessite une commande non vide.

### Un serveur HTTP a besoin d'une autorisation

Définissez `auth: "oauth"` plus toute métadonnée `oauth` requise, puis :

```bash
openclaw mcp login <name>
```

Suivez l'URL d'autorisation imprimée et relancez avec `--code` quand vous y êtes invité.

### Les modifications n'atteignent pas un agent actif

`openclaw mcp reload` actualise les runtimes possédés par le processus CLI actuel. Une Gateway ou un agent s'exécutant ailleurs a besoin de son propre rechargement, publication de config ou redémarrage.

## Connexes

- [Référence CLI MCP](/fr/cli/mcp)
- [Gérer les plugins](/fr/plugins/manage-plugins)
- [Politiques d'outils](/fr/tools)
