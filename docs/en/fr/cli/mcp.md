---
summary: "Exposer les conversations de canal OpenClaw sur MCP et gérer les définitions de serveur MCP enregistrées"
read_when:
  - Connecting Codex, Claude Code, or another MCP client to OpenClaw-backed channels
  - Running `openclaw mcp serve`
  - Managing OpenClaw-saved MCP server definitions
title: "mcp"
---

# mcp

`openclaw mcp` a deux fonctions :

- exécuter OpenClaw en tant que serveur MCP avec `openclaw mcp serve`
- gérer les définitions de serveur MCP sortantes appartenant à OpenClaw avec `list`, `show`,
  `set`, et `unset`

En d'autres termes :

- `serve` est OpenClaw agissant en tant que serveur MCP
- `list` / `show` / `set` / `unset` est OpenClaw agissant en tant que registre
  côté client MCP pour les autres serveurs MCP que ses runtimes peuvent consommer ultérieurement

Utilisez [`openclaw acp`](/fr/cli/acp) quand OpenClaw doit héberger lui-même une
session de harnais de codage et router ce runtime via ACP.

## OpenClaw en tant que serveur MCP

C'est le chemin `openclaw mcp serve`.

## Quand utiliser `serve`

Utilisez `openclaw mcp serve` quand :

- Codex, Claude Code, ou un autre client MCP doit communiquer directement avec
  les conversations de canal soutenues par OpenClaw
- vous avez déjà une passerelle OpenClaw locale ou distante avec des sessions routées
- vous voulez un serveur MCP qui fonctionne sur les backends de canal d'OpenClaw au lieu
  d'exécuter des ponts séparés par canal

Utilisez [`openclaw acp`](/fr/cli/acp) à la place quand OpenClaw doit héberger le runtime de codage
lui-même et garder la session de l'agent à l'intérieur d'OpenClaw.

## Comment ça marche

`openclaw mcp serve` démarre un serveur MCP stdio. Le client MCP possède ce
processus. Tant que le client garde la session stdio ouverte, le pont se connecte à une
passerelle OpenClaw locale ou distante via WebSocket et expose les conversations de canal routées sur MCP.

Cycle de vie :

1. le client MCP lance `openclaw mcp serve`
2. le pont se connecte à la passerelle
3. les sessions routées deviennent des conversations MCP et des outils de transcription/historique
4. les événements en direct sont mis en file d'attente en mémoire pendant que le pont est connecté
5. si le mode canal Claude est activé, la même session peut également recevoir
   des notifications push spécifiques à Claude

Comportement important :

- l'état de la file d'attente en direct commence quand le pont se connecte
- l'historique de transcription plus ancien est lu avec `messages_read`
- les notifications push Claude n'existent que pendant que la session MCP est active
- quand le client se déconnecte, le pont se ferme et la file d'attente en direct disparaît

## Choisir un mode client

Utilisez le même pont de deux façons différentes :

- Clients MCP génériques : outils MCP standard uniquement. Utilisez `conversations_list`,
  `messages_read`, `events_poll`, `events_wait`, `messages_send`, et les
  outils d'approbation.
- Claude Code : outils MCP standard plus l'adaptateur de canal spécifique à Claude.
  Activez `--claude-channel-mode on` ou laissez la valeur par défaut `auto`.

Actuellement, `auto` se comporte de la même manière que `on`. Il n'y a pas encore de détection de capacité client.

## Ce que `serve` expose

Le pont utilise les métadonnées de route de session de passerelle existantes pour exposer les
conversations soutenues par canal. Une conversation apparaît quand OpenClaw a déjà
un état de session avec une route connue telle que :

- `channel`
- métadonnées de destinataire ou de destination
- `accountId` optionnel
- `threadId` optionnel

Cela donne aux clients MCP un seul endroit pour :

- lister les conversations routées récentes
- lire l'historique de transcription récent
- attendre les nouveaux événements entrants
- envoyer une réponse via la même route
- voir les demandes d'approbation qui arrivent pendant que le pont est connecté

## Utilisation

```bash
# Local Gateway
openclaw mcp serve

# Remote Gateway
openclaw mcp serve --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token

# Remote Gateway with password auth
openclaw mcp serve --url wss://gateway-host:18789 --password-file ~/.openclaw/gateway.password

# Enable verbose bridge logs
openclaw mcp serve --verbose

# Disable Claude-specific push notifications
openclaw mcp serve --claude-channel-mode off
```

## Outils du pont

Le pont actuel expose ces outils MCP :

- `conversations_list`
- `conversation_get`
- `messages_read`
- `attachments_fetch`
- `events_poll`
- `events_wait`
- `messages_send`
- `permissions_list_open`
- `permissions_respond`

### `conversations_list`

Liste les conversations soutenues par session récentes qui ont déjà des métadonnées de route
dans l'état de session de la passerelle.

Filtres utiles :

- `limit`
- `search`
- `channel`
- `includeDerivedTitles`
- `includeLastMessage`

### `conversation_get`

Retourne une conversation par `session_key`.

### `messages_read`

Lit les messages de transcription récents pour une conversation soutenue par session.

### `attachments_fetch`

Extrait les blocs de contenu non-texte des messages de transcription. C'est une
vue de métadonnées sur le contenu de transcription, pas un magasin de blob de pièce jointe durable autonome.

### `events_poll`

Lit les événements en direct mis en file d'attente depuis un curseur numérique.

### `events_wait`

Long-poll jusqu'à ce que le prochain événement en file d'attente correspondant arrive ou qu'un délai d'expiration expire.

Utilisez ceci quand un client MCP générique a besoin d'une livraison quasi-temps réel sans
protocole push spécifique à Claude.

### `messages_send`

Envoie du texte via la même route déjà enregistrée sur la session.

Comportement actuel :

- nécessite une route de conversation existante
- utilise le canal, le destinataire, l'ID de compte et l'ID de thread de la session
- envoie du texte uniquement

### `permissions_list_open`

Liste les demandes d'approbation exec/plugin en attente que le pont a observées depuis
sa connexion à la passerelle.

### `permissions_respond`

Résout une demande d'approbation exec/plugin en attente avec :

- `allow-once`
- `allow-always`
- `deny`

## Modèle d'événement

Le pont maintient une file d'attente d'événements en mémoire pendant qu'il est connecté.

Types d'événements actuels :

- `message`
- `exec_approval_requested`
- `exec_approval_resolved`
- `plugin_approval_requested`
- `plugin_approval_resolved`
- `claude_permission_request`

Limites importantes :

- la file d'attente est en direct uniquement ; elle commence quand le pont MCP démarre
- `events_poll` et `events_wait` ne rejouent pas l'historique plus ancien de la passerelle par eux-mêmes
- le backlog durable doit être lu avec `messages_read`

## Notifications de canal Claude

Le pont peut également exposer les notifications de canal spécifiques à Claude. C'est
l'équivalent OpenClaw d'un adaptateur de canal Claude Code : les outils MCP standard restent
disponibles, mais les messages entrants en direct peuvent également arriver en tant que notifications MCP spécifiques à Claude.

Drapeaux :

- `--claude-channel-mode off` : outils MCP standard uniquement
- `--claude-channel-mode on` : activer les notifications de canal Claude
- `--claude-channel-mode auto` : valeur par défaut actuelle ; même comportement de pont que `on`

Quand le mode canal Claude est activé, le serveur annonce les capacités expérimentales Claude et peut émettre :

- `notifications/claude/channel`
- `notifications/claude/channel/permission`

Comportement actuel du pont :

- les messages de transcription `user` entrants sont transférés en tant que
  `notifications/claude/channel`
- les demandes de permission Claude reçues sur MCP sont suivies en mémoire
- si la conversation liée envoie ensuite `yes abcde` ou `no abcde`, le pont
  convertit cela en `notifications/claude/channel/permission`
- ces notifications sont en session en direct uniquement ; si le client MCP se déconnecte,
  il n'y a pas de cible push

C'est intentionnellement spécifique au client. Les clients MCP génériques doivent s'appuyer sur les outils de sondage standard.

## Configuration du client MCP

Exemple de configuration de client stdio :

```json
{
  "mcpServers": {
    "openclaw": {
      "command": "openclaw",
      "args": [
        "mcp",
        "serve",
        "--url",
        "wss://gateway-host:18789",
        "--token-file",
        "/path/to/gateway.token"
      ]
    }
  }
}
```

Pour la plupart des clients MCP génériques, commencez par la surface d'outil standard et ignorez
le mode Claude. Activez le mode Claude uniquement pour les clients qui comprennent réellement les
méthodes de notification spécifiques à Claude.

## Options

`openclaw mcp serve` supporte :

- `--url <url>` : URL WebSocket de la passerelle
- `--token <token>` : jeton de passerelle
- `--token-file <path>` : lire le jeton depuis un fichier
- `--password <password>` : mot de passe de passerelle
- `--password-file <path>` : lire le mot de passe depuis un fichier
- `--claude-channel-mode <auto|on|off>` : mode de notification Claude
- `-v`, `--verbose` : journaux détaillés sur stderr

Préférez `--token-file` ou `--password-file` aux secrets en ligne quand c'est possible.

## Sécurité et limite de confiance

Le pont n'invente pas le routage. Il expose uniquement les conversations que la passerelle
sait déjà comment router.

Cela signifie :

- les listes blanches d'expéditeurs, l'appairage et la confiance au niveau du canal appartiennent toujours à
  la configuration de canal OpenClaw sous-jacente
- `messages_send` ne peut répondre que via une route stockée existante
- l'état d'approbation est en direct/en mémoire uniquement pour la session de pont actuelle
- l'authentification du pont doit utiliser les mêmes contrôles de jeton ou de mot de passe de passerelle
  que vous feriez confiance pour tout autre client de passerelle distante

Si une conversation est manquante de `conversations_list`, la cause habituelle n'est pas
la configuration MCP. C'est des métadonnées de route manquantes ou incomplètes dans la session de passerelle sous-jacente.

## Test

OpenClaw expédie un smoke Docker déterministe pour ce pont :

```bash
pnpm test:docker:mcp-channels
```

Ce smoke :

- démarre un conteneur de passerelle ensemencé
- démarre un deuxième conteneur qui lance `openclaw mcp serve`
- vérifie la découverte de conversation, les lectures de transcription, les lectures de métadonnées de pièce jointe,
  le comportement de la file d'attente d'événements en direct et le routage d'envoi sortant
- valide les notifications de canal et de permission de style Claude sur le vrai pont MCP stdio

C'est le moyen le plus rapide de prouver que le pont fonctionne sans câbler un vrai
compte Telegram, Discord ou iMessage dans l'exécution du test.

Pour un contexte de test plus large, voir [Testing](/fr/help/testing).

## Dépannage

### Aucune conversation retournée

Signifie généralement que la session de passerelle n'est pas déjà routable. Confirmez que
la session sous-jacente a des métadonnées de route de canal/fournisseur, destinataire et compte/thread optionnel stockées.

### `events_poll` ou `events_wait` manque les messages plus anciens

Attendu. La file d'attente en direct commence quand le pont se connecte. Lisez l'historique de transcription plus ancien avec `messages_read`.

### Les notifications Claude ne s'affichent pas

Vérifiez tous ces éléments :

- le client a gardé la session MCP stdio ouverte
- `--claude-channel-mode` est `on` ou `auto`
- le client comprend réellement les méthodes de notification spécifiques à Claude
- le message entrant s'est produit après la connexion du pont

### Les approbations sont manquantes

`permissions_list_open` affiche uniquement les demandes d'approbation observées pendant que le pont
était connecté. Ce n'est pas une API d'historique d'approbation durable.

## OpenClaw en tant que registre client MCP

C'est le chemin `openclaw mcp list`, `show`, `set`, et `unset`.

Ces commandes n'exposent pas OpenClaw sur MCP. Elles gèrent les définitions de serveur MCP appartenant à OpenClaw sous `mcp.servers` dans la configuration OpenClaw.

Ces définitions enregistrées sont pour les runtimes qu'OpenClaw lance ou configure
ultérieurement, tels que Pi intégré et d'autres adaptateurs de runtime. OpenClaw stocke les
définitions de manière centralisée afin que ces runtimes n'aient pas besoin de conserver leurs propres listes de serveurs MCP en double.

Comportement important :

- ces commandes lisent ou écrivent uniquement la configuration OpenClaw
- elles ne se connectent pas au serveur MCP cible
- elles ne valident pas si la commande, l'URL ou le transport distant est
  accessible en ce moment
- les adaptateurs de runtime décident quelles formes de transport ils supportent réellement au moment de l'exécution

## Définitions de serveur MCP enregistrées

OpenClaw stocke également un registre de serveur MCP léger dans la configuration pour les surfaces
qui veulent des définitions MCP gérées par OpenClaw.

Commandes :

- `openclaw mcp list`
- `openclaw mcp show [name]`
- `openclaw mcp set <name> <json>`
- `openclaw mcp unset <name>`

Exemples :

```bash
openclaw mcp list
openclaw mcp show context7 --json
openclaw mcp set context7 '{"command":"uvx","args":["context7-mcp"]}'
openclaw mcp set docs '{"url":"https://mcp.example.com"}'
openclaw mcp unset context7
```

Exemple de forme de configuration :

```json
{
  "mcp": {
    "servers": {
      "context7": {
        "command": "uvx",
        "args": ["context7-mcp"]
      },
      "docs": {
        "url": "https://mcp.example.com"
      }
    }
  }
}
```

Champs typiques :

- `command`
- `args`
- `env`
- `cwd` ou `workingDirectory`
- `url`

Ces commandes gèrent uniquement la configuration enregistrée. Elles ne démarrent pas le pont de canal,
n'ouvrent pas une session client MCP en direct ou ne prouvent pas que le serveur cible est accessible.

## Limites actuelles

Cette page documente le bridge tel qu'il est livré aujourd'hui.

Limites actuelles :

- la découverte de conversation dépend des métadonnées de route de session Gateway existantes
- pas de protocole push générique au-delà de l'adaptateur spécifique à Claude
- pas encore d'outils d'édition ou de réaction de message
- pas encore de transport HTTP MCP dédié
- `permissions_list_open` inclut uniquement les approbations observées pendant que le bridge est connecté
