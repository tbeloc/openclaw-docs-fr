---
summary: "Flux d'application macOS pour contrôler une passerelle OpenClaw distante via SSH"
read_when:
  - Setting up or debugging remote mac control
title: "Contrôle à distance"
---

# OpenClaw distant (macOS ⇄ hôte distant)

Ce flux permet à l'application macOS d'agir comme un contrôle à distance complet pour une passerelle OpenClaw s'exécutant sur un autre hôte (bureau/serveur). C'est la fonctionnalité **Remote over SSH** (exécution distante) de l'application. Toutes les fonctionnalités—vérifications de santé, transfert de Voice Wake et Web Chat—réutilisent la même configuration SSH distante de _Paramètres → Général_.

## Modes

- **Local (ce Mac)** : Tout s'exécute sur l'ordinateur portable. Aucun SSH impliqué.
- **Remote over SSH (par défaut)** : Les commandes OpenClaw sont exécutées sur l'hôte distant. L'application mac ouvre une connexion SSH avec `-o BatchMode` plus votre identité/clé choisie et un transfert de port local.
- **Remote direct (ws/wss)** : Aucun tunnel SSH. L'application mac se connecte directement à l'URL de la passerelle (par exemple, via Tailscale Serve ou un proxy inverse HTTPS public).

## Transports distants

Le mode distant supporte deux transports :

- **Tunnel SSH** (par défaut) : Utilise `ssh -N -L ...` pour transférer le port de la passerelle vers localhost. La passerelle verra l'IP du nœud comme `127.0.0.1` car le tunnel est en boucle locale.
- **Direct (ws/wss)** : Se connecte directement à l'URL de la passerelle. La passerelle voit l'adresse IP réelle du client.

## Prérequis sur l'hôte distant

1. Installez Node + pnpm et construisez/installez l'interface de ligne de commande OpenClaw (`pnpm install && pnpm build && pnpm link --global`).
2. Assurez-vous que `openclaw` est sur PATH pour les shells non-interactifs (créez un lien symbolique dans `/usr/local/bin` ou `/opt/homebrew/bin` si nécessaire).
3. Ouvrez SSH avec authentification par clé. Nous recommandons les adresses IP **Tailscale** pour une accessibilité stable en dehors du LAN.

## Configuration de l'application macOS

1. Ouvrez _Paramètres → Général_.
2. Sous **OpenClaw runs**, choisissez **Remote over SSH** et définissez :
   - **Transport** : **SSH tunnel** ou **Direct (ws/wss)**.
   - **SSH target** : `user@host` (`:port` optionnel).
     - Si la passerelle est sur le même LAN et annonce Bonjour, sélectionnez-la dans la liste découverte pour remplir automatiquement ce champ.
   - **Gateway URL** (Direct uniquement) : `wss://gateway.example.ts.net` (ou `ws://...` pour local/LAN).
   - **Identity file** (avancé) : chemin vers votre clé.
   - **Project root** (avancé) : chemin de checkout distant utilisé pour les commandes.
   - **CLI path** (avancé) : chemin optionnel vers un point d'entrée/binaire `openclaw` exécutable (rempli automatiquement s'il est annoncé).
3. Cliquez sur **Test remote**. Le succès indique que la commande `openclaw status --json` distante s'exécute correctement. Les échecs signifient généralement des problèmes de PATH/CLI ; la sortie 127 signifie que l'interface de ligne de commande n'a pas été trouvée à distance.
4. Les vérifications de santé et Web Chat s'exécuteront maintenant automatiquement via ce tunnel SSH.

## Web Chat

- **Tunnel SSH** : Web Chat se connecte à la passerelle via le port de contrôle WebSocket transféré (18789 par défaut).
- **Direct (ws/wss)** : Web Chat se connecte directement à l'URL de passerelle configurée.
- Il n'y a plus de serveur HTTP WebChat séparé.

## Permissions

- L'hôte distant a besoin des mêmes approbations TCC que le mode local (Automation, Accessibility, Screen Recording, Microphone, Speech Recognition, Notifications). Exécutez l'intégration sur cette machine pour les accorder une fois.
- Les nœuds annoncent leur état de permission via `node.list` / `node.describe` afin que les agents sachent ce qui est disponible.

## Notes de sécurité

- Préférez les liaisons en boucle locale sur l'hôte distant et connectez-vous via SSH ou Tailscale.
- Le tunneling SSH utilise une vérification stricte de la clé d'hôte ; faites confiance à la clé d'hôte en premier pour qu'elle existe dans `~/.ssh/known_hosts`.
- Si vous liez la passerelle à une interface non-boucle locale, exigez une authentification par jeton/mot de passe.
- Voir [Security](/gateway/security) et [Tailscale](/gateway/tailscale).

## Flux de connexion WhatsApp (distant)

- Exécutez `openclaw channels login --verbose` **sur l'hôte distant**. Scannez le code QR avec WhatsApp sur votre téléphone.
- Réexécutez la connexion sur cet hôte si l'authentification expire. La vérification de santé signalera les problèmes de lien.

## Dépannage

- **exit 127 / not found** : `openclaw` n'est pas sur PATH pour les shells non-login. Ajoutez-le à `/etc/paths`, votre rc shell, ou créez un lien symbolique dans `/usr/local/bin`/`/opt/homebrew/bin`.
- **Health probe failed** : vérifiez l'accessibilité SSH, PATH, et que Baileys est connecté (`openclaw status --json`).
- **Web Chat stuck** : confirmez que la passerelle s'exécute sur l'hôte distant et que le port transféré correspond au port WS de la passerelle ; l'interface utilisateur nécessite une connexion WS saine.
- **Node IP shows 127.0.0.1** : attendu avec le tunnel SSH. Basculez **Transport** vers **Direct (ws/wss)** si vous voulez que la passerelle voie l'adresse IP réelle du client.
- **Voice Wake** : les phrases déclencheurs sont transférées automatiquement en mode distant ; aucun forwarder séparé n'est nécessaire.

## Sons de notification

Choisissez les sons par notification à partir de scripts avec `openclaw` et `node.invoke`, par exemple :

```bash
openclaw nodes notify --node <id> --title "Ping" --body "Remote gateway ready" --sound Glass
```

Il n'y a plus de bouton bascule global « son par défaut » dans l'application ; les appelants choisissent un son (ou aucun) par demande.
