---
summary: "Flux de messages, sessions, mise en file d'attente et visibilité du raisonnement"
read_when:
  - Explaining how inbound messages become replies
  - Clarifying sessions, queueing modes, or streaming behavior
  - Documenting reasoning visibility and usage implications
title: "Messages"
---

# Messages

Cette page explique comment OpenClaw gère les messages entrants, les sessions, la mise en file d'attente,
le streaming et la visibilité du raisonnement.

## Flux de messages (haut niveau)

```
Message entrant
  -> routage/liaisons -> clé de session
  -> file d'attente (si une exécution est active)
  -> exécution de l'agent (streaming + outils)
  -> réponses sortantes (limites de canal + chunking)
```

Les paramètres clés se trouvent dans la configuration :

- `messages.*` pour les préfixes, la mise en file d'attente et le comportement de groupe.
- `agents.defaults.*` pour les valeurs par défaut du streaming de bloc et du chunking.
- Remplacements de canal (`channels.whatsapp.*`, `channels.telegram.*`, etc.) pour les limites et les bascules de streaming.

Voir [Configuration](/fr/gateway/configuration) pour le schéma complet.

## Déduplications entrantes

Les canaux peuvent relancer le même message après les reconnexions. OpenClaw maintient un
cache de courte durée indexé par canal/compte/pair/session/ID de message afin que les
livraisons en double ne déclenchent pas une autre exécution d'agent.

## Débouncing entrant

Les messages consécutifs rapides du **même expéditeur** peuvent être regroupés en un seul
tour d'agent via `messages.inbound`. Le débouncing est limité par canal + conversation
et utilise le message le plus récent pour le threading de réponse/les ID.

Configuration (valeur par défaut globale + remplacements par canal) :

```json5
{
  messages: {
    inbound: {
      debounceMs: 2000,
      byChannel: {
        whatsapp: 5000,
        slack: 1500,
        discord: 1500,
      },
    },
  },
}
```

Notes :

- Le débouncing s'applique aux messages **texte uniquement** ; les médias/pièces jointes sont vidés immédiatement.
- Les commandes de contrôle contournent le débouncing pour rester autonomes.

## Sessions et appareils

Les sessions sont détenues par la passerelle, pas par les clients.

- Les chats directs s'effondrent dans la clé de session principale de l'agent.
- Les groupes/canaux obtiennent leurs propres clés de session.
- Le magasin de sessions et les transcriptions vivent sur l'hôte de la passerelle.

Plusieurs appareils/canaux peuvent être mappés à la même session, mais l'historique n'est pas
entièrement synchronisé avec chaque client. Recommandation : utilisez un appareil principal pour
les longues conversations afin d'éviter un contexte divergent. L'interface de contrôle et le TUI
affichent toujours la transcription de session soutenue par la passerelle, ils sont donc la source
de vérité.

Détails : [Gestion des sessions](/fr/concepts/session).

## Corps entrants et contexte historique

OpenClaw sépare le **corps du prompt** du **corps de la commande** :

- `Body` : texte du prompt envoyé à l'agent. Cela peut inclure des enveloppes de canal et
  des wrappers d'historique optionnels.
- `CommandBody` : texte utilisateur brut pour l'analyse des directives/commandes.
- `RawBody` : alias hérité pour `CommandBody` (conservé pour la compatibilité).

Quand un canal fournit l'historique, il utilise un wrapper partagé :

- `[Messages de chat depuis votre dernière réponse - pour le contexte]`
- `[Message actuel - répondez à ceci]`

Pour les **chats non directs** (groupes/canaux/salons), le **corps du message actuel** est préfixé avec
l'étiquette de l'expéditeur (même style utilisé pour les entrées d'historique). Cela maintient la cohérence
entre les messages en temps réel et les messages en file d'attente/historique dans le prompt de l'agent.

Les tampons d'historique sont **en attente uniquement** : ils incluent les messages de groupe qui n'ont _pas_
déclenché une exécution (par exemple, les messages gérés par mention) et **excluent** les messages
déjà dans la transcription de session.

Le stripping de directive s'applique uniquement à la section **message actuel** afin que l'historique
reste intact. Les canaux qui enveloppent l'historique doivent définir `CommandBody` (ou
`RawBody`) au texte du message original et garder `Body` comme le prompt combiné.
Les tampons d'historique sont configurables via `messages.groupChat.historyLimit` (valeur par défaut
globale) et les remplacements par canal comme `channels.slack.historyLimit` ou
`channels.telegram.accounts.<id>.historyLimit` (définissez `0` pour désactiver).

## Mise en file d'attente et suites

Si une exécution est déjà active, les messages entrants peuvent être mis en file d'attente, dirigés vers
l'exécution actuelle ou collectés pour un tour de suivi.

- Configurez via `messages.queue` (et `messages.queue.byChannel`).
- Modes : `interrupt`, `steer`, `followup`, `collect`, plus les variantes de backlog.

Détails : [Mise en file d'attente](/fr/concepts/queue).

## Streaming, chunking et batching

Le streaming de bloc envoie des réponses partielles au fur et à mesure que le modèle produit des blocs de texte.
Le chunking respecte les limites de texte du canal et évite de diviser le code entre guillemets.

Paramètres clés :

- `agents.defaults.blockStreamingDefault` (`on|off`, par défaut off)
- `agents.defaults.blockStreamingBreak` (`text_end|message_end`)
- `agents.defaults.blockStreamingChunk` (`minChars|maxChars|breakPreference`)
- `agents.defaults.blockStreamingCoalesce` (batching basé sur l'inactivité)
- `agents.defaults.humanDelay` (pause de type humain entre les réponses de bloc)
- Remplacements de canal : `*.blockStreaming` et `*.blockStreamingCoalesce` (les canaux non-Telegram nécessitent un `*.blockStreaming: true` explicite)

Détails : [Streaming + chunking](/fr/concepts/streaming).

## Visibilité du raisonnement et tokens

OpenClaw peut exposer ou masquer le raisonnement du modèle :

- `/reasoning on|off|stream` contrôle la visibilité.
- Le contenu du raisonnement compte toujours vers l'utilisation des tokens lorsqu'il est produit par le modèle.
- Telegram supporte le flux de raisonnement dans la bulle de brouillon.

Détails : [Directives de réflexion + raisonnement](/fr/tools/thinking) et [Utilisation des tokens](/fr/reference/token-use).

## Préfixes, threading et réponses

Le formatage des messages sortants est centralisé dans `messages` :

- `messages.responsePrefix`, `channels.<channel>.responsePrefix`, et `channels.<channel>.accounts.<id>.responsePrefix` (cascade de préfixe sortant), plus `channels.whatsapp.messagePrefix` (préfixe entrant WhatsApp)
- Threading de réponse via `replyToMode` et les valeurs par défaut par canal

Détails : [Configuration](/fr/gateway/configuration#messages) et documentation des canaux.
