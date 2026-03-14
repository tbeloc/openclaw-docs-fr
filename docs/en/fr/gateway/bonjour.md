```markdown
---
summary: "Découverte Bonjour/mDNS + débogage (balises Gateway, clients et modes de défaillance courants)"
read_when:
  - Débogage des problèmes de découverte Bonjour sur macOS/iOS
  - Modification des types de service mDNS, des enregistrements TXT ou de l'UX de découverte
title: "Découverte Bonjour"
---

# Découverte Bonjour / mDNS

OpenClaw utilise Bonjour (mDNS / DNS‑SD) comme une **commodité LAN uniquement** pour découvrir
une Gateway active (point de terminaison WebSocket). C'est un meilleur effort et ne **remplace pas** SSH ou
la connectivité basée sur Tailnet.

## Bonjour large zone (DNS‑SD Unicast) sur Tailscale

Si le nœud et la gateway se trouvent sur des réseaux différents, le mDNS multicast ne traversera pas la
limite. Vous pouvez conserver la même UX de découverte en basculant vers **DNS‑SD unicast**
("Bonjour large zone") sur Tailscale.

Étapes de haut niveau :

1. Exécutez un serveur DNS sur l'hôte gateway (accessible via Tailnet).
2. Publiez des enregistrements DNS‑SD pour `_openclaw-gw._tcp` sous une zone dédiée
   (exemple : `openclaw.internal.`).
3. Configurez le **DNS fractionné** Tailscale pour que votre domaine choisi se résout via ce
   serveur DNS pour les clients (y compris iOS).

OpenClaw prend en charge n'importe quel domaine de découverte ; `openclaw.internal.` n'est qu'un exemple.
Les nœuds iOS/Android parcourent à la fois `local.` et votre domaine large zone configuré.

### Configuration Gateway (recommandée)

```json5
{
  gateway: { bind: "tailnet" }, // tailnet uniquement (recommandé)
  discovery: { wideArea: { enabled: true } }, // active la publication DNS-SD large zone
}
```

### Configuration du serveur DNS unique (hôte gateway)

```bash
openclaw dns setup --apply
```

Cela installe CoreDNS et le configure pour :

- écouter sur le port 53 uniquement sur les interfaces Tailscale de la gateway
- servir votre domaine choisi (exemple : `openclaw.internal.`) depuis `~/.openclaw/dns/<domain>.db`

Validez depuis une machine connectée à tailnet :

```bash
dns-sd -B _openclaw-gw._tcp openclaw.internal.
dig @<TAILNET_IPV4> -p 53 _openclaw-gw._tcp.openclaw.internal PTR +short
```

### Paramètres DNS Tailscale

Dans la console d'administration Tailscale :

- Ajoutez un serveur de noms pointant vers l'IP tailnet de la gateway (UDP/TCP 53).
- Ajoutez un DNS fractionné pour que votre domaine de découverte utilise ce serveur de noms.

Une fois que les clients acceptent le DNS tailnet, les nœuds iOS peuvent parcourir
`_openclaw-gw._tcp` dans votre domaine de découverte sans multicast.

### Sécurité de l'écouteur Gateway (recommandée)

Le port WS Gateway (par défaut `18789`) se lie à la boucle locale par défaut. Pour l'accès LAN/tailnet,
liez explicitement et gardez l'authentification activée.

Pour les configurations tailnet uniquement :

- Définissez `gateway.bind: "tailnet"` dans `~/.openclaw/openclaw.json`.
- Redémarrez la Gateway (ou redémarrez l'application de barre de menus macOS).

## Ce qui annonce

Seule la Gateway annonce `_openclaw-gw._tcp`.

## Types de service

- `_openclaw-gw._tcp` — balise de transport gateway (utilisée par les nœuds macOS/iOS/Android).

## Clés TXT (indices non secrets)

La Gateway annonce de petits indices non secrets pour rendre les flux d'interface utilisateur pratiques :

- `role=gateway`
- `displayName=<nom convivial>`
- `lanHost=<nom d'hôte>.local`
- `gatewayPort=<port>` (WS Gateway + HTTP)
- `gatewayTls=1` (uniquement quand TLS est activé)
- `gatewayTlsSha256=<sha256>` (uniquement quand TLS est activé et l'empreinte est disponible)
- `canvasPort=<port>` (uniquement quand l'hôte canvas est activé ; actuellement le même que `gatewayPort`)
- `sshPort=<port>` (par défaut 22 s'il n'est pas remplacé)
- `transport=gateway`
- `cliPath=<chemin>` (optionnel ; chemin absolu vers un point d'entrée `openclaw` exécutable)
- `tailnetDns=<magicdns>` (indice optionnel quand Tailnet est disponible)

Notes de sécurité :

- Les enregistrements TXT Bonjour/mDNS sont **non authentifiés**. Les clients ne doivent pas traiter TXT comme un routage faisant autorité.
- Les clients doivent router en utilisant le point de terminaison de service résolu (SRV + A/AAAA). Traitez `lanHost`, `tailnetDns`, `gatewayPort` et `gatewayTlsSha256` comme des indices uniquement.
- L'épinglage TLS ne doit jamais permettre à un `gatewayTlsSha256` annoncé de remplacer une épingle précédemment stockée.
- Les nœuds iOS/Android doivent traiter les connexions directes basées sur la découverte comme **TLS uniquement** et exiger une confirmation explicite de l'utilisateur avant de faire confiance à une empreinte pour la première fois.

## Débogage sur macOS

Outils intégrés utiles :

- Parcourir les instances :

  ```bash
  dns-sd -B _openclaw-gw._tcp local.
  ```

- Résoudre une instance (remplacez `<instance>`) :

  ```bash
  dns-sd -L "<instance>" _openclaw-gw._tcp local.
  ```

Si la navigation fonctionne mais que la résolution échoue, vous rencontrez généralement une politique LAN ou
un problème de résolveur mDNS.

## Débogage dans les journaux Gateway

La Gateway écrit un fichier journal roulant (imprimé au démarrage comme
`gateway log file: ...`). Recherchez les lignes `bonjour:`, en particulier :

- `bonjour: advertise failed ...`
- `bonjour: ... name conflict resolved` / `hostname conflict resolved`
- `bonjour: watchdog detected non-announced service ...`

## Débogage sur nœud iOS

Le nœud iOS utilise `NWBrowser` pour découvrir `_openclaw-gw._tcp`.

Pour capturer les journaux :

- Paramètres → Gateway → Avancé → **Journaux de débogage de découverte**
- Paramètres → Gateway → Avancé → **Journaux de découverte** → reproduire → **Copier**

Le journal inclut les transitions d'état du navigateur et les changements d'ensemble de résultats.

## Modes de défaillance courants

- **Bonjour ne traverse pas les réseaux** : utilisez Tailnet ou SSH.
- **Multicast bloqué** : certains réseaux Wi‑Fi désactivent mDNS.
- **Veille / changement d'interface** : macOS peut temporairement supprimer les résultats mDNS ; réessayez.
- **La navigation fonctionne mais la résolution échoue** : gardez les noms de machine simples (évitez les emojis ou
  la ponctuation), puis redémarrez la Gateway. Le nom d'instance de service dérive du
  nom d'hôte, donc les noms trop complexes peuvent confondre certains résolveurs.

## Noms d'instance échappés (`\032`)

Bonjour/DNS‑SD échappe souvent les octets dans les noms d'instance de service sous forme de séquences décimales `\DDD`
(par exemple, les espaces deviennent `\032`).

- C'est normal au niveau du protocole.
- Les interfaces utilisateur doivent décoder pour l'affichage (iOS utilise `BonjourEscapes.decode`).

## Désactivation / configuration

- `OPENCLAW_DISABLE_BONJOUR=1` désactive la publicité (héritage : `OPENCLAW_DISABLE_BONJOUR`).
- `gateway.bind` dans `~/.openclaw/openclaw.json` contrôle le mode de liaison Gateway.
- `OPENCLAW_SSH_PORT` remplace le port SSH annoncé dans TXT (héritage : `OPENCLAW_SSH_PORT`).
- `OPENCLAW_TAILNET_DNS` publie un indice MagicDNS dans TXT (héritage : `OPENCLAW_TAILNET_DNS`).
- `OPENCLAW_CLI_PATH` remplace le chemin CLI annoncé (héritage : `OPENCLAW_CLI_PATH`).

## Documents connexes

- Politique de découverte et sélection de transport : [Découverte](/gateway/discovery)
- Appairage de nœud + approbations : [Appairage Gateway](/gateway/pairing)
```
