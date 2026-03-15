---
summary: "Statut de support Matrix, capacités et configuration"
read_when:
  - Working on Matrix channel features
title: "Matrix"
---

# Matrix (plugin)

Matrix est un protocole de messagerie ouvert et décentralisé. OpenClaw se connecte en tant qu'**utilisateur** Matrix
sur n'importe quel serveur d'accueil, vous avez donc besoin d'un compte Matrix pour le bot. Une fois connecté, vous pouvez envoyer des messages directs
au bot ou l'inviter dans des salons (« groupes » Matrix). Beeper est également une option client valide,
mais il nécessite que E2EE soit activé.

Statut : supporté via plugin (@vector-im/matrix-bot-sdk). Messages directs, salons, threads, médias, réactions,
sondages (envoi + démarrage de sondage en tant que texte), localisation et E2EE (avec support crypto).

## Plugin requis

Matrix est fourni en tant que plugin et n'est pas inclus dans l'installation principale.

Installez via CLI (registre npm) :

```bash
openclaw plugins install @openclaw/matrix
```

Extraction locale (lors de l'exécution à partir d'un dépôt git) :

```bash
openclaw plugins install ./extensions/matrix
```

Si vous choisissez Matrix lors de la configuration/intégration et qu'une extraction git est détectée,
OpenClaw proposera automatiquement le chemin d'installation local.

Détails : [Plugins](/fr/tools/plugin)

## Configuration

1. Installez le plugin Matrix :
   - Depuis npm : `openclaw plugins install @openclaw/matrix`
   - Depuis une extraction locale : `openclaw plugins install ./extensions/matrix`
2. Créez un compte Matrix sur un serveur d'accueil :
   - Parcourez les options d'hébergement sur [https://matrix.org/ecosystem/hosting/](https://matrix.org/ecosystem/hosting/)
   - Ou hébergez-le vous-même.
3. Obtenez un jeton d'accès pour le compte du bot :
   - Utilisez l'API de connexion Matrix avec `curl` sur votre serveur d'accueil :

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
   - Ou définissez `channels.matrix.userId` + `channels.matrix.password` : OpenClaw appelle le même
     point de terminaison de connexion, stocke le jeton d'accès dans `~/.openclaw/credentials/matrix/credentials.json`,
     et le réutilise au prochain démarrage.

4. Configurez les identifiants :
   - Env : `MATRIX_HOMESERVER`, `MATRIX_ACCESS_TOKEN` (ou `MATRIX_USER_ID` + `MATRIX_PASSWORD`)
   - Ou config : `channels.matrix.*`
   - Si les deux sont définis, la config a la priorité.
   - Avec jeton d'accès : l'ID utilisateur est récupéré automatiquement via `/whoami`.
   - Lorsqu'il est défini, `channels.matrix.userId` doit être l'ID Matrix complet (exemple : `@bot:example.org`).
5. Redémarrez la passerelle (ou terminez l'intégration).
6. Démarrez un message direct avec le bot ou invitez-le dans un salon à partir de n'importe quel client Matrix
   (Element, Beeper, etc. ; voir [https://matrix.org/ecosystem/clients/](https://matrix.org/ecosystem/clients/)). Beeper nécessite E2EE,
   donc définissez `channels.matrix.encryption: true` et vérifiez l'appareil.

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

Configuration E2EE (chiffrement de bout en bout activé) :

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

Le chiffrement de bout en bout est **supporté** via le SDK crypto Rust.

Activez avec `channels.matrix.encryption: true` :

- Si le module crypto se charge, les salons chiffrés sont déchiffrés automatiquement.
- Les médias sortants sont chiffrés lors de l'envoi vers des salons chiffrés.
- Lors de la première connexion, OpenClaw demande la vérification de l'appareil à vos autres sessions.
- Vérifiez l'appareil dans un autre client Matrix (Element, etc.) pour activer le partage de clés.
- Si le module crypto ne peut pas être chargé, E2EE est désactivé et les salons chiffrés ne seront pas déchiffrés ;
  OpenClaw enregistre un avertissement.
- Si vous voyez des erreurs de module crypto manquant (par exemple, `@matrix-org/matrix-sdk-crypto-nodejs-*`),
  autorisez les scripts de construction pour `@matrix-org/matrix-sdk-crypto-nodejs` et exécutez
  `pnpm rebuild @matrix-org/matrix-sdk-crypto-nodejs` ou récupérez le binaire avec
  `node node_modules/@matrix-org/matrix-sdk-crypto-nodejs/download-lib.js`.

L'état crypto est stocké par compte + jeton d'accès dans
`~/.openclaw/matrix/accounts/<account>/<homeserver>__<user>/<token-hash>/crypto/`
(base de données SQLite). L'état de synchronisation se trouve à côté dans `bot-storage.json`.
Si le jeton d'accès (appareil) change, un nouveau magasin est créé et le bot doit être
re-vérifié pour les salons chiffrés.

**Vérification de l'appareil :**
Lorsque E2EE est activé, le bot demandera la vérification à vos autres sessions au démarrage.
Ouvrez Element (ou un autre client) et approuvez la demande de vérification pour établir la confiance.
Une fois vérifié, le bot peut déchiffrer les messages dans les salons chiffrés.

## Multi-compte

Support multi-compte : utilisez `channels.matrix.accounts` avec des identifiants par compte et un `name` optionnel. Voir [`gateway/configuration`](/fr/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) pour le modèle partagé.

Chaque compte s'exécute en tant qu'utilisateur Matrix distinct sur n'importe quel serveur d'accueil. La configuration par compte
hérite des paramètres `channels.matrix` de niveau supérieur et peut remplacer n'importe quelle option
(politique DM, groupes, chiffrement, etc.).

```json5
{
  channels: {
    matrix: {
      enabled: true,
      dm: { policy: "pairing" },
      accounts: {
        assistant: {
          name: "Main assistant",
          homeserver: "https://matrix.example.org",
          accessToken: "syt_assistant_***",
          encryption: true,
        },
        alerts: {
          name: "Alerts bot",
          homeserver: "https://matrix.example.org",
          accessToken: "syt_alerts_***",
          dm: { policy: "allowlist", allowFrom: ["@admin:example.org"] },
        },
      },
    },
  },
}
```

Notes :

- Le démarrage du compte est sérialisé pour éviter les conditions de course avec les importations de modules concurrentes.
- Les variables d'environnement (`MATRIX_HOMESERVER`, `MATRIX_ACCESS_TOKEN`, etc.) s'appliquent uniquement au compte **par défaut**.
- Les paramètres de canal de base (politique DM, politique de groupe, mention gating, etc.) s'appliquent à tous les comptes sauf s'ils sont remplacés par compte.
- Utilisez `bindings[].match.accountId` pour acheminer chaque compte vers un agent différent.
- L'état crypto est stocké par compte + jeton d'accès (magasins de clés distincts par compte).

## Modèle de routage

- Les réponses reviennent toujours à Matrix.
- Les messages directs partagent la session principale de l'agent ; les salons correspondent à des sessions de groupe.

## Contrôle d'accès (messages directs)

- Par défaut : `channels.matrix.dm.policy = "pairing"`. Les expéditeurs inconnus reçoivent un code d'appairage.
- Approuvez via :
  - `openclaw pairing list matrix`
  - `openclaw pairing approve matrix <CODE>`
- Messages directs publics : `channels.matrix.dm.policy="open"` plus `channels.matrix.dm.allowFrom=["*"]`.
- `channels.matrix.dm.allowFrom` accepte les ID utilisateur Matrix complets (exemple : `@user:server`). L'assistant résout les noms d'affichage en ID utilisateur lorsque la recherche d'annuaire trouve une correspondance exacte unique.
- N'utilisez pas les noms d'affichage ou les localparts nus (exemple : `"Alice"` ou `"alice"`). Ils sont ambigus et sont ignorés pour la correspondance de liste d'autorisation. Utilisez les ID complets `@user:server`.

## Salons (groupes)

- Par défaut : `channels.matrix.groupPolicy = "allowlist"` (mention-gated). Utilisez `channels.defaults.groupPolicy` pour remplacer la valeur par défaut lorsqu'elle n'est pas définie.
- Note d'exécution : si `channels.matrix` est complètement absent, l'exécution revient à `groupPolicy="allowlist"` pour les vérifications de salon (même si `channels.defaults.groupPolicy` est défini).
- Salons de liste d'autorisation avec `channels.matrix.groups` (ID de salon ou alias ; les noms sont résolus en ID lorsque la recherche d'annuaire trouve une correspondance exacte unique) :

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

- `requireMention: false` active la réponse automatique dans ce salon.
- `groups."*"` peut définir les valeurs par défaut pour mention gating dans les salons.
- `groupAllowFrom` restreint les expéditeurs qui peuvent déclencher le bot dans les salons (ID utilisateur Matrix complets).
- Les listes d'autorisation `users` par salon peuvent restreindre davantage les expéditeurs dans un salon spécifique (utilisez les ID utilisateur Matrix complets).
- L'assistant de configuration demande les listes d'autorisation de salon (ID de salon, alias ou noms) et résout les noms uniquement sur une correspondance exacte et unique.
- Au démarrage, OpenClaw résout les noms de salon/utilisateur dans les listes d'autorisation en ID et enregistre le mappage ; les entrées non résolues sont ignorées pour la correspondance de liste d'autorisation.
- Les invitations sont rejointes automatiquement par défaut ; contrôlez avec `channels.matrix.autoJoin` et `channels.matrix.autoJoinAllowlist`.
- Pour autoriser **aucun salon**, définissez `channels.matrix.groupPolicy: "disabled"` (ou conservez une liste d'autorisation vide).
- Clé héritée : `channels.matrix.rooms` (même forme que `groups`).

## Threads

- Le threading de réponse est supporté.
- `channels.matrix.threadReplies` contrôle si les réponses restent dans les threads :
  - `off`, `inbound` (par défaut), `always`
- `channels.matrix.replyToMode` contrôle les métadonnées de réponse-à lorsqu'on ne répond pas dans un thread :
  - `off` (par défaut), `first`, `all`

## Capacités

| Fonctionnalité      | Statut                                                                                |
| ------------------- | ------------------------------------------------------------------------------------- |
| Messages directs    | ✅ Supporté                                                                           |
| Salons              | ✅ Supporté                                                                           |
| Threads             | ✅ Supporté                                                                           |
| Médias              | ✅ Supporté                                                                           |
| E2EE                | ✅ Supporté (module crypto requis)                                                    |
| Réactions           | ✅ Supporté (envoi/lecture via outils)                                                |
| Sondages            | ✅ Envoi supporté ; les démarrages de sondage entrants sont convertis en texte (réponses/fins ignorées) |
| Localisation        | ✅ Supporté (URI géo ; altitude ignorée)                                              |
| Commandes natives   | ✅ Supporté                                                                           |

## Dépannage

Exécutez d'abord cette échelle :

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Puis confirmez l'état d'appairage DM si nécessaire :

```bash
openclaw pairing list matrix
```

Défaillances courantes :

- Connecté mais messages de salon ignorés : salon bloqué par `groupPolicy` ou liste d'autorisation de salon.
- Messages directs ignorés : expéditeur en attente d'approbation lorsque `channels.matrix.dm.policy="pairing"`.
- Salons chiffrés échouent : support crypto ou incompatibilité des paramètres de chiffrement.

Pour le flux de triage : [/channels/troubleshooting](/fr/channels/troubleshooting).

## Référence de configuration (Matrix)

Configuration complète : [Configuration](/fr/gateway/configuration)

Options du fournisseur :

- `channels.matrix.enabled`: activer/désactiver le démarrage du canal.
- `channels.matrix.homeserver`: URL du serveur d'accueil.
- `channels.matrix.userId`: ID utilisateur Matrix (optionnel avec jeton d'accès).
- `channels.matrix.accessToken`: jeton d'accès.
- `channels.matrix.password`: mot de passe pour la connexion (jeton stocké).
- `channels.matrix.deviceName`: nom d'affichage de l'appareil.
- `channels.matrix.encryption`: activer E2EE (par défaut : false).
- `channels.matrix.initialSyncLimit`: limite de synchronisation initiale.
- `channels.matrix.threadReplies`: `off | inbound | always` (par défaut : inbound).
- `channels.matrix.textChunkLimit`: taille du bloc de texte sortant (caractères).
- `channels.matrix.chunkMode`: `length` (par défaut) ou `newline` pour diviser sur les lignes vides (limites de paragraphes) avant la segmentation par longueur.
- `channels.matrix.dm.policy`: `pairing | allowlist | open | disabled` (par défaut : pairing).
- `channels.matrix.dm.allowFrom`: liste blanche des DM (ID utilisateur Matrix complets). `open` nécessite `"*"`. L'assistant résout les noms en ID si possible.
- `channels.matrix.groupPolicy`: `allowlist | open | disabled` (par défaut : allowlist).
- `channels.matrix.groupAllowFrom`: expéditeurs autorisés pour les messages de groupe (ID utilisateur Matrix complets).
- `channels.matrix.allowlistOnly`: forcer les règles de liste blanche pour les DM + salons.
- `channels.matrix.groups`: liste blanche de groupes + carte de paramètres par salon.
- `channels.matrix.rooms`: liste blanche/configuration de groupe héritée.
- `channels.matrix.replyToMode`: mode répondre à pour les fils/étiquettes.
- `channels.matrix.mediaMaxMb`: limite de média entrant/sortant (MB).
- `channels.matrix.autoJoin`: gestion des invitations (`always | allowlist | off`, par défaut : always).
- `channels.matrix.autoJoinAllowlist`: ID/alias de salons autorisés pour la jonction automatique.
- `channels.matrix.accounts`: configuration multi-compte indexée par ID de compte (chaque compte hérite des paramètres de niveau supérieur).
- `channels.matrix.actions`: gating d'outils par action (réactions/messages/épingles/memberInfo/channelInfo).
