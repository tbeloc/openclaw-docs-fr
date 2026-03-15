---
summary: "Accès à distance via tunnels SSH (Gateway WS) et tailnets"
read_when:
  - Running or troubleshooting remote gateway setups
title: "Accès à distance"
---

# Accès à distance (SSH, tunnels et tailnets)

Ce repo supporte « remote over SSH » en maintenant une seule Gateway (le maître) en cours d'exécution sur un hôte dédié (desktop/serveur) et en connectant les clients à celle-ci.

- Pour les **opérateurs (vous / l'app macOS)** : le tunneling SSH est le fallback universel.
- Pour les **nœuds (iOS/Android et appareils futurs)** : connectez-vous à la **WebSocket** de la Gateway (LAN/tailnet ou tunnel SSH selon les besoins).

## L'idée centrale

- La WebSocket de la Gateway se lie à **loopback** sur votre port configuré (par défaut 18789).
- Pour une utilisation à distance, vous transférez ce port loopback via SSH (ou utilisez un tailnet/VPN et tunnelisez moins).

## Configurations VPN/tailnet courantes (où l'agent réside)

Pensez à l'**hôte Gateway** comme « où l'agent réside ». Il possède les sessions, les profils d'authentification, les canaux et l'état.
Votre laptop/desktop (et les nœuds) se connectent à cet hôte.

### 1) Gateway toujours active dans votre tailnet (VPS ou serveur domestique)

Exécutez la Gateway sur un hôte persistant et accédez-y via **Tailscale** ou SSH.

- **Meilleure UX :** gardez `gateway.bind: "loopback"` et utilisez **Tailscale Serve** pour l'interface de contrôle.
- **Fallback :** gardez loopback + tunnel SSH depuis n'importe quelle machine qui a besoin d'accès.
- **Exemples :** [exe.dev](/install/exe-dev) (VM facile) ou [Hetzner](/install/hetzner) (VPS production).

C'est idéal quand votre laptop s'endort souvent mais que vous voulez que l'agent soit toujours actif.

### 2) Le desktop domestique exécute la Gateway, le laptop est le contrôle à distance

Le laptop n'exécute **pas** l'agent. Il se connecte à distance :

- Utilisez le mode **Remote over SSH** de l'app macOS (Settings → General → « OpenClaw runs »).
- L'app ouvre et gère le tunnel, donc WebChat + les vérifications de santé « fonctionnent simplement ».

Runbook : [accès à distance macOS](/platforms/mac/remote).

### 3) Le laptop exécute la Gateway, accès à distance depuis d'autres machines

Gardez la Gateway locale mais exposez-la en toute sécurité :

- Tunnel SSH vers le laptop depuis d'autres machines, ou
- Tailscale Serve l'interface de contrôle et gardez la Gateway loopback uniquement.

Guide : [Tailscale](/gateway/tailscale) et [Aperçu Web](/web).

## Flux de commande (ce qui s'exécute où)

Un service gateway possède l'état + les canaux. Les nœuds sont des périphériques.

Exemple de flux (Telegram → nœud) :

- Le message Telegram arrive à la **Gateway**.
- La Gateway exécute l'**agent** et décide s'il faut appeler un outil de nœud.
- La Gateway appelle le **nœud** via la WebSocket de la Gateway (`node.*` RPC).
- Le nœud retourne le résultat ; la Gateway répond à Telegram.

Notes :

- **Les nœuds n'exécutent pas le service gateway.** Une seule gateway devrait s'exécuter par hôte sauf si vous exécutez intentionnellement des profils isolés (voir [Plusieurs gateways](/gateway/multiple-gateways)).
- Le mode « nœud » de l'app macOS est juste un client nœud via la WebSocket de la Gateway.

## Tunnel SSH (CLI + outils)

Créez un tunnel local vers la Gateway WS distante :

```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

Avec le tunnel actif :

- `openclaw health` et `openclaw status --deep` atteignent maintenant la gateway distante via `ws://127.0.0.1:18789`.
- `openclaw gateway {status,health,send,agent,call}` peut également cibler l'URL transférée via `--url` si nécessaire.

Note : remplacez `18789` par votre `gateway.port` configuré (ou `--port`/`OPENCLAW_GATEWAY_PORT`).
Note : quand vous passez `--url`, la CLI ne revient pas aux identifiants de config ou d'environnement.
Incluez `--token` ou `--password` explicitement. Les identifiants explicites manquants sont une erreur.

## Valeurs par défaut CLI distantes

Vous pouvez persister une cible distante pour que les commandes CLI l'utilisent par défaut :

```json5
{
  gateway: {
    mode: "remote",
    remote: {
      url: "ws://127.0.0.1:18789",
      token: "your-token",
    },
  },
}
```

Quand la gateway est loopback uniquement, gardez l'URL à `ws://127.0.0.1:18789` et ouvrez le tunnel SSH d'abord.

## Précédence des identifiants

La résolution des identifiants de la Gateway suit un contrat partagé unique sur les chemins call/probe/status et la surveillance d'approbation d'exécution Discord. Node-host utilise le même contrat de base avec une exception en mode local (il ignore intentionnellement `gateway.remote.*`) :

- Les identifiants explicites (`--token`, `--password`, ou `gatewayToken` d'outil) gagnent toujours sur les chemins d'appel qui acceptent l'authentification explicite.
- Sécurité des remplacements d'URL :
  - Les remplacements d'URL CLI (`--url`) ne réutilisent jamais les identifiants implicites de config/env.
  - Les remplacements d'URL Env (`OPENCLAW_GATEWAY_URL`) peuvent utiliser les identifiants env uniquement (`OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD`).
- Valeurs par défaut du mode local :
  - token : `OPENCLAW_GATEWAY_TOKEN` -> `gateway.auth.token` -> `gateway.remote.token` (le fallback distant s'applique uniquement quand l'entrée du token d'authentification local est non définie)
  - password : `OPENCLAW_GATEWAY_PASSWORD` -> `gateway.auth.password` -> `gateway.remote.password` (le fallback distant s'applique uniquement quand l'entrée du mot de passe d'authentification local est non définie)
- Valeurs par défaut du mode distant :
  - token : `gateway.remote.token` -> `OPENCLAW_GATEWAY_TOKEN` -> `gateway.auth.token`
  - password : `OPENCLAW_GATEWAY_PASSWORD` -> `gateway.remote.password` -> `gateway.auth.password`
- Exception du mode local node-host : `gateway.remote.token` / `gateway.remote.password` sont ignorés.
- Les vérifications de token probe/status distantes sont strictes par défaut : elles utilisent `gateway.remote.token` uniquement (pas de fallback de token local) quand elles ciblent le mode distant.
- Les variables env `CLAWDBOT_GATEWAY_*` héritées sont utilisées uniquement par les chemins d'appel de compatibilité ; la résolution probe/status/auth utilise `OPENCLAW_GATEWAY_*` uniquement.

## Interface de chat sur SSH

WebChat n'utilise plus de port HTTP séparé. L'interface de chat SwiftUI se connecte directement à la WebSocket de la Gateway.

- Transférez `18789` via SSH (voir ci-dessus), puis connectez les clients à `ws://127.0.0.1:18789`.
- Sur macOS, préférez le mode « Remote over SSH » de l'app, qui gère le tunnel automatiquement.

## App macOS « Remote over SSH »

L'app de barre de menu macOS peut piloter la même configuration de bout en bout (vérifications de statut distant, WebChat et transfert de Voice Wake).

Runbook : [accès à distance macOS](/platforms/mac/remote).

## Règles de sécurité (distant/VPN)

Version courte : **gardez la Gateway loopback uniquement** sauf si vous êtes sûr d'avoir besoin d'une liaison.

- **Loopback + SSH/Tailscale Serve** est la valeur par défaut la plus sûre (pas d'exposition publique).
- Le `ws://` en texte clair est loopback uniquement par défaut. Pour les réseaux privés de confiance,
  définissez `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` sur le processus client comme bris de verre.
- **Les liaisons non-loopback** (`lan`/`tailnet`/`custom`, ou `auto` quand loopback n'est pas disponible) doivent utiliser des tokens/mots de passe d'authentification.
- `gateway.remote.token` / `.password` sont des sources d'identifiants client. Ils ne configurent **pas** l'authentification du serveur par eux-mêmes.
- Les chemins d'appel locaux peuvent utiliser `gateway.remote.*` comme fallback uniquement quand `gateway.auth.*` est non défini.
- Si `gateway.auth.token` / `gateway.auth.password` est explicitement configuré via SecretRef et non résolu, la résolution échoue fermée (pas de fallback distant masquant).
- `gateway.remote.tlsFingerprint` épingle le certificat TLS distant quand vous utilisez `wss://`.
- **Tailscale Serve** peut authentifier le trafic de l'interface de contrôle/WebSocket via les en-têtes d'identité
  quand `gateway.auth.allowTailscale: true` ; les points de terminaison de l'API HTTP nécessitent toujours
  une authentification par token/mot de passe. Ce flux sans token suppose que l'hôte gateway est
  de confiance. Définissez-le à `false` si vous voulez des tokens/mots de passe partout.
- Traitez le contrôle du navigateur comme l'accès opérateur : tailnet uniquement + appairage de nœud délibéré.

Approfondissement : [Sécurité](/gateway/security).
