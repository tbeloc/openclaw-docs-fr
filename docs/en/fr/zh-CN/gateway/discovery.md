---
read_when:
  - 实现或更改 Bonjour 发现/广播
  - 调整远程连接模式（直连 vs SSH）
  - 设计远程节点的节点发现 + 配对
summary: 用于发现 Gateway 网关的节点发现和传输协议（Bonjour、Tailscale、SSH）
title: 设备发现 + 传输协议
x-i18n:
  generated_at: "2026-02-03T10:06:11Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: e12172c181515bfa6aab8625ed3fbc335b80ba92e2b516c02c6066aeeb9f884c
  source_path: gateway/discovery.md
  workflow: 15
---

# Découverte des appareils et protocoles de transport

OpenClaw a deux problèmes différents qui peuvent sembler similaires en surface :

1. **Contrôle à distance de l'opérateur** : l'application de la barre de menus macOS contrôle une passerelle Gateway s'exécutant ailleurs.
2. **Appairage des nœuds** : iOS/Android (et les nœuds futurs) découvrent la passerelle Gateway et s'appairent de manière sécurisée.

L'objectif de conception est de conserver toute la découverte/diffusion réseau dans la **passerelle Gateway** (`openclaw gateway`), et de laisser les clients (application Mac, iOS) en tant que consommateurs.

## Terminologie

- **Passerelle Gateway** : un processus de passerelle Gateway à long terme qui possède l'état (sessions, appairages, registre des nœuds) et exécute les canaux. La plupart des configurations utilisent une par hôte ; les configurations multi-Gateway isolées sont également possibles.
- **WS de passerelle Gateway (plan de contrôle)** : point de terminaison WebSocket par défaut sur `127.0.0.1:18789` ; peut être lié à LAN/tailnet via `gateway.bind`.
- **Transport WS direct** : point de terminaison WS de passerelle Gateway orienté LAN/tailnet (sans SSH).
- **Transport SSH (secours)** : contrôle à distance via transfert SSH de `127.0.0.1:18789`.
- **Pont TCP hérité (obsolète/supprimé)** : ancien transport de nœud (voir [Protocole de pont](/gateway/bridge-protocol)) ; n'est plus utilisé pour la diffusion de découverte.

Détails des protocoles :

- [Protocole de passerelle Gateway](/gateway/protocol)
- [Protocole de pont (hérité)](/gateway/bridge-protocol)

## Pourquoi nous conservons à la fois « direct » et SSH

- **WS direct** offre la meilleure expérience utilisateur sur le même réseau et tailnet :
  - Découverte automatique sur LAN via Bonjour
  - Jeton d'appairage + ACL gérés par la passerelle Gateway
  - Pas d'accès shell requis ; la surface du protocole reste compacte et auditable
- **SSH** reste un mécanisme de secours universel :
  - Fonctionne tant que vous avez accès SSH (même sur des réseaux sans rapport)
  - Peut gérer les problèmes de multidiffusion/mDNS
  - Aucun nouveau port entrant requis au-delà de SSH

## Entrées de découverte (comment les clients connaissent l'emplacement de la passerelle Gateway)

### 1) Bonjour / mDNS (LAN uniquement)

Bonjour est au mieux un effort et ne traverse pas les réseaux. Il est utilisé uniquement pour la commodité du « même LAN ».

Direction cible :

- La **passerelle Gateway** diffuse son point de terminaison WS via Bonjour.
- Les clients parcourent et affichent une liste « Sélectionner une passerelle Gateway », puis stockent le point de terminaison sélectionné.

Dépannage et détails des balises : [Bonjour](/gateway/bonjour).

#### Détails de la balise de service

- Type de service :
  - `_openclaw-gw._tcp` (balise de transport de passerelle Gateway)
- Clés TXT (non confidentielles) :
  - `role=gateway`
  - `lanHost=<hostname>.local`
  - `sshPort=22` (ou port diffusé)
  - `gatewayPort=18789` (WS + HTTP de passerelle Gateway)
  - `gatewayTls=1` (uniquement si TLS est activé)
  - `gatewayTlsSha256=<sha256>` (uniquement si TLS est activé et l'empreinte est disponible)
  - `canvasPort=18793` (port d'hôte de canevas par défaut ; servant `/__openclaw__/canvas/`)
  - `cliPath=<path>` (optionnel ; chemin absolu vers un point d'entrée `openclaw` exécutable ou un binaire)
  - `tailnetDns=<magicdns>` (conseil optionnel ; détection automatique quand Tailscale est disponible)

Désactiver/remplacer :

- `OPENCLAW_DISABLE_BONJOUR=1` désactive la diffusion.
- `gateway.bind` dans `~/.openclaw/openclaw.json` contrôle le mode de liaison de la passerelle Gateway.
- `OPENCLAW_SSH_PORT` remplace le port SSH diffusé dans TXT (par défaut 22).
- `OPENCLAW_TAILNET_DNS` publie le conseil `tailnetDns` (MagicDNS).
- `OPENCLAW_CLI_PATH` remplace le chemin CLI diffusé.

### 2) Tailnet (entre réseaux)

Pour les configurations de style Londres/Vienne, Bonjour ne peut pas aider. La cible « directe » recommandée est :

- Nom MagicDNS Tailscale (préféré) ou IP tailnet stable.

Si la passerelle Gateway peut détecter qu'elle s'exécute sous Tailscale, elle publie `tailnetDns` comme conseil optionnel pour les clients (y compris les balises de zone large).

### 3) Cible manuelle / SSH

Quand il n'y a pas de routage direct (ou que le direct est désactivé), les clients peuvent toujours se connecter en transférant le port de passerelle Gateway de boucle locale via SSH.

Voir [Accès à distance](/gateway/remote).

## Sélection du transport (stratégie client)

Comportement client recommandé :

1. Si un point de terminaison direct appairé est configuré et accessible, l'utiliser.
2. Sinon, si Bonjour trouve une passerelle Gateway sur le LAN, proposer une sélection « Utiliser cette passerelle Gateway » en un clic et l'enregistrer comme point de terminaison direct.
3. Sinon, si DNS/IP tailnet est configuré, essayer la connexion directe.
4. Sinon, revenir à SSH.

## Appairage + authentification (transport direct)

La passerelle Gateway est l'unique autorité pour l'admission des nœuds/clients.

- Les demandes d'appairage sont créées/approuvées/rejetées dans la passerelle Gateway (voir [Appairage de passerelle Gateway](/gateway/pairing)).
- La passerelle Gateway applique :
  - Authentification (jeton / paire de clés)
  - Portée/ACL (la passerelle Gateway n'est pas un proxy brut pour chaque méthode)
  - Limitation de débit

## Responsabilités des composants

- **Passerelle Gateway** : diffuse les balises de découverte, possède l'autorité de décision d'appairage et héberge le point de terminaison WS.
- **Application macOS** : vous aide à sélectionner une passerelle Gateway, affiche les invites d'appairage, utilise SSH uniquement comme mécanisme de secours.
- **Nœuds iOS/Android** : utilisent la navigation Bonjour comme fonction de commodité, se connectent à la passerelle Gateway WS appairée.
