---
summary: "Déplacer la route de réponse d'une session OpenClaw entre des canaux de chat liés"
title: "Amarrage de canal"
read_when:
  - Vous voulez que les réponses pour une session active se déplacent de Telegram vers Discord, Slack, Mattermost ou un autre canal lié
  - Vous configurez session.identityLinks pour les messages directs entre canaux
  - Une commande /dock indique que l'expéditeur n'est pas lié ou qu'aucune session active n'existe
---

L'amarrage de canal est le renvoi d'appel pour une session OpenClaw.

Il conserve le même contexte de conversation, mais change l'endroit où les
réponses futures pour cette session sont livrées.

## Exemple

Alice peut envoyer des messages à OpenClaw sur Telegram et Discord :

```json5
{
  session: {
    identityLinks: {
      alice: ["telegram:123", "discord:456"],
    },
  },
}
```

Si Alice envoie ceci depuis Telegram :

```text
/dock_discord
```

OpenClaw conserve le contexte de session actuel et change la route de réponse :

| Avant l'amarrage              | Après `/dock_discord`        |
| ----------------------------- | ---------------------------- |
| Les réponses vont à Telegram `123` | Les réponses vont à Discord `456` |

La session n'est pas recréée. L'historique de la transcription reste attaché à
la même session.

## Pourquoi l'utiliser

Utilisez l'amarrage quand une tâche commence dans une application de chat mais
que les réponses suivantes doivent arriver ailleurs.

Flux courant :

1. Démarrez une tâche d'agent depuis Telegram.
2. Passez à Discord où vous coordonnez le travail.
3. Envoyez `/dock_discord` depuis la session Telegram.
4. Conservez la même session OpenClaw, mais recevez les réponses futures dans Discord.

## Configuration requise

L'amarrage nécessite `session.identityLinks`. L'expéditeur source et le pair
cible doivent être dans le même groupe d'identité :

```json5
{
  session: {
    identityLinks: {
      alice: ["telegram:123", "discord:456", "slack:U123"],
    },
  },
}
```

Les valeurs sont des identifiants de pair préfixés par canal :

| Valeur         | Signification                      |
| -------------- | ---------------------------------- |
| `telegram:123` | Identifiant d'expéditeur Telegram `123`     |
| `discord:456`  | Identifiant de pair direct Discord `456` |
| `slack:U123`   | Identifiant d'utilisateur Slack `U123`         |

La clé canonique (`alice` ci-dessus) est seulement le nom du groupe d'identité
partagé. Les commandes d'amarrage utilisent les valeurs préfixées par canal
pour prouver que l'expéditeur source et le pair cible sont la même personne.

## Commandes

Les commandes d'amarrage sont générées à partir des plugins de canal chargés
qui supportent les commandes natives. Commandes groupées actuelles :

| Canal cible    | Commande           | Alias              |
| -------------- | ------------------ | ------------------ |
| Discord        | `/dock-discord`    | `/dock_discord`    |
| Mattermost     | `/dock-mattermost` | `/dock_mattermost` |
| Slack          | `/dock-slack`      | `/dock_slack`      |
| Telegram       | `/dock-telegram`   | `/dock_telegram`   |

Les alias avec tiret bas sont utiles sur les surfaces de commande natives
comme Telegram.

## Ce qui change

L'amarrage met à jour les champs de livraison de session active :

| Champ de session | Exemple après `/dock_discord`            |
| --------------- | ---------------------------------------- |
| `lastChannel`   | `discord`                                |
| `lastTo`        | `456`                                    |
| `lastAccountId` | le compte du canal cible, ou `default` |

Ces champs sont persistés dans le magasin de sessions et utilisés par la
livraison de réponses ultérieures pour cette session.

## Ce qui ne change pas

L'amarrage ne :

- crée pas de comptes de canal
- ne connecte pas un nouveau bot Discord, Telegram, Slack ou Mattermost
- n'accorde pas d'accès à un utilisateur
- ne contourne pas les listes blanches de canal ou les politiques de messages directs
- ne déplace pas l'historique de transcription vers une autre session
- ne fait pas partager une session à des utilisateurs non liés

Il change seulement la route de livraison pour la session actuelle.

## Dépannage

**La commande indique que l'expéditeur n'est pas lié.**

Ajoutez à la fois l'expéditeur actuel et le pair cible au même groupe
`session.identityLinks`. Par exemple, si l'expéditeur Telegram `123` doit
s'amarrer au pair Discord `456`, incluez à la fois `telegram:123` et
`discord:456`.

**La commande indique qu'aucune session active n'existe.**

Amarrez depuis une session de chat direct existante. La commande a besoin
d'une entrée de session active pour pouvoir persister la nouvelle route.

**Les réponses vont toujours à l'ancien canal.**

Vérifiez que la commande a répondu avec un message de succès, et confirmez
que l'identifiant du pair cible correspond à l'identifiant utilisé par ce
canal. L'amarrage change seulement la route de session active ; une autre
session peut toujours router ailleurs.

**Je dois revenir en arrière.**

Envoyez la commande correspondante pour le canal d'origine, comme
`/dock_telegram` ou `/dock-telegram`, depuis un expéditeur lié.
