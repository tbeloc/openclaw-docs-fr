```markdown
---
read_when:
  - 在 macOS/iOS 上调试 Bonjour 设备发现问题时
  - 更改 mDNS 服务类型、TXT 记录或设备发现用户体验时
summary: Bonjour/mDNS 设备发现 + 调试（Gateway 网关信标、客户端和常见故障模式）
title: Bonjour 设备发现
x-i18n:
  generated_at: "2026-02-03T07:47:48Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 47569da55f0c0523bd5ff05275dc95ccb52f75638193cfbdb4eaaa162aadf08c
  source_path: gateway/bonjour.md
  workflow: 15
---

# Découverte de périphériques Bonjour / mDNS

OpenClaw utilise Bonjour (mDNS / DNS‑SD) comme **moyen pratique limité au réseau local** pour découvrir
les passerelles Gateway actives (points de terminaison WebSocket). C'est un effort au mieux, et **ne peut pas**
remplacer les connexions SSH ou basées sur Tailnet.

## Bonjour à grande distance via Tailscale (DNS‑SD monodiffusion)

Si le nœud et la passerelle Gateway se trouvent sur des réseaux différents, le mDNS multidiffusion ne peut pas
traverser les limites. Vous pouvez maintenir la même expérience de découverte de périphériques en basculant vers
**DNS‑SD monodiffusion** basé sur Tailscale (« Bonjour à grande distance »).

Étapes récapitulatives :

1. Exécutez un serveur DNS sur l'hôte de la passerelle Gateway (accessible via Tailnet).
2. Publiez les enregistrements DNS‑SD pour `_openclaw-gw._tcp` sous une zone privée
   (exemple : `openclaw.internal.`).
3. Configurez le **DNS fractionné** de Tailscale pour que le nom de domaine que vous choisissez soit résolu
   par ce serveur DNS pour les clients (y compris iOS).

OpenClaw prend en charge n'importe quel nom de domaine de découverte ; `openclaw.internal.` n'est qu'un exemple.
Les nœuds iOS/Android parcourent à la fois `local.` et le domaine à grande distance que vous configurez.

### Configuration de la passerelle Gateway (recommandée)

```json5
{
  gateway: { bind: "tailnet" }, // tailnet uniquement (recommandé)
  discovery: { wideArea: { enabled: true } }, // activer la publication DNS-SD à grande distance
}
```

### Configuration du serveur DNS unique (hôte de la passerelle Gateway)

```bash
openclaw dns setup --apply
```

Cela installe CoreDNS et le configure pour :

- Écouter le port 53 uniquement sur l'interface Tailscale de la passerelle Gateway
- Servir le domaine que vous choisissez à partir de `~/.openclaw/dns/<domain>.db` (exemple : `openclaw.internal.`)

Vérifiez à partir d'une machine connectée à Tailnet :

```bash
dns-sd -B _openclaw-gw._tcp openclaw.internal.
dig @<TAILNET_IPV4> -p 53 _openclaw-gw._tcp.openclaw.internal PTR +short
```

### Configuration DNS de Tailscale

Dans la console d'administration Tailscale :

- Ajoutez un serveur de noms pointant vers l'adresse IP Tailnet de la passerelle Gateway (UDP/TCP 53).
- Ajoutez un DNS fractionné pour que votre domaine de découverte utilise ce serveur de noms.

Une fois que le client accepte le DNS Tailnet, le nœud iOS peut parcourir `_openclaw-gw._tcp` dans
votre domaine de découverte sans multidiffusion.

### Sécurité de l'écouteur de la passerelle Gateway (recommandée)

Le port WS de la passerelle Gateway (par défaut `18789`) est lié par défaut à la boucle locale. Pour l'accès
au réseau local/Tailnet, liez explicitement et maintenez l'authentification activée.

Pour une configuration Tailnet uniquement :

- Définissez `gateway.bind: "tailnet"` dans `~/.openclaw/openclaw.json`.
- Redémarrez la passerelle Gateway (ou redémarrez l'application de la barre de menus macOS).

## Ce qui est diffusé

Seule la passerelle Gateway diffuse `_openclaw-gw._tcp`.

## Types de services

- `_openclaw-gw._tcp` — Balise de transport de la passerelle Gateway (utilisée par les nœuds macOS/iOS/Android).

## Clés TXT (conseils non confidentiels)

La passerelle Gateway diffuse de petits conseils non confidentiels pour faciliter les flux d'interface utilisateur :

- `role=gateway`
- `displayName=<nom convivial>`
- `lanHost=<hostname>.local`
- `gatewayPort=<port>` (WS + HTTP de la passerelle Gateway)
- `gatewayTls=1` (uniquement si TLS est activé)
- `gatewayTlsSha256=<sha256>` (uniquement si TLS est activé et l'empreinte disponible)
- `canvasPort=<port>` (uniquement si l'hôte de canevas est activé ; par défaut `18793`)
- `sshPort=<port>` (par défaut 22 si non remplacé)
- `transport=gateway`
- `cliPath=<path>` (optionnel ; chemin absolu vers le point d'entrée `openclaw` exécutable)
- `tailnetDns=<magicdns>` (conseil optionnel quand Tailnet est disponible)

## Débogage sur macOS

Outils intégrés utiles :

- Parcourir les instances :
  ```bash
  dns-sd -B _openclaw-gw._tcp local.
  ```
- Résoudre une instance individuelle (remplacez `<instance>`) :
  ```bash
  dns-sd -L "<instance>" _openclaw-gw._tcp local.
  ```

Si la navigation fonctionne mais que la résolution échoue, vous rencontrez généralement une politique de réseau local ou
un problème de résolveur mDNS.

## Débogage dans les journaux de la passerelle Gateway

La passerelle Gateway écrit dans un fichier journal roulant (imprimé au démarrage sous la forme
`gateway log file: ...`). Recherchez les lignes `bonjour:`, en particulier :

- `bonjour: advertise failed ...`
- `bonjour: ... name conflict resolved` / `hostname conflict resolved`
- `bonjour: watchdog detected non-announced service ...`

## Débogage sur un nœud iOS

Le nœud iOS utilise `NWBrowser` pour découvrir `_openclaw-gw._tcp`.

Pour capturer les journaux :

- Paramètres → Passerelle Gateway → Avancé → **Discovery Debug Logs**
- Paramètres → Passerelle Gateway → Avancé → **Discovery Logs** → Reproduire → **Copy**

Les journaux incluent les transitions d'état du navigateur et les changements d'ensemble de résultats.

## Modes de défaillance courants

- **Bonjour ne traverse pas les réseaux** : Utilisez Tailnet ou SSH.
- **Multidiffusion bloquée** : Certains réseaux Wi‑Fi désactivent mDNS.
- **Veille / changements d'interface** : macOS peut temporairement supprimer les résultats mDNS ; réessayez.
- **Navigation fonctionne mais résolution échoue** : Gardez les noms de machines simples (évitez les emojis ou
  la ponctuation), puis redémarrez la passerelle Gateway. Le nom d'instance de service provient du
  nom d'hôte, donc les noms trop complexes peuvent confondre certains résolveurs.

## Noms d'instances échappés (`\032`)

Bonjour/DNS‑SD échappe souvent les octets dans les noms d'instances de service en tant que séquences décimales `\DDD`
(par exemple, l'espace devient `\032`).

- C'est normal au niveau du protocole.
- L'interface utilisateur doit décoder pour l'affichage (iOS utilise `BonjourEscapes.decode`).

## Désactivation / Configuration

- `OPENCLAW_DISABLE_BONJOUR=1` désactive la diffusion (hérité : `OPENCLAW_DISABLE_BONJOUR`).
- `gateway.bind` dans `~/.openclaw/openclaw.json` contrôle le mode de liaison de la passerelle Gateway.
- `OPENCLAW_SSH_PORT` remplace le port SSH diffusé dans TXT (hérité : `OPENCLAW_SSH_PORT`).
- `OPENCLAW_TAILNET_DNS` publie un conseil MagicDNS dans TXT (hérité : `OPENCLAW_TAILNET_DNS`).
- `OPENCLAW_CLI_PATH` remplace le chemin CLI diffusé (hérité : `OPENCLAW_CLI_PATH`).

## Documentation connexe

- Stratégie de découverte de périphériques et sélection de transport : [Découverte de périphériques](/gateway/discovery)
- Appairage de nœuds + approbation : [Appairage de la passerelle Gateway](/gateway/pairing)
```
