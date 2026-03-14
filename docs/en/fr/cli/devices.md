```markdown
summary: "Référence CLI pour `openclaw devices` (appairage d'appareils + rotation/révocation de tokens)"
read_when:
  - You are approving device pairing requests
  - You need to rotate or revoke device tokens
title: "devices"
---

# `openclaw devices`

Gérer les demandes d'appairage d'appareils et les tokens limités à un appareil.

## Commandes

### `openclaw devices list`

Lister les demandes d'appairage en attente et les appareils appairés.

```
openclaw devices list
openclaw devices list --json
```

### `openclaw devices remove <deviceId>`

Supprimer une entrée d'appareil appairé.

```
openclaw devices remove <deviceId>
openclaw devices remove <deviceId> --json
```

### `openclaw devices clear --yes [--pending]`

Effacer les appareils appairés en masse.

```
openclaw devices clear --yes
openclaw devices clear --yes --pending
openclaw devices clear --yes --pending --json
```

### `openclaw devices approve [requestId] [--latest]`

Approuver une demande d'appairage d'appareil en attente. Si `requestId` est omis, OpenClaw
approuve automatiquement la demande en attente la plus récente.

```
openclaw devices approve
openclaw devices approve <requestId>
openclaw devices approve --latest
```

### `openclaw devices reject <requestId>`

Rejeter une demande d'appairage d'appareil en attente.

```
openclaw devices reject <requestId>
```

### `openclaw devices rotate --device <id> --role <role> [--scope <scope...>]`

Faire tourner un token d'appareil pour un rôle spécifique (en mettant à jour optionnellement les portées).

```
openclaw devices rotate --device <deviceId> --role operator --scope operator.read --scope operator.write
```

### `openclaw devices revoke --device <id> --role <role>`

Révoquer un token d'appareil pour un rôle spécifique.

```
openclaw devices revoke --device <deviceId> --role node
```

## Options communes

- `--url <url>`: URL WebSocket de la passerelle (par défaut `gateway.remote.url` si configuré).
- `--token <token>`: Token de la passerelle (si requis).
- `--password <password>`: Mot de passe de la passerelle (authentification par mot de passe).
- `--timeout <ms>`: Délai d'expiration RPC.
- `--json`: Sortie JSON (recommandé pour les scripts).

Remarque : lorsque vous définissez `--url`, la CLI ne revient pas aux identifiants de configuration ou d'environnement.
Passez `--token` ou `--password` explicitement. Les identifiants explicites manquants sont une erreur.

## Remarques

- La rotation de token retourne un nouveau token (sensible). Traitez-le comme un secret.
- Ces commandes nécessitent la portée `operator.pairing` (ou `operator.admin`).
- `devices clear` est intentionnellement protégé par `--yes`.
- Si la portée d'appairage n'est pas disponible sur la boucle locale (et qu'aucun `--url` explicite n'est passé), list/approve peut utiliser un secours d'appairage local.

## Liste de contrôle de récupération de dérive de token

À utiliser lorsque Control UI ou d'autres clients continuent à échouer avec `AUTH_TOKEN_MISMATCH` ou `AUTH_DEVICE_TOKEN_MISMATCH`.

1. Confirmer la source actuelle du token de la passerelle :

```bash
openclaw config get gateway.auth.token
```

2. Lister les appareils appairés et identifier l'ID d'appareil affecté :

```bash
openclaw devices list
```

3. Faire tourner le token opérateur pour l'appareil affecté :

```bash
openclaw devices rotate --device <deviceId> --role operator
```

4. Si la rotation ne suffit pas, supprimer l'appairage obsolète et approuver à nouveau :

```bash
openclaw devices remove <deviceId>
openclaw devices list
openclaw devices approve <requestId>
```

5. Réessayer la connexion client avec le token/mot de passe partagé actuel.

Connexes :

- [Dépannage de l'authentification du tableau de bord](/web/dashboard#if-you-see-unauthorized-1008)
- [Dépannage de la passerelle](/gateway/troubleshooting#dashboard-control-ui-connectivity)
```
