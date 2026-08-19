---
summary: "Publiez une Gateway loopback via un Cloudflare Tunnel et authentifiez chaque client avec Cloudflare Access"
read_when:
  - You want a public HTTPS Gateway URL without opening a port
  - You want Cloudflare Access (SSO) to authenticate the Control UI
  - Your CLI, TUI, or nodes get HTTP 302 from a Cloudflare-fronted Gateway
title: "Cloudflare Tunnel et Access"
---

Exécutez la Gateway sur loopback, publiez-la via un Cloudflare Tunnel, et laissez Cloudflare
Access authentifier chaque requête avant qu'elle n'atteigne OpenClaw. La Gateway conserve
`gateway.bind: "loopback"`, donc aucun port n'est exposé et aucune règle de pare-feu entrante n'est
nécessaire ; `cloudflared` établit une connexion sortante depuis l'hôte.

C'est l'une des topologies d'accès à distance supportées aux côtés de [Tailscale](/fr/gateway/tailscale)
et d'un [tunnel SSH](/fr/gateway/remote#ssh-tunnel-cli--tools). Choisissez-la quand vous voulez une
URL HTTPS publique stable et une authentification SSO du fournisseur d'identité devant l'interface de contrôle.

## Avant de commencer

- Un compte Cloudflare avec la zone pour votre nom d'hôte, et Cloudflare Zero Trust activé.
- `cloudflared` installé sur l'hôte Gateway, et sur toute machine qui utilisera la CLI.
- Une Gateway en cours d'exécution sur `127.0.0.1:18789` avec `gateway.bind: "loopback"`.
- Une familiarité avec [l'authentification par proxy de confiance](/fr/gateway/trusted-proxy-auth), que cette topologie utilise.

## Comment les pièces s'assemblent

```text
navigateur / CLI / nœud  ->  Cloudflare Access (identité)  ->  Tunnel  ->  127.0.0.1:18789
```

Access authentifie la requête et injecte les en-têtes d'identité. La Gateway ne
réauthentifie pas la personne ni ne vérifie la signature JWT d'Access ; elle vérifie la
source du proxy de confiance et la présence de l'en-tête configuré, puis fait confiance à l'en-tête utilisateur. Parce que
`allowLoopback` permet également à d'autres processus locaux de présenter ces en-têtes, gardez le port Gateway privé à l'hôte et exécutez uniquement des charges de travail de confiance là-bas.

## Étape 1 : Acheminer le tunnel vers loopback

Ajoutez une règle d'entrée mappant votre nom d'hôte au port Gateway, puis exécutez `cloudflared`
en tant que service sur l'hôte Gateway :

```yaml
tunnel: <tunnel-id>
credentials-file: /root/.cloudflared/<tunnel-id>.json
ingress:
  - hostname: gateway.example
    service: http://localhost:18789
  - service: http_status:404
```

Consultez la documentation de Cloudflare pour créer le tunnel et l'enregistrement DNS.

## Étape 2 : Protéger le nom d'hôte avec Access

Créez une application Access pour `gateway.example` avec une politique qui autorise vos
utilisateurs. Notez les deux en-têtes qu'Access ajoute aux requêtes authentifiées, car la Gateway
les consomme à l'étape suivante :

- `cf-access-authenticated-user-email` — l'identité authentifiée.
- `cf-access-jwt-assertion` — l'assertion signée d'Access. OpenClaw vérifie uniquement que cet
  en-tête est présent et non vide ; il ne vérifie pas la signature JWT.

## Étape 3 : Faire confiance à ces en-têtes dans la Gateway

Définissez `gateway.auth.mode` sur `trusted-proxy` et nommez les en-têtes Access. `allowLoopback`
est requis ici : `cloudflared` se connecte depuis `127.0.0.1`, et l'authentification par proxy de confiance
attend autrement un proxy non-loopback.

```json5
{
  gateway: {
    bind: "loopback",
    trustedProxies: ["127.0.0.1", "::1"],
    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        userHeader: "cf-access-authenticated-user-email",
        requiredHeaders: ["cf-access-jwt-assertion"],
        allowLoopback: true,
      },
    },
  },
}
```

Exiger `cf-access-jwt-assertion` ajoute une deuxième vérification de présence, pas une
vérification cryptographique. Un processus local qui peut se connecter à la Gateway peut soumettre les deux en-têtes,
donc ne traitez pas ce paramètre comme une défense contre le code local non fiable. La limite de sécurité
est le port loopback verrouillé plus Cloudflare Access et le tunnel étant
le seul chemin pour le trafic externe.

## Étape 4 : Décider comment les nœuds et les workers entrent

Access protège chaque route sur le nom d'hôte, y compris celles que les nœuds utilisent. Choisissez l'une :

- **Exempter les routes auto-authentifiantes.** Autorisez `/j/*` et `/__openclaw__/worker`
  sans identité Access, et gardez la mise à niveau WebSocket activée sur la route worker. Les deux
  appliquent leurs propres identifiants de courte durée, donc ils ne dépendent pas d'Access. Voir
  [Nœuds](/fr/nodes#edge-routing).
- **Utiliser un jeton de service Access.** Ajoutez une politique Service Auth et donnez au nœud
  `gateway.cloudflareAccess.clientId` / `clientSecret`. Voir [CLI Nœud](/fr/cli/node).

Si vous ne faites ni l'un ni l'autre, `openclaw connect` échoue contre le tunnel même si le navigateur
fonctionne, car la requête de jointure est redirigée vers la page de connexion Access.

## Étape 5 : Connecter chaque client

**Interface de contrôle.** Ouvrez `https://gateway.example` et connectez-vous via Access. Avec
l'authentification par proxy de confiance, la Gateway mappe votre identité Access à une session d'opérateur.

**CLI et TUI.** Ceux-ci ne portent pas de cookies de navigateur, donc ils présentent un jeton Access sur
la mise à niveau WebSocket. Configurez `gateway.remote.edgeAuth` comme décrit dans
[Accès à distance](/fr/gateway/remote#gateway-behind-an-identity-aware-proxy), puis exécutez
`cloudflared access login https://gateway.example` une fois pour mettre en cache un jeton.

**Nœuds.** Suivez le choix fait à l'étape 4.

## Vérifier

```bash
openclaw tui
```

Attendez-vous à ce que le TUI atteigne `wss://gateway.example` et affiche `connected`. Une première
connexion peut signaler `device pairing required` ; approuvez-la dans l'interface de contrôle sous
Paramètres → Appareils, ou exécutez `openclaw devices approve --latest` sur l'hôte Gateway.

Atteindre l'invite d'appairage propre de la Gateway est en soi la preuve qu'Access a été
satisfait — une requête non authentifiée n'arrive jamais jusque-là.

## Préparation pour la production

- Gardez `gateway.bind: "loopback"`. Lier plus largement réexpose la Gateway à côté du
  tunnel et contourne complètement Access.
- Gardez `trustedProxies` limité à loopback. C'est la liste des adresses dont les en-têtes d'identité
  la Gateway croira.
- `trustedProxy.deviceAutoApprove` peut appairer les appareils automatiquement pour les
  identités authentifiées par Access. Cela supprime une étape d'approbation manuelle ; activez-le uniquement
  quand vous acceptez que quiconque passe Access obtient un appareil appairé avec les portées que vous
  listez.
- Les jetons Access expirent selon la durée de session de l'application. Attendez-vous à ce que les utilisateurs CLI réexécutent
  `cloudflared access login` quand leur jeton expire.

## Dépannage

| Symptôme                                                             | Cause et solution                                                                                                                                     |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gateway rejected websocket upgrade (HTTP 302)` de la CLI ou TUI | Access a intercepté la mise à niveau. Configurez `gateway.remote.edgeAuth` ; voir [Accès à distance](/fr/gateway/remote#gateway-behind-an-identity-aware-proxy). |
| Le navigateur fonctionne, `openclaw connect` échoue                             | Les routes des nœuds sont toujours derrière Access. Appliquez l'une des options de l'étape 4.                                                                          |
| `Exec provider ... exited with code 1`                              | Le fournisseur de secret exec s'exécute avec un environnement nettoyé ; `cloudflared` a besoin de `passEnv: ["HOME"]` pour lire son jeton en cache.                      |
| `secrets.providers.*.command must not be a symlink`                 | Pointez `command` vers le binaire résolu, pas un lien symbolique du gestionnaire de paquets.                                                                            |
| La Gateway démarre mais chaque requête est anonyme                       | `allowLoopback` n'est pas défini, donc les en-têtes du `cloudflared` local sont ignorés.                                                                    |

## Connexes

- [Accès à distance](/fr/gateway/remote)
- [Authentification par proxy de confiance](/fr/gateway/trusted-proxy-auth)
- [Nœuds](/fr/nodes)
- [Tailscale](/fr/gateway/tailscale)
- [Authentification](/fr/gateway/authentication)
