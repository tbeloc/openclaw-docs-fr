---
summary: "Découverte de nœuds et transports (Bonjour, Tailscale, SSH) pour trouver la passerelle"
read_when:
  - Implementing or changing Bonjour discovery/advertising
  - Adjusting remote connection modes (direct vs SSH)
  - Designing node discovery + pairing for remote nodes
title: "Découverte et transports"
---

# Découverte et transports

OpenClaw a deux problèmes distincts qui se ressemblent en surface :

1. **Contrôle à distance de l'opérateur** : l'application de barre de menu macOS contrôlant une passerelle s'exécutant ailleurs.
2. **Appairage de nœuds** : iOS/Android (et futurs nœuds) trouvant une passerelle et s'appairant de manière sécurisée.

L'objectif de conception est de garder toute découverte/publicité réseau dans la **Passerelle de nœud** (`openclaw gateway`) et de garder les clients (application Mac, iOS) comme consommateurs.

## Termes

- **Passerelle** : un processus de passerelle unique et longue durée qui possède l'état (sessions, appairage, registre de nœuds) et exécute les canaux. La plupart des configurations en utilisent une par hôte ; les configurations multi-passerelles isolées sont possibles.
- **Passerelle WS (plan de contrôle)** : le point de terminaison WebSocket sur `127.0.0.1:18789` par défaut ; peut être lié au LAN/tailnet via `gateway.bind`.
- **Transport WS direct** : un point de terminaison Passerelle WS face au LAN/tailnet (pas de SSH).
- **Transport SSH (secours)** : contrôle à distance en transférant `127.0.0.1:18789` via SSH.
- **Pont TCP hérité (déprécié/supprimé)** : transport de nœud plus ancien (voir [Protocole Bridge](/gateway/bridge-protocol)) ; n'est plus annoncé pour la découverte.

Détails du protocole :

- [Protocole de passerelle](/gateway/protocol)
- [Protocole Bridge (hérité)](/gateway/bridge-protocol)

## Pourquoi nous gardons à la fois « direct » et SSH

- **WS direct** offre la meilleure UX sur le même réseau et au sein d'un tailnet :
  - découverte automatique sur LAN via Bonjour
  - jetons d'appairage + ACL possédés par la passerelle
  - aucun accès shell requis ; la surface du protocole peut rester étroite et vérifiable
- **SSH** reste le secours universel :
  - fonctionne partout où vous avez accès SSH (même sur des réseaux non liés)
  - survit aux problèmes de multidiffusion/mDNS
  - ne nécessite aucun nouveau port entrant en dehors de SSH

## Entrées de découverte (comment les clients apprennent où se trouve la passerelle)

### 1) Bonjour / mDNS (LAN uniquement)

Bonjour est au mieux et ne traverse pas les réseaux. Il est utilisé uniquement pour la commodité « même LAN ».

Direction cible :

- La **passerelle** annonce son point de terminaison WS via Bonjour.
- Les clients parcourent et affichent une liste « choisir une passerelle », puis stockent le point de terminaison choisi.

Dépannage et détails de balise : [Bonjour](/gateway/bonjour).

#### Détails de la balise de service

- Types de service :
  - `_openclaw-gw._tcp` (balise de transport de passerelle)
- Clés TXT (non-secrètes) :
  - `role=gateway`
  - `lanHost=<hostname>.local`
  - `sshPort=22` (ou ce qui est annoncé)
  - `gatewayPort=18789` (Passerelle WS + HTTP)
  - `gatewayTls=1` (uniquement quand TLS est activé)
  - `gatewayTlsSha256=<sha256>` (uniquement quand TLS est activé et l'empreinte est disponible)
  - `canvasPort=<port>` (port d'hôte canvas ; actuellement le même que `gatewayPort` quand l'hôte canvas est activé)
  - `cliPath=<path>` (optionnel ; chemin absolu vers un point d'entrée ou un binaire `openclaw` exécutable)
  - `tailnetDns=<magicdns>` (indice optionnel ; détecté automatiquement quand Tailscale est disponible)

Notes de sécurité :

- Les enregistrements TXT Bonjour/mDNS sont **non authentifiés**. Les clients doivent traiter les valeurs TXT comme des indices UX uniquement.
- Le routage (hôte/port) doit préférer le **point de terminaison de service résolu** (SRV + A/AAAA) plutôt que `lanHost`, `tailnetDns` ou `gatewayPort` fournis par TXT.
- L'épinglage TLS ne doit jamais permettre à un `gatewayTlsSha256` annoncé de remplacer une épingle précédemment stockée.
- Les nœuds iOS/Android doivent traiter les connexions directes basées sur la découverte comme **TLS uniquement** et exiger une confirmation explicite « faire confiance à cette empreinte » avant de stocker une épingle pour la première fois (vérification hors bande).

Désactiver/remplacer :

- `OPENCLAW_DISABLE_BONJOUR=1` désactive la publicité.
- `gateway.bind` dans `~/.openclaw/openclaw.json` contrôle le mode de liaison de la passerelle.
- `OPENCLAW_SSH_PORT` remplace le port SSH annoncé dans TXT (par défaut 22).
- `OPENCLAW_TAILNET_DNS` publie un indice `tailnetDns` (MagicDNS).
- `OPENCLAW_CLI_PATH` remplace le chemin CLI annoncé.

### 2) Tailnet (inter-réseaux)

Pour les configurations de style Londres/Vienne, Bonjour ne sera pas utile. La cible « directe » recommandée est :

- Nom Tailscale MagicDNS (préféré) ou une adresse IP tailnet stable.

Si la passerelle peut détecter qu'elle s'exécute sous Tailscale, elle publie `tailnetDns` comme indice optionnel pour les clients (y compris les balises de zone large).

### 3) Cible manuelle / SSH

Quand il n'y a pas de route directe (ou que direct est désactivé), les clients peuvent toujours se connecter via SSH en transférant le port de passerelle de boucle locale.

Voir [Accès à distance](/gateway/remote).

## Sélection de transport (politique client)

Comportement client recommandé :

1. Si un point de terminaison direct appairé est configuré et accessible, l'utiliser.
2. Sinon, si Bonjour trouve une passerelle sur LAN, offrir un choix « Utiliser cette passerelle » en un clic et l'enregistrer comme point de terminaison direct.
3. Sinon, si un DNS/IP tailnet est configuré, essayer direct.
4. Sinon, revenir à SSH.

## Appairage + authentification (transport direct)

La passerelle est la source de vérité pour l'admission des nœuds/clients.

- Les demandes d'appairage sont créées/approuvées/rejetées dans la passerelle (voir [Appairage de passerelle](/gateway/pairing)).
- La passerelle applique :
  - authentification (jeton / paire de clés)
  - portées/ACL (la passerelle n'est pas un proxy brut pour chaque méthode)
  - limites de débit

## Responsabilités par composant

- **Passerelle** : annonce les balises de découverte, possède les décisions d'appairage et héberge le point de terminaison WS.
- **Application macOS** : vous aide à choisir une passerelle, affiche les invites d'appairage et utilise SSH uniquement comme secours.
- **Nœuds iOS/Android** : parcourent Bonjour par commodité et se connectent à la Passerelle WS appairée.
