---
summary: "Référence CLI pour `openclaw qr` (générer un QR d'appairage iOS + code de configuration)"
read_when:
  - Vous souhaitez appairer rapidement l'application iOS avec une passerelle
  - Vous avez besoin de la sortie du code de configuration pour un partage à distance/manuel
title: "qr"
---

# `openclaw qr`

Générez un QR d'appairage iOS et un code de configuration à partir de votre configuration de passerelle actuelle.

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
- `--no-ascii` : ignorer le rendu ASCII du QR
- `--json` : émettre JSON (`setupCode`, `gatewayUrl`, `auth`, `urlSource`)

## Remarques

- `--token` et `--password` s'excluent mutuellement.
- Le code de configuration lui-même porte maintenant un opaque `bootstrapToken` de courte durée, et non le jeton/mot de passe de passerelle partagé.
- Avec `--remote`, si les credentials distants effectivement actifs sont configurés en tant que SecretRefs et que vous ne transmettez pas `--token` ou `--password`, la commande les résout à partir de l'instantané de passerelle actif. Si la passerelle n'est pas disponible, la commande échoue rapidement.
- Sans `--remote`, les SecretRefs d'authentification de passerelle locale sont résolus quand aucun remplacement d'authentification CLI n'est transmis :
  - `gateway.auth.token` se résout quand l'authentification par jeton peut l'emporter (mode `gateway.auth.mode="token"` explicite ou mode déduit où aucune source de mot de passe ne l'emporte).
  - `gateway.auth.password` se résout quand l'authentification par mot de passe peut l'emporter (mode `gateway.auth.mode="password"` explicite ou mode déduit sans jeton gagnant de l'authentification/env).
- Si à la fois `gateway.auth.token` et `gateway.auth.password` sont configurés (y compris les SecretRefs) et que `gateway.auth.mode` n'est pas défini, la résolution du code de configuration échoue jusqu'à ce que le mode soit défini explicitement.
- Remarque sur l'asymétrie de version de passerelle : ce chemin de commande nécessite une passerelle qui supporte `secrets.resolve` ; les anciennes passerelles retournent une erreur de méthode inconnue.
- Après la numérisation, approuvez l'appairage de l'appareil avec :
  - `openclaw devices list`
  - `openclaw devices approve <requestId>`
