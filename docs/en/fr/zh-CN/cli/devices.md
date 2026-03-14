---
read_when:
  - Vous approuvez une demande d'appairage d'appareil
  - Vous devez effectuer une rotation ou révoquer un token d'appareil
summary: "Référence CLI pour `openclaw devices` (appairage d'appareil + rotation/révocation de token)"
title: devices
x-i18n:
  generated_at: "2026-02-03T07:44:52Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 52f903817d2886c1dc29b85d30168d1edff7944bd120a1e139159c9d99a1f517
  source_path: cli/devices.md
  workflow: 15
---

# `openclaw devices`

Gérez les demandes d'appairage d'appareil et les tokens limités à l'appareil.

## Commandes

### `openclaw devices list`

Listez les demandes d'appairage en attente et les appareils appairés.

```
openclaw devices list
openclaw devices list --json
```

### `openclaw devices approve <requestId>`

Approuvez une demande d'appairage d'appareil en attente.

```
openclaw devices approve <requestId>
```

### `openclaw devices reject <requestId>`

Rejetez une demande d'appairage d'appareil en attente.

```
openclaw devices reject <requestId>
```

### `openclaw devices rotate --device <id> --role <role> [--scope <scope...>]`

Effectuez une rotation du token d'appareil pour un rôle spécifique (mise à jour optionnelle du scope).

```
openclaw devices rotate --device <deviceId> --role operator --scope operator.read --scope operator.write
```

### `openclaw devices revoke --device <id> --role <role>`

Révoquez le token d'appareil pour un rôle spécifique.

```
openclaw devices revoke --device <deviceId> --role node
```

## Options générales

- `--url <url>` : URL WebSocket de la passerelle Gateway (par défaut `gateway.remote.url` après configuration).
- `--token <token>` : Token de la passerelle Gateway (si nécessaire).
- `--password <password>` : Mot de passe de la passerelle Gateway (authentification par mot de passe).
- `--timeout <ms>` : Délai d'expiration RPC.
- `--json` : Sortie JSON (recommandé pour les scripts).

## Remarques

- La rotation de token retourne un nouveau token (information sensible). Traitez-le comme vous le feriez pour une clé secrète.
- Ces commandes nécessitent le scope `operator.pairing` (ou `operator.admin`).
