---
read_when:
  - Vous souhaitez qu'OpenClaw reçoive des messages privés via Nostr
  - Vous configurez la messagerie décentralisée
summary: Canal de messages privés Nostr avec chiffrement NIP-04
title: Nostr
x-i18n:
  generated_at: "2026-02-03T07:44:13Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 6b9fe4c74bf5e7c0f59bbaa129ec5270fd29a248551a8a9a7dde6cff8fb46111
  source_path: channels/nostr.md
  workflow: 15
---

# Nostr

**Statut :** Plugin optionnel (désactivé par défaut).

Nostr est un protocole de réseau social décentralisé. Ce canal permet à OpenClaw de recevoir et de répondre à des messages privés (DMs) chiffrés via NIP-04.

## Installation (à la demande)

### Assistant d'intégration (recommandé)

- L'assistant d'intégration (`openclaw onboard`) et `openclaw channels add` listent les plugins de canal optionnels.
- La sélection de Nostr vous invite à installer le plugin à la demande.

Valeurs par défaut d'installation :

- **Canal Dev + git checkout disponible :** Utilise le chemin du plugin local.
- **Stable/Beta :** Télécharge depuis npm.

Vous pouvez toujours remplacer la sélection à l'invite.

### Installation manuelle

```bash
openclaw plugins install @openclaw/nostr
```

Utiliser un checkout local (flux de travail de développement) :

```bash
openclaw plugins install --link <path-to-openclaw>/extensions/nostr
```

Redémarrez la passerelle après l'installation ou l'activation du plugin.

## Configuration rapide

1. Générez une paire de clés Nostr (si nécessaire) :

```bash
# Utiliser nak
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

4. Redémarrez la passerelle.

## Référence de configuration

| Clé          | Type     | Valeur par défaut                           | Description                    |
| ------------ | -------- | ------------------------------------------- | ------------------------------ |
| `privateKey` | string   | Obligatoire                                 | Clé privée au format `nsec` ou hexadécimal |
| `relays`     | string[] | `['wss://relay.damus.io', 'wss://nos.lol']` | URL des relais (WebSocket)     |
| `dmPolicy`   | string   | `pairing`                                   | Politique d'accès aux messages privés |
| `allowFrom`  | string[] | `[]`                                        | Clés publiques des expéditeurs autorisés |
| `enabled`    | boolean  | `true`                                      | Activer/désactiver le canal    |
| `name`       | string   | -                                           | Nom d'affichage                |
| `profile`    | object   | -                                           | Métadonnées de profil NIP-01   |

## Métadonnées de profil

Les données de profil sont publiées en tant qu'événement NIP-01 `kind:0`. Vous pouvez les gérer à partir de l'interface de contrôle (Channels -> Nostr -> Profile) ou les définir directement dans la configuration.

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

Remarques :

- Les URL de profil doivent utiliser `https://`.
- L'importation depuis les relais fusionne les champs et préserve les remplacements locaux.

## Contrôle d'accès

### Politique de messages privés

- **pairing** (par défaut) : Les expéditeurs inconnus reçoivent un code d'appairage.
- **allowlist** : Seules les clés publiques dans `allowFrom` peuvent envoyer des messages privés.
- **open** : Recevoir les messages privés publiquement (nécessite `allowFrom: ["*"]`).
- **disabled** : Ignorer les messages privés reçus.

### Exemple de liste d'autorisation

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

- **Clé privée :** `nsec...` ou hexadécimal 64 caractères
- **Clé publique (`allowFrom`) :** `npub...` ou hexadécimal

## Relais

Valeurs par défaut : `relay.damus.io` et `nos.lol`.

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
- Évitez trop de relais (latence, doublons).
- Les relais payants peuvent améliorer la fiabilité.
- Les relais locaux conviennent aux tests (`ws://localhost:7777`).

## Support des protocoles

| NIP    | Statut      | Description                          |
| ------ | ----------- | ------------------------------------ |
| NIP-01 | Supporté    | Format d'événement de base + métadonnées de profil |
| NIP-04 | Supporté    | Messages privés chiffrés (`kind:4`)  |
| NIP-17 | Planifié    | Messages privés enveloppés en cadeau |
| NIP-44 | Planifié    | Chiffrement versionné                |

## Tests

### Relais local

```bash
# Démarrer strfry
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

### Tests manuels

1. Notez la clé publique du bot (npub) à partir des journaux.
2. Ouvrez un client Nostr (Damus, Amethyst, etc.).
3. Envoyez un message privé à la clé publique du bot.
4. Vérifiez la réponse.

## Dépannage

### Messages non reçus

- Vérifiez que la clé privée est valide.
- Assurez-vous que les URL des relais sont accessibles et utilisent `wss://` (`ws://` pour local).
- Confirmez que `enabled` n'est pas `false`.
- Vérifiez les erreurs de connexion aux relais dans les journaux de la passerelle.

### Réponses non envoyées

- Vérifiez que le relais accepte les écritures.
- Vérifiez la connectivité sortante.
- Notez les limites de débit des relais.

### Réponses en double

- C'est normal avec plusieurs relais.
- Les messages sont dédupliqués par ID d'événement ; seule la première livraison déclenche une réponse.

## Sécurité

- Ne validez jamais les clés privées.
- Utilisez des variables d'environnement pour stocker les clés.
- Pour les bots en production, envisagez d'utiliser `allowlist`.

## Limitations (MVP)

- Supporte uniquement les messages privés (pas de chats de groupe).
- Pas de support des pièces jointes multimédias.
- Supporte uniquement NIP-04 (support NIP-17 enveloppé en cadeau planifié).
