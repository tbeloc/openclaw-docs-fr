---
summary: "Déléguer l'authentification de la passerelle à un proxy inverse de confiance (Pomerium, Caddy, nginx + OAuth)"
read_when:
  - Running OpenClaw behind an identity-aware proxy
  - Setting up Pomerium, Caddy, or nginx with OAuth in front of OpenClaw
  - Fixing WebSocket 1008 unauthorized errors with reverse proxy setups
  - Deciding where to set HSTS and other HTTP hardening headers
---

# Authentification par Proxy de Confiance

> ⚠️ **Fonctionnalité sensible sur le plan de la sécurité.** Ce mode délègue entièrement l'authentification à votre proxy inverse. Une mauvaise configuration peut exposer votre passerelle à des accès non autorisés. Lisez attentivement cette page avant d'activer.

## Quand l'utiliser

Utilisez le mode d'authentification `trusted-proxy` quand :

- Vous exécutez OpenClaw derrière un **proxy conscient de l'identité** (Pomerium, Caddy + OAuth, nginx + oauth2-proxy, Traefik + forward auth)
- Votre proxy gère toute l'authentification et transmet l'identité de l'utilisateur via des en-têtes
- Vous êtes dans un environnement Kubernetes ou conteneur où le proxy est le seul chemin d'accès à la passerelle
- Vous rencontrez des erreurs WebSocket `1008 unauthorized` parce que les navigateurs ne peuvent pas transmettre les jetons dans les charges utiles WS

## Quand NE PAS l'utiliser

- Si votre proxy n'authentifie pas les utilisateurs (juste un terminateur TLS ou un équilibreur de charge)
- S'il existe un chemin d'accès à la passerelle qui contourne le proxy (trous de pare-feu, accès réseau interne)
- Si vous n'êtes pas sûr que votre proxy supprime/réécrit correctement les en-têtes transférés
- Si vous n'avez besoin que d'un accès personnel pour un seul utilisateur (envisagez Tailscale Serve + loopback pour une configuration plus simple)

## Comment ça fonctionne

1. Votre proxy inverse authentifie les utilisateurs (OAuth, OIDC, SAML, etc.)
2. Le proxy ajoute un en-tête avec l'identité de l'utilisateur authentifié (par exemple, `x-forwarded-user: nick@example.com`)
3. OpenClaw vérifie que la demande provient d'une **IP de proxy de confiance** (configurée dans `gateway.trustedProxies`)
4. OpenClaw extrait l'identité de l'utilisateur de l'en-tête configuré
5. Si tout est correct, la demande est autorisée

## Comportement d'appairage de l'interface de contrôle

Quand `gateway.auth.mode = "trusted-proxy"` est actif et que la demande réussit
les vérifications du proxy de confiance, les sessions WebSocket de l'interface de contrôle peuvent se connecter sans identité d'appairage d'appareil.

Implications :

- L'appairage n'est plus la porte d'entrée principale pour l'accès à l'interface de contrôle dans ce mode.
- Votre politique d'authentification du proxy inverse et `allowUsers` deviennent le contrôle d'accès effectif.
- Gardez l'entrée de la passerelle verrouillée aux IPs du proxy de confiance uniquement (`gateway.trustedProxies` + pare-feu).

## Configuration

```json5
{
  gateway: {
    // Utilisez loopback pour les configurations de proxy sur le même hôte ; utilisez lan/custom pour les hôtes de proxy distants
    bind: "loopback",

    // CRITIQUE : Ajoutez uniquement les IP(s) de votre proxy ici
    trustedProxies: ["10.0.0.1", "172.17.0.1"],

    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        // En-tête contenant l'identité de l'utilisateur authentifié (obligatoire)
        userHeader: "x-forwarded-user",

        // Optionnel : en-têtes qui DOIVENT être présents (vérification du proxy)
        requiredHeaders: ["x-forwarded-proto", "x-forwarded-host"],

        // Optionnel : restreindre à des utilisateurs spécifiques (vide = autoriser tous)
        allowUsers: ["nick@example.com", "admin@company.org"],
      },
    },
  },
}
```

Si `gateway.bind` est `loopback`, incluez une adresse de proxy loopback dans
`gateway.trustedProxies` (`127.0.0.1`, `::1`, ou un CIDR loopback équivalent).

### Référence de Configuration

| Champ                                       | Obligatoire | Description                                                                 |
| ------------------------------------------- | -------- | --------------------------------------------------------------------------- |
| `gateway.trustedProxies`                    | Oui      | Tableau des adresses IP du proxy à faire confiance. Les demandes d'autres IPs sont rejetées. |
| `gateway.auth.mode`                         | Oui      | Doit être `"trusted-proxy"`                                                   |
| `gateway.auth.trustedProxy.userHeader`      | Oui      | Nom de l'en-tête contenant l'identité de l'utilisateur authentifié                      |
| `gateway.auth.trustedProxy.requiredHeaders` | Non       | En-têtes supplémentaires qui doivent être présents pour que la demande soit de confiance       |
| `gateway.auth.trustedProxy.allowUsers`      | Non       | Liste blanche des identités d'utilisateurs. Vide signifie autoriser tous les utilisateurs authentifiés.    |

## Terminaison TLS et HSTS

Utilisez un seul point de terminaison TLS et appliquez HSTS là.

### Modèle recommandé : terminaison TLS du proxy

Quand votre proxy inverse gère HTTPS pour `https://control.example.com`, définissez
`Strict-Transport-Security` au proxy pour ce domaine.

- Bon ajustement pour les déploiements accessibles sur Internet.
- Garde le certificat + la politique de durcissement HTTP au même endroit.
- OpenClaw peut rester sur HTTP loopback derrière le proxy.

Exemple de valeur d'en-tête :

```text
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### Terminaison TLS de la passerelle

Si OpenClaw lui-même sert HTTPS directement (pas de proxy terminant TLS), définissez :

```json5
{
  gateway: {
    tls: { enabled: true },
    http: {
      securityHeaders: {
        strictTransportSecurity: "max-age=31536000; includeSubDomains",
      },
    },
  },
}
```

`strictTransportSecurity` accepte une valeur d'en-tête de chaîne, ou `false` pour désactiver explicitement.

### Conseils de déploiement

- Commencez par un max age court d'abord (par exemple `max-age=300`) tout en validant le trafic.
- Augmentez à des valeurs longue durée (par exemple `max-age=31536000`) uniquement après une grande confiance.
- Ajoutez `includeSubDomains` uniquement si chaque sous-domaine est prêt pour HTTPS.
- Utilisez preload uniquement si vous répondez intentionnellement aux exigences de preload pour votre ensemble de domaines.
- Le développement local loopback uniquement ne bénéficie pas de HSTS.

## Exemples de Configuration de Proxy

### Pomerium

Pomerium transmet l'identité dans `x-pomerium-claim-email` (ou d'autres en-têtes de réclamation) et un JWT dans `x-pomerium-jwt-assertion`.

```json5
{
  gateway: {
    bind: "lan",
    trustedProxies: ["10.0.0.1"], // IP de Pomerium
    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        userHeader: "x-pomerium-claim-email",
        requiredHeaders: ["x-pomerium-jwt-assertion"],
      },
    },
  },
}
```

Extrait de configuration Pomerium :

```yaml
routes:
  - from: https://openclaw.example.com
    to: http://openclaw-gateway:18789
    policy:
      - allow:
          or:
            - email:
                is: nick@example.com
    pass_identity_headers: true
```

### Caddy avec OAuth

Caddy avec le plugin `caddy-security` peut authentifier les utilisateurs et transmettre les en-têtes d'identité.

```json5
{
  gateway: {
    bind: "lan",
    trustedProxies: ["127.0.0.1"], // IP de Caddy (si sur le même hôte)
    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        userHeader: "x-forwarded-user",
      },
    },
  },
}
```

Extrait de Caddyfile :

```
openclaw.example.com {
    authenticate with oauth2_provider
    authorize with policy1

    reverse_proxy openclaw:18789 {
        header_up X-Forwarded-User {http.auth.user.email}
    }
}
```

### nginx + oauth2-proxy

oauth2-proxy authentifie les utilisateurs et transmet l'identité dans `x-auth-request-email`.

```json5
{
  gateway: {
    bind: "lan",
    trustedProxies: ["10.0.0.1"], // IP de nginx/oauth2-proxy
    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        userHeader: "x-auth-request-email",
      },
    },
  },
}
```

Extrait de configuration nginx :

```nginx
location / {
    auth_request /oauth2/auth;
    auth_request_set $user $upstream_http_x_auth_request_email;

    proxy_pass http://openclaw:18789;
    proxy_set_header X-Auth-Request-Email $user;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### Traefik avec Forward Auth

```json5
{
  gateway: {
    bind: "lan",
    trustedProxies: ["172.17.0.1"], // IP du conteneur Traefik
    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        userHeader: "x-forwarded-user",
      },
    },
  },
}
```

## Liste de Contrôle de Sécurité

Avant d'activer l'authentification par proxy de confiance, vérifiez :

- [ ] **Le proxy est le seul chemin** : Le port de la passerelle est firewallé de tout sauf votre proxy
- [ ] **trustedProxies est minimal** : Uniquement vos IPs de proxy réelles, pas des sous-réseaux entiers
- [ ] **Le proxy supprime les en-têtes** : Votre proxy réécrit (ne pas ajouter) les en-têtes `x-forwarded-*` des clients
- [ ] **Terminaison TLS** : Votre proxy gère TLS ; les utilisateurs se connectent via HTTPS
- [ ] **allowUsers est défini** (recommandé) : Restreindre aux utilisateurs connus plutôt que d'autoriser quiconque authentifié

## Audit de Sécurité

`openclaw security audit` signalera l'authentification par proxy de confiance avec une constatation de sévérité **critique**. C'est intentionnel — c'est un rappel que vous déléguez la sécurité à votre configuration de proxy.

L'audit vérifie :

- Configuration `trustedProxies` manquante
- Configuration `userHeader` manquante
- `allowUsers` vide (autorise tout utilisateur authentifié)

## Dépannage

### "trusted_proxy_untrusted_source"

La demande ne provenait pas d'une IP dans `gateway.trustedProxies`. Vérifiez :

- L'IP du proxy est-elle correcte ? (Les IPs des conteneurs Docker peuvent changer)
- Y a-t-il un équilibreur de charge devant votre proxy ?
- Utilisez `docker inspect` ou `kubectl get pods -o wide` pour trouver les IPs réelles

### "trusted_proxy_user_missing"

L'en-tête utilisateur était vide ou manquant. Vérifiez :

- Votre proxy est-il configuré pour transmettre les en-têtes d'identité ?
- Le nom de l'en-tête est-il correct ? (insensible à la casse, mais l'orthographe compte)
- L'utilisateur est-il réellement authentifié au proxy ?

### "trusted_proxy_missing_header"

Un en-tête obligatoire n'était pas présent. Vérifiez :

- Votre configuration de proxy pour ces en-têtes spécifiques
- Si les en-têtes sont supprimés quelque part dans la chaîne

### "trusted_proxy_user_not_allowed"

L'utilisateur est authentifié mais pas dans `allowUsers`. Soit les ajouter, soit supprimer la liste blanche.

### WebSocket Toujours en Échec

Assurez-vous que votre proxy :

- Supporte les mises à niveau WebSocket (`Upgrade: websocket`, `Connection: upgrade`)
- Transmet les en-têtes d'identité sur les demandes de mise à niveau WebSocket (pas seulement HTTP)
- N'a pas de chemin d'authentification séparé pour les connexions WebSocket

## Migration depuis l'Authentification par Jeton

Si vous passez de l'authentification par jeton à l'authentification par proxy de confiance :

1. Configurez votre proxy pour authentifier les utilisateurs et transmettre les en-têtes
2. Testez la configuration du proxy indépendamment (curl avec en-têtes)
3. Mettez à jour la configuration OpenClaw avec l'authentification par proxy de confiance
4. Redémarrez la passerelle
5. Testez les connexions WebSocket depuis l'interface de contrôle
6. Exécutez `openclaw security audit` et examinez les constatations

## Connexes

- [Security](/fr/gateway/security) — guide de sécurité complet
- [Configuration](/fr/gateway/configuration) — référence de configuration
- [Remote Access](/fr/gateway/remote) — autres modèles d'accès à distance
- [Tailscale](/fr/gateway/tailscale) — alternative plus simple pour l'accès tailnet uniquement
