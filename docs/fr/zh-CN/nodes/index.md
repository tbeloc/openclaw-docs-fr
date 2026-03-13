---
read_when:
  - Lors de l'appairage de nœuds iOS/Android à une passerelle Gateway
  - Lors de l'utilisation du canvas/camera du nœud pour fournir du contexte à un agent
  - Lors de l'ajout de nouvelles commandes de nœud ou d'outils CLI auxiliaires
summary: Nœuds : appairage, capacités, permissions et outils CLI auxiliaires pour canvas/camera/screen/system
title: Nœuds
x-i18n:
  generated_at: "2026-02-03T07:51:55Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 74e9420f61c653e4ceeb00f5a27e4266bd1c7715c1000edd969c3ee185e74de9
  source_path: nodes/index.md
  workflow: 15
---

# Nœuds

Un **nœud** est un appareil compagnon (macOS/iOS/Android/sans interface) qui se connecte à la passerelle Gateway **WebSocket** (même port que les opérateurs) avec `role: "node"` et expose une interface de commandes via `node.invoke` (par exemple `canvas.*`, `camera.*`, `system.*`). Détails du protocole : [Protocole Gateway](/gateway/protocol).

Transport hérité : [Protocole Bridge](/gateway/bridge-protocol) (TCP JSONL ; actuellement déprécié/supprimé pour les nœuds).

macOS peut également s'exécuter en **mode nœud** : l'application de la barre de menus se connecte au serveur WS de la passerelle Gateway et expose ses commandes canvas/camera locales en tant que nœud (donc `openclaw nodes …` peut fonctionner sur ce Mac).

Remarques :

- Les nœuds sont des **appareils périphériques**, pas une passerelle Gateway. Ils n'exécutent pas le service Gateway.
- Les messages Telegram/WhatsApp, etc., arrivent sur la **passerelle Gateway**, pas sur les nœuds.

## Appairage + État

**Les nœuds WS utilisent l'appairage d'appareils.** Un nœud présente l'identité de l'appareil lors de la `connexion` ; la passerelle Gateway crée une demande d'appairage d'appareil pour `role: node`. Approuvez via l'interface CLI (ou UI) de l'appareil.

CLI rapide :

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
```

Remarques :

- Lorsque le rôle d'appairage d'appareil du nœud inclut `node`, `nodes status` marque le nœud comme **appairé**.
- `node.pair.*` (CLI : `openclaw nodes pending/approve/reject`) est un stockage d'appairage de nœud distinct appartenant à la passerelle Gateway ; il **ne** limite pas la poignée de main `connect` WS.

## Hôte de nœud distant (system.run)

Utilisez un **hôte de nœud** lorsque votre passerelle Gateway s'exécute sur une machine et que vous souhaitez que les commandes s'exécutent sur une autre. Le modèle communique toujours avec la **passerelle Gateway** ; lorsque vous sélectionnez `host=node`, la passerelle Gateway transfère l'appel `exec` à l'**hôte de nœud**.

### Où s'exécute quoi

- **Hôte Gateway** : reçoit les messages, exécute le modèle, achemine les appels d'outils.
- **Hôte de nœud** : exécute `system.run`/`system.which` sur la machine du nœud.
- **Approbations** : exécutées sur l'hôte de nœud via `~/.openclaw/exec-approvals.json`.

### Démarrer l'hôte de nœud (premier plan)

Sur la machine du nœud :

```bash
openclaw node run --host <gateway-host> --port 18789 --display-name "Build Node"
```

### Accéder à une passerelle Gateway distante via un tunnel SSH (liaison loopback)

Si la passerelle Gateway est liée à loopback (`gateway.bind=loopback`, valeur par défaut en mode local),
l'hôte de nœud distant ne peut pas se connecter directement. Créez un tunnel SSH et pointez
l'hôte de nœud vers le port local du tunnel.

Exemple (hôte de nœud -> hôte Gateway) :

```bash
# Terminal A (garder en cours d'exécution) : transférer le port local 18790 -> Gateway 127.0.0.1:18789
ssh -N -L 18790:127.0.0.1:18789 user@gateway-host

# Terminal B : exporter le jeton Gateway et se connecter via le tunnel
export OPENCLAW_GATEWAY_TOKEN="<gateway-token>"
openclaw node run --host 127.0.0.1 --port 18790 --display-name "Build Node"
```

Remarques :

- Le jeton est `gateway.auth.token` dans la configuration Gateway (sur l'hôte Gateway `~/.openclaw/openclaw.json`).
- `openclaw node run` lit `OPENCLAW_GATEWAY_TOKEN` pour l'authentification.

### Démarrer l'hôte de nœud (service)

```bash
openclaw node install --host <gateway-host> --port 18789 --display-name "Build Node"
openclaw node restart
```

### Appairage + Nommage

Sur l'hôte Gateway :

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes list
```

Options de nommage :

- Utilisez `--display-name` sur `openclaw node run` / `openclaw node install` (persisté dans `~/.openclaw/node.json` sur le nœud).
- `openclaw nodes rename --node <id|name|ip> --name "Build Node"` (remplacement Gateway).

### Ajouter des commandes à la liste d'autorisation

L'approbation Exec est **par hôte de nœud**. Ajoutez des entrées de liste d'autorisation depuis la passerelle Gateway :

```bash
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/uname"
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/sw_vers"
```

Les approbations sont stockées dans `~/.openclaw/exec-approvals.json` sur l'hôte de nœud.

### Pointer exec vers le nœud

Configurez les valeurs par défaut (configuration Gateway) :

```bash
openclaw config set tools.exec.host node
openclaw config set tools.exec.security allowlist
openclaw config set tools.exec.node "<id-or-name>"
```

Ou par session :

```
/exec host=node security=allowlist node=<id-or-name>
```

Une fois défini, tout appel `exec` avec `host=node` s'exécute sur l'hôte de nœud (soumis aux
contraintes de liste d'autorisation/approbation du nœud).

Connexes :

- [CLI Hôte de nœud](/cli/node)
- [Outil Exec](/tools/exec)
- [Approbations Exec](/tools/exec-approvals)

## Invoquer des commandes

Bas niveau (RPC brut) :

```bash
openclaw nodes invoke --node <idOrNameOrIp> --command canvas.eval --params '{"javaScript":"location.href"}'
```

Pour les flux de travail plus courants « donner à l'agent une pièce jointe MEDIA », des outils auxiliaires de niveau supérieur existent.

## Captures d'écran (snapshot canvas)

Si le nœud affiche un Canvas (WebView), `canvas.snapshot` retourne `{ format, base64 }`.

Outil CLI auxiliaire (écrit dans un fichier temporaire et imprime `MEDIA:<path>`) :

```bash
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format png
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format jpg --max-width 1200 --quality 0.9
```

### Contrôle Canvas

```bash
openclaw nodes canvas present --node <idOrNameOrIp> --target https://example.com
openclaw nodes canvas hide --node <idOrNameOrIp>
openclaw nodes canvas navigate https://example.com --node <idOrNameOrIp>
openclaw nodes canvas eval --node <idOrNameOrIp> --js "document.title"
```

Remarques :

- `canvas present` accepte une URL ou un chemin de fichier local (`--target`), ainsi que des options `--x/--y/--width/--height` pour le positionnement.
- `canvas eval` accepte du JS en ligne (`--js`) ou des paramètres de position.

### A2UI (Canvas)

```bash
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --text "Hello"
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --jsonl ./payload.jsonl
openclaw nodes canvas a2ui reset --node <idOrNameOrIp>
```

Remarques :

- Seul A2UI v0.8 JSONL est supporté (v0.9/createSurface est rejeté).

## Photos + Vidéos (caméra de nœud)

Photos (`jpg`) :

```bash
openclaw nodes camera list --node <idOrNameOrIp>
openclaw nodes camera snap --node <idOrNameOrIp>            # Par défaut : deux orientations (2 lignes MEDIA)
openclaw nodes camera snap --node <idOrNameOrIp> --facing front
```

Clips vidéo (`mp4`) :

```bash
openclaw nodes camera clip --node <idOrNameOrIp> --duration 10s
openclaw nodes camera clip --node <idOrNameOrIp> --duration 3000 --no-audio
```

Remarques :

- Le nœud doit être au **premier plan** pour utiliser `canvas.*` et `camera.*` (les appels en arrière-plan retournent `NODE_BACKGROUND_UNAVAILABLE`).
- La durée des clips est limitée (actuellement `<= 60s`) pour éviter les charges base64 trop volumineuses.
- Android demande les permissions `CAMERA`/`RECORD_AUDIO` si possible ; les permissions refusées échouent avec `*_PERMISSION_REQUIRED`.

## Enregistrement d'écran (nœud)

Le nœud expose `screen.record` (mp4). Exemple :

```bash
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10 --no-audio
```

Remarques :

- `screen.record` nécessite que l'application du nœud soit au premier plan.
- Android affiche une invite de capture d'écran système avant l'enregistrement.
- L'enregistrement d'écran est limité à `<= 60s`.
- `--no-audio` désactive la capture du microphone (supporté sur iOS/Android ; macOS utilise la capture audio système).
- Lorsque plusieurs écrans sont disponibles, utilisez `--screen <index>` pour sélectionner l'affichage.

## Localisation (nœud)

Lorsque la localisation est activée dans les paramètres, le nœud expose `location.get`.

Outil CLI auxiliaire :

```bash
openclaw nodes location get --node <idOrNameOrIp>
openclaw nodes location get --node <idOrNameOrIp> --accuracy precise --max-age 15000 --location-timeout 10000
```

Remarques :

- La localisation est **désactivée par défaut**.
- « Toujours » nécessite les permissions système ; la récupération en arrière-plan est au mieux.
- La réponse inclut latitude/longitude, précision (mètres) et horodatage.

## SMS (nœud Android)

Lorsque l'utilisateur accorde la permission **SMS** et que l'appareil supporte la fonctionnalité téléphonique, un nœud Android peut exposer `sms.send`.

Appel bas niveau :

```bash
openclaw nodes invoke --node <idOrNameOrIp> --command sms.send --params '{"to":"+15555550123","message":"Hello from OpenClaw"}'
```

Remarques :

- La permission doit être acceptée sur l'appareil Android avant que la capacité soit diffusée.
- Les appareils purement Wi-Fi sans fonctionnalité téléphonique ne diffusent pas `sms.send`.

## Commandes système (hôte de nœud / nœud mac)

Les nœuds macOS exposent `system.run`, `system.notify` et `system.execApprovals.get/set`.
Les hôtes de nœud sans interface exposent `system.run`, `system.which` et `system.execApprovals.get/set`.

Exemples :

```bash
openclaw nodes run --node <idOrNameOrIp> -- echo "Hello from mac node"
openclaw nodes notify --node <idOrNameOrIp> --title "Ping" --body "Gateway ready"
```

Remarques :

- `system.run` retourne stdout/stderr/code de sortie dans la charge utile.
- `system.notify` respecte l'état des permissions de notification sur l'application macOS.
- `system.run` supporte `--cwd`, `--env KEY=VAL`, `--command-timeout` et `--needs-screen-recording`.
- `system.notify` supporte `--priority <passive|active|timeSensitive>` et `--delivery <system|overlay|auto>`.
- Les nœuds macOS rejettent les remplacements `PATH` ; les hôtes de nœud sans interface ne les acceptent que s'ils sont préfixés au PATH de l'hôte de nœud.
- En mode nœud macOS, `system.run` est soumis aux approbations exec dans l'application macOS (Paramètres → Approbations Exec). Le comportement Ask/allowlist/full est identique aux hôtes de nœud sans interface ; les invites refusées retournent `SYSTEM_RUN_DENIED`.
- Sur l'hôte de nœud sans interface, `system.run` est soumis aux approbations exec (`~/.openclaw/exec-approvals.json`).

## Liaison de nœud Exec

Lorsque plusieurs nœuds sont disponibles, vous pouvez lier exec à un nœud spécifique.
Cela définit le nœud par défaut pour `exec host=node` (peut être remplacé par agent).

Valeur par défaut globale :

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

## Mappage des permissions

Les nœuds
