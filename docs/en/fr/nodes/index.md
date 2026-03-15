---
summary: "Nodes: pairing, capabilities, permissions, and CLI helpers for canvas/camera/screen/device/notifications/system"
read_when:
  - Pairing iOS/Android nodes to a gateway
  - Using node canvas/camera for agent context
  - Adding new node commands or CLI helpers
title: "Nodes"
---

# Nodes

Un **node** est un appareil compagnon (macOS/iOS/Android/headless) qui se connecte au **WebSocket** de la Gateway (même port que les opérateurs) avec `role: "node"` et expose une surface de commande (par exemple `canvas.*`, `camera.*`, `device.*`, `notifications.*`, `system.*`) via `node.invoke`. Détails du protocole : [Gateway protocol](/fr/gateway/protocol).

Transport hérité : [Bridge protocol](/fr/gateway/bridge-protocol) (TCP JSONL ; déprécié/supprimé pour les nodes actuels).

macOS peut également s'exécuter en **mode node** : l'application de la barre de menus se connecte au serveur WS de la Gateway et expose ses commandes canvas/camera locales en tant que node (donc `openclaw nodes …` fonctionne sur ce Mac).

Notes :

- Les nodes sont des **périphériques**, pas des gateways. Ils n'exécutent pas le service gateway.
- Les messages Telegram/WhatsApp/etc. arrivent sur la **gateway**, pas sur les nodes.
- Guide de dépannage : [/nodes/troubleshooting](/fr/nodes/troubleshooting)

## Appairage + statut

**Les nodes WS utilisent l'appairage d'appareil.** Les nodes présentent une identité d'appareil lors de la `connect` ; la Gateway crée une demande d'appairage d'appareil pour `role: node`. Approuvez via la CLI des appareils (ou l'interface utilisateur).

CLI rapide :

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
```

Notes :

- `nodes status` marque un node comme **paired** lorsque son rôle d'appairage d'appareil inclut `node`.
- `node.pair.*` (CLI : `openclaw nodes pending/approve/reject`) est un magasin d'appairage de node distinct appartenant à la gateway ; il ne **bloque pas** la poignée de main WS `connect`.

## Hôte node distant (system.run)

Utilisez un **hôte node** lorsque votre Gateway s'exécute sur une machine et que vous souhaitez que les commandes s'exécutent sur une autre. Le modèle parle toujours à la **gateway** ; la gateway transfère les appels `exec` à l'**hôte node** lorsque `host=node` est sélectionné.

### Où s'exécute quoi

- **Hôte Gateway** : reçoit les messages, exécute le modèle, achemine les appels d'outils.
- **Hôte Node** : exécute `system.run`/`system.which` sur la machine node.
- **Approbations** : appliquées sur l'hôte node via `~/.openclaw/exec-approvals.json`.

Note sur l'approbation :

- Les exécutions de node soutenues par approbation lient le contexte exact de la demande.
- Pour les exécutions directes de fichiers shell/runtime, OpenClaw lie également au mieux un opérande de fichier local concret et refuse l'exécution si ce fichier change avant l'exécution.
- Si OpenClaw ne peut pas identifier exactement un fichier local concret pour une commande d'interpréteur/runtime, l'exécution soutenue par approbation est refusée au lieu de prétendre une couverture runtime complète. Utilisez le sandboxing, des hôtes séparés, ou une liste d'autorisation explicite de confiance/flux de travail complet pour une sémantique d'interpréteur plus large.

### Démarrer un hôte node (premier plan)

Sur la machine node :

```bash
openclaw node run --host <gateway-host> --port 18789 --display-name "Build Node"
```

### Gateway distante via tunnel SSH (liaison loopback)

Si la Gateway se lie à loopback (`gateway.bind=loopback`, par défaut en mode local), les hôtes node distants ne peuvent pas se connecter directement. Créez un tunnel SSH et pointez l'hôte node vers l'extrémité locale du tunnel.

Exemple (hôte node -> hôte gateway) :

```bash
# Terminal A (garder en cours d'exécution) : transférer local 18790 -> gateway 127.0.0.1:18789
ssh -N -L 18790:127.0.0.1:18789 user@gateway-host

# Terminal B : exporter le token gateway et se connecter via le tunnel
export OPENCLAW_GATEWAY_TOKEN="<gateway-token>"
openclaw node run --host 127.0.0.1 --port 18790 --display-name "Build Node"
```

Notes :

- `openclaw node run` supporte l'authentification par token ou mot de passe.
- Les variables d'environnement sont préférées : `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD`.
- La configuration de secours est `gateway.auth.token` / `gateway.auth.password`.
- En mode local, l'hôte node ignore intentionnellement `gateway.remote.token` / `gateway.remote.password`.
- En mode distant, `gateway.remote.token` / `gateway.remote.password` sont éligibles selon les règles de précédence distante.
- Si des SecretRefs `gateway.auth.*` locaux actifs sont configurés mais non résolus, l'authentification de l'hôte node échoue fermée.
- Les variables d'environnement héritées `CLAWDBOT_GATEWAY_*` sont intentionnellement ignorées par la résolution d'authentification de l'hôte node.

### Démarrer un hôte node (service)

```bash
openclaw node install --host <gateway-host> --port 18789 --display-name "Build Node"
openclaw node restart
```

### Appairage + nommage

Sur l'hôte gateway :

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw nodes status
```

Options de nommage :

- `--display-name` sur `openclaw node run` / `openclaw node install` (persiste dans `~/.openclaw/node.json` sur le node).
- `openclaw nodes rename --node <id|name|ip> --name "Build Node"` (remplacement gateway).

### Ajouter les commandes à la liste blanche

Les approbations exec sont **par hôte node**. Ajoutez des entrées de liste blanche depuis la gateway :

```bash
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/uname"
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/sw_vers"
```

Les approbations se trouvent sur l'hôte node à `~/.openclaw/exec-approvals.json`.

### Pointer exec vers le node

Configurez les valeurs par défaut (configuration gateway) :

```bash
openclaw config set tools.exec.host node
openclaw config set tools.exec.security allowlist
openclaw config set tools.exec.node "<id-or-name>"
```

Ou par session :

```
/exec host=node security=allowlist node=<id-or-name>
```

Une fois défini, tout appel `exec` avec `host=node` s'exécute sur l'hôte node (soumis à la liste blanche/approbations du node).

Connexes :

- [Node host CLI](/fr/cli/node)
- [Exec tool](/fr/tools/exec)
- [Exec approvals](/fr/tools/exec-approvals)

## Invocation de commandes

Bas niveau (RPC brut) :

```bash
openclaw nodes invoke --node <idOrNameOrIp> --command canvas.eval --params '{"javaScript":"location.href"}'
```

Des assistants de niveau supérieur existent pour les flux de travail courants "donner à l'agent une pièce jointe MEDIA".

## Captures d'écran (snapshots canvas)

Si le node affiche le Canvas (WebView), `canvas.snapshot` retourne `{ format, base64 }`.

Assistant CLI (écrit dans un fichier temporaire et imprime `MEDIA:<path>`) :

```bash
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format png
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format jpg --max-width 1200 --quality 0.9
```

### Contrôles Canvas

```bash
openclaw nodes canvas present --node <idOrNameOrIp> --target https://example.com
openclaw nodes canvas hide --node <idOrNameOrIp>
openclaw nodes canvas navigate https://example.com --node <idOrNameOrIp>
openclaw nodes canvas eval --node <idOrNameOrIp> --js "document.title"
```

Notes :

- `canvas present` accepte les URLs ou les chemins de fichiers locaux (`--target`), plus les options `--x/--y/--width/--height` pour le positionnement.
- `canvas eval` accepte du JS en ligne (`--js`) ou un argument positionnel.

### A2UI (Canvas)

```bash
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --text "Hello"
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --jsonl ./payload.jsonl
openclaw nodes canvas a2ui reset --node <idOrNameOrIp>
```

Notes :

- Seul A2UI v0.8 JSONL est supporté (v0.9/createSurface est rejeté).

## Photos + vidéos (caméra node)

Photos (`jpg`) :

```bash
openclaw nodes camera list --node <idOrNameOrIp>
openclaw nodes camera snap --node <idOrNameOrIp>            # par défaut : les deux façades (2 lignes MEDIA)
openclaw nodes camera snap --node <idOrNameOrIp> --facing front
```

Clips vidéo (`mp4`) :

```bash
openclaw nodes camera clip --node <idOrNameOrIp> --duration 10s
openclaw nodes camera clip --node <idOrNameOrIp> --duration 3000 --no-audio
```

Notes :

- Le node doit être **au premier plan** pour `canvas.*` et `camera.*` (les appels en arrière-plan retournent `NODE_BACKGROUND_UNAVAILABLE`).
- La durée du clip est limitée (actuellement `<= 60s`) pour éviter les charges utiles base64 surdimensionnées.
- Android demandera les permissions `CAMERA`/`RECORD_AUDIO` si possible ; les permissions refusées échouent avec `*_PERMISSION_REQUIRED`.

## Enregistrements d'écran (nodes)

Les nodes supportés exposent `screen.record` (mp4). Exemple :

```bash
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10 --no-audio
```

Notes :

- La disponibilité de `screen.record` dépend de la plateforme du node.
- Les enregistrements d'écran sont limités à `<= 60s`.
- `--no-audio` désactive la capture du microphone sur les plateformes supportées.
- Utilisez `--screen <index>` pour sélectionner un affichage lorsque plusieurs écrans sont disponibles.

## Localisation (nodes)

Les nodes exposent `location.get` lorsque la localisation est activée dans les paramètres.

Assistant CLI :

```bash
openclaw nodes location get --node <idOrNameOrIp>
openclaw nodes location get --node <idOrNameOrIp> --accuracy precise --max-age 15000 --location-timeout 10000
```

Notes :

- La localisation est **désactivée par défaut**.
- "Toujours" nécessite une permission système ; la récupération en arrière-plan est au mieux.
- La réponse inclut lat/lon, la précision (mètres) et l'horodatage.

## SMS (nodes Android)

Les nodes Android peuvent exposer `sms.send` lorsque l'utilisateur accorde la permission **SMS** et que l'appareil supporte la téléphonie.

Invocation bas niveau :

```bash
openclaw nodes invoke --node <idOrNameOrIp> --command sms.send --params '{"to":"+15555550123","message":"Hello from OpenClaw"}'
```

Notes :

- L'invite de permission doit être acceptée sur l'appareil Android avant que la capacité soit annoncée.
- Les appareils Wi-Fi uniquement sans téléphonie n'annonceront pas `sms.send`.

## Commandes d'appareil Android + données personnelles

Les nodes Android peuvent annoncer des familles de commandes supplémentaires lorsque les capacités correspondantes sont activées.

Familles disponibles :

- `device.status`, `device.info`, `device.permissions`, `device.health`
- `notifications.list`, `notifications.actions`
- `photos.latest`
- `contacts.search`, `contacts.add`
- `calendar.events`, `calendar.add`
- `callLog.search`
- `motion.activity`, `motion.pedometer`

Exemples d'invocations :

```bash
openclaw nodes invoke --node <idOrNameOrIp> --command device.status --params '{}'
openclaw nodes invoke --node <idOrNameOrIp> --command notifications.list --params '{}'
openclaw nodes invoke --node <idOrNameOrIp> --command photos.latest --params '{"limit":1}'
```

Notes :

- Les commandes de mouvement sont contrôlées par capacité selon les capteurs disponibles.

## Commandes système (nœud node / nœud mac)

Le nœud macOS expose `system.run`, `system.notify`, et `system.execApprovals.get/set`.
L'hôte de nœud headless expose `system.run`, `system.which`, et `system.execApprovals.get/set`.

Exemples :

```bash
openclaw nodes run --node <idOrNameOrIp> -- echo "Hello from mac node"
openclaw nodes notify --node <idOrNameOrIp> --title "Ping" --body "Gateway ready"
```

Notes :

- `system.run` retourne stdout/stderr/code de sortie dans la charge utile.
- `system.notify` respecte l'état des permissions de notification sur l'application macOS.
- Les métadonnées `platform` / `deviceFamily` de nœud non reconnues utilisent une liste d'autorisation par défaut conservatrice qui exclut `system.run` et `system.which`. Si vous avez intentionnellement besoin de ces commandes pour une plateforme inconnue, ajoutez-les explicitement via `gateway.nodes.allowCommands`.
- `system.run` supporte `--cwd`, `--env KEY=VAL`, `--command-timeout`, et `--needs-screen-recording`.
- Pour les wrappers shell (`bash|sh|zsh ... -c/-lc`), les valeurs `--env` limitées à la requête sont réduites à une liste d'autorisation explicite (`TERM`, `LANG`, `LC_*`, `COLORTERM`, `NO_COLOR`, `FORCE_COLOR`).
- Pour les décisions d'autorisation permanente en mode liste d'autorisation, les wrappers de dispatch connus (`env`, `nice`, `nohup`, `stdbuf`, `timeout`) conservent les chemins des exécutables internes au lieu des chemins des wrappers. Si le dépliage n'est pas sûr, aucune entrée de liste d'autorisation n'est conservée automatiquement.
- Sur les hôtes de nœud Windows en mode liste d'autorisation, les exécutions de wrapper shell via `cmd.exe /c` nécessitent une approbation (l'entrée de liste d'autorisation seule ne permet pas automatiquement la forme du wrapper).
- `system.notify` supporte `--priority <passive|active|timeSensitive>` et `--delivery <system|overlay|auto>`.
- Les hôtes de nœud ignorent les remplacements `PATH` et suppriment les clés de démarrage/shell dangereuses (`DYLD_*`, `LD_*`, `NODE_OPTIONS`, `PYTHON*`, `PERL*`, `RUBYOPT`, `SHELLOPTS`, `PS4`). Si vous avez besoin d'entrées PATH supplémentaires, configurez l'environnement du service hôte de nœud (ou installez les outils dans des emplacements standard) au lieu de passer `PATH` via `--env`.
- En mode nœud macOS, `system.run` est contrôlé par les approbations d'exécution dans l'application macOS (Paramètres → Approbations d'exécution).
  Ask/allowlist/full se comportent de la même manière que l'hôte de nœud headless ; les invites refusées retournent `SYSTEM_RUN_DENIED`.
- Sur l'hôte de nœud headless, `system.run` est contrôlé par les approbations d'exécution (`~/.openclaw/exec-approvals.json`).

## Liaison de nœud exec

Lorsque plusieurs nœuds sont disponibles, vous pouvez lier exec à un nœud spécifique.
Cela définit le nœud par défaut pour `exec host=node` (et peut être remplacé par agent).

Défaut global :

```bash
openclaw config set tools.exec.node "node-id-or-name"
```

Remplacement par agent :

```bash
openclaw config get agents.list
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"
```

Désactiver pour autoriser n'importe quel nœud :

```bash
openclaw config unset tools.exec.node
openclaw config unset agents.list[0].tools.exec.node
```

## Carte des permissions

Les nœuds peuvent inclure une carte `permissions` dans `node.list` / `node.describe`, indexée par nom de permission (par exemple `screenRecording`, `accessibility`) avec des valeurs booléennes (`true` = accordé).

## Hôte de nœud headless (multiplateforme)

OpenClaw peut exécuter un **hôte de nœud headless** (sans interface utilisateur) qui se connecte au WebSocket de la Gateway
et expose `system.run` / `system.which`. Ceci est utile sur Linux/Windows
ou pour exécuter un nœud minimal à côté d'un serveur.

Démarrez-le :

```bash
openclaw node run --host <gateway-host> --port 18789
```

Notes :

- L'appairage est toujours requis (la Gateway affichera une invite d'appairage d'appareil).
- L'hôte de nœud stocke son ID de nœud, son jeton, son nom d'affichage et ses informations de connexion à la gateway dans `~/.openclaw/node.json`.
- Les approbations d'exécution sont appliquées localement via `~/.openclaw/exec-approvals.json`
  (voir [Approbations d'exécution](/fr/tools/exec-approvals)).
- Sur macOS, l'hôte de nœud headless exécute `system.run` localement par défaut. Définissez
  `OPENCLAW_NODE_EXEC_HOST=app` pour router `system.run` via l'hôte d'exécution de l'application compagnon ; ajoutez
  `OPENCLAW_NODE_EXEC_FALLBACK=0` pour exiger l'hôte d'application et échouer fermé s'il n'est pas disponible.
- Ajoutez `--tls` / `--tls-fingerprint` lorsque le WS de la Gateway utilise TLS.

## Mode nœud Mac

- L'application barre de menus macOS se connecte au serveur WS de la Gateway en tant que nœud (donc `openclaw nodes …` fonctionne contre ce Mac).
- En mode distant, l'application ouvre un tunnel SSH pour le port de la Gateway et se connecte à `localhost`.
