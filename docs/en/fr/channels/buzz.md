---
summary: "Connecter les agents OpenClaw aux salons Buzz"
read_when:
  - You want people to reach an OpenClaw agent from Buzz
  - You are setting up a Buzz bot identity and room access
  - You are troubleshooting a Buzz connection
title: "Buzz"
---

Buzz est un plugin de canal officiel qui connecte les agents OpenClaw aux salons d'équipe
dans un espace de travail Buzz hébergé ou auto-hébergé.

## Ce qu'il fait

- Reçoit les messages texte des salons Buzz approuvés
- Répond dans le même salon et fil de discussion
- Envoie des messages texte via l'outil `message` intégré d'OpenClaw
- Supporte les exigences de mention et les listes blanches d'expéditeurs
- Découvre les salons après l'approbation du bot
- Se reconnecte et évite de traiter deux fois le même message

Le plugin actuel supporte les salons de groupe et les messages texte. Les messages directs,
les médias et fichiers, les réactions natives, la création de salons et l'approbation automatique des administrateurs
ne sont pas encore supportés.

## Modèle d'identité Buzz et de salon

Buzz utilise des paires de clés Nostr pour l'identité :

- La **clé privée** permet à OpenClaw de s'authentifier et de signer les messages. Elle reste avec
  la Gateway.
- La **clé publique** identifie le bot. Les propriétaires de Buzz l'utilisent pour l'approbation du relais,
  les administrateurs de salon l'utilisent pour accorder le rôle **Bot**, et OpenClaw peut utiliser les clés publiques
  dans les listes blanches d'expéditeurs.

L'URL du relais pointe vers un espace de travail Buzz. Chaque salon a un UUID, et OpenClaw
traite chaque UUID configuré comme une conversation de groupe séparée. Une Gateway et
une identité de bot peuvent servir de nombreux salons ; vous n'avez pas besoin d'une Gateway par agent ou salon.

## Avant de commencer

Vous avez besoin de :

1. L'URL du relais `wss://` pour votre espace de travail Buzz.
2. Un propriétaire ou administrateur Buzz qui peut approuver une identité de bot.
3. Au moins un salon où le bot peut être ajouté avec le rôle **Bot**.

<Warning>
Ne donnez jamais à OpenClaw la clé privée d'un propriétaire Buzz humain. OpenClaw crée ou utilise une
identité de bot dédiée et affiche la clé publique qu'un administrateur doit approuver.
</Warning>

## Installation

```bash
openclaw plugins install @openclaw/buzz
```

Redémarrez la Gateway après l'installation ou la mise à jour du plugin.

## Configuration guidée

Exécutez :

```bash
openclaw channels add --channel buzz
```

Le flux de configuration parcourt les étapes suivantes :

1. Entrez l'URL du relais Buzz si elle n'est pas déjà configurée.
2. OpenClaw réutilise l'identité de bot configurée ou en génère une automatiquement.
3. Si le bot n'a pas encore accès aux salons, donnez la clé publique affichée à un
   propriétaire ou administrateur de salon Buzz.
4. OpenClaw attend la confirmation du rôle **Bot** par Buzz et continue
   automatiquement. Si l'attente automatique expire, réessayez la découverte authentifiée
   ou revenez en arrière sans modifier l'identité générée.
5. Si Buzz retourne un salon, OpenClaw le sélectionne. Si Buzz en retourne plusieurs,
   sélectionnez les salons à utiliser et le salon sortant par défaut.
6. OpenClaw enregistre la configuration et vérifie silencieusement le salon authentifié
   quand la Gateway est en cours d'exécution.

La configuration initiale accepte les messages normaux des membres actuels des salons configurés
sans nécessiter une mention du compositeur. Les paramètres existants de mention explicite et
de liste blanche d'expéditeurs sont préservés quand la configuration est réexécutée.

L'attente automatique d'accès aux salons est limitée. Si l'accès n'est pas accordé à temps,
la configuration reste ouverte et offre des contrôles authentifiés Réessayer/Retour. Chaque réessai
réutilise le même relais et la même identité de bot ; le délai d'expiration ne désactive pas Buzz ni ne quitte la configuration.

### Approbation du bot

Chaque salon cible doit contenir l'identité du bot avec le rôle **Bot**. Un
membre humain existant ou un rôle de membre de salon ordinaire ne suffit pas.

Buzz desktop ne peut pas assigner de manière fiable le rôle Bot à une identité OpenClaw gérée en externe. Utilisez la CLI Buzz en tant que propriétaire ou administrateur de salon humain existant :

```bash
buzz channels add-member \
  --channel <ROOM_UUID> \
  --pubkey <BOT_PUBLIC_KEY> \
  --role bot
```

Exécutez cette commande en tant que propriétaire ou administrateur humain existant. Ne donnez jamais à OpenClaw cette
clé privée humaine.

Après la connexion de la Gateway, OpenClaw préserve un nom d'affichage de profil Buzz existant non vide. Pour un nouveau profil, il utilise le nom du compte de canal Buzz configuré, puis le nom d'identité de l'agent unique routé vers les
salons Buzz configurés, et enfin `OpenClaw`. Cela remplace la clé publique raccourcie dans Buzz après l'actualisation de son cache de profil.

OpenClaw enregistre également la même identité publique dans l'annuaire des agents de Buzz. Il
préserve un profil d'annuaire d'agents existant et une politique d'ajout de canal ; pour un nouveau
profil, il autorise les utilisateurs Buzz autorisés à ajouter l'identité. Cela permet à Buzz
d'assigner le rôle **Bot** quand l'identité est invitée à des salons supplémentaires
au lieu de la traiter comme un membre normal. OpenClaw reçoit toujours les messages
uniquement des salons explicitement sélectionnés dans `channels.buzz.groups`.

Buzz affiche `owner unavailable` quand le profil du bot n'a pas d'attestation de propriétaire NIP-OA valide. Cela ne signifie pas que l'accès au salon a échoué. Quand
`channels.buzz.authTag` est configuré, OpenClaw inclut cette attestation dans le
profil publié pour que Buzz puisse afficher le propriétaire humain vérifié.

Pendant que la Gateway est connectée, OpenClaw publie et actualise la présence Buzz
éphémère du bot toutes les 30 secondes. Buzz supprime la présence quand la
dernière connexion Gateway authentifiée pour cette identité de bot se ferme, donc
plusieurs instances Gateway ne marquent pas incorrectement l'une l'autre comme hors ligne.

Le relais `just dev` Buzz local ne nécessite pas d'adhésion de relais séparée par défaut. Un relais hébergé ou fermé peut nécessiter que la clé publique du bot soit ajoutée à
la communauté de l'espace de travail d'abord. L'ajout d'une adhésion communautaire accorde l'accès au relais ;
cela n'ajoute pas l'identité à un salon avec le rôle Bot.

```bash
buzz-admin add-member --pubkey <BOT_PUBLIC_KEY> --role member
```

OpenClaw ne peut pas accorder l'accès au salon ou au relais. Il affiche uniquement la clé publique du bot
nécessaire par l'humain autorisé.

## Outils d'agent et messagerie

Le plugin Buzz n'ajoute pas d'outil d'agent séparé réservé à Buzz. Il enregistre Buzz
comme destination pour l'outil `message` intégré d'OpenClaw et la livraison de réponse normale.

Les agents peuvent :

- Répondre à un message Buzz entrant dans son salon ou fil de discussion
- Envoyer du texte à un salon Buzz approuvé
- Utiliser le salon par défaut configuré quand un flux de travail ne spécifie pas de cible
- Utiliser les compétences, la mémoire et les outils autorisés normaux de l'agent routé

Les humains et les automations peuvent tester le même chemin sortant depuis la CLI :

```bash
openclaw message send \
  --channel buzz \
  --target buzz:<ROOM_UUID> \
  --message "Hello from OpenClaw"
```

### Router les salons vers différents agents

Les liaisons OpenClaw standard peuvent envoyer chaque salon Buzz à un agent,
espace de travail ou modèle différent tandis qu'une Gateway et un bot Buzz les servent tous :

```json5
{
  agents: {
    list: [
      { id: "support", workspace: "~/.openclaw/workspace-support" },
      { id: "engineering", workspace: "~/.openclaw/workspace-engineering" },
    ],
  },
  bindings: [
    {
      agentId: "support",
      match: {
        channel: "buzz",
        peer: { kind: "group", id: "buzz:<SUPPORT_ROOM_UUID>" },
      },
    },
    {
      agentId: "engineering",
      match: {
        channel: "buzz",
        peer: { kind: "group", id: "buzz:<ENGINEERING_ROOM_UUID>" },
      },
    },
  ],
}
```

Sans une liaison spécifique au salon, le routage OpenClaw normal sélectionne l'agent par défaut. Voir [Routage des canaux](/fr/channels/channel-routing) pour la précédence de correspondance.

## Contrôle d'accès

Buzz applique deux contrôles indépendants :

- **Exiger des mentions** : l'agent répond uniquement quand le bot est mentionné.
- **Accès de l'expéditeur** : autoriser chaque membre actuel d'un salon approuvé, désactiver
  l'entrée du salon, ou restreindre davantage les membres du salon aux clés publiques Buzz sélectionnées.

La configuration guidée initiale autorise les messages normaux des membres actuels des salons sélectionnés. OpenClaw charge la liste des salons signée par le relais de Buzz avant d'accepter les messages,
vérifie l'adhésion en mémoire avant la déduplication persistante ou le travail d'agent, et actualise
la liste après les événements de changement d'adhésion Buzz. Il n'y a pas de requête de relais par message ou d'interrogation de Gateway.

Utilisez `groupPolicy: "allowlist"` avec `groupAllowFrom` dans la configuration manuelle
quand seuls les membres de salon spécifiques doivent pouvoir activer l'agent.
Définissez `requireMention: true` uniquement quand le client Buzz utilisé par ces membres peut
adresser l'identité du bot.

Ces contrôles décident qui peut démarrer une exécution d'agent ; ils ne limitent pas ce que
l'agent routé peut faire après l'acceptation d'un message. Traitez les messages de salon comme
une entrée non fiable, et configurez la [politique de sandbox et d'outils](/fr/gateway/sandbox-vs-tool-policy-vs-elevated)
de cet agent pour le niveau de confiance du salon.

## Configuration manuelle

La configuration guidée est recommandée. La configuration équivalente ressemble à :

```json5
{
  channels: {
    buzz: {
      name: "OpenClaw",
      relayUrl: "wss://buzz.example.com",
      privateKey: "nsec1...",
      groupPolicy: "open",
      groups: {
        "7c4a6d2a-2ed9-4b4e-a5e2-4d705ee9b34c": {
          requireMention: false,
        },
      },
      defaultTo: "7c4a6d2a-2ed9-4b4e-a5e2-4d705ee9b34c",
    },
  },
}
```

Pour une politique d'expéditeur plus étroite :

```json5
{
  channels: {
    buzz: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["<64_CHARACTER_HEX_SENDER_PUBLIC_KEY>"],
    },
  },
}
```

Les cibles de salon sont des UUID. Utilisez l'UUID du salon affiché lors de la découverte ou demandez-le à un administrateur de salon ; un nom d'affichage tel que `general` n'est pas une cible valide.

Pour la configuration manuelle, les entrées `groupAllowFrom` doivent utiliser la forme
hexadécimale de 64 caractères.

### Stockage de la clé du bot

Le chemin guidé par défaut réutilise l'identité de bot actuelle ou génère une clé privée
et la stocke dans `channels.buzz.privateKey`, suivant la convention de configuration en texte brut actuelle d'OpenClaw.

Pour une clé existante, la configuration peut utiliser du texte brut ou une `env`, `file`, ou
`exec` SecretRef existante. Voir [Gestion des secrets](/fr/gateway/secrets) pour la configuration du fournisseur.
Le compte par défaut peut également lire :

```bash
export BUZZ_RELAY_URL="wss://buzz.example.com"
export BUZZ_PRIVATE_KEY="nsec1..."
```

Si un opérateur d'espace de travail hébergé vous donne une valeur d'autorisation d'identité, définissez
`channels.buzz.authTag` ou `BUZZ_AUTH_TAG`. Il peut utiliser les mêmes formes de texte brut ou SecretRef que la clé privée. Traitez cette valeur déléguée et réutilisable comme un
secret : gardez-la hors des journaux, captures d'écran, chat et contrôle de source, et préférez une
SecretRef pour les déploiements persistants. Demandez un remplacement et révoquez l'ancienne
valeur chaque fois que l'identité du bot ou l'autorisation du relais change, ou si l'une ou l'autre
des informations d'identification peut avoir été exposée.

Les opérateurs auto-hébergés peuvent générer une clé manuellement pour la récupération ou la configuration avancée :

```bash
buzz-admin generate-key
```

## Vérifier la connexion

Exécutez la sonde de canal authentifiée :

```bash
openclaw channels status --channel buzz --probe
```

Une sonde réussie confirme que le bot peut s'authentifier et que Buzz signale
le salon sélectionné avec le rôle **Bot**.

Ensuite, envoyez un vrai message :

```bash
openclaw message send \
  --channel buzz \
  --target buzz:<ROOM_UUID> \
  --message "OpenClaw Buzz test"
```

Pour un aller-retour complet, demandez à un utilisateur Buzz autorisé de mentionner le bot et confirmez qu'OpenClaw
répond dans le salon.

## Faire tourner l'identité du bot

La rotation de l'identité du bot nécessite l'approbation de l'administrateur pour la nouvelle clé publique :

1. Générez une nouvelle identité de bot dédiée.
2. Demandez à un administrateur d'approuver sa clé publique pour le relais et chaque salon configuré.
3. Remplacez la clé privée configurée et redémarrez ou rechargez la Gateway.
4. Testez les messages sortants et entrants.
5. Supprimez l'ancienne clé publique des salons et du relais.

Complétez l'approbation avant de changer les clés pour minimiser les temps d'arrêt. La rotation n'est pas
automatique aujourd'hui.

## Limites actuelles et feuille de route

Ces domaines de suivi sont prévus mais ne font pas partie du plugin actuel :

- Messages directs
- Téléchargement ou téléchargement de médias et fichiers
- Réactions emoji natives
- Création ou administration de salons depuis OpenClaw
- Approbation automatique de l'adhésion au relais et du rôle de salon
- Rotation guidée de l'identité du bot

## Dépannage

| Symptôme                                     | À vérifier                                                                                                                                    |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Aucune salle n'est découverte                | Confirmez que cette clé publique de bot exacte se trouve dans la salle avec le rôle **Bot**, puis réexécutez la même commande de configuration. |
| L'authentification échoue                    | Vérifiez l'URL du relais, la clé privée du bot, l'adhésion au relais fermé et toute valeur d'autorisation fournie par l'opérateur.         |
| Un message ne peut pas être envoyé           | Confirmez que le bot est un membre de la salle avec le rôle **Bot** et que l'UUID est configuré.                                            |
| Le bot reçoit les messages mais ne répond pas | Confirmez que l'expéditeur est toujours un membre de la salle, puis vérifiez la liste d'autorisation facultative de l'expéditeur et l'exigence de mention. |
| La configuration indique que la passerelle n'est pas en cours d'exécution | Démarrez-la avec `openclaw gateway`, puis exécutez `openclaw channels status --probe`.                                                       |
| La découverte automatique de salle expire    | Accordez le rôle Bot, puis choisissez Réessayer ; la même identité reste active.                                                            |

## Liens connexes

- [Aperçu des canaux](/fr/channels)
- [Contrôles d'accès aux canaux](/fr/channels/groups)
- [Gestion des secrets](/fr/gateway/secrets)
- [Dépannage des canaux](/fr/channels/troubleshooting)
