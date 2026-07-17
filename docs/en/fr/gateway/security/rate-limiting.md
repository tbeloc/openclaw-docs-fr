---
summary: "Référence pour chaque limite de débit de la Gateway : verrouillages pré-authentification, limitation des navigateurs et webhooks, le backstop d'écriture du plan de contrôle, les plafonds de sessions ACP et le délai de redémarrage"
read_when:
  - A client sees `rate limit exceeded for <method>`, `AUTH_RATE_LIMITED`, or lockout errors
  - You want to tune `gateway.auth.rateLimit`
  - You are reasoning about brute-force protection on an exposed Gateway
  - You need to know which Gateway surfaces are throttled, at what limits
title: "Limitation de débit"
---

La Gateway applique plusieurs limites de débit indépendantes. Elles protègent différentes
frontières, utilisent des clés basées sur différentes identités et échouent avec différentes formes d'erreur.
Cette page est la référence pour toutes les limites.

En un coup d'œil :

| Surface                             | Limite (par défaut)              | Clé basée sur                    | Configurable             |
| ----------------------------------- | -------------------------------- | -------------------------------- | ------------------------ |
| Authentification échouée (token/mot de passe/appareil) | 10 échecs / 60s, verrouillage 5 min | IP + portée des identifiants | `gateway.auth.rateLimit` |
| Échecs d'authentification WS d'origine navigateur | identique, loopback **non** exempté | IP, ou origine de page depuis loopback | `gateway.auth.rateLimit` |
| Authentification webhook (`/hooks`) échouée | 20 échecs / 60s, verrouillage 60s | IP | non |
| RPC d'écriture du plan de contrôle | 30 requêtes / 60s par méthode | méthode + appareil + IP | non |
| Création de session ACP | 120 sessions / 10s | instance de traducteur | interne |
| Cycles de redémarrage de Gateway | Délai de 30s entre les redémarrages | processus | non |

## Tentatives d'authentification (pré-authentification)

Les tentatives d'authentification échouées sont limitées par IP client, avant tout
traitement de requête. C'est la protection contre les attaques par force brute pour les Gateways exposées.

- Seules les identifiants _incorrects_ comptent. Les identifiants manquants (un client qui n'a jamais
  envoyé de token) et les authentifications réussies ne consomment pas le budget ; une
  authentification réussie réinitialise le compteur pour cette IP.
- Valeurs par défaut : 10 échecs par 60 secondes, puis un verrouillage de 5 minutes pour cette IP.
- Loopback (`127.0.0.1` / `::1`) est exempté par défaut pour que les sessions CLI locales
  ne puissent pas être verrouillées.
- Les compteurs sont limités par classe d'identifiants, donc une inondation contre une surface
  ne déplace pas une autre. Les portées incluent le token/mot de passe partagé de la gateway,
  les tokens d'appareil, l'appairage de nœud, la réapprobation de nœud apparié,
  les tokens d'amorçage d'appareil et l'émission de défi watchOS.

Pendant le verrouillage, les tentatives de connexion échouent avec :

```json
{
  "code": "INVALID_REQUEST",
  "message": "unauthorized: too many failed authentication attempts (retry later)",
  "retryable": true,
  "retryAfterMs": 297000,
  "details": {
    "code": "AUTH_RATE_LIMITED",
    "authReason": "rate_limited",
    "recommendedNextStep": "wait_then_retry"
  }
}
```

Les tentatives d'autres IP (y compris loopback) ne sont pas affectées pendant un verrouillage.

Configurez-le sous `gateway.auth.rateLimit` dans `openclaw.json` :

```json
{
  "gateway": {
    "auth": {
      "rateLimit": {
        "maxAttempts": 10,
        "windowMs": 60000,
        "lockoutMs": 300000,
        "exemptLoopback": true
      }
    }
  }
}
```

Les entrées `AUTH_RATE_LIMITED` répétées dans le journal de la Gateway signifient que quelqu'un
essaie de deviner les identifiants ; voir le [runbook d'exposition](/fr/gateway/security/exposure-runbook).

### Connexions d'origine navigateur

Les connexions WebSocket qui portent un en-tête `Origin` de navigateur utilisent les mêmes
limites mais avec l'exemption loopback **toujours désactivée** — une page malveillante dans
un navigateur local est toujours un client non fiable, donc localhost n'obtient pas de passe gratuit
sur ce chemin. Quand une telle connexion arrive _depuis_ une adresse loopback, ses
échecs sont clés par l'origine de page normalisée (par exemple
`browser-origin:https://evil.example`) plutôt que l'IP loopback partagée,
donc chaque origine obtient son propre bucket ; depuis des adresses non-loopback la clé
reste l'IP du client. Ceci n'est pas configurable.

### Webhooks

L'ingress HTTP `/hooks` a son propre limiteur d'échec : 20 authentifications échouées
par 60 secondes par IP client, puis un verrouillage de 60 secondes.
Loopback n'est pas exempté. Une authentification webhook réussie réinitialise le compteur. Les requêtes limitées reçoivent un simple HTTP `429 Too Many Requests` avec un en-tête `Retry-After` (secondes). Les limites sont fixes ; si une intégration légitime déclenche ceci,
corrigez ses identifiants plutôt que de réessayer plus fort.

## Écritures du plan de contrôle (backstop post-authentification)

Les RPC d'administration côté écriture (`config.apply`, `config.patch`, `plugins.install`,
`plugins.setEnabled`, `plugins.uninstall`, `update.run`, `worktrees.*`,
`gateway.restart.request`, ...) sont en outre limités en débit **après**
autorisation : 30 requêtes par 60 secondes, par méthode, par
`deviceId+clientIp`.

Ce n'est pas une frontière de sécurité — les appelants détiennent déjà `operator.admin` — c'est
un backstop qui limite les boucles de client ou d'agent qui s'emballent en martelant des opérations coûteuses. L'utilisation interactive ne le déclenche jamais ; chaque méthode a son propre bucket, donc
basculer un plugin ne consomme pas le budget des écritures de configuration.

Quand dépassé, la requête échoue avec une erreur réessayable :

```json
{
  "code": "UNAVAILABLE",
  "message": "rate limit exceeded for config.patch; retry after 35s",
  "retryable": true,
  "retryAfterMs": 34539,
  "details": { "method": "config.patch", "limit": "30 per 60s" }
}
```

Les clients doivent respecter `retryAfterMs`. La limite est fixe (non configurable) ;
les buckets expirent d'eux-mêmes et sont purgés par la maintenance de la Gateway.

## Création de session ACP

Le traducteur ACP plafonne la création de session à 120 nouvelles sessions par fenêtre de 10 secondes par instance de traducteur. Le dépassement échoue la requête avec une erreur dont le message porte le temps d'attente (il n'y a pas de champ structuré `retryAfterMs`
sur ce chemin) :

```
ACP session creation rate limit exceeded for <method>; retry after <n>s.
```

Cela limite les clients qui s'emballent et créent des sessions en boucle ; l'utilisation normale d'IDE et d'agent reste bien en dessous.

## Délai de redémarrage

Les requêtes de redémarrage de Gateway se fusionnent, puis appliquent un délai de 30 secondes entre les cycles de redémarrage. Un redémarrage demandé pendant le délai est planifié après son expiration plutôt que rejeté. C'est séparé du limiteur du plan de contrôle ci-dessus : `gateway.restart.request` consomme un slot de budget du plan de contrôle _et_
le redémarrage résultant obéit au délai.

## Notes opérationnelles

- Tous les limiteurs sont en mémoire et par processus, et plusieurs Gateways ne
  partagent pas l'état. Remplacer le processus Gateway efface les compteurs appartenant à la Gateway (verrouillages d'authentification, limitation webhook, buckets du plan de contrôle). Le délai de redémarrage survit intentionnellement aux cycles de redémarrage en processus — c'est ce qu'il limite — et se réinitialise uniquement avec le processus. Le plafond de session ACP appartient à son instance de traducteur et se réinitialise quand cette instance est recréée, pas au redémarrage de la Gateway.
- Les cartes de buckets sont bornées (plafonds d'entrée durs plus élagage périodique), donc
  les inondations de clés uniques ne peuvent pas faire croître la mémoire sans limite.
- Quand un client est derrière un proxy inverse, l'IP effective est l'IP client résolue ; voir [authentification de proxy de confiance](/fr/gateway/trusted-proxy-auth) pour savoir comment les en-têtes de proxy sont validés avant de pouvoir l'influencer.
- La signalisation de nouvelle tentative varie selon la surface : les limiteurs RPC de Gateway retournent
  `retryable: true` plus `retryAfterMs`, l'ingress webhook utilise HTTP 429
  avec un en-tête `Retry-After`, et ACP intègre l'attente dans le message d'erreur.
  Dans tous les cas, attendez la durée indiquée au lieu de réessayer
  immédiatement.
