---
read_when:
  - Lors du développement de fonctionnalités de canaux Nextcloud Talk
summary: Support, fonctionnalités et configuration de Nextcloud Talk
title: Nextcloud Talk
x-i18n:
  generated_at: "2026-02-03T10:04:00Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 21b7b9756c4356a76dc0f14c10e44ed74a284cf3badf87e2df75eb88d8a90c31
  source_path: channels/nextcloud-talk.md
  workflow: 15
---

# Nextcloud Talk (Plugin)

Statut : Support via plugin (bot webhook). Supporte les messages privés, les salons, les réactions emoji et les messages Markdown.

## Plugin requis

Nextcloud Talk est fourni sous forme de plugin et n'est pas inclus dans l'installation principale.

Installation via CLI (référentiel npm) :

```bash
openclaw plugins install @openclaw/nextcloud-talk
```

Installation par extraction locale (lors de l'exécution à partir du référentiel git) :

```bash
openclaw plugins install ./extensions/nextcloud-talk
```

Si vous avez sélectionné Nextcloud Talk lors de la configuration/l'assistant de démarrage et qu'une extraction git est détectée,
OpenClaw fournira automatiquement le chemin d'installation local.

Détails : [Plugins](/tools/plugin)

## Configuration rapide (démarrage)

1. Installez le plugin Nextcloud Talk.
2. Créez un bot sur votre serveur Nextcloud :
   ```bash
   ./occ talk:bot:install "OpenClaw" "<shared-secret>" "<webhook-url>" --feature reaction
   ```
3. Activez le bot dans les paramètres du salon cible.
4. Configurez OpenClaw :
   - Clés de configuration : `channels.nextcloud-talk.baseUrl` + `channels.nextcloud-talk.botSecret`
   - Ou variables d'environnement : `NEXTCLOUD_TALK_BOT_SECRET` (compte par défaut uniquement)
5. Redémarrez la passerelle (ou terminez l'assistant de démarrage).

Configuration minimale :

```json5
{
  channels: {
    "nextcloud-talk": {
      enabled: true,
      baseUrl: "https://cloud.example.com",
      botSecret: "shared-secret",
      dmPolicy: "pairing",
    },
  },
}
```

## Remarques importantes

- Le bot ne peut pas initier les messages privés. Les utilisateurs doivent d'abord envoyer un message au bot.
- L'URL du webhook doit être accessible par la passerelle ; s'il se trouve derrière un proxy, définissez `webhookPublicUrl`.
- L'API du bot ne supporte pas les téléchargements de médias ; les médias sont envoyés sous forme d'URL.
- La charge utile du webhook ne peut pas distinguer les messages privés des salons ; définissez `apiUser` + `apiPassword` pour activer les requêtes de type de salon (sinon les messages privés seront traités comme des salons).

## Contrôle d'accès (messages privés)

- Par défaut : `channels.nextcloud-talk.dmPolicy = "pairing"`. Les expéditeurs inconnus recevront un code d'appairage.
- Méthodes d'approbation :
  - `openclaw pairing list nextcloud-talk`
  - `openclaw pairing approve nextcloud-talk <CODE>`
- Messages privés ouverts : `channels.nextcloud-talk.dmPolicy="open"` plus `channels.nextcloud-talk.allowFrom=["*"]`.

## Salons (groupes)

- Par défaut : `channels.nextcloud-talk.groupPolicy = "allowlist"` (mention requise pour déclencher).
- Utilisez `channels.nextcloud-talk.rooms` pour configurer la liste blanche des salons :

```json5
{
  channels: {
    "nextcloud-talk": {
      rooms: {
        "room-token": { requireMention: true },
      },
    },
  },
}
```

- Pour désactiver tous les salons, gardez la liste blanche vide ou définissez `channels.nextcloud-talk.groupPolicy="disabled"`.

## Support des fonctionnalités

| Fonctionnalité | Statut |
| -------------- | ------ |
| Messages privés | Supporté |
| Salons | Supporté |
| Fils de discussion | Non supporté |
| Médias | URL uniquement |
| Réactions emoji | Supporté |
| Commandes natives | Non supporté |

## Référence de configuration (Nextcloud Talk)

Configuration complète : [Configuration](/gateway/configuration)

Options du fournisseur :

- `channels.nextcloud-talk.enabled` : Activer/désactiver le démarrage du canal.
- `channels.nextcloud-talk.baseUrl` : URL de l'instance Nextcloud.
- `channels.nextcloud-talk.botSecret` : Clé partagée du bot.
- `channels.nextcloud-talk.botSecretFile` : Chemin du fichier de clé.
- `channels.nextcloud-talk.apiUser` : Utilisateur API pour les requêtes de salon (détection de messages privés).
- `channels.nextcloud-talk.apiPassword` : Mot de passe API/application pour les requêtes de salon.
- `channels.nextcloud-talk.apiPasswordFile` : Chemin du fichier de mot de passe API.
- `channels.nextcloud-talk.webhookPort` : Port d'écoute du webhook (par défaut : 8788).
- `channels.nextcloud-talk.webhookHost` : Hôte du webhook (par défaut : 0.0.0.0).
- `channels.nextcloud-talk.webhookPath` : Chemin du webhook (par défaut : /nextcloud-talk-webhook).
- `channels.nextcloud-talk.webhookPublicUrl` : URL du webhook accessible en externe.
- `channels.nextcloud-talk.dmPolicy` : `pairing | allowlist | open | disabled`.
- `channels.nextcloud-talk.allowFrom` : Liste blanche des messages privés (ID utilisateur). `open` nécessite `"*"`.
- `channels.nextcloud-talk.groupPolicy` : `allowlist | open | disabled`.
- `channels.nextcloud-talk.groupAllowFrom` : Liste blanche des groupes (ID utilisateur).
- `channels.nextcloud-talk.rooms` : Paramètres et liste blanche par salon.
- `channels.nextcloud-talk.historyLimit` : Limite d'historique des groupes (0 pour désactiver).
- `channels.nextcloud-talk.dmHistoryLimit` : Limite d'historique des messages privés (0 pour désactiver).
- `channels.nextcloud-talk.dms` : Paramètres de remplacement par message privé (historyLimit).
- `channels.nextcloud-talk.textChunkLimit` : Taille de fragmentation du texte sortant (nombre de caractères).
- `channels.nextcloud-talk.chunkMode` : `length` (par défaut) ou `newline`, divise par lignes vides (limites de paragraphes) avant la fragmentation par longueur.
- `channels.nextcloud-talk.blockStreaming` : Désactiver la diffusion en continu fragmentée pour ce canal.
- `channels.nextcloud-talk.blockStreamingCoalesce` : Ajustement de coalescence de la diffusion en continu fragmentée.
- `channels.nextcloud-talk.mediaMaxMb` : Limite de taille des médias entrants (Mo).
