---
summary: "Sub-agents: spawning isolated agent runs that announce results back to the requester chat"
read_when:
  - You want background/parallel work via the agent
  - You are changing sessions_spawn or sub-agent tool policy
  - You are implementing or troubleshooting thread-bound subagent sessions
title: "Sub-Agents"
---

# Sub-agents

Les sub-agents sont des exécutions d'agent en arrière-plan lancées à partir d'une exécution d'agent existante. Elles s'exécutent dans leur propre session (`agent:<agentId>:subagent:<uuid>`) et, une fois terminées, **annoncent** leur résultat au canal de chat du demandeur.

## Commande slash

Utilisez `/subagents` pour inspecter ou contrôler les exécutions de sub-agents pour la **session actuelle** :

- `/subagents list`
- `/subagents kill <id|#|all>`
- `/subagents log <id|#> [limit] [tools]`
- `/subagents info <id|#>`
- `/subagents send <id|#> <message>`
- `/subagents steer <id|#> <message>`
- `/subagents spawn <agentId> <task> [--model <model>] [--thinking <level>]`

Contrôles de liaison de thread :

Ces commandes fonctionnent sur les canaux qui supportent les liaisons de thread persistantes. Voir **Canaux supportant les threads** ci-dessous.

- `/focus <subagent-label|session-key|session-id|session-label>`
- `/unfocus`
- `/agents`
- `/session idle <duration|off>`
- `/session max-age <duration|off>`

`/subagents info` affiche les métadonnées d'exécution (statut, horodatages, ID de session, chemin de transcription, nettoyage).

### Comportement de lancement

`/subagents spawn` démarre un sub-agent en arrière-plan en tant que commande utilisateur, pas un relais interne, et envoie une mise à jour de fin unique au canal de chat du demandeur lorsque l'exécution se termine.

- La commande spawn est non-bloquante ; elle retourne un ID d'exécution immédiatement.
- À la fin, le sub-agent annonce un message de résumé/résultat au canal de chat du demandeur.
- Pour les lancements manuels, la livraison est résiliente :
  - OpenClaw essaie d'abord la livraison directe `agent` avec une clé d'idempotence stable.
  - Si la livraison directe échoue, elle bascule vers le routage en file d'attente.
  - Si le routage en file d'attente n'est toujours pas disponible, l'annonce est relancée avec un backoff exponentiel court avant l'abandon final.
- La remise de fin au demandeur est un contexte interne généré à l'exécution (pas du texte créé par l'utilisateur) et inclut :
  - `Result` (texte de réponse `assistant`, ou dernier `toolResult` si la réponse assistant est vide)
  - `Status` (`completed successfully` / `failed` / `timed out` / `unknown`)
  - statistiques compactes de runtime/tokens
  - une instruction de livraison indiquant à l'agent demandeur de réécrire dans une voix assistant normale (pas de transmission de métadonnées internes brutes)
- `--model` et `--thinking` remplacent les valeurs par défaut pour cette exécution spécifique.
- Utilisez `info`/`log` pour inspecter les détails et la sortie après la fin.
- `/subagents spawn` est en mode one-shot (`mode: "run"`). Pour les sessions persistantes liées aux threads, utilisez `sessions_spawn` avec `thread: true` et `mode: "session"`.
- Pour les sessions du harnais ACP (Codex, Claude Code, Gemini CLI), utilisez `sessions_spawn` avec `runtime: "acp"` et voir [ACP Agents](/tools/acp-agents).

Objectifs principaux :

- Paralléliser le travail de « recherche / tâche longue / outil lent » sans bloquer l'exécution principale.
- Garder les sub-agents isolés par défaut (séparation de session + sandboxing optionnel).
- Garder la surface d'outils difficile à mal utiliser : les sub-agents n'obtiennent **pas** les outils de session par défaut.
- Supporter la profondeur de nidification configurable pour les modèles d'orchestrateur.

Note de coût : chaque sub-agent a son **propre** contexte et utilisation de tokens. Pour les tâches lourdes ou répétitives, définissez un modèle moins cher pour les sub-agents et gardez votre agent principal sur un modèle de meilleure qualité.
Vous pouvez configurer cela via `agents.defaults.subagents.model` ou des remplacements par agent.

## Outil

Utilisez `sessions_spawn` :

- Lance une exécution de sub-agent (`deliver: false`, voie globale : `subagent`)
- Puis exécute une étape d'annonce et publie la réponse d'annonce au canal de chat du demandeur
- Modèle par défaut : hérite de l'appelant sauf si vous définissez `agents.defaults.subagents.model` (ou `agents.list[].subagents.model` par agent) ; un `sessions_spawn.model` explicite gagne toujours.
- Réflexion par défaut : hérite de l'appelant sauf si vous définissez `agents.defaults.subagents.thinking` (ou `agents.list[].subagents.thinking` par agent) ; un `sessions_spawn.thinking` explicite gagne toujours.
- Délai d'expiration d'exécution par défaut : si `sessions_spawn.runTimeoutSeconds` est omis, OpenClaw utilise `agents.defaults.subagents.runTimeoutSeconds` quand il est défini ; sinon il revient à `0` (pas de délai d'expiration).

Paramètres de l'outil :

- `task` (requis)
- `label?` (optionnel)
- `agentId?` (optionnel ; lancer sous un autre ID d'agent si autorisé)
- `model?` (optionnel ; remplace le modèle du sub-agent ; les valeurs invalides sont ignorées et le sub-agent s'exécute sur le modèle par défaut avec un avertissement dans le résultat de l'outil)
- `thinking?` (optionnel ; remplace le niveau de réflexion pour l'exécution du sub-agent)
- `runTimeoutSeconds?` (par défaut `agents.defaults.subagents.runTimeoutSeconds` quand défini, sinon `0` ; quand défini, l'exécution du sub-agent est abandonnée après N secondes)
- `thread?` (par défaut `false` ; quand `true`, demande la liaison de thread de canal pour cette session de sub-agent)
- `mode?` (`run|session`)
  - par défaut `run`
  - si `thread: true` et `mode` omis, la valeur par défaut devient `session`
  - `mode: "session"` nécessite `thread: true`
- `cleanup?` (`delete|keep`, par défaut `keep`)
- `sandbox?` (`inherit|require`, par défaut `inherit` ; `require` rejette le lancement sauf si le runtime enfant cible est sandboxé)
- `sessions_spawn` n'accepte **pas** les paramètres de livraison de canal (`target`, `channel`, `to`, `threadId`, `replyTo`, `transport`). Pour la livraison, utilisez `message`/`sessions_send` à partir de l'exécution lancée.

## Sessions liées aux threads

Quand les liaisons de thread sont activées pour un canal, un sub-agent peut rester lié à un thread afin que les messages utilisateur de suivi dans ce thread continuent à être routés vers la même session de sub-agent.

### Canaux supportant les threads

- Discord (actuellement le seul canal supporté) : supporte les sessions de sub-agent liées aux threads persistantes (`sessions_spawn` avec `thread: true`), les contrôles manuels de thread (`/focus`, `/unfocus`, `/agents`, `/session idle`, `/session max-age`), et les clés d'adaptateur `channels.discord.threadBindings.enabled`, `channels.discord.threadBindings.idleHours`, `channels.discord.threadBindings.maxAgeHours`, et `channels.discord.threadBindings.spawnSubagentSessions`.

Flux rapide :

1. Lancez avec `sessions_spawn` en utilisant `thread: true` (et optionnellement `mode: "session"`).
2. OpenClaw crée ou lie un thread à cette cible de session dans le canal actif.
3. Les réponses et messages de suivi dans ce thread sont routés vers la session liée.
4. Utilisez `/session idle` pour inspecter/mettre à jour le dé-focus automatique d'inactivité et `/session max-age` pour contrôler le plafond dur.
5. Utilisez `/unfocus` pour détacher manuellement.

Contrôles manuels :

- `/focus <target>` lie le thread actuel (ou en crée un) à une cible de sub-agent/session.
- `/unfocus` supprime la liaison pour le thread lié actuel.
- `/agents` liste les exécutions actives et l'état de liaison (`thread:<id>` ou `unbound`).
- `/session idle` et `/session max-age` ne fonctionnent que pour les threads liés focalisés.

Commutateurs de configuration :

- Par défaut global : `session.threadBindings.enabled`, `session.threadBindings.idleHours`, `session.threadBindings.maxAgeHours`
- Les clés de remplacement de canal et de liaison automatique de lancement sont spécifiques à l'adaptateur. Voir **Canaux supportant les threads** ci-dessus.

Voir [Configuration Reference](/gateway/configuration-reference) et [Slash commands](/tools/slash-commands) pour les détails actuels de l'adaptateur.

Liste blanche :

- `agents.list[].subagents.allowAgents` : liste des ID d'agent qui peuvent être ciblés via `agentId` (`["*"]` pour autoriser n'importe lequel). Par défaut : uniquement l'agent demandeur.
- Garde d'héritage de sandbox : si la session du demandeur est sandboxée, `sessions_spawn` rejette les cibles qui s'exécuteraient sans sandbox.

Découverte :

- Utilisez `agents_list` pour voir quels ID d'agent sont actuellement autorisés pour `sessions_spawn`.

Archive automatique :

- Les sessions de sub-agent sont automatiquement archivées après `agents.defaults.subagents.archiveAfterMinutes` (par défaut : 60).
- L'archive utilise `sessions.delete` et renomme la transcription en `*.deleted.<timestamp>` (même dossier).
- `cleanup: "delete"` archive immédiatement après l'annonce (conserve toujours la transcription via renommage).
- L'archive automatique est au mieux ; les minuteurs en attente sont perdus si la passerelle redémarre.
- `runTimeoutSeconds` n'archive **pas** automatiquement ; il arrête seulement l'exécution. La session reste jusqu'à l'archive automatique.
- L'archive automatique s'applique également aux sessions de profondeur 1 et profondeur 2.

## Sub-Agents imbriqués

Par défaut, les sub-agents ne peuvent pas lancer leurs propres sub-agents (`maxSpawnDepth: 1`). Vous pouvez activer un niveau de nidification en définissant `maxSpawnDepth: 2`, ce qui permet le **modèle d'orchestrateur** : principal → sub-agent orchestrateur → sub-sub-agents workers.

### Comment activer

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxSpawnDepth: 2, // allow sub-agents to spawn children (default: 1)
        maxChildrenPerAgent: 5, // max active children per agent session (default: 5)
        maxConcurrent: 8, // global concurrency lane cap (default: 8)
        runTimeoutSeconds: 900, // default timeout for sessions_spawn when omitted (0 = no timeout)
      },
    },
  },
}
```

### Niveaux de profondeur

| Profondeur | Forme de clé de session                      | Rôle                                          | Peut lancer ?                |
| ---------- | -------------------------------------------- | --------------------------------------------- | ---------------------------- |
| 0          | `agent:<id>:main`                            | Agent principal                               | Toujours                     |
| 1          | `agent:<id>:subagent:<uuid>`                 | Sub-agent (orchestrateur quand profondeur 2 autorisée) | Seulement si `maxSpawnDepth >= 2` |
| 2          | `agent:<id>:subagent:<uuid>:subagent:<uuid>` | Sub-sub-agent (worker feuille)                | Jamais                       |

### Chaîne d'annonce

Les résultats remontent la chaîne :

1. Le worker de profondeur 2 se termine → annonce à son parent (orchestrateur de profondeur 1)
2. L'orchestrateur de profondeur 1 reçoit l'annonce, synthétise les résultats, se termine → annonce au principal
3. L'agent principal reçoit l'annonce et la livre à l'utilisateur

Chaque niveau ne voit que les annonces de ses enfants directs.

### Politique d'outils par profondeur

- Le rôle et la portée de contrôle sont écrits dans les métadonnées de session au moment du lancement. Cela empêche les clés de session plates ou restaurées de regagner accidentellement les privilèges d'orchestrateur.
- **Profondeur 1 (orchestrateur, quand `maxSpawnDepth >= 2`)** : Obtient `sessions_spawn`, `subagents`, `sessions_list`, `sessions_history` pour pouvoir gérer ses enfants. Les autres outils de session/système restent refusés.
- **Profondeur 1 (feuille, quand `maxSpawnDepth == 1`)** : Pas d'outils de session (comportement par défaut actuel).
- **Profondeur 2 (worker feuille)** : Pas d'outils de session — `sessions_spawn` est toujours refusé à la profondeur 2. Ne peut pas lancer d'autres enfants.

### Limite de lancement par agent

Chaque session d'agent (à n'importe quelle profondeur) peut avoir au maximum `maxChildrenPerAgent` (par défaut : 5) enfants actifs à la fois. Cela empêche l'expansion incontrôlée d'un seul orchestrateur.

### Arrêt en cascade

L'arrêt d'un orchestrateur de profondeur 1 arrête automatiquement tous ses enfants de profondeur 2 :

- `/stop` dans le chat principal arrête tous les agents de profondeur 1 et en cascade vers leurs enfants de profondeur 2.
- `/subagents kill <id>` arrête un sub-agent spécifique et en cascade vers ses enfants.
