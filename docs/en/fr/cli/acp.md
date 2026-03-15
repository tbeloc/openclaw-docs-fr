---
summary: "Exécuter le pont ACP pour les intégrations IDE"
read_when:
  - Setting up ACP-based IDE integrations
  - Debugging ACP session routing to the Gateway
title: "acp"
---

# acp

Exécutez le pont [Agent Client Protocol (ACP)](https://agentclientprotocol.com/) qui communique avec une passerelle OpenClaw.

Cette commande parle ACP via stdio pour les IDE et transfère les invites à la passerelle via WebSocket. Elle maintient les sessions ACP mappées aux clés de session de la passerelle.

`openclaw acp` est un pont ACP soutenu par une passerelle, et non un runtime d'éditeur natif ACP complet. Il se concentre sur le routage des sessions, la livraison des invites et les mises à jour de streaming basiques.

## Matrice de compatibilité

| Zone ACP                                                              | Statut      | Notes                                                                                                                                                                                                                                            |
| --------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `initialize`, `newSession`, `prompt`, `cancel`                        | Implémenté | Flux de pont principal via stdio vers chat/envoi de passerelle + abandon.                                                                                                                                                                        |
| `listSessions`, commandes slash                                        | Implémenté | La liste des sessions fonctionne par rapport à l'état de session de la passerelle ; les commandes sont annoncées via `available_commands_update`.                                                                                                                                       |
| `loadSession`                                                         | Partiel     | Relie la session ACP à une clé de session de passerelle et rejoue l'historique du texte utilisateur/assistant stocké. L'historique des outils/système n'est pas encore reconstruit.                                                                                                   |
| Contenu d'invite (`text`, `resource` intégré, images)                  | Partiel     | Le texte/les ressources sont aplatis en entrée de chat ; les images deviennent des pièces jointes de passerelle.                                                                                                                                                                 |
| Modes de session                                                         | Partiel     | `session/set_mode` est supporté et le pont expose les contrôles de session initiaux soutenus par la passerelle pour le niveau de réflexion, la verbosité des outils, le raisonnement, le détail d'utilisation et les actions élevées. Les surfaces de mode/config plus larges natives à ACP sont toujours hors de portée. |
| Mises à jour des informations de session et d'utilisation                                        | Partiel     | Le pont émet les notifications `session_info_update` et `usage_update` au meilleur effort à partir des snapshots de session de passerelle en cache. L'utilisation est approximative et n'est envoyée que lorsque les totaux de jetons de passerelle sont marqués comme frais.                                        |
| Streaming des outils                                                        | Partiel     | Les événements `tool_call` / `tool_call_update` incluent les E/S brutes, le contenu textuel et les emplacements de fichiers au meilleur effort lorsque les args/résultats des outils de passerelle les exposent. Les terminaux intégrés et la sortie plus riche native aux diffs ne sont toujours pas exposés.                        |
| Serveurs MCP par session (`mcpServers`)                                | Non supporté | Le mode pont rejette les demandes de serveur MCP par session. Configurez MCP sur la passerelle OpenClaw ou l'agent à la place.                                                                                                                                     |
| Méthodes de système de fichiers client (`fs/read_text_file`, `fs/write_text_file`) | Non supporté | Le pont n'appelle pas les méthodes de système de fichiers client ACP.                                                                                                                                                                          |
| Méthodes de terminal client (`terminal/*`)                                | Non supporté | Le pont ne crée pas de terminaux client ACP ni ne diffuse les identifiants de terminal via les appels d'outils.                                                                                                                                                         |
| Plans de session / streaming de réflexion                                     | Non supporté | Le pont émet actuellement le texte de sortie et l'état des outils, pas les mises à jour de plan ou de réflexion ACP.                                                                                                                                                         |

## Limitations connues

- `loadSession` rejoue l'historique du texte utilisateur et assistant stocké, mais ne reconstruit pas les appels d'outils historiques, les avis système ou les types d'événements plus riches natifs à ACP.
- Si plusieurs clients ACP partagent la même clé de session de passerelle, le routage des événements et des annulations sont au meilleur effort plutôt que strictement isolés par client. Préférez les sessions isolées par défaut `acp:<uuid>` lorsque vous avez besoin de tours propres locaux à l'éditeur.
- Les états d'arrêt de la passerelle sont traduits en raisons d'arrêt ACP, mais ce mappage est moins expressif qu'un runtime entièrement natif à ACP.
- Les contrôles de session initiaux exposent actuellement un sous-ensemble ciblé de boutons de passerelle : niveau de réflexion, verbosité des outils, raisonnement, détail d'utilisation et actions élevées. La sélection de modèle et les contrôles d'hôte d'exécution ne sont pas encore exposés en tant qu'options de configuration ACP.
- `session_info_update` et `usage_update` sont dérivés des snapshots de session de passerelle, pas de la comptabilité runtime native ACP en direct. L'utilisation est approximative, ne porte aucune donnée de coût et n'est émise que lorsque la passerelle marque les données de jetons totaux comme frais.
- Les données de suivi des outils sont au meilleur effort. Le pont peut exposer les chemins de fichiers qui apparaissent dans les args/résultats d'outils connus, mais n'émet pas encore les terminaux ACP ou les diffs de fichiers structurés.

## Utilisation

```bash
openclaw acp

# Passerelle distante
openclaw acp --url wss://gateway-host:18789 --token <token>

# Passerelle distante (jeton depuis un fichier)
openclaw acp --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token

# Attacher à une clé de session existante
openclaw acp --session agent:main:main

# Attacher par étiquette (doit déjà exister)
openclaw acp --session-label "support inbox"

# Réinitialiser la clé de session avant la première invite
openclaw acp --session agent:main:main --reset-session
```

## Client ACP (débogage)

Utilisez le client ACP intégré pour vérifier le pont sans IDE.
Il lance le pont ACP et vous permet de taper des invites de manière interactive.

```bash
openclaw acp client

# Pointer le pont lancé vers une passerelle distante
openclaw acp client --server-args --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token

# Remplacer la commande du serveur (par défaut : openclaw)
openclaw acp client --server "node" --server-args openclaw.mjs acp --url ws://127.0.0.1:19001
```

Modèle de permission (mode débogage client) :

- L'approbation automatique est basée sur une liste blanche et s'applique uniquement aux ID d'outils principaux de confiance.
- L'approbation automatique `read` est limitée au répertoire de travail actuel (`--cwd` lorsqu'il est défini).
- Les noms d'outils inconnus/non-principaux, les lectures hors de portée et les outils dangereux nécessitent toujours une approbation explicite.
- Le `toolCall.kind` fourni par le serveur est traité comme des métadonnées non fiables (pas une source d'autorisation).

## Comment utiliser ceci

Utilisez ACP lorsqu'un IDE (ou un autre client) parle le protocole client agent et que vous voulez qu'il pilote une session de passerelle OpenClaw.

1. Assurez-vous que la passerelle est en cours d'exécution (locale ou distante).
2. Configurez la cible de la passerelle (config ou drapeaux).
3. Pointez votre IDE pour exécuter `openclaw acp` via stdio.

Exemple de config (persisté) :

```bash
openclaw config set gateway.remote.url wss://gateway-host:18789
openclaw config set gateway.remote.token <token>
```

Exemple d'exécution directe (sans écriture de config) :

```bash
openclaw acp --url wss://gateway-host:18789 --token <token>
# préféré pour la sécurité du processus local
openclaw acp --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token
```

## Sélection des agents

ACP ne sélectionne pas les agents directement. Il achemine par la clé de session de la passerelle.

Utilisez les clés de session limitées à l'agent pour cibler un agent spécifique :

```bash
openclaw acp --session agent:main:main
openclaw acp --session agent:design:main
openclaw acp --session agent:qa:bug-123
```

Chaque session ACP mappe à une seule clé de session de passerelle. Un agent peut avoir plusieurs sessions ; ACP utilise par défaut une session isolée `acp:<uuid>` sauf si vous remplacez la clé ou l'étiquette.

Les `mcpServers` par session ne sont pas supportés en mode pont. Si un client ACP les envoie lors de `newSession` ou `loadSession`, le pont retourne une erreur claire au lieu de les ignorer silencieusement.

## Utilisation depuis `acpx` (Codex, Claude, autres clients ACP)

Si vous voulez qu'un agent de codage tel que Codex ou Claude Code parle à votre bot OpenClaw via ACP, utilisez `acpx` avec sa cible `openclaw` intégrée.

Flux typique :

1. Exécutez la passerelle et assurez-vous que le pont ACP peut la joindre.
2. Pointez `acpx openclaw` vers `openclaw acp`.
3. Ciblez la clé de session OpenClaw que vous voulez que l'agent de codage utilise.

Exemples :

```bash
# Demande unique dans votre session ACP OpenClaw par défaut
acpx openclaw exec "Summarize the active OpenClaw session state."

# Session nommée persistante pour les tours de suivi
acpx openclaw sessions ensure --name codex-bridge
acpx openclaw -s codex-bridge --cwd /path/to/repo \
  "Ask my OpenClaw work agent for recent context relevant to this repo."
```

Si vous voulez que `acpx openclaw` cible une passerelle et une clé de session spécifiques à chaque fois, remplacez la commande de l'agent `openclaw` dans `~/.acpx/config.json` :

```json
{
  "agents": {
    "openclaw": {
      "command": "env OPENCLAW_HIDE_BANNER=1 OPENCLAW_SUPPRESS_NOTES=1 openclaw acp --url ws://127.0.0.1:18789 --token-file ~/.openclaw/gateway.token --session agent:main:main"
    }
  }
}
```

Pour un checkout OpenClaw local au repo, utilisez le point d'entrée CLI direct au lieu du runner de développement pour que le flux ACP reste propre. Par exemple :

```bash
env OPENCLAW_HIDE_BANNER=1 OPENCLAW_SUPPRESS_NOTES=1 node openclaw.mjs acp ...
```

C'est le moyen le plus facile de laisser Codex, Claude Code ou un autre client conscient d'ACP extraire des informations contextuelles d'un agent OpenClaw sans scraper un terminal.

## Configuration de l'éditeur Zed

Ajoutez un agent ACP personnalisé dans `~/.config/zed/settings.json` (ou utilisez l'interface utilisateur des paramètres de Zed) :

```json
{
  "agent_servers": {
    "OpenClaw ACP": {
      "type": "custom",
      "command": "openclaw",
      "args": ["acp"],
      "env": {}
    }
  }
}
```

Pour cibler une passerelle ou un agent spécifique :

```json
{
  "agent_servers": {
    "OpenClaw ACP": {
      "type": "custom",
      "command": "openclaw",
      "args": [
        "acp",
        "--url",
        "wss://gateway-host:18789",
        "--token",
        "<token>",
        "--session",
        "agent:design:main"
      ],
      "env": {}
    }
  }
}
```

Dans Zed, ouvrez le panneau Agent et sélectionnez "OpenClaw ACP" pour démarrer un fil.

## Mappage des sessions

Par défaut, les sessions ACP obtiennent une clé de session de passerelle isolée avec un préfixe `acp:`.
Pour réutiliser une session connue, passez une clé de session ou une étiquette :

- `--session <key>` : utilisez une clé de session de passerelle spécifique.
- `--session-label <label>` : résolvez une session existante par étiquette.
- `--reset-session` : créez un nouvel identifiant de session pour cette clé (même clé, nouvelle transcription).

Si votre client ACP supporte les métadonnées, vous pouvez remplacer par session :

```json
{
  "_meta": {
    "sessionKey": "agent:main:main",
    "sessionLabel": "support inbox",
    "resetSession": true
  }
}
```

En savoir plus sur les clés de session à [/concepts/session](/concepts/session).

## Options

- `--url <url>` : URL WebSocket de la passerelle (par défaut gateway.remote.url si configuré).
- `--token <token>` : jeton d'authentification de la passerelle.
- `--token-file <path>` : lire le jeton d'authentification de la passerelle depuis un fichier.
- `--password <password>` : mot de passe d'authentification de la passerelle.
- `--password-file <path>` : lire le mot de passe d'authentification de la passerelle depuis un fichier.
- `--session <key>` : clé de session par défaut.
- `--session-label <label>` : étiquette de session par défaut à résoudre.
- `--require-existing` : échouer si la clé/étiquette de session n'existe pas.
- `--reset-session` : réinitialiser la clé de session avant la première utilisation.
- `--no-prefix-cwd` : ne pas préfixer les invites avec le répertoire de travail.
- `--verbose, -v` : journalisation détaillée vers stderr.

Note de sécurité :

- `--token` et `--password` peuvent être visibles dans les listes de processus locaux sur certains systèmes.
- Préférez `--token-file`/`--password-file` ou les variables d'environnement (`OPENCLAW_GATEWAY_TOKEN`, `OPENCLAW_GATEWAY_PASSWORD`).
- La résolution de l'authentification de la passerelle suit le contrat partagé utilisé par les autres clients de la passerelle :
  - mode local : env (`OPENCLAW_GATEWAY_*`) -> `gateway.auth.*` -> secours `gateway.remote.*` uniquement quand `gateway.auth.*` n'est pas défini (les SecretRefs configurés mais non résolus en mode local échouent fermés)
  - mode distant : `gateway.remote.*` avec secours env/config selon les règles de précédence distante
  - `--url` est sûr pour les remplacements et ne réutilise pas les identifiants implicites config/env ; passez explicitement `--token`/`--password` (ou les variantes fichier)
- Les processus enfants du backend d'exécution ACP reçoivent `OPENCLAW_SHELL=acp`, qui peut être utilisé pour les règles shell/profil spécifiques au contexte.
- `openclaw acp client` définit `OPENCLAW_SHELL=acp-client` sur le processus bridge généré.

### Options `acp client`

- `--cwd <dir>` : répertoire de travail pour la session ACP.
- `--server <command>` : commande du serveur ACP (par défaut : `openclaw`).
- `--server-args <args...>` : arguments supplémentaires passés au serveur ACP.
- `--server-verbose` : activer la journalisation détaillée sur le serveur ACP.
- `--verbose, -v` : journalisation détaillée du client.
