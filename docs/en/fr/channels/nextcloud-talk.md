---
summary: "Statut du support Nextcloud Talk, capacités et configuration"
read_when:
  - Working on Nextcloud Talk channel features
title: "Nextcloud Talk"
---

# Nextcloud Talk (plugin)

Statut : supporté via plugin (bot webhook). Les messages directs, les salons, les réactions et les messages markdown sont supportés.

## Plugin requis

Nextcloud Talk est fourni en tant que plugin et n'est pas inclus dans l'installation principale.

Installez via CLI (registre npm) :

```bash
openclaw plugins install @openclaw/nextcloud-talk
```

Checkout local (lors de l'exécution à partir d'un dépôt git) :

```bash
openclaw plugins install ./extensions/nextcloud-talk
```

Si vous choisissez Nextcloud Talk lors de la configuration/intégration et qu'un checkout git est détecté,
OpenClaw proposera automatiquement le chemin d'installation local.

Détails : [Plugins](/tools/plugin)

## Configuration rapide (débutant)

1. Installez le plugin Nextcloud Talk.
2. Sur votre serveur Nextcloud, créez un bot :

   ```bash
   ./occ talk:bot:install "OpenClaw" "<shared-secret>" "<webhook-url>" --feature reaction
   ```

3. Activez le bot dans les paramètres du salon cible.
4. Configurez OpenClaw :
   - Config : `channels.nextcloud-talk.baseUrl` + `channels.nextcloud-talk.botSecret`
   - Ou env : `NEXTCLOUD_TALK_BOT_SECRET` (compte par défaut uniquement)
5. Redémarrez la passerelle (ou terminez l'intégration).

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

## Notes

- Les bots ne peuvent pas initier de messages directs. L'utilisateur doit d'abord envoyer un message au bot.
- L'URL du webhook doit être accessible par la passerelle ; définissez `webhookPublicUrl` si vous êtes derrière un proxy.
- Les téléchargements de médias ne sont pas supportés par l'API du bot ; les médias sont envoyés sous forme d'URL.
- La charge utile du webhook ne distingue pas les messages directs des salons ; définissez `apiUser` + `apiPassword` pour activer les recherches de type de salon (sinon les messages directs sont traités comme des salons).

## Contrôle d'accès (messages directs)

- Par défaut : `channels.nextcloud-talk.dmPolicy = "pairing"`. Les expéditeurs inconnus reçoivent un code d'appairage.
- Approuvez via :
  - `openclaw pairing list nextcloud-talk`
  - `openclaw pairing approve nextcloud-talk <CODE>`
- Messages directs publics : `channels.nextcloud-talk.dmPolicy="open"` plus `channels.nextcloud-talk.allowFrom=["*"]`.
- `allowFrom` correspond uniquement aux identifiants d'utilisateur Nextcloud ; les noms d'affichage sont ignorés.

## Salons (groupes)

- Par défaut : `channels.nextcloud-talk.groupPolicy = "allowlist"` (contrôlé par mention).
- Salons de liste blanche avec `channels.nextcloud-talk.rooms` :

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

- Pour ne permettre aucun salon, gardez la liste blanche vide ou définissez `channels.nextcloud-talk.groupPolicy="disabled"`.

## Capacités

| Fonctionnalité      | Statut            |
| ------------------- | ----------------- |
| Messages directs    | Supporté          |
| Salons              | Supporté          |
| Fils de discussion  | Non supporté      |
| Médias              | URL uniquement    |
| Réactions           | Supporté          |
| Commandes natives   | Non supporté      |

## Référence de configuration (Nextcloud Talk)

Configuration complète : [Configuration](/gateway/configuration)

Options du fournisseur :

- `channels.nextcloud-talk.enabled` : activer/désactiver le démarrage du canal.
- `channels.nextcloud-talk.baseUrl` : URL de l'instance Nextcloud.
- `channels.nextcloud-talk.botSecret` : secret partagé du bot.
- `channels.nextcloud-talk.botSecretFile` : chemin du secret du fichier régulier. Les liens symboliques sont rejetés.
- `channels.nextcloud-talk.apiUser` : utilisateur API pour les recherches de salon (détection de messages directs).
- `channels.nextcloud-talk.apiPassword` : mot de passe API/application pour les recherches de salon.
- `channels.nextcloud-talk.apiPasswordFile` : chemin du fichier de mot de passe API.
- `channels.nextcloud-talk.webhookPort` : port d'écoute du webhook (par défaut : 8788).
- `channels.nextcloud-talk.webhookHost` : hôte du webhook (par défaut : 0.0.0.0).
- `channels.nextcloud-talk.webhookPath` : chemin du webhook (par défaut : /nextcloud-talk-webhook).
- `channels.nextcloud-talk.webhookPublicUrl` : URL du webhook accessible de l'extérieur.
- `channels.nextcloud-talk.dmPolicy` : `pairing | allowlist | open | disabled`.
- `channels.nextcloud-talk.allowFrom` : liste blanche de messages directs (identifiants d'utilisateur). `open` nécessite `"*"`.
- `channels.nextcloud-talk.groupPolicy` : `allowlist | open | disabled`.
- `channels.nextcloud-talk.groupAllowFrom` : liste blanche de groupes (identifiants d'utilisateur).
- `channels.nextcloud-talk.rooms` : paramètres par salon et liste blanche.
- `channels.nextcloud-talk.historyLimit` : limite d'historique de groupe (0 désactive).
- `channels.nextcloud-talk.dmHistoryLimit` : limite d'historique de messages directs (0 désactive).
- `channels.nextcloud-talk.dms` : remplacements par message direct (historyLimit).
- `channels.nextcloud-talk.textChunkLimit` : taille du bloc de texte sortant (caractères).
- `channels.nextcloud-talk.chunkMode` : `length` (par défaut) ou `newline` pour diviser sur les lignes vides (limites de paragraphes) avant la division par longueur.
- `channels.nextcloud-talk.blockStreaming` : désactiver le streaming de bloc pour ce canal.
- `channels.nextcloud-talk.blockStreamingCoalesce` : réglage de coalescence du streaming de bloc.
- `channels.nextcloud-talk.mediaMaxMb` : limite de médias entrants (Mo).
