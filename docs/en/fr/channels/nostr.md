---
summary: "Canal DM Nostr via messages chiffrés NIP-04"
read_when:
  - You want OpenClaw to receive DMs via Nostr
  - You're setting up decentralized messaging
title: "Nostr"
---

# Nostr

**Status:** Plugin optionnel (désactivé par défaut).

Nostr est un protocole décentralisé pour les réseaux sociaux. Ce canal permet à OpenClaw de recevoir et de répondre aux messages directs (DM) chiffrés via NIP-04.

## Installation (à la demande)

### Intégration (recommandé)

- L'assistant d'intégration (`openclaw onboard`) et `openclaw channels add` listent les plugins de canal optionnels.
- La sélection de Nostr vous invite à installer le plugin à la demande.

Paramètres par défaut d'installation :

- **Canal Dev + git checkout disponible :** utilise le chemin du plugin local.
- **Stable/Beta :** télécharge depuis npm.

Vous pouvez toujours remplacer le choix dans l'invite.

### Installation manuelle

```bash
openclaw plugins install @openclaw/nostr
```

Utiliser un checkout local (workflows de développement) :

```bash
openclaw plugins install --link <path-to-openclaw>/extensions/nostr
```

Redémarrez la Gateway après l'installation ou l'activation des plugins.

## Configuration rapide

1. Générez une paire de clés Nostr (si nécessaire) :

```bash
# Using nak
nak key generate
```

2. Ajoutez à la configuration :

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}"
    }
  }
}
```

3. Exportez la clé :

```bash
export NOSTR_PRIVATE_KEY="nsec1..."
```

4. Redémarrez la Gateway.

## Référence de configuration

| Clé          | Type     | Par défaut                              | Description                         |
| ------------ | -------- | --------------------------------------- | ----------------------------------- |
| `privateKey` | string   | requis                                  | Clé privée au format `nsec` ou hex  |
| `relays`     | string[] | `['wss://relay.damus.io', 'wss://nos.lol']` | URLs de relais (WebSocket)          |
| `dmPolicy`   | string   | `pairing`                               | Politique d'accès aux DM            |
| `allowFrom`  | string[] | `[]`                                    | Clés publiques des expéditeurs autorisés |
| `enabled`    | boolean  | `true`                                  | Activer/désactiver le canal         |
| `name`       | string   | -                                       | Nom d'affichage                     |
| `profile`    | object   | -                                       | Métadonnées de profil NIP-01        |

## Métadonnées de profil

Les données de profil sont publiées en tant qu'événement NIP-01 `kind:0`. Vous pouvez les gérer depuis l'interface de contrôle (Canaux -> Nostr -> Profil) ou les définir directement dans la configuration.

Exemple :

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "profile": {
        "name": "openclaw",
        "displayName": "OpenClaw",
        "about": "Personal assistant DM bot",
        "picture": "https://example.com/avatar.png",
        "banner": "https://example.com/banner.png",
        "website": "https://example.com",
        "nip05": "openclaw@example.com",
        "lud16": "openclaw@example.com"
      }
    }
  }
}
```

Notes :

- Les URLs de profil doivent utiliser `https://`.
- L'importation depuis les relais fusionne les champs et préserve les remplacements locaux.

## Contrôle d'accès

### Politiques de DM

- **pairing** (par défaut) : les expéditeurs inconnus reçoivent un code d'appairage.
- **allowlist** : seules les clés publiques dans `allowFrom` peuvent envoyer des DM.
- **open** : DM entrants publics (nécessite `allowFrom: ["*"]`).
- **disabled** : ignorer les DM entrants.

### Exemple de liste blanche

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "dmPolicy": "allowlist",
      "allowFrom": ["npub1abc...", "npub1xyz..."]
    }
  }
}
```

## Formats de clé

Formats acceptés :

- **Clé privée :** `nsec...` ou hex 64 caractères
- **Clés publiques (`allowFrom`) :** `npub...` ou hex

## Relais

Par défaut : `relay.damus.io` et `nos.lol`.

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "relays": ["wss://relay.damus.io", "wss://relay.primal.net", "wss://nostr.wine"]
    }
  }
}
```

Conseils :

- Utilisez 2-3 relais pour la redondance.
- Évitez trop de relais (latence, duplication).
- Les relais payants peuvent améliorer la fiabilité.
- Les relais locaux conviennent aux tests (`ws://localhost:7777`).

## Support du protocole

| NIP    | Statut    | Description                           |
| ------ | --------- | ------------------------------------- |
| NIP-01 | Supporté  | Format d'événement de base + métadonnées de profil |
| NIP-04 | Supporté  | DM chiffrés (`kind:4`)                |
| NIP-17 | Planifié  | DM enveloppés en cadeau               |
| NIP-44 | Planifié  | Chiffrement versionné                 |

## Tests

### Relais local

```bash
# Start strfry
docker run -p 7777:7777 ghcr.io/hoytech/strfry
```

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "relays": ["ws://localhost:7777"]
    }
  }
}
```

### Test manuel

1. Notez la clé publique du bot (npub) à partir des journaux.
2. Ouvrez un client Nostr (Damus, Amethyst, etc.).
3. Envoyez un DM à la clé publique du bot.
4. Vérifiez la réponse.

## Dépannage

### Ne pas recevoir de messages

- Vérifiez que la clé privée est valide.
- Assurez-vous que les URLs de relais sont accessibles et utilisent `wss://` (ou `ws://` pour local).
- Confirmez que `enabled` n'est pas `false`.
- Vérifiez les journaux de la Gateway pour les erreurs de connexion au relais.

### Ne pas envoyer de réponses

- Vérifiez que le relais accepte les écritures.
- Vérifiez la connectivité sortante.
- Surveillez les limites de débit du relais.

### Réponses en double

- Attendu lors de l'utilisation de plusieurs relais.
- Les messages sont dédupliqués par ID d'événement ; seule la première livraison déclenche une réponse.

## Sécurité

- Ne validez jamais les clés privées.
- Utilisez des variables d'environnement pour les clés.
- Envisagez `allowlist` pour les bots de production.

## Limitations (MVP)

- Messages directs uniquement (pas de chats de groupe).
- Pas de pièces jointes multimédias.
- NIP-04 uniquement (NIP-17 gift-wrap planifié).
