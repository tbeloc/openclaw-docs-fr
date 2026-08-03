---
summary: "Donnez à une Gateway en loopback uniquement une URL HTTPS stable réservée au tailnet avec Tailscale Serve"
read_when:
  - Replacing per-client SSH tunnels with one private Gateway URL
  - Connecting macOS, iOS, or Android clients to a remote Gateway
  - Diagnosing a Tailscale Serve URL that works locally but times out remotely
title: "Donnez à votre Gateway une URL HTTPS stable"
---

Tailscale Serve donne à votre Gateway une URL HTTPS sans exposer le port de la Gateway sur votre LAN ou sur l'internet public. La Gateway continue d'écouter sur loopback, tandis que Tailscale termine la connexion HTTPS avec un certificat valide et envoie les requêtes par proxy vers celle-ci.

Le résultat est `https://<host>.<tailnet>.ts.net`, accessible depuis les appareils autorisés sur votre tailnet et non depuis l'internet public. L'URL WebSocket correspondante est `wss://<host>.<tailnet>.ts.net`.

Si vous avez besoin d'une URL publique, utilisez plutôt [Tailscale Funnel](/fr/gateway/tailscale#public-internet-funnel-shared-password). Funnel est public, et OpenClaw nécessite une authentification par mot de passe pour celui-ci.

## Avant de commencer

Vous avez besoin de :

- [MagicDNS](https://tailscale.com/docs/features/magicdns) activé pour votre tailnet.
- [Certificats HTTPS](https://tailscale.com/docs/how-to/set-up-https-certificates) activés dans la console d'administration Tailscale sous **DNS > HTTPS Certificates**.
- Tailscale installé et connecté sur l'hôte Gateway.
- La Gateway déjà configurée avec une authentification par token, mot de passe ou trusted-proxy. Serve ne peut pas être combiné avec `gateway.auth.mode: "none"`.

OpenClaw localise automatiquement la CLI Tailscale. Il vérifie `tailscale` sur `PATH`, le bundle d'application macOS à `/Applications/Tailscale.app/Contents/MacOS/Tailscale`, les autres installations d'applications correspondantes sous `/Applications`, et la base de données locate du système. Vous n'avez pas besoin d'ajouter le binaire du bundle d'application macOS à `PATH`.

## 1. Activez Serve tout en conservant la liaison loopback

Exécutez ces commandes sur l'hôte Gateway :

```bash
openclaw config set gateway.bind loopback
openclaw config set gateway.tailscale.mode serve
openclaw gateway restart
```

La configuration équivalente est :

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: {
      mode: "serve",
    },
  },
}
```

OpenClaw configure Tailscale pour servir HTTPS sur le port `443` et envoyer par proxy vers le port Gateway, qui est `18789` par défaut. La Gateway elle-même reste sur `127.0.0.1:<port>`.

### Authentification par en-tête d'identité optionnelle

Pour autoriser explicitement les en-têtes d'identité Tailscale pour l'authentification WebSocket de l'interface de contrôle :

```bash
openclaw config set gateway.auth.allowTailscale true
```

Pour Serve avec authentification par token, OpenClaw active ce comportement par défaut sauf si vous le définissez sur `false`. Les modes authentification par mot de passe et trusted-proxy conservent leur limite d'authentification explicite sauf si vous acceptez.

Ce paramètre permet à une identité Tailscale vérifiée de satisfaire la vérification du secret partagé WebSocket de l'interface de contrôle. OpenClaw vérifie l'adresse du client transférée avec `tailscale whois` et la fait correspondre à l'en-tête `tailscale-user-login`. Il s'applique uniquement lorsque la requête arrive de loopback via Serve avec les en-têtes transférés attendus.

Il n'authentifie pas les points de terminaison de l'API HTTP, ne supprime pas les exigences d'identité de l'appareil du navigateur, n'authentifie pas les connexions de rôle de nœud et ne contourne pas l'appairage de nœud. Voir [En-têtes d'identité Tailscale](/fr/gateway/tailscale#tailscale-identity-headers-serve-only) pour le contrat complet.

## 2. Autorisez HTTPS dans votre politique tailnet

Les contrôles d'accès Tailscale s'appliquent à Serve. Si votre tailnet a une politique restrictive, autorisez les appareils clients à atteindre l'hôte Gateway sur le port TCP `443`.

Sans cette autorisation, l'URL Serve peut fonctionner sur l'hôte Gateway mais expirer silencieusement depuis tous les autres appareils. Ce symptôme ressemble à une Gateway cassée même si la politique tailnet bloque la connexion.

Utilisez le formulaire qui correspond à votre fichier de politique tailnet.

### Politique des grants modernes

Ajoutez cet objet au tableau `grants` existant :

```json
{
  "src": ["autogroup:member"],
  "dst": ["<gateway-host-or-ip>"],
  "ip": ["tcp:443"]
}
```

Par exemple, remplacez `<gateway-host-or-ip>` par un alias d'hôte défini dans votre politique, tel que `gateway-host`, ou par une adresse telle que `100.x.y.z`.

### Politique ACL plus ancienne

Ajoutez cet objet au tableau `acls` existant :

```json
{
  "action": "accept",
  "src": ["autogroup:member"],
  "dst": ["<gateway-host-or-ip>:443"]
}
```

`autogroup:member` autorise tous les membres authentifiés du tailnet. Pour une politique plus stricte, remplacez-le par un sélecteur d'utilisateur, de groupe, de tag ou d'appareil plus étroit qui couvre uniquement les clients qui ont besoin d'accès à la Gateway. Voir la documentation Tailscale pour [grants](https://tailscale.com/docs/features/access-control/grants) et [ACLs](https://tailscale.com/docs/features/access-control/acls).

## 3. Vérifiez la route et la limite loopback

Sur l'hôte Gateway, confirmez que Serve est actif :

```bash
tailscale serve status
```

La sortie doit afficher une route HTTPS pour `https://<host>.<tailnet>.ts.net` envoyant par proxy vers le port Gateway.

Depuis un autre appareil sur le même tailnet, vérifiez la réponse HTTPS :

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://<host>.<tailnet>.ts.net/
```

Attendez `200` pour la racine de l'interface de contrôle. Si cette requête expire mais que la même commande retourne `200` sur l'hôte Gateway, vérifiez d'abord l'autorisation TCP `443` de l'étape précédente.

Enfin, prouvez que le processus Gateway n'a pas ouvert son propre port au réseau :

```bash
lsof -nP -iTCP:<port> -sTCP:LISTEN
```

Pour le port par défaut, remplacez `<port>` par `18789`. L'écouteur Gateway doit être sur `127.0.0.1:<port>`, pas sur `0.0.0.0:<port>` ou une adresse LAN ou tailnet. Tailscale possède l'écouteur HTTPS et le chemin du proxy.

## 4. Utilisez l'URL depuis les clients

### Application macOS

Dans l'application OpenClaw macOS :

1. Ouvrez **Settings > Connection**.
2. Définissez **OpenClaw runs** sur **Remote (another host)**.
3. Définissez **Transport** sur **Direct (ws/wss)**.
4. Entrez `wss://<host>.<tailnet>.ts.net` dans **Gateway URL**.
5. Sélectionnez **Test remote**.

L'application se connecte maintenant directement via Tailscale Serve, le tunnel SSH par client n'est donc plus nécessaire.

### Applications compagnon iOS et Android

Les applications iOS et Android se connectent directement au WebSocket Gateway et ne gèrent pas un transport de tunnel SSH. Utilisez le même point de terminaison `wss://<host>.<tailnet>.ts.net` lors de l'appairage ou de la génération d'un code de configuration. Cela donne aux clients mobiles un itinéraire sécurisé qu'ils peuvent utiliser de n'importe où sur le tailnet.

Voir [Configuration de l'application iOS](/fr/platforms/ios) et [Configuration de la connexion Android](/fr/platforms/android#connection-runbook) pour leurs étapes d'appairage.

## Nom de vanité stable optionnel

Pour utiliser un nom de service Tailscale au lieu du nom d'hôte de l'appareil Gateway :

```bash
openclaw config set gateway.tailscale.serviceName svc:openclaw
openclaw gateway restart
```

Cela publie `https://openclaw.<tailnet>.ts.net`. L'hôte Gateway doit être un nœud tagué approuvé, et le Service peut nécessiter une approbation de la console d'administration avant que Serve puisse le publier. Voir [Services Tailscale](/fr/gateway/tailscale#tailnet-only-serve) pour les contraintes de configuration complètes.

## Dépannage

### L'URL expire depuis d'autres appareils

Exécutez la même commande `curl` sur l'hôte Gateway. Si l'hôte retourne `200` tandis que les autres appareils tailnet expirent, ajoutez ou réduisez l'autorisation de politique tailnet pour TCP `443`.

### Le certificat n'est pas émis ou la première requête est lente

Confirmez que MagicDNS et les certificats HTTPS sont activés dans la console d'administration Tailscale. L'émission initiale du certificat peut rendre la première requête HTTPS plus lente ; laissez-la se terminer, puis réessayez.

### La commande serve n'est pas disponible

Mettez à jour Tailscale et confirmez que votre build client installé expose la commande `tailscale serve` actuelle. La CLI Serve a changé dans Tailscale 1.52. Voir la [référence de commande Tailscale Serve](https://tailscale.com/docs/reference/tailscale-cli/serve).

### Les en-têtes d'identité Tailscale ne sont pas acceptés

Confirmez que `gateway.auth.allowTailscale` est `true` et que la requête arrive via l'URL Serve. Les requêtes loopback directes, LAN, IP tailnet brute et proxy inverse personnalisé ne sont pas admissibles pour l'authentification par en-tête d'identité Tailscale.

## Connexes

- [Référence Tailscale](/fr/gateway/tailscale)
- [Accès à distance](/fr/gateway/remote)
- [Authentification Gateway](/fr/gateway/authentication)
