---
read_when:
  - 运行或调试 Gateway 网关进程时
summary: Gateway 网关服务、生命周期和运维的运行手册
title: Gateway 网关运行手册
x-i18n:
  generated_at: "2026-02-03T07:50:03Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 497d58090faaa6bdae62780ce887b40a1ad81e2e99ff186ea2a5c2249c35d9ba
  source_path: gateway/index.md
  workflow: 15
---

# Manuel d'exploitation du service Gateway

Dernière mise à jour : 2025-12-09

## Qu'est-ce que c'est

- Un processus résident possédant une seule connexion Baileys/Telegram et un plan de contrôle/événements.
- Remplace la commande `gateway` héritée. Point d'entrée CLI : `openclaw gateway`.
- S'exécute jusqu'à l'arrêt ; quitte avec un code de sortie non nul en cas d'erreur fatale, permettant au superviseur de le redémarrer.

## Comment l'exécuter (localement)

```bash
openclaw gateway --port 18789
# Obtenir les journaux complets de débogage/trace dans stdio :
openclaw gateway --port 18789 --verbose
# Si le port est occupé, terminer l'écouteur puis démarrer :
openclaw gateway --force
# Boucle de développement (rechargement automatique lors de modifications TS) :
pnpm gateway:watch
```

- Configuration de rechargement à chaud en surveillant `~/.openclaw/openclaw.json` (ou `OPENCLAW_CONFIG_PATH`).
  - Mode par défaut : `gateway.reload.mode="hybrid"` (applique les modifications sûres à chaud, redémarre lors de modifications critiques).
  - Le rechargement à chaud utilise un redémarrage intra-processus via **SIGUSR1** si nécessaire.
  - Désactiver avec `gateway.reload.mode="off"`.
- Lie le plan de contrôle WebSocket à `127.0.0.1:<port>` (par défaut 18789).
- Sert également HTTP sur le même port (interface de contrôle, hooks, A2UI). Multiplexage sur un seul port.
  - OpenAI Chat Completions (HTTP) : [`/v1/chat/completions`](/gateway/openai-http-api).
  - OpenResponses (HTTP) : [`/v1/responses`](/gateway/openresponses-http-api).
  - Tools Invoke (HTTP) : [`/tools/invoke`](/gateway/tools-invoke-http-api).
- Démarre par défaut un serveur de fichiers Canvas sur `canvasHost.port` (par défaut `18793`), servant `http://<gateway-host>:18793/__openclaw__/canvas/` depuis `~/.openclaw/workspace/canvas`. Désactiver avec `canvasHost.enabled=false` ou `OPENCLAW_SKIP_CANVAS_HOST=1`.
- Envoie les journaux vers stdout ; utilisez launchd/systemd pour maintenir l'exécution et faire tourner les journaux.
- Lors du dépannage, passez `--verbose` pour refléter les journaux de débogage (poignées de main, requêtes/réponses, événements) du fichier journal vers stdio.
- `--force` utilise `lsof` pour trouver les écouteurs sur le port sélectionné, envoie SIGTERM, enregistre ce qu'il a terminé, puis démarre Gateway (échoue rapidement si `lsof` est manquant).
- Si vous exécutez sous un superviseur (launchd/systemd/mode sous-processus d'application mac), stop/restart envoie généralement **SIGTERM** ; les anciennes versions peuvent l'afficher comme code de sortie `pnpm` `ELIFECYCLE` **143** (SIGTERM), ce qui est un arrêt normal, pas un crash.
- **SIGUSR1** déclenche un redémarrage intra-processus lors de l'autorisation (outils Gateway/application de configuration/mises à jour, ou activez `commands.restart` pour un redémarrage manuel).
- L'authentification Gateway est requise par défaut : définissez `gateway.auth.token` (ou `OPENCLAW_GATEWAY_TOKEN`) ou `gateway.auth.password`. Les clients doivent envoyer `connect.params.auth.token/password`, sauf s'ils utilisent l'identité Tailscale Serve.
- L'assistant génère maintenant un jeton par défaut, même sur loopback.
- Priorité des ports : `--port` > `OPENCLAW_GATEWAY_PORT` > `gateway.port` > par défaut `18789`.

## Accès à distance

- Préférez Tailscale/VPN ; sinon, utilisez un tunnel SSH :
  ```bash
  ssh -N -L 18789:127.0.0.1:18789 user@host
  ```
- Ensuite, le client se connecte via le tunnel à `ws://127.0.0.1:18789`.
- Si un jeton est configuré, le client doit l'inclure dans `connect.params.auth.token` même via le tunnel.

## Plusieurs Gateway (même hôte)

Généralement inutile : un Gateway peut servir plusieurs canaux de messages et agents. Utilisez plusieurs Gateway uniquement si vous avez besoin de redondance ou d'isolation stricte (par exemple : bot de secours).

Supporté si vous isolez l'état + la configuration et utilisez des ports uniques. Guide complet : [Plusieurs Gateway](/gateway/multiple-gateways).

Les noms de service sont conscients du profil :

- macOS : `bot.molt.<profile>` (les anciens `com.openclaw.*` peuvent encore exister)
- Linux : `openclaw-gateway-<profile>.service`
- Windows : `OpenClaw Gateway (<profile>)`

Les métadonnées d'installation sont intégrées dans la configuration du service :

- `OPENCLAW_SERVICE_MARKER=openclaw`
- `OPENCLAW_SERVICE_KIND=gateway`
- `OPENCLAW_SERVICE_VERSION=<version>`

Mode bot de secours : maintenez un deuxième Gateway isolé avec son propre fichier de configuration, répertoire d'état, espace de travail et intervalle de port de base. Guide complet : [Guide du bot de secours](/gateway/multiple-gateways#rescue-bot-guide).

### Profil Dev (`--dev`)

Chemin rapide : exécutez une instance dev complètement isolée (configuration/état/espace de travail) sans toucher à votre configuration principale.

```bash
openclaw --dev setup
openclaw --dev gateway --allow-unconfigured
# Puis localisez l'instance dev :
openclaw --dev status
openclaw --dev health
```

Valeurs par défaut (remplaçables via env/flags/config) :

- `OPENCLAW_STATE_DIR=~/.openclaw-dev`
- `OPENCLAW_CONFIG_PATH=~/.openclaw-dev/openclaw.json`
- `OPENCLAW_GATEWAY_PORT=19001` (Gateway WS + HTTP)
- Port du service de contrôle du navigateur = `19003` (dérivé : `gateway.port+2`, loopback uniquement)
- `canvasHost.port=19005` (dérivé : `gateway.port+4`)
- Lorsque vous exécutez `setup`/`onboard` sous `--dev`, `agents.defaults.workspace` devient par défaut `~/.openclaw/workspace-dev`.

Ports dérivés (règle empirique) :

- Port de base = `gateway.port` (ou `OPENCLAW_GATEWAY_PORT` / `--port`)
- Port du service de contrôle du navigateur = base + 2 (loopback uniquement)
- `canvasHost.port = base + 4` (ou `OPENCLAW_CANVAS_HOST_PORT` / remplacement de config)
- Les ports CDP du profil du navigateur sont alloués automatiquement de `browser.controlPort + 9 .. + 108` (persistants par profil).

Liste de contrôle par instance :

- `gateway.port` unique
- `OPENCLAW_CONFIG_PATH` unique
- `OPENCLAW_STATE_DIR` unique
- `agents.defaults.workspace` unique
- Numéro WhatsApp séparé (si utilisation de WA)

Installer les services par profil :

```bash
openclaw --profile main gateway install
openclaw --profile rescue gateway install
```

Exemple :

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json OPENCLAW_STATE_DIR=~/.openclaw-a openclaw gateway --port 19001
OPENCLAW_CONFIG_PATH=~/.openclaw/b.json OPENCLAW_STATE_DIR=~/.openclaw-b openclaw gateway --port 19002
```

## Protocole (perspective opérationnelle)

- Documentation complète : [Protocole Gateway](/gateway/protocol) et [Protocole Bridge (hérité)](/gateway/bridge-protocol).
- La première trame que le client doit envoyer : `req {type:"req", id, method:"connect", params:{minProtocol,maxProtocol,client:{id,displayName?,version,platform,deviceFamily?,modelIdentifier?,mode,instanceId?}, caps, auth?, locale?, userAgent? } }`.
- Gateway répond `res {type:"res", id, ok:true, payload:hello-ok }` (ou `ok:false` avec erreur, puis ferme).
- Après la poignée de main :
  - Requête : `{type:"req", id, method, params}` → `{type:"res", id, ok, payload|error}`
  - Événement : `{type:"event", event, payload, seq?, stateVersion?}`
- Entrées de présence structurées : `{host, ip, version, platform?, deviceFamily?, modelIdentifier?, mode, lastInputSeconds?, ts, reason?, tags?[], instanceId? }` (pour les clients WS, `instanceId` provient de `connect.client.instanceId`).
- Les réponses `agent` sont en deux phases : d'abord `res` confirmant `{runId,status:"accepted"}`, puis `res` final `{runId,status:"ok"|"error",summary}` après la fin de l'exécution ; la sortie en flux arrive sous forme d'`event:"agent"`.

## Méthodes (ensemble initial)

- `health` — Snapshot de santé complet (même forme que `openclaw health --json`).
- `status` — Résumé court.
- `system-presence` — Liste de présence actuelle.
- `system-event` — Publier une présence/annotation système (structurée).
- `send` — Envoyer un message via un canal actif.
- `agent` — Exécuter un tour d'agent (flux les événements en retour sur la même connexion).
- `node.list` — Lister les nœuds appairés + actuellement connectés (incluant `caps`, `deviceFamily`, `modelIdentifier`, `paired`, `connected` et `commands` diffusés).
- `node.describe` — Décrire un nœud (capacités + commandes `node.invoke` supportées ; fonctionne pour les nœuds appairés et les nœuds non appairés actuellement connectés).
- `node.invoke` — Invoquer une commande sur un nœud (par exemple `canvas.*`, `camera.*`).
- `node.pair.*` — Cycle de vie d'appairage (`request`, `list`, `approve`, `reject`, `verify`).

Voir aussi : [Présence](/concepts/presence) pour comprendre comment la présence est générée/dédupliquée et pourquoi un `client.instanceId` stable est important.

## Événements

- `agent` — Événements d'outils/sortie en flux depuis une exécution d'agent (marqués avec seq).
- `presence` — Mises à jour de présence (incrémentielles avec stateVersion) poussées à tous les clients connectés.
- `tick` — Maintien de vie/no-op périodique pour confirmer l'activité.
- `shutdown` — Gateway se termine ; la charge utile inclut `reason` et optionnellement `restartExpectedMs`. Les clients doivent se reconnecter.

## Intégration WebChat

- WebChat est une interface utilisateur SwiftUI native qui communique directement avec le WebSocket Gateway pour l'historique, l'envoi, l'abandon et les événements.
- L'utilisation à distance passe par le même tunnel SSH/Tailscale ; si un jeton Gateway est configuré, le client l'inclut lors de `connect`.
- L'application macOS utilise une seule connexion WS (connexion partagée) ; elle remplit la présence à partir du snapshot initial et écoute les événements `presence` pour mettre à jour l'interface utilisateur.

## Types et validation

- Le serveur valide chaque trame entrante avec AJV par rapport aux schémas JSON émis à partir des définitions de protocole.
- Les clients (TS/Swift) consomment les types générés (TS les utilise directement ; Swift via le générateur du dépôt).
- Les définitions de protocole sont la source de vérité ; régénérez les schémas/modèles avec :
  - `pnpm protocol:gen`
  - `pnpm protocol:gen:swift`

## Snapshot de connexion

- `hello-ok` contient un `snapshot` avec `presence`, `health`, `stateVersion` et `uptimeMs`, ainsi que `policy {maxPayload,maxBufferedBytes,tickIntervalMs}`, afin que les clients puissent rendre immédiatement sans requête supplémentaire.
- `health`/`system-presence` restent disponibles pour l'actualisation manuelle, mais ne sont pas nécessaires à la connexion.

## Codes d'erreur (forme res.error)

- Les erreurs utilisent `{ code, message, details?, retryable?, retryAfterMs? }`.
- Codes standard :
  - `NOT_LINKED` — WhatsApp non authentifié.
  - `AGENT_TIMEOUT` — L'agent n'a pas répondu dans le délai configuré.
  - `INVALID_REQUEST` — Validation du schéma/paramètres échouée.
  - `UNAVAILABLE` — Gateway s'arrête ou les dépendances ne sont pas disponibles.

## Comportement de maintien de vie

- Les événements `tick` (ou ping/pong WS) sont émis périodiquement afin que les clients sachent que Gateway est actif même sans trafic.
- Les confirmations d'envoi/agent restent des réponses séparées ; ne surchargez pas tick pour l'envoi.

## Relecture / Lacunes

- Les événements ne sont pas relus. Les clients détectent les lacunes de seq et doivent actualiser (health + system-presence) avant de continuer. Les clients WebChat et macOS actualisent maintenant automatiquement lors de lacunes.

## Supervision (exemple macOS)

- Utilisez launchd pour maintenir le service actif :
  - Program : chemin vers `openclaw`
  - Arguments : `gateway`
  - KeepAlive : true
  - StandardOut/Err : chemin de fichier ou `syslog`
- En cas d'échec, launchd redémarre ; les erreurs de configuration fatales doivent rester en sortie afin que les opérateurs le remarquent.
- Les LaunchAgents sont par utilisateur et nécessitent une session connectée ; pour les configurations sans tête, utilisez un LaunchDaemon personnalisé
