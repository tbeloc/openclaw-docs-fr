---
summary: "OpenClaw Gateway CLI (`openclaw gateway`) — exécuter, interroger et découvrir des passerelles"
read_when:
  - Running the Gateway from the CLI (dev or servers)
  - Debugging Gateway auth, bind modes, and connectivity
  - Discovering gateways via Bonjour (LAN + tailnet)
title: "gateway"
---

# Gateway CLI

La passerelle est le serveur WebSocket d'OpenClaw (canaux, nœuds, sessions, hooks).

Les sous-commandes de cette page se trouvent sous `openclaw gateway …`.

Documentation connexe :

- [/gateway/bonjour](/fr/gateway/bonjour)
- [/gateway/discovery](/fr/gateway/discovery)
- [/gateway/configuration](/fr/gateway/configuration)

## Exécuter la passerelle

Exécuter un processus Gateway local :

```bash
openclaw gateway
```

Alias au premier plan :

```bash
openclaw gateway run
```

Remarques :

- Par défaut, la passerelle refuse de démarrer sauf si `gateway.mode=local` est défini dans `~/.openclaw/openclaw.json`. Utilisez `--allow-unconfigured` pour les exécutions ad-hoc/dev.
- La liaison au-delà de la boucle locale sans authentification est bloquée (garde-fou de sécurité).
- `SIGUSR1` déclenche un redémarrage en processus lorsqu'il est autorisé (`commands.restart` est activé par défaut ; définissez `commands.restart: false` pour bloquer le redémarrage manuel, tandis que l'outil gateway/config apply/update restent autorisés).
- Les gestionnaires `SIGINT`/`SIGTERM` arrêtent le processus de la passerelle, mais ils ne restaurent pas l'état personnalisé du terminal. Si vous enveloppez la CLI avec une TUI ou une entrée en mode brut, restaurez le terminal avant la sortie.

### Options

- `--port <port>` : port WebSocket (la valeur par défaut provient de la config/env ; généralement `18789`).
- `--bind <loopback|lan|tailnet|auto|custom>` : mode de liaison de l'écouteur.
- `--auth <token|password>` : remplacement du mode d'authentification.
- `--token <token>` : remplacement du jeton (définit également `OPENCLAW_GATEWAY_TOKEN` pour le processus).
- `--password <password>` : remplacement du mot de passe. Avertissement : les mots de passe en ligne peuvent être exposés dans les listes de processus locaux.
- `--password-file <path>` : lire le mot de passe de la passerelle à partir d'un fichier.
- `--tailscale <off|serve|funnel>` : exposer la passerelle via Tailscale.
- `--tailscale-reset-on-exit` : réinitialiser la configuration Tailscale serve/funnel à l'arrêt.
- `--allow-unconfigured` : autoriser le démarrage de la passerelle sans `gateway.mode=local` dans la config.
- `--dev` : créer une config dev + workspace si manquante (ignore BOOTSTRAP.md).
- `--reset` : réinitialiser la config dev + identifiants + sessions + workspace (nécessite `--dev`).
- `--force` : arrêter tout écouteur existant sur le port sélectionné avant de démarrer.
- `--verbose` : journaux détaillés.
- `--claude-cli-logs` : afficher uniquement les journaux claude-cli dans la console (et activer sa stdout/stderr).
- `--ws-log <auto|full|compact>` : style de journal websocket (par défaut `auto`).
- `--compact` : alias pour `--ws-log compact`.
- `--raw-stream` : enregistrer les événements de flux de modèle brut en jsonl.
- `--raw-stream-path <path>` : chemin jsonl du flux brut.

## Interroger une passerelle en cours d'exécution

Toutes les commandes de requête utilisent RPC WebSocket.

Modes de sortie :

- Par défaut : lisible par l'homme (coloré en TTY).
- `--json` : JSON lisible par machine (pas de style/spinner).
- `--no-color` (ou `NO_COLOR=1`) : désactiver ANSI tout en conservant la mise en page humaine.

Options partagées (où supportées) :

- `--url <url>` : URL WebSocket de la passerelle.
- `--token <token>` : jeton de la passerelle.
- `--password <password>` : mot de passe de la passerelle.
- `--timeout <ms>` : délai d'attente/budget (varie selon la commande).
- `--expect-final` : attendre une réponse "finale" (appels d'agent).

Remarque : lorsque vous définissez `--url`, la CLI ne revient pas à la config ou aux identifiants d'environnement.
Passez `--token` ou `--password` explicitement. Les identifiants explicites manquants sont une erreur.

### `gateway health`

```bash
openclaw gateway health --url ws://127.0.0.1:18789
```

### `gateway status`

`gateway status` affiche le service Gateway (launchd/systemd/schtasks) plus une sonde RPC optionnelle.

```bash
openclaw gateway status
openclaw gateway status --json
openclaw gateway status --require-rpc
```

Options :

- `--url <url>` : remplacer l'URL de la sonde.
- `--token <token>` : authentification par jeton pour la sonde.
- `--password <password>` : authentification par mot de passe pour la sonde.
- `--timeout <ms>` : délai d'attente de la sonde (par défaut `10000`).
- `--no-probe` : ignorer la sonde RPC (vue service uniquement).
- `--deep` : analyser aussi les services au niveau du système.
- `--require-rpc` : quitter avec un code non nul lorsque la sonde RPC échoue. Ne peut pas être combiné avec `--no-probe`.

Remarques :

- `gateway status` résout les SecretRefs d'authentification configurés pour l'authentification de la sonde si possible.
- Si une SecretRef d'authentification requise est non résolue dans ce chemin de commande, l'authentification de la sonde peut échouer ; passez `--token`/`--password` explicitement ou résolvez d'abord la source secrète.
- Utilisez `--require-rpc` dans les scripts et l'automatisation lorsqu'un service d'écoute ne suffit pas et que vous avez besoin que le RPC Gateway lui-même soit sain.
- Sur les installations systemd Linux, les vérifications de dérive d'authentification du service lisent les valeurs `Environment=` et `EnvironmentFile=` de l'unité (y compris `%h`, les chemins entre guillemets, les fichiers multiples et les fichiers optionnels `-`).

### `gateway probe`

`gateway probe` est la commande "déboguer tout". Elle sonde toujours :

- votre passerelle distante configurée (si définie), et
- localhost (boucle locale) **même si distant est configuré**.

Si plusieurs passerelles sont accessibles, elle les affiche toutes. Plusieurs passerelles sont supportées lorsque vous utilisez des profils/ports isolés (par exemple, un bot de secours), mais la plupart des installations exécutent toujours une seule passerelle.

```bash
openclaw gateway probe
openclaw gateway probe --json
```

Interprétation :

- `Reachable: yes` signifie qu'au moins une cible a accepté une connexion WebSocket.
- `RPC: ok` signifie que les appels RPC détaillés (`health`/`status`/`system-presence`/`config.get`) ont également réussi.
- `RPC: limited - missing scope: operator.read` signifie que la connexion a réussi mais que le RPC détaillé est limité en portée. Ceci est signalé comme une accessibilité **dégradée**, pas un échec complet.
- Le code de sortie est non nul uniquement lorsqu'aucune cible sondée n'est accessible.

Notes JSON (`--json`) :

- Niveau supérieur :
  - `ok` : au moins une cible est accessible.
  - `degraded` : au moins une cible avait un RPC détaillé limité en portée.
- Par cible (`targets[].connect`) :
  - `ok` : accessibilité après connexion + classification dégradée.
  - `rpcOk` : succès complet du RPC détaillé.
  - `scopeLimited` : RPC détaillé échoué en raison d'une portée d'opérateur manquante.

#### Distant via SSH (parité avec l'app Mac)

Le mode "Remote over SSH" de l'app macOS utilise un port-forward local afin que la passerelle distante (qui peut être liée à la boucle locale uniquement) devienne accessible à `ws://127.0.0.1:<port>`.

Équivalent CLI :

```bash
openclaw gateway probe --ssh user@gateway-host
```

Options :

- `--ssh <target>` : `user@host` ou `user@host:port` (le port par défaut est `22`).
- `--ssh-identity <path>` : fichier d'identité.
- `--ssh-auto` : choisir le premier hôte de passerelle découvert comme cible SSH (LAN/WAB uniquement).

Config (optionnel, utilisé comme valeurs par défaut) :

- `gateway.remote.sshTarget`
- `gateway.remote.sshIdentity`

### `gateway call <method>`

Assistant RPC bas niveau.

```bash
openclaw gateway call status
openclaw gateway call logs.tail --params '{"sinceMs": 60000}'
```

## Gérer le service Gateway

```bash
openclaw gateway install
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway uninstall
```

Remarques :

- `gateway install` supporte `--port`, `--runtime`, `--token`, `--force`, `--json`.
- Lorsque l'authentification par jeton nécessite un jeton et que `gateway.auth.token` est géré par SecretRef, `gateway install` valide que la SecretRef est résolvable mais ne persiste pas le jeton résolu dans les métadonnées d'environnement du service.
- Si l'authentification par jeton nécessite un jeton et que la SecretRef de jeton configurée est non résolue, l'installation échoue fermée au lieu de persister un texte brut de secours.
- Pour l'authentification par mot de passe sur `gateway run`, préférez `OPENCLAW_GATEWAY_PASSWORD`, `--password-file`, ou une `gateway.auth.password` soutenue par SecretRef plutôt que `--password` en ligne.
- En mode d'authentification déduit, `OPENCLAW_GATEWAY_PASSWORD`/`CLAWDBOT_GATEWAY_PASSWORD` shell uniquement ne relâche pas les exigences de jeton d'installation ; utilisez une config durable (`gateway.auth.password` ou config `env`) lors de l'installation d'un service géré.
- Si à la fois `gateway.auth.token` et `gateway.auth.password` sont configurés et que `gateway.auth.mode` n'est pas défini, l'installation est bloquée jusqu'à ce que le mode soit défini explicitement.
- Les commandes de cycle de vie acceptent `--json` pour les scripts.

## Découvrir les passerelles (Bonjour)

`gateway discover` analyse les balises Gateway (`_openclaw-gw._tcp`).

- Multicast DNS-SD : `local.`
- Unicast DNS-SD (Wide-Area Bonjour) : choisir un domaine (exemple : `openclaw.internal.`) et configurer split DNS + un serveur DNS ; voir [/gateway/bonjour](/fr/gateway/bonjour)

Seules les passerelles avec la découverte Bonjour activée (par défaut) annoncent la balise.

Les enregistrements de découverte Wide-Area incluent (TXT) :

- `role` (indice de rôle de passerelle)
- `transport` (indice de transport, par exemple `gateway`)
- `gatewayPort` (port WebSocket, généralement `18789`)
- `sshPort` (port SSH ; par défaut `22` s'il n'est pas présent)
- `tailnetDns` (nom d'hôte MagicDNS, si disponible)
- `gatewayTls` / `gatewayTlsSha256` (TLS activé + empreinte du certificat)
- `cliPath` (indice optionnel pour les installations distantes)

### `gateway discover`

```bash
openclaw gateway discover
```

Options :

- `--timeout <ms>` : délai d'attente par commande (browse/resolve) ; par défaut `2000`.
- `--json` : sortie lisible par machine (désactive aussi le style/spinner).

Exemples :

```bash
openclaw gateway discover --timeout 4000
openclaw gateway discover --json | jq '.beacons[].wsUrl'
```
