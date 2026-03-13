---
read_when:
  - Exécuter Gateway depuis la CLI (développement ou serveur)
  - Déboguer l'authentification, le mode de liaison et la connectivité de Gateway
  - Découvrir Gateway via Bonjour (LAN + tailnet)
summary: CLI OpenClaw Gateway (`openclaw gateway`) — Exécuter, interroger et découvrir Gateway
title: gateway
x-i18n:
  generated_at: "2026-02-03T07:45:15Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 054dd48056e4784f153c6511c8eb35b56f239db8d4e629661841a00259e9abbf
  source_path: cli/gateway.md
  workflow: 15
---

# CLI Gateway

Gateway est le serveur WebSocket d'OpenClaw (canaux, nœuds, sessions, hooks).

Les sous-commandes de cette page se trouvent sous `openclaw gateway …`.

Documentation connexe :

- [/gateway/bonjour](/gateway/bonjour)
- [/gateway/discovery](/gateway/discovery)
- [/gateway/configuration](/gateway/configuration)

## Exécuter Gateway

Exécuter un processus Gateway local :

```bash
openclaw gateway
```

Alias pour exécution au premier plan :

```bash
openclaw gateway run
```

Remarques :

- Par défaut, Gateway refusera de démarrer sauf si `gateway.mode=local` est défini dans `~/.openclaw/openclaw.json`. Utilisez `--allow-unconfigured` pour les exécutions temporaires/développement.
- La liaison à des adresses autres que loopback sans authentification est bloquée (garde-fou de sécurité).
- `SIGUSR1` déclenche un redémarrage en processus lors de l'autorisation (activez `commands.restart` ou utilisez les outils gateway/config apply/update).
- Les gestionnaires `SIGINT`/`SIGTERM` arrêtent le processus Gateway, mais ne restaurent pas l'état du terminal personnalisé. Si vous enveloppez la CLI avec une TUI ou une entrée en mode brut, restaurez le terminal avant de quitter.

### Options

- `--port <port>` : Port WebSocket (par défaut depuis la configuration/variables d'environnement ; généralement `18789`).
- `--bind <loopback|lan|tailnet|auto|custom>` : Mode de liaison de l'écouteur.
- `--auth <token|password>` : Remplacement du mode d'authentification.
- `--token <token>` : Remplacement du jeton (définit également `OPENCLAW_GATEWAY_TOKEN` pour le processus).
- `--password <password>` : Remplacement du mot de passe (définit également `OPENCLAW_GATEWAY_PASSWORD` pour le processus).
- `--tailscale <off|serve|funnel>` : Exposer Gateway via Tailscale.
- `--tailscale-reset-on-exit` : Réinitialiser la configuration Tailscale serve/funnel à la fermeture.
- `--allow-unconfigured` : Autoriser le démarrage de Gateway sans `gateway.mode=local` dans la configuration.
- `--dev` : Créer la configuration de développement + espace de travail s'il manque (ignorer BOOTSTRAP.md).
- `--reset` : Réinitialiser la configuration de développement + identifiants + sessions + espace de travail (nécessite `--dev`).
- `--force` : Tuer tout écouteur existant sur le port sélectionné avant le démarrage.
- `--verbose` : Journalisation détaillée.
- `--claude-cli-logs` : Afficher uniquement les journaux claude-cli sur la console (et activer son stdout/stderr).
- `--ws-log <auto|full|compact>` : Style de journalisation WebSocket (par défaut `auto`).
- `--compact` : Alias pour `--ws-log compact`.
- `--raw-stream` : Enregistrer les événements de flux de modèle brut en jsonl.
- `--raw-stream-path <path>` : Chemin jsonl du flux brut.

## Interroger un Gateway en cours d'exécution

Toutes les commandes de requête utilisent RPC WebSocket.

Modes de sortie :

- Par défaut : lisible par l'homme (couleurs en TTY).
- `--json` : JSON lisible par machine (sans style/indicateurs de progression).
- `--no-color` (ou `NO_COLOR=1`) : Désactiver ANSI mais conserver la mise en page lisible par l'homme.

Options partagées (où supportées) :

- `--url <url>` : URL WebSocket de Gateway.
- `--token <token>` : Jeton Gateway.
- `--password <password>` : Mot de passe Gateway.
- `--timeout <ms>` : Délai d'expiration/budget (varie selon la commande).
- `--expect-final` : Attendre une réponse "finale" (appels d'agent).

### `gateway health`

```bash
openclaw gateway health --url ws://127.0.0.1:18789
```

### `gateway status`

`gateway status` affiche le service Gateway (launchd/systemd/schtasks) ainsi qu'une sonde RPC optionnelle.

```bash
openclaw gateway status
openclaw gateway status --json
```

Options :

- `--url <url>` : Remplacer l'URL de sonde.
- `--token <token>` : Authentification par jeton pour la sonde.
- `--password <password>` : Authentification par mot de passe pour la sonde.
- `--timeout <ms>` : Délai d'expiration de la sonde (par défaut `10000`).
- `--no-probe` : Ignorer la sonde RPC (vue du service uniquement).
- `--deep` : Analyser également les services au niveau du système.

### `gateway probe`

`gateway probe` est la commande "déboguer tout". Elle sonde toujours :

- votre Gateway distant configuré (s'il est défini), et
- localhost (loopback) **même si un distant est configuré**.

Si plusieurs Gateway sont accessibles, elle les affiche tous. Plusieurs Gateway sont supportés lorsque vous utilisez des fichiers de configuration/ports isolés (par exemple, bot de secours), mais la plupart des installations exécutent toujours un seul Gateway.

```bash
openclaw gateway probe
openclaw gateway probe --json
```

#### Distant via SSH (homologue d'application macOS)

Le mode "Distant via SSH" de l'application macOS utilise le transfert de port local, donc le Gateway distant (peut-être lié uniquement à loopback) devient accessible via `ws://127.0.0.1:<port>`.

Équivalent CLI :

```bash
openclaw gateway probe --ssh user@gateway-host
```

Options :

- `--ssh <target>` : `user@host` ou `user@host:port` (port par défaut `22`).
- `--ssh-identity <path>` : Fichier d'identité.
- `--ssh-auto` : Sélectionner le premier hôte Gateway découvert comme cible SSH (LAN/WAB uniquement).

Configuration (optionnelle, utilisée comme valeurs par défaut) :

- `gateway.remote.sshTarget`
- `gateway.remote.sshIdentity`

### `gateway call <method>`

Utilitaire RPC bas niveau.

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
- Les commandes de cycle de vie acceptent `--json` pour les scripts.

## Découvrir Gateway (Bonjour)

`gateway discover` analyse les balises Gateway (`_openclaw-gw._tcp`).

- Multidiffusion DNS-SD : `local.`
- Monodiffusion DNS-SD (Bonjour étendu) : sélectionner un domaine (exemple : `openclaw.internal.`) et configurer le DNS divisé + serveur DNS ; voir [/gateway/bonjour](/gateway/bonjour)

Seuls les Gateway avec la découverte Bonjour activée (par défaut) diffusent des balises.

Les enregistrements de découverte étendue incluent (TXT) :

- `role` (indice de rôle Gateway)
- `transport` (indice de transport, par exemple `gateway`)
- `gatewayPort` (port WebSocket, généralement `18789`)
- `sshPort` (port SSH ; par défaut `22` s'il n'existe pas)
- `tailnetDns` (nom d'hôte MagicDNS, s'il est disponible)
- `gatewayTls` / `gatewayTlsSha256` (TLS activé + empreinte du certificat)
- `cliPath` (indice optionnel d'installation distante)

### `gateway discover`

```bash
openclaw gateway discover
```

Options :

- `--timeout <ms>` : Délai d'expiration pour chaque commande (parcourir/résoudre) ; par défaut `2000`.
- `--json` : Sortie lisible par machine (désactive également le style/indicateurs de progression).

Exemples :

```bash
openclaw gateway discover --timeout 4000
openclaw gateway discover --json | jq '.beacons[].wsUrl'
```
