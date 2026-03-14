---
read_when:
  - 运行或排查远程 Gateway 网关设置问题
summary: 使用 SSH 隧道（Gateway WS）和 tailnet 进行远程访问
title: 远程访问
x-i18n:
  generated_at: "2026-02-03T07:48:40Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 7e00bd2e048dfbd829913bef0f40a791b8d8c3e2f8a115fc0a13b03f136ebc93
  source_path: gateway/remote.md
  workflow: 15
---

# Accès à distance (SSH, tunnels et tailnet)

Ce dépôt prend en charge l'« accès à distance SSH » en exécutant une seule passerelle Gateway (nœud principal) sur un hôte dédié (bureau/serveur) et en laissant les clients s'y connecter.

- Pour les **opérateurs (vous/application macOS)** : les tunnels SSH sont une solution de secours universelle.
- Pour les **nœuds (iOS/Android et appareils futurs)** : connexion à la **WebSocket** Gateway (LAN/tailnet ou via tunnel SSH selon les besoins).

## Concept fondamental

- La WebSocket Gateway est liée à la **loopback** du port que vous configurez (18789 par défaut).
- Pour une utilisation à distance, vous transférez ce port loopback via SSH (ou utilisez tailnet/VPN pour réduire les besoins en tunnel).

## Configuration VPN/tailnet courante (où se trouve l'agent)

Considérez l'**hôte Gateway** comme « l'endroit où se trouve l'agent ». Il possède les sessions, les profils d'authentification, les canaux et l'état.
Votre ordinateur portable/bureau (et les nœuds) se connectent à cet hôte.

### 1) Gateway toujours en ligne dans tailnet (VPS ou serveur domestique)

Exécutez Gateway sur un hôte persistant et accédez-y via **Tailscale** ou SSH.

- **Meilleure expérience utilisateur :** conservez `gateway.bind: "loopback"` et utilisez **Tailscale Serve** pour l'interface de contrôle.
- **Solution de secours :** conservez loopback + établissez un tunnel SSH à partir de n'importe quelle machine qui a besoin d'accès.
- **Exemples :** [exe.dev](/install/exe-dev) (VM simple) ou [Hetzner](/install/hetzner) (VPS production).

C'est idéal quand votre ordinateur portable se met souvent en veille mais que vous voulez que l'agent soit toujours en ligne.

### 2) Bureau domestique exécutant Gateway, ordinateur portable comme contrôle à distance

L'ordinateur portable **n'exécute pas** l'agent. Il se connecte à distance :

- Utilisez le mode **Remote over SSH** de l'application macOS (Paramètres → Général → « OpenClaw runs »).
- L'application ouvre et gère le tunnel, donc WebChat + les contrôles de santé « fonctionnent directement ».

Guide opérationnel : [Accès à distance macOS](/platforms/mac/remote).

### 3) Ordinateur portable exécutant Gateway, accès à distance à partir d'autres machines

Conservez Gateway localement mais exposez-le de manière sécurisée :

- Tunnel SSH d'autres machines vers votre ordinateur portable, ou
- Tailscale Serve pour l'interface de contrôle et conservez Gateway en loopback uniquement.

Guides : [Tailscale](/gateway/tailscale) et [Aperçu Web](/web).

## Flux de commandes (ce qui s'exécute où)

Un service Gateway possède l'état + les canaux. Les nœuds sont des périphériques.

Exemple de flux (Telegram → nœud) :

- Le message Telegram arrive à la **Gateway**.
- Gateway exécute l'**agent** et décide s'il faut appeler un outil de nœud.
- Gateway appelle le **nœud** via Gateway WebSocket (RPC `node.*`).
- Le nœud retourne le résultat ; Gateway répond à Telegram.

Clarifications :

- **Les nœuds n'exécutent pas le service Gateway.** À moins que vous n'exécutiez intentionnellement une configuration isolée, une seule Gateway doit s'exécuter par hôte (voir [Passerelles multiples](/gateway/multiple-gateways)).
- Le « mode nœud » de l'application macOS est simplement un client nœud via Gateway WebSocket.

## Tunnels SSH (CLI + outils)

Créez un tunnel local vers une WebSocket Gateway distante :

```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

Une fois le tunnel établi :

- `openclaw health` et `openclaw status --deep` accèdent maintenant à la Gateway distante via `ws://127.0.0.1:18789`.
- `openclaw gateway {status,health,send,agent,call}` peut également spécifier l'URL transférée via `--url` si nécessaire.

Remarque : remplacez `18789` par votre `gateway.port` configuré (ou `--port`/`OPENCLAW_GATEWAY_PORT`).

## Valeurs par défaut CLI à distance

Vous pouvez persister la cible distante pour que les commandes CLI l'utilisent par défaut :

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

Quand Gateway est limité à loopback, conservez l'URL comme `ws://127.0.0.1:18789` et ouvrez d'abord le tunnel SSH.

## Interface de chat via SSH

WebChat n'utilise plus de port HTTP séparé. L'interface de chat SwiftUI se connecte directement à la WebSocket Gateway.

- Transférez `18789` via SSH (voir ci-dessus), puis laissez le client se connecter à `ws://127.0.0.1:18789`.
- Sur macOS, préférez le mode « Remote over SSH » de l'application, qui gère automatiquement les tunnels.

## Application macOS « Remote over SSH »

L'application de barre de menu macOS peut piloter de bout en bout la même configuration (vérification d'état à distance, WebChat et transfert de réveil vocal).

Guide opérationnel : [Accès à distance macOS](/platforms/mac/remote).

## Règles de sécurité (à distance/VPN)

Version courte : **conservez Gateway en loopback uniquement**, sauf si vous êtes sûr d'avoir besoin de la lier.

- **Loopback + SSH/Tailscale Serve** est la configuration par défaut la plus sûre (pas d'exposition publique).
- Les liaisons **non-loopback** (`lan`/`tailnet`/`custom`, ou `auto` quand loopback n'est pas disponible) doivent utiliser un jeton d'authentification/mot de passe.
- `gateway.remote.token` est **uniquement** pour les appels CLI distants — il **n'active pas** l'authentification locale.
- `gateway.remote.tlsFingerprint` épingle le certificat TLS distant lors de l'utilisation de `wss://`.
- Quand `gateway.auth.allowTailscale: true`, **Tailscale Serve** peut s'authentifier via les en-têtes d'identité. Si vous voulez utiliser un jeton/mot de passe, définissez-le sur `false`.
- Considérez l'accès au navigateur comme un accès opérateur : tailnet uniquement + appairage de nœud intentionnel.

En profondeur : [Sécurité](/gateway/security).
