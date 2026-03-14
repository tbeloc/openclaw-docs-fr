---
read_when:
  - Expliquer comment les messages entrants se transforment en réponses
  - Clarifier le comportement des conversations, des modes de file d'attente ou du streaming
  - Documenter la visibilité du raisonnement et l'impact sur l'utilisation
summary: Flux de messages, conversations, files d'attente et visibilité du raisonnement
title: Messages
x-i18n:
  generated_at: "2026-02-03T10:05:22Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 147362b61bee21ee6e303654d970a052325f076ddb45814306053f70409737b5
  source_path: concepts/messages.md
  workflow: 15
---

# Messages

Cette page résume comment OpenClaw traite les messages entrants, les conversations, les files d'attente, le streaming et la visibilité du raisonnement.

## Flux de messages (aperçu de haut niveau)

```
Message entrant
  -> Routage/liaison -> Clé de session
  -> File d'attente (s'il y a une tâche en cours)
  -> Exécution de l'agent (streaming + outils)
  -> Réponse sortante (limites de canal + chunking)
```

Les éléments de configuration clés se trouvent dans la configuration :

- `messages.*` pour les préfixes, la file d'attente et le comportement des groupes.
- `agents.defaults.*` pour le streaming par chunks et les valeurs par défaut de chunking.
- Les remplacements de canal (`channels.whatsapp.*`, `channels.telegram.*`, etc.) pour les limites et les commutateurs de streaming.

Voir le schéma complet dans [Configuration](/gateway/configuration).

## Dédoublonnage entrant

Les canaux peuvent relancer le même message après une reconnexion. OpenClaw maintient un cache à court terme, indexé par canal/compte/pair/session/ID de message, donc les relances ne déclenchent pas une autre exécution d'agent.

## Débounce entrant

Les messages rapides et consécutifs du **même expéditeur** peuvent être fusionnés en un seul tour d'agent via `messages.inbound`. Le débounce est limité par canal + session et utilise le message le plus récent pour la gestion des threads/ID de réponse.

Configuration (défaut global + remplacements par canal) :

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

Remarques :

- Le débounce s'applique uniquement aux messages **texte brut** ; les médias/pièces jointes sont vidés immédiatement.
- Les commandes de contrôle contournent le débounce et restent indépendantes.

## Sessions et appareils

Les sessions sont détenues par la passerelle Gateway, et non par le client.

- Les chats directs sont fusionnés dans la clé de session principale de l'agent.
- Les groupes/canaux obtiennent leurs propres clés de session.
- Le stockage de session et les journaux sont conservés sur l'hôte de la passerelle Gateway.

Plusieurs appareils/canaux peuvent être mappés à la même session, mais l'historique ne sera pas complètement synchronisé avec chaque client. Recommandation : utilisez un seul appareil principal pour les longues conversations, afin d'éviter les divergences de contexte. L'interface de contrôle et le TUI affichent toujours l'historique de session supporté par la passerelle Gateway, ils sont donc la source de vérité.

Détails : [Gestion des sessions](/concepts/session).

## Corps entrant et contexte historique

OpenClaw sépare le **corps du prompt** du **corps de la commande** :

- `Body` : texte du prompt envoyé à l'agent. Cela peut inclure l'enveloppe du canal et un wrapper historique optionnel.
- `CommandBody` : texte utilisateur brut pour l'analyse des directives/commandes.
- `RawBody` : ancien alias pour `CommandBody` (conservé pour la compatibilité).

Lorsque le canal fournit un historique, un wrapper partagé est utilisé :

- `[Chat messages since your last reply - for context]`
- `[Current message - respond to this]`

Pour les **chats non directs** (groupes/canaux/salons), le **corps du message actuel** est préfixé avec une étiquette d'expéditeur (avec le même style utilisé pour les entrées historiques). Cela maintient la cohérence entre les messages en temps réel dans le prompt de l'agent et les messages en file d'attente/historique.

Le tampon historique est **en attente uniquement** : il contient des messages de groupe qui n'ont *pas* déclenché une exécution (par exemple, les messages contrôlés par mention), et **exclut** les messages déjà dans l'enregistrement de session.

L'extraction de directives s'applique uniquement à la section **message actuel**, donc l'historique reste intact. Les canaux qui enveloppent l'historique doivent définir `CommandBody` (ou `RawBody`) sur le texte du message original, et laisser `Body` comme prompt combiné. Le tampon historique peut être configuré via `messages.groupChat.historyLimit` (défaut global) et les remplacements par canal (comme `channels.slack.historyLimit` ou `channels.telegram.accounts.<id>.historyLimit`) (définir `0` pour désactiver).

## File d'attente et messages de suivi

Si une exécution est déjà en cours, un message entrant peut être mis en file d'attente, importé dans l'exécution actuelle, ou collecté pour les tours suivants.

- Configuré via `messages.queue` (et `messages.queue.byChannel`).
- Modes : `interrupt`, `steer`, `followup`, `collect`, et variantes de backlog.

Détails : [File d'attente](/concepts/queue).

## Streaming, chunking et batching

Le streaming par chunks envoie des réponses partielles au fur et à mesure que le modèle génère des blocs de texte. Les chunks respectent les limites de texte du canal, en évitant de diviser le code entre clôtures.

Paramètres clés :

- `agents.defaults.blockStreamingDefault` (`on|off`, par défaut off)
- `agents.defaults.blockStreamingBreak` (`text_end|message_end`)
- `agents.defaults.blockStreamingChunk` (`minChars|maxChars|breakPreference`)
- `agents.defaults.blockStreamingCoalesce` (batching basé sur l'inactivité)
- `agents.defaults.humanDelay` (pauses humanisées entre les réponses par chunks)
- Remplacements de canal : `*.blockStreaming` et `*.blockStreamingCoalesce` (les canaux non-Telegram nécessitent un paramètre explicite `*.blockStreaming: true`)

Détails : [Streaming + Chunking](/concepts/streaming).

## Visibilité du raisonnement et tokens

OpenClaw peut afficher ou masquer le raisonnement du modèle :

- `/reasoning on|off|stream` contrôle la visibilité.
- Lorsque le modèle produit du contenu de raisonnement, il compte toujours dans l'utilisation des tokens.
- Telegram supporte le streaming du raisonnement dans des bulles de brouillon.

Détails : [Directives de pensée + raisonnement](/tools/thinking) et [Utilisation des tokens](/reference/token-use).

## Préfixes, threads et réponses

Le format des messages sortants est configuré de manière centralisée dans `messages` :

- `messages.responsePrefix` (préfixe sortant) et `channels.whatsapp.messagePrefix` (préfixe entrant WhatsApp)
- Threads de réponse via `replyToMode` et les valeurs par défaut par canal

Détails : [Configuration](/gateway/configuration#messages) et documentation des canaux.
