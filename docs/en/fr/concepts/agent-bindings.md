---
summary: "Acheminer les comptes de canal et les conversations vers le bon agent OpenClaw"
title: "Liaisons d'agents"
read_when:
  - Acheminement des comptes de canal vers différents agents
  - Envoi d'une conversation à un agent spécialisé
  - Décision de savoir si l'agent par défaut est suffisant
---

Quand un message arrive sur un canal, OpenClaw doit décider quel agent y répond. Par défaut, c'est simple : l'agent marqué `default: true` reçoit tout. Une liaison d'agent remplace cette décision pour une partie de votre trafic — chaque liaison nomme un `agentId` et correspond à des faits de canal tels que le compte, le pair, la guilde, l'équipe ou les rôles Discord, et l'agent correspondant possède la session résultante.

Les liaisons ne choisissent que l'agent. Elles ne créent pas de comptes de canal et n'accordent pas d'accès — une liaison n'est consultée qu'après que le canal a déjà accepté le message via ses règles normales d'appairage, de liste blanche et de compte.

## Quand utiliser une liaison

Si chaque conversation peut partager un espace de travail, une politique de modèle et une limite de session, vous n'avez pas besoin de liaisons — l'agent par défaut est la bonne réponse. Utilisez les liaisons quand vous voulez une division stable, par exemple :

- un compte de canal par agent
- une boîte de réception d'assistance acheminée vers un espace de travail d'assistance
- un message direct ou un groupe acheminé vers un spécialiste
- une guilde, une équipe ou un rôle Discord acheminé différemment du reste d'un compte

Configurez d'abord le compte de canal, puis liez-le. Une liaison pointant vers un compte que le canal n'accepte jamais ne fait rien.

## Acheminer un compte vers un agent

Cet exemple garde `main` comme secours et achemine le compte Discord nommé `support` vers son propre agent et espace de travail :

```json5
{
  agents: {
    entries: {
      main: {
        default: true,
        workspace: "~/.openclaw/workspace",
      },
      support: {
        workspace: "~/.openclaw/workspace-support",
      },
    },
  },
  bindings: [
    {
      agentId: "support",
      comment: "Route the support bot account to the support agent",
      match: {
        channel: "discord",
        accountId: "support",
      },
    },
  ],
}
```

Les messages sur le compte `support` se résolvent maintenant en `agentId: "support"` ; tous les autres comptes Discord et tous les autres canaux continuent d'utiliser `main` sauf si une autre liaison correspond.

La configuration du routage est lue au démarrage, alors redémarrez la passerelle, puis vérifiez la liste et les comptes de canal :

```bash
openclaw agents list --bindings
openclaw channels status --probe
```

## Correspondre à une conversation spécifique

Ajoutez `match.peer` quand seul un message direct, un groupe ou un canal doit atteindre l'agent spécialisé :

```json5
{
  bindings: [
    {
      agentId: "support",
      match: {
        channel: "discord",
        accountId: "default",
        peer: {
          kind: "channel",
          id: "123456789012345678",
        },
      },
    },
  ],
}
```

`peer.kind` accepte `direct`, `group` ou `channel`. Utilisez l'ID de pair canonique du canal, pas un nom d'affichage.

## Champs de correspondance et précédence

Chaque liaison nécessite `agentId` et `match.channel`. Les champs de correspondance de route optionnels :

- `accountId` : un compte configuré. L'omettre ne correspond qu'au compte par défaut du canal ; `"*"` est un secours explicite à l'échelle du canal.
- `peer` : un pair direct, groupe ou canal concret ou générique
- `guildId` et `teamId` : contraintes d'espace de groupe spécifiques au canal
- `roles` : ID de rôles Discord, évalués avec la contrainte de guilde
- `session.dmScope` : un remplacement optionnel de portée de session pour les messages directs correspondants

La précédence est par spécificité : les correspondances de conversation concrète et d'espace de groupe l'emportent sur les secours de compte et de canal. Au sein du même niveau, la première liaison dans l'ordre de configuration l'emporte — mettez les règles étroites avant les larges quand elles partagent un niveau.

Le `bindings` de niveau supérieur accepte également les entrées `type: "acp"` pour les conversations ACP persistantes. Celles-ci nécessitent un `match.peer.id` concret et suivent le contrat d'identité de conversation ACP au lieu de la précédence de route ordinaire ; voir [Agents ACP](/fr/tools/acp-agents) quand c'est ce dont vous avez besoin.

## Erreurs courantes

### Omettre accountId pour signifier chaque compte

Un `accountId` omis ne correspond qu'au compte par défaut du canal. Si vous voulez un secours à l'échelle du canal, dites-le explicitement avec `accountId: "*"`.

### Lier à un agent inconnu

Le `agentId` doit exister sous `agents.entries`, et exactement une entrée doit être marquée `default: true`. Une liaison qui référence un agent manquant achemine silencieusement mal.

### Traiter les liaisons comme un contrôle d'accès

Les liaisons choisissent un agent pour les messages qui ont déjà été admis. L'appairage, `dmPolicy`, la politique de groupe et les listes blanches sont des contrôles séparés — configurez-les indépendamment.

## Connexes

- [Routage multi-agent](/fr/concepts/multi-agent)
- [Configuration d'agent](/fr/gateway/config-agents)
- [Routage de canal](/fr/channels/channel-routing)
