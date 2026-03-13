---
read_when:
  - 设置或调试远程 mac 控制时
summary: macOS 应用通过 SSH 控制远程 OpenClaw Gateway 网关的流程
title: 远程控制
x-i18n:
  generated_at: "2026-02-03T07:52:53Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 61b43707250d5515fd0f85f092bdde24598f14904398ff3fca3736bcc48d72f8
  source_path: platforms/mac/remote.md
  workflow: 15
---

# OpenClaw à distance (macOS ⇄ hôte distant)

Ce processus permet à l'application macOS d'agir comme un contrôle à distance complet pour une passerelle OpenClaw Gateway s'exécutant sur un autre hôte (bureau/serveur). Il s'agit de la fonctionnalité **Remote over SSH** (exécution à distance) de l'application. Toutes les fonctionnalités — vérification de l'état, transfert de réveil vocal et Web Chat — réutilisent la même configuration SSH distante de _Settings → General_.

## Modes

- **Local (this Mac)** : tout s'exécute sur l'ordinateur portable. Aucun SSH impliqué.
- **Remote over SSH (par défaut)** : les commandes OpenClaw s'exécutent sur l'hôte distant. L'application mac ouvre une connexion SSH avec `-o BatchMode` plus l'identité/clé de votre choix, et effectue un transfert de port local.
- **Remote direct (ws/wss)** : pas de tunnel SSH. L'application mac se connecte directement à l'URL de la passerelle Gateway (par exemple, via Tailscale Serve ou un proxy inverse HTTPS public).

## Transports distants

Le mode distant prend en charge deux transports :

- **Tunnel SSH** (par défaut) : utilise `ssh -N -L ...` pour transférer le port de la passerelle Gateway vers localhost. La passerelle Gateway verra l'IP du nœud comme `127.0.0.1`, car le tunnel est une boucle locale.
- **Direct (ws/wss)** : connexion directe à l'URL de la passerelle Gateway. La passerelle Gateway voit l'adresse IP réelle du client.

## Prérequis sur l'hôte distant

1. Installez Node + pnpm et construisez/installez OpenClaw CLI (`pnpm install && pnpm build && pnpm link --global`).
2. Assurez-vous que `openclaw` se trouve dans le PATH du shell non interactif (le cas échéant, créez un lien symbolique vers `/usr/local/bin` ou `/opt/homebrew/bin`).
3. Activez SSH avec authentification par clé. Nous recommandons d'utiliser l'adresse IP **Tailscale** pour une accessibilité stable en dehors du réseau local.

## Configuration de l'application macOS

1. Ouvrez _Settings → General_.
2. Sous **OpenClaw runs**, sélectionnez **Remote over SSH** et configurez :
   - **Transport** : **SSH tunnel** ou **Direct (ws/wss)**.
   - **SSH target** : `user@host` (`:port` optionnel).
     - Si la passerelle Gateway se trouve sur le même réseau local et diffuse Bonjour, sélectionnez-la dans la liste de découverte pour remplir automatiquement ce champ.
   - **Gateway URL** (Direct uniquement) : `wss://gateway.example.ts.net` (ou `ws://...` pour local/réseau local).
   - **Identity file** (Avancé) : chemin d'accès à votre clé.
   - **Project root** (Avancé) : chemin de checkout distant utilisé pour les commandes.
   - **CLI path** (Avancé) : chemin optionnel vers le point d'entrée/binaire `openclaw` exécutable (rempli automatiquement lors de la diffusion).
3. Cliquez sur **Test remote**. Le succès indique que `openclaw status --json` distant s'exécute correctement. L'échec signifie généralement un problème de PATH/CLI ; le code de sortie 127 indique que le CLI est introuvable à distance.
4. La vérification de l'état et Web Chat s'exécuteront désormais automatiquement via ce tunnel SSH.

## Web Chat

- **Tunnel SSH** : Web Chat se connecte à la passerelle Gateway via le port de contrôle WebSocket transféré (18789 par défaut).
- **Direct (ws/wss)** : Web Chat se connecte directement à l'URL de la passerelle Gateway configurée.
- Il n'y a plus de serveur HTTP WebChat séparé.

## Permissions

- L'hôte distant nécessite les mêmes approbations TCC que le système local (Automation, Accessibility, Screen Recording, Microphone, Speech Recognition, Notifications). Exécutez l'assistant sur cette machine pour les accorder une seule fois.
- Les nœuds diffusent leur état de permissions via `node.list` / `node.describe` afin que les agents sachent lesquels sont disponibles.

## Considérations de sécurité

- Privilégiez les liaisons loopback sur l'hôte distant et connectez-vous via SSH ou Tailscale.
- Si vous liez la passerelle Gateway à une interface non-loopback, exigez une authentification par jeton/mot de passe.
- Voir [Security](/gateway/security) et [Tailscale](/gateway/tailscale).

## Flux de connexion WhatsApp (distant)

- **Sur l'hôte distant**, exécutez `openclaw channels login --verbose`. Scannez le code QR avec WhatsApp sur votre téléphone.
- Si l'authentification expire, réexécutez la connexion sur cet hôte. La vérification de l'état affichera les problèmes d'association.

## Dépannage

- **exit 127 / not found** : `openclaw` ne se trouve pas dans le PATH du shell non-login. Ajoutez-le à `/etc/paths`, votre rc shell, ou créez un lien symbolique vers `/usr/local/bin`/`/opt/homebrew/bin`.
- **Health probe failed** : vérifiez l'accessibilité SSH, le PATH, et si Baileys est connecté (`openclaw status --json`).
- **Web Chat bloqué** : confirmez que la passerelle Gateway s'exécute sur l'hôte distant, que le port transféré correspond au port WS de la passerelle Gateway ; l'interface utilisateur nécessite une connexion WS saine.
- **Node IP affiche 127.0.0.1** : c'est attendu lors de l'utilisation d'un tunnel SSH. Si vous souhaitez que la passerelle Gateway voie l'adresse IP réelle du client, basculez **Transport** vers **Direct (ws/wss)**.
- **Voice Wake** : la phrase de déclenchement est automatiquement transférée en mode distant ; aucun transfert séparé n'est nécessaire.

## Sons de notification

Choisissez un son pour chaque notification via un script avec `openclaw` et `node.invoke`, par exemple :

```bash
openclaw nodes notify --node <id> --title "Ping" --body "Remote gateway ready" --sound Glass
```

Il n'y a plus de commutateur global « son par défaut » dans l'application ; l'appelant choisit le son pour chaque demande (ou pas de son).
