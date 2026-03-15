---
summary: "Outils de session d'agent pour lister les sessions, récupérer l'historique et envoyer des messages entre sessions"
read_when:
  - Adding or modifying session tools
title: "Outils de Session"
---

# Outils de Session

Objectif : ensemble d'outils petit et difficile à mal utiliser pour que les agents puissent lister les sessions, récupérer l'historique et envoyer vers une autre session.

## Noms des Outils

- `sessions_list`
- `sessions_history`
- `sessions_send`
- `sessions_spawn`

## Modèle Clé

- Le bucket de chat direct principal est toujours la clé littérale `"main"` (résolue à la clé principale de l'agent actuel).
- Les chats de groupe utilisent `agent:<agentId>:<channel>:group:<id>` ou `agent:<agentId>:<channel>:channel:<id>` (passez la clé complète).
- Les tâches cron utilisent `cron:<job.id>`.
- Les hooks utilisent `hook:<uuid>` sauf s'ils sont explicitement définis.
- Les sessions de nœud utilisent `node-<nodeId>` sauf s'ils sont explicitement définis.

`global` et `unknown` sont des valeurs réservées et ne sont jamais listées. Si `session.scope = "global"`, nous l'alias en `main` pour tous les outils afin que les appelants ne voient jamais `global`.

## sessions_list

Lister les sessions sous forme de tableau de lignes.

Paramètres :

- `kinds?: string[]` filtre : l'un de `"main" | "group" | "cron" | "hook" | "node" | "other"`
- `limit?: number` nombre maximum de lignes (par défaut : valeur par défaut du serveur, limité par ex. 200)
- `activeMinutes?: number` uniquement les sessions mises à jour dans les N dernières minutes
- `messageLimit?: number` 0 = pas de messages (par défaut 0) ; >0 = inclure les N derniers messages

Comportement :

- `messageLimit > 0` récupère `chat.history` par session et inclut les N derniers messages.
- Les résultats des outils sont filtrés dans la sortie de la liste ; utilisez `sessions_history` pour les messages d'outils.
- Lors de l'exécution dans une session d'agent **en sandbox**, les outils de session par défaut à la **visibilité spawned uniquement** (voir ci-dessous).

Forme de ligne (JSON) :

- `key` : clé de session (chaîne)
- `kind` : `main | group | cron | hook | node | other`
- `channel` : `whatsapp | telegram | discord | signal | imessage | webchat | internal | unknown`
- `displayName` (étiquette d'affichage de groupe si disponible)
- `updatedAt` (ms)
- `sessionId`
- `model`, `contextTokens`, `totalTokens`
- `thinkingLevel`, `verboseLevel`, `systemSent`, `abortedLastRun`
- `sendPolicy` (remplacement de session s'il est défini)
- `lastChannel`, `lastTo`
- `deliveryContext` (normalisé `{ channel, to, accountId }` si disponible)
- `transcriptPath` (chemin dérivé au mieux du répertoire de stockage + sessionId)
- `messages?` (uniquement quand `messageLimit > 0`)

## sessions_history

Récupérer la transcription d'une session.

Paramètres :

- `sessionKey` (requis ; accepte la clé de session ou `sessionId` de `sessions_list`)
- `limit?: number` nombre maximum de messages (le serveur limite)
- `includeTools?: boolean` (par défaut false)

Comportement :

- `includeTools=false` filtre les messages `role: "toolResult"`.
- Retourne le tableau de messages au format de transcription brute.
- Lorsqu'un `sessionId` est donné, OpenClaw le résout à la clé de session correspondante (les ids manquants génèrent une erreur).

## sessions_send

Envoyer un message dans une autre session.

Paramètres :

- `sessionKey` (requis ; accepte la clé de session ou `sessionId` de `sessions_list`)
- `message` (requis)
- `timeoutSeconds?: number` (par défaut >0 ; 0 = fire-and-forget)

Comportement :

- `timeoutSeconds = 0` : mettre en file d'attente et retourner `{ runId, status: "accepted" }`.
- `timeoutSeconds > 0` : attendre jusqu'à N secondes pour la fin, puis retourner `{ runId, status: "ok", reply }`.
- Si l'attente expire : `{ runId, status: "timeout", error }`. L'exécution continue ; appelez `sessions_history` plus tard.
- Si l'exécution échoue : `{ runId, status: "error", error }`.
- Les exécutions d'annonce de livraison se font après la fin de l'exécution principale et sont au mieux ; `status: "ok"` ne garantit pas que l'annonce a été livrée.
- Les attentes via la passerelle `agent.wait` (côté serveur) afin que les reconnexions ne perdent pas l'attente.
- Le contexte du message agent-à-agent est injecté pour l'exécution principale.
- Les messages inter-sessions sont persistés avec `message.provenance.kind = "inter_session"` afin que les lecteurs de transcription puissent distinguer les instructions d'agent routées de l'entrée utilisateur externe.
- Après la fin de l'exécution principale, OpenClaw exécute une **boucle de réponse** :
  - Les tours 2+ alternent entre les agents demandeur et cible.
  - Répondez exactement `REPLY_SKIP` pour arrêter le ping-pong.
  - Le nombre maximum de tours est `session.agentToAgent.maxPingPongTurns` (0–5, par défaut 5).
- Une fois la boucle terminée, OpenClaw exécute l'**étape d'annonce agent-à-agent** (agent cible uniquement) :
  - Répondez exactement `ANNOUNCE_SKIP` pour rester silencieux.
  - Toute autre réponse est envoyée au canal cible.
  - L'étape d'annonce inclut la demande originale + la réponse du tour 1 + la dernière réponse ping-pong.

## Champ Canal

- Pour les groupes, `channel` est le canal enregistré sur l'entrée de session.
- Pour les chats directs, `channel` est mappé à partir de `lastChannel`.
- Pour cron/hook/node, `channel` est `internal`.
- S'il manque, `channel` est `unknown`.

## Sécurité / Politique d'Envoi

Blocage basé sur la politique par canal/type de chat (pas par id de session).

```json
{
  "session": {
    "sendPolicy": {
      "rules": [
        {
          "match": { "channel": "discord", "chatType": "group" },
          "action": "deny"
        }
      ],
      "default": "allow"
    }
  }
}
```

Remplacement à l'exécution (par entrée de session) :

- `sendPolicy: "allow" | "deny"` (non défini = hériter de la config)
- Définissable via `sessions.patch` ou `/send on|off|inherit` réservé au propriétaire (message autonome).

Points d'application :

- `chat.send` / `agent` (passerelle)
- logique de livraison de réponse automatique

## sessions_spawn

Générer une exécution de sous-agent dans une session isolée et annoncer le résultat au canal de chat du demandeur.

Paramètres :

- `task` (requis)
- `label?` (optionnel ; utilisé pour les journaux/UI)
- `agentId?` (optionnel ; générer sous un autre id d'agent si autorisé)
- `model?` (optionnel ; remplace le modèle du sous-agent ; les valeurs invalides génèrent une erreur)
- `thinking?` (optionnel ; remplace le niveau de réflexion pour l'exécution du sous-agent)
- `runTimeoutSeconds?` (par défaut `agents.defaults.subagents.runTimeoutSeconds` quand défini, sinon `0` ; quand défini, abandonne l'exécution du sous-agent après N secondes)
- `thread?` (par défaut false ; demander le routage lié au thread pour ce spawn quand supporté par le canal/plugin)
- `mode?` (`run|session` ; par défaut `run`, mais par défaut `session` quand `thread=true` ; `mode="session"` nécessite `thread=true`)
- `cleanup?` (`delete|keep`, par défaut `keep`)
- `sandbox?` (`inherit|require`, par défaut `inherit` ; `require` rejette le spawn sauf si le runtime enfant cible est en sandbox)
- `attachments?` (tableau optionnel de fichiers en ligne ; runtime de sous-agent uniquement, ACP rejette). Chaque entrée : `{ name, content, encoding?: "utf8" | "base64", mimeType? }`. Les fichiers sont matérialisés dans l'espace de travail enfant à `.openclaw/attachments/<uuid>/`. Retourne un reçu avec sha256 par fichier.
- `attachAs?` (optionnel ; `{ mountPath? }` indice réservé pour les implémentations de montage futures)

Liste blanche :

- `agents.list[].subagents.allowAgents` : liste des ids d'agent autorisés via `agentId` (`["*"]` pour autoriser n'importe lequel). Par défaut : uniquement l'agent demandeur.
- Garde d'héritage sandbox : si la session du demandeur est en sandbox, `sessions_spawn` rejette les cibles qui s'exécuteraient sans sandbox.

Découverte :

- Utilisez `agents_list` pour découvrir quels ids d'agent sont autorisés pour `sessions_spawn`.

Comportement :

- Démarre une nouvelle session `agent:<agentId>:subagent:<uuid>` avec `deliver: false`.
- Les sous-agents par défaut à l'ensemble complet d'outils **moins les outils de session** (configurable via `tools.subagents.tools`).
- Les sous-agents ne sont pas autorisés à appeler `sessions_spawn` (pas de spawning sous-agent → sous-agent).
- Toujours non-bloquant : retourne `{ status: "accepted", runId, childSessionKey }` immédiatement.
- Avec `thread=true`, les plugins de canal peuvent lier la livraison/routage à une cible de thread (le support Discord est contrôlé par `session.threadBindings.*` et `channels.discord.threadBindings.*`).
- Après la fin, OpenClaw exécute une **étape d'annonce de sous-agent** et poste le résultat au canal de chat du demandeur.
  - Si la réponse finale de l'assistant est vide, le dernier `toolResult` de l'historique du sous-agent est inclus comme `Result`.
- Répondez exactement `ANNOUNCE_SKIP` pendant l'étape d'annonce pour rester silencieux.
- Les réponses d'annonce sont normalisées à `Status`/`Result`/`Notes` ; `Status` provient du résultat d'exécution (pas du texte du modèle).
- Les sessions de sous-agent sont auto-archivées après `agents.defaults.subagents.archiveAfterMinutes` (par défaut : 60).
- Les réponses d'annonce incluent une ligne de statistiques (runtime, tokens, sessionKey/sessionId, chemin de transcription et coût optionnel).

## Visibilité de Session en Sandbox

Les outils de session peuvent être limités pour réduire l'accès entre sessions.

Comportement par défaut :

- `tools.sessions.visibility` par défaut à `tree` (session actuelle + sessions de sous-agent générées).
- Pour les sessions en sandbox, `agents.defaults.sandbox.sessionToolsVisibility` peut limiter fortement la visibilité.

Config :

```json5
{
  tools: {
    sessions: {
      // "self" | "tree" | "agent" | "all"
      // default: "tree"
      visibility: "tree",
    },
  },
  agents: {
    defaults: {
      sandbox: {
        // default: "spawned"
        sessionToolsVisibility: "spawned", // or "all"
      },
    },
  },
}
```

Notes :

- `self` : uniquement la clé de session actuelle.
- `tree` : session actuelle + sessions générées par la session actuelle.
- `agent` : toute session appartenant à l'id d'agent actuel.
- `all` : toute session (l'accès entre agents nécessite toujours `tools.agentToAgent`).
- Quand une session est en sandbox et `sessionToolsVisibility="spawned"`, OpenClaw limite la visibilité à `tree` même si vous définissez `tools.sessions.visibility="all"`.
