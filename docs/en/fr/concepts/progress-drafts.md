---
summary: "Brouillons de progression : un message de travail en cours visible qui se met à jour pendant qu'un agent s'exécute"
read_when:
  - Configuring visible progress updates for long-running chat turns
  - Choosing between partial, block, and progress streaming modes
  - Explaining how OpenClaw updates one channel message while work is in progress
  - Troubleshooting progress drafts, standalone progress messages, or finalization fallback
title: "Brouillons de progression"
---

Les brouillons de progression rendent les tours d'agent longue durée vivants dans le chat sans transformer la conversation en pile de réponses de statut temporaires.

Lorsque les brouillons de progression sont activés, OpenClaw crée un message de travail en cours visible uniquement après que le tour prouve qu'il effectue un vrai travail, le met à jour pendant que l'agent lit, planifie, appelle des outils ou attend une approbation, puis transforme ce brouillon en réponse finale lorsque le canal peut le faire en toute sécurité.

```text
Shelling...
📖 from docs/concepts/progress-drafts.md
🔎 Web Search: for "discord edit message"
🛠️ Bash: run tests
```

Utilisez les brouillons de progression lorsque vous voulez un message de statut unique et soigné pendant le travail intensif en outils et la réponse finale lorsque le tour est terminé.

## Démarrage rapide

Activez les brouillons de progression par canal avec `streaming.mode: "progress"` :

```json5
{
  channels: {
    discord: {
      streaming: {
        mode: "progress",
      },
    },
  },
}
```

C'est généralement suffisant. OpenClaw choisira automatiquement un libellé d'un mot, attendra que le travail dure au moins cinq secondes ou émette un deuxième événement de travail, ajoutera des lignes de progression compactes pendant que le travail utile se produit, et supprimera les bavardages de progression autonomes en double pour ce tour.

## Ce que les utilisateurs voient

Un brouillon de progression a deux parties :

| Partie          | Objectif                                                                                    |
| --------------- | ------------------------------------------------------------------------------------------- |
| Libellé         | Une courte ligne de démarrage/statut telle que `Thinking...` ou `Shelling...`.              |
| Lignes de progression | Mises à jour compactes d'exécution utilisant les mêmes icônes d'outils et le formateur de détail que la sortie détaillée. |

Le libellé apparaît après que l'agent commence un travail significatif et reste occupé pendant cinq secondes ou émet un deuxième événement de travail. Il fait partie de la liste de lignes de progression roulante, donc le statut de démarrage disparaît une fois que suffisamment de travail concret apparaît. Les réponses en texte brut uniquement n'affichent pas de brouillon de progression. Les lignes de progression sont ajoutées uniquement lorsque l'agent émet des mises à jour de travail utiles, par exemple `🛠️ Bash: run tests`, `🔎 Web Search: for "discord edit message"`, ou `✍️ Write: to /tmp/file`.
Par défaut, ils utilisent le même mode d'explication compacte que `/verbose` ; définissez `agents.defaults.toolProgressDetail: "raw"` lors du débogage et vous voulez également que les commandes/détails bruts soient ajoutés.
La réponse finale remplace le brouillon lorsque c'est possible ; sinon OpenClaw envoie la réponse finale normalement et nettoie ou arrête de mettre à jour le brouillon selon le transport du canal.

## Choisir un mode

`channels.<channel>.streaming.mode` contrôle le comportement visible en cours d'exécution :

| Mode       | Meilleur pour                    | Ce qui apparaît dans le chat                      |
| ---------- | -------------------------------- | ------------------------------------------------- |
| `off`      | Canaux silencieux                | Uniquement la réponse finale.                     |
| `partial`  | Regarder le texte de réponse apparaître | Un brouillon édité avec le dernier texte de réponse. |
| `block`    | Chunks d'aperçu de réponse plus grands | Un aperçu mis à jour ou ajouté en chunks plus grands. |
| `progress` | Tours longs ou intensifs en outils | Un brouillon de statut, puis la réponse finale.   |

Choisissez `progress` lorsque les utilisateurs se soucient davantage de « ce qui se passe » que de regarder le texte de réponse s'afficher jeton par jeton.

Choisissez `partial` lorsque la réponse elle-même est le signal de progression.

Choisissez `block` lorsque vous voulez des mises à jour d'aperçu de brouillon en chunks de texte plus grands. Sur Discord et Telegram, `streaming.mode: "block"` est toujours la diffusion d'aperçu, pas la livraison de bloc normal. Utilisez `streaming.block.enabled` ou l'héritage `blockStreaming` lorsque vous voulez des réponses de bloc normal.

## Configurer les libellés

Les libellés de progression se trouvent sous `channels.<channel>.streaming.progress`.

Le libellé par défaut est `auto`, qui choisit parmi le pool de libellés d'un mot avec ellipse intégré d'OpenClaw :

```text
Thinking...
Shelling...
Scuttling...
Clawing...
Pinching...
Molting...
Bubbling...
Tiding...
Reefing...
Cracking...
Sifting...
Brining...
Nautiling...
Krilling...
Barnacling...
Lobstering...
Tidepooling...
Pearling...
Snapping...
Surfacing...
```

Utilisez un libellé fixe :

```json5
{
  channels: {
    discord: {
      streaming: {
        mode: "progress",
        progress: {
          label: "Investigating",
        },
      },
    },
  },
}
```

Utilisez votre propre pool de libellés automatiques :

```json5
{
  channels: {
    discord: {
      streaming: {
        mode: "progress",
        progress: {
          label: "auto",
          labels: ["Checking", "Reading", "Testing", "Finishing"],
        },
      },
    },
  },
}
```

Masquez le libellé et affichez uniquement les lignes de progression :

```json5
{
  channels: {
    discord: {
      streaming: {
        mode: "progress",
        progress: {
          label: false,
        },
      },
    },
  },
}
```

## Contrôler les lignes de progression

Les lignes de progression sont activées par défaut en mode progression. Elles proviennent d'événements d'exécution réels : démarrages d'outils, mises à jour d'éléments, plans de tâches, approbations, sortie de commande, résumés de correctifs et activités d'agent similaires.

OpenClaw utilise le même formateur pour les brouillons de progression et `/verbose` :

```json5
{
  agents: {
    defaults: {
      toolProgressDetail: "explain", // explain | raw
    },
  },
}
```

`"explain"` est la valeur par défaut et maintient les brouillons stables avec des libellés concis comme `🛠️ check JS syntax for /tmp/app.js`. `"raw"` ajoute la commande/le détail sous-jacent lorsqu'il est disponible, ce qui est utile lors du débogage mais plus bruyant dans le chat.

Par exemple, la même commande apparaît différemment selon le mode de détail :

| Mode      | Ligne de progression                                           |
| --------- | -------------------------------------------------------------- |
| `explain` | `🛠️ check JS syntax for /tmp/app.js`                           |
| `raw`     | `🛠️ check JS syntax for /tmp/app.js, node --check /tmp/app.js` |

Limitez le nombre de lignes visibles :

```json5
{
  channels: {
    discord: {
      streaming: {
        mode: "progress",
        progress: {
          maxLines: 4,
        },
      },
    },
  },
}
```

Les lignes de progression sont compactées automatiquement pour réduire le reflux de bulles de chat pendant que le brouillon est édité.

OpenClaw tronque les lignes de progression longues par défaut afin que les éditions de brouillon répétées ne s'enroulent pas différemment à chaque mise à jour. Le budget par défaut par ligne est de 120 caractères. La prose se coupe à une limite de mot, tandis que les longs détails tels que les chemins ou les commandes brutes sont raccourcis avec une ellipse au milieu afin que le suffixe reste visible.

Ajustez le budget par ligne :

```json5
{
  channels: {
    discord: {
      streaming: {
        mode: "progress",
        progress: {
          maxLineChars: 160,
        },
      },
    },
  },
}
```

Slack peut rendre les lignes de progression sous forme de champs Block Kit structurés au lieu d'un seul corps de texte :

```json5
{
  channels: {
    slack: {
      streaming: {
        mode: "progress",
        progress: {
          render: "rich",
        },
      },
    },
  },
}
```

Le rendu riche conserve le même secours en texte brut afin que les canaux et les clients qui ne supportent pas la forme plus riche puissent toujours afficher le texte de progression compact.

Conservez le brouillon de progression unique mais masquez les lignes d'outils et de tâches :

```json5
{
  channels: {
    discord: {
      streaming: {
        mode: "progress",
        progress: {
          toolProgress: false,
        },
      },
    },
  },
}
```

Avec `toolProgress: false`, OpenClaw supprime toujours les anciens messages de progression d'outils autonomes pour ce tour. Le canal reste visuellement silencieux jusqu'à la réponse finale, sauf pour le libellé s'il en est configuré un.

## Comportement du canal

Chaque canal utilise le transport le plus propre qu'il supporte :

| Canal           | Transport de progression                | Notes                                                                 |
| --------------- | -------------------------------------- | --------------------------------------------------------------------- |
| Discord         | Envoyer un message, puis l'éditer.     | Les éditions de texte final en place lorsqu'elles tiennent dans un message d'aperçu sûr. |
| Matrix          | Envoyer un événement, puis l'éditer.   | La configuration de diffusion au niveau du compte contrôle les brouillons au niveau du compte. |
| Microsoft Teams | Flux natif Teams dans les chats personnels. | `streaming.mode: "block"` mappe à la livraison de bloc Teams. |
| Slack           | Flux natif ou brouillon éditable.      | La disponibilité des threads affecte si la diffusion native peut être utilisée. |
| Telegram        | Envoyer un message, puis l'éditer.     | Les anciens brouillons visibles peuvent être remplacés afin que les horodatages finaux restent utiles. |
| Mattermost      | Brouillon éditable.                    | L'activité des outils est repliée dans le même brouillon de style post. |

Les canaux sans support d'édition sûr reviennent généralement aux indicateurs de saisie ou à la livraison finale uniquement.

## Finalisation

Lorsque la réponse finale est prête, OpenClaw essaie de garder le chat propre :

- Si le brouillon peut devenir en toute sécurité la réponse finale, OpenClaw l'édite en place.
- Si le canal utilise la diffusion de progression native, OpenClaw finalise ce flux lorsque le transport natif accepte le texte final.
- Si la réponse finale contient des médias, une invite d'approbation, une cible de réponse explicite, trop de chunks ou une édition/envoi échoué, OpenClaw envoie la réponse finale via le chemin de livraison du canal normal.

Le chemin de secours est intentionnel. Il est préférable d'envoyer une réponse finale fraîche que de perdre du texte, de mal enfiler une réponse ou de remplacer un brouillon par une charge utile que le canal ne peut pas représenter en toute sécurité.

## Dépannage

**Je ne vois que la réponse finale.**

Vérifiez que `channels.<channel>.streaming.mode` est défini sur `progress` pour le compte ou le canal qui a traité le message. Certains chemins de réponse de groupe ou de citation peuvent désactiver les aperçus de brouillon pour un tour lorsque le canal ne peut pas éditer en toute sécurité le bon message.

**Je vois le libellé mais pas les lignes d'outils.**

Vérifiez `streaming.progress.toolProgress`. S'il est `false`, OpenClaw conserve le comportement de brouillon unique mais masque les lignes de progression des outils et des tâches.

**Je vois un message final frais au lieu d'un brouillon édité.**

C'est un secours de sécurité. Cela peut se produire pour les réponses médias, les réponses longues, les cibles de réponse explicites, les anciens brouillons Telegram, les cibles de thread Slack manquantes, les messages d'aperçu supprimés ou la finalisation du flux natif échouée.

**Je vois toujours des messages de progression autonomes.**

Le mode progression supprime les messages de progression d'outils autonomes par défaut lorsqu'un brouillon est actif. Si des messages autonomes apparaissent toujours, vérifiez que le tour utilise réellement le mode progression et non `streaming.mode: "off"` ou un chemin de canal qui ne peut pas créer de brouillon pour ce message.

**Teams se comporte différemment de Discord ou Telegram.**

Microsoft Teams utilise un flux natif dans les chats personnels au lieu du transport d'aperçu générique d'envoi et d'édition. Teams traite également `streaming.mode: "block"` comme la livraison de bloc Teams car il n'a pas le même mode de bloc d'aperçu de brouillon utilisé par Discord et Telegram.

## Connexes

- [Streaming and chunking](/fr/concepts/streaming)
- [Messages](/fr/concepts/messages)
- [Channel configuration](/fr/gateway/config-channels)
- [Discord](/fr/channels/discord)
- [Matrix](/fr/channels/matrix)
- [Microsoft Teams](/fr/channels/msteams)
- [Slack](/fr/channels/slack)
- [Telegram](/fr/channels/telegram)
