---
read_when:
  - 开发 Matrix 渠道功能
summary: Matrix 支持状态、功能和配置
title: Matrix
x-i18n:
  generated_at: "2026-02-03T07:44:02Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b276b5263593c766e7be6549abbb27927177e7b51cfd297b4825965372513ee4
  source_path: channels/matrix.md
  workflow: 15
---

# Matrix (Plugin)

Matrix est un protocole de messagerie ouvert et décentralisé. OpenClaw se connecte à n'importe quel serveur d'accueil en tant qu'**utilisateur** Matrix, vous devez donc créer un compte Matrix pour votre bot. Une fois connecté, vous pouvez envoyer des messages privés directement au bot ou l'inviter à rejoindre des salons (« groupes » Matrix). Beeper est également une option client valide, mais il nécessite l'activation de E2EE.

Statut : Pris en charge via plugin (@vector-im/matrix-bot-sdk). Prend en charge les messages privés, les salons, les fils de discussion, les médias, les réactions emoji, les sondages (envoi + poll-start en tant que texte), les emplacements et E2EE (nécessite la prise en charge du chiffrement).

## Plugin requis

Matrix est fourni en tant que plugin et n'est pas inclus dans l'installation principale.

Installation via CLI (référentiel npm) :

```bash
openclaw plugins install @openclaw/matrix
```

Extraction locale (lors de l'exécution à partir du référentiel git) :

```bash
openclaw plugins install ./extensions/matrix
```

Si vous sélectionnez Matrix lors de la configuration/initialisation et qu'une extraction git est détectée, OpenClaw fournira automatiquement le chemin d'installation local.

Détails : [Plugins](/tools/plugin)

## Configuration

1. Installez le plugin Matrix :
   - Depuis npm : `openclaw plugins install @openclaw/matrix`
   - Depuis une extraction locale : `openclaw plugins install ./extensions/matrix`
2. Créez un compte Matrix sur un serveur d'accueil :
   - Parcourez les options d'hébergement sur [https://matrix.org/ecosystem/hosting/](https://matrix.org/ecosystem/hosting/)
   - Ou auto-hébergez.
3. Obtenez un jeton d'accès pour le compte du bot :
   - Utilisez `curl` pour appeler l'API de connexion Matrix sur votre serveur d'accueil :

   ```bash
   curl --request POST \
     --url https://matrix.example.org/_matrix/client/v3/login \
     --header 'Content-Type: application/json' \
     --data '{
     "type": "m.login.password",
     "identifier": {
       "type": "m.id.user",
       "user": "your-user-name"
     },
     "password": "your-password"
   }'
   ```

   - Remplacez `matrix.example.org` par l'URL de votre serveur d'accueil.
   - Ou définissez `channels.matrix.userId` + `channels.matrix.password` : OpenClaw appellera le même point de terminaison de connexion, stockera le jeton d'accès dans `~/.openclaw/credentials/matrix/credentials.json`, et le réutilisera au prochain démarrage.

4. Configurez les identifiants :
   - Variables d'environnement : `MATRIX_HOMESERVER`, `MATRIX_ACCESS_TOKEN` (ou `MATRIX_USER_ID` + `MATRIX_PASSWORD`)
   - Ou configuration : `channels.matrix.*`
   - Si les deux sont définis, la configuration a la priorité.
   - Lors de l'utilisation d'un jeton d'accès : l'ID utilisateur est automatiquement récupéré via `/whoami`.
   - Lors de la définition, `channels.matrix.userId` doit être l'ID Matrix complet (exemple : `@bot:example.org`).
5. Redémarrez la passerelle (ou terminez l'initialisation).
6. Commencez à envoyer des messages privés au bot ou invitez-le à rejoindre des salons à partir de n'importe quel client Matrix (Element, Beeper, etc. ; voir https://matrix.org/ecosystem/clients/). Beeper nécessite E2EE, donc définissez `channels.matrix.encryption: true` et vérifiez l'appareil.

Configuration minimale (jeton d'accès, ID utilisateur récupéré automatiquement) :

```json5
{
  channels: {
    matrix: {
      enabled: true,
      homeserver: "https://matrix.example.org",
      accessToken: "syt_***",
      dm: { policy: "pairing" },
    },
  },
}
```

Configuration E2EE (activer le chiffrement de bout en bout) :

```json5
{
  channels: {
    matrix: {
      enabled: true,
      homeserver: "https://matrix.example.org",
      accessToken: "syt_***",
      encryption: true,
      dm: { policy: "pairing" },
    },
  },
}
```

## Chiffrement (E2EE)

Le chiffrement de bout en bout est **pris en charge** via le SDK de chiffrement Rust.

Activez avec `channels.matrix.encryption: true` :

- Si le module de chiffrement se charge avec succès, les salons chiffrés sont automatiquement déchiffrés.
- Lors de l'envoi vers des salons chiffrés, les médias sortants sont chiffrés.
- Lors de la première connexion, OpenClaw demandera la vérification de l'appareil à vos autres sessions.
- Vérifiez l'appareil dans un autre client Matrix (Element, etc.) pour activer le partage de clés.
- Si le module de chiffrement ne peut pas être chargé, E2EE sera désactivé et les salons chiffrés ne pourront pas être déchiffrés ; OpenClaw enregistrera un avertissement.
- Si vous voyez une erreur concernant un module de chiffrement manquant (par exemple `@matrix-org/matrix-sdk-crypto-nodejs-*`), autorisez le script de construction de `@matrix-org/matrix-sdk-crypto-nodejs` et exécutez `pnpm rebuild @matrix-org/matrix-sdk-crypto-nodejs`, ou utilisez `node node_modules/@matrix-org/matrix-sdk-crypto-nodejs/download-lib.js` pour obtenir les fichiers binaires.

L'état du chiffrement est stocké par compte + jeton d'accès dans `~/.openclaw/matrix/accounts/<account>/<homeserver>__<user>/<token-hash>/crypto/` (base de données SQLite). L'état de synchronisation est stocké dans `bot-storage.json` dans le même répertoire. Si le jeton d'accès (appareil) change, un nouveau stockage est créé et le bot doit être reverifié pour accéder aux salons chiffrés.

**Vérification de l'appareil :**
Lorsque E2EE est activé, le bot demandera la vérification à vos autres sessions au démarrage. Ouvrez Element (ou un autre client) et approuvez la demande de vérification pour établir la confiance. Une fois vérifié, le bot peut déchiffrer les messages dans les salons chiffrés.

## Modèle de routage

- Les réponses reviennent toujours à Matrix.
- Les messages privés partagent la session principale de l'agent ; les salons sont mappés aux sessions de groupe.

## Contrôle d'accès (Messages privés)

- Par défaut : `channels.matrix.dm.policy = "pairing"`. Les expéditeurs inconnus reçoivent un code d'appairage.
- Approuvez via :
  - `openclaw pairing list matrix`
  - `openclaw pairing approve matrix <CODE>`
- Messages privés ouverts : `channels.matrix.dm.policy="open"` plus `channels.matrix.dm.allowFrom=["*"]`.
- `channels.matrix.dm.allowFrom` n'accepte que les ID utilisateur Matrix complets (par exemple `@user:server`). L'assistant ne résout les noms d'affichage en ID utilisateur que si la recherche d'annuaire produit une correspondance exacte unique.

## Salons (Groupes)

- Par défaut : `channels.matrix.groupPolicy = "allowlist"` (mention gated). Utilisez `channels.defaults.groupPolicy` pour remplacer la valeur par défaut si elle n'est pas définie.
- Configurez la liste d'autorisation des salons avec `channels.matrix.groups` (ID de salon ou alias ; les noms ne sont résolus en ID que si la recherche d'annuaire produit une correspondance exacte unique) :

```json5
{
  channels: {
    matrix: {
      groupPolicy: "allowlist",
      groups: {
        "!roomId:example.org": { allow: true },
        "#alias:example.org": { allow: true },
      },
      groupAllowFrom: ["@owner:example.org"],
    },
  },
}
```

- `requireMention: false` active les réponses automatiques pour ce salon.
- `groups."*"` peut définir les valeurs par défaut de mention gated entre les salons.
- `groupAllowFrom` limite les expéditeurs qui peuvent déclencher le bot dans les salons (nécessite l'ID utilisateur Matrix complet).
- La liste d'autorisation `users` par salon peut restreindre davantage les expéditeurs dans un salon spécifique (nécessite l'ID utilisateur Matrix complet).
- L'assistant de configuration vous invite à entrer une liste d'autorisation de salons (ID de salon, alias ou nom), résolvant les noms uniquement en cas de correspondance exacte et unique.
- Au démarrage, OpenClaw résout les noms de salon/utilisateur dans la liste d'autorisation en ID et enregistre le mappage ; les entrées non résolues ne participent pas à la correspondance de la liste d'autorisation.
- Rejoindre automatiquement les invitations par défaut ; contrôlez avec `channels.matrix.autoJoin` et `channels.matrix.autoJoinAllowlist`.
- Pour **désactiver tous les salons**, définissez `channels.matrix.groupPolicy: "disabled"` (ou gardez la liste d'autorisation vide).
- Noms de clés hérités : `channels.matrix.rooms` (même structure que `groups`).

## Fils de discussion

- Prend en charge les réponses aux fils de discussion.
- `channels.matrix.threadReplies` contrôle si les réponses restent dans le fil :
  - `off`, `inbound` (par défaut), `always`
- `channels.matrix.replyToMode` contrôle les métadonnées reply-to lors de la réponse en dehors du fil :
  - `off` (par défaut), `first`, `all`

## Fonctionnalités

| Fonctionnalité | Statut                                                 |
| -------------- | ------------------------------------------------------ |
| Messages privés | ✅ Pris en charge                                      |
| Salons         | ✅ Pris en charge                                      |
| Fils de discussion | ✅ Pris en charge                                      |
| Médias         | ✅ Pris en charge                                      |
| E2EE           | ✅ Pris en charge (nécessite le module de chiffrement) |
| Réactions emoji | ✅ Pris en charge (envoi/lecture via outils)           |
| Sondages       | ✅ Envoi pris en charge ; les sondages entrants commencent convertis en texte (réponse/fin ignorées) |
| Emplacements   | ✅ Pris en charge (URI geo ; altitude ignorée)         |
| Commandes natives | ✅ Pris en charge                                      |

## Référence de configuration (Matrix)

Configuration complète : [Configuration](/gateway/configuration)

Options du fournisseur :

- `channels.matrix.enabled` : Activer/désactiver le démarrage du canal.
- `channels.matrix.homeserver` : URL du serveur d'accueil.
- `channels.matrix.userId` : ID utilisateur Matrix (optionnel lors de l'utilisation d'un jeton d'accès).
- `channels.matrix.accessToken` : Jeton d'accès.
- `channels.matrix.password` : Mot de passe de connexion (le jeton sera stocké).
- `channels.matrix.deviceName` : Nom d'affichage de l'appareil.
- `channels.matrix.encryption` : Activer E2EE (par défaut : false).
- `channels.matrix.initialSyncLimit` : Limite de synchronisation initiale.
- `channels.matrix.threadReplies` : `off | inbound | always` (par défaut : inbound).
- `channels.matrix.textChunkLimit` : Taille de fragmentation du texte sortant (caractères).
- `channels.matrix.chunkMode` : `length` (par défaut) ou `newline` pour diviser par lignes vides (limites de paragraphes) avant la fragmentation par longueur.
- `channels.matrix.dm.policy` : `pairing | allowlist | open | disabled` (par défaut : pairing).
- `channels.matrix.dm.allowFrom` : Liste d'autorisation des messages privés (nécessite l'ID utilisateur Matrix complet). `open` nécessite `"*"`. L'assistant résout les noms en ID si possible.
- `channels.matrix.groupPolicy` : `allowlist | open | disabled` (par défaut : allowlist).
- `channels.matrix.groupAllowFrom` : Liste des expéditeurs autorisés pour les messages de groupe (nécessite l'ID utilisateur Matrix complet).
- `channels.matrix.allowlistOnly` : Forcer les messages privés + salons à utiliser les règles de liste d'autorisation.
- `channels.matrix.groups` : Mappage de liste d'autorisation de groupe + paramètres par salon.
- `channels.matrix.rooms` : Liste d'autorisation/configuration de groupe hérité.
- `channels.matrix.replyToMode` : Mode reply-to pour les fils/étiquettes.
- `channels.matrix.mediaMaxMb` : Limite de médias entrants/sortants (MB).
- `channels.matrix.autoJoin` : Traitement des invitations (`always | allowlist | off`, par défaut : always).
- `channels.matrix.autoJoinAllowlist` : ID de salon/alias autorisés pour la jonction automatique.
- `channels.matrix.actions` : Limites d'outils par action (reactions/messages/pins/memberInfo/channelInfo).
