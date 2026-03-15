---
summary: "Référence CLI pour `openclaw qr` (générer un code QR d'appairage iOS + code de configuration)"
read_when:
  - You want to pair the iOS app with a gateway quickly
  - You need setup-code output for remote/manual sharing
title: "qr"
---

# `openclaw qr`

Générez un code QR d'appairage iOS et un code de configuration à partir de votre configuration Gateway actuelle.

## Utilisation

```bash
openclaw qr
openclaw qr --setup-code-only
openclaw qr --json
openclaw qr --remote
openclaw qr --url wss://gateway.example/ws
```

## Options

- `--remote` : utiliser `gateway.remote.url` plus le jeton/mot de passe distant de la configuration
- `--url <url>` : remplacer l'URL de la passerelle utilisée dans la charge utile
- `--public-url <url>` : remplacer l'URL publique utilisée dans la charge utile
- `--token <token>` : remplacer le jeton de passerelle par rapport auquel le flux d'amorçage s'authentifie
- `--password <password>` : remplacer le mot de passe de passerelle par rapport auquel le flux d'amorçage s'authentifie
- `--setup-code-only` : imprimer uniquement le code de configuration
- `--no-ascii` : ignorer le rendu ASCII du code QR
- `--json` : émettre JSON (`setupCode`, `gatewayUrl`, `auth`, `urlSource`)

## Notes

- `--token` et `--password` s'excluent mutuellement.
- Le code de configuration lui-même porte maintenant un `bootstrapToken` opaque de courte durée, et non le jeton/mot de passe de passerelle partagé.
- Avec `--remote`, si les identifiants distants effectivement actifs sont configurés en tant que SecretRefs et que vous ne transmettez pas `--token` ou `--password`, la commande les résout à partir de l'instantané de passerelle actif. Si la passerelle n'est pas disponible, la commande échoue rapidement.
- Sans `--remote`, les SecretRefs d'authentification de passerelle locale sont résolus quand aucun remplacement d'authentification CLI n'est transmis :
  - `gateway.auth.token` se résout quand l'authentification par jeton peut l'emporter (mode `gateway.auth.mode="token"` explicite ou mode déduit où aucune source de mot de passe ne l'emporte).
  - `gateway.auth.password` se résout quand l'authentification par mot de passe peut l'emporter (mode `gateway.auth.mode="password"` explicite ou mode déduit sans jeton gagnant de l'authentification/env).
- Si `gateway.auth.token` et `gateway.auth.password` sont tous deux configurés (y compris les SecretRefs) et que `gateway.auth.mode` n'est pas défini, la résolution du code de configuration échoue jusqu'à ce que le mode soit défini explicitement.
- Note sur l'asymétrie de version de passerelle : ce chemin de commande nécessite une passerelle qui prend en charge `secrets.resolve` ; les anciennes passerelles retournent une erreur de méthode inconnue.
- Après l'analyse, approuvez l'appairage de l'appareil avec :
  - `openclaw devices list`
  - `openclaw devices approve <requestId>`
