---
summary: "Statut du support Tlon/Urbit, capacités et configuration"
read_when:
  - Working on Tlon/Urbit channel features
title: "Tlon"
---

# Tlon (plugin)

Tlon est un messager décentralisé construit sur Urbit. OpenClaw se connecte à votre ship Urbit et peut
répondre aux messages directs et aux messages de chat de groupe. Les réponses de groupe nécessitent une mention @ par défaut et peuvent
être davantage restreintes via des listes blanches.

Statut : supporté via plugin. Les messages directs, les mentions de groupe, les réponses de thread, le formatage de texte enrichi et
les téléchargements d'images sont supportés. Les réactions et les sondages ne sont pas encore supportés.

## Plugin requis

Tlon est fourni en tant que plugin et n'est pas inclus dans l'installation principale.

Installez via CLI (registre npm) :

```bash
openclaw plugins install @openclaw/tlon
```

Checkout local (lors de l'exécution à partir d'un dépôt git) :

```bash
openclaw plugins install ./extensions/tlon
```

Détails : [Plugins](/tools/plugin)

## Configuration

1. Installez le plugin Tlon.
2. Rassemblez l'URL de votre ship et le code de connexion.
3. Configurez `channels.tlon`.
4. Redémarrez la passerelle.
5. Envoyez un message direct au bot ou mentionnez-le dans un canal de groupe.

Configuration minimale (compte unique) :

```json5
{
  channels: {
    tlon: {
      enabled: true,
      ship: "~sampel-palnet",
      url: "https://your-ship-host",
      code: "lidlut-tabwed-pillex-ridrup",
      ownerShip: "~your-main-ship", // recommandé : votre ship, toujours autorisé
    },
  },
}
```

## Ships privés/LAN

Par défaut, OpenClaw bloque les noms d'hôte privés/internes et les plages d'adresses IP pour la protection SSRF.
Si votre ship s'exécute sur un réseau privé (localhost, adresse IP LAN ou nom d'hôte interne),
vous devez explicitement accepter :

```json5
{
  channels: {
    tlon: {
      url: "http://localhost:8080",
      allowPrivateNetwork: true,
    },
  },
}
```

Cela s'applique aux URL comme :

- `http://localhost:8080`
- `http://192.168.x.x:8080`
- `http://my-ship.local:8080`

⚠️ N'activez ceci que si vous faites confiance à votre réseau local. Ce paramètre désactive les protections SSRF
pour les requêtes vers l'URL de votre ship.

## Canaux de groupe

La découverte automatique est activée par défaut. Vous pouvez également épingler les canaux manuellement :

```json5
{
  channels: {
    tlon: {
      groupChannels: ["chat/~host-ship/general", "chat/~host-ship/support"],
    },
  },
}
```

Désactiver la découverte automatique :

```json5
{
  channels: {
    tlon: {
      autoDiscoverChannels: false,
    },
  },
}
```

## Contrôle d'accès

Liste blanche des messages directs (vide = aucun message direct autorisé, utilisez `ownerShip` pour le flux d'approbation) :

```json5
{
  channels: {
    tlon: {
      dmAllowlist: ["~zod", "~nec"],
    },
  },
}
```

Autorisation de groupe (restreinte par défaut) :

```json5
{
  channels: {
    tlon: {
      defaultAuthorizedShips: ["~zod"],
      authorization: {
        channelRules: {
          "chat/~host-ship/general": {
            mode: "restricted",
            allowedShips: ["~zod", "~nec"],
          },
          "chat/~host-ship/announcements": {
            mode: "open",
          },
        },
      },
    },
  },
}
```

## Système de propriétaire et d'approbation

Définissez un ship propriétaire pour recevoir les demandes d'approbation lorsque des utilisateurs non autorisés tentent d'interagir :

```json5
{
  channels: {
    tlon: {
      ownerShip: "~your-main-ship",
    },
  },
}
```

Le ship propriétaire est **automatiquement autorisé partout** — les invitations de message direct sont acceptées automatiquement et
les messages de canal sont toujours autorisés. Vous n'avez pas besoin d'ajouter le propriétaire à `dmAllowlist` ou
`defaultAuthorizedShips`.

Lorsqu'il est défini, le propriétaire reçoit des notifications de message direct pour :

- Les demandes de message direct des ships qui ne figurent pas dans la liste blanche
- Les mentions dans les canaux sans autorisation
- Les demandes d'invitation de groupe

## Paramètres d'acceptation automatique

Accepter automatiquement les invitations de message direct (pour les ships dans dmAllowlist) :

```json5
{
  channels: {
    tlon: {
      autoAcceptDmInvites: true,
    },
  },
}
```

Accepter automatiquement les invitations de groupe :

```json5
{
  channels: {
    tlon: {
      autoAcceptGroupInvites: true,
    },
  },
}
```

## Cibles de livraison (CLI/cron)

Utilisez-les avec `openclaw message send` ou la livraison cron :

- Message direct : `~sampel-palnet` ou `dm/~sampel-palnet`
- Groupe : `chat/~host-ship/channel` ou `group:~host-ship/channel`

## Compétence groupée

Le plugin Tlon inclut une compétence groupée ([`@tloncorp/tlon-skill`](https://github.com/tloncorp/tlon-skill))
qui fournit un accès CLI aux opérations Tlon :

- **Contacts** : obtenir/mettre à jour les profils, lister les contacts
- **Canaux** : lister, créer, publier des messages, récupérer l'historique
- **Groupes** : lister, créer, gérer les membres
- **Messages directs** : envoyer des messages, réagir aux messages
- **Réactions** : ajouter/supprimer des réactions emoji aux publications et messages directs
- **Paramètres** : gérer les permissions du plugin via des commandes slash

La compétence est automatiquement disponible lors de l'installation du plugin.

## Capacités

| Fonctionnalité      | Statut                                      |
| ------------------- | ------------------------------------------- |
| Messages directs    | ✅ Supporté                                 |
| Groupes/canaux      | ✅ Supporté (mention-gated par défaut)      |
| Threads             | ✅ Supporté (réponses automatiques en thread) |
| Texte enrichi       | ✅ Markdown converti au format Tlon         |
| Images              | ✅ Téléchargées vers le stockage Tlon       |
| Réactions           | ✅ Via [compétence groupée](#compétence-groupée) |
| Sondages            | ❌ Pas encore supporté                      |
| Commandes natives   | ✅ Supporté (propriétaire uniquement par défaut) |

## Dépannage

Exécutez d'abord cette échelle :

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
```

Défaillances courantes :

- **Messages directs ignorés** : l'expéditeur ne figure pas dans `dmAllowlist` et aucun `ownerShip` n'est configuré pour le flux d'approbation.
- **Messages de groupe ignorés** : canal non découvert ou expéditeur non autorisé.
- **Erreurs de connexion** : vérifiez que l'URL du ship est accessible ; activez `allowPrivateNetwork` pour les ships locaux.
- **Erreurs d'authentification** : vérifiez que le code de connexion est à jour (les codes tournent).

## Référence de configuration

Configuration complète : [Configuration](/gateway/configuration)

Options du fournisseur :

- `channels.tlon.enabled` : activer/désactiver le démarrage du canal.
- `channels.tlon.ship` : nom du ship Urbit du bot (par ex. `~sampel-palnet`).
- `channels.tlon.url` : URL du ship (par ex. `https://sampel-palnet.tlon.network`).
- `channels.tlon.code` : code de connexion du ship.
- `channels.tlon.allowPrivateNetwork` : autoriser les URL localhost/LAN (contournement SSRF).
- `channels.tlon.ownerShip` : ship propriétaire pour le système d'approbation (toujours autorisé).
- `channels.tlon.dmAllowlist` : ships autorisés à envoyer des messages directs (vide = aucun).
- `channels.tlon.autoAcceptDmInvites` : accepter automatiquement les messages directs des ships de la liste blanche.
- `channels.tlon.autoAcceptGroupInvites` : accepter automatiquement toutes les invitations de groupe.
- `channels.tlon.autoDiscoverChannels` : découvrir automatiquement les canaux de groupe (par défaut : true).
- `channels.tlon.groupChannels` : nids de canaux épinglés manuellement.
- `channels.tlon.defaultAuthorizedShips` : ships autorisés pour tous les canaux.
- `channels.tlon.authorization.channelRules` : règles d'autorisation par canal.
- `channels.tlon.showModelSignature` : ajouter le nom du modèle aux messages.

## Notes

- Les réponses de groupe nécessitent une mention (par ex. `~your-bot-ship`) pour répondre.
- Réponses de thread : si le message entrant se trouve dans un thread, OpenClaw répond dans le thread.
- Texte enrichi : le formatage Markdown (gras, italique, code, en-têtes, listes) est converti au format natif de Tlon.
- Images : les URL sont téléchargées vers le stockage Tlon et intégrées en tant que blocs d'image.
